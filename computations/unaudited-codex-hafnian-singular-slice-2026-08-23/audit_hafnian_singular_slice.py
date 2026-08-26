#!/usr/bin/env python3
"""Exact two/three-site normal-slice audit of the N8 hafnian identity."""

from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse
import json
import sys


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_hafnian_singular_slice.json"
P, Q = 6, 7
RESIDUAL = tuple(range(6))


def edge(u, v):
    return (u, v) if u < v else (v, u)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(first, second),) + tail))


MATCHINGS = tuple(perfect_matchings(range(8)))
assert len(MATCHINGS) == 105


def matching_type_counts(exposed):
    exposed = set(exposed)
    counts = {}
    for matching in MATCHINGS:
        internal = sum(set(pair) <= exposed for pair in matching)
        crossing = sum(len(set(pair) & exposed) == 1 for pair in matching)
        residual = len(matching) - internal - crossing
        key = (internal, crossing, residual)
        counts[key] = counts.get(key, 0) + 1
    return counts


def zeros():
    return [[0] * 3 for _ in range(3)]


def identity():
    return [[int(i == j) for j in range(3)] for i in range(3)]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def set_oriented(blocks, u, v, matrix):
    blocks[edge(u, v)] = matrix if u < v else transpose(matrix)


def oriented(blocks, u, v):
    matrix = blocks.get(edge(u, v), zeros())
    return matrix if u < v else transpose(matrix)


def bilinear(matrix, left, right):
    return sum(
        left[a] * matrix[a][b] * right[b]
        for a, b in product(range(3), repeat=2)
    )


def star_contraction(blocks, site, residual, colour, residual_vector):
    matrix = oriented(blocks, site, residual)
    return sum(matrix[colour][b] * residual_vector[b] for b in range(3))


def two_site_normal_hessian(blocks, residual_vectors):
    result = zeros()
    for a, b in product(range(3), repeat=2):
        value = 0
        for matching in MATCHINGS:
            partner = {}
            for u, v in matching:
                partner[u] = v
                partner[v] = u
            r, s = partner[P], partner[Q]
            if r == Q:
                term = oriented(blocks, P, Q)[a][b]
                for u, v in matching:
                    if {u, v} == {P, Q}:
                        continue
                    term *= bilinear(
                        oriented(blocks, u, v),
                        residual_vectors[u], residual_vectors[v],
                    )
            else:
                term = star_contraction(blocks, P, r, a, residual_vectors[r])
                term *= star_contraction(blocks, Q, s, b, residual_vectors[s])
                for u, v in matching:
                    if P in (u, v) or Q in (u, v):
                        continue
                    term *= bilinear(
                        oriented(blocks, u, v),
                        residual_vectors[u], residual_vectors[v],
                    )
            value += term
        result[a][b] = value
    return result


def rank(matrix):
    matrix = [[Fraction(value) for value in row] for row in matrix]
    answer = 0
    width = len(matrix[0]) if matrix else 0
    for column in range(width):
        pivot = next(
            (row for row in range(answer, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[answer], matrix[pivot] = matrix[pivot], matrix[answer]
        value = matrix[answer][column]
        matrix[answer] = [entry / value for entry in matrix[answer]]
        for row in range(len(matrix)):
            if row == answer or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [
                entry - value * pivot_entry
                for entry, pivot_entry in zip(matrix[row], matrix[answer])
            ]
        answer += 1
    return answer


def e00():
    answer = zeros()
    answer[0][0] = 1
    return answer


def first_column(vector):
    return [[vector[row] if column == 0 else 0 for column in range(3)] for row in range(3)]


def subtract(left, right):
    return [[left[i][j] - right[i][j] for j in range(3)] for i in range(3)]


def normal_hessian_guard(direct, mutate=False):
    blocks = {}
    for u, v in ((0, 1), (2, 3), (4, 5)):
        set_oriented(blocks, u, v, e00())
    set_oriented(blocks, P, Q, direct)
    response = subtract(identity(), direct)
    for index, (r, s) in enumerate(((0, 1), (2, 3), (4, 5))):
        unit = [int(a == index) for a in range(3)]
        row = response[index]
        if mutate:
            row = [response[a][index] for a in range(3)]
        set_oriented(blocks, P, r, first_column(unit))
        set_oriented(blocks, Q, s, first_column(row))
    residual_vectors = {site: [1, 1, 1] for site in RESIDUAL}
    hessian = two_site_normal_hessian(blocks, residual_vectors)
    if hessian != identity():
        raise RuntimeError("crossed-endpoint row/column mutation breaks the literal Hessian")
    total_normal_hessian = [
        [0] * 3 + hessian[row] for row in range(3)
    ] + [
        transpose(hessian)[row] + [0] * 3 for row in range(3)
    ]
    assert rank(total_normal_hessian) == 6
    return {
        "direct_edge": direct,
        "direct_edge_rank": rank(direct),
        "response_matrix": response,
        "normal_mixed_block": hessian,
        "full_normal_hessian_rank": rank(total_normal_hessian),
    }


def audit(mutate=False):
    two_counts = matching_type_counts((P, Q))
    assert two_counts == {(1, 0, 3): 15, (0, 2, 2): 90}
    three_counts = matching_type_counts((5, P, Q))
    assert three_counts == {(1, 1, 2): 45, (0, 3, 1): 60}

    zero_direct = normal_hessian_guard(zeros(), mutate=mutate)
    hostile_direct_matrix = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
    hostile_direct = normal_hessian_guard(hostile_direct_matrix, mutate=mutate)
    assert hostile_direct["direct_edge_rank"] == 3

    result = {
        "status": "PASS singular slices are the frozen site-down hierarchy",
        "polynomial_identity": (
            "Haf(B_A(x)) = sum_c product_i x_(i,c), with "
            "B_ij=x_i^T A_ij x_j"
        ),
        "two_site_slice": {
            "zero_sites": [P, Q],
            "multiplicity": 2,
            "matching_partition": {
                "direct_pair_plus_three_residual": two_counts[(1, 0, 3)],
                "two_crossings_plus_two_residual": two_counts[(0, 2, 2)],
            },
            "leading_normal_form": (
                "sum_ab y_(6,a)y_(7,b)[A_67[a,b] q_R^[3] "
                "+ l_(6,a)l_(7,b) q_R^[2]]"
            ),
            "rhs_leading_normal_form": (
                "sum_c (product_(i in R) x_(i,c)) y_(6,c)y_(7,c)"
            ),
            "coordinate_count": 3 ** 2 * 3 ** 6,
            "normal_hessian_generic_rank": 6,
            "counterguards": [zero_direct, hostile_direct],
        },
        "three_site_slice": {
            "zero_sites": [5, P, Q],
            "multiplicity": 3,
            "matching_partition": {
                "one_internal_one_crossing_two_residual": three_counts[(1, 1, 2)],
                "three_crossings_one_residual": three_counts[(0, 3, 1)],
            },
            "leading_normal_form": (
                "(A_56 l_7 + A_57 l_6 + A_67 l_5) q_W^[2] "
                "+ l_5 l_6 l_7 q_W"
            ),
            "rhs_leading_normal_form": (
                "sum_c (product_(i in W) x_(i,c)) "
                "y_(5,c)y_(6,c)y_(7,c)"
            ),
            "coordinate_count": 3 ** 3 * 3 ** 5,
            "ordinary_hessian": "zero (the RHS has multiplicity three)",
        },
        "module_verdict": {
            "two_site_coordinate_bijection": "3^2 * 3^6 = 3^8 = 6561",
            "three_site_coordinate_bijection": "3^3 * 3^5 = 3^8 = 6561",
            "conclusion": (
                "Keeping all normal and residual colours is a permutation of the "
                "original coefficient rows.  The two-site normal Hessian is the "
                "full-nine carrier identity; the three-site normal cone is its "
                "literal site-down.  No new ideal generator is created."
            ),
        },
        "counterguard_verdict": (
            "At residual point x_i=(1,1,1) with residual matching "
            "01|23|45, the required RHS normal block is I_3.  For every direct "
            "matrix C, choose three crossing response pairs whose outer products "
            "sum to I_3-C.  Then the same full-rank normal Hessian is obtained. "
            "The checker replays C=0 and a hostile nonsymmetric rank-three C. "
            "Thus the two-jet forces neither rank nor a common channel on A_67."
        ),
        "scope": (
            "The pointwise counterguard matches the complete order-two normal jet "
            "at one residual point, not the full X5 polynomial identity.  The "
            "global polynomial normal slice is exactly a reindexing of full X5, "
            "so using it globally assumes the original unresolved equations."
        ),
        "smallest_genuinely_new_datum": (
            "A nonlinear compatibility among normal slices at different residual "
            "points, equivalently the archived response-dependent normal "
            "reinsertion/overlap identity; another singular derivative is not new."
        ),
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(canonical.encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate-crossed-orientation", action="store_true")
    args = parser.parse_args()
    result = audit(mutate=args.mutate_crossed_orientation)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check_results:
        if not OUT.exists() or OUT.read_text() != rendered:
            print("frozen result mismatch", file=sys.stderr)
            return 1
        print(result["status"], result["logical_sha256"])
        return 0
    OUT.write_text(rendered)
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
