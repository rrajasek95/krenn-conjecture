#!/usr/bin/env python3
"""Literal one-edge common-triple coefficient module for a curved OO pair.

The outgoing heads are normalized to 0 on ``pq`` and 1 on ``pr``.  For
every possible common p-colour ``a`` and fourth-site colour ``ell``, the
curvature word is

    (p,q,r,s,D) = (a,0,1,ell,2,2,2,2).

The two pair-chart presentations are expanded matching by matching.  After
the common-triple cut, the first coefficient at the remaining site ``s``
has seven physical edge columns.  Reinsertion by that same edge gives the
literal columns ``e * partial_e Haf(word)``.  These exhaust
multidegree-preserving linear/Koszul corrections with one fixed physical
edge at this coefficient level.

The desired curvature times the missing third anchor is tested in the
stronger source-realized form

    (A_pq(a,0) A_rs(1,ell) - A_pr(a,1) A_qs(0,ell))
       * Haf(D, 2,2,2,2).

No abstract row symbols are used: every feature is a labelled physical
perfect matching.  The checker also enlarges the seven columns to all 28
physical edge-reinsertion columns as a counterguard.
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
D = (4, 5, 6, 7)
PQ = (P, Q_SITE)
PR = (P, R)
EXPECTED_DIGEST = "c66fed782204351ab33d3a36ed2bff8b263043dd0fa0a8358ef61f92e84c751f"


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
S_EDGES = tuple(edge for edge in PHYSICAL_EDGES if S in edge)


def rational_rank(columns, features=None):
    """Rank of sparse matching-incidence columns over Q."""

    if features is None:
        features = tuple(sorted({feature for column in columns for feature in column}))
    matrix = [
        [Q(column.get(feature, 0)) for column in columns]
        for feature in features
    ]
    rank = 0
    number_columns = len(columns)
    for column in range(number_columns):
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


def colored_edge(edge, word):
    left, right = edge
    return left, right, word[left], word[right]


def colored_matching(matching, word):
    return tuple(sorted(colored_edge(edge, word) for edge in matching))


def edge_column(edge, word):
    """The literal reinsertion column e * partial_e Haf(word)."""

    return {
        colored_matching(matching, word): Q(1)
        for matching in PERFECT_MATCHINGS
        if edge in matching
    }


def chart_partition(matching, deleted_pair):
    return "direct" if tuple(sorted(deleted_pair)) in matching else "two-star"


def compatible_row_labels(a, ell):
    """Filter all 18 full-nine rows by the common-triple fine degree."""

    word = (a, 0, 1, ell, 2, 2, 2, 2)
    rows = []
    for chart in ("pq", "pr"):
        for i in COLORS:
            for j in COLORS:
                compatible = (i, j) == ((a, 0) if chart == "pq" else (a, 1))
                rows.append({
                    "chart": chart,
                    "label": f"{i}{j}",
                    "kind": "diagonal" if i == j else "offdiagonal",
                    "compatible": compatible,
                    # Although 00 or 11 can be the compatible labelled row,
                    # its common-triple coefficient has q-colour 0 and
                    # r-colour 1.  It is mixed and has no GHZ target.
                    "cut_target": int(compatible and len(set(word)) == 1),
                })
    selected = [row for row in rows if row["compatible"]]
    require(len(rows) == 18 and len(selected) == 2,
            "full-nine common-triple label filter changed")
    require({row["chart"] for row in selected} == {"pq", "pr"},
            "a chart disappeared from the common-triple cut")
    require(not any(row["cut_target"] for row in selected),
            "the distinct-head common-triple word acquired a target")
    return rows, selected


def target_vector(word):
    """Source realization of curvature times the pure-2 D anchor."""

    target = defaultdict(Q)
    for d_matching in matchings(D):
        positive = tuple(sorted((PQ, (R, S)) + d_matching))
        negative = tuple(sorted((PR, (Q_SITE, S)) + d_matching))
        target[colored_matching(positive, word)] += 1
        target[colored_matching(negative, word)] -= 1
    return {feature: value for feature, value in target.items() if value}


def explicit_s_cokernel_witness(target, word):
    """A two-feature covector killing every s-edge column but not target."""

    positive = colored_matching(
        tuple(sorted((PQ, (R, S), (4, 5), (6, 7)))), word
    )
    neutral = colored_matching(
        tuple(sorted(((P, 4), (Q_SITE, 5), (R, S), (6, 7)))), word
    )
    require(target.get(positive) == 1 and not target.get(neutral),
            "explicit target/neutral feature ledger changed")
    covector = {positive: Q(1), neutral: Q(-1)}
    for edge in S_EDGES:
        column = edge_column(edge, word)
        pairing = sum(
            coefficient * column.get(feature, 0)
            for feature, coefficient in covector.items()
        )
        require(pairing == 0, "explicit covector does not kill an s column")
    target_pairing = sum(
        coefficient * target.get(feature, 0)
        for feature, coefficient in covector.items()
    )
    require(target_pairing == 1,
            "explicit s-block cokernel witness lost the curvature target")
    return positive, neutral, target_pairing


def explicit_all_edge_cokernel_witness(target, word):
    """A six-matching covector killing all 28 edge-incidence columns."""

    signed_matchings = (
        (-1, ((0, 2), (1, 3), (4, 5), (6, 7))),
        (+1, ((0, 2), (1, 4), (3, 5), (6, 7))),
        (+1, ((0, 3), (1, 2), (4, 5), (6, 7))),
        (-1, ((0, 3), (1, 4), (2, 5), (6, 7))),
        (-1, ((0, 4), (1, 2), (3, 5), (6, 7))),
        (+1, ((0, 4), (1, 3), (2, 5), (6, 7))),
    )
    covector = {
        colored_matching(tuple(sorted(matching)), word): Q(sign)
        for sign, matching in signed_matchings
    }
    for edge in PHYSICAL_EDGES:
        column = edge_column(edge, word)
        pairing = sum(
            coefficient * column.get(feature, 0)
            for feature, coefficient in covector.items()
        )
        require(pairing == 0,
                "six-feature covector does not kill an all-edge column")
    target_pairing = sum(
        coefficient * target.get(feature, 0)
        for feature, coefficient in covector.items()
    )
    require(target_pairing == 1,
            "all-edge cokernel witness lost the curvature target")
    return covector, target_pairing


def audit_all_edge_kernel(word):
    """The seven edge-column relations are vertex potentials of sum zero."""

    columns = [edge_column(edge, word) for edge in PHYSICAL_EDGES]
    potential_vectors = []
    for distinguished in range(7):
        potential = [Q(0)] * 8
        potential[distinguished] = 1
        potential[7] = -1
        coefficients = {
            edge: potential[edge[0]] + potential[edge[1]]
            for edge in PHYSICAL_EDGES
        }
        combination = defaultdict(Q)
        for edge, column in zip(PHYSICAL_EDGES, columns, strict=True):
            for feature, value in column.items():
                combination[feature] += coefficients[edge] * value
        require(not {feature: value for feature, value in combination.items() if value},
                "a zero-sum vertex-potential relation failed")
        potential_vectors.append(tuple(coefficients[edge] for edge in PHYSICAL_EDGES))
    require(rational_rank([
        {index: value for index, value in enumerate(vector) if value}
        for vector in potential_vectors
    ]) == 7, "vertex-potential kernel basis lost independence")
    return len(potential_vectors)


def audit_one_normalization(a, ell):
    word = (a, 0, 1, ell, 2, 2, 2, 2)
    rows, selected = compatible_row_labels(a, ell)

    # Reconstruct each chart presentation matching by matching.  The direct
    # and two-star pieces are disjoint and have 15 and 90 terms.
    chart_counts = {}
    for chart, deleted_pair in (("pq", PQ), ("pr", PR)):
        direct = tuple(
            matching for matching in PERFECT_MATCHINGS
            if chart_partition(matching, deleted_pair) == "direct"
        )
        two_star = tuple(
            matching for matching in PERFECT_MATCHINGS
            if chart_partition(matching, deleted_pair) == "two-star"
        )
        require(len(direct) == 15 and len(two_star) == 90,
                "literal chart partition changed")
        require(set(direct).isdisjoint(two_star)
                and set(direct) | set(two_star) == set(PERFECT_MATCHINGS),
                "chart partition lost a physical matching")
        chart_counts[chart] = [len(direct), len(two_star)]

    colored_features = tuple(
        colored_matching(matching, word) for matching in PERFECT_MATCHINGS
    )
    require(len(set(colored_features)) == 105,
            "a fixed-word matching feature collision appeared")
    s_columns = [edge_column(edge, word) for edge in S_EDGES]
    target = target_vector(word)
    s_rank = rational_rank(s_columns)
    s_augmented_rank = rational_rank(s_columns + [target])
    require((s_rank, s_augmented_rank) == (7, 8),
            "one-edge residual-site cokernel changed")

    # Source-labelled copies from the two charts have only the tautological
    # comparison kernel: [C C] has rank 7 and kernel dimension 7.
    doubled_columns = s_columns + s_columns
    doubled_rank = rational_rank(doubled_columns)
    require(doubled_rank == 7 and len(doubled_columns) - doubled_rank == 7,
            "source-labelled chart-comparison kernel changed")

    # Strong counterguard: even if every physical edge is admitted as the
    # coefficient/reinsertion edge, the curvature-anchor vector is absent.
    all_columns = [edge_column(edge, word) for edge in PHYSICAL_EDGES]
    all_rank = rational_rank(all_columns)
    all_augmented_rank = rational_rank(all_columns + [target])
    require((all_rank, all_augmented_rank) == (21, 22),
            "all-edge enlargement unexpectedly contains the target")

    # The direct-double pieces of the literal normal packet are exactly the
    # two curvature-anchor halves.  They are projections of whole source
    # rows, not independently admissible generators.
    rs_column = edge_column((R, S), word)
    qs_column = edge_column((Q_SITE, S), word)
    pq_direct_rs = {
        colored_matching(matching, word): coefficient
        for matching, coefficient in (
            (matching, Q(1)) for matching in PERFECT_MATCHINGS
        )
        if (R, S) in matching and PQ in matching
    }
    pr_direct_qs = {
        colored_matching(matching, word): coefficient
        for matching, coefficient in (
            (matching, Q(1)) for matching in PERFECT_MATCHINGS
        )
        if (Q_SITE, S) in matching and PR in matching
    }
    require(set(pq_direct_rs) <= set(rs_column)
            and set(pr_direct_qs) <= set(qs_column),
            "curvature halves left their literal coefficient columns")
    require(len(pq_direct_rs) == len(pr_direct_qs) == 3,
            "direct-double anchor half should have three D matchings")
    reconstructed_target = defaultdict(Q, pq_direct_rs)
    for feature, coefficient in pr_direct_qs.items():
        reconstructed_target[feature] -= coefficient
    reconstructed_target = {
        feature: coefficient
        for feature, coefficient in reconstructed_target.items()
        if coefficient
    }
    require(reconstructed_target == target,
            "normal-packet direct-double projection changed")

    # Matching-by-matching chart comparison is the literal power-free
    # connection; differentiating at s gives its normal companion.
    for edge in S_EDGES:
        column = edge_column(edge, word)
        pq_direct = {
            feature: value for feature, value in column.items()
            if PQ in tuple((item[0], item[1]) for item in feature)
        }
        pr_direct = {
            feature: value for feature, value in column.items()
            if PR in tuple((item[0], item[1]) for item in feature)
        }
        pq_stars = {feature: value for feature, value in column.items()
                    if feature not in pq_direct}
        pr_stars = {feature: value for feature, value in column.items()
                    if feature not in pr_direct}
        connection = defaultdict(Q)
        for feature, value in pq_direct.items():
            connection[feature] += value
        for feature, value in pq_stars.items():
            connection[feature] += value
        for feature, value in pr_direct.items():
            connection[feature] -= value
        for feature, value in pr_stars.items():
            connection[feature] -= value
        require(not {feature: value for feature, value in connection.items() if value},
                "literal differentiated chart connection failed")

    positive, neutral, target_pairing = explicit_s_cokernel_witness(target, word)
    all_covector, all_target_pairing = explicit_all_edge_cokernel_witness(
        target, word
    )
    all_kernel_dimension = audit_all_edge_kernel(word)
    doubled_all_rank = rational_rank(all_columns + all_columns)
    require(doubled_all_rank == 21
            and 2 * len(all_columns) - doubled_all_rank == 35,
            "doubled all-edge source-labelled kernel changed")
    compatible_summary = [
        f"{row['chart']}:{row['label']}:{row['kind']}"
        for row in selected
    ]
    return {
        "a": a,
        "ell": ell,
        "word": "".join(map(str, word)),
        "full_nine_rows_considered": len(rows),
        "compatible_rows": compatible_summary,
        "compatible_cut_target_rank": sum(row["cut_target"] for row in selected),
        "chart_direct_two_star_terms": chart_counts,
        "s_edge_columns": len(s_columns),
        "s_edge_rank": s_rank,
        "s_edge_augmented_rank": s_augmented_rank,
        "s_edge_cokernel_dimension": len(PERFECT_MATCHINGS) - s_rank,
        "doubled_chart_columns": len(doubled_columns),
        "doubled_chart_rank": doubled_rank,
        "doubled_chart_kernel": len(doubled_columns) - doubled_rank,
        "all_edge_columns": len(all_columns),
        "all_edge_rank": all_rank,
        "all_edge_augmented_rank": all_augmented_rank,
        "all_edge_kernel_dimension": all_kernel_dimension,
        "all_edge_cokernel_dimension": len(PERFECT_MATCHINGS) - all_rank,
        "doubled_all_edge_kernel": 2 * len(all_columns) - doubled_all_rank,
        "curvature_anchor_terms": len(target),
        "explicit_cokernel_pairing": str(target_pairing),
        "all_edge_cokernel_support": len(all_covector),
        "all_edge_cokernel_pairing": str(all_target_pairing),
        "explicit_positive_matching": [list(edge) for edge in positive],
        "explicit_neutral_matching": [list(edge) for edge in neutral],
    }


def main():
    require(len(PERFECT_MATCHINGS) == 105, "K8 matching count changed")
    require(len(PHYSICAL_EDGES) == 28 and len(S_EDGES) == 7,
            "physical edge census changed")
    records = [
        audit_one_normalization(a, ell)
        for a in COLORS
        for ell in COLORS
    ]
    require({tuple(record["compatible_rows"]) for record in records} == {
        ("pq:00:diagonal", "pr:01:offdiagonal"),
        ("pq:10:offdiagonal", "pr:11:diagonal"),
        ("pq:20:offdiagonal", "pr:21:offdiagonal"),
    }, "compatible full-nine row types changed")
    ledger = {
        "normalizations": records,
        "physical_matchings": len(PERFECT_MATCHINGS),
        "interpretation": (
            "literal common-triple first-s coefficient module; "
            "one physical-edge reinsertion; source-realized missing anchor"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    require(digest == EXPECTED_DIGEST, f"ledger digest changed: {digest}")
    print("OO common-triple one-edge coefficient cokernel: PASS")
    print("normalizations: 9 (tail colour a and fourth-site colour ell)")
    print("18 full-nine rows/type; compatible rows/type: 2; cut target rank: 0")
    print("residual-site block: 7 columns, rank 7, target-augmented rank 8")
    print("two source-labelled chart copies: 14 columns, rank 7, kernel 7")
    print("all-edge counterguard: 28 columns, rank 21, kernel 7, cokernel 84")
    print("all-edge target-augmented rank 22; explicit six-feature pairing 1")
    print("explicit two-feature cokernel pairing with curvature anchor: 1")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
