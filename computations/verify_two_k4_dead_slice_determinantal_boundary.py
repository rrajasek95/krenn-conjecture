#!/usr/bin/env python3
"""Exact audit of the invertible-block obstruction for two K4 shores.

This verifies the finite and linear-algebraic parts of
``notes/two-k4-dead-slice-determinantal-boundary.md``:

* the 30 dead words split into eight coordinate lines and six Hamilton
  words;
* the universal four-vector square-free syzygy has nullity one, generated
  by alternating 3x3 determinants;
* the oriented-triangle incidence table has maximum four and exactly two
  maximizers;
* double counting forces two columns of each parity;
* the Hamilton contractions give 48 distinct binomials, and seven of their
  exponent differences have an odd integer dependence.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations, product

from flint import fmpz_mat


VERTICES = tuple(range(4))
COLORS = tuple(range(3))
DIFFERENCES = (1, 2, 3)


def factor_color(u: int, v: int) -> int:
    return DIFFERENCES.index(u ^ v)


def is_dead(word: tuple[int, ...]) -> bool:
    return not any(
        word[u] == word[v] == factor_color(u, v)
        for u, v in combinations(VERTICES, 2)
    )


def dead_coordinate_lines():
    answer = []
    for hole in VERTICES:
        remainder = tuple(v for v in VERTICES if v != hole)
        for values in product(COLORS, repeat=3):
            words = []
            for color in COLORS:
                word = [None] * 4
                word[hole] = color
                for vertex, value in zip(remainder, values):
                    word[vertex] = value
                words.append(tuple(word))
            if all(is_dead(word) for word in words):
                answer.append((hole, tuple(zip(remainder, values))))
    return tuple(answer)


def audit_dead_words():
    dead = tuple(
        word for word in product(COLORS, repeat=4) if is_dead(word)
    )
    lines = dead_coordinate_lines()
    covered = set()
    for hole, assignment in lines:
        for color in COLORS:
            word = [None] * 4
            word[hole] = color
            for vertex, value in assignment:
                word[vertex] = value
            covered.add(tuple(word))
    hamilton = tuple(word for word in dead if word not in covered)
    assert len(dead) == 30
    assert len(lines) == 8
    assert len(covered) == 24
    assert tuple("".join(map(str, word)) for word in hamilton) == (
        "0110", "0202", "1001", "1122", "2020", "2211"
    )
    return lines, hamilton


def audit_universal_syzygy():
    # A coefficient is indexed by (missing factor j, one coordinate in each
    # of the other three factors).  Multiplication by the generic vector
    # x_j sends it to three vector-valued quadrilinear coefficients.
    columns = []
    for missing in VERTICES:
        for indices in product(COLORS, repeat=3):
            columns.append((missing, indices))

    row_index = {}
    entries = []
    for column, (missing, indices) in enumerate(columns):
        full = [None] * 4
        iterator = iter(indices)
        for factor in VERTICES:
            if factor != missing:
                full[factor] = next(iterator)
        for vector_coordinate in COLORS:
            full[missing] = vector_coordinate
            key = (vector_coordinate, tuple(full))
            row = row_index.setdefault(key, len(row_index))
            entries.append((row, column))

    matrix_rows = [[0] * len(columns) for _ in row_index]
    for row, column in entries:
        matrix_rows[row][column] = 1
    matrix = fmpz_mat(matrix_rows)
    assert (matrix.nrows(), matrix.ncols(), matrix.rank()) == (195, 108, 107)

    # Build the alternating determinant cofactor vector explicitly and
    # verify that it spans the one-dimensional kernel.
    column_index = {column: index for index, column in enumerate(columns)}
    cofactor = [0] * len(columns)
    for missing in VERTICES:
        factors = tuple(j for j in VERTICES if j != missing)
        for sigma in permutations(COLORS):
            inversions = sum(
                sigma[r] > sigma[s]
                for r in COLORS for s in COLORS if r < s
            )
            # This sign convention is the one in sum_j x_j C_j=0.
            sign = (-1) ** (missing + inversions)
            indices = tuple(sigma[factors.index(j)] for j in factors)
            cofactor[column_index[missing, indices]] = sign
    product_vector = [
        sum(matrix[row, column] * cofactor[column]
            for column in range(matrix.ncols()))
        for row in range(matrix.nrows())
    ]
    assert not any(product_vector)


class UnionFind:
    def __init__(self):
        self.parent = {
            (vertex, color): (vertex, color)
            for vertex in VERTICES for color in COLORS
        }

    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, first, second):
        first, second = self.find(first), self.find(second)
        if first != second:
            self.parent[second] = first


def triangle_maps(lines):
    # Ordering is hole 0 (two orientations), then hole 1, and so on.
    assert tuple(hole for hole, _assignment in lines) == (
        0, 0, 1, 1, 2, 2, 3, 3
    )
    maximizers = []
    histogram = Counter()
    for mask in range(1 << len(lines)):
        union_find = UnionFind()
        for index, (_hole, assignment) in enumerate(lines):
            if not (mask & (1 << index)):
                continue
            union_find.union(assignment[0], assignment[1])
            union_find.union(assignment[0], assignment[2])
        valid = all(
            union_find.find((vertex, first))
            != union_find.find((vertex, second))
            for vertex in VERTICES
            for first, second in combinations(COLORS, 2)
        )
        if not valid:
            continue
        size = mask.bit_count()
        histogram[size] += 1
        if size == 4:
            maximizers.append(mask)

    assert histogram == {0: 1, 1: 8, 2: 16, 3: 8, 4: 2}
    assert maximizers == [
        sum(1 << index for index in (0, 2, 5, 6)),
        sum(1 << index for index in (1, 3, 4, 7)),
    ]

    maps = []
    for mask in maximizers:
        phi = {}
        for index, (hole, assignment) in enumerate(lines):
            if mask & (1 << index):
                for label in assignment:
                    assert label not in phi
                    phi[label] = hole
        assert len(phi) == 12
        maps.append(tuple(
            tuple(phi[vertex, color] for color in COLORS)
            for vertex in VERTICES
        ))
    assert maps == [
        ((3, 1, 2), (2, 0, 3), (1, 3, 0), (0, 2, 1)),
        ((2, 3, 1), (3, 2, 0), (0, 1, 3), (1, 0, 2)),
    ]
    return maps


def audit_hamilton_binomials(hamilton, maps):
    # Double counting forces exactly two columns of each maximizer type.  A
    # permutation of right tensor factors gives this canonical ordering.
    types = (0, 0, 1, 1)
    variables = tuple(
        (row, color, column)
        for row in VERTICES for color in COLORS for column in VERTICES
    )
    variable_index = {variable: index for index, variable in enumerate(variables)}
    differences = []
    metadata = []

    for word in hamilton:
        labels = tuple(
            tuple(maps[types[column]][row][word[row]] for row in VERTICES)
            for column in VERTICES
        )
        assert all(len(set(column_labels)) == 2 for column_labels in labels)
        choices = product(*(sorted(set(column_labels)) for column_labels in labels))
        for choice in choices:
            matchings = [
                row_at_column
                for row_at_column in permutations(VERTICES)
                if all(
                    labels[column][row_at_column[column]] == choice[column]
                    for column in VERTICES
                )
            ]
            assert len(matchings) in (0, 2)
            if not matchings:
                continue

            monomials = []
            difference = [0] * len(variables)
            for sign, matching in ((1, matchings[0]), (-1, matchings[1])):
                monomial = tuple(
                    (row, word[row], column)
                    for column, row in enumerate(matching)
                )
                monomials.append(monomial)
                for variable in monomial:
                    difference[variable_index[variable]] += sign

            # x^d=-1 is unchanged when d is negated.  Canonicalize so the
            # enumeration and the seven-entry certificate are stable.
            if next(value for value in difference if value) != 1:
                difference = [-value for value in difference]
                monomials.reverse()
                matchings.reverse()
            difference = tuple(difference)
            if difference not in differences:
                differences.append(difference)
                metadata.append((word, choice, tuple(matchings), tuple(monomials)))

    assert len(differences) == 48
    exponent_matrix = fmpz_mat([list(column) for column in zip(*differences)])
    assert (exponent_matrix.nrows(), exponent_matrix.ncols(),
            exponent_matrix.rank()) == (48, 48, 21)

    certificate = {1: 1, 2: -1, 3: 1, 9: -1, 10: 1, 11: -1, 25: -1}
    total = [0] * len(variables)
    for equation, multiplier in certificate.items():
        for variable, exponent in enumerate(differences[equation]):
            total[variable] += multiplier * exponent
    assert not any(total)
    assert sum(certificate.values()) == -1

    expected = {
        1: ("0110", (0, 3, 1, 1)),
        2: ("0110", (0, 3, 1, 2)),
        3: ("0110", (0, 3, 2, 1)),
        9: ("0202", (1, 3, 0, 0)),
        10: ("0202", (1, 3, 0, 2)),
        11: ("0202", (1, 3, 2, 0)),
        25: ("1122", (0, 1, 2, 2)),
    }
    for index, (word_text, choice) in expected.items():
        word, actual_choice, _matchings, _monomials = metadata[index]
        assert "".join(map(str, word)) == word_text
        assert actual_choice == choice


def main():
    lines, hamilton = audit_dead_words()
    audit_universal_syzygy()
    maps = triangle_maps(lines)
    audit_hamilton_binomials(hamilton, maps)
    print(
        "PASS: dead=8 lines+6 Hamilton, syzygy rank=107/108, "
        "triangle maxima=2, Hamilton binomials=48, certificate=7"
    )


if __name__ == "__main__":
    main()
