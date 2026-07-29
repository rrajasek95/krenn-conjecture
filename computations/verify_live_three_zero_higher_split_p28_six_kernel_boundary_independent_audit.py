#!/usr/bin/env python3
"""Independent audit of the p=28 selected six-kernel frontier.

This checker deliberately does not import the primary p=28 checker.  It
reconstructs the profile and selection ledgers from multiplicity counts,
queries the underlying H/S/C/L/Q/V classifier branch by branch, and audits
the Wronskian and common-lift arithmetic separately.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


P = 28
SPLITS = tuple((h, P - h) for h in range(22, 28))
EXPECTED_FULL = (824, 824, 872, 872, 920, 920)
EXPECTED_REDUCTIONS = {
    22: (824, 676, 12, 17, 705, 119),
    23: (824, 719, 12, 7, 738, 86),
    24: (872, 719, 13, 17, 749, 123),
    25: (872, 762, 13, 7, 782, 90),
    26: (920, 762, 14, 17, 793, 127),
    27: (920, 805, 14, 7, 826, 94),
}
EXPECTED_LOW_E = Counter({0: 101, 1: 79, 2: 60, 3: 44,
                          4: 29, 5: 18, 6: 10, 7: 3})
EXPECTED_LOW_REMAINDER = {
    (0, 10, 0, 0),
    (0, 10, 1, -2),
    (2, 7, 0, 1),
    (2, 7, 1, -1),
    (3, 6, 0, 0),
    (3, 6, 1, -2),
    (7, 0, 0, 2),
    (7, 0, 1, 0),
    (7, 0, 2, -2),
}
EXPECTED_BASELINES = {
    (3,) * 10,
    (4,) * 2 + (3,) * 7 + (1,),
    (4,) * 3 + (3,) * 6,
    (4,) * 7 + (1,),
}


Key = tuple[int, int, int, int]


def selected_gap(q: int, h: int, k: int) -> int:
    """Forced selected-row Wronskian weight minus its degree cap."""
    return q * q - 2 * q - h - 2 + max(0, q - k)


def original_profile(h: int, key: Key) -> tuple[int, ...]:
    e, a, b, u = key
    n1 = h + u
    assert n1 >= 0
    assert 4 * e + 3 * a + 2 * b + u == 30
    return (4,) * e + (3,) * a + (2,) * b + (1,) * n1


def all_bounded_profiles(h: int) -> tuple[Key, ...]:
    """Enumerate all non-all-singleton profiles with parts at most four."""
    answer: list[Key] = []
    total_mass = h + 30
    for e in range(total_mass // 4 + 1):
        for a in range((total_mass - 4 * e) // 3 + 1):
            for b in range((total_mass - 4 * e - 3 * a) // 2 + 1):
                n1 = total_mass - 4 * e - 3 * a - 2 * b
                u = n1 - h
                key = (e, a, b, u)
                if key != (0, 0, 0, 30):
                    answer.append(key)
    return tuple(answer)


def selections(h: int, key: Key) -> tuple[tuple[int, int], ...]:
    """Literal legal pairs (selected exact doubles, selected triples)."""
    _, a, b, u = key
    n1 = h + u
    answer: list[tuple[int, int]] = []
    for x in range(b + 1):
        for t in range(min(1, a) + 1):
            singleton_roles = h + 2 - 2 * (x + t)
            if 0 <= singleton_roles <= n1:
                answer.append((x, t))
    return tuple(answer)


def candidates(h: int) -> dict[Key, tuple[tuple[int, int], ...]]:
    return {
        key: choices
        for key in all_bounded_profiles(h)
        if (choices := selections(h, key))
    }


def complement(h: int, key: Key, x: int, t: int) -> tuple[int, ...]:
    e, a, b, u = key
    n1 = h + u
    singleton_roles = h + 2 - 2 * (x + t)
    parts = (
        (4,) * e
        + (3,) * (a - t)
        + (2,) * (b - x)
        + (1,) * (n1 - singleton_roles + t)
    )
    return tuple(sorted(parts, reverse=True))


def low_role(key: Key) -> bool:
    _, a, b, u = key
    return (
        u >= 2
        or (u >= 0 and a + b >= 1)
        or (u >= -2 and (b >= 2 or (a >= 1 and b >= 1)))
    )


def singleton_options(h: int, key: Key) -> tuple[tuple[int, int, int, int], ...]:
    """All legal moving-singleton choices (x,t,pool,fixed classes)."""
    e, a, b, u = key
    n1 = h + u
    answer: list[tuple[int, int, int, int]] = []
    for x in range(b + 1):
        for t in range(min(1, a) + 1):
            singleton_roles = h + 2 - 2 * (x + t)
            if not 1 <= singleton_roles <= n1:
                continue
            pool = n1 - (singleton_roles - 1)
            fixed_parts = (
                (4,) * e
                + (3,) * (a - t)
                + (2,) * (b - x)
                + (1,) * t
            )
            fixed_classes = len(fixed_parts)
            assert pool + sum(fixed_parts) == 29
            assert pool + fixed_classes - 2 >= 3

            forced_five = 4 * pool + sum(5 - part for part in fixed_parts)
            cap_five = 5 * ((pool + fixed_classes - 2) + 1 - 5)
            assert forced_five - cap_five == 1
            answer.append((x, t, pool, fixed_classes))
    return tuple(answer)


def greedy_singleton(h: int, key: Key) -> tuple[int, int, int, int]:
    e, a, b, u = key
    dmax = (h + 1) // 2
    x = min(b, dmax)
    t = int(a > 0 and x < dmax)
    pool = u - 1 + 2 * (x + t)
    fixed_classes = e + a + b - x
    return x, t, pool, fixed_classes


def singleton_reduces(h: int, key: Key) -> bool:
    options = singleton_options(h, key)
    greedy = greedy_singleton(h, key)
    if not options:
        assert greedy[2] < 1
        return False

    # The claimed optimization is exact: doubles improve 2P-C by five,
    # triples by four, so the prescribed greedy point maximizes the score.
    assert greedy in options
    scores = {option: 2 * option[2] - option[3] for option in options}
    assert scores[greedy] == max(scores.values())

    _, _, pool, fixed_classes = greedy
    for active in range(1, pool + 1):
        quotient_degree = pool + fixed_classes - 2 - 3 * active
        assert (quotient_degree >= 3) == (
            3 * active <= pool + fixed_classes - 5
        )
    return fixed_classes <= 2 * pool + 4


def triple_options(h: int, key: Key) -> tuple[tuple[int, int, tuple[int, ...]], ...]:
    """All legal moving-triple choices (fixed doubles, c, baseline)."""
    e, a, b, u = key
    if a < 2:
        return ()
    n1 = h + u
    answer: list[tuple[int, int, tuple[int, ...]]] = []
    for x in range(b + 1):
        singleton_roles = h - 2 * x
        if not 0 <= singleton_roles <= n1:
            continue
        leftover = n1 - singleton_roles
        selected = (
            (4,) * e
            + (3,) * (a - 1)
            + (2,) * (b - x)
            + (1,) * (leftover + 1)
        )
        baseline = (
            (4,) * e
            + (3,) * a
            + (2,) * (b - x)
            + (1,) * leftover
        )
        classes = len(selected)
        assert sum(selected) == 28 and max(selected) <= 4
        assert len(baseline) == classes and sum(baseline) == 30

        forced_six = sum(6 - part for part in baseline)
        cap_six = 6 * (classes + 1 - 6)
        forced_seven = sum(7 - part for part in baseline)
        cap_seven = 7 * (classes + 1 - 7)
        assert forced_six == cap_six
        assert forced_seven - cap_seven == 12
        answer.append((x, classes, tuple(sorted(baseline, reverse=True))))
    return tuple(answer)


def triple_reduces(h: int, key: Key) -> bool:
    return any(classes <= 8 for _, classes, _ in triple_options(h, key))


def double_options(
    h: int, key: Key
) -> tuple[tuple[int, int, int, int, tuple[int, ...]], ...]:
    """All legal moving-double choices (x,t,c,pool,baseline)."""
    e, a, b, u = key
    if b < 2:
        return ()
    n1 = h + u
    answer: list[tuple[int, int, int, int, tuple[int, ...]]] = []
    for x in range(b - 1):
        for t in range(min(1, a) + 1):
            singleton_roles = h - 2 * x - 2 * t
            if not 0 <= singleton_roles <= n1:
                continue
            leftover = n1 - singleton_roles
            selected = (
                (4,) * e
                + (3,) * (a - t)
                + (2,) * (b - x - 1)
                + (1,) * (leftover + t)
            )
            baseline = selected + (2,)
            classes = len(selected)
            pool = b - x
            assert pool >= 2
            assert sum(selected) == 28 and max(selected) <= 4
            assert len(baseline) == classes + 1 and sum(baseline) == 30

            degree = classes + 1
            forced_six = sum(6 - part for part in baseline)
            cap_six = 6 * (degree + 1 - 6)
            forced_seven = sum(7 - part for part in baseline)
            cap_seven = 7 * (degree + 1 - 7)
            assert forced_six == cap_six
            assert forced_seven - cap_seven == 12
            answer.append(
                (x, t, classes, pool, tuple(sorted(baseline, reverse=True)))
            )
    return tuple(answer)


def double_reduces(h: int, key: Key) -> bool:
    return any(classes <= 9 for _, _, classes, _, _ in double_options(h, key))


def gcd_correction(dimension: int, jet_order: int, gcd_order: int) -> int:
    """Correction relative to the base-point-free exact-jet estimate."""
    base = max(0, dimension - jet_order)
    if gcd_order <= jet_order:
        return (
            dimension * gcd_order
            + max(0, dimension - jet_order + gcd_order)
            - base
        )
    return dimension * gcd_order - base


def audit_boundary_and_wronskians() -> None:
    # Direct reconstruction from selected row weights: d cancels.
    for q in range(4, 13):
        for h in range(13, 35):
            for k in range(1, 16):
                for d in range(0, (h + 2) // 2 + 1):
                    s = h + 2 - 2 * d
                    degree = h + 3 - d
                    forced = d * (q - 2) + s * (q - 1) + max(0, q - k)
                    cap = q * (degree + 1 - q)
                    assert forced - cap == selected_gap(q, h, k)

    for p in range(14, 28):
        for h in range(13, p):
            assert selected_gap(6, h, p - h) > 0
    assert tuple(
        (h, 28 - h)
        for h in range(13, 28)
        if selected_gap(6, h, 28 - h) == 0
    ) == SPLITS
    for h, k in SPLITS:
        assert selected_gap(6, h, k) == 0
        assert selected_gap(7, h, k) == 12
        assert all(selected_gap(q, h, k) > 0 for q in range(7, h + 6))

    # Common factors never relax any exact-jet estimate used below.
    for dimension in range(4, 8):
        for jet_order in range(1, 5):
            for gcd_order in range(0, 10):
                assert gcd_correction(dimension, jet_order, gcd_order) >= 0

    # Uniform p=r(r+3) arithmetic, independently of any profile ledger.
    for r in range(3, 20):
        p = r * (r + 3)
        for classes in range(r + 2, 4 * r + 25):
            singleton_degree = classes - 2
            forced = (r + 1) * classes - (p + 1)
            cap = (r + 1) * (singleton_degree + 1 - (r + 1))
            assert forced - cap == 1

            restored_degree = classes
            forced_eq = (r + 2) * classes - (p + 2)
            cap_eq = (r + 2) * (restored_degree + 1 - (r + 2))
            forced_next = (r + 3) * classes - (p + 2)
            cap_next = (r + 3) * (restored_degree + 1 - (r + 3))
            assert forced_eq == cap_eq
            assert forced_next - cap_next == 2 * (r + 2)

            lower = r - 2
            assert (max(classes - 7, 0) < lower) == (classes <= r + 4)
            assert (max(classes - 8, 0) < lower) == (classes <= r + 5)


def audit_transports_and_intersections() -> None:
    z, x = sp.symbols("z x")
    cubic = sp.expand((z - x) ** 2 * (z + x))
    quartic = sp.expand((z - x) ** 2 * (z + x) ** 2)
    quintic = sp.expand((z - x) ** 3 * (z + x) ** 2)
    assert tuple(sp.Poly(poly, z).degree() for poly in (cubic, quartic, quintic)) == (
        3,
        4,
        5,
    )

    # Local transport: a square kills a first jet, translates a simple
    # relation row to a third-order row, and a cube kills a complete 2-jet.
    coeffs = sp.symbols("r0:5")
    local = sum(coeffs[j] * (z - x) ** j for j in range(5))
    square_local = (z - x) ** 2 * local
    assert square_local.subs(z, x) == 0
    assert sp.diff(square_local, z).subs(z, x) == 0
    assert sp.diff(square_local, z, 3).subs(z, x) == 6 * coeffs[1]
    cube_local = (z - x) ** 3 * local
    assert all(sp.diff(cube_local, z, j).subs(z, x) == 0 for j in range(3))

    def specialize(poly: sp.Expr, value: int) -> sp.Poly:
        return sp.Poly(poly.subs(x, value), z, domain=sp.QQ)

    f1, f2, f0 = (specialize(cubic, value) for value in (1, 2, 0))
    b1, b2 = (specialize(quartic, value) for value in (1, 2))
    g1, g2 = (specialize(quintic, value) for value in (1, 2))
    assert sp.gcd(f1, f2).degree() == 0
    assert sp.gcd(f0, f1).degree() == 0
    assert sp.gcd(b1, b2).degree() == 0
    assert sp.gcd(g1, g2).degree() == 0

    def multiplication_space(poly: sp.Poly, residual_degree: int, total: int) -> sp.Matrix:
        if residual_degree < 0:
            return sp.zeros(total + 1, 0)
        columns = []
        for power in range(residual_degree + 1):
            product = sp.Poly(poly.as_expr() * z**power, z, domain=sp.QQ)
            columns.append(
                sp.Matrix([product.nth(degree) for degree in range(total + 1)])
            )
        return sp.Matrix.hstack(*columns)

    # Verify the coprime intersection dimensions by exact coefficient ranks,
    # rather than assuming the product-divisibility formula in the note.
    for classes in range(4, 19):
        ub = multiplication_space(b1, classes - 4, classes)
        vb = multiplication_space(b2, classes - 4, classes)
        intersection_b = ub.cols + vb.cols - ub.row_join(vb).rank()
        assert intersection_b == max(classes - 7, 0)

        ug = multiplication_space(g1, classes - 4, classes + 1)
        vg = multiplication_space(g2, classes - 4, classes + 1)
        intersection_g = ug.cols + vg.cols - ug.row_join(vg).rank()
        assert intersection_g == max(classes - 8, 0)


def audit_census_classifier_and_reductions() -> None:
    full_counts: list[int] = []
    low_reference: set[Key] | None = None

    for h, k in SPLITS:
        observed = candidates(h)
        full_counts.append(len(observed))

        # Every literal selection saturates both the selected six-space and
        # relation four-space Wronskians.
        for key, choices in observed.items():
            profile = original_profile(h, key)
            assert sum(profile) == h + 30 and max(profile) <= 4
            for x, t in choices:
                d = x + t
                singleton_roles = h + 2 - 2 * d
                comp = complement(h, key, x, t)
                assert sum(comp) == 28 and max(comp) <= 4

                forced_selected = 4 * d + 5 * singleton_roles + (6 - k)
                cap_selected = 6 * ((h + 3 - d) + 1 - 6)
                assert forced_selected == cap_selected

                classes = len(comp)
                forced_relation = sum(4 - part for part in comp)
                cap_relation = 4 * ((classes - 4) + 1 - 4)
                assert forced_relation == cap_relation

        # Audit each classifier branch, not only its final label.
        statuses = Counter()
        for key in observed:
            profile = original_profile(h, key)
            assert profile != (1,) * sum(profile)
            assert max(profile) < h
            assert frontier.short_witness(profile, h) is None
            assert not frontier.moving_method_works(profile, h, 1, 3)
            assert not frontier.moving_method_works(profile, h, 2, 5)
            assert not frontier.moving_method_works(profile, h, 3, 7)
            assert not frontier.wronskian_value_core_closes(profile, h, 28)
            statuses[frontier.classify(profile, h, 28)] += 1
        assert statuses == Counter({"R": len(observed)})

        low = {key for key in observed if low_role(key)}
        literal_low = {
            key
            for key, choices in observed.items()
            if any(x + t <= 2 for x, t in choices)
        }
        assert low == literal_low
        assert len(low) == 344
        assert Counter(key[0] for key in low) == EXPECTED_LOW_E
        if low_reference is None:
            low_reference = low
        else:
            assert low == low_reference

        singleton = {key for key in observed if singleton_reduces(h, key)}
        triple = {key for key in observed if triple_reduces(h, key)}
        double = {key for key in observed if double_reduces(h, key)}
        triple_new = triple - singleton
        double_new = double - singleton - triple
        union = singleton | triple | double
        row = (
            len(observed),
            len(singleton),
            len(triple_new),
            len(double_new),
            len(union),
            len(set(observed) - union),
        )
        assert row == EXPECTED_REDUCTIONS[h]

        low_singleton = low & singleton
        low_triple_new = (low & triple) - low_singleton
        low_double_new = (low & double) - low_singleton - low_triple_new
        assert len(low_singleton) == 333
        assert len(low_triple_new) == 2
        assert not low_double_new
        assert low - union == EXPECTED_LOW_REMAINDER

    assert tuple(full_counts) == EXPECTED_FULL

    # The nine residual parameter tuples restore to exactly four natural
    # saturated baselines.  This does not assert that any profile is closed.
    baselines: set[tuple[int, ...]] = set()
    h = 22
    for key in EXPECTED_LOW_REMAINDER:
        e, a, b, _ = key
        if a:
            options = triple_options(h, key)
            chosen = [baseline for x, _, baseline in options if x == b]
            assert chosen
            baselines.add(chosen[0])
        else:
            _, _, pool, _ = greedy_singleton(h, key)
            assert pool == 1
            baselines.add((4,) * e + (1,) * pool)
    assert baselines == EXPECTED_BASELINES


def main() -> None:
    audit_boundary_and_wronskians()
    audit_transports_and_intersections()
    audit_census_classifier_and_reductions()
    print("independent p=28 six-kernel boundary audit: PASS")
    print("q=6 first equality splits: (22,6) through (27,1); q=7 excess: 12")
    print("profile counts: 824,824,872,872,920,920; every classifier status: R")
    print("d<=2 ledger: 344; explicit dimension drops: 335; residual cores: 9")
    print("scope guard: dimension-drop frontier only, not profile closure")


if __name__ == "__main__":
    main()
