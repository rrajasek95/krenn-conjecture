#!/usr/bin/env python3
"""Exact audits for the full-singular-row two-cross obstruction.

This verifies the finite ingredients of
``notes/two-k4-full-singular-row-two-cross-obstruction.md``:

* the K4 factor and directed-triangle combinatorics;
* the three-status demand with zero or one dirty local map;
* the demand/capacity proof that each coordinate row is active in at most
  two exceptional blocks;
* the exact two surviving matching patterns in the kernel-cleaned slice;
* the integer linear normal form of fixed-leg cancellation.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, product


Q = 3
SHORE_EDGES = tuple(combinations(range(4), 2))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


MATCHINGS = tuple(perfect_matchings(range(8)))


def internal_colour(u, v):
    return (1, 2, 3).index(u ^ v)


def compatible_edges(word):
    return tuple(
        (u, v)
        for u, v in SHORE_EDGES
        if word[u] == word[v] == internal_colour(u, v)
    )


def dead_coordinate_lines():
    """Eight triangle-tail lines, as (hole, fixed assignments)."""

    answer = []
    for hole in range(4):
        rest = tuple(vertex for vertex in range(4) if vertex != hole)
        for assignment in product(range(Q), repeat=3):
            word = [None] * 4
            for vertex, colour in zip(rest, assignment):
                word[vertex] = colour
            if all(not compatible_edges(tuple(
                colour if colour is not None else free_colour
                for colour in word
            )) for free_colour in range(Q)):
                answer.append((hole, tuple(zip(rest, assignment))))
    return tuple(answer)


def audit_k4_and_triangle_pairs():
    factors = {}
    for colour in range(Q):
        edges = tuple(
            edge for edge in SHORE_EDGES if internal_colour(*edge) == colour
        )
        assert len(edges) == 2
        assert set(edges[0]).isdisjoint(edges[1])
        assert compatible_edges((colour,) * 4) == edges
        factors[colour] = edges
    assert Counter(edge for edges in factors.values() for edge in edges) == {
        edge: 1 for edge in SHORE_EDGES
    }

    lines = dead_coordinate_lines()
    assert len(lines) == 8
    expected_pairs = {0: (4, 6), 1: (2, 7), 2: (3, 5)}
    for colour in range(Q):
        selected = tuple(
            number
            for number, (hole, assignment) in enumerate(lines)
            if hole != 0 and dict(assignment)[0] == colour
        )
        assert selected == expected_pairs[colour]

        first = dict(lines[selected[0]][1])
        second = dict(lines[selected[1]][1])
        common = set(first) & set(second) - {0}
        assert len(common) == 1
        shared_vertex = next(iter(common))
        assert first[shared_vertex] != second[shared_vertex]


def minimum_statuses_with_at_most_one_dirty(dirty):
    """Enumerate the rank implications for all four zero Per3 cofactors."""

    valid = []
    for mask in range(1 << 4):
        status = lambda column: bool(mask >> column & 1)
        good = True
        for omitted in range(4):
            columns = set(range(4)) - {omitted}
            if dirty is None or dirty not in columns:
                # A clean zero Per3 triple contains two rank-one maps.
                if sum(status(column) for column in columns) < 2:
                    good = False
                    break
            elif not status(dirty):
                # A non-status dirty map has two independent active images;
                # the one-defect lemma makes both clean maps statuses.
                if not all(status(column) for column in columns - {dirty}):
                    good = False
                    break
        if good:
            valid.append(mask)
    assert valid
    return min(mask.bit_count() for mask in valid)


def audit_activity_bound():
    assert minimum_statuses_with_at_most_one_dirty(None) == 3
    for dirty in range(4):
        assert minimum_statuses_with_at_most_one_dirty(dirty) == 3

    # Two triangle contexts selecting the same active exceptional row need
    # six statuses.  An active column carries at most one of the pair; an
    # inactive column carries at most two.
    demand = 6
    assert all(
        active + 2 * (4 - active) < demand for active in (3, 4)
    )


def canonical_edge(u, v):
    return (u, v) if u < v else (v, u)


def audit_kernel_cleaned_matching_slice():
    """After the four row-zero/kernel contractions, exactly two PMs live."""

    cases = 0
    for t in (1, 2, 3):
        colour = internal_colour(0, t)
        r, s = tuple(vertex for vertex in (1, 2, 3) if vertex != t)
        assert internal_colour(r, s) == colour

        for u, v in SHORE_EDGES:
            d = internal_colour(u, v)
            j, k = tuple(vertex for vertex in range(4) if vertex not in (u, v))
            assert internal_colour(j, k) == d

            for alpha, beta in product(range(Q), repeat=2):
                left_word = [None] * 4
                left_word[0] = left_word[t] = colour
                left_word[r], left_word[s] = alpha, beta

                surviving = set()
                for matching in MATCHINGS:
                    valid = True
                    for a, b in matching:
                        if b < 4:
                            if not (
                                left_word[a]
                                == left_word[b]
                                == internal_colour(a, b)
                            ):
                                valid = False
                                break
                        elif a >= 4:
                            x, y = a - 4, b - 4
                            # The chosen contractions leave uv as the only
                            # possible internal right edge: q_d=0 kills jk,
                            # and fixed colour d kills every incident edge.
                            if (x, y) != (u, v):
                                valid = False
                                break
                        elif a == 0:
                            # Rows at u,v vanish identically; contractions p
                            # and q kill the rows at j,k.
                            valid = False
                            break
                    if valid:
                        surviving.add(frozenset(
                            canonical_edge(*edge) for edge in matching
                        ))

                expected = {
                    frozenset((
                        canonical_edge(0, t),
                        canonical_edge(4 + u, 4 + v),
                        canonical_edge(r, 4 + j),
                        canonical_edge(s, 4 + k),
                    )),
                    frozenset((
                        canonical_edge(0, t),
                        canonical_edge(4 + u, 4 + v),
                        canonical_edge(r, 4 + k),
                        canonical_edge(s, 4 + j),
                    )),
                }
                assert surviving == expected
                cases += 1

    assert cases == 3 * 6 * 9
    return cases


def rational_rank(rows):
    matrix = [[Fraction(value) for value in row] for row in rows]
    nrows, ncols = len(matrix), len(matrix[0])
    pivot_row = 0
    for column in range(ncols):
        pivot = next(
            (row for row in range(pivot_row, nrows) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(nrows):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def audit_fixed_leg_normal_form():
    # Normalize nonzero z and y independently to e_0.  Unknowns are the
    # coordinates of x and w.  The kernel of x tensor e_0 + e_0 tensor w
    # is one-dimensional, with x and w both on the fixed lines.
    rows = []
    for first in range(3):
        for second in range(3):
            row = [0] * 6
            if second == 0:
                row[first] += 1
            if first == 0:
                row[3 + second] += 1
            rows.append(row)
    assert rational_rank(rows) == 5
    assert rows[3] == [0, 1, 0, 0, 0, 0]
    assert rows[6] == [0, 0, 1, 0, 0, 0]


def main():
    assert len(MATCHINGS) == 105
    audit_k4_and_triangle_pairs()
    audit_activity_bound()
    cases = audit_kernel_cleaned_matching_slice()
    audit_fixed_leg_normal_form()
    print(
        "PASS: full singular block row excluded by dead-slab activity "
        f"and kernel-cleaned two-cross rank collapse ({cases} slices)"
    )


if __name__ == "__main__":
    main()
