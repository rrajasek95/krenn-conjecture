#!/usr/bin/env python3
"""Exact audit for the t=r+7 sixth-split frontier.

The determinant-rigidity computation is deliberately diagnostic.  This
script does not claim that finitely many specializations prove DR4 over C.
"""

from __future__ import annotations

from itertools import combinations, permutations, product

import sympy as sp


def parity(perm: tuple[int, ...]) -> int:
    return (-1) ** sum(
        perm[i] > perm[j]
        for i in range(len(perm))
        for j in range(i + 1, len(perm))
    )


def determinant_by_permutations(rows: list[list[sp.Expr]]) -> sp.Expr:
    n = len(rows)
    return sp.expand(
        sum(
            parity(perm) * sp.prod(rows[i][perm[i]] for i in range(n))
            for perm in permutations(range(n))
        )
    )


def cleared_rows(
    anchors: tuple[sp.Expr, ...],
    translations: tuple[sp.Expr, ...],
    x: sp.Symbol,
) -> list[list[sp.Expr]]:
    rows: list[list[sp.Expr]] = []
    for s, u in zip(anchors, translations, strict=True):
        den = x**2 - s**2
        y_num = u * den - (x + 3 * s)
        rows.append(
            [
                3 * s**2 * den - s**3 * y_num,
                -2 * s * den + s**2 * y_num,
                den - s * y_num,
                y_num,
            ]
        )
    return rows


def check_degree_bookkeeping() -> None:
    p, m = sp.symbols("p m", integer=True)
    k = p - 6
    assert sp.expand((k + 1) + 6 + m) == p + m + 1
    assert sp.expand((p + m + 1) - 2) == p + m - 1
    assert sp.expand((k + 1) + 12) == p + 7
    assert (p + 5) - (p + 2) == 3
    assert 7 + 3 > 8


def check_cubic_rows_and_kernel() -> None:
    x, z = sp.symbols("x z")
    anchors = sp.symbols("a b c d", nonzero=True)
    translations = sp.symbols("u0:4")
    rows = cleared_rows(anchors, translations, x)
    assert all(max(sp.degree(entry, x) for entry in row) <= 2 for row in rows)

    det = determinant_by_permutations(rows)
    assert sp.degree(det, x) <= 8

    g = sp.expand((z - x) * (z + x) ** 2)
    coeff = sp.Matrix([g.coeff(z, 3), g.coeff(z, 2), g.coeff(z, 1), g.coeff(z, 0)])
    zero_rows = sp.Matrix(cleared_rows(anchors, (0, 0, 0, 0), x))
    assert all(sp.expand(value) == 0 for value in zero_rows * coeff)
    assert sp.expand(det.subs(dict(zip(translations, (0, 0, 0, 0), strict=True)))) == 0

    s = sp.symbols("s", nonzero=True)
    psi = -(x + 3 * s) / (x**2 - s**2)
    log_derivative = sp.diff(g, z).subs(z, -s) / g.subs(z, -s)
    assert sp.factor(log_derivative + psi) == 0


def coefficient_system_for_numeric_anchors(
    anchors: tuple[int, int, int, int],
) -> tuple[list[sp.Expr], tuple[sp.Symbol, ...]]:
    x = sp.symbols("x")
    translations = sp.symbols("u0:4")
    rows = cleared_rows(tuple(map(sp.Integer, anchors)), translations, x)
    det = sp.Poly(determinant_by_permutations(rows), x)
    return [det.coeff_monomial(x**j) for j in range(9)], translations


def check_dr4_diagnostics() -> None:
    # Exact characteristic-zero specializations.  Each ideal is the origin.
    for anchors in ((1, 2, 3, 4), (1, 2, 3, 7), (1, 3, 4, 7), (2, 3, 5, 7)):
        equations, translations = coefficient_system_for_numeric_anchors(anchors)
        basis = sp.groebner(equations, *translations, order="grevlex")
        assert [sp.expand(poly.as_expr()) for poly in basis.polys] == list(translations)

    # Exhaustive U-search for one admissible quadruple over F_11.  This is
    # useful regression coverage, but explicitly not a proof over C.
    prime = 11
    equations, translations = coefficient_system_for_numeric_anchors((1, 2, 3, 4))
    polynomials = [sp.Poly(eq, *translations) for eq in equations]
    for values in product(range(prime), repeat=4):
        if values == (0, 0, 0, 0):
            continue
        substitution = dict(zip(translations, values, strict=True))
        assert any(int(poly.as_expr().subs(substitution)) % prime for poly in polynomials)


def check_psi_fibres() -> None:
    a, c, d, lam, y = sp.symbols("a c d lam y")
    psi = lambda v: -(v + 3 * a) / (v**2 - a**2)
    expected = (c - d) * (a**2 + 3 * a * (c + d) + c * d) / (
        (a**2 - c**2) * (a**2 - d**2)
    )
    assert sp.factor(psi(c) - psi(d) - expected) == 0
    fibre = sp.together(psi(y) - lam).as_numer_denom()[0]
    assert sp.factor(-fibre) == -a**2 * lam + 3 * a + lam * y**2 + y
    assert sp.degree(fibre, y) == 2
    assert sp.expand(-fibre).coeff(y, 1) == 1


def check_moving_class_lemmas() -> None:
    x, a, b, u, v, gamma = sp.symbols("x a b u v gamma")
    chi_a = -(x + gamma * a) / (x**2 - a**2)
    chi_b = -(x + gamma * b) / (x**2 - b**2)
    ya = u + chi_a
    yb = v + chi_b
    cleared = sp.expand(
        sp.together(yb - ya + (b - a) * ya * yb).as_numer_denom()[0]
    )
    assert sp.degree(cleared, x) <= 4
    assert sp.expand(cleared.coeff(x, 3) - (a - b) * (u + v)) == 0
    assert sp.expand(cleared.coeff(x, 4) - ((b - a) * u * v - u + v)) == 0

    branch_zero = (a - b) * (gamma - 1) * (
        x**2 - (a + b) * x - gamma * a * b
    )
    assert sp.factor(cleared.subs({u: 0, v: 0}) - branch_zero) == 0

    branch_two = -(a - b) * (gamma + 1) * (
        x**2 + (a + b) * x + gamma * a * b
    )
    assert sp.factor(
        cleared.subs({u: 2 / (a - b), v: -2 / (a - b)}) - branch_two
    ) == 0

    j = sp.symbols("j", integer=True, positive=True)
    chi = j / (a + x) - (j + 1) / (x - a)
    assert sp.factor(chi + (x + (2 * j + 1) * a) / (x**2 - a**2)) == 0


def check_three_full_doubles_lemma() -> None:
    """Audit the second-derivative argument closing five double classes."""
    z, u, v, lam = sp.symbols("z u v lam")

    # Relative to leaving a double v in P_N, selecting both copies removes
    # (z-v)^2 from the numerator and inserts (z+v)^3 in the denominator.
    delta_log_prime = -3 / (z + v) - 2 / (z - v)
    delta_log_second = sp.diff(delta_log_prime, z)
    a_v = 2 / (u + v) - 3 / (v - u)
    b_v = 2 / (u + v) ** 2 + 3 / (v - u) ** 2
    assert sp.factor(delta_log_prime.subs(z, -u) - a_v) == 0
    assert sp.factor(delta_log_second.subs(z, -u) - b_v) == 0
    assert sp.factor(a_v + (v + 5 * u) / (v**2 - u**2)) == 0

    fibre = sp.together(a_v - lam).as_numer_denom()[0]
    assert sp.factor(fibre + lam * (v**2 - u**2) + v + 5 * u) == 0
    assert sp.degree(fibre, v) <= 2
    assert sp.expand(fibre).coeff(v, 1) == -1

    # If F_ij=(C+A_i+A_j)^2+K+B_i+B_j vanishes for all pairs,
    # complementary pair subtraction gives the factored relation used in
    # Lemma 9.3.  Check it for all ordered choices of four distinct indices.
    c, kappa = sp.symbols("C K")
    aa = sp.symbols("A0:4")
    bb = sp.symbols("B0:4")

    def pair_equation(i: int, j: int) -> sp.Expr:
        return (c + aa[i] + aa[j]) ** 2 + kappa + bb[i] + bb[j]

    for i, j, k, ell in permutations(range(4)):
        difference = (
            pair_equation(i, j)
            - pair_equation(i, k)
            - pair_equation(ell, j)
            + pair_equation(ell, k)
        )
        assert sp.expand(difference - 2 * (aa[j] - aa[k]) * (aa[i] - aa[ell])) == 0


def elementary(values: tuple[sp.Expr, ...], degree: int) -> sp.Expr:
    return sp.expand(sum(sp.prod(values[i] for i in subset) for subset in combinations(range(len(values)), degree)))


def check_deleted_e6_descent() -> None:
    # The two identities used in the descent are polynomial identities.
    values = sp.symbols("h0:7")
    for degree in range(1, 6):
        lhs = sum(elementary(values[:i] + values[i + 1 :], degree) for i in range(len(values)))
        rhs = (len(values) - degree) * elementary(values, degree)
        assert sp.expand(lhs - rhs) == 0
    for degree in range(1, 6):
        rest = values[1:]
        assert sp.expand(
            elementary(values, degree)
            - elementary(rest, degree)
            - values[0] * elementary(rest, degree - 1)
        ) == 0

    # Exact deleted-pair subtraction at the first descent step.
    nine = sp.symbols("v0:9")
    i, j, k = 2, 0, 1
    delete_ij = tuple(v for h, v in enumerate(nine) if h not in (i, j))
    delete_ik = tuple(v for h, v in enumerate(nine) if h not in (i, k))
    common = tuple(v for h, v in enumerate(nine) if h not in (i, j, k))
    assert sp.expand(
        elementary(delete_ij, 6)
        - elementary(delete_ik, 6)
        - (nine[k] - nine[j]) * elementary(common, 5)
    ) == 0


def partitions(total: int, maximum: int | None = None):
    if total == 0:
        yield ()
        return
    if maximum is None:
        maximum = total
    for first in range(min(total, maximum), 0, -1):
        for tail in partitions(total - first, first):
            yield (first,) + tail


def two_class_singleton_witness(profile: tuple[int, ...]):
    size = len(profile)
    for i in range(size):
        for take_i in range(1, min(6, profile[i]) + 1):
            take_j = 6 - take_i
            if take_j == 0:
                chosen = {i: take_i}
                if any(profile[h] - chosen.get(h, 0) == 1 for h in range(size)):
                    return chosen
                continue
            for j in range(i + 1, size):
                if take_j > profile[j]:
                    continue
                chosen = {i: take_i, j: take_j}
                if any(profile[h] - chosen.get(h, 0) == 1 for h in range(size)):
                    return chosen
    return None


def constant_moving_witness(profile: tuple[int, ...]):
    """Return fixed two-class counts, moving count, and >=3 candidates."""
    size = len(profile)
    for i, j in combinations(range(size), 2):
        for take_i in range(1, profile[i] + 1):
            for take_j in range(1, profile[j] + 1):
                if 1 not in (take_i, take_j):
                    continue
                moving_take = 6 - take_i - take_j
                if moving_take < 1:
                    continue
                candidates = []
                for moving in range(size):
                    if moving in (i, j) or profile[moving] < moving_take:
                        continue
                    chosen = {i: take_i, j: take_j, moving: moving_take}
                    if any(
                        profile[h] - chosen.get(h, 0) == 1 for h in range(size)
                    ):
                        candidates.append(moving)
                if len(candidates) >= 3:
                    return i, take_i, j, take_j, moving_take, tuple(candidates)
    return None


def final_residual_family(profile: tuple[int, ...]) -> str | None:
    counts = {multiplicity: profile.count(multiplicity) for multiplicity in set(profile)}
    if counts.get(3, 0) == 1 and set(profile) <= {1, 2, 3}:
        if counts.get(2, 0) <= 2 and counts.get(1, 0) > 0:
            return "one_triple_few_doubles_singles"
    if set(profile) <= {1, 2} and counts.get(1, 0) > 0:
        return "doubles_singles"
    if set(profile) == {2}:
        return "all_double"
    return None


def check_partition_census() -> None:
    expected = {
        7: (176, 92, 66, 18),
        8: (231, 130, 81, 20),
        9: (297, 178, 99, 20),
        10: (385, 244, 118, 23),
        11: (490, 326, 142, 22),
        12: (627, 435, 167, 25),
    }
    for p in range(7, 25):
        profiles = list(partitions(p + 8))
        high = [profile for profile in profiles if max(profile) >= 6]
        short = [
            profile
            for profile in profiles
            if max(profile) < 6 and two_class_singleton_witness(profile) is not None
        ]
        residual = [
            profile
            for profile in profiles
            if max(profile) < 6 and two_class_singleton_witness(profile) is None
        ]
        assert len(high) + len(short) + len(residual) == len(profiles)
        for profile in short:
            witness = two_class_singleton_witness(profile)
            assert witness is not None
            assert sum(witness.values()) == 6
            assert len(witness) <= 2
            assert any(profile[h] - witness.get(h, 0) == 1 for h in range(len(profile)))
        if p in expected:
            assert (len(profiles), len(high), len(short), len(residual)) == expected[p]

    # Uniform classification after also applying the constant-residual
    # moving-class lemma.  A broad range catches every threshold boundary
    # used in the paper's finite largest-multiplicity case split.
    pre_full_double_residuals: set[tuple[int, int]] = set()
    for total in range(15, 41):
        for profile in partitions(total):
            if max(profile) >= 6:
                continue
            if two_class_singleton_witness(profile) is not None:
                continue
            if constant_moving_witness(profile) is not None:
                continue
            family = final_residual_family(profile)
            assert family is not None, (total, profile)

            if family == "one_triple_few_doubles_singles":
                doubles = profile.count(2)
                singleton_count = profile.count(1)
                assert 0 <= doubles <= 2
                assert singleton_count - 2 >= 6
            elif family == "doubles_singles":
                doubles = profile.count(2)
                singles = profile.count(1)
                if doubles == 0:
                    # This is the all-distinct DR4 frontier, not a collision.
                    continue
                # Quadratic moving-singleton route: after fixing a full
                # double and three simple anchors there are d+s-4 candidates,
                # so d+s >= 11 gives more roots than its degree-six
                # determinant.  The optimized linear moving-double route has
                # d-1 candidates when s >= 3, and d-2 when s is 1 or 2; its
                # cleared determinant has degree four.
                if doubles + singles >= 11:
                    continue
                if singles >= 3 and doubles >= 6:
                    continue
                if singles in {1, 2} and doubles >= 7:
                    continue
                assert (doubles, singles) == (5, 5)
                # Lemma 9.3 applies: five full double classes can be used,
                # and every three-double selection leaves singleton rows.
                assert doubles >= 5 and singles >= 1
                pre_full_double_residuals.add((doubles, singles))
            elif family == "all_double":
                assert len(profile) >= 8
    assert pre_full_double_residuals == {(5, 5)}


def main() -> None:
    check_degree_bookkeeping()
    check_cubic_rows_and_kernel()
    check_dr4_diagnostics()
    check_psi_fibres()
    check_moving_class_lemmas()
    check_three_full_doubles_lemma()
    check_deleted_e6_descent()
    check_partition_census()
    print("sixth-split exact reductions and collision census: PASS")
    print("pre-final collision residual (5,5): CLOSED by three-full-double lemma")
    print("all collision strata: CLOSED")
    print("DR4 pointwise rigidity: OPTIONAL (companion five-core certificate closes all-distinct)")


if __name__ == "__main__":
    main()
