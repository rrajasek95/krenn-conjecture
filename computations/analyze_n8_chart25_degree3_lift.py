#!/usr/bin/env python3
"""Fixed-continuation test for the chart-25 off-carrier degree-three tail."""

from collections import Counter
from fractions import Fraction
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "analyze_n8_chart25_degree2_lift.py"
SPEC = importlib.util.spec_from_file_location("n8_chart25_degree2", BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)
QQ = Fraction
PRIME = 1009
DEGREE = 3


def close_leading(start_rows):
    rows = set(start_rows)
    frontier = set(start_rows)
    columns = set()
    layers = []
    while frontier:
        new_rows = set()
        before = len(columns)
        for position, row in enumerate(frontier, 1):
            for raw_column in BASE.incident_columns(row):
                column = BASE.canonical_column(raw_column)
                if (column in columns
                        or BASE.column_minimum_degree(column) != DEGREE):
                    continue
                columns.add(column)
                for output in BASE.column_rows(column):
                    if BASE.row_degree(output) == DEGREE:
                        representative = BASE.canonical_row(output)
                        if representative not in rows:
                            new_rows.add(representative)
            if position % 1000 == 0:
                print("scan", position, "/", len(frontier),
                      "new rows", len(new_rows), "columns", len(columns),
                      flush=True)
        rows.update(new_rows)
        frontier = new_rows
        layers.append((len(new_rows), len(columns) - before))
        print("layer", len(layers), layers[-1],
              "totals", len(rows), len(columns), flush=True)
    return tuple(sorted(rows)), tuple(sorted(columns, key=repr)), tuple(layers)


def invariant_entries(column, row_index):
    entries = Counter()
    for actual_column in BASE.column_orbit(column):
        for row in BASE.column_rows(actual_column):
            if BASE.row_degree(row) == DEGREE and row == BASE.canonical_row(row):
                entries[row_index[row]] += 1
    return dict(entries)


def modular_membership(rows, columns, residual):
    row_index = {row: index for index, row in enumerate(rows)}
    pivots = {}
    leading_counts = Counter()
    singleton_columns = 0
    for position, column in enumerate(columns, 1):
        entries = invariant_entries(column, row_index)
        singleton_columns += len(entries) == 1
        leading_counts[min(entries)] += 1
        vector = {index: value % PRIME for index, value in entries.items()
                  if value % PRIME}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                inverse = pow(value, -1, PRIME)
                pivots[pivot] = {index: coefficient * inverse % PRIME
                                 for index, coefficient in vector.items()}
                break
            for index, coefficient in pivots[pivot].items():
                new = (vector.get(index, 0) - value * coefficient) % PRIME
                if new:
                    vector[index] = new
                else:
                    vector.pop(index, None)
        if position % 1000 == 0:
            print("eliminate", position, "/", len(columns),
                  "rank", len(pivots), flush=True)
    target = {
        row_index[row]: (-value.numerator
                         * pow(value.denominator, -1, PRIME)) % PRIME
        for row, value in residual.items()
    }
    while target:
        pivot = min(target)
        if pivot not in pivots:
            break
        value = target[pivot]
        for index, coefficient in pivots[pivot].items():
            new = (target.get(index, 0) - value * coefficient) % PRIME
            if new:
                target[index] = new
            else:
                target.pop(index, None)
    leading = {
        "singleton_columns": singleton_columns,
        "duplicate_leading_rows": sum(value > 1
                                       for value in leading_counts.values()),
        "columns_on_duplicate_leading_rows": sum(
            value for value in leading_counts.values() if value > 1
        ),
        "maximum_shared_leading_columns": max(leading_counts.values()),
    }
    return len(pivots), target, leading


def degree2_correction():
    _, quotient = BASE.averaged_degree2_residual()
    rows, columns, _ = BASE.close_leading(quotient)
    return BASE.exact_solve(rows, columns, quotient)


def main():
    correction = degree2_correction()
    actual, quotient = BASE.corrected_residual_at_degree(DEGREE, correction)
    print("degree3 corrected residual actual", len(actual),
          "orbits", len(quotient), "values", Counter(quotient.values()),
          flush=True)
    rows, columns, layers = close_leading(quotient)
    rank, remainder, leading = modular_membership(rows, columns, quotient)
    print({
        "rows": len(rows), "columns": len(columns), "layers": layers,
        "rank_mod_1009": rank,
        "fixed_continuation_consistent": not remainder,
        "remainder_support": len(remainder),
        **leading,
    })


if __name__ == "__main__":
    main()
