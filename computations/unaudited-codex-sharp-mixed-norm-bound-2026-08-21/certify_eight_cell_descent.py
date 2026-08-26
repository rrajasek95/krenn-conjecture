#!/usr/bin/env python3
"""Certified smallest-support descent from the six-cell global minimizer."""

from __future__ import annotations

from collections import defaultdict
from itertools import product
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import integrate_negative_multiray_family as family  # noqa: E402
from certify_negative_family_global_min import I, source_intervals  # noqa: E402


U_HULL = (0.039758901367190055, 0.03975890472412364)
EXTRA = {
    (0, 5, 1, 0): -1,
    (2, 3, 0, 1): 1,
}
V_ENERGY = {
    0: {(2, 5): 1},
    1: {(0, 3): 1},
    2: {},
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def extended_terms():
    support = set(family.BASE) | set(family.LEAK) | set(EXTRA)
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


def v_derivatives(u):
    source = source_intervals(u)
    answer = {}
    for colour, layer in family.LAYERS.items():
        gaps = [source[edge + (colour, colour)][0].square() for edge in layer]
        multiplicities = [V_ENERGY[colour].get(edge, 0) for edge in layer]
        rho_v = sum((m / gap for m, gap in zip(multiplicities, gaps)), I(0))
        rho_v = rho_v / sum((I(1) / gap for gap in gaps), I(0))
        for edge, multiplicity in zip(layer, multiplicities):
            value = source[edge + (colour, colour)][0]
            answer[edge + (colour, colour)] = (rho_v - multiplicity) / (2 * value)
    for cell in family.LEAK:
        answer[cell] = I(0)
    return source, answer


def product_values(term, source, source_v):
    extra_count = sum(cell in EXTRA for cell in term)
    if extra_count:
        value = I(1)
        for cell in term:
            if cell in EXTRA:
                value = value * EXTRA[cell]
            else:
                value = value * source[cell][0]
        return extra_count, value, I(0)
    value = I(1)
    for cell in term:
        value = value * source[cell][0]
    derivative = I(0)
    for index, cell in enumerate(term):
        piece = source_v[cell]
        for other, other_cell in enumerate(term):
            if other != index:
                piece = piece * source[other_cell][0]
        derivative = derivative + piece
    return 0, value, derivative


def coefficient_interval():
    u = I(*U_HULL)
    source, source_v = v_derivatives(u)
    q = I(0)
    ledger = {}
    for word, terms in extended_terms().items():
        if len(set(word)) == 1:
            continue
        f0 = I(0)
        linear = I(0)
        quadratic = I(0)
        for term in terms:
            count, value, derivative = product_values(term, source, source_v)
            if count == 0:
                f0 = f0 + value
                quadratic = quadratic + derivative
            elif count == 1:
                linear = linear + value
            elif count == 2:
                quadratic = quadratic + value
            else:
                raise RuntimeError(term)
        contribution = linear.square() + 2 * f0 * quadratic
        q = q + contribution
        if contribution.lo != 0 or contribution.hi != 0:
            ledger["".join(map(str, word))] = (
                (contribution.lo, contribution.hi),
                (f0.lo, f0.hi),
                (linear.lo, linear.hi),
                (quadratic.lo, quadratic.hi),
            )
    return q, ledger


def main():
    rho, source = family.source_series()
    source.update({cell: (0,) for cell in EXTRA})
    stars, triangles = family.carrier_witnesses(source)
    q, ledger = coefficient_interval()
    print("u hull", U_HULL)
    print("canonical extra", EXTRA)
    print("certified dP/dv at v=0", q)
    print("nonzero word contributions", ledger)
    print("literal carrier blockers", len(stars), len(triangles))
    require(q.hi < 0, q)
    require(len(stars) == 168 and len(triangles) == 560,
            (len(stars), len(triangles)))


if __name__ == "__main__":
    main()
