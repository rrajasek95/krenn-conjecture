#!/usr/bin/env python3
"""Exact audit of the uniform five-witness live-component counterconfiguration."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations

import sympy as sp


DELTA = sp.diag(2, 3, 5)
H = sp.Matrix([[0, 1, 2], [1, 0, 3], [2, 3, 0]])
I3 = sp.eye(3)
Z3 = sp.zeros(3)
K = (
    sp.Matrix([[0, 0, 0], [0, 0, 1], [0, -1, 0]]),
    sp.Matrix([[0, 0, -1], [0, 0, 0], [1, 0, 0]]),
    sp.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]]),
)

DIRECTED = ((0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1))


def relation_space() -> tuple[sp.Matrix, ...]:
    columns = []
    for c, d in DIRECTED:
        matrix = sp.zeros(3)
        matrix[c, d] = 1
        columns.append(matrix * DELTA + DELTA * matrix.T)
    coordinate_map = sp.Matrix(
        [[matrix[0, 1], matrix[0, 2], matrix[1, 2]] for matrix in columns]
    ).T
    h = sp.Matrix([H[0, 1], H[0, 2], H[1, 2]])
    constraints = sp.Matrix([[h[1], -h[0], 0], [h[2], 0, -h[0]]])
    kernel = (constraints * coordinate_map).nullspace()
    assert len(kernel) == 4

    # The four-plane avoids every coordinate row and column two-plane.
    basis = sp.Matrix.hstack(*kernel)
    for c in range(3):
        row_positions = {index for index, (a, _b) in enumerate(DIRECTED) if a == c}
        col_positions = {index for index, (_a, b) in enumerate(DIRECTED) if b == c}
        assert basis.extract(
            [index for index in range(6) if index not in row_positions], range(4)
        ).rank() == 4
        assert basis.extract(
            [index for index in range(6) if index not in col_positions], range(4)
        ).rank() == 4

    answer = []
    for vector in kernel:
        matrix = sp.zeros(3)
        for coefficient, (c, d) in zip(vector, DIRECTED):
            matrix[c, d] = coefficient
        answer.append(matrix)
    return tuple(answer)


RELATION_BASIS = relation_space()


def construction(n: int):
    assert n >= 10 and n % 2 == 0
    internal_size = n - 2
    if n == 10:
        U = (0, 1, 2)
        Z = (3, 4, 5, 6, 7)
        signs = {**{u: 1 for u in U}, 3: -1, 4: -1, 5: -1, 6: -1, 7: 1}
        cross_edges = ((0, 3), (1, 4), (2, 5), (0, 6), (6, 7))
        chosen_matching = ((0, 3), (1, 4), (2, 5), (6, 7))
    else:
        half = internal_size // 2
        U = tuple(range(half))
        Z = tuple(range(half, internal_size))
        signs = {**{u: 1 for u in U}, **{z: -1 for z in Z}}
        cross_edges = tuple(zip(U, Z))
        chosen_matching = cross_edges

    blocks = {}
    for i, j in combinations(U, 2):
        blocks[i, j] = H / 2
    for i, j in cross_edges:
        blocks[min(i, j), max(i, j)] = H

    assert sum(signs.values()) == 0
    assert len(Z) >= 5
    assert len(chosen_matching) * 2 == internal_size
    return U, Z, signs, blocks, tuple(tuple(sorted(edge)) for edge in chosen_matching)


def block(blocks, i, j):
    if i < j:
        return blocks.get((i, j), Z3)
    return blocks.get((j, i), Z3).T


def perfect_matchings(vertices, blocks):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    i = vertices[0]
    for position, j in enumerate(vertices[1:], 1):
        if block(blocks, i, j) == Z3:
            continue
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest, blocks):
            yield ((min(i, j), max(i, j)),) + tail


def connected(vertices, blocks):
    reached = {vertices[0]}
    frontier = [vertices[0]]
    while frontier:
        i = frontier.pop()
        for j in vertices:
            if j not in reached and i != j and block(blocks, i, j) != Z3:
                reached.add(j)
                frontier.append(j)
    return reached == set(vertices)


def audit_order(n: int) -> None:
    U, Z, signs, blocks, chosen_matching = construction(n)
    W = tuple(range(n - 2))

    assert H.det() != 0 and DELTA.det() != 0
    assert connected(W, blocks)
    assert all(blocks[edge].det() != 0 for edge in blocks)
    assert len(U) >= 3  # the U-clique supplies an odd cycle

    matchings = tuple(perfect_matchings(W, blocks))
    assert matchings == (chosen_matching,)

    # Deleting the endpoints of any product supported on U destroys every
    # perfect matching, so all nine product Hessians vanish.
    for i, j in combinations(U, 2):
        remaining = tuple(vertex for vertex in W if vertex not in (i, j))
        assert not tuple(perfect_matchings(remaining, blocks))

    P = {i: I3 if i in U else Z3 for i in W}
    S = {i: P[i] * DELTA for i in W}

    # Every vector in the exact relation four-plane is the announced gauge.
    for M in RELATION_BASIS:
        response = M * DELTA + DELTA * M.T
        scalar = sp.simplify(response[0, 1] / H[0, 1])
        assert response == scalar * H
        alpha = {i: scalar * signs[i] for i in W}
        assert sp.simplify(sum(alpha.values())) == 0
        for i, j in combinations(W, 2):
            lifted = P[i] * M * S[j].T + S[i] * M.T * P[j].T
            gauge = sp.simplify(alpha[i] + alpha[j]) * block(blocks, i, j)
            assert lifted == gauge

    # Every live U-edge has precisely Z as its zero-cross witness set after
    # re-deletion.  The original deleted sites and the other U-sites are
    # rank-two nonwitnesses.
    for i, j in combinations(U, 2):
        witnesses = set()
        external_crosses = {
            "p": tuple(P[i] * form * P[j].T for form in K),
            "q": tuple(S[i] * form * S[j].T for form in K),
        }
        for name, crosses in external_crosses.items():
            assert all(matrix.rank() == 2 for matrix in crosses), name
        for x in W:
            if x in (i, j):
                continue
            crosses = tuple(
                block(blocks, i, x) * form * block(blocks, j, x).T
                for form in K
            )
            if any(matrix == Z3 for matrix in crosses):
                witnesses.add(x)
            else:
                assert all(matrix.rank() == 2 for matrix in crosses)
        assert witnesses == set(Z)

    # All six deleted-star rows reach every site in U.
    assert len(U) >= 3
    for c in range(3):
        assert sum(P[i][:, c] != Z3[:, c] for i in W) == len(U)
        assert sum(S[i][:, c] != Z3[:, c] for i in W) == len(U)


def main() -> None:
    for n in (10, 12, 14, 16, 18):
        audit_order(n)
    print("uniform live-component five-witness counterconfiguration: PASS")


if __name__ == "__main__":
    main()
