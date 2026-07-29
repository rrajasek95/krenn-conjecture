#!/usr/bin/env python3
"""Exact audit for live-component/zero-cut propagation.

This script checks only the coordinate linear algebra used in
``notes/live-component-zero-cut-propagation.md``.  The graph and gauge
arguments in that note are proofs, not finite computations.
"""

from sympy import Matrix, Rational, eye, zeros


def vec(a):
    return Matrix(list(a))


def matrix_rank_of_images(images):
    return Matrix.hstack(*(vec(x) for x in images)).rank()


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for k in range(1, len(vertices)):
        second = vertices[k]
        rest = vertices[1:k] + vertices[k + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def main():
    # A deliberately nonscalar diagonal ratio and a nondegenerate
    # symmetric zero-diagonal live matrix.
    Delta = Matrix.diag(2, 3, 5)
    H = Matrix([[0, 1, 2], [1, 0, 3], [2, 3, 0]])
    assert H.det() == 12

    directed = [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]
    z_basis = []
    for c, d in directed:
        E = zeros(3)
        E[c, d] = 1
        z_basis.append(E)

    def T(M):
        return M * Delta + Delta * M.T

    t_images = [T(E) for E in z_basis]
    assert matrix_rank_of_images(t_images) == 3

    # D = T^{-1}(C H): append -H as a seventh column and project the
    # nullspace to the six Z_0 coordinates.
    augmented = Matrix.hstack(*(vec(x) for x in t_images), -vec(H))
    null = augmented.nullspace()
    Dcoords = Matrix.hstack(*(v[:6, :] for v in null))
    assert Dcoords.rank() == 4

    # The live kernel is three-dimensional and lies in D.
    tmat = Matrix.hstack(*(vec(x) for x in t_images))
    Kcoords = Matrix.hstack(*tmat.nullspace())
    assert Kcoords.rank() == 3
    assert Matrix.hstack(Dcoords, Kcoords).rank() == 4

    # D avoids each two-coordinate directed row and column plane.
    for c in range(3):
        row_idx = [k for k, (a, _b) in enumerate(directed) if a == c]
        col_idx = [k for k, (_a, b) in enumerate(directed) if b == c]
        for idx in (row_idx, col_idx):
            plane = zeros(6, 2)
            plane[idx[0], 0] = 1
            plane[idx[1], 1] = 1
            assert Matrix.hstack(Dcoords, plane).rank() == 6

    # D^perp remembers the three opposite-coordinate ratios d_d/d_c.
    Dperp = Dcoords.T.nullspace()
    assert len(Dperp) == 2
    for c, d in ((0, 1), (0, 2), (1, 2)):
        cd = directed.index((c, d))
        dc = directed.index((d, c))
        for phi in Dperp:
            assert Delta[c, c] * phi[cd] == Delta[d, d] * phi[dc]
        assert any(phi[cd] != 0 for phi in Dperp)

    # Boundary calculation.  All skew matrices annihilating a 3 by 3
    # matrix X on the left force X=0.
    skew = []
    for c, d in ((0, 1), (0, 2), (1, 2)):
        N = zeros(3)
        N[c, d] = 1
        N[d, c] = -1
        skew.append(N)
    x_basis = []
    for c in range(3):
        for d in range(3):
            E = zeros(3)
            E[c, d] = 1
            x_basis.append(E)
    # Stack the three outputs N X vertically for each basis X.
    nx_columns = []
    for E in x_basis:
        nx_columns.append(Matrix.vstack(*(vec(N * E) for N in skew)))
    assert Matrix.hstack(*nx_columns).rank() == 9

    # H P^T=0 also forces P=0.
    hp_columns = [vec(H * E.T) for E in x_basis]
    assert Matrix.hstack(*hp_columns).rank() == 9

    # At a normalized live edge, the six symmetric products give all of
    # Sym^2(C^3).  The three squares remain independent modulo the three
    # off-diagonal products.
    product_blocks = []
    diagonal_blocks = []
    off_diagonal_blocks = []
    for c in range(3):
        E = zeros(3)
        E[c, c] = 2
        product_blocks.append(E)
        diagonal_blocks.append(E)
    for c, d in ((0, 1), (0, 2), (1, 2)):
        E = zeros(3)
        E[c, d] = 1
        E[d, c] = 1
        product_blocks.append(E)
        off_diagonal_blocks.append(E)
    assert matrix_rank_of_images(product_blocks) == 6
    assert matrix_rank_of_images(off_diagonal_blocks) == 3
    assert matrix_rank_of_images(off_diagonal_blocks + diagonal_blocks) == 6

    # If im(P) is a two-plane containing e_r, the restriction of K_r to
    # that image vanishes.  Rank-one matrices kill every alternating form,
    # while an invertible P retains rank two.
    K_forms = [
        Matrix([[0, 0, 0], [0, 0, 1], [0, -1, 0]]),
        Matrix([[0, 0, -1], [0, 0, 0], [1, 0, 0]]),
        Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]]),
    ]
    for r, Kr in enumerate(K_forms):
        other = [c for c in range(3) if c != r][0]
        P_plane = zeros(3)
        P_plane[r, 0] = 1
        P_plane[other, 1] = 1
        assert P_plane.rank() == 2
        assert P_plane.T * Kr * P_plane == zeros(3)
        P_line = zeros(3)
        P_line[(r + 1) % 3, 0] = 1
        assert P_line.rank() == 1
        assert P_line.T * Kr * P_line == zeros(3)
        assert Kr.rank() == 2

    # The nonzero sharp dead-edge rank pairs (2,1), (1,2), and (1,1)
    # arise from H-orthogonal colour row spaces.
    Hinv = H.inv()
    P2 = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 0]])
    v = (Hinv * Matrix([0, 0, 1])).T
    Q1 = Matrix.vstack(v, zeros(2, 3))
    assert P2.rank() == 2 and Q1.rank() == 1
    assert P2 * H * Q1.T == zeros(3)
    assert Q1 * H * P2.T == zeros(3)
    P1 = Matrix([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    w = (Hinv * Matrix([0, 1, 0])).T
    Q1b = Matrix.vstack(w, zeros(2, 3))
    assert P1.rank() == Q1b.rank() == 1
    assert P1 * H * Q1b.T == zeros(3)

    # Sharp relation/gauge countermodel on six internal sites.
    # Sites 0,1,2 are live; sites 3,4,5 have both deleted stars zero.
    live = {0, 1, 2}
    site_P = [eye(3) if i in live else zeros(3) for i in range(6)]
    site_S = [P * Delta for P in site_P]
    beta = [1, 1, 1, -1, -1, -1]
    assert sum(beta) == 0

    q = {}
    for i in range(6):
        for j in range(i + 1, 6):
            if i in live and j in live:
                q[i, j] = Rational(1, 2) * H
            elif (i in live) != (j in live):
                # This is an exceptional beta_i+beta_j=0 block and may
                # be chosen freely; choose it invertible.
                q[i, j] = H
            else:
                q[i, j] = zeros(3)
            assert site_P[i] * H * site_P[j].T == (beta[i] + beta[j]) * q[i, j]

    # The rank-three graph is K_3 joined to an independent three-set.
    rank3_edges = [(i, j) for (i, j), Q in q.items() if Q.rank() == 3]
    assert len(rank3_edges) == 3 + 9
    assert all((i, j) in rank3_edges for i in live for j in live if i < j)
    assert all(any(i in e for e in rank3_edges) for i in range(6))

    # Every relation in D has a one-dimensional response on live-live
    # pairs and zero response elsewhere.  The response is the vertex
    # gauge with parameters t on the live shore and -t on the zero shore.
    for coord in [Dcoords[:, k] for k in range(Dcoords.cols)]:
        M = sum((coord[k] * z_basis[k] for k in range(6)), zeros(3))
        TM = T(M)
        # Recover t from a nonzero entry of H; D guarantees TM=tH.
        scalar = TM[0, 1] / H[0, 1]
        assert TM == scalar * H
        alpha = [scalar if i in live else -scalar for i in range(6)]
        assert sum(alpha) == 0
        for i in range(6):
            for j in range(i + 1, 6):
                response = site_P[i] * M * site_S[j].T + site_S[i] * M.T * site_P[j].T
                assert response == (alpha[i] + alpha[j]) * q[i, j]

    # Each of the six global deleted-star rows reaches exactly three sites.
    for c in range(3):
        assert sum(site_P[i][:, c] != zeros(3, 1) for i in range(6)) == 3
        assert sum(site_S[i][:, c] != zeros(3, 1) for i in range(6)) == 3

    # Every Hessian response of a product supported on two live sites is
    # zero: the remaining 1-live/3-zero set forces a zero--zero q edge.
    for i in live:
        for j in live:
            if i >= j:
                continue
            remaining = [k for k in range(6) if k not in (i, j)]
            for matching in perfect_matchings(remaining):
                assert any(a not in live and b not in live for a, b in matching)

    # Q itself is nonzero.  At the word which is colour 0 on the live
    # shore and colour 1 on the zero shore, precisely the 3! all-cross
    # matchings contribute, each with coefficient H[0,1]^3=1.
    word = [0, 0, 0, 1, 1, 1]
    q_coefficient = 0
    for matching in perfect_matchings(range(6)):
        contribution = 1
        for a, b in matching:
            if a > b:
                a, b = b, a
            contribution *= q[a, b][word[a], word[b]]
        q_coefficient += contribution
    assert q_coefficient == 6

    print("live-component zero-cut propagation audit: PASS")


if __name__ == "__main__":
    main()
