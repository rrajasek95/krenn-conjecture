#!/usr/bin/env python3
"""Exact audit of a three-adjacent-five-cut quotient countermodel.

The displayed twelve endpoint-decorated sources are expanded over Q.  The
checker verifies the full matching tensor, the shared residual
intersection, all three complete high-sector quotient identities, the
three nonzero target defects, and support-minimality inside the displayed
source family.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import product


B = tuple(range(8))
S = tuple(range(6))
R = (6, 7)
ACTIVE = (2, 3, 4)

# (lower endpoint, upper endpoint, colour at lower endpoint,
#  colour at upper endpoint, weight).  In particular 35 is asymmetric.
SOURCES = (
    (0, 1, 0, 0, 1),
    (4, 5, 0, 0, 1),
    (0, 2, 1, 1, 1),
    (1, 4, 1, 1, 1),
    (3, 6, 1, 1, 1),
    (5, 7, 1, 1, 1),
    (0, 4, 2, 2, 1),
    (1, 3, 2, 2, 1),
    (2, 7, 2, 2, 1),
    (5, 6, 2, 2, 1),
    (2, 5, 0, 0, 1),
    (3, 5, 1, 0, 1),
)

REPAIR_SOURCES = (
    (2, 3, 2, 1, 1),
    (6, 7, 1, 2, -1),
)


def edge(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a < b else (b, a)


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index, second in enumerate(vertices[1:]):
        rest = vertices[1:index + 1] + vertices[index + 2:]
        for matching in perfect_matchings(rest):
            answer.append((edge(first, second),) + matching)
    return tuple(answer)


Tensor = dict[tuple[int, ...], Fraction]
Sparse = dict[int, Fraction]


def cells_from_mask(mask: int | None = None):
    cells = {}
    if mask is None:
        mask = (1 << len(SOURCES)) - 1
    for index, (a, b, ca, cb, weight) in enumerate(SOURCES):
        if mask & (1 << index):
            cells.setdefault((a, b), []).append((ca, cb, Fraction(weight)))
    return cells


def add_sources(cells, sources) -> None:
    for a, b, ca, cb, weight in sources:
        cells.setdefault((a, b), []).append((ca, cb, Fraction(weight)))


def add_term(tensor: Tensor, word: tuple[int, ...], value) -> None:
    value = Fraction(value)
    new = tensor.get(word, Fraction(0)) + value
    if new:
        tensor[word] = new
    else:
        tensor.pop(word, None)


def matching_terms(vertices: tuple[int, ...], cells):
    positions = {vertex: index for index, vertex in enumerate(vertices)}
    for matching in perfect_matchings(vertices):
        choices = [cells.get(pair, ()) for pair in matching]
        if any(not choice for choice in choices):
            continue
        for selected in product(*choices):
            word = [-1] * len(vertices)
            coefficient = Fraction(1)
            for (a, b), (ca, cb, weight) in zip(matching, selected):
                word[positions[a]] = ca
                word[positions[b]] = cb
                coefficient *= weight
            yield matching, tuple(word), coefficient


def matching_tensor(vertices: tuple[int, ...], cells) -> Tensor:
    answer: Tensor = {}
    for _matching, word, coefficient in matching_terms(vertices, cells):
        add_term(answer, word, coefficient)
    return answer


def sector(c_set: tuple[int, ...], crossings: int, cells) -> Tensor:
    left = set(c_set)
    answer: Tensor = {}
    for matching, word, coefficient in matching_terms(B, cells):
        count = sum((a in left) != (b in left) for a, b in matching)
        if count == crossings:
            add_term(answer, word, coefficient)
    return answer


WORDS5 = tuple(product(range(3), repeat=5))
WORD5_INDEX = {word: index for index, word in enumerate(WORDS5)}


def cofactor_columns(u_set: tuple[int, ...], cells) -> list[Sparse]:
    columns = []
    for hole in u_set:
        remaining = tuple(x for x in u_set if x != hole)
        cofactor = matching_tensor(remaining, cells)
        for colour in range(3):
            column: Sparse = {}
            for hword, coefficient in cofactor.items():
                assignment = {hole: colour}
                assignment.update(zip(remaining, hword))
                index = WORD5_INDEX[tuple(assignment[x] for x in u_set)]
                column[index] = column.get(index, Fraction(0)) + coefficient
            if column:
                columns.append(column)
    return columns


def insertion_column(
    u_set: tuple[int, ...], hole: int, colour: int, cells
) -> Sparse:
    remaining = tuple(x for x in u_set if x != hole)
    cofactor = matching_tensor(remaining, cells)
    column: Sparse = {}
    for hword, coefficient in cofactor.items():
        assignment = {hole: colour}
        assignment.update(zip(remaining, hword))
        index = WORD5_INDEX[tuple(assignment[x] for x in u_set)]
        column[index] = column.get(index, Fraction(0)) + coefficient
    return column


def rational_basis(vectors: list[Sparse]) -> dict[int, Sparse]:
    basis: dict[int, Sparse] = {}
    for source in vectors:
        vector = {i: Fraction(value) for i, value in source.items() if value}
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                scale = vector[pivot]
                basis[pivot] = {i: value / scale for i, value in vector.items()}
                break
            coefficient = vector[pivot]
            for i, value in basis[pivot].items():
                new = vector.get(i, Fraction(0)) - coefficient * value
                if new:
                    vector[i] = new
                else:
                    vector.pop(i, None)
    return basis


def rational_member(source: Sparse, basis: dict[int, Sparse]) -> bool:
    vector = {i: Fraction(value) for i, value in source.items() if value}
    while vector:
        pivot = min(vector)
        if pivot not in basis:
            return False
        coefficient = vector[pivot]
        for i, value in basis[pivot].items():
            new = vector.get(i, Fraction(0)) - coefficient * value
            if new:
                vector[i] = new
            else:
                vector.pop(i, None)
    return True


def tensor_sum(*tensors: Tensor) -> Tensor:
    answer: Tensor = {}
    for tensor in tensors:
        for word, coefficient in tensor.items():
            add_term(answer, word, coefficient)
    return answer


def scaled(tensor: Tensor, scalar: int) -> Tensor:
    return {word: scalar * coefficient for word, coefficient in tensor.items()}


def flatten_rows(
    tensor: Tensor, c_set: tuple[int, ...], u_set: tuple[int, ...]
) -> dict[tuple[int, ...], Sparse]:
    rows = {}
    for word, coefficient in tensor.items():
        cword = tuple(word[x] for x in c_set)
        uword = tuple(word[x] for x in u_set)
        row = rows.setdefault(cword, {})
        index = WORD5_INDEX[uword]
        row[index] = row.get(index, Fraction(0)) + coefficient
        if not row[index]:
            row.pop(index)
    return rows


DELTA: Tensor = {(colour,) * 8: Fraction(1) for colour in range(3)}


def cut_record(z: int, cells):
    u_set = tuple(x for x in S if x != z)
    c_set = (z, 6, 7)
    columns = cofactor_columns(u_set, cells)
    basis = rational_basis(columns)
    constants = [
        {WORD5_INDEX[(colour,) * 5]: Fraction(1)} for colour in range(3)
    ]
    t1 = sector(c_set, 1, cells)
    t3 = sector(c_set, 3, cells)
    residual = tensor_sum(t3, scaled(DELTA, -1))
    full = all(
        rational_member(row, basis)
        for row in flatten_rows(residual, c_set, u_set).values()
    )
    one_cross_factors = all(
        rational_member(row, basis)
        for row in flatten_rows(t1, c_set, u_set).values()
    )
    augmented = rational_basis(columns + constants)
    constant_members = tuple(rational_member(row, basis) for row in constants)
    return {
        "full": full,
        "defect": len(augmented) - len(basis),
        "constant_members": constant_members,
        "one_cross_factors": one_cross_factors,
        "rank": len(basis),
        "t1": t1,
        "t3": t3,
    }


def lift_row(
    c_set: tuple[int, ...], u_set: tuple[int, ...], cword, row: Sparse
) -> Tensor:
    answer: Tensor = {}
    for index, coefficient in row.items():
        uword = WORDS5[index]
        word = [-1] * 8
        for vertex, colour in zip(c_set, cword):
            word[vertex] = colour
        for vertex, colour in zip(u_set, uword):
            word[vertex] = colour
        add_term(answer, tuple(word), coefficient)
    return answer


def audit_full_tensor(cells) -> Tensor:
    terms = list(matching_terms(B, cells))
    expected_matchings = {
        ((0, 1), (2, 7), (3, 6), (4, 5)),
        ((0, 2), (1, 4), (3, 6), (5, 7)),
        ((0, 4), (1, 3), (2, 7), (5, 6)),
    }
    assert {matching for matching, _word, _coefficient in terms} == expected_matchings
    assert all(coefficient == 1 for _matching, _word, coefficient in terms)
    expected = {
        (0, 0, 2, 1, 0, 0, 1, 2): Fraction(1),
        (1,) * 8: Fraction(1),
        (2,) * 8: Fraction(1),
    }
    observed = matching_tensor(B, cells)
    assert observed == expected
    return observed


def audit_shared_residual(cells, full_tensor: Tensor) -> None:
    residual = tensor_sum(full_tensor, scaled(DELTA, -1))
    expected = {
        (0, 0, 2, 1, 0, 0, 1, 2): Fraction(1),
        (0,) * 8: Fraction(-1),
    }
    assert residual == expected

    # These are explicit cofactor-insertion decompositions of the same D
    # on the three adjacent cuts.
    descriptions = {
        2: (((2, 1, 2), 3, 1, 1), ((0, 0, 0), 3, 0, -1)),
        3: (((1, 1, 2), 2, 2, 1), ((0, 0, 0), 2, 0, -1)),
        4: (((0, 1, 2), 2, 2, 1), ((0, 0, 0), 3, 0, -1)),
    }
    for z, summands in descriptions.items():
        u_set = tuple(x for x in S if x != z)
        c_set = (z, 6, 7)
        reconstructed: Tensor = {}
        for cword, hole, colour, coefficient in summands:
            column = insertion_column(u_set, hole, colour, cells)
            assert column
            reconstructed = tensor_sum(
                reconstructed,
                scaled(lift_row(c_set, u_set, cword, column), coefficient),
            )
        assert reconstructed == residual


def audit_three_complete_quotients(cells) -> None:
    expected_members = {
        2: (True, False, True),
        3: (True, True, False),
        4: (True, False, False),
    }
    expected_t3 = {
        2: {(1,) * 8: Fraction(1)},
        3: {(2,) * 8: Fraction(1)},
        4: {
            (0, 0, 2, 1, 0, 0, 1, 2): Fraction(1),
            (1,) * 8: Fraction(1),
            (2,) * 8: Fraction(1),
        },
    }
    for z in ACTIVE:
        record = cut_record(z, cells)
        assert record["one_cross_factors"]
        assert record["full"]
        assert record["defect"] == expected_members[z].count(False)
        assert record["constant_members"] == expected_members[z]
        assert record["t3"] == expected_t3[z]


def audit_support_minimality() -> None:
    full_mask = (1 << len(SOURCES)) - 1
    survivors = []
    for mask in range(1, full_mask):
        cells = cells_from_mask(mask)
        if all(
            (record := cut_record(z, cells))["full"] and record["defect"]
            for z in ACTIVE
        ):
            survivors.append(mask)
    assert not survivors


def audit_mixed_word_repair() -> None:
    cells = cells_from_mask()
    add_sources(cells, REPAIR_SOURCES)
    killed_word = (0, 0, 2, 1, 0, 0, 1, 2)
    expected = {
        (1,) * 8: Fraction(1),
        (2,) * 8: Fraction(1),
        (1, 2, 1, 2, 0, 0, 1, 2): Fraction(-1),
        (1, 1, 1, 1, 1, 0, 1, 2): Fraction(-1),
        (2, 2, 0, 2, 2, 0, 1, 2): Fraction(-1),
    }
    full_tensor = matching_tensor(B, cells)
    assert full_tensor == expected
    assert killed_word not in full_tensor
    residual = tensor_sum(full_tensor, scaled(DELTA, -1))
    for z in ACTIVE:
        record = cut_record(z, cells)
        assert record["full"] and record["one_cross_factors"]
        assert record["defect"] == (1 if z in (2, 3) else 2)
        u_set = tuple(x for x in S if x != z)
        c_set = (z, 6, 7)
        basis = rational_basis(cofactor_columns(u_set, cells))
        assert all(
            rational_member(row, basis)
            for row in flatten_rows(residual, c_set, u_set).values()
        )


def main() -> None:
    cells = cells_from_mask()
    full_tensor = audit_full_tensor(cells)
    audit_shared_residual(cells, full_tensor)
    audit_three_complete_quotients(cells)
    audit_support_minimality()
    audit_mixed_word_repair()
    print("three adjacent complete five-cut quotient countermodel: PASS")
    print("shared residual lies in all three cofactor-insertion cylinders: PASS")
    print("defect dimensions on z=2,3,4 are 1,1,2: PASS")
    print("all 4094 proper displayed source subfamilies fail the fixed triple: PASS")
    print("two-source exact repair kills 00210012 and preserves the triple: PASS")


if __name__ == "__main__":
    main()
