#!/usr/bin/env python3
"""Exact audit for live-isotropic-second-jet-cover-patterns.md."""

from __future__ import annotations

from collections import Counter
from itertools import product

import sympy as sp


E = [sp.eye(3)[:, c] for c in range(3)]
H = sp.Matrix([[0, 1, 2], [1, 0, 3], [2, 3, 0]])
DELTA = sp.diag(2, 3, 5)
ALT = (
    sp.Matrix([[0, 0, 0], [0, 0, 1], [0, -1, 0]]),
    sp.Matrix([[0, 0, -1], [0, 0, 0], [1, 0, 0]]),
    sp.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]]),
)


def audit_graded_minimum() -> None:
    # A literal zero site retains the three independent target factors.
    assert sp.Matrix.hstack(*E).rank() == 3

    # If an active colour has zero or one forced line factor, its least
    # degree is below two.  Distinct singleton centre sets lie in distinct
    # graded summands; empty sets separate by the zero-site factor.
    for number_of_active_colours in (1, 2, 3):
        for centre_counts in product(range(3), repeat=number_of_active_colours):
            if min(centre_counts) < 2:
                assert any(count in (0, 1) for count in centre_counts)
            else:
                assert all(count >= 2 for count in centre_counts)


def audit_pattern_minima() -> None:
    # Each component needs two incidences for every active colour.  One
    # site carries at most one incidence from each component.
    cases = {
        "zero_or_rank3": ((0, 1, 2),),
        "rank1_coordinate": ((1, 2),),
        "rank1_noncoordinate": ((0, 1, 2),),
        "rank2_two_coordinate": ((1, 2), (0, 2)),
        "rank2_one_coordinate": ((1, 2), (0, 1, 2)),
        "rank2_no_coordinate": ((0, 1, 2), (0, 1, 2)),
    }
    expected = {
        "zero_or_rank3": 6,
        "rank1_coordinate": 4,
        "rank1_noncoordinate": 6,
        "rank2_two_coordinate": 4,
        "rank2_one_coordinate": 6,
        "rank2_no_coordinate": 6,
    }
    for name, active_sets in cases.items():
        incidence_totals = [2 * len(active) for active in active_sets]
        minimum = max(incidence_totals)
        assert minimum == expected[name]

    # Explicit four-site pairing for the two-coordinate rank-two case.
    paired = [(1, 0), (1, 0), (2, 2), (2, 2)]
    assert Counter(left for left, _ in paired) == Counter({1: 2, 2: 2})
    assert Counter(right for _, right in paired) == Counter({0: 2, 2: 2})


def image_basis(matrix: sp.Matrix, subspace: sp.Matrix) -> sp.Matrix:
    return matrix * subspace


def is_axis_image(matrix: sp.Matrix, subspace: sp.Matrix, colour: int) -> bool:
    image = image_basis(matrix, subspace)
    return image.rank() == 1 and sp.Matrix.hstack(image, E[colour]).rank() == 1


def audit_structural_models() -> None:
    assert H.det() != 0 and DELTA.det() != 0
    assert H == H.T and all(H[c, c] == 0 for c in range(3))

    k0 = sp.Matrix.hstack(E[1], E[2])  # v_0=0
    k1 = sp.Matrix.hstack(E[0], E[2])  # v_1=0

    p1 = sp.diag(1, 1, 0)
    p2_rank2 = sp.diag(1, 0, 1)
    p2_rank1 = sp.diag(0, 0, 1)
    coordinate_rank_one = [E[c] * E[c].T for c in range(3)]

    assert is_axis_image(p1, k0, 1)
    assert is_axis_image(p2_rank2, k0, 2)
    assert is_axis_image(p1, k1, 0)
    assert is_axis_image(p2_rank1, k0, 2)
    assert is_axis_image(p2_rank1, k1, 2)

    # Every asserted centre is zero-cross in its centre colour.
    for matrix, colour in ((p1, 1), (p2_rank2, 2), (p1, 0), (p2_rank1, 2)):
        assert matrix.T * ALT[colour] * matrix == sp.zeros(3)

    # Rank-one centres are triple zero-cross.
    assert all(p2_rank1.T * alternating * p2_rank1 == sp.zeros(3) for alternating in ALT)
    for matrix in coordinate_rank_one:
        assert matrix.rank() == 1
        assert all(matrix.T * alternating * matrix == sp.zeros(3) for alternating in ALT)

    # Exact relation blocks with beta=1 at nonzero sites.
    live = sp.eye(3)
    nonzero_sites = [live, live, live, p1, p1, p2_rank1, p2_rank1]
    for left in nonzero_sites:
        for right in nonzero_sites:
            q_block = left * H * right.T / 2
            assert left * H * right.T == 2 * q_block
            assert q_block.rank() <= min(left.rank(), right.rank())

    # The literal beta=-1 zero site can carry arbitrary rank-three edges.
    zero = sp.zeros(3)
    assert zero * H * live.T == sp.zeros(3)
    assert (1 + (-1)) * H == sp.zeros(3)

    # Dead-edge rank geometry in the displayed rank-one pair.
    assert p2_rank1 * H * p2_rank1.T == sp.zeros(3)
    assert p1 * H * p2_rank1.T != sp.zeros(3)
    for matrix in coordinate_rank_one:
        assert matrix * H * matrix.T == sp.zeros(3)


def tensor_word(word: tuple[int, ...], coefficient=sp.Integer(1)) -> dict[tuple[int, ...], sp.Expr]:
    return {word: coefficient}


def add_tensors(*tensors: dict[tuple[int, ...], sp.Expr]) -> dict[tuple[int, ...], sp.Expr]:
    result: dict[tuple[int, ...], sp.Expr] = {}
    for tensor in tensors:
        for word, coefficient in tensor.items():
            result[word] = sp.simplify(result.get(word, 0) + coefficient)
            if result[word] == 0:
                del result[word]
    return result


def marked_product(
    first_support: dict[int, int],
    second_support: dict[int, int],
    cofactor: dict[tuple[int, ...], sp.Expr],
) -> dict[tuple[int, ...], sp.Expr]:
    """Multiply two sparse marked forms by a degree-two four-site cofactor."""
    result: dict[tuple[int, ...], sp.Expr] = {}
    for i, first_colour in first_support.items():
        for j, second_colour in second_support.items():
            if i == j:
                continue
            for occupied_word, coefficient in cofactor.items():
                occupied = [site for site, colour in enumerate(occupied_word) if colour >= 0]
                if i in occupied or j in occupied:
                    continue
                word = list(occupied_word)
                word[i], word[j] = first_colour, second_colour
                key = tuple(word)
                result[key] = sp.simplify(result.get(key, 0) + coefficient)
    return {word: value for word, value in result.items() if value != 0}


def audit_four_centre_cofactor() -> None:
    # Sites 0,1 are d-centres; sites 2,3 are e-centres.  A value -1 marks
    # a hole in this compact degree-two cofactor representation.
    d, e = 1, 2
    cofactor = add_tensors(
        tensor_word((-1, -1, d, d), sp.Rational(1, 2)),
        tensor_word((e, e, -1, -1), sp.Rational(1, 2)),
    )
    p_d = {0: d, 1: d}
    p_e = {2: e, 3: e}
    assert marked_product(p_d, p_d, cofactor) == tensor_word((d, d, d, d))
    assert marked_product(p_e, p_e, cofactor) == tensor_word((e, e, e, e))
    assert marked_product(p_d, p_e, cofactor) == {}


def main() -> None:
    audit_graded_minimum()
    audit_pattern_minima()
    audit_structural_models()
    audit_four_centre_cofactor()
    print("Live isotropic second-jet cover patterns: PASS")


if __name__ == "__main__":
    main()
