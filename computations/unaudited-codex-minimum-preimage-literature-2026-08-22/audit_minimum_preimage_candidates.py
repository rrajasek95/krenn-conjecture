#!/usr/bin/env python3
"""Exact must-pass guards for three minimum-preimage theorem candidates."""

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
import audit_minimum_norm_mps_guard as mps_guard  # noqa: E402
import verify_minimal_norm_gauge as gauge  # noqa: E402


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def rank_q(matrix):
    rows = [[complex(value) for value in row] for row in matrix]
    if not rows:
        return 0
    pivot = 0
    for column in range(len(rows[0])):
        selected = next((row for row in range(pivot, len(rows))
                         if rows[row][column] != 0), None)
        if selected is None:
            continue
        rows[pivot], rows[selected] = rows[selected], rows[pivot]
        value = rows[pivot][column]
        rows[pivot] = [entry/value for entry in rows[pivot]]
        for row in range(len(rows)):
            if row == pivot or rows[row][column] == 0:
                continue
            value = rows[row][column]
            rows[row] = [left-value*right
                         for left, right in zip(rows[row], rows[pivot])]
        pivot += 1
        if pivot == len(rows):
            break
    return pivot


def n4_guard(mutate_edge_rank=False):
    matrices = mps_guard.n4_matrices()
    edges = tuple(combinations(range(4), 2))
    identity = [[int(i == j) for j in range(3)] for i in range(3)]
    edge_ranks = []
    for edge in edges:
        edge_ranks.append(rank_q(matrices[edge]))
    expected = 2 if mutate_edge_rank else 1
    require(edge_ranks == [expected] * 6,
            ("n4 live edge rank mutation guard", edge_ranks, expected))

    for vertex in range(4):
        reduced = [[0] * 3 for _ in range(3)]
        for edge, matrix in matrices.items():
            if vertex not in edge:
                continue
            for i in range(3):
                for j in range(3):
                    if vertex == edge[0]:
                        reduced[i][j] += sum(matrix[i][k]*matrix[j][k]
                                             for k in range(3))
                    else:
                        reduced[i][j] += sum(matrix[k][i]*matrix[k][j]
                                             for k in range(3))
        require(reduced == identity, (vertex, reduced))

    target = {word: int(len(set(word)) == 1)
              for word in product(range(3), repeat=4)}
    require(gauge.tensor_coefficients(matrices, 4, 3) == target,
            "n4 output is not exact ternary GHZ")

    # ED/conormal must-pass: A lies in the row space of D Phi_A, equivalently
    # D Phi_A^* lambda=A has a solution.  This tests the literal source map,
    # not merely its moment matrix.
    derivative = mps_guard.block_matrix(matrices, 4, edges)
    source_row = []
    for edge in edges:
        source_row.extend(entry for row in matrices[edge] for entry in row)
    derivative_rank = mps_guard.mps.exact_rank(derivative)
    augmented_rank = mps_guard.mps.exact_rank(derivative + [source_row])
    require(augmented_rank == derivative_rank,
            (derivative_rank, augmented_rank))

    block = mps_guard.n4_minimum_block_guard()
    require(block["global_minimum_norm_squared"] == 6, block)
    return {
        "output": "exact ternary GHZ",
        "norm_squared": 6,
        "port_grams": "I_3 at all four sites",
        "live_edge_ranks": edge_ranks,
        "derivative_rank": derivative_rank,
        "conormal_rowspace_membership": True,
        "star_triangle_ranks": "8 blocks, all 27/27",
    }


def phased_matrices_eisenstein():
    fourier = (
        (gauge.Z1, gauge.Z1, gauge.Z1),
        (gauge.Z1, gauge.ZW, gauge.ZW2),
        (gauge.Z1, gauge.ZW2, gauge.ZW),
    )
    matrices = {}
    for edge in gauge.FOURIER_FACTORS[0] + gauge.FOURIER_FACTORS[1]:
        matrices[edge] = fourier
    for colour, factor in enumerate(gauge.FOURIER_FACTORS[2:]):
        anchor = tuple(tuple(gauge.Z1 if i == colour and j == colour
                             else gauge.Z0 for j in range(3))
                       for i in range(3))
        for edge in factor:
            matrices[edge] = anchor
    for edge, phase in gauge.FOURIER_PHASES.items():
        matrices[edge] = tuple(tuple(gauge.zmul(phase, entry) for entry in row)
                               for row in matrices[edge])
    return matrices


def phased_coefficient(matrices, word):
    answer = gauge.Z0
    for matching in gauge.perfect_matchings(range(6)):
        term = gauge.Z1
        for edge in matching:
            term = gauge.zmul(
                term, matrices[edge][word[edge[0]]][word[edge[1]]])
        answer = gauge.zadd(answer, term)
    return answer


def phased_guard():
    matrices = phased_matrices_eisenstein()
    seven_identity = [[(7, 0) if i == j else gauge.Z0
                       for j in range(3)] for i in range(3)]
    for vertex in range(6):
        reduced = [[gauge.Z0 for _ in range(3)] for _ in range(3)]
        for edge, matrix in matrices.items():
            if vertex == edge[0]:
                local = gauge.zmatmul(matrix, gauge.zadjoint(matrix))
            elif vertex == edge[1]:
                transpose = gauge.ztranspose(matrix)
                local = gauge.zmatmul(transpose, gauge.zadjoint(transpose))
            else:
                continue
            reduced = [[gauge.zadd(reduced[i][j], local[i][j])
                        for j in range(3)] for i in range(3)]
        require(reduced == seven_identity, (vertex, reduced))

    require(all(phased_coefficient(matrices, (colour,) * 6) == gauge.Z1
                for colour in range(3)), "phased pure normalization")
    mixed = phased_coefficient(matrices, (0, 1, 0, 0, 0, 0))
    require(mixed == gauge.zadd(gauge.Z1, gauge.ZW), mixed)

    source = mps_guard.fourier_source_mod7()
    integer_matrices = {}
    for edge in combinations(range(6), 2):
        integer_matrices[edge] = tuple(tuple(source.get((*edge, a, b), 0)
                                              for b in range(3))
                                        for a in range(3))
    edges = tuple(integer_matrices)
    star_ranks = []
    for vertex in range(6):
        star = tuple(edge for edge in edges if vertex in edge)
        rank = gauge.rank_mod_prime(
            mps_guard.block_matrix(integer_matrices, 6, star), 7)
        star_ranks.append(rank)
        require(rank == 45, (vertex, rank))
    triangle_ranks = []
    for triangle in combinations(range(6), 3):
        block = tuple(combinations(triangle, 2))
        rank = gauge.rank_mod_prime(
            mps_guard.block_matrix(integer_matrices, 6, block), 7)
        triangle_ranks.append(rank)
        require(rank == 27, (triangle, rank))
    full_rank = gauge.rank_mod_prime(
        mps_guard.block_matrix(integer_matrices, 6, edges), 7)
    require(full_rank == 130, full_rank)
    return {
        "output": "non-GHZ (one mixed coefficient is 1+omega)",
        "port_grams": "7 I_3 at all six sites",
        "derivative_rank_mod7": full_rank,
        "derivative_kernel": "five-dimensional scalar vertex gauge",
        "conormal_rowspace_membership": (
            "yes: isotropy makes A orthogonal to that complete gauge kernel"
        ),
        "star_ranks": sorted(set(star_ranks)),
        "triangle_ranks": sorted(set(triangle_ranks)),
    }


def main():
    mutate = "--mutate-n4-edge-rank" in sys.argv
    n4 = n4_guard(mutate_edge_rank=mutate)
    phased = phased_guard()
    payload = {
        "map": (
            "Phi_n(A)_i = sum over perfect matchings M of "
            "product_{uv in M} A_uv[i_u,i_v]"
        ),
        "candidates": {
            "tensor_scaling_capacity": (
                "passes both controls but sees only the local-group orbit and "
                "the moment equations; reject for the fixed Phi fibre"
            ),
            "geometric_brascamp_lieb": (
                "the naive fixed 3x3 incident-edge datum already fails its "
                "coisometry hypothesis on n4 rank-one edges; adaptive image "
                "data reduce to isotropy and forget Phi; reject"
            ),
            "ed_conormal_correspondence": (
                "literal and source-relative: A=D Phi_A^* lambda at a smooth "
                "fibre minimum; both controls pass, so it is machinery rather "
                "than a cap theorem"
            ),
        },
        "controls": {"n4": n4, "phased_n6": phased},
        "singular_vector_tuple_guard": (
            "Segre/best-rank-one criticality does not apply to the quartic "
            "105-matching sum map and would be output-only"
        ),
    }
    logical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    print(json.dumps({"logical_sha256": sha256(logical.encode()).hexdigest(),
                      **payload}, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
