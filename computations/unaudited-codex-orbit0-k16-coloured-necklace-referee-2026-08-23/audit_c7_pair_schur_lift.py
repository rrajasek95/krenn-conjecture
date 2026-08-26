#!/usr/bin/env python3
"""Lift the eight-row target through common-parent source syzygies."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from math import gcd, lcm
from pathlib import Path
import sys
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C6_DIR = ROOT / "computations/unaudited-codex-orbit0-k16-c6-schur-boundary-2026-08-23"
C6_SCRIPT = C6_DIR / "audit_k16_c6_schur_boundary.py"
SCHUR = HERE / "results_c6_boundary_schur_lift.json"
RELATIVE = HERE / "results_unpivotable_c7_boundary.json"
OUT = HERE / "results_c7_pair_schur_lift.json"
LEDGER = HERE / "c7_pair_schur_lift_coefficients.tsv"
OUT_REDUCED = HERE / "results_c7_certified_reduction.json"
LEDGER_REDUCED = HERE / "c7_certified_reduction_coefficients.tsv"
RESIDUAL_REDUCED = HERE / "c7_certified_reduction_residual.tsv"
TIME_CAP = 175.0
ROW_CAP = 100_000


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


def primitive_with_scale(vector):
    divisor = 0
    for value in vector:
        divisor = gcd(divisor, abs(value))
    require(divisor, vector)
    reduced = tuple(value // divisor for value in vector)
    sign = 1 if next(value for value in reduced if value) > 0 else -1
    return tuple(sign * value for value in reduced), Fraction(sign, divisor)


def exact_solution(vectors, target):
    basis = {}
    for column_index, source in enumerate(vectors):
        value = {row: Fraction(coefficient)
                 for row, coefficient in enumerate(source) if coefficient}
        combination = {column_index: Fraction(1)}
        while value:
            pivot = min(value)
            if pivot not in basis:
                scale = value[pivot]
                basis[pivot] = (
                    {row: coefficient / scale for row, coefficient in value.items()},
                    {index: coefficient / scale
                     for index, coefficient in combination.items()})
                break
            scale = value[pivot]
            old_value, old_combination = basis[pivot]
            for row, coefficient in old_value.items():
                updated = value.get(row, 0) - scale * coefficient
                if updated:
                    value[row] = updated
                else:
                    value.pop(row, None)
            for index, coefficient in old_combination.items():
                updated = combination.get(index, 0) - scale * coefficient
                if updated:
                    combination[index] = updated
                else:
                    combination.pop(index, None)
    remainder = {row: Fraction(coefficient)
                 for row, coefficient in enumerate(target) if coefficient}
    solution = Counter()
    while remainder:
        pivot = min(remainder)
        require(pivot in basis, ("target outside span", pivot))
        scale = remainder[pivot]
        value, combination = basis[pivot]
        for row, coefficient in value.items():
            updated = remainder.get(row, 0) - scale * coefficient
            if updated:
                remainder[row] = updated
            else:
                remainder.pop(row, None)
        for index, coefficient in combination.items():
            solution[index] += scale * coefficient
    return Counter({key: value for key, value in solution.items() if value}), len(basis)


def remove_cells(row, cells):
    remaining = list(row)
    for cell in cells:
        remaining.remove(cell)
    return bytes(sorted(remaining))


def main():
    started = time.monotonic()
    reduce_c7 = "--reduce-c7" in sys.argv
    output_path = OUT_REDUCED if reduce_c7 else OUT
    ledger_path = LEDGER_REDUCED if reduce_c7 else LEDGER
    C6 = load("c7_pair_lift_c6", C6_SCRIPT)
    HQ, D24 = C6.HQ, C6.D24
    schur = json.loads(SCHUR.read_text())
    relative = json.loads(RELATIVE.read_text())
    require(relative["logical_sha256"] ==
            "f0a879fbf0e7a25574f37bc1ef0c164e15fb66bb37f41896468a418423b8743c",
            relative["logical_sha256"])
    rows = tuple(bytes.fromhex(record["row"])
                 for record in schur["uncertified_high_rows"])
    row_index = {row: index for index, row in enumerate(rows)}
    target = tuple(Fraction(record["coefficient"])
                   for record in schur["uncertified_high_rows"])
    require(len(row_index) == 8, len(row_index))

    all_columns = tuple(sorted({column for row in rows
                                for column in D24.incident_degree24_columns(row)},
                               key=lambda value: (value[0], value[1])))
    require(len(all_columns) == 278, len(all_columns))
    full_columns = []
    vectors = []
    parent_incidence = defaultdict(dict)
    occurrences = 0
    for column_index, column in enumerate(all_columns):
        literal = Counter()
        projected = Counter()
        for output in D24.degree24_column_rows(column):
            if D24.row_k_degree(output) > 16:
                continue
            occurrences += 1
            literal[output] += 1
            canonical = HQ.canonical_row(output)
            if canonical in row_index:
                projected[row_index[canonical]] += 1
            if len(C6.graph_data(output)[0]) > 7:
                parent_incidence[output][column_index] = (
                    parent_incidence[output].get(column_index, 0) + 1)
        full_columns.append(literal)
        vectors.append(tuple(projected.get(index, 0) for index in range(8)))
    require(occurrences <= ROW_CAP, occurrences)

    pairs = {}
    for parent, incidence in parent_incidence.items():
        items = sorted(incidence.items())
        for left_position, (left_index, lc) in enumerate(items):
            for right_index, rc in items[left_position + 1:]:
                raw = tuple(rc * vectors[left_index][coordinate]
                            - lc * vectors[right_index][coordinate]
                            for coordinate in range(8))
                if not any(raw):
                    continue
                vector, scale = primitive_with_scale(raw)
                pairs.setdefault(vector, {
                    "parent": parent,
                    "left_index": left_index,
                    "right_index": right_index,
                    "left_parent_coefficient": lc,
                    "right_parent_coefficient": rc,
                    "primitive_scale": scale,
                })
    pair_vectors = tuple(sorted(pairs))
    require(len(pair_vectors) == 5, len(pair_vectors))
    solution, rank = exact_solution(pair_vectors, target)
    require(rank == 4 and len(solution) <= 4, (rank, solution))
    require(tuple(sum(solution.get(index, 0) * vector[coordinate]
                      for index, vector in enumerate(pair_vectors))
                  for coordinate in range(8)) == target,
            "pair solution replay failed")

    combination = Counter()
    coefficient_rows = []
    for vector_index, solution_coefficient in sorted(solution.items()):
        record = pairs[pair_vectors[vector_index]]
        factor = solution_coefficient * record["primitive_scale"]
        left_factor = factor * record["right_parent_coefficient"]
        right_factor = -factor * record["left_parent_coefficient"]
        for output, coefficient in full_columns[record["left_index"]].items():
            combination[HQ.canonical_row(output)] += left_factor * coefficient
        for output, coefficient in full_columns[record["right_index"]].items():
            combination[HQ.canonical_row(output)] += right_factor * coefficient
        coefficient_rows.extend((
            ("pair-left", left_factor,
             HQ.column_key(all_columns[record["left_index"]])),
            ("pair-right", right_factor,
             HQ.column_key(all_columns[record["right_index"]])),
        ))
    combination = Counter({row: value for row, value in combination.items() if value})
    residual = Counter({row: target[index] for index, row in enumerate(rows)})
    for row, coefficient in combination.items():
        residual[row] -= coefficient
    residual = Counter({row: value for row, value in residual.items() if value})
    require(all(residual.get(row, 0) == 0 for row in rows),
            "eight-coordinate lift failed")
    exterior_before = len(residual)

    projected_cache = {}

    def projected_column(column):
        value = projected_cache.get(column)
        if value is None:
            value = Counter()
            for output in D24.degree24_column_rows(column):
                if D24.row_k_degree(output) <= 16:
                    value[HQ.canonical_row(output)] += 1
            projected_cache[column] = value
        return value

    pivot_uses = 0
    blocked_high = set()
    while True:
        candidates = []
        for row, coefficient in residual.items():
            cycles = len(C6.graph_data(row)[0])
            if cycles >= (7 if reduce_c7 else 8) and row not in blocked_high:
                candidates.append((cycles, row, coefficient))
        if not candidates:
            break
        cycles, row, coefficient = max(candidates,
                                       key=lambda item: (item[0], item[1]))
        pivot = C6.eligible_pivot(row)
        if pivot is None:
            blocked_high.add(row)
            continue
        word, selected = pivot
        column = (word, remove_cells(row, selected))
        column_value = projected_column(column)
        parent_coefficient = column_value[row]
        require(parent_coefficient > 0, (row.hex(), parent_coefficient))
        require(all(len(C6.graph_data(child)[0]) < cycles
                    for child in column_value if child != row),
                ("nontriangular pivot", row.hex()))
        factor = coefficient / parent_coefficient
        for child, value in column_value.items():
            residual[child] -= factor * value
            if residual[child] == 0:
                del residual[child]
        coefficient_rows.append(("c>7-pivot", factor, HQ.column_key(column)))
        pivot_uses += 1
        require(len(residual) <= ROW_CAP, ("row cap", len(residual)))
        require(time.monotonic() - started < TIME_CAP,
                ("time cap", pivot_uses, len(residual)))

    profile = Counter((D24.row_k_degree(row), len(C6.graph_data(row)[0]))
                      for row in residual)
    frontier = [(row, coefficient) for row, coefficient in residual.items()
                if len(C6.graph_data(row)[0]) >= 7]
    ledger_payload = "kind\tcoefficient\tcolumn\n" + "".join(
        f"{kind}\t{coefficient}\t{column}\n"
        for kind, coefficient, column in coefficient_rows)
    ledger_path.write_text(ledger_payload)
    residual_payload = "\n".join(
        f"{row.hex()}\t{coefficient}" for row, coefficient in sorted(residual.items())) + "\n"
    if reduce_c7:
        RESIDUAL_REDUCED.write_text("row\tcoefficient\n" + residual_payload)
    first_boundary_data = json.loads(
        (C6_DIR / "results_k16_c6_schur_boundary.json").read_text())
    first_boundary = {HQ.canonical_row(bytes.fromhex(record["row"]))
                      for record in first_boundary_data["blockers"]}
    first_boundary_overlap = sorted(set(residual) & first_boundary)
    result = {
        "schema": ("orbit0-k16-c7-certified-reduction-v1" if reduce_c7 else
                   "orbit0-k16-c7-common-parent-schur-lift-v1"),
        "status": ("EXACT_C7_CERTIFIED_REDUCTION_TO_C_LE_6" if reduce_c7 else
                   "EXACT_PAIR_LIFT_WITH_NEXT_FRONTIER"),
        "reduction_min_cycle_count": 7 if reduce_c7 else 8,
        "common_parent_pair_vectors": len(pair_vectors),
        "pair_rank_over_Q": rank,
        "solution_nonzero_pairs": len(solution),
        "solution_max_numerator": max(abs(value.numerator)
                                      for value in solution.values()),
        "solution_lcm_denominator": lcm(
            *(value.denominator for value in solution.values())),
        "exterior_support_before_c_gt_7_reduction": exterior_before,
        "certified_c_gt_7_pivot_uses": pivot_uses,
        "unpivotable_c_gt_7_support": len(blocked_high),
        "remaining_support": len(residual),
        "remaining_profile_K_degree_cycle_count": {
            f"{degree},{cycles}": count
            for (degree, cycles), count in sorted(profile.items())
        },
        "remaining_c_ge_7_support": len(frontier),
        "remaining_c7_support": sum(1 for row in residual
                                    if len(C6.graph_data(row)[0]) == 7),
        "prior_28_c6_boundary_exact_H_orbit_overlap": len(first_boundary_overlap),
        "prior_28_c6_boundary_overlap_rows": [row.hex()
                                                for row in first_boundary_overlap],
        "frontier_rows": [
            {
                "row": row.hex(),
                "coefficient": str(coefficient),
                "K_degree": D24.row_k_degree(row),
                "cycle_count": len(C6.graph_data(row)[0]),
            }
            for row, coefficient in sorted(frontier)
        ],
        "lex_first_frontier_row": min((row.hex() for row, _ in frontier),
                                      default=None),
        "remaining_residual_sha256": sha256(residual_payload.encode()).hexdigest(),
        "exported_residual_tsv_sha256": (
            sha256(RESIDUAL_REDUCED.read_bytes()).hexdigest() if reduce_c7 else None),
        "coefficient_ledger_sha256": sha256(ledger_payload.encode()).hexdigest(),
        "scope": (
            "One exact lift through the rank-4 common-parent pair span, then "
            f"only certified c>={'7' if reduce_c7 else '8'} triangular pivots "
            "in the K<=16 H-coinvariant quotient. The surviving lower frontier "
            "is unresolved; direct rank-8 fills were deliberately not used."
        ),
        "pinned": {
            "schur_logical": schur["logical_sha256"],
            "relative_interface_logical": relative["logical_sha256"],
        },
        "elapsed_seconds": time.monotonic() - started,
    }
    logical = dict(result)
    logical.pop("elapsed_seconds")
    result["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in (
        "status", "solution_nonzero_pairs",
        "exterior_support_before_c_gt_7_reduction",
        "certified_c_gt_7_pivot_uses", "unpivotable_c_gt_7_support",
        "remaining_support", "remaining_c_ge_7_support",
        "remaining_c7_support", "remaining_profile_K_degree_cycle_count",
        "logical_sha256", "elapsed_seconds")}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
