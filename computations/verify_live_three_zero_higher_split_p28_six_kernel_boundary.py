#!/usr/bin/env python3
"""Exact audit of the first selected six-kernel boundary at p=28."""

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
FULL_COUNTS = {22: 824, 23: 824, 24: 872, 25: 872, 26: 920, 27: 920}
REDUCTION_COUNTS = {
    22: (824, 676, 12, 17, 705, 119),
    23: (824, 719, 12, 7, 738, 86),
    24: (872, 719, 13, 17, 749, 123),
    25: (872, 762, 13, 7, 782, 90),
    26: (920, 762, 14, 17, 793, 127),
    27: (920, 805, 14, 7, 826, 94),
}

LOW_REMAINDER = {
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


def selected_gap(q: int, h: int, k: int) -> int:
    return q * q - 2 * q - h - 2 + max(0, q - k)


def profile(h: int, key: tuple[int, int, int, int]) -> tuple[int, ...]:
    e, a, b, u = key
    assert 4 * e + 3 * a + 2 * b + u == 30
    assert h + u >= 0
    return (4,) * e + (3,) * a + (2,) * b + (1,) * (h + u)


def formal_choices(
    h: int, key: tuple[int, int, int, int]
) -> tuple[tuple[int, int], ...]:
    """Pairs (x,t): x selected doubles and t selected triples."""
    _, a, b, u = key
    total_singletons = h + u
    answer = []
    for t in range(min(1, a) + 1):
        for x in range(b + 1):
            d = x + t
            selected_singletons = h + 2 - 2 * d
            if 0 <= selected_singletons <= total_singletons:
                answer.append((x, t))
    return tuple(answer)


def candidates(h: int) -> dict[tuple[int, int, int, int], tuple[tuple[int, int], ...]]:
    """All non-D p=28 profiles with a legal formal selection."""
    answer = {}
    total = h + 30
    for e in range(total // 4 + 1):
        for a in range(total // 3 + 1):
            for b in range(total // 2 + 1):
                u = 30 - 4 * e - 3 * a - 2 * b
                key = (e, a, b, u)
                if h + u < 0 or key == (0, 0, 0, 30):
                    continue
                choices = formal_choices(h, key)
                if choices:
                    answer[key] = choices
    return answer


def low_role_applicable(key: tuple[int, int, int, int]) -> bool:
    _, a, b, u = key
    return (
        u >= 2
        or (u >= 0 and a + b >= 1)
        or (u >= -2 and (b >= 2 or (a >= 1 and b >= 1)))
    )


def selected_complement(
    h: int, key: tuple[int, int, int, int], x: int, t: int
) -> tuple[int, ...]:
    e, a, b, u = key
    d = x + t
    selected_singletons = h + 2 - 2 * d
    leftover_singletons = h + u - selected_singletons
    parts = (
        (4,) * e
        + (3,) * (a - t)
        + (2,) * (b - x)
        + (1,) * (leftover_singletons + t)
    )
    return tuple(sorted(parts, reverse=True))


def singleton_choice(
    h: int, key: tuple[int, int, int, int]
) -> tuple[int, int, int, int]:
    """Greedy moving-singleton choice (x,t,P,C)."""
    e, a, b, u = key
    dmax = (h + 1) // 2  # retain at least one singleton role
    x = min(b, dmax)
    t = int(a > 0 and x < dmax)
    pool = u - 1 + 2 * (x + t)
    fixed_classes = e + a + b - x
    return x, t, pool, fixed_classes


def singleton_reduces(h: int, key: tuple[int, int, int, int]) -> bool:
    x, t, pool, fixed_classes = singleton_choice(h, key)
    if pool < 1:
        return False

    e, a, b, _ = key
    fixed_parts = (
        (4,) * e
        + (3,) * (a - t)
        + (2,) * (b - x)
        + (1,) * t
    )
    assert len(fixed_parts) == fixed_classes
    assert pool + sum(fixed_parts) == 29

    degree = pool + fixed_classes - 2
    forced_five = 4 * pool + sum(5 - part for part in fixed_parts)
    cap_five = 5 * (degree + 1 - 5)
    assert forced_five - cap_five == 1

    # If m pool selections were active, a common four-space after
    # division by their 3m-degree product would need degree at least 3.
    for active in range(1, pool + 1):
        possible = 3 * active <= pool + fixed_classes - 5
        quotient_degree = degree - 3 * active
        assert possible == (quotient_degree >= 3)

    return fixed_classes <= 2 * pool + 4


def triple_options(
    h: int, key: tuple[int, int, int, int]
) -> tuple[tuple[int, int], ...]:
    """Pairs (x,c) for a moving triple and x fixed doubles."""
    e, a, b, u = key
    if a < 2:
        return ()
    answer = []
    for x in range(b + 1):
        d = x + 1
        leftover_singletons = u + 2 * x
        if d > (h + 2) // 2 or leftover_singletons < 0:
            continue
        classes = e + a + b + u + x

        selected = (
            (4,) * e
            + (3,) * (a - 1)
            + (2,) * (b - x)
            + (1,) * (leftover_singletons + 1)
        )
        baseline = (
            (4,) * e
            + (3,) * a
            + (2,) * (b - x)
            + (1,) * leftover_singletons
        )
        assert sum(selected) == 28
        assert len(selected) == classes
        assert sum(baseline) == 30
        assert len(baseline) == classes

        forced_six = sum(6 - part for part in baseline)
        cap_six = 6 * (classes + 1 - 6)
        forced_seven = sum(7 - part for part in baseline)
        cap_seven = 7 * (classes + 1 - 7)
        assert forced_six == cap_six
        assert forced_seven - cap_seven == 12

        pair_dimension = max(classes - 7, 0)
        assert (pair_dimension <= 1) == (classes <= 8)
        answer.append((x, classes))
    return tuple(answer)


def triple_reduces(h: int, key: tuple[int, int, int, int]) -> bool:
    return any(classes <= 8 for _, classes in triple_options(h, key))


def double_options(
    h: int, key: tuple[int, int, int, int]
) -> tuple[tuple[int, int, int, int], ...]:
    """Tuples (x,t,c,pool) for a moving double family."""
    e, a, b, u = key
    if b < 2:
        return ()
    answer = []
    for t in range(min(1, a) + 1):
        for x in range(b - 1):  # retain at least two moving doubles
            d = 1 + x + t
            leftover_singletons = u + 2 * x + 2 * t
            if d > (h + 2) // 2 or leftover_singletons < 0:
                continue
            classes = e + a + b + u + x + 2 * t - 1
            pool = b - x

            selected = (
                (4,) * e
                + (3,) * (a - t)
                + (2,) * (b - x - 1)
                + (1,) * (leftover_singletons + t)
            )
            baseline = selected + (2,)
            assert sum(selected) == 28
            assert len(selected) == classes
            assert sum(baseline) == 30
            assert len(baseline) == classes + 1

            common_degree = classes + 1
            forced_six = sum(6 - part for part in baseline)
            cap_six = 6 * (common_degree + 1 - 6)
            forced_seven = sum(7 - part for part in baseline)
            cap_seven = 7 * (common_degree + 1 - 7)
            assert forced_six == cap_six
            assert forced_seven - cap_seven == 12

            pair_dimension = max(classes - 8, 0)
            assert (pair_dimension <= 1) == (classes <= 9)
            answer.append((x, t, classes, pool))
    return tuple(answer)


def double_reduces(h: int, key: tuple[int, int, int, int]) -> bool:
    return any(classes <= 9 for _, _, classes, _ in double_options(h, key))


def audit_first_boundary() -> None:
    for p in range(14, 28):
        for h in range(13, p):
            k = p - h
            assert selected_gap(6, h, k) > 0

    zeros = []
    for h in range(13, 28):
        k = 28 - h
        gap = selected_gap(6, h, k)
        if gap == 0:
            zeros.append((h, k))
        else:
            assert gap > 0
    assert tuple(zeros) == SPLITS
    assert all(selected_gap(7, h, k) == 12 for h, k in SPLITS)


def audit_uniform_first_threshold_lifts() -> None:
    for relation_dimension in range(3, 30):
        r = relation_dimension
        first_mass = r * (r + 3)

        # A moving-singleton baseline has mass p+1 and degree C-2.
        # Its hypothetical (r+1)-space misses the cap by one.
        common_classes = 5 * r + 17
        singleton_mass = first_mass + 1
        singleton_forced = (r + 1) * common_classes - singleton_mass
        singleton_degree = common_classes - 2
        singleton_cap = (r + 1) * (
            singleton_degree + 1 - (r + 1)
        )
        assert singleton_forced - singleton_cap == 1

        for active in range(1, 20):
            quotient_degree = singleton_degree - 3 * active
            possible = quotient_degree >= r - 1
            assert possible == (
                3 * active <= common_classes - r - 1
            )

        # Restoring a moving triple or double gives mass p+2 and a
        # polynomial degree equal to the number of baseline classes.
        restored_mass = first_mass + 2
        assert restored_mass == (r + 1) * (r + 2)
        restored_degree = common_classes
        equality_forced = (r + 2) * common_classes - restored_mass
        equality_cap = (r + 2) * (
            restored_degree + 1 - (r + 2)
        )
        next_forced = (r + 3) * common_classes - restored_mass
        next_cap = (r + 3) * (
            restored_degree + 1 - (r + 3)
        )
        assert equality_forced == equality_cap
        assert next_forced - next_cap == 2 * (r + 2)

        # Two transported r-spaces in an at-most-(r+2)-space meet in
        # dimension at least r-2.  Compare this with the quartic and
        # quintic pair ambient dimensions.
        for classes in range(1, 3 * r + 20):
            lower = r - 2
            quartic_pair = max(classes - 7, 0)
            quintic_pair = max(classes - 8, 0)
            assert (quartic_pair < lower) == (classes <= r + 4)
            assert (quintic_pair < lower) == (classes <= r + 5)


def audit_relation_boundary() -> None:
    # The q=6 truncated-mass condition at mass 28 is equivalent to all
    # complementary parts being at most four.
    for parts in frontier.partitions(28):
        truncated = sum(min(part, 4) for part in parts)
        assert (truncated >= 28) == (max(parts) <= 4)


def audit_census_and_equality() -> None:
    low_reference = None
    for h, k in SPLITS:
        observed = candidates(h)
        assert len(observed) == FULL_COUNTS[h]

        # Every boundary candidate remains R under the currently audited
        # route classifier.
        assert all(
            frontier.classify(profile(h, key), h, 28) == "R"
            for key in observed
        )

        low = {key for key in observed if low_role_applicable(key)}
        assert len(low) == 344
        if low_reference is None:
            low_reference = low
        else:
            assert low == low_reference
        assert Counter(key[0] for key in low) == {
            0: 101,
            1: 79,
            2: 60,
            3: 44,
            4: 29,
            5: 18,
            6: 10,
            7: 3,
        }

        # Audit every formal selection, not just one witness per profile.
        for key, choices in observed.items():
            for x, t in choices:
                d = x + t
                selected_singletons = h + 2 - 2 * d
                complement = selected_complement(h, key, x, t)
                assert sum(complement) == 28
                assert max(complement) <= 4

                selected_forced = (
                    4 * d
                    + 5 * selected_singletons
                    + max(0, 6 - k)
                )
                selected_cap = 6 * ((h + 3 - d) + 1 - 6)
                assert selected_forced == selected_cap

                classes = len(complement)
                relation_forced = sum(4 - part for part in complement)
                relation_cap = 4 * ((classes - 4) + 1 - 4)
                assert relation_forced == relation_cap
                assert sum(min(part, 4) for part in complement) == 28


def audit_transports() -> None:
    z, x = sp.symbols("z x")
    f = sp.expand((z - x) ** 2 * (z + x))
    quartic = sp.expand((z - x) ** 2 * (z + x) ** 2)
    quintic = sp.expand((z - x) ** 3 * (z + x) ** 2)
    assert sp.Poly(f, z).degree() == 3
    assert sp.Poly(quartic, z).degree() == 4
    assert sp.Poly(quintic, z).degree() == 5

    r0, r1, r2 = sp.symbols("r0 r1 r2")
    local = r0 + r1 * (z - x) + r2 * (z - x) ** 2
    assert sp.diff((z - x) ** 2 * local, z, 3).subs(z, x) == 6 * r1
    assert sp.diff((z - x) ** 3 * local, z, 2).subs(z, x) == 0


def audit_reductions() -> None:
    for h, _ in SPLITS:
        keys = set(candidates(h))
        singleton = {key for key in keys if singleton_reduces(h, key)}
        triple = {key for key in keys if triple_reduces(h, key)}
        double = {key for key in keys if double_reduces(h, key)}

        triple_new = triple - singleton
        double_new = double - singleton - triple
        union = singleton | triple | double
        observed = (
            len(keys),
            len(singleton),
            len(triple_new),
            len(double_new),
            len(union),
            len(keys - union),
        )
        assert observed == REDUCTION_COUNTS[h]

        low = {key for key in keys if low_role_applicable(key)}
        low_singleton = low & singleton
        low_triple_new = (low & triple) - low_singleton
        low_double_new = (low & double) - low_singleton - low_triple_new
        assert len(low_singleton) == 333
        assert len(low_triple_new) == 2
        assert not low_double_new
        assert low - union == LOW_REMAINDER


def main() -> None:
    audit_first_boundary()
    audit_uniform_first_threshold_lifts()
    audit_relation_boundary()
    audit_census_and_equality()
    audit_transports()
    audit_reductions()
    print("p=28 first selected six-kernel boundary: PASS")
    print("full profile counts: 824,824,872,872,920,920")
    print("d<=2 subledger: 344; common lifts force 335 dimension drops")
    print("remaining d<=2 equality cores: 9")


if __name__ == "__main__":
    main()
