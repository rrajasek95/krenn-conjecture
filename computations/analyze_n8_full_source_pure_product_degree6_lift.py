#!/usr/bin/env python3
"""Compact residual-led degree-six frontier after the exact n=8 degree-5 lift."""

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
import importlib.util
import json
import pickle
from pathlib import Path


HERE = Path(__file__).resolve().parent
D5_PATH = HERE / "verify_n8_full_source_pure_product_degree5_lift.py"
SPEC = importlib.util.spec_from_file_location("n8_degree5", D5_PATH)
D5 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(D5)

STATE5_PATH = "/tmp/n8_degree5_compact_state.pkl"
STATE6_PATH = "/tmp/n8_degree6_compact_state.pkl"
QQ = Fraction


VERTEX_MASK = tuple(
    (1 << coordinate[0]) | (1 << coordinate[1])
    for coordinate in D5.COORDINATES
)


def incident_columns(row):
    decoded = [D5.COORDINATES[value] for value in row]
    for selected in combinations(range(12), 4):
        mask = 0
        for index in selected:
            mask |= VERTEX_MASK[row[index]]
        if mask != 0xff:
            continue
        word = [None] * 8
        for index in selected:
            left, right, left_colour, right_colour = decoded[index]
            word[left] = left_colour
            word[right] = right_colour
        if len(set(word)) == 1:
            continue
        selected_set = frozenset(selected)
        multiplier = bytes(row[index] for index in range(12)
                           if index not in selected_set)
        yield D5.word_code(word), multiplier


def pure_target_rows(maximum_degree):
    terms_by_colour_degree = []
    for colour in D5.SOURCE.COLOURS:
        groups = defaultdict(list)
        for term in D5.iter_word_terms(D5.word_code((colour,) * 8)):
            groups[D5.row_degree(term)].append(term)
        terms_by_colour_degree.append(groups)
    actual = set()
    canonical = set()
    for degrees in product(range(maximum_degree + 1), repeat=3):
        if sum(degrees) > maximum_degree:
            continue
        groups = [terms_by_colour_degree[colour].get(degree, ())
                  for colour, degree in enumerate(degrees)]
        for terms in product(*groups):
            row = bytes(sorted(sum((tuple(term) for term in terms), ())))
            if row in actual:
                raise RuntimeError("pure target multiplicity")
            actual.add(row)
            canonical.add(D5.canonical_row(row))
    return actual, canonical


def certificate_columns():
    certificate = json.loads(D5.CERTIFICATE_PATH.read_bytes())
    for item in certificate["solution"]:
        column = (
            D5.word_code(tuple(item["word"])),
            bytes(D5.COORDINATE_ID[tuple(variable)]
                  for variable in item["multiplier"]),
        )
        yield column, QQ(item["numerator"], item["denominator"])


def exact_degree6_tail():
    actual, canonical = pure_target_rows(6)
    target = {row for row in canonical if D5.row_degree(row) == 6}
    residual = Counter({row: QQ(-1) for row in target})
    actual_columns = 0
    streamed_terms = 0
    for position, (column, scalar) in enumerate(certificate_columns(), 1):
        for actual_column in D5.column_orbit(column):
            actual_columns += 1
            for output in D5.iter_column_outputs(actual_column):
                if D5.row_degree(output) != 6:
                    continue
                streamed_terms += 1
                if output == D5.canonical_row(output):
                    residual[output] += scalar
        if position % 1000 == 0:
            print("tail", position, "/7861 residual", len(residual), flush=True)
    residual = {row: value for row, value in residual.items() if value}
    print("degree6 exact tail: target actual", sum(D5.row_degree(row) == 6
          for row in actual), "orbits", len(target), "actual columns",
          actual_columns, "terms", streamed_terms, "residual", len(residual),
          "coefficients", sorted(set(residual.values())), flush=True)
    return residual, target


def seed_all_previous_tails(previous_columns, target):
    rows = set(target)
    for position, column in enumerate(previous_columns, 1):
        for output in D5.iter_column_outputs(column):
            if D5.row_degree(output) == 6:
                rows.add(D5.canonical_row(output))
        if position % 10000 == 0:
            print("previous tails", position, "/", len(previous_columns),
                  "rows", len(rows), flush=True)
    return rows


def close_degree6(start_rows):
    rows = set(start_rows)
    frontier = set(start_rows)
    columns = set()
    layers = []
    while frontier:
        new_rows = set()
        new_columns = 0
        for position, row in enumerate(frontier, 1):
            for raw_column in incident_columns(row):
                column = D5.canonical_column(raw_column)
                if column in columns or D5.column_minimum_degree(column) != 6:
                    continue
                columns.add(column)
                new_columns += 1
                for output in D5.iter_column_outputs(column):
                    if D5.row_degree(output) == 6:
                        representative = D5.canonical_row(output)
                        if representative not in rows:
                            new_rows.add(representative)
            if position % 5000 == 0:
                print("closure", position, "/", len(frontier),
                      "newrows", len(new_rows), "cols", len(columns), flush=True)
        rows.update(new_rows)
        frontier = new_rows
        layers.append((len(new_rows), new_columns))
        print("degree6 layer", len(layers), layers[-1],
              "totals", len(rows), len(columns), flush=True)
    return rows, columns, layers


def main():
    with open(STATE5_PATH, "rb") as source:
        state5 = pickle.load(source)
    previous_columns = set(state5["low_columns"]) | set(state5["coupled_columns"])
    if len(previous_columns) != 224153:
        raise RuntimeError("degree-five coupled column census changed")
    residual, target = exact_degree6_tail()
    # First solve the fixed-tail leading problem.  Raw union of every earlier
    # column tail has 776,193 rows before closure; Schur/Bockstein coupling is
    # applied only after extracting a leading dual.
    rows, columns, layers = close_degree6(residual)
    print("degree6 fixed-tail closure", len(rows), len(columns), layers, flush=True)
    with open(STATE6_PATH, "wb") as output:
        pickle.dump({
            "degree6_tail": residual,
            "degree6_target": target,
            "degree6_rows": rows,
            "degree6_columns": columns,
            "degree6_layers": layers,
            "raw_coupled_seed_rows": 776193,
        }, output, protocol=5)
    print("checkpointed", STATE6_PATH, flush=True)


if __name__ == "__main__":
    main()
