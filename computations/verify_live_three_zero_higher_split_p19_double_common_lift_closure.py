#!/usr/bin/env python3
"""Exact audit for the p=19 dense-double common-lift closure."""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_q5_boundary_census as q5
import verify_live_three_zero_higher_split_p19_singleton_parity_common_lift_closure as singleton


EXPECTED = {
    0: {
        (1, 10, -2),
        (2, 8, -1),
        (3, 6, 0),
        (3, 7, -2),
        (4, 5, -1),
        (5, 3, 0),
        (5, 4, -2),
    },
    1: {
        (0, 9, -1),
        (1, 7, 0),
        (1, 8, -2),
        (2, 6, -1),
        (3, 4, 0),
        (3, 5, -2),
        (4, 3, -1),
    },
}


def selected_pair_data(e: int, a: int, b: int, u: int) -> dict[str, int]:
    leftover_singletons = u + 2
    complement_classes = e + a + (b - 2) + leftover_singletons
    relation_degree = complement_classes - 4
    common_degree = relation_degree + 5
    return {
        "leftover_singletons": leftover_singletons,
        "complement_classes": complement_classes,
        "relation_degree": relation_degree,
        "common_degree": common_degree,
    }


def complement_profile(
    e: int, a: int, b: int, leftover_singletons: int
) -> tuple[int, ...]:
    return tuple(
        sorted(
            (4,) * e
            + (3,) * a
            + (2,) * (b - 2)
            + (1,) * leftover_singletons,
            reverse=True,
        )
    )


def route_applies(e: int, a: int, b: int, u: int) -> bool:
    if b < 3 or u < -2:
        return False
    data = selected_pair_data(e, a, b, u)
    degree = data["common_degree"]
    return degree <= 9 or (degree == 10 and b >= 6)


def audit_exact_families() -> None:
    observed = {0: set(), 1: set()}
    for e in (0, 1):
        for a, b, u in singleton.parameter_families(e):
            if route_applies(e, a, b, u):
                observed[e].add((a, b, u))

                data = selected_pair_data(e, a, b, u)
                expected_degree = (
                    22 - 2 * a - b if e == 0 else 19 - 2 * a - b
                )
                assert data["common_degree"] == expected_degree
                assert data["relation_degree"] + 5 == expected_degree
                assert data["leftover_singletons"] >= 0

                complement = complement_profile(
                    e, a, b, data["leftover_singletons"]
                )
                assert sum(complement) == 19
                assert len(complement) == data["complement_classes"]
                assert sum(min(part, 6) for part in complement) == 19

                for h in range(13, 19):
                    profile = singleton.profile_from_parameters(
                        h, e, a, b, u
                    )
                    selection = q5.Selection(2, 0, complement)
                    assert selection in q5.formal_selections(
                        profile, h, 19
                    )
                    assert (h + u) - (h - 2) == data[
                        "leftover_singletons"
                    ]
                    k = 19 - h
                    assert 22 - h + max(0, 6 - k) > 0

                # The baseline adds one exact double row.  A common
                # six-space exceeds its degree cap by nine at p=19.
                fixed_parts = complement
                forced_weight = sum(
                    max(0, 6 - part) for part in fixed_parts
                ) + (6 - 2)
                common_classes = data["complement_classes"] + 1
                assert common_classes == data["common_degree"]
                cap = 6 * (data["common_degree"] + 1 - 6)
                assert forced_weight - cap == 9

                if data["common_degree"] <= 9:
                    assert b >= 3
                    assert b - 1 >= 2  # two moving partners after fixing i
                else:
                    assert data["common_degree"] == 10
                    assert b - 2 >= 4  # four partners after fixing i,v

    assert observed == EXPECTED
    assert len(observed[0]) == len(observed[1]) == 7


def audit_uniform_six_space_bound() -> None:
    # A common six-space is possible only when the formal complement has
    # six-capped mass at least 28.
    for fixed_parts in (
        (),
        (1,),
        (2, 3),
        (4, 9),
        (1, 2, 3, 4),
        (6, 7, 12),
    ):
        classes = len(fixed_parts)
        capped_mass = sum(min(part, 6) for part in fixed_parts)
        baseline_weight = sum(
            max(0, 6 - part) for part in fixed_parts
        ) + 4  # the moving exact-double row
        degree = classes + 1
        cap = 6 * (degree + 1 - 6)
        assert baseline_weight - cap == 28 - capped_mass


def audit_intersections_and_complete_graph() -> None:
    # A quintic-multiple space in degree N has dimension N-4.  Two
    # coprime quintics have intersection dimension max(N-9, 0).
    for degree in range(5, 16):
        single_dim = degree - 5 + 1
        pair_dim = max(degree - 10 + 1, 0)
        assert single_dim == degree - 4
        if degree <= 9:
            assert pair_dim == 0
        if degree == 10:
            assert pair_dim == 1

    # Subtracting complete-graph equations with two different external
    # indices gives 2(A_i-A_j)(A_k-A_l)=0.
    ai, aj, ak, al = sp.symbols("ai aj ak al")
    bk, bl = sp.symbols("bk bl")
    difference_i = bk - bl + 2 * ai * (ak - al)
    difference_j = bk - bl + 2 * aj * (ak - al)
    assert sp.factor(
        difference_i - difference_j
        - 2 * (ai - aj) * (ak - al)
    ) == 0

    # Exhaust finite equality patterns: the four-index identity permits
    # at most two values, and if there are two, one occurs only once.
    from itertools import combinations, product

    for size in range(4, 9):
        for values in product(range(3), repeat=size):
            valid = True
            for four in combinations(range(size), 4):
                i, j, k, ell = four
                pairings = (
                    ((i, j), (k, ell)),
                    ((i, k), (j, ell)),
                    ((i, ell), (j, k)),
                )
                if any(
                    (values[a] - values[b])
                    * (values[c] - values[d])
                    != 0
                    for (a, b), (c, d) in pairings
                ):
                    valid = False
                    break
            if valid:
                counts = sorted(
                    (values.count(v) for v in set(values)), reverse=True
                )
                assert len(counts) <= 2
                if len(counts) == 2:
                    assert counts[1] == 1
                assert counts[0] >= size - 1 >= 3

    # Exact logarithmic jet and its degree-two fibre polynomial.
    z, x, v, fibre = sp.symbols("z x v fibre")
    g = (z - x) ** 3 * (z + x) ** 2
    jet = sp.factor(sp.diff(g, z).subs(z, v) / g.subs(z, v))
    assert sp.factor(jet - (5 * v + x) / (v**2 - x**2)) == 0
    fibre_polynomial = sp.expand(fibre * (v**2 - x**2) - (5 * v + x))
    assert sp.Poly(fibre_polynomial, x).degree() <= 2
    assert sp.Poly(fibre_polynomial, x).coeff_monomial(x) == -1


def audit_combined_ledger() -> None:
    singleton_closed = {0: set(), 1: set()}
    for e in (0, 1):
        for a, b, u in singleton.parameter_families(e):
            data = singleton.selected_data(e, a, b, u)
            if data["pool"] >= 1 and data["fixed_classes"] <= 5:
                singleton_closed[e].add((a, b, u))
        assert singleton_closed[e].isdisjoint(EXPECTED[e])

    assert len(singleton_closed[0]) == 32
    assert len(singleton_closed[1]) == 25
    assert sum(
        len(singleton_closed[e] | EXPECTED[e]) for e in (0, 1)
    ) == 71
    assert sum(len(singleton.parameter_families(e)) for e in (0, 1)) == 94


def main() -> None:
    audit_exact_families()
    audit_uniform_six_space_bound()
    audit_intersections_and_complete_graph()
    audit_combined_ledger()
    print("p=19 dense-double common-lift closure: PASS")
    print("new dense-double families: 7 no-quartic + 7 quartic = 14")
    print("combined new p=19 ledger: 71/94 closed, 23 remain")
    print("common-kernel, intersection, and fibre identities: audited")


if __name__ == "__main__":
    main()
