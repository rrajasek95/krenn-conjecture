#!/usr/bin/env python3
"""Exhaust two decorated-cell repairs of the six-vertex three-factor source."""

from __future__ import annotations

import itertools

from verify_binary_spinflip_cycle_identity import perfect_matchings


N = 6
Q = 3
VERTICES = tuple(range(N))
MATCHINGS = tuple(perfect_matchings(VERTICES))
FACTORS = (
    ((0, 1), (2, 3), (4, 5)),
    ((0, 5), (1, 2), (3, 4)),
    ((0, 3), (1, 5), (2, 4)),
)
BASE = {
    (edge, (color, color))
    for color, matching in enumerate(FACTORS)
    for edge in matching
}
ALL_CELLS = tuple(
    (edge, colors)
    for edge in itertools.combinations(VERTICES, 2)
    for colors in itertools.product(range(Q), repeat=2)
)
COLORINGS = tuple(itertools.product(range(Q), repeat=N))
CONSTANTS = {(color,) * N for color in range(Q)}


def terms(support, coloring):
    return tuple(
        matching
        for matching in MATCHINGS
        if all((edge, (coloring[edge[0]], coloring[edge[1]])) in support
               for edge in matching)
    )


def main():
    candidates = tuple(cell for cell in ALL_CELLS if cell not in BASE)
    survivors = []
    for extras in itertools.combinations(candidates, 2):
        support = BASE | set(extras)
        active = set()
        valid = True
        nontrivial = []
        for coloring in COLORINGS:
            fiber = terms(support, coloring)
            if coloring not in CONSTANTS and len(fiber) == 1:
                valid = False
                break
            if coloring not in CONSTANTS and fiber:
                nontrivial.append((coloring, fiber))
            for matching in fiber:
                for edge in matching:
                    cell = (edge, (coloring[edge[0]], coloring[edge[1]]))
                    if cell in extras:
                        active.add(cell)
        if valid and active == set(extras):
            survivors.append((extras, nontrivial))
    print("survivors", len(survivors))
    for extras, fibers in survivors[:20]:
        print("extras", extras)
        print("mixed", [(c, len(f)) for c, f in fibers])


if __name__ == "__main__":
    main()
