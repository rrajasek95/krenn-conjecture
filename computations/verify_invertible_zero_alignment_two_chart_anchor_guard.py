#!/usr/bin/env python3
"""Exact lightweight audit of the padded two-chart zero-alignment guard."""

if not __debug__:
    raise RuntimeError("run without -O so imported exact assertions remain active")

from fractions import Fraction as F
from itertools import product

import verify_curved_two_chart_anchor_complementarity as base


def require(condition, message):
    if not condition:
        raise AssertionError(message)


PADDED_GUARD = list(base.ENDPOINT_GUARD) + base.cells([
    (1, "p", "q", 1),
    (2, "p", "q", 1),
    (1, "p", "r", 1),
    (2, "p", "r", 1),
])


def determinant3(matrix):
    a, b, c = matrix
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def local_matrix(rows, site):
    """Rows are source labels; return physical-colour by source-label."""
    matrix = [[F(0) for _ in range(3)] for _ in range(3)]
    for label, row in enumerate(rows):
        for monomial, value in row.items():
            require(len(monomial) == 1, "endpoint row is not linear")
            local_site, colour = monomial[0]
            if local_site == site:
                matrix[colour][label] += value
    return matrix


def column(matrix, index):
    return tuple(matrix[row][index] for row in range(3))


def wedge_matrix(first, second, target):
    axis = tuple(F(i == target) for i in range(3))
    return [
        [determinant3((column(first, i), column(second, j), axis))
         for j in range(3)]
        for i in range(3)
    ]


def is_zero_matrix(matrix):
    return all(not value for row in matrix for value in row)


def aggregate_entry(x, y, colour_x, colour_y):
    total = F(0)
    for a, b, ca, cb, weight in PADDED_GUARD:
        if (a, b, ca, cb) == (x, y, colour_x, colour_y):
            total += weight
        elif (a, b, ca, cb) == (y, x, colour_y, colour_x):
            total += weight
    return total


def audit_chart(endpoints, cross_site):
    residual, q, first, second, direct = base.chart(PADDED_GUARD, *endpoints)
    q2 = base.divided_power(q, 2)
    q3 = base.divided_power(q, 3)

    require(q2, f"{endpoints}: common square vanished")
    require(not q3, f"{endpoints}: common cube did not vanish")
    require(
        all(cross_site in dict(monomial) for monomial in q2),
        f"{endpoints}: padding collision hypothesis failed",
    )
    require(base.vector_rank(first) == 3, f"{endpoints}: first star not good")
    require(base.vector_rank(second) == 3, f"{endpoints}: second star not good")
    require(determinant3(direct) == 6, f"{endpoints}: direct block not invertible")

    failed = []
    for i in range(3):
        for j in range(3):
            lhs = base.add(
                base.scale(q3, direct[i][j]),
                base.multiply(base.multiply(first[i], second[j]), q2),
            )
            expected = base.target(residual, i) if i == j else {}
            if lhs != expected:
                failed.append((i, j))
                require(i == j and i in (1, 2), f"{endpoints}: unexpected row failure")
                require(not lhs, f"{endpoints}: missing anchor has a residual error")
    require(failed == [(1, 1), (2, 2)], f"{endpoints}: wrong failed-row ledger")

    alignment_sets = []
    for target in range(3):
        aligned = set()
        for site in residual:
            p_site = local_matrix(first, site)
            s_site = local_matrix(second, site)
            if is_zero_matrix(wedge_matrix(p_site, s_site, target)):
                aligned.add(site)
        alignment_sets.append(aligned)
    expected_alignment = set(residual) - {cross_site}
    require(
        all(aligned == expected_alignment for aligned in alignment_sets),
        f"{endpoints}: wrong zero-alignment sets {alignment_sets}",
    )

    # Reuse the pre-existing exact Omega audit on the padded packet.
    rows = [[False for _ in range(3)] for _ in range(3)]
    rows[0][0] = True
    require(
        base.audit_chart(PADDED_GUARD, endpoints, rows, "one_zero"),
        f"{endpoints}: expected nonzero common square",
    )
    return tuple(len(aligned) for aligned in alignment_sets)


def audit_incidence_bound():
    checked = 0
    for incidences in product(range(4), repeat=6):
        if sum(incidences) < 9:
            continue
        # A double high-rank site costs one coordinate-plane site; a triple
        # site must be low-rank and costs two units in 2L+C.
        minimum_weight = sum(1 if a == 2 else 2 if a == 3 else 0
                             for a in incidences)
        require(minimum_weight >= 3, f"incidence bound failed: {incidences}")
        checked += 1
    return checked


def main():
    pq_sizes = audit_chart(("p", "q"), "r")
    pr_sizes = audit_chart(("p", "r"), "q")

    A = aggregate_entry("p", "q", 0, 0)
    B = aggregate_entry("p", "r", 0, 0)
    Fcell = aggregate_entry("q", "s", 0, 0)
    U = aggregate_entry("r", "s", 0, 0)
    curvature = A * U - B * Fcell
    require((A, B, Fcell, U) == (6, 6, 6, -6), "wrong four-cut cells")
    require(curvature == -72, "curvature vanished")

    incidence_patterns = audit_incidence_bound()
    print("PASS: padded direct determinants 6, 6")
    print(f"PASS: zero-alignment sizes pq={pq_sizes}, pr={pr_sizes}")
    print(f"PASS: physical curvature {curvature}")
    print(f"PASS: incidence normal form ({incidence_patterns} patterns)")
    print("PASS: exactly rows (1,1) and (2,2) are missing in each chart")


if __name__ == "__main__":
    main()
