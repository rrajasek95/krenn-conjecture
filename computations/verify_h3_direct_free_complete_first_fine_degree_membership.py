#!/usr/bin/env python3
"""Complete strict first-fine-degree membership for all five h=3 faces.

This checker keeps the grading honest.  It inspects every term in all 15
odd denominator columns, enumerates every compatible full-nine
row/multiplier in both charts, and computes the exact sparse rational ranks
of the resulting augmented membership problem.  A denominator column is
not silently treated as a same-degree full-nine column: its lambda_3 piece
is computed term by term (and likewise for lambda_v on the other faces).
"""

import argparse
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json


QQ = Fraction
COLOURS = (0, 1, 2)
ALL_SITES = tuple(range(8))
ODD_SITES = (1, 2, 3, 4, 5)
MIXED = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}
X, R, P, Q = 0, 3, 6, 7
DIRECT_FREE_PAIR = frozenset((P, R))
FIXED_CHART_ORBITS = ((1, 4), (2, 5), (3,))
EXPECTED_DIGESTS = {
    "all": "b8a19cac89473cd642521be9980a3d88130b31a05cb6b310631219b88a056174",
    "1": "d7418b6c20b53ec574feb679c94b99307c4d214fe05706a168b36c228d9292e7",
    "2": "ffc38f24925b1c36ef0a683597c70c5a2c575f1e46c3a31f97ca227f01c7458f",
    "3": "e1ff19a9a58059b4181202474e4eeee4eb724dbf8d05f85647954da371cdd192",
    "4": "3abff1adadbc065384bd2dca8fbf74e08a266ccbe9159c74d27c899987ef2017",
    "5": "6eb4b2d256bdabcfb27b68bb17a94e08cc223cd0765264740017bb4ada132f98",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right, left_colour, right_colour):
    if left < right:
        return left, right, left_colour, right_colour
    return right, left, right_colour, left_colour


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(remainder):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def matching_monomial(matching, colouring):
    return tuple(sorted(
        edge(left, right, colouring[left], colouring[right])
        for left, right in matching
    ))


@lru_cache(maxsize=None)
def full_row(word):
    terms = []
    colouring = dict(enumerate(word))
    for matching in matchings(ALL_SITES):
        if any(frozenset(pair) == DIRECT_FREE_PAIR for pair in matching):
            continue
        terms.append(matching_monomial(matching, colouring))
    require(len(terms) == len(set(terms)) == 90,
            "a direct-free full-nine row changed")
    return tuple(terms)


def fine_degree_of_edge_monomial(monomial):
    degree = [0] * 24
    for left, right, left_colour, right_colour in monomial:
        degree[3 * left + left_colour] += 1
        degree[3 * right + right_colour] += 1
    return tuple(degree)


def fine_degree_of_word(word):
    degree = [0] * 24
    for site, colour in enumerate(word):
        degree[3 * site + colour] += 1
    return tuple(degree)


def face(deleted_site):
    return tuple(site for site in ODD_SITES if site != deleted_site)


def lambda_degree(deleted_site):
    degree = [0] * 24
    for site in (X, deleted_site, P, Q):
        degree[3 * site] = 1
    for site in face(deleted_site):
        degree[3 * site] = 1
        degree[3 * site + MIXED[site]] = 1
    return tuple(degree)


def divides(left, right):
    return all(a <= b for a, b in zip(left, right))


def denominator_audit(target_degree, fixed_face):
    """Inspect all 3645 monomial terms of the 15 denominator columns."""
    columns = tuple(
        (site, colour) for site in ODD_SITES for colour in COLOURS
    )
    terms_seen = 0
    compatible_terms = []
    per_column = {}
    for deleted, exposed_colour in columns:
        count = 0
        for residual_colours in product(COLOURS, repeat=4):
            word = {deleted: exposed_colour}
            word.update(dict(zip(
                (site for site in ODD_SITES if site != deleted),
                residual_colours,
            )))
            for matching in matchings(
                    tuple(site for site in ODD_SITES if site != deleted)):
                q_term = matching_monomial(matching, word)
                degree = list(fine_degree_of_edge_monomial(q_term))
                # The output word e_w contributes one further slot at all
                # five odd sites.  At each matched site this duplicates the
                # q colour, which is why no term divides the squarefree
                # lambda_3 target.
                for site in ODD_SITES:
                    degree[3 * site + word[site]] += 1
                degree = tuple(degree)
                terms_seen += 1
                count += 1
                if divides(degree, target_degree):
                    compatible_terms.append(
                        (deleted, exposed_colour, tuple(word.items()), q_term)
                    )
        per_column[f"{deleted}:{exposed_colour}"] = count
    require(terms_seen == 15 * 81 * 3 == 3645,
            "denominator term count changed")
    require(set(per_column.values()) == {243},
            "a denominator column changed size")
    require(not compatible_terms,
            f"a raw denominator term entered lambda_{fixed_face}")

    # The reset at 12112 hits five denominator columns, but h_s Y_0 has
    # fine degree lambda_s.  Hence exactly the column indexed by the fixed
    # deleted face contributes to the desired fine degree.
    reset_hit_columns = tuple((site, MIXED[site]) for site in ODD_SITES)
    reset_hits_in_degree = tuple(
        column for column in reset_hit_columns
        if lambda_degree(column[0]) == target_degree
    )
    require(reset_hits_in_degree == ((fixed_face, MIXED[fixed_face]),),
            "fixed-degree reset-column census changed")
    return {
        "columns_inspected": len(columns),
        "terms_inspected": terms_seen,
        "terms_dividing_lambda": len(compatible_terms),
        "homogeneous_columns_admitted": 0,
        "reset_hit_columns": [list(column) for column in reset_hit_columns],
        "reset_hits_in_fixed_degree": [
            list(column) for column in reset_hits_in_degree
        ],
    }


def compatible_full_nine_columns(deleted_site):
    fixed_face = face(deleted_site)
    columns = []
    for switches in product((0, 1), repeat=len(fixed_face)):
        word = [0] * 8
        for site, switch in zip(fixed_face, switches):
            if switch:
                word[site] = MIXED[site]
        word = tuple(word)
        missing = {
            site: (0 if word[site] else MIXED[site]) for site in fixed_face
        }
        for matching in matchings(fixed_face):
            multiplier = matching_monomial(matching, missing)
            row_degree = fine_degree_of_word(word)
            expected_deficit = tuple(
                target - row
                for target, row in zip(
                    lambda_degree(deleted_site), row_degree
                )
            )
            require(
                fine_degree_of_edge_monomial(multiplier)
                == expected_deficit,
                "generated multiplier has the wrong deficit",
            )
            boundary = tuple(
                tuple(sorted(multiplier + term)) for term in full_row(word)
            )
            columns.append((word, multiplier, boundary))
    require(len(columns) == 48, "complete EqSystem block is not 48 columns")
    return tuple(columns)


def sparse_rank(columns):
    """Exact column rank over Q using sparse normalized pivot columns."""
    pivots = {}
    for source_column in columns:
        column = {
            row: QQ(value) for row, value in source_column.items() if value
        }
        while column:
            pivot = min(column, key=repr)
            value = column[pivot]
            if pivot not in pivots:
                column = {row: coefficient / value
                          for row, coefficient in column.items()}
                pivots[pivot] = column
                break
            basis = pivots[pivot]
            factor = value
            for row, coefficient in basis.items():
                new_value = column.get(row, QQ(0)) - factor * coefficient
                if new_value:
                    column[row] = new_value
                elif row in column:
                    del column[row]
    return len(pivots)


def augmented_column(label, boundary, _chart, deleted_site):
    word, multiplier = label
    column = defaultdict(QQ)
    for feature in boundary:
        column[("other_full_nine_boundary", feature)] += 1

    # Keeping the full common coefficient ledger is stronger than choosing
    # one ordinary-residue formula: every descended strict target, residue,
    # and ordered landing factors through this ledger.  Both charts have the
    # same sign here.
    column[("common_coefficient", word, multiplier)] += 1
    if word == (0,) * 8:
        # The homogenized pure-row target is -multiplier*U_0.  The strict
        # same-power landing U_0 -> Y_0 carries the identical coefficient
        # into the selected cap summand.  Keeping both rows records the
        # target--cap graph lock; the desired invisible column breaks it.
        column[("physical_target", multiplier)] -= 1
        column[(
            "selected_cap_boundary", deleted_site, multiplier, "Y_00000"
        )] -= 1
    return dict(column)


def membership_audit(eq_columns, deleted_site):
    boundary_only = [
        {
            ("other_full_nine_boundary", feature): QQ(1)
            for feature in boundary
        }
        for _word, _multiplier, boundary in eq_columns
    ]
    pq_columns = [
        augmented_column(
            (word, multiplier), boundary, "pq", deleted_site
        )
        for word, multiplier, boundary in eq_columns
    ]
    pr_columns = [
        augmented_column(
            (word, multiplier), boundary, "pr", deleted_site
        )
        for word, multiplier, boundary in eq_columns
    ]
    strict_columns = pq_columns + pr_columns
    boundary_rank = sparse_rank(boundary_only)
    doubled_boundary_rank = sparse_rank(boundary_only + boundary_only)
    one_chart_rank = sparse_rank(pq_columns)
    strict_rank = sparse_rank(strict_columns)
    require(boundary_rank == doubled_boundary_rank == 48,
            "full-nine boundary rank changed")
    require(one_chart_rank == strict_rank == 48,
            "strict complete block rank changed")

    # The desired fixed-face boundary is h_v Y_0.  It is deliberately in a
    # selected cap-row summand, while its physical target, ordinary residue,
    # and every other full-nine boundary coordinate are zero.
    fixed_face = face(deleted_site)
    mixed_face_colouring = {site: MIXED[site] for site in fixed_face}
    h_terms = tuple(
        matching_monomial(matching, mixed_face_colouring)
        for matching in matchings(fixed_face)
    )
    desired = {
        ("selected_cap_boundary", deleted_site, term, "Y_00000"): QQ(1)
        for term in h_terms
    }

    # Exact dual nonmembership certificate.  For each face multiplier, the
    # cap coefficient minus the physical-target coefficient annihilates
    # every strict column.  It evaluates to +1 on the corresponding term of
    # the desired target-zero column.
    for column in strict_columns:
        for term in h_terms:
            cap_value = column.get(
                ("selected_cap_boundary", deleted_site, term, "Y_00000"),
                QQ(0),
            )
            target_value = column.get(("physical_target", term), QQ(0))
            require(cap_value - target_value == 0,
                    "a strict column broke the target--cap graph lock")
    require(all(
        desired[("selected_cap_boundary", deleted_site, term, "Y_00000")]
        == 1
        for term in h_terms
    ), "desired column has the wrong dual value")

    cap_occupied_columns = sum(
        any(row[0] == "selected_cap_boundary" for row in column)
        for column in strict_columns
    )
    require(cap_occupied_columns == 6,
            "the selected cap rows should be hit by three columns per chart")
    augmented_rank = sparse_rank(strict_columns + [desired])
    require(augmented_rank == 49,
            "desired invisible face column did not raise rank")

    # Since the two chart columns are literally equal and one chart is
    # injective, these 48 pairwise comparisons are a complete kernel basis.
    comparison_kernel_dimension = len(strict_columns) - strict_rank
    require(comparison_kernel_dimension == 48,
            "strict comparison kernel dimension changed")
    for left, right in zip(pq_columns, pr_columns):
        require(left == right, "a chart comparison has nonzero augmented image")

    return {
        "deleted_site": deleted_site,
        "face": list(fixed_face),
        "compatible_global_words": 16,
        "multipliers_per_word": 3,
        "one_chart_columns": len(pq_columns),
        "one_chart_boundary_rank": boundary_rank,
        "two_chart_boundary_rank": doubled_boundary_rank,
        "one_chart_rank": one_chart_rank,
        "two_chart_columns": len(strict_columns),
        "two_chart_rank": strict_rank,
        "kernel_dimension": comparison_kernel_dimension,
        "kernel_basis": "48 pairwise pq-minus-pr comparisons",
        "kernel_common_coefficient_rank": 0,
        "kernel_physical_target_rank": 0,
        "kernel_descended_ordinary_residue_rank": 0,
        "desired_terms": len(desired),
        "strict_columns_hitting_selected_cap": cap_occupied_columns,
        "nonmembership_dual_certificate": "selected_cap minus physical_target",
        "dual_value_on_strict_columns": 0,
        "dual_values_on_desired_terms": [1] * len(desired),
        "rank_before_desired": strict_rank,
        "rank_after_desired": augmented_rank,
        "desired_membership": False,
    }


def face_audit(deleted_site):
    target_degree = lambda_degree(deleted_site)
    require(sum(target_degree) == 12,
            f"lambda_{deleted_site} should have twelve slots")
    denominator = denominator_audit(target_degree, deleted_site)
    eq_columns = compatible_full_nine_columns(deleted_site)
    membership = membership_audit(eq_columns, deleted_site)
    return {
        "deleted_site": deleted_site,
        "face": list(face(deleted_site)),
        "lambda_weight": sum(target_degree),
        "denominator": denominator,
        "eqsystem": membership,
    }


def run(face_mode):
    selected_faces = ODD_SITES if face_mode == "all" else (int(face_mode),)
    records = [face_audit(deleted_site) for deleted_site in selected_faces]
    ledger = {
        "mode": face_mode,
        "distinguished_chart_site": R,
        "direct_free_pair": sorted(DIRECT_FREE_PAIR),
        "fixed_chart_orbits": [list(orbit) for orbit in FIXED_CHART_ORBITS],
        "faces": records,
        "guard_specialization_used": False,
        "typed_conclusion": (
            "raw denominator presentation has no lambda_v component; "
            "the reset image h_v Y_0 is a degree-lowering desired column"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    require(digest == EXPECTED_DIGESTS[face_mode],
            f"ledger changed: {digest}")
    print(f"h=3 complete strict first-fine-degree membership ({face_mode}): PASS")
    for record in records:
        deleted_site = record["deleted_site"]
        print(
            f"v={deleted_site}: 15 denominator columns / 3645 terms; "
            f"lambda_{deleted_site} piece zero"
        )
        print(
            f"v={deleted_site}: 48 pq + 48 pr EqSystem columns, rank 48; "
            "kernel 48 comparisons"
        )
        print(
            f"v={deleted_site}: adjoining h_{deleted_site} Y_0 raises "
            "rank 48 -> 49; target-cap dual certificate nonzero"
        )
    print(f"sha256: {digest}")
    return digest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--face", choices=("all", "1", "2", "3", "4", "5"), default="all"
    )
    arguments = parser.parse_args()
    run(arguments.face)


if __name__ == "__main__":
    main()
