#!/usr/bin/env python3
"""Exact ternary cap-selection theorem on the six-distinct-port chart.

Delete reciprocal endpoints p,q and suppose their three labelled star rows
are literal one-site ports P_0,P_1,P_2 and S_0,S_1,S_2 on six distinct
residual sites.  For a completely general cap K=(k_ij), the first jet is

    R_K = sum_ij k_ij P_i S_j.

This checker reconstructs R_K^[2] in the site-square-zero algebra and proves
that its nine coefficients are exactly the 2x2 permanents of K.  It then
checks an integral certificate showing that these permanents, saturated by
k00*k11*k22 (and hence by any reciprocal scalar as well), give the unit
ideal over characteristic zero.

It also exhausts the support lemma used at the non-port-separated boundary:
a simple edge family with no two disjoint edges is contained in a star or a
triangle.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json


NVAR = 9
ZERO = (0,) * NVAR
VARIABLE_NAMES = tuple(f"k{i}{j}" for i in range(3) for j in range(3))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def variable(i, j):
    exponent = [0] * NVAR
    exponent[3 * i + j] = 1
    return {tuple(exponent): F(1)}


def constant(value):
    return {} if not value else {ZERO: F(value)}


def add(*terms):
    answer = defaultdict(F)
    for scale, polynomial in terms:
        for exponent, coefficient in polynomial.items():
            answer[exponent] += F(scale) * coefficient
    return {
        exponent: coefficient
        for exponent, coefficient in answer.items()
        if coefficient
    }


def multiply(left, right):
    answer = defaultdict(F)
    for first, a in left.items():
        for second, b in right.items():
            exponent = tuple(
                x + y for x, y in zip(first, second, strict=True)
            )
            answer[exponent] += a * b
    return {
        exponent: coefficient
        for exponent, coefficient in answer.items()
        if coefficient
    }


def scale(value, polynomial):
    return {
        exponent: F(value) * coefficient
        for exponent, coefficient in polynomial.items()
        if value * coefficient
    }


def product(*polynomials):
    answer = constant(1)
    for polynomial in polynomials:
        answer = multiply(answer, polynomial)
    return answer


def permanent(k, rows, columns):
    i, m = rows
    j, n = columns
    return add(
        (1, multiply(k[i][j], k[m][n])),
        (1, multiply(k[i][n], k[m][j])),
    )


def reconstruct_port_square(k):
    """Enumerate the exact four-site coefficients of R_K^[2]."""

    # Sites 0,1,2 are P_0,P_1,P_2; sites 3,4,5 are S_0,S_1,S_2.
    edges = {(i, 3 + j): k[i][j] for i in range(3) for j in range(3)}
    coefficients = {}
    for sites in combinations(range(6), 4):
        a, b, c, d = sites
        value = {}
        for (u, v), (w, x) in (
            ((a, b), (c, d)),
            ((a, c), (b, d)),
            ((a, d), (b, c)),
        ):
            value = add((1, value), (1, multiply(
                edges.get(tuple(sorted((u, v))), {}),
                edges.get(tuple(sorted((w, x))), {}),
            )))
        if value:
            coefficients[sites] = value
    return coefficients


def audit_permanent_packet():
    k = [[variable(i, j) for j in range(3)] for i in range(3)]
    coefficients = reconstruct_port_square(k)
    expected = {}
    for rows in combinations(range(3), 2):
        for columns in combinations(range(3), 2):
            sites = tuple(sorted(rows + tuple(3 + j for j in columns)))
            expected[sites] = permanent(k, rows, columns)
    require(coefficients == expected, "R_K^[2] stopped being the permanent packet")
    require(len(coefficients) == 9, "six-port coefficient census changed")
    return k, coefficients


def audit_saturation_certificate(k, permanents):
    # Four of the nine permanent equations already give the active unit.
    a, b, c = k[0]
    d, e, f = k[1]
    g, _h, i = k[2]
    f01 = permanents[(0, 1, 3, 4)]  # ae+bd
    g1 = permanents[(0, 1, 3, 5)]   # af+cd
    g2 = permanents[(0, 1, 4, 5)]   # bf+ce
    f02 = permanents[(0, 2, 3, 5)]  # ai+cg

    # a*g2-b*g1+c*f01 = 2*a*c*e.
    inner = add(
        (1, multiply(a, g2)),
        (-1, multiply(b, g1)),
        (1, multiply(c, f01)),
    )
    require(inner == scale(2, product(a, c, e)),
            "first permanent certificate changed")

    # e*i*(2*a*e*f02-g*inner) = 2*(a*e*i)^2.
    certificate = multiply(
        product(e, i),
        add(
            (2, product(a, e, f02)),
            (-1, multiply(g, inner)),
        ),
    )
    diagonal_activity = product(a, e, i)
    require(certificate == scale(2, product(
        diagonal_activity, diagonal_activity
    )), "active saturation certificate changed")

    # A reciprocal direct block lambda*E_ba only adds the open condition
    # s=lambda*k_ba != 0.  The diagonal activity already makes the ideal
    # empty, for all nine possible positions of the literal coordinate cell.
    reciprocal_positions = []
    for row in range(3):
        for column in range(3):
            full_activity = product(diagonal_activity, k[row][column])
            require(full_activity, "reciprocal activity polynomial vanished")
            reciprocal_positions.append((row, column))
    return {
        "certificate_terms": len(certificate),
        "diagonal_activity_power": 2,
        "reciprocal_positions": reciprocal_positions,
    }


def is_star_or_triangle(vertices, edges):
    if not edges:
        return True
    common = set(vertices)
    for edge in edges:
        common &= set(edge)
    if common:
        return True
    used = set().union(*(set(edge) for edge in edges))
    return len(used) == 3 and all(set(edge) <= used for edge in edges)


def audit_intersecting_support_theorem():
    # Exhaust the six-site support universe used by the cap packet.  The
    # statement is graph-theoretic and the same proof works for every size:
    # choose two meeting edges ab,ac; every edge meets both, hence contains a
    # or equals bc.
    vertices = tuple(range(6))
    all_edges = tuple(combinations(vertices, 2))
    intersecting = 0
    for mask in range(1 << len(all_edges)):
        edges = tuple(
            edge for index, edge in enumerate(all_edges)
            if mask & (1 << index)
        )
        if any(set(left).isdisjoint(right)
               for left, right in combinations(edges, 2)):
            continue
        intersecting += 1
        require(is_star_or_triangle(vertices, edges),
                f"intersecting family escaped star/triangle: {edges}")
    require(intersecting == 192, "six-site intersecting-family census changed")
    return intersecting


def main():
    k, permanents = audit_permanent_packet()
    saturation = audit_saturation_certificate(k, permanents)
    intersecting = audit_intersecting_support_theorem()
    ledger = {
        "cap_variables": list(VARIABLE_NAMES),
        "residual_port_sites": 6,
        "quadratic_coefficients": len(permanents),
        "coefficient_kind": "all 2x2 permanents of K",
        "saturation": saturation,
        "intersecting_supports_on_six_sites": intersecting,
        "structural_boundary": (
            "clean active cap forces a kernel in the four-port product map; "
            "under unique-fibre support R_K is contained in a star or triangle"
        ),
        "proof_interface": [
            {
                "case": "intersecting support",
                "normal_forms": ["star", "triangle"],
                "status": "R_K^[2]=0 termwise; exact hafnian Schur descent applies",
            },
            {
                "case": "two-colour coordinate four-port exchange",
                "status": "covered by adjacent-cubic descent",
            },
            {
                "case": "ternary four-site or repeated-label cancellation circuit",
                "status": "open; curved rank-one overlap does not yet construct K",
            },
        ],
        "characteristic": "not 2 (application: C)",
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    expected = "ddf105f562fda6658a70533fc260b523a3f960b208b322c30414daaf872877c8"
    require(digest == expected, f"reciprocal cap-selection ledger changed: {digest}")
    print("reciprocal ternary cap-selection variety: PASS")
    print("six distinct ports: 9 permanent equations; active saturation is unit")
    print("general clean cap: four-port product kernel, or star/triangle support")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
