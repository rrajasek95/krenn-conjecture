#!/usr/bin/env python3
"""Outward interval branch screen for the exact two-parameter 8-cell family."""

from __future__ import annotations

from collections import defaultdict
from itertools import product
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import integrate_negative_multiray_family as family  # noqa: E402
from certify_negative_family_global_min import I, down, up  # noqa: E402
from certify_eight_cell_descent import EXTRA  # noqa: E402


def root_bracket(energies):
    lo = max(energies)
    hi = max(1.0, lo + 1.0)

    def equation(rho):
        value = 1.0
        for energy in energies:
            value *= rho - energy
        return value - 1.0

    while equation(hi) < 0:
        hi *= 2
    for _ in range(58):
        middle = (lo + hi) / 2
        if equation(middle) < 0:
            lo = middle
        else:
            hi = middle
    return down(lo), up(hi)


def energy_profiles(u, v):
    return {
        0: (0, u + v, u / 100, 0),
        1: (v, 0, u / 4, 0),
        2: (101 * u / 100, 0, 0, u / 4),
    }


def source_box(u, v):
    source = {}
    corners = ((u.lo, v.lo), (u.lo, v.hi),
               (u.hi, v.lo), (u.hi, v.hi))
    for colour, layer in family.LAYERS.items():
        corner_energies = [energy_profiles(a, b)[colour] for a, b in corners]
        roots = [root_bracket(energies) for energies in corner_energies]
        for index, edge in enumerate(layer):
            gaps = []
            for root, energies in zip(roots, corner_energies):
                gaps.extend((root[0] - energies[index],
                             root[1] - energies[index]))
            source[edge + (colour, colour)] = I(
                down(math.sqrt(max(0.0, min(gaps)))),
                up(math.sqrt(max(gaps))),
            )
    root_u = u.sqrt()
    root_v = v.sqrt()
    for cell, coefficient in family.LEAK.items():
        source[cell] = float(coefficient) * root_u
    for cell, coefficient in EXTRA.items():
        source[cell] = coefficient * root_v
    return source


def terms():
    support = set(family.BASE) | set(family.LEAK) | set(EXTRA)
    cells = defaultdict(list)
    for cell in support:
        cells[cell[:2]].append(cell)
    answer = defaultdict(list)
    for matching in family.PM8:
        choices = [cells[edge] for edge in matching]
        if any(not choice for choice in choices):
            continue
        for picked in product(*choices):
            word = [None] * 8
            for a, b, i, j in picked:
                word[a], word[b] = i, j
            answer[tuple(word)].append(tuple(picked))
    return answer


TERMS = terms()


U_COEFFICIENTS = {
    0: (0, 1, 1 / 100, 0),
    1: (0, 0, 1 / 4, 0),
    2: (101 / 100, 0, 0, 1 / 4),
}


def p_box(ulo, uhi, vlo, vhi):
    source = source_box(I(ulo, uhi), I(vlo, vhi))
    p = I(0)
    for word, monomials in TERMS.items():
        if len(set(word)) == 1:
            continue
        amplitude = I(0)
        for monomial in monomials:
            value = I(1)
            for cell in monomial:
                value = value * source[cell]
            amplitude = amplitude + value
        p = p + amplitude.square()
    return p


def boundary_u_coefficient(vlo, vhi):
    """Coefficient of u at u=0, including all sqrt(u) leak terms."""
    source = source_box(I(0), I(vlo, vhi))
    source_u = {}
    for colour, layer in family.LAYERS.items():
        gaps = [source[edge + (colour, colour)].square() for edge in layer]
        coefficients = U_COEFFICIENTS[colour]
        rho_u = sum((a / gap for a, gap in zip(coefficients, gaps)), I(0))
        rho_u = rho_u / sum((I(1) / gap for gap in gaps), I(0))
        for edge, coefficient in zip(layer, coefficients):
            value = source[edge + (colour, colour)]
            source_u[edge + (colour, colour)] = (rho_u - coefficient) / (2 * value)
    for cell in EXTRA:
        source_u[cell] = I(0)

    coefficient = I(0)
    for word, monomials in TERMS.items():
        if len(set(word)) == 1:
            continue
        f0, linear, quadratic = I(0), I(0), I(0)
        for monomial in monomials:
            count = sum(cell in family.LEAK for cell in monomial)
            if count == 0:
                value = I(1)
                for cell in monomial:
                    value = value * source[cell]
                f0 = f0 + value
                derivative = I(0)
                for index, cell in enumerate(monomial):
                    piece = source_u[cell]
                    for other, other_cell in enumerate(monomial):
                        if other != index:
                            piece = piece * source[other_cell]
                    derivative = derivative + piece
                quadratic = quadratic + derivative
            elif count in (1, 2):
                value = I(1)
                for cell in monomial:
                    if cell in family.LEAK:
                        value = value * float(family.LEAK[cell])
                    else:
                        value = value * source[cell]
                if count == 1:
                    linear = linear + value
                else:
                    quadratic = quadratic + value
        coefficient = coefficient + linear.square() + 2 * f0 * quadratic
    return coefficient


def main():
    old_min_upper = 1.798070075935624
    print("boundary point", p_box(0, 0, 0.26439997, 0.26439999))
    print("boundary normal coefficient near minimizer",
          boundary_u_coefficient(0.2568, 0.2720))
    # Coarse global screen.  The tail bounds are literal single-output bounds:
    # u>=5 uses 22002222; v>=5 uses 12222000 and gives at least v^2.
    pieces = 100
    kept = []
    for i in range(pieces):
        ulo, uhi = 5 * i / pieces, 5 * (i + 1) / pieces
        for j in range(pieces):
            vlo, vhi = 5 * j / pieces, 5 * (j + 1) / pieces
            p = p_box(ulo, uhi, vlo, vhi)
            if p.lo <= old_min_upper:
                kept.append((ulo, uhi, vlo, vhi, p.lo))
    print("coarse kept", len(kept))
    if kept:
        print("coarse hull", min(x[0] for x in kept), max(x[1] for x in kept),
              min(x[2] for x in kept), max(x[3] for x in kept),
              min(x[4] for x in kept))


if __name__ == "__main__":
    main()
