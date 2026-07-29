#!/usr/bin/env python3
"""Exact lightweight audit of the N=8 rank-one clean-cap torus obstruction."""

from collections import Counter
from fractions import Fraction as F
from itertools import combinations

from verify_polarized_paircap_counterexample import (
    C,
    COLORINGS,
    EDGES,
    MATCHINGS,
    paircap_example,
    polarized_coefficients,
    target,
)


def square_free_product(left, right):
    product = {}
    for i, j in EDGES:
        for a in range(C):
            for b in range(C):
                value = left.get((i, a), F(0)) * right.get((j, b), F(0))
                value += right.get((i, a), F(0)) * left.get((j, b), F(0))
                if value:
                    product[((i, j), a, b)] = value
    return product


def add_edges(*families):
    answer = Counter()
    for family in families:
        answer.update(family)
    return {cell: value for cell, value in answer.items() if value}


def hafnian(edge_family):
    answer = {}
    for word in COLORINGS:
        value = F(0)
        for matching in MATCHINGS:
            term = F(1)
            for edge in matching:
                term *= edge_family.get((edge, word[edge[0]], word[edge[1]]), F(0))
            value += term
        answer[word] = value
    return answer


def cubic_sector(old_edges, response_edges, response_count):
    """Cubic matching sector with exactly response_count response edges."""
    answer = {}
    for word in COLORINGS:
        value = F(0)
        for matching in MATCHINGS:
            for chosen in combinations(range(3), response_count):
                term = F(1)
                chosen = set(chosen)
                for index, edge in enumerate(matching):
                    family = response_edges if index in chosen else old_edges
                    term *= family.get((edge, word[edge[0]], word[edge[1]]), F(0))
                value += term
        answer[word] = value
    return answer


def rational_rank(matrix):
    rows = [list(map(F, row)) for row in matrix]
    rank = 0
    for column in range(len(rows[0])):
        pivot = next(
            (row for row in range(rank, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        value = rows[rank][column]
        rows[rank] = [entry / value for entry in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [
                entry - value * pivot_entry
                for entry, pivot_entry in zip(rows[row], rows[rank])
            ]
        rank += 1
    return rank


def audit_rank_one_linear_span():
    # In coordinates t=phi_1/phi_0 and u=phi_2/phi_0, the equal-diagonal
    # rank-one torus has the seven independent coordinates below.
    characters = (
        (0, 0), (-1, 0), (0, -1), (1, 0),
        (1, -1), (0, 1), (-1, 1),
    )
    assert len(set(characters)) == 7

    points = ((2, 3), (2, 5), (3, 2), (3, 5), (5, 2), (5, 3), (5, 7))
    evaluations = [
        [
            F(1),
            F(1, t),
            F(1, u),
            F(t),
            F(t, u),
            F(u),
            F(u, t),
        ]
        for t, u in points
    ]
    assert rational_rank(evaluations) == 7
    return len(characters)


def audit_saturation_certificate():
    # Monomials are exponent triples in (lambda_0, lambda_1, lambda_2).
    lhs = Counter({(2, 1, 1): 1})
    rhs = Counter()
    # lambda_0^2 lambda_2 (lambda_1-lambda_0)
    rhs[(2, 1, 1)] += 1
    rhs[(3, 0, 1)] -= 1
    # lambda_0^3 (lambda_2-lambda_0)
    rhs[(3, 0, 1)] += 1
    rhs[(4, 0, 0)] -= 1
    # lambda_0 * lambda_0^3
    rhs[(4, 0, 0)] += 1
    assert +lhs == +rhs


def main():
    cap_span = audit_rank_one_linear_span()
    q, p_star, q_star, z = paircap_example()
    pq = square_free_product(p_star, q_star)

    # The selected decomposable cap has direct scalar 3, response 3PQ,
    # and raw output (x+3PQ)x^2/2=Delta_6.
    assert z == add_edges(q, {cell: 3 * value for cell, value in pq.items()})
    expected_target = target()
    assert polarized_coefficients(q, z) == expected_target

    # Its canonical effective quadratic is y=x+PQ.
    y = add_edges(q, pq)
    effective = hafnian(y)
    defect = {
        word: 3 * effective[word] - expected_target[word]
        for word in COLORINGS
        if 3 * effective[word] != expected_target[word]
    }
    expected_defect = {
        (1, 0, 0, 1, 0, 0): F(1),
        (2, 0, 1, 1, 0, 2): F(6),
    }
    assert defect == expected_defect

    # For lambda_i=lambda, s=3lambda and E=s^2*(lambda*defect).
    denominator_cleared_error = {
        word: 9 * coefficient for word, coefficient in defect.items()
    }
    assert denominator_cleared_error == {
        (1, 0, 0, 1, 0, 0): F(9),
        (2, 0, 1, 1, 0, 2): F(54),
    }

    # Independently expand E=s*r^2*x/2+r^3/6 at s=3, r=3PQ.
    response = {cell: 3 * value for cell, value in pq.items()}
    two_response = cubic_sector(q, response, 2)
    three_response = cubic_sector(q, response, 3)
    direct_error = {
        word: 3 * two_response[word] + three_response[word]
        for word in COLORINGS
        if 3 * two_response[word] + three_response[word]
    }
    assert direct_error == denominator_cleared_error

    audit_saturation_certificate()
    print(
        "N=8 clean-cap linear-space obstruction: PASS; "
        f"cap span={cap_span}; target words=729; defect support=2; "
        "active saturation power=1"
    )


if __name__ == "__main__":
    main()
