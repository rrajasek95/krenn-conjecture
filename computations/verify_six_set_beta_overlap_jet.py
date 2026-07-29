#!/usr/bin/env python3
"""Exact audits for the six-set beta-overlap and mixed-jet identities.

All computations are over F_P.  A nonzero modular minor also certifies the
corresponding characteristic-zero rank statement for the same integer data.
"""

from __future__ import annotations

from itertools import combinations, permutations, product
from random import Random

import verify_six_set_one_crossing_hessian_pullback as base


P = base.P
Q = base.Q


def identity_matrix():
    return tuple(
        tuple(int(left == right) for right in range(Q))
        for left in range(Q)
    )


def beta_x_words():
    beta = {(0, 0, 0, 0, 0): 2}
    beta.update({
        word: -1
        for word in product((0, 1), repeat=5)
        if sum(word) == 2
    })
    return beta


def lambda_words():
    functional = {(0, 0, 0, 0, 0, 0): 3}
    functional.update({
        word: -1
        for word in product((0, 1), repeat=6)
        if sum(word) == 2
    })
    return functional


def audit_functional_overlap_and_cofactors():
    S = tuple(range(6))
    identity = identity_matrix()
    internal_S = {edge: identity for edge in combinations(S, 2)}
    beta = beta_x_words()
    Lambda = lambda_words()

    # Sum_x e_0^*(x) tensor beta_x = 4 Lambda_S.
    summed = {}
    for x in S:
        U = tuple(vertex for vertex in S if vertex != x)
        for word_U, value in beta.items():
            word = [0] * 6
            word[x] = 0
            for vertex, color in zip(U, word_U, strict=True):
                word[vertex] = color
            key = tuple(word)
            summed[key] = summed.get(key, 0) + value
    all_words = product(range(Q), repeat=6)
    for word in all_words:
        assert summed.get(word, 0) == 4 * Lambda.get(word, 0)

    # Lambda kills the zero-crossing principal tensor H_S.
    lambda_hs = 0
    for word, coefficient in Lambda.items():
        colors = dict(zip(S, word, strict=True))
        lambda_hs += coefficient * base.matching_value(
            internal_S, S, colors
        )
    assert lambda_hs == 0

    # Each beta_x kills every individual V_u tensor H_(U_x-u) insertion.
    for x in S:
        U = tuple(vertex for vertex in S if vertex != x)
        for u in U:
            for u_color in range(Q):
                value = 0
                for word, coefficient in beta.items():
                    colors_U = dict(zip(U, word, strict=True))
                    if colors_U[u] != u_color:
                        continue
                    remainder = tuple(v for v in U if v != u)
                    colors_remainder = {
                        v: colors_U[v] for v in remainder
                    }
                    value += coefficient * base.matching_value(
                        internal_S, remainder, colors_remainder
                    )
                assert value == 0

    # The first surviving Lambda-curried cofactor is the two-site form
    # 3(e_0^* tensor e_0^* - e_1^* tensor e_1^*).
    for a, b in combinations(S, 2):
        remainder = tuple(v for v in S if v not in (a, b))
        for color_a, color_b in product(range(Q), repeat=2):
            value = 0
            for word, coefficient in Lambda.items():
                colors_S = dict(zip(S, word, strict=True))
                if colors_S[a] != color_a or colors_S[b] != color_b:
                    continue
                colors_remainder = {
                    v: colors_S[v] for v in remainder
                }
                value += coefficient * base.matching_value(
                    internal_S, remainder, colors_remainder
                )
            expected = 3 * (
                int(color_a == 0 and color_b == 0)
                - int(color_a == 1 and color_b == 1)
            )
            assert value == expected


def contracted_sector(edges, S, R, functional, crossing_number):
    B = S + R
    R_set = set(R)
    matchings = tuple(base.perfect_matchings(B))
    selected = tuple(
        matching
        for matching in matchings
        if sum(
            (left in R_set) != (right in R_set)
            for left, right in matching
        ) == crossing_number
    )
    answer = {}
    for word_R in product(range(Q), repeat=len(R)):
        total = 0
        colors_R = dict(zip(R, word_R, strict=True))
        for word_S, functional_value in functional.items():
            colors = colors_R | dict(zip(S, word_S, strict=True))
            matching_sum = 0
            for matching in selected:
                term = 1
                for left, right in matching:
                    term = (
                        term
                        * base.edge_entry(
                            edges,
                            left,
                            right,
                            colors[left],
                            colors[right],
                        )
                    ) % P
                matching_sum = (matching_sum + term) % P
            total += functional_value * matching_sum
        answer[word_R] = total % P
    return answer


def audit_two_crossing_hessian_identity_and_nonvanishing():
    rng = Random(1618033)
    S = tuple(range(6))
    R = tuple(range(6, 10))
    identity = identity_matrix()
    internal_S = {edge: identity for edge in combinations(S, 2)}
    internal_R = {
        edge: base.random_matrix(rng) for edge in combinations(R, 2)
    }
    cross = {
        (s, r): base.random_matrix(rng)
        for s in S
        for r in R
    }
    edges = internal_S | internal_R | cross
    Lambda = lambda_words()

    direct_two = contracted_sector(edges, S, R, Lambda, 2)
    direct_four = contracted_sector(edges, S, R, Lambda, 4)

    # Construct the quadratic response X on R.  Endpoint orientation is
    # handled by edge_entry, so this works with S<R labels as chosen here.
    X = {}
    for p, q in combinations(R, 2):
        block = [[0] * Q for _ in range(Q)]
        for a, b in combinations(S, 2):
            for color_p, color_q in product(range(Q), repeat=2):
                for source_color, sign in ((0, 1), (1, -1)):
                    block[color_p][color_q] += sign * (
                        base.edge_entry(
                            edges, p, a, color_p, source_color
                        )
                        * base.edge_entry(
                            edges, q, b, color_q, source_color
                        )
                        + base.edge_entry(
                            edges, p, b, color_p, source_color
                        )
                        * base.edge_entry(
                            edges, q, a, color_q, source_color
                        )
                    )
        X[p, q] = tuple(
            tuple(entry % P for entry in row) for row in block
        )

    hessian_response = {}
    for word_R in product(range(Q), repeat=len(R)):
        colors_R = dict(zip(R, word_R, strict=True))
        value = 0
        for p, q in combinations(R, 2):
            remainder = tuple(v for v in R if v not in (p, q))
            remainder_colors = {v: colors_R[v] for v in remainder}
            value += (
                X[p, q][colors_R[p]][colors_R[q]]
                * base.matching_value(
                    internal_R, remainder, remainder_colors
                )
            )
        hessian_response[word_R] = 3 * value % P

    assert direct_two == hessian_response

    # Boundary annihilation does not kill either surviving sector.
    assert any(direct_two.values())
    assert any(direct_four.values())

    # Lowest mixed pair equation for two vertices x,v in S.  With identity
    # internal S-blocks, both defects either pair directly or leak to two
    # distinct R-sites through their (1,0) cross cells.
    B = S + R
    for x, v in combinations(S, 2):
        remainder = tuple(t for t in B if t not in (x, v))
        all_zero_remainder = {t: 0 for t in remainder}
        direct_pair_cofactor = base.matching_value(
            edges, remainder, all_zero_remainder
        )
        leakage = 0
        for p in R:
            for q in R:
                if p == q:
                    continue
                four_holes = tuple(
                    t for t in B if t not in (x, v, p, q)
                )
                leakage += (
                    base.edge_entry(edges, x, p, 1, 0)
                    * base.edge_entry(edges, v, q, 1, 0)
                    * base.matching_value(
                        edges,
                        four_holes,
                        {t: 0 for t in four_holes},
                    )
                )
        mixed_colors = {t: 0 for t in B}
        mixed_colors[x] = mixed_colors[v] = 1
        mixed_coefficient = base.matching_value(edges, B, mixed_colors)
        assert mixed_coefficient % P == (
            direct_pair_cofactor + leakage
        ) % P


def audit_pure_star_pair_probe():
    rng = Random(424242)
    B = tuple(range(8))
    x = 0
    identity = identity_matrix()
    edges = {}
    for edge in combinations(B, 2):
        edges[edge] = (
            identity if x in edge else base.random_matrix(rng)
        )

    constant_colors = {vertex: 0 for vertex in B}
    constant = base.matching_value(edges, B, constant_colors)
    expansion = 0
    mixed_values = []
    for v in B[1:]:
        remainder = tuple(t for t in B if t not in (x, v))
        cofactor = base.matching_value(
            edges, remainder, {t: 0 for t in remainder}
        )
        expansion += cofactor
        mixed = dict(constant_colors)
        mixed[x] = mixed[v] = 1
        mixed_value = base.matching_value(edges, B, mixed)
        assert mixed_value == cofactor
        mixed_values.append(mixed_value)
    assert constant % P == expansion % P
    assert any(value % P for value in mixed_values)


def audit_hessian_cokernel_target():
    rng = Random(271828)
    R = tuple(range(6))
    for _attempt in range(20):
        internal = {
            edge: base.random_matrix(rng)
            for edge in combinations(R, 2)
        }
        if not all(base.determinant3(matrix) for matrix in internal.values()):
            continue
        words = tuple(product(range(Q), repeat=6))
        word_index = {word: index for index, word in enumerate(words)}
        columns = []
        for p, q in combinations(R, 2):
            remainder = tuple(v for v in R if v not in (p, q))
            for color_p, color_q in product(range(Q), repeat=2):
                column = {}
                for word_remainder in product(range(Q), repeat=4):
                    colors = dict(
                        zip(remainder, word_remainder, strict=True)
                    )
                    value = base.matching_value(
                        internal, remainder, colors
                    )
                    if not value:
                        continue
                    word = [0] * 6
                    word[p], word[q] = color_p, color_q
                    for vertex in remainder:
                        word[vertex] = colors[vertex]
                    column[word_index[tuple(word)]] = value
                columns.append(column)
        if base.sparse_rank(columns) == 130:
            break
    else:
        raise AssertionError("no gauge-rigid specialization found")

    for color in range(Q):
        target = {word_index[(color,) * 6]: 1}
        assert base.sparse_rank(columns + [target]) == 131


def audit_six_crossing_nonvanishing():
    # With identity cross blocks and |R|=6, the all-cross sector has value
    # 3*6! at 0^R and -6! at every R-word of weight two in color 1.
    S = tuple(range(6))
    R = tuple(range(6, 12))
    identity = identity_matrix()
    cross = {
        (s, r): identity for s in S for r in R
    }
    Lambda = lambda_words()

    for word_R, expected in (
        ((0,) * 6, 3 * 720),
        ((1, 1, 0, 0, 0, 0), -720),
    ):
        colors_R = dict(zip(R, word_R, strict=True))
        total = 0
        for permutation in permutations(R):
            for word_S, coefficient in Lambda.items():
                colors_S = dict(zip(S, word_S, strict=True))
                term = coefficient
                for s, r in zip(S, permutation, strict=True):
                    term *= base.edge_entry(
                        cross, s, r, colors_S[s], colors_R[r]
                    )
                total += term
        assert total == expected


def main():
    audit_functional_overlap_and_cofactors()
    audit_two_crossing_hessian_identity_and_nonvanishing()
    audit_pure_star_pair_probe()
    audit_hessian_cokernel_target()
    audit_six_crossing_nonvanishing()
    print("six beta functionals average to 4 Lambda and kill zero/one-hole responses PASS")
    print("Lambda(T2) = 3 dH_q(X) coefficientwise PASS")
    print("random exact audit: Lambda(T2) and Lambda(T4) are both nonzero")
    print("weight-two mixed pair/cofactor identities PASS")
    print("pure identity star is killed by the first weight-two mixed coefficients")
    print("dense R=6: constants lie outside the rank-130 Hessian image")
    print("identity cross chart: Lambda(T6) is nonzero")


if __name__ == "__main__":
    main()
