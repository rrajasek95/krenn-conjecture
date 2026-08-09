#!/usr/bin/env python3
"""Scalar determinant-cleared OO connection and its literal residual.

The tempting connection treats the three pure target tensors X_0,X_1,X_2
as an invertible diagonal 3x3 block, forms an adjugate/inverse, and asks a
Maurer--Cartan curvature to kill the common-two-star Bianchi remainder from
``verify_oo_common_triple_adjugate_remainder.py``.

Two multiplications must be separated.  Pure target tensors do have zero
pairwise product in the site-square-zero bookkeeping algebra.  But after
fixed-word coefficient extraction the pure equations are scalar source
polynomials F_i-1, so F_0 F_1 F_2 is a unit in the coefficient quotient and
determinant clearing is legitimate there.

The checker therefore performs the scalar test.  It embeds the selected
curvature square in a full 3x3 response frame, checks its polynomial
adjugate, and retains the pq/pr matching and target tags.  The resulting
Maurer--Cartan/adjugate curvature is the complete diagonal cap graph
-kappa*(T+R), hence a literal diagonal-anchor boundary.  The desired
target-free class -kappa*R differs by kappa*T and remains detected by the
integral covector.  Thus scalar localization is valid, but it does not
supply the missing connection-to-diagonal nullhomotopy.
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

import verify_oo_common_triple_adjugate_remainder as remainder  # noqa: E402
import verify_oo_common_triple_two_edge_anchor_identity as two  # noqa: E402
import verify_oo_common_triple_two_edge_leibniz_obstruction as obs  # noqa: E402


Q = Fraction
EXPECTED_DIGEST = "5993f5eed23db28579d2b0bbbd57d49e35daf224432e204bd16947ff4097f540"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def clean(polynomial):
    return {monomial: value for monomial, value in polynomial.items() if value}


def physical_monomial(colour, sites=two.D):
    return frozenset((site, colour) for site in sites)


def physical_multiply(left, right):
    """Product in the site-square-zero algebra, retaining endpoint colours."""

    answer = defaultdict(Q)
    for left_monomial, left_value in left.items():
        left_sites = {site for site, _colour in left_monomial}
        for right_monomial, right_value in right.items():
            right_sites = {site for site, _colour in right_monomial}
            if left_sites & right_sites:
                continue
            answer[left_monomial | right_monomial] += left_value * right_value
    return clean(answer)


def physical_target(colour):
    return {physical_monomial(colour): Q(1)}


def formal_add(*polynomials):
    answer = defaultdict(Q)
    for polynomial in polynomials:
        for monomial, value in polynomial.items():
            answer[monomial] += value
    return clean(answer)


def formal_scale(scalar, polynomial):
    return clean({monomial: Q(scalar) * value
                  for monomial, value in polynomial.items()})


def formal_multiply(left, right):
    answer = defaultdict(Q)
    for left_monomial, left_value in left.items():
        for right_monomial, right_value in right.items():
            answer[tuple(sorted(left_monomial + right_monomial))] += (
                left_value * right_value
            )
    return clean(answer)


def formal_variable(name):
    return {(name,): Q(1)}


def formal_matrix_multiply(left, right):
    answer = [[{} for _ in range(3)] for _ in range(3)]
    for row in range(3):
        for column in range(3):
            answer[row][column] = formal_add(*(
                formal_multiply(left[row][middle], right[middle][column])
                for middle in range(3)
            ))
    return answer


def audit_two_multiplications():
    targets = [physical_target(colour) for colour in two.COLORS]
    pair_products = {
        f"X{left}X{right}": len(physical_multiply(targets[left], targets[right]))
        for left in two.COLORS for right in two.COLORS if left < right
    }
    require(pair_products == {"X0X1": 0, "X0X2": 0, "X1X2": 0},
            "two pure targets acquired a source-graded product")
    determinant = physical_multiply(
        physical_multiply(targets[0], targets[1]), targets[2]
    )
    require(not determinant,
            "the pure-target determinant stopped being site-square-zero")

    # External Laurent variables do satisfy the ordinary adjugate identity,
    # but the externalization is not multiplicative from the source algebra:
    # source X0*X1=0 whereas formal X0*X1 is nonzero.
    formal_targets = [formal_variable(f"X{colour}") for colour in two.COLORS]
    diagonal = [[{} for _ in range(3)] for _ in range(3)]
    adjugate = [[{} for _ in range(3)] for _ in range(3)]
    for colour in two.COLORS:
        diagonal[colour][colour] = formal_targets[colour]
        others = [value for value in two.COLORS if value != colour]
        adjugate[colour][colour] = formal_multiply(
            formal_targets[others[0]], formal_targets[others[1]]
        )
    product = formal_matrix_multiply(diagonal, adjugate)
    formal_determinant = formal_multiply(
        formal_multiply(formal_targets[0], formal_targets[1]),
        formal_targets[2],
    )
    expected = [[{} for _ in range(3)] for _ in range(3)]
    for colour in two.COLORS:
        expected[colour][colour] = formal_determinant
    require(product == expected and formal_determinant,
            "the external diagonal adjugate identity changed")
    require(not physical_multiply(targets[0], targets[1])
            and formal_multiply(formal_targets[0], formal_targets[1]),
            "external target scalarization unexpectedly became multiplicative")
    return {
        "residual_sites": list(two.D),
        "target_physical_degree": len(two.D),
        "pair_products": pair_products,
        "physical_det_terms": len(determinant),
        "tensor_hasse_localization_exists": False,
        "formal_det_terms": len(formal_determinant),
        "fixed_word_scalar_coefficient_multiplication_source_valid": True,
        "scalar_pure_equations": ["F0-1", "F1-1", "F2-1"],
        "scalar_localization_F0F1F2_unit": True,
    }


def audit_full_response_adjugate():
    """Determinant-clear the selected 2x2 curvature square inside 3x3."""

    one = {(): Q(1)}
    zero = {}
    a = formal_variable("A")
    b = formal_variable("B")
    f = formal_variable("F")
    u = formal_variable("U")
    kappa = formal_add(formal_multiply(a, u),
                       formal_scale(-1, formal_multiply(b, f)))
    frame = [
        [a, b, zero],
        [f, u, zero],
        [zero, zero, one],
    ]
    adjugate = [
        [u, formal_scale(-1, b), zero],
        [formal_scale(-1, f), a, zero],
        [zero, zero, kappa],
    ]
    product = formal_matrix_multiply(frame, adjugate)
    expected = [[{} for _ in range(3)] for _ in range(3)]
    for colour in range(3):
        expected[colour][colour] = kappa
    require(product == expected,
            "the full determinant-cleared response adjugate changed")

    # The two adjugate contractions are the selected Maurer--Cartan square.
    lambda_c2 = formal_add(
        formal_scale(-1, formal_multiply(f, b)),
        formal_multiply(a, u),
    )
    eta_c1 = formal_add(
        formal_multiply(u, a),
        formal_scale(-1, formal_multiply(b, f)),
    )
    require(lambda_c2 == eta_c1 == kappa,
            "the two determinant-cleared curvature contractions disagree")
    return {
        "frame": "[[A,B,0],[F,U,0],[0,0,1]]",
        "determinant": "kappa=A*U-B*F",
        "adjugate": "[[U,-B,0],[-F,A,0],[0,0,kappa]]",
        "frame_times_adjugate": "kappa*I3",
        "lambda_c2": "kappa",
        "eta_c1": "kappa",
        "scalar_determinant_clearing_valid": True,
    }


def add_scaled(target, column, scalar):
    for feature, value in column.items():
        target[feature] += Q(scalar) * value
        if not target[feature]:
            del target[feature]


def formal_scale_vector(scalar, vector):
    return {
        feature: formal_scale(value, scalar)
        for feature, value in vector.items() if value
    }


def formal_pairing(covector, vector):
    return formal_add(*(
        formal_scale(covector.get(feature, 0), value)
        for feature, value in vector.items()
    ))


def audit_one_normalization(a, ell):
    word = (a, 0, 1, ell, 2, 2, 2, 2)
    full_nine = two.compatible_rows(a, ell)
    require(sum(row["mixed_cut"] for row in full_nine) == 2
            and sum(row["missing_anchor_cut"] for row in full_nine) == 2,
            "the full-nine scalar fine-degree projection changed")
    coefficients, positive, negative = remainder.explicit_minimal_row()
    lead_coefficients = {positive: Q(1), negative: Q(-1)}
    remainder_coefficients = {
        column: value for column, value in coefficients.items()
        if column not in (positive, negative)
    }
    lead = remainder.combine(lead_coefficients, word)
    normal = remainder.combine(remainder_coefficients, word)
    require(normal == {feature: -value for feature, value in lead.items()},
            "the Bianchi normal packet changed")
    require(len(normal) == 6,
            "the minimal source residual stopped having six matching terms")

    covector, target_weights = obs.pair_covector(word)
    require(obs.pairing(covector, normal) == -1,
            "the connection residual lost its integral pairing")
    target = two.curvature_target(word)
    require(obs.pairing(covector, target) == 1,
            "the curvature target lost its integral pairing")
    diagonals = [
        two.diagonal_anchor_column(partial, word)
        for _chart in ("pq", "pr")
        for partial in two.ENDPOINT_MATCHINGS
    ]
    require(all(obs.pairing(covector, column) == 0 for column in diagonals),
            "the residual covector stopped killing the diagonal anchors")

    # The signed difference of the two literal diagonal rows is exactly
    # -(target+normal).  Hence determinant-cleared curvature gives the full
    # cap graph and is already a diagonal boundary.  Removing only its
    # target coordinate leaves -kappa*normal, whose pairing is +kappa and
    # therefore cannot differ from the graph by diagonal-anchor multiples.
    diagonal_difference = defaultdict(Q)
    add_scaled(
        diagonal_difference,
        two.diagonal_anchor_column(positive, word),
        1,
    )
    add_scaled(
        diagonal_difference,
        two.diagonal_anchor_column(negative, word),
        -1,
    )
    cap_graph = defaultdict(Q)
    add_scaled(cap_graph, target, 1)
    add_scaled(cap_graph, normal, 1)
    require(dict(diagonal_difference)
            == {feature: -value for feature, value in cap_graph.items()},
            "the literal diagonal row is not the negative cap graph")
    require(obs.pairing(covector, cap_graph) == 0
            and obs.pairing(covector, diagonal_difference) == 0,
            "the cap graph stopped being a diagonal-boundary class")

    kappa = formal_add(
        formal_multiply(formal_variable("A"), formal_variable("U")),
        formal_scale(-1, formal_multiply(
            formal_variable("B"), formal_variable("F")
        )),
    )
    connection_curvature = formal_scale_vector(
        formal_scale(-1, kappa), cap_graph
    )
    diagonal_boundary = formal_scale_vector(kappa, diagonal_difference)
    require(connection_curvature == diagonal_boundary,
            "the scalar connection curvature is not the diagonal boundary")
    target_free = formal_scale_vector(formal_scale(-1, kappa), normal)
    require(formal_pairing(covector, target_free) == kappa,
            "the target-free scalar connection residual changed")
    return {
        "a": a,
        "ell": ell,
        "word": "".join(map(str, word)),
        "pq_mixed_row": f"pq:{a}0",
        "pr_mixed_row": f"pr:{a}1",
        "diagonal_anchor_rows": ["pq:22", "pr:22"],
        "full_nine_rows_before_projection": len(full_nine),
        "fine_degree_mixed_rows": 2,
        "fine_degree_anchor_rows": 2,
        "other_response_channels_in_fine_degree": 0,
        "normal_column_support": len(remainder_coefficients),
        "normal_source_terms": len(normal),
        "normal_pairing": "-1",
        "target_pairing": "1",
        "cap_graph_pairing": "0",
        "curvature_open_pairing": "-kappa",
        "diagonal_pairings": [
            str(obs.pairing(covector, column)) for column in diagonals
        ],
        "determinant_cleared_curvature": "-kappa*(target+normal)",
        "determinant_cleared_curvature_is_diagonal_boundary": True,
        "target_free_candidate": "-kappa*normal",
        "target_free_candidate_pairing": "kappa",
        "required_connection_to_diagonal_residual": "kappa*target",
        "scalar_maurer_cartan_candidate_closes_class": False,
    }


def main():
    multiplications = audit_two_multiplications()
    response_adjugate = audit_full_response_adjugate()
    records = [
        audit_one_normalization(a, ell)
        for a in two.COLORS for ell in two.COLORS
    ]
    ledger = {
        "two_multiplications": multiplications,
        "full_response_adjugate": response_adjugate,
        "normalizations": records,
        "interpretation": (
            "determinant-cleared Maurer-Cartan candidate audited in the "
            "source scalar fixed-word coefficient ring with literal pq/pr "
            "matching and diagonal-target provenance retained"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    require(digest == EXPECTED_DIGEST, f"ledger digest changed: {digest}")

    print("OO scalar Maurer-Cartan connection test: PASS")
    print("tensor target products vanish, but scalar pure equations Fi-1 make Fi units")
    print("full response frame*adjugate=kappa*I3 in the scalar coefficient ring")
    print("minimal residual: 10 Bianchi columns, 6 literal matching terms")
    print("integral pairing: Lambda(R)=-1, Lambda(kappa R)=-kappa")
    print("Maurer-Cartan curvature=-kappa*(T+R), a literal diagonal boundary")
    print("target-free -kappa*R has residual pairing kappa and is not a cycle")
    print("verdict: scalar localization is valid but does not close the nullhomotopy")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
