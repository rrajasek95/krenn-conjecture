#!/usr/bin/env python3
"""Exact minimum-support carrier and P2 screen around the negative four-cell ray.

The frozen four-cell tangent is the sum of a P2=5 no-frozen-star ray with
amplitude 1/2 and a P2=-3/2 descending ray with amplitude 1.  Its P2 is
-1/4, but two identity response triangles remain.  This script tests whether
one further balanced elementary ray can destroy every identity star/triangle,
then audits any nonpositive survivor against arbitrary-K response carriers.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
RESPONSE = HERE.parent / "unaudited-codex-response-star-2026-08-20"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(RESPONSE))

from probe_laurent_crosscolour_leakage import (  # noqa: E402
    BASE, LAYERS, derivative_coefficients, enumerate_feasible,
    existing_mixed_cross, mixed_inner,
)
from response_star_core import (  # noqa: E402
    response_row, response_star_record, response_triangle_record,
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


ANCHOR = {
    (2, 5, 1, 2): Fraction(1, 2),
    (4, 6, 1, 2): Fraction(1, 2),
}
DESCENDING = {
    (0, 2, 2, 0): Fraction(1),
    (5, 7, 0, 2): Fraction(-1),
}
Y0 = ANCHOR | DESCENDING
ACTIVE_PAIRS = tuple(sorted({(u, v) for u, v, _, _ in BASE}))


def weighted_balance_correction(y):
    degree = {}
    for (u, v, a, b), value in y.items():
        square = value * value
        degree[u, a] = degree.get((u, a), Fraction(0)) + square
        degree[v, b] = degree.get((v, b), Fraction(0)) + square
    z = {}
    for colour, layer in LAYERS.items():
        edge_degrees = []
        for u, v in layer:
            require(degree.get((u, colour), 0) == degree.get((v, colour), 0),
                    (colour, u, v, degree.get((u, colour), 0),
                     degree.get((v, colour), 0)))
            edge_degrees.append(degree.get((u, colour), Fraction(0)))
        common = sum(edge_degrees, Fraction(0)) / 4
        for edge, value in zip(layer, edge_degrees):
            z[edge + (colour, colour)] = (common - value) / 2
    return z


def p2(y):
    z = weighted_balance_correction(y)
    base, linear, quadratic = derivative_coefficients(y, z)
    return mixed_inner(linear, linear) + 2 * existing_mixed_cross(base, quadratic)


def dense_source(y):
    source = {(u, v): [[Fraction(0) for _ in range(3)] for _ in range(3)]
              for u, v in combinations(range(8), 2)}
    for (u, v, a, b), value in BASE.items():
        source[u, v][a][b] = value
    for (u, v, a, b), value in y.items():
        source[u, v][a][b] += value
    return source


def identity_response_edges(source, p, q):
    residual = tuple(site for site in range(8) if site not in (p, q))
    identity = [Fraction(int(i == j)) for i in range(3) for j in range(3)]
    answer = set()
    for a, b in combinations(residual, 2):
        for alpha in range(3):
            for beta in range(3):
                row = response_row(source, p, q, a, b, alpha, beta)
                if sum(x * y for x, y in zip(row, identity)):
                    answer.add((a, b))
                    break
            if (a, b) in answer:
                break
    return answer


def identity_carriers(y):
    source = dense_source(y)
    answer = []
    for p, q in ACTIVE_PAIRS:
        edges = identity_response_edges(source, p, q)
        if not edges:
            answer.append((p, q, "zero", ()))
            continue
        centres = tuple(site for site in range(8) if site not in (p, q)
                        and all(site in edge for edge in edges))
        for centre in centres:
            answer.append((p, q, "star", (centre,)))
        union = set().union(*map(set, edges))
        if len(union) == 3:
            answer.append((p, q, "triangle", tuple(sorted(union))))
    return answer


def full_carriers(y):
    source = dense_source(y)
    answer = []
    for p, q in combinations(range(8), 2):
        residual = tuple(site for site in range(8) if site not in (p, q))
        for centre in residual:
            record = response_star_record(source, p, q, centre)
            if record["passes"]:
                answer.append((p, q, "star", (centre,), record["rank"], record["cap"]))
        for triangle in combinations(residual, 3):
            record = response_triangle_record(source, p, q, triangle)
            if record["passes"]:
                answer.append((p, q, "triangle", triangle,
                               record["rank"], record["cap"]))
    return answer


def main():
    require(p2(Y0) == Fraction(-1, 4), p2(Y0))
    initial = identity_carriers(Y0)
    print("base P2", p2(Y0), "identity carriers", initial)
    require(initial == [
        (2, 3, "triangle", (0, 4, 5)),
        (5, 7, "triangle", (0, 2, 6)),
    ], initial)

    supports = sorted({tuple(sorted(row["cells"])) for row in enumerate_feasible()})
    require(len(supports) == 72, len(supports))
    survivors = []
    epsilon = Fraction(1, 10)
    for cells in supports:
        if set(cells) & set(Y0):
            continue
        for signs in product((Fraction(-1), Fraction(1)), repeat=2):
            y = dict(Y0)
            for cell, sign in zip(cells, signs):
                y[cell] = epsilon * sign
            value = p2(y)
            carriers = identity_carriers(y)
            if not carriers and value <= 0:
                survivors.append((value, cells, signs, y))
    survivors.sort(key=lambda item: (item[0], item[1], item[2]))
    print("six-cell identity-carrier-free nonpositive candidates", len(survivors))
    for record in survivors[:10]:
        print("CANDIDATE", record[:3])
    require(survivors, "one added elementary ray never destroys both triangles")

    value, cells, signs, y = survivors[0]
    arbitrary = full_carriers(y)
    print("first candidate P2", value, "extra", cells, signs)
    print("full arbitrary-K carriers", len(arbitrary))
    for record in arbitrary:
        print("CARRIER", record)


if __name__ == "__main__":
    main()
