#!/usr/bin/env python3
"""Exact audit of the one-unused-anchor, all-cycle Hessian guard."""

from collections import Counter
from fractions import Fraction
from itertools import combinations
import sys


if not __debug__:
    raise RuntimeError("run without -O: this audit uses assertions")


A = 0
B = 1
DELTA = 2
VERTICES8 = tuple(range(8))
RESIDUAL = tuple(range(6))
EDGES6 = tuple(combinations(RESIDUAL, 2))
EDGE_INDEX = {pair: index for index, pair in enumerate(EDGES6)}

A_EDGES = {
    (0, 6),
    (1, 7),
    (0, 3),
    (1, 5),
    (2, 3),
    (4, 5),
}
B_EDGES = {(0, 1), (2, 4), (3, 6), (5, 7)}
DELTA_EDGES = {(0, 4), (1, 3), (2, 7), (5, 6)}
QA_SUPPORT = {(0, 3), (1, 5), (2, 3), (4, 5)}
QB_SUPPORT = {(0, 1), (2, 4)}
QDELTA_SUPPORT = {(0, 4), (1, 3)}


def edge(left, right):
    return (left, right) if left < right else (right, left)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return [()]
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(rest):
            answer.append((edge(first, second),) + matching)
    return answer


def rank(matrix):
    rows = [[Fraction(value) for value in row] for row in matrix]
    pivot_row = 0
    for column in range(len(rows[0])):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(rows[row], rows[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def edge_vector(entries):
    answer = [Fraction(0)] * len(EDGES6)
    for pair, value in entries.items():
        answer[EDGE_INDEX[edge(*pair)]] += Fraction(value)
    return answer


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def matvec(matrix, vector):
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def audit_eight_site_signature():
    supported = []
    for matching in perfect_matchings(VERTICES8):
        if all(pair in A_EDGES | B_EDGES for pair in matching):
            colours = tuple(A if pair in A_EDGES else B for pair in matching)
            supported.append((matching, colours))

    assert supported == [
        (((0, 1), (2, 4), (3, 6), (5, 7)), (B, B, B, B)),
        (((0, 6), (1, 7), (2, 3), (4, 5)), (A, A, A, A)),
    ]

    signatures = Counter()
    for matching, colours in supported:
        word = [None] * 8
        for pair, colour in zip(matching, colours):
            word[pair[0]] = colour
            word[pair[1]] = colour
        signatures[tuple(word)] += 1
    assert signatures == Counter({(A,) * 8: 1, (B,) * 8: 1})


def audit_three_diagonal_eight_site_packet():
    edge_colours = {
        **{pair: A for pair in A_EDGES},
        **{pair: B for pair in B_EDGES},
        **{pair: DELTA for pair in DELTA_EDGES},
    }
    supported = [
        matching
        for matching in perfect_matchings(VERTICES8)
        if all(pair in edge_colours for pair in matching)
    ]
    assert len(supported) == 9

    cell_counts = Counter()
    diagonal_signatures = Counter()
    for matching in supported:
        word = [None] * 8
        for pair in matching:
            colour = edge_colours[pair]
            word[pair[0]] = colour
            word[pair[1]] = colour
        cell = (word[6], word[7])
        cell_counts[cell] += 1
        if cell[0] == cell[1]:
            diagonal_signatures[tuple(word)] += 1

    assert diagonal_signatures == Counter(
        {(A,) * 8: 1, (B,) * 8: 1, (DELTA,) * 8: 1}
    )
    assert cell_counts == Counter(
        {
            (A, A): 1,
            (B, B): 1,
            (DELTA, DELTA): 1,
            (A, B): 1,
            (A, DELTA): 1,
            (B, DELTA): 2,
            (DELTA, A): 2,
        }
    )


def residual_q_edges():
    edges = {}
    for pair in QA_SUPPORT:
        edges[pair] = (A, A)
    for pair in QB_SUPPORT:
        edges[pair] = (B, B)
    return edges


def three_colour_residual_q_edges():
    edges = residual_q_edges()
    for pair in QDELTA_SUPPORT:
        edges[pair] = (DELTA, DELTA)
    return edges


P_STARS = {
    A: (0, A),
    B: (3, B),
    DELTA: None,
}
S_STARS = {
    A: (1, A),
    B: (5, B),
    DELTA: None,
}


def response(row, column):
    p_star = P_STARS[row]
    s_star = S_STARS[column]
    if p_star is None or s_star is None or p_star[0] == s_star[0]:
        return Counter()

    occupied = {p_star[0], s_star[0]}
    complement = tuple(site for site in RESIDUAL if site not in occupied)
    answer = Counter()
    q_edges = residual_q_edges()
    for matching in perfect_matchings(complement):
        if not all(pair in q_edges for pair in matching):
            continue
        word = [None] * 6
        word[p_star[0]] = p_star[1]
        word[s_star[0]] = s_star[1]
        for pair in matching:
            left_colour, right_colour = q_edges[pair]
            word[pair[0]] = left_colour
            word[pair[1]] = right_colour
        answer[tuple(word)] += 1
    return answer


THREE_COLOUR_P_STARS = {
    A: (0, A),
    B: (3, B),
    DELTA: (5, DELTA),
}
THREE_COLOUR_S_STARS = {
    A: (1, A),
    B: (5, B),
    DELTA: (2, DELTA),
}


def three_colour_response(row, column):
    p_star = THREE_COLOUR_P_STARS[row]
    s_star = THREE_COLOUR_S_STARS[column]
    if p_star[0] == s_star[0]:
        return Counter()

    occupied = {p_star[0], s_star[0]}
    complement = tuple(site for site in RESIDUAL if site not in occupied)
    answer = Counter()
    q_edges = three_colour_residual_q_edges()
    for matching in perfect_matchings(complement):
        if not all(pair in q_edges for pair in matching):
            continue
        word = [None] * 6
        word[p_star[0]] = p_star[1]
        word[s_star[0]] = s_star[1]
        for pair in matching:
            word[pair[0]], word[pair[1]] = q_edges[pair]
        answer[tuple(word)] += 1
    return answer


def audit_nine_row_ledger_and_cap():
    desired = {
        (A, A): Counter({(A,) * 6: 1}),
        (B, B): Counter({(B,) * 6: 1}),
    }
    for row in (A, B, DELTA):
        for column in (A, B, DELTA):
            actual = response(row, column)
            assert actual == desired.get((row, column), Counter())

    assert response(A, A) == Counter({(A,) * 6: 1})
    assert response(B, B) == Counter({(B,) * 6: 1})
    assert response(DELTA, DELTA) == Counter()

    full_nine_targets = {
        (row, column): (
            Counter({(row,) * 6: 1}) if row == column else Counter()
        )
        for row in (A, B, DELTA)
        for column in (A, B, DELTA)
    }
    satisfied = {
        cell
        for cell, target in full_nine_targets.items()
        if response(*cell) == target
    }
    assert len(satisfied) == 8
    assert set(full_nine_targets) - satisfied == {(DELTA, DELTA)}

    complement = [
        matching
        for matching in perfect_matchings((2, 3, 4, 5))
        if all(pair in QA_SUPPORT for pair in matching)
    ]
    assert complement == [((2, 3), (4, 5))]

    # The E_aa selector is direct-zero because d=0.  Its cap planes contain
    # the a-target exactly at sites 0 and 1, its coefficient on 01 is one,
    # and the corresponding literal transition is 0*0-E_aa=-E_aa.
    assert P_STARS[A] == (0, A)
    assert S_STARS[A] == (1, A)
    cap_planes = {
        site: {
            colour
            for star in (P_STARS[A], S_STARS[A])
            if star is not None and star[0] == site
            for colour in (star[1],)
        }
        for site in RESIDUAL
    }
    assert {site for site, plane in cap_planes.items() if A in plane} == {0, 1}
    assert (0, 1) not in QA_SUPPORT
    q_01_aa = Fraction(int((0, 1) in QA_SUPPORT))
    direct_aa = Fraction(0)
    endpoint_assignment_aa = Fraction(1)
    assert q_01_aa * direct_aa - endpoint_assignment_aa == -1


def audit_three_diagonal_row_ledger():
    rows = {
        (row, column): three_colour_response(row, column)
        for row in (A, B, DELTA)
        for column in (A, B, DELTA)
    }
    assert rows[(A, A)] == Counter({(A,) * 6: 1})
    assert rows[(B, B)] == Counter({(B,) * 6: 1})
    assert rows[(DELTA, DELTA)] == Counter({(DELTA,) * 6: 1})
    assert rows[(B, A)] == rows[(DELTA, B)] == Counter()

    assert rows[(A, B)] == Counter({(A, DELTA, B, DELTA, B, B): 1})
    assert rows[(A, DELTA)] == Counter({(A, DELTA, DELTA, DELTA, A, A): 1})
    assert rows[(B, DELTA)] == Counter(
        {
            (B, B, DELTA, B, A, A): 1,
            (DELTA, A, DELTA, B, DELTA, A): 1,
        }
    )
    assert rows[(DELTA, A)] == Counter(
        {
            (A, A, B, A, B, DELTA): 1,
            (DELTA, A, A, A, DELTA, DELTA): 1,
        }
    )

    full_nine_targets = {
        (row, column): (
            Counter({(row,) * 6: 1}) if row == column else Counter()
        )
        for row in (A, B, DELTA)
        for column in (A, B, DELTA)
    }
    failed = {
        cell
        for cell, target in full_nine_targets.items()
        if rows[cell] != target
    }
    assert failed == {(A, B), (A, DELTA), (B, DELTA), (DELTA, A)}

    # The three stars in each family are globally linearly independent:
    # they occupy distinct site/physical-colour coordinates.
    assert len(set(THREE_COLOUR_P_STARS.values())) == 3
    assert len(set(THREE_COLOUR_S_STARS.values())) == 3


def q_value(pair):
    return Fraction(int(edge(*pair) in QA_SUPPORT))


def hessian():
    universe = set(RESIDUAL)
    return [
        [
            q_value(tuple(universe - set(left) - set(right)))
            if set(left).isdisjoint(right)
            else Fraction(0)
            for right in EDGES6
        ]
        for left in EDGES6
    ]


def curvature_covector(matched_edge, reverse):
    r, s = 0, 1
    u, v = matched_edge
    if reverse:
        u, v = v, u
    return edge_vector(
        {
            (r, s): q_value((u, v)),
            (u, v): q_value((r, s)),
            (r, u): -q_value((s, v)),
            (s, v): -q_value((r, u)),
        }
    )


def cycle_value(matched_edge, reverse):
    r, s = 0, 1
    u, v = matched_edge
    if reverse:
        u, v = v, u
    return q_value((r, s)) * q_value((u, v)) - q_value((r, u)) * q_value((s, v))


def audit_hessian_obstruction():
    matrix = hessian()
    witness = edge_vector({(0, 1): 1, (0, 4): -1, (1, 2): -1, (2, 4): 1})
    beta = edge_vector({(0, 1): 1})
    assert rank(matrix) == 10
    assert matvec(matrix, witness) == [0] * len(EDGES6)

    observed = {}
    for matched_edge in ((2, 3), (4, 5)):
        for reverse in (False, True):
            assert cycle_value(matched_edge, reverse) == 0
            covector = curvature_covector(matched_edge, reverse)
            pairing = dot(covector, witness)
            observed[(matched_edge, int(reverse))] = pairing
            assert dot(covector, beta) == 1
            assert pairing
            augmented = [
                row + [covector[index]]
                for index, row in enumerate(matrix)
            ]
            assert rank(augmented) == 11

    assert observed == {
        ((2, 3), 0): Fraction(1),
        ((2, 3), 1): Fraction(2),
        ((4, 5), 0): Fraction(2),
        ((4, 5), 1): Fraction(1),
    }

    # Scope guard: the individual failures do not imply failure of their
    # span.  This signed mixture detects beta and has an explicit pullback.
    first = curvature_covector((2, 3), False)
    second = curvature_covector((2, 3), True)
    mixture = [-2 * left + right for left, right in zip(first, second)]
    pullback = edge_vector({(0, 3): -1, (1, 5): 1, (2, 3): -1})
    assert mixture == edge_vector({(0, 1): -1, (1, 2): -1})
    assert dot(mixture, beta) == -1
    assert matvec(matrix, pullback) == mixture


def main():
    audit_eight_site_signature()
    audit_three_diagonal_eight_site_packet()
    audit_nine_row_ledger_and_cap()
    audit_three_diagonal_row_ledger()
    audit_hessian_obstruction()
    print("one-unused-anchor all-cycle eight-row guard: PASS")
    print("  exact eight-site signature: X_a^8 + X_b^8")
    print("  residual row ledger: 8/9 literal rows")
    print("  complementary packet: all 3 diagonal anchors, 4 off-diagonal failures")
    print("  Hessian ranks: 10 -> 11 for all four cycle normals")
    print("  signed cycle-span repair: explicit pullback PASS")


if __name__ == "__main__":
    main()
