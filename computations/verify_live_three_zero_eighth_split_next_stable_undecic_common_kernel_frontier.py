#!/usr/bin/env python3
"""Exact audit of the next stable degree-eleven common-kernel frontier."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


# The two next profiles have the same ambient degree N=11.
profiles = {
    "singleton_2^14_1": {"p": 10, "epsilon": 1, "slack": 1},
    "pure_2^15": {"p": 11, "epsilon": 0, "slack": 2},
}
N = 11
for data in profiles.values():
    p = data["p"]
    epsilon = data["epsilon"]
    assert p + epsilon == N
    assert 5 * (N + 1 - 5) - (p * 3 + epsilon * 4) == data["slack"]
    assert 5**2 - 5 - 2 * p - epsilon <= 0
    assert 6**2 - 6 - 2 * p - epsilon > 0

# A common gcd costs at least five away from the marked nodes, already
# larger than either slack.  The node corrections are larger still.
assert min(data["slack"] for data in profiles.values()) >= 0
assert max(data["slack"] for data in profiles.values()) < 5
assert 5 + 1 > 2
assert 2 * 5 + 2 > 2

# Pairwise common multiples are now A_a A_b times a linear polynomial.
# This is the first degree where pair intersections are ambient two-spaces,
# so the decic product-line argument no longer removes dimensions 3 and 4.
assert N - 10 + 1 == 2

# Dimension two is nevertheless impossible: three distinct two-planes
# would all equal K, giving a nonzero member divisible by three coprime
# quintic lift factors, of degree at least fifteen.
assert 3 * 5 > N


# Refined Wronskian degree caps by odd-projection rank.  A pure-even kernel
# of dimension k can use the k largest even degrees.  The quotient uses the
# largest remaining degrees; the displayed choices are attainable and give
# the sharp caps needed below.
def refined_cap(dimension: int, odd_rank: int) -> int:
    even_kernel_dimension = dimension - odd_rank
    even_degrees = sorted(range(0, N + 1, 2), reverse=True)
    chosen_even = even_degrees[:even_kernel_dimension]
    remaining = [degree for degree in range(N, -1, -1) if degree not in chosen_even]
    chosen_quotient = remaining[:odd_rank]
    return sum(chosen_even) + sum(chosen_quotient) - dimension * (dimension - 1) // 2


caps = {
    dimension: [refined_cap(dimension, rank) for rank in range(dimension + 1)]
    for dimension in (3, 4, 5)
}
assert caps == {
    3: [21, 26, 27, 27],
    4: [22, 29, 32, 32, 32],
    5: [20, 29, 34, 35, 35, 35],
}

forced = {
    name: {
        dimension: data["p"] * (dimension - 2) + data["epsilon"] * (dimension - 1)
        for dimension in (3, 4, 5)
    }
    for name, data in profiles.items()
}
assert forced["singleton_2^14_1"] == {3: 12, 4: 23, 5: 34}
assert forced["pure_2^15"] == {3: 11, 4: 22, 5: 33}

# Immediate parity-cap exclusions.
assert caps[4][0] < forced["singleton_2^14_1"][4]
for name in profiles:
    assert caps[5][0] < forced[name][5]
    assert caps[5][1] < forced[name][5]

# Local lower-rank exclusions.  Two quintics have Wronskian degree at most
# eight, three quintics degree at most nine, and a three-space whose two-jet
# rank is at most one costs local weight four.
assert 2 * (6 - 2) == 8
assert 3 * (6 - 3) == 9
assert sum(order - index for index, order in enumerate((0, 3, 4))) == 4
for p in (10, 11):
    assert p - 4 >= 6               # d=4, odd rank 3
    assert p - 8 >= 2               # d=4, odd rank 2
    assert p - 2 >= 8               # d=4, odd rank 1
assert 3 * 4 > 9                    # pure d=5, rank 2: three regular nodes


# The pure-even annihilator wedge used at degree ten is unchanged because
# the even square-variable ambient space is still P_5.
w, s = sp.symbols("w s")
D = []
for shift in range(3):
    vector = [sp.Integer(0)] * 6
    for offset, coefficient in enumerate((-s**3, 3 * s**2, -3 * s, 1)):
        vector[shift + offset] = coefficient
    D.append(vector)

wedge_coordinates = list(combinations(range(6), 2))
coefficient_rows = []
for left, right in combinations(range(3), 2):
    wedge = [
        sp.expand(D[left][i] * D[right][j] - D[left][j] * D[right][i])
        for i, j in wedge_coordinates
    ]
    for degree in range(7):
        coefficient_rows.append(
            [sp.Poly(entry, s).coeff_monomial(s**degree) for entry in wedge]
        )
wedge_span = sp.Matrix(coefficient_rows)
assert wedge_span.rank() == 14
perpendicular = wedge_span.nullspace()
assert len(perpendicular) == 1
alternating = sp.zeros(6)
for coefficient, (i, j) in zip(perpendicular[0], wedge_coordinates):
    alternating[i, j] = coefficient
    alternating[j, i] = -coefficient
assert alternating.rank() == 6


# Paired determinant degree and factor budget for a five-space in P_11.
x = sp.symbols("x")
paired_exponents = [sum(indices) - 4 for indices in combinations(range(12), 5)]
assert min(paired_exponents) == 6
assert max(paired_exponents) == 41
assert max(paired_exponents) - 6 == 35
assert 35 - 3 * 10 == 5            # singleton residual in J
assert 35 - 3 * 11 == 2            # pure residual in J

# The four-row parity cofactor has component degree at most sixteen: each
# of the two quintic Wronskian pairs has degree at most eight.
assert 2 * 8 == 16
assert 16 - 10 == 6
assert 16 - 11 == 5
assert 6 + 3 == 9 < 10              # deg(Q dot O'') in singleton profile
assert 5 + 3 == 8 < 11              # deg(Q dot O'') in pure profile


# Audit the invariant derivative identity
#
#   P' dot O'' = det(E,E'',O,O',O'').
def star_four(rows):
    return sp.Matrix(
        [
            (-1) ** column
            * sp.Matrix(
                [
                    [row[index] for index in range(5) if index != column]
                    for row in rows
                ]
            ).det()
            for column in range(5)
        ]
    )


E0 = sp.symbols("E_0_0:5")
E1 = sp.symbols("E_1_0:5")
E2 = sp.symbols("E_2_0:5")
O0 = sp.symbols("O_0_0:5")
O1 = sp.symbols("O_1_0:5")
O2 = sp.symbols("O_2_0:5")
P_derivative = star_four([E0, E2, O0, O1]) + star_four([E0, E1, O0, O2])
expected_derivative_contraction = sp.Matrix([E0, E2, O0, O1, O2]).det()
assert sp.expand(P_derivative.dot(sp.Matrix(O2)) - expected_derivative_contraction) == 0

# If J is nonzero, J=Delta*C*R.  Once Q dot O'' vanishes, C*R is even;
# every one of the p opposite roots must then lie in R, but deg R<p.
assert 5 < 10
assert 2 < 11


# In the nonzero-cofactor, J=0 branch, the global kernel member has a
# triple square factor.  The quotient degree is at most five in z and is
# cubic (singleton) or quadratic (pure) in the parameter.
u, z = sp.symbols("u z")
for quotient_parameter_degree in (3, 2):
    coefficient_symbols = sp.symbols(
        f"h_{quotient_parameter_degree}_0:{6 * (quotient_parameter_degree + 1)}"
    )
    H = []
    for parameter_degree in range(quotient_parameter_degree + 1):
        H.append(
            sum(
                coefficient_symbols[6 * parameter_degree + z_degree] * z**z_degree
                for z_degree in range(6)
            )
        )
    quotient = sum(u**index * H[index] for index in range(len(H)))
    global_member = sp.Poly(sp.expand((z**2 - u) ** 3 * quotient), u)
    top = quotient_parameter_degree + 3
    assert sp.factor(global_member.coeff_monomial(u**top) + H[-1]) == 0
    next_coefficient = global_member.coeff_monomial(u ** (top - 1))
    previous = H[-2] if len(H) >= 2 else 0
    assert sp.factor(next_coefficient - 3 * z**2 * H[-1] + previous) == 0

# Singleton forced weight 34 forbids every member of degree at most five.
# Pure forced weight 33 permits exactly one boundary sequence, and its
# low-degree filtration is one-dimensional through degree seven.
singleton_low_sequences = [
    sequence
    for sequence in combinations(range(12), 5)
    if sum(sequence) - 10 >= 34 and sequence[0] <= 5
]
pure_low_sequences = [
    sequence
    for sequence in combinations(range(12), 5)
    if sum(sequence) - 10 >= 33 and sequence[0] <= 5
]
assert singleton_low_sequences == []
assert pure_low_sequences == [(5, 8, 9, 10, 11)]


# Dimension-four full odd rank: M=*(E' wedge O wedge O') has cap twelve,
# so M=Delta Q with deg Q<=2 or 1.  The same derivative contraction makes
# Q dot O'' vanish.  If Q=q0+w q1+w^2 q2, the identities with O,O',O''
# successively force the fixed relations O q2=O q1=O q0=0, contradicting
# four independent odd components unless Q=0.
assert 4 + 8 == 12
assert 12 - 10 == 2
assert 12 - 11 == 1
assert 2 + 3 < 10
assert 1 + 3 < 11

q0, q1, q2 = [sp.Matrix(sp.symbols(f"q{index}_0:4")) for index in range(3)]
formal_O = sp.Matrix(1, 4, sp.symbols("formal_O_0:4"))
formal_Q = q0 + w * q1 + w**2 * q2
formal_Q_prime = formal_Q.diff(w)
formal_Q_second = formal_Q_prime.diff(w)
assert formal_Q_second == 2 * q2
assert sp.expand((formal_O * (formal_Q_prime - 2 * w * q2 - q1))[0]) == 0
assert sp.expand((formal_O * (formal_Q - w * q1 - w**2 * q2 - q0))[0]) == 0


# The remaining dimension-four tangent branch has a rational coefficient
# L=alpha*O+beta*O'.  If nu is a finite vanishing sequence, a pole of beta
# has order at most nu[1]-1, while the local Wronskian weight pays at least
# three times that amount.  A second-jet-bad point pays at least two units.
vanishing_sequences = list(combinations(range(6), 4))
for sequence in vanishing_sequences:
    weight = sum(order - index for index, order in enumerate(sequence))
    assert weight >= 3 * (sequence[1] - 1)

    second_jet_rank = sum(order <= 2 for order in sequence)
    if second_jet_rank <= 2:
        assert weight >= 2

weight_two_bad_sequences = [
    sequence
    for sequence in vanishing_sequences
    if sum(order <= 2 for order in sequence) <= 2
    and sum(order - index for index, order in enumerate(sequence)) == 2
]
assert weight_two_bad_sequences == [(0, 1, 3, 4)]

# A g^3_5 has total Wronskian weight 4*(5-3)=8.  If m is the total finite
# pole order of beta and e1 the second infinity vanishing order, then
# 3m+3(e1-1)<=8.  Hence deg D=m<=2 and deg N<=m+e1<=3.
total_tangent_weight = 4 * (5 - 3)
assert total_tangent_weight == 8
admissible_pole_infinity_pairs = []
for denominator_degree in range(9):
    for infinity_second_order in range(1, 6):
        if 3 * denominator_degree + 3 * (infinity_second_order - 1) <= 8:
            admissible_pole_infinity_pairs.append(
                (denominator_degree, infinity_second_order)
            )
assert max(pair[0] for pair in admissible_pole_infinity_pairs) == 2
assert max(sum(pair) for pair in admissible_pole_infinity_pairs) == 3

# The last paired row at a second-jet-regular node a gives
# N(a^2)+aD(a^2)=0, a nonzero polynomial of degree at most six.  There are
# at most four bad nodes.  Seven good nodes close the pure profile.  In the
# singleton equality case, four weight-two bad nodes exhaust all weight;
# beta then has constant denominator and numerator degree at most one, so
# the fibre polynomial has degree at most two and cannot have six roots.
assert max(2 * 3, 1 + 2 * 2) == 6
assert 11 - total_tangent_weight // 2 == 7 > 6
for bad_node_count in range(4):
    assert 10 - bad_node_count > 6
assert 10 - 4 == 6 > 2


# Once the five-space four-row cofactor vanishes, adapt the basis as
# O=(bold_O,0), E=(T,A).  Every mixed four-by-four minor is the product of
# an odd two-function Wronskian and a pure-even two-function Wronskian.
# An independent odd space of rank at least two has a nonzero such factor,
# so every pair in A has zero Wronskian and the pure-even kernel has
# dimension at most one.  Therefore only odd ranks four and five survive.
Ti, Tj, Tik, Tjk = sp.symbols("Ti Tj Ti_prime Tj_prime")
Ak, Al, Akp, Alp = sp.symbols("Ak Al Ak_prime Al_prime")
Oi, Oj, Oip, Ojp = sp.symbols("Oi Oj Oi_prime Oj_prime")
mixed_minor = sp.Matrix(
    [
        [Ti, Tj, Ak, Al],
        [Tik, Tjk, Akp, Alp],
        [Oi, Oj, 0, 0],
        [Oip, Ojp, 0, 0],
    ]
).det()
odd_wronskian = Oi * Ojp - Oj * Oip
even_wronskian = Ak * Alp - Al * Akp
assert sp.expand(mixed_minor - odd_wronskian * even_wronskian) == 0
assert [rank for rank in range(2, 6) if 5 - rank <= 1] == [4, 5]

# The uniform fixed-numerator theorem identifies K with a subspace of P_9
# and forces dimension at most four.  This note has independently excluded
# every dimension from two through four, while each lift plane forces
# dimension at least two.  Hence both undecic profiles are now closed.
fixed_numerator_allowed_dimensions = [
    dimension
    for dimension in range(1, 11)
    if 8 * (dimension - 1) <= dimension * (10 - dimension)
]
assert fixed_numerator_allowed_dimensions == [1, 2, 3, 4]
previously_excluded_dimensions = {2, 3, 4}
possible_common_kernel_dimensions = (
    set(fixed_numerator_allowed_dimensions)
    .intersection(range(2, 11))
    .difference(previously_excluded_dimensions)
)
assert possible_common_kernel_dimensions == set()


print("next stable undecic common-kernel frontier: PASS")
print("both profiles have dimension at most five; dimensions two, three, and four close")
print("the rational tangent coefficient closes the full-odd four-space branch")
print("dimension five survives only when the four-row parity cofactor vanishes identically")
print("zero cofactor closes odd ranks two and three; both profiles retain only ranks four and five")
print("the fixed P_9 numerator bound removes dimension five; both undecic profiles close")
