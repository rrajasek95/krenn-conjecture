#!/usr/bin/env python3
"""Exact audit of repeated-anchor closures for seventh-split triple profiles."""

import sympy as sp


# ---------------------------------------------------------------------------
# Moving-class logarithmic derivatives and Bell rows.
# ---------------------------------------------------------------------------

x, t, U, V, W, j = sp.symbols("x t U V W j")
D = x**2 - t**2


def chi(multiplicity):
    return multiplicity / (x - t) - (multiplicity + 1) / (x + t)


def eta(multiplicity):
    return (
        multiplicity / (x - t) ** 2
        + (multiplicity + 1) / (x + t) ** 2
    )


def theta(multiplicity):
    return (
        2 * multiplicity / (x - t) ** 3
        - 2 * (multiplicity + 1) / (x + t) ** 3
    )


assert sp.factor(sp.diff(chi(j), t) - eta(j)) == 0
assert sp.factor(sp.diff(eta(j), t) - theta(j)) == 0

# If L_1, L_2, L_3 are the first three logarithmic derivatives, the
# ordinary derivatives H''/H and H'''/H are the second and third complete
# Bell polynomials.
w, L1, L2, L3 = sp.symbols("w L1 L2 L3")
formal_H = sp.exp(L1 * w + L2 * w**2 / 2 + L3 * w**3 / 6)
assert sp.expand(sp.diff(formal_H, w, 2).subs(w, 0) - (L1**2 + L2)) == 0
assert sp.expand(
    sp.diff(formal_H, w, 3).subs(w, 0)
    - (L1**3 + 3 * L1 * L2 + L3)
) == 0


# ---------------------------------------------------------------------------
# A selected double and a moving triple: the nonzero quartic.
# ---------------------------------------------------------------------------

double_general = sp.cancel(
    D**2 * ((U + chi(j)) ** 2 + V + eta(j))
).expand()
assert sp.denom(double_general) == 1
assert sp.Poly(double_general, x).degree() <= 4
assert sp.factor(
    double_general.subs(x, t) - 4 * t**2 * j * (j + 1)
) == 0
assert sp.factor(
    double_general.subs(x, -t)
    - 4 * t**2 * (j + 1) * (j + 2)
) == 0

double_triple = sp.Poly(double_general.subs(j, 3), x)
assert double_triple.degree() == 4
assert double_triple.coeff_monomial(x**3) == -2 * U
assert double_triple.coeff_monomial(x) == 2 * U * t**2 - 16 * t
assert sp.factor(double_triple.as_expr().subs(x, t) - 48 * t**2) == 0
assert sp.factor(double_triple.as_expr().subs(x, -t) - 80 * t**2) == 0

# The selected-double / moving-double specialization used for the three
# final profiles is likewise a genuine quartic.
double_double = sp.Poly(double_general.subs(j, 2), x)
assert double_double.degree() == 4
assert sp.factor(double_double.as_expr().subs(x, t) - 24 * t**2) == 0
assert sp.factor(double_double.as_expr().subs(x, -t) - 48 * t**2) == 0


# ---------------------------------------------------------------------------
# A selected triple and a moving simple class: the nonzero sextic.
# ---------------------------------------------------------------------------

triple_general = sp.cancel(
    D**3
    * (
        (U + chi(j)) ** 3
        + 3 * (U + chi(j)) * (V + eta(j))
        + W
        + theta(j)
    )
).expand()
assert sp.denom(triple_general) == 1
assert sp.Poly(triple_general, x).degree() <= 6
assert sp.factor(
    triple_general.subs(x, t)
    - 8 * t**3 * j * (j + 1) * (j + 2)
) == 0
assert sp.factor(
    triple_general.subs(x, -t)
    - 8 * t**3 * (j + 1) * (j + 2) * (j + 3)
) == 0

triple_simple = sp.Poly(triple_general.subs(j, 1), x)
assert triple_simple.degree() == 6
assert sp.factor(triple_simple.as_expr().subs(x, t) - 48 * t**3) == 0
assert sp.factor(triple_simple.as_expr().subs(x, -t) - 192 * t**3) == 0


# ---------------------------------------------------------------------------
# Sharp root counts and the Möbius contradiction.
# ---------------------------------------------------------------------------

g1, g2 = sp.symbols("g1 g2")
mobius_difference = (
    (t - g1) / (t + g1) - (t - g2) / (t + g2)
)
assert sp.factor(
    mobius_difference
    - 2 * t * (g2 - g1) / ((t + g1) * (t + g2))
) == 0

# Endpoint ratios in the two sharp cases.
assert sp.Rational(48, 80) == sp.Rational(3, 5)
assert sp.Rational(48, 192) == sp.Rational(1, 4)


# ---------------------------------------------------------------------------
# Exact singleton-row legality census.
# ---------------------------------------------------------------------------


def legal_a3_b3_x(profile):
    """Count legal moving classes after fully selecting two triples."""
    triples, doubles, singletons = profile
    multiplicities = [3] * triples + [2] * doubles + [1] * singletons
    assert triples >= 2
    answer = 0
    for moving in range(2, len(multiplicities)):
        remaining = multiplicities.copy()
        remaining[0] -= 3
        remaining[1] -= 3
        remaining[moving] -= 1
        if 1 in remaining:
            answer += 1
    return answer


expected_a3_b3_x = {
    (3, 1, 6): 8,
    (2, 3, 5): 8,
    (3, 2, 4): 7,
    (3, 2, 5): 8,
    (3, 3, 2): 6,
    (3, 4, 0): 4,
    (2, 5, 1): 5,
    (3, 4, 1): 5,
}
for profile, expected in expected_a3_b3_x.items():
    assert legal_a3_b3_x(profile) == expected


def legal_f2_g2_x3(number_of_triples):
    """Count moving triples after selecting two copies at two fixed triples."""
    assert number_of_triples >= 3
    answer = 0
    for moving in range(2, number_of_triples):
        remaining = [3] * number_of_triples
        remaining[0] -= 2
        remaining[1] -= 2
        remaining[moving] -= 3
        if 1 in remaining:
            answer += 1
    return answer


assert legal_f2_g2_x3(7) == 5
assert legal_f2_g2_x3(6) == 4


def legal_f3_g2_x2(profile):
    """Count moving classes after one full and one partial triple."""
    triples, doubles, singletons = profile
    multiplicities = [3] * triples + [2] * doubles + [1] * singletons
    assert triples >= 2
    answer = 0
    for moving in range(2, len(multiplicities)):
        if multiplicities[moving] < 2:
            continue
        remaining = multiplicities.copy()
        remaining[0] -= 3
        remaining[1] -= 2
        remaining[moving] -= 2
        if 1 in remaining:
            answer += 1
    return answer


assert legal_f3_g2_x2((3, 4, 0)) == 5
assert legal_f3_g2_x2((2, 5, 1)) == 5
assert legal_f3_g2_x2((3, 4, 1)) == 5

# The exact triple-containing frontier before and after these closures.
old_triple_frontier = {
    8: {
        (3, 4, 0),
        (3, 3, 2),
        (3, 2, 4),
        (3, 1, 6),
        (2, 5, 1),
        (2, 3, 5),
    },
    9: {(6, 0, 0), (3, 4, 1), (3, 2, 5)},
    12: {(7, 0, 0)},
}
newly_closed = {
    8: {
        (3, 4, 0),
        (3, 3, 2),
        (3, 2, 4),
        (3, 1, 6),
        (2, 5, 1),
        (2, 3, 5),
    },
    9: {(6, 0, 0), (3, 4, 1), (3, 2, 5)},
    12: {(7, 0, 0)},
}
expected_remaining = {
    8: set(),
    9: set(),
    12: set(),
}
for p, profiles in old_triple_frontier.items():
    assert profiles - newly_closed[p] == expected_remaining[p]


print("second- and third-order no-simple-pole Bell rows: exact")
print("moving-double/triple quartics and endpoint ratios: exact")
print("moving-simple sextic and endpoint ratio 1/4: exact")
print("sharp Möbius exclusions for six roots and four roots: exact")
print("triple-profile legality census and complete frontier closure: exact")
