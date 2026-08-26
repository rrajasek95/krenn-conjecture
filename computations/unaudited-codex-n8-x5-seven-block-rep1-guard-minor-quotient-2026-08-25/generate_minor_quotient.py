#!/usr/bin/env python3
"""Generate the exact guard+incidence minor quotient for representative 1."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import os
from collections import Counter
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE_DIR = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-incidence-pivot-quotient-2026-08-25"
OBLIGATION = ROOT / "computations/unaudited-codex-n8-x5-seven-block-guard-dual-gate-2026-08-25/results_full_family_obligation.json"
PINS = {
    BASE_DIR / "MANIFEST.sha256": "87bf2d17fcd4c5b8d52ba74c3cca8ecf5a19be2878df1fc2a86c70e05e7773cc",
    BASE_DIR / "generate_quotient.py": "03993104d59aecf887cecbc9ea6f1c5e2703a5449933961d73520c53cb7ae68b",
    BASE_DIR / "rep1_pivot_i0_p00_x0_y0_p32003.sing": "b54e527887fd9fe250d24f21d932f6f25a0ddb6d38e36c03328d2c1ca91d02e3",
    OBLIGATION: "22b471512c6ac6a6ff86bb65fbd4f1fec094208a1c99d338865dfee89c0cb3a0",
}
TINY = {"coordinate": 0, "outside": (0, 0), "x_pivot": 0, "q_kind": "y", "q_pivot": 0, "minor_pair": (0, 1)}


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


def load_base():
    specification = importlib.util.spec_from_file_location("sealed_rep1_pivot_quotient", BASE_DIR / "generate_quotient.py")
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def orbit_representative(record):
    coordinate, p, q, r, kind, s, a, b = record
    candidates = []
    for permutation in itertools.permutations(range(3)):
        aa, bb = sorted((permutation[a], permutation[b]))
        candidates.append((permutation[coordinate], permutation[p], permutation[q], permutation[r], kind, permutation[s], aa, bb))
    return min(candidates)


def orbit_ledger():
    raw = []
    for coordinate, p, q, r, s in itertools.product(range(3), repeat=5):
        for kind in ("y", "z"):
            for other in range(3):
                if other != q:
                    a, b = sorted((q, other))
                    raw.append((coordinate, p, q, r, kind, s, a, b))
    groups = {}
    for record in raw:
        groups.setdefault(orbit_representative(record), []).append(record)
    assert len(raw) == 972 and len(groups) == 162
    assert set(map(len, groups.values())) == {6}
    return raw, groups


def build_context(base, chart):
    coordinate = chart["coordinate"]
    p, _ = chart["outside"]
    r = chart["x_pivot"]
    kind = chart["q_kind"]
    s = chart["q_pivot"]
    a, b = chart["minor_pair"]
    assert p in range(3) and a < b and chart["outside"][1] in (a, b)
    c = next(item for item in range(3) if item not in (a, b))
    solved = {(0, 6, i, j) for i, j in itertools.product(range(3), repeat=2)}
    if kind == "y":
        solved |= {(1, 3, s, i) for i in range(3)}
    else:
        solved |= {(3, 5, i, s) for i in range(3)}
    source = {
        (edge, i, j): f"a{edge[0]}{edge[1]}_{i}{j}"
        for edge in base.RETAINED for i, j in itertools.product(range(3), repeat=2)
        if (edge[0], edge[1], i, j) not in solved
    }
    assert len(source) == 78
    xn = {j: f"xn{j}" for j in range(3) if j != r}
    yn = {j: f"yn{j}" for j in range(3) if not (kind == "y" and j == s)}
    zn = {j: f"zn{j}" for j in range(3) if not (kind == "z" and j == s)}
    t = {i: f"t{i}" for i in range(3)}

    def raw(edge, i, j):
        return source[edge, i, j]

    def w(j):
        return "1" if j == r else xn[j]

    def qy(j):
        return "1" if kind == "y" and j == s else yn[j]

    def qz(j):
        return "1" if kind == "z" and j == s else zn[j]

    def v(j):
        return raw(base.OUTSIDE, p, j)

    determinant = base.difference(base.product(w(a), v(b)), base.product(w(b), v(a)))

    def entry(edge, i, j):
        if edge in base.FIXED:
            return "1" if i == j else "0"
        if edge == base.ELIMINATED:
            return f"-({base.summation(base.product(raw(base.OUTSIDE, i, k), raw((2, 6), j, k)) for k in range(3))})"
        if edge == (0, 6):
            reduced_rhs = base.difference("abar" if i == coordinate else "0", base.product(t[i], w(c)))
            if j == a:
                return base.summation((base.product(reduced_rhs, v(b)), base.product(w(b), t[i], v(c))))
            if j == b:
                return f"-({base.summation((base.product(w(a), t[i], v(c)), base.product(reduced_rhs, v(a))))})"
            assert j == c
            return base.product(determinant, t[i])
        if kind == "y" and edge == (1, 3) and i == s:
            leading = "beta" if j == coordinate else "0"
            tail = base.summation(
                [base.product(raw((1, 3), k, j), qy(k)) for k in range(3) if k != s]
                + [base.product(raw((3, 5), j, k), qz(k)) for k in range(3)]
            )
            return base.difference(leading, tail)
        if kind == "z" and edge == (3, 5) and j == s:
            leading = "beta" if i == coordinate else "0"
            tail = base.summation(
                [base.product(raw((1, 3), k, i), qy(k)) for k in range(3)]
                + [base.product(raw((3, 5), i, k), qz(k)) for k in range(3) if k != s]
            )
            return base.difference(leading, tail)
        return raw(edge, i, j)

    variables = list(source.values()) + list(xn.values()) + ["abar"] + list(yn.values()) + list(zn.values()) + ["beta"] + list(t.values()) + ["sat"]
    assert len(variables) == len(set(variables)) == 91
    return entry, variables, determinant


def amplitude(base, entry, word):
    terms = []
    for matching in base.SUPPORTED:
        factors = []
        for edge in matching:
            value = entry(edge, word[edge[0]], word[edge[1]])
            if value == "0":
                break
            factors.append(value)
        else:
            terms.append(base.product(*factors))
    return base.summation(terms)


def build_program(base, chart, ring="32003"):
    entry, variables, determinant = build_context(base, chart)
    equations = []
    for word in itertools.product(range(3), repeat=8):
        value = amplitude(base, entry, word)
        equations.append(f"({value})-1" if len(set(word)) == 1 else value)
    p, q = chart["outside"]
    # The response row p, A06*row_p(A47)^T, is tautological by construction.
    for i, j in itertools.product(range(3), repeat=2):
        if j != p:
            equations.append(base.summation(base.product(entry((0, 6), i, k), entry(base.OUTSIDE, j, k)) for k in range(3)))
    for i, j in itertools.product(range(3), repeat=2):
        correction = base.summation(
            base.product(entry((1, 7), i, k), entry((2, 6), k, ell), entry(base.OUTSIDE, j, ell))
            for k, ell in itertools.product(range(3), repeat=2)
        )
        equations.append(base.difference(entry(base.OUTSIDE, j, i), correction))
    equations.append(base.product("abar", "beta", entry(base.OUTSIDE, p, q), determinant, "sat") + "-1")
    assert len(equations) == 6577
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
    base = load_base()
    assert hashlib.sha256(base.build_program(base.TINY).encode()).hexdigest() == PINS[BASE_DIR / "rep1_pivot_i0_p00_x0_y0_p32003.sing"]
    raw, groups = orbit_ledger()
    all_equal = {
        orbit_representative((0, 0, 0, 0, "y", 0, *sorted((0, other))))
        for other in (1, 2)
    }
    assert len(all_equal) == 1
    obligations = json.loads(OBLIGATION.read_text())["six_full_family_representatives"][1]
    stars = obligations["two_sandwich_stars"]
    assert len(stars) == 10
    selected = next(item for item in stars if item["factorization_up_to_output_permutation"] == "A06^T*K*[A13^T|A35]")
    alternative_a06 = next(item for item in stars if item["factorization_up_to_output_permutation"] == "A06^T*K*[A45|A47]")
    assert selected["cap"] == "03" and selected["star_center"] == 4
    assert alternative_a06["cap"] == "04" and alternative_a06["star_center"] == 3
    assert "A45" in alternative_a06["Q"]
    program = build_program(base, TINY)
    source = HERE / "rep1_minor_i0_p00_x0_y0_d01_p32003.sing"
    atomic_write(source, program)
    metadata = {
        "schema": "KRENN_X5_REP1_GUARD_MINOR_QUOTIENT_V1",
        "status": "PASS_STRICTLY_SMALLER_EXACT_QUOTIENT_DESIGN",
        "antecedent_manifest_sha256": PINS[BASE_DIR / "MANIFEST.sha256"],
        "exact_reduction": {
            "guard_vector": "v=row_p(A47), with v_q=A47[pq] nonzero",
            "normalized_witness": "w=x/x_r, with w_r=1 and A06*w=alpha*e_i",
            "independence": "A06*v=0 and alpha nonzero imply w and v are linearly independent",
            "minor_cover": "because v_q nonzero, at least one d(q,t)=w_q*v_t-w_t*v_q for t!=q is nonzero",
            "parameterization": "choose d=d(a,b), set alpha=d*abar and the remaining A06 column c=d*t; Cramer formulas solve the other two A06 columns polynomially",
            "reverse": "divide alpha by d and recover the original witness x=w/(d*abar); all nine A06 entries satisfy the original incidence and guard-row-p equations",
            "combined_saturation": "abar*beta*A47[pq]*d*sat-1"
        },
        "chart_census": {
            "raw_refined_charts": len(raw),
            "s3_orbits": len(groups),
            "orbits_by_partner_kind": {kind: sum(1 for item in groups if item[4] == kind) for kind in ("y", "z")},
            "orbit_size_census": dict(Counter(map(len, groups.values()))),
            "all_equal_y_minor_orbits": len(all_equal),
            "complete": True
        },
        "counts": {
            "original_incidence_variables": 100,
            "first_quotient_variables": 94,
            "minor_quotient_variables": 91,
            "original_incidence_generators": 6586,
            "first_quotient_generators": 6580,
            "minor_quotient_generators": 6577,
            "A06_entries_solved": 9,
            "partner_entries_solved": 3,
            "tautological_guard_equations_removed": 3
        },
        "alternate_carrier_audit": {
            "frozen_two_sandwich_stars": 10,
            "selected": selected["factorization_up_to_output_permutation"],
            "only_other_common_A06": alternative_a06["factorization_up_to_output_permutation"],
            "why_not_stronger": "its Q contains fixed A45=I, hence Q is full and it does not exclude any e_i already in P=Col(A06)",
            "scope": "no stronger automatic proof among the ten frozen two-sandwich stars; not a no-go for other carrier types"
        },
        "materialized_input": {"chart": TINY, "path": source.name, "sha256": hashlib.sha256(program.encode()).hexdigest(), "ring": "p32003"},
        "scope": {"design_only": True, "launches": 0, "rep1_closed": False, "D12_reads": False}
    }
    atomic_write(HERE / "minor_quotient_metadata.json", json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": metadata["status"], "variables": 91, "generators": 6577, "orbits": 162}, sort_keys=True))


if __name__ == "__main__":
    main()
