#!/usr/bin/env python3
"""Exact audit of the unified k=5 pair-drop kernel and its closures."""

from itertools import combinations
from math import comb
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


H = 8
P = 13
K = 5
TOTAL = 23


def profile(triples=0, doubles=0, singletons=None):
    if singletons is None:
        singletons = TOTAL - 3 * triples - 2 * doubles
    answer = (3,) * triples + (2,) * doubles + (1,) * singletons
    assert singletons >= 0 and sum(answer) == TOTAL
    return answer


def complement_signature(candidate, d, selected_triples):
    triples = candidate.count(3)
    doubles = candidate.count(2)
    singletons = candidate.count(1)
    s = 10 - 2 * d
    selected_doubles = d - selected_triples
    answer = (
        [3] * (triples - selected_triples)
        + [2] * (doubles - selected_doubles)
        + [1] * (singletons - s + selected_triples)
    )
    return tuple(sorted(answer, reverse=True))


def selection_types(candidate):
    """Multiplicity types covered by the lemma, not individual choices."""

    triples = candidate.count(3)
    doubles = candidate.count(2)
    singletons = candidate.count(1)
    answer = []
    for d in range(5):
        s = 10 - 2 * d
        for selected_triples in (0, 1):
            selected_doubles = d - selected_triples
            if (
                selected_triples <= triples
                and 0 <= selected_doubles <= doubles
                and s <= singletons
            ):
                answer.append(
                    (
                        d,
                        selected_triples,
                        complement_signature(candidate, d, selected_triples),
                    )
                )
    return tuple(answer)


def audit_legal_graph(candidate, d, selected_triples):
    """Check every pair and every genuinely different zero location."""

    s = 10 - 2 * d
    triples = candidate.count(3)
    doubles = candidate.count(2)
    singletons = candidate.count(1)
    selected_doubles = d - selected_triples
    assert selected_triples <= triples
    assert selected_doubles <= doubles
    assert s <= singletons

    layers = (
        tuple(("T", i) for i in range(selected_triples))
        + tuple(("D", i) for i in range(selected_doubles))
        + tuple(("S", i) for i in range(s))
    )
    unselected_singletons = singletons - s
    assert len(layers) == 10 - d

    # None, each selected singleton, and one representative unselected
    # singleton are the exact zero-placement orbits.
    zero_scenarios = [None]
    zero_scenarios.extend(layer for layer in layers if layer[0] == "S")
    if unselected_singletons:
        zero_scenarios.append(("U", 0))

    factor_degree = {layer: (3 if layer[0] == "S" else 2) for layer in layers}
    degree_cap = 11 - d
    total_factor_degree = sum(factor_degree.values())
    assert total_factor_degree == 30 - 4 * d

    for zero in zero_scenarios:
        legal_edges = set()
        illegal_edges = set()
        for left, right in combinations(layers, 2):
            lowered = {left, right}

            # Nonzero singleton guards in the complement.  A selected
            # triple supplies one unless lowered; a lowered double always
            # supplies one; omitted singleton layers supply themselves;
            # and original unselected singletons remain throughout.
            nonzero_guards = unselected_singletons
            if zero is not None and zero[0] == "U":
                nonzero_guards -= 1
            nonzero_guards += sum(
                layer[0] == "T" and layer not in lowered for layer in layers
            )
            nonzero_guards += sum(
                layer[0] == "D" and layer in lowered for layer in layers
            )
            nonzero_guards += sum(
                layer[0] == "S" and layer in lowered and layer != zero
                for layer in layers
            )

            edge = frozenset((left, right))
            if nonzero_guards:
                legal_edges.add(edge)
            else:
                illegal_edges.add(edge)

        assert len(illegal_edges) <= 1
        if illegal_edges:
            assert selected_triples == 1
            assert zero is not None and zero[0] == "S"
            assert illegal_edges == {
                frozenset((next(layer for layer in layers if layer[0] == "T"), zero))
            }

        # Even at a missing-edge endpoint, all legal neighbor factors
        # have degree greater than the ambient polynomial degree.
        for layer in layers:
            neighbors = {
                next(iter(edge - {layer}))
                for edge in legal_edges
                if layer in edge
            }
            neighbor_degree = sum(factor_degree[item] for item in neighbors)
            assert neighbor_degree > degree_cap

    return len(zero_scenarios)


# ---------------------------------------------------------------------------
# Kernel arithmetic for every d.
# ---------------------------------------------------------------------------

for d in range(5):
    s = 10 - 2 * d
    layer_count = 10 - d
    degree_cap = 11 - d
    assert 2 * d + s == 10
    assert 2 * d + 3 * s == 30 - 4 * d
    assert 25 - 4 * d > degree_cap
    assert 1 + 2 * layer_count == 2 * degree_cap - 1
    assert 3 + 2 * (layer_count - 1) == 2 * degree_cap - 1

    for lowered_singletons in range(3):
        residual_degree = 7 - d - lowered_singletons
        lift_factor_degree = 4 + lowered_singletons
        assert residual_degree + lift_factor_degree == degree_cap

    for dimension in range(5, degree_cap + 2):
        forced_weight = d * (dimension - 2) + s * (dimension - 1)
        wronskian_cap = dimension * (degree_cap + 1 - dimension)
        deficit = forced_weight - wronskian_cap
        assert deficit == dimension**2 - 2 * dimension - 10
        assert deficit > 0

        # These are the local corrections used after removing a gcd.
        assert deficit + dimension + 1 > 0
        assert deficit + 2 * dimension + 2 > 0

    for absorbed_singletons in range(s + 1):
        square_degree = (degree_cap - 2 * absorbed_singletons) // 2
        if square_degree < 2:
            continue
        forced_square_weight = 2 * (s - absorbed_singletons)
        square_wronskian_cap = 3 * (square_degree - 2)
        assert forced_square_weight > square_wronskian_cap

    ambient_dimension = degree_cap + 1
    row_count = layer_count
    kernel_dimension = 4
    row_rank = ambient_dimension - kernel_dimension
    relation_dimension = row_count - row_rank
    assert (row_rank, relation_dimension) == (8 - d, 2)

    selected_denominator_degree = 3 * d + 2 * s
    annihilated_moments = degree_cap + 1
    numerator_degree = selected_denominator_degree - annihilated_moments - 1
    assert selected_denominator_degree == 20 - d
    assert numerator_degree == 7
    assert 2 * d + s == 10


# A simple gcd zero at an exact singleton row forces a common square
# factor in the primitive even space.
z, r = sp.symbols("z r")
b0, b1 = sp.symbols("b0 b1", nonzero=True)
e0, e1 = sp.symbols("e0 e1")
local_g = z + r
local_unit = b0 + b1 * (z + r)
local_even = e0 + e1 * (z**2 - r**2)
simple_absorption_row = sp.diff(local_unit * local_g * local_even, z).subs(z, -r)
assert sp.expand(simple_absorption_row - b0 * e0) == 0


# ---------------------------------------------------------------------------
# Exact differential and its leading cancellation.
# ---------------------------------------------------------------------------

mu = sp.symbols("mu")
A_value, A_prime, N_value, N_prime = sp.symbols(
    "A_value A_prime N_value N_prime"
)
quotient_numerator = (
    (6 * (z + mu) ** 5 * N_value + (z + mu) ** 6 * N_prime) * A_value
    - (z + mu) ** 6 * N_value * A_prime
)
factored_numerator = (z + mu) ** 5 * (
    A_value * ((z + mu) * N_prime + 6 * N_value)
    - (z + mu) * A_prime * N_value
)
assert sp.expand(quotient_numerator - factored_numerator) == 0

for multiplicities in ((3, 3, 3, 3, 1), (3, 3, 3, 2, 2)):
    roots = sp.symbols(f"a0:{len(multiplicities)}")
    A = sp.prod(
        (z - root) ** multiplicity
        for root, multiplicity in zip(roots, multiplicities)
    )
    gcd = sp.prod(
        (z - root) ** (multiplicity - 1)
        for root, multiplicity in zip(roots, multiplicities)
    )
    radical = sp.cancel(A / gcd)
    reduced_derivative = sp.cancel(sp.diff(A, z) / gcd)
    assert sp.Poly(radical, z).degree() == 5
    assert sp.Poly(reduced_derivative, z).degree() == 4
    assert sp.Poly(reduced_derivative, z).LC() == 13

    for n in range(8):
        N = z**n
        differential_polynomial = sp.Poly(
            sp.expand(
                radical * ((z + mu) * sp.diff(N, z) + 6 * N)
                - (z + mu) * reduced_derivative * N
            ),
            z,
        )
        assert differential_polynomial.degree() <= 11
        if n < 7:
            assert differential_polynomial.coeff_monomial(z ** (5 + n)) == n - 7
        else:
            assert differential_polynomial.coeff_monomial(z**12) == 0


# Complementary singleton: S=z-r makes the residue equal to the unit.
x = z - r
b2 = sp.symbols("b2")
B = b0 + b1 * x + b2 * x**2
assert sp.diff(B * x, z).subs(z, r) == b0


# Complementary doubles: exact row, swap identity, and fibre degree.
u, v, x_value = sp.symbols("u v x")
c0, c1, c2 = sp.symbols("c0 c1 c2")
local_x = z - u
double_unit = c0 + c1 * local_x + c2 * local_x**2
assert sp.diff(double_unit * local_x, z, 2).subs(z, u) == 2 * c1


def phi(anchor, value):
    return 2 / (anchor + value) + 3 / (anchor - value)


assert sp.factor(phi(u, x_value) - (5 * u + x_value) / (u**2 - x_value**2)) == 0
before = 2 / (u + x_value) - 3 / (u - v)
after = 2 / (u + v) - 3 / (u - x_value)
assert sp.factor((before - after) - (phi(u, x_value) - phi(u, v))) == 0
fibre_value = sp.symbols("lambda")
fibre_polynomial = sp.Poly(
    sp.expand(fibre_value * (u**2 - x_value**2) - 5 * u - x_value),
    x_value,
)
assert fibre_polynomial.degree() <= 2
assert fibre_polynomial.coeff_monomial(x_value) == -1


# ---------------------------------------------------------------------------
# Exact census and application audit.
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

accepted_before = {
    profile(doubles=11),
    profile(doubles=10),
    (4, 4) + (3,) * 5,
    profile(triples=5, doubles=4),
    profile(triples=4, doubles=5),
    profile(triples=5, doubles=3),
    profile(triples=4, doubles=4),
    profile(triples=3, doubles=4),
    profile(triples=4, doubles=1),
    profile(triples=3, doubles=7),
}
assert accepted_before <= frozen and len(accepted_before) == 10
open_before = frozen - accepted_before
assert len(open_before) == 34

expected_nonapplicable = {profile(triples=2, doubles=8)}
kernel_applicable = {candidate for candidate in open_before if selection_types(candidate)}
assert open_before - kernel_applicable == expected_nonapplicable
assert len(kernel_applicable) == 33

zero_orbits_audited = 0
individual_choices = 0
linear_applications = {}
for candidate in open_before:
    triples = candidate.count(3)
    doubles = candidate.count(2)
    singletons = candidate.count(1)
    for d, selected_triples, signature in selection_types(candidate):
        zero_orbits_audited += audit_legal_graph(candidate, d, selected_triples)
        s = 10 - 2 * d
        individual_choices += (
            comb(triples, selected_triples)
            * comb(doubles, d - selected_triples)
            * comb(singletons, s)
        )
        if len(signature) == 5:
            assert candidate not in linear_applications
            linear_applications[candidate] = (d, selected_triples, signature)

signature_singleton = (3, 3, 3, 3, 1)
signature_two_doubles = (3, 3, 3, 2, 2)
expected_singleton_targets = {
    profile(triples=5, doubles=2),
    profile(triples=5, doubles=1),
    profile(triples=5, doubles=0),
    profile(triples=4, doubles=3),
    profile(triples=4, doubles=2),
    profile(triples=4, doubles=0),
}
expected_double_targets = {
    profile(triples=3, doubles=6),
    profile(triples=3, doubles=3),
    profile(triples=3, doubles=2),
}
assert set(linear_applications) == expected_singleton_targets | expected_double_targets
assert {
    candidate
    for candidate, (_, _, signature) in linear_applications.items()
    if signature == signature_singleton
} == expected_singleton_targets
assert {
    candidate
    for candidate, (_, _, signature) in linear_applications.items()
    if signature == signature_two_doubles
} == expected_double_targets

new_closures = expected_singleton_targets | {profile(triples=3, doubles=6)}
explicitly_unclosed_linear = {
    profile(triples=3, doubles=3),
    profile(triples=3, doubles=2),
}
assert len(new_closures) == 7
assert set(linear_applications) == new_closures | explicitly_unclosed_linear

# For the double-complement profiles the number of other double values is
# q-1.  A quadratic fibre is contradictory exactly for the q=6 case here;
# q=3 and q=2 do not supply three distinct fibre points.
for candidate in expected_double_targets:
    doubles = candidate.count(2)
    d, selected_triples, signature = linear_applications[candidate]
    assert selected_triples == 0 and signature == signature_two_doubles
    assert doubles == d + 2
    if candidate in new_closures:
        assert doubles - 1 >= 3
    else:
        assert doubles - 1 < 3

# The theorem also recovers two earlier routes, without new credit.
recovered = {
    profile(triples=4, doubles=1),
    profile(triples=3, doubles=4),
}
for candidate in recovered:
    signatures = {item[2] for item in selection_types(candidate)}
    assert signatures & {signature_singleton, signature_two_doubles}

accepted_after = accepted_before | new_closures
open_after = frozen - accepted_after
assert len(accepted_after) == 17
assert len(open_after) == 27
assert profile(doubles=9) in open_after
assert explicitly_unclosed_linear <= open_after


print("k=5 unified pair-drop linear-plane closures: PASS")
print("kernel parameters: d=0..4, including the one-missing-edge case")
print(
    f"census audit: {len(kernel_applicable)}/34 open profiles kernel-applicable; "
    f"{len(linear_applications)} linear targets"
)
print(
    f"selection audit: {individual_choices} individual choices in "
    f"{zero_orbits_audited} zero-placement orbits"
)
print("new closures: 7; explicitly unclosed linear targets: 2")
print("updated ledger: 17 accepted, 27 open")
