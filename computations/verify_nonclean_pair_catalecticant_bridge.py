#!/usr/bin/env python3
"""Exact audit for ``notes/nonclean-pair-catalecticant-bridge.md``.

The six-site quadratic in the note is the union of three monochromatic
perfect matchings.  This script checks over the integers / a large prime:

* H_q has the maximum possible rank 130, hence only its five gauge
  directions are in the kernel;
* each pure target X_c has a one-cell preimage supported on q;
* Q(q)=q^3/3! is Delta_3 plus one mixed word;
* every active q-cell has nonzero cofactor, but no absent physical edge is
  a clean exposed edge for any colour; and
* every four-site pair cofactor has local flattening rank at most two, so
  none is locally equivalent to the ternary four-party GHZ tensor.
"""

from __future__ import annotations

import itertools
from collections import defaultdict

import networkx as nx


PRIME = 1_000_003
VERTICES = tuple(range(6))
COLORS = tuple(range(3))
EDGES = tuple(itertools.combinations(VERTICES, 2))
WORDS = tuple(itertools.product(COLORS, repeat=6))
WORD_INDEX = {word: index for index, word in enumerate(WORDS)}
CELLS = tuple((edge, a, b) for edge in EDGES for a in COLORS for b in COLORS)
CELL_INDEX = {cell: index for index, cell in enumerate(CELLS)}

MATCHINGS = (
    ((0, 4), (1, 2), (3, 5)),
    ((0, 1), (2, 5), (3, 4)),
    ((0, 2), (1, 3), (4, 5)),
)
Q_CELLS = tuple(
    (edge, colour, colour)
    for colour, matching in enumerate(MATCHINGS)
    for edge in matching
)


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


def hessian_rows(q_cells=Q_CELLS):
    """Sparse rows of H_q(Z)=Zq^2/2 for the unit-cell quadratic q."""
    rows = defaultdict(lambda: defaultdict(int))
    for left, right in itertools.combinations(q_cells, 2):
        left_edge, left_a, left_b = left
        right_edge, right_a, right_b = right
        if set(left_edge) & set(right_edge):
            continue
        remaining = tuple(
            sorted(set(VERTICES) - set(left_edge) - set(right_edge))
        )
        for a, b in itertools.product(COLORS, repeat=2):
            word = [None] * 6
            word[left_edge[0]] = left_a
            word[left_edge[1]] = left_b
            word[right_edge[0]] = right_a
            word[right_edge[1]] = right_b
            word[remaining[0]] = a
            word[remaining[1]] = b
            rows[tuple(word)][(remaining, a, b)] += 1
    return {word: dict(row) for word, row in rows.items()}


def hessian_columns(rows):
    columns = [[0] * len(WORDS) for _ in CELLS]
    for word, row in rows.items():
        row_index = WORD_INDEX[word]
        for cell, coefficient in row.items():
            columns[CELL_INDEX[cell]][row_index] = coefficient
    return columns


def rank_mod(matrix, prime=PRIME):
    values = [[entry % prime for entry in row] for row in matrix]
    row_count = len(values)
    column_count = len(values[0]) if values else 0
    rank = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, row_count) if values[row][column]),
            None,
        )
        if pivot is None:
            continue
        values[rank], values[pivot] = values[pivot], values[rank]
        inverse = pow(values[rank][column], prime - 2, prime)
        values[rank] = [entry * inverse % prime for entry in values[rank]]
        pivot_row = values[rank]
        for row in range(row_count):
            if row == rank or values[row][column] == 0:
                continue
            multiple = values[row][column]
            values[row] = [
                (entry - multiple * pivot_entry) % prime
                for entry, pivot_entry in zip(values[row], pivot_row)
            ]
        rank += 1
        if rank == row_count:
            break
    return rank


def column_dictionary(columns, cell):
    column = columns[CELL_INDEX[cell]]
    return {
        word: column[index]
        for index, word in enumerate(WORDS)
        if column[index]
    }


def audit_hessian_and_targets(rows, columns):
    # The universal six-site vertex gauges give a five-dimensional kernel,
    # hence rank at most 135-5=130.  The modular lower bound is exact.
    assert rank_mod(columns) == 130

    target_lifts = (
        ((1, 2), 0, 0),
        ((0, 1), 1, 1),
        ((0, 2), 2, 2),
    )
    for colour, cell in enumerate(target_lifts):
        assert column_dictionary(columns, cell) == {(colour,) * 6: 1}

    # H_q(q)=3Q(q).  Sum the nine active columns and divide by three.
    hessian_at_q = defaultdict(int)
    for cell in Q_CELLS:
        for word, coefficient in column_dictionary(columns, cell).items():
            hessian_at_q[word] += coefficient
    assert all(coefficient % 3 == 0 for coefficient in hessian_at_q.values())
    matching_power = {
        word: coefficient // 3
        for word, coefficient in hessian_at_q.items()
        if coefficient
    }
    assert matching_power == {
        (0, 0, 0, 0, 0, 0): 1,
        (1, 1, 1, 1, 1, 1): 1,
        (2, 2, 2, 2, 2, 2): 1,
        (0, 2, 1, 2, 0, 1): 1,
    }

    # Every active cell has a nonzero derivative/cofactor.
    assert all(column_dictionary(columns, cell) for cell in Q_CELLS)


def clean_exposed(rows, edge, colour, q_cells=Q_CELLS):
    support_edges = {cell[0] for cell in q_cells}
    if edge in support_edges:
        return False
    coefficient = None
    for a, b in itertools.product(COLORS, repeat=2):
        word = [colour] * 6
        word[edge[0]] = a
        word[edge[1]] = b
        row = rows.get(tuple(word), {})
        cell = (edge, a, b)
        if set(row) != {cell} or row[cell] == 0:
            return False
        if coefficient is None:
            coefficient = row[cell]
        elif row[cell] != coefficient:
            return False
    return True


def audit_no_clean_exposure(rows, q_cells=Q_CELLS):
    assert not any(
        clean_exposed(rows, edge, colour, q_cells)
        for edge in EDGES
        for colour in COLORS
    )


def audit_rank_degenerate_external_lift_boundary():
    q_cells = (
        ((3, 4), 2, 2),
        ((4, 5), 2, 2),
        ((0, 4), 0, 0),
        ((1, 3), 0, 0),
        ((2, 3), 1, 1),
        ((0, 2), 1, 1),
        ((0, 1), 2, 2),
        ((3, 5), 1, 1),
        ((1, 3), 1, 1),
        ((0, 4), 1, 1),
        ((1, 4), 0, 0),
        ((2, 5), 0, 0),
        ((3, 4), 0, 0),
    )
    rows = hessian_rows(q_cells)
    columns = hessian_columns(rows)
    assert rank_mod(columns) == 125

    # X_1 and X_2 have lifts on active physical edges; X_0 has a one-cell
    # lift on the absent edge 03.
    lifts = (
        (((0, 3), 0, 0), (0,) * 6),
        (((1, 4), 1, 1), (1,) * 6),
        (((2, 3), 2, 2), (2,) * 6),
    )
    for cell, target in lifts:
        assert column_dictionary(columns, cell) == {target: 1}

    support_edges = {cell[0] for cell in q_cells}
    restricted_columns = [
        columns[CELL_INDEX[(edge, a, b)]]
        for edge in support_edges
        for a, b in itertools.product(COLORS, repeat=2)
    ]
    assert rank_mod(restricted_columns) == 85
    x0 = [int(word == (0,) * 6) for word in WORDS]
    assert rank_mod(restricted_columns + [x0]) == 86

    # Despite the singleton pure row on edge 03, some other rows of every
    # absent edge block have competitors.  There is no clean exposed block.
    audit_no_clean_exposure(rows, q_cells)
    assert all(column_dictionary(columns, cell) for cell in q_cells)


def four_site_cofactor(deleted_edge):
    remaining = tuple(vertex for vertex in VERTICES if vertex not in deleted_edge)
    support = set(Q_CELLS)
    output = defaultdict(int)
    for matching in perfect_matchings(remaining):
        compatible = []
        for edge in matching:
            compatible.append(
                tuple(
                    colour
                    for colour in COLORS
                    if (tuple(sorted(edge)), colour, colour) in support
                )
            )
        for edge_colours in itertools.product(*compatible):
            word = [None] * 4
            for edge, colour in zip(matching, edge_colours, strict=True):
                word[remaining.index(edge[0])] = colour
                word[remaining.index(edge[1])] = colour
            output[tuple(word)] += 1
    return remaining, dict(output)


def flattening_matrix(output, mode):
    other_modes = tuple(index for index in range(4) if index != mode)
    other_words = tuple(itertools.product(COLORS, repeat=3))
    other_index = {word: index for index, word in enumerate(other_words)}
    matrix = [[0] * len(other_words) for _ in COLORS]
    for word, coefficient in output.items():
        rest = tuple(word[index] for index in other_modes)
        matrix[word[mode]][other_index[rest]] += coefficient
    return matrix


def audit_no_pair_cofactor_descent():
    for edge in EDGES:
        _remaining, output = four_site_cofactor(edge)
        assert output
        local_ranks = tuple(rank_mod(flattening_matrix(output, mode)) for mode in range(4))
        assert max(local_ranks) <= 2


def audit_gauge_vectors(rows, columns):
    gauge_vectors = []
    for distinguished in range(5):
        alpha = [0] * 6
        alpha[distinguished] = 1
        alpha[5] = -1
        vector = [0] * len(CELLS)
        for cell in Q_CELLS:
            edge = cell[0]
            vector[CELL_INDEX[cell]] = alpha[edge[0]] + alpha[edge[1]]
        gauge_vectors.append(vector)
        image = [0] * len(WORDS)
        for cell_index, scalar in enumerate(vector):
            if scalar == 0:
                continue
            for row_index, coefficient in enumerate(columns[cell_index]):
                image[row_index] += scalar * coefficient
        assert not any(image)
    assert rank_mod(gauge_vectors) == 5


def graph_perfect_matchings(graph, vertices=None):
    vertices = tuple(graph if vertices is None else vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for second in vertices[1:]:
        if not graph.has_edge(first, second):
            continue
        remainder = tuple(
            vertex for vertex in vertices if vertex not in (first, second)
        )
        for tail in graph_perfect_matchings(graph, remainder):
            yield (tuple(sorted((first, second))),) + tail


def audit_global_separator_countermodel():
    # Parts {0,1,2}, {3,4,5}, {6,7}.  Its complement components have
    # parities odd, odd, even, while the support itself is 5-connected.
    graph = nx.complete_multipartite_graph(3, 3, 2)
    vertices = tuple(graph)
    assert nx.node_connectivity(graph) == 5

    matchings = (
        ((0, 3), (1, 6), (2, 5), (4, 7)),
        ((0, 7), (1, 5), (2, 3), (4, 6)),
        ((0, 6), (1, 3), (2, 4), (5, 7)),
    )
    assert all(
        len({vertex for edge in matching for vertex in edge}) == 8
        for matching in matchings
    )
    assert len({edge for matching in matchings for edge in matching}) == 12

    # Assign cell (c,c) to matching c and cell (0,0) to every other edge.
    edge_cell = {tuple(sorted(edge)): None for edge in graph.edges}
    for colour, matching in enumerate(matchings):
        for edge in matching:
            assert edge_cell[edge] is None
            edge_cell[edge] = (colour, colour)
    for edge in edge_cell:
        if edge_cell[edge] is None:
            edge_cell[edge] = (0, 0)

    # The three matchings supply a coordinate anchor at every vertex/color.
    for vertex in vertices:
        for colour in COLORS:
            assert any(
                vertex in edge and edge_cell[edge] == (colour, colour)
                for edge in matchings[colour]
            )

    all_matchings = tuple(graph_perfect_matchings(graph))
    assert len(all_matchings) == 36

    # Every edge has a nonzero complementary perfect matching, hence its
    # positive singleton cell has a nonzero full cofactor.
    for edge in graph.edges:
        remaining = tuple(vertex for vertex in vertices if vertex not in edge)
        assert next(graph_perfect_matchings(graph, remaining), None) is not None

    # There is no nontrivial tight odd cut.
    for shore_size in (3, 5):
        for shore_tuple in itertools.combinations(vertices, shore_size):
            shore = set(shore_tuple)
            crossing_counts = {
                sum((left in shore) != (right in shore) for left, right in matching)
                for matching in all_matchings
            }
            assert crossing_counts != {1}

    # For every deleted pair, the complement induced on vertices adjacent
    # to at least one endpoint is disconnected.  Thus the graph satisfies
    # the global outcome of the pair trichotomy without a low support cut.
    for left, right in itertools.combinations(vertices, 2):
        remaining = set(vertices) - {left, right}
        active = (set(graph[left]) | set(graph[right])) & remaining
        internal = graph.subgraph(remaining).copy()
        complement = nx.complement(internal)
        assert not nx.is_connected(complement.subgraph(active))

    # Exact local irredundancy of the singleton star atoms.  An atom is the
    # selected edge cell times the matching tensor on the other six sites.
    for center in vertices:
        incident = tuple(tuple(sorted((center, neighbor))) for neighbor in graph[center])
        atoms = []
        for selected in incident:
            selected_word = edge_cell[selected]
            remainder = tuple(vertex for vertex in vertices if vertex not in selected)
            atom = defaultdict(int)
            for matching in graph_perfect_matchings(graph, remainder):
                word = [None] * 8
                word[selected[0]], word[selected[1]] = selected_word
                for edge in matching:
                    word[edge[0]], word[edge[1]] = edge_cell[edge]
                atom[tuple(word)] += 1
            atoms.append(dict(atom))
        words = tuple(sorted(set().union(*(set(atom) for atom in atoms))))
        matrix = [[atom.get(word, 0) for word in words] for atom in atoms]
        assert rank_mod(matrix) == len(incident)


def main():
    rows = hessian_rows()
    columns = hessian_columns(rows)
    audit_hessian_and_targets(rows, columns)
    audit_gauge_vectors(rows, columns)
    audit_no_clean_exposure(rows)
    audit_no_pair_cofactor_descent()
    audit_rank_degenerate_external_lift_boundary()
    audit_global_separator_countermodel()
    print("six-site Hessian rank 130 and five exact gauges: PASS")
    print("three supported one-cell target lifts and Q=Delta+mixed: PASS")
    print("active cofactors, no clean exposed edge, no rank-3 pair descent: PASS")
    print("rank-degenerate external-lift/no-clean boundary: PASS")
    print("global K_{3,3,2} separator/parity countermodel: PASS")


if __name__ == "__main__":
    main()
