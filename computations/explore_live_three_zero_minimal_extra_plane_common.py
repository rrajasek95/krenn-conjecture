#!/usr/bin/env python3
"""Explore sparse exact response rows for the all-common minimal extra plane."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations, product

import sympy as sp


a, b, direct_scale = sp.symbols("a b direct_scale")
H = sp.Matrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
I = sp.eye(3)
D = sp.diag(1, 1, 0)
ACTIVE = tuple(range(5))
COLUMNS = tuple((site, colour) for colour in range(3) for site in ACTIVE)
COLUMN_INDEX = {column: index for index, column in enumerate(COLUMNS)}


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    return tuple(
        ((first, vertices[position]),) + tail
        for position in range(1, len(vertices))
        for tail in perfect_matchings(
            vertices[1:position] + vertices[position + 1 :]
        )
    )


def response_builder(extra):
    matrices = (I, I, D, D, extra)
    blocks = {
        (left, right): matrices[left] * H * matrices[right].T / 2
        for left, right in combinations(range(5), 2)
    }

    def edge(word, left, right):
        if left < right:
            return blocks[left, right][word[left], word[right]]
        return blocks[right, left][word[right], word[left]]

    def hafnian(word, vertices):
        return sum(
            (
                sp.prod(
                    edge(word, left, right)
                    for left, right in matching
                )
                for matching in perfect_matchings(vertices)
            ),
            sp.S.Zero,
        )

    def response(word, source_left, source_right):
        row = [sp.S.Zero] * len(COLUMNS)
        if (
            source_left != source_right
            and {source_left, source_right} == {0, 1}
        ):
            for star_site in ACTIVE:
                remaining = tuple(
                    site for site in range(5) if site != star_site
                )
                row[COLUMN_INDEX[star_site, word[star_site]]] += (
                    direct_scale * hafnian(word, remaining)
                )
        for left, right in combinations(range(5), 2):
            marked = (
                matrices[left][word[left], source_left]
                * matrices[right][word[right], source_right]
                + matrices[left][word[left], source_right]
                * matrices[right][word[right], source_left]
            )
            if marked == 0:
                continue
            for star_site in ACTIVE:
                if star_site in (left, right):
                    continue
                remaining = tuple(
                    site
                    for site in range(5)
                    if site not in (left, right, star_site)
                )
                row[COLUMN_INDEX[star_site, word[star_site]]] += (
                    marked * hafnian(word, remaining)
                )
        return tuple(sp.cancel(entry) for entry in row)

    return response


def is_nonzero_constant(entry):
    return entry != 0 and not (entry.free_symbols & {a, b, direct_scale})


def sparse_greedy(name, extra):
    response = response_builder(extra)
    records = []
    for word in product(range(3), repeat=5):
        for source in range(3):
            row = response(word, source, source)
            if any(row):
                records.append((word, source, row))

    killed = set()
    selected = []
    while True:
        choice = None
        for word, source, row in records:
            support = [
                index
                for index, entry in enumerate(row)
                if entry != 0 and index not in killed
            ]
            if len(support) == 1 and is_nonzero_constant(row[support[0]]):
                choice = word, source, row, support[0]
                break
        if choice is None:
            break
        word, source, row, pivot = choice
        killed.add(pivot)
        selected.append((word, source, COLUMNS[pivot], row[pivot]))

    print(name, "constant triangular pivots", len(killed), "/", len(COLUMNS))
    for word, source, pivot, coefficient in selected:
        print(" ", "".join(map(str, word)), f";{source}{source}", pivot, coefficient)
    print("remaining", tuple(COLUMNS[index] for index in range(15) if index not in killed))

    sparse = []
    for word, source, row in records:
        support = tuple(
            index
            for index, entry in enumerate(row)
            if entry != 0 and index not in killed
        )
        if 1 <= len(support) <= 4:
            sparse.append((len(support), word, source, support, row))
    sparse.sort(key=lambda record: record[0])
    for size, word, source, support, row in sparse[:80]:
        print(
            size,
            "".join(map(str, word)),
            f";{source}{source}",
            [(COLUMNS[index], sp.factor(row[index])) for index in support],
        )


def independent_labels(records, substitution):
    basis = {}
    labels = []
    for label, symbolic_row in records:
        row = [sp.cancel(entry.subs(substitution)) for entry in symbolic_row]
        for pivot in sorted(basis):
            if row[pivot] != 0:
                scale = row[pivot]
                row = [
                    sp.cancel(entry - scale * basis_entry)
                    for entry, basis_entry in zip(row, basis[pivot])
                ]
        pivot = next((index for index, entry in enumerate(row) if entry != 0), None)
        if pivot is None:
            continue
        scale = row[pivot]
        basis[pivot] = [sp.cancel(entry / scale) for entry in row]
        labels.append(label)
        if len(labels) == len(COLUMNS):
            break
    return labels


def kernel_and_witness(name, extra):
    response = response_builder(extra)
    records = []
    for word in product(range(3), repeat=5):
        for source in range(3):
            row = response(word, source, source)
            records.append(((word, source, source), row))

    test_points = {
        "01": ((2, 5), (0, 2), (-3, 2), (1, sp.Rational(-4, 3)), (0, -1), (-3, 0), (0, -3)),
        "12": ((2, 5), (0, 2), (2, sp.Rational(5, 3)), (0, sp.Rational(-1, 3))),
        "02": ((2, 5), (0, 2), (1, sp.Rational(-2, 3)), (0, -1), (0, sp.Rational(-1, 3))),
    }[name]
    determinants = []
    for avalue, bvalue in test_points:
        labels = independent_labels(records, {a: avalue, b: bvalue})
        print(name, "point", (avalue, bvalue), "rank", len(labels))
        if len(labels) < len(COLUMNS):
            continue
        label_set = set(labels)
        matrix = sp.Matrix([row for label, row in records if label in label_set])
        determinant = sp.factor(sp.cancel(matrix.det(method="domain-ge")))
        determinants.append(determinant)
        print(" determinant", determinant)
        print(
            " labels",
            tuple(
                ("".join(map(str, word)), source_left, source_right)
                for word, source_left, source_right in labels
            ),
        )
    generators = [sp.Poly(value, a, b) for value in determinants]
    groebner = sp.groebner(generators, a, b, order="grevlex")
    print(name, "determinantal ideal sample", tuple(groebner.polys))


def main():
    charts = {
        "01": sp.Matrix([[1, 0, a], [0, 1, b], [0, 0, 0]]),
        "12": sp.Matrix([[a, 1, 0], [b, 0, 1], [0, 0, 0]]),
        "02": sp.Matrix([[1, a, 0], [0, b, 1], [0, 0, 0]]),
    }
    for name, extra in charts.items():
        # sparse_greedy(name, extra)
        kernel_and_witness(name, extra)


if __name__ == "__main__":
    main()
