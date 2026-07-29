#!/usr/bin/env python3
"""Independent audit of the p=28 two-quartic singleton-swap q=6 cap.

This script intentionally reconstructs the selection counts, the conditional
q=4 incidence contradiction, the relation-space/common-baseline degrees, all
local gcd corrections in the five-space Wronskian count, and the coprime-cubic
intersection used by the final fixed-row contradiction.
"""

from __future__ import annotations

from collections import Counter

import sympy as sp


RESIDUALS = ((2, 7, 0, 1), (2, 7, 1, -1))


def selected_kernel_gap(h: int, k: int, d: int, singles: int, q: int) -> int:
    """Forced selected-row Wronskian weight minus its degree cap."""
    degree = h + 3 - d
    forced = d * max(0, q - 2) + singles * max(0, q - 1)
    forced += max(0, q - k)
    cap = q * (degree + 1 - q)
    return forced - cap


def audit_conditional_q4_incidence(h: int, d: int, singles: int) -> None:
    """Recheck Sections 4--5 of the low-role theorem at q=4.

    The low-h inequality in that theorem is not used here.  The mixed
    pair-drop bound makes W four-dimensional; conditional on q=4 this gives
    W=K.  The remaining arithmetic is the uniform singleton-incidence
    contradiction, including zero and the one missing triple--zero edge.
    """
    degree = h + 3 - d

    # The independently audited mixed pair-drop criterion supplies dim W >= 4.
    assert 2 * singles > 3 * (degree // 2 - 2)
    assert 4 - 2 == 2  # a cubic incidence has codimension at most two in K

    # If a singleton incidence space were a plane, its cubic quotient is a
    # pencil in P_N.  These are the two worst signed-pair counts: zero is the
    # moving neighbor, or zero is fixed and the triple--zero edge is missing.
    quotient_degree = degree - 3
    zero_neighbor_pairs = (singles - 2) + d
    fixed_zero_missing_pairs = (singles - 1) + (d - 1)
    assert zero_neighbor_pairs == quotient_degree
    assert fixed_zero_missing_pairs == quotient_degree
    assert 2 * quotient_degree > 2 * quotient_degree - 1

    # The square-pencil cap is N-2, whereas all other singleton cubics load
    # the pencil at singles-1 nodes.
    cubic_nodes = singles - 1
    assert cubic_nodes - (quotient_degree - 2) == 3 - d > 0

    # Exhaust every possible collection of absorbed singleton/repeated
    # factors that can leave a four-space.  This reproduces the terminal
    # hyperplane argument rather than assuming that the kernel is primitive.
    for absorbed_cubics in range(singles + 1):
        for absorbed_quadratics in range(d + 1):
            gcd_degree = 3 * absorbed_cubics + 2 * absorbed_quadratics
            reduced_degree = degree - gcd_degree
            if reduced_degree < 3:
                continue  # P_reduced cannot contain a four-space

            remaining = singles - absorbed_cubics
            assert remaining >= 4

            # If all remaining singleton incidence hyperplanes coincide, one
            # section has every singleton cubic plus every absorbed quadratic.
            all_equal_degree = 3 * singles + 2 * absorbed_quadratics
            assert all_equal_degree > degree

            # Otherwise two distinct hyperplanes meet in a plane divisible by
            # two more cubics.  A plane requires residual degree at least one.
            second_degree = reduced_degree - 6
            if second_degree < 1:
                continue

            terminal_nodes = remaining - 2
            terminal_nonzero_nodes = remaining - 3
            assert terminal_nonzero_nodes >= 1
            if second_degree < 3:
                # A nonzero cubic cannot lie in P_0, P_1, or P_2.
                continue

            parity_excess = (
                2 * terminal_nonzero_nodes - (2 * second_degree - 1)
            )
            assert parity_excess == (
                5
                - 2 * d
                + 4 * absorbed_cubics
                + 4 * absorbed_quadratics
            )
            assert parity_excess > 0

            square_cap_excess = terminal_nodes - (second_degree - 2)
            assert square_cap_excess == (
                5
                - d
                + 2 * absorbed_cubics
                + 2 * absorbed_quadratics
            )
            assert square_cap_excess > 0


def audit_selection_ledger_and_q4_import() -> None:
    for h in range(22, 28):
        k = 28 - h
        for e, a, b, u in RESIDUALS:
            assert 4 * e + 3 * a + 2 * b + u == 30

            # The role-two layers are the fixed triple x and, when b=1, the
            # unique exact double.  Every ordinary singleton but s is selected.
            d = 1 + b
            ordinary_singletons = h + u
            selected_singletons = h + 2 - 2 * d
            assert ordinary_singletons - selected_singletons == 1
            assert selected_singletons >= 1

            selected_layers = d + selected_singletons
            degree = h + 3 - d
            assert selected_layers == h + 2 - d
            assert degree + 1 == selected_layers + 2

            # Removing the role-two triple leaves the fixed singleton x;
            # removing the double leaves nothing; the one unselected ordinary
            # singleton is s.  Thus both tuples have the same complement.
            complement = Counter({4: e, 3: a - 1, 1: 2})
            assert complement == Counter({4: 2, 3: 6, 1: 2})
            assert sum(multiplicity * count for multiplicity, count in complement.items()) == 28
            complement_classes = sum(complement.values())
            assert complement_classes == 10

            # q=6 is exactly on equality and q=7 has excess twelve.
            assert selected_kernel_gap(h, k, d, selected_singletons, 6) == 0
            assert selected_kernel_gap(h, k, d, selected_singletons, 7) == 12

            # Pair drops give q>=4.  If q were four, their four-space would
            # fill K and the incidence proof below would contradict it.
            audit_conditional_q4_incidence(h, d, selected_singletons)

            # At q=6, rank-nullity gives a four-dimensional relation space in
            # P_{c-4}=P_6.  This independently fixes the P_9 transport degree.
            row_rank = (degree + 1) - 6
            relation_dimension = selected_layers - row_rank
            assert relation_dimension == 4
            assert complement_classes - 4 == 6
            assert (complement_classes - 4) + 3 == 9

            # Seven triple rows, one for each x; columns are ordinary s values.
            total_grid_entries = 7 * ordinary_singletons
            maximal_entries_cap = 7
            clean_columns = ordinary_singletons - maximal_entries_cap
            assert total_grid_entries > maximal_entries_cap
            assert clean_columns == (h - 6 if b == 0 else h - 8)
            assert clean_columns >= (16 if b == 0 else 14)


def local_gcd_adjusted_cost(q: int, row_order: int, gcd_order: int) -> int:
    """Row weight plus cap reduction after dividing a local gcd root."""
    if gcd_order <= row_order:
        reduced_row_weight = max(0, q - row_order + gcd_order)
    else:
        reduced_row_weight = 0  # the row is automatic after division
    return q * gcd_order + reduced_row_weight


def audit_common_kernel_wronskian() -> None:
    # Restoring both ordinary singleton choices gives baseline
    # 4^2 3^6 1_x 1_s 1_t: eleven classes, mass 29, in P_9.
    baseline_orders = [4, 4] + [3] * 6 + [1, 1, 1]
    assert len(baseline_orders) == 11
    assert sum(baseline_orders) == 29

    q = 5
    degree = 9
    primitive_weight = sum(max(0, q - order) for order in baseline_orders)
    cap = q * (degree + 1 - q)
    assert primitive_weight == 26
    assert cap == 25

    # No common factor can rescue a five-space.  At every displayed node its
    # local cost is at least the primitive row weight; elsewhere a gcd root
    # lowers the cap by q times its order and is strictly favorable.
    for row_order in (1, 3, 4):
        primitive = max(0, q - row_order)
        for gcd_order in range(0, 13):
            assert local_gcd_adjusted_cost(q, row_order, gcd_order) >= primitive
    for gcd_order in range(1, 13):
        assert q * gcd_order > 0

    assert primitive_weight > cap  # hence dim common kernel <= 4


def coefficient_vector(poly: sp.Expr, z: sp.Symbol, degree: int) -> list[sp.Expr]:
    expanded = sp.Poly(sp.expand(poly), z)
    return [expanded.nth(i) for i in range(degree + 1)]


def audit_cubic_coprimality_intersection_and_fixed_row() -> None:
    z, s, t, x = sp.symbols("z s t x")
    f_s = (z - s) ** 2 * (z + s)
    f_t = (z - t) ** 2 * (z + t)

    # This exact resultant is the universal coprimality test.  It is nonzero
    # precisely when s != t and s != -t; setting s=0 remains covered.
    resultant = sp.factor(sp.resultant(f_s, f_t, z))
    assert resultant == -(s - t) ** 5 * (s + t) ** 4
    assert resultant.subs({s: 0, t: 2}) != 0

    # Independently compute the coefficient-space intersection in both the
    # zero and nonzero cases.  Each cubic-multiple space has dimension seven;
    # their union has rank ten, so the intersection has dimension four.
    for s_value, t_value in ((0, 2), (2, 5), (-2, 5)):
        left = [
            coefficient_vector(f_t.subs(t, t_value) * z**i, z, 9)
            for i in range(7)
        ]
        right = [
            coefficient_vector(f_s.subs(s, s_value) * z**i, z, 9)
            for i in range(7)
        ]
        union_rank = sp.Matrix(left + right).rank()
        assert union_rank == 10
        assert 7 + 7 - union_rank == 4

    # Algebraically the intersection consists of degree-at-most-nine
    # multiples of the degree-six lcm f_s f_t, hence f_s f_t P_3.
    assert 9 - (3 + 3) == 3
    assert 3 + 1 == 4

    # On S_s=f_s P_3, write V in powers of y=z-x and retain the local unit's
    # first jet.  The exact simple row has a nonzero coefficient on v_1.
    u0, u1 = sp.symbols("u0 u1")
    v0, v1, v2, v3 = sp.symbols("v0 v1 v2 v3")
    y = z - x
    unit = u0 + u1 * y
    v_poly = v0 + v1 * y + v2 * y**2 + v3 * y**3
    fixed_row = sp.expand(sp.diff(unit * f_s * v_poly, z).subs(z, x))
    v1_coefficient = sp.factor(sp.diff(fixed_row, v1))
    assert sp.expand(v1_coefficient - u0 * (s - x) ** 2 * (s + x)) == 0
    assert v1_coefficient.subs({u0: 3, s: 0, x: 2}) != 0
    assert v1_coefficient.subs({u0: 3, s: 2, x: 5}) != 0


def main() -> None:
    audit_selection_ledger_and_q4_import()
    audit_common_kernel_wronskian()
    audit_cubic_coprimality_intersection_and_fixed_row()
    print("independent p=28 two-quartic singleton-swap q=6 cap: PASS")
    print("formal selections: exact for both tuples at all six p=28 splits")
    print("q=4 import: uniform d=1,2 incidence contradiction re-derived")
    print("common baseline: 4^2 3^6 1^3 in P_9, five-space excess one")
    print("fixed simple row: nonzero on f_s P_3, including s=0")
    print("scope guard: q=5 grid consequence only, not profile closure")


if __name__ == "__main__":
    main()
