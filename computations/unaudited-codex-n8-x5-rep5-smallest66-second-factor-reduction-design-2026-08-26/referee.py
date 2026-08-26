#!/usr/bin/env python3
"""Independent reconstruction referee for the second rep5 coordinate-factor cover."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT = ROOT / "computations/unaudited-codex-n8-x5-rep5-smallest67-factor-determinant-reduction-design-2026-08-26"
SOURCE = PARENT / "sources/V_a24_00_Q_design.sing"
DESIGN = json.loads((HERE / "results_design.json").read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha(SOURCE) == "4821a045e6f4c799a002a9d097c7353857b8058f4dfdb01b1048d09b5dcd6927"
assert DESIGN["schema"] == "KRENN_X5_REP5_SMALLEST66_SECOND_FACTOR_REDUCTION_DESIGN_V1"
assert DESIGN["scope"]["singular_runs"] == DESIGN["scope"]["ideal_solves"] == 0


def split(path):
    text = path.read_text()
    names = text.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
    body = text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
    return names, body.split(",\n")


parent_names, _ = split(SOURCE)
universe = parent_names + ["inv_second_factor"]
index = {name: i for i, name in enumerate(universe)}


def parse(path):
    ring, expressions = split(path)
    result = []
    for expression in expressions:
        polynomial = {}
        for raw in re.findall(r"[+-]?[^+-]+", expression):
            sign = -1 if raw.startswith("-") else 1
            factors = raw.lstrip("+-").split("*")
            coefficient = sign
            if factors[0].isdigit():
                coefficient *= int(factors.pop(0))
            monomial = tuple(sorted(index[factor] for factor in factors if factor))
            polynomial[monomial] = polynomial.get(monomial, 0) + coefficient
        polynomial = {monomial: coefficient for monomial, coefficient in polynomial.items() if coefficient}
        assert polynomial
        result.append(polynomial)
    return ring, result


def canonical(values):
    answer = []
    seen = set()
    for polynomial in values:
        polynomial = {monomial: coefficient for monomial, coefficient in polynomial.items() if coefficient}
        if not polynomial:
            continue
        if len(polynomial) == 1 and () in polynomial:
            return [{(): 1}]
        key = tuple(sorted(polynomial.items()))
        if key not in seen:
            seen.add(key)
            answer.append(polynomial)
    return answer


ring, parent = parse(SOURCE)
assert ring == parent_names and len(ring) == 66 and len(parent) == 3591
pivot_name = DESIGN["selected_cover"]["selected_coordinate"]
assert pivot_name == "a04_00"
pivot = index[pivot_name]

divided = []
factor_count = 0
zero = []
for polynomial in parent:
    if all(pivot in monomial for monomial in polynomial):
        factor_count += 1
        quotient = {}
        for monomial, coefficient in polynomial.items():
            work = list(monomial)
            work.remove(pivot)
            quotient[tuple(work)] = coefficient
        divided.append(quotient)
    else:
        divided.append(polynomial)
    zero.append({monomial: coefficient for monomial, coefficient in polynomial.items() if pivot not in monomial})
assert factor_count == 108
inverse = index["inv_second_factor"]
expected_D = canonical(divided + [{(): 1, tuple(sorted((pivot, inverse))): -1}])
expected_V = canonical(zero)

records = {record["kind"]: record for record in DESIGN["selected_cover"]["sources"]}
D_path = HERE / records["D"]["path"]
V_path = HERE / records["V"]["path"]
D_ring, actual_D = parse(D_path)
V_ring, actual_V = parse(V_path)
assert D_ring == parent_names + ["inv_second_factor"] and actual_D == expected_D
assert V_ring == [name for name in parent_names if name != pivot_name] and actual_V == expected_V
assert sha(D_path) == records["D"]["sha256"] and sha(V_path) == records["V"]["sha256"]
assert records["D"]["variables"] == 67 and records["D"]["generators"] == 3592 and records["D"]["total_terms"] == 137579
assert records["V"]["variables"] == 65 and records["V"]["generators"] == 3483 and records["V"]["total_terms"] == 128231


def rank_mod(rows, prime):
    echelon = {}
    for raw in rows:
        row = {column: value % prime for column, value in raw.items() if value % prime}
        while row:
            column = min(row)
            if column not in echelon:
                inverse_value = pow(row[column], -1, prime)
                echelon[column] = {key: value * inverse_value % prime for key, value in row.items()}
                break
            factor = row[column]
            known = echelon[column]
            row = {key: (row.get(key, 0) - factor * known.get(key, 0)) % prime for key in set(row) | set(known)}
            row = {key: value for key, value in row.items() if value}
    return len(echelon)


grading_rows = []
linear_rows = []
adjacency = [set() for _ in parent_names]
active = set()
monic = []
for equation, polynomial in enumerate(parent):
    monomials = sorted(polynomial)
    base = Counter(monomials[0])
    for monomial in monomials[1:]:
        current = Counter(monomial)
        row = {i: base[i] - current[i] for i in set(base) | set(current) if base[i] != current[i]}
        if row:
            grading_rows.append(row)
    linear = {monomial[0]: coefficient for monomial, coefficient in polynomial.items() if len(monomial) == 1}
    if linear:
        linear_rows.append(linear)
    support = {i for monomial in polynomial for i in monomial}
    active |= support
    for i in support:
        adjacency[i] |= support - {i}
        if abs(polynomial.get((i,), 0)) == 1 and all(i not in monomial for monomial in polynomial if monomial != (i,)):
            monic.append([equation, parent_names[i]])
assert [rank_mod(grading_rows, prime) for prime in (32003, 65521)] == [66, 66]
assert [rank_mod(linear_rows, prime) for prime in (32003, 65521)] == [39, 39]
assert active == set(range(66)) and not monic
unseen = set(range(66))
components = []
while unseen:
    queue = deque([min(unseen)])
    component = set()
    while queue:
        vertex = queue.popleft()
        if vertex in component:
            continue
        component.add(vertex)
        queue.extend(adjacency[vertex] - component)
    unseen -= component
    components.append(component)
assert [len(component) for component in components] == [66]

minor_ledger = DESIGN["minor_rank_split"]["candidate_ledger"]
assert len(minor_ledger) == 47
assert sum(record["size"] == 2 for record in minor_ledger) == 44
assert sum(record["size"] == 3 for record in minor_ledger) == 3
assert all(not record["exact_generator_up_to_sign"] and record["divisible_generators"] == 0 for record in minor_ledger)

hostiles = json.loads((HERE / "results_hostiles.json").read_text())
assert hostiles["status"] == "PASS_17_HOSTILES" and len(hostiles["tests"]) == 17 and all(hostiles["tests"].values())

result = {
    "schema": "KRENN_X5_REP5_SMALLEST66_SECOND_FACTOR_REFEREE_V1",
    "status": "PASS_EXACT_SECOND_FACTOR_COVER_DESIGN_ONLY",
    "input_sha256": sha(SOURCE),
    "design_sha256": sha(HERE / "results_design.json"),
    "coordinate": pivot_name,
    "factor_count": factor_count,
    "source_hashes": {"D": sha(D_path), "V": sha(V_path)},
    "source_sizes": {"D": [67, 3592, 137579], "V": [65, 3483, 128231]},
    "grading_rank": 66,
    "grading_nullity": 0,
    "linear_rank": 39,
    "component_sizes": [66],
    "minor_tests": 47,
    "forward_reverse_reconstructed": True,
    "hostiles": 17,
    "singular_runs": 0,
    "ideal_solves": 0,
    "closure_added": False,
}
tmp = HERE / "results_referee.json.tmp"
tmp.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
tmp.replace(HERE / "results_referee.json")
print(json.dumps({key: result[key] for key in ("status", "coordinate", "factor_count", "source_sizes", "minor_tests", "hostiles", "singular_runs")}, sort_keys=True))
