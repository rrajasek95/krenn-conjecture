#!/usr/bin/env python3
"""Generate an exact incidence-pivot quotient for representative 1."""

from __future__ import annotations

import hashlib
import itertools
import json
import os
from collections import Counter
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT_DIR = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-diagonal-incidence-gate-2026-08-25"
PARENT_META = PARENT_DIR / "gate_metadata.json"
PINS = {
    PARENT_DIR / "MANIFEST.sha256": "36e39752896a052d8bfe75af29c39c4d8c09c090afb8a9692e818a63c9a811bf",
    PARENT_META: "97342352d9162253c0c27aefdeba81f25b1265751e4c29daf706f828f4c9572e",
    PARENT_DIR / "generate_rep1.py": "5d0c0297311b729a1c2ddccb62a1ae92eb7a75a97acb7caf30d9fdb2b511c204",
}
COLORS = tuple(range(3))
FIXED = frozenset(((0, 3), (1, 6), (2, 7), (4, 5)))
VARIABLE = frozenset(((0, 4), (1, 2), (3, 5), (6, 7)))
ADDED = frozenset(((0, 6), (1, 3), (1, 7), (2, 5), (2, 6), (4, 6), (4, 7)))
ELIMINATED = (4, 6)
OUTSIDE = (4, 7)
NONFIXED = tuple(sorted(VARIABLE | ADDED))
RETAINED = tuple(edge for edge in NONFIXED if edge != ELIMINATED)
SUPPORT = FIXED | set(NONFIXED)
TINY = {"coordinate": 0, "outside": (0, 0), "x_pivot": 0, "q_kind": "y", "q_pivot": 0}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_write(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value)
    os.replace(temporary, path)


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


PM8 = tuple(sorted(matchings(tuple(range(8)))))
SUPPORTED = tuple(matching for matching in PM8 if set(matching) <= SUPPORT)
assert len(PM8) == 105 and len(SUPPORTED) == 12


def wrapped(value):
    return f"({value})" if "+" in value or ("-" in value[1:]) or value.startswith("-") else value


def product(*factors):
    if any(factor == "0" for factor in factors):
        return "0"
    factors = [wrapped(factor) for factor in factors if factor != "1"]
    return "*".join(factors) if factors else "1"


def summation(terms):
    terms = [term for term in terms if term != "0"]
    return "+".join(terms).replace("+-", "-") if terms else "0"


def difference(leading, tail):
    if tail == "0":
        return leading
    if leading == "0":
        return f"-({tail})"
    return f"{leading}-({tail})"


def parent_digest_and_census():
    records = []
    census = Counter()
    for word in itertools.product(COLORS, repeat=8):
        terms = []
        for matching in SUPPORTED:
            factors = []
            for edge in matching:
                i, j = word[edge[0]], word[edge[1]]
                if edge in FIXED:
                    if i != j:
                        break
                else:
                    factors.append(f"A{edge[0]}{edge[1]}[{i}{j}]")
            else:
                terms.append("*".join(factors) or "1")
        target = 1 if len(set(word)) == 1 else 0
        census[len(terms)] += 1
        records.append(("".join(map(str, word)), target, tuple(terms)))
    payload = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest(), dict(sorted(census.items()))


def orbit_representative(record):
    coordinate, p, q, r, kind, s = record
    candidates = []
    for permutation in itertools.permutations(COLORS):
        candidates.append((permutation[coordinate], permutation[p], permutation[q], permutation[r], kind, permutation[s]))
    return min(candidates)


def orbit_ledger():
    raw = [
        (coordinate, p, q, r, kind, s)
        for coordinate, p, q, r, s in itertools.product(COLORS, repeat=5)
        for kind in ("y", "z")
    ]
    groups = {}
    for record in raw:
        representative = orbit_representative(record)
        groups.setdefault(representative, []).append(record)
    assert len(raw) == 486 and len(groups) == 82
    assert all(representative[0] == 0 for representative in groups)
    assert sorted(map(len, groups.values())) == [3] * 2 + [6] * 80
    return raw, groups


def build_context(chart):
    coordinate = chart["coordinate"]
    x_pivot = chart["x_pivot"]
    q_kind = chart["q_kind"]
    q_pivot = chart["q_pivot"]
    solved = {(0, 6, i, x_pivot) for i in COLORS}
    if q_kind == "y":
        solved |= {(1, 3, q_pivot, i) for i in COLORS}
    else:
        solved |= {(3, 5, i, q_pivot) for i in COLORS}
    source = {
        (edge, i, j): f"a{edge[0]}{edge[1]}_{i}{j}"
        for edge in RETAINED for i, j in itertools.product(COLORS, repeat=2)
        if (edge[0], edge[1], i, j) not in solved
    }
    assert len(source) == 84
    xn = {j: f"xn{j}" for j in COLORS if j != x_pivot}
    yn = {j: f"yn{j}" for j in COLORS if not (q_kind == "y" and j == q_pivot)}
    zn = {j: f"zn{j}" for j in COLORS if not (q_kind == "z" and j == q_pivot)}
    assert len(xn) == 2 and len(yn) + len(zn) == 5

    def raw_source(edge, i, j):
        return source[edge, i, j]

    def q_y(j):
        return "1" if q_kind == "y" and j == q_pivot else yn[j]

    def q_z(j):
        return "1" if q_kind == "z" and j == q_pivot else zn[j]

    def entry(edge, i, j):
        if edge in FIXED:
            return "1" if i == j else "0"
        if edge == ELIMINATED:
            # A46=-A47*A26^T.
            return f"-({summation(product(raw_source(OUTSIDE, i, k), raw_source((2, 6), j, k)) for k in COLORS)})"
        if edge == (0, 6) and j == x_pivot:
            leading = "alpha" if i == coordinate else "0"
            tail = summation(product(raw_source((0, 6), i, k), xn[k]) for k in COLORS if k != x_pivot)
            return difference(leading, tail)
        if q_kind == "y" and edge == (1, 3) and i == q_pivot:
            leading = "beta" if j == coordinate else "0"
            tail = summation(
                [product(raw_source((1, 3), k, j), q_y(k)) for k in COLORS if k != q_pivot]
                + [product(raw_source((3, 5), j, k), q_z(k)) for k in COLORS]
            )
            return difference(leading, tail)
        if q_kind == "z" and edge == (3, 5) and j == q_pivot:
            leading = "beta" if i == coordinate else "0"
            tail = summation(
                [product(raw_source((1, 3), k, i), q_y(k)) for k in COLORS]
                + [product(raw_source((3, 5), i, k), q_z(k)) for k in COLORS if k != q_pivot]
            )
            return difference(leading, tail)
        return raw_source(edge, i, j)

    variables = list(source.values()) + list(xn.values()) + ["alpha"] + list(yn.values()) + list(zn.values()) + ["beta", "sat"]
    assert len(variables) == len(set(variables)) == 94
    return source, entry, variables


def amplitude(entry, word):
    terms = []
    for matching in SUPPORTED:
        factors = []
        for edge in matching:
            value = entry(edge, word[edge[0]], word[edge[1]])
            if value == "0":
                break
            factors.append(value)
        else:
            terms.append(product(*factors))
    return summation(terms)


def build_program(chart, ring="32003"):
    _, entry, variables = build_context(chart)
    equations = []
    for word in itertools.product(COLORS, repeat=8):
        value = amplitude(entry, word)
        equations.append(f"({value})-1" if len(set(word)) == 1 else value)
    # A06*A47^T=0 after the incidence-pivot substitution.
    for i, j in itertools.product(COLORS, repeat=2):
        equations.append(summation(product(entry((0, 6), i, k), entry(OUTSIDE, j, k)) for k in COLORS))
    # (I-A17*A26)*A47^T=0.
    for i, j in itertools.product(COLORS, repeat=2):
        correction = summation(
            product(entry((1, 7), i, k), entry((2, 6), k, ell), entry(OUTSIDE, j, ell))
            for k, ell in itertools.product(COLORS, repeat=2)
        )
        equations.append(difference(entry(OUTSIDE, j, i), correction))
    p, q = chart["outside"]
    equations.append(f"alpha*beta*{entry(OUTSIDE, p, q)}*sat-1")
    assert len(equations) == 6580
    lines = [
        "option(noredefine);",
        f"ring r={ring},({','.join(variables)}),dp;",
        "ideal I=" + ",\n".join(equations) + ";",
        'print("INPUT_GENERATORS="+string(size(I)));',
        "ideal G=slimgb(I);",
        'print("GROEBNER_SIZE="+string(size(G)));',
        "poly remainder=reduce(1,G);",
        'print("UNIT_REMAINDER="+string(remainder));',
        'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }',
        "quit;",
    ]
    return "\n".join(lines) + "\n"


def main():
    for path, expected in PINS.items():
        assert sha256(path) == expected
    parent = json.loads(PARENT_META.read_text())
    digest, census = parent_digest_and_census()
    assert digest == parent["parent_full_x5_digest"] == "61640fb492640847a58cf9f5e2f1dbc3f381736d7909325f35b2dfffb211d5eb"
    assert {str(key): value for key, value in census.items()} == {str(key): value for key, value in parent["parent_term_census"].items()}
    raw, groups = orbit_ledger()
    program = build_program(TINY)
    program_path = HERE / "rep1_pivot_i0_p00_x0_y0_p32003.sing"
    atomic_write(program_path, program)
    representatives = [list(item) for item in sorted(groups)]
    metadata = {
        "schema": "KRENN_X5_REP1_INCIDENCE_PIVOT_QUOTIENT_V1",
        "status": "PASS_EXACT_CONTRACTION_DESIGN",
        "parent_manifest_sha256": PINS[PARENT_DIR / "MANIFEST.sha256"],
        "parent_full_x5_digest": digest,
        "parent_term_census": census,
        "source_orientation": {
            "elimination": "A46=-A47*A26^T",
            "guard": ["A06*A47^T=0", "(I-A17*A26)*A47^T=0"],
            "carrier": "A06^T*K*[A13^T|A35]",
            "left_incidence": "A06*x=e_i",
            "partner_incidence": "A13^T*y+A35*z=e_i",
            "y_pivot_solves": "row s of A13",
            "z_pivot_solves": "column s of A35",
        },
        "equivalence": {
            "forward": "on x_r,q_s,A47[pq] nonzero set xnorm=x/x_r, alpha=1/x_r, qnorm=q/q_s, beta=1/q_s; solve the three A06 pivot-column and three A13-row/A35-column entries",
            "reverse": "from alpha*beta*A47[pq] nonzero set x=xnorm/alpha and q=qnorm/beta; substituted entries give A06*x=e_i and A13^T*y+A35*z=e_i",
            "combined_saturation": "alpha*beta*A47[pq]*sat-1",
            "chart_union_complete": True,
        },
        "chart_census": {
            "raw_charts": len(raw),
            "s3_orbits": len(groups),
            "orbits_by_partner_kind": {kind: sum(1 for item in groups if item[4] == kind) for kind in ("y", "z")},
            "orbit_size_census": dict(Counter(map(len, groups.values()))),
            "representatives": representatives,
        },
        "counts": {
            "parent_variables": 100,
            "quotient_variables": 94,
            "variables_removed": 6,
            "parent_generators": 6586,
            "quotient_generators": 6580,
            "generators_removed": 6,
            "solved_block_entries": 6,
            "explicit_incidence_equations": 0,
        },
        "tiny_diagnostic": {
            "chart": TINY,
            "input": program_path.name,
            "input_sha256": hashlib.sha256(program.encode()).hexdigest(),
            "ring": "p32003",
            "native_wall_seconds": 15,
            "rss_cap_bytes": 4 * 1024**3,
            "mathematical_scope": "diagnostic only",
        },
        "scope": {"representative_1_only": True, "rep1_closed": False, "broad_run": False, "D12_reads": False},
    }
    atomic_write(HERE / "quotient_metadata.json", json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": metadata["status"], "variables": 94, "generators": 6580, "chart_orbits": 82}, sort_keys=True))


if __name__ == "__main__":
    main()
