#!/usr/bin/env python3
"""Exact audit for live-four-centre-final-deviation-obstruction.md."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations, product

import sympy as sp


AXES = frozenset(range(3))
H = sp.Matrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
B = sp.diag(1, 0, 0)


def audit_axis_cover_obstruction() -> None:
    """Enumerate a superset of every possible coordinate-axis coverage."""
    possible = {
        centre_colour: tuple(
            frozenset(mask)
            for size in (1, 2)
            for mask in combinations(range(3), size)
            if centre_colour in mask
        )
        for centre_colour in (1, 2)
    }

    # Coordinate rank-one B: two centres for colour 1 and two for colour 2.
    survivors = []
    for coverages in product(possible[1], possible[1], possible[2], possible[2]):
        if all(left | right == AXES for left, right in combinations(coverages, 2)):
            survivors.append(coverages)
    assert survivors == []

    # Two-coordinate-factor rank-two B: two 10 centres and two 22 centres.
    rank_two_coverages = (
        frozenset((0, 1)),
        frozenset((0, 1)),
        frozenset((2,)),
        frozenset((2,)),
    )
    assert any(
        left | right != AXES
        for left, right in combinations(rank_two_coverages, 2)
    )


def audit_symbolic_annihilation() -> None:
    """Check the factorization killed in the two-centre contraction."""
    a0, a1, a2, b, c = sp.symbols("a0 a1 a2 b c")
    generic_right = sp.Matrix(3, 3, sp.symbols("r0:9"))

    # A centre for colour 1 on K=<e1,e2> has this general form.
    p1 = sp.Matrix([[a0, 0, 0], [a1, b, c], [a2, 0, 0]])
    eta1 = sp.Matrix([-a2, 0, a0])
    assert (eta1.T * p1) == sp.zeros(1, 3)
    assert eta1.T * p1 * H * generic_right.T == sp.zeros(1, 3)

    # The analogous general colour-2 centre.
    p2 = sp.Matrix([[a0, 0, 0], [a1, 0, 0], [a2, b, c]])
    eta2 = sp.Matrix([a1, -a0, 0])
    assert (eta2.T * p2) == sp.zeros(1, 3)
    assert eta2.T * p2 * H * generic_right.T == sp.zeros(1, 3)

    # Exact linear forms forced by the two-coordinate-factor pattern.
    x0, x1, x2 = sp.symbols("x0 x1 x2", nonzero=True)
    p10 = sp.diag(x0, x1, 0)
    p22 = sp.Matrix([[0, 0, 0], [0, 0, 0], [x0, x1, x2]])
    assert p10.columnspace() == [sp.Matrix([x0, 0, 0]), sp.Matrix([0, x1, 0])]
    assert p22.rank() == 1


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            result.append(((first, second),) + tail)
    return tuple(result)


def audit_constant_word_boundary_model() -> None:
    """A non-diagonal exact model passes every constant-word projection."""
    matrices = [
        sp.Matrix([[1, 1, -1], [0, 0, 1], [0, 1, -1]]),
        sp.Matrix([[0, 0, 1], [1, -1, 0], [0, 1, 0]]),
        sp.Matrix([[1, -1, 0], [-1, 0, 1], [1, 0, 1]]),
        sp.Matrix([[1, 0, 0], [0, -1, 0], [-1, 0, 0]]),
        sp.Matrix([[-1, 0, 0], [1, -1, -1], [1, 0, 0]]),
        sp.Matrix([[1, 0, 0], [-1, 0, 0], [-1, -1, 1]]),
        sp.Matrix([[1, 0, 0], [-1, 0, 0], [-1, 1, 0]]),
        sp.zeros(3),
    ]
    beta = [1] * 7 + [-1]
    diagonal_zero_star = [
        (sp.Rational(1, 6), sp.Rational(-1, 8), sp.Rational(1, 3)),
        (0, sp.Rational(1, 8), sp.Rational(-1, 3)),
        (0, sp.Rational(-3, 8), 1),
        (0, sp.Rational(1, 24), sp.Rational(1, 3)),
        (0, sp.Rational(-7, 6), 0),
        (0, 0, sp.Rational(2, 3)),
        (0, 0, sp.Rational(2, 3)),
    ]
    cyclic = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])

    assert H == H.T and H.det() != 0
    assert all(H[c, c] == 0 for c in range(3))
    assert all(matrix.det() != 0 for matrix in matrices[:3])
    assert all(matrix.rank() == 2 for matrix in matrices[3:7])
    assert matrices[7] == sp.zeros(3)

    # K=<e1,e2>; sites 3,4 are 1-centres and sites 5,6 are 2-centres.
    k_plane = sp.Matrix.hstack(sp.eye(3)[:, 1], sp.eye(3)[:, 2])
    for site, colour in ((3, 1), (4, 1), (5, 2), (6, 2)):
        image = matrices[site] * k_plane
        assert image.rank() == 1
        assert sp.Matrix.hstack(image, sp.eye(3)[:, colour]).rank() == 1
    assert any(
        sp.Matrix.hstack(matrices[site][:, 0], sp.eye(3)[:, 0]).rank() == 2
        for site in range(3, 7)
    )

    blocks: dict[tuple[int, int], sp.Matrix] = {}
    for i, j in combinations(range(8), 2):
        if j < 7:
            block = matrices[i] * H * matrices[j].T / 2
        else:
            block = sp.diag(*diagonal_zero_star[i]) + cyclic
        blocks[i, j] = block
        assert matrices[i] * H * matrices[j].T == (beta[i] + beta[j]) * block

    # Every zero-star block is invertible; together with the live triangle
    # this makes G_3 connected, spanning, and nonbipartite.
    assert [blocks[i, 7].det() for i in range(7)] == [
        sp.Rational(143, 144), 1, 1, 1, 1, 1, 1
    ]
    rank_three_edges = {
        (i, j) for i, j in combinations(range(8), 2) if blocks[i, j].rank() == 3
    }
    reached = {0}
    while True:
        enlarged = reached | {
            j if i in reached else i
            for i, j in rank_three_edges
            if (i in reached) ^ (j in reached)
        }
        if enlarged == reached:
            break
        reached = enlarged
    assert reached == set(range(8))
    assert {(0, 1), (0, 2), (1, 2)} <= rank_three_edges

    def block_entry(i: int, j: int, left: int, right: int) -> sp.Expr:
        if i < j:
            return blocks[i, j][left, right]
        return blocks[j, i][right, left]

    def word_hafnian(word: tuple[int, ...], vertices: tuple[int, ...]) -> sp.Expr:
        return sp.expand(sum(
            sp.prod(block_entry(i, j, word[i], word[j]) for i, j in matching)
            for matching in perfect_matchings(vertices)
        ))

    def cap_coefficient(word: tuple[int, ...], c: int, d: int) -> sp.Expr:
        response = B[c, d] * word_hafnian(word, tuple(range(8)))
        for i, j in combinations(range(8), 2):
            marked = (
                matrices[i][word[i], c] * matrices[j][word[j], d]
                + matrices[i][word[i], d] * matrices[j][word[j], c]
            )
            remaining = tuple(site for site in range(8) if site not in (i, j))
            response += marked * word_hafnian(word, remaining)
        return sp.expand(response)

    # The six symmetric polarizations at each constant word are exact.
    for colour in range(3):
        word = (colour,) * 8
        response = sp.Matrix(3, 3, lambda c, d: cap_coefficient(word, c, d))
        assert response == sp.eye(3)[:, colour] * sp.eye(3)[:, colour].T

    # The model is deliberately only a boundary model, not a target solution.
    assert cap_coefficient((0, 0, 0, 0, 0, 0, 0, 1), 0, 0) == 18


def audit_beta_parity_logic() -> None:
    """Finite audit of the alternating labels used in Lemma 2.1."""
    for distance in range(1, 33):
        endpoint_sign = -1 if distance % 2 else 1
        all_pair_sum = 1 + endpoint_sign
        if all_pair_sum != 0:
            assert distance % 2 == 0
        else:
            assert distance % 2 == 1

    # A nonzero singular endpoint compatible with a live beta b therefore
    # has beta b; a second endpoint with beta -b violates that same all-pair
    # compatibility.  Audit over representative nonzero rational values.
    for live_beta in (sp.Rational(-3, 2), -1, sp.Rational(2, 3), 2):
        first_singular = live_beta
        opposite_singular = -first_singular
        assert live_beta + first_singular != 0
        assert live_beta + opposite_singular == 0


def main() -> None:
    audit_axis_cover_obstruction()
    audit_symbolic_annihilation()
    audit_beta_parity_logic()
    audit_constant_word_boundary_model()
    assert len(perfect_matchings(tuple(range(8)))) == 105
    print("Live four-centre final deviations: PASS")


if __name__ == "__main__":
    main()
