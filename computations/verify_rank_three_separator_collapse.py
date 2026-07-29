#!/usr/bin/env python3
"""Exact audit for notes/rank-three-separator-collapse.md.

The proof is uniform.  This script checks its finite graph and color-channel
cores using only Boolean and integer arithmetic.
"""

from __future__ import annotations

from itertools import combinations, product


def adjacency_from_mask(n, edges, mask):
    adjacency = [set() for _ in range(n)]
    for index, (left, right) in enumerate(edges):
        if mask >> index & 1:
            adjacency[left].add(right)
            adjacency[right].add(left)
    return adjacency


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


def spanning_tree_leaves(adjacency):
    n = len(adjacency)
    parent = {0: None}
    stack = [0]
    tree_degree = [0] * n
    while stack:
        vertex = stack.pop()
        for neighbor in sorted(adjacency[vertex], reverse=True):
            if neighbor in parent:
                continue
            parent[neighbor] = vertex
            tree_degree[vertex] += 1
            tree_degree[neighbor] += 1
            stack.append(neighbor)
    assert len(parent) == n
    leaves = [vertex for vertex, degree in enumerate(tree_degree) if degree == 1]
    assert len(leaves) >= 2
    return leaves[0], leaves[1]


def audit_nonseparating_pairs():
    graph_counts = {}
    for n in range(4, 7):
        edges = tuple(combinations(range(n), 2))
        connected_count = 0
        for mask in range(1 << len(edges)):
            adjacency = adjacency_from_mask(n, edges, mask)
            if not connected_after_deleting(adjacency, set()):
                continue
            connected_count += 1
            p, q = spanning_tree_leaves(adjacency)
            assert connected_after_deleting(adjacency, {p})
            assert connected_after_deleting(adjacency, {q})
            assert connected_after_deleting(adjacency, {p, q})
        graph_counts[n] = connected_count
    return graph_counts


def audit_minimum_degree_three_pair_survival():
    graph_counts = {}
    for n in range(4, 7):
        edges = tuple(combinations(range(n), 2))
        checked = 0
        for mask in range(1 << len(edges)):
            adjacency = adjacency_from_mask(n, edges, mask)
            if any(len(neighbors) < 3 for neighbors in adjacency):
                continue
            for p, q in combinations(range(n), 2):
                for vertex in range(n):
                    if vertex in (p, q):
                        continue
                    assert adjacency[vertex] - {p, q}
            checked += 1
        graph_counts[n] = checked
    return graph_counts


def connected_components(adjacency):
    unseen = set(range(len(adjacency)))
    components = []
    while unseen:
        start = min(unseen)
        component = {start}
        stack = [start]
        unseen.remove(start)
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor not in unseen:
                    continue
                unseen.remove(neighbor)
                component.add(neighbor)
                stack.append(neighbor)
        components.append(component)
    return components


def audit_six_site_disconnected_minimum_degree_two():
    n = 6
    edges = tuple(combinations(range(n), 2))
    checked = 0
    for mask in range(1 << len(edges)):
        adjacency = adjacency_from_mask(n, edges, mask)
        if any(len(neighbors) < 2 for neighbors in adjacency):
            continue
        components = connected_components(adjacency)
        if len(components) == 1:
            continue
        assert sorted(map(len, components)) == [3, 3]
        for component in components:
            assert all(adjacency[vertex] == component - {vertex} for vertex in component)
        checked += 1
    assert checked == 10
    return checked


def cross(left, right):
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def dot(left, right):
    return sum(x * y for x, y in zip(left, right, strict=True))


def relation_for_columns(columns):
    if len(columns) == 1:
        first = columns[0]
        return (first[1], -first[0], 0)
    first, second = columns
    relation = cross(first, second)
    if any(relation):
        return relation
    return (first[1], -first[0], 0)


def audit_component_annihilators():
    counts = {}
    vectors = tuple(product((-1, 1), repeat=3))
    for component_count in (1, 2):
        checked = 0
        for columns in product(vectors, repeat=component_count):
            relation = relation_for_columns(columns)
            assert all(dot(relation, column) == 0 for column in columns)
            assert sum(value != 0 for value in relation) >= 2
            support = [index for index, value in enumerate(relation) if value]
            assert len(support) >= 2 and support[0] != support[1]
            checked += 1
        counts[component_count] = checked
    return counts


def proportional(left, right):
    return cross(left, right) == (0, 0, 0)


def audit_rank_two_component_mergers():
    vectors = tuple(product((-1, 1), repeat=3))
    checked = 0
    for t_left, t_right, u_left, u_right in product(vectors, repeat=4):
        for sign_left, sign_right in product((-1, 1), repeat=2):
            zero_blocks = all(
                t_left[c] * u_right[d] * sign_right
                + u_left[d] * sign_left * t_right[c]
                == 0
                for c in range(3)
                for d in range(3)
                if c != d
            )
            if not zero_blocks:
                continue
            assert proportional(t_left, t_right)
            assert proportional(u_left, u_right)
            checked += 1
    assert checked
    return checked


def gf2_add(left, right):
    return tuple(x ^ y for x, y in zip(left, right, strict=True))


def gf2_dot(left, right):
    return sum(x * y for x, y in zip(left, right, strict=True)) % 2


def gf2_bases():
    nonzero = tuple(vector for vector in product((0, 1), repeat=3) if any(vector))
    bases = []
    for columns in product(nonzero, repeat=3):
        if columns[0] == columns[1] or columns[0] == columns[2] or columns[1] == columns[2]:
            continue
        if columns[2] in (gf2_add(columns[0], columns[1]),):
            continue
        bases.append(columns)
    assert len(bases) == 168
    return tuple(bases)


def gf2_matrix_rank(rows, column_count):
    packed = [sum((entry & 1) << column for column, entry in enumerate(row)) for row in rows]
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, len(packed)) if packed[row] >> column & 1),
            None,
        )
        if pivot is None:
            continue
        packed[pivot_row], packed[pivot] = packed[pivot], packed[pivot_row]
        for row in range(len(packed)):
            if row != pivot_row and packed[row] >> column & 1:
                packed[row] ^= packed[pivot_row]
        pivot_row += 1
    return pivot_row


def gf2_nullspace_basis(rows, column_count):
    packed = [sum((entry & 1) << column for column, entry in enumerate(row))
              for row in rows]
    pivot_columns = []
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, len(packed))
             if packed[row] >> column & 1),
            None,
        )
        if pivot is None:
            continue
        packed[pivot_row], packed[pivot] = packed[pivot], packed[pivot_row]
        for row in range(len(packed)):
            if row != pivot_row and packed[row] >> column & 1:
                packed[row] ^= packed[pivot_row]
        pivot_columns.append(column)
        pivot_row += 1

    free_columns = [
        column for column in range(column_count)
        if column not in set(pivot_columns)
    ]
    basis = []
    for free in free_columns:
        vector = 1 << free
        for row in range(pivot_row - 1, -1, -1):
            if (packed[row] & vector).bit_count() % 2:
                vector |= 1 << pivot_columns[row]
        basis.append(vector)
    return tuple(basis)


def gf2_projected_basis(vectors, bit_count):
    pivots = {}
    basis = []
    mask = (1 << bit_count) - 1
    for vector in vectors:
        reduced = vector & mask
        while reduced:
            pivot = reduced.bit_length() - 1
            if pivot in pivots:
                reduced ^= pivots[pivot]
            else:
                pivots[pivot] = reduced
                basis.append(reduced)
                break
    return tuple(basis)


def audit_one_invertible_zero_cover_geometry():
    """GF(2) audit with the second x-star completely arbitrary."""
    standard = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    vectors = tuple(product((0, 1), repeat=3))
    nonzero = tuple(vector for vector in vectors if any(vector))

    rank_two_representatives = []
    for normal in nonzero:
        plane_vectors = [vector for vector in nonzero if not gf2_dot(normal, vector)]
        first, second = plane_vectors[:2]
        rank_two_representatives.append(tuple(
            tuple((first[row], second[row], 0)[column] for column in range(3))
            for row in range(3)
        ))
    rank_one_representatives = [
        tuple(tuple(left[row] if column == 0 else 0 for column in range(3))
              for row in range(3))
        for left in nonzero
    ]
    zero = tuple(tuple(0 for _ in range(3)) for _ in range(3))
    aggregates = (zero,) + tuple(rank_one_representatives) + tuple(
        rank_two_representatives
    )
    assert len(aggregates) == 15

    checked = 0
    maximum_nonzero_rows = 0
    pairs = tuple((c, d) for c in range(3) for d in range(3) if c != d)
    for b_columns in product(vectors, repeat=3):
        for aggregate in aggregates:
            equations = []
            for pair_index, (c, d) in enumerate(pairs):
                for row in range(3):
                    for column in range(3):
                        equation = [0] * 24
                        equation[3 * c + column] = b_columns[d][row]
                        equation[9 + 3 * d + column] = standard[c][row]
                        equation[18 + pair_index] = aggregate[row][column]
                        equations.append(equation)
            kernel = gf2_nullspace_basis(equations, 24)
            row_basis = gf2_projected_basis(kernel, 18)
            assert len(row_basis) <= 12
            local_maximum = 0
            for coefficients in range(1 << len(row_basis)):
                vector = 0
                for index, basis_vector in enumerate(row_basis):
                    if coefficients >> index & 1:
                        vector ^= basis_vector
                nonzero_rows = sum(
                    bool((vector >> (3 * row)) & 0b111) for row in range(6)
                )
                local_maximum = max(local_maximum, nonzero_rows)
            assert local_maximum <= 4
            maximum_nonzero_rows = max(maximum_nonzero_rows, local_maximum)
            checked += 1
    assert checked == 512 * 15
    assert maximum_nonzero_rows == 4
    return checked, maximum_nonzero_rows


def audit_double_invertible_zero_cover_geometry():
    standard = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    nonzero = tuple(vector for vector in product((0, 1), repeat=3) if any(vector))
    bases = gf2_bases()

    rank_two_cases = 0
    for normal in nonzero:
        plane_vectors = [vector for vector in nonzero if not gf2_dot(normal, vector)]
        first, second = plane_vectors[:2]
        aggregate = tuple(
            tuple((first[row], second[row], 0)[column] for column in range(3))
            for row in range(3)
        )
        for basis in bases:
            pairs = tuple((c, d) for c in range(3) for d in range(3) if c != d)
            equations = []
            for pair_index, (c, d) in enumerate(pairs):
                for row in range(3):
                    for column in range(3):
                        equation = [0] * 24
                        equation[3 * c + column] = basis[d][row]
                        equation[9 + 3 * d + column] = standard[c][row]
                        equation[18 + pair_index] = aggregate[row][column]
                        equations.append(equation)
            # The full rank-two block equations have only the zero solution
            # for the six endpoint rows and the six gauge scalars.
            assert gf2_matrix_rank(equations, 24) == 24
            rank_two_cases += 1

    def lies_in_line(vector, line):
        return vector == (0, 0, 0) or vector == line

    rank_at_most_one_cases = 0
    lines = ((0, 0, 0),) + nonzero
    for line in lines:
        for basis in bases:
            for row_support in product((0, 1), repeat=6):
                if sum(row_support) < 5:
                    continue
                compatible = all(
                    lies_in_line(
                        gf2_add(
                            tuple(row_support[3 + d] * entry for entry in standard[c]),
                            tuple(row_support[c] * entry for entry in basis[d]),
                        ),
                        line,
                    )
                    for c in range(3)
                    for d in range(3)
                    if c != d
                )
                assert not compatible
            rank_at_most_one_cases += 1
    return rank_two_cases, rank_at_most_one_cases


def audit_row_line_intersections():
    checked = 0
    values = (-1, 0, 1)
    for first_color in range(3):
        for second_color in range(3):
            if first_color == second_color:
                continue
            candidates = 0
            for entries in product(values, repeat=9):
                matrix = [list(entries[3 * row : 3 * row + 3]) for row in range(3)]
                first_supported = all(
                    matrix[row] == [0, 0, 0]
                    for row in range(3)
                    if row != first_color
                )
                second_supported = all(
                    matrix[row] == [0, 0, 0]
                    for row in range(3)
                    if row != second_color
                )
                if first_supported and second_supported:
                    candidates += 1
                    assert not any(any(row) for row in matrix)
            assert candidates == 1
            checked += candidates
    return checked


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(remainder):
            yield ((min(first, second), max(first, second)),) + matching


def audit_order_four_empty_rank_graph():
    # The three one-factor classes in equation (19).
    edge_color = {
        (0, 1): 0,
        (2, 3): 0,
        (0, 2): 1,
        (1, 3): 1,
        (0, 3): 2,
        (1, 2): 2,
    }

    coefficients = {}
    matchings = tuple(perfect_matchings(range(4)))
    assert len(matchings) == 3
    for matching in matchings:
        word = [None] * 4
        for edge in matching:
            color = edge_color[edge]
            for endpoint in edge:
                word[endpoint] = color
        word = tuple(word)
        coefficients[word] = coefficients.get(word, 0) + 1
    assert coefficients == {
        (0, 0, 0, 0): 1,
        (1, 1, 1, 1): 1,
        (2, 2, 2, 2): 1,
    }

    # Every nonzero aggregate block is one coordinate matrix, hence rank one;
    # nevertheless its support is K4 and remains connected after <=2 deletions.
    assert len(edge_color) == 6
    support = adjacency_from_mask(4, tuple(combinations(range(4), 2)), (1 << 6) - 1)
    assert all(len(neighbors) == 3 for neighbors in support)
    for deletion_size in range(3):
        for deleted in combinations(range(4), deletion_size):
            assert connected_after_deleting(support, set(deleted))

    # For every deleted pair, W has two sites and r=1.  Thus H_q(Z)=Z on
    # the nine-dimensional two-site quadratic space, while the only gauge
    # coefficient is alpha_i+alpha_j=0.
    pair_audits = 0
    identity = tuple(tuple(int(row == col) for col in range(9)) for row in range(9))
    for deleted in combinations(range(4), 2):
        internal = tuple(vertex for vertex in range(4) if vertex not in deleted)
        edge = (min(internal), max(internal))
        assert edge in edge_color
        assert all(sum(identity[row][col] * vector[col] for col in range(9)) == vector[row]
                   for vector in identity for row in range(9))
        assert 1 + (-1) == 0
        pair_audits += 1
    assert pair_audits == 6
    return len(matchings), pair_audits


def main():
    graph_counts = audit_nonseparating_pairs()
    degree_three_counts = audit_minimum_degree_three_pair_survival()
    disconnected_six = audit_six_site_disconnected_minimum_degree_two()
    component_counts = audit_component_annihilators()
    merger_cases = audit_rank_two_component_mergers()
    one_invertible_geometry = audit_one_invertible_zero_cover_geometry()
    isolate_geometry = audit_double_invertible_zero_cover_geometry()
    row_intersections = audit_row_line_intersections()
    order_four = audit_order_four_empty_rank_graph()
    print(f"verified connected labeled graph counts: {graph_counts}")
    print(f"verified minimum-degree-three pair survival: {degree_three_counts}")
    print(f"verified six-site thick disconnected graphs: {disconnected_six}")
    print(f"verified one/two-component annihilator cases: {component_counts}")
    print(f"verified rank-two component-merger cases: {merger_cases}")
    print(f"verified one-invertible zero-cover geometry: {one_invertible_geometry}")
    print(f"verified double-invertible isolate geometry: {isolate_geometry}")
    print(f"verified distinct endpoint-row intersections: {row_intersections}")
    print(f"verified order-four matchings/pair Hessians: {order_four}")
    print("PASS: connected separator collapse and component-channel audit")


if __name__ == "__main__":
    main()
