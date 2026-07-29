#!/usr/bin/env python3
"""Finite row-matroid audit for the exact-two singular classification."""

from __future__ import annotations

from itertools import combinations, product

import verify_two_k4_dead_slice_determinantal_boundary as dense
import verify_two_k4_rank2_three_singular_boundary as rank_two


VERTICES = tuple(range(4))
COLORS = tuple(range(3))


class UnionFind:
    def __init__(self, active):
        self.parent = {item: item for item in active}

    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, first, second):
        first, second = self.find(first), self.find(second)
        if first != second:
            self.parent[second] = first


def row_matroids(rank):
    """All zero/proportional row matroids of a 3x3 matrix of given rank."""

    if rank == 3:
        return ((frozenset(COLORS), tuple(frozenset((c,)) for c in COLORS)),)
    if rank == 2:
        answer = [
            (frozenset(COLORS), tuple(frozenset((c,)) for c in COLORS))
        ]
        for pair in combinations(COLORS, 2):
            third = next(color for color in COLORS if color not in pair)
            answer.append((
                frozenset(COLORS),
                (frozenset(pair), frozenset((third,))),
            ))
        for zero in COLORS:
            active = frozenset(color for color in COLORS if color != zero)
            answer.append((
                active,
                tuple(frozenset((color,)) for color in sorted(active)),
            ))
        return tuple(answer)
    if rank == 1:
        return tuple(
            (
                active := frozenset(
                    color for color in COLORS if mask & (1 << color)
                ),
                (active,),
            )
            for mask in range(1, 1 << len(COLORS))
        )
    if rank == 0:
        return ((frozenset(), ()),)
    raise ValueError(rank)


def status_masks(singular_matroids):
    """All realizable oriented-triangle rank-one status masks.

    ``singular_matroids`` maps a vertex to one of ``row_matroids``.  Other
    vertices have the uniform rank-three row matroid.  A selected zero row
    is omitted; rank at most one means that all remaining selected labels
    occupy one projective class.
    """

    lines = dense.dead_coordinate_lines()
    active = {
        (vertex, color)
        for vertex in VERTICES for color in COLORS
        if (
            vertex not in singular_matroids
            or color in singular_matroids[vertex][0]
        )
    }
    prescribed_groups = {
        vertex: singular_matroids[vertex][1]
        if vertex in singular_matroids
        else tuple(frozenset((color,)) for color in COLORS)
        for vertex in VERTICES
    }

    answers = set()
    for seed in range(1 << len(lines)):
        union_find = UnionFind(active)
        for vertex, groups in prescribed_groups.items():
            for group in groups:
                group = tuple(group)
                for color in group[1:]:
                    union_find.union(
                        (vertex, group[0]), (vertex, color)
                    )

        for index, (_hole, assignment) in enumerate(lines):
            if not (seed & (1 << index)):
                continue
            selected = [label for label in assignment if label in active]
            for label in selected[1:]:
                union_find.union(selected[0], label)

        # Distinct prescribed projective groups at one vertex may not merge.
        valid = True
        for vertex, groups in prescribed_groups.items():
            for first, second in combinations(groups, 2):
                if union_find.find((vertex, next(iter(first)))) == \
                        union_find.find((vertex, next(iter(second)))):
                    valid = False
        if not valid:
            continue

        actual = 0
        for index, (_hole, assignment) in enumerate(lines):
            selected = [label for label in assignment if label in active]
            if len({union_find.find(label) for label in selected}) == 1:
                actual |= 1 << index
        answers.add(actual)
    return tuple(sorted(answers))


def maximum_capacity(rank_pair):
    first_rank, second_rank = rank_pair
    return max(
        max(mask.bit_count() for mask in status_masks({0: first, 1: second}))
        for first in row_matroids(first_rank)
        for second in row_matroids(second_rank)
    )


def single_capacity(rank):
    return max(
        max(mask.bit_count() for mask in status_masks({0: matroid}))
        for matroid in row_matroids(rank)
    )


def main():
    # One exceptional block in a column.
    assert {rank: single_capacity(rank) for rank in (2, 1, 0)} == {
        2: 4, 1: 5, 0: 6
    }

    # Two exceptional blocks at different vertices of one block column.
    pair_capacities = {
        pair: maximum_capacity(pair)
        for pair in ((2, 2), (2, 1), (2, 0), (1, 1), (1, 0), (0, 0))
    }
    assert pair_capacities == {
        (2, 2): 5,
        (2, 1): 5,
        (2, 0): 6,
        (1, 1): 6,
        (1, 0): 6,
        (0, 0): 6,
    }

    maximum_zero_rows = {2: 1, 1: 2, 0: 3}
    single_capacities = {2: 4, 1: 5, 0: 6}

    # Disjoint block-row/block-column positions.  There are two entirely
    # good columns, hence base capacity eight.
    expected_disjoint = {
        (2, 2): (20, 16),
        (2, 1): (18, 17),
        (2, 0): (16, 18),
        (1, 1): (16, 18),
        (1, 0): (16, 19),
        (0, 0): (16, 20),
    }
    for pair, expected in expected_disjoint.items():
        dirty = min(8, 2 * sum(maximum_zero_rows[rank] for rank in pair))
        demand = 24 - dirty
        capacity = 8 + sum(single_capacities[rank] for rank in pair)
        assert (demand, capacity) == expected
        assert (demand > capacity) == (pair in ((2, 2), (2, 1)))

    # Aligned blocks, viewed after transposition as two exceptions in one
    # column.  The rank-22 and rank-21 cases are the only ones claimed to
    # close by this coarse count.
    expected_aligned = {(2, 2): (20, 17), (2, 1): (18, 17)}
    for pair, expected in expected_aligned.items():
        dirty = min(8, 2 * sum(maximum_zero_rows[rank] for rank in pair))
        demand = 24 - dirty
        capacity = 12 + pair_capacities[pair]
        assert (demand, capacity) == expected
        assert demand > capacity

    # The sharper correlated audit closes the coarse survivor (2,0), in
    # addition to rechecking (2,2) and (2,1), for both relative positions.
    rank_two.audit_column_capacity_bounds()
    rank_two.audit_all_two_block_configurations()

    print(
        "PASS: every exact-two rank pair containing rank2 is excluded; "
        "survivors restricted to 11/10/00"
    )


if __name__ == "__main__":
    main()
