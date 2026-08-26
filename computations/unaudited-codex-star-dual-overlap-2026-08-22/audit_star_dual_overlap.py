#!/usr/bin/env python3
"""Exact incidence-rank audit for least-star dual overlap equations."""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product
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


def source_mod7_n6():
    cells = guard.fourier_source_mod7()
    return {
        edge: tuple(tuple(cells.get((*edge, a, b), 0) for b in range(3))
                    for a in range(3))
        for edge in combinations(range(6), 2)
    }


def star_edges(n, vertex):
    return tuple(edge for edge in combinations(range(n), 2) if vertex in edge)


def dot_columns(left, left_column, right, right_column, prime):
    return sum(row[left_column] * other[right_column]
               for row, other in zip(left, right)) % prime


def overlap_matrix(matrices, n, selected_edges=None, prime=1009):
    """D on direct_sum_v im(L_v), in the L_v column coordinates."""
    selected_edges = tuple(selected_edges or combinations(range(n), 2))
    width = 9 * (n - 1)
    stars = {
        vertex: guard.block_matrix(matrices, n, star_edges(n, vertex))
        for vertex in range(n)
    }
    rows = []
    for edge in selected_edges:
        residual = guard.block_matrix(matrices, n, (edge,))
        for cell in range(9):
            row = [0] * (n * width)
            for sign, vertex in ((1, edge[0]), (-1, edge[1])):
                star = stars[vertex]
                for column in range(width):
                    row[vertex * width + column] = (
                        sign * dot_columns(residual, cell, star, column, prime)
                    ) % prime
            rows.append(row)
    return rows


def solve_mod(matrix, vector, prime):
    """One exact solution of a full-row-rank linear system over F_prime."""
    rows = [[entry % prime for entry in row] + [value % prime]
            for row, value in zip(matrix, vector)]
    pivot_row = 0
    pivots = []
    width = len(matrix[0])
    for column in range(width):
        pivot = next((row for row in range(pivot_row, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], -1, prime)
        rows[pivot_row] = [entry * inverse % prime
                           for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [(left - scale * right) % prime
                         for left, right in zip(rows[row], rows[pivot_row])]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    require(pivot_row == len(rows), (pivot_row, len(rows)))
    solution = [0] * width
    for row, column in enumerate(pivots):
        solution[column] = rows[row][-1]
    require(all(sum(entry * value for entry, value in zip(row, solution))
                % prime == target % prime
                for row, target in zip(matrix, vector)), "bad solution")
    return solution


def source_star_vector(matrices, n, vertex, prime):
    answer = []
    for edge in star_edges(n, vertex):
        answer.extend(entry % prime for row in matrices[edge] for entry in row)
    return answer


def canonical_duals(matrices, n, prime):
    """Choose exact algebraic duals L_v^T Lambda_v=A_v* over F_prime."""
    duals = []
    for vertex in range(n):
        star = guard.block_matrix(matrices, n, star_edges(n, vertex))
        transpose = [list(column) for column in zip(*star)]
        dual = solve_mod(transpose,
                         source_star_vector(matrices, n, vertex, prime),
                         prime)
        duals.append(dual)
    for edge in combinations(range(n), 2):
        residual = guard.block_matrix(matrices, n, (edge,))
        transpose = [list(column) for column in zip(*residual)]
        difference = [(left - right) % prime
                      for left, right in zip(duals[edge[0]], duals[edge[1]])]
        require(all(sum(a * b for a, b in zip(row, difference)) % prime == 0
                    for row in transpose), (edge, "overlap failed"))
    return duals


def cycle_ranks(matrices, n, prime):
    triangle = ((0, 1), (1, 2), (0, 2))
    square = ((0, 1), (1, 2), (2, 3), (0, 3))
    tri_matrix = overlap_matrix(matrices, n, triangle, prime)
    square_matrix = overlap_matrix(matrices, n, square, prime)
    return {
        "triangle": gauge.rank_mod_prime(tri_matrix, prime),
        "triangle_rows": 27,
        "four_cycle": gauge.rank_mod_prime(square_matrix, prime),
        "four_cycle_rows": 36,
    }


def n4_control(mutate_cycle=False):
    n, prime = 4, 1009
    matrices = guard.n4_matrices()
    star_ranks = [gauge.rank_mod_prime(
        guard.block_matrix(matrices, n, star_edges(n, vertex)), prime)
                  for vertex in range(n)]
    require(star_ranks == [27] * 4, star_ranks)
    residual_ranks = [gauge.rank_mod_prime(
        guard.block_matrix(matrices, n, (edge,)), prime)
                      for edge in combinations(range(n), 2)]
    require(residual_ranks == [9] * 6, residual_ranks)
    overlap = overlap_matrix(matrices, n, prime=prime)
    overlap_rank = gauge.rank_mod_prime(overlap, prime)
    require(overlap_rank == 54, overlap_rank)

    # Here every star matrix has orthonormal one-hot columns.  Consequently
    # the literal Hermitian least dual is L_v A_v*, and all four equal GHZ.
    words = tuple(product(range(3), repeat=n))
    least_duals = []
    for vertex in range(n):
        star = guard.block_matrix(matrices, n, star_edges(n, vertex))
        gram = [[sum(row[i] * row[j] for row in star)
                 for j in range(27)] for i in range(27)]
        require(gram == [[int(i == j) for j in range(27)]
                         for i in range(27)], (vertex, "nonidentity Gram"))
        source = source_star_vector(matrices, n, vertex, prime)
        least_duals.append([
            sum(row[column] * source[column] for column in range(27))
            for row in star
        ])
    require(all(dual == least_duals[0] for dual in least_duals),
            "n4 least duals differ")
    expected = [int(len(set(word)) == 1) for word in words]
    require(least_duals[0] == expected, "n4 least dual is not GHZ")

    cycles = cycle_ranks(matrices, n, prime)
    expected_triangle = 26 if mutate_cycle else 27
    require(cycles["triangle"] == expected_triangle,
            ("hostile cycle mutation", cycles))
    require(cycles["four_cycle"] == 36, cycles)
    return {
        "star_ranks": star_ranks,
        "edge_residual_ranks": residual_ranks,
        "restricted_overlap_rank": overlap_rank,
        "restricted_overlap_domain": 108,
        "restricted_overlap_kernel": 54,
        "full_dual_domain": 324,
        "full_overlap_kernel": 270,
        "least_duals": "all four equal the ternary GHZ output tensor",
        "cycle_ranks": cycles,
    }


def n6_control():
    n, prime = 6, 7
    matrices = source_mod7_n6()
    star_ranks = [gauge.rank_mod_prime(
        guard.block_matrix(matrices, n, star_edges(n, vertex)), prime)
                  for vertex in range(n)]
    require(star_ranks == [45] * 6, star_ranks)
    residual_ranks = [gauge.rank_mod_prime(
        guard.block_matrix(matrices, n, (edge,)), prime)
                      for edge in combinations(range(n), 2)]
    require(residual_ranks == [9] * 15, residual_ranks)
    overlap = overlap_matrix(matrices, n, prime=prime)
    overlap_rank = gauge.rank_mod_prime(overlap, prime)
    require(overlap_rank == 135, overlap_rank)
    cycles = cycle_ranks(matrices, n, prime)
    require(cycles == {"triangle": 27, "triangle_rows": 27,
                       "four_cycle": 36, "four_cycle_rows": 36}, cycles)

    # This exact split-prime calculation chooses canonical algebraic duals.
    # Least Hermitian duals obey the same overlap equations formally because
    # both endpoint star-adjoint equations recover the same A_pq.
    duals = canonical_duals(matrices, n, prime)
    dual_span = gauge.rank_mod_prime(duals, prime)
    require(dual_span > 1, dual_span)
    return {
        "field": "F_7, omega -> 2; full row rank proves the Q(omega) rank",
        "star_ranks": star_ranks,
        "edge_residual_ranks": residual_ranks,
        "restricted_overlap_rank": overlap_rank,
        "restricted_overlap_domain": 270,
        "restricted_overlap_kernel": 135,
        "full_dual_domain": 4374,
        "full_overlap_kernel": 4239,
        "canonical_dual_span_rank": dual_span,
        "all_15_overlap_equations": "PASS",
        "cycle_ranks": cycles,
    }


def main():
    n4 = n4_control(mutate_cycle="--mutate-cycle-rank" in sys.argv)
    n6 = n6_control()
    payload = {
        "theorem": (
            "If every star L_v=direct_sum_{e incident v} T_e is injective, "
            "then D(Lambda)_pq=T_pq^*(Lambda_p-Lambda_q) is surjective. "
            "Indeed ker D^* is zero by star injectivity."
        ),
        "consequence": (
            "The overlap rows have no cycle/Koszul syzygy on an injective-star "
            "chart. Least-star compatibility follows tautologically from the "
            "two endpoint equations recovering the same A_pq."
        ),
        "controls": {"n4_exact_ghz": n4, "n6_phased_non_ghz": n6},
        "terminal_verdict": (
            "acyclicity no-go: overlap compatibility adds no source equation "
            "until a star determinant vanishes; only that boundary can carry "
            "new normality information"
        ),
    }
    logical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    print(json.dumps({"logical_sha256": sha256(logical.encode()).hexdigest(),
                      **payload}, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
