#!/usr/bin/env python3
"""Optional SymPy search; acceptance uses only verify.py and the saved DAG.

Instrument the installed SymPy Buchberger implementation to retain exact
ideal-membership arithmetic. The replay does not trust its pair-selection
criteria, its claim to be a Groebner basis, or this generator.
"""

from itertools import combinations
from pathlib import Path
import inspect
import json
import sympy
from sympy.polys import groebnertools
from sympy.polys.domains import QQ
from sympy.polys.rings import ring

HERE = Path(__file__).resolve().parent
R, *xs = ring("x:12", QQ, order="grevlex")
pairs = [e for e in combinations(range(6), 2) if e not in ((0, 1), (2, 3), (4, 5))]
D = [[R.zero for _ in range(6)] for _ in range(6)]
for (p, q), x in zip(pairs, xs):
    D[p][q] = D[q][p] = x
for p, q in ((0, 1), (2, 3), (4, 5)):
    D[p][q] = D[q][p] = R.one
C = [[R.zero for _ in range(6)] for _ in range(6)]
for i, j in combinations(range(6), 2):
    p, q, r, t = [k for k in range(6) if k not in (i, j)]
    C[i][j] = C[j][i] = D[p][q]*D[r][t]+D[p][r]*D[q][t]+D[p][t]*D[q][r]
equations, positions = [], []
for p in range(6):
    for q in range(6):
        f = sum((D[p][r]*C[r][q] for r in range(6)), R.zero)
        if f and f not in equations:
            equations.append(f)
            positions.append((p, q))

nodes, ids = [], {}


def register(polynomial, record):
    if polynomial not in ids:
        ids[polynomial] = len(nodes)
        nodes.append(record)
    return polynomial


for f, position in zip(equations, positions):
    register(f, dict(input_position=position))


def tracked_rem(p, divisors):
    quotients, remainder = p.div(divisors)
    if remainder:
        terms = [(ids[p], R.one)]
        terms.extend((ids[f], -q) for f, q in zip(divisors, quotients) if q)
        register(remainder, dict(terms=terms))
    return remainder


def tracked_monic(p):
    h = p.monic()
    return register(h, dict(terms=[(ids[p], R.ground_new(1/p.LC))]))


def tracked_spoly(f, g, domain):
    h = groebnertools.spoly(f, g, domain)
    if h:
        lm = R.monomial_lcm(f.LM, g.LM)
        a = R.term_new(R.monomial_div(lm, f.LM), QQ.one)
        b = R.term_new(R.monomial_div(lm, g.LM), -QQ.one)
        if a*f+b*g != h:
            raise ValueError("Unexpected installed SymPy S-polynomial convention")
        register(h, dict(terms=[(ids[f], a), (ids[g], b)]))
    return h


source = inspect.getsource(groebnertools._buchberger)
replacements = {
    "g.rem([ f[j] for j in J ])": "tracked_rem(g, [f[j] for j in J])",
    "p.rem(f[:i])": "tracked_rem(p, f[:i])",
    "h.monic()": "tracked_monic(h)",
    "r.monic()": "tracked_monic(r)",
}
for old, new in replacements.items():
    if source.count(old) != 1:
        raise ValueError("Unsupported SymPy implementation: " + old)
    source = source.replace(old, new)
scope = dict(spoly=tracked_spoly, tracked_rem=tracked_rem, tracked_monic=tracked_monic)
exec(compile(source, "<instrumented-installed-SymPy>", "exec"), scope)
basis = scope["_buchberger"](equations[:], R)
if basis != [R.one]:
    raise ValueError("Search did not produce the unit ideal")

last = ids[R.one]
needed = set()


def visit(i):
    if i in needed:
        return
    needed.add(i)
    for j, _ in nodes[i].get("terms", []):
        visit(j)


visit(last)
ordered = sorted(needed)
new_ids = {old: new for new, old in enumerate(ordered)}


def serialize(poly):
    return [[list(monomial), str(coefficient)] for monomial, coefficient in sorted(poly.items())]


output_nodes = []
for i in ordered:
    record = nodes[i]
    if "input_position" in record:
        output_nodes.append(record)
    else:
        output_nodes.append(dict(terms=[[new_ids[j], serialize(q)] for j, q in record["terms"]]))
receipt = dict(
    description="Exact ideal-membership derivation of 1 from D C = 0 with D01=D23=D45=1",
    variables=[list(e) for e in pairs],
    normalized_matching=[[0, 1], [2, 3], [4, 5]],
    nodes=output_nodes,
    final_node=new_ids[last],
    generator_sympy_version=sympy.__version__)
(HERE / "scalar-matching-certificate.json").write_text(json.dumps(receipt, separators=(",", ":"))+"\n")
print(f"Generated {len(output_nodes)} retained arithmetic nodes from {len(nodes)} search nodes.")
