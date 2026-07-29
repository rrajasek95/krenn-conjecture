#!/usr/bin/env python3
"""Exact audit of all-order formal-five-layer duality at h=8."""

from itertools import combinations
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


H = 8


def formal_simple_witness(profile):
    repeated = [i for i, multiplicity in enumerate(profile) if multiplicity >= 2]
    for chosen_tuple in combinations(repeated, 5):
        chosen = set(chosen_tuple)
        legal = True
        for partial_tuple in combinations(chosen_tuple, 2):
            partial = set(partial_tuple)
            takes = {
                i: (1 if i in partial else 2)
                for i in chosen_tuple
            }
            if sum(takes.values()) != H or not frontier.leaves_singleton(
                profile, takes
            ):
                legal = False
                break
        if not legal:
            continue

        complement = tuple(
            multiplicity - (2 if i in chosen else 0)
            for i, multiplicity in enumerate(profile)
            if multiplicity - (2 if i in chosen else 0) > 0
        )
        classes = len(complement)
        simple = complement.count(1)
        if classes < 5 or simple > 2 * classes - 10:
            return chosen_tuple, complement
    return None


def check_uniform_algebra() -> None:
    k, c, n = sp.symbols("k c n", integer=True, positive=True)
    total = k + 18
    complement_degree = total - 10
    assert sp.expand(complement_degree - (k + 8)) == 0

    numerator_degree = complement_degree + 6
    denominator_degree = (k + 1) + 3 * 5
    assert sp.expand(denominator_degree - numerator_degree) == 2

    # The five value rows alone bound the sextic kernel by four.  Audit
    # every viable mixture of local gcd orders: at an exact order-two
    # node the reduced-space order is two for gcd order zero, one for
    # gcd order one, and the row is absorbed for gcd order at least
    # three.  Gcd order two would leave an exact value equation and is
    # impossible after removal of the gcd.
    d = sp.symbols("d", integer=True, positive=True)
    deficit = sp.expand(5 * (d - 2) - d * (7 - d))
    assert deficit == d**2 - 2 * d - 10
    for dimension in range(5, 8):
        baseline = deficit.subs(d, dimension)
        assert baseline > 0
        for order_one_nodes in range(6):
            for absorbed_nodes in range(6 - order_one_nodes):
                ordinary_nodes = 5 - order_one_nodes - absorbed_nodes
                forced_weight = (
                    ordinary_nodes * (dimension - 2)
                    + order_one_nodes * (dimension - 1)
                )
                least_gcd_degree = order_one_nodes + 3 * absorbed_nodes
                reduced_cap = dimension * (
                    7 - least_gcd_degree - dimension
                )
                observed_deficit = forced_weight - reduced_cap
                expected_deficit = (
                    baseline
                    + (dimension + 1) * order_one_nodes
                    + (2 * dimension + 2) * absorbed_nodes
                )
                assert observed_deficit == expected_deficit
                assert observed_deficit > 0

    # Principal-part moments give N<=7.  Differentiation has the sharp
    # all-order leading coefficient n-7 and leaves S in P_{c-4}.
    leading = sp.expand(n + (k + 1) - (k + 8))
    assert leading == n - 7
    assert leading.subs(n, 7) == 0
    assert sp.expand((c + 6) - 2 * 5) == c - 4
    assert sp.expand(2 * (c - 4) - 2) == 2 * c - 10

    # Exact formal-layer identity for arbitrary fixed excess.
    z, t = sp.symbols("z t")
    for multiplicity in range(2, 9):
        partial = (z - t) ** (multiplicity - 1) / (z + t) ** 2
        lifted_partial = (
            (z - t) ** (multiplicity - 2)
            * (z**2 - t**2)
            / (z + t) ** 3
        )
        assert sp.factor(partial - lifted_partial) == 0


def check_fourth_order_increment() -> None:
    p = 12
    total = p + H + 2
    counts, residual_tuple = frontier.census(H, p)
    assert total == 22
    assert counts == {
        "H": 480,
        "S": 411,
        "C": 28,
        "L": 21,
        "Q": 15,
        "R": 46,
        "D": 1,
    }
    residuals = set(residual_tuple)

    expected = {
        (4, 3, 3, 3, 3, 3, 3),
        (3, 3, 3, 3, 2, 2, 2, 2, 2),
        (3, 3, 3, 3, 3, 2, 2, 2, 1),
        (3, 3, 3, 2, 2, 2, 2, 2, 2, 1),
        (3, 3, 3, 3, 2, 2, 2, 2, 1, 1),
        (3, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1),
    }
    observed = {
        profile
        for profile in residuals
        if formal_simple_witness(profile) is not None
    }
    assert observed == expected

    expected_signatures = {
        (4, 3, 3, 3, 3, 3, 3): (7, 5),
        (3, 3, 3, 3, 2, 2, 2, 2, 2): (4, 0),
        (3, 3, 3, 3, 3, 2, 2, 2, 1): (6, 3),
        (3, 3, 3, 2, 2, 2, 2, 2, 2, 1): (5, 1),
        (3, 3, 3, 3, 2, 2, 2, 2, 1, 1): (6, 3),
        (3, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1): (6, 3),
    }
    canonical_choices = {
        (4, 3, 3, 3, 3, 3, 3): (1, 2, 3, 4, 5),
        (3, 3, 3, 3, 2, 2, 2, 2, 2): (4, 5, 6, 7, 8),
        (3, 3, 3, 3, 3, 2, 2, 2, 1): (0, 1, 5, 6, 7),
        (3, 3, 3, 2, 2, 2, 2, 2, 2, 1): (3, 4, 5, 6, 7),
        (3, 3, 3, 3, 2, 2, 2, 2, 1, 1): (0, 4, 5, 6, 7),
        (3, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1): (3, 4, 5, 6, 7),
    }
    for profile in expected:
        chosen = canonical_choices[profile]
        assert len(chosen) == 5
        assert all(profile[index] >= 2 for index in chosen)

        legal_cores = 0
        for partial_pair in combinations(chosen, 2):
            takes = {
                index: (1 if index in partial_pair else 2)
                for index in chosen
            }
            assert sum(takes.values()) == H
            assert frontier.leaves_singleton(profile, takes)
            legal_cores += 1
        assert legal_cores == 10

        chosen_set = set(chosen)
        complement = tuple(
            multiplicity - (2 if index in chosen_set else 0)
            for index, multiplicity in enumerate(profile)
            if multiplicity - (2 if index in chosen_set else 0) > 0
        )
        assert sum(complement) == 12  # k+8 at k=4
        signature = (len(complement), complement.count(1))
        assert signature == expected_signatures[profile]
        classes, simple = signature
        assert classes < 5 or simple > 2 * classes - 10


def main() -> None:
    check_uniform_algebra()
    check_fourth_order_increment()
    print("PASS: all-order formal-five-layer duality at h=8")
    print("five value rows alone force sextic-kernel dimension four")
    print("dual degree c-4 is k-independent")
    print("six frozen h=8,k=4 profiles each have ten legal canonical cores")


if __name__ == "__main__":
    main()
