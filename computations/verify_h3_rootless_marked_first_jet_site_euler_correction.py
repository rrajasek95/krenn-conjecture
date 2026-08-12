#!/usr/bin/env python3
"""Exact physical first-jet correction for the five marked h=3 polars.

At scalar coefficient level each marked Jacobian column has a private
residual-matching feature.  At the first localized polynomial level, however,
the site-Euler torus gives an exact physical kernel vector with marked
coefficient one.  Two such commuting torus directions also give the literal
mixed Hasse correction.  The checker does not invent an ordinary-residue or
terminal landing map for that corrected physical jet.
"""

from collections import defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COLORS = (0, 1, 2)
SITES = tuple(range(8))
ODD = (1, 2, 3, 4, 5)
MIXED = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}
X, R, P, Q = 0, 3, 6, 7
DIRECT_FREE = frozenset((P, R))
EXPECTED_DIGEST = "c4bfb9a3243580c015f55e0cf9492a9b949c6a59697d5c7e21f98e90e8ccec74"
PINS = {
    "computations/verify_h3_rootless_five_ridge_response_bianchi_cokernel.py":
        "2e09f9be1ed1b57821c64dd690df7e4d6b2efebe93cb8aae9ff0a58b3190022d",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def edge(left, right, left_color, right_color):
    if left < right:
        return left, right, left_color, right_color
    return right, left, right_color, left_color


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


def surviving_matchings():
    answer = tuple(
        matching
        for matching in matchings(SITES)
        if DIRECT_FREE not in {frozenset(pair) for pair in matching}
    )
    require(len(answer) == 90, "direct-free matching count")
    return answer


MATCHINGS = surviving_matchings()
PHYSICAL_EDGES = tuple(combinations(SITES, 2))
COORDINATES = tuple(
    edge(left, right, left_color, right_color)
    for left, right in PHYSICAL_EDGES
    for left_color in COLORS
    for right_color in COLORS
)


def selected_word(deleted):
    word = [0] * 8
    for site in ODD:
        if site != deleted:
            word[site] = MIXED[site]
    return tuple(word)


def monomial(matching, word):
    return tuple(sorted(
        edge(left, right, word[left], word[right])
        for left, right in matching
    ))


def derivative_columns(word):
    columns = {coordinate: set() for coordinate in COORDINATES}
    for matching in MATCHINGS:
        term = monomial(matching, word)
        for variable in term:
            residual = list(term)
            residual.remove(variable)
            columns[variable].add(tuple(residual))
    return columns


def scalar_membership_audit():
    records = []
    for deleted in ODD:
        word = selected_word(deleted)
        columns = derivative_columns(word)
        nonzero = {key: value for key, value in columns.items() if value}
        require(len(columns) == 252 and len(nonzero) == 27,
                "physical coordinate inventory changed")
        require(sum(map(len, nonzero.values())) == 360,
                "selected-row Jacobian incidence changed")

        owners = defaultdict(list)
        for coordinate, features in nonzero.items():
            for feature in features:
                owners[feature].append(coordinate)
        require(len(owners) == 360, "derivative supports collided")
        require(all(len(values) == 1 for values in owners.values()),
                "one residual feature has multiple coordinate owners")

        u = edge(X, deleted, 0, 0)
        t = edge(P, Q, 0, 0)
        for name, marked in (("u", u), ("t", t)):
            require(marked in nonzero, f"{name}: marked column vanished")
            separator = min(nonzero[marked])
            require(owners[separator] == [marked],
                    f"{name}: primitive separator lost uniqueness")
            records.append({
                "deleted": deleted,
                "marked": name,
                "word": "".join(map(str, word)),
                "complete_coordinate_columns": len(columns),
                "nonzero_coordinate_columns": len(nonzero),
                "zero_coordinate_columns": len(columns) - len(nonzero),
                "total_source_features": len(owners),
                "marked_terms": len(nonzero[marked]),
                "primitive_separator": str(separator),
                "separator_on_marked": 1,
                "separator_on_other_columns": 0,
                "scalar_marked_one_kernel_exists": False,
            })
    return records


def site_weights(positive, negative):
    weights = {site: 0 for site in SITES}
    weights[positive] = 1
    weights[negative] = -1
    require(sum(weights.values()) == 0, "site weights not target preserving")
    return weights


def edge_weight(pair, weights):
    left, right = pair
    return weights[left] + weights[right]


def matching_hasse_coefficients(matching, left_weights, right_weights):
    left = [edge_weight(pair, left_weights) for pair in matching]
    right = [edge_weight(pair, right_weights) for pair in matching]
    require(sum(left) == sum(left_weights.values()) == 0,
            "left site-Euler first derivative")
    require(sum(right) == sum(right_weights.values()) == 0,
            "right site-Euler first derivative")
    jacobian_correction = sum(a * b for a, b in zip(left, right))
    mixed_hessian = sum(
        left[i] * right[j]
        for i in range(4)
        for j in range(4)
        if i != j
    )
    require(jacobian_correction + mixed_hessian == 0,
            "mixed Hasse correction failed")
    return mixed_hessian, jacobian_correction


def global_site_euler_audit():
    # The proof is word-independent: decorating a matching changes variable
    # names but not its four endpoint weights.  Hence these 90 checks apply
    # to every one of the complete 3^8 literal output rows.
    complete_rows = len(tuple(product(COLORS, repeat=8)))
    require(complete_rows == 6561, "full literal word inventory changed")

    normalized = []
    for deleted in ODD:
        # Candidate A isolates the ordered marked polar, but acts on the
        # four-site response companion and therefore has nonzero ores.
        auxiliary = next(site for site in ODD if site != deleted)
        left_weights = site_weights(X, auxiliary)
        right_weights = site_weights(P, auxiliary)
        u_pair = (X, deleted)
        t_pair = (P, Q)
        require(edge_weight(u_pair, left_weights) == 1,
                "left torus does not mark u")
        require(edge_weight(t_pair, right_weights) == 1,
                "right torus does not mark t")
        require(edge_weight(t_pair, left_weights) == 0,
                "left torus also moves t")
        require(edge_weight(u_pair, right_weights) == 0,
                "right torus also moves u")
        require(set(u_pair).isdisjoint(t_pair),
                "marked Hessian variables stopped being disjoint")

        for matching in MATCHINGS:
            mixed_hessian, jacobian_correction = (
                matching_hasse_coefficients(
                    matching, left_weights, right_weights
                )
            )

            pair_set = {frozenset(pair) for pair in matching}
            if frozenset(u_pair) in pair_set and frozenset(t_pair) in pair_set:
                desired = (
                    edge_weight(u_pair, left_weights)
                    * edge_weight(t_pair, right_weights)
                )
                reverse = (
                    edge_weight(t_pair, left_weights)
                    * edge_weight(u_pair, right_weights)
                )
                require(
                    (desired, reverse, mixed_hessian, jacobian_correction)
                    == (1, 0, -1, 1),
                    "marked polar/gauge cancellation changed",
                )

        face = tuple(site for site in ODD if site != deleted)
        left_face_sum = sum(left_weights[site] for site in face)
        right_face_sum = sum(right_weights[site] for site in face)
        endpoint_aggregate = (
            sum(left_weights[site] for site in (X, deleted, P, Q))
            * sum(right_weights[site] for site in (X, deleted, P, Q))
        )
        require(
            (left_face_sum, right_face_sum, endpoint_aggregate,
             left_face_sum * right_face_sum) == (-1, -1, 1, 1),
            "anchor-one candidate lost its residue companion",
        )

        # Candidate B acts only at x and p.  It is invisible on every
        # q_(v,N) response monomial, but the opposite marked components now
        # cancel the primitive endpoint anchor.
        ores_left = site_weights(X, P)
        ores_right = site_weights(P, X)
        require(
            (
                edge_weight(u_pair, ores_left),
                edge_weight(t_pair, ores_right),
                edge_weight(t_pair, ores_left),
                edge_weight(u_pair, ores_right),
            ) == (1, 1, -1, -1),
            "ores-zero marked weights changed",
        )
        for matching in MATCHINGS:
            mixed_hessian, jacobian_correction = (
                matching_hasse_coefficients(
                    matching, ores_left, ores_right
                )
            )
            pair_set = {frozenset(pair) for pair in matching}
            if frozenset(u_pair) in pair_set and frozenset(t_pair) in pair_set:
                require(
                    (mixed_hessian, jacobian_correction) == (2, -2),
                    "ores-zero gauge stopped cancelling the anchor",
                )
        require(
            all(ores_left[site] == ores_right[site] == 0 for site in face),
            "ores-zero tangent acts on a residual face site",
        )

        normalized.append({
            "deleted": deleted,
            "auxiliary_site": auxiliary,
            "anchor_one_left_direction": (
                "xi_e=(lambda_i+lambda_j)*a_e/a_(xv)^00, "
                "lambda_x=1,lambda_aux=-1"
            ),
            "anchor_one_right_direction": (
                "eta_e=(mu_i+mu_j)*a_e/a_(pq)^00, "
                "mu_p=1,mu_aux=-1"
            ),
            "marked_xi_u": 1,
            "marked_eta_t": 1,
            "marked_mixed_hessian_coefficient": 1,
            "reverse_marked_hessian_coefficient": 0,
            "full_hessian_coefficient_on_marked_matching": -1,
            "jacobian_correction_on_marked_matching": 1,
            "corrected_physical_coefficient": 0,
            "anchor_one_endpoint_aggregate": endpoint_aggregate,
            "anchor_one_ordinary_residue": left_face_sum * right_face_sum,
            "ores_zero_left_weights": ores_left,
            "ores_zero_right_weights": ores_right,
            "ores_zero_marked_hessian": 2,
            "ores_zero_jacobian_correction": -2,
            "ores_zero_endpoint_anchor": 0,
            "ores_zero_ordinary_residue": 0,
            "mixed_correction": (
                "zeta_e=(lambda_i+lambda_j)(mu_i+mu_j)"
                "*a_e/(a_(xv)^00*a_(pq)^00)"
            ),
            "source_boundary": 0,
            "physical_target": 0,
            "coefficient_open": ["a_(xv)^00", "a_(pq)^00"],
        })

    return {
        "direct_free_matchings_checked_per_face": len(MATCHINGS),
        "literal_output_words_covered": complete_rows,
        "literal_matching_rows_covered_per_face": complete_rows * len(MATCHINGS),
        "first_hasse_equations": "J*xi=J*eta=0",
        "second_hasse_equation": "J*zeta+H(xi,eta)=0",
        "physical_cokernel_class": 0,
        "primitive_anchor_incidence_supplied": False,
        "anchor_ores_conservation": (
            "corrected endpoint anchor=(1+b)(1+c)="
            "four-site response companion"
        ),
        "normalized_faces": normalized,
    }


def symbolic_anchor_ores_conservation():
    records = []
    for b in range(-3, 4):
        for c in range(-3, 4):
            first_ores_left = -(1 + b)
            first_ores_right = -(1 + c)
            marked_hessian = 1 + b * c
            endpoint_jacobian_correction = b + c
            endpoint_anchor = marked_hessian + endpoint_jacobian_correction
            mixed_ores = first_ores_left * first_ores_right
            require(
                endpoint_anchor == mixed_ores == (1 + b) * (1 + c),
                "anchor/ores conservation identity failed",
            )
            if first_ores_left == first_ores_right == 0:
                require((b, c, endpoint_anchor) == (-1, -1, 0),
                        "zero first ores retained a primitive anchor")
            records.append({
                "b": b,
                "c": c,
                "first_ores": [first_ores_left, first_ores_right],
                "marked_hessian": marked_hessian,
                "endpoint_J_zeta": endpoint_jacobian_correction,
                "corrected_endpoint_anchor": endpoint_anchor,
                "mixed_ordinary_residue": mixed_ores,
            })
    return {
        "identity": (
            "(1+bc)+(b+c)=(1+b)(1+c)="
            "(-(1+b))*(-(1+c))"
        ),
        "integer_tests": records,
        "zero_first_ores_forces": {"b": -1, "c": -1, "anchor": 0},
    }


def main():
    pin_dependencies()
    ledger = {
        "scalar_complete_column_test": scalar_membership_audit(),
        "localized_site_euler_correction": global_site_euler_audit(),
        "anchor_ordinary_residue_conservation":
            symbolic_anchor_ores_conservation(),
        "augmented_status": {
            "source_boundary": "zero on all complete literal rows",
            "physical_target": "zero because the full output tensor is fixed",
            "ordinary_residue": (
                "exact five-ridge q_(v,N) companion; equals endpoint anchor"
            ),
            "terminal_grade_map": (
                "sector polar has anchor one only when ordinary residue is one"
            ),
            "zero_indeterminacy": (
                "site-Euler family cannot give anchor one with ores zero"
            ),
            "corrected_source_class": "zero gauge class",
            "primitive_relative_anchor": "not supplied by a torus orbit",
            "P_e_v_constructed": False,
        },
        "coefficient_ring_dichotomy": {
            "constant_coordinate_span": "primitive separator; no correction",
            "localized_polynomial_span": "site-Euler correction exists",
        },
        "answer": (
            "site-Euler jets satisfy anchor=ordinary residue; zero augmented "
            "residue forces zero anchor, so no P(e_v) is constructed"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_PINNED":
        require(digest == EXPECTED_DIGEST, f"ledger changed: {digest}")
    print("h=3 rootless marked first-jet site-Euler correction: PASS")
    print("scalar coordinate columns: separated in the selected mixed row")
    print("localized physical coordinates: exact site-Euler first jets")
    print("mixed Hasse correction: exact and gauge-zero on all 6561 rows")
    print("marked polar survives only in the sector projection, not physically")
    print("anchor/ordinary-residue conservation: anchor=ores=(1+b)(1+c)")
    print("zero first ores forces b=c=-1 and corrected anchor zero")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
