#!/usr/bin/env python3
"""Independent literal referee for the rep5 four-subchart design."""
from __future__ import annotations

import hashlib
import json
import os
import re
from collections import Counter
from pathlib import Path

if not __debug__:
    raise RuntimeError("assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep5-selected72-both-branch-further-reduction-design-2026-08-26"
PARENT = ROOT / "computations/unaudited-codex-n8-x5-rep5-torus-selected-further-reduction-design-2026-08-26"
PARENT_REF = ROOT / "computations/unaudited-codex-n8-x5-rep5-torus-selected-further-reduction-design-referee-2026-08-26"
OPEN = PARENT / "sources/stage0_a37_201_Q_design.sing"
CLOSED = PARENT / "sources/stage1_a37_200_closed_Q_design.sing"

PINS = {
    DESIGN / "MANIFEST.sha256": "142f351a5c77f69b1e025e112e9036b125a22215cf5a0652a4187a153c365bf1",
    DESIGN / "results_design.json": "3498302c9056896a23139b0da26fd0eb5ae65d2af0256d0d82a11c0ef885deac",
    PARENT / "MANIFEST.sha256": "a1be34a89dae7597ab06efe6eaba6e0e4fc12256949f667ac8124ee93c35690e",
    PARENT_REF / "FINAL_MANIFEST.sha256": "d87fe6724f8d1f4bf628eb01986339c86705e55adf9b471cfeed140e725b123e",
    OPEN: "1e49c2b4127f1a185f50dbacbc63a51b97c210cb5dd9bd16a97f914c897fac1f",
    CLOSED: "502b68d7c669708c4e0497c7c457793e584fb2a89e07f70e54e85e83b750dd19",
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
    "parent": replay(PARENT / "MANIFEST.sha256"),
    "parent_referee": replay(PARENT_REF / "FINAL_MANIFEST.sha256"),
}


def raw_program(path: Path) -> tuple[list[str], list[str]]:
    text = path.read_text()
    variables = text.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
    body = text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
    assert "(" not in body and ")" not in body
    return variables, body.split(",\n")


open_variables, _ = raw_program(OPEN)
universe = open_variables + ["inv_a04_20"]
variable_index = {variable: index for index, variable in enumerate(universe)}


def parse(path: Path) -> tuple[list[str], list[dict[tuple[int, ...], int]]]:
    variables, expressions = raw_program(path)
    allowed = set(variables)
    polynomials = []
    for expression in expressions:
        polynomial: dict[tuple[int, ...], int] = {}
        for raw in re.findall(r"[+-]?[^+-]+", expression):
            sign = -1 if raw.startswith("-") else 1
            token = raw[1:] if raw[:1] in "+-" else raw
            coefficient = sign
            factors = []
            for factor in token.split("*"):
                if factor.isdigit():
                    coefficient *= int(factor)
                else:
                    assert factor in allowed and factor in variable_index, factor
                    factors.append(variable_index[factor])
            monomial = tuple(sorted(factors))
            polynomial[monomial] = polynomial.get(monomial, 0) + coefficient
        polynomial = {monomial: coefficient for monomial, coefficient in polynomial.items() if coefficient}
        assert polynomial
        polynomials.append(polynomial)
    return variables, polynomials


def canonical(polynomials):
    result = []
    seen = set()
    for polynomial in polynomials:
        polynomial = {monomial: coefficient for monomial, coefficient in polynomial.items() if coefficient}
        if not polynomial:
            continue
        key = tuple(sorted(polynomial.items()))
        if key not in seen:
            seen.add(key)
            result.append(polynomial)
    return result


def specialize(polynomials, coordinate, value):
    output = []
    for polynomial in polynomials:
        reduced = {}
        for monomial, coefficient in polynomial.items():
            if value == 0 and coordinate in monomial:
                continue
            new_monomial = tuple(index for index in monomial if not (value == 1 and index == coordinate))
            reduced[new_monomial] = reduced.get(new_monomial, 0) + coefficient
        output.append(reduced)
    return canonical(output)


open_ring, open_polynomials = parse(OPEN)
closed_ring, closed_polynomials = parse(CLOSED)
assert open_ring == closed_ring == open_variables
assert len(open_variables) == 72
assert len(open_polynomials) == len(closed_polynomials) == 6561

result = json.loads((DESIGN / "results_design.json").read_text())
assert result["status"] == "PASS_EXACT_FURTHER_COVERS_BOTH_PARENT_BRANCHES"
assert result["combined_cover"] == {"all_sources_exact_Q_design_only": True, "direct_implication_between_parent_branches": False, "every_parent_point_covered": True, "parent_branches_covered": ["q=1", "q=0"], "subcharts": 4}

open_records = result["open_q1_factor_localization"]["sources"]
closed_records = result["closed_q0_residual_torus"]["sources"]
records = open_records + closed_records
paths = [DESIGN / record["path"] for record in records]
for record, path in zip(records, paths):
    assert path.is_file() and sha(path) == record["sha256"]

# q=1 parent: exact D(x)/V(x) localization.  On D(x), divide precisely the
# generators wholly divisible by x and adjoin x*inv=1.  On V(x), specialize
# literally.  Compare each generated ideal polynomial-for-polynomial.
x = variable_index["a04_20"]
inv = variable_index["inv_a04_20"]
open_D_ring, open_D = parse(paths[0])
open_V_ring, open_V = parse(paths[1])
divided = []
divisible = 0
for polynomial in open_polynomials:
    if all(x in monomial for monomial in polynomial):
        divisible += 1
        reduced = {}
        for monomial, coefficient in polynomial.items():
            work = list(monomial)
            work.remove(x)
            reduced[tuple(work)] = coefficient
        divided.append(reduced)
    else:
        divided.append(polynomial)
expected_open_D = canonical(divided + [{(): 1, tuple(sorted((x, inv))): -1}])
expected_open_V = specialize(open_polynomials, x, 0)
assert divisible == 486
assert open_D == expected_open_D and open_V == expected_open_V
assert open_D_ring == open_variables + ["inv_a04_20"]
assert open_V_ring == [variable for variable in open_variables if variable != "a04_20"]

# Independently exhaust the factor-coordinate census; no other coordinate
# divides a source generator.
factor_coordinates = []
for coordinate, name in enumerate(open_variables):
    count = sum(all(coordinate in monomial for monomial in polynomial) for polynomial in open_polynomials)
    if count:
        factor_coordinates.append([name, count])
assert factor_coordinates == [["a04_20", 486], ["a04_21", 486], ["a04_22", 486]]

# q=0 parent: literal V(r) and root-free normalized D(r).  Verify the slice
# sources and the full homogeneous weight action.
r_name = result["closed_q0_residual_torus"]["selected_coordinate"]
assert r_name == "a35_21" and result["closed_q0_residual_torus"]["selected_weight"] == -1
r_coordinate = variable_index[r_name]
closed_D_ring, closed_D = parse(paths[2])
closed_V_ring, closed_V = parse(paths[3])
assert closed_D == specialize(closed_polynomials, r_coordinate, 1)
assert closed_V == specialize(closed_polynomials, r_coordinate, 0)
expected_closed_ring = [variable for variable in closed_ring if variable != r_name]
assert closed_D_ring == closed_V_ring == expected_closed_ring

weights = {variable_index[name]: weight for name, weight in result["closed_q0_residual_torus"]["primitive_weights"].items()}
constraint_rows = []
for polynomial in closed_polynomials:
    monomials = sorted(polynomial)
    base = Counter(monomials[0])
    base_degree = sum(weights.get(index, 0) * exponent for index, exponent in base.items())
    for monomial in monomials[1:]:
        current = Counter(monomial)
        assert sum(weights.get(index, 0) * exponent for index, exponent in current.items()) == base_degree
        row = {index: base[index] - current[index] for index in set(base) | set(current) if base[index] != current[index]}
        if row:
            constraint_rows.append(row)


def rank_mod(rows, prime):
    echelon = {}
    for raw in rows:
        row = {column: value % prime for column, value in raw.items() if value % prime}
        while row:
            pivot = min(row)
            if pivot not in echelon:
                inverse = pow(row[pivot], -1, prime)
                echelon[pivot] = {column: value * inverse % prime for column, value in row.items()}
                break
            factor = row[pivot]
            known = echelon[pivot]
            row = {column: (row.get(column, 0) - factor * known.get(column, 0)) % prime for column in set(row) | set(known)}
            row = {column: value for column, value in row.items() if value}
    return len(echelon)


modular_ranks = [rank_mod(constraint_rows, prime) for prime in (32003, 65521)]
assert modular_ranks == [71, 71]
# The explicit nonzero weight vector bounds rank by 71 over Q; modular rank 71
# bounds it below by 71.  Thus the Q-nullity is exactly one.
assert any(weights.values()) and weights[r_coordinate] == -1

parent_ref = json.loads((PARENT_REF / "results_referee.json").read_text())
assert parent_ref["status"] == "PASS_EXACT_TWO_CHART_RESIDUAL_ONE_TORUS_COVER_DESIGN_ONLY"
assert parent_ref["cover_proof"]["exhaustive"] is True
assert parent_ref["cover_proof"]["root_free"] is True
assert [source["sha256"] for source in parent_ref["cover_proof"]["sources"]] == [sha(OPEN), sha(CLOSED)]

# Rank the four exact subcharts by a fail-closed, finite syntax objective.  The
# first coordinate is variables, then generator count, expanded term count,
# degree mass, and bytes.  No claim is made that this predicts solve time.
ranked = []
for record in records:
    ranked.append({
        "path": record["path"],
        "objective": [record["variables"], record["generators"], record["total_terms"], record["degree_mass"], record["bytes"]],
        "variables": record["variables"],
        "generators": record["generators"],
        "total_terms": record["total_terms"],
        "maximum_terms": record["maximum_terms"],
        "sha256": record["sha256"],
    })
ranked.sort(key=lambda item: (item["objective"], item["path"]))
assert ranked[0]["path"] == "sources/closed_q0_V_a35_21_Q_design.sing"
assert ranked[0]["objective"] == [71, 6075, 192489, 963540, 6212317]

output = {
    "schema": "KRENN_X5_REP5_SELECTED72_BOTH_BRANCH_FURTHER_REDUCTION_INDEPENDENT_REFEREE_V1",
    "status": "PASS_LITERAL_FOUR_SUBCHART_EXHAUSTIVE_COVER_DESIGN_ONLY",
    "producer": {"manifest_sha256": PINS[DESIGN / "MANIFEST.sha256"], "result_sha256": PINS[DESIGN / "results_design.json"]},
    "manifest_replay_counts": manifest_counts,
    "parent_cover": {"branches": ["D(a37_20) normalized to q=1", "V(a37_20) at q=0"], "exhaustive": True, "root_free": True},
    "open_q1_replay": {"coordinate": "a04_20", "factor_coordinates": factor_coordinates, "divided_generators": divisible, "D_source_sha256": sha(paths[0]), "V_source_sha256": sha(paths[1]), "exhaustive": True},
    "closed_q0_replay": {"coordinate": r_name, "weight": -1, "modular_grading_ranks": modular_ranks, "nullity_over_Q": 1, "D_source_sha256": sha(paths[2]), "V_source_sha256": sha(paths[3]), "exhaustive": True, "root_free": True},
    "combined": {"parent_branches": 2, "subcharts": 4, "every_parent_point_covered": True, "direct_implication_between_parents": False},
    "ranked_next_charts": ranked,
    "smallest_sound_next": {"path": ranked[0]["path"], "sha256": ranked[0]["sha256"], "objective": ranked[0]["objective"], "recommended_action": "source-level symbolic reduction census first; if no exact reduction, this is the smallest held solver chart"},
    "scope": {"design_only": True, "singular_runs": 0, "ideal_solves": 0, "mathematical_coverage_added": False, "rep5_closed": False},
}
temporary = HERE / "results_referee.json.tmp"
temporary.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "results_referee.json")
print(json.dumps({"status": output["status"], "next": ranked[0]["path"], "solves": 0}, sort_keys=True))
