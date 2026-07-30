#!/usr/bin/env python3
"""Lightweight exact checks for the rank-two alignment kernel-cap descent."""

from itertools import combinations, permutations, product


if not __debug__:
    raise SystemExit("run without -O: this checker uses assertions")


def matmul(a, b, p):
    return [
        [sum(a[i][k] * b[k][j] for k in range(3)) % p for j in range(3)]
        for i in range(3)
    ]


def transpose(a):
    return [list(row) for row in zip(*a)]


def det(a, p):
    return (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    ) % p


def rank(a, p):
    m = [row[:] for row in a]
    r = 0
    for c in range(3):
        pivot = next((i for i in range(r, 3) if m[i][c] % p), None)
        if pivot is None:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        inv = pow(m[r][c] % p, -1, p)
        m[r] = [(inv * x) % p for x in m[r]]
        for i in range(3):
            if i != r and m[i][c] % p:
                t = m[i][c] % p
                m[i] = [(m[i][j] - t * m[r][j]) % p for j in range(3)]
        r += 1
    return r


def adj(a, p):
    return [
        [
            (a[(j + 1) % 3][(i + 1) % 3] * a[(j + 2) % 3][(i + 2) % 3]
             - a[(j + 1) % 3][(i + 2) % 3] * a[(j + 2) % 3][(i + 1) % 3])
            % p
            for j in range(3)
        ]
        for i in range(3)
    ]


def mv(a, v, p):
    return [sum(a[i][j] * v[j] for j in range(3)) % p for i in range(3)]


def outer(u, v, p):
    return [[u[i] * v[j] % p for j in range(3)] for i in range(3)]


def scale(a, t, p):
    return [[t * x % p for x in row] for row in a]


def normalized(v, p):
    first = next(x for x in v if x % p)
    inv = pow(first % p, -1, p)
    return tuple(inv * x % p for x in v)


def kernel_line(a, p):
    assert rank(a, p) == 2
    for v in product(range(p), repeat=3):
        if any(v) and mv(a, v, p) == [0, 0, 0]:
            return normalized(v, p)
    raise AssertionError("rank-two matrix has no kernel vector")


def support(v):
    return {i for i, x in enumerate(v) if x}


def j_matrix(e, p):
    # u^T J_e v = det(u,v,e_e).
    if e == 0:
        return [[0, 0, 0], [0, 0, 1], [0, -1 % p, 0]]
    if e == 1:
        return [[0, 0, -1 % p], [0, 0, 0], [1, 0, 0]]
    return [[0, 1, 0], [-1 % p, 0, 0], [0, 0, 0]]


def check_adjugate_samples():
    p = 5
    checked = 0
    state = 17
    for e in range(3):
        j = j_matrix(e, p)
        for _ in range(2500):
            vals = []
            for _ in range(18):
                state = (37 * state + 11) % 1000003
                vals.append(state % p)
            P = [vals[3 * i:3 * i + 3] for i in range(3)]
            S = [vals[9 + 3 * i:12 + 3 * i] for i in range(3)]
            d = matmul(matmul(transpose(P), j, p), S, p)
            if rank(d, p) != 2:
                continue
            lhs = adj(d, p)
            se = [adj(S, p)[i][e] for i in range(3)]
            pe = [adj(P, p)[i][e] for i in range(3)]
            assert lhs == outer(se, pe, p)
            xi = kernel_line(transpose(d), p)
            eta = kernel_line(d, p)
            assert normalized(pe, p) == xi
            assert normalized(se, p) == eta
            pxi = mv(P, xi, p)
            seta = mv(S, eta, p)
            assert all(pxi[i] == 0 for i in range(3) if i != e)
            assert all(seta[i] == 0 for i in range(3) if i != e)
            checked += 1
    assert checked > 1000
    return checked


def check_support_classification():
    p = 3
    rank_two = 0
    disjoint = 0
    crossed = 0
    for flat in product(range(p), repeat=9):
        d = [list(flat[3 * i:3 * i + 3]) for i in range(3)]
        if rank(d, p) != 2:
            continue
        rank_two += 1
        xi = kernel_line(transpose(d), p)
        eta = kernel_line(d, p)
        sx, se = support(xi), support(eta)
        if not (sx & se):
            disjoint += 1
            assert len(sx) == 1 or len(se) == 1
            if len(sx) == 1:
                i = next(iter(sx))
                assert all(d[i][j] == 0 for j in range(3))
            if len(se) == 1:
                j = next(iter(se))
                assert all(d[i][j] == 0 for i in range(3))
        for e in range(3):
            if sx & se <= {e}:
                crossed += 1
                if len(sx) == 1:
                    i = next(iter(sx))
                    assert all(d[i][j] == 0 for j in range(3))
                elif len(sx) == 3:
                    assert se == {e}
                elif e not in sx:
                    assert len(sx) == 2
                    assert se == ({0, 1, 2} - sx)
                else:
                    a = next(iter(sx - {e}))
                    b = next(iter({0, 1, 2} - {e, a}))
                    assert se <= {e, b}
    assert rank_two > 0 and disjoint > 0 and crossed > 0
    return rank_two, disjoint, crossed


def check_three_marked_matching():
    vertices = range(6)
    edges = list(combinations(vertices, 2))
    checked = 0
    for marked in combinations(vertices, 3):
        marked = set(marked)
        for cap in edges:
            if marked & set(cap):
                continue
            rest = [v for v in vertices if v not in cap]
            matchings = []
            a = rest[0]
            for b in rest[1:]:
                tail = [v for v in rest[1:] if v != b]
                matchings.append(((a, b), tuple(tail)))
            for first, tail in matchings:
                second = tuple(tail)
                assert len(second) == 2
                assert (set(first) <= marked or set(second) <= marked)
                checked += 1
    assert checked > 0
    return checked


def check_sharp_local_models():
    p = 5
    e = 0
    j = j_matrix(e, p)

    # Common zero row (and here also a zero column): P=S=I gives J_0.
    I = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    d_row = matmul(matmul(transpose(I), j, p), I, p)
    assert rank(d_row, p) == 2
    assert kernel_line(transpose(d_row), p) == (1, 0, 0)

    # Noncoordinate left kernel {0,1}, coordinate right kernel {2}.
    P = [[1, 0, 0], [1, -1 % p, 0], [0, 0, 1]]
    S = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
    d_col = matmul(matmul(transpose(P), j, p), S, p)
    assert rank(d_col, p) == 2
    assert support(kernel_line(transpose(d_col), p)) == {0, 1}
    assert kernel_line(d_col, p) == (0, 0, 1)
    assert all(d_col[i][2] == 0 for i in range(3))

    # The invertible-local target-centred cross: {0,1} against {0,2}.
    R = [[1, 0, 0], [1, 0, -1 % p], [0, 1, 0]]
    d_cross = matmul(matmul(transpose(P), j, p), R, p)
    assert rank(d_cross, p) == 2
    assert support(kernel_line(transpose(d_cross), p)) == {0, 1}
    assert support(kernel_line(d_cross, p)) == {0, 2}
    assert det(P, p) and det(R, p)

    # The kernel-cap contraction has zero direct coefficient, and a retained
    # diagonal plus an off-diagonal coefficient whenever its support is not
    # one coincident coordinate cell.
    xi = kernel_line(transpose(d_cross), p)
    eta = kernel_line(d_cross, p)
    assert sum(xi[i] * d_cross[i][j] * eta[j]
               for i in range(3) for j in range(3)) % p == 0
    common = support(xi) & support(eta)
    assert common == {0}
    cells = {(i, k) for i in support(xi) for k in support(eta)}
    assert (0, 0) in cells and any(i != k for i, k in cells)
    return d_row, d_col, d_cross


def main():
    adjugate = check_adjugate_samples()
    rank_two, disjoint, crossed = check_support_classification()
    matchings = check_three_marked_matching()
    check_sharp_local_models()
    print("rank-two alignment kernel-cap descent: PASS")
    print(f"  adjugate/target-line samples: {adjugate}")
    print(f"  F3 rank-two matrices: {rank_two}")
    print(f"  disjoint-support matrices: {disjoint}")
    print(f"  target-centred support incidences: {crossed}")
    print(f"  three-marked matching checks: {matchings}")


if __name__ == "__main__":
    main()
