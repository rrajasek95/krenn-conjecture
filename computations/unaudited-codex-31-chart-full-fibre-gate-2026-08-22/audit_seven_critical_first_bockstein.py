#!/usr/bin/env python3
"""Compute the first source-labelled lift of the seven chart syzygies.

The 31 target-row/31 support-column incidence has rank 24 and seven exact
zero-column representatives.  This audit expands those representatives on
the literal matching outputs, builds the complete first-shell column packet,
and tests whether each tail belongs to that packet over two prime fields.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = ROOT / "computations" / "analyze_n8_full_s8s3_pure_product_membership.py"
SPEC = importlib.util.spec_from_file_location("matching_source", SOURCE_PATH)
SOURCE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(SOURCE)

QQ = Fraction
PRIMES = (1009, 1013)


def add_scaled(target, source, scale):
    for key, coefficient in source.items():
        value = target.get(key, QQ(0)) + scale * coefficient
        if value:
            target[key] = value
        else:
            target.pop(key, None)


def column_counter(column):
    return Counter(SOURCE.column_outputs(column))


def critical_representatives(target_rows, support_columns):
    row_index = {row: index for index, row in enumerate(target_rows)}
    incidence = []
    for column in support_columns:
        entries = Counter(
            row_index[row]
            for row in SOURCE.column_outputs(column)
            if row in row_index
        )
        incidence.append({row: QQ(value) for row, value in entries.items()})

    pivots = {}
    pivot_representatives = {}
    zeros = []
    for column_number, source in enumerate(incidence):
        vector = dict(source)
        representative = {column_number: QQ(1)}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                pivots[pivot] = {
                    row: coefficient / value
                    for row, coefficient in vector.items()
                }
                pivot_representatives[pivot] = {
                    column: coefficient / value
                    for column, coefficient in representative.items()
                }
                break
            add_scaled(vector, pivots[pivot], -value)
            add_scaled(representative, pivot_representatives[pivot], -value)
        if not vector:
            zeros.append(representative)
    if len(pivots) != 24 or len(zeros) != 7:
        raise RuntimeError("31-chart critical census changed")
    return tuple(zeros)


def literal_tail(representative, support_columns, target_set):
    tail = {}
    for column_number, coefficient in representative.items():
        add_scaled(tail, column_counter(support_columns[column_number]), coefficient)
    target_part = {row: value for row, value in tail.items() if row in target_set}
    if target_part:
        raise RuntimeError("critical source did not cancel its target rows")
    return tail


def modular_vector(vector, row_index, prime):
    answer = {}
    for row, coefficient in vector.items():
        value = (
            coefficient.numerator
            * pow(coefficient.denominator, -1, prime)
        ) % prime
        if value:
            answer[row_index[row]] = value
    return answer


def add_modular_basis(vector, basis, prime):
    vector = dict(vector)
    while vector:
        pivot = min(vector)
        value = vector[pivot]
        if pivot not in basis:
            inverse = pow(value, -1, prime)
            basis[pivot] = {
                row: coefficient * inverse % prime
                for row, coefficient in vector.items()
            }
            return True
        for row, coefficient in basis[pivot].items():
            new_value = (vector.get(row, 0) - value * coefficient) % prime
            if new_value:
                vector[row] = new_value
            else:
                vector.pop(row, None)
    return False


def reduce_modular(vector, basis, prime):
    vector = dict(vector)
    while vector:
        pivot = min(vector)
        value = vector[pivot]
        if pivot not in basis:
            break
        for row, coefficient in basis[pivot].items():
            new_value = (vector.get(row, 0) - value * coefficient) % prime
            if new_value:
                vector[row] = new_value
            else:
                vector.pop(row, None)
    return vector


def exact_column_basis(column_vectors, row_index):
    """Lex exact basis with source provenance in the original columns."""
    basis = {}
    provenance = {}
    for column_number, source in enumerate(column_vectors):
        vector = {row_index[row]: value for row, value in source.items()}
        representative = {column_number: QQ(1)}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in basis:
                basis[pivot] = {
                    row: coefficient / value for row, coefficient in vector.items()
                }
                provenance[pivot] = {
                    column: coefficient / value
                    for column, coefficient in representative.items()
                }
                break
            add_scaled(vector, basis[pivot], -value)
            add_scaled(representative, provenance[pivot], -value)
    return basis, provenance


def exact_coordinates(vector, basis, provenance, row_index):
    """Return coefficients expressing vector in the exact basis span."""
    remainder = {row_index[row]: value for row, value in vector.items()}
    coordinates = {}
    while remainder:
        pivot = min(remainder)
        value = remainder[pivot]
        if pivot not in basis:
            raise RuntimeError("tail left the exact first-shell column span")
        add_scaled(remainder, basis[pivot], -value)
        add_scaled(coordinates, provenance[pivot], value)
    return coordinates


def audit():
    target_rows = tuple(sorted(SOURCE.target_orbit_rows()))
    target_set = frozenset(target_rows)
    support_columns = tuple(sorted(set().union(*(
        SOURCE.incident_columns(row) for row in target_rows
    ))))
    if len(target_rows) != 31 or len(support_columns) != 31:
        raise RuntimeError("leading chart packet changed")
    representatives = critical_representatives(target_rows, support_columns)
    tails = tuple(
        literal_tail(representative, support_columns, target_set)
        for representative in representatives
    )

    first_rows = tuple(sorted(set().union(*(tail.keys() for tail in tails))))
    all_first_rows = tuple(sorted(
        set().union(*(column_counter(column) for column in support_columns))
        - target_set
    ))
    first_columns = tuple(sorted(
        set().union(*(SOURCE.incident_columns(row) for row in all_first_rows))
        - set(support_columns)
    ))
    if len(all_first_rows) != 570 or len(first_columns) != 741:
        raise RuntimeError("complete first matching shell changed")

    row_index = {row: index for index, row in enumerate(all_first_rows)}
    column_vectors = []
    for column in first_columns:
        entries = Counter(
            row for row in SOURCE.column_outputs(column) if row in row_index
        )
        column_vectors.append({row: QQ(value) for row, value in entries.items()})

    prime_ledgers = []
    for prime in PRIMES:
        basis = {}
        for vector in column_vectors:
            add_modular_basis(modular_vector(vector, row_index, prime), basis, prime)
        remainders = tuple(
            len(reduce_modular(modular_vector(tail, row_index, prime), basis, prime))
            for tail in tails
        )
        combined = dict(basis)
        augmented = tuple(
            add_modular_basis(modular_vector(tail, row_index, prime), combined, prime)
            for tail in tails
        )
        prime_ledgers.append({
            "prime": prime,
            "rank": len(basis),
            "tail_remainders": remainders,
            "tail_rank_increments": augmented,
            "augmented_rank": len(combined),
        })

    exact_basis, exact_provenance = exact_column_basis(column_vectors, row_index)
    if len(exact_basis) != 540:
        raise RuntimeError("exact first-shell rank disagrees with modular ranks")
    exact_solutions = tuple(
        exact_coordinates(tail, exact_basis, exact_provenance, row_index)
        for tail in tails
    )

    second_tails = []
    previous_rows = target_set | frozenset(all_first_rows)
    for representative, solution in zip(representatives, exact_solutions):
        corrected = {}
        for column_number, coefficient in representative.items():
            add_scaled(corrected, column_counter(support_columns[column_number]), coefficient)
        for column_number, coefficient in solution.items():
            add_scaled(corrected, column_counter(first_columns[column_number]), -coefficient)
        forbidden = {row: value for row, value in corrected.items() if row in previous_rows}
        if forbidden:
            raise RuntimeError("exact first-shell correction left an earlier row")
        second_tails.append(corrected)

    exact_coefficients = [
        coefficient
        for solution in exact_solutions
        for coefficient in solution.values()
    ]
    denominator_lcm = 1
    import math
    for coefficient in exact_coefficients:
        denominator_lcm = math.lcm(denominator_lcm, coefficient.denominator)

    return {
        "target_rows": len(target_rows),
        "support_columns": len(support_columns),
        "critical_sources": len(representatives),
        "critical_source_term_counts": tuple(map(len, representatives)),
        "critical_tail_rows": len(first_rows),
        "critical_tail_term_counts": tuple(map(len, tails)),
        "complete_first_rows": len(all_first_rows),
        "complete_first_columns": len(first_columns),
        "first_column_nonzeros": sum(map(len, column_vectors)),
        "prime_ledgers": prime_ledgers,
        "exact_rank": len(exact_basis),
        "exact_solution_term_counts": tuple(map(len, exact_solutions)),
        "exact_solution_denominator_lcm": denominator_lcm,
        "second_tail_rows": len(set().union(*(tail.keys() for tail in second_tails))),
        "second_tail_term_counts": tuple(map(len, second_tails)),
    }


def main():
    result = audit()
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
