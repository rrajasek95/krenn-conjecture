#!/usr/bin/env python3
"""Exact audit of the common-origin factorization/rank countermodel.

The checker has three independent parts:

1. derive the symbolic six-cycle hafnian and cofactor determinants;
2. verify the rational q, all nine responses, and all nine products
   (p_i q)(s_j q) in the site-square-zero algebra; and
3. verify the distinct-target complementary-triple factorization.

Nothing is inferred numerically.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

import sympy as sp


SITES = tuple(range(6))
EDGES = tuple(combinations(SITES, 2))
TOP = frozenset(SITES)


def hafnian(vertices, edge_values):
    """Recursive hafnian over an arbitrary exact coefficient ring."""
    vertices = tuple(vertices)
    if not vertices:
        return 1
    first = vertices[0]
    answer = 0
    for second in vertices[1:]:
        edge = tuple(sorted((first, second)))
        rest = tuple(v for v in vertices if v not in edge)
        answer += edge_values.get(edge, 0) * hafnian(rest, edge_values)
    return sp.expand(answer) if isinstance(answer, sp.Basic) else answer


def multiply(left, right):
    """Multiply sparse scalar tensors in the site-square-zero algebra."""
    answer = {}
    for support_left, coefficient_left in left.items():
        for support_right, coefficient_right in right.items():
            if support_left & support_right:
                continue
            support = support_left | support_right
            answer[support] = answer.get(support, Fraction(0)) + (
                coefficient_left * coefficient_right
            )
    return {support: value for support, value in answer.items() if value}


def divided_square(q):
    answer = {}
    edge_items = list(q.items())
    for index, (edge_one, value_one) in enumerate(edge_items):
        for edge_two, value_two in edge_items[index + 1 :]:
            if edge_one & edge_two:
                continue
            support = edge_one | edge_two
            answer[support] = answer.get(support, Fraction(0)) + value_one * value_two
    return {support: value for support, value in answer.items() if value}


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for second in vertices[1:]:
        edge = frozenset((first, second))
        rest = tuple(site for site in vertices if site not in edge)
        for matching in perfect_matchings(rest):
            answer.append((edge,) + matching)
    return tuple(answer)


def linear_form(entries):
    return {
        frozenset((site,)): Fraction(value)
        for site, value in entries.items()
        if value
    }


def symbolic_cycle_audit():
    a, b, c, d, e, f = sp.symbols("a b c d e f")
    cycle = (0, 1, 5, 2, 4, 3)
    weights = (a, b, c, d, e, f)
    q = {
        tuple(sorted((cycle[index], cycle[(index + 1) % 6]))): weights[index]
        for index in range(6)
    }
    assert sp.factor(hafnian(SITES, q)) == a * c * e + b * d * f

    left = (0, 5, 4)
    right = (1, 2, 3)
    D = sp.Matrix(
        [
            [
                hafnian(tuple(site for site in SITES if site not in (u, column)), q)
                for column in right
            ]
            for u in left
        ]
    )
    expected = sp.Matrix(
        ((c * e, b * e, b * d), (d * f, a * e, a * d), (c * f, b * f, a * c))
    )
    assert D == expected
    assert sp.factor(D.det()) == (a * c * e - b * d * f) ** 2

    C = sp.zeros(6)
    for u, v in EDGES:
        C[u, v] = C[v, u] = hafnian(
            tuple(w for w in SITES if w not in (u, v)), q
        )
    assert sp.factor(C.det()) == -(a * c * e - b * d * f) ** 4
    on_hafnian_zero = sp.factor(C.det().subs(f, -a * c * e / (b * d)))
    assert on_hafnian_zero == -16 * a**4 * c**4 * e**4


def rational_common_origin_audit():
    q_edges = {
        frozenset((0, 1)): Fraction(2),
        frozenset((1, 5)): Fraction(1),
        frozenset((2, 5)): Fraction(-1),
        frozenset((2, 4)): Fraction(1),
        frozenset((3, 4)): Fraction(1),
        frozenset((0, 3)): Fraction(2),
    }
    q = dict(q_edges)
    F = divided_square(q)

    # The only two perfect matchings have weights -2 and +2.
    matching_ledger = []
    for matching in perfect_matchings(SITES):
        if not all(edge in q for edge in matching):
            continue
        value = Fraction(1)
        for edge in matching:
            value *= q[edge]
        matching_ledger.append((matching, value))
    assert [value for _matching, value in matching_ledger] == [Fraction(-2), Fraction(2)]
    assert sum(value for _matching, value in matching_ledger) == 0
    q_cubed = multiply(q, F)
    assert q_cubed == {}

    C = sp.zeros(6)
    for u, v in EDGES:
        C[u, v] = C[v, u] = F.get(TOP - {u, v}, Fraction(0))
    expected_C = sp.Matrix(
        (
            (0, -1, 1, 1, 0, 0),
            (-1, 0, 0, 0, -2, 2),
            (1, 0, 0, 0, 2, 2),
            (1, 0, 0, 0, -2, 2),
            (0, -2, 2, -2, 0, 0),
            (0, 2, 2, 2, 0, 0),
        )
    )
    assert C == expected_C
    assert C.det() == -256

    p = (
        linear_form({0: 1}),
        linear_form({1: 1}),
        linear_form({2: 1}),
    )
    s = (
        linear_form({1: Fraction(-1, 2), 3: Fraction(1, 2)}),
        linear_form({0: Fraction(-1, 2), 5: Fraction(1, 4)}),
        linear_form({4: Fraction(1, 4), 5: Fraction(1, 4)}),
    )

    inverse = C.inv()
    S = sp.Matrix(
        [
            [form.get(frozenset((site,)), 0) for site in SITES]
            for form in s
        ]
    )
    P = sp.Matrix.hstack(sp.eye(3), sp.zeros(3, 3))
    assert S == inverse[:3, :]
    assert P * C * S.T == sp.eye(3)

    A = tuple(multiply(form, q) for form in p)
    B = tuple(multiply(form, q) for form in s)
    response_matrix = sp.zeros(3)
    factored_matrix = sp.zeros(3)
    for i in range(3):
        for j in range(3):
            response = multiply(multiply(p[i], s[j]), F)
            expected_response = {TOP: Fraction(1)} if i == j else {}
            assert response == expected_response
            response_matrix[i, j] = response.get(TOP, 0)

            factored = multiply(A[i], B[j])
            expected_factored = {TOP: Fraction(2)} if i == j else {}
            assert factored == expected_factored
            factored_matrix[i, j] = factored.get(TOP, 0)
    assert response_matrix == sp.eye(3)
    assert factored_matrix == 2 * sp.eye(3)


def distinct_target_support_audit():
    triples = (
        frozenset((0, 1, 2)),
        frozenset((0, 1, 3)),
        frozenset((0, 2, 3)),
    )
    assert len(set(triples)) == 3
    for i, left in enumerate(triples):
        for j, other_left in enumerate(triples):
            right = TOP - other_left
            if i == j:
                assert not (left & right)
                assert left | right == TOP
            else:
                assert left & right


def main():
    symbolic_cycle_audit()
    rational_common_origin_audit()
    distinct_target_support_audit()
    print("symbolic six-cycle hafnian/cofactor determinant: PASS")
    print("rational common-q 3x3 diagonal factorization: PASS")
    print("independent-target complementary support factorization: PASS")


if __name__ == "__main__":
    main()
