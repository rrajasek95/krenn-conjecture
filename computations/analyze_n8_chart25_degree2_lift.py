#!/usr/bin/env python3
"""Exact full-source degree-two lift of the chart-25 identity."""

from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import importlib.util
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
CHECKER_PATH = HERE / "verify_n8_chart25_pure_product_membership.py"
SPEC = importlib.util.spec_from_file_location("n8_chart25", CHECKER_PATH)
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)
FULL = CHECKER.FULL
QQ = Fraction
PRIME = 1009
EXPECTED_LEDGER_SHA256 = (
    "4857b72b9a8fda295b4a8694c15d937f811238d3b26e4b1994183924dc32f3f6"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def setup():
    CHECKER.DUAL.configure_chart25()
    functional = CHECKER.expanded_dual()
    allowed = frozenset(variable for row in functional for variable in row)
    coordinates = tuple(
        (left, right, left_colour, right_colour)
        for left, right in combinations(range(8), 2)
        for left_colour in range(3) for right_colour in range(3)
    )
    coordinate_id = {variable: index for index, variable in enumerate(coordinates)}
    allowed_ids = frozenset(coordinate_id[variable] for variable in allowed)
    transforms = tuple(bytes(
        coordinate_id[FULL.transform_variable(variable, group)]
        for variable in coordinates
    ) for group in FULL.SUPPORT_STABILIZER)
    return coordinates, coordinate_id, allowed_ids, transforms


COORDINATES, COORDINATE_ID, ALLOWED_IDS, TRANSFORMS = setup()
MATCHINGS = FULL.perfect_matchings(range(8))


def row_degree(row):
    return sum(variable not in ALLOWED_IDS for variable in row)


@lru_cache(maxsize=None)
def canonical_row(row):
    return min(bytes(sorted(transform[value] for value in row))
               for transform in TRANSFORMS)


@lru_cache(maxsize=None)
def column_orbit(column):
    word, multiplier = column
    answer = set()
    for group_index, (vertex_permutation, colour_permutation) in enumerate(
            FULL.SUPPORT_STABILIZER):
        transformed_word = [None] * 8
        for vertex in range(8):
            transformed_word[vertex_permutation[vertex]] = (
                colour_permutation[word[vertex]]
            )
        transformed_multiplier = bytes(sorted(
            TRANSFORMS[group_index][value] for value in multiplier
        ))
        answer.add((tuple(transformed_word), transformed_multiplier))
    return tuple(sorted(answer, key=repr))


def canonical_column(column):
    return column_orbit(column)[0]


@lru_cache(maxsize=None)
def word_terms(word):
    return tuple(bytes(sorted(
        COORDINATE_ID[FULL.edge(left, right, word[left], word[right])]
        for left, right in matching
    )) for matching in MATCHINGS)


@lru_cache(maxsize=None)
def column_rows(column):
    word, multiplier = column
    return tuple(bytes(sorted(multiplier + term)) for term in word_terms(word))


@lru_cache(maxsize=None)
def column_minimum_degree(column):
    return min(map(row_degree, column_rows(column)))


@lru_cache(maxsize=None)
def incident_columns(row):
    decoded = [COORDINATES[value] for value in row]
    answer = []
    for selected in combinations(range(12), 4):
        word = [None] * 8
        covered = []
        for index in selected:
            left, right, left_colour, right_colour = decoded[index]
            covered.extend((left, right))
            word[left] = left_colour
            word[right] = right_colour
        if len(set(covered)) != 8 or len(set(word)) == 1:
            continue
        selected_set = frozenset(selected)
        multiplier = bytes(row[index] for index in range(12)
                           if index not in selected_set)
        answer.append((tuple(word), multiplier))
    return tuple(answer)


def seed_columns():
    functional = CHECKER.expanded_dual()
    allowed = frozenset(variable for row in functional for variable in row)
    extras = tuple(sorted(allowed - FULL.SUPPORT_SET))
    normalized = (
        (), (extras[2], extras[11]), (extras[15], extras[18]),
        (extras[2], extras[11], extras[15], extras[18]),
    )
    columns = []
    for monomial in normalized:
        multiplier = monomial + CHECKER.support_completion(
            monomial, CHECKER.MIXED_WORD
        )
        columns.append((
            CHECKER.MIXED_WORD,
            bytes(sorted(COORDINATE_ID[variable] for variable in multiplier)),
        ))
    return tuple(columns)


def averaged_degree2_residual():
    residual = defaultdict(QQ)
    for seed in seed_columns():
        for column in column_orbit(seed):
            scalar = QQ(1, len(column_orbit(seed)))
            for row in column_rows(column):
                if row_degree(row) == 2:
                    residual[row] += scalar
    pure_groups = []
    for colour in range(3):
        groups = defaultdict(list)
        for row in word_terms((colour,) * 8):
            groups[row_degree(row)].append(row)
        pure_groups.append(groups)
    for degrees in product(range(3), repeat=3):
        if sum(degrees) != 2:
            continue
        for terms in product(*(pure_groups[colour][degrees[colour]]
                               for colour in range(3))):
            residual[bytes(sorted(b"".join(terms)))] -= 1
    residual = {row: value for row, value in residual.items() if value}
    for row, value in residual.items():
        for transform in TRANSFORMS:
            image = bytes(sorted(transform[index] for index in row))
            if residual.get(image) != value:
                raise RuntimeError("averaged chart25 tail is not invariant")
    quotient = {}
    for row, value in residual.items():
        representative = canonical_row(row)
        if row == representative:
            quotient[row] = value
    return residual, quotient


def corrected_residual_at_degree(degree, correction):
    """Return the full invariant tail after applying the degree-two lift."""
    residual = defaultdict(QQ)
    for seed in seed_columns():
        orbit = column_orbit(seed)
        scalar = QQ(1, len(orbit))
        for column in orbit:
            for row in column_rows(column):
                if row_degree(row) == degree:
                    residual[row] += scalar
    for representative, scalar in correction.items():
        for column in column_orbit(representative):
            for row in column_rows(column):
                if row_degree(row) == degree:
                    residual[row] += scalar
    pure_groups = []
    for colour in range(3):
        groups = defaultdict(list)
        for row in word_terms((colour,) * 8):
            groups[row_degree(row)].append(row)
        pure_groups.append(groups)
    for degrees in product(range(degree + 1), repeat=3):
        if sum(degrees) != degree:
            continue
        for terms in product(*(pure_groups[colour].get(degrees[colour], ())
                               for colour in range(3))):
            residual[bytes(sorted(b"".join(terms)))] -= 1
    residual = {row: value for row, value in residual.items() if value}
    quotient = {}
    for row, value in residual.items():
        for transform in TRANSFORMS:
            image = bytes(sorted(transform[index] for index in row))
            if residual.get(image) != value:
                raise RuntimeError("corrected chart25 tail is not invariant")
        representative = canonical_row(row)
        if row == representative:
            quotient[row] = value
    return residual, quotient


def close_leading(start_rows):
    rows = set(start_rows)
    frontier = set(start_rows)
    columns = set()
    layers = []
    while frontier:
        new_rows = set()
        before = len(columns)
        for position, row in enumerate(frontier, 1):
            for raw_column in incident_columns(row):
                column = canonical_column(raw_column)
                if column in columns or column_minimum_degree(column) != 2:
                    continue
                columns.add(column)
                for output in column_rows(column):
                    if row_degree(output) == 2:
                        representative = canonical_row(output)
                        if representative not in rows:
                            new_rows.add(representative)
            if position % 5000 == 0:
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
    for actual_column in column_orbit(column):
        for row in column_rows(actual_column):
            if row_degree(row) == 2 and row == canonical_row(row):
                entries[row_index[row]] += 1
    return dict(entries)


def modular_membership(rows, columns, residual):
    row_index = {row: index for index, row in enumerate(rows)}
    pivots = {}
    for position, column in enumerate(columns, 1):
        vector = {index: value % PRIME for index, value in
                  invariant_entries(column, row_index).items() if value % PRIME}
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
        if position % 5000 == 0:
            print("eliminate", position, "/", len(columns),
                  "rank", len(pivots), flush=True)
    target = {
        row_index[row]: (-value.numerator * pow(value.denominator, -1, PRIME)) % PRIME
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
    return len(pivots), target


def exact_solve(rows, columns, residual):
    row_index = {row: index for index, row in enumerate(rows)}
    equations = [dict() for _ in rows]
    for column_index, column in enumerate(columns):
        for index, value in invariant_entries(column, row_index).items():
            equations[index][column_index] = QQ(value)
    pivots = {}
    for position, (row, coefficients) in enumerate(zip(rows, equations), 1):
        coefficients = dict(coefficients)
        rhs = -residual.get(row, QQ(0))
        while coefficients:
            pivot = min(coefficients)
            value = coefficients[pivot]
            if pivot not in pivots:
                coefficients = {index: coefficient / value
                                for index, coefficient in coefficients.items()}
                rhs /= value
                pivots[pivot] = coefficients, rhs
                break
            pivot_row, pivot_rhs = pivots[pivot]
            for index, coefficient in pivot_row.items():
                new = coefficients.get(index, QQ(0)) - value * coefficient
                if new:
                    coefficients[index] = new
                else:
                    coefficients.pop(index, None)
            rhs -= value * pivot_rhs
        else:
            if rhs:
                raise RuntimeError("exact chart25 degree2 system inconsistent")
        if position % 500 == 0:
            print("exact rows", position, "/", len(rows),
                  "pivots", len(pivots), flush=True)
    solution = [QQ(0)] * len(columns)
    for pivot in sorted(pivots, reverse=True):
        pivot_row, rhs = pivots[pivot]
        solution[pivot] = rhs - sum(
            coefficient * solution[index]
            for index, coefficient in pivot_row.items() if index != pivot
        )
    for row, coefficients in zip(rows, equations):
        value = sum(solution[index] * coefficient
                    for index, coefficient in coefficients.items())
        if value != -residual.get(row, QQ(0)):
            raise RuntimeError("exact chart25 degree2 solution replay failed")
    return {columns[index]: value for index, value in enumerate(solution) if value}


def correction_encoding(correction):
    return [
        {
            "word": "".join(map(str, word)),
            "multiplier": list(multiplier),
            "numerator": value.numerator,
            "denominator": value.denominator,
        }
        for (word, multiplier), value in sorted(correction.items(), key=repr)
    ]


def leading_statistics(rows, columns):
    row_index = {row: index for index, row in enumerate(rows)}
    supports = [invariant_entries(column, row_index) for column in columns]
    leading_counts = Counter(min(entries) for entries in supports)
    return {
        "singleton_columns": sum(len(entries) == 1 for entries in supports),
        "duplicate_leading_rows": sum(value > 1 for value in leading_counts.values()),
        "columns_on_duplicate_leading_rows": sum(
            value for value in leading_counts.values() if value > 1
        ),
        "maximum_shared_leading_columns": max(leading_counts.values()),
    }


def main():
    actual, quotient = averaged_degree2_residual()
    print("degree2 averaged residual actual", len(actual),
          "orbits", len(quotient), "values", Counter(quotient.values()), flush=True)
    rows, columns, layers = close_leading(quotient)
    rank, remainder = modular_membership(rows, columns, quotient)
    require(not remainder, "chart25 degree-two tail failed modulo 1009")
    correction = exact_solve(rows, columns, quotient)
    values = Counter(correction.values())
    denominator_lcm = math.lcm(*(
        value.denominator for value in correction.values()
    ))
    corrected_actual, corrected_quotient = corrected_residual_at_degree(
        2, correction
    )
    require(not corrected_actual and not corrected_quotient,
            "chart25 exact degree-two correction failed full replay")
    leading = leading_statistics(rows, columns)
    ledger = {
        "actual_residual_rows": len(actual),
        "residual_row_orbits": len(quotient),
        "row_orbits": len(rows),
        "column_orbits": len(columns),
        "closure_layers": layers,
        "rank_mod_1009": rank,
        "correction_support": len(correction),
        "correction_denominator_lcm": denominator_lcm,
        "correction_value_histogram": sorted(
            (value.numerator, value.denominator, count)
            for value, count in values.items()
        ),
        **leading,
        "correction": correction_encoding(correction),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "chart25 degree-two lift ledger changed")
    print("chart 25 degree-two full-source lift: PASS")
    print("row/column orbits:", len(rows), len(columns))
    print("rank mod 1009:", rank)
    print("exact correction support:", len(correction))
    print("correction denominator lcm:", denominator_lcm)
    print("singleton columns:", leading["singleton_columns"])
    print("duplicate leading rows:", leading["duplicate_leading_rows"])
    print("columns on duplicate leading rows:",
          leading["columns_on_duplicate_leading_rows"])
    print("maximum shared leading columns:",
          leading["maximum_shared_leading_columns"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
