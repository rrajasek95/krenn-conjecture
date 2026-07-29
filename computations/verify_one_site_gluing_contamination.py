#!/usr/bin/env python3
"""Exact audit of one-site gluing and its triangular-prism contaminant.

The checker uses only integer arithmetic.  It verifies that two canonical
four-site ternary GHZ sources contract to Delta_6 at the tensor level, while
the edgewise effective source has one additional rainbow coefficient.  It
also audits the support and source-Hessian escape data quoted in
notes/one-site-gluing-cubic-contamination.md.
"""

from __future__ import annotations

from fractions import Fraction
import itertools


COLORS = (0, 1, 2)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def edge(u, v):
    return tuple(sorted((u, v)))


def entry(matrices, u, v, a, b):
    if u < v:
        return matrices.get((u, v), {}).get((a, b), 0)
    return matrices.get((v, u), {}).get((b, a), 0)


def matching_tensor(vertices, matrices, crossing_cut=None, crossing_count=None):
    vertices = tuple(vertices)
    answer = {}
    for word in itertools.product(COLORS, repeat=len(vertices)):
        coloring = dict(zip(vertices, word, strict=True))
        value = 0
        for matching in perfect_matchings(vertices):
            if crossing_cut is not None:
                crossings = sum(
                    (u in crossing_cut) != (v in crossing_cut) for u, v in matching
                )
                if crossings != crossing_count:
                    continue
            term = 1
            for u, v in matching:
                term *= entry(matrices, u, v, coloring[u], coloring[v])
            value += term
        if value:
            answer[word] = value
    return answer


def canonical_k4(center, leaves):
    """The three one-factors of K4, with center--leaf i colored i."""
    leaves = tuple(leaves)
    matrices = {}
    for color in COLORS:
        matrices[edge(center, leaves[color])] = {(color, color): 1}
        other = [leaf for index, leaf in enumerate(leaves) if index != color]
        matrices[edge(*other)] = {(color, color): 1}
    return matrices


def contract_tensors(
    left,
    left_vertices,
    left_site,
    right,
    right_vertices,
    right_site,
    bilinear=None,
):
    """Contract two coefficient dictionaries by an exact bilinear form."""
    if bilinear is None:
        bilinear = {(color, color): 1 for color in COLORS}
    left_rest = tuple(v for v in left_vertices if v != left_site)
    right_rest = tuple(v for v in right_vertices if v != right_site)
    answer = {}
    for left_word, left_value in left.items():
        left_coloring = dict(zip(left_vertices, left_word, strict=True))
        for right_word, right_value in right.items():
            right_coloring = dict(zip(right_vertices, right_word, strict=True))
            coefficient = bilinear.get(
                (left_coloring[left_site], right_coloring[right_site]), 0
            )
            if not coefficient:
                continue
            word = tuple(left_coloring[v] for v in left_rest) + tuple(
                right_coloring[v] for v in right_rest
            )
            answer[word] = (
                answer.get(word, 0) + coefficient * left_value * right_value
            )
    return {word: value for word, value in answer.items() if value}


def dense_test_matrix(u, v, salt):
    """A deterministic, nonsymmetric, off-diagonal integer aggregate block."""
    return {
        (a, b): (salt + 2 * u + 3 * v + 5 * a - 7 * b + 11 * a * b)
        for a in COLORS
        for b in COLORS
    }


def effective_cross(left_block, bilinear, right_block):
    """Coordinate formula C=A^T K B with distinguished-site rows."""
    return {
        (i, j): sum(
            left_block[a, i] * bilinear[a, b] * right_block[b, j]
            for a in COLORS
            for b in COLORS
        )
        for i in COLORS
        for j in COLORS
    }


def audit_arbitrary_covector_formula():
    left_vertices = (0, 1, 2, 3)
    right_vertices = (4, 5, 6, 7)
    left = {
        edge(u, v): dense_test_matrix(u, v, 13)
        for u, v in itertools.combinations(left_vertices, 2)
    }
    right = {
        edge(u, v): dense_test_matrix(u, v, -19)
        for u, v in itertools.combinations(right_vertices, 2)
    }
    bilinear = {
        (a, b): 2 - 3 * a + 5 * b + 7 * a * b for a in COLORS for b in COLORS
    }

    left_tensor = matching_tensor(left_vertices, left)
    right_tensor = matching_tensor(right_vertices, right)
    contracted = contract_tensors(
        left_tensor,
        left_vertices,
        0,
        right_tensor,
        right_vertices,
        4,
        bilinear,
    )

    surviving = (1, 2, 3, 5, 6, 7)
    combined = {
        pair: matrix
        for source in (left, right)
        for pair, matrix in source.items()
        if 0 not in pair and 4 not in pair
    }
    for x in (1, 2, 3):
        for y in (5, 6, 7):
            combined[edge(x, y)] = effective_cross(
                left[edge(0, x)], bilinear, right[edge(4, y)]
            )
    one_cross = matching_tensor(
        surviving, combined, crossing_cut={1, 2, 3}, crossing_count=1
    )
    assert contracted == one_cross


def connected_after_deleting(adjacency, deleted):
    remaining = set(adjacency) - set(deleted)
    if not remaining:
        return True
    first = next(iter(remaining))
    seen = {first}
    stack = [first]
    while stack:
        vertex = stack.pop()
        for neighbor in adjacency[vertex] - set(deleted):
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return seen == remaining


def rational_rank(rows):
    matrix = [[Fraction(value) for value in row] for row in rows]
    if not matrix:
        return 0
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [value / pivot_value for value in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiplier = matrix[row][column]
            matrix[row] = [
                value - multiplier * pivot_value
                for value, pivot_value in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def four_site_source_hessian_rank(vertices, matrices):
    """Rank of Z -> Zq on arbitrary edge-block perturbations over Q."""
    vertices = tuple(vertices)
    pairs = tuple(itertools.combinations(vertices, 2))
    columns = tuple((pair, a, b) for pair in pairs for a in COLORS for b in COLORS)
    words = tuple(itertools.product(COLORS, repeat=4))
    word_index = {word: index for index, word in enumerate(words)}
    rows = [[0 for _ in columns] for _ in words]
    for column, (pair, a, b) in enumerate(columns):
        u, v = pair
        complement = tuple(vertex for vertex in vertices if vertex not in pair)
        x, y = complement
        complement_matrix = matrices.get(edge(x, y), {})
        for (c, d), value in complement_matrix.items():
            local = {u: a, v: b}
            if x < y:
                local[x], local[y] = c, d
            else:
                local[x], local[y] = d, c
            word = tuple(local[vertex] for vertex in vertices)
            rows[word_index[word]][column] += value
    return rational_rank(rows)


def main():
    audit_arbitrary_covector_formula()

    # Use separate center labels only while checking the two input tensors.
    left_vertices = ("p", "x0", "x1", "x2")
    right_vertices = ("q", "y0", "y1", "y2")
    left = canonical_k4("p", ("x0", "x1", "x2"))
    right = canonical_k4("q", ("y0", "y1", "y2"))
    left_tensor = matching_tensor(left_vertices, left)
    right_tensor = matching_tensor(right_vertices, right)
    delta4 = {(color,) * 4: 1 for color in COLORS}
    assert left_tensor == delta4
    assert right_tensor == delta4

    contracted = contract_tensors(
        left_tensor, left_vertices, "p", right_tensor, right_vertices, "q"
    )
    delta6 = {(color,) * 6: 1 for color in COLORS}
    assert contracted == delta6

    # Relabel the six surviving sites by x_i=i and y_i=3+i.  The effective
    # edge formula A_(px)^T I B_(qy) leaves exactly the three colored spokes.
    vertices = tuple(range(6))
    effective = {}
    for color in COLORS:
        effective[edge(color, 3 + color)] = {(color, color): 1}
        other = [index for index in COLORS if index != color]
        effective[edge(*other)] = {(color, color): 1}
        effective[edge(3 + other[0], 3 + other[1])] = {(color, color): 1}

    one_cross = matching_tensor(
        vertices, effective, crossing_cut={0, 1, 2}, crossing_count=1
    )
    three_cross = matching_tensor(
        vertices, effective, crossing_cut={0, 1, 2}, crossing_count=3
    )
    full = matching_tensor(vertices, effective)
    rainbow = (0, 1, 2, 0, 1, 2)
    assert one_cross == delta6
    assert three_cross == {rainbow: 1}
    assert full == delta6 | {rainbow: 1}

    supported_matchings = tuple(
        matching
        for matching in perfect_matchings(vertices)
        if all(edge(*pair) in effective for pair in matching)
    )
    assert len(supported_matchings) == 4
    assert all(
        any(
            any(edge(*pair) == supported_edge for pair in matching)
            for matching in supported_matchings
        )
        for supported_edge in effective
    )

    adjacency = {vertex: set() for vertex in vertices}
    for u, v in effective:
        adjacency[u].add(v)
        adjacency[v].add(u)
    assert all(len(adjacency[vertex]) == 3 for vertex in vertices)
    assert all(
        connected_after_deleting(adjacency, deleted)
        for size in (0, 1, 2)
        for deleted in itertools.combinations(vertices, size)
    )

    # The only nontrivial odd shores have size three.  Every one has a
    # supported matching crossing three times, so there is no tight cut.
    for shore in itertools.combinations(vertices, 3):
        crossing_numbers = {
            sum((u in shore) != (v in shore) for u, v in matching)
            for matching in supported_matchings
        }
        assert 3 in crossing_numbers

    # All nine blocks have rank one, so the rank>=2 and rank-three graphs
    # are empty.  Quantitatively, every four-site source Hessian has far
    # more than the three universal gauge directions in its kernel.
    hessian_census = {}
    for deleted_pair in itertools.combinations(vertices, 2):
        remaining = tuple(vertex for vertex in vertices if vertex not in deleted_pair)
        rank = four_site_source_hessian_rank(remaining, effective)
        hessian_census[rank] = hessian_census.get(rank, 0) + 1
        assert 54 - rank > 3
    assert hessian_census == {35: 6, 34: 3, 26: 6}

    print("arbitrary dense blocks and arbitrary bilinear K: contraction=one-cross PASS")
    print("two canonical K4 tensors contract exactly to Delta_(6,3): PASS")
    print("effective source: one-cross=Delta_(6,3), three-cross=e_012012")
    print("triangular prism: 4 perfect matchings, cubic, 3-connected, tight-cut-free")
    print("all blocks rank one; four-site Hessian ranks 35^6, 34^3, 26^6")


if __name__ == "__main__":
    main()
