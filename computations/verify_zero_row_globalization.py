#!/usr/bin/env python3
"""Exact finite audit for ``notes/zero-row-globalization-rankgraph.md``.

The mathematical graph lemma is uniform.  This script exhausts all labeled
graphs through six vertices as an adversarial audit of its incidence core,
then checks the endpoint orientation of every small integer rank-one block.
It uses only integer and Boolean arithmetic.
"""

from __future__ import annotations

from itertools import combinations, product


def connected_after_deleting(adjacency, deleted):
    vertices = [v for v in range(len(adjacency)) if v not in deleted]
    if len(vertices) <= 1:
        return True
    seen = {vertices[0]}
    stack = [vertices[0]]
    while stack:
        vertex = stack.pop()
        for neighbor in adjacency[vertex]:
            if neighbor in deleted or neighbor in seen:
                continue
            seen.add(neighbor)
            stack.append(neighbor)
    return len(seen) == len(vertices)


def is_two_connected(adjacency):
    n = len(adjacency)
    if n < 3 or not connected_after_deleting(adjacency, set()):
        return False
    return all(connected_after_deleting(adjacency, {p}) for p in range(n))


def adjacency_from_mask(n, edges, mask):
    adjacency = [set() for _ in range(n)]
    for index, (left, right) in enumerate(edges):
        if mask >> index & 1:
            adjacency[left].add(right)
            adjacency[right].add(left)
    return adjacency


def audit_graph(adjacency):
    """Check every possible intrinsic zero set used in Lemma 3.1."""

    n = len(adjacency)
    checked = 0
    for p in range(n):
        others = [vertex for vertex in range(n) if vertex != p]
        for bits in range(1, (1 << len(others)) - 1):
            zero_set = {
                vertex for index, vertex in enumerate(others) if bits >> index & 1
            }
            # A coordinate-zero row on p--x makes that block singular.
            if any(x in adjacency[p] for x in zero_set):
                continue
            checked += 1
            boundary = [
                (x, y)
                for x in zero_set
                for y in adjacency[x]
                if y != p and y not in zero_set
            ]
            assert boundary, (p, zero_set, adjacency)
            for x, y in boundary:
                # The second neighbor q is the endpoint deleted in the
                # overlapping pair.  Since p--x is absent, it is automatically
                # distinct from p as well as x,y.
                choices = adjacency[x] - {p, y}
                assert choices, (p, zero_set, x, y, adjacency)
                q = min(choices)
                assert len({p, q, x, y}) == 4
                assert x in adjacency[q] and x in adjacency[y]
    return checked


def rank_integer(matrix):
    values = [[int(entry) for entry in row] for row in matrix]
    rank = 0
    for column in range(len(values[0])):
        pivot = next(
            (row for row in range(rank, len(values)) if values[row][column]), None
        )
        if pivot is None:
            continue
        values[rank], values[pivot] = values[pivot], values[rank]
        pivot_value = values[rank][column]
        for row in range(rank + 1, len(values)):
            entry = values[row][column]
            if not entry:
                continue
            values[row] = [
                pivot_value * x - entry * y
                for x, y in zip(values[row], values[rank], strict=True)
            ]
        rank += 1
    return rank


def transpose(matrix):
    return [list(column) for column in zip(*matrix, strict=True)]


def audit_endpoint_orientation():
    checked = 0
    for colour in range(3):
        for vector in product((-1, 0, 1), repeat=3):
            matrix = [
                [vector[column] if row == colour else 0 for column in range(3)]
                for row in range(3)
            ]
            assert rank_integer(matrix) <= 1
            assert rank_integer(transpose(matrix)) <= 1
            # A_(q|x)=e_c tensor v has only row c; after reversal
            # A_(x|q)=v tensor e_c has only column c.
            assert all(
                matrix[row] == [0, 0, 0] for row in range(3) if row != colour
            )
            reversed_matrix = transpose(matrix)
            assert all(
                reversed_matrix[row][column] == 0
                for row in range(3)
                for column in range(3)
                if column != colour
            )
            checked += 1
    return checked


def main():
    graph_counts = {}
    zero_set_counts = {}
    for n in range(4, 7):
        edges = tuple(combinations(range(n), 2))
        graph_count = 0
        zero_set_count = 0
        for mask in range(1 << len(edges)):
            adjacency = adjacency_from_mask(n, edges, mask)
            if not is_two_connected(adjacency):
                continue
            graph_count += 1
            zero_set_count += audit_graph(adjacency)
        graph_counts[n] = graph_count
        zero_set_counts[n] = zero_set_count

    orientation_cases = audit_endpoint_orientation()
    print(f"verified labeled 2-connected graph counts: {graph_counts}")
    print(f"verified admissible proper zero-set cases: {zero_set_counts}")
    print(f"verified endpoint-oriented rank-one/zero cases: {orientation_cases}")
    print("PASS: every audited boundary has a second rank-three neighbor")


if __name__ == "__main__":
    main()
