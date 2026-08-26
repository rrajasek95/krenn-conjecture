#!/usr/bin/env python3
"""Exact minimum support and interval normal costs at the clean-cap boundary."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import product
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import integrate_negative_multiray_family as family  # noqa: E402
from probe_laurent_crosscolour_leakage import (  # noqa: E402
    BASE, enumerate_feasible, support_separated_identity_cap,
)
from certify_negative_family_global_min import I, down, up  # noqa: E402
from certify_eight_cell_global_branch import source_box  # noqa: E402
from certify_eight_cell_descent import EXTRA as BOUNDARY_LEAK  # noqa: E402


CAPS = ((2, 3, 4), (2, 4, 3), (3, 4, 2),
        (5, 6, 7), (5, 7, 6), (6, 7, 5))
FULL_HITTERS = (
    ((2, 6, 1, 0), (4, 7, 1, 0)),
    ((2, 6, 1, 2), (4, 5, 1, 2)),
    ((2, 6, 2, 0), (3, 7, 2, 0)),
    ((2, 7, 2, 1), (3, 5, 2, 1)),
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def d_polynomial(x):
    return (3 * x ** 8 + 2 * x ** 7 + x ** 6 + 3 * x ** 4
            + 2 * x ** 3 + 3 * x ** 2 - 20)


def minimizer_v_interval():
    lo, hi = Fraction(1073, 1000), Fraction(537, 500)
    require(d_polynomial(lo) < 0 < d_polynomial(hi), (lo, hi))
    for _ in range(90):
        middle = (lo + hi) / 2
        if d_polynomial(middle) < 0:
            lo = middle
        else:
            hi = middle
    vlo = lo - lo ** -3
    vhi = hi - hi ** -3
    return down(float(vlo)), up(float(vhi))


def star_hitting_rays():
    boundary_cells = tuple(BOUNDARY_LEAK)
    rays = sorted({tuple(sorted(row["cells"])) for row in enumerate_feasible()
                   if not set(row["cells"]) & set(boundary_cells)})
    hitters = []
    for ray in rays:
        row = {"cells": boundary_cells + ray}
        if not any(support_separated_identity_cap(row, *cap) for cap in CAPS):
            hitters.append(ray)
    return rays, hitters


def exact_full_blockers(ray):
    source = {cell: None for cell in BASE}
    source.update({cell: None for cell in BOUNDARY_LEAK})
    source.update({cell: None for cell in ray})
    try:
        stars, triangles = family.carrier_witnesses(source)
    except RuntimeError:
        return False
    return len(stars) == 168 and len(triangles) == 560


def terms(ray):
    support = set(BASE) | set(BOUNDARY_LEAK) | set(ray)
    edge_cells = defaultdict(list)
    for cell in support:
        edge_cells[cell[:2]].append(cell)
    answer = defaultdict(list)
    for matching in family.PM8:
        choices = [edge_cells[edge] for edge in matching]
        if any(not choice for choice in choices):
            continue
        for picked in product(*choices):
            word = [None] * 8
            for u, v, a, b in picked:
                word[u], word[v] = a, b
            answer[tuple(word)].append(tuple(picked))
    return answer


def energy_multiplicities(ray):
    degree = defaultdict(int)
    for u, v, a, b in ray:
        degree[u, a] += 1
        degree[v, b] += 1
    answer = {}
    for colour, layer in family.LAYERS.items():
        values = []
        for u, v in layer:
            require(degree[u, colour] == degree[v, colour],
                    (ray, colour, u, v, degree))
            values.append(degree[u, colour])
        answer[colour] = values
    return answer


def coefficient(ray, signs, vlo, vhi):
    return combined_coefficient(dict(zip(ray, signs)), vlo, vhi)


def combined_coefficient(direction, vlo, vhi):
    """Normal coefficient for an arbitrary real cell direction."""
    ray = tuple(sorted(direction))
    source = source_box(I(0), I(vlo, vhi))
    degree = defaultdict(Fraction)
    for (u, v, a, b), value in direction.items():
        degree[u, a] += Fraction(value) ** 2
        degree[v, b] += Fraction(value) ** 2
    multiplicities = {}
    for colour, layer in family.LAYERS.items():
        values = []
        for u, v in layer:
            require(degree[u, colour] == degree[v, colour],
                    (direction, colour, u, v, degree))
            values.append(degree[u, colour])
        multiplicities[colour] = values
    source_w = {}
    for colour, layer in family.LAYERS.items():
        gaps = [source[edge + (colour, colour)].square() for edge in layer]
        values = multiplicities[colour]
        rho_w = sum((m / gap for m, gap in zip(values, gaps)), I(0))
        rho_w = rho_w / sum((I(1) / gap for gap in gaps), I(0))
        for edge, value in zip(layer, values):
            diagonal = source[edge + (colour, colour)]
            source_w[edge + (colour, colour)] = (rho_w - value) / (2 * diagonal)
    for cell in BOUNDARY_LEAK:
        source_w[cell] = I(0)

    q = I(0)
    sign = direction
    for word, monomials in terms(ray).items():
        if len(set(word)) == 1:
            continue
        f0, linear, quadratic = I(0), I(0), I(0)
        for monomial in monomials:
            count = sum(cell in sign for cell in monomial)
            if count == 0:
                value = I(1)
                for cell in monomial:
                    value = value * source[cell]
                f0 = f0 + value
                derivative = I(0)
                for index, cell in enumerate(monomial):
                    piece = source_w[cell]
                    for other, other_cell in enumerate(monomial):
                        if other != index:
                            piece = piece * source[other_cell]
                    derivative = derivative + piece
                quadratic = quadratic + derivative
            elif count in (1, 2):
                value = I(1)
                for cell in monomial:
                    value = value * (sign[cell] if cell in sign else source[cell])
                if count == 1:
                    linear = linear + value
                else:
                    quadratic = quadratic + value
        q = q + linear.square() + 2 * f0 * quadratic
    return q


def main():
    vlo, vhi = minimizer_v_interval()
    rays, star_hitters = star_hitting_rays()
    full_hitters = [ray for ray in star_hitters if exact_full_blockers(ray)]
    print("boundary v interval", (vlo, vhi))
    print("elementary rays", len(rays), "star hitters", len(star_hitters),
          "full 728-blocker hitters", len(full_hitters))
    require(tuple(full_hitters) == FULL_HITTERS, full_hitters)
    records = []
    for ray in full_hitters:
        best = None
        for signs in product((-1, 1), repeat=2):
            value = coefficient(ray, signs, vlo, vhi)
            if best is None or value.lo < best[0].lo:
                best = (value, signs)
        records.append((ray, best[1], best[0]))
        print("FULL", ray, "best signs", best[1], "dP/dw", best[0])
        require(best[0].lo > 0, (ray, best))
    print("minimum normal lower bound", min(record[2].lo for record in records))


if __name__ == "__main__":
    main()
