#!/usr/bin/env python3
"""Lightweight exact checks for the augmented E2 clean-cap polynomial.

Only the Python standard library is used.  A six-site square-free
commutative algebra supplies one generic t=3 test; small Fraction-valued
polynomial routines audit the active-root saturation examples.
"""

from fractions import Fraction as Q
from math import factorial


N = 6
FULL = (1 << N) - 1


def add(*xs):
    out = {}
    for x in xs:
        for support, value in x.items():
            out[support] = out.get(support, Q(0)) + value
            if out[support] == 0:
                del out[support]
    return out


def scale(a, x):
    if a == 0:
        return {}
    return {support: a * value for support, value in x.items()}


def mul(x, y):
    out = {}
    for left, a in x.items():
        for right, b in y.items():
            if left & right:
                continue
            support = left | right
            out[support] = out.get(support, Q(0)) + a * b
    return {support: value for support, value in out.items() if value}


def power(x, degree):
    out = {0: Q(1)}
    for _ in range(degree):
        out = mul(out, x)
    return out


def divided_power(x, degree):
    return scale(Q(1, factorial(degree)), power(x, degree))


def edge_quadratic(values):
    out = {}
    cursor = iter(values)
    for i in range(N):
        for j in range(i + 1, N):
            out[(1 << i) | (1 << j)] = Q(next(cursor))
    return out


def gamma(q, beta):
    out = {}
    for support, value in q.items():
        sites = [i for i in range(N) if support & (1 << i)]
        assert len(sites) == 2
        out[support] = (beta[sites[0]] + beta[sites[1]]) * value
    return {support: value for support, value in out.items() if value}


def top(x):
    value = x.get(FULL, Q(0))
    return {} if value == 0 else {FULL: value}


def clean_error(q, s, r, t):
    terms = []
    for j in range(2, t + 1):
        term = mul(divided_power(r, j), divided_power(q, t - j))
        terms.append(scale(s ** (t - j), term))
    return top(add(*terms))


def coefficient_error(F0, C, T0, s0, sigma, t, j):
    first = mul(divided_power(C, j), divided_power(F0, t - j))
    if j == t:
        return top(first)
    scalar = -Q(comb(t - 1, j)) * s0 ** (t - 1 - j) * (-sigma) ** j
    return top(add(first, scale(scalar, T0)))


def comb(n, k):
    if k < 0 or k > n:
        return 0
    return factorial(n) // (factorial(k) * factorial(n - k))


def eval_vector_polynomial(coefficients, z):
    return add(*(scale(z**j, value) for j, value in enumerate(coefficients)))


def trim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p


def poly_divmod(a, b):
    a = trim(a)
    b = trim(b)
    assert b
    if len(a) < len(b):
        return [], a
    quotient = [Q(0)] * (len(a) - len(b) + 1)
    while len(a) >= len(b):
        degree = len(a) - len(b)
        coefficient = a[-1] / b[-1]
        quotient[degree] = coefficient
        for j, value in enumerate(b):
            a[degree + j] -= coefficient * value
        a = trim(a)
    return trim(quotient), a


def poly_gcd(a, b):
    a, b = trim(a), trim(b)
    while b:
        _, remainder = poly_divmod(a, b)
        a, b = b, remainder
    if not a:
        return []
    return [value / a[-1] for value in a]


def remove_activity_factors(poly, activity):
    poly = trim(poly)
    activity = trim(activity)
    if not activity:
        raise ValueError("an identically zero activity polynomial has no active locus")
    if len(activity) == 1:
        return poly
    while poly:
        quotient, remainder = poly_divmod(poly, activity)
        if remainder:
            break
        poly = quotient
    return trim(poly)


def main():
    t = 3
    q = edge_quadratic([1, -2, 3, 4, -1, 2, 5, -3, 1, 2, -4, 3, 1, 2, -2])
    r0 = edge_quadratic([2, 1, -1, 3, -2, 4, -3, 2, 5, -1, 1, 3, -2, 4, 1])
    beta = [Q(2), Q(-1), Q(3), Q(0), Q(-2), Q(1)]
    sigma = sum(beta, Q(0))
    s0 = Q(7)

    gamma_beta = gamma(q, beta)
    centered = [value - sigma / 2 for value in beta]
    C = add(gamma_beta, scale(-sigma, q))
    assert C == gamma(q, centered)

    gauge_left = top(mul(gamma_beta, divided_power(q, t - 1)))
    gauge_right = top(scale(sigma, divided_power(q, t)))
    assert gauge_left == gauge_right

    F0 = add(scale(s0, q), r0)
    T0 = top(add(scale(s0, divided_power(q, t)), mul(r0, divided_power(q, t - 1))))
    coefficients = [
        coefficient_error(F0, C, T0, s0, sigma, t, j)
        for j in range(t + 1)
    ]
    explicit_t3 = [
        top(add(divided_power(F0, 3), scale(-(s0**2), T0))),
        top(add(mul(C, divided_power(F0, 2)), scale(2 * s0 * sigma, T0))),
        top(add(mul(divided_power(C, 2), F0), scale(-(sigma**2), T0))),
        top(divided_power(C, 3)),
    ]
    assert coefficients == explicit_t3

    for z in [Q(-3), Q(-1, 2), Q(0), Q(2), Q(5, 3)]:
        s = s0 - z * sigma
        r = add(r0, scale(z, gamma_beta))
        F = add(scale(s, q), r)

        pair_left = top(add(scale(s, divided_power(q, t)), mul(r, divided_power(q, t - 1))))
        assert pair_left == T0

        direct = clean_error(q, s, r, t)
        closed = top(add(divided_power(F, t), scale(-(s ** (t - 1)), T0)))
        normal = top(
            add(
                divided_power(add(F0, scale(z, C)), t),
                scale(-((s0 - z * sigma) ** (t - 1)), T0),
            )
        )
        polarized = eval_vector_polynomial(coefficients, z)
        assert direct == closed == normal == polarized

    pure_direct = clean_error(q, -sigma, gamma_beta, t)
    assert pure_direct == top(divided_power(C, t))

    # gcd(z^2-1, (z^2-1)(z+2)) has active roots when activity is constant.
    p1 = [Q(-1), Q(0), Q(1)]
    p2 = [Q(-2), Q(-1), Q(2), Q(1)]
    assert poly_gcd(p1, p2) == p1
    assert remove_activity_factors(p1, [Q(7)]) == p1
    try:
        remove_activity_factors(p1, [])
    except ValueError:
        pass
    else:
        raise AssertionError("zero activity polynomial must be rejected")

    # With s0=2 and sigma=1, 2-z is the activity factor.
    activity = [Q(2), Q(-1)]
    inactive_only = power_poly(activity, 3)
    assert len(remove_activity_factors(inactive_only, activity)) == 1

    active_factor = [Q(1), Q(1)]  # z+1
    mixed = multiply_poly(power_poly(activity, 2), active_factor)
    residual = remove_activity_factors(mixed, activity)
    assert residual == active_factor
    assert len(residual) > 1

    # Guard the scope of the one-error-line corollary.  Merely having a
    # parameter z does not force a vector zero: (z, z-1) has gcd one.
    unrelated_components = [[Q(0), Q(1)], [Q(-1), Q(1)]]
    common = poly_gcd(*unrelated_components)
    assert common == [Q(1)]
    assert len(remove_activity_factors(common, activity)) == 1

    print("verified augmented E2 affine normal form and active-root criterion")


def multiply_poly(a, b):
    out = [Q(0)] * (len(a) + len(b) - 1)
    for i, left in enumerate(a):
        for j, right in enumerate(b):
            out[i + j] += left * right
    return trim(out)


def power_poly(poly, degree):
    out = [Q(1)]
    for _ in range(degree):
        out = multiply_poly(out, poly)
    return out


if __name__ == "__main__":
    main()
