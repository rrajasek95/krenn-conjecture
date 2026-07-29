#!/usr/bin/env python3
"""Independent exact audit of the one-boundary-star obstructions.

This file deliberately imports no project checker.  It reconstructs the
endpoint-ordered aggregate blocks, matching tensors, five-site insertion
spaces, symbolic 63-cell star coefficient forms, and the literal undo model
directly over Q.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import product


Q = Fraction
ALL_SITES = tuple(range(8))
INTERNAL_SITES = tuple(range(6))
COLOURS = tuple(range(3))

Source = tuple[int, int, int, int, int]
Edge = tuple[int, int]
Cell = tuple[int, int]
Word = tuple[int, ...]
Tensor = dict[Word, Q]
Vector = dict[Word, Q]
Blocks = dict[Edge, dict[Cell, Q]]
StarVariable = tuple[int, int, int, int]
LinearForm = dict[StarVariable, Q]


BASE: tuple[Source, ...] = (
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

REPAIR: tuple[Source, ...] = (
    (2, 3, 2, 1, 1),
    (6, 7, 1, 2, -1),
)

REPAIRED = BASE + REPAIR

W0 = (0, 0, 2, 1, 0, 0, 1, 2)
W1 = (1, 2, 1, 2, 0, 0, 1, 2)
W2 = (1, 1, 1, 1, 1, 0, 1, 2)
W3 = (2, 2, 0, 2, 2, 0, 1, 2)
V6 = (1, 2, 1, 2, 0, 1, 1, 1)


def add_entry(mapping: dict, key, amount: Q) -> None:
    updated = mapping.get(key, Q(0)) + amount
    if updated:
        mapping[key] = updated
    else:
        mapping.pop(key, None)


def canonical_source(source: Source) -> tuple[Edge, Cell, Q]:
    u, v, colour_u, colour_v, weight = source
    if u == v:
        raise ValueError("loops are not permitted")
    if u < v:
        return (u, v), (colour_u, colour_v), Q(weight)
    return (v, u), (colour_v, colour_u), Q(weight)


def aggregate(sources: tuple[Source, ...]) -> Blocks:
    answer: Blocks = {}
    for source in sources:
        edge, cell, weight = canonical_source(source)
        block = answer.setdefault(edge, {})
        add_entry(block, cell, weight)
        if not block:
            answer.pop(edge)
    return answer


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[Edge, ...], ...]:
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    anchor = vertices[0]
    output: list[tuple[Edge, ...]] = []
    for index in range(1, len(vertices)):
        partner = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder):
            output.append(((anchor, partner),) + tail)
    return tuple(output)


def matching_terms(
    vertices: tuple[int, ...], blocks: Blocks
) -> list[tuple[tuple[Edge, ...], Word, Q]]:
    position = {site: index for index, site in enumerate(vertices)}
    output: list[tuple[tuple[Edge, ...], Word, Q]] = []
    for matching in perfect_matchings(vertices):
        choices = [tuple(blocks.get(edge, {}).items()) for edge in matching]
        if any(not edge_choices for edge_choices in choices):
            continue
        for selected in product(*choices):
            word = [-1] * len(vertices)
            coefficient = Q(1)
            for (u, v), (cell, weight) in zip(matching, selected):
                word[position[u]], word[position[v]] = cell
                coefficient *= weight
            output.append((matching, tuple(word), coefficient))
    return output


def matching_tensor(vertices: tuple[int, ...], blocks: Blocks) -> Tensor:
    output: Tensor = {}
    for _matching, word, coefficient in matching_terms(vertices, blocks):
        add_entry(output, word, coefficient)
    return output


def insertion_generators(u_sites: tuple[int, ...], blocks: Blocks) -> list[Vector]:
    output: list[Vector] = []
    for hole in u_sites:
        remaining = tuple(site for site in u_sites if site != hole)
        cofactor = matching_tensor(remaining, blocks)
        for inserted_colour in COLOURS:
            column: Vector = {}
            for cofactor_word, coefficient in cofactor.items():
                assignment = dict(zip(remaining, cofactor_word))
                assignment[hole] = inserted_colour
                word = tuple(assignment[site] for site in u_sites)
                add_entry(column, word, coefficient)
            if column:
                output.append(column)
    return output


def echelon(vectors: list[Vector]) -> dict[Word, Vector]:
    """Sparse exact column-span basis, using the largest word as pivot."""
    pivots: dict[Word, Vector] = {}
    for supplied in vectors:
        vector = {word: Q(value) for word, value in supplied.items() if value}
        while vector:
            pivot = max(vector)
            if pivot not in pivots:
                scale = vector[pivot]
                pivots[pivot] = {
                    word: coefficient / scale for word, coefficient in vector.items()
                }
                break
            multiplier = vector[pivot]
            for word, coefficient in pivots[pivot].items():
                add_entry(vector, word, -multiplier * coefficient)
    return pivots


def lies_in_span(vector: Vector, pivots: dict[Word, Vector]) -> bool:
    remainder = {word: Q(value) for word, value in vector.items() if value}
    while remainder:
        pivot = max(remainder)
        if pivot not in pivots:
            return False
        multiplier = remainder[pivot]
        for word, coefficient in pivots[pivot].items():
            add_entry(remainder, word, -multiplier * coefficient)
    return True


def dot(functional: Vector, vector: Vector) -> Q:
    return sum(
        (coefficient * vector.get(word, Q(0)) for word, coefficient in functional.items()),
        Q(0),
    )


DELTA: Tensor = {(colour,) * 8: Q(1) for colour in COLOURS}


def residual(full_tensor: Tensor) -> Tensor:
    answer = dict(full_tensor)
    for word, coefficient in DELTA.items():
        add_entry(answer, word, -coefficient)
    return answer


def flattened_rows(tensor: Tensor, z: int) -> dict[Word, Vector]:
    c_sites = (z, 6, 7)
    u_sites = tuple(site for site in INTERNAL_SITES if site != z)
    rows: dict[Word, Vector] = {}
    for word, coefficient in tensor.items():
        c_word = tuple(word[site] for site in c_sites)
        u_word = tuple(word[site] for site in u_sites)
        row = rows.setdefault(c_word, {})
        add_entry(row, u_word, coefficient)
        if not row:
            rows.pop(c_word)
    return rows


def cut_summary(z: int, blocks: Blocks, full_tensor: Tensor) -> tuple[bool, int]:
    u_sites = tuple(site for site in INTERNAL_SITES if site != z)
    columns = insertion_generators(u_sites, blocks)
    span = echelon(columns)
    complete = all(
        lies_in_span(row, span) for row in flattened_rows(residual(full_tensor), z).values()
    )
    constants = [{(colour,) * 5: Q(1)} for colour in COLOURS]
    defect = len(echelon(columns + constants)) - len(span)
    return complete, defect


def star_variables(center: int) -> set[StarVariable]:
    output: set[StarVariable] = set()
    for other in ALL_SITES:
        if other == center:
            continue
        u, v = sorted((center, other))
        for colour_u in COLOURS:
            for colour_v in COLOURS:
                output.add((u, v, colour_u, colour_v))
    return output


def fixed_away_from_star(center: int) -> Blocks:
    return aggregate(
        tuple(source for source in REPAIRED if center not in source[:2])
    )


def symbolic_star_coefficient(center: int, word: Word) -> LinearForm:
    """Return [e_word]H as a linear form in the final incident cells."""
    fixed = fixed_away_from_star(center)
    answer: defaultdict[StarVariable, Q] = defaultdict(Q)
    for matching in perfect_matchings(ALL_SITES):
        incident = [edge for edge in matching if center in edge]
        assert len(incident) == 1
        star_edge = incident[0]
        coefficient = Q(1)
        for edge in matching:
            if edge == star_edge:
                continue
            cell = (word[edge[0]], word[edge[1]])
            edge_value = fixed.get(edge, {}).get(cell, Q(0))
            if not edge_value:
                coefficient = Q(0)
                break
            coefficient *= edge_value
        if coefficient:
            variable = (
                star_edge[0],
                star_edge[1],
                word[star_edge[0]],
                word[star_edge[1]],
            )
            answer[variable] += coefficient
    return {variable: coefficient for variable, coefficient in answer.items() if coefficient}


def combine_forms(*terms: tuple[Q, LinearForm]) -> LinearForm:
    answer: dict[StarVariable, Q] = {}
    for scalar, form in terms:
        for variable, coefficient in form.items():
            add_entry(answer, variable, scalar * coefficient)
    return answer


def assembled_word(
    c_sites: tuple[int, ...], c_word: Word, u_sites: tuple[int, ...], u_word: Word
) -> Word:
    assignment = dict(zip(c_sites, c_word))
    assignment.update(zip(u_sites, u_word))
    return tuple(assignment[site] for site in ALL_SITES)


def audit_endpoint_tensor_and_scope() -> None:
    assert len(perfect_matchings(ALL_SITES)) == 105
    for center in (6, 7):
        variables = star_variables(center)
        assert len(variables) == 7 * 3 * 3 == 63
        assert all(center in variable[:2] for variable in variables)

    base_blocks = aggregate(BASE)
    assert base_blocks[(3, 5)] == {(1, 0): Q(1)}
    assert (0, 1) not in base_blocks[(3, 5)]
    base_tensor = matching_tensor(ALL_SITES, base_blocks)
    assert base_tensor == {
        W0: Q(1),
        (1,) * 8: Q(1),
        (2,) * 8: Q(1),
    }

    repaired_tensor = matching_tensor(ALL_SITES, aggregate(REPAIRED))
    assert repaired_tensor == {
        (1,) * 8: Q(1),
        (2,) * 8: Q(1),
        W1: Q(-1),
        W2: Q(-1),
        W3: Q(-1),
    }


def audit_fourth_cut_obstruction() -> None:
    blocks = aggregate(REPAIRED)
    expected_defects = {0: 3, 1: 3, 5: 1}
    baseline_tensor = matching_tensor(ALL_SITES, blocks)
    for z, expected_defect in expected_defects.items():
        u_sites = tuple(site for site in INTERNAL_SITES if site != z)
        beta_zero = {(0,) * 5: Q(1)}
        columns = insertion_generators(u_sites, blocks)
        assert all(dot(beta_zero, column) == 0 for column in columns)
        _complete, defect = cut_summary(z, blocks, baseline_tensor)
        assert defect == expected_defect

        c_sites = (z, 6, 7)
        assert assembled_word(c_sites, (0, 0, 0), u_sites, (0,) * 5) == (0,) * 8

    # This is a symbolic assertion for all 63 final aggregate cells, rather
    # than a collection of numerical star samples.
    for center in (6, 7):
        assert symbolic_star_coefficient(center, (0,) * 8) == {}


def audit_cumulative_identities() -> None:
    # Site 7: x=A_27[22], y=A_67[12].
    x7 = (2, 7, 2, 2)
    y7 = (6, 7, 1, 2)
    all_two_7 = symbolic_star_coefficient(7, (2,) * 8)
    w0_7 = symbolic_star_coefficient(7, W0)
    w1_7 = symbolic_star_coefficient(7, W1)
    assert all_two_7 == {x7: Q(1)}
    assert w0_7 == {x7: Q(1), y7: Q(1)}
    assert w1_7 == {y7: Q(1)}
    assert combine_forms((Q(1), all_two_7), (Q(-1), w0_7), (Q(1), w1_7)) == {}

    blocks = aggregate(REPAIRED)
    u3 = (0, 1, 2, 4, 5)
    beta7 = {(2,) * 5: Q(1)}
    assert all(dot(beta7, column) == 0 for column in insertion_generators(u3, blocks))
    assert assembled_word((3, 6, 7), (2, 2, 2), u3, (2,) * 5) == (2,) * 8

    # Site 6: p=A_36[11], r=A_46[01], y=A_67[12].
    p6 = (3, 6, 1, 1)
    r6 = (4, 6, 0, 1)
    y6 = (6, 7, 1, 2)
    all_one_6 = symbolic_star_coefficient(6, (1,) * 8)
    v6 = symbolic_star_coefficient(6, V6)
    w0_6 = symbolic_star_coefficient(6, W0)
    w1_6 = symbolic_star_coefficient(6, W1)
    assert all_one_6 == {p6: Q(1)}
    assert v6 == {r6: Q(1)}
    assert w0_6 == {p6: Q(1), r6: Q(1), y6: Q(1)}
    assert w1_6 == {y6: Q(1)}
    assert combine_forms(
        (Q(1), all_one_6), (Q(1), v6), (Q(-1), w0_6), (Q(1), w1_6)
    ) == {}

    u2 = (0, 1, 3, 4, 5)
    beta6 = {
        (1, 1, 1, 1, 1): Q(1),
        (1, 2, 2, 0, 1): Q(1),
    }
    assert all(dot(beta6, column) == 0 for column in insertion_generators(u2, blocks))
    assert assembled_word((2, 6, 7), (1, 1, 1), u2, (1,) * 5) == (1,) * 8
    assert (
        assembled_word((2, 6, 7), (1, 1, 1), u2, (1, 2, 2, 0, 1))
        == V6
    )

    # Both beta target contractions are exactly one in the stated colour.
    for beta, target_colour in ((beta7, 2), (beta6, 1)):
        target = tuple(beta.get((colour,) * 5, Q(0)) for colour in COLOURS)
        assert target == tuple(Q(int(colour == target_colour)) for colour in COLOURS)


def audit_literal_undo() -> None:
    # The final +E_12 cell cancels the repaired -E_12 cell on edge 67.
    undo_sources = REPAIRED + ((6, 7, 1, 2, 1),)
    blocks = aggregate(undo_sources)
    assert (6, 7) not in blocks
    assert blocks[(2, 3)] == {(2, 1): Q(1)}

    terms = matching_terms(ALL_SITES, blocks)
    full_tensor = matching_tensor(ALL_SITES, blocks)
    expected = {
        W0: Q(1),
        (1,) * 8: Q(1),
        (2,) * 8: Q(1),
    }
    assert full_tensor == expected
    assert len(terms) == 3
    assert all(full_tensor.get(word, Q(0)) == 0 for word in (W1, W2, W3))

    for z, expected_defect in {2: 1, 3: 1, 4: 2}.items():
        complete, defect = cut_summary(z, blocks, full_tensor)
        assert complete
        assert defect == expected_defect


def main() -> None:
    audit_endpoint_tensor_and_scope()
    audit_fourth_cut_obstruction()
    audit_cumulative_identities()
    audit_literal_undo()
    print("independent boundary-star obstruction audit: PASS")
    print("endpoint order and repaired matching tensor: PASS")
    print("63-cell symbolic star identities over Q (hence C): PASS")
    print("fourth-cut defects (3,3,1) and all-zero obstruction: PASS")
    print("site-7/site-6 cumulative identities and kernel witnesses: PASS")
    print("literal undo cuts and defects (1,1,2): PASS")


if __name__ == "__main__":
    main()
