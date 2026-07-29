#!/usr/bin/env python3
"""Exact obstruction to adding a third active module to the best overlap.

Fix the best {0,1}/{0,2} placement from binary-restriction-route.md and add
one {1,2} copy of the active rank-two gadget in any of its 6! vertex
placements.  All module cells have arbitrary nonzero coefficients; any
coincident aggregate cell may cancel to zero.  Exhaustive support-fiber
analysis shows that every pattern retaining all three constant coefficients
has a mixed coloring with exactly one nonzero matching term.
"""

from __future__ import annotations

import collections
import itertools


N = 6
VERTICES = tuple(range(N))
BASE_CELLS = {
    (0, 1): {(0, 0)},
    (2, 3): {(0, 0), (1, 1)},
    (0, 2): {(0, 1)},
    (1, 3): {(0, 1)},
    (4, 5): {(0, 0)},
    (0, 5): {(1, 1)},
    (1, 2): {(1, 1)},
    (3, 4): {(1, 1)},
}


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for pos in range(1, len(vertices)):
        v = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1 :]
        for matching in perfect_matchings(rest):
            yield ((u, v),) + matching


PM = tuple(perfect_matchings(VERTICES))
MIXED_COLORINGS = tuple(
    coloring
    for coloring in itertools.product(range(3), repeat=N)
    if len(set(coloring)) > 1
)


def embedded_cells(permutation, color_map, origin):
    answer = collections.defaultdict(list)
    for (u, v), cells in BASE_CELLS.items():
        x, y = permutation[u], permutation[v]
        swap = x > y
        edge = (min(x, y), max(x, y))
        for a, b in cells:
            aa, bb = color_map[a], color_map[b]
            if swap:
                aa, bb = bb, aa
            answer[(edge, aa, bb)].append(origin)
    return answer


def merge_origins(*modules):
    answer = collections.defaultdict(list)
    for module in modules:
        for key, values in module.items():
            answer[key].extend(values)
    return answer


def matching_nonzero(matching, coloring, origins, nonzero):
    for edge in matching:
        u, v = edge
        cell = (edge, coloring[u], coloring[v])
        if cell not in origins or not nonzero[cell]:
            return False
    return True


def matching_count(coloring, origins, nonzero):
    return sum(
        matching_nonzero(matching, coloring, origins, nonzero)
        for matching in PM
    )


def main():
    first = embedded_cells(VERTICES, (0, 1), "01")
    second = embedded_cells((0, 1, 2, 3, 5, 4), (0, 2), "02")

    placements = 0
    patterns = 0
    max_shared = 0
    for permutation in itertools.permutations(VERTICES):
        third = embedded_cells(permutation, (1, 2), "12")
        origins = merge_origins(first, second, third)
        shared = tuple(key for key, values in origins.items() if len(values) > 1)
        shared_index = {key: index for index, key in enumerate(shared)}
        max_shared = max(max_shared, len(shared))
        placements += 1

        for mask in range(1 << len(shared)):
            patterns += 1
            nonzero = {
                key: len(values) == 1
                or bool(mask & (1 << shared_index[key]))
                for key, values in origins.items()
            }
            if any(
                matching_count((color,) * N, origins, nonzero) == 0
                for color in range(3)
            ):
                continue
            assert any(
                matching_count(coloring, origins, nonzero) == 1
                for coloring in MIXED_COLORINGS
            ), (permutation, mask)

    assert placements == 720
    print(f"verified third-module placements={placements}")
    print(f"audited coincident-cell patterns={patterns}")
    print(f"maximum coincident aggregate cells={max_shared}")
    print("every constant-compatible pattern forces a unique mixed term")


if __name__ == "__main__":
    main()
