#!/usr/bin/env python3
"""Exact audit of the two-K4 anchor-free bridge obstruction.

The calculation is purely finite.  It checks the full-matching sector
decomposition, exhausts all 2^9 aggregate bridge supports, and verifies the
rank-one endpoint-line propagation used in the accompanying proof.
"""

from __future__ import annotations

import itertools


COLORS = tuple(range(3))
LEFT_ANCHOR = 0
LEFT = (1, 2, 3)
RIGHT_ANCHOR = 4
RIGHT = (5, 6, 7)


def canonical(edge):
    return tuple(sorted(edge))


def perfect_matchings(vertices, support):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        edge = canonical((first, second))
        if edge not in support:
            continue
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest, support):
            yield tuple(sorted((edge,) + tail))


def internal_edges(anchor, sites):
    answer = set()
    for color in COLORS:
        answer.add(canonical((anchor, sites[color])))
        other = [sites[index] for index in COLORS if index != color]
        answer.add(canonical(other))
    return answer


def audit_matching_sectors():
    left_internal = internal_edges(LEFT_ANCHOR, LEFT)
    right_internal = internal_edges(RIGHT_ANCHOR, RIGHT)
    bridges = {canonical((u, v)) for u in LEFT for v in RIGHT}
    support = left_internal | right_internal | bridges
    matchings = tuple(perfect_matchings(range(8), support))
    assert len(matchings) == 27

    counts = {0: 0, 2: 0}
    signatures = {(r, s): 0 for r in COLORS for s in COLORS}
    for matching in matchings:
        cross = tuple(edge for edge in matching if edge in bridges)
        assert len(cross) in counts
        counts[len(cross)] += 1
        if not cross:
            continue

        left_anchor_edge = next(edge for edge in matching if LEFT_ANCHOR in edge)
        right_anchor_edge = next(edge for edge in matching if RIGHT_ANCHOR in edge)
        left_mate = next(v for v in left_anchor_edge if v != LEFT_ANCHOR)
        right_mate = next(v for v in right_anchor_edge if v != RIGHT_ANCHOR)
        r = LEFT.index(left_mate)
        s = RIGHT.index(right_mate)
        signatures[r, s] += 1

        assert {u for edge in cross for u in edge if u in LEFT} == {
            LEFT[index] for index in COLORS if index != r
        }
        assert {u for edge in cross for u in edge if u in RIGHT} == {
            RIGHT[index] for index in COLORS if index != s
        }

    assert counts == {0: 9, 2: 18}
    assert set(signatures.values()) == {2}

    # Adding the central anchor edge gives 15 more matchings.  Each of them
    # contains that edge, so all 15 are confined to whichever anchor-color
    # coordinates its tensor supports.
    central = canonical((LEFT_ANCHOR, RIGHT_ANCHOR))
    enlarged = tuple(perfect_matchings(range(8), support | {central}))
    using_central = [matching for matching in enlarged if central in matching]
    assert len(enlarged) == 42
    assert len(using_central) == 15


def complementary_matching_bits(mask, deleted_left, deleted_right):
    rows = [i for i in COLORS if i != deleted_left]
    columns = [j for j in COLORS if j != deleted_right]

    def active(i, j):
        return bool(mask & (1 << (3 * i + j)))

    return (
        active(rows[0], columns[0]) and active(rows[1], columns[1]),
        active(rows[0], columns[1]) and active(rows[1], columns[0]),
    )


def audit_support_lemma():
    survivors = []
    for mask in range(1 << 9):
        valid = True
        for r, s in itertools.product(COLORS, repeat=2):
            first, second = complementary_matching_bits(mask, r, s)
            if r == s:
                valid &= first == second
            else:
                valid &= first or second
        if valid:
            survivors.append(mask)
    assert survivors == [(1 << 9) - 1]


class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, item):
        self.parent.setdefault(item, item)
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, first, second):
        first = self.find(first)
        second = self.find(second)
        if first != second:
            self.parent[second] = first


def audit_line_propagation_and_conflict():
    lines = UnionFind()
    # Incidence line tokens are (shore, physical vertex, opposite vertex).
    # Each diagonal complementary square identifies the two incidences at
    # each of its four corners.
    for deleted in COLORS:
        rows = [i for i in COLORS if i != deleted]
        columns = [j for j in COLORS if j != deleted]
        for i in rows:
            lines.union(("L", i, columns[0]), ("L", i, columns[1]))
        for j in columns:
            lines.union(("R", j, rows[0]), ("R", j, rows[1]))

    for i in COLORS:
        assert len({lines.find(("L", i, j)) for j in COLORS}) == 1
    for j in COLORS:
        assert len({lines.find(("R", j, i)) for i in COLORS}) == 1

    # Every off-diagonal signature (r,s) requires the common line at each
    # surviving left vertex i != r to be the coordinate line e_r.
    requirements = {i: set() for i in COLORS}
    for r, s in itertools.product(COLORS, repeat=2):
        if r == s:
            continue
        for i in COLORS:
            if i != r:
                requirements[i].add(r)
    assert requirements == {0: {1, 2}, 1: {0, 2}, 2: {0, 1}}
    assert all(len(colors) == 2 for colors in requirements.values())


def matching_data(mask, deleted_left, deleted_right):
    rows = [i for i in COLORS if i != deleted_left]
    columns = [j for j in COLORS if j != deleted_right]

    def active(edge):
        i, j = edge
        return bool(mask & (1 << (3 * i + j)))

    matchings = (
        ((rows[0], columns[0]), (rows[1], columns[1])),
        ((rows[0], columns[1]), (rows[1], columns[0])),
    )
    bits = tuple(all(active(edge) for edge in matching) for matching in matchings)
    return rows, columns, matchings, bits


def untouched_slice_line_conflict(omitted, mask):
    """Return ``(support_valid, forced_line_conflict)`` exactly."""
    data = {}
    valid = True
    for r, s in itertools.product(COLORS, repeat=2):
        if (r, s) in omitted:
            continue
        datum = matching_data(mask, r, s)
        data[r, s] = datum
        bits = datum[3]
        valid &= bits[0] == bits[1] if r == s else any(bits)
    if not valid:
        return False, False

    lines = UnionFind()
    rank_one = set()
    labels = {}

    def add_label(token, color):
        labels.setdefault(lines.find(token), set()).add(color)

    # First promote every supported diagonal zero square.
    for (r, s), (rows, columns, matchings, bits) in data.items():
        if r != s or bits != (True, True):
            continue
        rank_one.update(matchings[0] + matchings[1])
        for i in rows:
            lines.union(("L", i, columns[0]), ("L", i, columns[1]))
        for j in columns:
            lines.union(("R", j, rows[0]), ("R", j, rows[1]))

    # A unique nonzero pure term promotes and labels both its edges.
    for (r, s), (_rows, _columns, matchings, bits) in data.items():
        if r == s or sum(bits) != 1:
            continue
        matching = matchings[bits.index(True)]
        rank_one.update(matching)
        for i, j in matching:
            add_label(("L", i, j), r)
            add_label(("R", j, i), s)

    # If both terms occur but a vertex already has one common rank-one
    # incidence line, the pure output labels that line.
    for (r, s), (rows, columns, _matchings, bits) in data.items():
        if r == s or bits != (True, True):
            continue
        for i in rows:
            tokens = [("L", i, j) for j in columns]
            if (
                all((i, j) in rank_one for j in columns)
                and lines.find(tokens[0]) == lines.find(tokens[1])
            ):
                add_label(tokens[0], r)
        for j in columns:
            tokens = [("R", j, i) for i in rows]
            if (
                all((i, j) in rank_one for i in rows)
                and lines.find(tokens[0]) == lines.find(tokens[1])
            ):
                add_label(tokens[0], s)

    # Union operations preceded all labels, so roots are stable.
    return True, any(len(colors) > 1 for colors in labels.values())


def audit_sparse_central_cells():
    """Audit one cell and, more broadly, one coordinate row or column."""

    expected_masks = {
        (0, 0): {
            sum(1 << (3 * i + j) for i, j in itertools.product(COLORS, repeat=2)
                if (i, j) not in {(1, 2), (2, 1)}),
            ((1 << 9) - 1) ^ (1 << (3 * 2 + 1)),
            ((1 << 9) - 1) ^ (1 << (3 * 1 + 2)),
            (1 << 9) - 1,
        },
        (0, 1): {
            sum(1 << (3 * i + j)
                for i, j in {(0, 0), (0, 1), (0, 2),
                             (1, 0), (1, 1), (2, 1)}),
            (1 << 9) - 1,
        },
    }

    for omitted_cell in ((0, 0), (0, 1)):
        omitted = {omitted_cell}
        survivors = []
        for mask in range(1 << 9):
            valid, conflict = untouched_slice_line_conflict(omitted, mask)
            if not valid:
                continue
            survivors.append(mask)
            assert conflict, (omitted_cell, mask)

        assert set(survivors) == expected_masks[omitted_cell]

    # If the central aggregate tensor is supported in one coordinate row
    # e_p tensor V, or one coordinate column V tensor e_q, only those anchor
    # slices are contaminated.  The untouched equations alone still close
    # every possible bridge support by the same implications.
    audited_central_masks = set()
    for central_mask in range(1 << 9):
        support = {
            (i, j)
            for i, j in itertools.product(COLORS, repeat=2)
            if central_mask & (1 << (3 * i + j))
        }
        active_rows = {i for i, _ in support}
        active_columns = {j for _, j in support}
        if len(active_rows) > 1 and len(active_columns) > 1:
            continue
        audited_central_masks.add(central_mask)
        assert all(
            (lambda result: not result[0] or result[1])(
                untouched_slice_line_conflict(support, bridge_mask)
            )
            for bridge_mask in range(1 << 9)
        )
    assert len(audited_central_masks) == 34  # empty plus 33 nonempty masks


def main():
    audit_matching_sectors()
    audit_support_lemma()
    audit_line_propagation_and_conflict()
    audit_sparse_central_cells()
    print("full matchings: 27 anchor-free; 42 with the central anchor edge")
    print("bridge support truth table: unique survivor is all nine edges")
    print("three zero squares force one incidence line at every endpoint")
    print("off-diagonal signatures force two distinct colors on each left line")
    print("central support in one coordinate row/column: all 34 masks conflict")
    print("verified two-K4 anchor-free bridge obstruction")


if __name__ == "__main__":
    main()
