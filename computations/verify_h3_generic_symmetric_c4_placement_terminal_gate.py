#!/usr/bin/env python3
"""Audit the sole generic symmetric four-site C4 placement from f382251.

The residual lower face is the invariant line in the three-match C4 module

    s = q23*q45 + q24*q35 + q25*q34.

The committed occurrence/KS, collision and endpoint-odd Cartan constructions
only supply augmentation-zero directions in this local module.  The
punctured-C4 theorem is a normalized target-coloop *route*, not a source
column, and the committed relative-C4 candidates live in collision grades
without the original H2 direction-pair object.  Thus none is the required
same-grade placement.

The primitive invariant dual epsilon=(1/3,1/3,1/3) detects s and kills the
entire augmentation-zero plane.  For any source-labelled placement, let
mu_j be the induced values on the four cap corners of 4373ae6.  That theorem
promotes epsilon by

    target_j=-mu_j, W_j=-mu_j, ores_j=mu_j,
    ridge=-sum_j alpha_j mu_j,

with q=ainc=Eq=0.  It then gives the exact filler-or-terminal alternative.
The one missing source column is therefore named explicitly: a protected-zero
augmentation-one relative-C4 restriction/insertion column in the original
H2(D,Q01) word/fine/direction-pair grade (and its covariant transports).
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_pure_trapped_h2_c2_c4_p2_descent_reduction.py":
        "026eb42fac96e2c21e6466f51322a18d45d975bcf5f48e0dc33f9cfa740d8d41",
    "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py":
        "b03c096eb5bc4e6307cafa966f3d66d8c087e78bb8793c8448eec33f51e7e76a",
    "computations/verify_h3_c4_punctured_cube_alternate_target_lift.py":
        "15494dbdcf5d019d6fc858d2bad016a48dc966f63c672e739491a3692842c503",
    "computations/verify_h3_trace_cartan_even_repair_relative_c4_scope_gate.py":
        "645df036367a7fe60f3ce625dc37710f7e83129a84a3619005945ca6b4f0a486",
    "computations/verify_h3_universal_response_deformation_e14_orbit_ks_gate.py":
        "39713f3683dd3d2376e5a911987ee3670ec291cf850072d6b4932e7a93745fc7",
    "computations/verify_h3_endpoint_odd_cartan_prism_augmentation.py":
        "24ec9e3c1d1f9b689fa5a47faf9900c16724dc215fee0a41a0b653f410427fb3",
    "computations/verify_h3_o2_augmented_terminal_cap_cartan_extension_gate.py":
        "8a9bfe47c934658d1b10ad42f283d6a017c27125bcb98615882e4bacd975f1eb",
}
EXPECTED_LEDGER_SHA256 = (
    "63a39bb1c510e86b67e8fbf5867a4abc691aaf5d7545781e7ee11ae8e64ae49d"
)

MATCHES = ("23|45", "24|35", "25|34")
SYMMETRIC = (Q(1), Q(1), Q(1))
EPSILON = (Q(1, 3), Q(1, 3), Q(1, 3))
DIFFERENCES = (
    (Q(1), Q(-1), Q(0)),
    (Q(0), Q(1), Q(-1)),
)
ALPHA = (Q(-1), Q(1), Q(1), Q(-1))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def dot(left, right) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def invariant_line_audit() -> dict[str, object]:
    # Site relabelling permutes the three perfect matchings of K4.  The
    # symmetric vector is fixed by every such permutation; the standard
    # augmentation-zero plane is its exact complement in characteristic 0.
    orbit = set()
    for permutation in permutations(range(3)):
        transported = tuple(SYMMETRIC[index] for index in permutation)
        require(transported == SYMMETRIC,
                ("the symmetric C4 line stopped being invariant", permutation))
        for vector in DIFFERENCES:
            orbit.add(tuple(vector[index] for index in permutation))
    require(rank(DIFFERENCES) == 2 and rank(tuple(orbit)) == 2
            and rank(DIFFERENCES + (SYMMETRIC,)) == 3,
            ("the C4 trivial/standard split changed", orbit))
    require(all(dot(EPSILON, value) == 0 for value in orbit)
            and dot(EPSILON, SYMMETRIC) == 1,
            "the primitive symmetric dual changed")
    return {
        "local_basis": list(MATCHES),
        "symmetric_face": [str(value) for value in SYMMETRIC],
        "site_permutation_orbit_size": 1,
        "augmentation_zero_rank": rank(tuple(orbit)),
        "rank_after_symmetric_face": rank(DIFFERENCES + (SYMMETRIC,)),
        "primitive_dual": [str(value) for value in EPSILON],
        "primitive_dual_on_symmetric_face": str(dot(EPSILON, SYMMETRIC)),
        "interpretation": (
            "the generic equal-value C4 is the trivial S3 summand; centered "
            "occurrence, collision and odd differences occupy the standard "
            "augmentation-zero summand"
        ),
    }


def typed_candidate_audit() -> dict[str, object]:
    lower_grades = {
        "DQ01": {
            "source_order": "Hasse[2]",
            "direction_pair": ["D", "Q01"],
            "operation_profile": {"D": 1, "P": 0, "S": 0, "Q": 1},
            "residual_sites": [2, 3, 4, 5],
            "tail": list(MATCHES),
        },
        "P0S1": {
            "source_order": "Hasse[2]",
            "direction_pair": ["P0", "S1"],
            "operation_profile": {"D": 0, "P": 1, "S": 1, "Q": 0},
            "residual_sites": [2, 3, 4, 5],
            "tail": list(MATCHES),
        },
    }

    candidates = {
        "punctured_C4": {
            "is_source_column": False,
            "is_route_theorem": True,
            "requires_normalized_target_coloop_chart": True,
            "requires_selected_endpoints_and_common_tail": True,
            "same_generic_H2_grade": False,
            "reason": (
                "it is an integral complete-row certificate followed by "
                "alternate-target reselection, not a relative-C4 column"
            ),
        },
        "centered_response_KS": {
            "is_source_column_in_its_relative_Tate_family": True,
            "is_column_in_the_fixed_physical_correction_complex": False,
            "local_augmentation": 0,
            "boundary_type": "centered occurrence c_f",
            "same_generic_H2_grade": False,
            "reason": (
                "its boundary lies in the occurrence augmentation ideal; "
                "the symmetric C4 line has augmentation one"
            ),
        },
        "endpoint_odd_Cartan": {
            "is_source_column": True,
            "local_augmentation": 0,
            "corner_signature": [str(value) for value in ALPHA],
            "carries_root_word_change_and_labelled_residue": True,
            "same_generic_H2_grade": False,
            "reason": (
                "endpoint oddization is augmentation zero and starts from a "
                "root-oriented seed; it does not create the H2 DQ/PS seed"
            ),
        },
        "committed_collision_relative_C4_candidates": {
            "is_source_column": False,
            "coarse_required_signature_known": True,
            "known_repeated_edge_packets": ["02", "01", "04", "12", "24"],
            "original_H2_direction_pair_retained": False,
            "same_generic_H2_grade": False,
            "reason": (
                "the matching replacements are typed occurrence pairs, but "
                "no committed theorem makes them protected relative source "
                "boundaries in the original H2 direction-pair object"
            ),
        },
    }
    require(all(not record["same_generic_H2_grade"]
                for record in candidates.values()),
            "a candidate unexpectedly acquired the exact generic H2 grade")
    require(all(sum(profile["operation_profile"].values()) == 2
                for profile in lower_grades.values()),
            "the H2 operation profiles changed")
    return {
        "two_literal_source_representatives": lower_grades,
        "site_colour_transport_guard": (
            "literal site/colour relabelling permutes labels but preserves "
            "Hasse order and the D/P/S/Q operation profile; equality of one "
            "bare edge label is not equality of the direction-pair grade"
        ),
        "candidate_table": candidates,
        "exact_committed_identification_exists": False,
    }


def cap_extension_for_mu(mu: tuple[Q, Q, Q, Q]) -> dict[str, object]:
    # Recheck the exact 4373ae6 formula on the 13 known r0/T/rho/K columns.
    # Rows: B[4], Eq[4], q, ainc, target[4], W[4], ores[4], ridge.
    labels = (
        *(f"B{index}" for index in range(4)),
        *(f"Eq{index}" for index in range(4)),
        "q", "ainc",
        *(f"target{index}" for index in range(4)),
        *(f"W{index}" for index in range(4)),
        *(f"ores{index}" for index in range(4)),
        "ridge",
    )

    def vector(**entries):
        return tuple(Q(entries.get(label, 0)) for label in labels)

    columns = []
    for corner in range(4):
        columns.extend((
            vector(**{f"B{corner}": 1, f"Eq{corner}": 1,
                      f"target{corner}": 1, "ainc": -1}),
            vector(**{f"W{corner}": -1, f"target{corner}": 1}),
            vector(**{f"W{corner}": 1, f"ores{corner}": 1}),
        ))
    columns.append(vector(**{
        **{f"ores{corner}": ALPHA[corner] for corner in range(4)},
        "ridge": 1,
    }))

    alpha_mu = dot(ALPHA, mu)
    extension = vector(**{
        **{f"B{corner}": mu[corner] for corner in range(4)},
        **{f"target{corner}": -mu[corner] for corner in range(4)},
        **{f"W{corner}": -mu[corner] for corner in range(4)},
        **{f"ores{corner}": mu[corner] for corner in range(4)},
        "ridge": -alpha_mu,
    })
    require(all(dot(extension, column) == 0 for column in columns),
            ("the 4373ae6 extension stopped annihilating the old packet", mu))
    return {
        "selected_cap_values_mu": [str(value) for value in mu],
        "extension": {
            "q": "0", "ainc": "0", "Eq": "0",
            "target": [str(-value) for value in mu],
            "W": [str(-value) for value in mu],
            "ores": [str(value) for value in mu],
            "ridge": str(-alpha_mu),
        },
        "annihilates_all_13_known_r0_T_rho_K_columns": True,
    }


def missing_column_and_terminal_audit() -> dict[str, object]:
    # The formula is valid for the cap-corner values induced by *any* future
    # placement.  The selected e0 packet is retained only as a literal sign
    # check.  Its four cap corners must not be confused with the separate six
    # pure-column tails in the relative-C4 census.
    samples = {}
    for name, mu in {
        "zero": (Q(0), Q(0), Q(0), Q(0)),
        "cap_corner_0": (Q(1), Q(0), Q(0), Q(0)),
        "mixed_alpha": ALPHA,
    }.items():
        samples[name] = cap_extension_for_mu(mu)
    require(samples["cap_corner_0"]["extension"]["ridge"] == "1",
            "the cap-corner-0 ridge sign changed")
    return {
        "one_explicit_missing_source_column": {
            "name": "U_C4[D,Q01;2345]",
            "source_object": (
                "relative restriction/insertion generator in the literal "
                "Hasse[2](D,Q01) response word/fine/direction-pair grade"
            ),
            "local_boundary": (
                "q23*q45 + q24*q35 + q25*q34, with the three occurrence "
                "tags retained"
            ),
            "relative_tail": (
                "one literal augmentation-one b_i in the six-column C4 tail, "
                "chosen by the physical C4 replacement"
            ),
            "occurrence_augmentation": "1",
            "required_zero_rows": [
                "q", "ainc", "Eq", "target", "W", "ordinary residue",
                "shifted ridge",
            ],
            "covariance": (
                "site/colour and DQ/PS source transports produce the other "
                "four-site representatives without forgetting the H2 tag"
            ),
            "status": "NOT CONSTRUCTED BY ANY PINNED CELL",
        },
        "primitive_local_dual": {
            "epsilon_on_three_C4_occurrences": [str(value) for value in EPSILON],
            "value_on_missing_column": "1",
            "value_on_all_committed_in_grade_augmentation_zero_shadows": "0",
            "cap_values_after_the_missing_placement": (
                "mu_j=psi(B_j^cap), determined by the placed local output"
            ),
        },
        "4373ae6_promotion_formula": {
            "q_ainc_Eq": 0,
            "target_j": "-mu_j",
            "W_j": "-mu_j",
            "ores_j": "mu_j",
            "ridge": "-sum_j alpha_j mu_j",
            "verified_samples": samples,
        },
        "post_placement_exact_fork": {
            "inside_exhaustive_physical_image": (
                "protected-zero relative filler/generator closes the C4 face"
            ),
            "outside_exhaustive_physical_image": (
                "the displayed target/W/ores/ridge extension is an augmented "
                "terminal detecting the symmetric C4 class"
            ),
            "third_branch": False,
        },
        "scope_guard": (
            "4373ae6 promotes the dual after the source-labelled same-grade "
            "placement; it does not itself construct U_C4 or turn a bare "
            "coefficient augmentation into a physical terminal.  Its four "
            "cap corners B_j^cap are not the six pure tails b_i of the C4 "
            "replacement census"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 generic symmetric C4 placement / terminal gate",
        "pins": PINS,
        "local_trivial_standard_split": invariant_line_audit(),
        "committed_cell_typing": typed_candidate_audit(),
        "missing_column_and_terminal_extension": missing_column_and_terminal_audit(),
        "verdict": (
            "The sole generic symmetric C4 residual from f382251 is not a "
            "committed punctured-C4, KS or Cartan cell after physical grade "
            "transport.  Its invariant augmentation-one line is detected by "
            "the primitive average dual.  The 4373ae6 cap/Cartan extension "
            "is explicit for every induced cap-corner packet mu, but one "
            "source column remains: U_C4[D,Q01;2345], the "
            "protected-zero same-grade relative-C4 restriction/insertion "
            "primitive.  Its construction closes the face; failure in an "
            "exhaustive placed map gives the augmented terminal."
        ),
        "nonclaims": [
            "the normalized punctured-C4 route is not promoted to a generic source column",
            "a bare repeated-edge coincidence is not called a word/fine/direction-pair transport",
            "the primitive coefficient dual is not called physical before the 4373ae6 placement hypothesis",
        ],
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("generic symmetric C4 = invariant augmentation-one line")
    print("punctured/KS/Cartan committed identification: NO")
    print("primitive average dual + 4373ae6 extension: EXACT AFTER PLACEMENT")
    print("missing column: U_C4[D,Q01;2345]")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
