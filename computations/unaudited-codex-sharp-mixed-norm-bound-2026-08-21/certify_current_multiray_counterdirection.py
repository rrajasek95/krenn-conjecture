#!/usr/bin/env python3
"""Exact four-cell descending normal at the corrected 18-cell minimum."""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import integrate_negative_multiray_family as family  # noqa: E402
import integrate_global_normal_counterfamily as current  # noqa: E402
import screen_next_active_set_descent as single  # noqa: E402
from certify_negative_family_global_min import I  # noqa: E402


LEFT = {
    (0, 4, 1, 2): Fraction(1),
    (1, 3, 2, 1): Fraction(1),
}
RIGHT = {
    (1, 5, 2, 0): Fraction(1),
    (2, 4, 0, 2): Fraction(-1),
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def gram_orthogonal(support):
    remote = defaultdict(set)
    for u, v, a, b in support:
        remote[u, v, b].add(a)
        remote[v, u, a].add(b)
    return all(len(colours) == 1 for colours in remote.values())


def term_ledger(active):
    support = single.CURRENT_SUPPORT | set(active)
    edge_cells = defaultdict(list)
    for cell in support:
        edge_cells[cell[:2]].append(cell)
    answer = defaultdict(list)
    from itertools import product
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


def quadratic(direction):
    raw = current.source_box(single.WLO, single.WHI,
                             single.VLO, single.VHI)
    source = {cell: value for cell, (value, _) in raw.items()}
    degree = defaultdict(Fraction)
    for (u, v, a, b), value in direction.items():
        square = value * value
        degree[u, a] += square
        degree[v, b] += square
    source_z = {}
    for colour, layer in family.LAYERS.items():
        gaps = [source[edge + (colour, colour)].square() for edge in layer]
        values = []
        for u, v in layer:
            require(degree[u, colour] == degree[v, colour],
                    (direction, colour, u, v, degree))
            values.append(degree[u, colour])
        denominator = sum((I(1) / gap for gap in gaps), I(0))
        rho_z = sum((float(value) / gap
                     for value, gap in zip(values, gaps)), I(0)) / denominator
        for edge, value in zip(layer, values):
            diagonal = source[edge + (colour, colour)]
            source_z[edge + (colour, colour)] = (rho_z - float(value)) / (2 * diagonal)
    for cell in current.BOUNDARY:
        source_z[cell] = I(0)
    for cell in current.DIRECTION:
        source_z[cell] = I(0)

    q = I(0)
    for word, monomials in term_ledger(direction).items():
        if len(set(word)) == 1:
            continue
        f0, linear, second = I(0), I(0), I(0)
        for monomial in monomials:
            count = sum(cell in direction for cell in monomial)
            if count == 0:
                value = I(1)
                for cell in monomial:
                    value = value * source[cell]
                f0 = f0 + value
                derivative = I(0)
                for index, cell in enumerate(monomial):
                    piece = source_z[cell]
                    for other, other_cell in enumerate(monomial):
                        if other != index:
                            piece = piece * source[other_cell]
                    derivative = derivative + piece
                second = second + derivative
            elif count <= 2:
                value = I(1)
                for cell in monomial:
                    value = value * (float(direction[cell])
                                     if cell in direction else source[cell])
                if count == 1:
                    linear = linear + value
                else:
                    second = second + value
        q = q + linear.square() + 2 * f0 * second
    return q


def add(left, right, scale=Fraction(1)):
    answer = dict(left)
    for cell, value in right.items():
        answer[cell] = answer.get(cell, Fraction(0)) + scale * value
    return {cell: value for cell, value in answer.items() if value}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate-delete-right", action="store_true")
    args = parser.parse_args()
    active = LEFT if args.mutate_delete_right else add(LEFT, RIGHT, Fraction(5))
    support = single.CURRENT_SUPPORT | set(active)
    require(gram_orthogonal(support), "port Gram orthogonality failed")
    try:
        stars, triangles = family.carrier_witnesses({cell: None for cell in support})
    except RuntimeError as error:
        raise RuntimeError("literal carrier blocker failed") from error
    require((len(stars), len(triangles)) == (168, 560),
            (len(stars), len(triangles)))

    a, b = quadratic(LEFT), quadratic(RIGHT)
    total = quadratic(add(LEFT, RIGHT))
    cross = (total - a - b) / 2
    determinant = a * b - cross.square()
    chosen = quadratic(active)
    require(determinant.hi < 0 and chosen.hi < 0,
            (a, b, cross, determinant, chosen))
    print("critical box", (single.VLO, single.VHI),
          (single.WLO, single.WHI))
    print("matrix", a, cross, b, "det", determinant)
    print("rational descending direction", active)
    print("normal coefficient", chosen)
    print("support cells", len(support), "carrier blockers", len(stars), len(triangles))


if __name__ == "__main__":
    main()
