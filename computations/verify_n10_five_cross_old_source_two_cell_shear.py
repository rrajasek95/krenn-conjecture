#!/usr/bin/env python3
"""Two-generator unipotent-shear closure of the N=10 quotient witnesses."""

from __future__ import annotations

import importlib.util
from collections import Counter
from itertools import combinations
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_dependence():
    path = Path(__file__).with_name(
        "verify_n10_five_cross_old_source_one_cell_dependence.py"
    )
    spec = importlib.util.spec_from_file_location("dependence", path)
    require(spec is not None and spec.loader is not None, "cannot load dependence")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def matrix_add(*terms):
    return tuple(
        tuple(sum(term[row][column] for term in terms) for column in range(len(terms[0][0])))
        for row in range(len(terms[0]))
    )


def matrix_scale(matrix, scalar):
    return tuple(
        tuple(scalar * value for value in row)
        for row in matrix
    )


def selected_square(columns, selected):
    return tuple(
        tuple(columns[column][row] for column in selected)
        for row in range(len(columns[0]))
    )


def zero_matrix(size):
    return tuple(tuple(0 for _column in range(size)) for _row in range(size))


def matrix_equal(left, right):
    return left == right


def acyclic_shear_record(matrices):
    size = len(matrices[0])
    edges = {
        (row, column)
        for matrix in matrices
        for row in range(size)
        for column in range(size)
        if matrix[row][column]
    }
    return acyclic_edge_record(edges, size)


def acyclic_edge_record(edges, size):
    require(
        all(row != column for row, column in edges),
        "a shear acquired a diagonal entry",
    )
    adjacency = {
        vertex: tuple(column for row, column in edges if row == vertex)
        for vertex in range(size)
    }
    state = [0] * size
    depths = [0] * size

    def visit(vertex):
        require(state[vertex] != 1, "the joint shear support has a cycle")
        if state[vertex] == 2:
            return depths[vertex]
        state[vertex] = 1
        depths[vertex] = max(
            (1 + visit(target) for target in adjacency[vertex]),
            default=0,
        )
        state[vertex] = 2
        return depths[vertex]

    longest_path = max((visit(vertex) for vertex in range(size)), default=0)
    return len(edges), longest_path


def sparse_named_matrix(matrix, names):
    return tuple(
        (names[row], names[column], value)
        for row in range(len(matrix))
        for column in range(len(matrix))
        if (value := matrix[row][column])
    )


def add_old_coordinates(dependence, module, base, coordinates):
    cells = {edge: list(entries) for edge, entries in base.items()}
    for coordinate in coordinates:
        module.add_sources(cells, ((*coordinate, dependence.Q(1)),))
    return cells


def main() -> None:
    dependence = load_dependence()
    quotient = dependence.load_quotient()
    cached = quotient.load_cached_blocks()
    matrix_cache = cached.load_cache_module()
    palette = matrix_cache.load_palette()
    five = palette.load_five_frontier()
    four = five.load_four_closure()
    bounded = four.load_bounded_frontier()
    data = bounded.prepare()
    module = data["module"]
    sample = tuple(map(dependence.Q, matrix_cache.SAMPLE))
    left_coordinates = tuple(
        coordinate for coordinate in data["coordinates"]
        if coordinate[1] == 8
    )
    right_coordinates = tuple(
        coordinate for coordinate in data["coordinates"]
        if coordinate[1] == 9
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

    unit_gate = data["one_cell"].load_unit_gate()
    direction_pairs = tuple(combinations(dependence.ADMISSIBLE_DIRECTIONS, 2))
    require(len(direction_pairs) == 91, "direction-pair count changed")
    character_constraints = [
        data["one_cell"].coordinate_character(coordinate)
        for coordinate in sorted(
            data["one_cell"].support_coordinates(data["base"])
        )
    ]
    character_constraints.extend(data["one_cell"].target_characters())
    character_basis = module.rational_basis(character_constraints)
    require(len(character_basis) == 15, "old-source character rank changed")
    pair_character_ranks = Counter(
        len(
            module.rational_basis(
                list(character_basis.values())
                + [
                    data["one_cell"].coordinate_character(direction)
                    for direction in pair
                ]
            )
        )
        for pair in direction_pairs
    )
    require(
        pair_character_ranks == Counter({17: 89, 16: 2}),
        "direction-pair character ranks changed",
    )
    for pair in direction_pairs:
        old_cells = add_old_coordinates(
            dependence, module, data["base"], pair
        )
        require(
            all(
                unit_gate.active_complete(module.cut_record(cut, old_cells))
                for cut in unit_gate.THREE_CUTS
            ),
            f"unit two-cell old source left the exactness locus: {pair}",
        )
    full_unit_cells = add_old_coordinates(
        dependence,
        module,
        data["base"],
        dependence.ADMISSIBLE_DIRECTIONS,
    )
    require(
        all(
            unit_gate.active_complete(module.cut_record(cut, full_unit_cells))
            for cut in unit_gate.THREE_CUTS
        ),
        "the full unit boundary plane left the exactness locus",
    )

    single_cache = {}
    factorization_census = Counter()
    base_defect_census = Counter()
    interaction_census = Counter()
    nilpotent_incidence_census = Counter()
    first_unfactored = None
    exceptional_pairs = []
    global_shear_edges = {}
    global_matrix_support = {}
    global_sizes = {}
    for pair in direction_pairs:
        pair_census = Counter()
        for support, witnesses in cases.items():
            for metadata in witnesses:
                columns0 = metadata["columns0"]
                singles = []
                for direction in pair:
                    key = (support, metadata["name"], direction)
                    if key not in single_cache:
                        single_cache[key] = dependence.changed_columns(
                            data,
                            support,
                            metadata,
                            add_old_coordinates(
                                dependence, module, data["base"], (direction,)
                            ),
                            sample,
                        )
                    singles.append(single_cache[key])
                columns12 = dependence.changed_columns(
                    data,
                    support,
                    metadata,
                    add_old_coordinates(
                        dependence, module, data["base"], pair
                    ),
                    sample,
                )

                affine_bilinear_support = tuple(
                    tuple(
                        columns0[column][row]
                        or singles[0][column][row] - columns0[column][row]
                        or singles[1][column][row] - columns0[column][row]
                        or (
                            columns12[column][row]
                            - singles[0][column][row]
                            - singles[1][column][row]
                            + columns0[column][row]
                        )
                        for row in range(len(columns0[column]))
                    )
                    for column in range(len(columns0))
                )
                size = len(columns0[0])
                base_rank = dependence.support_rank(
                    affine_bilinear_support[:-1]
                )
                require(base_rank < size, "two-cell family filled the base rank")
                base_defect_census[size - base_rank] += 1

                matrix0 = selected_square(columns0, metadata["selected"])
                matrix1 = selected_square(singles[0], metadata["selected"])
                matrix2 = selected_square(singles[1], metadata["selected"])
                matrix12 = selected_square(columns12, metadata["selected"])
                inverse = dependence.matrix_inverse(matrix0)
                difference1 = matrix_add(matrix1, matrix_scale(matrix0, -1))
                difference2 = matrix_add(matrix2, matrix_scale(matrix0, -1))
                interaction = matrix_add(
                    matrix12,
                    matrix_scale(matrix1, -1),
                    matrix_scale(matrix2, -1),
                    matrix0,
                )
                shear1 = dependence.matrix_multiply(inverse, difference1)
                shear2 = dependence.matrix_multiply(inverse, difference2)
                shear12 = dependence.matrix_multiply(inverse, interaction)
                forward = dependence.matrix_multiply(shear1, shear2)
                reverse = dependence.matrix_multiply(shear2, shear1)
                zero = zero_matrix(size)
                require(
                    dependence.nilpotency_index(shear1) is not None
                    and dependence.nilpotency_index(shear2) is not None,
                    "one-cell shear lost nilpotency",
                )
                if matrix_equal(shear12, forward):
                    factorization = "forward"
                elif matrix_equal(shear12, reverse):
                    factorization = "reverse"
                elif matrix_equal(shear12, zero):
                    factorization = "zero"
                else:
                    factorization = "unfactored"
                pair_census[factorization] += 1
                incidence_record = acyclic_shear_record(
                    (shear1, shear2, shear12)
                )
                nilpotent_incidence_census[incidence_record] += 1
                witness_key = (support, metadata["name"])
                global_sizes[witness_key] = (
                    len(columns0), len(columns0[0])
                )
                global_shear_edges.setdefault(witness_key, set()).update(
                    (row, column)
                    for shear in (shear1, shear2, shear12)
                    for row in range(size)
                    for column in range(size)
                    if shear[row][column]
                )
                global_matrix_support.setdefault(witness_key, set()).update(
                    (column, row)
                    for column in range(len(affine_bilinear_support))
                    for row in range(len(affine_bilinear_support[column]))
                    if affine_bilinear_support[column][row]
                )
                if factorization == "unfactored" and first_unfactored is None:
                    all_names = metadata["labels"] + ("residual",)
                    selected_names = tuple(
                        all_names[index] for index in metadata["selected"]
                    )
                    first_unfactored = (
                        pair,
                        support,
                        metadata["name"],
                        incidence_record,
                        sparse_named_matrix(shear1, selected_names),
                        sparse_named_matrix(shear2, selected_names),
                        sparse_named_matrix(shear12, selected_names),
                    )
                interaction_census[
                    (
                        dependence.dense_rank(shear1),
                        dependence.dense_rank(shear2),
                        dependence.dense_rank(shear12),
                        factorization,
                    )
                ] += 1
        factorization_census[tuple(sorted(pair_census.items()))] += 1
        if pair_census["unfactored"]:
            exceptional_pairs.append((pair, pair_census["unfactored"]))

    require(sum(base_defect_census.values()) == 91 * 62, "pair audit count changed")
    require(
        base_defect_census == Counter({1: 5_642}),
        "two-cell base-defect census changed",
    )
    require(
        factorization_census
        == Counter(
            {
                (("forward", 62),): 88,
                (("forward", 58), ("unfactored", 4)): 1,
                (("forward", 50), ("unfactored", 12)): 1,
                (("forward", 52), ("unfactored", 10)): 1,
            }
        ),
        "two-cell factorization palette changed",
    )
    require(
        interaction_census
        == Counter(
            {
                (0, 0, 0, "forward"): 5_155,
                (0, 1, 0, "forward"): 341,
                (1, 0, 0, "forward"): 120,
                (0, 0, 1, "unfactored"): 19,
                (0, 1, 1, "unfactored"): 5,
                (1, 0, 1, "unfactored"): 2,
            }
        ),
        "two-cell interaction-rank palette changed",
    )
    require(
        nilpotent_incidence_census
        == Counter({(0, 0): 5_155, (1, 1): 456, (2, 1): 31}),
        "joint nilpotent-incidence palette changed",
    )
    global_incidence_census = Counter()
    global_base_defect_census = Counter()
    for witness_key, shear_edges in global_shear_edges.items():
        column_count, row_count = global_sizes[witness_key]
        global_incidence_census[
            acyclic_edge_record(shear_edges, row_count)
        ] += 1
        support_edges = global_matrix_support[witness_key]
        support_columns = tuple(
            tuple((column, row) in support_edges for row in range(row_count))
            for column in range(column_count)
        )
        base_rank = dependence.support_rank(support_columns[:-1])
        global_base_defect_census[row_count - base_rank] += 1
    require(len(global_shear_edges) == 62, "global witness count changed")
    require(
        global_base_defect_census == Counter({1: 62}),
        "full-plane base support defect changed",
    )
    require(
        all(longest_path <= 1 for _edges, longest_path in global_incidence_census),
        "full-plane shear radical is not square-zero",
    )
    require(
        global_incidence_census
        == Counter({(1, 1): 48, (2, 1): 7, (0, 0): 7}),
        "full-plane nilpotent-incidence census changed",
    )
    require(
        tuple(exceptional_pairs)
        == (
            (((2, 3, 0, 1), (6, 7, 1, 1)), 4),
            (((2, 3, 1, 1), (6, 7, 1, 1)), 12),
            (((2, 3, 1, 1), (6, 7, 2, 1)), 10),
        ),
        "exceptional interaction-pair ledger changed",
    )
    require(
        first_unfactored
        == (
            ((2, 3, 0, 1), (6, 7, 1, 1)),
            (
                (0, 8, 1, 0),
                (0, 8, 1, 2),
                (2, 9, 0, 0),
                (5, 9, 1, 0),
                (5, 9, 1, 2),
            ),
            "aug1",
            (1, 1),
            (),
            (),
            (((3, 1), "residual", dependence.Q(1)),),
        ),
        "first bilinear interaction changed",
    )
    print("N=10 quotient old-source two-cell shear: exact frontier")
    print("admissible old-source direction pairs: 91/91 at the unit point")
    print(f"base-plus-pair character ranks: {pair_character_ranks}")
    print("pair-witness systems: 5642")
    print(f"base support-defect census: {base_defect_census}")
    print(f"factorization palette: {factorization_census}")
    print(f"interaction rank palette: {interaction_census}")
    print(f"nilpotent-incidence palette: {nilpotent_incidence_census}")
    print(f"full-plane nilpotent incidence: {global_incidence_census}")
    print(f"full-plane base support defects: {global_base_defect_census}")
    print(f"exceptional direction pairs: {tuple(exceptional_pairs)}")
    print(f"first unfactored interaction: {first_unfactored}")
    print("non-acyclic two-cell shears: 0")
    print("scope: full anchored 14-parameter boundary-deformation plane")
    print("arbitrary-old-source identity certified: 0")


if __name__ == "__main__":
    main()
