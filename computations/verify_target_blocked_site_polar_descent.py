#!/usr/bin/env python3
"""Exact lightweight audits for the blocked-site polar descent."""

from itertools import combinations, product
from random import Random


SITES = tuple(range(6))
COLORS = tuple(range(3))
FIELD = 5


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


MATCHINGS = tuple(perfect_matchings(SITES))


def dot(left, right, modulus=FIELD):
    return sum(a * b for a, b in zip(left, right)) % modulus


def rank_mod(rows, modulus=FIELD):
    matrix = [[entry % modulus for entry in row] for row in rows]
    if not matrix:
        return 0
    rank = 0
    columns = len(matrix[0])
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(rank, len(matrix))
                if matrix[row][column] % modulus
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column] % modulus, -1, modulus)
        matrix[rank] = [inverse * value % modulus for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank:
                continue
            multiple = matrix[row][column] % modulus
            if multiple:
                matrix[row] = [
                    (left - multiple * right) % modulus
                    for left, right in zip(matrix[row], matrix[rank])
                ]
        rank += 1
    return rank


def edge(x, y):
    return (x, y) if x < y else (y, x)


def first_dark(left, right):
    for probe in product(range(FIELD), repeat=3):
        if any(probe) and dot(probe, left) == dot(probe, right) == 0:
            return probe
    raise RuntimeError("two vectors in dimension three lost an annihilator")


def q_eval(q, x, y, probe_x, probe_y):
    x0, y0 = edge(x, y)
    matrix = q[(x0, y0)]
    if x > y:
        probe_x, probe_y = probe_y, probe_x
    return sum(
        probe_x[a] * matrix[a][b] * probe_y[b]
        for a in COLORS
        for b in COLORS
    ) % FIELD


def beta_eval(left, right, x, y, probe_x, probe_y):
    return (
        dot(probe_x, left[x]) * dot(probe_y, right[y])
        + dot(probe_x, right[x]) * dot(probe_y, left[y])
    ) % FIELD


def tangent_eval(left, right, q, probes):
    total = 0
    for matching in MATCHINGS:
        for distinguished in range(3):
            term = 1
            for index, (x, y) in enumerate(matching):
                if index == distinguished:
                    term *= beta_eval(
                        left, right, x, y, probes[x], probes[y]
                    )
                else:
                    term *= q_eval(q, x, y, probes[x], probes[y])
            total += term
    return total % FIELD


def hafnian_four(q, vertices, probes):
    return sum(
        q_eval(q, x, y, probes[x], probes[y])
        * q_eval(q, z, w, probes[z], probes[w])
        for (x, y), (z, w) in perfect_matchings(vertices)
    ) % FIELD


def audit_two_site_cut():
    """Numeric exact audit of the universal quotient coefficient identity."""
    rng = Random(20260730)
    checks = 0
    for _ in range(160):
        left = [
            tuple(rng.randrange(FIELD) for _ in COLORS) for _ in SITES
        ]
        right = [
            tuple(rng.randrange(FIELD) for _ in COLORS) for _ in SITES
        ]
        q = {
            (x, y): tuple(
                tuple(rng.randrange(FIELD) for _ in COLORS)
                for _ in COLORS
            )
            for x, y in combinations(SITES, 2)
        }
        x, y = rng.sample(SITES, 2)
        target = rng.randrange(3)
        unit = tuple(int(color == target) for color in COLORS)
        probes = {x: unit, y: unit}
        rest = tuple(site for site in SITES if site not in (x, y))
        for site in rest:
            probes[site] = first_dark(left[site], right[site])
        actual = tangent_eval(left, right, q, probes)
        expected = (
            beta_eval(left, right, x, y, unit, unit)
            * hafnian_four(q, rest, probes)
        ) % FIELD
        check(actual == expected, "two-site dark quotient identity failed")
        checks += 1
    return checks


def audit_companion_proportionality():
    """Exhaust the scalar components of t|_(v-perp)=0 iff t is in Cv."""
    modulus = 3
    vectors = tuple(product(range(modulus), repeat=3))
    checks = 0
    for v in vectors:
        annihilator = tuple(u for u in vectors if dot(u, v, modulus) == 0)
        for t in vectors:
            hypothesis = all(dot(u, t, modulus) == 0 for u in annihilator)
            proportional = (
                not any(t)
                if not any(v)
                else rank_mod((v, t), modulus) <= 1
            )
            check(
                hypothesis == proportional,
                "companion quotient proportionality failed",
            )
            checks += 1
    return checks


def audit_local_blocking_geometry():
    vectors = tuple(product(range(3), repeat=2))
    axis_a = (1, 0)
    axis_b = (0, 1)
    checks = 0
    for left in vectors:
        for right in vectors:
            rank = rank_mod((left, right), 3)
            blocked_a = rank_mod((left, right, axis_a), 3) == rank
            blocked_b = rank_mod((left, right, axis_b), 3) == rank
            if blocked_a and blocked_b:
                check(rank == 2, "two blocked axes did not fill the plane")
            elif blocked_a:
                check(
                    rank == 1 and left[1] == right[1] == 0,
                    "sole a-blocking was not the a-coordinate line",
                )
            elif blocked_b:
                check(
                    rank == 1 and left[0] == right[0] == 0,
                    "sole b-blocking was not the b-coordinate line",
                )
            checks += 1

    subsets = tuple(
        frozenset(site for site in SITES if mask & (1 << site))
        for mask in range(1 << len(SITES))
    )
    for blocked_a in subsets:
        for blocked_b in subsets:
            if (
                len(blocked_a) >= 3
                and len(blocked_b) >= 3
                and not blocked_a & blocked_b
            ):
                check(
                    len(blocked_a) == len(blocked_b) == 3
                    and blocked_a | blocked_b == frozenset(SITES),
                    "disjoint blocking sets were not complementary triples",
                )
                checks += 1
    return checks


# The exact guard from the rank-drop audit.
GUARD_L = {(0, 0): 1, (2, 0): 1, (4, 0): 1}
GUARD_S = {(1, 0): 1, (2, 1): 1, (4, 1): 1}
GUARD_Q = {(2, 3, 0, 0): 1, (4, 5, 0, 0): 1}


def form_unit(site, color):
    return {(site, color): 1}


def q_coefficient(table, x, y, color_x, color_y):
    if x > y:
        x, y = y, x
        color_x, color_y = color_y, color_x
    return table.get((x, y, color_x, color_y), 0)


def cap_coefficient(left, right, x, y, color_x, color_y):
    return (
        left.get((x, color_x), 0) * right.get((y, color_y), 0)
        + right.get((x, color_x), 0) * left.get((y, color_y), 0)
    )


def q_three_coefficient(word):
    return sum(
        product_value(
            q_coefficient(GUARD_Q, x, y, word[x], word[y])
            for x, y in matching
        )
        for matching in MATCHINGS
    )


def product_value(values):
    result = 1
    for value in values:
        result *= value
    return result


def response_coefficient(left, right, word):
    total = 0
    for matching in MATCHINGS:
        for distinguished in range(3):
            term = 1
            for index, (x, y) in enumerate(matching):
                if index == distinguished:
                    term *= cap_coefficient(
                        left, right, x, y, word[x], word[y]
                    )
                else:
                    term *= q_coefficient(
                        GUARD_Q, x, y, word[x], word[y]
                    )
            total += term
    return total


def row_support(left, right, direct):
    support = {}
    for word in product(COLORS, repeat=6):
        value = response_coefficient(left, right, word)
        value += direct * q_three_coefficient(word)
        if value:
            support[word] = value
    return support


def local_guard_vectors(site):
    return (
        tuple(GUARD_L.get((site, color), 0) for color in COLORS),
        tuple(GUARD_S.get((site, color), 0) for color in COLORS),
    )


def audit_guard():
    p_rows = (GUARD_L, form_unit(3, 1), form_unit(5, 2))
    s_rows = (GUARD_S, form_unit(3, 1), form_unit(5, 2))
    direct = ((0, 0, 0), (0, 1, 0), (0, 0, 0))
    failed = []
    passed = []
    for i in COLORS:
        for j in COLORS:
            support = row_support(p_rows[i], s_rows[j], direct[i][j])
            target = (
                {tuple(i for _ in SITES): 1} if i == j else {}
            )
            (passed if support == target else failed).append((i, j))
    check(
        passed == [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 2),
            (2, 0),
            (2, 1),
        ],
        "guard did not retain the selected and six off-diagonal rows",
    )
    check(failed == [(1, 1), (2, 2)], "guard failure ledger changed")

    target_axis = (1, 0, 0)
    blocked = {
        site
        for site in SITES
        if rank_mod((*local_guard_vectors(site), target_axis))
        == rank_mod(local_guard_vectors(site))
    }
    check(blocked == {0, 1, 2, 4}, "complete guard blocking set changed")
    check(
        all(not blocked <= set(pair) for pair in combinations(SITES, 2)),
        "a pair unexpectedly covered the four-blocked guard",
    )

    # At x=2 the endpoint term is zero and the q-incidence term is X_0.
    incidence = {}
    for (site_l, color_l), value_l in GUARD_L.items():
        if site_l == 2:
            continue
        for (site_s, color_s), value_s in GUARD_S.items():
            if site_s == 2:
                continue
            # Contract q_23 at its site-2 colour zero.
            z_site, z_color, z_value = 3, 0, 1
            # q_45 is the off-x quadratic.
            q_sites = ((4, 0), (5, 0))
            atoms = (
                (site_l, color_l),
                (site_s, color_s),
                (z_site, z_color),
                *q_sites,
            )
            if len({site for site, _ in atoms}) < 5:
                continue
            word = tuple(color for _, color in sorted(atoms))
            incidence[word] = incidence.get(word, 0) + (
                value_l * value_s * z_value
            )
    check(incidence == {(0, 0, 0, 0, 0): 1}, "guard incidence changed")
    return len(passed), len(failed)


def audit_toric_tautology():
    rng = Random(304)
    checks = 0
    nonzero = tuple(range(1, FIELD))
    for _ in range(160):
        xi_a, xi_b, eta_a, eta_b, v_a = (
            rng.choice(nonzero) for _ in range(5)
        )
        v_b = -xi_a * v_a * pow(xi_b, -1, FIELD) % FIELD
        companion = (
            eta_a * v_b * pow(eta_b * v_a % FIELD, -1, FIELD)
        ) % FIELD
        target_ratio = (
            -xi_a * eta_a * pow(xi_b * eta_b % FIELD, -1, FIELD)
        ) % FIELD
        check(companion == target_ratio, "toric ratio was not isotropy")
        checks += 1
    return checks


def main():
    cut_checks = audit_two_site_cut()
    companion_checks = audit_companion_proportionality()
    geometry_checks = audit_local_blocking_geometry()
    passed, failed = audit_guard()
    toric_checks = audit_toric_tautology()
    print(f"two-site physical coefficient cuts: PASS ({cut_checks})")
    print(f"full-nine companion proportionality: PASS ({companion_checks})")
    print(f"blocking-set geometry: PASS ({geometry_checks})")
    print(f"dense toric/isotropy comparisons: PASS ({toric_checks})")
    print(
        "guard ledger: PASS "
        f"({passed} rows hold, {failed} missing diagonal rows)"
    )


if __name__ == "__main__":
    main()
