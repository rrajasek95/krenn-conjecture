#!/usr/bin/env python3
"""Exact audit of the complementary-kernel colon single-row guard.

All calculations take place over Q in the commutative square-zero algebra

    Q[u0,...,u4]/(u0^2,...,u4^2).

The guard satisfies both target-centred kernel contraction tables and 26 of
the 27 uncontracted overlap rows.  Its only uncontracted residual is the
(b,e,a) row, while the weighted selector quadratic is a nonzero, sharp
colon element.
"""

from fractions import Fraction
from itertools import product


if not __debug__:
    raise SystemExit("run without -O: this checker uses assertions")


Q = Fraction
LABELS = range(3)
TOP_MASK = (1 << 5) - 1


def add(left, right):
    out = dict(left)
    for mask, value in right.items():
        out[mask] = out.get(mask, Q(0)) + value
        if out[mask] == 0:
            del out[mask]
    return out


def scale(poly, scalar):
    scalar = Q(scalar)
    return {
        mask: scalar * value
        for mask, value in poly.items()
        if scalar * value
    }


def multiply(left, right):
    out = {}
    for first, a in left.items():
        for second, b in right.items():
            if first & second:
                continue
            mask = first | second
            out[mask] = out.get(mask, Q(0)) + a * b
    return {mask: value for mask, value in out.items() if value}


def sum_polys(polys):
    out = {}
    for poly in polys:
        out = add(out, poly)
    return out


def variable(site):
    return {1 << site: Q(1)}


def linear(coefficients, variables):
    return sum_polys(
        scale(variables[site], coefficient)
        for site, coefficient in enumerate(coefficients)
    )


def top_coefficient(*factors):
    value = {0: Q(1)}
    for factor in factors:
        value = multiply(value, factor)
    return value.get(TOP_MASK, Q(0))


def linear_coefficient(form, site):
    return form.get(1 << site, Q(0))


def vector_combination(coefficients, forms):
    return sum_polys(
        scale(form, coefficient)
        for coefficient, form in zip(coefficients, forms)
    )


def matrix_vector(matrix, vector):
    return [
        sum(Q(matrix[i][j]) * Q(vector[j]) for j in LABELS)
        for i in LABELS
    ]


def left_vector_matrix(vector, matrix):
    return [
        sum(Q(vector[i]) * Q(matrix[i][j]) for i in LABELS)
        for j in LABELS
    ]


def matrix_rank(matrix):
    work = [[Q(value) for value in row] for row in matrix]
    row = 0
    for column in range(len(work[0])):
        pivot = next(
            (index for index in range(row, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        inverse = Q(1) / work[row][column]
        work[row] = [inverse * value for value in work[row]]
        for index in range(len(work)):
            if index == row or not work[index][column]:
                continue
            scalar = work[index][column]
            work[index] = [
                work[index][j] - scalar * work[row][j]
                for j in range(len(work[0]))
            ]
        row += 1
        if row == len(work):
            break
    return row


def guard_data():
    u = [variable(site) for site in range(5)]
    omega_top = {TOP_MASK: Q(1)}

    z = add(multiply(u[1], u[3]), multiply(u[2], u[4]))
    z_divided_2 = scale(multiply(z, z), Q(1, 2))

    x = [
        linear((0, 0, 0, 0, -1), u),
        linear((1, 0, 0, 0, 1), u),
        linear((0, 0, 0, -1, 0), u),
    ]
    y = [
        linear((1, 0, 1, 0, 0), u),
        linear((0, -1, 0, 0, 0), u),
        linear((0, 1, 1, -1, 0), u),
    ]
    t = [
        linear((0, 0, -1, 1, 1), u),
        linear((0, 0, 0, 0, 1), u),
        linear((-1, -1, -1, 1, 0), u),
    ]

    P = (
        (-1, 0, 1),
        (1, 0, -1),
        (1, -1, -1),
    )
    R = (
        (3, 0, -3),
        (-3, 0, 3),
        (0, -1, 0),
    )
    T = (
        (3, -1, 0),
        (1, -1, 1),
        (-2, -1, -2),
    )

    xi = (1, 1, 0)
    eta = (1, 0, 1)
    eta_prime = (1, 0, 1)
    target_scalars = (4, -1, 2)
    targets = [scale(omega_top, scalar) for scalar in target_scalars]

    return {
        "u": u,
        "top": omega_top,
        "z": z,
        "z_divided_2": z_divided_2,
        "x": x,
        "y": y,
        "t": t,
        "P": P,
        "R": R,
        "T": T,
        "xi": xi,
        "eta": eta,
        "eta_prime": eta_prime,
        "target_scalars": target_scalars,
        "targets": targets,
    }


def check_kernels_and_curvature(data):
    P = data["P"]
    R = data["R"]
    T = data["T"]
    xi = data["xi"]
    eta = data["eta"]
    eta_prime = data["eta_prime"]

    assert left_vector_matrix(xi, P) == [0, 0, 0]
    assert left_vector_matrix(xi, R) == [0, 0, 0]
    assert matrix_vector(P, eta) == [0, 0, 0]
    assert matrix_vector(R, eta_prime) == [0, 0, 0]
    assert matrix_rank(P) == matrix_rank(R) == 2

    # The completed {e,a} selector square is genuinely generic here.
    B = T[0][1]
    C = T[1][0]
    determinant = T[0][0] * T[1][1] - B * C
    assert (B, C, determinant) == (-1, 1, -2)

    # At the literal site u4, A=P_{be}, B_selected=R_{ba},
    # F=[u4]y_e, and U=[u4]t_a.
    selected_A = P[2][0]
    selected_B = R[2][1]
    selected_F = linear_coefficient(data["y"][0], 4)
    selected_U = linear_coefficient(data["t"][1], 4)
    curvature = selected_A * selected_U - selected_B * selected_F
    assert (selected_A, selected_B, curvature) == (1, -1, 1)
    return curvature


def full_row_residual(data, i, j, k):
    P = data["P"]
    R = data["R"]
    T = data["T"]
    x = data["x"]
    y = data["y"]
    t = data["t"]
    z = data["z"]
    z_divided_2 = data["z_divided_2"]
    targets = data["targets"]

    direct = sum_polys(
        (
            scale(t[k], P[i][j]),
            scale(y[j], R[i][k]),
            scale(x[i], T[j][k]),
        )
    )
    left = add(
        multiply(direct, z_divided_2),
        multiply(multiply(multiply(x[i], y[j]), t[k]), z),
    )
    right = targets[i] if i == j == k else {}
    return add(left, scale(right, -1))


def check_twenty_six_rows(data):
    residuals = {
        (i, j, k): full_row_residual(data, i, j, k)
        for i, j, k in product(LABELS, repeat=3)
        if full_row_residual(data, i, j, k)
    }
    assert residuals == {(2, 0, 1): scale(data["top"], -1)}

    xi = data["xi"]
    eta = data["eta"]
    eta_prime = data["eta_prime"]

    # The unique residual is invisible to both contraction tensors.
    for j, k in product(LABELS, repeat=2):
        contracted = sum_polys(
            scale(full_row_residual(data, i, j, k), xi[i])
            for i in LABELS
        )
        assert not contracted
    for i in LABELS:
        contracted = sum_polys(
            scale(
                full_row_residual(data, i, j, k),
                eta[j] * eta_prime[k],
            )
            for j, k in product(LABELS, repeat=2)
        )
        assert not contracted
    return residuals


def check_literal_contractions(data):
    x = data["x"]
    y = data["y"]
    t = data["t"]
    z = data["z"]
    T = data["T"]
    xi = data["xi"]
    eta = data["eta"]
    eta_prime = data["eta_prime"]
    targets = data["targets"]

    L = vector_combination(xi, x)
    assert L == data["u"][0]

    for j, k in product(LABELS, repeat=2):
        normalized = add(
            multiply(y[j], t[k]),
            scale(z, Q(T[j][k], 2)),
        )
        left = multiply(multiply(L, normalized), z)
        right = scale(targets[j], xi[j]) if j == k else {}
        assert left == right

    y_eta = vector_combination(eta, y)
    t_eta_prime = vector_combination(eta_prime, t)
    tau = sum(
        Q(eta[j]) * Q(T[j][k]) * Q(eta_prime[k])
        for j, k in product(LABELS, repeat=2)
    )
    assert tau == -1
    right_kernel_quadratic = add(
        multiply(y_eta, t_eta_prime),
        scale(z, tau / 2),
    )
    for i in LABELS:
        left = multiply(multiply(x[i], right_kernel_quadratic), z)
        right = scale(targets[i], eta[i] * eta_prime[i])
        assert left == right

    # The two packets share exactly their e-anchor contraction.
    shared_left = multiply(multiply(L, right_kernel_quadratic), z)
    shared_right = scale(targets[0], xi[0] * eta[0] * eta_prime[0])
    assert shared_left == shared_right


def check_sharp_colon_and_missing_row(data):
    y = data["y"]
    t = data["t"]
    x = data["x"]
    z = data["z"]
    T = data["T"]
    xi = data["xi"]

    B = T[0][1]
    C = T[1][0]
    omega = add(
        scale(multiply(y[0], t[1]), C),
        scale(multiply(y[1], t[0]), -B),
    )
    L = vector_combination(xi, x)

    assert omega
    assert multiply(omega, z)  # The colon class is not merely in Ann(z).
    assert not multiply(multiply(L, omega), z)

    row_bea = full_row_residual(data, 2, 0, 1)
    row_bae = full_row_residual(data, 2, 1, 0)
    assert row_bea == scale(data["top"], -1)
    assert not row_bae

    # This is the full-source weighted row whose quadratic term is
    # x_b * omega * z; it fails by exactly the omitted (b,e,a) residual.
    weighted_residual = add(scale(row_bea, C), scale(row_bae, -B))
    assert weighted_residual == scale(data["top"], -1)

    P = data["P"]
    R = data["R"]
    z_divided_2 = data["z_divided_2"]
    companion = sum_polys(
        (
            scale(t[1], C * P[2][0]),
            scale(y[0], C * R[2][1]),
            scale(t[0], -B * P[2][1]),
            scale(y[1], -B * R[2][0]),
        )
    )
    expanded_weighted_row = add(
        multiply(x[2], multiply(omega, z)),
        multiply(companion, z_divided_2),
    )
    assert expanded_weighted_row == weighted_residual
    return len(omega)


def check_no_forced_macaulay_dual():
    """A formal rootless decoration has full degree-five Macaulay rank."""
    # Rows are the three quadratic shifts of s^3 and then of t^3 in the
    # ordered basis s^5,s^4t,...,t^5.
    rows = [
        [1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
    ]
    assert matrix_rank(rows) == 6
    return 6 - matrix_rank(rows)


def main():
    data = guard_data()
    curvature = check_kernels_and_curvature(data)
    residuals = check_twenty_six_rows(data)
    check_literal_contractions(data)
    colon_terms = check_sharp_colon_and_missing_row(data)
    macaulay_nullity = check_no_forced_macaulay_dual()

    print("complementary-kernel colon single-row guard: PASS")
    print(f"  uncontracted rows holding: {27 - len(residuals)}/27")
    print(f"  sole residual row: {next(iter(residuals))}")
    print(f"  selected curvature: {curvature}")
    print(f"  nonzero colon terms: {colon_terms}")
    print(f"  formal rootless Macaulay dual nullity: {macaulay_nullity}")


if __name__ == "__main__":
    main()
