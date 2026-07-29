#!/usr/bin/env python3
"""Exact Q audit of the fixed-interior three/four-cut intersections.

This standalone checker reconstructs the repaired six-site interior,
forms every five-site cofactor-insertion cylinder, and computes their
intersections by algebraic annihilator duality in the 3^6 word basis.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import product


Q = Fraction
SIX = tuple(range(6))
COLOURS = tuple(range(3))
WORDS6 = tuple(product(COLOURS, repeat=6))

INTERNAL_SOURCES = (
    (0, 1, 0, 0, 1),
    (4, 5, 0, 0, 1),
    (0, 2, 1, 1, 1),
    (1, 4, 1, 1, 1),
    (0, 4, 2, 2, 1),
    (1, 3, 2, 2, 1),
    (2, 5, 0, 0, 1),
    (3, 5, 1, 0, 1),
    (2, 3, 2, 1, 1),
)

Word = tuple[int, ...]
Vector = dict[Word, Q]
Tensor = dict[Word, Q]


def aggregate():
    blocks = {}
    for u, v, colour_u, colour_v, weight in INTERNAL_SOURCES:
        block = blocks.setdefault((u, v), {})
        cell = (colour_u, colour_v)
        block[cell] = block.get(cell, Q(0)) + Q(weight)
    return blocks


@lru_cache(maxsize=None)
def matchings(vertices: tuple[int, ...]):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def add(container: dict, key, value: Q) -> None:
    total = container.get(key, Q(0)) + value
    if total:
        container[key] = total
    else:
        container.pop(key, None)


def matching_tensor(vertices: tuple[int, ...], blocks) -> Tensor:
    positions = {site: index for index, site in enumerate(vertices)}
    answer: Tensor = {}
    for matching in matchings(vertices):
        choices = [tuple(blocks.get(edge, {}).items()) for edge in matching]
        if any(not choice for choice in choices):
            continue
        for selected in product(*choices):
            word = [-1] * len(vertices)
            coefficient = Q(1)
            for (u, v), ((colour_u, colour_v), weight) in zip(matching, selected):
                word[positions[u]] = colour_u
                word[positions[v]] = colour_v
                coefficient *= weight
            add(answer, tuple(word), coefficient)
    return answer


def insertion_columns(u_sites: tuple[int, ...], blocks) -> list[Vector]:
    columns: list[Vector] = []
    for hole in u_sites:
        rest = tuple(site for site in u_sites if site != hole)
        cofactor = matching_tensor(rest, blocks)
        for colour in COLOURS:
            column: Vector = {}
            for cofactor_word, coefficient in cofactor.items():
                assignment = dict(zip(rest, cofactor_word))
                assignment[hole] = colour
                add(column, tuple(assignment[site] for site in u_sites), coefficient)
            if column:
                columns.append(column)
    return columns


def echelon(vectors: list[Vector]):
    answer: dict[Word, Vector] = {}
    for supplied in vectors:
        vector = {word: Q(value) for word, value in supplied.items() if value}
        while vector:
            pivot = min(vector)
            if pivot not in answer:
                scale = vector[pivot]
                answer[pivot] = {word: value / scale for word, value in vector.items()}
                break
            multiple = vector[pivot]
            for word, value in answer[pivot].items():
                updated = vector.get(word, Q(0)) - multiple * value
                if updated:
                    vector[word] = updated
                else:
                    vector.pop(word, None)
    return answer


def member(vector: Vector, span: dict[Word, Vector]) -> bool:
    remainder = {word: Q(value) for word, value in vector.items() if value}
    while remainder:
        pivot = min(remainder)
        if pivot not in span:
            return False
        multiple = remainder[pivot]
        for word, value in span[pivot].items():
            updated = remainder.get(word, Q(0)) - multiple * value
            if updated:
                remainder[word] = updated
            else:
                remainder.pop(word, None)
    return True


def rref_equations(equations: list[Vector], coordinates: tuple[Word, ...]):
    rows = [{word: Q(value) for word, value in row.items() if value} for row in equations]
    rows = [row for row in rows if row]
    pivots = []
    active = 0
    for coordinate in coordinates:
        found = next(
            (index for index in range(active, len(rows)) if rows[index].get(coordinate)),
            None,
        )
        if found is None:
            continue
        rows[active], rows[found] = rows[found], rows[active]
        scale = rows[active][coordinate]
        rows[active] = {word: value / scale for word, value in rows[active].items()}
        for index, row in enumerate(rows):
            if index == active or not row.get(coordinate):
                continue
            multiple = row[coordinate]
            for word, value in rows[active].items():
                updated = row.get(word, Q(0)) - multiple * value
                if updated:
                    row[word] = updated
                else:
                    row.pop(word, None)
        pivots.append(coordinate)
        active += 1
        if active == len(rows):
            break
    assert all(not row for row in rows[active:])
    return rows[:active], tuple(pivots)


def annihilator_basis(equations: list[Vector], coordinates: tuple[Word, ...]):
    rows, pivots = rref_equations(equations, coordinates)
    pivot_set = set(pivots)
    answer = []
    for free in coordinates:
        if free in pivot_set:
            continue
        vector: Vector = {free: Q(1)}
        for row, pivot in zip(rows, pivots):
            value = -row.get(free, Q(0))
            if value:
                vector[pivot] = value
        answer.append(vector)
    return answer


def lifted_cylinder_annihilators(z: int, blocks) -> list[Vector]:
    u_sites = tuple(site for site in SIX if site != z)
    columns = insertion_columns(u_sites, blocks)
    k_basis = annihilator_basis(columns, tuple(product(COLOURS, repeat=5)))
    lifted = []
    for colour_z in COLOURS:
        for beta in k_basis:
            functional: Vector = {}
            for u_word, coefficient in beta.items():
                assignment = dict(zip(u_sites, u_word))
                assignment[z] = colour_z
                functional[tuple(assignment[site] for site in SIX)] = coefficient
            lifted.append(functional)
    return lifted


def cylinder_intersection(cuts: tuple[int, ...], blocks) -> list[Vector]:
    equations = []
    for z in cuts:
        equations.extend(lifted_cylinder_annihilators(z, blocks))
    return annihilator_basis(equations, WORDS6)


def unit(word: Word) -> Vector:
    return {word: Q(1)}


def vector_sum(*vectors: Vector) -> Vector:
    answer: Vector = {}
    for vector in vectors:
        for word, coefficient in vector.items():
            add(answer, word, coefficient)
    return answer


U0 = unit((0, 0, 2, 1, 0, 0))
U1 = unit((1, 2, 1, 2, 0, 0))
U2 = unit((1, 1, 1, 1, 1, 0))
U3 = unit((2, 2, 0, 2, 2, 0))
TAIL_SUM = vector_sum(U1, U2, U3)
H_S_EXPECTED = vector_sum(U0, TAIL_SUM)


def assert_same_span(observed: list[Vector], expected: list[Vector]) -> None:
    observed_basis = echelon(observed)
    expected_basis = echelon(expected)
    assert len(observed_basis) == len(expected_basis)
    assert all(member(vector, observed_basis) for vector in expected)
    assert all(member(vector, expected_basis) for vector in observed)


def audit_internal_tensor_and_defects(blocks) -> None:
    assert matching_tensor(SIX, blocks) == H_S_EXPECTED
    expected_flags = {
        0: (False, False, False),
        1: (False, False, False),
        2: (True, False, True),
        3: (True, True, False),
        4: (True, False, False),
        5: (False, True, True),
    }
    for z in range(6):
        u_sites = tuple(site for site in SIX if site != z)
        columns = insertion_columns(u_sites, blocks)
        span = echelon(columns)
        constants = [unit((colour,) * 5) for colour in COLOURS]
        flags = tuple(member(constant, span) for constant in constants)
        defect = len(echelon(columns + constants)) - len(span)
        assert flags == expected_flags[z]
        assert defect == expected_flags[z].count(False)


def audit_intersections(blocks) -> None:
    three_expected = [
        unit((0, 0, 0, 0, 0, 0)),
        unit((0, 0, 0, 1, 0, 0)),
        unit((0, 0, 0, 1, 1, 0)),
        unit((0, 0, 0, 1, 2, 0)),
        unit((0, 0, 0, 2, 0, 0)),
        unit((0, 0, 1, 1, 0, 0)),
        U0,
        TAIL_SUM,
    ]
    assert_same_span(cylinder_intersection((2, 3, 4), blocks), three_expected)
    assert_same_span(cylinder_intersection((2, 3, 4, 0), blocks), [U0, TAIL_SUM])
    assert_same_span(cylinder_intersection((2, 3, 4, 1), blocks), [U0, TAIL_SUM])
    assert_same_span(cylinder_intersection((2, 3, 4, 5), blocks), [H_S_EXPECTED])
    assert_same_span(cylinder_intersection((0, 1, 2, 3, 4, 5), blocks), [H_S_EXPECTED])


def audit_formal_three_atom_relaxation(blocks) -> None:
    # Three independently controlled cross monomials can make Delta exactly.
    # Sharing the underlying star cells would also activate cross products;
    # this check deliberately certifies only the formal linear relaxation.
    data = (
        (2, 0, 0, 3, 0, 0),
        (3, 1, 1, 5, 1, 1),
        (2, 2, 2, 5, 2, 2),
    )
    full_terms = []
    for i, colour_i, boundary_6, j, colour_j, boundary_7 in data:
        rest = tuple(site for site in SIX if site not in (i, j))
        cofactor = matching_tensor(rest, blocks)
        lifted: Tensor = {}
        for rest_word, coefficient in cofactor.items():
            assignment = dict(zip(rest, rest_word))
            assignment[i] = colour_i
            assignment[j] = colour_j
            full_word = tuple(assignment[site] for site in SIX) + (
                boundary_6,
                boundary_7,
            )
            add(lifted, full_word, coefficient)
        full_terms.append(lifted)
    assert full_terms == [
        {(0,) * 8: Q(1)},
        {(1,) * 8: Q(1)},
        {(2,) * 8: Q(1)},
    ]


def main() -> None:
    blocks = aggregate()
    audit_internal_tensor_and_defects(blocks)
    audit_intersections(blocks)
    audit_formal_three_atom_relaxation(blocks)
    print("fixed-interior three/four-cut cylinder intersections: PASS")
    print("cuts 2,3,4 intersection dimension 8 with explicit basis: PASS")
    print("adding cut 0 or 1 leaves the explicit two-plane: PASS")
    print("adding cut 5, or all six cuts, leaves span(H_S): PASS")
    print("formal independent-monomial Delta realization is not star-factorized: PASS")


if __name__ == "__main__":
    main()
