#!/usr/bin/env python3
"""Exact audit of the full-rank-site response-invisibility countermodel."""

from fractions import Fraction
from collections import Counter
from itertools import combinations, product

import sympy as sp


# A tensor monomial is a tuple of six local basis labels.  ``None`` means
# that the site is unoccupied.  Site zero has labels 0,1,2; the other five
# sites have their unique line label 0.
ONE = (None,) * 6


def add(*elements):
    out = {}
    for element in elements:
        for monomial, coefficient in element.items():
            out[monomial] = out.get(monomial, Fraction(0)) + coefficient
            if not out[monomial]:
                del out[monomial]
    return out


def scale(coefficient, element):
    coefficient = Fraction(coefficient)
    return {
        monomial: coefficient * value
        for monomial, value in element.items()
        if coefficient * value
    }


def multiply(left, right):
    out = {}
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            if any(
                a is not None and b is not None
                for a, b in zip(monomial_left, monomial_right)
            ):
                continue
            monomial = tuple(
                a if a is not None else b
                for a, b in zip(monomial_left, monomial_right)
            )
            out[monomial] = (
                out.get(monomial, Fraction(0))
                + coefficient_left * coefficient_right
            )
            if not out[monomial]:
                del out[monomial]
    return out


def divided_power(element, degree):
    """Square-free divided power: one unordered choice of ``degree`` atoms."""

    atoms = [({monomial: coefficient}) for monomial, coefficient in element.items()]
    out = {}
    for selected in combinations(atoms, degree):
        term = {ONE: Fraction(1)}
        for atom in selected:
            term = multiply(term, atom)
        out = add(out, term)
    return out


def local(site, basis=0):
    monomial = [None] * 6
    monomial[site] = basis
    return {tuple(monomial): Fraction(1)}


def edge(site_zero_basis, other_site, coefficient=1):
    monomial = [None] * 6
    monomial[0] = site_zero_basis
    monomial[other_site] = 0
    return {tuple(monomial): Fraction(coefficient)}


def scalar_edge(left, right, coefficient=1):
    monomial = [None] * 6
    monomial[left] = monomial[right] = 0
    return {tuple(monomial): Fraction(coefficient)}


# Specialize the response-invisible family to a=e_0 and b=e_1.
q = add(
    edge(0, 1), scale(2, edge(2, 1)), edge(0, 2),
    scale(2, edge(2, 3)), edge(1, 4), edge(1, 5),
    scalar_edge(1, 5), scalar_edge(2, 5, -1),
    scalar_edge(2, 4), scalar_edge(3, 4),
)

p = (
    local(0, 0),
    add(scale(-Fraction(1, 2), local(1)), scale(Fraction(1, 2), local(3))),
    local(4),
)
s = (
    add(scale(-Fraction(1, 2), local(1)), scale(Fraction(1, 2), local(3))),
    local(0, 1),
    add(scale(-Fraction(1, 4), local(1)), scale(-Fraction(1, 4), local(3))),
)

q2 = divided_power(q, 2)
q3 = divided_power(q, 3)
assert q3 == {}

targets = []
for colour in range(3):
    monomial = (colour, 0, 0, 0, 0, 0)
    targets.append({monomial: Fraction(1)})

for i in range(3):
    for j in range(3):
        response = multiply(multiply(p[i], s[j]), q2)
        assert response == (targets[i] if i == j else {})

# The incident endpoint directions at site zero contain all three axes.
incident_directions = {
    (1, 0): Fraction(1),
    (1, 2): Fraction(2),
    (2, 0): Fraction(1),
    (3, 2): Fraction(2),
    (4, 1): Fraction(1),
    (5, 1): Fraction(1),
}
span_matrix = sp.Matrix(
    [
        [incident_directions.get((site, colour), 0) for site in range(1, 6)]
        for colour in range(3)
    ]
)
assert span_matrix.rank() == 3


def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for matching in matchings(rest):
            yield ((first, second),) + matching


# Keep a and b arbitrary under scalar contraction.  A=x(a), B=x(b).
x0, x1, x2, A, B = sp.symbols("x0 x1 x2 A B")
weights = {
    (0, 1): A + 2 * x2,
    (0, 2): A,
    (0, 3): 2 * x2,
    (0, 4): B,
    (0, 5): B,
    (1, 5): sp.Integer(1),
    (2, 5): sp.Integer(-1),
    (2, 4): sp.Integer(1),
    (3, 4): sp.Integer(1),
}

C = sp.zeros(6)
for u in range(6):
    for v in range(6):
        if u == v:
            continue
        complement = tuple(w for w in range(6) if w not in (u, v))
        value = 0
        for matching in matchings(complement):
            term = 1
            for left, right in matching:
                term *= weights.get(tuple(sorted((left, right))), 0)
            value += term
        C[u, v] = sp.expand(value)

expected_C = sp.Matrix(
    [
        [0, -1, 1, 1, 0, 0],
        [-1, 0, B, 0, -2 * x2, A + 2 * x2],
        [1, B, 0, B, 2 * x2, A + 2 * x2],
        [1, 0, B, 0, -2 * x2, A + 2 * x2],
        [0, -2 * x2, 2 * x2, -2 * x2, 0, 0],
        [0, A + 2 * x2, A + 2 * x2, A + 2 * x2, 0, 0],
    ]
)
assert C == expected_C

# Independently recover the full five-vector star-deformation response
# map.  This freezes the simultaneous kernel used in the note instead of
# checking only its two-vector specialization.
t1, t2, t3, t4, t5 = sp.symbols("t1:6")
deformed_weights = dict(weights)
for site, increment in enumerate((t1, t2, t3, t4, t5), start=1):
    deformed_weights[(0, site)] += increment

deformed_C = sp.zeros(6)
for u in range(6):
    for v in range(6):
        if u == v:
            continue
        complement = tuple(w for w in range(6) if w not in (u, v))
        deformed_C[u, v] = sp.expand(
            sum(
                sp.prod(
                    deformed_weights.get(tuple(sorted(edge)), 0)
                    for edge in matching
                )
                for matching in matchings(complement)
            )
        )

# The chain identity is vector-valued; audit its coefficient in the free
# symbols standing for the three components of a,b,e_2.
a_vec = sp.Matrix(sp.symbols("a0:3"))
b_vec = sp.Matrix(sp.symbols("b0:3"))
e2_vec = sp.Matrix([0, 0, 1])
star = (2 * e2_vec + a_vec, a_vec, 2 * e2_vec, b_vec, b_vec)
cofactor_row = (-1, 1, 1, 0, 0)
chain = sum(
    (coefficient * vector for coefficient, vector in zip(cofactor_row, star)),
    sp.zeros(3, 1),
)
assert chain == sp.zeros(3, 1)

P = sp.zeros(3, 6)
P[0, 0] = x0
P[1, 1] = -sp.Rational(1, 2)
P[1, 3] = sp.Rational(1, 2)
P[2, 4] = 1

S = sp.zeros(3, 6)
S[0, 1] = -sp.Rational(1, 2)
S[0, 3] = sp.Rational(1, 2)
S[1, 0] = x1
S[2, 1] = -sp.Rational(1, 4)
S[2, 3] = -sp.Rational(1, 4)

response = (P * C * S.T).applyfunc(sp.expand)
target = sp.diag(x0, x1, x2)
assert response == target
response_change = (P * (deformed_C - C) * S.T).applyfunc(sp.expand)
expected_change = sp.Matrix(
    [
        [0, 0, 0],
        [(t4 - t5) / 2, 0, 0],
        [(-t1 + t2 + t3) / 2, 0, (t1 - t2 + t3) / 4],
    ]
)
assert response_change == expected_change
assert response_change.subs({t1: A, t2: A, t3: 0, t4: B, t5: B}) == sp.zeros(3)
assert response.adjugate() == sp.diag(x1 * x2, x0 * x2, x0 * x1)
assert sp.factor(C.det()) == -64 * x2**2 * (A + 2 * x2) ** 2

print("full-rank-site response-invisibility countermodel: PASS")
print("q atoms / q^[2] atoms:", len(q), len(q2))
print("all nine tensor responses: PASS")
print("five-vector deformation kernel: PASS")
print("incident endpoint rank at site zero:", span_matrix.rank())
print("symbolic response:", response)
print("cofactor determinant:", sp.factor(C.det()))


# ---------------------------------------------------------------------------
# The stronger two-site-separated countermodel.


def two_site_edge(left_basis, right_basis, coefficient=1):
    monomial = [None] * 6
    monomial[0] = left_basis
    monomial[1] = right_basis
    return {tuple(monomial): Fraction(coefficient)}


q_two = add(
    scale(2, two_site_edge(2, 2)),
    two_site_edge(1, 2),
    edge(1, 2),
    scale(2, edge(2, 3)),
    edge(0, 5),
    # Here ``local(1, 2) * local(5)`` is the edge f_2 z_5.
    multiply(local(1, 2), local(5)),
    scalar_edge(2, 5, -1),
    scalar_edge(2, 4),
    scalar_edge(3, 4),
)

p_two = (
    local(0, 0),
    local(1, 1),
    add(local(2), scale(-1, local(3))),
)
s_two = (
    scale(-1, local(1, 0)),
    scale(-1, local(0, 1)),
    scale(Fraction(1, 4), add(local(0, 1), local(4), local(5))),
)

q_two_2 = divided_power(q_two, 2)
q_two_3 = divided_power(q_two, 3)
assert q_two_3 == {}

two_site_targets = [
    {(colour, colour, 0, 0, 0, 0): Fraction(1)}
    for colour in range(3)
]
for i in range(3):
    for j in range(3):
        response_tensor = multiply(multiply(p_two[i], s_two[j]), q_two_2)
        assert response_tensor == (two_site_targets[i] if i == j else {})

# q has target rank three at site zero and target rank one at site one.
site_zero_star = sp.Matrix(
    [
        [0, 0, 0, 0, 1],
        [1, 1, 0, 0, 0],
        [2, 0, 2, 0, 0],
    ]
)
# Columns of the second display are the edge-01 and edge-15 endpoint
# vectors after choosing a site-zero coefficient; both lie on f_2.
site_one_star = sp.Matrix([[0, 0], [0, 0], [1, 1]])
assert site_zero_star.rank() == 3
assert site_one_star.rank() == 1

# Rebuild the two-site cofactor pencil.  A and B are contractions of a
# retained two-vector deformation family; X,Y are x(e_2), y(f_2).  The
# fixed tensor model above is the exact specialization A=x0, B=x1.
X, Y = sp.symbols("X Y")
two_weights = {
    (0, 1): (B + 2 * X) * Y,
    (0, 2): B,
    (0, 3): 2 * X,
    (0, 5): A,
    (1, 5): Y,
    (2, 5): sp.Integer(-1),
    (2, 4): sp.Integer(1),
    (3, 4): sp.Integer(1),
}

C_two = sp.zeros(6)
for u in range(6):
    for v in range(6):
        if u == v:
            continue
        complement = tuple(w for w in range(6) if w not in (u, v))
        C_two[u, v] = sp.expand(
            sum(
                sp.prod(
                    two_weights.get(tuple(sorted(edge_pair)), 0)
                    for edge_pair in matching
                )
                for matching in matchings(complement)
            )
        )

y0, y1 = sp.symbols("y0 y1")
P_two = sp.zeros(3, 6)
P_two[0, 0] = x0
P_two[1, 1] = y1
P_two[2, 2] = 1
P_two[2, 3] = -1

S_two = sp.zeros(3, 6)
S_two[0, 1] = -y0
S_two[1, 0] = -x1
S_two[2, 0] = B / 4
S_two[2, 4] = sp.Rational(1, 4)
S_two[2, 5] = sp.Rational(1, 4)

two_response = (P_two * C_two * S_two.T).applyfunc(sp.expand)
assert two_response == sp.diag(x0 * y0, x1 * y1, X * Y)
assert sp.factor(C_two.det()) == -64 * X**2 * Y**4 * (B + 2 * X) ** 2
fixed_two_response = two_response.subs({A: x0, B: x1, X: x2, Y: sp.Symbol("y2")})
assert fixed_two_response == sp.diag(x0 * y0, x1 * y1, x2 * sp.Symbol("y2"))

# Both vector chain identities.  At site zero, the internal cofactors are
# (-1, f_2, f_2, 0, 0), giving the displayed cancellation.  At site one
# every incident endpoint vector is on f_2, and the same two matching
# packets cancel.
e0v = sp.Matrix([1, 0, 0])
e1v = sp.Matrix([0, 1, 0])
e2v = sp.Matrix([0, 0, 1])
site_zero_chain = (
    -(2 * e2v + e1v) * Y + e1v * Y + 2 * e2v * Y
)
assert site_zero_chain == sp.zeros(3, 1)
f2v = sp.Matrix([0, 0, 1])
site_one_chain = -(B + 2 * X) * f2v + (B + 2 * X) * f2v
assert site_one_chain == sp.zeros(3, 1)


# ---------------------------------------------------------------------------
# Exhaust the equality case of the global rank budget.

rank_type_count = Counter()
overlap_type_count = Counter()
equality_assignments = 0

for masks in product(range(1, 8), repeat=6):
    ranks = tuple(mask.bit_count() for mask in masks)
    if sum(ranks) != 12:
        continue
    colour_counts = tuple(
        sum((mask >> colour) & 1 for mask in masks)
        for colour in range(3)
    )
    if colour_counts != (4, 4, 4):
        continue
    if max(ranks) < 3:
        continue

    equality_assignments += 1
    rank_type = tuple(Counter(ranks)[rank] for rank in (3, 2, 1))
    rank_type_count[rank_type] += 1

    omission_pairs = tuple(
        frozenset(
            site
            for site, mask in enumerate(masks)
            if not ((mask >> colour) & 1)
        )
        for colour in range(3)
    )
    assert all(len(pair) == 2 for pair in omission_pairs)
    intersections = tuple(
        sorted(
            len(omission_pairs[i] & omission_pairs[j])
            for i in range(3)
            for j in range(i + 1, 3)
        )
    )
    coincident_pairs = sum(
        omission_pairs[i] == omission_pairs[j]
        for i in range(3)
        for j in range(i + 1, 3)
    )
    overlap_type_count[(rank_type, intersections, coincident_pairs)] += 1

assert equality_assignments == 2550
assert rank_type_count == Counter(
    {(1, 4, 1): 1080, (2, 2, 2): 1350, (3, 0, 3): 120}
)
assert overlap_type_count == Counter(
    {
        ((1, 4, 1), (0, 0, 1), 0): 1080,
        ((2, 2, 2), (0, 0, 2), 1): 270,
        ((2, 2, 2), (0, 1, 1), 0): 1080,
        ((3, 0, 3), (1, 1, 1), 0): 120,
    }
)

# The quotient right side has flattening rank equal to the number of
# colours sharing P: both its response/quotient factors and its four-site
# pure factors are independent coordinate vectors.  Hence a decomposable
# left side N_P tensor F_P permits at most one such colour.
for number_of_shared_colours in (1, 2, 3):
    quotient_rhs = sp.zeros(3, 3)
    for colour in range(number_of_shared_colours):
        quotient_rhs[colour, colour] = 1
    assert quotient_rhs.rank() == number_of_shared_colours

print("two-site-separated full-rank countermodel: PASS")
print("two-site response:", two_response)
print("two-site cofactor determinant:", sp.factor(C_two.det()))
print("rank-budget equality assignments:", equality_assignments)
print("rank types:", dict(rank_type_count))
print("omission overlap types:", dict(overlap_type_count))
