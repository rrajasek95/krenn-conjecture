#!/usr/bin/env python3
"""Exact lightweight checks for the target-centred cross descent."""

from itertools import product


def require(condition, message="exact check failed"):
    """Optimization-safe replacement for assert."""
    if not condition:
        raise AssertionError(message)


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b, modulus=None):
    out = [
        [sum(a[i][k] * b[k][j] for k in range(len(b)))
         for j in range(len(b[0]))]
        for i in range(len(a))
    ]
    if modulus is not None:
        out = [[value % modulus for value in row] for row in out]
    return out


def matvec(a, v, modulus=None):
    out = [sum(row[j] * v[j] for j in range(len(v))) for row in a]
    if modulus is not None:
        out = [value % modulus for value in out]
    return out


def det3(a, modulus=None):
    value = (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    )
    return value if modulus is None else value % modulus


def rank_mod(a, p):
    rows = [[value % p for value in row] for row in a]
    rank = 0
    for column in range(len(rows[0])):
        pivot = next(
            (i for i in range(rank, len(rows)) if rows[i][column]), None
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][column], -1, p)
        rows[rank] = [(inv * value) % p for value in rows[rank]]
        for i in range(len(rows)):
            if i == rank or rows[i][column] == 0:
                continue
            scale = rows[i][column]
            rows[i] = [
                (value - scale * pivot_value) % p
                for value, pivot_value in zip(rows[i], rows[rank])
            ]
        rank += 1
    return rank


def j_matrix(label, p=None):
    minus_one = -1 if p is None else p - 1
    matrices = (
        [[0, 0, 0], [0, 0, 1], [0, minus_one, 0]],
        [[0, 0, minus_one], [0, 0, 0], [1, 0, 0]],
        [[0, 1, 0], [minus_one, 0, 0], [0, 0, 0]],
    )
    return matrices[label]


def poly_add(left, right):
    answer = dict(left)
    for monomial, coefficient in right.items():
        answer[monomial] = answer.get(monomial, 0) + coefficient
        if answer[monomial] == 0:
            del answer[monomial]
    return answer


def poly_scale(poly, scalar):
    return {
        monomial: scalar * coefficient
        for monomial, coefficient in poly.items()
        if scalar * coefficient
    }


def response_polynomials(A, B, C, D, xi_e=2, xi_a=3):
    # Coefficients are indexed by r^2, rs, s^2.
    e_response = (-xi_e * B, -xi_e * D, 0)
    a_response = (0, xi_a * A, xi_a * C)
    return e_response, a_response


def proportional(left, right):
    """Whether two nonzero binary linear forms are proportional."""
    return left[0] * right[1] == left[1] * right[0]


def check_kernel_contractions():
    """Audit the index contractions with independent integer samples."""
    checked = 0
    state = 29
    for _ in range(200):
        # Build two rank-two matrices with a common prescribed left kernel.
        values = []
        for _ in range(12):
            state = (73 * state + 19) % 1000003
            values.append((state % 11) - 5)
        row0 = values[0:3]
        row2 = values[3:6]
        row0p = values[6:9]
        row2p = values[9:12]
        d = [row0, [-value for value in row0], row2]
        dp = [row0p, [-value for value in row0p], row2p]
        xi = [1, 1, 0]
        require(matvec(transpose(d), xi) == [0, 0, 0])
        require(matvec(transpose(dp), xi) == [0, 0, 0])

        # Coefficients of t_k and y_j vanish after the i contraction.
        for j, k in product(range(3), repeat=2):
            require(sum(xi[i] * d[i][j] for i in range(3)) == 0)
            require(sum(xi[i] * dp[i][k] for i in range(3)) == 0)
            target = sum(
                xi[i] * int(i == j == k) for i in range(3)
            )
            require(target == (xi[j] if j == k else 0))
        checked += 1

    # Audit the other full contraction with two actual right kernels.
    d = [[0, 1, 0], [0, -1, 0], [2, 0, -1]]
    dp = [[0, 1, 0], [0, -1, 0], [3, 0, -1]]
    eta = [1, 0, 2]
    etap = [1, 0, 3]
    require(matvec(d, eta) == [0, 0, 0])
    require(matvec(dp, etap) == [0, 0, 0])
    for i in range(3):
        for k in range(3):
            require(sum(d[i][j] * eta[j] * etap[k]
                        for j in range(3)) == 0)
        for j in range(3):
            require(sum(dp[i][k] * eta[j] * etap[k]
                        for k in range(3)) == 0)
        target = sum(
            eta[j] * etap[k] * int(i == j == k)
            for j, k in product(range(3), repeat=2)
        )
        require(target == eta[i] * etap[i])
    return checked


def check_coordinate_boundary_ledger():
    lines = {
        "e": (1, 0),
        "b": (0, 1),
        "full": (1, 1),
    }
    expected = {
        ("full", "full"): {0, 1},
        ("e", "full"): {0},
        ("full", "e"): {0},
        ("b", "full"): {1},
        ("full", "b"): {1},
        ("e", "e"): {0},
        ("b", "b"): {1},
        ("e", "b"): set(),
        ("b", "e"): set(),
    }
    for names, support in expected.items():
        left, right = (lines[name] for name in names)
        actual = {i for i in range(2) if left[i] * right[i]}
        require(actual == support)
    return len(expected)


def check_selector_conic():
    # Work in a formal basis yee, yea, yae, yaa.
    yee = {(0,): 1}
    yea = {(1,): 1}
    yae = {(2,): 1}
    yaa = {(3,): 1}
    tested = 0
    for A, B, C, D in product(range(-2, 3), repeat=4):
        delta = A * D - B * C
        if not delta:
            continue

        rho0 = poly_add(poly_scale(yea, A), poly_scale(yee, -B))
        rho1 = {}
        for term in (
            poly_scale(yea, C),
            poly_scale(yee, -D),
            poly_scale(yae, -B),
            poly_scale(yaa, A),
        ):
            rho1 = poly_add(rho1, term)
        rho2 = poly_add(poly_scale(yaa, C), poly_scale(yae, -D))

        lhs = {}
        for scalar, rho in ((-C * D, rho0), (B * C, rho1),
                            (-A * B, rho2)):
            lhs = poly_add(lhs, poly_scale(rho, scalar))
        rhs = poly_scale(poly_add(poly_scale(yae, B),
                                  poly_scale(yea, -C)), delta)
        require(lhs == rhs)

        # The chosen v makes u^T T v the zero polynomial.
        # Coefficients in r^2, rs, s^2 are checked separately.
        isotropy = (
            A * (-B) + B * A,
            A * (-D) + B * C + C * (-B) + D * A,
            C * (-D) + D * C,
        )
        require(isotropy == (0, 0, 0))

        e_response, a_response = response_polynomials(A, B, C, D)
        require(e_response == (-2 * B, -2 * D, 0))
        require(a_response == (0, 3 * A, 3 * C))

        # In the invertible case the response forms have a common linear
        # factor exactly on the triangular boundary B*C=0, including
        # the A=0 and D=0 coordinate-factor specializations.
        left_factors = ((1, 0), (B, D))
        right_factors = ((0, 1), (A, C))
        common_factor = any(
            proportional(left, right)
            for left in left_factors for right in right_factors
        )
        require(common_factor == (B * C == 0))
        tested += 1
    require(tested > 100)
    return tested


def check_intersection_classification():
    """Exhaust (28)-(29) over the 28 subspaces of F3^3."""
    p = 3
    vectors = list(product(range(p), repeat=3))

    def span(generators):
        if not generators:
            return frozenset({(0, 0, 0)})
        return frozenset(
            tuple(
                sum(coefficients[k] * generators[k][i]
                    for k in range(len(generators))) % p
                for i in range(3)
            )
            for coefficients in product(range(p), repeat=len(generators))
        )

    subspaces = {span(())}
    subspaces.update(span((u,)) for u in vectors if any(u))
    subspaces.update(
        span((u, v))
        for u in vectors if any(u)
        for v in vectors if any(v)
    )
    subspaces.add(span(((1, 0, 0), (0, 1, 0), (0, 0, 1))))
    require(len(subspaces) == 28)

    checked = 0
    for u in product(range(p), repeat=3):
        if not any(u):
            continue
        for image in subspaces:
            if not all(
                sum(u[i] * j_matrix(label, p)[i][j] * v[j]
                    for i in range(3) for j in range(3)) % p == 0
                for label in (0, 1)
                for v in image
            ):
                continue
            r = {1: 0, 3: 1, 9: 2, 27: 3}[len(image)]
            require(r <= 2)
            if r == 2:
                # im S equals span(e0,e1), and u lies in that plane.
                require(u[2] == 0)
                require(all(v[2] == 0 for v in image))
            checked += 1
    require(checked > 0)
    return checked


def check_curvature_guard():
    J0 = j_matrix(0)
    P = [[1, 0, 0], [1, -1, 0], [0, 0, 1]]
    xi = [1, 1, 0]

    def S(u):
        return [[1, 0, 0], [-u, 0, 1], [0, 1, 0]]

    def d(u):
        return matmul(matmul(transpose(P), J0), S(u))

    for u in (1, 2):
        direct = d(u)
        require(direct == [[0, 1, 0], [0, -1, 0], [u, 0, -1]])
        require(rank_mod(direct, 101) == 2)
        require(matvec(transpose(direct), xi) == [0, 0, 0])
        require(matvec(direct, [1, 0, u]) == [0, 0, 0])
        require(matvec(P, xi) == [1, 0, 0])
        require(matvec(S(u), [1, 0, u]) == [1, 0, 0])
        require(det3(P) and det3(S(u)))

    T = [[1, 1, 0], [1, 2, 0], [0, 0, 1]]
    require(det3(T) == 1)
    require(T[0][0] * T[1][1] - T[0][1] * T[1][0] == 1)
    A = d(1)[0][1]
    B0 = d(2)[0][1]
    U10, F10 = 1, 0
    require(A == B0 == 1)
    require(A * U10 - B0 * F10 == 1)
    return 2


def main():
    contractions = check_kernel_contractions()
    boundaries = check_coordinate_boundary_ledger()
    conics = check_selector_conic()
    intersections = check_intersection_classification()
    guards = check_curvature_guard()
    print("target-centred cross odd-overlap descent: PASS")
    print(f"  common-kernel contraction samples: {contractions}")
    print(f"  right-kernel boundary cases: {boundaries}")
    print(f"  invertible selector blocks: {conics}")
    print(f"  F3 intersection incidences: {intersections}")
    print(f"  physical alignment guards: {guards}")


if __name__ == "__main__":
    main()
