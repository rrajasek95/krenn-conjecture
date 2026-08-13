#!/usr/bin/env python3
"""Audit the first square from the trapped Hessian to Interface I.

After embedding the two endpoint rows at sites P=6,S=7, swapping tail
sites 3,4 and recolouring tail 0->1 sends the marked trapped occurrence
exactly to the covariance-curvature corner E+T0.  Endpoint oddization and
the two-site Weyl action therefore give the correct four-corner alpha.

The fixed-right tangent domain, however, varies only the P endpoint and q.
Its polarized second Hasse symbol has eight P-tail terms.  The physical
Interface-I codimension-two class has sixteen terms: the disjoint eight
S-tail terms are mandatory.  Endpoint oddization and tail Weyl transport
preserve this left/right split.  Hence Cartan naturality cannot fill the
missing half; a right-endpoint Hessian/comparison chart is the first exact
extension class.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import ast
import contextlib
import importlib.util
import io
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_trapped_carrier_occurrence_graph_hessian_cone_gate.py":
        "ce28ff5d25bf575c280a21c0e35c6dc1ebef54eb039ac94cdc25932a61b95829",
    "computations/verify_h3_residual_q_covariance_curvature_commutator.py":
        "46a3b6595ab147a17e80908157571a33b61e7faed32deb996506068e206baee9",
    "computations/verify_h3_order6_endpoint_odd_hpl_secondary_transfer.py":
        "5a89d25227562b397d6cf3f16306346ce7d9fd16fb73a0f0a4486355a7cef29e",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_h3_complete_hasse_cartan_naturality_square_gate.py":
        "3ea6a79bc6918cc4569bd12ad0b1634679c28037b687b6ae7c0e610e81998279",
    "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py":
        "647124e7c6646727653f7377d015d4f12010f39b8398b048a4ea065eedc73968",
}
EXPECTED_LEDGER_SHA256 = (
    "7f7f7b08d626af8ef8f27276f43b6b558d54cb6b11b7b1a065ba2176a4d1d98c"
)

P = 6
S = 7
ALPHA = (Q(-1), Q(1), Q(1), Q(-1))


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def edge(left: int, right: int, a: int, b: int):
    if left < right:
        return left, right, a, b
    return right, left, b, a


E_PLUS = (edge(P, 0, 1, 1), edge(S, 1, 1, 1))
E_MINUS = (edge(P, 1, 1, 1), edge(S, 0, 1, 1))
T_ZERO = (edge(2, 4, 1, 1), edge(3, 5, 1, 1))
T_ONE = (edge(2, 4, 2, 1), edge(3, 5, 1, 2))
CORNERS = tuple(tuple(sorted(endpoint + tail)) for endpoint, tail in (
    (E_PLUS, T_ZERO),
    (E_MINUS, T_ZERO),
    (E_PLUS, T_ONE),
    (E_MINUS, T_ONE),
))


def permute_site(cell, permutation):
    left, right, a, b = cell
    return edge(permutation.get(left, left), permutation.get(right, right), a, b)


def recolour_sites(cell, sites, old, new):
    left, right, a, b = cell
    if left in sites and a == old:
        a = new
    if right in sites and b == old:
        b = new
    return left, right, a, b


def endpoint_kind(cell):
    sites = cell[:2]
    if P in sites:
        return "P"
    if S in sites:
        return "S"
    return "q"


def shadow(allowed_kinds=None):
    answer = Counter()
    for coefficient, corner in zip(ALPHA, CORNERS, strict=True):
        moving = tuple(cell for cell in corner
                       if allowed_kinds is None
                       or endpoint_kind(cell) in allowed_kinds)
        for pair in combinations(moving, 2):
            answer[tuple(sorted(pair))] += coefficient
    return Counter({pair: value for pair, value in answer.items() if value})


def add_packets(left, right):
    answer = Counter(left)
    for pair, value in right.items():
        answer[pair] += value
    return Counter({pair: value for pair, value in answer.items() if value})


def swap_endpoint_sites(cell):
    return permute_site(cell, {0: 1, 1: 0})


def tail_weyl(cell):
    left, right, a, b = cell
    if left in (2, 5) and a in (1, 2):
        a = 3 - a
    if right in (2, 5) and b in (1, 2):
        b = 3 - b
    return left, right, a, b


def endpoint_transpose(cell):
    """P<->S together with residual endpoint swap 0<->1."""
    return permute_site(cell, {0: 1, 1: 0, P: S, S: P})


def transform_pair(pair, transform):
    return tuple(sorted(transform(cell) for cell in pair))


def rank(vectors):
    if not vectors:
        return 0
    labels = sorted(set().union(*(set(vector) for vector in vectors)))
    work = [[Q(vector.get(label, 0)) for label in labels]
            for vector in vectors]
    row = 0
    for column in range(len(labels)):
        pivot = next((index for index in range(row, len(work))
                      if work[index][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        value = work[row][column]
        work[row] = [entry / value for entry in work[row]]
        for index in range(len(work)):
            if index == row or not work[index][column]:
                continue
            value = work[index][column]
            work[index] = [left - value * right for left, right
                           in zip(work[index], work[row], strict=True)]
        row += 1
    return row


def coarse_corner_profile(packet):
    answer = [Q(0)] * len(CORNERS)
    for index, corner in enumerate(CORNERS):
        corner_pairs = set(combinations(corner, 2))
        answer[index] = sum((value for pair, value in packet.items()
                             if tuple(sorted(pair)) in {
                                 tuple(sorted(item)) for item in corner_pairs
                             }), Q(0))
    return tuple(answer)


def audit():
    actual_pins = {}
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative,
                                     actual))
        actual_pins[relative] = actual

    # The six-site marked occurrence, embedded at P,S, is the full matching
    # P0|S1|23|45.  Tail permutation (3 4) followed by 0->1 recolouring at
    # sites 2..5 lands exactly on E+T0.
    trapped = tuple(sorted((
        edge(P, 0, 1, 1),
        edge(S, 1, 1, 1),
        edge(2, 3, 0, 0),
        edge(4, 5, 0, 0),
    )))
    normalized = tuple(sorted(
        recolour_sites(permute_site(cell, {3: 4, 4: 3}),
                       {2, 3, 4, 5}, 0, 1)
        for cell in trapped
    ))
    require(normalized == CORNERS[0],
            "the trapped occurrence stopped landing on E+T0")

    # Verify the four-corner orbit and signs literally.
    require(tuple(sorted(swap_endpoint_sites(cell)
                         for cell in CORNERS[0])) == CORNERS[1],
            "endpoint oddization stopped sending E+T0 to E-T0")
    require(tuple(sorted(tail_weyl(cell)
                         for cell in CORNERS[0])) == CORNERS[2],
            "tail Weyl stopped sending E+T0 to E+T1")
    require(tuple(sorted(tail_weyl(swap_endpoint_sites(cell))
                         for cell in CORNERS[0])) == CORNERS[3],
            "the transported fourth corner changed")

    full = shadow()
    left = shadow({"P", "q"})       # fixed right endpoint s
    right = shadow({"S", "q"})      # fixed left endpoint p
    require(len(full) == 16 and set(full.values()) == {Q(-1), Q(1)},
            "the physical codimension-two -delta packet changed")
    require(len(left) == len(right) == 8,
            "fixed-endpoint Hessian half-size changed")
    require(not (set(left) & set(right)),
            "left and right endpoint Hessian halves began to overlap")
    require(add_packets(left, right) == full,
            "the two endpoint polarizations stopped summing to -delta")
    require(all(any(endpoint_kind(cell) == "P" for cell in pair)
                and any(endpoint_kind(cell) == "q" for cell in pair)
                for pair in left),
            "fixed-right Hessian acquired a non-P-tail term")
    require(all(any(endpoint_kind(cell) == "S" for cell in pair)
                and any(endpoint_kind(cell) == "q" for cell in pair)
                for pair in right),
            "fixed-left Hessian acquired a non-S-tail term")

    # Both symmetry generators preserve endpoint type, hence cannot turn the
    # left Hasse half into the missing right half.
    for transform in (swap_endpoint_sites, tail_weyl):
        transformed_left = {
            transform_pair(pair, transform): value for pair, value in left.items()
        }
        require(all(any(endpoint_kind(cell) == "P" for cell in pair)
                    for pair in transformed_left),
                "Cartan/Weyl transport changed P polarization into S")

    # The combined endpoint transpose fixes every four-edge corner and sends
    # the fixed-right half to the fixed-left half with the correct sign.
    require(all(tuple(sorted(endpoint_transpose(cell) for cell in corner))
                == corner for corner in CORNERS),
            "combined endpoint transpose stopped fixing the corner orbit")
    transpose_left = Counter({
        transform_pair(pair, endpoint_transpose): value
        for pair, value in left.items()
    })
    require(transpose_left == right,
            "combined endpoint transpose stopped constructing epsilon_S")

    # Coarse four-corner shadows hide the discrepancy: each half is a scalar
    # multiple 2*alpha, while the full packet is 4*alpha.
    coarse_left = coarse_corner_profile(left)
    coarse_right = coarse_corner_profile(right)
    coarse_full = coarse_corner_profile(full)
    require(coarse_left == coarse_right == tuple(2 * value for value in ALPHA)
            and coarse_full == tuple(4 * value for value in ALPHA),
            ("coarse corner normalization changed", coarse_left,
             coarse_right, coarse_full))

    # The quotient obstruction is literally the right half.  Its eight
    # coordinate functionals are independent modulo the left half.
    right_basis = [Counter({pair: value}) for pair, value in right.items()]
    require(rank((left,)) == 1 and rank(right_basis) == 8
            and rank((left,) + tuple(right_basis)) == 9,
            "endpoint-polarization quotient rank changed")

    # Audit the actual canonical repeated grade and six-term matching rows.
    # The same transpose is a physical symmetry, but it transports them to a
    # conjugate component rather than preserving the literal component.
    separator_path = ROOT / (
        "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py"
    )
    specification = importlib.util.spec_from_file_location(
        "endpoint_polarization_separator", separator_path
    )
    require(specification is not None and specification.loader is not None,
            "cannot import physical six-term separator")
    separator = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(separator)
    with contextlib.redirect_stdout(io.StringIO()):
        separator_ledger = separator.audit()
    fine_degree = tuple(separator_ledger["canonical_fine_degree"])
    transpose_permutation = {0: 1, 1: 0, P: S, S: P}
    transpose_degree = [0] * len(fine_degree)
    for site in range(8):
        for colour in range(3):
            transpose_degree[3 * transpose_permutation.get(site, site) + colour] = (
                fine_degree[3 * site + colour]
            )
    transpose_degree = tuple(transpose_degree)
    require(transpose_degree != fine_degree,
            "canonical repeated grade unexpectedly became transpose invariant")
    selected_features = tuple(ast.literal_eval(value) for value in
                              separator_ledger["selected_private_features"])
    transpose_features = tuple(tuple(sorted(endpoint_transpose(cell)
                                              for cell in monomial))
                               for monomial in selected_features)
    require(not (set(selected_features) & set(transpose_features)),
            "the six private rows unexpectedly became transpose invariant")

    return {
        "theorem": "fixed-right Hessian to six-term endpoint-polarization gate",
        "pins": actual_pins,
        "normalization": {
            "trapped_full_word": "11000011",
            "tail_site_permutation": "(3 4)",
            "tail_recolouring": "0->1 at sites 2,3,4,5",
            "normalized_corner": "E+T0",
            "pure_Interface_I_word": "11111111",
            "tail_Weyl_word": "11211211",
            "word_and_corner_grade_match": True,
        },
        "corner_square": {
            "order": ["E+T0", "E-T0", "E+T1", "E-T1"],
            "alpha": [int(value) for value in ALPHA],
            "operator": "(1-s)(w-1)",
        },
        "polarized_second_hasse": {
            "physical_full_minus_delta_terms": len(full),
            "fixed_right_P_tail_terms": len(left),
            "missing_fixed_left_S_tail_terms": len(right),
            "left_right_support_intersection": 0,
            "full_equals_left_plus_right": True,
            "coarse_left": [int(value) for value in coarse_left],
            "coarse_right": [int(value) for value in coarse_right],
            "coarse_full": [int(value) for value in coarse_full],
            "warning": (
                "after rescaling, either eight-term half has the same four-"
                "corner alpha shadow; only literal endpoint labels detect "
                "the missing half"
            ),
        },
        "commuting_square": {
            "top": "fixed-right occurrence graph Hessian H2_(p,q)(f)",
            "left_to_bottom": (
                "tail normalization followed by endpoint-odd Cartan/Weyl "
                "naturality"
            ),
            "bottom_image": "C2_P: eight P-tail terms",
            "required_bottom": "C2_full=C2_P direct-sum C2_S",
            "defect_Ext_class": "epsilon_S=C2_S, the eight S-tail terms",
            "criterion": (
                "the square reaches the physical -delta class iff a source-"
                "valid fixed-left/right-endpoint comparison supplies epsilon_S"
            ),
        },
        "why_Cartan_does_not_fill_it": (
            "the endpoint site swap 0<->1 and the tail Weyl action preserve "
            "whether a Hasse pair uses external endpoint P or S"
        ),
        "minimal_positive_extension": {
            "domain": (
                "append the 36 right-endpoint s columns to the 36 p plus "
                "135 q columns, and use the full four-factor anchor polar"
            ),
            "anchor": "df has dp, ds, dq23, dq45 terms",
            "comparison": (
                "construct the transpose fixed-left Hessian in the identical "
                "word/fine/repeated grade and prove its S-tail symbol is "
                "epsilon_S with compatible augmented terminals"
            ),
        },
        "endpoint_transpose_audit": {
            "involution": (
                "P<->S and response-head transpose, composed with residual "
                "site swap 0<->1"
            ),
            "complete_source_equations": (
                "p_i s_j q^[2]=delta_ij X_i transports to the head-transpose "
                "equation; q^[3]=X0 is fixed"
            ),
            "corner_orbit_fixed": True,
            "P_tail_to_S_tail": True,
            "protected_marked_product_fixed": True,
            "target_and_word": "fixed on the selected equal-colour endpoints",
            "ores_eta_sigma": (
                "transport equivariantly; eta_0 and eta_1 are relabelled, "
                "and the external P-S sigma edge is fixed"
            ),
            "associated_graded_square_closed": True,
            "canonical_repeated_fine_grade_preserved": False,
            "canonical_fine_degree": list(fine_degree),
            "transpose_fine_degree": list(transpose_degree),
            "six_private_feature_overlap": len(
                set(selected_features) & set(transpose_features)
            ),
            "physical_six_term_readout": (
                "Lambda transports to a conjugate physical Lambda^T, but is "
                "not the same labelled sum-of-six-minus-ainc row"
            ),
            "remaining_grade_map": (
                "a shifted repeated-grade comparison identifying the "
                "transpose component with the canonical faces-(3,5) component"
            ),
        },
        "curvature_shortcut_guard": {
            "proved": (
                "a nonlifted xi has a physical output dual psi with psi*A=0 "
                "and psi(F_[2](xi)) nonzero"
            ),
            "not_proved": (
                "psi can be chosen in one response head/word and its detected "
                "Hessian is a decomposable common-q endpoint minor"
            ),
            "existing_Fitting_input_needed": (
                "same-head response contraction plus a nonzero evaluated "
                "decorated cofactor/minor and endpoint visibility"
            ),
            "conclusion": (
                "the intrinsic curvature dual is not yet a typed active-fan "
                "carrier; a block-localization/decomposability theorem is "
                "an alternative to supplying epsilon_S"
            ),
        },
        "cross_gate_reduced_Eq_test": {
            "Interface_II_symbol_label": (
                "second Hasse face of response generator R_11,110000"
            ),
            "literal_symbol_image": "C2_P in the response endpoint-tail sector",
            "pure_Eq_projection": 0,
            "candidate_common_class": "(H0-u)*e_Eq",
            "candidate_label": "unary/pure-Eq conormal sector",
            "graph_coordinate_warning": (
                "u_f is constrained by u_f=f and varies with the marked "
                "occurrence; it is not the global target homogenizer u"
            ),
            "verdict": (
                "the complete diagonal response-to-PP Hasse symbol does not "
                "send F_[2](xi) to reduced Eq.  Such a projection requires "
                "an off-diagonal response-to-Eq normal/mapping-cone map"
            ),
            "possible_unification_after_extension": (
                "a single augmented cell could carry both epsilon_S and the "
                "reduced-Eq face, but this is the missing comparison rather "
                "than a consequence of polarization"
            ),
        },
        "scope": (
            "exact associated-graded word, corner, endpoint polarization and "
            "quotient calculation.  It does not construct the right-endpoint "
            "Hessian lift, the full augmented comparison square, or an "
            "active-fan landing for an arbitrary output curvature dual"
        ),
    }


def main() -> None:
    ledger = audit()
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("endpoint polarization ledger changed", digest))
    print("h3 trapped Hessian -> six-term endpoint polarization: PASS")
    print("word/fine corner normalization: exact E+T0 -> alpha square")
    print("fixed-right Hasse image: 8 P-tail terms; physical -delta: 16")
    print("endpoint transpose constructs the 8 disjoint S-tail terms")
    print("remaining defect: conjugate repeated grade / Lambda^T != Lambda")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
