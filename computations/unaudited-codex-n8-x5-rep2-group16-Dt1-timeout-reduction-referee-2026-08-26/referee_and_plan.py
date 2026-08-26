#!/usr/bin/env python3
"""Literal referee and held one-lane plan for the rep2 group16 D(t1) slice."""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import re
from collections import Counter
from pathlib import Path

if not __debug__:
    raise RuntimeError("assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-Dt1-timeout-reduction-design-2026-08-26"
TCOVER = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-tcover-complement3-exact-q-held-2026-08-26"
COMPARISON = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-torus-gauge-referee-comparison-2026-08-26"
SOURCE = TCOVER / "sources/rep2_group016_67_Dt1_runtime_Q.sing"
SLICE = DESIGN / "sources/rep2_group16_Dt1_it1_GLOBAL_UNIT_GAUGE_Q_design.sing"

PINS = {
    DESIGN / "MANIFEST.sha256": "aab19d2f51693fed67f587d83fe0d2e108888d626d788e4d00a9362a3be978be",
    DESIGN / "results_design.json": "2fde51cc869ec34a4ad40dabc73ed0e06598225c672cba40ef3d7499664adbac",
    SLICE: "32707a25c384ea038790e393e18654e3e41a34f59aa4303bc4eb74115d073e37",
    SOURCE: "f0212ca6edfec2941b68a0161d8a4f81c9455f3729d94150e16eafb057043244",
    TCOVER / "TERMINAL_MANIFEST.sha256": "5d9fdcbfea5aab0245ffde35ab62b4ab3626c99d8b88d09b5a8554ae8bd49551",
    TCOVER / "source_ledger.json": "59cce6093bdb98fff5a17df3140c240ef9c68c2fbf7eafef9bc6780acf40f046",
    TCOVER / "batch_result.json": "5b3250c4ee21d1392e148f4094bf6095bd39e94a835799cc6b3d643a79e6b510",
    TCOVER / "results/lane1_Vt1_Dt2.json": "74edb47efd0fc3f1a408376def232add11b2652d852341a538ce38e772a66351",
    TCOVER / "results/lane2_Dt1.json": "b4656dd9e74e31b38a63af40404e8b0d0291f5a5d31e471dde104ab59d2e0c8f",
    COMPARISON / "combined_57_ledger.json": "9d74277670a3fb8d98c7ec04678fd4f86034f1a4a6d69d745c410fb1a74373e9",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(path: Path) -> int:
    count = 0
    for line in path.read_text().splitlines():
        digest, name = line.split(None, 1)
        target = (path.parent / name.strip()).resolve()
        if not target.is_file():
            target = (ROOT / name.strip()).resolve()
        assert target.is_file() and sha(target) == digest, target
        count += 1
    return count


for path, digest in PINS.items():
    assert path.is_file() and sha(path) == digest, path
manifest_counts = {
    "design": replay(DESIGN / "MANIFEST.sha256"),
    "three_lane_terminal": replay(TCOVER / "TERMINAL_MANIFEST.sha256"),
    "57_chart_comparison": replay(COMPARISON / "MANIFEST.sha256"),
}


def parse_program(text: str) -> tuple[list[str], list[dict[tuple[str, ...], int]]]:
    variables = text.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
    body = text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
    assert "(" not in body and ")" not in body
    equations = body.split(",\n")
    parsed = []
    allowed = set(variables)
    for expression in equations:
        polynomial: dict[tuple[str, ...], int] = {}
        for raw in re.findall(r"[+-]?[^+-]+", expression.strip()):
            sign = -1 if raw.startswith("-") else 1
            token = raw[1:] if raw[:1] in "+-" else raw
            coefficient = sign
            factors = []
            for factor in token.split("*"):
                if factor.isdigit():
                    coefficient *= int(factor)
                else:
                    assert factor in allowed, factor
                    factors.append(factor)
            monomial = tuple(sorted(factors, key=variables.index))
            polynomial[monomial] = polynomial.get(monomial, 0) + coefficient
        polynomial = {monomial: coefficient for monomial, coefficient in polynomial.items() if coefficient}
        assert polynomial
        parsed.append(polynomial)
    return variables, parsed


source_variables, source_polynomials = parse_program(SOURCE.read_text())
slice_variables, slice_polynomials = parse_program(SLICE.read_text())
assert len(source_variables) == 64 and len(source_polynomials) == 6569
assert len(slice_variables) == 61 and len(slice_polynomials) == 6568
assert set(source_variables) - set(slice_variables) == {"it1", "sat", "t1"}

design = json.loads((DESIGN / "results_design.json").read_text())
assert design["status"] == "PASS_EXACT_MAXIMAL_GLOBAL_UNIT_TORUS_GAUGE"
assert design["cover"]["maximal_primitive_global_gauge_coordinates"] == ["it1", "sat"]
assert design["cover"]["global_gauge_assignments_including_inverse_partners"] == {"it1": 1, "sat": 1, "t1": 1}
assert design["cover"]["closed_branch_empty"] is True
assert design["conclusion"] == {"mathematical_coverage": False, "old_chart_relaunch": False, "old_timeout_consumed": True, "singular_runs": 0}

# Independently verify every source polynomial is homogeneous for every one of
# the six integer grading basis vectors.  This makes the recorded torus action
# literal, rather than a generic-open inference.
grading_basis = design["grading"]["basis"]
assert len(grading_basis) == design["grading"]["nullity"] == 6
assert all(len(vector) == len(source_variables) for vector in grading_basis)
for polynomial in source_polynomials:
    for vector in grading_basis:
        degrees = {sum(vector[source_variables.index(factor)] for factor in monomial) for monomial in polynomial}
        assert len(degrees) == 1

# Recover global-unit witnesses directly.  q is a unit when a generator has
# constant +/-1 and q divides every other monomial.
global_units: dict[str, list[int]] = {}
for equation_index, polynomial in enumerate(source_polynomials):
    if abs(polynomial.get((), 0)) != 1:
        continue
    supports = [set(monomial) for monomial in polynomial if monomial]
    if not supports:
        continue
    for variable in set.intersection(*supports):
        global_units.setdefault(variable, []).append(equation_index)
assert global_units == {"it1": [6568], "sat": [6567], "t1": [6568]}
assert source_polynomials[6568] == {(): -1, tuple(sorted(("it1", "t1"), key=source_variables.index)): 1}

# The it1 and sat weight rows span a primitive rank-two summand: gcd of all
# 2x2 minors is one, so normalization uses no root extraction.
rows = [[vector[source_variables.index(variable)] for vector in grading_basis] for variable in ("it1", "sat")]
minor_gcd = 0
for left, right in itertools.combinations(range(6), 2):
    minor_gcd = math.gcd(minor_gcd, abs(rows[0][left] * rows[1][right] - rows[0][right] * rows[1][left]))
assert minor_gcd == 1
assert rows == design["cover"]["maximal_primitive_global_gauge_weight_rows"]

# Independently specialize the original ideal at it1=sat=t1=1, combine terms,
# remove zero and duplicate generators, and compare the literal 61-variable
# source polynomial-for-polynomial.
assignments = {"it1", "sat", "t1"}
specialized = []
seen = set()
for polynomial in source_polynomials:
    reduced: dict[tuple[str, ...], int] = {}
    for monomial, coefficient in polynomial.items():
        new_monomial = tuple(factor for factor in monomial if factor not in assignments)
        reduced[new_monomial] = reduced.get(new_monomial, 0) + coefficient
    reduced = {monomial: coefficient for monomial, coefficient in reduced.items() if coefficient}
    if not reduced:
        continue
    key = tuple(sorted(reduced.items()))
    if key not in seen:
        seen.add(key)
        specialized.append(reduced)
assert specialized == slice_polynomials
assert sum(len(polynomial) for polynomial in specialized) == 244567

# Reconstruct the 57 -> 60 chart refinement and its exact remaining scope.
ledger57 = json.loads((COMPARISON / "combined_57_ledger.json").read_text())
assert len(ledger57) == 57
assert len({(record["guard_pivot_k"], record["torus_stratum_index"]) for record in ledger57}) == 57
assert {record["guard_pivot_k"] for record in ledger57} == {0, 1, 2}
assert all({record["torus_stratum_index"] for record in ledger57 if record["guard_pivot_k"] == k} == set(range(19)) for k in range(3))
kind_counts = Counter(record["torus_kind"] for record in ledger57)
assert kind_counts == {"A67_entry_open": 27, "A67_zero_A12_entry_open": 27, "A67_zero_A12_zero": 3}
tcover_ledger = json.loads((TCOVER / "source_ledger.json").read_text())
assert len(tcover_ledger["partition"]) == 4
assert tcover_ledger["single_chart_closes_group16"] is False
lane1 = json.loads((TCOVER / "results/lane1_Vt1_Dt2.json").read_text())
lane2 = json.loads((TCOVER / "results/lane2_Dt1.json").read_text())
batch = json.loads((TCOVER / "batch_result.json").read_text())
assert lane1["status"] == "UNIT_IDEAL_EXACT_Q"
assert lane2["status"] == "FAIL_CLOSED_RESOURCE" and lane2["termination"] == "NATIVE_WALL_CAP_480"
assert batch["status"] == "STOPPED_FAIL_CLOSED" and batch["skipped_after_stop"] == ["Vt1_Vt2_Dt0"]
expanded_chart_count = len(ledger57) - 1 + len(tcover_ledger["partition"])
closed_refined_strata = 2  # V(t0,t1,t2) and V(t1) intersect D(t2)
remaining_charts = expanded_chart_count - closed_refined_strata
assert expanded_chart_count == 60 and remaining_charts == 58

# Materialize a held exact-Q source by changing only the terminal epilogue.
slice_text = SLICE.read_text()
assert slice_text.endswith('print("INPUT_GENERATORS="+string(size(I)));\nquit;\n')
epilogue = '''print("INPUT_GENERATORS="+string(size(I)));
ideal G=slimgb(I);
poly unit_remainder=reduce(1,G);
print("GROEBNER_SIZE="+string(size(G)));
print("UNIT_REMAINDER="+string(unit_remainder));
if ((size(G)==1) && (unit_remainder==0)) { print("STATUS=UNIT_IDEAL"); }
else { print("STATUS=NONUNIT_OR_UNCERTIFIED"); }
quit;
'''
runtime_text = slice_text.removesuffix('print("INPUT_GENERATORS="+string(size(I)));\nquit;\n') + epilogue
runtime_path = HERE / "rep2_group16_Dt1_global_unit_gauge_runtime_Q.sing"
temporary = runtime_path.with_suffix(".sing.tmp")
temporary.write_text(runtime_text)
os.replace(temporary, runtime_path)
runtime_variables, runtime_polynomials = parse_program(runtime_text)
assert runtime_variables == slice_variables and runtime_polynomials == slice_polynomials
runtime_sha = sha(runtime_path)

held_plan = {
    "schema": "KRENN_X5_REP2_GROUP16_DT1_GLOBAL_UNIT_GAUGE_EXACT_Q_HELD_PLAN_V1",
    "status": "APPROVE_HELD_ZERO_RUNS",
    "logical_scope": "rep2 group16 D(t1) stratum only",
    "source": {"path": runtime_path.name, "sha256": runtime_sha, "field": "Q", "variables": 61, "generators": 6568},
    "design_dependency": {"manifest_sha256": PINS[DESIGN / "MANIFEST.sha256"], "result_sha256": PINS[DESIGN / "results_design.json"]},
    "consumed_timeout": {"result_sha256": PINS[TCOVER / "results/lane2_Dt1.json"], "relaunch": False},
    "resources": {"native_wall_seconds": 480, "wrapper_wall_seconds": 510, "rss_bytes": 8589934592, "parallel": False},
    "execution_contract": {"single_lane": True, "fresh_clearance_required": True, "atomic_outputs": True, "refuse_overwrite": True, "stop_any_outcome": True, "automatic_relaunch": False, "other_charts": False},
    "acceptance": {"returncode": 0, "input_variables": 61, "input_generators": 6568, "groebner_size": 1, "unit_remainder": 0, "status": "UNIT_IDEAL"},
    "attempts": 0,
    "launch_authorized": False,
    "group16_closed_on_success": False,
    "rep2_closed_on_success": False,
}
plan_tmp = HERE / "HELD_PLAN.json.tmp"
plan_tmp.write_text(json.dumps(held_plan, indent=2, sort_keys=True) + "\n")
os.replace(plan_tmp, HERE / "HELD_PLAN.json")

result = {
    "schema": "KRENN_X5_REP2_GROUP16_DT1_TIMEOUT_REDUCTION_INDEPENDENT_REFEREE_V1",
    "status": "PASS_EXACT_61VAR_GLOBAL_UNIT_TORUS_GAUGE_AND_HELD_LANE",
    "producer": {"manifest_sha256": PINS[DESIGN / "MANIFEST.sha256"], "result_sha256": PINS[DESIGN / "results_design.json"], "slice_sha256": PINS[SLICE]},
    "manifest_replay_counts": manifest_counts,
    "literal_source_equivalence": {"input_variables": 64, "input_generators": 6569, "assignments": {"it1": 1, "sat": 1, "t1": 1}, "slice_variables": 61, "slice_generators": 6568, "slice_total_terms": 244567},
    "global_unit_witnesses": global_units,
    "primitive_rank_two_minor_gcd": minor_gcd,
    "chart_census": {"original": 57, "refined": 60, "closed_refined_strata": 2, "remaining": 58, "untouched_original_charts": 56, "other_unclosed_refined_chart": "V(t1,t2) intersect D(t0)"},
    "next_exact_cover": {"nontrivial_lanes": 1, "empty_branches": 0, "runtime_source_sha256": runtime_sha, "variables": 61, "generators": 6568, "scope": "equivalent slice for failed D(t1) chart only"},
    "held_plan_sha256": sha(HERE / "HELD_PLAN.json"),
    "solver_runs": 0,
    "mathematical_coverage_added": False,
    "group16_closed": False,
    "rep2_closed": False,
}
result_tmp = HERE / "results_referee.json.tmp"
result_tmp.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
os.replace(result_tmp, HERE / "results_referee.json")
print(json.dumps({"status": result["status"], "runtime_sha256": runtime_sha, "remaining": 58}, sort_keys=True))
