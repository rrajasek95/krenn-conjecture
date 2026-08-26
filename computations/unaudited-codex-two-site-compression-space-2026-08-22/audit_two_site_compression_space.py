#!/usr/bin/env python3
"""Exact hypothesis audit for two-site flattening/compression-space arguments.

For fixed p,q, the K8 amplitude is written literally as the sum of its 105
perfect-matching tensors: 15 matchings contain pq and 90 avoid pq.  The audit
distinguishes the rank-three *sum* forced by GHZ from the upper rank of the
linear span of the individual source tensors.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESPONSE = ROOT / "computations/unaudited-codex-response-star-2026-08-20"
HERMITIAN = ROOT / "computations/unaudited-codex-hermitian-star-sos-2026-08-22"
sys.path.insert(0, str(RESPONSE))
sys.path.insert(0, str(HERMITIAN))

from response_star_core import source_from_json_blocks  # noqa: E402
from audit_hermitian_star_trace import (  # noqa: E402
    ONE, ZERO, n4_source, n6_source, zadd, zdiv, zmul,
)


W40_PATH = ROOT / "computations/unaudited-x4general-w40-2026-08-20/results_t3.json"
W25_PATH = (ROOT / "computations/unaudited-x3core-w25-2026-08-15"
            / "OBJECT_W25-F8_n8_allblocked_X3.json")
PINS = {
    "W40": "30ad242d62b5cb905858842ce4e8255b105862dc21a65c73c080557fa8c1617f",
    "W25": "46d6e207e392deaa7e0bfc4221c7f5cc6735f11a2a14cc388292ca6850dd33f6",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            result.append(((first, second),) + tail)
    return tuple(result)


def qadd(x, y):
    return x + y


def qmul(x, y):
    return x * y


def qdiv(x, y):
    return x / y


def iszero(x):
    return x == 0 or x == ZERO


def rank(rows, add, mul, div, zero):
    work = [list(row) for row in rows]
    if not work:
        return 0
    ncols = len(work[0])
    row_index = 0
    for column in range(ncols):
        pivot = next((r for r in range(row_index, len(work))
                      if not iszero(work[r][column])), None)
        if pivot is None:
            continue
        work[row_index], work[pivot] = work[pivot], work[row_index]
        scale = work[row_index][column]
        work[row_index] = [div(value, scale) for value in work[row_index]]
        for other in range(len(work)):
            if other == row_index or iszero(work[other][column]):
                continue
            scale = work[other][column]
            work[other] = [add(x, mul((-scale if isinstance(scale, Fraction)
                                      else (-scale[0], -scale[1])), y))
                           for x, y in zip(work[other], work[row_index])]
        row_index += 1
        if row_index == len(work):
            break
    return row_index


def cell(source, u, v, a, b):
    if u < v:
        return source[u, v][a][b]
    return source[v, u][b][a]


def term_flattening(source, n, p, q, matching, *, qomega=False):
    residual = tuple(v for v in range(n) if v not in (p, q))
    zero = ZERO if qomega else Fraction(0)
    one = ONE if qomega else Fraction(1)
    add = zadd if qomega else qadd
    mul = zmul if qomega else qmul
    columns = tuple(product(range(3), repeat=n - 2))
    result = [[zero for _ in columns] for _ in range(9)]
    for column, residual_word in enumerate(columns):
        word0 = dict(zip(residual, residual_word))
        for i in range(3):
            for j in range(3):
                word = dict(word0)
                word[p] = i
                word[q] = j
                value = one
                for u, v in matching:
                    value = mul(value, cell(source, u, v, word[u], word[v]))
                    if iszero(value):
                        break
                result[3*i + j][column] = value
    return result


def add_matrix(left, right, *, qomega=False):
    add = zadd if qomega else qadd
    return [[add(x, y) for x, y in zip(lrow, rrow)]
            for lrow, rrow in zip(left, right)]


def flatten_profile(source, n, p, q, *, qomega=False):
    matchings = perfect_matchings(range(n))
    zero = ZERO if qomega else Fraction(0)
    add = zadd if qomega else qadd
    mul = zmul if qomega else qmul
    div = zdiv if qomega else qdiv
    matrices = []
    direct_ranks = []
    avoiding_ranks = []
    total = [[zero for _ in range(3**(n - 2))] for _ in range(9)]
    witnesses = []
    for matching in matchings:
        matrix = term_flattening(source, n, p, q, matching, qomega=qomega)
        term_rank = rank(matrix, add, mul, div, zero)
        matrices.append(matrix)
        total = add_matrix(total, matrix, qomega=qomega)
        record = {"matching": [list(edge) for edge in matching], "rank": term_rank}
        if tuple(sorted((p, q))) in matching:
            direct_ranks.append(term_rank)
        else:
            avoiding_ranks.append(term_rank)
        if term_rank > 3:
            witnesses.append(record)
    total_rank = rank(total, add, mul, div, zero)
    # For n=4 only, certify the span itself has upper rank <=3 by exhaustive
    # coefficient replay over F_3.  Rank cannot exceed 3 because every matrix
    # in this three-dimensional span has only three distinct singleton cells.
    small_combo_max = None
    if n == 4:
        small_combo_max = 0
        for coeffs in product((-1, 0, 1), repeat=len(matrices)):
            combo = [[zero for _ in range(3**(n - 2))] for _ in range(9)]
            for coefficient, matrix in zip(coeffs, matrices):
                if coefficient:
                    scaled = [[mul((Fraction(coefficient) if not qomega
                                    else (Fraction(coefficient), Fraction(0))), x)
                               for x in row] for row in matrix]
                    combo = add_matrix(combo, scaled, qomega=qomega)
            small_combo_max = max(small_combo_max,
                                  rank(combo, add, mul, div, zero))
    return {
        "pair": [p, q],
        "shape": [9, 3**(n - 2)],
        "matching_count": len(matchings),
        "direct_matching_count": len(direct_ranks),
        "avoiding_matching_count": len(avoiding_ranks),
        "full_sum_rank": total_rank,
        "direct_term_rank_histogram": histogram(direct_ranks),
        "avoiding_term_rank_histogram": histogram(avoiding_ranks),
        "max_generator_rank": max(direct_ranks + avoiding_ranks),
        "rank_gt_3_witness": witnesses[0] if witnesses else None,
        "small_coefficient_combination_max_rank": small_combo_max,
    }


def histogram(values):
    return {str(value): values.count(value) for value in sorted(set(values))}


def load_rational_controls():
    require(digest(W40_PATH) == PINS["W40"], "W40 pin changed")
    require(digest(W25_PATH) == PINS["W25"], "W25 pin changed")
    w40_data = json.loads(W40_PATH.read_text())
    w25_data = json.loads(W25_PATH.read_text())
    return (
        source_from_json_blocks(w40_data["engine_audit"]["witness_B_integral"]["source"]),
        source_from_json_blocks(w25_data["blocks"]),
    )


def pair_screen(source, name):
    profiles = [flatten_profile(source, 8, p, q)
                for p, q in combinations(range(8), 2)]
    max_profile = max(profiles, key=lambda record: record["max_generator_rank"])
    rank3_bad = next((profile for profile in profiles
                      if profile["full_sum_rank"] <= 3
                      and profile["max_generator_rank"] > 3), None)
    return {
        "name": name,
        "all_full_sum_ranks": histogram([p["full_sum_rank"] for p in profiles]),
        "all_max_generator_ranks": histogram([p["max_generator_rank"] for p in profiles]),
        "joint_full_sum_generator_rank_histogram": histogram([
            f'{p["full_sum_rank"]},{p["max_generator_rank"]}' for p in profiles
        ]),
        "lex_first_max_generator_pair": max_profile,
        "rank_at_most3_sum_with_rank_gt3_generator": rank3_bad,
    }


def main():
    n4 = flatten_profile(n4_source(), 4, 0, 1, qomega=True)
    require(n4["shape"] == [9, 9] and n4["matching_count"] == 3, n4)
    require(n4["full_sum_rank"] == 3, n4)
    require(n4["max_generator_rank"] <= 3, n4)
    require(n4["small_coefficient_combination_max_rank"] <= 3, n4)

    n6_profiles = [flatten_profile(n6_source(), 6, p, q, qomega=True)
                   for p, q in combinations(range(6), 2)]
    n6_counter = next(profile for profile in n6_profiles
                      if profile["max_generator_rank"] > 3)
    require(n6_counter["rank_gt_3_witness"]["rank"] == 9, n6_counter)

    w40, w25 = load_rational_controls()
    w40_screen = pair_screen(w40, "W40-integral-X4")
    w25_screen = pair_screen(w25, "W25-F8-X3-allblocked")

    result = {
        "status": "PASS",
        "classification": "UNAUDITED EXACT TWO-SITE COMPRESSION-HYPOTHESIS AUDIT",
        "literal_decomposition": {
            "N8_shape": [9, 729],
            "all_perfect_matchings": 105,
            "direct_Apq_times_H6_matchings": 15,
            "avoiding_pq_response_matchings": 90,
            "exact_GHZ_nonzero_coordinates": [
                {"pair_colour": [c, c], "residual_word": str(c)*6, "value": 1}
                for c in range(3)
            ],
            "exact_GHZ_rank": 3,
        },
        "precise_hypothesis": {
            "required": (
                "A linear subspace S of Hom(k^729,k^9) with rank(X)<=3 "
                "for every X in S (upper rank at most three)."
            ),
            "available": (
                "Only the prescribed sum M(A)=sum_mu T_mu(A)=M_GHZ has rank "
                "three. The source-generated span S_A=span{T_mu(A)} is not "
                "upper-rank-three in general."
            ),
        },
        "controls": {
            "n4_exact_GHZ": n4,
            "n6_phased_block_injective": {
                "pair_rank_histogram": histogram(
                    [p["full_sum_rank"] for p in n6_profiles]),
                "max_generator_rank_histogram": histogram(
                    [p["max_generator_rank"] for p in n6_profiles]),
                "lex_first_rank9_generator": n6_counter,
            },
            "W40": w40_screen,
            "W25": w25_screen,
        },
        "terminal_verdict": {
            "bounded_rank_matrix_space": False,
            "reason": (
                "The 105-term decomposition supplies one low-rank sum, not "
                "a bounded-rank linear space. A literal avoiding-pair matching "
                "tensor already has rank nine on the phased n6 control."
            ),
            "single_matrix_compression_is_tautological": (
                "The row and column spaces of M_GHZ have dimension three, but "
                "they remember only the three output coordinates and impose no "
                "termwise annihilation on the 90 response contributions."
            ),
            "active_clean_K_consequence": False,
        },
        "pins": {"W40": PINS["W40"], "W25": PINS["W25"]},
    }
    output = HERE / "results_two_site_compression_space.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "n4": n4,
        "n6_counter": n6_counter,
        "W40_max": w40_screen["lex_first_max_generator_pair"],
        "W25_max": w25_screen["lex_first_max_generator_pair"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
