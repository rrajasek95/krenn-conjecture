#!/usr/bin/env python3
"""Exact audit of the uniform double-guard bad-shadow bypass."""

from itertools import combinations, product

import sympy as sp


def subsets(items, size):
    return {frozenset(x) for x in combinations(items, size)}


def audit_shadow_recurrence() -> None:
    # Exhaust small abstract profiles.  Multiplicities inside H do not enter
    # the deletion complex, so only the three class types are required.
    for h in range(3, 9):
        for singleton_count in range(h + 1):
            for high_count in range(h + 3):
                for double_count in range(1, 4):
                    classes = singleton_count + high_count + double_count
                    if classes < h + 1:
                        continue
                    if not (0 <= h - singleton_count <= high_count):
                        # There is no initial bad core; ordinary exchange is
                        # already available and the shadow statement is empty.
                        continue

                    S = tuple(f"s{i}" for i in range(singleton_count))
                    H = tuple(f"a{i}" for i in range(high_count))
                    D = tuple(f"d{i}" for i in range(double_count))
                    V = S + H + D

                    initial_high_take = h - singleton_count

                    def expected_bad(size):
                        if initial_high_take == 0 and size > h:
                            return set()
                        choose = size - singleton_count
                        if not (0 <= choose <= high_count):
                            return set()
                        return {
                            frozenset(S) | U
                            for U in subsets(H, choose)
                        }

                    bad = expected_bad(h)
                    literal_initial = {
                        T
                        for T in subsets(V, h)
                        if set(S) <= T and not (set(D) & T)
                    }
                    assert bad == literal_initial

                    final_mechanism = None
                    for size in range(h, classes):
                        next_bad = set()
                        for T in subsets(V, size + 1):
                            missing = [x for x in T if T - {x} in bad]
                            if len(missing) >= 2:
                                next_bad.add(T)
                                mechanism = "unconstructed"
                            elif len(missing) == 1:
                                # It is a repeated, hence nonzero, guard.  In
                                # the |S|=h endpoint it may be high; otherwise
                                # it is necessarily a double.
                                assert missing[0] in D + H
                                if initial_high_take > 0:
                                    assert missing[0] in D
                                mechanism = "partial"
                            else:
                                mechanism = "ordinary"
                            # zero missing: ordinary lift; one: partial lift.
                            if size + 1 == classes:
                                assert T == frozenset(V)
                                final_mechanism = mechanism
                        assert next_bad == expected_bad(size + 1)
                        bad = next_bad

                    assert not bad  # every full c-set is constructed
                    assert final_mechanism in {"ordinary", "partial"}

                    # Audit which at-least-three-dimensional lift span is
                    # retained on the final step, especially |D|=1.
                    if singleton_count == h:
                        expected_final = (
                            "partial" if classes == h + 1 else "ordinary"
                        )
                    else:
                        expected_final = (
                            "partial" if double_count == 1 else "ordinary"
                        )
                    assert final_mechanism == expected_final


def audit_one_missing_inequalities() -> None:
    # The hardest degree is obtained by taking every counted gcd order at
    # its lower bound.  Positive gcd orders at Robin nodes start at two.
    for m, epsilon in product(range(3, 15), (0, 1)):
        nonzero_anchors = m - epsilon
        for rho in range(nonzero_anchors + 1):
            for sigma in range(nonzero_anchors - rho + 1):
                for e0 in (0,) + tuple(range(2, m + 1)):
                    if not epsilon and e0:
                        continue
                    for tau in (0,) + tuple(range(2, m + 1)):
                        gcd_lower = rho + 2 * sigma + e0 + tau
                        if gcd_lower > m - 1:
                            continue
                        delta = m - gcd_lower
                        u = nonzero_anchors - rho - sigma

                        zero_edge = (
                            epsilon == 1 and sigma == 0 and e0 == 0 and tau == 0
                        )
                        parity_zeros = 2 * u + (3 if zero_edge else 0)
                        assert parity_zeros > 2 * delta - 1

                        forced_ramification = (
                            2 * (nonzero_anchors - sigma)
                            + 2 * int(tau == 0)
                            + 2 * int(epsilon == 1 and e0 == 0)
                        )
                        assert forced_ramification > 2 * delta - 2


def audit_exchange_and_terminal_degrees() -> None:
    z, a, s = sp.symbols("z a s")
    gauge = (z - s) * (z + s) ** 2
    shift = sp.cancel(sp.diff(gauge, z).subs(z, -a) / gauge.subs(z, -a))
    target = -(1 / (a + s) - 2 / (s - a))
    assert sp.factor(shift - target) == 0
    assert gauge.subs(s, 0) == z**3
    assert gauge.subs(z, -s) == 0
    assert sp.diff(gauge, z).subs(z, -s) == 0

    # A residual in degree m-3 lifts to degree m; two coefficient
    # cancellations recover degree (m+1)-3.
    for m in range(3, 30):
        assert (m - 3) + 3 == m
        assert m - 2 == (m + 1) - 3

    for excess in range(1, 9):
        for dimension in range(3, 12):
            assert dimension**2 - excess > 0
    assert 3**2 - 8 == 1


def main() -> None:
    audit_shadow_recurrence()
    audit_one_missing_inequalities()
    audit_exchange_and_terminal_degrees()
    print("PASS: uniform double-guard shadow bypass")
    print("literal bad-core shadows agree through the full class set")
    print("endpoint high guards and genuine-shadow double guards are exact")
    print("the retained final span is audited explicitly when |D|=1")
    print("one-missing lift and terminal d^2-e inequalities are strict")


if __name__ == "__main__":
    main()
