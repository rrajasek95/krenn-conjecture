#!/usr/bin/env python3
"""Exact anchor-local audit of the four zero-based dangerous N=8 charts.

The input charts are the representatives numbered 25--28 in the quotient
eliminator's ``results.json``.  This checker deliberately reconstructs raw
hafnian terms from the 105 perfect matchings.  It keeps all twelve selected
pure cells as named Laurent variables: no anchor value is set to one.

The principal finite objects produced here are

* the 4/6 singleton-X4 anchor occurrences;
* every cancellation mate, graded by number of non-anchor cells;
* the degree-one (3,3,2) exposure map; and
* the complete filtered degree-two incidence component of the trivial
  twelve-anchor localized identity.

This is an unaudited reduction, not an N=8 nonexistence proof.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import argparse
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results.json"
UPSTREAM = (
    HERE.parent / "unaudited-codex-x4-quotient-eliminator-2026-08-20"
    / "results.json"
)

N = 8
COLORS = range(3)
EDGES = tuple(combinations(range(N), 2))
CELLS = tuple((u, v, a, b) for u, v in EDGES for a in COLORS for b in COLORS)
CELL_ID = {cell: index for index, cell in enumerate(CELLS)}
NAME_ID = {f"x{u}{v}_{a}{b}": index
           for index, (u, v, a, b) in enumerate(CELLS)}
PRIME = 1009
CHARTS = {
    25: (
        ((0, 1), (2, 3), (4, 5), (6, 7)),
        ((0, 2), (1, 3), (4, 6), (5, 7)),
        ((0, 4), (1, 5), (2, 6), (3, 7)),
    ),
    26: (
        ((0, 1), (2, 3), (4, 5), (6, 7)),
        ((0, 2), (1, 3), (4, 6), (5, 7)),
        ((0, 4), (1, 5), (2, 7), (3, 6)),
    ),
    27: (
        ((0, 1), (2, 3), (4, 5), (6, 7)),
        ((0, 2), (1, 3), (4, 6), (5, 7)),
        ((0, 4), (1, 6), (2, 5), (3, 7)),
    ),
    28: (
        ((0, 1), (2, 3), (4, 5), (6, 7)),
        ((0, 2), (1, 3), (4, 6), (5, 7)),
        ((0, 4), (1, 6), (2, 7), (3, 5)),
    ),
}
EXPECTED_D3 = {
    25: ({"-2": 3, "-1": 80, "1": 144}, 0, 282),
    26: ({"-1": 74, "1": 96}, 0, 211),
    27: ({"-1": 68, "1": 96}, 0, 205),
    28: ({"-1": 71, "1": 93}, 2, 207),
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    u = vertices[0]
    answer = []
    for i, v in enumerate(vertices[1:], 1):
        residual = vertices[1:i] + vertices[i + 1 :]
        for tail in perfect_matchings(residual):
            answer.append(((u, v),) + tail)
    return tuple(answer)


PM8 = perfect_matchings(tuple(range(N)))
require(len(PM8) == 105, "perfect-matching engine changed")


def word_name(word):
    return "".join(map(str, word))


def profile(word):
    return tuple(sorted(Counter(word).values(), reverse=True))


def mixed_x4(word):
    return len(set(word)) > 1 and max(Counter(word).values()) >= 4


def cell_name(cell):
    u, v, a, b = cell
    return f"x{u}{v}_{a}{b}"


def anchor_data(matchings):
    anchors = tuple(sorted(
        (u, v, c, c) for c, matching in enumerate(matchings)
        for u, v in matching
    ))
    edge_colour = {
        (u, v): c for c, matching in enumerate(matchings) for u, v in matching
    }
    require(len(anchors) == len(edge_colour) == 12,
            "dangerous chart is not a twelve-edge simple cubic skeleton")
    return anchors, edge_colour


def term_cells(word, matching):
    return tuple(sorted((u, v, word[u], word[v]) for u, v in matching))


def term_ids(word, matching):
    return bytes(sorted(CELL_ID[cell] for cell in term_cells(word, matching)))


def anchor_occurrences(matchings):
    anchors, edge_colour = anchor_data(matchings)
    answer = []
    for matching in PM8:
        if not all(edge in edge_colour for edge in matching):
            continue
        word = [None] * N
        for u, v in matching:
            word[u] = word[v] = edge_colour[u, v]
        word = tuple(word)
        cells = term_cells(word, matching)
        require(all(cell in anchors for cell in cells),
                "anchor occurrence used a non-anchor cell")
        answer.append((word, matching, cells))
    return tuple(answer)


def singleton_and_mate_ledger(matchings):
    anchors, _edge_colour = anchor_data(matchings)
    anchor_set = frozenset(anchors)
    occurrences = anchor_occurrences(matchings)
    word_counts = Counter(word for word, _matching, _cells in occurrences)
    require(all(count == 1 for count in word_counts.values()),
            "dangerous skeleton acquired an anchor cancellation")
    pure = tuple(item for item in occurrences if len(set(item[0])) == 1)
    mixed = tuple(item for item in occurrences if len(set(item[0])) > 1)
    require(len(pure) == 3 and all(mixed_x4(item[0]) for item in mixed),
            "anchor occurrence classification changed")
    require(len(mixed) in (4, 6), "dangerous 4/6 singleton count changed")

    records = []
    aggregate = Counter()
    for word, anchor_matching, anchor_cells in mixed:
        degree_histogram = Counter()
        degree_two = []
        for matching in PM8:
            if matching == anchor_matching:
                continue
            cells = term_cells(word, matching)
            degree = sum(cell not in anchor_set for cell in cells)
            degree_histogram[degree] += 1
            if degree == 2:
                degree_two.append([cell_name(cell) for cell in cells])
        require(degree_histogram == Counter({2: 12, 3: 32, 4: 60}),
                "singleton cancellation-mate grading changed")
        aggregate.update(degree_histogram)
        records.append({
            "word": word_name(word),
            "profile": list(profile(word)),
            "anchor_matching": [list(edge) for edge in anchor_matching],
            "anchor_monomial": [cell_name(cell) for cell in anchor_cells],
            "anchor_cofactor_in_product_m0m1m2": [
                cell_name(cell) for cell in anchors if cell not in anchor_cells
            ],
            "cancellation_mate_degree_histogram": {
                str(k): v for k, v in sorted(degree_histogram.items())
            },
            "degree_two_mates": degree_two,
        })
    return {
        "anchors": [cell_name(cell) for cell in anchors],
        "pure_anchor_monomials": {
            str(c): [cell_name((u, v, c, c)) for u, v in matchings[c]]
            for c in COLORS
        },
        "invariant_anchor_products": {
            f"m_{c}": "*".join(
                cell_name((u, v, c, c)) for u, v in matchings[c]
            ) for c in COLORS
        },
        "singleton_x4_count": len(mixed),
        "singleton_x4": records,
        "aggregate_cancellation_mate_degree_histogram": {
            str(k): v for k, v in sorted(aggregate.items())
        },
    }


def central_exposure_ledger(matchings):
    anchors, _edge_colour = anchor_data(matchings)
    anchor_set = frozenset(anchors)
    exposures = defaultdict(list)
    minimum_histogram = Counter()
    for word in product(COLORS, repeat=N):
        if profile(word) != (3, 3, 2):
            continue
        terms = []
        for matching in PM8:
            cells = term_cells(word, matching)
            degree = sum(cell not in anchor_set for cell in cells)
            terms.append((degree, cells))
        minimum = min(degree for degree, _cells in terms)
        leading = tuple(cells for degree, cells in terms if degree == minimum)
        minimum_histogram[minimum, len(leading)] += 1
        if minimum == 1:
            require(len(leading) == 1,
                    "central degree-one row has multiple leading terms")
            off = tuple(cell for cell in leading[0] if cell not in anchor_set)
            require(len(off) == 1, "central leading monomial is not linear")
            exposures[off[0]].append(word_name(word))
    require(minimum_histogram == Counter({
        (1, 1): 48, (2, 3): 336, (3, 15): 864, (4, 105): 432,
    }), "central filtered census changed")
    multiplicities = Counter(map(len, exposures.values()))
    require(multiplicities in (Counter({2: 24}), Counter({1: 48})),
            "central exposure multiplicities changed")
    return {
        "minimum_degree_leading_term_histogram": {
            f"degree_{degree}_terms_{terms}": count
            for (degree, terms), count in sorted(minimum_histogram.items())
        },
        "degree_one_rows": 48,
        "degree_one_exposed_cells": len(exposures),
        "exposure_multiplicity_histogram": {
            str(k): v for k, v in sorted(multiplicities.items())
        },
        "exposures": {
            cell_name(cell): words for cell, words in sorted(exposures.items())
        },
    }


def anchor_ids(matchings):
    return frozenset(CELL_ID[cell] for cell in anchor_data(matchings)[0])


@lru_cache(maxsize=None)
def word_terms(word):
    return tuple(term_ids(word, matching) for matching in PM8)


def row_degree(row, anchors):
    return sum(cell not in anchors for cell in row)


@lru_cache(maxsize=None)
def column_rows(column):
    word, multiplier = column
    return tuple(bytes(sorted(multiplier + term)) for term in word_terms(word))


@lru_cache(maxsize=None)
def column_minimum_degree(column, anchors):
    return min(row_degree(row, anchors) for row in column_rows(column))


@lru_cache(maxsize=None)
def incident_columns(row):
    decoded = [CELLS[cell] for cell in row]
    answer = set()
    for selected in combinations(range(12), 4):
        word = [None] * N
        covered = []
        for index in selected:
            u, v, a, b = decoded[index]
            covered.extend((u, v))
            word[u], word[v] = a, b
        if len(set(covered)) != N or len(set(word)) == 1:
            continue
        selected_set = frozenset(selected)
        multiplier = bytes(row[index] for index in range(12)
                           if index not in selected_set)
        answer.add((tuple(word), multiplier))
    return tuple(sorted(answer, key=repr))


def filtered_target(matchings, degree):
    anchors = anchor_ids(matchings)
    groups = []
    for c in COLORS:
        by_degree = defaultdict(list)
        for row in word_terms((c,) * N):
            by_degree[row_degree(row, anchors)].append(row)
        groups.append(by_degree)
    target = Counter()
    for degrees in product(range(degree + 1), repeat=3):
        if sum(degrees) != degree:
            continue
        for terms in product(*(groups[c].get(degrees[c], ()) for c in COLORS)):
            target[bytes(sorted(b"".join(terms)))] += 1
    return target


def seed_columns(matchings):
    anchors_tuple, _edge_colour = anchor_data(matchings)
    anchors = bytes(sorted(CELL_ID[cell] for cell in anchors_tuple))
    seeds = []
    for word, _matching, cells in anchor_occurrences(matchings):
        if len(set(word)) == 1:
            continue
        selected = [CELL_ID[cell] for cell in cells]
        multiplier = list(anchors)
        for cell in selected:
            multiplier.remove(cell)
        column = (word, bytes(sorted(multiplier)))
        require(column_minimum_degree(column, frozenset(anchors)) == 0,
                "seed column lost its anchor term")
        seeds.append(column)
    return tuple(seeds)


def degree_two_component(matchings):
    """Close K-degree two and construct an exact rational certificate."""
    anchors = anchor_ids(matchings)
    seeds = seed_columns(matchings)
    target0 = filtered_target(matchings, 0)
    target2 = filtered_target(matchings, 2)
    require(target0 == Counter({bytes(sorted(anchors)): 1}),
            "degree-zero pure target changed")
    start = set(target2)
    for column in seeds:
        start.update(row for row in column_rows(column)
                     if row_degree(row, anchors) == 2)
    rows = set(start)
    frontier = deque(sorted(start))
    columns = set()
    while frontier:
        row = frontier.popleft()
        for column in incident_columns(row):
            if column in columns:
                continue
            if column_minimum_degree(column, anchors) != 2:
                continue
            columns.add(column)
            for output in column_rows(column):
                if row_degree(output, anchors) != 2 or output in rows:
                    continue
                rows.add(output)
                frontier.append(output)

    ordered_rows = [bytes(sorted(anchors))] + sorted(rows)
    ordered_columns = list(seeds) + sorted(columns, key=repr)
    row_index = {row: i for i, row in enumerate(ordered_rows)}
    basis = {}
    independent_columns = []
    for column_number, column in enumerate(ordered_columns):
        vector = Counter()
        for row in column_rows(column):
            degree = row_degree(row, anchors)
            if degree in (0, 2):
                vector[row_index[row]] += 1
        vector = {i: v % PRIME for i, v in vector.items() if v % PRIME}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in basis:
                inv = pow(value, -1, PRIME)
                basis[pivot] = {
                    i: v * inv % PRIME for i, v in vector.items()
                }
                independent_columns.append(column_number)
                break
            pivot_row = basis[pivot]
            for i, v in pivot_row.items():
                nv = (vector.get(i, 0) - value * v) % PRIME
                if nv:
                    vector[i] = nv
                else:
                    vector.pop(i, None)
    target = {0: 1}
    target.update({row_index[row]: value % PRIME
                   for row, value in target2.items()})
    original_target_nonzeros = len(target)
    while target:
        pivot = min(target)
        value = target[pivot]
        if pivot not in basis:
            break
        for i, v in basis[pivot].items():
            nv = (target.get(i, 0) - value * v) % PRIME
            if nv:
                target[i] = nv
            else:
                target.pop(i, None)
    require(not target and len(independent_columns) == len(ordered_rows),
            "degree-two target component is not full row rank")

    # A nonzero determinant modulo PRIME certifies that the selected square
    # submatrix is invertible over Q.  Solve that exact square system and
    # replay the resulting certificate on the literal degree-zero/two rows.
    selected_columns = tuple(ordered_columns[i] for i in independent_columns)
    matrix = []
    rhs = []
    for row_number, row in enumerate(ordered_rows):
        matrix.append([])
        for column in selected_columns:
            matrix[-1].append(Fraction(sum(
                output == row for output in column_rows(column)
                if row_degree(output, anchors) in (0, 2)
            )))
        rhs.append(Fraction(1 if row_number == 0 else target2.get(row, 0)))
    augmented = [left + [right] for left, right in zip(matrix, rhs)]
    size = len(augmented)
    for col in range(size):
        pivot = next((row for row in range(col, size)
                      if augmented[row][col]), None)
        require(pivot is not None, "modularly selected exact minor vanished")
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        scale = augmented[col][col]
        augmented[col] = [value / scale for value in augmented[col]]
        for row in range(size):
            if row == col or not augmented[row][col]:
                continue
            scale = augmented[row][col]
            augmented[row] = [
                left - scale * right
                for left, right in zip(augmented[row], augmented[col])
            ]
    solution = tuple(augmented[i][-1] for i in range(size))
    certificate = tuple(
        (coefficient, column)
        for coefficient, column in zip(solution, selected_columns)
        if coefficient
    )
    replay = Counter()
    for coefficient, column in certificate:
        for row in column_rows(column):
            if row_degree(row, anchors) in (0, 2):
                replay[row] += coefficient
    expected = Counter({bytes(sorted(anchors)): Fraction(1)})
    expected.update({row: Fraction(value) for row, value in target2.items()})
    replay += Counter()  # delete zero entries in all supported Python modes
    require(replay == expected, "exact degree-two certificate replay failed")
    mutation = Counter(replay)
    coefficient, column = certificate[0]
    for row in column_rows(column):
        if row_degree(row, anchors) in (0, 2):
            mutation[row] -= 2 * coefficient
    mutation += Counter()
    require(mutation != expected, "certificate sign mutation did not fire")

    denominator_lcm = 1
    for coefficient, _column in certificate:
        denominator_lcm = math.lcm(denominator_lcm, coefficient.denominator)
    coefficient_histogram = Counter(
        str(coefficient) for coefficient, _column in certificate
    )
    certificate_ledger = []
    for coefficient, (word, multiplier) in certificate:
        certificate_ledger.append({
            "coefficient": str(coefficient),
            "word": word_name(word),
            "multiplier": [cell_name(CELLS[cell]) for cell in multiplier],
            "minimum_K_degree": column_minimum_degree(
                (word, multiplier), anchors
            ),
        })
    return {
        "filter": "K = ideal of the 240 cells outside the twelve named anchors",
        "degree_zero_seed_columns": len(seeds),
        "degree_two_rows": len(rows),
        "degree_two_columns": len(columns),
        "matrix_rows_including_degree_zero": len(ordered_rows),
        "matrix_columns_including_seeds": len(ordered_columns),
        "modulus": PRIME,
        "modular_rank": len(basis),
        "target_nonzeros": original_target_nonzeros,
        "target_remainder_nonzeros": len(target),
        "target_in_image_mod_prime": not target,
        "exact_certificate_terms": len(certificate),
        "exact_certificate_denominator_lcm": denominator_lcm,
        "exact_certificate_coefficient_histogram": dict(sorted(
            coefficient_histogram.items()
        )),
        "exact_certificate": certificate_ledger,
        "exact_replay": True,
        "sign_mutation_fired": True,
    }


def close_exact_degree(start_rows, anchors, degree):
    """Return the literal row/column incidence component at one K-degree."""
    rows = set(start_rows)
    frontier = deque(sorted(start_rows))
    columns = set()
    while frontier:
        row = frontier.popleft()
        for column in incident_columns(row):
            if column in columns:
                continue
            if column_minimum_degree(column, anchors) != degree:
                continue
            columns.add(column)
            for output in column_rows(column):
                if row_degree(output, anchors) != degree or output in rows:
                    continue
                rows.add(output)
                frontier.append(output)
    return rows, columns


def modular_span(rows, columns, target):
    """Exact integer matrix, finite-field discovery membership."""
    ordered_rows = tuple(rows)
    row_index = {row: i for i, row in enumerate(ordered_rows)}
    basis = {}
    for column in columns:
        vector = Counter(row_index[row] for row in column if row in row_index)
        vector = {i: value % PRIME for i, value in vector.items()
                  if value % PRIME}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in basis:
                inverse = pow(value, -1, PRIME)
                basis[pivot] = {
                    i: entry * inverse % PRIME
                    for i, entry in vector.items()
                }
                break
            for i, entry in basis[pivot].items():
                new = (vector.get(i, 0) - value * entry) % PRIME
                if new:
                    vector[i] = new
                else:
                    vector.pop(i, None)
    residual = {row_index[row]: value % PRIME
                for row, value in target.items() if value % PRIME}
    original_nonzeros = len(residual)
    while residual:
        pivot = min(residual)
        value = residual[pivot]
        if pivot not in basis:
            break
        for i, entry in basis[pivot].items():
            new = (residual.get(i, 0) - value * entry) % PRIME
            if new:
                residual[i] = new
            else:
                residual.pop(i, None)
    return len(basis), original_nonzeros, len(residual)


def degree_three_component(matchings):
    """Complete coupled K-degrees 0,2,3 and replay an exact certificate."""
    anchors = anchor_ids(matchings)
    anchor_row = bytes(sorted(anchors))
    seeds = seed_columns(matchings)
    target2 = filtered_target(matchings, 2)
    start2 = set(target2)
    for column in seeds:
        start2.update(row for row in column_rows(column)
                      if row_degree(row, anchors) == 2)
    rows2, columns2 = close_exact_degree(start2, anchors, 2)
    lower_columns = tuple(seeds) + tuple(sorted(columns2, key=repr))

    target3 = filtered_target(matchings, 3)
    start3 = set(target3)
    for column in lower_columns:
        start3.update(row for row in column_rows(column)
                      if row_degree(row, anchors) == 3)
    rows3, columns3 = close_exact_degree(start3, anchors, 3)

    ordered_rows = (anchor_row,) + tuple(sorted(rows2)) + tuple(sorted(rows3))
    all_columns = lower_columns + tuple(sorted(columns3, key=repr))
    truncated_columns = []
    for column in all_columns:
        truncated_columns.append(tuple(
            row for row in column_rows(column)
            if row_degree(row, anchors) in (0, 2, 3)
        ))
    target = Counter({anchor_row: 1})
    target.update(target2)
    target.update(target3)
    rank, target_nonzeros, remainder = modular_span(
        ordered_rows, truncated_columns, target
    )

    # The lexicographically selected exact d2 certificate has a remarkably
    # simple tail: target3 minus that tail is a sum of distinct rows, each
    # with coefficient +1.  Every such row has a literal min-degree-three
    # column with exactly one leading output, so adjoining those columns is
    # an exact characteristic-zero lift through K-degree three.
    d2 = degree_two_component(matchings)
    exact_d2 = []
    for item in d2["exact_certificate"]:
        exact_d2.append((
            Fraction(item["coefficient"]),
            (
                tuple(map(int, item["word"])),
                bytes(sorted(NAME_ID[name] for name in item["multiplier"])),
            ),
        ))
    current3 = Counter()
    for coefficient, column in exact_d2:
        for row in column_rows(column):
            if row_degree(row, anchors) == 3:
                current3[row] += coefficient
    residual3 = {
        row: Fraction(target3[row]) - current3[row]
        for row in set(target3) | set(current3)
        if Fraction(target3[row]) - current3[row]
    }
    singleton_columns = {}
    for column in sorted(columns3, key=repr):
        outputs = tuple(row for row in column_rows(column)
                        if row_degree(row, anchors) == 3)
        require(len(outputs) == 1,
                "minimum-degree-three column acquired multiple leading rows")
        singleton_columns.setdefault(outputs[0], column)
    unhandled = tuple(sorted(set(residual3) - set(singleton_columns)))
    kernel_adjustment = []
    if unhandled:
        # Chart 28 has one row outside the singleton-column image for the
        # lexicographically selected d2 lift.  A two-column direction in the
        # complete d2 kernel changes exactly that quotient coordinate.  Find
        # it from a small exact full-row-rank system rather than freezing it.
        require(len(unhandled) == 1 and residual3[unhandled[0]] == -1,
                "unexpected degree-three singleton cokernel")
        constraint_rows = (
            (anchor_row,) + tuple(sorted(rows2)) + unhandled
        )
        constraint_index = {
            row: index for index, row in enumerate(constraint_rows)
        }
        modular_basis = {}
        independent = []
        for column_number, column in enumerate(lower_columns):
            vector = Counter(
                constraint_index[row] for row in column_rows(column)
                if row in constraint_index
            )
            vector = {i: value % PRIME for i, value in vector.items()
                      if value % PRIME}
            while vector:
                pivot = min(vector)
                value = vector[pivot]
                if pivot not in modular_basis:
                    inverse = pow(value, -1, PRIME)
                    modular_basis[pivot] = {
                        i: entry * inverse % PRIME
                        for i, entry in vector.items()
                    }
                    independent.append(column_number)
                    break
                for i, entry in modular_basis[pivot].items():
                    new = (vector.get(i, 0) - value * entry) % PRIME
                    if new:
                        vector[i] = new
                    else:
                        vector.pop(i, None)
            if len(independent) == len(constraint_rows):
                break
        require(len(independent) == len(constraint_rows),
                "degree-two kernel adjustment system lost full row rank")
        selected = tuple(lower_columns[i] for i in independent)
        augmented = []
        for row in constraint_rows:
            augmented.append([
                Fraction(sum(output == row for output in column_rows(column)))
                for column in selected
            ] + [Fraction(residual3[row] if row in unhandled else 0)])
        size = len(augmented)
        for col in range(size):
            pivot = next((row for row in range(col, size)
                          if augmented[row][col]), None)
            require(pivot is not None,
                    "modular kernel-adjustment minor vanished over Q")
            augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
            scale = augmented[col][col]
            augmented[col] = [value / scale for value in augmented[col]]
            for row in range(size):
                if row == col or not augmented[row][col]:
                    continue
                scale = augmented[row][col]
                augmented[row] = [
                    left - scale * right
                    for left, right in zip(augmented[row], augmented[col])
                ]
        kernel_adjustment = [
            (augmented[i][-1], selected[i]) for i in range(size)
            if augmented[i][-1]
        ]
        require(len(kernel_adjustment) == 2
                and Counter(value for value, _column in kernel_adjustment)
                == Counter({Fraction(-1): 1, Fraction(1): 1}),
                "chart-28 kernel adjustment ceased to be a two-column difference")
        exact_d2.extend(kernel_adjustment)
        current3 = Counter()
        for coefficient, column in exact_d2:
            for row in column_rows(column):
                if row_degree(row, anchors) == 3:
                    current3[row] += coefficient
        residual3 = {
            row: Fraction(target3[row]) - current3[row]
            for row in set(target3) | set(current3)
            if Fraction(target3[row]) - current3[row]
        }
        unhandled = tuple(sorted(set(residual3) - set(singleton_columns)))
    require(not unhandled,
            "degree-three residual has no singleton source pivot")
    exact_d3 = tuple((coefficient, singleton_columns[row])
                     for row, coefficient in sorted(residual3.items()))
    exact_certificate = tuple(exact_d2) + exact_d3
    replay = Counter()
    for coefficient, column in exact_certificate:
        for row in column_rows(column):
            if row_degree(row, anchors) in (0, 2, 3):
                replay[row] += coefficient
    replay = Counter({row: value for row, value in replay.items() if value})
    expected = Counter({anchor_row: Fraction(1)})
    expected.update({row: Fraction(value) for row, value in target2.items()})
    expected.update({row: Fraction(value) for row, value in target3.items()})
    require(replay == expected, "exact degree-three certificate replay failed")
    mutation = Counter(replay)
    negative = next(((coefficient, column)
                     for coefficient, column in exact_d3
                     if coefficient < 0), None)
    require(negative is not None,
            "degree-three certificate lost its negative signed tail")
    coefficient, column = negative
    for row in column_rows(column):
        if row_degree(row, anchors) in (0, 2, 3):
            mutation[row] -= 2 * coefficient
    mutation = Counter({row: value for row, value in mutation.items() if value})
    require(mutation != expected, "degree-three sign mutation did not fire")
    exact_ledger = []
    for coefficient, (word, multiplier) in exact_certificate:
        exact_ledger.append({
            "coefficient": str(coefficient),
            "word": word_name(word),
            "multiplier": [cell_name(CELLS[cell]) for cell in multiplier],
            "minimum_K_degree": column_minimum_degree(
                (word, multiplier), anchors
            ),
        })
    residual_histogram = dict(sorted(
        Counter(str(value) for value in residual3.values()).items()
    ))
    chart = next(index for index, value in CHARTS.items()
                 if value == matchings)
    require(
        (residual_histogram, len(kernel_adjustment), len(exact_certificate))
        == EXPECTED_D3[chart],
        "frozen signed degree-three certificate census changed",
    )
    return {
        "filter": "K = ideal of the 240 cells outside the twelve named anchors",
        "coupled_degrees": [0, 2, 3],
        "degree_zero_seed_columns": len(seeds),
        "degree_two_rows": len(rows2),
        "degree_two_columns": len(columns2),
        "degree_three_rows": len(rows3),
        "degree_three_columns": len(columns3),
        "matrix_rows": len(ordered_rows),
        "matrix_columns": len(all_columns),
        "modulus": PRIME,
        "modular_rank": rank,
        "target_nonzeros": target_nonzeros,
        "target_remainder_nonzeros": remainder,
        "target_in_image_mod_prime": remainder == 0,
        "fixed_degree_two_certificate_tail_residual_rows": len(residual3),
        "fixed_degree_two_certificate_tail_coefficient_histogram": residual_histogram,
        "degree_two_kernel_adjustment_terms": len(kernel_adjustment),
        "minimum_degree_three_column_leading_term_histogram": {
            "1": len(columns3)
        },
        "residual_rows_with_singleton_source_pivot": len(residual3),
        "exact_certificate_terms": len(exact_certificate),
        "exact_certificate_denominator_lcm": 1,
        "exact_certificate_coefficient_histogram": dict(sorted(Counter(
            str(coefficient) for coefficient, _column in exact_certificate
        ).items())),
        "exact_certificate": exact_ledger,
        "exact_replay": True,
        "negative_sign_mutation_fired": True,
        "conclusion": "H0*H1*H2 belongs to I_mix + K^4 over Q",
        "scope": "exact characteristic-zero filtered identity through degree three",
    }


def cramer_template_scope(matchings):
    """Record why the support-specific five-row packet does not transfer."""
    anchors, _edge_colour = anchor_data(matchings)
    blocks = Counter((u, v) for u, v, _a, _b in anchors)
    require(set(blocks.values()) == {1} and len(blocks) == 12,
            "selected skeleton unexpectedly contains a multi-cell block")
    # In the unrestricted chart no cell is zero.  Expanding H_word along a
    # varied site therefore has one independent neighbour-block summand for
    # each of its seven neighbours.  The m25 packet used exactly two full
    # neighbour blocks plus one supported singleton and support-zeroed all
    # other summands.
    return {
        "selected_skeleton_nonzero_cells_per_physical_block": 1,
        "selected_skeleton_physical_blocks": 12,
        "unrestricted_localized_chart_forces_other_cells_zero": False,
        "universal_varied_site_neighbour_summands": 7,
        "m25_packet_live_full_neighbour_blocks": 2,
        "m25_packet_live_singleton_spikes": 1,
        "m25_packet_directly_instantiates": False,
        "reason": (
            "anchor localization inverts twelve cells but imposes no support "
            "zeros; the five extra neighbour-block cofactor vectors in a "
            "varied-site hafnian packet remain independent terms"
        ),
    }


def check_upstream_representatives():
    data = json.loads(UPSTREAM.read_text())
    records = {
        item["orbit"]: item["representative"]
        for item in data["pure_matching_orbits"]["records"]
        if item["orbit"] in CHARTS
    }
    require(set(records) == set(CHARTS), "upstream dangerous charts missing")
    for chart, matching in CHARTS.items():
        expected = [[list(edge) for edge in colour] for colour in matching]
        require(records[chart] == expected,
                f"upstream representative changed at chart {chart}")
    return sha256(UPSTREAM.read_bytes()).hexdigest()


def audit(include_degree_two=True):
    upstream_sha = check_upstream_representatives()
    charts = {}
    for chart, matchings in CHARTS.items():
        record = {
            "representative": [[list(edge) for edge in colour]
                               for colour in matchings],
            "anchor_packet": singleton_and_mate_ledger(matchings),
            "central_332": central_exposure_ledger(matchings),
            "cramer_packet_scope": cramer_template_scope(matchings),
        }
        if include_degree_two:
            record["filtered_degree_two"] = degree_two_component(matchings)
            record["filtered_degree_three_exact"] = degree_three_component(
                matchings
            )
        charts[str(chart)] = record
    core = {
        "status": "UNAUDITED exact finite reduction; no N=8 closure claimed",
        "upstream_results_sha256": upstream_sha,
        "charts": charts,
        "controls": {
            "raw_perfect_matchings": len(PM8),
            "anchor_values_specialized": 0,
            "named_anchor_variables_retained": 12,
            "all_four_chart_representatives_rechecked": True,
        },
    }
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    return core


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--skip-degree-two", action="store_true")
    args = parser.parse_args()
    result = audit(not args.skip_degree_two)
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("dangerous-chart anchor audit: PASS")
    for chart, record in result["charts"].items():
        packet = record["anchor_packet"]
        central = record["central_332"]
        line = (
            f"chart {chart}: singleton X4={packet['singleton_x4_count']}, "
            f"central exposed cells={central['degree_one_exposed_cells']}"
        )
        if "filtered_degree_two" in record:
            d2 = record["filtered_degree_two"]
            line += (
                f", d2 rows/cols={d2['degree_two_rows']}/"
                f"{d2['degree_two_columns']}, in_image={d2['target_in_image_mod_prime']}"
            )
        print(line)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
