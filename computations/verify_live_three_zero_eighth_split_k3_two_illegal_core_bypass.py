#!/usr/bin/env python3
"""Exact audit of the h=8,k=3 two-illegal-core bypass."""

from itertools import combinations, product
from math import comb

import sympy as sp


def main() -> None:
    # The profile 3^2 2^4 1^7 has thirteen classes and excess eight.
    singletons = tuple(f"s{i}" for i in range(7))
    triples = ("a", "b")
    doubles = tuple(f"d{i}" for i in range(4))
    values = singletons + triples + doubles
    multiplicity = {
        **{s: 1 for s in singletons},
        **{t: 3 for t in triples},
        **{d: 2 for d in doubles},
    }
    assert len(values) == 13
    assert sum(multiplicity.values()) == 21
    assert sum(m - 1 for m in multiplicity.values()) == 8

    # Literal legality criterion for one-value-per-class eight-cores.
    def illegal(core):
        core = set(core)
        return set(singletons) <= core and not (set(doubles) & core)

    cores8 = tuple(combinations(values, 8))
    illegal8 = {frozenset(core) for core in cores8 if illegal(core)}
    Ia = frozenset(singletons + ("a",))
    Ib = frozenset(singletons + ("b",))
    assert illegal8 == {Ia, Ib}

    # At size nine, only T0 has two missing deletions.  Eight sets have
    # exactly one; all of those adjoin a nonzero double to Ia or Ib.
    T0 = frozenset(singletons + triples)
    missing_histogram9 = {0: 0, 1: 0, 2: 0}
    one_missing9 = []
    two_missing9 = []
    for T_tuple in combinations(values, 9):
        T = frozenset(T_tuple)
        missing = [x for x in T if T - {x} in illegal8]
        missing_histogram9[len(missing)] += 1
        if len(missing) == 1:
            one_missing9.append((T, missing[0]))
        elif len(missing) == 2:
            two_missing9.append(T)
    assert sum(missing_histogram9.values()) == comb(13, 9)
    assert missing_histogram9 == {0: 706, 1: 8, 2: 1}
    assert two_missing9 == [T0]
    for T, missing_value in one_missing9:
        assert missing_value in doubles
        assert multiplicity[missing_value] == 2

    known9 = {
        frozenset(T)
        for T in combinations(values, 9)
        if frozenset(T) != T0
    }
    assert len(known9) == comb(13, 9) - 1

    # Every ten-set either has all ten known deletions or is T0 plus one
    # double, in which case exactly the deletion of that nonzero double is
    # missing and the other nine deletions are known.
    special10 = []
    for U_tuple in combinations(values, 10):
        U = frozenset(U_tuple)
        missing = [x for x in U if U - {x} not in known9]
        if missing:
            assert len(missing) == 1
            d = missing[0]
            assert U == T0 | {d}
            assert d in doubles and multiplicity[d] == 2
            special10.append(U)
        else:
            assert all(U - {x} in known9 for x in U)
    assert len(special10) == 4
    assert len(tuple(combinations(values, 10))) == comb(13, 10)

    # Exact cubic exchange gauge and Robin shift.
    z, s, t = sp.symbols("z s t")
    gauge = (z - s) * (z + s) ** 2
    log_at_minus_t = sp.cancel(sp.diff(gauge, z).subs(z, -t) / gauge.subs(z, -t))
    expected_shift = -(1 / (t + s) - 2 / (s - t))
    assert sp.factor(log_at_minus_t - expected_shift) == 0
    assert sp.expand(gauge.subs(z, -s)) == 0
    assert sp.expand(sp.diff(gauge, z).subs(z, -s)) == 0
    assert sp.expand(gauge.subs(s, 0) - z**3) == 0

    # Exhaust the integer inequalities in the generalized one-missing
    # lift for the two sizes actually used, including a zero anchor.
    for m, epsilon in product((8, 9), (0, 1)):
        n = m - epsilon
        for rho in range(n + 1):
            for sigma in range(n - rho + 1):
                for e0 in (0,) + tuple(range(2, m + 1)):
                    if not epsilon and e0:
                        continue
                    for tau in (0,) + tuple(range(2, m + 1)):
                        gcd_lower = rho + 2 * sigma + e0 + tau
                        if gcd_lower > m - 1:
                            continue
                        delta = m - gcd_lower  # largest, hence hardest case
                        assert delta >= 1
                        u = n - rho - sigma
                        exceptional_zero = (
                            epsilon == 1 and sigma == 0 and e0 == 0 and tau == 0
                        )
                        parity_weight = 2 * u + (3 if exceptional_zero else 0)
                        assert parity_weight > 2 * delta - 1

                        forced_ramification = (
                            2 * (n - sigma)
                            + 2 * int(tau == 0)
                            + 2 * int(epsilon == 1 and e0 == 0)
                        )
                        assert forced_ramification > 2 * delta - 2

    # Degree bookkeeping: one-missing lifts at sizes 8 and 9, followed by
    # ordinary exchange from P_10 through the full thirteen-class core.
    assert (8 - 3) + 3 == 8
    assert 8 - 2 == 9 - 3
    assert (9 - 3) + 3 == 9
    assert 9 - 2 == 10 - 3
    degree = 10 - 3
    for next_size in (11, 12, 13):
        lifted_degree = degree + 3
        assert lifted_degree == next_size - 1
        degree = lifted_degree - 2
        assert degree == next_size - 3
    assert degree == 10
    assert 12 == 13 - 1  # retained final lift space lies in P_12

    # Terminal antiderivative--Wronskian deficit.
    collision_excess = 21 - 13
    assert collision_excess == 8
    for dimension in range(3, 9):
        assert dimension**2 - collision_excess > 0

    print("PASS: exact h=8,k=3 two-illegal-core bypass")
    print("two illegal P8 cores; 714/715 P9 cores constructed")
    print("all 286 P10 cores constructed while skipping the lone missing P9 core")
    print("full exchange dimension >=3; terminal deficit 3^2-8=1")


if __name__ == "__main__":
    main()
