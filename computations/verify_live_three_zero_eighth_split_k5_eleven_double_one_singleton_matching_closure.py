#!/usr/bin/env python3
"""Exact audit for the k=5 profile 2^11 1 matching closure."""

from itertools import combinations, product

import sympy as sp


# ---------------------------------------------------------------------------
# Formal-five and Wronskian degrees.
# ---------------------------------------------------------------------------

h, k, M = 8, 5, 23
selected_doubles = 5
outside_doubles = 11 - selected_doubles
outside_singletons = 1
complement_degree = 2 * outside_doubles + outside_singletons
complement_roots = outside_doubles + outside_singletons
relation_degree = complement_roots - 4
wronskian_degree = 2 * relation_degree - 2
residual_degree = wronskian_degree - outside_singletons

assert M == 2 * h + k + 2
assert (outside_doubles, complement_degree, complement_roots) == (6, 13, 7)
assert (relation_degree, wronskian_degree, residual_degree) == (3, 4, 3)


# ---------------------------------------------------------------------------
# Exact local residue rows and their quotient coordinates.
# ---------------------------------------------------------------------------

z = sp.symbols("z")
B0, B1, B2 = sp.symbols("B0 B1 B2", nonzero=True)
S0, S1, S2 = sp.symbols("S0 S1 S2")

# Taylor coefficients at a pole: B=B0+B1 z+B2 z^2/2 and similarly for S.
B = B0 + B1 * z + B2 * z**2 / 2
S = S0 + S1 * z + S2 * z**2 / 2
order_two_residue = sp.expand(B * S).coeff(z, 1)
order_three_residue = sp.expand(B * S).coeff(z, 2)
p = B1 / B0
U = B2 / B0
assert sp.simplify(order_two_residue / B0 - (S1 + p * S0)) == 0
assert sp.simplify(2 * order_three_residue / B0 - (S2 + 2 * p * S1 + U * S0)) == 0

A, x = sp.symbols("A x")
p, J = sp.symbols("p J")
U = p**2 + J
hrow = U - A * (2 * p + x * U)
l2 = 2 + 4 * x * p + x**2 * U
l3 = 6 * x + 6 * x**2 * p + x**3 * U

c0, c2, c3, w = sp.symbols("c0 c2 c3 w")
Sq = c0 * (1 - A * w) + c2 * w**2 + c3 * w**3
Lq = sp.diff(Sq, w, 2) + 2 * p * sp.diff(Sq, w) + U * Sq
Lqx = sp.expand(Lq.subs(w, x))
assert sp.expand(Lqx.coeff(c0) - hrow) == 0
assert sp.expand(Lqx.coeff(c2) - l2) == 0
assert sp.expand(Lqx.coeff(c3) - l3) == 0


# ---------------------------------------------------------------------------
# Fourth Boolean difference of the quotient-row minor.
# ---------------------------------------------------------------------------

y = sp.symbols("y")
p0, q0, j0, k0 = sp.symbols("p0 q0 j0 k0")
alpha = sp.symbols("alpha0:4")
beta = sp.symbols("beta0:4")
delta_j = sp.symbols("delta_j0:4")
delta_k = sp.symbols("delta_k0:4")


def quotient_tail(node, logjet, derivjet):
    second = logjet**2 + derivjet
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

S22 = sum(
    alpha[i] * alpha[j]
    * sp.prod(beta[k_] for k_ in range(4) if k_ not in (i, j))
    for i, j in combinations(range(4), 2)
)
assert sp.expand(mixed_difference + 4 * x**2 * y**2 * (x - y) * S22) == 0


# ---------------------------------------------------------------------------
# The Phi fibre and common-zero identities.
# ---------------------------------------------------------------------------

u, v, a, b = sp.symbols("u v a b")


def Phi(anchor, point):
    return (5 * anchor + point) / (anchor**2 - point**2)


phi_difference = sp.factor(Phi(u, a) - Phi(u, b))
expected_difference = (
    (a - b) * (a * b + 5 * u * (a + b) + u**2)
    / ((u**2 - a**2) * (u**2 - b**2))
)
assert sp.simplify(phi_difference - expected_difference) == 0

Hu = a * b + 5 * u * (a + b) + u**2
Hv = a * b + 5 * v * (a + b) + v**2
assert sp.factor(Hu - Hv) == (u - v) * (u + v + 5 * a + 5 * b)
common_sum = -(u + v) / 5
assert sp.expand(Hu.subs(a + b, common_sum)) == a * b - u * v


# ---------------------------------------------------------------------------
# K7 three-matching incidence ranks after deleting a matching.
# ---------------------------------------------------------------------------


def is_matching(edges):
    return len({vertex for edge in edges for vertex in edge}) == 2 * len(edges)


vertices7 = tuple(range(7))
edges7 = list(combinations(vertices7, 2))
incidence_ranks = []
for deleted_size in range(4):
    deleted = {(2 * i, 2 * i + 1) for i in range(deleted_size)}
    columns = [edge for edge in edges7 if edge not in deleted]
    matchings = [
        matching
        for matching in combinations(columns, 3)
        if is_matching(matching)
    ]
    column_index = {edge: index for index, edge in enumerate(columns)}
    matrix = sp.zeros(len(matchings), len(columns))
    for row_index, matching in enumerate(matchings):
        for edge in matching:
            matrix[row_index, column_index[edge]] = 1
    rank = matrix.rank()
    incidence_ranks.append(rank)
    assert rank == len(columns) == 21 - deleted_size

assert incidence_ranks == [21, 20, 19, 18]


# ---------------------------------------------------------------------------
# Nonexceptional triples used in the projective propagation.
# ---------------------------------------------------------------------------

aa, bb, cc, tt = sp.symbols("aa bb cc tt")


def e1(values):
    return sum(values)


def e2(values):
    return sum(values[i] * values[j] for i, j in combinations(range(len(values)), 2))


good_pair = aa**2 + aa * bb + bb**2
assert sp.expand(e2((aa, bb, -aa - bb)) + good_pair) == 0
assert sp.expand(e2((-2 * tt, tt, tt)) + 3 * tt**2) == 0

# If all four three-submatchings had e1=0, the coefficient matrix is
# J_4-I_4 and is invertible in characteristic zero.
triple_sum_matrix = sp.ones(4, 4) - sp.eye(4)
assert triple_sum_matrix.det() == -3

# If every pair in a nonzero triple had x^2+xy+y^2=0, the ratios would be
# the two distinct primitive cube roots and the triple would have e1=e2=0.
omega = sp.symbols("omega")
cyclotomic = sp.Poly(omega**2 + omega + 1, omega)
assert sp.rem(sp.Poly(1 + omega + omega**2, omega), cyclotomic) == 0
assert sp.rem(sp.Poly(omega + omega**2 + omega**3, omega), cyclotomic) == 0
assert sp.rem(sp.Poly(3 * omega**2, omega), cyclotomic) != 0


# ---------------------------------------------------------------------------
# One-forbidden-edge placement audit.
# ---------------------------------------------------------------------------


class UnionFind:
    def __init__(self, elements):
        self.parent = {element: element for element in elements}

    def find(self, element):
        parent = self.parent[element]
        if parent != element:
            self.parent[element] = self.find(parent)
        return self.parent[element]

    def union(self, first, second):
        first_root = self.find(first)
        second_root = self.find(second)
        if first_root != second_root:
            self.parent[second_root] = first_root


vertices9 = tuple(range(9))
all_edges9 = list(combinations(vertices9, 2))
base_a = (0, 1)
base_b = (2, 3)
five_set = set(range(4, 9))


def impose_complement_triangle(uf, used_edges, forbidden):
    remaining = set(vertices9)
    for edge in used_edges:
        remaining.difference_update(edge)
    triangle = [
        edge for edge in combinations(sorted(remaining), 2) if edge != forbidden
    ]
    assert len(triangle) >= 2
    for edge in triangle[1:]:
        uf.union(triangle[0], edge)


# The base edges come from an allowed three-matching, so the possible common
# zero is neither base_a nor base_b.  Include the no-common-zero case too.
forbidden_cases = [None] + [
    edge for edge in all_edges9 if edge not in (base_a, base_b)
]
assert len(forbidden_cases) == 35

for forbidden in forbidden_cases:
    allowed = [edge for edge in all_edges9 if edge != forbidden]
    uf = UnionFind(allowed)
    internal = [
        edge for edge in combinations(sorted(five_set), 2) if edge != forbidden
    ]

    # Stage 1: triples (a,b,d), nonexceptional because good_pair != 0.
    for edge in internal:
        impose_complement_triangle(uf, (base_a, base_b, edge), forbidden)
    internal_root = uf.find(internal[0])
    assert all(uf.find(edge) == internal_root for edge in internal)

    # Stage 2: triples (a,t,t) and (b,t,t), nonexceptional for t != 0.
    for base in (base_a, base_b):
        for first, second in combinations(internal, 2):
            if is_matching((base, first, second)):
                impose_complement_triangle(
                    uf, (base, first, second), forbidden
                )

    a_root = uf.find(base_a)
    b_root = uf.find(base_b)
    internal_root = uf.find(internal[0])
    for endpoint in base_a:
        for vertex in five_set:
            edge = tuple(sorted((endpoint, vertex)))
            if edge != forbidden:
                assert uf.find(edge) == a_root
    for endpoint in base_b:
        for vertex in five_set:
            edge = tuple(sorted((endpoint, vertex)))
            if edge != forbidden:
                assert uf.find(edge) == b_root

    # Stage 3: triples (a,b,t), nonexceptional because good_pair != 0.
    a_edges = [edge for edge in allowed if uf.find(edge) == a_root]
    b_edges = [edge for edge in allowed if uf.find(edge) == b_root]
    t_edges = [edge for edge in allowed if uf.find(edge) == internal_root]
    used_stage_three = 0
    for edge_a in a_edges:
        for edge_b in b_edges:
            for edge_t in t_edges:
                if is_matching((edge_a, edge_b, edge_t)):
                    impose_complement_triangle(
                        uf, (edge_a, edge_b, edge_t), forbidden
                    )
                    used_stage_three += 1
    assert used_stage_three > 0
    assert uf.find(base_a) == uf.find(base_b) == uf.find(internal[0])

    # In fact the exact propagation joins every allowed edge.  A final
    # four-matching therefore has four equal nonzero labels and e2=6t^2.
    common_root = uf.find(base_a)
    assert all(uf.find(edge) == common_root for edge in allowed)
    final_matchings = [
        matching
        for matching in combinations(allowed, 4)
        if is_matching(matching)
    ]
    assert final_matchings


assert sp.expand(e2((tt, tt, tt, tt)) - 6 * tt**2) == 0

print("k=5 eleven-double/one-singleton matching closure: PASS")
print("K7 incidence ranks:", incidence_ranks)
print("forbidden-edge placements audited:", len(forbidden_cases))
