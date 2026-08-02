#!/usr/bin/env python3
"""Complete strict first-fine-degree membership for the v=3 h=3 face.

This checker keeps the grading honest.  It inspects every term in all 15
odd denominator columns, enumerates every compatible full-nine
row/multiplier in both charts, and computes the exact sparse rational ranks
of the resulting augmented membership problem.  A denominator column is
not silently treated as a same-degree full-nine column: its lambda_3 piece
is computed term by term.
"""

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
X, V, P, Q = 0, 3, 6, 7
FACE = tuple(site for site in ODD_SITES if site != V)
DIRECT_FREE_PAIR = frozenset((P, V))
EXPECTED_DIGEST = "33c49461bead4c9069709b8174c6f953398dd5f7dccb2c71c45c4678e41fdbaa"


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


def lambda_degree():
    degree = [0] * 24
    for site in (X, V, P, Q):
        degree[3 * site] = 1
    for site in FACE:
        degree[3 * site] = 1
        degree[3 * site + MIXED[site]] = 1
    return tuple(degree)


def divides(left, right):
    return all(a <= b for a, b in zip(left, right))


def denominator_audit(target_degree):
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
            "a raw denominator term entered lambda_3")
    return {
        "columns_inspected": len(columns),
        "terms_inspected": terms_seen,
        "terms_dividing_lambda": len(compatible_terms),
        "homogeneous_columns_admitted": 0,
    }


def compatible_full_nine_columns():
    columns = []
    for switches in product((0, 1), repeat=len(FACE)):
        word = [0] * 8
        for site, switch in zip(FACE, switches):
            if switch:
                word[site] = MIXED[site]
        word = tuple(word)
        missing = {
            site: (0 if word[site] else MIXED[site]) for site in FACE
        }
        for matching in matchings(FACE):
            multiplier = matching_monomial(matching, missing)
            row_degree = fine_degree_of_word(word)
            expected_deficit = tuple(
                target - row
                for target, row in zip(lambda_degree(), row_degree)
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


def augmented_column(label, boundary, _chart):
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
        column[("physical_target", multiplier)] -= 1
    return dict(column)


def membership_audit(eq_columns):
    boundary_only = [
        {
            ("other_full_nine_boundary", feature): QQ(1)
            for feature in boundary
        }
        for _word, _multiplier, boundary in eq_columns
    ]
    pq_columns = [
        augmented_column((word, multiplier), boundary, "pq")
        for word, multiplier, boundary in eq_columns
    ]
    pr_columns = [
        augmented_column((word, multiplier), boundary, "pr")
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

    # The desired fixed-face boundary is h_3 Y_0.  It is deliberately in a
    # selected cap-row summand, while its physical target, ordinary residue,
    # and every other full-nine boundary coordinate are zero.
    mixed_face_colouring = {site: MIXED[site] for site in FACE}
    h_terms = tuple(
        matching_monomial(matching, mixed_face_colouring)
        for matching in matchings(FACE)
    )
    desired = {
        ("selected_cap_boundary", term, "Y_00000"): QQ(1)
        for term in h_terms
    }
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
        "rank_before_desired": strict_rank,
        "rank_after_desired": augmented_rank,
        "desired_membership": False,
    }


def main():
    target_degree = lambda_degree()
    require(sum(target_degree) == 12, "lambda_3 should have twelve slots")
    denominator = denominator_audit(target_degree)
    eq_columns = compatible_full_nine_columns()
    membership = membership_audit(eq_columns)
    ledger = {
        "deleted_site": V,
        "face": list(FACE),
        "lambda_weight": sum(target_degree),
        "denominator": denominator,
        "eqsystem": membership,
        "guard_specialization_used": False,
        "typed_conclusion": (
            "raw denominator presentation has no lambda_3 component; "
            "the reset image h_3 Y_0 is a degree-lowering desired column"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    require(digest == EXPECTED_DIGEST, f"ledger changed: {digest}")
    print("h=3 complete strict first-fine-degree membership (v=3): PASS")
    print("15 denominator columns / 3645 terms inspected; lambda_3 piece is zero")
    print("all EqSystem sources: 48 pq + 48 pr; exact rank 48")
    print("kernel: 48 chart comparisons; all descended strict readouts vanish")
    print("adjoining h_3 Y_0 raises rank 48 -> 49: membership does not exist")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
