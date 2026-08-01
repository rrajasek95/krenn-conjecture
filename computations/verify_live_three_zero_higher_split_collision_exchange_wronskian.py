#!/usr/bin/env python3
"""Exact audits for the higher collision value-core exchange theorem."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


def partitions(total: int, maximum: int | None = None) -> list[tuple[int, ...]]:
    """All decreasing positive integer partitions of ``total``."""
    if total == 0:
        return [()]
    if maximum is None or maximum > total:
        maximum = total
    answer: list[tuple[int, ...]] = []
    for first in range(maximum, 0, -1):
        for tail in partitions(total - first, min(first, total - first)):
            answer.append((first,) + tail)
    return answer


def has_singleton_complement(profile: tuple[int, ...], selected: set[int]) -> bool:
    return any(
        multiplicity - (1 if index in selected else 0) == 1
        for index, multiplicity in enumerate(profile)
    )


def every_h_value_core_is_legal(profile: tuple[int, ...], h: int) -> bool:
    c = len(profile)
    if c < h:
        return False
    return all(
        has_singleton_complement(profile, set(core))
        for core in combinations(range(c), h)
    )


def legality_formula(profile: tuple[int, ...], h: int) -> bool:
    c = len(profile)
    n1 = profile.count(1)
    n2 = profile.count(2)
    return c >= h and (n1 >= h + 1 or n2 >= c - h + 1)


def has_short_witness(profile: tuple[int, ...], h: int) -> bool:
    """Brute-force the exact one/two-class Hermite witness."""
    c = len(profile)
    for size in (1, 2):
        for support in combinations(range(c), size):
            vectors = [(h,)] if size == 1 else [(left, h - left) for left in range(1, h)]
            for counts in vectors:
                if any(count > profile[index] for index, count in zip(support, counts)):
                    continue
                remaining = list(profile)
                for index, count in zip(support, counts):
                    remaining[index] -= count
                if 1 in remaining:
                    return True
    return False


def check_legality_and_short_witnesses() -> None:
    """Audit the exact legality formula and literal short condition."""
    tested = 0
    for total in range(3, 19):
        for profile in partitions(total):
            for h in range(2, min(8, len(profile)) + 1):
                require(
                    every_h_value_core_is_legal(profile, h) == legality_formula(
                        profile, h
                    ),
                    "every_h_value_core_is_legal(profile, h) == legality_formu...",
                )
                tested += 1

                direct = False
                c = len(profile)
                for size in (1, 2):
                    for support in combinations(range(c), size):
                        if size == 1:
                            vectors = ((value,) for value in range(1, profile[support[0]] + 1))
                        else:
                            vectors = (
                                (left, right)
                                for left in range(1, profile[support[0]] + 1)
                                for right in range(1, profile[support[1]] + 1)
                            )
                        for vector in vectors:
                            if sum(vector) != h:
                                continue
                            remainder = list(profile)
                            for index, value in zip(support, vector):
                                remainder[index] -= value
                            if 1 in remainder:
                                direct = True
                                break
                        if direct:
                            break
                    if direct:
                        break
                require(
                    has_short_witness(profile, h) == direct,
                    "has_short_witness(profile, h) == direct",
                )
    require(
        tested > 5_000,
        "tested > 5_000",
    )


def check_split_and_hermite_degrees() -> None:
    for h in range(7, 31):
        for k in range(1, 16):
            p = h + k
            total = 2 * h + k + 2
            require(
                total == p + h + 2,
                "total == p + h + 2",
            )
            denominator_degree = (k + 1) + 2 * h
            numerator_cap = denominator_degree - 2
            complement_degree = p + 2
            require(
                denominator_degree == p + h + 1,
                "denominator_degree == p + h + 1",
            )
            require(
                numerator_cap - complement_degree == h - 3,
                "numerator_cap - complement_degree == h - 3",
            )

            for represented_classes in (1, 2):
                short_denominator = (k + 1) + h + represented_classes
                short_numerator_cap = short_denominator - 2
                require(
                    short_denominator == p + represented_classes + 1,
                    "short_denominator == p + represented_classes + 1",
                )
                require(
                    short_numerator_cap <= p + 1 < p + 2,
                    "short_numerator_cap <= p + 1 < p + 2",
                )

            for c in range(h + 1, total + 1):
                excess = total - c
                infinity_decay = (k + 1 + 2 * c) - (excess + c - 1)
                require(
                    infinity_decay == 2 * (c - h),
                    "infinity_decay == 2 * (c - h)",
                )


def elementary(values: tuple[sp.Symbol, ...], degree: int) -> sp.Expr:
    if degree == 0:
        return sp.Integer(1)
    return sum(sp.prod(choice) for choice in combinations(values, degree))


def check_large_class_descent_identities() -> None:
    x = sp.symbols("x0:8")
    for size in range(3, 9):
        variables = x[:size]
        for degree in range(1, size):
            lhs = sum(
                elementary(variables[:i] + variables[i + 1 :], degree)
                for i in range(size)
            )
            rhs = (size - degree) * elementary(variables, degree)
            require(
                sp.expand(lhs - rhs) == 0,
                "sp.expand(lhs - rhs) == 0",
            )
            for i, value in enumerate(variables):
                deleted = variables[:i] + variables[i + 1 :]
                require(
                    sp.expand(
                        elementary(variables, degree)
                        - elementary(deleted, degree)
                        - value * elementary(deleted, degree - 1)
                    ) == 0,
                    "sp.expand( elementary(variables, degree) - elementary(del...",
                )


def check_cubic_exchange_and_zero_anchor() -> None:
    z, a, b = sp.symbols("z a b")
    g = (z - b) * (z + b) ** 2
    psi = 1 / (a + b) - 2 / (b - a)
    require(
        sp.factor(sp.diff(g, z).subs(z, -a) / g.subs(z, -a) + psi) == 0,
        "sp.factor(sp.diff(g, z).subs(z, -a) / g.subs(z, -a) + psi...",
    )
    require(
        sp.expand(g.subs(z, -b)) == 0,
        "sp.expand(g.subs(z, -b)) == 0",
    )
    require(
        sp.expand(sp.diff(g, z).subs(z, -b)) == 0,
        "sp.expand(sp.diff(g, z).subs(z, -b)) == 0",
    )
    require(
        sp.expand(g.subs(b, 0) - z**3) == 0,
        "sp.expand(g.subs(b, 0) - z**3) == 0",
    )

    old_B, old_D, q = sp.symbols("old_B old_D q", nonzero=True)
    new_B = old_B / (z - b)
    new_D = old_D * (z + b) ** 2
    require(
        sp.factor(new_B * g * q / new_D - old_B * q / old_D) == 0,
        "sp.factor(new_B * g * q / new_D - old_B * q / old_D) == 0",
    )

    # The possible zero class is a singleton, and exchanges with it remain
    # regular: psi(0,b)=-1/b.
    require(
        sp.factor(psi.subs(a, 0) + 1 / b) == 0,
        "sp.factor(psi.subs(a, 0) + 1 / b) == 0",
    )


def check_exchange_degrees_and_three_lift_counts() -> None:
    for h in range(7, 20):
        for c in range(h + 1, h + 20):
            residual_degree = h - 3
            for old_size in range(h, c):
                require(
                    residual_degree == old_size - 3,
                    "residual_degree == old_size - 3",
                )
                lift_degree = residual_degree + 3
                require(
                    lift_degree == old_size,
                    "lift_degree == old_size",
                )
                residual_degree = lift_degree - 2
                require(
                    residual_degree == (old_size + 1) - 3,
                    "residual_degree == (old_size + 1) - 3",
                )
            require(
                c - 4 + 3 == c - 1,
                "c - 4 + 3 == c - 1",
            )

    # Sharp gcd/Riemann--Hurwitz inequalities in the three-lift lemma.
    for n in range(1, 20):
        for epsilon in (0, 1):
            e0_values = (0,) if not epsilon else (0, 2, 3, 4)
            for rho in range(n + 1):
                for sigma in range(n + 1):
                    for e0 in e0_values:
                        delta = n + epsilon - 1 - rho - 2 * sigma - e0
                        if delta < 1:
                            continue
                        cross_anchors = n - rho - sigma
                        require(
                            cross_anchors >= delta,
                            "cross_anchors >= delta",
                        )
                        require(
                            n - sigma >= delta,
                            "n - sigma >= delta",
                        )
                        require(
                            n - sigma - (delta - 1) > 0,
                            "n - sigma - (delta - 1) > 0",
                        )


def check_full_core_robin_and_local_residues() -> None:
    z = sp.symbols("z")
    nodes = sp.symbols("x0:5")
    P = sp.prod(z - node for node in nodes)
    for index, node in enumerate(nodes):
        expected = 2 * sum(
            1 / (node - other)
            for other_index, other in enumerate(nodes)
            if other_index != index
        )
        require(
            sp.factor(
                sp.diff(P, z, 2).subs(z, node) / sp.diff(P, z).subs(z, node) - expected
            ) == 0,
            "sp.factor( sp.diff(P, z, 2).subs(z, node) / sp.diff(P, z)...",
        )

    w, c2, G0, G1 = sp.symbols("w c2 G0 G1")
    require(
        sp.residue(c2 * (G0 + G1 * w) / w**2, w, 0) == c2 * G1,
        "sp.residue(c2 * (G0 + G1 * w) / w**2, w, 0) == c2 * G1",
    )

    for k in range(1, 9):
        coeffs = sp.symbols(f"a0:{k + 2}")
        regular = sum(coeffs[j] * w**j for j in range(k + 2))
        require(
            sp.residue(regular / w ** (k + 1), w, 0) == coeffs[k],
            "sp.residue(regular / w ** (k + 1), w, 0) == coeffs[k]",
        )


def check_stationary_multiplier_space() -> None:
    w = sp.symbols("w")
    for ell in range(0, 8):
        p_coeffs = sp.symbols(f"p0:{ell + 2}", nonzero=True)
        local_P = sum(p_coeffs[j] * w**j for j in range(ell + 2))
        jets = [sp.Integer(1)]
        for j in range(ell):
            jets.append(sp.integrate(sp.expand(local_P * w**j), w))
        matrix = sp.Matrix(
            [[sp.expand(jet).coeff(w, order) for jet in jets] for order in range(ell + 1)]
        )
        require(
            sp.factor(matrix.det() - p_coeffs[0] ** ell / sp.factorial(ell)) == 0,
            "sp.factor(matrix.det() - p_coeffs[0] ** ell / sp.factoria...",
        )

    for h in range(7, 30):
        for k in range(1, 15):
            total = 2 * h + k + 2
            for c in range(h + 1, total + 1):
                D = 2 * (c - h) - 2
                ell = max(0, D - c)
                require(
                    ell == max(0, c - 2 * h - 2),
                    "ell == max(0, c - 2 * h - 2)",
                )
                require(
                    ell <= k,
                    "ell <= k",
                )
                if c < total:
                    require(
                        ell <= k - 1,
                        "ell <= k - 1",
                    )
                require(
                    2 * (c - h) - D == 2,
                    "2 * (c - h) - D == 2",
                )


def check_local_jet_claim() -> None:
    """Direct matrices audit the common-pole gcd cases in (41)--(43)."""
    for k in range(1, 11):
        for ell in range(0, k + 1):
            for u in range(0, k + 1):
                n = k - u
                pairing = sp.Matrix(
                    [
                        [1 if row + column == n else 0 for column in range(n + 1)]
                        for row in range(min(ell, n) + 1)
                    ]
                )
                expected_rank = min(ell + 1, n + 1)
                require(
                    pairing.rank() == expected_rank,
                    "pairing.rank() == expected_rank",
                )
                a = n + 1 - expected_rank
                require(
                    a == max(n - ell, 0),
                    "a == max(n - ell, 0)",
                )
                if a == 0:
                    require(
                        ell >= n,
                        "ell >= n",
                    )
                    continue
                require(
                    ell < n,
                    "ell < n",
                )
                for d in range(3, 12):
                    low = list(range(min(d, a)))
                    high_count = max(d - a, 0)
                    high = list(range(n + 1, n + 1 + high_count))
                    sequence = low + high
                    weight = sum(order - index for index, order in enumerate(sequence))
                    require(
                        weight == (ell + 1) * max(d - a, 0),
                        "weight == (ell + 1) * max(d - a, 0)",
                    )


def local_weight(d: int, k: int, ell: int, u: int) -> int | None:
    """Return (43), or None for the base-point-free impossibility."""
    if u > k:
        return 0
    n = k - u
    if ell >= n:
        return None
    return (ell + 1) * max(d - n + ell, 0)


def wronskian_parameter_feasible(c: int, k: int, ell: int) -> bool:
    for d in range(3, c + 1):
        for b in range(c + 1):
            for u in range(c + 1):
                if d > c - 2 * b - u:
                    continue
                weight = local_weight(d, k, ell, u)
                if weight is None:
                    continue
                lhs = (c - b) * (d - 1) + weight
                rhs = d * (c - d - 2 * b - u)
                if lhs <= rhs:
                    return True
    return False


def omega(c: int, h: int, k: int) -> int:
    ell = max(0, c - 2 * h - 2)
    if ell < k:
        return 9 - c + (ell + 1) * max(3 - k + ell, 0)
    return 9 - c + 3 * (k + 1)


def check_wronskian_inequality_and_reduction() -> None:
    d, c, b, u, weight = sp.symbols("d c b u weight")
    lhs = (c - b) * (d - 1) + weight
    rhs = d * (c - d - 2 * b - u)
    require(
        sp.expand(
            lhs - rhs - (d**2 - c + b * (d + 1) + d * u + weight)
        ) == 0,
        "sp.expand( lhs - rhs - (d**2 - c + b * (d + 1) + d * u + ...",
    )

    for h_value in range(7, 31):
        for k_value in range(1, 16):
            total = 2 * h_value + k_value + 2
            for c_value in range(h_value + 1, total + 1):
                ell_value = max(0, c_value - 2 * h_value - 2)
                feasible = wronskian_parameter_feasible(c_value, k_value, ell_value)
                require(
                    (omega(c_value, h_value, k_value) > 0) == (not feasible),
                    "(omega(c_value, h_value, k_value) > 0) == (not feasible)",
                )

    for k_value, last_closed in [(1, 10), (2, 9), (3, 8), (8, 8)]:
        h_value = 7
        for c_value in range(8, 15):
            require(
                (omega(c_value, h_value, k_value) > 0) == (c_value <= last_closed),
                "(omega(c_value, h_value, k_value) > 0) == (c_value <= las...",
            )


def check_small_excess_vandermonde() -> None:
    z, mu = sp.symbols("z mu")
    for k_value in range(1, 9):
        for degree in range(0, 8):
            t = (z + mu) ** degree
            G = (z + mu) ** (k_value + 1) * t
            require(
                sp.expand(
                    sp.diff(G, z)
                    - (degree + k_value + 1) * (z + mu) ** (degree + k_value)
                ) == 0,
                "sp.expand( sp.diff(G, z) - (degree + k_value + 1) * (z + ...",
            )

    size = 5
    k = sp.Integer(3)
    shifted_nodes = sp.symbols(f"v0:{size}")
    matrix = sp.Matrix(
        [
            [
                (column + k + 1) * shifted_nodes[row] ** (column + k)
                for column in range(size)
            ]
            for row in range(size)
        ]
    )
    vandermonde = sp.prod(
        shifted_nodes[j] - shifted_nodes[i]
        for i in range(size)
        for j in range(i + 1, size)
    )
    expected = (
        sp.prod(column + k + 1 for column in range(size))
        * sp.prod(value**k for value in shifted_nodes)
        * vandermonde
    )
    require(
        sp.factor(matrix.det() - expected) == 0,
        "sp.factor(matrix.det() - expected) == 0",
    )

    for h in range(7, 20):
        for k_value in range(1, 10):
            total = 2 * h + k_value + 2
            for excess in (0, 1, 2):
                c = total - excess
                require(
                    excess + (c - 1) <= c + 1,
                    "excess + (c - 1) <= c + 1",
                )
                require(
                    (c - 3) + excess + (c - 1) <= 2 * c - 2,
                    "(c - 3) + excess + (c - 1) <= 2 * c - 2",
                )


def check_named_profiles() -> None:
    h, k = 7, 1
    profile_881 = (2,) * 8 + (1,)
    require(
        sum(profile_881) == 2 * h + k + 2,
        "sum(profile_881) == 2 * h + k + 2",
    )
    require(
        legality_formula(profile_881, h),
        "legality_formula(profile_881, h)",
    )
    require(
        omega(len(profile_881), h, k) > 0,
        "omega(len(profile_881), h, k) > 0",
    )

    profile_773 = (2,) * 7 + (1,) * 3
    require(
        sum(profile_773) == 2 * h + k + 2,
        "sum(profile_773) == 2 * h + k + 2",
    )
    require(
        legality_formula(profile_773, h),
        "legality_formula(profile_773, h)",
    )
    require(
        omega(len(profile_773), h, k) > 0,
        "omega(len(profile_773), h, k) > 0",
    )
    require(
        omega(11, h, k) == 0,
        "omega(11, h, k) == 0",
    )


def main() -> None:
    check_legality_and_short_witnesses()
    check_split_and_hermite_degrees()
    check_large_class_descent_identities()
    check_cubic_exchange_and_zero_anchor()
    check_exchange_degrees_and_three_lift_counts()
    check_full_core_robin_and_local_residues()
    check_stationary_multiplier_space()
    check_local_jet_claim()
    check_wronskian_inequality_and_reduction()
    check_small_excess_vandermonde()
    check_named_profiles()
    print("higher collision value-core exchange/Wronskian theorem: PASS")
    print("uniform h-core legality and short Hermite witnesses: exact")
    print("weighted common-pole jet and gcd cases: exact")
    print("small-excess residue surjectivity and Wronskian frontier: exact")


if __name__ == "__main__":
    main()
