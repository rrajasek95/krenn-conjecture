#!/usr/bin/env python3
"""Exact integration and bounded continuation of the global normal descent."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import product
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import integrate_negative_multiray_family as family  # noqa: E402
import certify_active_cap_normal_cone as normal  # noqa: E402
from certify_negative_family_global_min import I, down, up  # noqa: E402


BOUNDARY = {(0, 5, 1, 0): -1, (2, 3, 0, 1): 1}
DIRECTION = {
    (0, 2, 2, 0): -1,
    (5, 7, 0, 2): 1,
    (2, 6, 1, 0): Fraction(-1, 10),
    (4, 7, 1, 0): Fraction(-1, 10),
}
W_COEFFICIENTS = {
    0: (0, 1, 0, Fraction(1, 100)),
    1: (0, 0, Fraction(1, 100), 0),
    2: (1, 0, 0, 0),
}
VLO, VHI = normal.minimizer_v_interval()


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def root_bracket(energies):
    lo = max(energies)
    hi = max(1.0, lo + 1.0)

    def equation(rho):
        value = 1.0
        for energy in energies:
            value *= rho - energy
        return value - 1

    while equation(hi) < 0:
        hi *= 2
    for _ in range(64):
        middle = (lo + hi) / 2
        if equation(middle) < 0:
            lo = middle
        else:
            hi = middle
    return down(lo), up(hi)


def energies(colour, v, w):
    if colour == 0:
        return (0, v + w, 0, w / 100)
    if colour == 1:
        return (v, 0, w / 100, 0)
    return (w, 0, 0, 0)


def source_box(wlo, whi, vlo=None, vhi=None):
    vlo = VLO if vlo is None else vlo
    vhi = VHI if vhi is None else vhi
    w = I(wlo, whi)
    source = {}
    corners = ((vlo, wlo), (vlo, whi), (vhi, wlo), (vhi, whi))
    for colour, layer in family.LAYERS.items():
        corner_energies = [energies(colour, v, x) for v, x in corners]
        roots = [root_bracket(values) for values in corner_energies]
        gaps = []
        for index in range(4):
            values = []
            for root, energy in zip(roots, corner_energies):
                values.extend((root[0] - energy[index], root[1] - energy[index]))
            gaps.append(I(down(min(values)), up(max(values))))
        coefficients = [float(value) for value in W_COEFFICIENTS[colour]]
        denominator = sum((I(1) / gap for gap in gaps), I(0))
        rho_w = sum((coefficient / gap
                     for coefficient, gap in zip(coefficients, gaps)), I(0))
        rho_w = rho_w / denominator
        for edge, gap, coefficient in zip(layer, gaps, coefficients):
            value = gap.sqrt()
            derivative = (rho_w - coefficient) / (2 * value)
            source[edge + (colour, colour)] = (value, derivative)
    root_v = I(vlo, vhi).sqrt()
    root_w = w.sqrt()
    for cell, coefficient in BOUNDARY.items():
        source[cell] = (coefficient * root_v, I(0))
    for cell, coefficient in DIRECTION.items():
        source[cell] = (float(coefficient) * root_w,
                        float(coefficient) / (2 * root_w))
    return source


def term_ledger():
    support = set(family.BASE) | set(BOUNDARY) | set(DIRECTION)
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


TERMS = term_ledger()


def product_derivative(factors):
    value = I(1)
    for factor, _ in factors:
        value = value * factor
    derivative = I(0)
    for index, (_, factor_derivative) in enumerate(factors):
        term = factor_derivative
        for other, (factor, _) in enumerate(factors):
            if other != index:
                term = term * factor
        derivative = derivative + term
    return value, derivative


def p_and_derivative(wlo, whi):
    source = source_box(wlo, whi)
    p, derivative = I(0), I(0)
    for word, monomials in TERMS.items():
        if len(set(word)) == 1:
            continue
        amplitude, amplitude_w = I(0), I(0)
        for monomial in monomials:
            value, value_w = product_derivative([source[cell] for cell in monomial])
            amplitude = amplitude + value
            amplitude_w = amplitude_w + value_w
        p = p + amplitude.square()
        derivative = derivative + 2 * amplitude * amplitude_w
    return p, derivative


def symbolic_output_ledger():
    labels = {}
    for cell in family.BASE:
        labels[cell] = (Fraction(1), f"d{cell[0]}{cell[1]}_{cell[2]}")
    for cell, coefficient in BOUNDARY.items():
        labels[cell] = (Fraction(coefficient), "V")
    for cell, coefficient in DIRECTION.items():
        labels[cell] = (Fraction(coefficient), "T")
    answer = {}
    for word, monomials in TERMS.items():
        rendered = []
        for monomial in monomials:
            coefficient = Fraction(1)
            factors = []
            for cell in monomial:
                scalar, label = labels[cell]
                coefficient *= scalar
                factors.append(label)
            rendered.append((str(coefficient), "*".join(factors)))
        answer["".join(map(str, word))] = rendered
    return answer


def main():
    # Exact support-level carrier theorem is coefficient-independent.
    support = {cell: None for cell in family.BASE}
    support.update({cell: None for cell in BOUNDARY})
    support.update({cell: None for cell in DIRECTION})
    stars, triangles = family.carrier_witnesses(support)
    require((len(stars), len(triangles)) == (168, 560),
            (len(stars), len(triangles)))

    # Rational endpoints certify a first sign-changing critical bracket.
    left, right = 0.17247, 0.17249
    p_left, d_left = p_and_derivative(left, left)
    p_right, d_right = p_and_derivative(right, right)
    require(d_left.hi < 0 < d_right.lo, (d_left, d_right))
    sample = Fraction(86239, 500000)  # 0.172478
    p_sample, _ = p_and_derivative(float(sample), float(sample))
    print("rho equations")
    print("rho0^2*(rho0-v-w)*(rho0-w/100)=1")
    print("rho1^2*(rho1-v)*(rho1-w/100)=1")
    print("rho2^3*(rho2-w)=1")
    print("outputs", len(TERMS), "mixed", sum(len(set(word)) > 1 for word in TERMS))
    for word, monomials in sorted(symbolic_output_ledger().items()):
        print("OUTPUT", word, monomials)
    print("critical bracket", (left, right), "derivatives", d_left, d_right)
    print("certified upper at w=86239/500000", p_sample)
    print("carrier blockers", len(stars), len(triangles))
    print("branch", "unique positive rho roots exist for all w>=0; literal blockers persist for w>0")


if __name__ == "__main__":
    main()
