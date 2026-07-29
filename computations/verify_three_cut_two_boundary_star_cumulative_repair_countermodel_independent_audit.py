#!/usr/bin/env python3
"""Independent audit of the two-boundary-star cumulative repair model.

This checker imports no project module.  It uses a dense SymPy rational
matrix implementation, distinct from the primary sparse reducer, while
rebuilding all endpoint-ordered matching tensors from source cells.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import product

import sympy as sp


SITES = tuple(range(8))
INTERIOR = tuple(range(6))
COLOURS = (0, 1, 2)

BASE_SOURCES = (
    (0, 1, 0, 0, 1), (4, 5, 0, 0, 1),
    (0, 2, 1, 1, 1), (1, 4, 1, 1, 1),
    (0, 4, 2, 2, 1), (1, 3, 2, 2, 1),
    (2, 5, 0, 0, 1), (3, 5, 1, 0, 1),
    (2, 3, 2, 1, 1),
    (5, 6, 1, 1, 1), (3, 7, 1, 1, 1),
    (2, 6, 2, 2, 1), (5, 7, 2, 2, 1),
)

REPAIR = ((6, 7, 2, 1, -1),)
MIXED = (0, 0, 2, 1, 0, 0, 2, 1)
OLD = (
    (0, 0, 2, 1, 0, 0, 1, 2),
    (1, 2, 1, 2, 0, 0, 1, 2),
    (1, 1, 1, 1, 1, 0, 1, 2),
    (2, 2, 0, 2, 2, 0, 1, 2),
)
NEW_DEBTS = (
    (1, 2, 1, 2, 0, 0, 2, 1),
    (1, 1, 1, 1, 1, 0, 2, 1),
    (2, 2, 0, 2, 2, 0, 2, 1),
)


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        mate = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            answer.append(((first, mate),) + tail)
    return tuple(answer)


def blocks(sources):
    answer = {}
    for left, right, colour_left, colour_right, weight in sources:
        assert left < right
        cell_map = answer.setdefault((left, right), {})
        cell = (colour_left, colour_right)
        cell_map[cell] = cell_map.get(cell, sp.Rational(0)) + sp.Rational(weight)
    return answer


def expanded_terms(vertices: tuple[int, ...], edge_blocks):
    positions = {site: index for index, site in enumerate(vertices)}
    answer = []
    for matching in perfect_matchings(vertices):
        options = [tuple(edge_blocks.get(edge, {}).items()) for edge in matching]
        if any(not option for option in options):
            continue
        for choices in product(*options):
            word = [-1] * len(vertices)
            coefficient = sp.Rational(1)
            for edge, (cell, weight) in zip(matching, choices):
                left, right = edge
                word[positions[left]], word[positions[right]] = cell
                coefficient *= weight
            if coefficient:
                answer.append((matching, tuple(word), coefficient))
    return answer


def tensor(vertices: tuple[int, ...], edge_blocks):
    answer = {}
    for _matching, word, coefficient in expanded_terms(vertices, edge_blocks):
        answer[word] = answer.get(word, 0) + coefficient
        if answer[word] == 0:
            del answer[word]
    return answer


def vector(word_order, entries):
    return sp.Matrix([entries.get(word, 0) for word in word_order])


def insertion_matrix(u_sites: tuple[int, ...], edge_blocks):
    word_order = tuple(product(COLOURS, repeat=len(u_sites)))
    columns = []
    for hole in u_sites:
        rest = tuple(site for site in u_sites if site != hole)
        cofactor = tensor(rest, edge_blocks)
        for colour in COLOURS:
            entries = {}
            for rest_word, coefficient in cofactor.items():
                assignment = dict(zip(rest, rest_word))
                assignment[hole] = colour
                word = tuple(assignment[site] for site in u_sites)
                entries[word] = entries.get(word, 0) + coefficient
            if entries:
                columns.append(vector(word_order, entries))
    matrix = sp.Matrix.hstack(*columns) if columns else sp.zeros(len(word_order), 0)
    return word_order, matrix


def in_column_span(candidate: sp.Matrix, matrix: sp.Matrix) -> bool:
    return matrix.rank() == sp.Matrix.hstack(matrix, candidate).rank()


def cut_data(z: int, edge_blocks, full):
    u_sites = tuple(site for site in INTERIOR if site != z)
    c_sites = (z, 6, 7)
    word_order, insertion = insertion_matrix(u_sites, edge_blocks)
    residual = dict(full)
    for colour in COLOURS:
        diagonal = (colour,) * 8
        residual[diagonal] = residual.get(diagonal, 0) - 1
        if residual[diagonal] == 0:
            del residual[diagonal]

    rows = {}
    for word, coefficient in residual.items():
        c_word = tuple(word[site] for site in c_sites)
        u_word = tuple(word[site] for site in u_sites)
        rows.setdefault(c_word, {})[u_word] = coefficient
    complete = all(in_column_span(vector(word_order, row), insertion)
                   for row in rows.values())

    constants = [vector(word_order, {(colour,) * 5: 1})
                 for colour in COLOURS]
    flags = tuple(in_column_span(constant, insertion) for constant in constants)
    augmented = sp.Matrix.hstack(insertion, *constants)
    defect = augmented.rank() - insertion.rank()
    return complete, flags, defect


def inserted_row(u_sites, hole, colour, edge_blocks):
    rest = tuple(site for site in u_sites if site != hole)
    cofactor = tensor(rest, edge_blocks)
    result = {}
    for rest_word, coefficient in cofactor.items():
        assignment = dict(zip(rest, rest_word))
        assignment[hole] = colour
        result[tuple(assignment[site] for site in u_sites)] = coefficient
    return result


def lift(c_sites, u_sites, c_word, row, scalar):
    result = {}
    for u_word, coefficient in row.items():
        assignment = dict(zip(c_sites, c_word))
        assignment.update(zip(u_sites, u_word))
        word = tuple(assignment[site] for site in SITES)
        result[word] = result.get(word, 0) + scalar * coefficient
    return result


def add_tensors(*summands):
    result = {}
    for supplied in summands:
        for word, coefficient in supplied.items():
            result[word] = result.get(word, 0) + coefficient
            if result[word] == 0:
                del result[word]
    return result


def check_base_family():
    edge_blocks = blocks(BASE_SOURCES)
    terms = expanded_terms(SITES, edge_blocks)
    assert len(perfect_matchings(SITES)) == 105
    assert [(matching, word, coefficient) for matching, word, coefficient in terms] == [
        (((0, 1), (2, 6), (3, 7), (4, 5)), MIXED, 1),
        (((0, 2), (1, 4), (3, 7), (5, 6)), (1,) * 8, 1),
        (((0, 4), (1, 3), (2, 6), (5, 7)), (2,) * 8, 1),
    ]
    full = tensor(SITES, edge_blocks)
    assert full == {MIXED: 1, (1,) * 8: 1, (2,) * 8: 1}
    assert full.get((0,) * 8, 0) == 0
    assert all(full.get(word, 0) == 0 for word in OLD)

    assert tensor((0, 1, 4, 5), edge_blocks) == {(0, 0, 0, 0): 1}
    assert tensor((0, 1, 3, 5), edge_blocks) == {(0, 0, 1, 0): 1}
    assert tensor((0, 1, 2, 5), edge_blocks) == {(0, 0, 0, 0): 1}

    residual = {MIXED: 1, (0,) * 8: -1}
    decompositions = {
        2: (((2, 2, 1), 3, 1, 1), ((0, 0, 0), 3, 0, -1)),
        3: (((1, 2, 1), 2, 2, 1), ((0, 0, 0), 2, 0, -1)),
        4: (((0, 2, 1), 2, 2, 1), ((0, 0, 0), 3, 0, -1)),
    }
    for z, data in decompositions.items():
        u_sites = tuple(site for site in INTERIOR if site != z)
        c_sites = (z, 6, 7)
        pieces = []
        for c_word, hole, colour, scalar in data:
            pieces.append(lift(c_sites, u_sites, c_word,
                               inserted_row(u_sites, hole, colour, edge_blocks),
                               scalar))
        assert add_tensors(*pieces) == residual

    expected_cuts = {
        0: (False, (False, False, False), 3),
        1: (False, (False, False, False), 3),
        2: (True, (True, False, True), 1),
        3: (True, (True, True, False), 1),
        4: (True, (True, False, False), 2),
        5: (False, (False, True, True), 1),
    }
    assert {z: cut_data(z, edge_blocks, full) for z in INTERIOR} == expected_cuts
    return full


def check_one_cell_repair():
    edge_blocks = blocks(BASE_SOURCES + REPAIR)
    terms = expanded_terms(SITES, edge_blocks)
    # Three original supported matchings plus four matchings through 67.
    assert len(terms) == 7
    full = tensor(SITES, edge_blocks)
    assert full == {
        (1,) * 8: 1,
        (2,) * 8: 1,
        NEW_DEBTS[0]: -1,
        NEW_DEBTS[1]: -1,
        NEW_DEBTS[2]: -1,
    }
    assert full.get(MIXED, 0) == 0
    assert all(full.get(word, 0) == 0 for word in OLD)
    expected_cuts = {
        0: (False, (False, False, False), 3),
        1: (False, (False, False, False), 3),
        2: (True, (True, False, True), 1),
        3: (True, (True, True, False), 1),
        4: (True, (True, False, False), 2),
        5: (False, (False, True, True), 1),
    }
    assert {z: cut_data(z, edge_blocks, full) for z in INTERIOR} == expected_cuts


def main():
    check_base_family()
    check_one_cell_repair()
    print("independent cumulative two-boundary-star audit: PASS")
    print("endpoint-ordered full support and all old/new debts: PASS")
    print("complete cuts exactly 2,3,4; defects (1,1,2): PASS")
    print("single 67 repair transports the debt to three suffix-21 words: PASS")
    print("scope: exact relaxation countermodel, not a Krenn counterexample")


if __name__ == "__main__":
    main()
