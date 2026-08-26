#!/usr/bin/env python3
"""Adjugate cancellation and partner-rank design inside rank(A07)=3; no solve."""
from __future__ import annotations

import collections
import copy
import hashlib
import itertools
import json
import os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT = ROOT / "computations/unaudited-codex-n8-x5-anchor-no-rectangle-design-2026-08-25"
PINS = {
    PARENT / "MANIFEST.sha256": "4a15e9a2dd807b21169ca57b5e2aa7925db60bff804a1afc4227f2fd34822d75",
    PARENT / "audit_anchor_no_rectangle.py": "33b81ce551b1c88e5dac65b4b07878a13ed259b75a6efa14424678852d87f4b1",
    PARENT / "results_anchor_no_rectangle_design.json": "237fd1c51283174f579ce68574a8b30d26fbb9673a76f2ab363ea613927cd274",
    PARENT / "canonical_reduced_full_x5_Q.sing": "25b25aac93a336c36c0299c5d6ee9b2a984b5ca0e644170ef235af92f01124f3",
}
COLORS = tuple(range(3))
S3 = tuple(itertools.permutations(COLORS))
RETAINED_BLOCKS = ("04", "06", "07", "13", "14", "17", "35")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def poly_add(target, coefficient, monomial):
    monomial = tuple(sorted(monomial))
    target[monomial] += coefficient
    if target[monomial] == 0:
        del target[monomial]


def det_poly():
    answer = collections.Counter()
    for permutation in S3:
        inversions = sum(permutation[i] > permutation[j] for i in COLORS for j in range(i + 1, 3))
        poly_add(answer, -1 if inversions % 2 else 1, tuple((i, permutation[i]) for i in COLORS))
    return answer


def adj_poly(i, j):
    rows = [value for value in COLORS if value != j]
    columns = [value for value in COLORS if value != i]
    answer = collections.Counter()
    sign = -1 if (i + j) % 2 else 1
    poly_add(answer, sign, ((rows[0], columns[0]), (rows[1], columns[1])))
    poly_add(answer, -sign, ((rows[0], columns[1]), (rows[1], columns[0])))
    return answer


def multiply_entry_poly(left, atom):
    answer = collections.Counter()
    for monomial, coefficient in left.items():
        poly_add(answer, coefficient, monomial + (atom,))
    return answer


def adjugate_replay():
    determinant = det_poly()
    checks = []
    for side in ("adj_times_A", "A_times_adj"):
        for i, j in itertools.product(COLORS, repeat=2):
            value = collections.Counter()
            for k in COLORS:
                adjugate = adj_poly(i, k) if side == "adj_times_A" else adj_poly(k, j)
                atom = (k, j) if side == "adj_times_A" else (i, k)
                value.update(multiply_entry_poly(adjugate, atom))
            value = collections.Counter({m: c for m, c in value.items() if c})
            assert value == (determinant if i == j else collections.Counter())
            checks.append([side, i, j])
    return checks


def wrapped(value):
    return f"({value})" if "+" in value or ("-" in value[1:]) or value.startswith("-") else value


def product(*values):
    if any(value == "0" for value in values):
        return "0"
    values = [wrapped(value) for value in values if value != "1"]
    return "*".join(values) if values else "1"


def summation(values):
    values = [value for value in values if value != "0"]
    return "+".join(values).replace("+-", "-") if values else "0"


def difference(left, right):
    if right == "0":
        return left
    if left == "0":
        return f"-({right})"
    return f"{left}-({right})"


def variable_entry(block, row, column):
    return f"a{block}_{row}{column}"


def rank1_entry(block, row, column, axis=0):
    if block in RETAINED_BLOCKS:
        return variable_entry(block, row, column)
    assert block in ("25", "26")
    return f"v{block}_{column}" if row == axis else "0"


def det3(block):
    terms = []
    for permutation in S3:
        inversions = sum(permutation[i] > permutation[j] for i in COLORS for j in range(i + 1, 3))
        term = product(*(variable_entry(block, i, permutation[i]) for i in COLORS))
        terms.append(term if inversions % 2 == 0 else f"-({term})")
    return summation(terms)


def amplitude_with_entry(word, E):
    a, b, c, d, e, f, g, h = word
    R = summation(["1" if a == d and e == f else "0", product(E("04", a, e), E("35", d, f))])
    S = summation(["1" if b == g and c == h else "0", product(E("17", b, h), E("26", c, g))])
    T = summation([E("13", b, d) if e == f else "0", product(E("14", b, e), E("35", d, f))])
    U = summation([E("06", a, g) if c == h else "0", product(E("07", a, h), E("26", c, g))])
    return summation([product(R, S), product(T, U)])


def amplitude(word):
    return amplitude_with_entry(word, rank1_entry)


def rank2_entry(block, row, column, axis=0, pivot_color=1):
    if block in RETAINED_BLOCKS:
        return variable_entry(block, row, column)
    assert block in ("25", "26")
    x, y = f"x{block}_{column}", f"y{block}_{column}"
    remaining = next(value for value in COLORS if value not in (axis, pivot_color))
    if row == axis:
        return x
    if row == pivot_color:
        return y
    assert row == remaining
    return product("t", y)


def rank2_generator_census():
    raw = []
    for word in itertools.product(COLORS, repeat=8):
        value = amplitude_with_entry(word, rank2_entry)
        target = "1" if len(set(word)) == 1 else "0"
        raw.append(difference(value, target))
    distinct = list(dict.fromkeys(value for value in raw if value != "0"))
    # A07 determinant and one nonzero 2-minor of the 6x2 coefficient matrix.
    saturations = 2
    return {
        "raw_full_x5_words": len(raw),
        "tautological_zero_words": raw.count("0"),
        "distinct_nonzero_full_x5_generators": len(distinct),
        "saturations": saturations,
        "generators": len(distinct) + saturations,
    }


def build_rank1_program():
    matrix_variables = [
        variable_entry(block, i, j)
        for block in RETAINED_BLOCKS
        for i, j in itertools.product(COLORS, repeat=2)
    ]
    partner_variables = [f"v{block}_{j}" for block in ("25", "26") for j in COLORS]
    variables = matrix_variables + partner_variables + ["u07", "sv"]
    assert len(matrix_variables) == 63 and len(partner_variables) == 6
    assert len(variables) == len(set(variables)) == 71
    raw_equations = []
    amplitude_digest = hashlib.sha256()
    for word in itertools.product(COLORS, repeat=8):
        value = amplitude(word)
        target = "1" if len(set(word)) == 1 else "0"
        equation = difference(value, target)
        raw_equations.append(equation)
        amplitude_digest.update(("".join(map(str, word)) + ":" + equation + "\n").encode())
    # Rank-one support makes many word equations tautological or literally
    # identical.  Removing zeros and repeats is exact ideal equality.
    equations = list(dict.fromkeys(value for value in raw_equations if value != "0"))
    assert len(raw_equations) == 6561 and raw_equations.count("0") == 2916
    assert len(equations) == 2918
    equations.extend([difference(product("u07", det3("07")), "1"), difference(product("sv", "v25_0"), "1")])
    assert len(equations) == len(set(equations)) == 2920
    assert all(value not in ("0", "1", "-1") for value in equations)
    program = "\n".join([
        "// DESIGN INPUT ONLY: no ideal run authorized.",
        "option(noredefine);",
        f"ring r=0,({','.join(variables)}),dp;",
        "ideal I=" + ",\n".join(equations) + ";",
        'print("INPUT_VARIABLES="+string(nvars(r)));',
        'print("INPUT_GENERATORS="+string(size(I)));',
        "quit;",
        "",
    ])
    assert "slimgb" not in program and "std(" not in program and "groebner" not in program.lower()
    path = HERE / "rankA07_3_partner_rank1_axis0_v25c0_Q.sing"
    temporary = path.with_suffix(".sing.tmp")
    temporary.write_text(program)
    os.replace(temporary, path)
    return {
        "path": path.name,
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
        "variables": 71,
        "generators": 2920,
        "raw_full_x5_words": 6561,
        "tautological_zero_words": 2916,
        "distinct_nonzero_full_x5_generators": 2918,
        "amplitude_ledger_sha256": amplitude_digest.hexdigest(),
        "solver_commands": 0,
    }


def orbit_census_rank1():
    charts = tuple((axis, block, column) for axis in COLORS for block in (25, 26) for column in COLORS)
    def action(chart, color):
        axis, block, column = chart
        return color[axis], block, color[column]
    remaining = set(charts)
    orbits = []
    while remaining:
        representative = min(remaining)
        orbit = {action(representative, color) for color in S3}
        remaining -= orbit
        orbits.append({"representative": list(representative), "size": len(orbit)})
    assert len(charts) == 18 and len(orbits) == 4
    return {"raw_charts": 18, "S3_orbits": 4, "orbit_ledger": orbits}


def orbit_census_rank2():
    partner_rows = tuple((block, column) for block in (25, 26) for column in COLORS)
    charts = tuple(
        (axis, pivot_color, minor)
        for axis in COLORS
        for pivot_color in COLORS if pivot_color != axis
        for minor in itertools.combinations(partner_rows, 2)
    )
    def action(chart, color):
        axis, pivot_color, minor = chart
        mapped_minor = tuple(sorted((block, color[column]) for block, column in minor))
        return color[axis], color[pivot_color], mapped_minor
    remaining = set(charts)
    orbits = []
    while remaining:
        representative = min(remaining)
        orbit = {action(representative, color) for color in S3}
        remaining -= orbit
        orbits.append({
            "representative": [representative[0], representative[1], [list(value) for value in representative[2]]],
            "size": len(orbit),
        })
    assert len(charts) == 90
    return {"raw_charts": 90, "S3_orbits": len(orbits), "orbit_ledger": orbits}


def orbit_census_rank3():
    partner_rows = tuple((block, column) for block in (25, 26) for column in COLORS)
    charts = tuple(itertools.combinations(partner_rows, 3))
    def action(chart, color):
        return tuple(sorted((block, color[column]) for block, column in chart))
    remaining = set(charts)
    orbits = []
    while remaining:
        representative = min(remaining)
        orbit = {action(representative, color) for color in S3}
        remaining -= orbit
        orbits.append({"representative": [list(value) for value in representative], "size": len(orbit)})
    assert len(charts) == 20
    return {"raw_charts": 20, "S3_orbits": len(orbits), "orbit_ledger": orbits}


def validate(result):
    assert result["schema"] == "KRENN_X5_ANCHOR_RANK3_ADJUGATE_PARTNER_DESIGN_V1"
    assert result["status"] == "PASS_EXACT_PARTNER_RANK_STRATIFICATION_ONE_SMALLER_INPUT_NO_SOLVE"
    assert result["adjugate_cancellation"]["matrix_entries_replayed"] == 18
    assert result["branches"]["partner_rank0"]["status"] == "CLOSED_SELECTED_CARRIER_ACTIVE"
    assert result["branches"]["partner_rank1"]["counts"] == {"variables": 71, "generators": 2920, "raw_charts": 18, "S3_orbits": 4}
    assert result["branches"]["partner_rank2"]["counts"]["variables"] == 78
    assert result["branches"]["partner_rank3"]["counts"]["variables"] == 83
    assert result["scope"] == {"inputs_materialized": 1, "solver_runs": 0, "full_rankA07_branch_closed": False, "full_conjecture": False}


def hostile(result, mutation):
    candidate = copy.deepcopy(result)
    mutation(candidate)
    try:
        validate(candidate)
    except (AssertionError, KeyError, TypeError):
        return True
    return False


def main():
    for path, expected in PINS.items():
        assert sha256(path) == expected, (path, sha256(path), expected)
    parent = json.loads((PARENT / "results_anchor_no_rectangle_design.json").read_text())
    assert parent["selected_rank_design"]["rank3"] == {
        "condition": "det(A07)!=0 (mirror det(A06)!=0)",
        "generators": 6562,
        "remaining_carrier_obligation": "selected star can only help when ColSpan(A25,A26) is proper and contains no standard basis vector; otherwise another carrier or full-X5 identity is required",
        "saturation": "u07*det(A07)-1",
        "status": "EXACT_SMALLER_IDEAL_NOT_SOLVED",
        "variables": 82,
    }
    checks = adjugate_replay()
    assert len(checks) == 18
    source = build_rank1_program()
    rank1 = orbit_census_rank1()
    rank2 = orbit_census_rank2()
    rank2_generators = rank2_generator_census()
    rank3 = orbit_census_rank3()
    result = {
        "schema": "KRENN_X5_ANCHOR_RANK3_ADJUGATE_PARTNER_DESIGN_V1",
        "status": "PASS_EXACT_PARTNER_RANK_STRATIFICATION_ONE_SMALLER_INPUT_NO_SOLVE",
        "starting_branch": {
            "condition": "rank(A07)=3",
            "ideal": {"variables": 82, "generators": 6562},
            "selected_response": "L(K)=[A25^T|A26^T]*K*A07^T",
            "partner_matrix": "C=[A25|A26] in Mat(3,6)",
        },
        "adjugate_cancellation": {
            "inverse": "B07=u07*adj(A07), with u07*det(A07)=1",
            "identities": ["B07*A07=I3", "A07*B07=I3"],
            "matrix_entries_replayed": len(checks),
            "response_equivalence": "L(K)=0 iff A25^T*K=0 and A26^T*K=0, by right multiplication with B07^T",
            "kernel": "ker(L)={K:C^T*K=0}",
            "activity": "trace pairing fails iff rank(C)=3; K_ii fails iff e_i is in Col(C)",
        },
        "elimination_audit": {
            "A07_full_x5_occurrence": "A07 remains in the full-X5 amplitudes A07[a,h]*A26[c,g]",
            "nonstructural_guard_equations": 0,
            "direct_matrix_elimination": "none: unlike the rectangle guard branch, no equation identifies another block with A07^{-1}",
            "inverse_reparameterization": "replacing A07 by B07=A07^{-1} preserves the same 9-dimensional GL3 localization and the same 10-variable/1-relation affine presentation; it is not a count reduction",
            "strict_reduction_source": "stratify the partner column space forced by the adjugate-cancelled response, then parameterize only carrier-inactive strata",
        },
        "branches": {
            "partner_rank0": {
                "status": "CLOSED_SELECTED_CARRIER_ACTIVE",
                "proof": "C=0 gives L=0; trace and all K_ii are live on M3",
            },
            "partner_rank1": {
                "status": "EXACT_SMALLER_INACTIVE_DESIGN_NOT_SOLVED",
                "surviving_condition": "Col(C)=span(e_i); otherwise the selected carrier is active",
                "parameterization": "C=e_i*v^T, v in Q^6 nonzero",
                "forward": "rank(C)=1 and e_i in Col(C) force every column to be its i-th entry times e_i; choose one nonzero v coordinate",
                "reverse": "a saturated nonzero v coordinate makes C rank one with Col(C)=span(e_i), and substitution preserves every full-X5 amplitude",
                "counts": {"variables": 71, "generators": 2920, "raw_charts": rank1["raw_charts"], "S3_orbits": rank1["S3_orbits"]},
                "deduplication": {"raw_full_x5_words": 6561, "tautological_zero_words": 2916, "distinct_nonzero_full_x5_generators": 2918, "saturations": 2},
                "orbit_ledger": rank1["orbit_ledger"],
            },
            "partner_rank2": {
                "status": "EXACT_SMALLER_INACTIVE_DESIGN_NOT_MATERIALIZED_NOT_SOLVED",
                "surviving_condition": "e_i in Col(C); otherwise the selected carrier is active",
                "parameterization": "C=[e_i,u]*V^T with u_i=0, one non-i coordinate of u normalized to 1, and rank(V)=2",
                "forward_reverse": "the normalized quotient direction represents every two-plane containing e_i; a selected nonzero 2-minor of V makes the factorization rank two and reversible",
                "counts": {"variables": 78, "generators": rank2_generators["generators"], "raw_charts": rank2["raw_charts"], "S3_orbits": rank2["S3_orbits"]},
                "deduplication": rank2_generators,
                "orbit_ledger": rank2["orbit_ledger"],
            },
            "partner_rank3": {
                "status": "EXACT_FULL_PARTNER_RANK_DESIGN_NOT_MATERIALIZED_NOT_SOLVED",
                "condition": "rank(C)=3; the selected response has zero kernel",
                "counts": {"variables": 83, "generators": 6563, "raw_charts": rank3["raw_charts"], "S3_orbits": rank3["S3_orbits"]},
                "orbit_ledger": rank3["orbit_ledger"],
            },
        },
        "canonical_input": source,
        "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
        "scope": {"inputs_materialized": 1, "solver_runs": 0, "full_rankA07_branch_closed": False, "full_conjecture": False},
    }
    validate(result)
    tests = {
        "rank1_count_mutation": hostile(result, lambda value: value["branches"]["partner_rank1"]["counts"].__setitem__("variables", 70)),
        "rank0_underclaim": hostile(result, lambda value: value["branches"]["partner_rank0"].__setitem__("status", "OPEN")),
        "solve_injection": hostile(result, lambda value: value["scope"].__setitem__("solver_runs", 1)),
        "branch_overclaim": hostile(result, lambda value: value["scope"].__setitem__("full_rankA07_branch_closed", True)),
        "conjecture_overclaim": hostile(result, lambda value: value["scope"].__setitem__("full_conjecture", True)),
    }
    assert all(tests.values())
    result["hostile_tests"] = tests
    output = HERE / "results_anchor_rank3_adjugate_partner_design.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps({"status": result["status"], "canonical_variables": 71, "canonical_generators": 2920, "solver_runs": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
