#!/usr/bin/env python3
"""Exact checks for the sitewise common-power response filtration.

The general ideal argument is proved in the companion note.  This checker
audits its finite Cauchy--Binet incidence ledger, the compound/adjugate
identities, and the exact one-site lift of the scalar six-cycle.
"""

from collections import Counter
from itertools import combinations, permutations, product

import sympy as sp


U = tuple(range(6))
triples = tuple(combinations(U, 3))


def nonzero_cofactor_permutations(rows, cols):
    """Permutations indexing terms that avoid the zero diagonal of C."""

    for perm in permutations(cols):
        if all(row != col for row, col in zip(rows, perm)):
            yield perm


# In every nonzero Cauchy--Binet monomial, site u is absent from one C
# factor for a selected P column and from one for a selected S column.
pattern_histogram = Counter()
term_count = 0
for rows in triples:
    for cols in triples:
        perms = tuple(nonzero_cofactor_permutations(rows, cols))
        if not perms:
            continue
        exponents = tuple(
            3 - int(u in rows) - int(u in cols)
            for u in U
        )
        assert min(exponents) >= 1
        assert sum(exponents) == 12
        overlap = len(set(rows) & set(cols))
        assert exponents.count(1) == overlap
        assert exponents.count(3) == overlap
        assert exponents.count(2) == 6 - 2 * overlap
        pattern_histogram[tuple(sorted(exponents))] += 1
        term_count += len(perms)

assert set(pattern_histogram) == {
    (2, 2, 2, 2, 2, 2),
    (1, 2, 2, 2, 2, 3),
    (1, 1, 2, 2, 3, 3),
    (1, 1, 1, 3, 3, 3),
}

# If every local endpoint span has dimension at most two, the entrywise
# four-cover and the site cover force exactly two axes per site and two
# omissions of each colour.  Audit the integer implication exhaustively.
incidence_vectors = []
for masks in product(range(1, 7), repeat=6):
    # Nonzero 3-bit masks of size at most two.
    if any(mask.bit_count() > 2 for mask in masks):
        continue
    counts = tuple(sum((mask >> c) & 1 for mask in masks) for c in range(3))
    if min(counts) < 4:
        continue
    assert counts == (4, 4, 4)
    assert all(mask.bit_count() == 2 for mask in masks)
    omitted_colours = []
    for mask in masks:
        missing = [c for c in range(3) if not ((mask >> c) & 1)]
        assert len(missing) == 1
        omitted_colours.append(missing[0])
    assert Counter(omitted_colours) == Counter({0: 2, 1: 2, 2: 2})
    incidence_vectors.append(masks)
assert incidence_vectors

# The adjugate of a sum of two rank-one 3x3 matrices.
a = sp.Matrix(sp.symbols("a0:3"))
b = sp.Matrix(sp.symbols("b0:3"))
c = sp.Matrix(sp.symbols("c0:3"))
d = sp.Matrix(sp.symbols("d0:3"))
rank_two = a * c.T + b * d.T
adj_expected = c.cross(d) * a.cross(b).T
assert (rank_two.adjugate() - adj_expected).applyfunc(sp.expand) == sp.zeros(3)

# The second compound of A B^T with two inner columns is an outer product
# of the two wedges.  Use the (01,02,12) minor order.
pairs = ((0, 1), (0, 2), (1, 2))
A = sp.Matrix.hstack(a, b)
B = sp.Matrix.hstack(d, c)  # AB^T = a d^T + b c^T
product = A * B.T
compound = sp.Matrix(
    [[product.extract(I, J).det() for J in pairs] for I in pairs]
)
wedge_A = sp.Matrix([A.extract(I, (0, 1)).det() for I in pairs])
wedge_B = sp.Matrix([B.extract(J, (0, 1)).det() for J in pairs])
assert (compound - wedge_A * wedge_B.T).applyfunc(sp.expand) == sp.zeros(3)

# Exact one-site lift of the scalar six-cycle.
x0, x1, x2 = sp.symbols("x0 x1 x2")
C0 = sp.Matrix(
    [
        [0, -1, 1, 1, 0, 0],
        [-1, 0, 0, 0, -2, 2],
        [1, 0, 0, 0, 2, 2],
        [1, 0, 0, 0, -2, 2],
        [0, -2, 2, -2, 0, 0],
        [0, 2, 2, 2, 0, 0],
    ]
)
C = C0.copy()
for row in range(1, 6):
    for col in range(1, 6):
        C[row, col] *= x2

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
assert sp.expand(response.det() - x0 * x1 * x2) == 0
assert response.adjugate() == sp.diag(x1 * x2, x0 * x2, x0 * x1)

# The two six-cycle matching weights and the local chain vector.
assert 2 * (-1) * 1 + 1 * 1 * 2 == 0
cofactor_row = sp.Matrix([-1, 1, 1, 0, 0])
incident_e2_coefficients = sp.Matrix([2, 0, 2, 0, 0])
assert cofactor_row.dot(incident_e2_coefficients) == 0

# Reconstruct every cofactor entry directly from the six scalar edge
# weights, with the site-zero incident weights carrying x2.
edge = {
    (0, 1): 2 * x2,
    (1, 5): 1,
    (2, 5): -1,
    (2, 4): 1,
    (3, 4): 1,
    (0, 3): 2 * x2,
}


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


reconstructed = sp.zeros(6)
for u in U:
    for v in U:
        if u == v:
            continue
        complement = tuple(w for w in U if w not in (u, v))
        value = 0
        for matching in matchings(complement):
            term = 1
            for left, right in matching:
                term *= edge.get(tuple(sorted((left, right))), 0)
            value += term
        reconstructed[u, v] = sp.expand(value)
assert reconstructed == C

print("sitewise common-power response filtration: PASS")
print("Cauchy--Binet nonzero term count:", term_count)
print("incidence patterns:", dict(sorted(pattern_histogram.items())))
print("rank-at-most-two incidence assignments:", len(incidence_vectors))
print("one-site response:", response)
