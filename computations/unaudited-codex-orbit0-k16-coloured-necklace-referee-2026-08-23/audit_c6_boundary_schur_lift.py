#!/usr/bin/env python3
"""Lift one exact 28-coordinate solution and perform one certified Schur page."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from math import gcd
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C6_DIR = ROOT / "computations/unaudited-codex-orbit0-k16-c6-schur-boundary-2026-08-23"
C6_SCRIPT = C6_DIR / "audit_k16_c6_schur_boundary.py"
C6_RESULT = C6_DIR / "results_k16_c6_schur_boundary.json"
INTERFACE = C6_DIR / "boundary_incident_interface.json"
PAIR_RESULT = HERE / "results_c6_boundary_literal_critical_pairs.json"
OUT = HERE / "results_c6_boundary_schur_lift.json"
LEDGER = HERE / "c6_boundary_schur_lift_coefficients.tsv"
ROW_CAP = 250_000
TIME_CAP = 175.0


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
    """Return a sparse exact combination of vectors equal to target."""
    basis = {}
    for column_index, source in enumerate(vectors):
        value = {row: Fraction(coefficient)
                 for row, coefficient in enumerate(source) if coefficient}
        combination = {column_index: Fraction(1)}
        while value:
            pivot = min(value)
            if pivot not in basis:
                scale = value[pivot]
                value = {row: coefficient / scale
                         for row, coefficient in value.items()}
                combination = {index: coefficient / scale
                               for index, coefficient in combination.items()}
                basis[pivot] = (value, combination)
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
        require(pivot in basis, ("target outside pair span", pivot))
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
    solution = Counter({index: coefficient for index, coefficient in solution.items()
                        if coefficient})
    return solution, len(basis)


def remove_cells(row, cells):
    remaining = list(row)
    for cell in cells:
        remaining.remove(cell)
    return bytes(sorted(remaining))


def main():
    started = time.monotonic()
    C6 = load("schur_lift_c6", C6_SCRIPT)
    HQ, D24 = C6.HQ, C6.D24
    seed = json.loads(C6_RESULT.read_text())
    page = json.loads(INTERFACE.read_text())
    pair_result = json.loads(PAIR_RESULT.read_text())
    require(pair_result["logical_sha256"] ==
            "73f833a3404d2bc2f1a3a4162ba928e29497d458a08acf82c88ec903ff0bfee5",
            pair_result["logical_sha256"])

    literal_blockers = tuple(bytes.fromhex(record["row"])
                             for record in seed["blockers"])
    blockers = tuple(HQ.canonical_row(row) for row in literal_blockers)
    blocker_index = {row: index for index, row in enumerate(blockers)}
    require(len(blocker_index) == 28, len(blocker_index))
    target = tuple(Fraction(*record["target_mass"])
                   for record in seed["blockers"])

    column_vectors = {}
    high_parents = set()
    for record in page["columns"]:
        orbit_size = record["orbit_size"]
        vector = [0] * 28
        for row_hex, mass in record["entries"]:
            row = bytes.fromhex(row_hex)
            if row in blocker_index:
                require(mass % orbit_size == 0, (record["key"], row_hex))
                vector[blocker_index[row]] += mass // orbit_size
            if D24.row_k_degree(row) == 16 and len(C6.graph_data(row)[0]) >= 7:
                high_parents.add(row)
        column_vectors[record["key"]] = tuple(vector)
    require(len(high_parents) == 374, len(high_parents))

    zero = (0,) * 28
    pairs = {}
    for parent in sorted(high_parents):
        descriptors = []
        for column in sorted(set(D24.incident_degree24_columns(parent)),
                             key=lambda value: (value[0], value[1])):
            outputs = D24.degree24_column_rows(column)
            coefficient = sum(row == parent for row in outputs)
            require(coefficient > 0, (parent.hex(), column))
            canonical_key = HQ.column_key(HQ.canonical_column(column))
            descriptors.append((coefficient,
                                column_vectors.get(canonical_key, zero),
                                column, canonical_key))
        for left_index, left_record in enumerate(descriptors):
            lc, left, left_column, left_key = left_record
            for rc, right, right_column, right_key in descriptors[left_index + 1:]:
                raw = tuple(rc * x - lc * y
                            for x, y in zip(left, right, strict=True))
                if raw == zero:
                    continue
                vector, scale = primitive_with_scale(raw)
                pairs.setdefault(vector, {
                    "parent": parent,
                    "left": left_column,
                    "right": right_column,
                    "left_key": left_key,
                    "right_key": right_key,
                    "left_parent_coefficient": lc,
                    "right_parent_coefficient": rc,
                    "primitive_scale": scale,
                })
    vectors = tuple(sorted(pairs))
    require(len(vectors) == 102, len(vectors))
    solution, pair_rank = exact_solution(vectors, target)
    require(pair_rank == 28, pair_rank)
    require(len(solution) <= 28, len(solution))
    replay = [sum(solution.get(index, 0) * vector[row]
                  for index, vector in enumerate(vectors))
              for row in range(28)]
    require(tuple(replay) == target, (replay, target))

    column_cache = {}

    def column_projection(column):
        value = column_cache.get(column)
        if value is None:
            value = Counter()
            for row in D24.degree24_column_rows(column):
                if D24.row_k_degree(row) <= 16:
                    value[HQ.canonical_row(row)] += 1
            column_cache[column] = value
        return value

    combination = Counter()
    coefficient_ledger = []
    for vector_index, solution_coefficient in sorted(solution.items()):
        record = pairs[vectors[vector_index]]
        factor = solution_coefficient * record["primitive_scale"]
        left_factor = factor * record["right_parent_coefficient"]
        right_factor = -factor * record["left_parent_coefficient"]
        for row, coefficient in column_projection(record["left"]).items():
            combination[row] += left_factor * coefficient
        for row, coefficient in column_projection(record["right"]).items():
            combination[row] += right_factor * coefficient
        coefficient_ledger.append({
            "vector_index": vector_index,
            "solution": solution_coefficient,
            "primitive_scale": record["primitive_scale"],
            "parent": record["parent"].hex(),
            "left_column": HQ.column_key(record["left"]),
            "left_factor": left_factor,
            "right_column": HQ.column_key(record["right"]),
            "right_factor": right_factor,
        })
    combination = Counter({row: value for row, value in combination.items() if value})
    target_rows = Counter({row: target[index]
                           for index, row in enumerate(blockers) if target[index]})
    residual = Counter(target_rows)
    for row, coefficient in combination.items():
        residual[row] -= coefficient
    residual = Counter({row: value for row, value in residual.items() if value})
    require(all(residual.get(row, 0) == 0 for row in blockers),
            "28-coordinate solution did not lift")
    pre_reduction_support = len(residual)

    pivot_uses = 0
    pivot_coefficients = Counter()
    uncertified_high_rows = set()
    while True:
        candidates = []
        for row, coefficient in residual.items():
            cycles = len(C6.graph_data(row)[0])
            if cycles >= 7 and row not in uncertified_high_rows:
                candidates.append((cycles, row, coefficient))
        if not candidates:
            break
        cycles, row, coefficient = max(candidates, key=lambda item: (item[0], item[1]))
        pivot = C6.eligible_pivot(row)
        if pivot is None:
            uncertified_high_rows.add(row)
            continue
        word, selected = pivot
        column = (word, remove_cells(row, selected))
        projected = column_projection(column)
        parent_coefficient = projected[row]
        require(parent_coefficient > 0, (row.hex(), parent_coefficient))
        require(all(len(C6.graph_data(child)[0]) < cycles
                    for child, value in projected.items()
                    if child != row and value),
                ("nontriangular pivot", row.hex(), cycles))
        factor = coefficient / parent_coefficient
        for child, value in projected.items():
            residual[child] -= factor * value
            if residual[child] == 0:
                del residual[child]
        pivot_coefficients[HQ.column_key(column)] += factor
        pivot_uses += 1
        require(len(residual) <= ROW_CAP, ("row cap", len(residual)))
        require(time.monotonic() - started < TIME_CAP,
                ("time cap", pivot_uses, len(residual)))

    profile = Counter()
    for row in residual:
        profile[(D24.row_k_degree(row), len(C6.graph_data(row)[0]))] += 1
    high_profile = {key: value for key, value in profile.items() if key[1] >= 7}
    low_profile = {key: value for key, value in profile.items() if key[1] <= 6}
    require(sum(high_profile.values()) == len(uncertified_high_rows),
            (high_profile, len(uncertified_high_rows)))

    ledger_lines = ["kind\tcoefficient\tcolumn_or_parent"]
    for record in coefficient_ledger:
        ledger_lines.append(
            f"pair-left\t{record['left_factor']}\t{record['left_column']}")
        ledger_lines.append(
            f"pair-right\t{record['right_factor']}\t{record['right_column']}")
    for key, coefficient in sorted(pivot_coefficients.items()):
        if coefficient:
            ledger_lines.append(f"c>=7-pivot\t{coefficient}\t{key}")
    ledger_payload = "\n".join(ledger_lines) + "\n"
    LEDGER.write_text(ledger_payload)

    residual_digest_payload = "\n".join(
        f"{row.hex()}\t{coefficient}"
        for row, coefficient in sorted(residual.items())) + "\n"
    result = {
        "schema": "orbit0-k16-c6-boundary-schur-lift-v1",
        "status": ("EXACT_ONE_SCHUR_PAGE_WITH_UNCERTIFIED_HIGH_BOUNDARY"
                   if high_profile else
                   "EXACT_ONE_SCHUR_PAGE_WITH_C_LE_6_RESIDUAL"),
        "pair_vectors": len(vectors),
        "pair_rank_over_Q": pair_rank,
        "rational_solution_nonzero_pairs": len(solution),
        "rational_solution_max_numerator": max(abs(value.numerator)
                                               for value in solution.values()),
        "rational_solution_lcm_denominator": __import__("math").lcm(
            *(value.denominator for value in solution.values())),
        "lifted_source_columns": len(column_cache),
        "exterior_support_before_high_cycle_reduction": pre_reduction_support,
        "certified_high_cycle_pivot_uses": pivot_uses,
        "distinct_high_cycle_pivot_columns": sum(bool(value)
                                                  for value in pivot_coefficients.values()),
        "remaining_support": len(residual),
        "remaining_profile_K_degree_cycle_count": {
            f"{degree},{cycles}": count
            for (degree, cycles), count in sorted(profile.items())
        },
        "uncertified_high_cycle_support": sum(high_profile.values()),
        "uncertified_high_cycle_profile": {
            f"{degree},{cycles}": count
            for (degree, cycles), count in sorted(high_profile.items())
        },
        "lex_first_uncertified_high_row": (
            min(uncertified_high_rows).hex() if uncertified_high_rows else None),
        "uncertified_high_rows": [
            {
                "row": row.hex(),
                "coefficient": str(residual[row]),
                "K_degree": D24.row_k_degree(row),
                "cycle_count": len(C6.graph_data(row)[0]),
            }
            for row in sorted(uncertified_high_rows)
        ],
        "remaining_c_le_6_support": sum(low_profile.values()),
        "remaining_c_le_6_profile": {
            f"{degree},{cycles}": count
            for (degree, cycles), count in sorted(low_profile.items())
        },
        "remaining_coefficient_l1": str(sum(abs(value) for value in residual.values())),
        "remaining_max_numerator": max((abs(value.numerator)
                                        for value in residual.values()), default=0),
        "remaining_lcm_denominator": __import__("math").lcm(
            *(value.denominator for value in residual.values())) if residual else 1,
        "remaining_residual_sha256": sha256(
            residual_digest_payload.encode()).hexdigest(),
        "coefficient_ledger_sha256": sha256(ledger_payload.encode()).hexdigest(),
        "scope": (
            "One exact rational lift of the full-rank 28-coordinate boundary "
            "solution, followed only by source-faithful deterministic c>=7 "
            "pivots in the K<=16 H-coinvariant quotient. Unpivotable c>=7 "
            "rows and every c<=6 remainder are unresolved; no full membership "
            "or K16 closure is claimed."
        ),
        "pinned": {
            "pair_projection_logical": pair_result["logical_sha256"],
            "boundary_seed_logical": seed["logical_sha256"],
            "incident_interface_logical": page["logical_sha256"],
        },
        "elapsed_seconds": time.monotonic() - started,
    }
    logical = dict(result)
    logical.pop("elapsed_seconds")
    result["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in (
        "status", "rational_solution_nonzero_pairs",
        "exterior_support_before_high_cycle_reduction",
        "certified_high_cycle_pivot_uses", "remaining_support",
        "remaining_profile_K_degree_cycle_count", "logical_sha256",
        "elapsed_seconds")}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
