#!/usr/bin/env python3
"""Classify generic four-site augmented first-jet ranks by support graph.

This is an exact finite-field discovery script.  Each present physical edge
gets a deterministic invertible 3-by-3 matrix over GF(P).  For every one of
the 64 support graphs on four labelled sites it computes

    J_q : C + direct_sum_{ab} V_a tensor V_b -> tensor_a V_a,
          (lambda, Z) |-> lambda H_4(q) + DH_4(q)[Z],

where perturbations Z are allowed on all six cells, including absent cells.
It also computes the dimension of the displayed vertex-gauge image.
"""

from itertools import combinations, product


P = 1_000_003
VERTICES = tuple(range(4))
EDGES = tuple(combinations(VERTICES, 2))
WORDS = tuple(product(range(3), repeat=4))
WORD_INDEX = {word: index for index, word in enumerate(WORDS)}


def inv_mod(a):
    return pow(a % P, P - 2, P)


def rank_mod(columns):
    if not columns:
        return 0
    rows = len(columns[0])
    matrix = [[columns[col][row] % P for col in range(len(columns))]
              for row in range(rows)]
    rank = 0
    for col in range(len(columns)):
        pivot = next((row for row in range(rank, rows)
                      if matrix[row][col]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = inv_mod(matrix[rank][col])
        matrix[rank] = [(value * scale) % P for value in matrix[rank]]
        for row in range(rows):
            if row == rank or not matrix[row][col]:
                continue
            scale = matrix[row][col]
            matrix[row] = [
                (left - scale * right) % P
                for left, right in zip(matrix[row], matrix[rank])
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def determinant(matrix):
    a = [list(row) for row in matrix]
    out = 1
    for col in range(3):
        pivot = next((row for row in range(col, 3) if a[row][col] % P), None)
        if pivot is None:
            return 0
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            out = -out
        out = out * a[col][col] % P
        scale = inv_mod(a[col][col])
        for row in range(col + 1, 3):
            factor = a[row][col] * scale % P
            for k in range(col, 3):
                a[row][k] = (a[row][k] - factor * a[col][k]) % P
    return out % P


def edge_matrices():
    matrices = {}
    for edge_index, edge in enumerate(EDGES):
        seed = 19 + 37 * edge_index
        matrix = tuple(tuple(
            (seed + 11 * i + 17 * j + 7 * i * j + 3 * i * i + j * j) % P
            for j in range(3)) for i in range(3))
        # Add a diagonal offset until the deterministic block is invertible.
        offset = 0
        while determinant(tuple(tuple(
                (matrix[i][j] + (offset if i == j else 0)) % P
                for j in range(3)) for i in range(3))) == 0:
            offset += 1
        matrices[edge] = tuple(tuple(
            (matrix[i][j] + (offset if i == j else 0)) % P
            for j in range(3)) for i in range(3))
    return matrices


MATRICES = edge_matrices()


def edge_value(blocks, edge, colors):
    u, v = edge
    matrix = blocks.get(edge)
    return 0 if matrix is None else matrix[colors[u]][colors[v]]


def h4_column(blocks):
    matchings = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
    return [sum(edge_value(blocks, first, word)
                * edge_value(blocks, second, word)
                for first, second in matchings) % P
            for word in WORDS]


def derivative_column(blocks, varied_edge, i, j):
    complement = tuple(vertex for vertex in VERTICES if vertex not in varied_edge)
    complement_edge = tuple(sorted(complement))
    out = [0] * len(WORDS)
    u, v = varied_edge
    for word in WORDS:
        if word[u] == i and word[v] == j:
            out[WORD_INDEX[word]] = edge_value(blocks, complement_edge, word)
    return out


def gauge_columns(blocks):
    h4 = h4_column(blocks)
    columns = []
    for vertex in VERTICES:
        column = [(-value) % P for value in h4]
        for edge in EDGES:
            u, v = edge
            coefficient = int(vertex == u) + int(vertex == v)
            if not coefficient:
                continue
            complement = tuple(x for x in VERTICES if x not in edge)
            complement_edge = tuple(sorted(complement))
            for word in WORDS:
                column[WORD_INDEX[word]] = (
                    column[WORD_INDEX[word]]
                    + coefficient * edge_value(blocks, edge, word)
                    * edge_value(blocks, complement_edge, word)
                ) % P
        columns.append(column)
    # These are images under J and should be zero; instead return parameter
    # tuple columns in C + six 3x3 cells to measure the gauge subspace itself.
    parameter_columns = []
    for vertex in VERTICES:
        column = [P - 1] + [0] * 54
        for edge_index, edge in enumerate(EDGES):
            if vertex not in edge or edge not in blocks:
                continue
            matrix = blocks[edge]
            for i in range(3):
                for j in range(3):
                    column[1 + 9 * edge_index + 3 * i + j] = matrix[i][j]
        parameter_columns.append(column)
    assert all(not any(column) for column in columns)
    return parameter_columns


def graph_properties(mask):
    edges = [edge for index, edge in enumerate(EDGES) if mask >> index & 1]
    adjacency = {vertex: set() for vertex in VERTICES}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    active = {vertex for edge in edges for vertex in edge}
    connected = False
    bipartite = True
    if active:
        seen = set()
        colors = {}
        components = 0
        for root in active:
            if root in seen:
                continue
            components += 1
            colors[root] = 0
            stack = [root]
            seen.add(root)
            while stack:
                u = stack.pop()
                for v in adjacency[u]:
                    if v not in seen:
                        seen.add(v)
                        colors[v] = 1 - colors[u]
                        stack.append(v)
                    elif colors[v] == colors[u]:
                        bipartite = False
        connected = components == 1 and len(active) == 4
    return len(edges), connected, bipartite


def main():
    summaries = {}
    for mask in range(1 << len(EDGES)):
        blocks = {edge: MATRICES[edge] for index, edge in enumerate(EDGES)
                  if mask >> index & 1}
        columns = [h4_column(blocks)]
        columns.extend(derivative_column(blocks, edge, i, j)
                       for edge in EDGES for i in range(3) for j in range(3))
        rank = rank_mod(columns)
        kernel = 55 - rank
        gauge = rank_mod(gauge_columns(blocks))
        key = graph_properties(mask) + (kernel - gauge,)
        summaries.setdefault(key, []).append(mask)
    for key in sorted(summaries):
        edge_count, connected, bipartite, excess = key
        print(f"edges={edge_count} connected={int(connected)} "
              f"bipartite={int(bipartite)} excess={excess} "
              f"count={len(summaries[key])}")


if __name__ == "__main__":
    main()
