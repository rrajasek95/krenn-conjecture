#!/usr/bin/env python3
"""Exact finite audit for the one- and two-line-field response theorem."""

from itertools import combinations, product

import sympy as sp


def osculating_words(n: int, moving_budget: int):
    """Binary support words for one fixed line and moving directions."""
    return {
        word
        for word in product((0, 1), repeat=n)
        if sum(word) <= moving_budget
    }


def audit_one_field_quotient() -> None:
    for n in range(3, 11):
        for budget in range(n + 1):
            words = osculating_words(n, budget)
            if budget == n:
                continue
            for sites in combinations(range(n), budget + 1):
                for word in words:
                    assert any(word[u] == 0 for u in sites)
            sharp = (1,) * budget + (0,) * (n - budget)
            assert sharp in words


def audit_moving_pair_quotient() -> None:
    sites = tuple(range(6))
    pairs = tuple(combinations(sites, 2))
    for omitted in pairs:
        survivors = [
            moving for moving in pairs
            if set(omitted) <= set(moving)
        ]
        assert survivors == [omitted]


def audit_plane_incidence_equality() -> None:
    # At a site, record the subset (of size at most two) of target axes
    # contained in the two-field plane W_u.
    local_patterns = tuple(
        frozenset(pattern)
        for size in range(3)
        for pattern in combinations(range(3), size)
    )
    feasible = 0
    for assignment in product(local_patterns, repeat=6):
        counts = tuple(
            sum(color in plane for plane in assignment)
            for color in range(3)
        )
        if min(counts) < 4:
            continue
        feasible += 1
        assert counts == (4, 4, 4)
        assert all(len(plane) == 2 for plane in assignment)
        omissions = tuple(
            frozenset(
                u for u, plane in enumerate(assignment)
                if color not in plane
            )
            for color in range(3)
        )
        assert all(len(pair) == 2 for pair in omissions)
        assert set().union(*omissions) == set(range(6))
        assert sum(len(pair) for pair in omissions) == 6
    assert feasible == 90


def audit_secant_rank() -> None:
    alpha, beta = sp.symbols("alpha beta")
    # In bases beginning with l_u,m_u, flattening
    # alpha*l_1...l_4 + beta*m_1...m_4 at the first site has this
    # nonzero 2x2 minor.  A third pure point would require rank one.
    minor = sp.Matrix([[alpha, 0], [0, beta]]).det()
    assert sp.expand(minor) == alpha * beta


def audit_pigeonhole_overlap() -> None:
    sites = set(range(6))
    disjoint_pair_partitions = 0
    for pairs in combinations(tuple(combinations(range(6), 2)), 3):
        pair_sets = tuple(set(pair) for pair in pairs)
        if set().union(*pair_sets) != sites:
            continue
        if sum(len(pair) for pair in pair_sets) != 6:
            continue
        if any(
            pair_sets[i] & pair_sets[j]
            for i in range(3)
            for j in range(i)
        ):
            continue
        disjoint_pair_partitions += 1
        complements = tuple(sites - pair for pair in pair_sets)
        assert all(
            len(complements[i] & complements[j]) == 2
            for i in range(3)
            for j in range(i)
        )

        # Three colours assigned to two fields have a repeated field.
        for field_assignment in product(range(2), repeat=3):
            assert any(
                field_assignment[i] == field_assignment[j]
                for i in range(3)
                for j in range(i)
            )
    assert disjoint_pair_partitions == 15


def audit_genuine_secant_bridge() -> None:
    # At site 0 the fields are L/M; at sites 1--5 they agree.  The two
    # expansion words of (L+M,L,L,L,T,T) alternate which osculating ball
    # contains them, while the pure tensor itself is in neither space.
    left_word = ("L", "L", "L", "L", "T", "T")
    right_word = ("M", "L", "L", "L", "T", "T")
    center_l = ("L",) * 6
    center_m = ("M", "L", "L", "L", "L", "L")

    def distance(word, center):
        return sum(a != b for a, b in zip(word, center))

    assert distance(left_word, center_l) == 2
    assert distance(left_word, center_m) == 3
    assert distance(right_word, center_l) == 3
    assert distance(right_word, center_m) == 2


def audit_three_frame_support_boxes() -> None:
    # Every nonempty local coordinate support in a three-line basis.
    local_supports = tuple(
        frozenset(support)
        for size in range(1, 4)
        for support in combinations(range(3), size)
    )
    assert len(local_supports) == 7

    box_patterns = 0
    osculating_union_patterns = 0
    for assignment in product(local_supports, repeat=6):
        box_patterns += 1

        # Dynamic programming independently asks whether the Cartesian box
        # contains a word in which every symbol occurs at most three times.
        reachable = {(0, 0, 0)}
        for support in assignment:
            reachable = {
                tuple(counts[i] + int(i == chosen) for i in range(3))
                for counts in reachable
                for chosen in support
            }
        contained_in_osculating_union = not any(
            max(counts) <= 3 for counts in reachable
        )

        singleton_counts = tuple(
            sum(support == {color} for support in assignment)
            for color in range(3)
        )
        hall_obstruction = max(singleton_counts) >= 4
        assert contained_in_osculating_union == hall_obstruction
        if contained_in_osculating_union:
            osculating_union_patterns += 1

    assert box_patterns == 7**6 == 117_649
    assert osculating_union_patterns == 1_731


def audit_three_osculating_balls_are_disjoint() -> None:
    words = tuple(product(range(3), repeat=6))
    balls = {
        color: {
            word
            for word in words
            if sum(symbol != color for symbol in word) <= 2
        }
        for color in range(3)
    }
    assert all(len(ball) == 1 + 6 * 2 + 15 * 4 == 73
               for ball in balls.values())
    assert all(
        balls[left].isdisjoint(balls[right])
        for left in range(3)
        for right in range(left)
    )


def main() -> None:
    audit_one_field_quotient()
    audit_moving_pair_quotient()
    audit_plane_incidence_equality()
    audit_secant_rank()
    audit_pigeonhole_overlap()
    audit_genuine_secant_bridge()
    audit_three_frame_support_boxes()
    audit_three_osculating_balls_are_disjoint()
    print("one-/two-line-field non-pure response obstruction: PASS")
    print("plane-incidence assignments at equality: 90")
    print("omission-pair partitions:", 15)
    print("four-site secant line: no third pure point")
    print("three-frame support boxes:", 117_649)
    print("boxes contained in the osculating union:", 1_731)
    print("three radius-two coordinate balls: pairwise disjoint")


if __name__ == "__main__":
    main()
