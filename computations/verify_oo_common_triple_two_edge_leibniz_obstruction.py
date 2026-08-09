#!/usr/bin/env python3
"""Exact lower-filtration obstruction to lifting the two-edge OO identity.

The four-column identity in
``verify_oo_common_triple_two_edge_anchor_identity.py`` lives in the second
coefficient/reinsertion module.  This checker expands the exact second-order
Leibniz cross terms and reduces their combined tail against

* the literal one-edge module from commit a2356b4, with both chart copies;
* both labelled copies of the three compatible 22 diagonal-anchor columns.

An integral covector proves the tail is nonzero in that quotient.  The
Euler contractions over all compatible two-edge pairs are also checked.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import verify_oo_common_triple_two_edge_anchor_identity as two  # noqa: E402


Q = Fraction
EXPECTED_DIGEST = "601df68efa257a52ab7096c91a555e5bb5447988e497915d19d066f17f1e5ae4"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def clean(polynomial):
    return {term: value for term, value in polynomial.items() if value}


def variable(item):
    return {(item,): Q(1)}


def add(*polynomials):
    answer = defaultdict(Q)
    for polynomial in polynomials:
        for term, value in polynomial.items():
            answer[term] += value
    return clean(answer)


def scale(scalar, polynomial):
    return clean({term: Q(scalar) * value for term, value in polynomial.items()})


def multiply(*polynomials):
    result = {(): Q(1)}
    for polynomial in polynomials:
        answer = defaultdict(Q)
        for left_term, left_value in result.items():
            for right_term, right_value in polynomial.items():
                term = tuple(sorted(left_term + right_term, key=repr))
                answer[term] += left_value * right_value
        result = clean(answer)
    return result


def derivative(polynomial, item):
    answer = defaultdict(Q)
    for term, value in polynomial.items():
        multiplicity = term.count(item)
        if not multiplicity:
            continue
        remainder = list(term)
        remainder.remove(item)
        answer[tuple(remainder)] += multiplicity * value
    return clean(answer)


def second_reinsertion(polynomial, first, second):
    return multiply(
        variable(first),
        variable(second),
        derivative(derivative(polynomial, first), second),
    )


def gamma(polynomial_left, polynomial_right, first, second):
    """The exact second-order Leibniz cross term."""

    cross = add(
        multiply(derivative(polynomial_left, first),
                 derivative(polynomial_right, second)),
        multiply(derivative(polynomial_left, second),
                 derivative(polynomial_right, first)),
    )
    return multiply(variable(first), variable(second), cross)


def poly_equal(left, right):
    return clean(left) == clean(right)


def cross(left, right):
    return (
        add(multiply(left[1], right[2]), scale(-1, multiply(left[2], right[1]))),
        add(multiply(left[2], right[0]), scale(-1, multiply(left[0], right[2]))),
        add(multiply(left[0], right[1]), scale(-1, multiply(left[1], right[0]))),
    )


def outer(left, right):
    return [[multiply(left[i], right[j]) for j in range(3)] for i in range(3)]


def matrix_add(left, right):
    return [[add(left[i][j], right[i][j]) for j in range(3)] for i in range(3)]


def matrix_multiply(left, right):
    return [[
        add(*(multiply(left[i][k], right[k][j]) for k in range(3)))
        for j in range(3)
    ] for i in range(3)]


def adjugate_3(matrix):
    answer = [[{} for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            rows = [row for row in range(3) if row != i]
            columns = [column for column in range(3) if column != j]
            minor = add(
                multiply(matrix[rows[0]][columns[0]], matrix[rows[1]][columns[1]]),
                scale(-1, multiply(
                    matrix[rows[0]][columns[1]], matrix[rows[1]][columns[0]]
                )),
            )
            answer[j][i] = minor if (i + j) % 2 == 0 else scale(-1, minor)
    return answer


def audit_rank_two_adjugate():
    """Multiplication-safe rank-two identity proposed as a bypass."""

    u = tuple(variable(("u", i)) for i in range(3))
    v = tuple(variable(("v", i)) for i in range(3))
    x = tuple(variable(("x", i)) for i in range(3))
    y = tuple(variable(("y", i)) for i in range(3))
    q = variable(("q",))
    matrix = matrix_add(outer(u, v), [
        [multiply(q, entry) for entry in row] for row in outer(x, y)
    ])
    observed = adjugate_3(matrix)
    expected = [
        [multiply(q, entry) for entry in row]
        for row in outer(cross(v, y), cross(u, x))
    ]
    require(all(poly_equal(observed[i][j], expected[i][j])
                for i in range(3) for j in range(3)),
            "rank-two adjugate formula changed")
    product = matrix_multiply(matrix, observed)
    require(all(not product[i][j] for i in range(3) for j in range(3)),
            "B*adj(B) is not the zero source identity")
    return {
        "adjugate": "q*(v cross y)*(u cross x)^T",
        "B_adjB_nonzero_entries": 0,
        "residual_degree": 6,
    }


def edge_variable(edge, word):
    return "edge", *two.colored_edge(edge, word)


def matching_polynomial(word):
    return {
        tuple(sorted(
            (edge_variable(edge, word) for edge in matching), key=repr
        )): Q(1)
        for matching in two.PERFECT_MATCHINGS
    }


def d_hafnian_polynomial():
    word = (2,) * 8
    return {
        tuple(sorted(
            (edge_variable(edge, word) for edge in matching), key=repr
        )): Q(1)
        for matching in two.matchings(two.D)
    }


def one_edge_column(edge, word):
    return {
        two.source_feature(matching, word): Q(1)
        for matching in two.PERFECT_MATCHINGS
        if edge in matching
    }


def pair_covector(word):
    """Extend the six-matching all-edge witness over the target rows."""

    signed_matchings = (
        (-1, ((0, 2), (1, 3), (4, 5), (6, 7))),
        (+1, ((0, 2), (1, 4), (3, 5), (6, 7))),
        (+1, ((0, 3), (1, 2), (4, 5), (6, 7))),
        (-1, ((0, 3), (1, 4), (2, 5), (6, 7))),
        (-1, ((0, 4), (1, 2), (3, 5), (6, 7))),
        (+1, ((0, 4), (1, 3), (2, 5), (6, 7))),
    )
    covector = {
        two.source_feature(tuple(sorted(matching)), word): Q(sign)
        for sign, matching in signed_matchings
    }
    target_weights = {}
    for partial in two.ENDPOINT_MATCHINGS:
        source_column = two.mixed_second_column(partial, word)
        weight = sum(
            covector.get(feature, 0) * value
            for feature, value in source_column.items()
        )
        covector[two.target_feature(partial, word)] = weight
        target_weights[partial] = weight
    require(tuple(target_weights[partial]
                  for partial in two.ENDPOINT_MATCHINGS) == (0, -1, 1),
            "extended target weights changed")
    return covector, target_weights


def pairing(covector, column):
    return sum(covector.get(feature, 0) * value
               for feature, value in column.items())


def audit_product_rules(word):
    hafnian = matching_polynomial(word)
    endpoint_records = []
    for partial in two.ENDPOINT_MATCHINGS:
        first_edge, second_edge = partial
        first = edge_variable(first_edge, word)
        second = edge_variable(second_edge, word)

        # Expand H=e*d_eH+H_not_e.  Because d_eH is e-independent, the
        # entire J_ef contribution is the Leibniz cross term Gamma(e,d_eH).
        first_cofactor = derivative(hafnian, first)
        containing_first = multiply(variable(first), first_cofactor)
        without_first = add(hafnian, scale(-1, containing_first))
        require(not derivative(first_cofactor, first),
                "a matching cofactor retained its removed edge")
        require(not second_reinsertion(without_first, first, second),
                "the no-first-edge remainder acquired a second coefficient")
        mixed_second = second_reinsertion(hafnian, first, second)
        mixed_gamma = gamma(variable(first), first_cofactor, first, second)
        require(mixed_second == mixed_gamma,
                "mixed second coefficient is not its exact Leibniz cross term")
        require(len(mixed_second) == 3,
                "endpoint second coefficient term count changed")

        # The diagonal column m*(H_D-X2) is likewise the pure cross term in
        # J_ef(e * (f*G)); neither strict factor has a second coefficient.
        x2 = variable(("target", "X2_D"))
        diagonal_base = add(d_hafnian_polynomial(), scale(-1, x2))
        left = variable(first)
        right = multiply(variable(second), diagonal_base)
        diagonal_product = multiply(left, right)
        require(not second_reinsertion(left, first, second)
                and not second_reinsertion(right, first, second),
                "a strict diagonal factor acquired a second coefficient")
        diagonal_second = second_reinsertion(diagonal_product, first, second)
        diagonal_gamma = gamma(left, right, first, second)
        require(diagonal_second == diagonal_gamma == diagonal_product,
                "diagonal multiplier is not its exact Leibniz cross term")

        endpoint_records.append({
            "partial": [list(edge) for edge in partial],
            "mixed_gamma_terms": len(mixed_gamma),
            "diagonal_gamma_terms": len(diagonal_gamma),
        })
    return endpoint_records


def audit_euler(word):
    """Check the multiplication-safe total contractions integrally."""

    all_sum = defaultdict(Q)
    for partial in two.ALL_TWO_EDGE_PARTIALS:
        add_scaled(all_sum, two.mixed_second_column(partial, word), 1)
    full_row = {
        two.source_feature(matching, word): Q(1)
        for matching in two.PERFECT_MATCHINGS
    }
    require(dict(all_sum) == {feature: 6 * value
                              for feature, value in full_row.items()},
            "all-pair second Euler contraction is not 6H")

    s_sum = defaultdict(Q)
    for partial in two.S_TWO_EDGE_PARTIALS:
        add_scaled(s_sum, two.mixed_second_column(partial, word), 1)
    require(dict(s_sum) == {feature: 3 * value
                            for feature, value in full_row.items()},
            "fixed-s second Euler contraction is not 3H")

    first_sum = defaultdict(Q)
    for edge in two.PHYSICAL_EDGES:
        add_scaled(first_sum, one_edge_column(edge, word), 1)
    require(dict(first_sum) == {feature: 4 * value
                                for feature, value in full_row.items()},
            "first Euler contraction is not 4H")
    return {"first": 4, "fixed_s_second": 3, "all_second": 6}


def add_scaled(target, column, scalar):
    for feature, value in column.items():
        target[feature] += Q(scalar) * value
        if not target[feature]:
            del target[feature]


def audit_lower_module(word):
    s_one = [one_edge_column(edge, word)
             for edge in two.PHYSICAL_EDGES if two.S in edge]
    all_one = [one_edge_column(edge, word) for edge in two.PHYSICAL_EDGES]
    # Retain both source-labelled copies, as in the preceding modules.
    s_one_doubled = s_one + s_one
    all_one_doubled = all_one + all_one
    diagonals = [
        two.diagonal_anchor_column(partial, word)
        for _chart in ("pq", "pr")
        for partial in two.ENDPOINT_MATCHINGS
    ]
    target = two.curvature_target(word)

    s_rank, _, _, _ = two.rational_rank(s_one_doubled)
    s_lower_rank, s_features, _, _ = two.rational_rank(
        s_one_doubled + diagonals
    )
    s_target_rank, _, _, _ = two.rational_rank(
        s_one_doubled + diagonals + [target]
    )
    all_rank, _, _, _ = two.rational_rank(all_one_doubled)
    all_lower_rank, all_features, _, _ = two.rational_rank(
        all_one_doubled + diagonals
    )
    all_target_rank, _, _, _ = two.rational_rank(
        all_one_doubled + diagonals + [target]
    )
    require((len(s_one_doubled), s_rank) == (14, 7),
            "doubled fixed-s one-edge module changed")
    require((s_lower_rank, s_features, s_target_rank) == (10, 108, 11),
            "fixed-s lower-module obstruction rank changed")
    require((len(all_one_doubled), all_rank) == (56, 21),
            "doubled all-edge module changed")
    require((all_lower_rank, all_features, all_target_rank) == (24, 108, 25),
            "all-edge lower-module obstruction rank changed")

    covector, target_weights = pair_covector(word)
    for column in all_one_doubled + diagonals:
        require(pairing(covector, column) == 0,
                "integral obstruction covector missed a lower column")
    target_pairing = pairing(covector, target)
    require(target_pairing == 1,
            "integral obstruction covector lost the Spencer tail")
    m_pq_rs = tuple(sorted(((two.P, two.Q_SITE), (two.R, two.S))))
    m_pr_qs = tuple(sorted(((two.P, two.R), (two.Q_SITE, two.S))))
    adjugate_lead = defaultdict(Q)
    add_scaled(adjugate_lead, two.mixed_second_column(m_pq_rs, word), 1)
    add_scaled(adjugate_lead, two.mixed_second_column(m_pr_qs, word), -1)
    adjugate_lead_pairing = pairing(covector, adjugate_lead)
    require(adjugate_lead_pairing == 1,
            "curvature lead lost its adjugate counterguard pairing")
    # A multiplication-safe adjugate identity with this lead has total
    # source boundary zero.  Its unshown remainder must therefore pair -1,
    # and cannot be built from the lower columns, all of which pair zero.
    required_adjugate_remainder_pairing = -adjugate_lead_pairing

    return {
        "s_lower_columns": len(s_one_doubled) + len(diagonals),
        "s_lower_rank": s_lower_rank,
        "s_lower_cokernel": s_features - s_lower_rank,
        "s_target_augmented_rank": s_target_rank,
        "all_lower_columns": len(all_one_doubled) + len(diagonals),
        "all_lower_rank": all_lower_rank,
        "all_lower_cokernel": all_features - all_lower_rank,
        "all_target_augmented_rank": all_target_rank,
        "covector_source_support": 6,
        "covector_target_weights": [
            str(target_weights[partial]) for partial in two.ENDPOINT_MATCHINGS
        ],
        "covector_target_pairing": str(target_pairing),
        "adjugate_curvature_lead_pairing": str(adjugate_lead_pairing),
        "required_adjugate_remainder_pairing": str(
            required_adjugate_remainder_pairing
        ),
        "adjugate_remainder_in_lower_module": False,
    }


def audit_four_tail(word):
    m_pq_rs = tuple(sorted(((two.P, two.Q_SITE), (two.R, two.S))))
    m_pr_qs = tuple(sorted(((two.P, two.R), (two.Q_SITE, two.S))))
    tail = defaultdict(Q)
    add_scaled(tail, two.mixed_second_column(m_pq_rs, word), 1)
    add_scaled(tail, two.mixed_second_column(m_pr_qs, word), -1)
    add_scaled(tail, two.diagonal_anchor_column(m_pq_rs, word), -1)
    add_scaled(tail, two.diagonal_anchor_column(m_pr_qs, word), 1)
    require(dict(tail) == two.curvature_target(word),
            "combined Leibniz tail is not curvature times X2")
    return len(tail)


def audit_one_normalization(a, ell):
    word = (a, 0, 1, ell, 2, 2, 2, 2)
    product_records = audit_product_rules(word)
    euler = audit_euler(word)
    lower = audit_lower_module(word)
    tail_terms = audit_four_tail(word)
    return {
        "a": a,
        "ell": ell,
        "word": "".join(map(str, word)),
        "product_records": product_records,
        "euler_multiplicities": euler,
        "four_column_tail_terms": tail_terms,
        "lower_module": lower,
    }


def main():
    adjugate = audit_rank_two_adjugate()
    records = [
        audit_one_normalization(a, ell)
        for a in two.COLORS
        for ell in two.COLORS
    ]
    ledger = {
        "rank_two_adjugate": adjugate,
        "normalizations": records,
        "interpretation": (
            "second Spencer/Leibniz tails reduced against doubled literal "
            "one-edge module plus both labelled 22 anchor rows"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    require(digest == EXPECTED_DIGEST, f"ledger digest changed: {digest}")

    print("OO two-edge Leibniz/occupancy lift obstruction: PASS")
    print("every selected second column is its exact Leibniz cross term")
    print("Euler contractions: sum_e C_e=4H, sum_s-pairs J=3H, sum_all J=6H")
    print("fixed-s lower module + anchors: rank 10; tail-augmented rank 11")
    print("all-edge lower module + anchors: rank 24; tail-augmented rank 25")
    print("integral 6-source+3-target covector kills the lower module, pairs tail=1")
    print("rank-two B*adj(B)=0 passes, but its curvature lead requires a remainder pairing -1")
    print("therefore the adjugate remainder is not in the one-edge/diagonal module")
    print("verdict: no order-one/diagonal null-homotopy of the two-edge identity")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
