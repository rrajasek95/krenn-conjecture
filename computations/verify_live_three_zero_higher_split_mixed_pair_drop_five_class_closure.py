#!/usr/bin/env python3
"""Exact arithmetic audit of the uniform mixed pair-drop five-class lemma."""

from __future__ import annotations

import sympy as sp


def profile(triples: int, doubles: int, singletons: int) -> tuple[int, ...]:
    return (3,) * triples + (2,) * doubles + (1,) * singletons


def complement(
    candidate: tuple[int, ...], d: int, selected_triples: int
) -> tuple[int, ...]:
    s = H + 2 - 2 * d
    selected_doubles = d - selected_triples
    answer = (
        [3] * (candidate.count(3) - selected_triples)
        + [2] * (candidate.count(2) - selected_doubles)
        + [1] * (candidate.count(1) - s + selected_triples)
    )
    return tuple(sorted(answer, reverse=True))


# Symbolic identities in h,d,k.
h, d, k, n = sp.symbols("h d k n", integer=True)
s = h + 2 - 2 * d
layers = h + 2 - d
D = h + 3 - d
assert sp.expand(2 * d + s - (h + 2)) == 0
assert sp.expand(d + s - layers) == 0
assert sp.expand(2 * d + 3 * s - (3 * h + 6 - 4 * d)) == 0
assert sp.expand((4 + n) + (layers - n - 3) - D) == 0
assert sp.expand(3 * d + 2 * s - (2 * h + 4 - d)) == 0
assert sp.expand(2 * d + s - (h + 2)) == 0
assert sp.expand(n + (k + 1) - (h + k) - (n + 1 - h)) == 0


# Every admissible d has enough legal-neighbor degree for h >= 8.  Check a
# broad exact integer range, including both parities and boundary d values.
qualifying_pairs = []
for H in range(8, 201):
    for formal_doubles in range((H + 2) // 2 + 1):
        singletons = H + 2 - 2 * formal_doubles
        degree_cap = H + 3 - formal_doubles
        total_factor_degree = 3 * H + 6 - 4 * formal_doubles
        assert total_factor_degree > degree_cap
        assert total_factor_degree - 3 > degree_cap
        if singletons:
            # This is the worst endpoint of the unique possibly missing
            # triple--zero edge.
            assert total_factor_degree - 5 > degree_cap

        lhs0 = 2 * singletons
        rhs0 = 3 * (degree_cap // 2 - 2)
        if lhs0 > rhs0:
            qualifying_pairs.append((H, formal_doubles))
            for absorbed in range(singletons + 1):
                square_degree = degree_cap // 2 - absorbed
                lhs = 2 * (singletons - absorbed)
                rhs = 3 * (square_degree - 2)
                assert lhs - rhs == (lhs0 - rhs0) + absorbed
                assert lhs > rhs


# At h=8 the strict inequality includes exactly d=0,...,4 among the
# singleton-bearing choices used by the theorem.
assert [d0 for h0, d0 in qualifying_pairs if h0 == 8] == [0, 1, 2, 3, 4]


# Relation count and target degree.  A four-dimensional lift span supplies
# at least two row relations; five complementary roots give P_1.
for H in range(8, 80):
    for formal_doubles in range((H + 2) // 2 + 1):
        singletons = H + 2 - 2 * formal_doubles
        if 2 * singletons <= 3 * ((H + 3 - formal_doubles) // 2 - 2):
            continue
        degree_cap = H + 3 - formal_doubles
        row_count = H + 2 - formal_doubles
        ambient_dimension = degree_cap + 1
        minimum_relations = row_count - (ambient_dimension - 4)
        assert minimum_relations == 2
        selected_denominator_degree = 3 * formal_doubles + 2 * singletons
        numerator_degree = (
            selected_denominator_degree - ambient_dimension - 1
        )
        assert numerator_degree == H - 1
        for common_order in range(1, 20):
            complement_degree = H + common_order
            assert (H - 1) + (common_order + 1) - complement_degree == 0
        complementary_classes = 5
        e_degree_cap = complementary_classes + H - 2
        contact_degree = H + 2
        assert e_degree_cap - contact_degree == 1


# Exact h=8,k=5 applications with simple five-class complement.
H = 8
applications = {
    profile(5, 2, 4): (3, 1),
    profile(5, 1, 6): (2, 1),
    profile(5, 0, 8): (1, 1),
    profile(4, 3, 5): (3, 0),
    profile(4, 2, 7): (2, 0),
    profile(4, 0, 11): (0, 0),
}
for candidate, (formal_doubles, selected_triples) in applications.items():
    assert sum(candidate) == 2 * H + 5 + 2 == 23
    selected_singletons = H + 2 - 2 * formal_doubles
    assert candidate.count(1) >= selected_singletons
    assert candidate.count(2) >= formal_doubles - selected_triples
    remaining = complement(candidate, formal_doubles, selected_triples)
    assert remaining == (3, 3, 3, 3, 1)
    assert 2 * selected_singletons > 3 * (
        (H + 3 - formal_doubles) // 2 - 2
    )


# The local simple-pole contradiction with S=z-r.
z, root = sp.symbols("z root")
b0, b1, b2 = sp.symbols("b0 b1 b2", nonzero=True)
local = z - root
unit = b0 + b1 * local + b2 * local**2
assert sp.diff(unit * local, z).subs(z, root) == b0


print("higher-split mixed pair-drop five-class closure: PASS")
print(f"strict (h,d) pairs audited through h=200: {len(qualifying_pairs)}")
print("neighbor-degree and absorbed-singleton inequalities: exact")
print("all six h=8,k=5 simple-complement applications: exact")
