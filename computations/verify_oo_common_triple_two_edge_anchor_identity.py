#!/usr/bin/env python3
"""Exact two-edge common-triple OO coefficient/anchor module.

This is the next coefficient layer after
``verify_oo_common_triple_one_edge_syzygy_cokernel.py``.  It keeps literal
matching monomials and labelled pq/pr row copies.  For the distinct-head
word (a,0,1,ell,2,2,2,2), a mixed column is

    e*f * partial_e partial_f Haf(word)

for a disjoint two-edge partial matching containing an edge through the
remaining site s.  The three partial matchings on p,q,r,s also multiply the
literal four-site diagonal row ``Haf(D,2^4)-X2_D``.  This retains the target
instead of replacing the diagonal row by an abstract symbol.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json


Q = Fraction
COLORS = (0, 1, 2)
SITES = tuple(range(8))
P, Q_SITE, R, S = 0, 1, 2, 3
ENDPOINTS = (P, Q_SITE, R, S)
D = (4, 5, 6, 7)
PQ = (P, Q_SITE)
PR = (P, R)
EXPECTED_DIGEST = "cc2f54e38019ad5fbff97384185e7132a245edd3716d740f054b21ef4630950d"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], start=1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(rest):
            answer.append((tuple(sorted((first, second))),) + tail)
    return tuple(tuple(sorted(matching)) for matching in answer)


PERFECT_MATCHINGS = tuple(sorted(matchings(SITES)))
PHYSICAL_EDGES = tuple(combinations(SITES, 2))
ENDPOINT_MATCHINGS = tuple(sorted(matchings(ENDPOINTS)))
S_TWO_EDGE_PARTIALS = tuple(sorted({
    tuple(sorted((first, second)))
    for first, second in combinations(PHYSICAL_EDGES, 2)
    if set(first).isdisjoint(second) and (S in first or S in second)
}))
ALL_TWO_EDGE_PARTIALS = tuple(sorted({
    tuple(sorted((first, second)))
    for first, second in combinations(PHYSICAL_EDGES, 2)
    if set(first).isdisjoint(second)
}))


def colored_edge(edge, word):
    left, right = edge
    return left, right, word[left], word[right]


def colored_matching(matching, word):
    return tuple(sorted(colored_edge(edge, word) for edge in matching))


def source_feature(matching, word):
    return "source", colored_matching(matching, word)


def target_feature(partial, word):
    return (
        "target",
        tuple(sorted(colored_edge(edge, word) for edge in partial)),
        "X2_D",
    )


def mixed_second_column(partial, word):
    """Literal ef * d_e d_f of the fixed-word hafnian row."""

    require(len(partial) == 2 and set(partial[0]).isdisjoint(partial[1]),
            "second coefficient requires a two-edge partial matching")
    result = {
        source_feature(matching, word): Q(1)
        for matching in PERFECT_MATCHINGS
        if all(edge in matching for edge in partial)
    }
    require(len(result) == 3,
            "a two-edge coefficient should have three completions on K4")
    return result


def diagonal_anchor_column(partial, word):
    """partial * (Haf(D,2^4) - X2_D), expanded literally."""

    require(partial in ENDPOINT_MATCHINGS,
            "a compatible diagonal-anchor multiplier must cover p,q,r,s")
    result = {
        source_feature(tuple(sorted(partial + d_matching)), word): Q(1)
        for d_matching in matchings(D)
    }
    result[target_feature(partial, word)] = Q(-1)
    require(len(result) == 4, "diagonal anchor column size changed")
    return result


def add_scaled(target, column, scalar):
    for feature, value in column.items():
        target[feature] += Q(scalar) * value
        if not target[feature]:
            del target[feature]


def rational_rank(columns):
    features = tuple(sorted(
        {feature for column in columns for feature in column}, key=repr
    ))
    matrix = [
        [Q(column.get(feature, 0)) for column in columns]
        for feature in features
    ]
    rank = 0
    pivot_columns = []
    pivot_rows = []
    for column in range(len(columns)):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        feature_list = list(features)
        feature_list[rank], feature_list[pivot] = feature_list[pivot], feature_list[rank]
        features = tuple(feature_list)
        pivot_value = matrix[rank][column]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(
                    matrix[row], matrix[rank], strict=True
                )
            ]
        pivot_columns.append(column)
        pivot_rows.append(features[rank])
        rank += 1
    return rank, len(features), tuple(pivot_columns), tuple(pivot_rows)


def compatible_rows(a, ell):
    """Audit all 18 full-nine labels and the two diagonal-anchor cuts."""

    word = (a, 0, 1, ell, 2, 2, 2, 2)
    records = []
    for chart in ("pq", "pr"):
        mixed_label = (a, 0) if chart == "pq" else (a, 1)
        for i in COLORS:
            for j in COLORS:
                records.append({
                    "chart": chart,
                    "label": f"{i}{j}",
                    "kind": "diagonal" if i == j else "offdiagonal",
                    "mixed_cut": (i, j) == mixed_label,
                    "missing_anchor_cut": (i, j) == (2, 2),
                    "mixed_target": int(
                        (i, j) == mixed_label and len(set(word)) == 1
                    ),
                })
    require(len(records) == 18, "full-nine label count changed")
    require(sum(record["mixed_cut"] for record in records) == 2,
            "common-triple mixed row filter changed")
    require(sum(record["missing_anchor_cut"] for record in records) == 2,
            "the two labelled 22 anchor rows disappeared")
    require(not any(record["mixed_target"] for record in records),
            "the distinct-head mixed cut acquired a GHZ target")
    return records


def chart_sector(partial, deleted_pair):
    return "direct" if tuple(sorted(deleted_pair)) in partial else "two-star"


def curvature_target(word):
    positive = ((P, Q_SITE), (R, S))
    negative = ((P, R), (Q_SITE, S))
    return {
        target_feature(tuple(sorted(positive)), word): Q(1),
        target_feature(tuple(sorted(negative)), word): Q(-1),
    }


def audit_integral_identity(columns, word):
    m_pq_rs = tuple(sorted(((P, Q_SITE), (R, S))))
    m_pr_qs = tuple(sorted(((P, R), (Q_SITE, S))))
    coefficients = {
        ("mixed", "pq", m_pq_rs): Q(1),
        ("mixed", "pr", m_pr_qs): Q(-1),
        ("diagonal", "pq", m_pq_rs): Q(-1),
        ("diagonal", "pr", m_pr_qs): Q(1),
    }
    boundary = defaultdict(Q)
    for label, coefficient in coefficients.items():
        add_scaled(boundary, columns[label], coefficient)
    expected = curvature_target(word)
    require(dict(boundary) == expected,
            "four-column integral curvature-anchor identity changed")
    require(all(abs(value) == 1 for value in coefficients.values()),
            "integral identity lost unit coefficients")
    return coefficients, expected


def audit_one_normalization(a, ell):
    word = (a, 0, 1, ell, 2, 2, 2, 2)
    row_records = compatible_rows(a, ell)
    require(len(set(colored_matching(matching, word)
                    for matching in PERFECT_MATCHINGS)) == 105,
            "fixed-word source features collided")

    # Literal labelled columns.  Each chart sees the same source polynomial,
    # but the copies remain distinct in the domain.
    columns = {}
    for chart in ("pq", "pr"):
        for partial in S_TWO_EDGE_PARTIALS:
            columns[("mixed", chart, partial)] = mixed_second_column(
                partial, word
            )
        for partial in ENDPOINT_MATCHINGS:
            columns[("diagonal", chart, partial)] = diagonal_anchor_column(
                partial, word
            )

    mixed_one_chart = [
        columns[("mixed", "pq", partial)]
        for partial in S_TWO_EDGE_PARTIALS
    ]
    mixed_two_chart = mixed_one_chart + [
        columns[("mixed", "pr", partial)]
        for partial in S_TWO_EDGE_PARTIALS
    ]
    full_columns = list(columns.values())
    target = curvature_target(word)

    mixed_rank, mixed_features, _, _ = rational_rank(mixed_one_chart)
    doubled_mixed_rank, _, _, _ = rational_rank(mixed_two_chart)
    mixed_target_rank, _, _, _ = rational_rank(mixed_one_chart + [target])
    full_rank, full_features, pivot_columns, pivot_rows = rational_rank(full_columns)
    full_target_rank, _, _, _ = rational_rank(full_columns + [target])
    require(
        (len(mixed_one_chart), mixed_rank, mixed_features,
         mixed_target_rank) == (105, 70, 105, 71),
        "fixed-s mixed second-coefficient ledger changed",
    )
    require(doubled_mixed_rank == 70,
            "the labelled chart copy changed the mixed image")
    require(
        (len(full_columns), full_rank, full_features, full_target_rank)
        == (216, 73, 108, 73),
        "diagonal-augmented two-edge module ledger changed",
    )

    identity, expected_target = audit_integral_identity(columns, word)

    # The selected curvature halves occupy the expected literal chart
    # sectors.  The third endpoint pairing is two-star in both charts.
    m_pq_rs, m_pr_qs, m_ps_qr = ENDPOINT_MATCHINGS
    require(
        (chart_sector(m_pq_rs, PQ), chart_sector(m_pq_rs, PR))
        == ("direct", "two-star"),
        "pq|rs source-sector placement changed",
    )
    require(
        (chart_sector(m_pr_qs, PQ), chart_sector(m_pr_qs, PR))
        == ("two-star", "direct"),
        "pr|qs source-sector placement changed",
    )
    require(
        (chart_sector(m_ps_qr, PQ), chart_sector(m_ps_qr, PR))
        == ("two-star", "two-star"),
        "ps|qr source-sector placement changed",
    )

    # Larger exact counterguard: admit every nonzero disjoint two-edge
    # coefficient, not only those through s.
    all_columns = {}
    for chart in ("pq", "pr"):
        for partial in ALL_TWO_EDGE_PARTIALS:
            all_columns[("mixed", chart, partial)] = mixed_second_column(
                partial, word
            )
        for partial in ENDPOINT_MATCHINGS:
            all_columns[("diagonal", chart, partial)] = diagonal_anchor_column(
                partial, word
            )
    all_mixed_one = [
        all_columns[("mixed", "pq", partial)]
        for partial in ALL_TWO_EDGE_PARTIALS
    ]
    all_full = list(all_columns.values())
    all_mixed_rank, _, _, _ = rational_rank(all_mixed_one)
    all_full_rank, all_features, _, _ = rational_rank(all_full)
    all_target_rank, _, _, _ = rational_rank(all_full + [target])
    require(
        (len(all_mixed_one), all_mixed_rank) == (210, 91),
        "all-two-edge mixed rank changed",
    )
    require(
        (len(all_full), all_full_rank, all_features, all_target_rank)
        == (426, 94, 108, 94),
        "all-two-edge diagonal-augmented ledger changed",
    )

    identity_ledger = [
        {
            "coefficient": str(value),
            "kind": label[0],
            "chart": label[1],
            "partial": [list(edge) for edge in label[2]],
        }
        for label, value in identity.items()
    ]
    compatible = [
        f"{record['chart']}:{record['label']}:{record['kind']}"
        for record in row_records if record["mixed_cut"]
    ]
    anchors = [
        f"{record['chart']}:{record['label']}"
        for record in row_records if record["missing_anchor_cut"]
    ]
    pivot_digest = sha256(repr((pivot_columns, pivot_rows)).encode()).hexdigest()
    return {
        "a": a,
        "ell": ell,
        "word": "".join(map(str, word)),
        "full_nine_rows_considered": len(row_records),
        "compatible_mixed_rows": compatible,
        "compatible_diagonal_anchors": anchors,
        "mixed_cut_target_rank": sum(
            record["mixed_target"] for record in row_records
        ),
        "s_two_edge_partials": len(S_TWO_EDGE_PARTIALS),
        "mixed_one_chart_rank": mixed_rank,
        "mixed_one_chart_kernel": len(mixed_one_chart) - mixed_rank,
        "mixed_two_chart_rank": doubled_mixed_rank,
        "mixed_two_chart_kernel": len(mixed_two_chart) - doubled_mixed_rank,
        "mixed_target_augmented_rank": mixed_target_rank,
        "full_columns": len(full_columns),
        "full_rank": full_rank,
        "full_kernel": len(full_columns) - full_rank,
        "full_feature_dimension": full_features,
        "full_cokernel": full_features - full_rank,
        "full_target_augmented_rank": full_target_rank,
        "curvature_target_terms": len(expected_target),
        "integral_identity": identity_ledger,
        "full_pivot_digest": pivot_digest,
        "all_two_edge_partials": len(ALL_TWO_EDGE_PARTIALS),
        "all_mixed_rank": all_mixed_rank,
        "all_full_columns": len(all_full),
        "all_full_rank": all_full_rank,
        "all_full_kernel": len(all_full) - all_full_rank,
        "all_full_cokernel": all_features - all_full_rank,
        "all_target_augmented_rank": all_target_rank,
    }


def main():
    require(len(PERFECT_MATCHINGS) == 105, "K8 matching count changed")
    require(len(ENDPOINT_MATCHINGS) == 3,
            "four-endpoint matching count changed")
    require(len(S_TWO_EDGE_PARTIALS) == 105,
            "fixed-s two-edge partial count changed")
    require(len(ALL_TWO_EDGE_PARTIALS) == 210,
            "all two-edge partial count changed")

    records = [
        audit_one_normalization(a, ell)
        for a in COLORS
        for ell in COLORS
    ]
    require({tuple(record["compatible_mixed_rows"]) for record in records} == {
        ("pq:00:diagonal", "pr:01:offdiagonal"),
        ("pq:10:offdiagonal", "pr:11:diagonal"),
        ("pq:20:offdiagonal", "pr:21:offdiagonal"),
    }, "compatible common-triple row types changed")
    require({tuple(record["compatible_diagonal_anchors"])
             for record in records} == {("pq:22", "pr:22")},
            "missing diagonal anchor labels changed")
    ledger = {
        "normalizations": records,
        "interpretation": (
            "literal common-triple second coefficient/reinsertion module; "
            "labelled pq/pr copies; four-site 22 anchors retained"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    require(digest == EXPECTED_DIGEST, f"ledger digest changed: {digest}")

    print("OO common-triple two-edge anchor identity: PASS")
    print("normalizations: 9; full-nine rows considered/type: 18")
    print("fixed-s mixed: 105 columns/chart, rank 70; target absent (rank 71)")
    print("with two labelled 22 anchors: 216 columns, rank 73, cokernel 35")
    print("curvature*X2 target lies in image: target-augmented rank 73")
    print("integral identity: +M_pq[pq|rs]-M_pr[pr|qs]"
          "-D_pq[pq|rs]+D_pr[pr|qs]")
    print("all-two-edge guard: 426 columns, rank 94, cokernel 14")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
