#!/usr/bin/env python3
"""Exact obstruction to superposing two active binary GHZ modules at n=6.

One copy of the eight-edge rank-two gadget uses global colors {0,1}; a
second copy uses {0,2} after an arbitrary permutation of the six vertices.
Every displayed cell of each copy may carry an arbitrary nonzero complex
coefficient (so this includes all nonzero reweightings that preserve the
module identities).  Coincident cells from the two copies are aggregated
and may cancel exactly.

For all 6! relative placements and every possible zero/nonzero pattern of
the coincident aggregate cells, the following holds: if all three constant
colorings have at least one nonzero matching term, some mixed coloring has
exactly one nonzero matching term.  Its coefficient cannot vanish over a
field.  Thus a pure two-module superposition cannot realize Delta_(6,3),
independently of coefficient values and cancellations inside shared cells.
"""

from __future__ import annotations

import collections
import itertools


N = 6
VERTICES = tuple(range(N))

# Decorated support of computations/verify_active_ranktwo_binary_gadget.py.
# The rank-two edge 23 contributes two distinct cells.
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


def merge_origins(left, right):
    answer = collections.defaultdict(list)
    for key, origins in itertools.chain(left.items(), right.items()):
        answer[key].extend(origins)
    return answer


def matching_cells(matching, coloring, origins):
    answer = []
    for edge in matching:
        u, v = edge
        key = (edge, coloring[u], coloring[v])
        if key not in origins:
            return None
        answer.append(key)
    return tuple(answer)


def nonzero_matching_count(coloring, origins, nonzero):
    count = 0
    for matching in PM:
        cells = matching_cells(matching, coloring, origins)
        if cells is not None and all(nonzero[cell] for cell in cells):
            count += 1
    return count


def main():
    first = embedded_cells(VERTICES, (0, 1), "first")
    placements = 0
    zero_patterns = 0
    max_shared = 0
    minimum_forced_unique = len(MIXED_COLORINGS)

    for permutation in itertools.permutations(VERTICES):
        second = embedded_cells(permutation, (0, 2), "second")
        origins = merge_origins(first, second)
        shared = tuple(key for key, values in origins.items() if len(values) == 2)
        max_shared = max(max_shared, len(shared))
        placements += 1

        placement_has_admissible_pattern = False
        for mask in range(1 << len(shared)):
            zero_patterns += 1
            nonzero = {
                key: len(values) == 1
                or bool(mask & (1 << shared.index(key)))
                for key, values in origins.items()
            }

            # A nonzero constant coefficient needs at least one nonzero term.
            if any(
                nonzero_matching_count((color,) * N, origins, nonzero) == 0
                for color in range(3)
            ):
                continue
            placement_has_admissible_pattern = True

            forced_unique = sum(
                nonzero_matching_count(coloring, origins, nonzero) == 1
                for coloring in MIXED_COLORINGS
            )
            minimum_forced_unique = min(minimum_forced_unique, forced_unique)
            assert forced_unique > 0, (permutation, mask)

        # Some placements can make a constant color disappear for every
        # shared-cell cancellation pattern; those are already impossible.
        if not placement_has_admissible_pattern:
            minimum_forced_unique = min(minimum_forced_unique, 0)

    assert placements == 720
    print(f"verified all relative placements={placements}")
    print(f"audited shared-cell zero patterns={zero_patterns}")
    print(f"maximum coincident decorated cells={max_shared}")
    print("every constant-compatible pattern has a unique mixed matching term")


if __name__ == "__main__":
    main()
