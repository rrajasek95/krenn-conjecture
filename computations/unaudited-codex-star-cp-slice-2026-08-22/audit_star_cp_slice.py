#!/usr/bin/env python3
"""Exact one-site star slice/CP-uniqueness counterguard."""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MPS_DIR = ROOT / "computations" / "unaudited-codex-global-minimal-mps-2026-08-21"
sys.path.insert(0, str(ROOT / "computations"))
sys.path.insert(0, str(MPS_DIR))
import audit_minimum_norm_mps_guard as guard  # noqa: E402
import verify_minimal_norm_gauge as gauge  # noqa: E402


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def rank(matrix, prime):
    return gauge.rank_mod_prime(matrix, prime)


def output_tensor(matrices, n, prime):
    return {word: value % prime for word, value in
            gauge.tensor_coefficients(matrices, n, 3).items()}


def subset_tensor(matrices, vertices, prime):
    vertices = tuple(vertices)
    result = {}
    for word in product(range(3), repeat=len(vertices)):
        colours = dict(zip(vertices, word))
        value = 0
        for matching in gauge.perfect_matchings(vertices):
            term = 1
            for edge in matching:
                term *= matrices[edge][colours[edge[0]]][colours[edge[1]]]
            value += term
        result[word] = value % prime
    return result


def rest_columns(matrices, n, vertex, prime):
    """Columns e_b(q) tensor H_(V-{v,q}), labelled by (q,b)."""
    rest = tuple(site for site in range(n) if site != vertex)
    words = tuple(product(range(3), repeat=len(rest)))
    columns = {}
    for neighbour in rest:
        complement = tuple(site for site in range(n)
                           if site not in (vertex, neighbour))
        cofactor = subset_tensor(matrices, complement, prime)
        for colour in range(3):
            column = []
            for word in words:
                local = dict(zip(rest, word))
                value = (cofactor[tuple(local[site] for site in complement)]
                         if local[neighbour] == colour else 0)
                column.append(value)
            columns[(neighbour, colour)] = column
    return rest, words, columns


def site_slices(output, n, vertex):
    rest = tuple(site for site in range(n) if site != vertex)
    words = tuple(product(range(3), repeat=len(rest)))
    slices = []
    for colour in range(3):
        vector = []
        for word in words:
            full = list(word)
            full.insert(vertex, colour)
            vector.append(output[tuple(full)])
        slices.append(vector)
    return rest, words, slices


def column_rank(columns, prime):
    return rank([list(row) for row in zip(*columns)], prime)


def intersection_dimension(left_columns, right_columns, prime):
    left_rank = column_rank(left_columns, prime)
    right_rank = column_rank(right_columns, prime)
    union_rank = column_rank(left_columns + right_columns, prime)
    return left_rank + right_rank - union_rank


def slice_flattening_rank(vector, rest, words, selected_site, prime):
    other = tuple(site for site in rest if site != selected_site)
    table = {word: value for word, value in zip(words, vector)}
    rows = []
    for colour in range(3):
        row = []
        for other_word in product(range(3), repeat=len(other)):
            local = dict(zip(other, other_word))
            local[selected_site] = colour
            row.append(table[tuple(local[site] for site in rest)])
        rows.append(row)
    return rank(rows, prime)


def verify_star_equation(matrices, output, n, vertex, prime):
    rest, words, columns = rest_columns(matrices, n, vertex, prime)
    _, _, slices = site_slices(output, n, vertex)
    routes = {}
    for colour in range(3):
        reconstructed = [0] * len(words)
        support = []
        for neighbour in rest:
            matrix = matrices[tuple(sorted((vertex, neighbour)))]
            row_index = colour if vertex < neighbour else None
            for neighbour_colour in range(3):
                coefficient = (matrix[colour][neighbour_colour]
                               if vertex < neighbour
                               else matrix[neighbour_colour][colour]) % prime
                if coefficient:
                    support.append((neighbour, neighbour_colour, coefficient))
                    column = columns[(neighbour, neighbour_colour)]
                    reconstructed = [(left + coefficient * right) % prime
                                     for left, right in zip(reconstructed, column)]
        require(reconstructed == slices[colour],
                (vertex, colour, "star decomposition failed"))
        routes[colour] = support
    return rest, words, columns, slices, routes


def permuted_n4_source(permutation):
    matrices = guard.n4_matrices()
    zero = tuple(tuple(0 for _ in range(3)) for _ in range(3))
    result = {}
    for edge, matrix in matrices.items():
        changed = [[0] * 3 for _ in range(3)]
        for old in range(3):
            if matrix[old][old]:
                new = permutation[old]
                changed[new][new] = matrix[old][old]
        result[edge] = tuple(tuple(row) for row in changed) if any(
            any(row) for row in changed) else zero
    return result


def n4_control(mutate_intersections=False):
    n, vertex, prime = 4, 0, 1009
    route_permutations = []
    reference = None
    for colour_permutation in permutations(range(3)):
        matrices = permuted_n4_source(colour_permutation)
        output = output_tensor(matrices, n, prime)
        expected = {word: int(len(set(word)) == 1)
                    for word in product(range(3), repeat=n)}
        require(output == expected, colour_permutation)
        rest, words, columns, slices, routes = verify_star_equation(
            matrices, output, n, vertex, prime)
        rest_matrix = [columns[key] for key in sorted(columns)]
        require(column_rank(rest_matrix, prime) == 9, "n4 rest rank")
        pure = [[int(word == (colour,) * len(rest)) for word in words]
                for colour in range(3)]
        intersections = []
        for neighbour in rest:
            local = [columns[(neighbour, colour)] for colour in range(3)]
            intersections.append(intersection_dimension(local, pure, prime))
        expected_intersections = [0, 1, 1] if mutate_intersections else [1, 1, 1]
        require(intersections == expected_intersections,
                ("hostile intersection mutation", intersections))

        routing = tuple(next(neighbour for neighbour, _b, _value
                             in routes[colour]) for colour in range(3))
        require(all(len(routes[colour]) == 1 for colour in range(3)), routes)
        require(len(set(routing)) == 3, routing)
        route_permutations.append(routing)
        if reference is None:
            reference = {
                "rest_rank": 9,
                "L_v_rank": 27,
                "Uq_intersection_P": intersections,
                "slice_flattening_ranks": {
                    str(colour): [slice_flattening_rank(
                        slices[colour], rest, words, neighbour, prime)
                                  for neighbour in rest]
                    for colour in range(3)
                },
                "edge_block_ranks": [rank(matrix, prime)
                                      for matrix in matrices.values()],
                "K_equal_I_cap_guard": (
                    "for every pair s=1 and kappa=(1,1,1); at n=4 the cap "
                    "error sum is empty"
                ),
            }
    require(len(set(route_permutations)) == 6, route_permutations)
    require(reference["edge_block_ranks"] == [1] * 6, reference)
    return {
        **reference,
        "colour_relabellings": 6,
        "distinct_neighbour_routings": sorted(set(route_permutations)),
        "one_neighbour_carries_all_three": False,
        "CP_uniqueness_status": (
            "GHZ rank-3 CP decomposition is unique, but it recovers only the "
            "three pure tensors, not their three different matching-edge labels"
        ),
    }


def n6_source_mod7():
    cells = guard.fourier_source_mod7()
    return {
        edge: tuple(tuple(cells.get((*edge, a, b), 0) for b in range(3))
                    for a in range(3))
        for edge in combinations(range(6), 2)
    }


def n6_control():
    n, vertex, prime = 6, 0, 7
    matrices = n6_source_mod7()
    output = output_tensor(matrices, n, prime)
    rest, words, columns, slices, routes = verify_star_equation(
        matrices, output, n, vertex, prime)
    all_columns = [columns[key] for key in sorted(columns)]
    rest_rank = column_rank(all_columns, prime)
    require(rest_rank == 15, rest_rank)
    slice_rank = column_rank(slices, prime)
    require(slice_rank == 3, slice_rank)
    pure = [[int(word == (colour,) * len(rest)) for word in words]
            for colour in range(3)]
    slice_pure_intersection = intersection_dimension(slices, pure, prime)
    uq_slice_intersections = []
    uq_pure_intersections = []
    for neighbour in rest:
        local = [columns[(neighbour, colour)] for colour in range(3)]
        uq_slice_intersections.append(
            intersection_dimension(local, slices, prime))
        uq_pure_intersections.append(
            intersection_dimension(local, pure, prime))
    flattening_ranks = {
        str(colour): [slice_flattening_rank(
            slices[colour], rest, words, neighbour, prime)
                      for neighbour in rest]
        for colour in range(3)
    }
    mixed_nonzero = sum(value != 0 for word, value in output.items()
                        if len(set(word)) != 1)
    require(mixed_nonzero > 0, mixed_nonzero)
    require(any(value > 1 for row in flattening_ranks.values() for value in row),
            flattening_ranks)
    require(all(output[(colour,) * n] == 1 for colour in range(3)),
            "pure normalization")
    return {
        "field": "F_7, omega -> 2",
        "rest_map_rank": rest_rank,
        "L_v_rank": 3 * rest_rank,
        "target_site_slice_rank": slice_rank,
        "target_slice_intersection_pure_space": slice_pure_intersection,
        "Uq_intersection_target_slice_space": uq_slice_intersections,
        "Uq_intersection_pure_space": uq_pure_intersections,
        "fixed_slice_q_flattening_ranks": flattening_ranks,
        "nonzero_mixed_output_words": mixed_nonzero,
        "pure_coefficients": [output[(colour,) * n] for colour in range(3)],
        "failure_mode": (
            "the three site slices contain mixed words and have non-Segre "
            "flattenings, so there is no rank-3 GHZ CP decomposition to which "
            "uniqueness can be applied"
        ),
    }


def main():
    n4 = n4_control(mutate_intersections=(
        "--mutate-intersection-profile" in sys.argv))
    n6 = n6_control()
    payload = {
        "literal_star_factorization": (
            "for fixed v, Phi(A)[a,*]=R_v x_a with "
            "R_v=direct_sum_q (e_b(q) tensor H_(V-{v,q}))"
        ),
        "slice_invariant": (
            "dim(U_q intersect P), plus the rank of each fixed-v slice across "
            "q | remaining sites"
        ),
        "controls": {"n4_exact_ghz": n4, "n6_phased_non_ghz": n6},
        "terminal_verdict": (
            "CP uniqueness cannot see edge provenance: even exact n4 GHZ has "
            "injective L_v and unique CP terms but routes the three colours "
            "through three different neighbours. The n6 guard fails earlier "
            "because its mixed slices are not Segre rank one."
        ),
    }
    logical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    print(json.dumps({"logical_sha256": sha256(logical.encode()).hexdigest(),
                      **payload}, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
