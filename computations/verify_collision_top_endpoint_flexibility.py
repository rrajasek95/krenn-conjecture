#!/usr/bin/env python3
"""Exact countermodels to using only the top three collision equations.

For n=6,8,10 this constructs a rational dense scalar W with prescribed
hafnian and nonzero deleted-pair cofactors, a nonzero one-binary tangent K,
and the unique pairwise q0 correction.  It enumerates every coefficient
with n, n-1, or n-2 z labels and checks the reversed half-shift target.
The constructed q0 deliberately does not satisfy the bottom binary GHZ
equation; this proves that top-end flexibility must be coupled to it.
"""

from __future__ import annotations

import itertools
from fractions import Fraction
from math import prod as product


X, Y, Z = range(3)


def odd_double_factorial(value):
    answer = 1
    for factor in range(value, 0, -2):
        answer *= factor
    return answer


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, partner in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, partner),) + tail


def coefficient(source, vertices, coloring):
    total = Fraction(0)
    for matching in perfect_matchings(vertices):
        term = Fraction(1)
        for u, v in matching:
            term *= source.get((u, v, coloring[u], coloring[v]), 0)
        total += term
    return total


def scalar_hafnian(weights, vertices):
    total = Fraction(0)
    for matching in perfect_matchings(vertices):
        term = Fraction(1)
        for edge in matching:
            term *= weights[edge]
        total += term
    return total


def matrix_rank(matrix):
    work = [list(map(Fraction, row)) for row in matrix]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(pivot_row + 1, len(work)):
            if not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                left - scale * right
                for left, right in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def construct(n):
    vertices = tuple(range(n))
    edges = tuple(itertools.combinations(vertices, 2))
    target_top = Fraction(1, 2 ** (n - 1))
    target_pair = Fraction(1, 2 ** (n - 3))

    # Complete scalar graph with one adjusted edge.  Its hafnian is affine
    # in w_01, with coefficients (n-3)!! and (n-2)(n-3)!!.
    cofactor_01 = odd_double_factorial(n - 3)
    special = target_top / cofactor_01 - (n - 2)
    weights = {edge: Fraction(1) for edge in edges}
    weights[(0, 1)] = special
    assert scalar_hafnian(weights, vertices) == target_top

    cofactors = {}
    for first, second in edges:
        remaining = tuple(v for v in vertices if v not in (first, second))
        cofactors[(first, second)] = scalar_hafnian(weights, remaining)
        assert cofactors[(first, second)] != 0

    source = {}
    for edge, value in weights.items():
        source[edge + (Z, Z)] = value

    # A nonzero tangent concentrated on the binary site zero.  The two
    # coefficients cancel in the sole top-tangent scalar equation there.
    source[(0, 1, X, Z)] = cofactors[(0, 2)]
    source[(0, 2, X, Z)] = -cofactors[(0, 1)]
    assert (
        source[(0, 1, X, Z)] * cofactors[(0, 1)]
        + source[(0, 2, X, Z)] * cofactors[(0, 2)]
        == 0
    )

    # K^2=0 because both tangent cells meet site zero.  Every direct q0
    # cell can therefore be solved independently through its nonzero W
    # cofactor.
    for edge in edges:
        source[edge + (X, X)] = target_pair / cofactors[edge]

    return source, weights, cofactors


def verify(n):
    vertices = tuple(range(n))
    source, weights, cofactors = construct(n)
    audits = 0
    for z_count in (n, n - 1, n - 2):
        binary_count = n - z_count
        for binary_sites in itertools.combinations(vertices, binary_count):
            for binary_colors in itertools.product((X, Y), repeat=binary_count):
                coloring = [Z] * n
                for site, color in zip(binary_sites, binary_colors):
                    coloring[site] = color
                coloring = tuple(coloring)
                value = coefficient(source, vertices, coloring)
                target = (
                    Fraction(1, 2 ** (n - 1))
                    if z_count == n
                    else Fraction(1, 2 ** (n - 3))
                    if z_count == n - 2 and all(color == X for color in binary_colors)
                    else Fraction(0)
                )
                assert value == target, (n, coloring, value, target)
                audits += 1

    # This top-end solution is not a bottom-end solution: q0 has no y cell,
    # so its all-y coefficient is zero rather than one.
    all_y = (Y,) * n
    assert coefficient(source, vertices, all_y) == 0
    print(
        f"n={n}: top coefficients={audits}, all cofactors nonzero, "
        f"special_w01={weights[(0, 1)]}"
    )


def verify_hamilton_coupling_support(n):
    """Audit the least-cell-bottom / one-matching-top obstruction."""
    vertices = tuple(range(n))
    shores = {vertex: vertex % 2 for vertex in vertices}
    px = tuple((i, i + 1) for i in range(0, n, 2))
    py = tuple((i, i + 1) for i in range(1, n - 1, 2)) + ((0, n - 1),)
    cycle = set(px) | set(py)

    # A nonunit rational weighted representative of the exact hypotheses.
    # The occurrence graph has exactly its two alternating matchings, and
    # the last weight in each factor normalizes the products to 2 and 1.
    x_weights = [Fraction(index + 2) for index in range(n // 2)]
    y_weights = [Fraction(index + 3) for index in range(n // 2)]
    x_weights[-1] *= Fraction(2, 1) / product(x_weights)
    y_weights[-1] *= Fraction(1, 1) / product(y_weights)
    assert product(x_weights) == 2 and product(y_weights) == 1

    if n == 6:
        # Two bottom-tangent cells for a same-shore binary pair would need
        # four distinct vertices in a shore of size three.
        for shore in (0, 1):
            members = tuple(v for v in vertices if shores[v] == shore)
            for first, second in itertools.combinations(members, 2):
                for first_z in members:
                    for second_z in members:
                        if first_z == first or second_z == second:
                            continue
                        assert len({first, second, first_z, second_z}) < 4

    matchings = tuple(perfect_matchings(vertices))
    supported_cycle_matchings = tuple(
        matching for matching in matchings if all(edge in cycle for edge in matching)
    )
    assert {
        frozenset(matching) for matching in supported_cycle_matchings
    } == {frozenset(px), frozenset(py)}
    for matching in matchings:
        # Arbitrary nonzero one-factor weights can be used; this exact
        # representative has the required product 2^(1-n).
        w_weights = [Fraction(index + 5) for index in range(n // 2)]
        w_weights[-1] *= Fraction(1, 2 ** (n - 1)) / product(w_weights)
        assert product(w_weights) == Fraction(1, 2 ** (n - 1))
        mate = {}
        for first, second in matching:
            mate[first] = second
            mate[second] = first
        matching_edges = {tuple(sorted(edge)) for edge in matching}

        bad_pairs = []
        for first, second in itertools.combinations(vertices, 2):
            if (first, second) in matching_edges:
                continue
            # For W supported on this matching, the unique possible KxK
            # completion uses z endpoints mate(second), mate(first).
            allowed = (
                shores[mate[second]] == shores[first]
                and shores[mate[first]] == shores[second]
            )
            if not allowed:
                bad_pairs.append((first, second))
        assert bad_pairs, matching
    print(
        f"n={n}: weighted Hamilton hypotheses checked; every one-factor W "
        f"has a forbidden nonmatching pair ({len(matchings)} matchings audited)"
    )


def verify_dense_top_star_transport_failure():
    """No nonzero W-star move lifts through the rational top two-jet."""
    n = 6
    vertices = tuple(range(n))
    source, _, _ = construct(n)
    for star in vertices:
        columns = []
        decorations = (
            (0, ((Z, Z),)),
            (1, ((Z, X), (Z, Y), (X, Z), (Y, Z))),
            (2, ((X, X), (X, Y), (Y, X), (Y, Y))),
        )
        for grade, cells in decorations:
            for neighbor in vertices:
                if neighbor == star:
                    continue
                first, second = sorted((star, neighbor))
                for star_color, neighbor_color in cells:
                    endpoint_colors = (
                        (star_color, neighbor_color)
                        if star == first
                        else (neighbor_color, star_color)
                    )
                    columns.append((grade, neighbor, *endpoint_colors))

        rows = []
        for binary_count in (0, 1, 2):
            for binary_sites in itertools.combinations(vertices, binary_count):
                for binary_colors in itertools.product((X, Y), repeat=binary_count):
                    coloring = [Z] * n
                    for site, color in zip(binary_sites, binary_colors):
                        coloring[site] = color
                    row = []
                    for _, neighbor, first_color, second_color in columns:
                        first, second = sorted((star, neighbor))
                        if (coloring[first], coloring[second]) != (
                            first_color,
                            second_color,
                        ):
                            row.append(Fraction(0))
                            continue
                        remaining = tuple(
                            vertex
                            for vertex in vertices
                            if vertex not in (star, neighbor)
                        )
                        row.append(coefficient(source, remaining, coloring))
                    rows.append(row)

        d0_columns = n - 1
        full_rank = matrix_rank(rows)
        correction_rank = matrix_rank(
            [row[d0_columns:] for row in rows]
        )
        assert (len(rows), len(columns), full_rank, correction_rank) == (
            73,
            45,
            37,
            32,
        )
        # Adding the five D0 columns raises rank by five, so their classes
        # are independent modulo all D1,D2 corrections.  Hence the kernel
        # of the complete lift matrix projects trivially to D0.
        assert full_rank - correction_rank == d0_columns
    print("n=6: every dense-top star has ranks full/corrections=37/32")


def main():
    for n in (6, 8, 10):
        verify(n)
    for n in (6, 8, 10, 12):
        verify_hamilton_coupling_support(n)
    verify_dense_top_star_transport_failure()
    print("verified exact top-end flexibility countermodels")
    print("verified coupled Hamilton / one-factor-W support obstruction")
    print("verified dense top-star transport failure")


if __name__ == "__main__":
    main()
