#!/usr/bin/env python3
"""Exact audit of the full-27 colon-cycle guard.

The calculations use only ``fractions.Fraction`` and the square-zero
algebra Q[u_0,...,u_{2h-2}]/(u_i^2).  The base packet has all 27 literal
rows, rank-two direct blocks, normalized diagonal targets, and a nonzero
selector colon class.  Tensoring by disjoint matching edges verifies the
same identities at several higher odd complements; the note proves the
uniform statement.
"""

from fractions import Fraction
from itertools import product


Q = Fraction
LABELS = range(3)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


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


def divided_power(poly, exponent):
    out = {0: Q(1)}
    for step in range(1, exponent + 1):
        out = scale(multiply(out, poly), Q(1, step))
    return out


def variable(site):
    return {1 << site: Q(1)}


def linear(coefficients, variables):
    return sum_polys(
        scale(variables[site], coefficient)
        for site, coefficient in enumerate(coefficients)
    )


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
        pivot_value = work[row][column]
        work[row] = [value / pivot_value for value in work[row]]
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


def coefficient(poly, site):
    return poly.get(1 << site, Q(0))


def packet(h):
    require(h >= 3, "the odd-complement packet starts at h=3")
    site_count = 2 * h - 1
    variables = [variable(site) for site in range(site_count)]
    u = variables

    z = sum_polys(
        (
            scale(multiply(u[1], u[2]), 4),
            multiply(u[1], u[3]),
            multiply(u[2], u[4]),
        )
    )
    for site in range(5, site_count, 2):
        z = add(z, multiply(u[site], u[site + 1]))

    x = [
        scale(u[4], Q(1, 8)),
        scale(add(u[0], u[4]), Q(-1, 3)),
        scale(u[3], Q(1, 2)),
    ]
    y = [
        add(u[0], u[2]),
        scale(u[1], -1),
        sum_polys((u[1], u[2], scale(u[3], -1))),
    ]
    t = [
        sum_polys((scale(u[2], -1), u[3], u[4])),
        u[4],
        sum_polys((scale(u[0], -1), scale(u[1], -1),
                   scale(u[2], -1), u[3])),
    ]

    P = (
        (Q(-3, 8), 0, Q(3, 8)),
        (1, 0, -1),
        (Q(3, 2), Q(1, 2), Q(-3, 2)),
    )
    R = (
        (Q(5, 8), 0, Q(-5, 8)),
        (Q(-5, 3), 0, Q(5, 3)),
        (-2, -2, 2),
    )
    T = (
        (-9, -1, 0),
        (1, -3, 1),
        (2, 3, -2),
    )
    xi = (-8, -3, 0)
    eta = (1, 0, 1)
    eta_prime = (1, 0, 1)
    top = {(1 << site_count) - 1: Q(1)}
    return {
        "h": h,
        "variables": variables,
        "z": z,
        "z_h_minus_1": divided_power(z, h - 1),
        "z_h_minus_2": divided_power(z, h - 2),
        "x": x,
        "y": y,
        "t": t,
        "P": P,
        "R": R,
        "T": T,
        "xi": xi,
        "eta": eta,
        "eta_prime": eta_prime,
        "targets": [top, top, top],
        "top": top,
    }


def row_residual(data, i, j, k):
    direct = sum_polys(
        (
            scale(data["t"][k], data["P"][i][j]),
            scale(data["y"][j], data["R"][i][k]),
            scale(data["x"][i], data["T"][j][k]),
        )
    )
    left = add(
        multiply(direct, data["z_h_minus_1"]),
        multiply(
            multiply(multiply(data["x"][i], data["y"][j]),
                     data["t"][k]),
            data["z_h_minus_2"],
        ),
    )
    right = data["targets"][i] if i == j == k else {}
    return add(left, scale(right, -1))


def check_linear_data(data):
    P, R, T = data["P"], data["R"], data["T"]
    xi, eta, eta_prime = data["xi"], data["eta"], data["eta_prime"]
    require(matrix_rank(P) == matrix_rank(R) == 2, "direct ranks")
    require(left_vector_matrix(xi, P) == [0, 0, 0], "left P kernel")
    require(left_vector_matrix(xi, R) == [0, 0, 0], "left R kernel")
    require(matrix_vector(P, eta) == [0, 0, 0], "right P kernel")
    require(matrix_vector(R, eta_prime) == [0, 0, 0], "right R kernel")
    require(data["targets"] == [data["top"], data["top"], data["top"]],
            "normalized targets are deliberately collinear in the scalar shadow")

    B, C = T[0][1], T[1][0]
    determinant = T[0][0] * T[1][1] - B * C
    require((B, C, determinant) == (-1, 1, 28), "generic T square")

    if data["h"] == 3:
        star_matrices = []
        for family in (data["x"], data["y"], data["t"]):
            star_matrices.append(
                [[coefficient(form, site) for site in range(5)]
                 for form in family]
            )
        require(all(matrix_rank(star) == 3 for star in star_matrices),
                "injective endpoint stars")

        selected_A = P[2][0]
        selected_B = R[2][1]
        selected_F = coefficient(data["y"][0], 4)
        selected_U = coefficient(data["t"][1], 4)
        curvature = selected_A * selected_U - selected_B * selected_F
        require(curvature == Q(3, 2), "selected literal curvature")


def check_all_rows(data):
    residuals = {
        (i, j, k): row_residual(data, i, j, k)
        for i, j, k in product(LABELS, repeat=3)
        if row_residual(data, i, j, k)
    }
    require(not residuals, f"nonzero full-row residuals: {residuals}")


def check_contractions(data):
    h = data["h"]
    x, y, t, z = data["x"], data["y"], data["t"], data["z"]
    T = data["T"]
    xi, eta, eta_prime = data["xi"], data["eta"], data["eta_prime"]
    L = vector_combination(xi, x)
    require(L == data["variables"][0], "L=u0")

    for j, k in product(LABELS, repeat=2):
        normalized = add(
            multiply(y[j], t[k]),
            scale(z, Q(T[j][k], h - 1)),
        )
        left = multiply(multiply(L, normalized), data["z_h_minus_2"])
        right = scale(data["targets"][j], xi[j]) if j == k else {}
        require(left == right, f"left contraction {(j, k)}")

    y_eta = vector_combination(eta, y)
    t_eta_prime = vector_combination(eta_prime, t)
    tau = sum(
        Q(eta[j]) * Q(T[j][k]) * Q(eta_prime[k])
        for j, k in product(LABELS, repeat=2)
    )
    require(tau == -9, "right contraction radial coefficient")
    normalized = add(multiply(y_eta, t_eta_prime), scale(z, Q(tau, h - 1)))
    for i in LABELS:
        left = multiply(multiply(x[i], normalized), data["z_h_minus_2"])
        right = scale(data["targets"][i], eta[i] * eta_prime[i])
        require(left == right, f"right contraction {i}")


def check_colon_cycle(data):
    h = data["h"]
    x, y, t = data["x"], data["y"], data["t"]
    P, R, T = data["P"], data["R"], data["T"]
    B, C = T[0][1], T[1][0]
    omega = add(
        scale(multiply(y[0], t[1]), C),
        scale(multiply(y[1], t[0]), -B),
    )
    L = vector_combination(data["xi"], x)
    suspended_omega = multiply(omega, data["z_h_minus_2"])
    require(omega, "nonzero omega")
    require(suspended_omega, "omega is not killed by the radial power")
    require(not multiply(L, suspended_omega), "omega is in the sharp colon")

    companion = sum_polys(
        (
            scale(t[1], C * P[2][0]),
            scale(y[0], C * R[2][1]),
            scale(t[0], -B * P[2][1]),
            scale(y[1], -B * R[2][0]),
        )
    )
    omega_term = multiply(x[2], suspended_omega)
    companion_term = multiply(companion, data["z_h_minus_1"])
    require(omega_term, "the colon summand in the weighted cycle is nonzero")
    require(companion_term, "the direct-star companion summand is nonzero")
    weighted_cycle = add(omega_term, companion_term)
    require(not weighted_cycle, "restored weighted row is a source cycle")

    weighted_residual = add(
        scale(row_residual(data, 2, 0, 1), C),
        scale(row_residual(data, 2, 1, 0), -B),
    )
    require(not weighted_residual, "literal weighted residual")

    if h == 3:
        u = data["variables"]
        expected_omega_z = add(
            scale(multiply(multiply(multiply(u[0], u[1]), u[2]), u[4]), 4),
            multiply(multiply(multiply(u[0], u[1]), u[3]), u[4]),
        )
        require(multiply(omega, data["z"]) == expected_omega_z,
                "displayed omega*z")
        expected_companion = sum_polys(
            (
                scale(u[0], -2), scale(u[1], 2),
                scale(u[2], Q(-5, 2)), scale(u[3], Q(1, 2)),
                scale(u[4], 2),
            )
        )
        require(companion == expected_companion, "displayed companion")


def check_selector_conic():
    data = packet(3)
    y, t, T = data["y"], data["t"], data["T"]
    A, B = T[0][0], T[0][1]
    C, D = T[1][0], T[1][1]
    determinant = A * D - B * C
    theta = (-D * C, B * C, -A * B)

    # y(s,t)t(v(s,t)) in the coefficient order s^2, st, t^2.
    coefficients = [
        add(scale(multiply(y[0], t[0]), -B),
            scale(multiply(y[0], t[1]), A)),
        sum_polys((
            scale(multiply(y[0], t[0]), -D),
            scale(multiply(y[0], t[1]), C),
            scale(multiply(y[1], t[0]), -B),
            scale(multiply(y[1], t[1]), A),
        )),
        add(scale(multiply(y[1], t[0]), -D),
            scale(multiply(y[1], t[1]), C)),
    ]
    theta_value = sum_polys(
        scale(coefficient_poly, theta[index])
        for index, coefficient_poly in enumerate(coefficients)
    )
    omega = add(
        scale(multiply(y[0], t[1]), C),
        scale(multiply(y[1], t[0]), -B),
    )
    require(theta_value == scale(omega, -determinant),
            "selector-conic third direction")

    target_e = (-B, -D, 0)
    target_a = (0, A, C)
    require(sum(theta[i] * target_e[i] for i in range(3)) == 0,
            "theta kills e anchor")
    require(sum(theta[i] * target_a[i] for i in range(3)) == 0,
            "theta kills a anchor")


def check_formal_macaulay_guard(max_h=10):
    for h in range(3, max_h + 1):
        # The shifts of s^h give columns 0,...,h-1; the shifts of t^h
        # give columns h,...,2h-1 in the degree-(2h-1) monomial basis.
        rows = []
        for column in range(2 * h):
            row = [Q(0)] * (2 * h)
            row[column] = Q(1)
            rows.append(row)
        require(matrix_rank(rows) == 2 * h,
                f"formal Macaulay rank at h={h}")


def main():
    for h in range(3, 9):
        data = packet(h)
        check_linear_data(data)
        check_all_rows(data)
        check_contractions(data)
        check_colon_cycle(data)
    check_selector_conic()
    check_formal_macaulay_guard()
    print("full-27 colon-cycle guard: PASS")
    print("  uniform packets checked: h=3,...,8")
    print("  literal rows holding per packet: 27/27")
    print("  direct ranks: (2,2); det T_{e,a}: 28")
    print("  normalized diagonal target coefficients: (1,1,1)")
    print("  selector colon class: nonzero and source-cycled")
    print("  formal rootless Macaulay ranks checked: 2h for h=3,...,10")


if __name__ == "__main__":
    main()
