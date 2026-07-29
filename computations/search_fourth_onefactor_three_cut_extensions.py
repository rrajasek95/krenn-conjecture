#!/usr/bin/env python3
"""Exact search for a third active cut after adding one diagonal one-factor.

This is a falsification search, not a Krenn certificate.  It starts from
the sharp two-cut model in the adjacent complete-high-sector note and adds
one further unit diagonal one-factor, in any of the three colours.  Shared
underlying edges retain all colour occurrences.  Every complete-cut and
target-defect test is performed exactly over Q by the routines used in the
independently audited three-factor exhaustion.
"""

from fractions import Fraction
from itertools import product

from search_three_cut_complete_high_sector_onefactor_families import (
    ALL_MATCHINGS,
    B,
    S,
    perfect_matchings,
    rational_basis,
    rational_member,
)


BASE = (
    ((0, 1), (2, 3), (4, 5), (6, 7)),
    ((0, 2), (1, 4), (3, 6), (5, 7)),
    ((0, 4), (1, 3), (2, 7), (5, 6)),
)


def matching_tensor(vertices, edge_cells):
    positions = {vertex: index for index, vertex in enumerate(vertices)}
    answer = {}
    for matching in perfect_matchings(vertices):
        if any(pair not in edge_cells for pair in matching):
            continue
        for selected in product(*(edge_cells[pair] for pair in matching)):
            word = [-1] * len(vertices)
            coefficient = Fraction(1)
            for (a, b), (colour, value) in zip(matching, selected):
                word[positions[a]] = colour
                word[positions[b]] = colour
                coefficient *= value
            key = tuple(word)
            answer[key] = answer.get(key, Fraction(0)) + coefficient
            if not answer[key]:
                del answer[key]
    return answer


def cofactor_columns(u_set, edge_cells):
    words = tuple(product(range(3), repeat=5))
    index = {word: i for i, word in enumerate(words)}
    columns = []
    for hole in u_set:
        remaining = tuple(x for x in u_set if x != hole)
        cofactor = matching_tensor(remaining, edge_cells)
        for colour in range(3):
            column = {}
            for h_word, coefficient in cofactor.items():
                assignment = {hole: colour}
                assignment.update(zip(remaining, h_word))
                word = tuple(assignment[x] for x in u_set)
                coordinate = index[word]
                column[coordinate] = (
                    column.get(coordinate, Fraction(0)) + coefficient
                )
            if column:
                columns.append(column)
    return columns


def high_residual_rows(z, edge_cells):
    u_set = tuple(x for x in S if x != z)
    c_set = (z, 6, 7)
    u_words = tuple(product(range(3), repeat=5))
    u_index = {word: i for i, word in enumerate(u_words)}
    rows = {}
    left = set(c_set)
    for matching in ALL_MATCHINGS:
        if any(pair not in edge_cells for pair in matching):
            continue
        crossings = sum((a in left) != (b in left) for a, b in matching)
        if crossings != 3:
            continue
        for selected in product(*(edge_cells[pair] for pair in matching)):
            word = [-1] * len(B)
            coefficient = Fraction(1)
            for (a, b), (colour, value) in zip(matching, selected):
                word[a] = colour
                word[b] = colour
                coefficient *= value
            c_word = tuple(word[x] for x in c_set)
            u_word = tuple(word[x] for x in u_set)
            row = rows.setdefault(c_word, {})
            coordinate = u_index[u_word]
            row[coordinate] = (
                row.get(coordinate, Fraction(0)) + coefficient
            )
            if not row[coordinate]:
                del row[coordinate]

    for colour in range(3):
        c_word = (colour,) * 3
        u_word = (colour,) * 5
        row = rows.setdefault(c_word, {})
        coordinate = u_index[u_word]
        row[coordinate] = row.get(coordinate, Fraction(0)) - 1
        if not row[coordinate]:
            del row[coordinate]
    return [row for row in rows.values() if row]


def cut_record(z, edge_cells):
    u_set = tuple(x for x in S if x != z)
    columns = cofactor_columns(u_set, edge_cells)
    residual_rows = high_residual_rows(z, edge_cells)
    words = tuple(product(range(3), repeat=5))
    word_index = {word: i for i, word in enumerate(words)}
    constants = [
        {word_index[(colour,) * 5]: Fraction(1)} for colour in range(3)
    ]
    basis = rational_basis(columns)
    complete = all(rational_member(row, basis) for row in residual_rows)
    augmented = rational_basis(columns + constants)
    return complete, len(augmented) - len(basis)


def edge_cells(extra, colour, weight):
    answer = {}
    for base_colour, matching in enumerate(BASE):
        for pair in matching:
            answer.setdefault(pair, []).append((base_colour, Fraction(1)))
    for pair in extra:
        answer.setdefault(pair, []).append((colour, Fraction(weight)))
    return answer


def main() -> None:
    best = -1
    records = []
    scanned = 0
    for weight in (-3, -2, -1, 1, 2, 3):
        for colour in range(3):
            for extra in ALL_MATCHINGS:
                cells = edge_cells(extra, colour, weight)
                replay = tuple(cut_record(z, cells) for z in S)
                good = tuple(
                    z for z, (complete, defect) in enumerate(replay)
                    if complete and defect
                )
                scanned += 1
                if len(good) > best:
                    best = len(good)
                    records = [(weight, colour, extra, good, replay)]
                elif len(good) == best:
                    records.append((weight, colour, extra, good, replay))

    print(f"scanned={scanned} max_active_complete_cuts={best}")
    for weight, colour, extra, good, replay in records[:20]:
        print(
            f"weight={weight} colour={colour} extra={extra} "
            f"cuts={good} records={replay}"
        )
    print(f"maximizing_records={len(records)}")


if __name__ == "__main__":
    main()
