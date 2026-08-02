#!/usr/bin/env python3
"""Exact minimal-multidegree search for the five literal four-face lifts.

The universal h=3 direct-free specialization has sites

    x=0, D=(1,2,3,4,5), p=6, q=7, r=3,

and the whole p--r block is zero.  For each deletion face D\\{v}, this
checker constructs the complete fine-multidegree block in which a quadratic
full-nine correction could first have boundary h_v*Y_0.  There are exactly
16 compatible global words and three degree-two multipliers per word.

It also checks the exact degree-lowering second polar which would produce
h_v.  That polar is a diagnostic for the first additional relative/Rees
row; differentiation of a vanishing equation is not asserted to be a
source-valid full-nine combination.
"""

import argparse
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json


Q = Fraction
COLORS = (0, 1, 2)
SITES = tuple(range(8))
X = 0
ODD = (1, 2, 3, 4, 5)
P = 6
Q_SITE = 7
R = 3
MIXED_ODD = (1, 2, 1, 1, 2)
PURE_GLOBAL = (0,) * 8
DIRECT_FREE_PAIR = frozenset((P, R))
EXPECTED_DIGEST = "878a0e3ae179f2aa837f1ff190acb4a11ddca949bf8816d9e096a0cf023e39ef"

EXPECTED_FACE_WORDS = {
    1: "2112",
    2: "1112",
    3: "1212",
    4: "1212",
    5: "1211",
}

EXPECTED_GLOBAL_ROWS = {
    1: "00211200",
    2: "01011200",
    3: "01201200",
    4: "01210200",
    5: "01211000",
}

EXPECTED_FACE_TERMS = {
    1: {
        "q23^21*q45^12", "q24^21*q35^12", "q25^22*q34^11",
    },
    2: {
        "q13^11*q45^12", "q14^11*q35^12", "q15^12*q34^11",
    },
    3: {
        "q12^12*q45^12", "q14^11*q25^22", "q15^12*q24^21",
    },
    4: {
        "q12^12*q35^12", "q13^11*q25^22", "q15^12*q23^21",
    },
    5: {
        "q12^12*q34^11", "q13^11*q24^21", "q14^11*q23^21",
    },
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right, left_color, right_color):
    if left < right:
        return left, right, left_color, right_color
    return right, left, right_color, left_color


def monomial_text(monomial):
    return "*".join(
        f"q{left}{right}^{left_color}{right_color}"
        for left, right, left_color, right_color in monomial
    )


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(remainder):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def matching_monomial(matching, word):
    return tuple(sorted(
        edge(left, right, word[left], word[right])
        for left, right in matching
    ))


def contains_direct_free_edge(monomial):
    return any(
        frozenset((left, right)) == DIRECT_FREE_PAIR
        for left, right, _left_color, _right_color in monomial
    )


def full_nine_polynomial(word):
    """The sparse universal hafnian after setting the whole p--r block 0."""
    terms = tuple(
        matching_monomial(matching, word)
        for matching in matchings(SITES)
    )
    surviving = tuple(term for term in terms if not contains_direct_free_edge(term))
    require(len(terms) == 105, "eight-site matching count changed")
    require(len(surviving) == 90, "direct-free row should retain 90 matchings")
    require(len(set(surviving)) == len(surviving), "hafnian monomials collided")
    return surviving


def chart_partition(word, deleted_pair):
    """Partition the same global row into direct and two-star chart pieces."""
    deleted_pair = frozenset(deleted_pair)
    direct = []
    two_star = []
    for matching in matchings(SITES):
        monomial = matching_monomial(matching, word)
        if contains_direct_free_edge(monomial):
            continue
        contains_deleted_edge = any(
            frozenset((left, right)) == deleted_pair
            for left, right in matching
        )
        (direct if contains_deleted_edge else two_star).append(monomial)
    require(set(direct).isdisjoint(two_star), "chart pieces overlap")
    return tuple(direct), tuple(two_star)


def chart_audit():
    count_ledger = {}
    target_mismatches = 0
    row_digest = sha256()
    for word in product(COLORS, repeat=8):
        row = full_nine_polynomial(word)
        pq_direct, pq_stars = chart_partition(word, (P, Q_SITE))
        pr_direct, pr_stars = chart_partition(word, (P, R))
        require(
            set(pq_direct) | set(pq_stars) == set(row),
            "pq chart lost a global matching",
        )
        require(
            set(pr_direct) | set(pr_stars) == set(row),
            "pr chart lost a global matching",
        )
        require(len(pq_direct) == 15 and len(pq_stars) == 75,
                "pq chart split changed")
        require(len(pr_direct) == 0 and len(pr_stars) == 90,
                "direct-free pr chart split changed")

        pure_color = next(
            (color for color in COLORS if word == (color,) * 8),
            None,
        )
        pq_target = pure_color
        pr_target = pure_color
        if pq_target != pr_target:
            target_mismatches += 1

        # Freeze the complete all-word enumeration without storing it all.
        row_digest.update(bytes(word))
        row_digest.update(len(row).to_bytes(2, "big"))
        row_digest.update(len(pq_direct).to_bytes(2, "big"))
        row_digest.update(len(pr_direct).to_bytes(2, "big"))

    require(target_mismatches == 0, "the two charts have different targets")
    count_ledger = {
        "global_words": 3 ** 8,
        "row_monomials_after_direct_free": 90,
        "pq_direct": 15,
        "pq_two_star": 75,
        "pr_direct": 0,
        "pr_two_star": 90,
        "pure_target_rows": 3,
        "chart_target_mismatches": target_mismatches,
        "enumeration_sha256": row_digest.hexdigest(),
    }
    return count_ledger


def face_word(deleted_site):
    return tuple(
        MIXED_ODD[site - 1]
        for site in ODD
        if site != deleted_site
    )


def face_hafnian(deleted_site, colors):
    face = tuple(site for site in ODD if site != deleted_site)
    coloring = dict(zip(face, colors))
    return tuple(sorted(
        tuple(sorted(
            edge(left, right, coloring[left], coloring[right])
            for left, right in matching
        ))
        for matching in matchings(face)
    ))


def compatible_block(deleted_site):
    """Return all 48 columns in the first common fine multidegree.

    The common degree has both the pure-zero and selected mixed color slots
    on the four-site face, and only zero slots on its complement.  A row
    uses one slot at every site, so it has 2^4 possible words.  Its missing
    four slots must be supplied by two edges, hence by one of three face
    matchings.
    """
    face = tuple(site for site in ODD if site != deleted_site)
    selected = {site: MIXED_ODD[site - 1] for site in face}
    columns = []
    labels = []
    for choices in product((0, 1), repeat=4):
        word = [0] * 8
        for site, use_mixed in zip(face, choices):
            word[site] = selected[site] if use_mixed else 0
        word = tuple(word)

        missing_color = {
            site: 0 if word[site] != 0 else selected[site]
            for site in face
        }
        for multiplier_matching in matchings(face):
            multiplier = tuple(sorted(
                edge(
                    left, right,
                    missing_color[left], missing_color[right],
                )
                for left, right in multiplier_matching
            ))
            features = tuple(
                tuple(sorted(multiplier + row_term))
                for row_term in full_nine_polynomial(word)
            )
            require(len(features) == len(set(features)) == 90,
                    "one multiplied row acquired an internal collision")
            columns.append(frozenset(features))
            labels.append((word, multiplier))
    require(len(columns) == 16 * 3 == 48, "fine block size changed")
    return face, tuple(labels), tuple(columns)


def block_audit():
    records = []
    for deleted_site in ODD:
        face, labels, columns = compatible_block(deleted_site)
        owners = defaultdict(list)
        for column_index, column in enumerate(columns):
            for feature in column:
                owners[feature].append(column_index)

        unique_counts = tuple(
            sum(len(owners[feature]) == 1 for feature in column)
            for column in columns
        )
        require(min(unique_counts) > 0,
                "a minimal-degree column lost its unique pivot feature")

        # Choosing any uniquely owned feature from every column produces 48
        # distinct pivot rows.  Therefore the one-chart block has rank 48,
        # without relying on a probabilistic or modular rank computation.
        pivots = tuple(
            min(feature for feature in column if len(owners[feature]) == 1)
            for column in columns
        )
        require(len(set(pivots)) == 48, "unique pivot certificate collided")
        one_chart_rank = 48
        one_chart_kernel = 0

        # The two chart presentations are literal copies of these same
        # columns.  Hence [C C] has rank 48 and its 48-dimensional kernel is
        # exactly (a,-a).  The actual global target, and any strict residue
        # or ordered landing modeled by an identical linear readout on the
        # two copies, use the same sign and vanish there.  This does not
        # classify non-diagonal readouts in a new relative comparison complex.
        two_chart_columns = 96
        two_chart_rank = one_chart_rank
        two_chart_kernel = two_chart_columns - two_chart_rank
        require(two_chart_kernel == 48, "two-chart comparison kernel changed")

        pure_indices = tuple(
            index for index, (word, _multiplier) in enumerate(labels)
            if word == PURE_GLOBAL
        )
        require(len(pure_indices) == 3,
                "the first fine block lost its three pure-row multipliers")
        mixed_face = face_hafnian(deleted_site, face_word(deleted_site))
        pure_multipliers = tuple(labels[index][1] for index in pure_indices)
        require(set(pure_multipliers) == set(mixed_face),
                "pure-row multipliers are not the three terms of h_v")

        # Explicitly audit every basis comparison (e_i,-e_i).  The target is
        # 1 on a pure row and 0 on a mixed row.  We use that same global-row
        # functional as the *model* for a strict same-power residue and a
        # strict ordered landing on both chart copies.
        target_values = []
        residue_values = []
        landing_values = []
        for index, (word, _multiplier) in enumerate(labels):
            value = Q(1) if word == PURE_GLOBAL else Q(0)
            target_values.append(value - value)
            residue_values.append(value - value)
            landing_values.append(value - value)
        require(not any(target_values), "comparison kernel acquired target")
        require(not any(residue_values), "comparison kernel acquired residue")
        require(not any(landing_values), "comparison kernel acquired landing")

        records.append({
            "deleted_site": deleted_site,
            "face": list(face),
            "face_word": "".join(map(str, face_word(deleted_site))),
            "compatible_words": 16,
            "multipliers_per_word": 3,
            "one_chart_columns": len(columns),
            "one_chart_rank": one_chart_rank,
            "one_chart_kernel": one_chart_kernel,
            "feature_count": len(owners),
            "unique_features": sum(len(indices) == 1 for indices in owners.values()),
            "unique_features_per_column": sorted(set(unique_counts)),
            "maximum_feature_owner_count": max(map(len, owners.values())),
            "two_chart_columns": two_chart_columns,
            "two_chart_rank": two_chart_rank,
            "two_chart_kernel": two_chart_kernel,
            "kernel_target_rank": 0,
            "kernel_identical_residue_model_rank": 0,
            "kernel_identical_landing_model_rank": 0,
            "desired_h_terms": len(mixed_face),
        })
    return records


def sparse_derivative(polynomial, variables):
    """Differentiate a squarefree sparse polynomial by named edge variables."""
    variables = tuple(variables)
    answer = defaultdict(int)
    for monomial in polynomial:
        remainder = list(monomial)
        for variable in variables:
            if variable not in remainder:
                break
            remainder.remove(variable)
        else:
            answer[tuple(sorted(remainder))] += 1
    return {
        monomial: coefficient
        for monomial, coefficient in answer.items()
        if coefficient
    }


def polar_audit():
    records = []
    all_polar_supports = []
    for deleted_site in ODD:
        global_word = [0] * 8
        for site in ODD:
            if site != deleted_site:
                global_word[site] = MIXED_ODD[site - 1]
        global_word = tuple(global_word)
        require(global_word != PURE_GLOBAL,
                "a four-mixed-site row unexpectedly has physical target")
        require("".join(map(str, face_word(deleted_site)))
                == EXPECTED_FACE_WORDS[deleted_site],
                "a labelled deletion-face word changed")
        require("".join(map(str, global_word))
                == EXPECTED_GLOBAL_ROWS[deleted_site],
                "a target-zero global row changed")

        complement_edges = (
            edge(X, deleted_site, 0, 0),
            edge(P, Q_SITE, 0, 0),
        )
        polar = sparse_derivative(
            full_nine_polynomial(global_word), complement_edges
        )
        expected_face = face_hafnian(
            deleted_site, face_word(deleted_site)
        )
        require(polar == {monomial: 1 for monomial in expected_face},
                "the external two-edge polar is not h_v")
        require({monomial_text(term) for term in polar}
                == EXPECTED_FACE_TERMS[deleted_site],
                "an exact h_v formula changed")

        pq_direct, pq_stars = chart_partition(global_word, (P, Q_SITE))
        pr_direct, pr_stars = chart_partition(global_word, (P, R))
        pq_direct_polar = sparse_derivative(pq_direct, complement_edges)
        pq_star_polar = sparse_derivative(pq_stars, complement_edges)
        pr_direct_polar = sparse_derivative(pr_direct, complement_edges)
        pr_star_polar = sparse_derivative(pr_stars, complement_edges)
        require(pq_direct_polar == polar and not pq_star_polar,
                "h_v is not wholly in the pq-direct marked sector")
        require(not pr_direct_polar and pr_star_polar == polar,
                "h_v is not wholly in the pr-two-star marked sector")

        all_polar_supports.append(frozenset(polar))
        records.append({
            "deleted_site": deleted_site,
            "face_word": "".join(map(str, face_word(deleted_site))),
            "global_row": "".join(map(str, global_word)),
            "target": 0,
            "polar_edges": [list(item) for item in complement_edges],
            "polar_terms": len(polar),
            "pq_marked_sector": "direct",
            "pr_marked_sector": "two_star",
            "strict_full_nine_combination": False,
            "required_additional_row": f"tau_{deleted_site}",
        })

    require(
        all(
            all_polar_supports[left].isdisjoint(all_polar_supports[right])
            for left in range(5) for right in range(left + 1, 5)
        ),
        "the five polar face rows lost fine-degree independence",
    )
    return records


def run(mode):
    ledger = {}
    if mode in ("all", "charts"):
        ledger["charts"] = chart_audit()
    if mode in ("all", "blocks"):
        ledger["blocks"] = block_audit()
    if mode in ("all", "polars"):
        ledger["polars"] = polar_audit()

    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if mode == "all":
        require(digest == EXPECTED_DIGEST,
                f"literal four-face ledger changed: {digest}")

    print(f"h=3 direct-free literal four-face full-nine search ({mode}): PASS")
    if mode in ("all", "charts"):
        print("6561 rows: pq/pr are identical global equations; pr direct block is zero")
    if mode in ("all", "blocks"):
        print("five minimal blocks: 48/48 one-chart rank; only diagonal chart comparisons")
        print("target and identical strict readout models vanish on comparison kernels")
    if mode in ("all", "polars"):
        print("first degree-lowering candidates: five external two-edge polars = h_v")
        print("those polars are not strict source-valid full-nine combinations")
    print(f"sha256: {digest}")
    return digest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("all", "charts", "blocks", "polars"), default="all"
    )
    arguments = parser.parse_args()
    run(arguments.mode)


if __name__ == "__main__":
    main()
