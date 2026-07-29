#!/usr/bin/env python3
"""Exact audit of the clean near-perfect pair-cap obstruction at n=8.

On six internal sites let q consist of two nonzero pure ``cc`` cells for
each colour c, forming a perfect matching after omission of an edge e_c.
The core is *clean* when none of the three omitted physical edges occurs
among any of the six q-edges.  For unit coefficients this script checks:

* there are 43,245 ordered clean cores;
* 36,045 have connected omitted-edge multigraph;
* the remaining 7,200 cores have six S_6 x S_3 support orbits;
* three orbit representatives have explicit two-word left functionals
  which annihilate H_q(Z)=Zq^2/2 but not X_0; and
* singleton rows in the other three representatives give the target and
  zero incidences used by the crossed-target proof.

Only support and nonvanishing are used in the proof, so arbitrary nonzero
weights on the six displayed q-cells are covered after rescaling the
two-word functionals.  No floating-point arithmetic is used here.
"""

from __future__ import annotations

import itertools
from collections import Counter, defaultdict


VERTICES = tuple(range(6))
COLORS = tuple(range(3))
EDGES = tuple(itertools.combinations(VERTICES, 2))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remainder):
            yield ((first, second),) + tail


CHOICES = tuple(
    (missing, tuple(sorted(matching)))
    for missing in EDGES
    for matching in perfect_matchings(
        vertex for vertex in VERTICES if vertex not in missing
    )
)


# Canonical representatives of the six disconnected clean support orbits.
# Each colour record is (omitted edge, matching on its four other sites).
REPRESENTATIVES = (
    (
        ((0, 1), ((2, 3), (4, 5))),
        ((0, 1), ((2, 3), (4, 5))),
        ((2, 4), ((0, 3), (1, 5))),
    ),
    (
        ((0, 1), ((2, 3), (4, 5))),
        ((0, 1), ((2, 4), (3, 5))),
        ((2, 5), ((0, 3), (1, 4))),
    ),
    (
        ((0, 1), ((2, 3), (4, 5))),
        ((0, 2), ((1, 3), (4, 5))),
        ((3, 4), ((0, 5), (1, 2))),
    ),
    (
        ((0, 1), ((2, 3), (4, 5))),
        ((0, 2), ((1, 4), (3, 5))),
        ((3, 4), ((0, 5), (1, 2))),
    ),
    (
        ((0, 1), ((2, 3), (4, 5))),
        ((2, 4), ((0, 3), (1, 5))),
        ((3, 5), ((0, 2), (1, 4))),
    ),
    (
        ((0, 1), ((2, 3), (4, 5))),
        ((2, 4), ((0, 3), (1, 5))),
        ((3, 5), ((0, 4), (1, 2))),
    ),
)


def is_clean(core):
    omitted = {record[0] for record in core}
    support = {edge for record in core for edge in record[1]}
    return omitted.isdisjoint(support)


def omitted_graph_connected(core):
    edges = tuple(record[0] for record in core)
    vertices = set().union(*(set(edge) for edge in edges))
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    pending = [next(iter(vertices))]
    seen = set()
    while pending:
        vertex = pending.pop()
        if vertex in seen:
            continue
        seen.add(vertex)
        pending.extend(adjacency[vertex] - seen)
    return seen == vertices


def degree_partition(core):
    edges = tuple(record[0] for record in core)
    vertices = set().union(*(set(edge) for edge in edges))
    return tuple(
        sorted(
            (sum(vertex in edge for edge in edges) for vertex in vertices),
            reverse=True,
        )
    )


PERMUTATIONS = tuple(itertools.permutations(VERTICES))


def permute_edge(edge, permutation):
    return tuple(sorted((permutation[edge[0]], permutation[edge[1]])))


def canonical_support(core):
    """Canonicalize under site permutations and simultaneous colour relabeling."""
    best = None
    for permutation in PERMUTATIONS:
        records = tuple(
            sorted(
                (
                    permute_edge(missing, permutation),
                    tuple(
                        sorted(permute_edge(edge, permutation) for edge in matching)
                    ),
                )
                for missing, matching in core
            )
        )
        if best is None or records < best:
            best = records
    return best


def enumerate_clean_cores():
    clean = []
    connected_shapes = Counter()
    for core in itertools.product(CHOICES, repeat=3):
        if not is_clean(core):
            continue
        clean.append(core)
        if omitted_graph_connected(core):
            connected_shapes[degree_partition(core)] += 1

    assert len(clean) == 43_245
    assert sum(connected_shapes.values()) == 36_045
    assert connected_shapes == {
        (2, 2, 1, 1): 12_960,  # three-edge path
        (2, 2, 2): 3_240,  # triangle
        (3, 1, 1, 1): 9_720,  # three-edge star
        (3, 2, 1): 9_720,  # a parallel pair and an adjacent edge
        (3, 3): 405,  # three parallel edges
    }

    disconnected = [core for core in clean if not omitted_graph_connected(core)]
    assert len(disconnected) == 7_200
    orbit_counts = Counter(canonical_support(core) for core in disconnected)
    expected = {
        canonical_support(representative): size
        for representative, size in zip(
            REPRESENTATIVES,
            (1_080, 1_080, 2_160, 2_160, 360, 360),
            strict=True,
        )
    }
    assert orbit_counts == expected


def q_cells(core):
    return tuple(
        (edge, colour, colour)
        for colour, (_missing, matching) in enumerate(core)
        for edge in matching
    )


def hessian_rows(core):
    """Sparse integer rows of H_q(Z)=Zq^2/2 for unit q coefficients."""
    cells = q_cells(core)
    rows = defaultdict(lambda: defaultdict(int))
    for left, right in itertools.combinations(cells, 2):
        left_edge, left_a, left_b = left
        right_edge, right_a, right_b = right
        if set(left_edge) & set(right_edge):
            continue
        remaining = tuple(
            sorted(set(VERTICES) - set(left_edge) - set(right_edge))
        )
        assert len(remaining) == 2
        for a, b in itertools.product(COLORS, repeat=2):
            coloring = [None] * 6
            coloring[left_edge[0]] = left_a
            coloring[left_edge[1]] = left_b
            coloring[right_edge[0]] = right_a
            coloring[right_edge[1]] = right_b
            coloring[remaining[0]] = a
            coloring[remaining[1]] = b
            z_cell = (remaining, a, b)
            rows[tuple(coloring)][z_cell] += 1
    return {coloring: dict(row) for coloring, row in rows.items()}


def audit_left_functional(core, functional):
    rows = hessian_rows(core)
    column_values = defaultdict(int)
    for coloring, coefficient in functional.items():
        for cell, value in rows.get(coloring, {}).items():
            column_values[cell] += coefficient * value
    assert all(value == 0 for value in column_values.values())
    assert functional.get((0,) * 6, 0) == 1


def special_labels(core):
    return tuple(
        (site, colour)
        for colour, (missing, _matching) in enumerate(core)
        for site in missing
    )


def oriented_cell(left, right):
    left_site, left_color = left
    right_site, right_color = right
    assert left_site != right_site
    if left_site < right_site:
        return ((left_site, right_site), left_color, right_color)
    return ((right_site, left_site), right_color, left_color)


def singleton_rows_for_cell(rows, cell):
    return tuple(
        coloring
        for coloring, row in rows.items()
        if row == {cell: 1}
    )


def audit_target_and_zero_relations(core, zero_pairs):
    rows = hessian_rows(core)
    labels = special_labels(core)
    support = set(q_cells(core))

    for colour in COLORS:
        pair = (2 * colour, 2 * colour + 1)
        cell = oriented_cell(labels[pair[0]], labels[pair[1]])
        assert cell not in support
        assert (colour,) * 6 in singleton_rows_for_cell(rows, cell)

    for left_index, right_index in zero_pairs:
        cell = oriented_cell(labels[left_index], labels[right_index])
        assert cell not in support
        witnesses = singleton_rows_for_cell(rows, cell)
        assert any(coloring not in {(c,) * 6 for c in COLORS} for coloring in witnesses)


def crossed_pattern_is_inconsistent(zero_pairs):
    """After two crossed-target lemmas all six points are pure.

    A target edge joins opposite pure types and a zero edge joins equal
    pure types.  Enumerating the 64 type assignments is an exact audit of
    the final parity contradiction.
    """
    target_pairs = {(0, 1), (2, 3), (4, 5)}
    zero_pairs = {tuple(sorted(pair)) for pair in zero_pairs}
    for assignment in itertools.product((0, 1), repeat=6):
        targets_hold = all(assignment[i] != assignment[j] for i, j in target_pairs)
        zeros_hold = all(assignment[i] == assignment[j] for i, j in zero_pairs)
        if targets_hold and zeros_hold:
            return False
    return True


def audit_disconnected_certificates():
    # The first three representatives have two-word left-kernel witnesses.
    # Their coefficients are all one here; with arbitrary nonzero q-cell
    # weights the two coefficients are rescaled by the corresponding two
    # nonzero matching products.
    left_functionals = (
        {(0, 0, 0, 0, 0, 0): 1, (0, 0, 0, 0, 1, 1): -1},
        {(0, 0, 0, 0, 0, 0): 1, (0, 0, 1, 1, 1, 1): -1},
        {(0, 0, 0, 0, 0, 0): 1, (0, 0, 0, 0, 1, 1): -1},
    )
    for core, functional in zip(
        REPRESENTATIVES[:3], left_functionals, strict=True
    ):
        audit_left_functional(core, functional)

    # Labels 2c,2c+1 are the two special endpoints of omitted edge e_c.
    # Each list contains two crossed pairs for targets 0--1, two crossed
    # pairs for targets 0--2, and at least one final incompatible bridge.
    zero_patterns = (
        {
            (0, 3), (1, 2),
            (0, 4), (1, 5),
            (2, 4),
        },
        {
            (0, 3), (1, 2),
            (0, 5), (1, 4),
            (2, 5),
        },
        {
            (0, 3), (1, 2),
            (0, 4), (1, 5),
            (2, 4),
        },
    )
    for core, zero_pairs in zip(
        REPRESENTATIVES[3:], zero_patterns, strict=True
    ):
        audit_target_and_zero_relations(core, zero_pairs)
        assert crossed_pattern_is_inconsistent(zero_pairs)


def main():
    enumerate_clean_cores()
    audit_disconnected_certificates()
    print("clean near-perfect six-site cores: 43,245 exact")
    print("connected omitted-edge cores: 36,045 (uniform edge-table obstruction)")
    print("disconnected cores: 7,200 in six exact S6 x S3 orbits")
    print("three image witnesses and three singleton crossed-target audits: PASS")


if __name__ == "__main__":
    main()
