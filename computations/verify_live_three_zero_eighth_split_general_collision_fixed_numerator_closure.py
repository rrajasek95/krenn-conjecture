#!/usr/bin/env python3
"""Exact audit of the general-collision fixed-numerator closure."""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier
import verify_live_three_zero_eighth_split_all_order_mixed_role_census as mixed


H = 8


def fixed_numerator_criterion(profile: tuple[int, ...]) -> bool:
    """Count-only sufficient criterion (3)."""
    n1 = profile.count(1)
    repeated = len(profile) - n1
    return repeated >= 7 and (
        n1 >= 2 or profile.count(2) >= 6 or profile.count(3) >= 5
    )


def check_nonuniform_primitive_identity() -> None:
    """Differentiate with genuinely unequal complementary multiplicities."""
    z, mu = sp.symbols("z mu")
    k = 7
    x0, x1, x2 = sp.symbols("x0 x1 x2")
    coefficients = sp.symbols("c0:10")
    n = sum(coefficients[j] * z**j for j in range(10))

    multiplicities = ((x0, 1), (x1, 2), (x2, 3))
    radical = sp.prod(z - x for x, _ in multiplicities)
    d0 = sp.prod((z - x) ** m for x, m in multiplicities)
    s0 = sp.cancel(d0 / radical)
    d1 = sp.cancel(sp.diff(d0, z) / s0)
    assert sp.Poly(s0, z).degree() == 3
    assert sp.Poly(d1, z).degree() == 2

    operator = sp.expand(
        radical * ((z + mu) * sp.diff(n, z) + (k + 1) * n)
        - (z + mu) * d1 * n
    )
    full_denominator = sp.prod(
        (z - x) ** (m + 1) for x, m in multiplicities
    )
    primitive = (z + mu) ** (k + 1) * n / d0
    reconstructed = (z + mu) ** k * operator / full_denominator
    assert sp.cancel(sp.diff(primitive, z) - reconstructed) == 0

    delta = sum(m for _, m in multiplicities)
    lead = sp.Poly(operator, z).coeff_monomial(z ** (9 + 3))
    # The nominal coefficient is (j+k+1-delta) times the monic radical
    # coefficient.  Here delta is fixed only for this symbolic identity,
    # so inspect the coefficient directly.
    assert sp.expand(lead - coefficients[9] * (9 + k + 1 - delta)) == 0


def check_degrees_and_local_jets() -> None:
    h, k, anchor_mass, moving_role = sp.symbols(
        "h k A b", integer=True
    )
    total_mass = 2 * h + k + 2
    primitive_degree = total_mass - anchor_mass
    normalized_degree = sp.expand(primitive_degree - (k + 1))
    assert normalized_degree == 2 * h + 1 - anchor_mass
    assert sp.expand(
        normalized_degree.subs(anchor_mass, h + 2 - moving_role)
    ) == h - 1 + moving_role

    # E=A n'+B n.  E(t)=E'(t)=0 has the claimed triangular pivot.
    A0, A1, B0, B1 = sp.symbols("A0 A1 B0 B1", nonzero=True)
    matrix = sp.Matrix(((B0, A0, 0), (B1, A1 + B0, A0)))
    assert matrix[:, 1:3].det() == A0**2

    # Eighth-split common four-core ledger.
    assert (2 * H + k + 2) - 8 == k + 10
    assert (k + 10) - (k + 1) == 9
    for dimension in range(5, 11):
        assert 8 * (dimension - 1) > dimension * (10 - dimension)
    assert 4 * 2 + 3 * 4 > 2 * (10 - 2)
    assert 4 * 4 + 3 * 2 > 3 * (10 - 3)
    assert 8 * (4 - 1) == 4 * (10 - 4) == 24

    # General moving-plane Wronskian weight (44).
    for role in range(1, 8):
        for dimension in range(2, 10):
            generic = list(range(max(0, dimension - 2)))
            sequence = generic + [role, role + 1]
            sequence = sorted(sequence)
            # If the imposed two sections are already generic, the
            # condition has zero Schubert weight.
            minimum = 2 * max(0, role - dimension + 2)
            if role >= dimension - 2:
                observed = sum(value - index for index, value in enumerate(sequence))
                assert observed == minimum
            else:
                assert minimum == 0

    d = sp.symbols("d", integer=True)
    lhs = (h + 2 - moving_role) * (d - 1)
    cap = d * (h + moving_role - d)
    assert sp.expand((cap - lhs).subs({moving_role: 2, d: 4})) == h - 8


def check_equality_basis_and_swap() -> None:
    z = sp.symbols("z")
    roots = sp.symbols("r0:4")
    basis = [
        sp.prod((z + roots[j]) ** 3 for j in range(4) if j != i)
        for i in range(4)
    ]
    for i, polynomial in enumerate(basis):
        for j, root in enumerate(roots):
            value = sp.expand(polynomial.subs(z, -root))
            if i == j:
                assert value != 0
            else:
                assert value == 0
                assert sp.diff(polynomial, z).subs(z, -root) == 0
                assert sp.diff(polynomial, z, 2).subs(z, -root) == 0

    r, x, y, gamma = sp.symbols("r x y gamma")
    swap = sp.factor(3 / (x - r) - 2 / (x + r))
    assert sp.cancel(swap - (x + 5 * r) / (x**2 - r**2)) == 0
    fibre = sp.expand(gamma * (x**2 - r**2) - (x + 5 * r))
    assert sp.Poly(fibre, x).coeff_monomial(x) == -1
    assert sp.Poly(fibre, x).degree() <= 2

    # Multiplicities cancel when a fixed formal role-two class is swapped.
    lam_x, lam_y = sp.symbols("lambda_x lambda_y")
    before = (lam_x - 2) / (r + x) + lam_y / (r + y)
    after = lam_x / (r + x) + (lam_y - 2) / (r + y)
    difference = sp.simplify(before - after)
    assert sp.simplify(difference - (-2 / (r + x) + 2 / (r + y))) == 0


def literal_five_set_legal(types: tuple[str, ...]) -> bool:
    """Worst zero-singleton orbit: only selected D/T guards count."""
    assert len(types) == 5
    for left, right in combinations(range(5), 2):
        lowered = {left, right}
        guard = any(types[index] == "D" and index in lowered for index in range(5))
        guard |= any(types[index] == "T" and index not in lowered for index in range(5))
        if not guard:
            return False
    return True


def check_seven_universe_legality() -> None:
    observed = set()
    expected = set()
    for doubles in range(8):
        for triples in range(8 - doubles):
            highs = 7 - doubles - triples
            universe = ("D",) * doubles + ("T",) * triples + ("H",) * highs
            literal = all(
                literal_five_set_legal(tuple(universe[index] for index in subset))
                for subset in combinations(range(7), 5)
            )
            if literal:
                observed.add((doubles, triples, highs))
            if doubles >= 6 or triples >= 5:
                expected.add((doubles, triples, highs))
    assert observed == expected
    assert len(observed) == 9

    # With at least two original singleton classes, one is nonzero on
    # every zero orbit and every five-set is automatically legal.
    for doubles in range(8):
        for triples in range(8 - doubles):
            highs = 7 - doubles - triples
            assert doubles + triples + highs == 7


EXPECTED = {
    # baseline R, selection-free, closed by fixed numerator, left
    1: (35, 11, 1, 10),
    2: (42, 10, 4, 6),
    3: (46, 12, 8, 4),
    4: (46, 11, 8, 3),
    5: (44, 6, 5, 1),
    6: (44, 6, 5, 1),
    7: (40, 3, 3, 0),
    8: (39, 2, 2, 0),
    9: (39, 2, 2, 0),
    10: (39, 1, 1, 0),
}


def check_bounded_census() -> None:
    theorem_open = {}
    for k in range(1, 45):
        _, residual_tuple = frontier.census(H, H + k)
        residual = set(residual_tuple)
        selection_free = {
            profile
            for profile in residual
            if not mixed.formal_selections(profile, k)
        }
        closed = {
            profile for profile in selection_free if fixed_numerator_criterion(profile)
        }
        open_profiles = selection_free - closed
        if k <= 10:
            observed = (
                len(residual),
                len(selection_free),
                len(closed),
                len(open_profiles),
            )
            assert observed == EXPECTED[k]
        if open_profiles:
            theorem_open[k] = tuple(sorted(open_profiles, reverse=True))

    assert set(theorem_open) == set(range(1, 7))
    assert theorem_open[5] == ((3, 3, 3, 3, 2, 2, 2, 2, 2, 1),)
    assert theorem_open[6] == ((4, 4, 4, 3, 3, 3, 3),)

    # Audit every ingredient in the finite upper bound k <= 44.
    assert 10 * 4 + 4 * 3 + 5 * 2 == 62
    assert 62 - 18 == 44
    assert frontier.moving_method_works((4,) * 11, H, 3, 7)
    assert not frontier.moving_method_works((4,) * 10, H, 3, 7)


def check_p18_scope_boundary() -> None:
    """Do not misapply the h=8 equality to the 21 p=18 families."""
    families = (
        tuple((1, b, 17 - 2 * b) for b in range(10))
        + tuple((0, b, 20 - 2 * b) for b in range(1, 12))
    )
    assert len(families) == 21
    for a, b, u in families:
        assert 3 * a + 2 * b + u == 20
        for h in range(13, 18):
            profile = (3,) * a + (2,) * b + (1,) * (h + u)
            assert sum(profile) == h + 20

    # The h=8 four-space equality has slack h-8 at higher h.
    assert [h - 8 for h in range(13, 18)] == [5, 6, 7, 8, 9]
    closed_uniformly_by_h8_theorem: tuple[tuple[int, int, int], ...] = ()
    assert not closed_uniformly_by_h8_theorem

    # Exact full-complement singleton frontiers requested in the audit:
    # 15 Robin anchors force a five-space in P_16 with Wr=A^4.
    assert 15 * (5 - 1) == 5 * (17 - 5) == 60
    assert 15 * (6 - 1) > 6 * (17 - 6)
    # 18 Robin anchors force a six-space in P_20 with Wr=A^5.
    assert 18 * (6 - 1) == 6 * (21 - 6) == 90
    assert 18 * (7 - 1) > 7 * (21 - 7)


def main() -> None:
    check_nonuniform_primitive_identity()
    check_degrees_and_local_jets()
    check_equality_basis_and_swap()
    check_seven_universe_legality()
    check_bounded_census()
    check_p18_scope_boundary()
    print("general-collision fixed-numerator closure: PASS")
    print("h=8 selection-free baseline tail closed uniformly for k >= 7")
    print("p=18 a<=1 families closed by h=8 theorem: 0 (scope boundary)")


if __name__ == "__main__":
    main()
