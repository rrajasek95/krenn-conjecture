#!/usr/bin/env python3
"""Exact OO one-anchor and permanent-null counterguard audit.

This reuses two already frozen literal packets, but independently checks the
new statements:

* the one-anchor packet contains a curved pair of rank-one arms with distinct
  outgoing head axes;
* one arm is good and the shared-end star of the other is injective, while
  its remote endpoint is rank zero (so this is not a counterexample to the
  doubly-good OO theorem);
* a 2x2 permanent-zero response completion has the correct first response
  but seven nonzero higher mixed defects; and
* one diagonal coefficient and one off-diagonal coefficient are the minimal
  literal pair separating the two old complementary guards.
"""

from fractions import Fraction as F
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import verify_curved_two_chart_anchor_complementarity as complement  # noqa: E402
import verify_h3_one_anchor_selector_four_cut_guard as one_anchor  # noqa: E402


def require(condition, message):
    if not condition:
        raise AssertionError(message)


EIGHT_SITES = ("p", "q") + one_anchor.SITES
SITE_ORDER = {site: index for index, site in enumerate(EIGHT_SITES)}


def canonical_cell(u, v, i, j):
    if SITE_ORDER[u] < SITE_ORDER[v]:
        return u, v, i, j
    return v, u, j, i


def add_cell(blocks, u, v, i, j, value):
    key = canonical_cell(u, v, i, j)
    blocks[key] = blocks.get(key, F(0)) + F(value)
    if not blocks[key]:
        del blocks[key]


def entry(blocks, u, v, i, j):
    return blocks.get(canonical_cell(u, v, i, j), F(0))


def rational_rank(rows):
    matrix = [[F(value) for value in row] for row in rows]
    rank = 0
    columns = len(matrix[0]) if matrix else 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(
                    matrix[row], matrix[rank], strict=True
                )
            ]
        rank += 1
    return rank


def star_rank(blocks, endpoint, deleted_neighbor):
    neighbors = [
        site for site in EIGHT_SITES if site not in (endpoint, deleted_neighbor)
    ]
    columns = [(site, colour) for site in neighbors for colour in range(3)]
    rows = [
        [entry(blocks, endpoint, site, row_colour, colour) for site, colour in columns]
        for row_colour in range(3)
    ]
    return rational_rank(rows)


def build_one_anchor_eight_site_packet():
    blocks = {}
    add_cell(blocks, "p", "q", 0, 1, 1)
    for row, form in enumerate(one_anchor.P):
        for (site, colour), value in form.items():
            add_cell(blocks, "p", site, row, colour, value)
    for row, form in enumerate(one_anchor.S):
        for (site, colour), value in form.items():
            add_cell(blocks, "q", site, row, colour, value)
    for u, i, v, j, value in one_anchor.Q_EDGES:
        add_cell(blocks, u, v, i, j, value)
    return blocks


def audit_curved_oo_boundary():
    blocks = build_one_anchor_eight_site_packet()

    # pq=E_01 and pA0=E_00 are rank-one arms with distinct right/head axes.
    pq = [[entry(blocks, "p", "q", i, j) for j in range(3)] for i in range(3)]
    pr = [[entry(blocks, "p", "A0", i, j) for j in range(3)] for i in range(3)]
    require(rational_rank(pq) == rational_rank(pr) == 1, "OO arms lost rank one")
    require(
        {j for i in range(3) for j in range(3) if pq[i][j]} == {1},
        "pq head axis changed",
    )
    require(
        {j for i in range(3) for j in range(3) if pr[i][j]} == {0},
        "pA0 head axis changed",
    )

    # At s=B0 and output colour 0, AU-BF = 1*0 - 1*1 = -1.
    curvature = (
        entry(blocks, "p", "q", 0, 1)
        * entry(blocks, "A0", "B0", 0, 0)
        - entry(blocks, "p", "A0", 0, 0)
        * entry(blocks, "q", "B0", 1, 0)
    )
    require(curvature == -1, "curved OO minor changed")

    ranks = {
        "p|q": star_rank(blocks, "p", "q"),
        "q|p": star_rank(blocks, "q", "p"),
        "p|A0": star_rank(blocks, "p", "A0"),
        "A0|p": star_rank(blocks, "A0", "p"),
    }
    require(ranks == {"p|q": 3, "q|p": 3, "p|A0": 3, "A0|p": 0}, "OO rank ledger changed")

    x0 = (0,) * len(one_anchor.SITES)
    require(one_anchor.pair_row(0, 0) == {x0: F(1)}, "00 anchor changed")
    for i in range(3):
        for j in range(3):
            if i != j:
                require(one_anchor.pair_row(i, j) == {}, "off-diagonal row changed")
    return ranks, curvature


def audit_permanent_null_failure():
    # r = p0*s0 + p0*s1 + p1*s0 - p1*s1 has coefficient permanent zero.
    matrix = ((1, 1), (1, -1))
    require(matrix[0][0] * matrix[1][1] + matrix[0][1] * matrix[1][0] == 0, "permanent changed")

    family = {}
    # First exponent records q degree; second exponent records r degree.
    for u, i, v, j, value in one_anchor.Q_EDGES:
        one_anchor.add_edge(family, u, i, v, j, {(1, 0): value})
    for i in range(2):
        for j in range(2):
            one_anchor.add_outer(
                family,
                one_anchor.P[i],
                one_anchor.S[j],
                {(0, 1): F(matrix[i][j])},
            )
    tensor = one_anchor.matching_tensor(family)

    x0 = (0,) * len(one_anchor.SITES)
    require(tensor[x0] == {(2, 1): F(1)}, "first response is no longer X0")
    mixed = {word: value for word, value in tensor.items() if word != x0}
    require(len(mixed) == 7, "higher-defect count changed")
    degree_census = {}
    for polynomial in mixed.values():
        require(len(polynomial) == 1, "a defect acquired multiple bidegrees")
        degree = next(iter(polynomial))
        degree_census[degree] = degree_census.get(degree, 0) + 1
    require(degree_census == {(1, 2): 3, (0, 3): 4}, "higher cumulant census changed")
    require(
        sorted(next(iter(poly.values())) for poly in mixed.values())
        == [F(-6), F(-6), F(2), F(2), F(2), F(6), F(6)],
        "higher cumulant coefficients changed",
    )
    return degree_census


def chart_row(cells, endpoints, i, j):
    residual, q, first, second, direct = complement.chart(cells, *endpoints)
    return residual, complement.add(
        complement.scale(complement.divided_power(q, 3), direct[i][j]),
        complement.multiply(
            complement.multiply(first[i], second[j]),
            complement.divided_power(q, 2),
        ),
    )


def audit_atomic_guard_separator():
    # On the pq chart, the diagonal guard's unique (2,1) failure is
    # (cs)_(2,1) (ad)_2 (br)_1.
    omega = complement.key({"a": 2, "b": 1, "c": 2, "d": 2, "r": 1, "s": 1})
    expected = {}
    for name, cells in (
        ("diagonal", complement.DIAGONAL_GUARD),
        ("offdiagonal", complement.ENDPOINT_GUARD),
    ):
        residual, diagonal = chart_row(cells, ("p", "q"), 2, 2)
        _, offdiagonal = chart_row(cells, ("p", "q"), 2, 1)
        x2 = complement.key({site: 2 for site in residual})
        expected[name] = (diagonal.get(x2, F(0)), offdiagonal.get(omega, F(0)))
    require(expected == {"diagonal": (F(1), F(1)), "offdiagonal": (F(0), F(0))}, "atomic guard separator changed")
    return expected


def main():
    ranks, curvature = audit_curved_oo_boundary()
    degree_census = audit_permanent_null_failure()
    separator = audit_atomic_guard_separator()
    print("OO one-anchor/permanent-null frontier: PASS")
    print(f"curved distinct-head arms: kappa={curvature}; star ranks={ranks}")
    print(f"permanent-zero completion higher defects: {degree_census}")
    print(f"(diagonal-22, offdiagonal-21-word) guard values: {separator}")


if __name__ == "__main__":
    main()
