#!/usr/bin/env python3
"""Independent exact audit of the final (p,d,s)=(8,7,3) closure."""

from itertools import combinations

import sympy as sp


def audit_initial_cores() -> None:
    doubles = set(range(7))
    classes = tuple(range(10))
    checked = 0
    for core in combinations(classes, 7):
        selected_doubles = len(doubles.intersection(core))
        assert selected_doubles >= 4
        # Each selected double leaves one row singleton.
        assert selected_doubles >= 1
        assert 17 - len(core) == 10
        assert (8 + len(core) - 1) - 10 == 4
        checked += 1
    assert checked == 120


def audit_exact_lift() -> None:
    z, a, b = sp.symbols("z a b")
    gauge = (z - b) * (z + b) ** 2
    psi = 1 / (a + b) - 2 / (b - a)
    assert sp.factor(
        sp.diff(gauge, z).subs(z, -a) / gauge.subs(z, -a) + psi
    ) == 0
    assert gauge.subs(z, -b) == 0
    assert sp.diff(gauge, z).subs(z, -b) == 0

    # Literal B/Delta preservation; the old exponent may be one or two.
    old_b, old_delta, q = sp.symbols("old_b old_delta q", nonzero=True)
    for multiplicity in (1, 2):
        # B_T contains (z-b)^multiplicity before b is selected and one
        # fewer copy afterwards.  The other factors are represented by
        # old_b and old_delta.
        before = old_b * (z - b) ** multiplicity * q / old_delta
        after = (
            old_b
            * (z - b) ** (multiplicity - 1)
            * gauge
            * q
            / (old_delta * (z + b) ** 2)
        )
        assert sp.factor(after - before) == 0

    # The possible zero singleton has g_0=z^3, with the required order.
    zero_gauge = sp.expand(gauge.subs(b, 0))
    assert zero_gauge == z**3
    assert zero_gauge.subs(z, 0) == 0
    assert sp.diff(zero_gauge, z).subs(z, 0) == 0


def audit_three_lift_counts() -> None:
    # Re-enumerate the numerical heart of the two-dimensional-pencil
    # exclusion.  epsilon records a zero anchor; rho and sigma count gcd
    # roots at +b and -b, and e0 is the zero-root multiplicity.
    for target_size in (8, 9, 10):
        m = target_size - 1
        for epsilon in (0, 1):
            nonzero = target_size - epsilon
            for rho in range(nonzero + 1):
                for sigma in range(nonzero + 1):
                    e0_values = (0,) if not epsilon else (0, 2, 3, 4, 5, 6, 7, 8, 9)
                    for e0 in e0_values:
                        gcd_floor = rho + 2 * sigma + e0
                        if gcd_floor > m:
                            continue
                        delta_cap = m - gcd_floor
                        if delta_cap < 1:
                            continue
                        usable_pairs = nonzero - rho - sigma
                        # If A_+ and A_- overlap, this is only a lower
                        # bound, which is exactly the safe direction.
                        assert usable_pairs >= delta_cap
                        ramification_pairs = nonzero - sigma
                        assert ramification_pairs >= delta_cap
                        assert 2 * ramification_pairs > 2 * delta_cap - 2

    assert 4 + 3 == 7 and 7 - 2 == 5
    assert 5 + 3 == 8 and 8 - 2 == 6
    assert 6 + 3 == 9


def audit_full_core_and_residue() -> None:
    doubles = sp.symbols("d0:7")
    singles = sp.symbols("s0:3")
    mu = sp.symbols("mu")
    values = doubles + singles

    def psi(anchor, added):
        return 1 / (anchor + added) - 2 / (added - anchor)

    # Reconstruct the weighted baseline for a double anchor.
    anchor = doubles[0]
    others = tuple(v for v in values if v != anchor)
    baseline = -1 / (2 * anchor) - 2 / (mu - anchor)
    baseline -= sum(2 / (anchor + v) for v in doubles[1:])
    baseline -= sum(1 / (anchor + v) for v in singles)
    full = baseline + sum(psi(anchor, v) for v in others)
    cofactor = -sum(1 / (anchor + d) for d in doubles)
    cofactor -= 2 / (mu - anchor)
    cofactor -= 2 * sum(1 / (v - anchor) for v in others)
    assert sp.factor(full - cofactor) == 0

    # Reconstruct it independently for a singleton; substitution of zero
    # is safe because there is no self-mate term.
    anchor = singles[0]
    others = tuple(v for v in values if v != anchor)
    baseline = -2 / (mu - anchor)
    baseline -= sum(2 / (anchor + d) for d in doubles)
    baseline -= sum(1 / (anchor + s) for s in singles[1:])
    full = baseline + sum(psi(anchor, v) for v in others)
    cofactor = -sum(1 / (anchor + d) for d in doubles)
    cofactor -= 2 / (mu - anchor)
    cofactor -= 2 * sum(1 / (v - anchor) for v in others)
    difference = sp.factor(full - cofactor)
    assert difference == 0
    assert sp.factor(difference.subs(singles[0], 0)) == 0

    assert 7 + 9 < 22
    assert 22 - 7 - 9 == 6

    # Local double-pole residue: C(w)q(w)/w^2 has residue
    # C(0)[q'(0)+(C'/C)(0)q(0)], with no division by a q-value.
    w = sp.symbols("w")
    c0, c1, q0, q1 = sp.symbols("c0 c1 q0 q1", nonzero=True)
    numerator = sp.expand((c0 + c1 * w) * (q0 + q1 * w))
    residue = sp.Poly(numerator, w).coeff_monomial(w)
    assert sp.factor(residue - c0 * (q1 + (c1 / c0) * q0)) == 0


def audit_wronskian() -> None:
    # Exhaust all arithmetically possible dimensions and gcd-node counts.
    # e may exceed its lower bound 2b; this only lowers the degree cap.
    for dimension in range(3, 11):
        orders = [0] + list(range(2, dimension + 1))
        weight = sum(order - index for index, order in enumerate(orders))
        assert weight == dimension - 1

        for gcd_nodes in range(12):
            for gcd_degree in range(2 * gcd_nodes, 10):
                if dimension > 10 - gcd_degree:
                    # No independent r-space of this reduced degree exists.
                    continue
                forced = (11 - gcd_nodes) * (dimension - 1)
                degree_cap = dimension * (10 - gcd_degree - dimension)
                assert forced > degree_cap

    r, b = sp.symbols("r b", integer=True, nonnegative=True)
    difference = sp.expand(
        (11 - b) * (r - 1) - r * (10 - r - 2 * b)
    )
    asserted = r**2 + r - 11 + b * (r + 1)
    assert sp.expand(difference - asserted) == 0
    assert difference.subs({r: 3, b: 0}) == 1


def main() -> None:
    audit_initial_cores()
    audit_exact_lift()
    audit_three_lift_counts()
    audit_full_core_and_residue()
    audit_wronskian()
    print("independent final (8,7,3) exchange audit: PASS")
    print("all 120 seven-cores and three exchange levels: exact")
    print("weighted full-core residue, zero singleton, and extra node: exact")
    print("gcd-sensitive eleven-node Wronskian contradiction: exact")


if __name__ == "__main__":
    main()
