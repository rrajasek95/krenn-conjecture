#!/usr/bin/env python3
"""Exact audits for overlaps of the forced six-set top residues.

The ambient local model has twelve sites.  A set Z of size 6+d carries
identity blocks, P has size 6-d, and the six-sets are S_D=Z-D for all
d-subsets D.  After contracting D at color zero, the pulled six-crossing
responses form the unsigned edge-incidence map of KG(6+d,d).
"""

from __future__ import annotations

from itertools import combinations, permutations, product
from random import Random

import verify_six_set_one_crossing_hessian_pullback as base


P_MOD = base.P
Q = base.Q


def identity_matrix():
    return tuple(
        tuple(int(left == right) for right in range(Q))
        for left in range(Q)
    )


def rho_words(size):
    answer = {(0,) * size: 3}
    answer.update({
        word: -1
        for word in product((0, 1), repeat=size)
        if sum(word) == 2
    })
    return answer


def dense_rank(vectors):
    columns = [
        {index: value % P_MOD for index, value in enumerate(vector) if value}
        for vector in vectors
    ]
    return base.sparse_rank(columns)


def hessian_columns(vertices, edges):
    words = tuple(product(range(Q), repeat=6))
    word_index = {word: index for index, word in enumerate(words)}
    position = {vertex: index for index, vertex in enumerate(vertices)}
    columns = []
    for left, right in combinations(vertices, 2):
        remainder = tuple(
            vertex for vertex in vertices if vertex not in (left, right)
        )
        for left_color, right_color in product(range(Q), repeat=2):
            column = {}
            for remainder_word in product(range(Q), repeat=4):
                colors = dict(
                    zip(remainder, remainder_word, strict=True)
                )
                value = base.matching_value(edges, remainder, colors)
                if not value:
                    continue
                word = [0] * 6
                word[position[left]] = left_color
                word[position[right]] = right_color
                for vertex in remainder:
                    word[position[vertex]] = colors[vertex]
                column[word_index[tuple(word)]] = value
            columns.append(column)
    return columns


def audit_overlap(d, seed, expected_rank):
    assert d in (1, 2)
    rng = Random(seed)
    Z = tuple(range(6 + d))
    P = tuple(range(6 + d, 12))
    identity = identity_matrix()
    omitted_sets = tuple(combinations(Z, d))
    omitted_index = {
        omitted: index for index, omitted in enumerate(omitted_sets)
    }

    internal_P = {
        edge: base.random_matrix(rng) for edge in combinations(P, 2)
    }
    cross = {
        (z, p): base.random_matrix(rng) for z in Z for p in P
    }
    assert all(
        base.determinant3(matrix)
        for matrix in tuple(internal_P.values()) + tuple(cross.values())
    )

    p_words = tuple(product(range(Q), repeat=len(P)))
    p_permutations = tuple(permutations(P))
    rho = rho_words(len(P))
    atoms = {}
    top_responses = [[0] * len(p_words) for _ in omitted_sets]

    # An atom is indexed by two disjoint d-sets D,A.  The d! bijections
    # from A to D all have identity weight after the D-slots are fixed at
    # zero.  The remaining U is bijected to P.
    for left_index, D in enumerate(omitted_sets):
        D_set = set(D)
        for A in omitted_sets[left_index + 1 :]:
            if D_set.intersection(A):
                continue
            U = tuple(
                vertex
                for vertex in Z
                if vertex not in D_set and vertex not in set(A)
            )
            assert len(U) == len(P)
            values = []
            for p_word in p_words:
                colors_P = dict(zip(P, p_word, strict=True))
                total = 0
                for u_word, coefficient in rho.items():
                    colors_U = dict(zip(U, u_word, strict=True))
                    for p_permutation in p_permutations:
                        term = coefficient
                        for u, p in zip(U, p_permutation, strict=True):
                            term = (
                                term
                                * base.edge_entry(
                                    cross,
                                    u,
                                    p,
                                    colors_U[u],
                                    colors_P[p],
                                )
                            ) % P_MOD
                        total = (total + term) % P_MOD
                # d! identity bijections between A and D.
                factorial_d = 1 if d == 1 else 2
                values.append(factorial_d * total % P_MOD)
            atoms[D, A] = values
            right_index = omitted_index[A]
            for word_index, value in enumerate(values):
                top_responses[left_index][word_index] = (
                    top_responses[left_index][word_index] + value
                ) % P_MOD
                top_responses[right_index][word_index] = (
                    top_responses[right_index][word_index] + value
                ) % P_MOD

    assert dense_rank(top_responses) == expected_rank

    # The abstract unsigned incidence matrix has full row rank as well.
    graph_edges = tuple(atoms)
    incidence_rows = []
    for D in omitted_sets:
        incidence_rows.append([
            int(D == edge[0] or D == edge[1])
            for edge in graph_edges
        ])
    assert dense_rank(incidence_rows) == len(omitted_sets)

    # Directly check the all-cross expansion for two sample output words
    # and the first omitted set.  This guards the atom/incidence derivation.
    D = omitted_sets[0]
    S = tuple(vertex for vertex in Z if vertex not in D)
    R = P + D
    lambda_s = rho_words(6)
    all_cross_edges = dict(cross)
    all_cross_edges.update({
        edge: identity for edge in combinations(Z, 2)
    })
    sample_indices = (0, min(1, len(p_words) - 1))
    for sample_index in sample_indices:
        colors_P = dict(zip(P, p_words[sample_index], strict=True))
        direct = 0
        for s_word, coefficient in lambda_s.items():
            colors_S = dict(zip(S, s_word, strict=True))
            colors_R = colors_P | {vertex: 0 for vertex in D}
            for r_permutation in permutations(R):
                term = coefficient
                for s, r in zip(S, r_permutation, strict=True):
                    term = (
                        term
                        * base.edge_entry(
                            all_cross_edges,
                            s,
                            r,
                            colors_S[s],
                            colors_R[r],
                        )
                    ) % P_MOD
                direct = (direct + term) % P_MOD
        assert direct == top_responses[0][sample_index]

    # Every even complement R_D lies on the dense gauge-rigid chart.
    for D in omitted_sets:
        R = tuple(sorted(P + D))
        edges_R = dict(internal_P)
        edges_R.update({
            (min(z, p), max(z, p)): cross[z, p]
            for z in D
            for p in P
        })
        edges_R.update({edge: identity for edge in combinations(D, 2)})
        assert all(
            base.determinant3(edges_R[min(edge), max(edge)])
            for edge in combinations(R, 2)
        )
        assert base.sparse_rank(hessian_columns(R, edges_R)) == 130

    # Every e_0 row from a site of S_D reaches all six vertices of R_D;
    # Theorem 4.1 of the accompanying note therefore makes every associated
    # odd-shore monomer map injective.
    for D in omitted_sets:
        S = tuple(vertex for vertex in Z if vertex not in D)
        R = P + D
        for x in S:
            for r in R:
                matrix = (
                    identity
                    if r in D
                    else cross[x, r]
                )
                assert any(matrix[0])


def main():
    audit_overlap(d=1, seed=777, expected_rank=7)
    audit_overlap(d=2, seed=888, expected_rank=28)
    print("one-deletion K7 incidence rank 7/7 and top-response rank 7/7 PASS")
    print("two-deletion KG(8,2) incidence rank 28/28 and top-response rank 28/28 PASS")
    print("all 7 + 28 overlapping external Hessians have rank 130/135")
    print("sample all-cross expansions equal the symmetric atom sums")


if __name__ == "__main__":
    main()
