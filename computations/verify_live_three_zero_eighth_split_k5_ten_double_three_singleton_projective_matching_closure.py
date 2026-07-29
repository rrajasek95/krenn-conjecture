#!/usr/bin/env python3
"""Exact audit for the k=5 profile 2^10 1^3 projective closure."""

from itertools import combinations, product

import sympy as sp


# ---------------------------------------------------------------------------
# Mixed-layer construction and sharp kernel dimensions.
# ---------------------------------------------------------------------------

h, k, M = 8, 5, 23
selected_doubles = 4
selected_singletons = 2
formal_layers = selected_doubles + selected_singletons
formal_roles = 2 * selected_doubles + selected_singletons
pair_drop_count = len(tuple(combinations(range(formal_layers), 2)))

assert M == 2 * h + k + 2
assert (formal_layers, formal_roles, pair_drop_count) == (6, 10, 15)

for lowered_singletons in range(3):
    residual_degree = 3 - lowered_singletons
    lift_degree = 2 * (2 - lowered_singletons) + 3 * lowered_singletons
    assert residual_degree + lift_degree == 7

outside_doubles = 10 - selected_doubles
outside_singletons = 3 - selected_singletons
A_degree = 2 * outside_doubles + outside_singletons
denominator_degree = 6 + 3 * selected_doubles + 2 * selected_singletons
numerator_degree_cap = A_degree + 7
assert (outside_doubles, outside_singletons) == (6, 1)
assert (A_degree, denominator_degree, numerator_degree_cap) == (13, 22, 20)
assert denominator_degree - numerator_degree_cap == 2

# A kernel of dimension at least five violates the unit-gcd Wronskian cap.
unit_deficits = {}
for dimension in range(5, 9):
    forced_weight = 4 * (dimension - 2) + 2 * (dimension - 1)
    degree_cap = dimension * (8 - dimension)
    deficit = forced_weight - degree_cap
    unit_deficits[dimension] = deficit
    assert deficit == dimension**2 - 2 * dimension - 10
    assert deficit > 0

# The parity-reduced dimension-three alternative has a strict deficit for
# every possible allocation among the four double and two singleton nodes.
parity_deficits = []
for r1 in range(selected_doubles + 1):
    for r3 in range(selected_doubles - r1 + 1):
        for absorbed_singletons in range(selected_singletons + 1):
            deficit = 7 + 5 * r1 + 7 * r3 + 2 * absorbed_singletons
            parity_deficits.append(deficit)
            assert deficit > 0

# Dual-relation degree bookkeeping.
selected_principal_denominator_degree = 3 * selected_doubles + 2 * selected_singletons
relation_numerator_degree_cap = 7
contact_degree = 2 * selected_doubles + selected_singletons
relation_image_degree_cap = A_degree - contact_degree
leading_coefficient_at_cap = relation_numerator_degree_cap + 6 - A_degree
assert selected_principal_denominator_degree == 16
assert (contact_degree, relation_image_degree_cap) == (10, 3)
assert leading_coefficient_at_cap == 0


# ---------------------------------------------------------------------------
# Exact local residue rows and quotient coordinates.
# ---------------------------------------------------------------------------

z = sp.symbols("z")
B0, B1, B2 = sp.symbols("B0 B1 B2", nonzero=True)
S0, S1, S2 = sp.symbols("S0 S1 S2")

Bjet = B0 + B1 * z + B2 * z**2 / 2
Sjet = S0 + S1 * z + S2 * z**2 / 2
order_two_residue = sp.expand(Bjet * Sjet).coeff(z, 1)
order_three_residue = sp.expand(Bjet * Sjet).coeff(z, 2)
p = B1 / B0
U = B2 / B0
assert sp.simplify(order_two_residue / B0 - (S1 + p * S0)) == 0
assert sp.simplify(2 * order_three_residue / B0 - (S2 + 2 * p * S1 + U * S0)) == 0

robin, x = sp.symbols("robin x")
p, Jjet = sp.symbols("p Jjet")
U = p**2 + Jjet
hrow = U - robin * (2 * p + x * U)
l2 = 2 + 4 * x * p + x**2 * U
l3 = 6 * x + 6 * x**2 * p + x**3 * U

c0, c2, c3, w = sp.symbols("c0 c2 c3 w")
quotient_cubic = c0 * (1 - robin * w) + c2 * w**2 + c3 * w**3
double_row = (
    sp.diff(quotient_cubic, w, 2)
    + 2 * p * sp.diff(quotient_cubic, w)
    + U * quotient_cubic
)
double_row_at_x = sp.expand(double_row.subs(w, x))
assert sp.expand(double_row_at_x.coeff(c0) - hrow) == 0
assert sp.expand(double_row_at_x.coeff(c2) - l2) == 0
assert sp.expand(double_row_at_x.coeff(c3) - l3) == 0


# ---------------------------------------------------------------------------
# Fourth Boolean difference of the quotient-row minor.
# ---------------------------------------------------------------------------

y = sp.symbols("y")
p0, q0, j0, k0 = sp.symbols("p0 q0 j0 k0")
alpha = sp.symbols("alpha0:4")
beta = sp.symbols("beta0:4")
delta_j = sp.symbols("delta_j0:4")
delta_k = sp.symbols("delta_k0:4")


def quotient_tail(node, logjet, derivative_jet):
    second = logjet**2 + derivative_jet
    return (
        2 + 4 * node * logjet + node**2 * second,
        6 * node + 6 * node**2 * logjet + node**3 * second,
    )


mixed_difference = 0
for bits in product((0, 1), repeat=4):
    pp = p0 + sum(bits[i] * alpha[i] for i in range(4))
    qq = q0 + sum(bits[i] * beta[i] for i in range(4))
    jj = j0 + sum(bits[i] * delta_j[i] for i in range(4))
    kk = k0 + sum(bits[i] * delta_k[i] for i in range(4))
    l2u, l3u = quotient_tail(x, pp, jj)
    l2v, l3v = quotient_tail(y, qq, kk)
    minor = l2u * l3v - l3u * l2v
    mixed_difference += (-1) ** (4 - sum(bits)) * minor

middle_coefficient = sum(
    alpha[i]
    * alpha[j]
    * sp.prod(beta[index] for index in range(4) if index not in (i, j))
    for i, j in combinations(range(4), 2)
)
assert sp.expand(
    mixed_difference
    + 4 * x**2 * y**2 * (x - y) * middle_coefficient
) == 0


# ---------------------------------------------------------------------------
# Phi increments and the common-collision pair map.
# ---------------------------------------------------------------------------

u, v, a, b = sp.symbols("u v a b")


def Phi(anchor, point):
    return (5 * anchor + point) / (anchor**2 - point**2)


phi_difference = sp.factor(Phi(u, a) - Phi(u, b))
expected_difference = (
    (a - b)
    * (a * b + 5 * u * (a + b) + u**2)
    / ((u**2 - a**2) * (u**2 - b**2))
)
assert sp.simplify(phi_difference - expected_difference) == 0

Hu = a * b + 5 * u * (a + b) + u**2
Hv = a * b + 5 * v * (a + b) + v**2
assert sp.factor(Hu - Hv) == (u - v) * (u + v + 5 * a + 5 * b)
common_sum = -(u + v) / 5
assert sp.expand(Hu.subs(a + b, common_sum)) == a * b - u * v

# In (sum, product) coordinates tau(s,p)=(-s/5,p) is injective.  If its
# image overlaps its input pair, or if an iterate closes a cycle, the pair
# has sum zero, forbidden by the no-opposite hypothesis.
s, pair_product = sp.symbols("s pair_product")
tau_matrix = sp.diag(sp.Rational(-1, 5), 1)
assert tau_matrix.det() == sp.Rational(-1, 5)
assert sp.solve(sp.Eq(s, -s / 5), s) == [0]
for cycle_length in range(1, 46):
    assert sp.Rational(-1, 5) ** cycle_length != 1


# ---------------------------------------------------------------------------
# Symbolic projective quadratic pairing.
# ---------------------------------------------------------------------------

aa = sp.symbols("aa0:4")
bb = sp.symbols("bb0:4")


def quadratic_coefficients(first, second):
    return sp.Matrix(
        [[
            bb[first] * bb[second],
            aa[first] * bb[second] + bb[first] * aa[second],
            aa[first] * aa[second],
        ]]
    )


pairing = sp.Matrix([[0, 0, 1], [0, 1, 0], [1, 0, 0]])
assert pairing.det() == -1
q01 = quadratic_coefficients(0, 1)
q23 = quadratic_coefficients(2, 3)
paired_value = sp.expand((q01 * pairing * q23.T)[0])
symbolic_middle = sum(
    aa[i]
    * aa[j]
    * sp.prod(bb[index] for index in range(4) if index not in (i, j))
    for i, j in combinations(range(4), 2)
)
assert sp.expand(paired_value - symbolic_middle) == 0

# With two subspaces orthogonal for this nonsingular form, the usual
# dimension formula gives dim(U_X)+dim(U_Y)<=3.  The rank-one side has a
# common unordered factor pair.  When the two factors differ, audit all
# possible two-label assignments on K4: exactly the four star/triangle
# patterns and their label swaps occur.
vertices4 = tuple(range(4))
edges4 = tuple(combinations(vertices4, 2))
edge_index4 = {edge: index for index, edge in enumerate(edges4)}
opposite_pairs4 = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)
opposite_indices4 = tuple(
    (edge_index4[first], edge_index4[second])
    for first, second in opposite_pairs4
)
factor_assignments = {
    bits
    for bits in product((0, 1), repeat=6)
    if all(bits[first] + bits[second] == 1 for first, second in opposite_indices4)
}
star_triangle_assignments = set()
for center in vertices4:
    star = tuple(
        int(center in edge)
        for edge in edges4
    )
    star_triangle_assignments.add(star)
    star_triangle_assignments.add(tuple(1 - bit for bit in star))
assert len(factor_assignments) == 8
assert factor_assignments == star_triangle_assignments


# ---------------------------------------------------------------------------
# Solver-free equality backtrack for the K8 lemma.
# ---------------------------------------------------------------------------

vertices8 = tuple(range(8))
edges8 = tuple(combinations(vertices8, 2))
edge_index8 = {edge: index for index, edge in enumerate(edges8)}
five_sets8 = tuple(combinations(vertices8, 5))

# A split is represented once, by the side containing vertex zero.
splits8 = tuple(
    (side, tuple(vertex for vertex in vertices8 if vertex not in side))
    for side in combinations(vertices8, 4)
    if 0 in side
)
assert len(splits8) == 35


def star_triangle_pattern(side, center):
    remainder = tuple(vertex for vertex in side if vertex != center)
    star = tuple(
        edge_index8[tuple(sorted((center, vertex)))]
        for vertex in remainder
    )
    triangle = tuple(
        edge_index8[edge]
        for edge in combinations(remainder, 2)
    )
    return star, triangle


split_patterns8 = tuple(
    tuple(
        star_triangle_pattern(side, center)
        for side in split
        for center in side
    )
    for split in splits8
)
assert all(len(patterns) == 8 for patterns in split_patterns8)


def canonical_partition(labels):
    relabel = {}
    return tuple(
        relabel.setdefault(label, len(relabel))
        for label in labels
    )


def merge_pattern(state, pattern):
    parents = list(range(max(state) + 1))

    def find(label):
        while parents[label] != label:
            parents[label] = parents[parents[label]]
            label = parents[label]
        return label

    for group in pattern:
        for position in group[1:]:
            first_root = find(state[group[0]])
            next_root = find(state[position])
            if first_root != next_root:
                parents[next_root] = first_root
    return canonical_partition(find(label) for label in state)


def pattern_holds(state, pattern):
    return all(
        state[group[0]] == state[group[1]] == state[group[2]]
        for group in pattern
    )


def has_monochromatic_k5(state):
    return any(
        len(
            {
                state[edge_index8[edge]]
                for edge in combinations(five_set, 2)
            }
        )
        == 1
        for five_set in five_sets8
    )


initial_partition = tuple(range(len(edges8)))
first_side, _ = splits8[0]
assert first_side == (0, 1, 2, 3)
normalized_partition = merge_pattern(initial_partition, split_patterns8[0][0])
assert sum(
    not any(pattern_holds(normalized_partition, pattern) for pattern in patterns)
    for patterns in split_patterns8
) == 34

dead_states = set()
visited_states = 0


def has_survivor(state):
    """Return whether this branch satisfies all splits without a mono K5."""

    global visited_states
    if has_monochromatic_k5(state):
        return False
    visited_states += 1
    if state in dead_states:
        return False

    unsatisfied = tuple(
        split_index
        for split_index, patterns in enumerate(split_patterns8)
        if not any(pattern_holds(state, pattern) for pattern in patterns)
    )
    if not unsatisfied:
        return True

    # Minimum remaining values: count distinct, immediately viable children.
    # Ties are broken by the fixed lexicographic split order.
    def viable_child_count(split_index):
        return len(
            {
                child
                for pattern in split_patterns8[split_index]
                for child in (merge_pattern(state, pattern),)
                if not has_monochromatic_k5(child)
            }
        )

    chosen_split = min(
        unsatisfied,
        key=lambda split_index: (viable_child_count(split_index), split_index),
    )

    seen_children = set()
    for pattern in split_patterns8[chosen_split]:
        child = merge_pattern(state, pattern)
        if child in seen_children:
            continue
        seen_children.add(child)
        if has_survivor(child):
            return True

    dead_states.add(state)
    return False


assert not has_survivor(normalized_partition)
assert visited_states == 1883
assert len(dead_states) == 1725


# ---------------------------------------------------------------------------
# Cleared quartic fibres.
# ---------------------------------------------------------------------------

fibre_value, Acoef, Bcoef = sp.symbols("fibre_value Acoef Bcoef")
cleared_fibre = sp.expand(
    Bcoef * (5 * u + z) * (v**2 - z**2)
    - Acoef * (5 * v + z) * (u**2 - z**2)
    - fibre_value * (u**2 - z**2) * (v**2 - z**2)
)
assert sp.Poly(cleared_fibre, z).degree() <= 4
assert sp.expand(
    cleared_fibre.subs(z, u) - 6 * Bcoef * u * (v - u) * (v + u)
) == 0
assert sp.expand(
    cleared_fibre.subs(z, v) - 6 * Acoef * v * (v - u) * (v + u)
) == 0


print("k=5 ten-double/three-singleton projective matching closure: PASS")
print(f"unit-gcd deficits: {unit_deficits}")
print(f"equality backtrack: {visited_states} visits, {len(dead_states)} dead states")
