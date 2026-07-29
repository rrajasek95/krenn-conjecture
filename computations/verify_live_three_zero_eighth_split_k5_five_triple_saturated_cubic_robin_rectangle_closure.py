#!/usr/bin/env python3
"""Exact audit of the two k=5 saturated-cubic closures."""

from collections import Counter
from itertools import combinations
from math import comb
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


H, P, K, TOTAL = 8, 13, 5, 23
FIVE_TRIPLE_TARGET = (3,) * 5 + (2,) * 3 + (1,) * 2
FOUR_TRIPLE_TARGET = (3,) * 4 + (2,) * 4 + (1,) * 3
TARGETS = {FIVE_TRIPLE_TARGET, FOUR_TRIPLE_TARGET}
PREVIOUSLY_CLOSED = {
    (2,) * 11 + (1,),
    (2,) * 10 + (1,) * 3,
    (4, 4) + (3,) * 5,
    (3,) * 5 + (2,) * 4,
    (3,) * 4 + (2,) * 5 + (1,),
}


def zero_scenarios(profile):
    return (None,) + tuple(
        index for index, multiplicity in enumerate(profile) if multiplicity == 1
    )


def residual_multiplicities(profile, takes):
    return tuple(
        multiplicity - takes.get(index, 0)
        for index, multiplicity in enumerate(profile)
    )


def minimum_nonzero_guards(profile, takes):
    residual = residual_multiplicities(profile, takes)
    return min(
        sum(
            multiplicity == 1 and index != zero_index
            for index, multiplicity in enumerate(residual)
        )
        for zero_index in zero_scenarios(profile)
    )


def audit_formal_choice(profile, chosen):
    guard_histogram = Counter()
    legal = True
    for lowered_pair in combinations(chosen, 2):
        takes = {
            index: (1 if index in lowered_pair else 2)
            for index in chosen
        }
        assert sum(takes.values()) == H
        guards = minimum_nonzero_guards(profile, takes)
        guard_histogram[guards] += 1
        legal &= guards >= 1
    assert sum(guard_histogram.values()) == 10
    return legal, guard_histogram


def formal_complement(profile, chosen):
    chosen_set = set(chosen)
    return tuple(
        sorted(
            (
                multiplicity - (2 if index in chosen_set else 0)
                for index, multiplicity in enumerate(profile)
                if multiplicity - (2 if index in chosen_set else 0) > 0
            ),
            reverse=True,
        )
    )


# ---------------------------------------------------------------------------
# Exact current ledger and inventory of every remaining five-triple choice.
# ---------------------------------------------------------------------------

counts, frozen_tuple = frontier.census(H, P)
frozen = set(frozen_tuple)
assert counts == {
    "H": 637,
    "S": 501,
    "C": 30,
    "L": 23,
    "R": 44,
    "Q": 19,
    "D": 1,
}
assert len(frozen) == 44
open_before = frozen - PREVIOUSLY_CLOSED
assert len(open_before) == 39

expected_five_triple_profiles = {
    (3,) * 5 + (2,) * double_count + (1,) * (8 - 2 * double_count)
    for double_count in range(4)
}
five_triple_profiles = {
    profile for profile in open_before if profile.count(3) == 5
}
assert five_triple_profiles == expected_five_triple_profiles
assert FIVE_TRIPLE_TARGET in five_triple_profiles
assert FOUR_TRIPLE_TARGET in open_before

# For d doubles and x selected doubles, the remaining 5-x formal layers are
# triples.  The complement is 3^x 2^(d-x) 1^(13-2d-x), its relation degree
# is c-4, and its simple-root Wronskian slack is exactly 3-x.
inventory = Counter()
formal_choices = 0
core_zero_scenarios = 0
for profile in five_triple_profiles:
    double_count = profile.count(2)
    repeated = tuple(
        index for index, multiplicity in enumerate(profile) if multiplicity >= 2
    )
    for chosen in combinations(repeated, 5):
        formal_choices += 1
        core_zero_scenarios += 10 * len(zero_scenarios(profile))
        legal, _ = audit_formal_choice(profile, chosen)
        assert legal

        selected_doubles = sum(profile[index] == 2 for index in chosen)
        complementary_profile = formal_complement(profile, chosen)
        classes = len(complementary_profile)
        simple_roots = complementary_profile.count(1)
        relation_degree = classes - 4
        wronskian_slack = 2 * relation_degree - 2 - simple_roots

        assert complementary_profile == (
            (3,) * selected_doubles
            + (2,) * (double_count - selected_doubles)
            + (1,) * (13 - 2 * double_count - selected_doubles)
        )
        assert classes == 13 - double_count - selected_doubles
        assert simple_roots == 13 - 2 * double_count - selected_doubles
        assert relation_degree == 9 - double_count - selected_doubles
        assert wronskian_slack == 3 - selected_doubles
        inventory[(double_count, selected_doubles)] += 1

expected_inventory = Counter(
    {
        (double_count, selected_doubles): (
            comb(double_count, selected_doubles)
            * comb(5, selected_doubles)
        )
        for double_count in range(4)
        for selected_doubles in range(double_count + 1)
    }
)
assert inventory == expected_inventory
assert formal_choices == 84
assert core_zero_scenarios == 3240

saturated_keys = {
    key for key in inventory if 3 - key[1] == 0
}
assert saturated_keys == {(3, 3)}
assert inventory[(3, 3)] == 10

# The ten saturated choices select all three doubles and two triples.
triple_indices = tuple(range(5))
double_indices = (5, 6, 7)
targeted_core_count = 0
targeted_zero_scenarios = 0
for selected_triples in combinations(triple_indices, 2):
    chosen = double_indices + selected_triples
    legal, guard_histogram = audit_formal_choice(FIVE_TRIPLE_TARGET, chosen)
    assert legal
    assert guard_histogram == Counter({3: 6, 5: 3, 1: 1})
    complementary_profile = formal_complement(FIVE_TRIPLE_TARGET, chosen)
    assert complementary_profile == (3,) * 3 + (1,) * 4
    assert (len(complementary_profile), complementary_profile.count(1)) == (7, 4)
    assert len(complementary_profile) - 4 == 3
    assert 2 * 3 - 2 == 4
    targeted_core_count += 10
    targeted_zero_scenarios += 10 * len(zero_scenarios(FIVE_TRIPLE_TARGET))
assert targeted_core_count == 100
assert targeted_zero_scenarios == 300

# The companion four-triple profile has four saturated choices: all four
# doubles and one of the four triples.
four_triple_core_count = 0
four_triple_zero_scenarios = 0
four_triple_indices = tuple(range(4))
four_double_indices = (4, 5, 6, 7)
for selected_triple in four_triple_indices:
    chosen = four_double_indices + (selected_triple,)
    legal, guard_histogram = audit_formal_choice(FOUR_TRIPLE_TARGET, chosen)
    assert legal
    assert guard_histogram == Counter({5: 6, 3: 4})
    complementary_profile = formal_complement(FOUR_TRIPLE_TARGET, chosen)
    assert complementary_profile == (3,) * 3 + (1,) * 4
    assert (len(complementary_profile), complementary_profile.count(1)) == (7, 4)
    four_triple_core_count += 10
    four_triple_zero_scenarios += 10 * len(
        zero_scenarios(FOUR_TRIPLE_TARGET)
    )
assert four_triple_core_count == 40
assert four_triple_zero_scenarios == 160


# ---------------------------------------------------------------------------
# Derivative exponents and the saturated cubic accessory identity.
# ---------------------------------------------------------------------------

z, mu = sp.symbols("z mu")
singleton_values = sp.symbols("r0:2")
selected_triples = sp.symbols("s0:2")
outside_triples = sp.symbols("u0:3")
formal_doubles = sp.symbols("delta0:3")

L = sp.prod(z - value for value in singleton_values)
U = sp.prod(z - value for value in selected_triples)
Q = sp.prod(
    z + value for value in formal_doubles + selected_triples
)
A = L * U * sp.prod((z - value) ** 3 for value in outside_triples)
gcd_factor = sp.prod((z - value) ** 2 for value in outside_triples)
derivative_factor = sp.cancel((z + mu) ** K * gcd_factor * Q**2 / A**2)
expected_factor = sp.cancel(
    (z + mu) ** 5
    * Q**2
    / (
        L**2
        * U**2
        * sp.prod((z - value) ** 4 for value in outside_triples)
    )
)
assert sp.cancel(derivative_factor - expected_factor) == 0
assert sp.degree(A, z) == 13
assert sp.degree(Q, z) == 5
assert 5 + 2 * 5 + 3 == 18
assert 2 * 2 + 2 * 2 + 4 * 3 == 20

f_coefficients = sp.symbols("f0:4")
g_coefficients = sp.symbols("g0:4")
f = sum(f_coefficients[index] * z**index for index in range(4))
g = sum(g_coefficients[index] * z**index for index in range(4))
W = sp.expand(f * sp.diff(g, z) - sp.diff(f, z) * g)
accessory = sp.expand(
    sp.diff(f, z) * sp.diff(g, z, 2)
    - sp.diff(f, z, 2) * sp.diff(g, z)
)
assert sp.Poly(W, z).degree() <= 4
assert sp.Poly(accessory, z).degree() <= 2
assert sp.Poly(accessory, z).coeff_monomial(z**2) == (
    6 * sp.Poly(W, z).coeff_monomial(z**4)
)
assert sp.Poly(accessory, z).coeff_monomial(z) == (
    3 * sp.Poly(W, z).coeff_monomial(z**3)
)
for solution in (f, g):
    ode = sp.expand(
        W * sp.diff(solution, z, 2)
        - sp.diff(W, z) * sp.diff(solution, z)
        + accessory * solution
    )
    assert ode == 0

# Four saturated simple roots force W to their product.  Interpolation of
# V(x_i)=-W'(x_i)Y_i has cubic coefficient -sum(Y_i), while deg(V)<=2.
nodes = sp.symbols("x0:4")
robin_coefficients = sp.symbols("Y0:4")
node_W = sp.prod(z - node for node in nodes)
interpolant = -sum(
    robin_coefficients[index]
    * sp.prod(z - nodes[j] for j in range(4) if j != index)
    for index in range(4)
)
assert sp.Poly(interpolant, z).coeff_monomial(z**3) == -sum(
    robin_coefficients
)
assert sp.limit(z * interpolant / node_W, z, sp.oo) == -sum(
    robin_coefficients
)


# ---------------------------------------------------------------------------
# Full Robin sum and the choose-two Boolean rectangle.
# ---------------------------------------------------------------------------

a, b, c, d, e = sp.symbols("a b c d e")
triple_values = (a, b, c, d, e)
r_values = sp.symbols("rho0:2")
delta_values = sp.symbols("delta0:3")


def robin_sum(selected):
    selected = tuple(selected)
    outside = tuple(
        value for value in triple_values if value not in selected
    )
    simple_roots = r_values + selected
    total_robin = 0
    for root in simple_roots:
        total_robin += 5 / (root + mu)
        total_robin += 2 * sum(
            1 / (root + value) for value in delta_values
        )
        total_robin += 2 * sum(
            1 / (root + value) for value in selected
        )
        total_robin -= 2 * sum(
            1 / (root - other)
            for other in simple_roots
            if other != root
        )
        total_robin -= 4 * sum(
            1 / (root - value) for value in outside
        )
    return total_robin


rectangle = sp.factor(
    sp.cancel(
        robin_sum((a, c))
        - robin_sum((a, d))
        - robin_sum((b, c))
        + robin_sum((b, d))
    )
)
expected_rectangle = sp.factor(
    4
    * (a - b)
    * (c - d)
    * (a + b + c + d)
    / ((a + c) * (a + d) * (b + c) * (b + d))
)
assert sp.cancel(rectangle - expected_rectangle) == 0

total_triples = sum(triple_values)
four_sums = tuple(total_triples - value for value in triple_values)
for left, right in combinations(range(5), 2):
    assert sp.expand(four_sums[left] - four_sums[right]) == (
        triple_values[right] - triple_values[left]
    )


# ---------------------------------------------------------------------------
# The choose-one moment elimination for 3^4 2^4 1^3.
# ---------------------------------------------------------------------------

# If W is monic with z^3 coefficient w3, the two universal leading
# coefficients of V give, via V/W=-sum Y_i/(z-x_i), the three moments
# M0=0, M1=-6, M2=3*w3=-3*sum(x_i).
t, w3, w2, w1, w0, v0 = sp.symbols("t w3 w2 w1 w0 v0")
quotient_at_infinity = sp.series(
    (6 * t**2 + 3 * w3 * t**3 + v0 * t**4)
    / (1 + w3 * t + w2 * t**2 + w1 * t**3 + w0 * t**4),
    t,
    0,
    4,
).removeO()
assert sp.expand(quotient_at_infinity) == 6 * t**2 - 3 * w3 * t**3

aa = sp.symbols("aa")
fixed_singletons = sp.symbols("R0:3")
fixed_doubles = sp.symbols("D0:4")
all_four_triples = sp.symbols("A0:4")


def fixed_singleton_part(root):
    return (
        5 / (root + mu)
        + 2 * sum(1 / (root + value) for value in fixed_doubles)
        - 2 * sum(
            1 / (root - other)
            for other in fixed_singletons
            if other != root
        )
        - 4 * sum(1 / (root - value) for value in all_four_triples)
    )


# For each of the four actual selected triples, audit that the exact Robin
# coefficient at a fixed singleton r is K_r+2/(r+a)+2/(r-a), with K_r
# independent of the selection.
for selected_triple in all_four_triples:
    outside = tuple(
        value for value in all_four_triples if value != selected_triple
    )
    for root in fixed_singletons:
        selected_robin_at_root = (
            5 / (root + mu)
            + 2 * sum(1 / (root + value) for value in fixed_doubles)
            + 2 / (root + selected_triple)
            - 2 * sum(
                1 / (root - other)
                for other in fixed_singletons
                if other != root
            )
            - 2 / (root - selected_triple)
            - 4 * sum(1 / (root - value) for value in outside)
        )
        selected_robin_rewritten = (
            fixed_singleton_part(root)
            + 2 / (root + selected_triple)
            + 2 / (root - selected_triple)
        )
        assert sp.cancel(
            selected_robin_at_root - selected_robin_rewritten
        ) == 0

# The remaining moment algebra is universal in three fixed values K_r;
# keeping them atomic makes the certificate fast and transparent.
K_values = sp.symbols("KR0:3")
K0 = sum(K_values)
K1 = sum(root * value for root, value in zip(fixed_singletons, K_values))
K2 = sum(root**2 * value for root, value in zip(fixed_singletons, K_values))
sigma = sum(fixed_singletons)
p_plus = sum(1 / (root + aa) for root in fixed_singletons)

robin_at_singletons = tuple(
    value + 2 / (root + aa) + 2 / (root - aa)
    for root, value in zip(fixed_singletons, K_values)
)
first_difference = sp.factor(
    sum(
        (root - aa) * value
        for root, value in zip(fixed_singletons, robin_at_singletons)
    )
)
second_difference = sp.factor(
    sum(
        root * (root - aa) * value
        for root, value in zip(fixed_singletons, robin_at_singletons)
    )
)
assert sp.cancel(
    first_difference - (K1 - aa * K0 + 12 - 4 * aa * p_plus)
) == 0
assert sp.cancel(
    second_difference
    - (K2 - aa * K1 + 4 * sigma - 12 * aa + 4 * aa**2 * p_plus)
) == 0

# M0=0, M1=-6, M2=-3(sigma+aa).  The first difference gives
# 4*aa*p=K1-aa*K0+18.  Substitution into the second leaves one fixed
# nonzero quadratic for every selected triple value.
k0, k1, k2, sig, p_symbol = sp.symbols("k0 k1 k2 sig p_symbol")
p_from_first = k1 - aa * k0 + 18
second_after_substitution = sp.expand(
    k2
    - aa * k1
    + 4 * sig
    - 12 * aa
    + aa * p_from_first
)
assert second_after_substitution == k2 + 4 * sig + 6 * aa - k0 * aa**2
moment_second_difference = -3 * sig + 3 * aa
fixed_quadratic = sp.expand(
    moment_second_difference - second_after_substitution
)
assert fixed_quadratic == k0 * aa**2 - 3 * aa - k2 - 7 * sig
assert sp.Poly(fixed_quadratic, aa).degree() <= 2
assert sp.Poly(fixed_quadratic, aa).coeff_monomial(aa) == -3
assert len(all_four_triples) == 4 > 2

open_after = open_before - TARGETS
assert len(open_after) == 37
assert (2,) * 9 + (1,) * 5 in open_after


print("k=5 saturated-cubic Robin closures: PASS")
print("inventory: 4 profiles, 84 formal choices, 3240 core/zero scenarios")
print("saturated targets: 14 pencils and 140 legal pair-drop cores")
print("updated ledger: 7 accepted, 37 open")
