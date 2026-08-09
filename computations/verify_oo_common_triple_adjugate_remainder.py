#!/usr/bin/env python3
"""Exact minimal multiplication-safe remainder for the curved OO pair.

The preceding two-edge checker isolates the curvature lead

    M_{pq|rs} - M_{pr|qs}.

Any coefficient of a genuine source identity (in particular of
``B*adj(B)=0``) with this lead must add a source remainder.  This checker
classifies the entire literal fixed-s second-coefficient kernel.  It is a
direct sum of seven K6 edge/perfect-matching kernels, and each summand is
exactly the zero-sum vertex-potential family

    alpha_{uv} = beta_u + beta_v,       sum_u beta_u = 0.

The two curvature halves lie in different summands.  A normalized nonzero
coefficient in either summand has support at least six.  Two explicit
six-term potential rows therefore give a support-minimal 12-term source
identity.  Its 10-term nonlead remainder is checked against the integral
obstruction covector and against all previously allowed one-edge and
diagonal rows.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import verify_oo_common_triple_two_edge_anchor_identity as two  # noqa: E402
import verify_oo_common_triple_two_edge_leibniz_obstruction as obs  # noqa: E402


Q = Fraction
EXPECTED_DIGEST = "87d3f988aa90c6bb4823062a165348cd42510f55fcfeb034a462d5e67ca15ddd"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def partial(first, second):
    return tuple(sorted((tuple(sorted(first)), tuple(sorted(second)))))


def add_scaled(target, column, scalar):
    for feature, value in column.items():
        target[feature] += Q(scalar) * value
        if not target[feature]:
            del target[feature]


def combine(coefficients, word):
    answer = defaultdict(Q)
    for matching, scalar in coefficients.items():
        add_scaled(answer, two.mixed_second_column(matching, word), scalar)
    return dict(answer)


def fixed_s_block(s_edge):
    """The 15 second coefficients whose unique s-edge is ``s_edge``."""

    s_edge = tuple(sorted(s_edge))
    require(two.S in s_edge, "a fixed-s block needs an edge through s")
    vertices = tuple(site for site in two.SITES if site not in s_edge)
    return vertices, tuple(
        partial(s_edge, edge) for edge in combinations(vertices, 2)
    )


def potential_coefficients(s_edge, beta):
    vertices, columns = fixed_s_block(s_edge)
    require(sum(Q(beta.get(vertex, 0)) for vertex in vertices) == 0,
            "a block potential must have sum zero")
    answer = {}
    for column in columns:
        other_edge = next(edge for edge in column if two.S not in edge)
        scalar = Q(beta.get(other_edge[0], 0)) + Q(beta.get(other_edge[1], 0))
        if scalar:
            answer[column] = scalar
    return answer


def matrix_rank(rows):
    matrix = [[Q(value) for value in row] for row in rows]
    rank = 0
    columns = len(matrix[0]) if matrix else 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [entry / pivot_value for entry in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(
                    matrix[row], matrix[rank], strict=True
                )
            ]
        rank += 1
    return rank


def consistent(rows, rhs):
    coefficient_rank = matrix_rank(rows)
    augmented_rank = matrix_rank([
        list(row) + [value] for row, value in zip(rows, rhs, strict=True)
    ])
    return coefficient_rank == augmented_rank


def audit_support_minimum():
    """Exhaust all supports <=5 for a normalized K6 potential row."""

    vertices = tuple(range(6))
    edges = tuple(combinations(vertices, 2))
    distinguished = (0, 1)
    tested = 0
    for size in range(1, 6):
        for support_tail in combinations(
            tuple(edge for edge in edges if edge != distinguished), size - 1
        ):
            support = {distinguished, *support_tail}
            rows = [[Q(1)] * 6]
            rhs = [Q(0)]
            normalized = [Q(0)] * 6
            normalized[0] = normalized[1] = Q(1)
            rows.append(normalized)
            rhs.append(Q(1))
            for left, right in edges:
                if (left, right) in support:
                    continue
                equation = [Q(0)] * 6
                equation[left] = equation[right] = Q(1)
                rows.append(equation)
                rhs.append(Q(0))
            require(not consistent(rows, rhs),
                    "a normalized K6 potential acquired support <= 5")
            tested += 1

    example = [Q(1, 2), Q(1, 2), Q(1, 2),
               Q(-1, 2), Q(-1, 2), Q(-1, 2)]
    require(sum(example) == 0 and example[0] + example[1] == 1,
            "minimum-support example lost its normalization")
    support = sum(
        example[left] + example[right] != 0 for left, right in edges
    )
    require(support == 6, "the K6 potential example no longer has support 6")
    return tested, support


def audit_kernel_classification(word):
    records = []
    all_columns = set()
    for neighbor in two.SITES:
        if neighbor == two.S:
            continue
        s_edge = tuple(sorted((two.S, neighbor)))
        vertices, block = fixed_s_block(s_edge)
        all_columns.update(block)
        columns = [two.mixed_second_column(column, word) for column in block]
        rank, features, _, _ = two.rational_rank(columns)
        require((len(block), rank, features) == (15, 10, 15),
                "a K6 second-coefficient block changed")

        potential_rows = []
        for distinguished in vertices[:-1]:
            beta = {distinguished: Q(1), vertices[-1]: Q(-1)}
            coefficients = potential_coefficients(s_edge, beta)
            require(not combine(coefficients, word),
                    "a zero-sum vertex potential is not a source relation")
            potential_rows.append({
                index: coefficients.get(column, 0)
                for index, column in enumerate(block)
                if coefficients.get(column, 0)
            })
        potential_rank, _, _, _ = two.rational_rank(potential_rows)
        require(potential_rank == 5 == len(block) - rank,
                "vertex potentials no longer exhaust the block kernel")
        records.append({
            "s_edge": list(s_edge),
            "columns": len(block),
            "rank": rank,
            "kernel": len(block) - rank,
            "potential_kernel_rank": potential_rank,
        })
    require(all_columns == set(two.S_TWO_EDGE_PARTIALS),
            "fixed-s blocks do not partition the 105 columns")
    return records


def explicit_minimal_row():
    p, q, r, s = two.P, two.Q_SITE, two.R, two.S
    d0, d1, d2, d3 = two.D
    first = potential_coefficients((r, s), {
        p: Q(1, 2), q: Q(1, 2), d0: Q(1, 2),
        d1: Q(-1, 2), d2: Q(-1, 2), d3: Q(-1, 2),
    })
    second = potential_coefficients((q, s), {
        p: Q(-1, 2), r: Q(-1, 2), d0: Q(-1, 2),
        d1: Q(1, 2), d2: Q(1, 2), d3: Q(1, 2),
    })
    coefficients = dict(first)
    for column, value in second.items():
        coefficients[column] = coefficients.get(column, 0) + value
        if not coefficients[column]:
            del coefficients[column]

    positive = partial((p, q), (r, s))
    negative = partial((p, r), (q, s))
    require(coefficients.get(positive) == 1
            and coefficients.get(negative) == -1,
            "the minimal row lost its curvature lead")
    require(len(first) == len(second) == 6 and len(coefficients) == 12,
            "the explicit block support changed")
    require(set(first).isdisjoint(second),
            "the two s-edge blocks stopped being independent")
    require(all(
        two.chart_sector(column, two.PQ) == "two-star"
        and two.chart_sector(column, two.PR) == "two-star"
        for column in coefficients if column not in (positive, negative)
    ), "the nonlead remainder left the common two-star sector")
    return coefficients, positive, negative


def coefficient_ledger(coefficients, positive, negative):
    records = []
    for column, scalar in sorted(coefficients.items()):
        records.append({
            "coefficient": str(scalar),
            "partial": [list(edge) for edge in column],
            "role": "lead" if column in (positive, negative) else "remainder",
            "pq_sector": two.chart_sector(column, two.PQ),
            "pr_sector": two.chart_sector(column, two.PR),
        })
    return records


def audit_one_normalization(a, ell, kernel_records, support_tests, support_minimum):
    word = (a, 0, 1, ell, 2, 2, 2, 2)
    full_nine = two.compatible_rows(a, ell)
    mixed_cuts = [row for row in full_nine if row["mixed_cut"]]
    anchor_cuts = [row for row in full_nine if row["missing_anchor_cut"]]
    require(len(full_nine) == 18 and len(mixed_cuts) == len(anchor_cuts) == 2,
            "the full-nine fine-degree selection changed")
    coefficients, positive, negative = explicit_minimal_row()
    require(not combine(coefficients, word),
            "the full 12-term source row is not zero")

    lead_coefficients = {positive: Q(1), negative: Q(-1)}
    remainder_coefficients = {
        column: value for column, value in coefficients.items()
        if column not in (positive, negative)
    }
    lead = combine(lead_coefficients, word)
    remainder = combine(remainder_coefficients, word)
    require(remainder == {feature: -value for feature, value in lead.items()},
            "the nonlead remainder is not the negative curvature lead")
    require(len(lead) == len(remainder) == 6,
            "the reduced source support changed")

    covector, _ = obs.pair_covector(word)
    lead_pairing = obs.pairing(covector, lead)
    remainder_pairing = obs.pairing(covector, remainder)
    require((lead_pairing, remainder_pairing) == (1, -1),
            "the minimal row lost its obstruction pairing")

    # No individual physical coefficient row is the remainder.  Its exact
    # provenance is instead the normal side of the one 12-column
    # cross-chart direct-double Bianchi relation L+R=0.
    individual_rows = [
        two.mixed_second_column(column, word)
        for column in two.S_TWO_EDGE_PARTIALS
    ] + [obs.one_edge_column(edge, word) for edge in two.PHYSICAL_EDGES]
    require(all(column != remainder and {
        feature: -value for feature, value in column.items()
    } != remainder for column in individual_rows),
            "the Bianchi remainder became one physical coefficient row")

    s_one = [obs.one_edge_column(edge, word)
             for edge in two.PHYSICAL_EDGES if two.S in edge] * 2
    all_one = [obs.one_edge_column(edge, word)
               for edge in two.PHYSICAL_EDGES] * 2
    diagonals = [
        two.diagonal_anchor_column(column, word)
        for _chart in ("pq", "pr")
        for column in two.ENDPOINT_MATCHINGS
    ]
    s_lower = s_one + diagonals
    all_lower = all_one + diagonals
    s_rank, _, _, _ = two.rational_rank(s_lower)
    s_augmented, _, _, _ = two.rational_rank(s_lower + [remainder])
    all_rank, _, _, _ = two.rational_rank(all_lower)
    all_augmented, _, _, _ = two.rational_rank(all_lower + [remainder])
    require((s_rank, s_augmented, all_rank, all_augmented) == (10, 11, 24, 25),
            "the remainder/lower-module rank guard changed")

    # The four-column curvature/anchor identity may be rewritten with this
    # exact source row, but not killed: its source remainder still raises
    # the known lower image by one and is detected integrally.
    target = two.curvature_target(word)
    rewritten = defaultdict(Q)
    add_scaled(rewritten, remainder, -1)
    add_scaled(rewritten, two.diagonal_anchor_column(positive, word), -1)
    add_scaled(rewritten, two.diagonal_anchor_column(negative, word), 1)
    require(dict(rewritten) == target,
            "the curvature target rewrite through the remainder changed")

    return {
        "a": a,
        "ell": ell,
        "word": "".join(map(str, word)),
        "full_nine_rows": len(full_nine),
        "compatible_mixed_cuts": [
            f"{row['chart']}:{row['label']}" for row in mixed_cuts
        ],
        "compatible_anchor_cuts": [
            f"{row['chart']}:{row['label']}" for row in anchor_cuts
        ],
        "block_ledger": kernel_records,
        "support_subsets_ruled_out": support_tests,
        "one_block_minimum_support": support_minimum,
        "full_row_support": len(coefficients),
        "lead_support": len(lead_coefficients),
        "remainder_column_support": len(remainder_coefficients),
        "lead_source_terms": len(lead),
        "remainder_source_terms": len(remainder),
        "all_remainder_columns_common_two_star": True,
        "lead_pairing": str(lead_pairing),
        "remainder_pairing": str(remainder_pairing),
        "rank_one_curvature_open_pairing": "-kappa",
        "single_physical_coefficient_row": False,
        "single_cross_chart_bianchi_normal_packet": True,
        "fixed_s_lower_rank": s_rank,
        "fixed_s_remainder_augmented_rank": s_augmented,
        "all_edge_lower_rank": all_rank,
        "all_edge_remainder_augmented_rank": all_augmented,
        "target_rewritten_but_not_killed": True,
        "minimal_row": coefficient_ledger(coefficients, positive, negative),
    }


def main():
    support_tests, support_minimum = audit_support_minimum()
    sample_word = (2, 0, 1, 2, 2, 2, 2, 2)
    kernel_records = audit_kernel_classification(sample_word)
    records = [
        audit_one_normalization(
            a, ell, kernel_records, support_tests, support_minimum
        )
        for a in two.COLORS for ell in two.COLORS
    ]
    ledger = {
        "normalizations": records,
        "interpretation": (
            "literal fixed-s common-triple coefficient of a multiplication-"
            "safe source identity; complete K6 vertex-potential kernel; "
            "minimal adjugate-compatible remainder tested against old rows"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    require(digest == EXPECTED_DIGEST, f"ledger digest changed: {digest}")

    print("OO common-triple adjugate remainder: PASS")
    print("fixed-s module: 7 independent K6 blocks, each 15 columns/rank 10/kernel 5")
    print("each block kernel is exactly alpha_uv=beta_u+beta_v, sum beta=0")
    print("normalized lead needs >=6 columns/block; curvature pair needs >=12")
    print("explicit row: 2 lead + 10 common-two-star remainder columns = 0")
    print("source reduction: 6 lead terms + 6 opposite remainder terms")
    print("integral obstruction pairing: lead=1, remainder=-1")
    print("all-nine provenance: one mixed cut/chart; R is the single Bianchi normal packet")
    print("rank-one curvature-open substitution: Lambda(kappa*R)=-kappa != 0")
    print("remainder raises old lower ranks 10->11 and 24->25")
    print("missing row: connection-to-diagonal nullhomotopy, not another Bianchi/jet")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
