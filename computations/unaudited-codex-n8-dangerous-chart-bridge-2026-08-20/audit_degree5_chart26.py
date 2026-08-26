#!/usr/bin/env python3
"""Exact invariant K-degree-five lift for chart 26 / legacy chart 29.

The 16-element stabilizer of the twelve named anchors is used only as an
exact rational quotient.  Every quotient solution is expanded as the
average of all sixteen literal transforms and replayed over Q on actual
monomial rows.  Modular arithmetic is discovery only.

Conclusion on success: ``H0 H1 H2 in I_mix + K^6``.  This still does not
control the full localized chart; degrees six through twelve remain.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROBE_PATH = HERE / "probe_degree5_chart26_orbit.py"
SPEC = importlib.util.spec_from_file_location("degree5_probe", PROBE_PATH)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)
BASE = PROBE.BASE
OUT = HERE / "results_degree5_chart26.json"
P = 1009
EXPECTED_RESULT_SHA256 = (
    "2c7e35f08ed2932cd99e4df4deb603625f55439281a69ac15759f7ad9b412f5c"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


@lru_cache(maxsize=None)
def row_orbit(row):
    return tuple(sorted({bytes(sorted(transform[cell] for cell in row))
                         for transform in PROBE.TRANSFORMS}))


@lru_cache(maxsize=None)
def row_orbit_size(row):
    return len(row_orbit(row))


def reduce_vector(vector, basis):
    vector = {i: value % P for i, value in vector.items() if value % P}
    for pivot in sorted(basis):
        if pivot not in vector:
            continue
        value = vector[pivot]
        base = basis[pivot][0]
        for i, entry in base.items():
            new = (vector.get(i, 0) - value * entry) % P
            if new:
                vector[i] = new
            else:
                vector.pop(i, None)
    return vector


def build_basis(vectors, stop_rank=None):
    """Return pivot -> (normalized vector, combination in input vectors)."""
    basis = {}
    for number, raw in enumerate(vectors):
        vector = {i: value % P for i, value in raw.items() if value % P}
        combination = {number: 1}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in basis:
                inverse = pow(value, -1, P)
                vector = {i: entry * inverse % P
                          for i, entry in vector.items()}
                combination = {i: entry * inverse % P
                               for i, entry in combination.items()}
                basis[pivot] = (vector, combination)
                break
            base_vector, base_combination = basis[pivot]
            for i, entry in base_vector.items():
                new = (vector.get(i, 0) - value * entry) % P
                if new:
                    vector[i] = new
                else:
                    vector.pop(i, None)
            for i, entry in base_combination.items():
                new = (combination.get(i, 0) - value * entry) % P
                if new:
                    combination[i] = new
                else:
                    combination.pop(i, None)
        if stop_rank is not None and len(basis) == stop_rank:
            break
    return basis


def solve_with_basis(target, basis):
    residual = {i: value % P for i, value in target.items() if value % P}
    solution = {}
    while residual:
        pivot = min(residual)
        require(pivot in basis, "target is outside the modular image")
        value = residual[pivot]
        base_vector, base_combination = basis[pivot]
        for i, entry in base_vector.items():
            new = (residual.get(i, 0) - value * entry) % P
            if new:
                residual[i] = new
            else:
                residual.pop(i, None)
        for i, entry in base_combination.items():
            new = (solution.get(i, 0) + value * entry) % P
            if new:
                solution[i] = new
            else:
                solution.pop(i, None)
    return {i: value if value <= P // 2 else value - P
            for i, value in solution.items()}


def invariant_column_vector(column, representatives, degrees):
    """Scaled invariant quotient: count outputs in each row orbit."""
    index = {row: i for i, row in enumerate(representatives)}
    answer = Counter()
    for output in BASE.column_rows(column):
        if BASE.row_degree(output, PROBE.ANCHORS) not in degrees:
            continue
        representative = PROBE.canonical_row(output)
        if representative in index:
            answer[index[representative]] += 1
    return answer


def expand_average(certificate, degrees):
    """Expand coefficients on invariant average columns to actual rows."""
    answer = Counter()
    group_order = len(PROBE.STABILIZER)
    for coefficient, column in certificate:
        for action in range(group_order):
            transformed = PROBE.transform_column(column, action)
            for row in BASE.column_rows(transformed):
                if BASE.row_degree(row, PROBE.ANCHORS) in degrees:
                    answer[row] += coefficient / group_order
    return Counter({row: value for row, value in answer.items() if value})


def target_actual(degrees):
    answer = Counter()
    if 0 in degrees:
        answer[bytes(sorted(PROBE.ANCHORS))] = Fraction(1)
    for degree in degrees:
        if degree:
            answer.update({row: Fraction(value)
                           for row, value in BASE.filtered_target(
                               PROBE.MATCHINGS, degree
                           ).items()})
    return answer


def audit():
    lower, records = PROBE.lower_through_degree4()
    target5 = BASE.filtered_target(PROBE.MATCHINGS, 5)
    actual_start = set(target5)
    for column in lower:
        actual_start.update(row for row in BASE.column_rows(column)
                            if BASE.row_degree(row, PROBE.ANCHORS) == 5)
    rows5 = {PROBE.canonical_row(row) for row in actual_start}
    frontier = set(rows5)
    columns5 = set()
    while frontier:
        new_rows = set()
        for row in frontier:
            for raw_column in BASE.incident_columns(row):
                column = PROBE.canonical_column(raw_column)
                if column in columns5:
                    continue
                if BASE.column_minimum_degree(column, PROBE.ANCHORS) != 5:
                    continue
                columns5.add(column)
                for output in BASE.column_rows(column):
                    if BASE.row_degree(output, PROBE.ANCHORS) != 5:
                        continue
                    representative = PROBE.canonical_row(output)
                    if representative not in rows5:
                        rows5.add(representative)
                        new_rows.add(representative)
        frontier = new_rows
    require((len(rows5), len(columns5)) == (16515, 53228),
            "degree-five orbit closure changed")

    singleton = {}
    triples = []
    for column in sorted(columns5, key=repr):
        outputs = tuple(PROBE.canonical_row(row)
                        for row in BASE.column_rows(column)
                        if BASE.row_degree(row, PROBE.ANCHORS) == 5)
        if len(outputs) == 1:
            singleton.setdefault(outputs[0], column)
        else:
            require(len(outputs) == 3,
                    "degree-five column left the 1/3 leading split")
            triples.append((outputs, column))
    non_singleton = tuple(sorted(set(rows5) - set(singleton)))
    non_index = {row: i for i, row in enumerate(non_singleton)}
    triple_vectors = []
    triple_columns = []
    for outputs, column in triples:
        vector = Counter(non_index[row] for row in outputs
                         if row in non_index)
        if vector:
            triple_vectors.append(vector)
            triple_columns.append(column)
    triple_basis = build_basis(triple_vectors)
    quotient_indices = tuple(i for i in range(len(non_singleton))
                             if i not in triple_basis)
    print(
        "degree-five coupled quotient:", len(non_singleton),
        len(triple_basis), len(quotient_indices), flush=True,
    )
    quotient_position = {index: pos for pos, index in enumerate(quotient_indices)}

    # Lower orbit rows and columns through K-degree four.
    lower_degrees = (0, 2, 3, 4)
    lower_rows = {bytes(sorted(PROBE.ANCHORS))}
    for degree in (2, 3, 4):
        lower_rows.update(PROBE.canonical_row(row) for row in records[degree][0])
    lower_rows = tuple(sorted(lower_rows))
    lower_index = {row: i for i, row in enumerate(lower_rows)}
    lower_columns = tuple(sorted({PROBE.canonical_column(column)
                                  for column in lower}, key=repr))

    augmented_vectors = []
    for column in lower_columns:
        vector = Counter()
        for output in BASE.column_rows(column):
            degree = BASE.row_degree(output, PROBE.ANCHORS)
            representative = PROBE.canonical_row(output)
            if degree in lower_degrees:
                vector[lower_index[representative]] += 1
        tail = Counter(non_index[PROBE.canonical_row(output)]
                       for output in BASE.column_rows(column)
                       if BASE.row_degree(output, PROBE.ANCHORS) == 5
                       and PROBE.canonical_row(output) in non_index)
        remainder = reduce_vector(tail, triple_basis)
        for index, value in remainder.items():
            require(index in quotient_position,
                    "triple reduction left a pivot coordinate")
            vector[len(lower_rows) + quotient_position[index]] += value
        augmented_vectors.append(vector)

    target_lower_actual = target_actual(lower_degrees)
    augmented_target = Counter()
    for row in lower_rows:
        augmented_target[lower_index[row]] = (
            target_lower_actual[row] * row_orbit_size(row)
        )
    target5_scaled = Counter()
    for row, value in target5.items():
        representative = PROBE.canonical_row(row)
        if row == representative and representative in non_index:
            target5_scaled[non_index[representative]] = (
                Fraction(value) * row_orbit_size(representative)
            )
    target_remainder = reduce_vector(target5_scaled, triple_basis)
    for index, value in target_remainder.items():
        require(index in quotient_position,
                "target reduction left a triple pivot")
        augmented_target[len(lower_rows) + quotient_position[index]] = value

    augmented_basis = build_basis(augmented_vectors)
    lower_solution = solve_with_basis(augmented_target, augmented_basis)
    lower_certificate = tuple(
        (Fraction(value), lower_columns[index])
        for index, value in sorted(lower_solution.items())
    )
    replay_lower = expand_average(lower_certificate, lower_degrees)
    require(replay_lower == target_lower_actual,
            "centered lower quotient solution failed exact Q replay")

    current5 = expand_average(lower_certificate, (5,))
    target5_actual = target_actual((5,))
    residual5 = Counter(target5_actual)
    residual5.subtract(current5)
    residual5 = Counter({row: value for row, value in residual5.items() if value})
    residual_scaled = Counter()
    for representative in rows5:
        residual_scaled[representative] = (
            residual5[representative] * row_orbit_size(representative)
        )

    non_target = Counter({non_index[row]: residual_scaled[row]
                          for row in non_singleton if residual_scaled[row]})
    triple_solution = solve_with_basis(non_target, triple_basis)
    triple_certificate = tuple(
        (Fraction(value), triple_columns[index])
        for index, value in sorted(triple_solution.items())
    )
    for coefficient, column in triple_certificate:
        for output in BASE.column_rows(column):
            representative = PROBE.canonical_row(output)
            if BASE.row_degree(output, PROBE.ANCHORS) == 5:
                residual_scaled[representative] -= coefficient
    require(not any(residual_scaled[row] for row in non_singleton),
            "triple certificate left a coupled degree-five row")
    singleton_certificate = []
    for row in sorted(singleton):
        if residual_scaled[row]:
            singleton_certificate.append((residual_scaled[row], singleton[row]))
    certificate = lower_certificate + triple_certificate + tuple(singleton_certificate)
    replay = expand_average(certificate, (0, 2, 3, 4, 5))
    expected = target_actual((0, 2, 3, 4, 5))
    require(replay == expected,
            "full invariant degree-five certificate failed exact Q replay")
    negative = next((item for item in certificate if item[0] < 0), None)
    require(negative is not None, "degree-five certificate has no negative term")
    mutated = list(certificate)
    index = mutated.index(negative)
    mutated[index] = (-negative[0], negative[1])
    require(expand_average(tuple(mutated), (0, 2, 3, 4, 5)) != expected,
            "negative degree-five sign mutation did not fire")

    ledger = []
    for coefficient, column in certificate:
        ledger.append({
            "coefficient_on_orbit_average": str(coefficient),
            "word": BASE.word_name(column[0]),
            "multiplier": [BASE.cell_name(BASE.CELLS[cell])
                           for cell in column[1]],
            "column_orbit_size": len(PROBE.column_orbit(column)),
            "minimum_K_degree": BASE.column_minimum_degree(
                column, PROBE.ANCHORS
            ),
        })
    core = {
        "status": "UNAUDITED exact invariant filtered identity",
        "chart": 26,
        "legacy_one_based_chart": 29,
        "stabilizer_order": len(PROBE.STABILIZER),
        "degree5_row_column_orbits": [len(rows5), len(columns5)],
        "min_degree5_coupled_quotient": {
            "non_singleton_rows": len(non_singleton),
            "triple_rank_mod_1009": len(triple_basis),
            "quotient_dimension": len(quotient_indices),
        },
        "augmented_lower_system": {
            "lower_row_orbits": len(lower_rows),
            "lower_column_orbits": len(lower_columns),
            "rows_with_degree5_quotient": len(lower_rows) + len(quotient_indices),
            "rank_mod_1009": len(augmented_basis),
        },
        "certificate": {
            "lower_terms": len(lower_certificate),
            "triple_terms": len(triple_certificate),
            "singleton_terms": len(singleton_certificate),
            "total_orbit_average_terms": len(certificate),
            "coefficient_histogram": dict(sorted(Counter(
                str(value) for value, _column in certificate
            ).items())),
            "exact_rational_actual_row_replay": True,
            "negative_sign_mutation_fired": True,
            "terms": ledger,
        },
        "conclusion": "H0*H1*H2 belongs to I_mix + K^6 over Q",
        "full_localized_chart_controlled": False,
        "remaining_K_degrees": [6, 7, 8, 9, 10, 11, 12],
    }
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    require(digest == EXPECTED_RESULT_SHA256,
            "frozen degree-five exact-result digest changed")
    core["result_sha256"] = digest
    return core


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    result = audit()
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("chart26 exact degree-five audit: PASS")
    print("certificate terms:",
          result["certificate"]["total_orbit_average_terms"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
