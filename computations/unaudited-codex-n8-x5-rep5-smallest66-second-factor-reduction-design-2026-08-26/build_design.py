#!/usr/bin/env python3
"""Exact symbolic census and second factor cover for the rep5 66-variable branch."""
from __future__ import annotations

import copy
import hashlib
import itertools
import json
import os
import re
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COMP = ROOT / "computations"
PARENT = COMP / "unaudited-codex-n8-x5-rep5-smallest67-factor-determinant-reduction-design-2026-08-26"
SOURCE = PARENT / "sources/V_a24_00_Q_design.sing"
PINS = {
    PARENT / "MANIFEST.sha256": "0a8a9dcfdda319822a8776e287dfb7e713cbd3617086db048816ecd9b0547c2f",
    PARENT / "results_design.json": "b41bf2cf68395e1e0782c5dbe642e411df69c9f0bf79b47dd9cc2c218c2e636d",
    PARENT / "results_referee.json": "6ce2bdc6364fa10aff1a4e20e83abd41157a63b725bbebcd277c9b5495507f63",
    SOURCE: "4821a045e6f4c799a002a9d097c7353857b8058f4dfdb01b1048d09b5dcd6927",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


for pinned_path, digest in PINS.items():
    assert sha(pinned_path) == digest, (pinned_path, sha(pinned_path), digest)


def atomic(path: Path, value: object) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)


def split(path: Path) -> tuple[list[str], list[str]]:
    text = path.read_text()
    variables = text.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
    body = text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
    return variables, body.split(",\n")


names, raw_expressions = split(SOURCE)
inverse_name = "inv_second_factor"
universe = names + [inverse_name]
index = {name: i for i, name in enumerate(universe)}


def parse(path: Path) -> tuple[list[str], list[dict[tuple[int, ...], int]]]:
    ring, expressions = split(path)
    parsed = []
    for expression in expressions:
        polynomial: dict[tuple[int, ...], int] = {}
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
        parsed.append(polynomial)
    return ring, parsed


ring, polynomials = parse(SOURCE)
assert ring == names and len(names) == 66 and len(polynomials) == 3591
assert len(polynomials) == len({tuple(sorted(polynomial.items())) for polynomial in polynomials})


def canonical(values: list[dict[tuple[int, ...], int]]) -> list[dict[tuple[int, ...], int]]:
    answer = []
    seen = set()
    for value in values:
        value = {monomial: coefficient for monomial, coefficient in value.items() if coefficient}
        if not value:
            continue
        if len(value) == 1 and () in value:
            return [{(): 1}]
        key = tuple(sorted(value.items()))
        if key not in seen:
            seen.add(key)
            answer.append(value)
    return answer


def specialize(values, variable: int, scalar: int):
    answer = []
    for polynomial in values:
        reduced = {}
        for monomial, coefficient in polynomial.items():
            if scalar == 0 and variable in monomial:
                continue
            target = tuple(i for i in monomial if not (scalar == 1 and i == variable))
            reduced[target] = reduced.get(target, 0) + coefficient
        answer.append(reduced)
    return canonical(answer)


def rank_mod(rows: list[dict[int, int]], prime: int) -> int:
    echelon = {}
    for source_row in rows:
        row = {column: value % prime for column, value in source_row.items() if value % prime}
        while row:
            pivot = min(row)
            if pivot not in echelon:
                inverse = pow(row[pivot], -1, prime)
                echelon[pivot] = {column: value * inverse % prime for column, value in row.items()}
                break
            factor = row[pivot]
            known = echelon[pivot]
            row = {
                column: (row.get(column, 0) - factor * known.get(column, 0)) % prime
                for column in set(row) | set(known)
            }
            row = {column: value for column, value in row.items() if value}
    return len(echelon)


def rank_q(rows: list[dict[int, int]]) -> int:
    echelon = {}
    for source_row in rows:
        row = {column: Fraction(value) for column, value in source_row.items() if value}
        while row:
            pivot = min(row)
            if pivot not in echelon:
                scale = row[pivot]
                echelon[pivot] = {column: value / scale for column, value in row.items()}
                break
            factor = row[pivot]
            known = echelon[pivot]
            row = {
                column: row.get(column, Fraction()) - factor * known.get(column, Fraction())
                for column in set(row) | set(known)
            }
            row = {column: value for column, value in row.items() if value}
    return len(echelon)


grading_rows = []
linear_rows = []
active = set()
affine = 0
monic = []
factor_counts = {name: 0 for name in names}
adjacency = [set() for _ in names]
for equation, polynomial in enumerate(polynomials):
    monomials = sorted(polynomial)
    base = Counter(monomials[0])
    for monomial in monomials[1:]:
        current = Counter(monomial)
        row = {i: base[i] - current[i] for i in set(base) | set(current) if base[i] != current[i]}
        if row:
            grading_rows.append(row)
    support = {i for monomial in polynomial for i in monomial}
    active |= support
    affine += max(map(len, polynomial)) <= 1
    linear = {monomial[0]: coefficient for monomial, coefficient in polynomial.items() if len(monomial) == 1}
    if linear:
        linear_rows.append(linear)
    for i in support:
        adjacency[i] |= support - {i}
        if all(i in monomial for monomial in polynomial):
            factor_counts[names[i]] += 1
        if abs(polynomial.get((i,), 0)) == 1 and all(i not in monomial for monomial in polynomial if monomial != (i,)):
            monic.append([equation, names[i]])

grading_mod = [rank_mod(grading_rows, prime) for prime in (32003, 65521)]
assert grading_mod == [66, 66]
linear_mod = [rank_mod(linear_rows, prime) for prime in (32003, 65521)]
linear_exact = rank_q(linear_rows)
assert linear_mod == [linear_exact, linear_exact]
assert active == set(range(66)) and affine == 0 and not monic

unseen = set(range(66))
components = []
while unseen:
    todo = deque([min(unseen)])
    component = set()
    while todo:
        vertex = todo.popleft()
        if vertex in component:
            continue
        component.add(vertex)
        todo.extend(adjacency[vertex] - component)
    unseen -= component
    components.append(component)
assert [len(component) for component in components] == [66]

# Exhaustive literal 2x2-minor / complete-determinant census of every available matrix block.
cells_by_stem = {}
for name in names:
    match = re.fullmatch(r"(a\d+)_([012])([012])", name)
    if match:
        cells_by_stem.setdefault(match[1], {})[(int(match[2]), int(match[3]))] = index[name]


def sign(permutation):
    return -1 if sum(permutation[i] > permutation[j] for i in range(len(permutation)) for j in range(i + 1, len(permutation))) % 2 else 1


def determinant(cells, rows, columns):
    answer = {}
    for permutation in itertools.permutations(columns):
        monomial = tuple(sorted(cells[(row, column)] for row, column in zip(rows, permutation)))
        positions = tuple(columns.index(column) for column in permutation)
        answer[monomial] = answer.get(monomial, 0) + sign(positions)
    return {monomial: coefficient for monomial, coefficient in answer.items() if coefficient}


minor_candidates = []
for stem, cells in sorted(cells_by_stem.items()):
    for rows in itertools.combinations(range(3), 2):
        for columns in itertools.combinations(range(3), 2):
            if all((row, column) in cells for row in rows for column in columns):
                minor_candidates.append((f"{stem}_minor_{rows[0]}{rows[1]}_{columns[0]}{columns[1]}", stem, 2, determinant(cells, rows, columns)))
    if len(cells) == 9:
        minor_candidates.append((f"{stem}_det", stem, 3, determinant(cells, range(3), range(3))))


def exponent(monomial):
    return tuple(monomial.count(i) for i in range(66))


def lead(polynomial):
    return max(polynomial, key=lambda monomial: (len(monomial), exponent(monomial)))


def divide_monomial(dividend, divisor):
    work = list(dividend)
    for value in divisor:
        work.remove(value)
    return tuple(work)


def divisible_by(polynomial, divisor):
    work = {monomial: Fraction(coefficient) for monomial, coefficient in polynomial.items()}
    leading_divisor = lead(divisor)
    leading_coefficient = divisor[leading_divisor]
    while work:
        leading = lead(work)
        if any(x < y for x, y in zip(exponent(leading), exponent(leading_divisor))):
            return False
        quotient = divide_monomial(leading, leading_divisor)
        coefficient = work[leading] / leading_coefficient
        for monomial, value in divisor.items():
            target = tuple(sorted(quotient + monomial))
            work[target] = work.get(target, Fraction()) - coefficient * value
            if not work[target]:
                del work[target]
    return True


generator_keys = {tuple(sorted(polynomial.items())) for polynomial in polynomials}
minor_ledger = []
for candidate_name, stem, size, divisor in minor_candidates:
    key = tuple(sorted(divisor.items()))
    negative = tuple(sorted((monomial, -coefficient) for monomial, coefficient in divisor.items()))
    minor_ledger.append({
        "name": candidate_name,
        "block": stem,
        "size": size,
        "terms": len(divisor),
        "exact_generator_up_to_sign": key in generator_keys or negative in generator_keys,
        "divisible_generators": sum(divisible_by(polynomial, divisor) for polynomial in polynomials),
    })
assert minor_ledger and all(not item["exact_generator_up_to_sign"] and item["divisible_generators"] == 0 for item in minor_ledger)


def stats(ring_names, values):
    allowed = {index[name] for name in ring_names}
    used = {i for polynomial in values for monomial in polynomial for i in monomial if i in allowed}
    return {
        "variables": len(ring_names),
        "generators": len(values),
        "total_terms": sum(map(len, values)),
        "degree_mass": sum(len(monomial) for polynomial in values for monomial in polynomial),
        "maximum_terms": max(map(len, values)),
        "inactive": sorted(set(ring_names) - {universe[i] for i in used}),
        "unit_structural": values == [{(): 1}],
    }


factor_candidates = []
for name, count in factor_counts.items():
    if count:
        zero = specialize(polynomials, index[name], 0)
        zero_stats = stats([candidate for candidate in names if candidate != name], zero)
        factor_candidates.append({
            "coordinate": name,
            "divisible_generators": count,
            "zero_generators": zero_stats["generators"],
            "zero_terms": zero_stats["total_terms"],
            "zero_degree_mass": zero_stats["degree_mass"],
            "objective": [-count, zero_stats["total_terms"], zero_stats["generators"], name],
        })
assert factor_candidates
choice = min(factor_candidates, key=lambda item: tuple(item["objective"]))
pivot_name = choice["coordinate"]
pivot = index[pivot_name]
divided = []
divided_count = 0
for polynomial in polynomials:
    if all(pivot in monomial for monomial in polynomial):
        divided_count += 1
        quotient = {}
        for monomial, coefficient in polynomial.items():
            work = list(monomial)
            work.remove(pivot)
            quotient[tuple(work)] = coefficient
        divided.append(quotient)
    else:
        divided.append(polynomial)
assert divided_count == choice["divisible_generators"]
inverse = index[inverse_name]
D = canonical(divided + [{(): 1, tuple(sorted((pivot, inverse))): -1}])
V = specialize(polynomials, pivot, 0)


def serialize(polynomial):
    pieces = []
    for monomial, coefficient in sorted(polynomial.items(), key=lambda item: (len(item[0]), item[0])):
        factors = "*".join(universe[i] for i in monomial)
        magnitude = abs(coefficient)
        body = str(magnitude) if not factors else factors if magnitude == 1 else f"{magnitude}*{factors}"
        pieces.append((("-" if coefficient < 0 else "+") if pieces else ("-" if coefficient < 0 else "")) + body)
    return "".join(pieces)


def write_source(path, ring_names, values, comment):
    text = "\n".join([
        "// EXACT Q DESIGN INPUT ONLY: no Singular/ideal run authorized.",
        "// " + comment,
        "option(noredefine);",
        f"ring r=0,({','.join(ring_names)}),dp;",
        "ideal I=" + ",\n".join(serialize(polynomial) for polynomial in values) + ";",
        'print("INPUT_VARIABLES="+string(nvars(r)));',
        'print("INPUT_GENERATORS="+string(size(I)));',
        "quit;",
        "",
    ])
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text)
    os.replace(tmp, path)


source_dir = HERE / "sources"
source_dir.mkdir(exist_ok=True)
for stale in source_dir.glob("*.sing"):
    stale.unlink()
specifications = [
    ("D", names + [inverse_name], D, f"D({pivot_name}): invert and divide {divided_count} complete coordinate factors."),
    ("V", [name for name in names if name != pivot_name], V, f"V({pivot_name}): set {pivot_name}=0 literally."),
]
source_records = []
for kind, ring_names, values, comment in specifications:
    path = source_dir / f"{kind}_{pivot_name}_Q_design.sing"
    write_source(path, ring_names, values, comment)
    rebuilt_ring, rebuilt = parse(path)
    assert rebuilt_ring == ring_names and rebuilt == values
    removed = [name for name in names if name not in ring_names]
    ideal_body = path.read_text().split("ideal I=", 1)[1]
    assert all(not re.search(rf"\b{re.escape(name)}\b", ideal_body) for name in removed)
    source_records.append({
        "kind": kind,
        "path": str(path.relative_to(HERE)),
        "sha256": sha(path),
        "bytes": path.stat().st_size,
        "removed_identifiers": removed,
        **stats(ring_names, values),
    })
assert source_records[1]["variables"] == 65
assert source_records[1]["generators"] < len(polynomials)
assert source_records[1]["total_terms"] < sum(map(len, polynomials))

result = {
    "schema": "KRENN_X5_REP5_SMALLEST66_SECOND_FACTOR_REDUCTION_DESIGN_V1",
    "status": "PASS_EXACT_SECOND_FACTOR_COVER_NO_TORUS_MONIC_OR_LITERAL_MINOR_REDUCTION",
    "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
    "input": {"sha256": PINS[SOURCE], **stats(names, polynomials)},
    "grading": {"constraint_rows": len(grading_rows), "modular_ranks": grading_mod, "rank_over_Q": 66, "nullity_over_Q": 0},
    "linear_rank": {"rows_with_linear_part": len(linear_rows), "modular_ranks": linear_mod, "exact_rank_over_Q": linear_exact},
    "inactive_monic": {"inactive_coordinates": [], "affine_linear_generators": affine, "unit_monic_graph_substitutions": monic},
    "block_structure": {"components": 1, "component_sizes": [66]},
    "factor_structure": {
        "complete_factor_counts": factor_counts,
        "nonzero_coordinates": len(factor_candidates),
        "maximum_count": max(factor_counts.values()),
        "candidate_ledger": factor_candidates,
    },
    "minor_rank_split": {
        "available_candidates": len(minor_ledger),
        "two_by_two_minors": sum(item["size"] == 2 for item in minor_ledger),
        "three_by_three_determinants": sum(item["size"] == 3 for item in minor_ledger),
        "exact_generator_matches": 0,
        "exact_generator_factors": 0,
        "strict_smaller_literal_rank_split_found": False,
        "scope": "literal equality/divisibility only; no ideal-membership or radical-membership claim",
        "candidate_ledger": minor_ledger,
    },
    "selected_cover": {
        "identity": "D(x) union V(x)",
        "selected_coordinate": pivot_name,
        "divisible_generators": divided_count,
        "forward_D": "adjoin inv*x=1 and divide every x-multiple generator by x",
        "reverse_D": "forget unique inv=1/x and multiply divided generators by x",
        "forward_V": "set x=0 literally",
        "root_free": True,
        "exhaustive": True,
        "strictly_smaller_V_branch": True,
        "sources": source_records,
    },
    "scope": {"singular_runs": 0, "ideal_solves": 0, "mathematical_coverage_added": False, "rep5_closed": False},
}
atomic(HERE / "results_design.json", result)


def validate(value):
    assert value["status"] == "PASS_EXACT_SECOND_FACTOR_COVER_NO_TORUS_MONIC_OR_LITERAL_MINOR_REDUCTION"
    assert value["input"]["sha256"] == PINS[SOURCE] and value["grading"]["rank_over_Q"] == 66 and value["grading"]["nullity_over_Q"] == 0
    assert not value["inactive_monic"]["inactive_coordinates"] and not value["inactive_monic"]["unit_monic_graph_substitutions"]
    assert value["block_structure"]["component_sizes"] == [66] and value["minor_rank_split"]["available_candidates"] == len(minor_ledger)
    assert value["minor_rank_split"]["exact_generator_matches"] == value["minor_rank_split"]["exact_generator_factors"] == 0
    assert value["selected_cover"]["divisible_generators"] == divided_count and value["selected_cover"]["root_free"] and value["selected_cover"]["exhaustive"]
    assert value["selected_cover"]["strictly_smaller_V_branch"] and len(value["selected_cover"]["sources"]) == 2
    assert value["scope"]["singular_runs"] == 0 and value["scope"]["mathematical_coverage_added"] is False


mutations = [
    lambda value: value.__setitem__("status", "PASS"),
    lambda value: value["input"].__setitem__("sha256", "0" * 64),
    lambda value: value["grading"].__setitem__("rank_over_Q", 65),
    lambda value: value["grading"].__setitem__("nullity_over_Q", 1),
    lambda value: value["inactive_monic"]["inactive_coordinates"].append("fake"),
    lambda value: value["inactive_monic"]["unit_monic_graph_substitutions"].append("fake"),
    lambda value: value["block_structure"].__setitem__("component_sizes", [65, 1]),
    lambda value: value["minor_rank_split"].__setitem__("available_candidates", 0),
    lambda value: value["minor_rank_split"].__setitem__("exact_generator_matches", 1),
    lambda value: value["minor_rank_split"].__setitem__("exact_generator_factors", 1),
    lambda value: value["selected_cover"].__setitem__("divisible_generators", divided_count - 1),
    lambda value: value["selected_cover"].__setitem__("root_free", False),
    lambda value: value["selected_cover"].__setitem__("exhaustive", False),
    lambda value: value["selected_cover"].__setitem__("strictly_smaller_V_branch", False),
    lambda value: value["selected_cover"]["sources"].pop(),
    lambda value: value["scope"].__setitem__("singular_runs", 1),
    lambda value: value["scope"].__setitem__("mathematical_coverage_added", True),
]
hostiles = {}
for number, mutation in enumerate(mutations, 1):
    value = copy.deepcopy(result)
    mutation(value)
    try:
        validate(value)
    except (AssertionError, KeyError, TypeError):
        hostiles[f"hostile_{number:02d}"] = True
    else:
        hostiles[f"hostile_{number:02d}"] = False
assert len(hostiles) == 17 and all(hostiles.values())
atomic(HERE / "results_hostiles.json", {
    "schema": "KRENN_X5_REP5_SMALLEST66_SECOND_FACTOR_HOSTILES_V1",
    "status": "PASS_17_HOSTILES",
    "tests": hostiles,
    "solver_runs": 0,
})
print(json.dumps({
    "status": result["status"],
    "grading": [66, 0],
    "linear_rank": linear_exact,
    "minor_tests": len(minor_ledger),
    "factor_choice": pivot_name,
    "sources": 2,
    "hostiles": 17,
    "solves": 0,
}, sort_keys=True))
