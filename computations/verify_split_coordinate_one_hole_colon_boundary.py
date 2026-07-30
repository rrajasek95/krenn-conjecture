#!/usr/bin/env python3
"""Exact audit of the split-coordinate one-hole colon boundary.

The sharp guard is calculated over Q in the commutative site-square-zero
algebra on five scalar sites.  It satisfies 26 of the 27 uncontracted
overlap rows, both kernel-contracted packets, split literal zero columns,
rank-two direct blocks, injective restricted stars, and nonzero selected
curvature.  Its sole residual is the (b,e,a)=(2,0,1) row.  The normalized
(e,b) effective quadratic has a nonzero image in the common p-star
one-hole colon kernel.

This is a quotient/square-free guard, not a ternary GHZ source: its three
top targets are scalar multiples of one top monomial.
"""

from fractions import Fraction
from itertools import product


if not __debug__:
    raise SystemExit("run without -O: this checker uses assertions")


Q = Fraction
LABELS = range(3)
SITES = range(5)
TOP_MASK = (1 << 5) - 1
OMITTED_ROW = (2, 0, 1)


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
    u = [variable(site) for site in SITES]
    omega = {TOP_MASK: Q(1)}

    z = add(multiply(u[1], u[3]), multiply(u[2], u[4]))
    z_divided_2 = scale(multiply(z, z), Q(1, 2))

    x = [
        linear((0, 1, -1, 0, 0), u),
        linear((1, 0, -1, 1, 0), u),
        linear((0, -1, 0, 0, -1), u),
    ]
    y = [
        linear((-1, 0, 0, -1, 0), u),
        linear((0, 0, 0, 1, -1), u),
        linear((0, 0, 0, 1, 0), u),
    ]
    t = [
        linear((0, 0, 1, 0, 0), u),
        linear((0, -1, 0, -1, 0), u),
        linear((1, 0, -1, 0, 1), u),
    ]

    d = (
        (0, -2, -1),
        (0, 2, 1),
        (0, 1, 0),
    )
    d_prime = (
        (1, 1, 0),
        (-1, -1, 0),
        (1, -2, 0),
    )
    T = (
        (-1, -3, -1),
        (1, 0, -4),
        (0, 1, -1),
    )

    xi = (1, 1, 0)
    eta = (1, 0, 0)
    eta_prime = (0, 0, 1)
    targets = [scale(omega, -1) for _ in LABELS]

    return {
        "u": u,
        "omega": omega,
        "z": z,
        "z_divided_2": z_divided_2,
        "x": x,
        "y": y,
        "t": t,
        "d": d,
        "d_prime": d_prime,
        "T": T,
        "xi": xi,
        "eta": eta,
        "eta_prime": eta_prime,
        "targets": targets,
    }


def full_row_residual(data, i, j, k):
    d = data["d"]
    d_prime = data["d_prime"]
    T = data["T"]
    x = data["x"]
    y = data["y"]
    t = data["t"]
    z = data["z"]
    z_divided_2 = data["z_divided_2"]

    direct = sum_polys(
        (
            scale(t[k], d[i][j]),
            scale(y[j], d_prime[i][k]),
            scale(x[i], T[j][k]),
        )
    )
    left = add(
        multiply(direct, z_divided_2),
        multiply(multiply(multiply(x[i], y[j]), t[k]), z),
    )
    right = data["targets"][i] if i == j == k else {}
    return add(left, scale(right, -1))


def effective_quadratic(data, j, k):
    return add(
        multiply(data["y"][j], data["t"][k]),
        scale(data["z"], Q(data["T"][j][k], 2)),
    )


def check_direct_blocks_and_stars(data):
    d = data["d"]
    d_prime = data["d_prime"]
    xi = data["xi"]
    eta = data["eta"]
    eta_prime = data["eta_prime"]

    assert left_vector_matrix(xi, d) == [0, 0, 0]
    assert left_vector_matrix(xi, d_prime) == [0, 0, 0]
    assert matrix_vector(d, eta) == [0, 0, 0]
    assert matrix_vector(d_prime, eta_prime) == [0, 0, 0]
    assert matrix_rank(d) == matrix_rank(d_prime) == 2

    assert all(d[i][0] == 0 for i in LABELS)
    assert all(d_prime[i][2] == 0 for i in LABELS)
    assert not any(all(value == 0 for value in row) for row in d)
    assert not any(all(value == 0 for value in row) for row in d_prime)
    assert not any(
        all(d[i][j] == d_prime[i][j] == 0 for i in LABELS)
        for j in LABELS
    )

    # The restricted triples already have full row rank, hence adjoining
    # the cross endpoint components leaves all four full endpoint stars
    # injective.
    for forms in (data["x"], data["y"], data["t"]):
        coefficients = [
            [form.get(1 << site, Q(0)) for site in SITES]
            for form in forms
        ]
        assert matrix_rank(coefficients) == 3

    # The {e,a} compression is in the generic crossed-square stratum.
    T = data["T"]
    determinant = T[0][0] * T[1][1] - T[0][1] * T[1][0]
    assert (T[0][1], T[1][0], determinant) == (-3, 1, 3)


def check_rows_and_contractions(data):
    residuals = {
        (i, j, k): full_row_residual(data, i, j, k)
        for i, j, k in product(LABELS, repeat=3)
        if full_row_residual(data, i, j, k)
    }
    assert residuals == {OMITTED_ROW: data["omega"]}

    xi = data["xi"]
    eta = data["eta"]
    eta_prime = data["eta_prime"]

    # The omitted row is invisible to both contractions.
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

    L = vector_combination(xi, data["x"])
    for j, k in product(LABELS, repeat=2):
        C_jk = multiply(effective_quadratic(data, j, k), data["z"])
        left = multiply(L, C_jk)
        right = scale(data["targets"][j], xi[j]) if j == k else {}
        assert left == right

    Q_eb = effective_quadratic(data, 0, 2)
    C_eb = multiply(Q_eb, data["z"])
    assert Q_eb
    assert C_eb
    for form in data["x"]:
        assert not multiply(form, C_eb)

    expected_C = sum_polys(
        (
            multiply(
                multiply(multiply(data["u"][0], data["u"][1]), data["u"][2]),
                data["u"][3],
            ),
            scale(multiply(multiply(multiply(data["u"][0], data["u"][1]), data["u"][3]), data["u"][4]), -1),
            scale(multiply(multiply(multiply(data["u"][0], data["u"][2]), data["u"][3]), data["u"][4]), -1),
            scale(multiply(multiply(multiply(data["u"][1], data["u"][2]), data["u"][3]), data["u"][4]), -1),
        )
    )
    assert C_eb == expected_C
    return residuals, len(C_eb)


def check_curvature(data):
    # Exact endpoint order: A=d_{0,1}, B=d'_{0,0}, while the fourth-site
    # entries at site 2 are F=(y_1)_2 and U=(t_0)_2.
    A = data["d"][0][1]
    B = data["d_prime"][0][0]
    F = data["y"][1].get(1 << 2, Q(0))
    U = data["t"][0].get(1 << 2, Q(0))
    curvature = A * U - B * F
    assert (A, B, F, U, curvature) == (-2, 1, 0, 1, -2)
    return curvature


def check_formal_macaulay_rank():
    # The three quadratic shifts of s^3 and t^3 fill all six quintics.
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
    check_direct_blocks_and_stars(data)
    residuals, colon_terms = check_rows_and_contractions(data)
    curvature = check_curvature(data)
    macaulay_nullity = check_formal_macaulay_rank()

    print("split-coordinate one-hole colon boundary: PASS")
    print(f"  uncontracted rows holding: {27 - len(residuals)}/27")
    print(f"  sole residual row: {next(iter(residuals))}")
    print(f"  nonzero colon quartic terms: {colon_terms}")
    print(f"  selected curvature: {curvature}")
    print(f"  formal rootless Macaulay dual nullity: {macaulay_nullity}")


if __name__ == "__main__":
    main()
