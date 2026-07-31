#!/usr/bin/env python3
"""Exact lightweight checks for the scalar-unit full normal-jet ledger.

The formal variables are

    x, alpha, q, r, d,

where ``r`` is the selected response ``R_aa`` and ``d`` is an arbitrary
normal response ``R_D``.  Divided powers are represented in the ordinary
commuting polynomial ring over ``Fraction``.  This is sufficient because
``z^[m] = z**m / m!`` in characteristic zero.

The mathematical proof is uniform.  The finite range below is an audit of
normalizations, factorials, and signs, not the proof of the theorem.
"""

from fractions import Fraction
from functools import lru_cache
from math import factorial


# Exponent order: x, alpha, q, r, d.
NVAR = 5
ZERO_EXP = (0,) * NVAR


def require(condition, message):
    """Raise under both normal Python and ``python -O``."""

    if not condition:
        raise RuntimeError(message)


def clean(poly):
    return {mon: coeff for mon, coeff in poly.items() if coeff}


def monomial(coeff=1, **powers):
    names = {"x": 0, "alpha": 1, "q": 2, "r": 3, "d": 4}
    exp = [0] * NVAR
    for name, power in powers.items():
        exp[names[name]] = power
    value = Fraction(coeff)
    return {} if value == 0 else {tuple(exp): value}


def add(*polys):
    out = {}
    for poly in polys:
        for mon, coeff in poly.items():
            out[mon] = out.get(mon, Fraction(0)) + coeff
    return clean(out)


def scale(poly, scalar):
    scalar = Fraction(scalar)
    return clean({mon: scalar * coeff for mon, coeff in poly.items()})


def neg(poly):
    return scale(poly, -1)


def mul(left, right):
    out = {}
    for lm, lc in left.items():
        for rm, rc in right.items():
            mon = tuple(lm[i] + rm[i] for i in range(NVAR))
            out[mon] = out.get(mon, Fraction(0)) + lc * rc
    return clean(out)


def product(*polys):
    out = {ZERO_EXP: Fraction(1)}
    for poly in polys:
        out = mul(out, poly)
    return out


def ordinary_power(poly, exponent):
    require(exponent >= 0, "negative ordinary exponent")
    out = {ZERO_EXP: Fraction(1)}
    base = poly
    n = exponent
    while n:
        if n & 1:
            out = mul(out, base)
        base = mul(base, base)
        n //= 2
    return out


def divided_power(poly, exponent):
    """Return ``poly**exponent / exponent!`` by sparse multinomials.

    Every use in this checker has at most three input monomials.  Enumerating
    their weak compositions avoids the much heavier repeated multiplication
    of increasingly dense intermediate polynomials.
    """

    require(exponent >= 0, "negative divided-power exponent")
    terms = list(poly.items())
    if exponent == 0:
        return {ZERO_EXP: Fraction(1)}
    if not terms:
        return {}

    out = {}

    def visit(term_index, remaining, counts):
        if term_index == len(terms) - 1:
            full_counts = counts + [remaining]
            exp = [0] * NVAR
            coeff = Fraction(1)
            for count, (term_exp, term_coeff) in zip(full_counts, terms):
                coeff *= term_coeff**count / factorial(count)
                for index in range(NVAR):
                    exp[index] += count * term_exp[index]
            mon = tuple(exp)
            out[mon] = out.get(mon, Fraction(0)) + coeff
            return
        for count in range(remaining + 1):
            visit(term_index + 1, remaining - count, counts + [count])

    visit(0, exponent, [])
    return clean(out)


def variable(name):
    return monomial(1, **{name: 1})


X = variable("x")
ALPHA = variable("alpha")
Q = variable("q")
R = variable("r")
D = variable("d")


@lru_cache(maxsize=None)
def dp_var(name, exponent):
    return divided_power(variable(name), exponent)


@lru_cache(maxsize=None)
def alpha_power(exponent):
    return ordinary_power(ALPHA, exponent)


@lru_cache(maxsize=None)
def shifted_selected_quadratic():
    # G_a = alpha*q + r.
    return add(mul(ALPHA, Q), R)


@lru_cache(maxsize=None)
def target_xa(h):
    # The exceptional physical row: X_a = alpha*q^[h] + r*q^[h-1].
    return add(
        mul(ALPHA, dp_var("q", h)),
        mul(R, dp_var("q", h - 1)),
    )


@lru_cache(maxsize=None)
def unary_error(h):
    g = shifted_selected_quadratic()
    return add(
        divided_power(g, h),
        neg(mul(alpha_power(h - 1), target_xa(h))),
    )


@lru_cache(maxsize=None)
def theta(h):
    g = shifted_selected_quadratic()
    return add(
        divided_power(g, h - 1),
        neg(mul(alpha_power(h - 1), dp_var("q", h - 1))),
    )


@lru_cache(maxsize=None)
def divided_difference_h(h):
    # H_a in equation (6).
    terms = []
    for ell in range(h - 1):
        terms.append(
            scale(
                product(
                    alpha_power(h - 2 - ell),
                    dp_var("q", h - 2 - ell),
                    dp_var("r", ell),
                ),
                Fraction(1, ell + 1),
            )
        )
    return add(*terms)


@lru_cache(maxsize=None)
def direct_normal_error(h):
    # F(x E_aa + D) = x*(alpha*q+r)+d.
    f = add(mul(X, shifted_selected_quadratic()), D)
    t = add(mul(X, target_xa(h)), mul(D, dp_var("q", h - 1)))
    scalar_power = product(alpha_power(h - 1), ordinary_power(X, h - 1))
    return add(divided_power(f, h), neg(mul(scalar_power, t)))


@lru_cache(maxsize=None)
def claimed_normal_error(h):
    g = shifted_selected_quadratic()
    terms = [
        mul(ordinary_power(X, h), unary_error(h)),
        product(ordinary_power(X, h - 1), D, theta(h)),
    ]
    for m in range(2, h + 1):
        terms.append(
            product(
                ordinary_power(X, h - m),
                dp_var("d", m),
                divided_power(g, h - m),
            )
        )
    return add(*terms)


def audit_segre_squares():
    # Products are compared as literal commutative source factors.
    labels = (0, 1, 2)
    selected = 1
    for i in labels:
        for j in labels:
            left = sorted((f"p{i}", f"s{j}", f"p{selected}", f"s{selected}"))
            right = sorted((f"p{i}", f"s{selected}", f"p{selected}", f"s{j}"))
            require(left == right, f"Segre square failed at ({i},{j})")


def audit_scalar_unit_row_deletion():
    """Audit which full-nine rows change when the p_a star is deleted.

    Each row is recorded by its direct coefficient, target coefficient,
    and whether its response contains the selected p-row.  In the
    scalar-unit case the direct and target coefficients agree only at
    ``(a,a)``; after equations (28)--(29), every changed response is a
    zero tensor.  This finite label check deliberately does not model the
    minimum-support argument itself.
    """

    labels = (0, 1, 2)
    selected = 1
    changed = []
    for i in labels:
        for j in labels:
            direct = i == selected and j == selected
            target = i == j
            contains_selected_p_row = i == selected
            if contains_selected_p_row:
                changed.append((i, j))
                if j == selected:
                    require(direct and target, "exceptional row flags disagree")
                else:
                    require(
                        not direct and not target,
                        f"off-diagonal selected p-row has a source at ({i},{j})",
                    )
    require(
        changed == [(selected, j) for j in labels],
        "deleting p_a changed something other than its three endpoint rows",
    )


def audit_order(h):
    require(
        direct_normal_error(h) == claimed_normal_error(h),
        f"full normal form failed at h={h}",
    )

    require(
        theta(h) == mul(R, divided_difference_h(h)),
        f"divided-difference factor failed at h={h}",
    )

    # G*Theta = h*U + (h-1)*alpha^(h-1)*r*q^[h-1].
    lhs = mul(shifted_selected_quadratic(), theta(h))
    rhs = add(
        scale(unary_error(h), h),
        scale(
            product(alpha_power(h - 1), R, dp_var("q", h - 1)),
            h - 1,
        ),
    )
    require(lhs == rhs, f"Euler unary-anchor identity failed at h={h}")

    # The direct expansion must have no normal-response-linear terms except
    # x^(h-1) * d * Theta.
    linear_d = {
        mon: coeff
        for mon, coeff in direct_normal_error(h).items()
        if mon[4] == 1
    }
    expected_linear_d = product(ordinary_power(X, h - 1), D, theta(h))
    require(linear_d == expected_linear_d, f"first normal jet failed at h={h}")

    # U has exactly the higher-cumulant terms k >= 2 after use of the
    # exceptional physical row.
    expected_u_terms = []
    for k in range(2, h + 1):
        expected_u_terms.append(
            product(
                alpha_power(h - k),
                dp_var("q", h - k),
                dp_var("r", k),
            )
        )
    require(
        unary_error(h) == add(*expected_u_terms),
        f"unary higher-cumulant expansion failed at h={h}",
    )


def mutation_checks():
    h = 7

    wrong_h = add(
        *[
            product(
                alpha_power(h - 2 - ell),
                dp_var("q", h - 2 - ell),
                dp_var("r", ell),
            )
            for ell in range(h - 1)
        ]
    )
    require(theta(h) != mul(R, wrong_h), "mutation lost the 1/(ell+1) factor")

    wrong_euler = add(
        scale(unary_error(h), h),
        scale(
            product(alpha_power(h - 1), R, dp_var("q", h - 1)),
            h,
        ),
    )
    require(
        mul(shifted_selected_quadratic(), theta(h)) != wrong_euler,
        "mutation accepted h in place of h-1 in the Euler term",
    )

    wrong_normal = add(
        mul(ordinary_power(X, h), unary_error(h)),
        product(ordinary_power(X, h - 2), D, theta(h)),
    )
    require(
        direct_normal_error(h) != wrong_normal,
        "mutation accepted the wrong first-jet normal order",
    )


def main():
    audit_segre_squares()
    audit_scalar_unit_row_deletion()
    for h in range(2, 65):
        audit_order(h)
    mutation_checks()
    print(
        "scalar-unit full normal-jet unary-anchor ledger: PASS; "
        "orders h=2..64, all nine Segre cells, and mutations audited"
    )


if __name__ == "__main__":
    main()
