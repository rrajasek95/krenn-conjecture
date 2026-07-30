#!/usr/bin/env python3
"""Exact checks for the shared-kernel odd five-site normal form."""

from fractions import Fraction
from itertools import product


if not __debug__:
    raise SystemExit("run without -O: this checker uses assertions")


def rank_mod(rows, p):
    matrix = [[entry % p for entry in row] for row in rows]
    row = 0
    for col in range(len(matrix[0])):
        pivot = next(
            (i for i in range(row, len(matrix)) if matrix[i][col] % p),
            None,
        )
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        inv = pow(matrix[row][col], -1, p)
        matrix[row] = [(inv * value) % p for value in matrix[row]]
        for i in range(len(matrix)):
            if i == row or not matrix[i][col] % p:
                continue
            scalar = matrix[i][col] % p
            matrix[i] = [
                (matrix[i][j] - scalar * matrix[row][j]) % p
                for j in range(len(matrix[0]))
            ]
        row += 1
        if row == len(matrix):
            break
    return row


def check_selector_quotient():
    """The generic Mat2/(Delta + C T) quotient is measured by omega_T."""
    p = 5
    checked = 0
    for A, B, C, D in product(range(p), repeat=4):
        if B == C == 0:
            continue
        diagonal_0 = [1, 0, 0, 0]
        diagonal_1 = [0, 0, 0, 1]
        direct = [A, B, C, D]
        omega = [0, C, -B % p, 0]
        assert rank_mod([diagonal_0, diagonal_1, direct], p) == 3
        assert sum(omega[i] * direct[i] for i in range(4)) % p == 0
        assert omega[0] == omega[3] == 0
        assert any(omega)
        checked += 1
    assert checked == p**4 - p**2
    return checked


def check_invertible_parametrization():
    """Audit the isotropic Segre and its missing quadratic direction."""
    checked = 0
    for A, B, C, D in product(range(-2, 3), repeat=4):
        determinant = A * D - B * C
        if determinant == 0 or (B == 0 and C == 0):
            continue

        theta = (-D * C, B * C, -A * B)
        assert any(theta)
        for s, t in ((1, 1), (1, 2), (-2, 1)):
            u = (s, t)
            v = (-(B * s + D * t), A * s + C * t)
            Tv = (A * v[0] + B * v[1], C * v[0] + D * v[1])
            assert u[0] * Tv[0] + u[1] * Tv[1] == 0

        target_e = (-B, -D, 0)
        target_a = (0, A, C)
        assert sum(theta[i] * target_e[i] for i in range(3)) == 0
        assert sum(theta[i] * target_a[i] for i in range(3)) == 0

        # Coefficients of y(u)t(v) in s^2, st, t^2.  The physical
        # product basis is Y_ee, Y_ea, Y_ae, Y_aa.
        square = [-B, A, 0, 0]
        mixed = [-D, C, -B, A]
        square_a = [0, 0, -D, C]
        contracted = [
            theta[0] * square[i]
            + theta[1] * mixed[i]
            + theta[2] * square_a[i]
            for i in range(4)
        ]
        expected = [0, -determinant * C, determinant * B, 0]
        assert contracted == expected
        checked += 1
    assert checked > 100
    return checked


def torus_zero(T):
    """Find a rational all-nonzero u,v with u^T T v=0, if present."""
    candidates = [Fraction(i) for i in range(-7, 8) if i]

    if not any(T[i][j] for i in range(2) for j in range(2)):
        return (Fraction(1), Fraction(1)), (Fraction(1), Fraction(1))

    first_column = (T[0][0], T[1][0])
    second_column = (T[0][1], T[1][1])
    if second_column == (0, 0):
        if all(first_column):
            r = -Fraction(first_column[0], first_column[1])
            assert r
            return (Fraction(1), r), (Fraction(1), Fraction(1))
        return None
    if first_column == (0, 0):
        if all(second_column):
            r = -Fraction(second_column[0], second_column[1])
            assert r
            return (Fraction(1), r), (Fraction(1), Fraction(1))
        return None

    # Put u=(1,r), v=(1,s), and solve the affine-linear equation for s.
    for r in candidates:
        constant = Fraction(T[0][0]) + r * T[1][0]
        coefficient = Fraction(T[0][1]) + r * T[1][1]
        if constant and coefficient:
            s = -constant / coefficient
            if s:
                return (Fraction(1), r), (Fraction(1), s)

    return None


def check_torus_criterion():
    checked = 0
    for flat in product(range(-2, 3), repeat=4):
        support = sum(value != 0 for value in flat)
        T = (flat[:2], flat[2:])
        witness = torus_zero(T)
        if support == 1:
            assert witness is None
        else:
            assert witness is not None
            u, v = witness
            assert all(u) and all(v)
            assert sum(
                u[i] * T[i][j] * v[j]
                for i in range(2)
                for j in range(2)
            ) == 0
        checked += 1
    return checked


def add(left, right):
    out = dict(left)
    for mask, value in right.items():
        out[mask] = out.get(mask, Fraction(0)) + value
        if out[mask] == 0:
            del out[mask]
    return out


def scale(poly, scalar):
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
            out[mask] = out.get(mask, Fraction(0)) + a * b
    return {mask: value for mask, value in out.items() if value}


def monomial(*sites):
    mask = sum(1 << site for site in sites)
    assert mask.bit_count() == len(sites)
    return {mask: Fraction(1)}


def check_nonzero_colon_guard():
    """A nonzero omega can be killed by Lz; cancellation is invalid."""
    L = monomial(0)
    z = add(monomial(1, 3), monomial(2, 4))
    Y_ea = scale(monomial(1, 3), Fraction(-1))
    Y_ae = scale(monomial(2, 4), Fraction(-1))
    half_z = scale(z, Fraction(1, 2))

    normalized_ea = add(Y_ea, half_z)
    normalized_ae = add(Y_ae, half_z)
    omega = add(Y_ea, scale(Y_ae, Fraction(-1)))

    assert normalized_ea and normalized_ae and omega
    assert not multiply(multiply(L, normalized_ea), z)
    assert not multiply(multiply(L, normalized_ae), z)
    assert not multiply(multiply(L, omega), z)
    assert multiply(L, z)
    return len(omega)


def main():
    quotient = check_selector_quotient()
    parametrizations = check_invertible_parametrization()
    torus = check_torus_criterion()
    colon_terms = check_nonzero_colon_guard()
    print("shared-kernel odd five-site Koszul normal form: PASS")
    print(f"  F5 generic selector quotients: {quotient}")
    print(f"  small invertible parametrizations: {parametrizations}")
    print(f"  small torus-support checks: {torus}")
    print(f"  nonzero colon-guard terms: {colon_terms}")


if __name__ == "__main__":
    main()
