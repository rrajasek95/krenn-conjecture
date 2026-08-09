#!/usr/bin/env python3
"""Exact incidence action of the missing occupied N=8 source modulus.

The preceding boundary-plane checker covered fourteen absent cells on the
physical edges 23 and 67.  The tangent audit finds one further source-faithful
direction modulo target gauge: changing the already occupied cell 23;21.
This checker adjoins that direction and reconstructs every coefficient of the
resulting (edge-23, edge-67)-bidegree-(1,1) family on all 62 positive-degree
N=10 quotient witnesses.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction

import verify_n10_five_cross_old_source_two_cell_shear as shear


Q = Fraction
OCCUPIED_MODULUS = (2, 3, 2, 1)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def add_weighted_old_coordinates(module, base, weighted_coordinates):
    cells = {edge: list(entries) for edge, entries in base.items()}
    module.add_sources(
        cells,
        tuple((*coordinate, Q(weight)) for coordinate, weight in weighted_coordinates),
    )
    return cells


def matrix_difference(left, right):
    return shear.matrix_add(left, shear.matrix_scale(right, -1))


def column_rank(module, columns):
    return len(
        module.rational_basis(
            [
                {row: value for row, value in enumerate(column) if value}
                for column in columns
            ]
        )
    )


def graph_record(matrices):
    size = len(matrices[0])
    edges = {
        (row, column)
        for matrix in matrices
        for row in range(size)
        for column in range(size)
        if matrix[row][column]
    }
    loops = tuple(sorted(edge for edge in edges if edge[0] == edge[1]))
    adjacency = {
        vertex: tuple(column for row, column in edges if row == vertex)
        for vertex in range(size)
    }
    state = [0] * size
    depths = [0] * size
    cyclic = False

    def visit(vertex):
        nonlocal cyclic
        if state[vertex] == 1:
            cyclic = True
            return 0
        if state[vertex] == 2:
            return depths[vertex]
        state[vertex] = 1
        depths[vertex] = max(
            (1 + visit(target) for target in adjacency[vertex] if target != vertex),
            default=0,
        )
        state[vertex] = 2
        return depths[vertex]

    longest_path = max((visit(vertex) for vertex in range(size)), default=0)
    return len(edges), len(loops), cyclic or bool(loops), longest_path, tuple(sorted(edges))


def setup():
    dependence = shear.load_dependence()
    quotient = dependence.load_quotient()
    cached = quotient.load_cached_blocks()
    matrix_cache = cached.load_cache_module()
    palette = matrix_cache.load_palette()
    five = palette.load_five_frontier()
    four = five.load_four_closure()
    bounded = four.load_bounded_frontier()
    data = bounded.prepare()
    left_coordinates = tuple(
        coordinate for coordinate in data["coordinates"] if coordinate[1] == 8
    )
    right_coordinates = tuple(
        coordinate for coordinate in data["coordinates"] if coordinate[1] == 9
    )
    pair_survivors = five.universal_pair_survivors(
        data, left_coordinates, right_coordinates
    )
    cases = dependence.surviving_cases(
        quotient,
        cached,
        palette,
        five,
        four,
        matrix_cache,
        bounded,
        data,
        pair_survivors,
        right_coordinates,
    )
    return dependence, matrix_cache, data, cases


def main() -> None:
    dependence, matrix_cache, data, cases = setup()
    module = data["module"]
    sample = tuple(map(Q, matrix_cache.SAMPLE))
    left_directions = tuple(
        direction
        for direction in dependence.ADMISSIBLE_DIRECTIONS
        if direction[:2] == (2, 3)
    ) + (OCCUPIED_MODULUS,)
    right_directions = tuple(
        direction
        for direction in dependence.ADMISSIBLE_DIRECTIONS
        if direction[:2] == (6, 7)
    )
    directions = left_directions + right_directions
    require(len(left_directions) == 8 and len(right_directions) == 7, "direction split changed")

    base_entries = {
        (left, right, left_colour, right_colour): weight
        for (left, right), entries in data["base"].items()
        for left_colour, right_colour, weight in entries
    }
    require(base_entries.get(OCCUPIED_MODULUS) == 1, "occupied modulus base weight changed")

    single_cache = {}
    pair_cache = {}
    graph_census = Counter()
    base_defect_census = Counter()
    modulus_action_census = Counter()
    deleted_modulus_rank_census = Counter()
    deleted_modulus_support_census = Counter()
    first_cycle = None
    first_modulus_action = None
    loop_arrow_orientation = Counter()
    for support, witnesses in cases.items():
        for metadata in witnesses:
            key0 = (support, metadata["name"])
            columns0 = metadata["columns0"]
            matrix0 = shear.selected_square(columns0, metadata["selected"])
            inverse = dependence.matrix_inverse(matrix0)
            coefficient_families = [columns0]
            normalized = []
            normalized_tags = []
            modulus_matrix = None
            single_columns = {}
            for direction in directions:
                key = key0 + (direction,)
                if key not in single_cache:
                    single_cache[key] = dependence.changed_columns(
                        data,
                        support,
                        metadata,
                        add_weighted_old_coordinates(
                            module, data["base"], ((direction, Q(1)),)
                        ),
                        sample,
                    )
                columns1 = single_cache[key]
                single_columns[direction] = columns1
                difference_columns = tuple(
                    tuple(columns1[column][row] - columns0[column][row] for row in range(len(columns0[column])))
                    for column in range(len(columns0))
                )
                coefficient_families.append(difference_columns)
                matrix1 = shear.selected_square(columns1, metadata["selected"])
                action = dependence.matrix_multiply(
                    inverse, matrix_difference(matrix1, matrix0)
                )
                normalized.append(action)
                normalized_tags.append(("single", direction, action))
                if direction == OCCUPIED_MODULUS:
                    modulus_matrix = action

            require(modulus_matrix is not None, "occupied modulus action missing")
            modulus_record = (
                dependence.dense_rank(modulus_matrix),
                dependence.nilpotency_index(modulus_matrix),
            )
            modulus_action_census[modulus_record] += 1
            if modulus_record[0] and first_modulus_action is None:
                first_modulus_action = (
                    support,
                    metadata["name"],
                    shear.sparse_named_matrix(modulus_matrix, metadata["labels"] + ("residual",)),
                )

            for left in left_directions:
                for right in right_directions:
                    pair_key = key0 + (left, right)
                    if pair_key not in pair_cache:
                        pair_cache[pair_key] = dependence.changed_columns(
                            data,
                            support,
                            metadata,
                            add_weighted_old_coordinates(
                                module,
                                data["base"],
                                ((left, Q(1)), (right, Q(1))),
                            ),
                            sample,
                        )
                    columns12 = pair_cache[pair_key]
                    interaction_columns = tuple(
                        tuple(
                            columns12[column][row]
                            - single_columns[left][column][row]
                            - single_columns[right][column][row]
                            + columns0[column][row]
                            for row in range(len(columns0[column]))
                        )
                        for column in range(len(columns0))
                    )
                    coefficient_families.append(interaction_columns)
                    interaction_matrix = shear.selected_square(
                        interaction_columns, metadata["selected"]
                    )
                    normalized.append(
                        dependence.matrix_multiply(inverse, interaction_matrix)
                    )
                    normalized_tags.append(
                        (
                            "interaction",
                            (left, right),
                            normalized[-1],
                        )
                    )

            modulus_square = dependence.matrix_multiply(
                modulus_matrix, modulus_matrix
            )
            require(
                modulus_square == modulus_matrix,
                "occupied modulus ceased to be a diagonal idempotent",
            )
            require(
                all(
                    not modulus_matrix[row][column]
                    for row in range(len(modulus_matrix))
                    for column in range(len(modulus_matrix))
                    if row != column
                ),
                "occupied modulus acquired an off-diagonal action",
            )
            require(
                all(
                    not matrix[row][row]
                    for tag, _label, matrix in normalized_tags
                    if not (tag == "single" and _label == OCCUPIED_MODULUS)
                    for row in range(len(matrix))
                ),
                "a boundary or interaction term acquired a diagonal part",
            )
            if any(value for row in modulus_matrix for value in row):
                zero = shear.zero_matrix(len(modulus_matrix))
                for tag, label, radical_matrix in normalized_tags:
                    if tag == "single" and label == OCCUPIED_MODULUS:
                        continue
                    require(
                        dependence.matrix_multiply(
                            modulus_matrix, radical_matrix
                        )
                        == zero,
                        "the idempotent acquired a left radical action",
                    )
                    require(
                        dependence.matrix_multiply(
                            radical_matrix, modulus_matrix
                        )
                        == radical_matrix,
                        "a radical arrow ceased to point into the idempotent",
                    )

            deleted_cells = add_weighted_old_coordinates(
                module, data["base"], ((OCCUPIED_MODULUS, Q(-1)),)
            )
            deleted_columns = dependence.changed_columns(
                data, support, metadata, deleted_cells, sample
            )
            deleted_base_rank = column_rank(module, deleted_columns[:-1])
            deleted_augmented_rank = column_rank(module, deleted_columns)
            deleted_modulus_rank_census[
                (len(deleted_columns[0]) - deleted_base_rank,
                 deleted_augmented_rank - deleted_base_rank)
            ] += 1
            deleted_modulus_support_census[support] += (
                deleted_augmented_rank > deleted_base_rank
            )

            size = len(columns0[0])
            union_support = tuple(
                tuple(
                    any(family[column][row] for family in coefficient_families)
                    for row in range(size)
                )
                for column in range(len(columns0))
            )
            base_rank = dependence.support_rank(union_support[:-1])
            require(base_rank < size, "the full-plane base support filled its rank")
            base_defect_census[size - base_rank] += 1

            record = graph_record(normalized)
            nonloop_edges = tuple(edge for edge in record[4] if edge[0] != edge[1])
            nonloop_record = shear.acyclic_edge_record(
                set(nonloop_edges), len(matrix0)
            )
            require(nonloop_record[1] <= 1, "the incidence radical ceased to be square-zero")
            require(record[1] <= 1, "more than one diagonal vertex appeared")
            loop_vertices = tuple(row for row, column in record[4] if row == column)
            if loop_vertices:
                loop_vertex = loop_vertices[0]
                orientations = tuple(
                    sorted(
                        "into" if column == loop_vertex else
                        "out" if row == loop_vertex else
                        "disjoint"
                        for row, column in nonloop_edges
                    )
                )
                loop_arrow_orientation[orientations] += 1
            graph_census[record[:4]] += 1
            if record[2] and first_cycle is None:
                first_cycle = (support, metadata["name"], record[4])

    require(sum(graph_census.values()) == 62, "witness count changed")
    supports_retaining_jump = sum(bool(count) for count in deleted_modulus_support_census.values())
    lost_supports = tuple(
        sorted(
            support
            for support, count in deleted_modulus_support_census.items()
            if not count
        )
    )
    require(base_defect_census == Counter({1: 62}), "base-defect census changed")
    require(
        modulus_action_census == Counter({(0, 1): 50, (1, None): 12}),
        "occupied-modulus action census changed",
    )
    require(
        deleted_modulus_rank_census == Counter({(1, 1): 50, (1, 0): 12}),
        "deleted-modulus quotient census changed",
    )
    require(
        graph_census
        == Counter(
            {
                (0, 0, False, 0): 7,
                (1, 0, False, 1): 36,
                (2, 0, False, 1): 7,
                (2, 1, True, 1): 12,
            }
        ),
        "full incidence graph census changed",
    )
    require(
        loop_arrow_orientation == Counter({("into",): 12}),
        "idempotent/radical orientation changed",
    )
    require(
        supports_retaining_jump == 40 and len(lost_supports) == 12,
        "deleted-modulus support frontier changed",
    )
    print("N=10 occupied-modulus incidence audit: exact frontier")
    print(f"directions: {len(directions)} = {len(left_directions)} on 23 + {len(right_directions)} on 67")
    print(f"base support-defect census: {dict(sorted(base_defect_census.items()))}")
    print(f"occupied-modulus action (rank,nilpotency): {dict(sorted(modulus_action_census.items(), key=repr))}")
    print(f"deleted-modulus (base defect, quotient jump): {dict(sorted(deleted_modulus_rank_census.items()))}")
    print(f"supports retaining a quotient jump after deletion: {supports_retaining_jump}/{len(cases)}")
    print(f"full incidence graph census (arrows,loops,cyclic,path): {dict(sorted(graph_census.items(), key=repr))}")
    print(f"loop/radical orientation: {dict(loop_arrow_orientation)}")
    print(f"first occupied-modulus action: {first_modulus_action}")
    print(f"first cyclic action: {first_cycle}")
    print(f"first support losing its quotient jump at deletion: {lost_supports[0]}")
    print("scope: 62 evaluated positive-degree Fitting witnesses at the fixed cross torus point")


if __name__ == "__main__":
    main()
