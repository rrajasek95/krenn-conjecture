#!/usr/bin/env python3
"""Exact audit of the h=8,k=4 profile 2^9 1^4 rainbow closure."""

from __future__ import annotations

from itertools import combinations, product
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier
import verify_live_three_zero_eighth_split_k4_updated_census as census


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


H_SPLIT = 8
K = 4
TOTAL = 22
PROFILE = (2,) * 9 + (1,) * 4
z, w, mu = sp.symbols("z w mu")


def all_matchings(vertices):
    """All matchings, including nonperfect ones, without duplication."""
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    yield from all_matchings(vertices[1:])
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in all_matchings(rest):
            yield (frozenset((first, second)),) + tail


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            yield (frozenset((first, second)),) + tail


def check_pair_drop_cores_and_lifts() -> None:
    require(
        sum(PROFILE) == TOTAL == 2 * H_SPLIT + K + 2,
        "sum(PROFILE) == TOTAL == 2 * H_SPLIT + K + 2",
    )
    double_indices = tuple(range(9))
    singleton_indices = tuple(range(9, 13))
    core_count = 0

    for selected_doubles in combinations(double_indices, 3):
        formal_roles = {
            **{index: 2 for index in selected_doubles},
            **{index: 1 for index in singleton_indices},
        }
        require(
            len(formal_roles) == 7,
            "len(formal_roles) == 7",
        )
        require(
            sum(formal_roles.values()) == 10,
            "sum(formal_roles.values()) == 10",
        )

        for lowered_pair in combinations(formal_roles, 2):
            takes = {
                index: role - (1 if index in lowered_pair else 0)
                for index, role in formal_roles.items()
            }
            takes = {index: role for index, role in takes.items() if role}
            complement = [
                multiplicity - takes.get(index, 0)
                for index, multiplicity in enumerate(PROFILE)
            ]
            omitted_singletons = sum(
                index in singleton_indices for index in lowered_pair
            )
            represented = len(takes)
            residual_degree = represented - 3
            lift_degree = sum(
                3 if index in singleton_indices else 2
                for index in lowered_pair
            )

            require(
                sum(takes.values()) == H_SPLIT,
                "sum(takes.values()) == H_SPLIT",
            )
            require(
                sum(complement) == 14,
                "sum(complement) == 14",
            )
            require(
                complement.count(1) == 2,
                "complement.count(1) == 2",
            )
            require(
                frontier.leaves_singleton(PROFILE, takes),
                "frontier.leaves_singleton(PROFILE, takes)",
            )
            require(
                represented == 7 - omitted_singletons,
                "represented == 7 - omitted_singletons",
            )
            require(
                residual_degree == 4 - omitted_singletons,
                "residual_degree == 4 - omitted_singletons",
            )
            require(
                lift_degree == 4 + omitted_singletons,
                "lift_degree == 4 + omitted_singletons",
            )
            require(
                residual_degree + lift_degree == 8,
                "residual_degree + lift_degree == 8",
            )
            core_count += 1

    require(
        core_count == sp.binomial(9, 3) * sp.binomial(7, 2) == 1764,
        "core_count == sp.binomial(9, 3) * sp.binomial(7, 2) == 1764",
    )

    x, r = sp.symbols("x r")
    double_lift = z**2 - x**2
    singleton_lift = (z - r) * (z + r) ** 2
    require(
        sp.factor(
            (z - x) / (z + x) ** 2 - double_lift / (z + x) ** 3
        ) == 0,
        "sp.factor( (z - x) / (z + x) ** 2 - double_lift / (z + x)...",
    )
    require(
        sp.factor((z - r) - singleton_lift / (z + r) ** 2) == 0,
        "sp.factor((z - r) - singleton_lift / (z + r) ** 2) == 0",
    )
    require(
        3 * 2 + 4 * 3 == 18 > 8,
        "3 * 2 + 4 * 3 == 18 > 8",
    )
    require(
        12 + 8 == 20,
        "12 + 8 == 20",
    )
    require(
        5 + 3 * 3 + 4 * 2 == 22,
        "5 + 3 * 3 + 4 * 2 == 22",
    )
    require(
        22 - 20 == 2,
        "22 - 20 == 2",
    )


def check_kernel_bound_and_parity_boundary() -> None:
    # Three exact order-two rows and four exact order-one rows on P_8.
    for dimension in range(5, 10):
        baseline = 3 * (dimension - 2) + 4 * (dimension - 1)
        cap = dimension * (9 - dimension)
        deficit = baseline - cap
        require(
            deficit == dimension**2 - 2 * dimension - 10,
            "deficit == dimension**2 - 2 * dimension - 10",
        )
        require(
            deficit > 0,
            "deficit > 0",
        )

        for simple_double_gcd in range(4):
            for absorbed_doubles in range(4 - simple_double_gcd):
                ordinary_doubles = (
                    3 - simple_double_gcd - absorbed_doubles
                )
                for absorbed_singletons in range(5):
                    gcd_degree = (
                        simple_double_gcd
                        + 3 * absorbed_doubles
                        + 2 * absorbed_singletons
                    )
                    forced_weight = (
                        ordinary_doubles * (dimension - 2)
                        + simple_double_gcd * (dimension - 1)
                        + (4 - absorbed_singletons) * (dimension - 1)
                    )
                    reduced_cap = dimension * (
                        9 - gcd_degree - dimension
                    )
                    observed = forced_weight - reduced_cap
                    expected = (
                        deficit
                        + (dimension + 1) * simple_double_gcd
                        + (2 * dimension + 2) * absorbed_doubles
                        + (dimension + 1) * absorbed_singletons
                    )
                    require(
                        observed == expected,
                        "observed == expected",
                    )
                    require(
                        observed > 0,
                        "observed > 0",
                    )

    p_coefficients = sp.symbols("p0:9")
    q_coefficients = sp.symbols("q0:9")
    p = sum(p_coefficients[index] * z**index for index in range(9))
    q = sum(q_coefficients[index] * z**index for index in range(9))
    parity_minor = sp.expand(p * q.subs(z, -z) - p.subs(z, -z) * q)
    require(
        sp.expand(parity_minor.subs(z, -z) + parity_minor) == 0,
        "sp.expand(parity_minor.subs(z, -z) + parity_minor) == 0",
    )
    require(
        sp.Poly(parity_minor, z).degree() <= 15,
        "sp.Poly(parity_minor, z).degree() <= 15",
    )

    layer_values = sp.symbols("v0:7")
    ordinary_divisor = z * sp.prod(
        z**2 - value**2 for value in layer_values
    )
    zero_divisor = z**3 * sp.prod(
        z**2 - value**2 for value in layer_values[:6]
    )
    require(
        sp.Poly(ordinary_divisor, z).degree() == 15,
        "sp.Poly(ordinary_divisor, z).degree() == 15",
    )
    require(
        sp.Poly(zero_divisor, z).degree() == 15,
        "sp.Poly(zero_divisor, z).degree() == 15",
    )

    # At a zero singleton, a basis adapted to U_0 has two members
    # divisible by z^3, so every parity minor has order at least three.
    a_coefficients = sp.symbols("a0:9")
    b_coefficients = sp.symbols("b0:6")
    c_coefficients = sp.symbols("c0:6")
    p0 = sum(a_coefficients[index] * z**index for index in range(9))
    p1 = z**3 * sum(b_coefficients[index] * z**index for index in range(6))
    p2 = z**3 * sum(c_coefficients[index] * z**index for index in range(6))
    for left, right in ((p0, p1), (p0, p2), (p1, p2)):
        minor = sp.Poly(
            sp.expand(left * right.subs(z, -z) - left.subs(z, -z) * right),
            z,
        )
        require(
            all(
                minor.coeff_monomial(z**degree) == 0
                for degree in range(3)
            ),
            "all( minor.coeff_monomial(z**degree) == 0 for degree in r...",
        )

    # A simple gcd zero at an exact order-one row would force the
    # primitive space to have another common zero.
    b0, g0, e0 = sp.symbols("b0 g0 e0", nonzero=True)
    local_product = b0 * (w * g0) * e0
    require(
        sp.diff(local_product, w).subs(w, 0) == b0 * g0 * e0,
        "sp.diff(local_product, w).subs(w, 0) == b0 * g0 * e0",
    )

    local_sections = (sp.Integer(1), w**2, w**3)
    local_wronskian = sp.det(
        sp.Matrix(
            [
                [
                    sp.diff(section, w, derivative)
                    for section in local_sections
                ]
                for derivative in range(3)
            ]
        )
    )
    require(
        sp.factor(local_wronskian) == 6 * w**2,
        "sp.factor(local_wronskian) == 6 * w**2",
    )

    table = {
        0: (8, 6),
        1: (6, 3),
        2: (4, 0),
    }
    for absorbed_singletons, (forced, cap) in table.items():
        square_degree = (8 - 2 * absorbed_singletons) // 2
        require(
            forced == 2 * (4 - absorbed_singletons),
            "forced == 2 * (4 - absorbed_singletons)",
        )
        require(
            cap == 3 * (square_degree - 2),
            "cap == 3 * (square_degree - 2)",
        )
        require(
            forced > cap,
            "forced > cap",
        )
    require(
        (8 - 2 * 3) // 2 == 1,
        "(8 - 2 * 3) // 2 == 1",
    )


def check_relation_plane_and_outside_rows() -> None:
    selected = sp.symbols("t0:3")
    outside = sp.symbols("u0:6")
    singletons = sp.symbols("r0:4")
    Q = sp.prod(z + value for value in selected)
    C = sp.prod(z - value for value in outside)
    H = sp.prod(z + value for value in singletons)
    A = C**2
    g_A = C
    radical = sp.cancel(A / g_A)
    D_A = sp.cancel(sp.diff(A, z) / g_A)

    require(
        sp.Poly(A, z).degree() == 12,
        "sp.Poly(A, z).degree() == 12",
    )
    require(
        sp.Poly(g_A, z).degree() == 6,
        "sp.Poly(g_A, z).degree() == 6",
    )
    require(
        sp.Poly(radical, z).degree() == 6,
        "sp.Poly(radical, z).degree() == 6",
    )
    require(
        sp.Poly(D_A, z).degree() == 5,
        "sp.Poly(D_A, z).degree() == 5",
    )
    require(
        sp.Poly(D_A, z).LC() == 12,
        "sp.Poly(D_A, z).LC() == 12",
    )

    coefficients = sp.symbols("n0:8")
    N = sum(coefficients[index] * z**index for index in range(8))
    differential = sp.expand(
        radical * ((z + mu) * sp.diff(N, z) + 5 * N)
        - (z + mu) * D_A * N
    )
    G = (z + mu) ** 5 * N / A
    require(
        sp.cancel(
            sp.diff(G, z)
            - (z + mu) ** 4 * g_A * differential / A**2
        ) == 0,
        "sp.cancel( sp.diff(G, z) - (z + mu) ** 4 * g_A * differen...",
    )
    require(
        sp.Poly(differential, z).degree() <= 12,
        "sp.Poly(differential, z).degree() <= 12",
    )

    for degree in range(8):
        trial = z**degree
        trial_differential = sp.Poly(
            sp.expand(
                radical
                * ((z + mu) * sp.diff(trial, z) + 5 * trial)
                - (z + mu) * D_A * trial
            ),
            z,
        )
        if degree < 7:
            require(
                trial_differential.degree() == degree + 6,
                "trial_differential.degree() == degree + 6",
            )
            require(
                trial_differential.coeff_monomial(
                    z ** (degree + 6)
                ) == degree - 7,
                "trial_differential.coeff_monomial( z ** (degree + 6) ) ==...",
            )
        else:
            require(
                trial_differential.degree() <= 12,
                "trial_differential.degree() <= 12",
            )
            require(
                trial_differential.coeff_monomial(z**13) == 0,
                "trial_differential.coeff_monomial(z**13) == 0",
            )

    contact_divisor = sp.expand(Q**2 * H)
    require(
        sp.Poly(contact_divisor, z).degree() == 10,
        "sp.Poly(contact_divisor, z).degree() == 10",
    )
    require(
        7 - (9 - 4) == 2,
        "7 - (9 - 4) == 2",
    )
    require(
        17 - 10 == 7,
        "17 - 10 == 7",
    )
    require(
        12 - 10 == 2,
        "12 - 10 == 2",
    )

    # Exact normalized order-three-pole row on the quadratics.
    b0, b1, b2 = sp.symbols("B0 B1 B2", nonzero=True)
    s0, s1, s2 = sp.symbols("s0 s1 s2")
    unit = b0 + b1 * w + b2 * w**2 / 2
    section = s0 + s1 * w + s2 * w**2 / 2
    row = sp.diff(unit * section, w, 2).subs(w, 0) / b0
    expected = (
        s2 + 2 * (b1 / b0) * s1 + (b2 / b0) * s0
    )
    require(
        sp.expand(row - expected) == 0,
        "sp.expand(row - expected) == 0",
    )


def check_pair_identities_and_boolean_differences() -> None:
    p, q, U, V = sp.symbols("p q U V")
    common = q - p + 2 * p * q
    chi_u_at_v = 2 + 4 * p + U
    chi_v_at_u = 2 - 4 * q + V

    # Cross-multiplying proportional rows on the two anchored squares
    # and on (z-u)(z-v) gives exactly these division-free equations.
    first_cross = sp.expand(
        chi_u_at_v * (1 - q) - 2 * (1 + p)
    )
    second_cross = sp.expand(
        chi_v_at_u * (1 + p) - 2 * (1 - q)
    )
    require(
        sp.expand(first_cross - (U * (1 - q) - 2 * common)) == 0,
        "sp.expand(first_cross - (U * (1 - q) - 2 * common)) == 0",
    )
    require(
        sp.expand(second_cross - (V * (1 + p) - 2 * common)) == 0,
        "sp.expand(second_cross - (V * (1 + p) - 2 * common)) == 0",
    )

    anchor, value = sp.symbols("anchor value")
    phi = 2 / (anchor + value) + 3 / (anchor - value)
    psi = -2 / (anchor + value) ** 2 - 3 / (anchor - value) ** 2
    require(
        sp.factor(phi - (5 * anchor + value) / (anchor**2 - value**2)) == 0,
        "sp.factor(phi - (5 * anchor + value) / (anchor**2 - value...",
    )
    require(
        sp.diff(2 / (anchor + value), anchor) - (
            -2 / (anchor + value) ** 2
        ) == 0,
        "sp.diff(2 / (anchor + value), anchor) - ( -2 / (anchor + ...",
    )
    require(
        sp.diff(3 / (anchor - value), anchor) - (
            -3 / (anchor - value) ** 2
        ) == 0,
        "sp.diff(3 / (anchor - value), anchor) - ( -3 / (anchor - ...",
    )
    require(
        psi == (
            -2 / (anchor + value) ** 2 - 3 / (anchor - value) ** 2
        ),
        "psi == ( -2 / (anchor + value) ** 2 - 3 / (anchor - value...",
    )

    p0, q0, up0, vp0 = sp.symbols("p0 q0 up0 vp0")
    alpha = sp.symbols("alpha0:3")
    beta = sp.symbols("beta0:3")
    gamma = sp.symbols("gamma0:3")
    epsilon = sp.symbols("epsilon0:3")
    third_differences = [sp.Integer(0), sp.Integer(0)]

    for bits in product((0, 1), repeat=3):
        p_value = p0 + sum(bits[i] * alpha[i] for i in range(3))
        q_value = q0 + sum(bits[i] * beta[i] for i in range(3))
        u_value = (
            p_value**2
            + up0
            + sum(bits[i] * gamma[i] for i in range(3))
        )
        v_value = (
            q_value**2
            + vp0
            + sum(bits[i] * epsilon[i] for i in range(3))
        )
        common_value = q_value - p_value + 2 * p_value * q_value
        equations = (
            u_value * (1 - q_value) - 2 * common_value,
            v_value * (1 + p_value) - 2 * common_value,
        )
        sign = (-1) ** (3 - sum(bits))
        for index in range(2):
            third_differences[index] += sign * equations[index]

    expected_first = -2 * (
        alpha[0] * alpha[1] * beta[2]
        + alpha[0] * alpha[2] * beta[1]
        + alpha[1] * alpha[2] * beta[0]
    )
    expected_second = 2 * (
        beta[0] * beta[1] * alpha[2]
        + beta[0] * beta[2] * alpha[1]
        + beta[1] * beta[2] * alpha[0]
    )
    require(
        sp.factor(third_differences[0] - expected_first) == 0,
        "sp.factor(third_differences[0] - expected_first) == 0",
    )
    require(
        sp.factor(third_differences[1] - expected_second) == 0,
        "sp.factor(third_differences[1] - expected_second) == 0",
    )


def check_fibres_and_six_vertex_deletion() -> None:
    u, v, x, y = sp.symbols("u v x y")

    def phi(anchor, value):
        return (5 * anchor + value) / (anchor**2 - value**2)

    difference = sp.factor(phi(u, x) - phi(u, y))
    expected = (
        (x - y)
        * (x * y + 5 * u * (x + y) + u**2)
        / ((u**2 - x**2) * (u**2 - y**2))
    )
    require(
        sp.factor(difference - expected) == 0,
        "sp.factor(difference - expected) == 0",
    )

    fibre_value = sp.symbols("lambda")
    fibre_polynomial = sp.expand(
        fibre_value * (u**2 - x**2) - 5 * u - x
    )
    require(
        sp.Poly(fibre_polynomial, x).degree() <= 2,
        "sp.Poly(fibre_polynomial, x).degree() <= 2",
    )
    require(
        sp.Poly(fibre_polynomial, x).coeff_monomial(x) == -1,
        "sp.Poly(fibre_polynomial, x).coeff_monomial(x) == -1",
    )

    h_u = x * y + 5 * u * (x + y) + u**2
    h_v = x * y + 5 * v * (x + y) + v**2
    require(
        sp.factor(h_u - h_v) == (
            u - v
        ) * (u + v + 5 * x + 5 * y),
        "sp.factor(h_u - h_v) == ( u - v ) * (u + v + 5 * x + 5 * y)",
    )
    fixed_sum = -(u + v) / 5
    require(
        sp.expand(h_u.subs(x + y, fixed_sum)) == x * y - u * v,
        "sp.expand(h_u.subs(x + y, fixed_sum)) == x * y - u * v",
    )

    # Abstract audit of the deletion lemma for every two matchings on
    # seven vertices whose common-edge set has size at most one.
    vertices = tuple(range(7))
    matchings = tuple(all_matchings(vertices))
    require(
        len(matchings) == 232,
        "len(matchings) == 232",
    )

    def restricted_is_perfect(matching, deleted):
        remaining = set(vertices) - {deleted}
        restricted = {
            edge for edge in matching if deleted not in edge
        }
        covered = set().union(*(set(edge) for edge in restricted))
        return len(restricted) == 3 and covered == remaining

    for matching_u in matchings:
        set_u = set(matching_u)
        for matching_v in matchings:
            set_v = set(matching_v)
            if len(set_u & set_v) > 1:
                continue
            require(
                any(
                    not restricted_is_perfect(matching_u, deleted)
                    and not restricted_is_perfect(matching_v, deleted)
                    and all(
                        deleted in edge for edge in set_u & set_v
                    )
                    for deleted in vertices
                ),
                "any( not restricted_is_perfect(matching_u, deleted) and n...",
            )


def check_rainbow_obstruction() -> None:
    vertices = tuple(range(6))
    edges = tuple(
        frozenset(edge) for edge in combinations(vertices, 2)
    )
    perfect = tuple(
        frozenset(matching) for matching in perfect_matchings(vertices)
    )
    require(
        len(edges) == 15,
        "len(edges) == 15",
    )
    require(
        len(perfect) == 15,
        "len(perfect) == 15",
    )
    require(
        all(len(matching) == 3 for matching in perfect),
        "all(len(matching) == 3 for matching in perfect)",
    )
    require(
        all(
            sum(edge in matching for matching in perfect) == 3
            for edge in edges
        ),
        "all( sum(edge in matching for matching in perfect) == 3 f...",
    )

    # The disjointness graph KG(6,2) is connected, so equality of cubes
    # inside every perfect matching propagates to all edge ratios.
    seen = {edges[0]}
    frontier_edges = [edges[0]]
    while frontier_edges:
        edge = frontier_edges.pop()
        for candidate in edges:
            if edge.isdisjoint(candidate) and candidate not in seen:
                seen.add(candidate)
                frontier_edges.append(candidate)
    require(
        seen == set(edges),
        "seen == set(edges)",
    )

    stars = {
        frozenset(edge for edge in edges if vertex in edge)
        for vertex in vertices
    }
    exact_transversals = {
        frozenset(family)
        for family in combinations(edges, 5)
        if all(len(set(family) & set(matching)) == 1 for matching in perfect)
    }
    require(
        exact_transversals == stars,
        "exact_transversals == stars",
    )
    require(
        all(len(star) == 5 for star in stars),
        "all(len(star) == 5 for star in stars)",
    )
    require(
        all(
            left & right
            for left, right in combinations(stars, 2)
        ),
        "all( left & right for left, right in combinations(stars, ...",
    )

    # Algebra behind the three cube-root colors.
    r0, r1, r2, t = sp.symbols("r0 r1 r2 t")
    cubic = sp.expand((t - r0) * (t - r1) * (t - r2))
    e1 = r0 + r1 + r2
    e2 = r0 * r1 + r0 * r2 + r1 * r2
    e3 = r0 * r1 * r2
    require(
        sp.expand(
            cubic - (t**3 - e1 * t**2 + e2 * t - e3)
        ) == 0,
        "sp.expand( cubic - (t**3 - e1 * t**2 + e2 * t - e3) ) == 0",
    )


def check_profile_location() -> None:
    counts, residuals = frontier.census(8, 12)
    require(
        counts["R"] == 46,
        "counts[\"R\"] == 46",
    )
    require(
        PROFILE in residuals,
        "PROFILE in residuals",
    )
    expected_increment = {PROFILE}
    require(
        census.EXPECTED_NINE_DOUBLE_FOUR_SINGLETON_RAINBOW
            == expected_increment,
        "census.EXPECTED_NINE_DOUBLE_FOUR_SINGLETON_RAINBOW == exp...",
    )
    require(
        census.EXPECTED_RESIDUALS == (),
        "census.EXPECTED_RESIDUALS == ()",
    )


def main() -> None:
    check_pair_drop_cores_and_lifts()
    check_kernel_bound_and_parity_boundary()
    check_relation_plane_and_outside_rows()
    check_pair_identities_and_boolean_differences()
    check_fibres_and_six_vertex_deletion()
    check_rainbow_obstruction()
    check_profile_location()
    print("PASS: h=8,k=4 profile 2^9 1^4 rainbow closure")
    print("1764 legal pair-drop cores give the exact P_8 kernel")
    print("seven rows have a relation plane in P_2")
    print("fixed-pair third differences force cube-root edge colors")
    print("K6 has no three-star rainbow partition")


if __name__ == "__main__":
    main()
