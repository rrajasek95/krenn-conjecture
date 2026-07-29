#!/usr/bin/env python3
"""Independent direct-intersection audit for the fixed six-site interior.

This checker imports no project module.  Unlike the primary dual-annihilator
calculation, it constructs each cylinder as a sparse primal column space and
intersects those spaces directly by solving [A|-B](x,y)=0 over QQ.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import product

import sympy as sp


SITES = tuple(range(6))
COLOURS = (0, 1, 2)
WORDS6 = tuple(product(COLOURS, repeat=6))

SOURCES = (
    (0, 1, 0, 0, 1), (4, 5, 0, 0, 1),
    (0, 2, 1, 1, 1), (1, 4, 1, 1, 1),
    (0, 4, 2, 2, 1), (1, 3, 2, 2, 1),
    (2, 5, 0, 0, 1), (3, 5, 1, 0, 1),
    (2, 3, 2, 1, 1),
)


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for index in range(1, len(vertices)):
        mate = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            result.append(((first, mate),) + tail)
    return tuple(result)


def aggregate():
    result = {}
    for left, right, left_colour, right_colour, weight in SOURCES:
        assert left < right
        cells = result.setdefault((left, right), {})
        cell = (left_colour, right_colour)
        cells[cell] = cells.get(cell, 0) + sp.Rational(weight)
    return result


def matching_tensor(vertices: tuple[int, ...], edge_blocks):
    positions = {site: index for index, site in enumerate(vertices)}
    result = {}
    for matching in perfect_matchings(vertices):
        choices = [tuple(edge_blocks.get(edge, {}).items()) for edge in matching]
        if any(not choice for choice in choices):
            continue
        for selected in product(*choices):
            word = [-1] * len(vertices)
            coefficient = sp.Rational(1)
            for (left, right), (cell, weight) in zip(matching, selected):
                word[positions[left]], word[positions[right]] = cell
                coefficient *= weight
            key = tuple(word)
            result[key] = result.get(key, 0) + coefficient
            if result[key] == 0:
                del result[key]
    return result


def add(result, word, coefficient):
    result[word] = result.get(word, 0) + coefficient
    if result[word] == 0:
        del result[word]


def sparse_basis(vectors):
    """Reduced pivot dictionary, returned as an independent vector list."""
    pivots = {}
    for supplied in vectors:
        row = {word: sp.Rational(value) for word, value in supplied.items() if value}
        while row:
            pivot = min(row)
            if pivot not in pivots:
                scale = row[pivot]
                row = {word: value / scale for word, value in row.items()}
                # Clear the new pivot from earlier rows for stable comparison.
                for old_pivot, old_row in list(pivots.items()):
                    if old_row.get(pivot):
                        multiple = old_row[pivot]
                        updated = dict(old_row)
                        for word, value in row.items():
                            add(updated, word, -multiple * value)
                        pivots[old_pivot] = updated
                pivots[pivot] = row
                break
            multiple = row[pivot]
            for word, value in pivots[pivot].items():
                add(row, word, -multiple * value)
    return [pivots[pivot] for pivot in sorted(pivots)]


def in_span(vector, basis):
    pivots = {min(row): row for row in sparse_basis(basis)}
    remainder = {word: sp.Rational(value) for word, value in vector.items() if value}
    while remainder:
        pivot = min(remainder)
        if pivot not in pivots:
            return False
        multiple = remainder[pivot]
        for word, value in pivots[pivot].items():
            add(remainder, word, -multiple * value)
    return True


def insertion_vectors(u_sites: tuple[int, ...], edge_blocks):
    result = []
    for hole in u_sites:
        rest = tuple(site for site in u_sites if site != hole)
        cofactor = matching_tensor(rest, edge_blocks)
        for colour in COLOURS:
            column = {}
            for rest_word, coefficient in cofactor.items():
                assignment = dict(zip(rest, rest_word))
                assignment[hole] = colour
                add(column, tuple(assignment[site] for site in u_sites), coefficient)
            if column:
                result.append(column)
    return sparse_basis(result)


def cylinder_basis(z: int, edge_blocks):
    u_sites = tuple(site for site in SITES if site != z)
    insertions = insertion_vectors(u_sites, edge_blocks)
    lifted = []
    for colour in COLOURS:
        for vector in insertions:
            column = {}
            for u_word, coefficient in vector.items():
                assignment = dict(zip(u_sites, u_word))
                assignment[z] = colour
                column[tuple(assignment[site] for site in SITES)] = coefficient
            lifted.append(column)
    return sparse_basis(lifted)


def intersection(left, right):
    left = sparse_basis(left)
    right = sparse_basis(right)
    coordinates = sorted({word for vector in left + right for word in vector})
    equations = sp.Matrix([
        [vector.get(word, 0) for vector in left]
        + [-vector.get(word, 0) for vector in right]
        for word in coordinates
    ])
    kernel = equations.nullspace()
    result = []
    for relation in kernel:
        vector = {}
        for coefficient, column in zip(relation[:len(left), :], left):
            if coefficient:
                for word, value in column.items():
                    add(vector, word, coefficient * value)
        if vector:
            result.append(vector)
    return sparse_basis(result)


def intersect_cuts(cuts, cylinders):
    result = cylinders[cuts[0]]
    for cut in cuts[1:]:
        result = intersection(result, cylinders[cut])
    return result


def unit(word):
    return {word: sp.Rational(1)}


def vector_sum(*vectors):
    result = {}
    for vector in vectors:
        for word, coefficient in vector.items():
            add(result, word, coefficient)
    return result


U0 = unit((0, 0, 2, 1, 0, 0))
U1 = unit((1, 2, 1, 2, 0, 0))
U2 = unit((1, 1, 1, 1, 1, 0))
U3 = unit((2, 2, 0, 2, 2, 0))
UPLUS = vector_sum(U1, U2, U3)
HS = vector_sum(U0, UPLUS)


def assert_same_span(observed, expected):
    observed = sparse_basis(observed)
    expected = sparse_basis(expected)
    assert len(observed) == len(expected)
    assert all(in_span(vector, observed) for vector in expected)
    assert all(in_span(vector, expected) for vector in observed)


def check_internal_expansion_and_defects(edge_blocks):
    assert matching_tensor(SITES, edge_blocks) == HS
    expected = {
        0: ((False, False, False), 3),
        1: ((False, False, False), 3),
        2: ((True, False, True), 1),
        3: ((True, True, False), 1),
        4: ((True, False, False), 2),
        5: ((False, True, True), 1),
    }
    for z in SITES:
        u_sites = tuple(site for site in SITES if site != z)
        insertion = insertion_vectors(u_sites, edge_blocks)
        constants = [unit((colour,) * 5) for colour in COLOURS]
        flags = tuple(in_span(constant, insertion) for constant in constants)
        defect = len(sparse_basis(insertion + constants)) - len(insertion)
        assert (flags, defect) == expected[z]


def check_direct_intersections(edge_blocks):
    cylinders = {z: cylinder_basis(z, edge_blocks) for z in SITES}
    three = intersect_cuts((2, 3, 4), cylinders)
    fourth0 = intersect_cuts((2, 3, 4, 0), cylinders)
    fourth1 = intersect_cuts((2, 3, 4, 1), cylinders)
    fourth5 = intersect_cuts((2, 3, 4, 5), cylinders)
    all_six = intersect_cuts((0, 1, 2, 3, 4, 5), cylinders)

    expected_three = [
        unit((0, 0, 0, 0, 0, 0)),
        unit((0, 0, 0, 1, 0, 0)),
        unit((0, 0, 0, 1, 1, 0)),
        unit((0, 0, 0, 1, 2, 0)),
        unit((0, 0, 0, 2, 0, 0)),
        unit((0, 0, 1, 1, 0, 0)),
        U0, UPLUS,
    ]
    assert_same_span(three, expected_three)
    assert_same_span(fourth0, [U0, UPLUS])
    assert_same_span(fourth1, [U0, UPLUS])
    assert_same_span(fourth5, [HS])
    assert_same_span(all_six, [HS])
    assert [len(three), len(fourth0), len(fourth1),
            len(fourth5), len(all_six)] == [8, 2, 2, 1, 1]
    assert [729 - value for value in (8, 2, 2, 1, 1)] == [721, 727, 727, 728, 728]


def lift_formal_atom(i, colour_i, boundary6, j, colour_j, boundary7,
                     edge_blocks):
    rest = tuple(site for site in SITES if site not in (i, j))
    cofactor = matching_tensor(rest, edge_blocks)
    result = {}
    for rest_word, coefficient in cofactor.items():
        assignment = dict(zip(rest, rest_word))
        assignment[i] = colour_i
        assignment[j] = colour_j
        word = tuple(assignment[site] for site in SITES) + (boundary6, boundary7)
        add(result, word, coefficient)
    return result


def check_formal_relaxation(edge_blocks):
    atoms = [
        lift_formal_atom(2, 0, 0, 3, 0, 0, edge_blocks),
        lift_formal_atom(3, 1, 1, 5, 1, 1, edge_blocks),
        lift_formal_atom(2, 2, 2, 5, 2, 2, edge_blocks),
    ]
    assert atoms == [unit((0,) * 8), unit((1,) * 8), unit((2,) * 8)]
    assert vector_sum(*atoms) == vector_sum(
        unit((0,) * 8), unit((1,) * 8), unit((2,) * 8)
    )


def main():
    edge_blocks = aggregate()
    check_internal_expansion_and_defects(edge_blocks)
    check_direct_intersections(edge_blocks)
    check_formal_relaxation(edge_blocks)
    print("independent fixed-interior fourth-cut audit: PASS")
    print("direct primal intersections: dimensions 8,2,2,1,1 with stated bases")
    print("all six constant intersections and target defects: PASS")
    print("formal three-atom Delta uses independent monomials only: PASS")
    print("scope: exact fixed-interior theorem, not star-factor realizability")


if __name__ == "__main__":
    main()
