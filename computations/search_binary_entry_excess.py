#!/usr/bin/env python3
"""Enumerate tiny support extensions of the entry-minimal binary normal form.

This is a finite support audit, not an algebraic existence proof.  Fix the
alternating Hamilton realization on six vertices and add k decorated cells.
Report extensions in which every mixed coloring has either zero or at least
two supported perfect-matching monomials and every added cell is active.
"""

from __future__ import annotations

import itertools

from verify_binary_spinflip_cycle_identity import perfect_matchings


N = 6
VERTICES = tuple(range(N))
MATCHINGS = tuple(perfect_matchings(VERTICES))
P0 = ((0, 1), (2, 3), (4, 5))
P1 = ((0, 5), (1, 2), (3, 4))
BASE = {(edge, (0, 0)) for edge in P0} | {(edge, (1, 1)) for edge in P1}
ALL_CELLS = [
    (edge, colors)
    for edge in itertools.combinations(VERTICES, 2)
    for colors in itertools.product((0, 1), repeat=2)
]


def compatible(cell, coloring):
    (u, v), (a, b) = cell
    return coloring[u] == a and coloring[v] == b


def supported_terms(support, coloring):
    answer = []
    for matching in MATCHINGS:
        cells = tuple((edge, (coloring[edge[0]], coloring[edge[1]])) for edge in matching)
        if all(cell in support for cell in cells):
            answer.append(cells)
    return answer


def admissible(extras):
    support = BASE | set(extras)
    used = set()
    fibers = {}
    for coloring in itertools.product((0, 1), repeat=N):
        terms = supported_terms(support, coloring)
        fibers[coloring] = terms
        if coloring not in ((0,) * N, (1,) * N) and len(terms) == 1:
            return None
        for term in terms:
            used.update(set(term) & set(extras))
    if used != set(extras):
        return None
    return fibers


def main():
    candidates = [cell for cell in ALL_CELLS if cell not in BASE]
    for k in (1, 2, 3):
        survivors = []
        for extras in itertools.combinations(candidates, k):
            fibers = admissible(extras)
            if fibers is not None:
                mixed = [(c, t) for c, t in fibers.items() if c not in ((0,) * N, (1,) * N) and t]
                survivors.append((extras, mixed))
                if len(survivors) >= 5:
                    break
        print(f"k={k} survivors_shown={len(survivors)}")
        for extras, mixed in survivors:
            print(" extras", extras)
            print(" mixed fiber sizes", [(c, len(t)) for c, t in mixed])


if __name__ == "__main__":
    main()
