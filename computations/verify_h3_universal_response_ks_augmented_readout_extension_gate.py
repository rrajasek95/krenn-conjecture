#!/usr/bin/env python3
"""Audit augmented readouts on the universal response KS generator.

The response deformation canonically supplies ``d epsilon_s=-c_f``.  Together
with the old aggregate response/target conormal it also supplies the scaled
formal anchor law ``c_f+B=90 dz_f-du``.  Matching naturality fixes the
aggregate-matching part of physical q.

It does not canonically assign the independent augmented rows (ainc, hence q,
W, the labelled shifted ridge, or eta/sigma) to epsilon_s.  The same
unaugmented differential admits arbitrary values in those rows.  In
particular, a q defect supported only on the new formal generator need not
have a witness in the old physical source and cannot trigger the physical
generator/Fredholm alternative.

Thus word/fine/repeated-grade landing of epsilon_s in the complete physical
AugP2/E14 domain remains logically prior to terminal promotion.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
N = 90
PINS = {
    "computations/verify_h3_universal_response_deformation_e14_orbit_ks_gate.py":
        "39713f3683dd3d2376e5a911987ee3670ec291cf850072d6b4932e7a93745fc7",
    "notes/h3-universal-response-deformation-e14-orbit-ks-gate.md":
        "d9032c365e8fd8fb5baf320dcc5adac8832c023119fb7d4df69d02cce3d5878f",
    "computations/verify_dark_cartan_physical_q_protected_quotient_comparison.py":
        "eb56cdb4ab1915f8ce35ab3acf0398b4f526c52a17c9c8ebafcc7a5ad4f86bcc",
    "notes/dark-cartan-physical-q-protected-quotient-comparison.md":
        "a99c5a53e36917db9cf5e69d61a68188fbdf051890c9e99347d8aa0ac96fae42",
    "computations/verify_h3_scaled_occurrence_anchor_bridge_alternative.py":
        "ba01612572513e02c60bd5d9a319d8302013e3d73e6a52ae229af8b07dd02507",
    "notes/h3-scaled-occurrence-anchor-bridge-alternative.md":
        "d89d40b3ff69e0d7dc8105b1aa1eea40dceabc84007c1b9759d1a2932ecba572",
    "computations/verify_h3_relative_occurrence_e14_w_carrier_landing_gate.py":
        "37f571234346c8a90465a5e021bb5ed97b0caec68e31a8b80346d25f94c9f337",
    "notes/h3-relative-occurrence-e14-w-carrier-landing-gate.md":
        "a4a0e1be3cff6779f3641f6c3f1faa6431eac01b85a4cdf1bfbfc9d595d56888",
    "computations/verify_h3_cplus_q_ridge_w_terminal_reduction.py":
        "b2ace6e49aa5ec1b8347a0e88cc39f36e5d773e1aab1d82f424533de8ce52a9a",
    "notes/h3-cplus-q-ridge-w-terminal-reduction.md":
        "856a4932b1c28dfba34195fa2b37dbf0b3a54cbc98e1f80fe0195535885a7e69",
    "computations/verify_h3_universal_graph_derived_base_change_physical_descent_gate.py":
        "9e60fb8410288a192b8be3b59938e5e7ba4ea42b455fee67b94ca6ef37777fde",
    "notes/h3-universal-graph-derived-base-change-physical-descent-gate.md":
        "510f7fd8912fe26fe27f3375497d19e90389c7ac94f66c4c7f674ea9565fe475",
}
EXPECTED_LEDGER_SHA256 = "0deb498dc7249280d35d825a205061c93da1dcf6d2bee3bd9644e845a7a6e1df"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0))
                 for entries in zip(*vectors, strict=True))


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank width")
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(height):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def formal_anchor_and_matching_audit() -> dict[str, object]:
    # Coordinates are (marked occurrence z_f, aggregate of the other 89
    # occurrences, global target anchor u).  B is the old aggregate
    # response/target conormal and c_f is the centered numerator.
    B = tuple(map(Q, (1, 1, -1)))
    c_f = tuple(map(Q, (N - 1, -1, 0)))
    scaled_anchor = tuple(map(Q, (N, 0, -1)))
    require(add(c_f, B) == scaled_anchor
            and rank((B, c_f)) == 2,
            "the scaled anchor identity changed")

    # Matching naturality determines M(epsilon_s), but q=M-ainc.  Two
    # choices of the independent ainc row have the same M value and
    # different q values.
    matching_value = Q(1)
    q_without_ainc = matching_value - Q(0)
    q_with_ainc = matching_value - Q(1)
    require(q_without_ainc == 1 and q_with_ainc == 0,
            "the M-minus-ainc guard changed")
    return {
        "coordinate_order": ["z_f", "sum_unmarked_z", "u"],
        "aggregate_response_target_conormal_B": [1, 1, -1],
        "centered_conormal_c_f": [N - 1, -1, 0],
        "identity": "c_f+B=90*dz_f-du",
        "formal_scaled_anchor_is_canonical": True,
        "physical_target_anchor_landing_constructed": False,
        "matching_aggregate_on_epsilon_s_is_B_natural": True,
        "q_definition": "q=M-ainc",
        "ainc_from_response_differentiation": False,
        "same_M_two_possible_q_values": [1, 0],
    }


def augmented_extension_ambiguity_audit() -> dict[str, object]:
    # An augmented column consists of one principal-boundary coordinate and
    # five external rows.  Fixing d epsilon_s=-c_f fixes only the first
    # coordinate.  Unit changes in each external row leave the underlying
    # response differential unchanged and are linearly independent.
    rows = ("ainc/q", "W", "labelled_ridge", "eta", "sigma")
    base = (Q(1),) + (Q(0),) * len(rows)
    alternatives = tuple(
        (Q(1),) + tuple(Q(index == row) for index in range(len(rows)))
        for row in range(len(rows))
    )
    differences = tuple(
        tuple(alt[index] - base[index] for index in range(len(base)))
        for alt in alternatives
    )
    require(all(alt[0] == base[0] for alt in alternatives)
            and rank(differences) == len(rows),
            "the augmented-extension ambiguity changed")
    return {
        "fixed_unaugmented_column": "d epsilon_s=-c_f",
        "independent_external_rows": list(rows),
        "dimension_of_extension_ambiguity": len(rows),
        "unaugmented_response_family_determines_external_rows": False,
        "formal_trivial_eta_sigma_extension_available": True,
        "formal_trivial_eta_sigma_is_physical_ridge_packet": False,
        "eta_sigma_naturality_consequence": (
            "once the labelled -dOmega ridge is supplied, its unique "
            "contractions transport; naturality does not supply the ridge"
        ),
        "W_consequence": (
            "the independent occurrence-to-E14 W landing remains the "
            "rank-one equation w_E14=t"
        ),
    }


def premature_q_promotion_counterguard() -> dict[str, object]:
    # L_phys=<e0> and J_phys is an isomorphism, so it has neither a kernel
    # generator nor a left cokernel separator.  The formal extension adds
    # epsilon with J(epsilon)=0 and q(epsilon)=1.  Its q defect is nonzero,
    # but its only witness lies outside L_phys.
    J_formal = tuple(map(Q, (1, 0)))
    q_formal = tuple(map(Q, (0, 1)))
    physical_basis = tuple(map(Q, (1, 0)))
    epsilon_s = tuple(map(Q, (0, 1)))
    require(dot(J_formal, physical_basis) == 1
            and dot(J_formal, epsilon_s) == 0
            and dot(q_formal, epsilon_s) == 1
            and rank((physical_basis,)) == 1,
            "the premature-q counterguard changed")
    return {
        "physical_domain": "L_phys=<e0>",
        "physical_protected_map": "J_phys(e0)=1",
        "physical_kernel_dimension": 0,
        "physical_left_cokernel_dimension": 0,
        "formal_extension": "L_formal=L_phys plus <epsilon_s>",
        "formal_values": "J(epsilon_s)=0, q(epsilon_s)=1",
        "formal_q_defect_nonzero": True,
        "formal_defect_witness_is_physical": False,
        "generator_or_Fredholm_promotion_valid": False,
        "missing_hypothesis": (
            "a protected word/fine/repeated-grade comparison placing "
            "epsilon_s in a complete physical relative domain with physical q"
        ),
    }


def toric_shear_cross_term_audit() -> dict[str, object]:
    # Four corners are
    #   endpoint orientation 10/01 x residual matching 23|45 / 24|35.
    # The differentiated toric minor is the unique interaction character.
    xi = tuple(map(Q, (1, -1, -1, 1)))
    constant = tuple(map(Q, (1, 1, 1, 1)))
    endpoint_10 = tuple(map(Q, (1, 1, 0, 0)))
    endpoint_01 = tuple(map(Q, (0, 0, 1, 1)))
    matching_2345 = tuple(map(Q, (1, 0, 1, 0)))
    matching_2435 = tuple(map(Q, (0, 1, 0, 1)))
    separable_rows = (
        constant, endpoint_10, endpoint_01,
        matching_2345, matching_2435,
    )
    require(rank(separable_rows) == 3
            and all(dot(row, xi) == 0 for row in separable_rows)
            and rank(separable_rows + (xi,)) == 4,
            "the endpoint/matching toric interaction changed")

    # In the coefficient shadow, ainc depends only on endpoint orientation
    # and the matching aggregate only on the residual matching.  Their
    # difference is still separable and therefore cannot detect xi.
    aggregate_matching = add(matching_2345, (Q(0),) * 4)
    anchor_incidence = endpoint_10
    q_shadow = tuple(left - right for left, right in
                     zip(aggregate_matching, anchor_incidence, strict=True))
    require(dot(aggregate_matching, xi) == 0
            and dot(anchor_incidence, xi) == 0
            and dot(q_shadow, xi) == 0,
            "the toric interaction acquired a separable q shadow")
    return {
        "four_corner_order": [
            "p1s0*q23q45", "p1s0*q24q35",
            "p0s1*q23q45", "p0s1*q24q35",
        ],
        "toric_minor_derivative": [1, -1, -1, 1],
        "polynomial": (
            "(p1s0-p0s1)(q23q45-q24q35)"
        ),
        "separable_endpoint_plus_matching_row_rank": 3,
        "mixed_annihilator_dimension": 1,
        "aggregate_matching_shadow_on_derivative": 0,
        "anchor_incidence_shadow_on_derivative": 0,
        "q_equals_M_minus_ainc_shadow_on_derivative": 0,
        "identified_with_physical_fan_q_packet": False,
        "reason": (
            "the toric minor is a degree-zero mixed conormal; a fan q row "
            "is a terminal on a complete repeated-grade relative domain. "
            "Identifying them requires the missing source-labelled landing"
        ),
    }


def word_grade_and_terminal_frontier_audit() -> dict[str, object]:
    # Treat the response KS line and the E14/AugP2 line as distinct graded
    # summands.  No scalar identity between their coefficient shadows creates
    # an off-diagonal degree-zero map.
    response_ks = tuple(map(Q, (1, 0)))
    physical_e14 = tuple(map(Q, (0, 1)))
    require(rank((response_ks, physical_e14)) == 2,
            "the word-grade direct-sum guard changed")
    return {
        "response_KS_object": "centered occurrence in word 11:110000",
        "physical_destination_objects": [
            "E14 unary word 000101",
            "cap word 01211222 / t*q_(v,N) / repeated P3+K2",
        ],
        "graded_direct_sum_rank": 2,
        "coefficient_naturality_creates_off_diagonal_map": False,
        "independent_rows_after_response_KS": [
            "word/fine/repeated landing", "physical ainc/q",
            "physical W landing", "labelled shifted ridge",
        ],
        "rows_automatic_after_labelled_ridge": ["eta", "sigma"],
        "q_defect_alternative_available_after_landing": True,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "universal response KS augmented-readout extension gate",
        "pins": PINS,
        "formal_anchor_and_matching": formal_anchor_and_matching_audit(),
        "augmented_extension_ambiguity": augmented_extension_ambiguity_audit(),
        "premature_q_promotion_counterguard": (
            premature_q_promotion_counterguard()
        ),
        "toric_shear_cross_term": toric_shear_cross_term_audit(),
        "word_grade_and_terminal_frontier": (
            word_grade_and_terminal_frontier_audit()
        ),
        "verdict": (
            "Differentiation of the complete response family canonically "
            "gives d epsilon_s=-c_f, the scaled formal anchor identity, and "
            "B-natural aggregate matching.  It does not determine ainc, "
            "hence physical q, W, or the labelled shifted ridge; eta/sigma "
            "are automatic only after that ridge is physically placed.  A "
            "nonzero q defect supported on formal epsilon_s has no physical "
            "kernel witness and cannot trigger generator/Fredholm.  The "
            "toric shear derivative is the mixed endpoint/matching line and "
            "is killed by the separable matching, anchor, and q shadows; it "
            "is not a fan q row without the same missing physical landing. "
            "The word/fine/repeated-grade landing remains logically prior."
        ),
        "shortest_remaining_theorem": (
            "construct one protected augmented placement of epsilon_s in "
            "the complete physical AugP2/E14 domain.  The formal anchor and "
            "matching laws then transport; the q defect alternative closes "
            "q, the independent W equation must be checked, and the labelled "
            "ridge uniquely supplies eta/sigma"
        ),
        "scope": (
            "canonical h=3 characteristic-zero centered response module. "
            "This is an augmented-typing counterguard, not a proof that no "
            "physical placement exists."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("response derivative: d epsilon_s=-c_f (CANONICAL)")
    print("scaled anchor + aggregate matching: FORMAL YES")
    print("ainc/q, W, labelled ridge: NOT DETERMINED")
    print("eta/sigma: UNIQUE ONLY AFTER PHYSICAL RIDGE")
    print("q defect on formal epsilon_s: NOT A PHYSICAL TERMINAL")
    print("toric shear cross-term: q/anchor SHADOW ZERO; GRADE LANDING OPEN")
    print("first gate: WORD/FINE/REPEATED PHYSICAL LANDING")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
