#!/usr/bin/env python3
"""Exact finite-field audits for the six-set Hessian pullback note.

The proofs in the note are characteristic-zero arguments.  These independent
computations check their polynomial identities over the prime field F_P:

* direct one-crossing enumeration equals the boundary--monomer factorization;
* the monomer contraction equals the augmented internal Hessian expression;
* a dense six-site specialization has Hessian kernel exactly the five
  vertex gauges and its identity-star seven-site monomer map is injective;
* six simultaneous target-nonzero witnesses annihilate every individual
  boundary response when all blocks incident to the distinguished six-set
  are identities; and
* the six overlapping five-set sectors count each R|S zero-crossing
  matching six times and each two-crossing matching twice.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations, product
from random import Random


P = 1_000_003
Q = 3


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def random_matrix(rng):
    return tuple(
        tuple(rng.randrange(1, P) for _ in range(Q))
        for _ in range(Q)
    )


def determinant3(matrix):
    return (
        matrix[0][0] * (
            matrix[1][1] * matrix[2][2]
            - matrix[1][2] * matrix[2][1]
        )
        - matrix[0][1] * (
            matrix[1][0] * matrix[2][2]
            - matrix[1][2] * matrix[2][0]
        )
        + matrix[0][2] * (
            matrix[1][0] * matrix[2][1]
            - matrix[1][1] * matrix[2][0]
        )
    ) % P


def edge_entry(edges, left, right, left_color, right_color):
    if left < right:
        return edges[left, right][left_color][right_color]
    return edges[right, left][right_color][left_color]


def matching_value(edges, vertices, colors):
    answer = 0
    for matching in perfect_matchings(vertices):
        term = 1
        for left, right in matching:
            term = (
                term
                * edge_entry(
                    edges,
                    left,
                    right,
                    colors[left],
                    colors[right],
                )
            ) % P
        answer = (answer + term) % P
    return answer


def audit_boundary_monomer_factorization():
    rng = Random(20260725)
    vertices = tuple(range(8))
    C = (0, 1, 2)
    C_set = set(C)
    U = tuple(vertex for vertex in vertices if vertex not in C_set)
    edges = {
        edge: random_matrix(rng)
        for edge in combinations(vertices, 2)
    }
    matchings = tuple(perfect_matchings(vertices))

    @lru_cache(maxsize=None)
    def hafnian(subset, word):
        colors = dict(zip(subset, word, strict=True))
        return matching_value(edges, subset, colors)

    checked = 0
    for left_word in product(range(Q), repeat=3):
        for right_word in product(range(Q), repeat=5):
            colors = dict(zip(C, left_word, strict=True))
            colors.update(zip(U, right_word, strict=True))

            direct = 0
            for matching in matchings:
                crossing = sum(
                    (left in C_set) != (right in C_set)
                    for left, right in matching
                )
                if crossing != 1:
                    continue
                term = 1
                for left, right in matching:
                    term = (
                        term
                        * edge_entry(
                            edges,
                            left,
                            right,
                            colors[left],
                            colors[right],
                        )
                    ) % P
                direct = (direct + term) % P

            factored = 0
            for c in C:
                C_remainder = tuple(vertex for vertex in C if vertex != c)
                left_remainder = tuple(colors[vertex] for vertex in C_remainder)
                P_c = hafnian(C_remainder, left_remainder)
                boundary = 0
                for u in U:
                    U_remainder = tuple(vertex for vertex in U if vertex != u)
                    right_remainder = tuple(
                        colors[vertex] for vertex in U_remainder
                    )
                    boundary += (
                        edge_entry(
                            edges, c, u, colors[c], colors[u]
                        )
                        * hafnian(U_remainder, right_remainder)
                    )
                factored = (factored + P_c * boundary) % P

            assert direct == factored % P
            checked += 1
    assert checked == Q**8


def audit_monomer_hessian_identity():
    rng = Random(314159)
    R = tuple(range(6))
    x = 6
    internal = {
        edge: random_matrix(rng)
        for edge in combinations(R, 2)
    }
    star = {
        (s, x): random_matrix(rng)
        for s in R
    }
    edges = internal | star
    z = {
        vertex: tuple(rng.randrange(P) for _ in range(Q))
        for vertex in R + (x,)
    }
    lam = tuple(rng.randrange(P) for _ in range(Q))

    @lru_cache(maxsize=None)
    def hafnian(subset, word):
        colors = dict(zip(subset, word, strict=True))
        return matching_value(edges, subset, colors)

    p = {}
    for s in R:
        p[s] = tuple(
            sum(
                lam[a] * edge_entry(edges, x, s, a, b)
                for a in range(Q)
            ) % P
            for b in range(Q)
        )
    lambda_zx = sum(lam[a] * z[x][a] for a in range(Q)) % P

    checked = 0
    for word in product(range(Q), repeat=len(R)):
        colors_R = dict(zip(R, word, strict=True))

        left = 0
        for x_color in range(Q):
            colors_C = colors_R | {x: x_color}
            monomer = 0
            for c in R + (x,):
                remainder = tuple(
                    vertex for vertex in R + (x,) if vertex != c
                )
                remainder_word = tuple(colors_C[v] for v in remainder)
                monomer += z[c][colors_C[c]] * hafnian(
                    remainder, remainder_word
                )
            left = (left + lam[x_color] * monomer) % P

        h_R = hafnian(R, word)
        derivative = 0
        for r, s in combinations(R, 2):
            remainder = tuple(
                vertex for vertex in R if vertex not in (r, s)
            )
            remainder_word = tuple(colors_R[v] for v in remainder)
            block = (
                p[r][colors_R[r]] * z[s][colors_R[s]]
                + z[r][colors_R[r]] * p[s][colors_R[s]]
            ) % P
            derivative += block * hafnian(remainder, remainder_word)

        right = (lambda_zx * h_R + derivative) % P
        assert left == right
        checked += 1
    assert checked == Q**6


def sparse_rank(columns):
    pivots = {}
    for original in columns:
        column = {
            row: value % P
            for row, value in original.items()
            if value % P
        }
        while column:
            pivot = min(column)
            value = column[pivot]
            known = pivots.get(pivot)
            if known is None:
                inverse = pow(value, P - 2, P)
                column = {
                    row: coefficient * inverse % P
                    for row, coefficient in column.items()
                }
                pivots[pivot] = column
                break
            for row, coefficient in known.items():
                reduced = (
                    column.get(row, 0) - value * coefficient
                ) % P
                if reduced:
                    column[row] = reduced
                elif row in column:
                    del column[row]
    return len(pivots)


def audit_dense_hessian_and_monomer_ranks():
    rng = Random(271828)
    R = tuple(range(6))
    x = 6

    # The first deterministic draw already has all blocks invertible and
    # maximum Hessian rank; retain the loop as an adversarial guard against
    # changes to the seed or generator.
    for _attempt in range(20):
        internal = {
            edge: random_matrix(rng)
            for edge in combinations(R, 2)
        }
        if not all(determinant3(matrix) for matrix in internal.values()):
            continue

        words_R = tuple(product(range(Q), repeat=6))
        word_index_R = {word: index for index, word in enumerate(words_R)}
        hessian_columns = []
        for r, s in combinations(R, 2):
            remainder = tuple(
                vertex for vertex in R if vertex not in (r, s)
            )
            for a, b in product(range(Q), repeat=2):
                column = {}
                for remainder_word in product(range(Q), repeat=4):
                    colors = dict(zip(remainder, remainder_word, strict=True))
                    value = matching_value(internal, remainder, colors)
                    if not value:
                        continue
                    word = [0] * 6
                    word[r], word[s] = a, b
                    for vertex in remainder:
                        word[vertex] = colors[vertex]
                    column[word_index_R[tuple(word)]] = value
                hessian_columns.append(column)

        hessian_rank = sparse_rank(hessian_columns)
        if hessian_rank == 130:
            break
    else:
        raise AssertionError("no gauge-rigid dense specialization found")

    identity = tuple(
        tuple(int(a == b) for b in range(Q))
        for a in range(Q)
    )
    star = {(s, x): identity for s in R}
    edges = internal | star
    # The e_0 row of every identity star matrix is nonzero, hence its site
    # support is all six vertices and in particular at least three.  This
    # is the star used by the simultaneous boundary-witness countermodel.
    assert all(any(star[s, x][0]) for s in R)

    C = R + (x,)
    words_C = tuple(product(range(Q), repeat=7))
    word_index_C = {word: index for index, word in enumerate(words_C)}
    monomer_columns = []
    for c in C:
        remainder = tuple(vertex for vertex in C if vertex != c)
        for color_c in range(Q):
            column = {}
            for remainder_word in product(range(Q), repeat=6):
                colors = dict(zip(remainder, remainder_word, strict=True))
                value = matching_value(edges, remainder, colors)
                if not value:
                    continue
                word = [0] * 7
                word[c] = color_c
                for vertex in remainder:
                    word[vertex] = colors[vertex]
                column[word_index_C[tuple(word)]] = value
            monomer_columns.append(column)
    assert sparse_rank(monomer_columns) == 21


def audit_all_boundary_response_annihilators():
    """Check the simultaneous local countermodel from Section 6.

    Label the common six-set by 0,...,5 and use identity blocks both inside
    it and from every external shore vertex into it.  The internal blocks
    on the external shore do not enter these boundary contractions; they
    can be chosen as in ``audit_dense_hessian_and_monomer_ranks`` so that
    every relevant monomer map is injective.
    """

    S = tuple(range(6))
    R = tuple(range(6, 12))
    identity = tuple(
        tuple(int(a == b) for b in range(Q))
        for a in range(Q)
    )
    edges = {
        edge: identity
        for edge in combinations(S + R, 2)
        if edge[0] in S or edge[1] in S
    }

    for x in S:
        U = tuple(vertex for vertex in S if vertex != x)
        C = R + (x,)
        word_constant = (0, 0, 0, 0, 0)
        beta = {word_constant: 2}
        beta.update({
            word: -1
            for word in product((0, 1), repeat=5)
            if sum(word) == 2
        })

        # In fact beta kills each four-site cofactor insertion separately.
        # This makes the boundary equations independent of the cross blocks.
        for u in U:
            curried = [0] * Q
            for u_color in range(Q):
                total = 0
                for word, beta_value in beta.items():
                    colors_U = dict(zip(U, word, strict=True))
                    if colors_U[u] != u_color:
                        continue
                    remainder = tuple(v for v in U if v != u)
                    remainder_colors = {
                        v: colors_U[v] for v in remainder
                    }
                    total += beta_value * matching_value(
                        edges, remainder, remainder_colors
                    )
                curried[u_color] = total
            assert curried == [0, 0, 0]

        # Directly contract beta against every response
        # R_c^U = sum_u A_cu tensor H_(U-u).
        for c in C:
            response = [0] * Q
            for c_color in range(Q):
                total = 0
                for word, beta_value in beta.items():
                    colors_U = dict(zip(U, word, strict=True))
                    for u in U:
                        remainder = tuple(v for v in U if v != u)
                        remainder_colors = {
                            v: colors_U[v] for v in remainder
                        }
                        h_four = matching_value(
                            edges, remainder, remainder_colors
                        )
                        total += (
                            beta_value
                            * edge_entry(
                                edges,
                                c,
                                u,
                                c_color,
                                colors_U[u],
                            )
                            * h_four
                        )
                response[c_color] = total
            assert response == [0, 0, 0]

        # The same functional remains nonzero on the target constant row.
        assert beta[word_constant] == 2


def audit_six_cut_multiplicities():
    for n in (8, 10):
        vertices = tuple(range(n))
        S = set(range(6))
        R = set(vertices) - S
        for matching in perfect_matchings(vertices):
            j = sum(
                (left in R) != (right in R)
                for left, right in matching
            )
            multiplicity = 0
            for x in S:
                C_x = R | {x}
                crossing = sum(
                    (left in C_x) != (right in C_x)
                    for left, right in matching
                )
                multiplicity += int(crossing == 1)
            expected = 6 if j == 0 else 2 if j == 2 else 0
            assert multiplicity == expected


def audit_dense_six_tensor_annihilators():
    vertices = tuple(range(6))
    identity = tuple(
        tuple(int(a == b) for b in range(Q))
        for a in range(Q)
    )
    edges = {
        edge: identity
        for edge in combinations(vertices, 2)
    }

    for x in vertices:
        U = tuple(vertex for vertex in vertices if vertex != x)
        rows = []
        for x_color in range(Q):
            row = {}
            for word in product(range(Q), repeat=5):
                colors = dict(zip(U, word, strict=True)) | {x: x_color}
                value = matching_value(edges, vertices, colors)
                if value:
                    row[word] = value
            rows.append(row)

        # The parity classes supporting the three rows are pairwise
        # disjoint and nonempty, so the mode flattening has rank three.
        assert all(rows)
        assert all(
            set(rows[left]).isdisjoint(rows[right])
            for left in range(Q)
            for right in range(left + 1, Q)
        )

        word_constant = (0, 0, 0, 0, 0)
        word_mixed = (0, 0, 0, 1, 1)
        beta = {word_constant: 1, word_mixed: -5}
        for row in rows:
            assert sum(
                beta.get(word, 0) * value
                for word, value in row.items()
            ) == 0
        assert beta[word_constant] == 1
        assert beta.get((1, 1, 1, 1, 1), 0) == 0
        assert beta.get((2, 2, 2, 2, 2), 0) == 0


def main():
    audit_boundary_monomer_factorization()
    audit_monomer_hessian_identity()
    audit_dense_hessian_and_monomer_ranks()
    audit_dense_six_tensor_annihilators()
    audit_all_boundary_response_annihilators()
    audit_six_cut_multiplicities()
    print("boundary--monomer factorization: 3^8 coefficients PASS")
    print("monomer--Hessian identity: 3^6 coefficients PASS")
    print("dense R=6 Hessian rank 130/135 and identity-star monomer rank 21/21 PASS")
    print("dense invertible K6 tensor has target-nonzero kernels at all modes")
    print("all six target-nonzero witnesses kill every boundary response")
    print("six-cut sector multiplicities at n=8,10 PASS")


if __name__ == "__main__":
    main()
