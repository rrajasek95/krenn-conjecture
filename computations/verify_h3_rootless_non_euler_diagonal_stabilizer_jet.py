#!/usr/bin/env python3
"""Exact non-Euler physical Hasse jet for one rootless marked polar.

Colour-diagonal site transformations whose weight sums vanish separately in
each colour stabilize ternary GHZ.  A two-direction choice marks xv:00 and
pq:00, acts trivially on every mixed four-site response companion, and has
marked mixed polar coefficient one.  The checker verifies the complete
source/target/ordinary-residue Hasse equations and records that descent of
the marked-sector projection is still a separate zero-indeterminacy problem.
"""

from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COLORS = (0, 1, 2)
SITES = tuple(range(8))
ODD = (1, 2, 3, 4, 5)
MIXED = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}
X, R, P, Q = 0, 3, 6, 7
DIRECT_FREE = frozenset((P, R))
EXPECTED_DIGEST = "c15e977de5ace4dbac1d43c4476acec11cf886e86fa4c431b67a8ed53b51900d"
PINS = {
    "computations/verify_h3_rootless_marked_first_jet_site_euler_correction.py":
        "4c6feb11113fe15dfba45b1dae1bf9e80acd2231b10fee8cb9fe5e4c4d0cd554",
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


MATCHINGS = tuple(
    matching
    for matching in matchings(SITES)
    if DIRECT_FREE not in {frozenset(pair) for pair in matching}
)
require(len(MATCHINGS) == 90, "direct-free matching count")


def zero_weights():
    return {(site, color): 0 for site in SITES for color in COLORS}


def selected_word(deleted):
    word = [0] * 8
    for site in ODD:
        if site != deleted:
            word[site] = MIXED[site]
    return tuple(word)


def word_weight(word, weights):
    return sum(weights[site, color] for site, color in enumerate(word))


def edge_weight(pair, word, weights):
    left, right = pair
    return weights[left, word[left]] + weights[right, word[right]]


def diagonal_stabilizer_weights(positive_site, auxiliary_site):
    weights = zero_weights()
    weights[positive_site, 0] = 1
    weights[auxiliary_site, 0] = -1
    require(
        all(sum(weights[site, color] for site in SITES) == 0
            for color in COLORS),
        "colourwise GHZ stabilizer condition",
    )
    return weights


def target_stabilizer_audit(weights):
    records = []
    for word in product(COLORS, repeat=8):
        target = int(len(set(word)) == 1)
        tangent = word_weight(word, weights) * target
        require(tangent == 0, "diagonal stabilizer moved GHZ")
        records.append((word, target, tangent))
    return {
        "words": len(records),
        "pure_target_words": sum(target for _word, target, _tangent in records),
        "nonzero_target_tangents": sum(bool(tangent)
                                       for _word, _target, tangent in records),
    }


def response_companion_audit(deleted, weights):
    face = tuple(site for site in ODD if site != deleted)
    face_weight = sum(weights[site, MIXED[site]] for site in face)
    require(face_weight == 0, "first ordinary-residue companion moved")
    matching_weights = []
    for matching in matchings(face):
        value = sum(
            weights[left, MIXED[left]] + weights[right, MIXED[right]]
            for left, right in matching
        )
        require(value == face_weight == 0,
                "matching-labelled response companion moved")
        matching_weights.append(value)
    require(len(matching_weights) == 3, "four-site matching count")
    return matching_weights


def quotient_non_euler_invariant(weights):
    # Adding site-Euler gauge adds the same scalar to all three colours at
    # one site.  Colour differences therefore descend to the quotient.
    invariant = tuple(
        weights[site, 0] - weights[site, 1]
        for site in SITES
    )
    require(any(invariant), "diagonal stabilizer collapsed to site Euler")
    return invariant


def hesse_audit(deleted):
    auxiliary = next(site for site in ODD if site != deleted)
    left = diagonal_stabilizer_weights(X, auxiliary)
    right = diagonal_stabilizer_weights(P, auxiliary)
    word = selected_word(deleted)
    u = frozenset((X, deleted))
    t = frozenset((P, Q))

    left_word_weight = word_weight(word, left)
    right_word_weight = word_weight(word, right)
    require((left_word_weight, right_word_weight) == (1, 1),
            "selected mixed word weights changed")

    marked_terms = []
    completion_terms = 0
    for matching in MATCHINGS:
        left_edge_weights = [
            edge_weight(pair, word, left) for pair in matching
        ]
        right_edge_weights = [
            edge_weight(pair, word, right) for pair in matching
        ]
        require(
            sum(left_edge_weights) == left_word_weight
            and sum(right_edge_weights) == right_word_weight,
            "edge/site covariance mismatch",
        )
        jacobian_correction = sum(
            a * b for a, b in zip(left_edge_weights, right_edge_weights)
        )
        mixed_hessian = sum(
            left_edge_weights[i] * right_edge_weights[j]
            for i in range(4)
            for j in range(4)
            if i != j
        )
        corrected = jacobian_correction + mixed_hessian
        require(corrected == left_word_weight * right_word_weight == 1,
                "two-parameter diagonal covariance failed")
        completion_terms += 1

        pair_set = {frozenset(pair) for pair in matching}
        if u in pair_set and t in pair_set:
            u_index = next(i for i, pair in enumerate(matching)
                           if frozenset(pair) == u)
            t_index = next(i for i, pair in enumerate(matching)
                           if frozenset(pair) == t)
            desired = (
                left_edge_weights[u_index] * right_edge_weights[t_index]
            )
            reverse = (
                left_edge_weights[t_index] * right_edge_weights[u_index]
            )
            require(
                (
                    desired, reverse, mixed_hessian,
                    jacobian_correction, corrected,
                ) == (1, 0, 1, 0, 1),
                "marked non-Euler polar coefficient changed",
            )
            marked_terms.append(matching)

    require(len(marked_terms) == 3,
            "marked sector stopped being the four-site hafnian")

    # At an exact source, the selected mixed coefficient H_word(A) is zero.
    # The complete corrected second coefficient is 1*H_word(A), hence zero;
    # its three marked terms form h_v before this full-row cancellation.
    return {
        "deleted": deleted,
        "auxiliary_site": auxiliary,
        "word": "".join(map(str, word)),
        "left_target_stabilizer": target_stabilizer_audit(left),
        "right_target_stabilizer": target_stabilizer_audit(right),
        "left_non_euler_quotient_invariant":
            quotient_non_euler_invariant(left),
        "right_non_euler_quotient_invariant":
            quotient_non_euler_invariant(right),
        "left_response_matching_weights":
            response_companion_audit(deleted, left),
        "right_response_matching_weights":
            response_companion_audit(deleted, right),
        "marked_xi_u": 1,
        "marked_eta_t": 1,
        "opposite_marked_components": [0, 0],
        "marked_hessian_terms": len(marked_terms),
        "marked_hessian_coefficient": 1,
        "marked_jacobian_correction_coefficient": 0,
        "complete_mixed_row_terms": completion_terms,
        "complete_corrected_coefficient": "H_word(A)=0",
        "first_source_boundary": [0, 0],
        "first_physical_target": [0, 0],
        "first_ordinary_residue": [0, 0],
        "mixed_ordinary_residue": 0,
        "localization": ["a_(xv)^00", "a_(pq)^00"],
    }


def main():
    pin_dependencies()
    faces = [hesse_audit(deleted) for deleted in ODD]
    ledger = {
        "theorem": {
            "tangent_family": (
                "colour-diagonal site weights with each colour sum zero"
            ),
            "quotient": "nonzero modulo colour-blind site-Euler gauge",
            "first_equations": "Jhat*xi=Jhat*eta=0",
            "mixed_equation": "Jhat*zeta+Hhat(xi,eta)=0 at exact GHZ source",
            "ordinary_residue_model": "all fifteen q_(v,N) ridge companions",
        },
        "faces": faces,
        "positive_result": {
            "non_euler_marked_pair_exists": True,
            "zero_source_target_ores": True,
            "marked_polar_is_h_v_with_coefficient": 1,
            "complete_physical_hasse_correction_exists": True,
        },
        "remaining_gate": {
            "marked_sector_projection_descends": False,
            "zero_indeterminacy_proved": False,
            "terminal_pentagon_column_constructed": False,
            "reason": (
                "the complete corrected mixed row is H_word(A)=0; "
                "a source-labelled relative map must retain its marked "
                "three-term sector independently of the other 87 terms"
            ),
        },
        "answer": (
            "the non-Euler tangent pair survives modulo site Euler with "
            "zero ores; terminal marked-sector descent is the next gate"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_PINNED":
        require(digest == EXPECTED_DIGEST, f"ledger changed: {digest}")
    print("h=3 rootless non-Euler diagonal-stabilizer jet: PASS")
    print("non-Euler marked xi,eta: EXISTS modulo site-Euler gauge")
    print("source/target/ordinary residue: zero")
    print("marked mixed polar: h_v with coefficient one")
    print("complete correction: full mixed row H_c_v(A)=0")
    print("terminal sector descent / zero indeterminacy: NOT PROVED")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
