#!/usr/bin/env python3
"""Exact ideals for repeated supports in the three-singleton pure profile.

This explorer keeps arbitrary 3x3 endpoint-ordered blocks of q.  It checks
the two support types (P,P,Q), P != Q, by substituting the complete linear
kernel of qF=0 into every coefficient of q^[2]-F.  The all-equal support is
retained as the known K4-positive branch and is checked by a direct witness.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import shutil
import subprocess
import tempfile


U = tuple(range(6))
COLOURS = tuple(range(3))
EDGES = tuple(combinations(U, 2))
EDGE_INDEX = {e: i for i, e in enumerate(EDGES)}
NQ = 15 * 9


def q_index(pair, cu, cv):
    return 9 * EDGE_INDEX[pair] + 3 * cu + cv


def qf_rows(terms):
    rows = {}
    for colour, pair, weight in terms:
        u, v = pair
        for cu, cv in product(COLOURS, repeat=2):
            word = [colour] * 6
            word[u], word[v] = cu, cv
            row = rows.setdefault(tuple(word), {})
            col = q_index(pair, cu, cv)
            row[col] = row.get(col, Fraction(0)) + Fraction(weight)
    return tuple(row for row in rows.values() if row)


def sparse_rref(source_rows):
    pivots = {}
    for source in source_rows:
        row = {c: Fraction(x) for c, x in source.items() if x}
        for c in sorted(pivots):
            if c not in row:
                continue
            scale = row[c]
            for k, x in pivots[c].items():
                row[k] = row.get(k, Fraction(0)) - scale * x
                if not row[k]:
                    del row[k]
        if not row:
            continue
        c = min(row)
        scale = row[c]
        row = {k: x / scale for k, x in row.items()}
        for old in pivots.values():
            if c not in old:
                continue
            scale = old[c]
            for k, x in row.items():
                old[k] = old.get(k, Fraction(0)) - scale * x
                if not old[k]:
                    del old[k]
        pivots[c] = row
        pivots = dict(sorted(pivots.items()))
    return pivots


def linear_expression(pieces):
    out = []
    for name, x in pieces:
        if not x:
            continue
        if x == 1:
            out.append(name)
        elif x == -1:
            out.append(f"-({name})")
        elif x.denominator == 1:
            out.append(f"({x.numerator})*({name})")
        else:
            out.append(f"({x.numerator}/{x.denominator})*({name})")
    return "0" if not out else "(" + ")+(".join(out) + ")"


def parameterize(terms):
    pivots = sparse_rref(qf_rows(terms))
    free = tuple(c for c in range(NQ) if c not in pivots)
    variables = tuple(f"t{i}" for i in range(len(free)))
    by_col = [[] for _ in range(NQ)]
    for name, c in zip(variables, free):
        by_col[c].append((name, Fraction(1)))
        for pivot, row in pivots.items():
            if c in row:
                by_col[pivot].append((name, -row[c]))
    values = {}
    for pair in EDGES:
        for cu, cv in product(COLOURS, repeat=2):
            c = q_index(pair, cu, cv)
            values[pair, cu, cv] = linear_expression(by_col[c])
    return variables, values, len(pivots)


def add(*xs):
    xs = tuple(x for x in xs if x != "0")
    return "0" if not xs else "(" + ")+(".join(xs) + ")"


def mul(x, y):
    return "0" if x == "0" or y == "0" else f"({x})*({y})"


def cell(values, u, v, cu, cv):
    if u < v:
        return values[(u, v), cu, cv]
    return values[(v, u), cv, cu]


def equations(terms):
    variables, values, rank = parameterize(terms)
    target = Counter()
    for colour, pair, weight in terms:
        sites = tuple(u for u in U if u not in pair)
        target[sites, (colour,) * 4] += weight
    pairings = ((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2))
    generators = []
    for sites in combinations(U, 4):
        for colours in product(COLOURS, repeat=4):
            poly = add(*(
                mul(
                    cell(values, sites[a], sites[b], colours[a], colours[b]),
                    cell(values, sites[c], sites[d], colours[c], colours[d]),
                )
                for a, b, c, d in pairings
            ))
            constant = target[sites, colours]
            if constant:
                poly = add(poly, str(-constant))
            if poly != "0":
                generators.append(poly)
    return variables, tuple(generators), rank


def run_singular(terms, timeout):
    singular = shutil.which("Singular")
    if singular is None:
        raise RuntimeError("Singular not found")
    variables, generators, rank = equations(terms)
    program = (
        f"ring r=0,({','.join(variables)}),dp;\n"
        f"ideal I={','.join(generators)};\n"
        "ideal G=slimgb(I);\n"
        'if ((size(G)==1) && (string(G[1])=="1")) '
        '{ print("UNIT"); } else { print("NONUNIT"); print(size(G)); }\n'
        "exit;\n"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as handle:
        handle.write(program)
        path = handle.name
    result = subprocess.run(
        [singular, "-q", path], capture_output=True, text=True, timeout=timeout
    )
    return rank, len(variables), len(generators), result.stdout.strip()


def audit_k4_witness():
    # Missing pair 45; the three one-factors of K4 on 0123.
    coloured_edges = {
        0: ((0, 1), (2, 3)),
        1: ((0, 2), (1, 3)),
        2: ((0, 3), (1, 2)),
    }
    # Every cross-colour pair of edges intersects, and each colour has one
    # disjoint pair.  This is exactly q^[2]=sum E_c(45), q^[3]=0.
    for c in COLOURS:
        assert not set(coloured_edges[c][0]) & set(coloured_edges[c][1])
    for c, d in combinations(COLOURS, 2):
        assert all(set(e) & set(f) for e in coloured_edges[c] for f in coloured_edges[d])
    assert all(4 not in e and 5 not in e for es in coloured_edges.values() for e in es)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args()
    audit_k4_witness()
    cases = {
        "adjacent": ((0, (0, 1), 1), (1, (0, 1), 1), (2, (0, 2), 1)),
        "disjoint": ((0, (0, 1), 1), (1, (0, 1), 1), (2, (2, 3), 1)),
    }
    print("all-equal repeated support: exact K4 witness PASS")
    for name, terms in cases.items():
        rank, nullity, ngen, verdict = run_singular(terms, args.timeout)
        print(name, "qF rank/nullity", rank, nullity, "generators", ngen, verdict)


if __name__ == "__main__":
    main()
