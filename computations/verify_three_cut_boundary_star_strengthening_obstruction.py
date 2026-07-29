#!/usr/bin/env python3
"""Exact audit of boundary-star obstructions beyond the three-cut model.

Every non-star aggregate cell is fixed to the repaired sparse construction,
while all 63 decorated cells incident to site 6 or site 7 are allowed to be
arbitrary.  The script verifies the coefficient identities obstructing a
fourth cut and a cumulative mixed-word repair, and checks the literal
three-debt-word undo model over Q.  It imports no project checker.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import product


Q = Fraction
SITES = tuple(range(8))
SIX = tuple(range(6))
COLOURS = tuple(range(3))

PRIMARY = (
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

REPAIR = (
    (2, 3, 2, 1, 1),
    (6, 7, 1, 2, -1),
)

REPAIRED = PRIMARY + REPAIR

W0 = (0, 0, 2, 1, 0, 0, 1, 2)
W1 = (1, 2, 1, 2, 0, 0, 1, 2)
W2 = (1, 1, 1, 1, 1, 0, 1, 2)
W3 = (2, 2, 0, 2, 2, 0, 1, 2)
V6 = (1, 2, 1, 2, 0, 1, 1, 1)

Word = tuple[int, ...]
Vector = dict[Word, Q]
Tensor = dict[Word, Q]
Edge = tuple[int, int]
Cell = tuple[int, int]
Source = tuple[int, int, int, int, int]
Blocks = dict[Edge, dict[Cell, Q]]
StarVariable = tuple[int, int, int]
LinearForm = dict[StarVariable, Q]


def canonical(source: Source) -> tuple[Edge, Cell, Q]:
    u, v, colour_u, colour_v, weight = source
    if u < v:
        return (u, v), (colour_u, colour_v), Q(weight)
    if v < u:
        return (v, u), (colour_v, colour_u), Q(weight)
    raise ValueError("loop source")


def aggregate(sources: tuple[Source, ...]) -> Blocks:
    blocks: Blocks = {}
    for source in sources:
        edge, cell, weight = canonical(source)
        block = blocks.setdefault(edge, {})
        total = block.get(cell, Q(0)) + weight
        if total:
            block[cell] = total
        else:
            block.pop(cell, None)
        if not block:
            blocks.pop(edge, None)
    return blocks


@lru_cache(maxsize=None)
def matchings(vertices: tuple[int, ...]) -> tuple[tuple[Edge, ...], ...]:
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    answer: list[tuple[Edge, ...]] = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def add(tensor: dict, key, value: Q) -> None:
    total = tensor.get(key, Q(0)) + value
    if total:
        tensor[key] = total
    else:
        tensor.pop(key, None)


def matching_tensor(vertices: tuple[int, ...], blocks: Blocks) -> Tensor:
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


def insertion_columns(u_sites: tuple[int, ...], blocks: Blocks) -> list[Vector]:
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


def basis(vectors: list[Vector]) -> dict[Word, Vector]:
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


def tensor_sum(*terms: tuple[Q, Tensor]) -> Tensor:
    answer: Tensor = {}
    for scalar, tensor in terms:
        for word, coefficient in tensor.items():
            add(answer, word, scalar * coefficient)
    return answer


DELTA: Tensor = {(colour,) * 8: Q(1) for colour in COLOURS}


def flatten(tensor: Tensor, c_sites: tuple[int, ...], u_sites: tuple[int, ...]):
    rows: dict[Word, Vector] = {}
    for word, coefficient in tensor.items():
        c_word = tuple(word[site] for site in c_sites)
        u_word = tuple(word[site] for site in u_sites)
        add(rows.setdefault(c_word, {}), u_word, coefficient)
    return rows


def cut_record(z: int, blocks: Blocks, full_tensor: Tensor):
    u_sites = tuple(site for site in SIX if site != z)
    c_sites = (z, 6, 7)
    columns = insertion_columns(u_sites, blocks)
    span = basis(columns)
    residual = tensor_sum((Q(1), full_tensor), (Q(-1), DELTA))
    complete = all(member(row, span) for row in flatten(residual, c_sites, u_sites).values())
    constants = [{(colour,) * 5: Q(1)} for colour in COLOURS]
    flags = tuple(member(constant, span) for constant in constants)
    defect = len(basis(columns + constants)) - len(span)
    return {
        "complete": complete,
        "flags": flags,
        "defect": defect,
        "columns": columns,
        "u_sites": u_sites,
    }


def dot(functional: Vector, vector: Vector) -> Q:
    return sum(
        (coefficient * vector.get(word, Q(0)) for word, coefficient in functional.items()),
        Q(0),
    )


def fixed_nonstar_blocks(center: int) -> Blocks:
    fixed = tuple(
        source for source in REPAIRED if center not in source[:2]
    )
    return aggregate(fixed)


def star_coefficient_form(word: Word, center: int) -> LinearForm:
    """Coefficient of a full word as a form in all 63 final star cells.

    A key (j,a,b) means the coefficient of colour a at the noncentral
    endpoint j and colour b at the central endpoint.
    """
    fixed = fixed_nonstar_blocks(center)
    form: defaultdict[StarVariable, Q] = defaultdict(Q)
    for matching in matchings(SITES):
        star_edges = [edge for edge in matching if center in edge]
        assert len(star_edges) == 1
        star_edge = star_edges[0]
        other_site = star_edge[0] if star_edge[1] == center else star_edge[1]
        coefficient = Q(1)
        possible = True
        for edge in matching:
            if edge == star_edge:
                continue
            cell = (word[edge[0]], word[edge[1]])
            value = fixed.get(edge, {}).get(cell, Q(0))
            if not value:
                possible = False
                break
            coefficient *= value
        if possible:
            form[(other_site, word[other_site], word[center])] += coefficient
    return {variable: value for variable, value in form.items() if value}


def audit_fourth_cut_obstruction() -> None:
    internal = aggregate(REPAIRED)

    # On every inactive five-set, all-zero coordinate evaluation kills the
    # full insertion space.  The insertion spaces are star-independent.
    for z in (0, 1, 5):
        u_sites = tuple(site for site in SIX if site != z)
        beta_zero = {(0,) * 5: Q(1)}
        columns = insertion_columns(u_sites, internal)
        assert columns
        assert all(dot(beta_zero, column) == 0 for column in columns)

    # No arbitrary site-6 or site-7 star has an all-zero completion through
    # the fixed non-star blocks.
    for center in (6, 7):
        assert star_coefficient_form((0,) * 8, center) == {}

    # These target defects remain nonzero because star blocks never occur in
    # an internal U_z cofactor.
    baseline = aggregate(REPAIRED)
    full = matching_tensor(SITES, baseline)
    expected = {0: 3, 1: 3, 5: 1}
    for z, dimension in expected.items():
        assert cut_record(z, baseline, full)["defect"] == dimension


def audit_cumulative_repair_invariants() -> None:
    # Arbitrary site-7 star.  x is cell 22 on 27 and y is cell 12 on 67.
    x7 = (2, 2, 2)
    y7 = (6, 1, 2)
    assert star_coefficient_form((2,) * 8, 7) == {x7: Q(1)}
    assert star_coefficient_form(W0, 7) == {x7: Q(1), y7: Q(1)}
    assert star_coefficient_form(W1, 7) == {y7: Q(1)}

    # The all-two coordinate functional lies in K_{U_3}; a complete cut 3
    # therefore forces the all-two coefficient to be one.
    internal = aggregate(REPAIRED)
    u3 = (0, 1, 2, 4, 5)
    beta7 = {(2,) * 5: Q(1)}
    assert all(dot(beta7, column) == 0 for column in insertion_columns(u3, internal))

    # Arbitrary site-6 star.  The relevant star cells are p on 36, r on 46,
    # and y on 67.
    p6 = (3, 1, 1)
    r6 = (4, 0, 1)
    y6 = (7, 2, 1)
    assert star_coefficient_form((1,) * 8, 6) == {p6: Q(1)}
    assert star_coefficient_form(V6, 6) == {r6: Q(1)}
    assert star_coefficient_form(W0, 6) == {
        p6: Q(1),
        r6: Q(1),
        y6: Q(1),
    }
    assert star_coefficient_form(W1, 6) == {y6: Q(1)}

    # beta6 evaluates at U_2 words 11111 and 12201.  It kills every
    # insertion column and has target value e_1.
    u2 = (0, 1, 3, 4, 5)
    beta6 = {
        (1, 1, 1, 1, 1): Q(1),
        (1, 2, 2, 0, 1): Q(1),
    }
    assert all(dot(beta6, column) == 0 for column in insertion_columns(u2, internal))
    assert beta6[(1,) * 5] == 1
    assert beta6.get((0,) * 5, Q(0)) == 0
    assert beta6.get((2,) * 5, Q(0)) == 0


def audit_literal_three_word_undo() -> None:
    # Adding +E_12 on 67 cancels the repaired -E_12 aggregate cell.  The 23
    # source remains internally visible but is inert in the full tensor.
    sources = REPAIRED + ((6, 7, 1, 2, 1),)
    blocks = aggregate(sources)
    full = matching_tensor(SITES, blocks)
    expected = {
        W0: Q(1),
        (1,) * 8: Q(1),
        (2,) * 8: Q(1),
    }
    assert full == expected
    assert all(full.get(word, Q(0)) == 0 for word in (W1, W2, W3))
    expected_flags = {
        2: (True, False, True),
        3: (True, True, False),
        4: (True, False, False),
    }
    for z in (2, 3, 4):
        record = cut_record(z, blocks, full)
        assert record["complete"]
        assert record["flags"] == expected_flags[z]
        assert record["defect"] == expected_flags[z].count(False)


def main() -> None:
    assert len(matchings(SITES)) == 105
    audit_fourth_cut_obstruction()
    audit_cumulative_repair_invariants()
    audit_literal_three_word_undo()
    print("three-cut boundary-star strengthening obstruction: PASS")
    print("no site-6/site-7 star completion can activate cuts 0,1,5: PASS")
    print("site-7 and site-6 cumulative mixed-word invariants: PASS")
    print("literal three-debt-word undo preserves active cuts 2,3,4: PASS")


if __name__ == "__main__":
    main()
