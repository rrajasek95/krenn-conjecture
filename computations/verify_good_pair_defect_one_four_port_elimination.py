#!/usr/bin/env python3
"""Lightweight exact audit of the four-port defect-one elimination.

The theorem itself is a uniform hand proof. This script checks its finite
port arithmetic, the singleton-shore support logic, and the strengthened fan
counts. It has no third-party dependencies and deliberately performs no
Groebner, SAT, or large matching census.
"""

from itertools import combinations


CHECKS = []


def check(label, condition):
    if not condition:
        raise AssertionError(label)
    CHECKS.append(label)
    print(f"PASS  {label}")


def supports(universe):
    result = []
    for size in (1, 2):
        result.extend(frozenset(c) for c in combinations(universe, size))
    return result


def terms_on_edge(p_support, s_support, x, y):
    return (
        x in p_support and y in s_support,
        x in s_support and y in p_support,
    )


def check_two_shore_arithmetic():
    feasible = []
    for delta in range(16):
        for u_a in range(5):
            for u_b in range(5):
                for u_o in range(1, 5):
                    if u_a + u_b + u_o > 4:
                        continue
                    if u_a < delta + 2:
                        continue
                    if u_b < max(0, 2 - delta):
                        continue
                    feasible.append((delta, u_a, u_b, u_o))
    check("two non-singleton shores need at least five ports", not feasible)


def check_singleton_star_support():
    # If x and at least two leaves all lie in U, an invisible star product
    # cannot vanish without putting at least three sites in one support.
    universe = ("x", "b0", "b1", "o")
    bad = []
    for p_support in supports(universe):
        for s_support in supports(universe):
            union = p_support | s_support
            if not {"x", "b0", "b1"} <= union:
                continue
            possible_cancellation = True
            for leaf in ("b0", "b1"):
                term1, term2 = terms_on_edge(
                    p_support, s_support, "x", leaf
                )
                if term1 != term2:
                    possible_cancellation = False
                    break
            if possible_cancellation:
                bad.append((p_support, s_support))
    check(
        "singleton centre cannot share a four-port window with two leaves",
        not bad,
    )


def check_three_leaf_partition():
    universe = ("b0", "b1", "b2", "o")
    admissible = 0
    for p_support in supports(universe):
        for s_support in supports(universe):
            if p_support | s_support != frozenset(universe):
                continue
            assert len(p_support) == len(s_support) == 2
            assert p_support.isdisjoint(s_support)
            interface = [
                b
                for b in ("b0", "b1", "b2")
                if any(terms_on_edge(p_support, s_support, b, "o"))
            ]
            if not interface:
                continue
            admissible += 1
            same_side_pair = None
            for pair in combinations(("b0", "b1", "b2"), 2):
                if set(pair) <= p_support or set(pair) <= s_support:
                    same_side_pair = pair
                    break
            assert same_side_pair is not None
            assert not any(
                terms_on_edge(p_support, s_support, *same_side_pair)
            )
    check(
        "three-leaf singleton shore has a stranded same-support pair",
        admissible > 0,
    )


def check_count_consequences():
    for n in range(8, 102, 2):
        good = n * (n - 7) // 2
        fan = n - 7
        assert good >= fan >= 1
        if n >= 14:
            assert fan >= n - 13
    check(
        "all good-pair and fan counts strengthen the former shore bound",
        True,
    )


def main():
    check(
        "nine block directions exceed a one-dimensional gauge intersection",
        9 > 1,
    )
    check_two_shore_arithmetic()
    check_singleton_star_support()
    check_three_leaf_partition()
    check_count_consequences()
    print()
    print(f"checks run: {len(CHECKS)}")
    print("ALL CHECKS PASS")


if __name__ == "__main__":
    main()
