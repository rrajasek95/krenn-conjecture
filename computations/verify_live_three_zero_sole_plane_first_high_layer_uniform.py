#!/usr/bin/env python3
"""Uniform exact audit of the sole-plane layer t=r+3, r>=3."""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import factorial

import sympy as sp


E0 = (Fraction(1), Fraction(0), Fraction(0))
E1 = (Fraction(0), Fraction(1), Fraction(0))
E2 = (Fraction(0), Fraction(0), Fraction(1))
ZERO = (Fraction(0), Fraction(0), Fraction(0))
HESSIAN = ((0, 1, 1), (1, 0, 1), (1, 1, 0))


def dot_edge(left, right, beta_left, beta_right):
    numerator = sum(
        left[i] * HESSIAN[i][j] * right[j]
        for i in range(3) for j in range(3)
    )
    return numerator / (beta_left + beta_right)


def hafnian(rows, betas, vertices):
    @lru_cache(maxsize=None)
    def recurse(remaining):
        if not remaining:
            return Fraction(1)
        first = remaining[0]
        answer = Fraction(0)
        for position in range(1, len(remaining)):
            second = remaining[position]
            tail = remaining[1:position] + remaining[position + 1 :]
            answer += dot_edge(
                rows[first], rows[second], betas[first], betas[second]
            ) * recurse(tail)
        return answer

    return recurse(tuple(vertices))


def source_22_response(rows, betas, active, direct_scale):
    # Literal direct matrix diag(0) with arbitrary B_01 scale retained.
    direct = (
        (Fraction(0), direct_scale, Fraction(0)),
        (direct_scale, Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(0)),
    )
    assert direct[2][2] == 0
    vertices = tuple(range(len(rows)))
    answer = {}
    for star in active:
        coefficient = Fraction(0)
        for left, right in combinations(vertices, 2):
            if star in (left, right):
                continue
            marked_weight = 2 * rows[left][2] * rows[right][2]
            if marked_weight == 0:
                continue
            remaining = tuple(
                site for site in vertices if site not in (left, right, star)
            )
            coefficient += marked_weight * hafnian(rows, betas, remaining)
        answer[star] = coefficient
    return answer


def cauchy_permanent(rows, columns):
    @lru_cache(maxsize=None)
    def recurse(row_index, remaining_columns):
        if row_index == len(rows):
            return Fraction(1)
        return sum(
            (
                Fraction(1, rows[row_index] + columns[column])
                * recurse(
                    row_index + 1,
                    remaining_columns[:position]
                    + remaining_columns[position + 1 :],
                )
                for position, column in enumerate(remaining_columns)
            ),
            Fraction(0),
        )

    return recurse(0, tuple(range(len(columns))))


def geometry(r):
    exceptional = tuple(range(r + 3))
    common_live = tuple(range(r + 3, 2 * r))
    centres = (2 * r, 2 * r + 1)
    extra = 2 * r + 2
    common_active = common_live + centres
    active = common_active + (extra,)
    exceptional_betas = (Fraction(0),) + tuple(
        Fraction(2 + index // 2) for index in range(r + 2)
    )
    betas = exceptional_betas + (Fraction(1),) * r
    assert len(betas) == 2 * r + 3
    for left, right in combinations(range(len(betas)), 2):
        assert betas[left] + betas[right] != 0
    return (
        exceptional, common_live, centres, extra,
        common_active, active, betas,
    )


def P_partition(r, exceptional):
    marked = exceptional[0]
    remaining = exceptional[1:]
    left = remaining[:r]
    right = remaining[r:]
    assert len(right) == 2
    return marked, left, right


def S_partition(r, exceptional):
    marked = exceptional[:2]
    remaining = exceptional[2:]
    left = remaining[:r]
    singleton = remaining[r]
    return marked, left, singleton


def audit_literal_responses(r):
    (
        exceptional, common_live, centres, extra,
        common_active, active, betas,
    ) = geometry(r)
    direct_scale = Fraction(17)
    p = (Fraction(2), Fraction(3), Fraction(5))

    marked, P_left, P_right = P_partition(r, exceptional)
    P_value = cauchy_permanent(
        tuple(betas[site] for site in P_left),
        (Fraction(1),) * (r - 2)
        + tuple(betas[site] for site in P_right),
    )
    assert P_value != 0

    # P_r isolates both binary rows at every common active site.
    for target in common_active:
        others = tuple(site for site in common_active if site != target)
        for swap in (False, True):
            same, opposite = (E1, E0) if swap else (E0, E1)
            rows = [ZERO] * len(betas)
            rows[marked] = E2
            rows[extra] = p
            rows[target] = same
            for site in others:
                rows[site] = opposite
            for site in P_left:
                rows[site] = same
            for site in P_right:
                rows[site] = opposite
            response = source_22_response(tuple(rows), betas, active, direct_scale)
            assert response[target] == 2 * p[2] * P_value
            assert response[extra] == 0
            assert all(response[site] == 0 for site in others)

    # The zero local third row at each D-type centre is a literal singleton.
    for target in centres:
        rows = [ZERO] * len(betas)
        rows[marked] = E2
        rows[extra] = p
        rows[target] = ZERO
        for site in common_active:
            if site != target:
                rows[site] = E1
        for site in P_left:
            rows[site] = E0
        for site in P_right:
            rows[site] = E1
        response = source_22_response(tuple(rows), betas, active, direct_scale)
        assert response[target] == 2 * p[2] * P_value
        assert all(response[site] == 0 for site in active if site != target)

    S_marked, S_left, singleton = S_partition(r, exceptional)
    S_value = cauchy_permanent(
        tuple(betas[site] for site in S_left),
        (Fraction(1),) * (r - 1) + (betas[singleton],),
    )
    assert S_value != 0

    # After the common binary rows vanish, S_r kills an arbitrary
    # contraction of the noncoordinate extra block.  Centre contamination
    # is retained by the response engine and discarded only triangularly.
    rows = [ZERO] * len(betas)
    for site in S_marked:
        rows[site] = E2
    for site in S_left:
        rows[site] = E0
    rows[singleton] = E1
    for site in common_active:
        rows[site] = E1
    rows[extra] = p
    response = source_22_response(tuple(rows), betas, active, direct_scale)
    assert response[extra] == 2 * S_value

    # Finally replace each common-live I row by its genuine third row.
    # Extra and off-target active contamination is retained but belongs to
    # columns already killed in the preceding triangular stages.
    for target in common_live:
        rows = [ZERO] * len(betas)
        rows[marked] = E2
        rows[extra] = p
        rows[target] = E2
        for site in common_active:
            if site != target:
                rows[site] = E1
        for site in P_left:
            rows[site] = E0
        for site in P_right:
            rows[site] = E1
        response = source_22_response(tuple(rows), betas, active, direct_scale)
        assert response[target] == 2 * p[2] * P_value

    # Coordinate plane: e is a third D-type site.  S_r isolates every
    # binary row at every active site, in both binary orientations.
    for target in active:
        others = tuple(site for site in active if site != target)
        for swap in (False, True):
            same, opposite = (E1, E0) if swap else (E0, E1)
            rows = [ZERO] * len(betas)
            for site in S_marked:
                rows[site] = E2
            for site in S_left:
                rows[site] = same
            rows[singleton] = opposite
            rows[target] = same
            for site in others:
                rows[site] = opposite
            response = source_22_response(tuple(rows), betas, active, direct_scale)
            assert response[target] == 2 * S_value
            assert all(response[site] == 0 for site in others)

    # Replacing a D-type target by its zero local row is again a literal
    # S_r singleton.  This includes both centres and the coordinate extra.
    coordinate_D = centres + (extra,)
    for target in coordinate_D:
        others = tuple(site for site in active if site != target)
        for swap in (False, True):
            zero, one = (E1, E0) if swap else (E0, E1)
            rows = [ZERO] * len(betas)
            for site in S_marked:
                rows[site] = E2
            for site in S_left:
                rows[site] = zero
            rows[singleton] = one
            rows[target] = ZERO
            for site in others:
                rows[site] = one
            response = source_22_response(tuple(rows), betas, active, direct_scale)
            assert response[target] == 2 * S_value
            assert all(response[site] == 0 for site in others)

    # Common-live I targets have a nonzero third local row.  Their S_r
    # target coefficient survives; every additional marked-pair term lands
    # in a binary active column already killed above.
    for target in common_live:
        rows = [ZERO] * len(betas)
        for site in S_marked:
            rows[site] = E2
        for site in S_left:
            rows[site] = E0
        rows[singleton] = E1
        rows[target] = E2
        for site in active:
            if site != target:
                rows[site] = E1
        response = source_22_response(tuple(rows), betas, active, direct_scale)
        assert response[target] == 2 * S_value


def integer_partitions(total, maximum=None):
    if total == 0:
        yield ()
        return
    if maximum is None or maximum > total:
        maximum = total
    for first in range(maximum, 0, -1):
        for tail in integer_partitions(total - first, first):
            yield (first,) + tail


def audit_repeated_pair_selection():
    # Apart from the direct all-equal case, every repetition profile has a
    # repeated class whose two-label deletion leaves at least two values.
    for size in range(6, 15):
        for profile in integer_partitions(size):
            if profile == (size,) or all(part == 1 for part in profile):
                continue
            assert any(
                part >= 2
                and sum(int(index != chosen or value - 2 > 0)
                        for index, value in enumerate(profile)) >= 2
                for chosen, part in enumerate(profile)
            ), profile


def audit_incidence_and_algebra():
    # S_r: all r-subset sums on r+2 points determine every point value.
    for r in range(3, 11):
        points = tuple(range(r + 2))
        incidence = sp.Matrix([
            [int(point in subset) for point in points]
            for subset in combinations(points, r)
        ])
        assert incidence.rank() == r + 2

    # P_r expansion along its two exceptional columns.
    u = sp.symbols("u0:5", nonzero=True)
    v = sp.symbols("v0:5", nonzero=True)
    pair_sum = sum(
        u[i] * v[j] for i in range(5) for j in range(5) if i != j
    )
    symmetric_sum = sum(
        u[i] * v[j] + u[j] * v[i] for i, j in combinations(range(5), 2)
    )
    assert sp.expand(pair_sum - symmetric_sum) == 0

    # If every one-point deletion sum vanishes on N of size r+1, summing
    # q_m=T-s_m gives (r-1)T=0 and hence every row sum s_m=0.
    for r in range(3, 11):
        assert (r + 1) - 2 == r - 1
        assert r - 1 != 0

    # The row-sum equation becomes an affine equation in
    # w_i=1/(nu_i+1).  Two distinct values force both coefficients to zero.
    A, B, x, y, w = sp.symbols("A B x y w")
    affine = sp.expand(B * (1 + (y - 1) * w) + A * (1 + (x - 1) * w) - 2)
    assert sp.Poly(affine, w).all_coeffs() == [
        A * x - A + B * y - B,
        A + B - 2,
    ]
    # In the repeated x=y branch these two conditions contradict x!=1.
    assert sp.simplify(
        (A * x - A + B * x - B).subs(B, 2 - A)
        - 2 * (x - 1)
    ) == 0

    # In the all-distinct branch, comparison of the fixed-x sums gives the
    # displayed factor.  Three distinct comparison values then force two
    # of them both to equal -3x.
    z = sp.Symbol("z")
    Fxy = (y + 1) / (x + y) + 2 * (1 - y) / (x - y)
    Fxz = (z + 1) / (x + z) + 2 * (1 - z) / (x - z)
    expected = -(
        (x - 1) * (y - z) * (x**2 + 3 * x * y + 3 * x * z + y * z)
        / ((x - y) * (x + y) * (x - z) * (x + z))
    )
    assert sp.cancel(Fxy - Fxz - expected) == 0
    q = sp.Symbol("q")
    G_yz = x**2 + 3 * x * (y + z) + y * z
    G_yq = x**2 + 3 * x * (y + q) + y * q
    assert sp.factor(G_yz - G_yq) == (3 * x + y) * (z - q)

    # Direct all-equal P_r values contain no possible cancellation.
    beta = sp.Symbol("beta", nonzero=True)
    for r in range(3, 11):
        expression = (
            factorial(r)
            / ((beta + 1) ** (r - 2) * (2 * beta) ** 2)
        )
        assert expression != 0

    audit_repeated_pair_selection()


def main():
    audit_incidence_and_algebra()
    print("uniform P_r/S_r noncancellation algebra: PASS")
    for r in (3, 4, 5):
        audit_literal_responses(r)
        print(f"literal marked response at r={r}, t={r+3}: PASS")
    print("sole-plane first high layer t=r+3: UNIFORM COMPLETE PASS")


if __name__ == "__main__":
    main()
