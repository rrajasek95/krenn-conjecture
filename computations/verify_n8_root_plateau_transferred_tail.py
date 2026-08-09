#!/usr/bin/env python3
"""Compute the first exact transferred tails below the 31-root plateau."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
MORSE_PATH = HERE / "verify_n8_chart_incidence_lex_morse.py"
SPEC = importlib.util.spec_from_file_location("n8_chart_morse", MORSE_PATH)
MORSE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MORSE)
SOURCE = MORSE.SOURCE
QQ = Fraction
EXPECTED_LEDGER_SHA256 = (
    "99b60126095523705554a78ac08c41b85230f7d255979e09b07e0531285e8c57"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add_scaled(target, source, scale):
    for index, coefficient in source.items():
        output = target.get(index, QQ(0)) + scale * coefficient
        if output:
            target[index] = output
        else:
            target.pop(index, None)


def replay(columns, representative):
    answer = {}
    for column, coefficient in representative.items():
        add_scaled(answer, columns[column], coefficient)
    return answer


def diagonal_count(row):
    return sum(
        first % 3 == second % 3
        for first, second in SOURCE.mate_edges(SOURCE.decode_key(row))
    )


def rank_mod_prime(columns, prime):
    basis = {}
    for source in columns:
        vector = {
            row: (coefficient.numerator
                  * pow(coefficient.denominator, -1, prime)) % prime
            for row, coefficient in source.items()
            if coefficient.numerator % prime
        }
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                inverse = pow(vector[pivot], -1, prime)
                basis[pivot] = {
                    row: coefficient * inverse % prime
                    for row, coefficient in vector.items()
                    if coefficient * inverse % prime
                }
                break
            scale = vector[pivot]
            for row, coefficient in basis[pivot].items():
                value = (vector.get(row, 0) - scale * coefficient) % prime
                if value:
                    vector[row] = value
                else:
                    vector.pop(row, None)
    return len(basis)


def encoded_tail(column):
    return tuple(
        (row, coefficient.numerator, coefficient.denominator)
        for row, coefficient in sorted(column.items())
    )


def audit():
    roots = tuple(sorted(SOURCE.target_orbit_rows()))
    require(len(roots) == 31, "target root orbit count changed")
    root_index = {row: index for index, row in enumerate(roots)}
    columns = tuple(sorted(set().union(*(
        SOURCE.incident_columns(row) for row in roots
    ))))
    require(len(columns) == 31, "root plateau column count changed")

    full_columns = []
    top_columns = []
    for column in columns:
        full = Counter(SOURCE.column_outputs(column))
        full_columns.append({row: QQ(value) for row, value in full.items()})
        top_columns.append({
            root_index[row]: QQ(value)
            for row, value in full.items() if row in root_index
        })

    # Repeat the frozen lex column reduction, retaining exact provenance.
    pivots = {}
    pivot_representatives = {}
    zero_representatives = {}
    for column_number, source in enumerate(top_columns):
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
            require(not replay(top_columns, representative),
                    "top-kernel provenance did not replay")
            zero_representatives[column_number] = representative

    require(len(pivots) == 24 and len(zero_representatives) == 7,
            "root plateau rank/nullity changed")
    transferred = tuple(
        replay(full_columns, representative)
        for _column, representative in sorted(zero_representatives.items())
    )
    require(all(tail for tail in transferred),
            "a top-kernel relation vanished in the full fibre module")
    require(all(not (set(tail) & set(roots)) for tail in transferred),
            "a transferred tail retained a diagonal-12 root")
    require(all(diagonal_count(row) < 12
                for tail in transferred for row in tail),
            "a transferred tail failed to lower diagonal degree")

    levels = tuple(sorted({
        diagonal_count(row) for tail in transferred for row in tail
    }, reverse=True))
    level_columns = {
        level: tuple({
            row: coefficient for row, coefficient in tail.items()
            if diagonal_count(row) == level
        } for tail in transferred)
        for level in levels
    }
    level_ranks = {
        level: rank_mod_prime(columns_at_level, 2147483647)
        for level, columns_at_level in level_columns.items()
    }
    tail_records = tuple(encoded_tail(tail) for tail in transferred)
    ledger = {
        "root_rows": len(roots),
        "root_columns": len(columns),
        "root_plateau_rank": len(pivots),
        "root_plateau_kernel_columns": len(zero_representatives),
        "root_plateau_kernel_source_column_indices": [
            column + 1 for column in sorted(zero_representatives)
        ],
        "transferred_tail_term_counts": [len(tail) for tail in transferred],
        "transferred_tail_total_terms": sum(map(len, transferred)),
        "transferred_diagonal_level_histogram": dict(sorted(Counter(
            diagonal_count(row)
            for tail in transferred for row in tail
        ).items(), reverse=True)),
        "transferred_unique_states_by_diagonal_level": {
            level: len(set().union(*(
                set(column) for column in columns_at_level
            )))
            for level, columns_at_level in level_columns.items()
        },
        "transferred_level_ranks_mod_2147483647": level_ranks,
        "transferred_tail_sha256": sha256(repr(tail_records).encode()).hexdigest(),
        "scope_guard": (
            "exact first transferred relations obtained by cancelling the "
            "entire diagonal-12 root plateau; lower-level plateaus have not "
            "yet been contracted"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "root plateau transferred-tail ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
