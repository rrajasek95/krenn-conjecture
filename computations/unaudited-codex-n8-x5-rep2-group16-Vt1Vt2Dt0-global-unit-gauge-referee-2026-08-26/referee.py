#!/usr/bin/env python3
"""Independent literal referee for the unlaunched V(t1,t2)D(t0) gauge."""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import re
from pathlib import Path

if not __debug__:
    raise RuntimeError("assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-Vt1Vt2Dt0-global-unit-gauge-design-2026-08-26"
TCOVER = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-tcover-complement3-exact-q-held-2026-08-26"
SOURCE = TCOVER / "sources/rep2_group016_67_Vt1_Vt2_Dt0_runtime_Q.sing"
SLICE = DESIGN / "sources/rep2_group16_Dt1_it0_GLOBAL_UNIT_GAUGE_Q_design.sing"
PINS = {
    DESIGN / "MANIFEST.sha256": "02e228e1f8eaaea3abf063c1c9534a1245b98f50743155c85eae619dc59cfbfe",
    DESIGN / "results_design.json": "fd52371267dc88718cc01b6b41997138c672025427f8ade0d7fe25f57cbb2028",
    SOURCE: "819ba657d4e7ad27e0348613b72c84bfca517376bfab6158b50c07a09e87509b",
    SLICE: "bb9c275233ff981a5d3f5dbbe5ac20ed49bc652c1b7f35b34c9cc5eeab3c4884",
    TCOVER / "batch_result.json": "5b3250c4ee21d1392e148f4094bf6095bd39e94a835799cc6b3d643a79e6b510",
    TCOVER / "TERMINAL_MANIFEST.sha256": "5d9fdcbfea5aab0245ffde35ab62b4ab3626c99d8b88d09b5a8554ae8bd49551",
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
manifest_counts = {"design": replay(DESIGN / "MANIFEST.sha256"), "batch_terminal": replay(TCOVER / "TERMINAL_MANIFEST.sha256")}


def parse(path: Path):
    text = path.read_text()
    variables = text.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
    body = text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
    assert "(" not in body and ")" not in body
    polynomials = []
    index = {variable: position for position, variable in enumerate(variables)}
    for expression in body.split(",\n"):
        polynomial = {}
        for raw in re.findall(r"[+-]?[^+-]+", expression):
            sign = -1 if raw.startswith("-") else 1
            token = raw[1:] if raw[:1] in "+-" else raw
            coefficient = sign
            factors = []
            for factor in token.split("*"):
                if factor.isdigit():
                    coefficient *= int(factor)
                else:
                    assert factor in index
                    factors.append(index[factor])
            monomial = tuple(sorted(factors))
            polynomial[monomial] = polynomial.get(monomial, 0) + coefficient
        polynomial = {monomial: coefficient for monomial, coefficient in polynomial.items() if coefficient}
        assert polynomial
        polynomials.append(polynomial)
    return variables, polynomials


source_variables, source_polynomials = parse(SOURCE)
slice_variables, slice_local_polynomials = parse(SLICE)
assert len(source_variables) == 64 and len(source_polynomials) == 6569
assert len(slice_variables) == 61 and len(slice_local_polynomials) == 6568
assert set(source_variables) - set(slice_variables) == {"it0", "sat", "t0"}

# Translate the slice's local monomial indices back to the parent ring.
parent_index = {variable: position for position, variable in enumerate(source_variables)}
slice_polynomials = []
for polynomial in slice_local_polynomials:
    translated = {}
    for monomial, coefficient in polynomial.items():
        translated[tuple(sorted(parent_index[slice_variables[position]] for position in monomial))] = coefficient
    slice_polynomials.append(translated)

design = json.loads((DESIGN / "results_design.json").read_text())
assert design["status"] == "PASS_EXACT_MAXIMAL_GLOBAL_UNIT_TORUS_GAUGE"
assert design["cover"]["maximal_primitive_global_gauge_coordinates"] == ["it0", "sat"]
assert design["cover"]["global_gauge_assignments_including_inverse_partners"] == {"it0": 1, "sat": 1, "t0": 1}
assert design["cover"]["closed_branch_empty"] is True
assert design["conclusion"] == {"mathematical_coverage": False, "prior_batch_stop_preserved": True, "singular_runs": 0, "this_chart_previously_launched": False}

grading_basis = design["grading"]["basis"]
assert len(grading_basis) == design["grading"]["nullity"] == 6
for polynomial in source_polynomials:
    for vector in grading_basis:
        degrees = {sum(vector[position] for position in monomial) for monomial in polynomial}
        assert len(degrees) == 1

global_units = {}
for equation_index, polynomial in enumerate(source_polynomials):
    if abs(polynomial.get((), 0)) != 1:
        continue
    supports = [set(monomial) for monomial in polynomial if monomial]
    if supports:
        for position in set.intersection(*supports):
            global_units.setdefault(source_variables[position], []).append(equation_index)
assert global_units == {"it0": [6568], "sat": [6567], "t0": [6568]}
inverse = tuple(sorted((parent_index["it0"], parent_index["t0"])))
assert source_polynomials[6568] == {(): -1, inverse: 1}

rows = [[vector[parent_index[variable]] for vector in grading_basis] for variable in ("it0", "sat")]
minor_gcd = 0
for left, right in itertools.combinations(range(6), 2):
    minor_gcd = math.gcd(minor_gcd, abs(rows[0][left] * rows[1][right] - rows[0][right] * rows[1][left]))
assert minor_gcd == 1
assert rows == design["cover"]["maximal_primitive_global_gauge_weight_rows"]

assigned = {parent_index[name] for name in ("it0", "sat", "t0")}
specialized = []
seen = set()
for polynomial in source_polynomials:
    reduced = {}
    for monomial, coefficient in polynomial.items():
        new_monomial = tuple(position for position in monomial if position not in assigned)
        reduced[new_monomial] = reduced.get(new_monomial, 0) + coefficient
    reduced = {monomial: coefficient for monomial, coefficient in reduced.items() if coefficient}
    if not reduced:
        continue
    key = tuple(sorted(reduced.items()))
    if key not in seen:
        seen.add(key)
        specialized.append(reduced)
assert specialized == slice_polynomials
assert sum(len(polynomial) for polynomial in specialized) == 659385

batch = json.loads((TCOVER / "batch_result.json").read_text())
assert batch["status"] == "STOPPED_FAIL_CLOSED"
assert batch["skipped_after_stop"] == ["Vt1_Vt2_Dt0"]
assert design["batch_stop_binding"]["this_chart_previously_launched"] is False

output = {
    "schema": "KRENN_X5_REP2_GROUP16_VT1VT2DT0_GLOBAL_UNIT_GAUGE_INDEPENDENT_REFEREE_V1",
    "status": "PASS_EXACT_61VAR_GLOBAL_UNIT_GAUGE_UNLAUNCHED",
    "producer": {"manifest_sha256": PINS[DESIGN / "MANIFEST.sha256"], "result_sha256": PINS[DESIGN / "results_design.json"], "slice_sha256": PINS[SLICE]},
    "manifest_replay_counts": manifest_counts,
    "literal_source_equivalence": {"input_variables": 64, "input_generators": 6569, "assignments": {"it0": 1, "sat": 1, "t0": 1}, "slice_variables": 61, "slice_generators": 6568, "slice_total_terms": 659385},
    "global_unit_witnesses": global_units,
    "primitive_rank_two_minor_gcd": minor_gcd,
    "batch_stop_preserved": True,
    "previously_launched": False,
    "filename_note": "slice filename contains legacy Dt1 token; logical binding is hash-pinned V(t1,t2)D(t0) and the mismatch is cosmetic",
    "scope": {"design_only": True, "singular_runs": 0, "mathematical_coverage_added": False, "group16_closed": False, "rep2_closed": False},
}
tmp = HERE / "results_referee.json.tmp"
tmp.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
os.replace(tmp, HERE / "results_referee.json")
print(json.dumps({"status": output["status"], "solves": 0}, sort_keys=True))
