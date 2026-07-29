#!/usr/bin/env python3
"""Exact audit for four-centre-common-power-one-hole-obstruction.md."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


H = sp.Matrix([[0, 1, 2], [1, 0, 3], [2, 3, 0]])
DELTA = sp.diag(2, 3, 5)
LIVE = sp.eye(3)
ZERO = sp.zeros(3)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def scalar_hafnian(weights: dict[tuple[int, int], sp.Expr], vertices: tuple[int, ...]) -> sp.Expr:
    total = 0
    for matching in perfect_matchings(vertices):
        term = 1
        for i, j in matching:
            term *= weights[tuple(sorted((i, j)))]
        total += term
    return sp.expand(total)


def audit_pattern(name: str, centres: list[sp.Matrix], direct_b: sp.Matrix) -> None:
    # Sites 0,1,2 are live, 3,...,6 are centres, and 7 is the literal
    # zero boundary.  Its scalar star entries stay algebraically free.
    matrices = [LIVE, LIVE, LIVE, *centres, ZERO]
    beta = [1] * 7 + [-1]
    assert len(matrices) == 8
    direct_a_pq = direct_b * DELTA
    assert direct_b == direct_a_pq * DELTA.inv()
    assert direct_b == direct_b.T

    q_blocks: dict[tuple[int, int], sp.Matrix] = {}
    zero_star_symbols = {}
    for i, j in combinations(range(8), 2):
        left = matrices[i] * H * matrices[j].T
        if i == 7 or j == 7:
            assert beta[i] + beta[j] == 0
            block = sp.Matrix(3, 3, lambda a, b: sp.symbols(f"z_{name}_{i}_{j}_{a}_{b}"))
            assert left == sp.zeros(3)
        else:
            assert beta[i] + beta[j] == 2
            block = left / 2
            assert left == (beta[i] + beta[j]) * block
        q_blocks[i, j] = block

    for colour in range(3):
        weights = {}
        for i, j in combinations(range(8), 2):
            weights[i, j] = q_blocks[i, j][colour, colour]
            if i != 7 and j != 7:
                assert weights[i, j] == 0
            else:
                zero_star_symbols[i, j] = weights[i, j]

        full = scalar_hafnian(weights, tuple(range(8)))
        assert full == 0

        # The c-coordinate of the local marked vector P_i e_c.
        marked_scalar = [matrices[i][colour, colour] for i in range(8)]
        assert marked_scalar[7] == 0
        diagonal_response = 0
        audited_pairs = 0
        for i, j in combinations(range(8), 2):
            if not marked_scalar[i] or not marked_scalar[j]:
                continue
            remaining = tuple(site for site in range(8) if site not in (i, j))
            cofactor = scalar_hafnian(weights, remaining)
            assert cofactor == 0
            diagonal_response += 2 * marked_scalar[i] * marked_scalar[j] * cofactor
            audited_pairs += 1
        assert audited_pairs > 0
        assert sp.expand(diagonal_response) == 0

        d_c = (2, 3, 5)[colour]
        b_cc = direct_b[colour, colour]
        residual = sp.expand(diagonal_response + b_cc * full - sp.Rational(1, d_c))
        assert residual == -sp.Rational(1, d_c)


def main() -> None:
    audit_pattern(
        "rank1",
        [sp.diag(1, 1, 0), sp.diag(1, 1, 0),
         sp.diag(1, 0, 1), sp.diag(1, 0, 1)],
        sp.diag(1, 0, 0),
    )
    audit_pattern(
        "rank2",
        [sp.diag(1, 1, 0), sp.diag(1, 1, 0),
         sp.diag(0, 0, 1), sp.diag(0, 0, 1)],
        sp.Matrix([[0, sp.Rational(1, 2), 0],
                   [sp.Rational(1, 2), 0, 0],
                   [0, 0, 0]]),
    )
    assert len(tuple(perfect_matchings(tuple(range(8))))) == 105
    print("Four-centre common-power one-hole obstruction: PASS")


if __name__ == "__main__":
    main()
