#!/usr/bin/env python3
"""Exact Q audit of the two-boundary-star cumulative-repair countermodel.

The script imports no project checker.  It expands all 105 matchings,
verifies the complete tensor and four killed debt coordinates, reconstructs
the three residual insertion-cylinder decompositions, computes all six cut
tests, and checks the target-defect dimensions.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import product


Q = Fraction
SITES = tuple(range(8))
SIX = tuple(range(6))
COLOURS = tuple(range(3))

# Nine fixed S-internal sources from the repaired background, followed by
# four simultaneous boundary-star sources.  Every weight is one.
SOURCES = (
    (0, 1, 0, 0, 1),
    (4, 5, 0, 0, 1),
    (0, 2, 1, 1, 1),
    (1, 4, 1, 1, 1),
    (0, 4, 2, 2, 1),
    (1, 3, 2, 2, 1),
    (2, 5, 0, 0, 1),
    (3, 5, 1, 0, 1),
    (2, 3, 2, 1, 1),
    (5, 6, 1, 1, 1),
    (3, 7, 1, 1, 1),
    (2, 6, 2, 2, 1),
    (5, 7, 2, 2, 1),
)

MIXED = (0, 0, 2, 1, 0, 0, 2, 1)
OLD_DEBTS = (
    (0, 0, 2, 1, 0, 0, 1, 2),
    (1, 2, 1, 2, 0, 0, 1, 2),
    (1, 1, 1, 1, 1, 0, 1, 2),
    (2, 2, 0, 2, 2, 0, 1, 2),
)
SYMMETRIC_REPAIR = ((6, 7, 2, 1, -1),)
SWAPPED_DEBTS = (
    (1, 2, 1, 2, 0, 0, 2, 1),
    (1, 1, 1, 1, 1, 0, 2, 1),
    (2, 2, 0, 2, 2, 0, 2, 1),
)

Word = tuple[int, ...]
Vector = dict[Word, Q]
Tensor = dict[Word, Q]
Edge = tuple[int, int]
Cell = tuple[int, int]
Blocks = dict[Edge, dict[Cell, Q]]


def aggregate(sources=SOURCES):
    blocks: Blocks = {}
    for u, v, colour_u, colour_v, weight in sources:
        assert u < v
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


def terms(vertices: tuple[int, ...], blocks: Blocks):
    positions = {site: index for index, site in enumerate(vertices)}
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
            yield matching, tuple(word), coefficient


def matching_tensor(vertices: tuple[int, ...], blocks: Blocks) -> Tensor:
    answer: Tensor = {}
    for _matching, word, coefficient in terms(vertices, blocks):
        add(answer, word, coefficient)
    return answer


def tensor_sum(*summands: tuple[Q, Tensor]) -> Tensor:
    answer: Tensor = {}
    for scalar, tensor in summands:
        for word, coefficient in tensor.items():
            add(answer, word, scalar * coefficient)
    return answer


DELTA: Tensor = {(colour,) * 8: Q(1) for colour in COLOURS}


def insertion_columns(u_sites: tuple[int, ...], blocks: Blocks):
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


def one_insertion(
    u_sites: tuple[int, ...], hole: int, colour: int, blocks: Blocks
) -> Vector:
    rest = tuple(site for site in u_sites if site != hole)
    cofactor = matching_tensor(rest, blocks)
    answer: Vector = {}
    for cofactor_word, coefficient in cofactor.items():
        assignment = dict(zip(rest, cofactor_word))
        assignment[hole] = colour
        add(answer, tuple(assignment[site] for site in u_sites), coefficient)
    return answer


def basis(vectors: list[Vector]):
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


def flatten(tensor: Tensor, c_sites: tuple[int, ...], u_sites: tuple[int, ...]):
    rows: dict[Word, Vector] = {}
    for word, coefficient in tensor.items():
        c_word = tuple(word[site] for site in c_sites)
        u_word = tuple(word[site] for site in u_sites)
        add(rows.setdefault(c_word, {}), u_word, coefficient)
    return rows


def cut_record(z: int, blocks: Blocks, full: Tensor):
    u_sites = tuple(site for site in SIX if site != z)
    c_sites = (z, 6, 7)
    columns = insertion_columns(u_sites, blocks)
    span = basis(columns)
    residual = tensor_sum((Q(1), full), (Q(-1), DELTA))
    complete = all(member(row, span) for row in flatten(residual, c_sites, u_sites).values())
    constants = [{(colour,) * 5: Q(1)} for colour in COLOURS]
    flags = tuple(member(constant, span) for constant in constants)
    defect = len(basis(columns + constants)) - len(span)
    return complete, flags, defect


def lift(c_sites, u_sites, c_word, row: Vector) -> Tensor:
    answer: Tensor = {}
    for u_word, coefficient in row.items():
        assignment = dict(zip(c_sites, c_word))
        assignment.update(zip(u_sites, u_word))
        add(answer, tuple(assignment[site] for site in SITES), coefficient)
    return answer


def audit_tensor(blocks: Blocks) -> Tensor:
    supported = list(terms(SITES, blocks))
    expected_matchings = {
        ((0, 1), (2, 6), (3, 7), (4, 5)),
        ((0, 2), (1, 4), (3, 7), (5, 6)),
        ((0, 4), (1, 3), (2, 6), (5, 7)),
    }
    assert len(matchings(SITES)) == 105
    assert len(supported) == 3
    assert {matching for matching, _word, _coefficient in supported} == expected_matchings
    assert all(coefficient == 1 for _matching, _word, coefficient in supported)
    expected = {
        MIXED: Q(1),
        (1,) * 8: Q(1),
        (2,) * 8: Q(1),
    }
    full = matching_tensor(SITES, blocks)
    assert full == expected
    assert full.get((0,) * 8, Q(0)) == 0
    assert full[(1,) * 8] == full[(2,) * 8] == 1
    assert all(full.get(word, Q(0)) == 0 for word in OLD_DEBTS)
    return full


def audit_explicit_residual_decompositions(blocks: Blocks, full: Tensor) -> None:
    residual = tensor_sum((Q(1), full), (Q(-1), DELTA))
    assert residual == {MIXED: Q(1), (0,) * 8: Q(-1)}
    named = {
        (0, 1, 4, 5): {(0, 0, 0, 0): Q(1)},
        (0, 1, 3, 5): {(0, 0, 1, 0): Q(1)},
        (0, 1, 2, 5): {(0, 0, 0, 0): Q(1)},
    }
    for sites, expected in named.items():
        assert matching_tensor(sites, blocks) == expected
    descriptions = {
        2: (((2, 2, 1), 3, 1, 1), ((0, 0, 0), 3, 0, -1)),
        3: (((1, 2, 1), 2, 2, 1), ((0, 0, 0), 2, 0, -1)),
        4: (((0, 2, 1), 2, 2, 1), ((0, 0, 0), 3, 0, -1)),
    }
    for z, summands in descriptions.items():
        u_sites = tuple(site for site in SIX if site != z)
        c_sites = (z, 6, 7)
        reconstructed: Tensor = {}
        for c_word, hole, colour, scalar in summands:
            row = one_insertion(u_sites, hole, colour, blocks)
            reconstructed = tensor_sum(
                (Q(1), reconstructed),
                (Q(scalar), lift(c_sites, u_sites, c_word, row)),
            )
        assert reconstructed == residual


def audit_all_cuts(blocks: Blocks, full: Tensor) -> None:
    expected = {
        0: (False, (False, False, False), 3),
        1: (False, (False, False, False), 3),
        2: (True, (True, False, True), 1),
        3: (True, (True, True, False), 1),
        4: (True, (True, False, False), 2),
        5: (False, (False, True, True), 1),
    }
    for z in range(6):
        assert cut_record(z, blocks, full) == expected[z]


def audit_symmetric_one_cell_repair() -> None:
    blocks = aggregate(SOURCES + SYMMETRIC_REPAIR)
    full = matching_tensor(SITES, blocks)
    expected = {
        (1,) * 8: Q(1),
        (2,) * 8: Q(1),
        SWAPPED_DEBTS[0]: Q(-1),
        SWAPPED_DEBTS[1]: Q(-1),
        SWAPPED_DEBTS[2]: Q(-1),
    }
    assert full == expected
    assert full.get(MIXED, Q(0)) == 0
    assert all(full.get(word, Q(0)) == 0 for word in OLD_DEBTS)
    audit_all_cuts(blocks, full)


def main() -> None:
    blocks = aggregate()
    full = audit_tensor(blocks)
    audit_explicit_residual_decompositions(blocks, full)
    audit_all_cuts(blocks, full)
    audit_symmetric_one_cell_repair()
    print("two-boundary-star cumulative-repair countermodel: PASS")
    print("exact support is 1^8, 2^8, and 00210021: PASS")
    print("all four prior debt coordinates vanish: PASS")
    print("complete active cuts are exactly z=2,3,4 with defects 1,1,2: PASS")
    print("no fourth cut is complete and the colour-zero diagonal is missing: PASS")
    print("one-cell symmetric repair moves 00210021 to three suffix-21 debts: PASS")


if __name__ == "__main__":
    main()
