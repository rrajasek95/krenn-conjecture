#!/usr/bin/env python3
r"""Compose the normalized-C5 carrier with the affine/Hall landing chain.

The residual-tail visibility theorem exports a nonzero complete q-cell
column.  This checker records exactly how far that datum propagates through
the source-valid endpoint attachment, affine, Fitting, and strict-Hall
theorems.  It also replays the sharp local-rank guard: independence of
complete response columns may live entirely in their cofactor tails, while
all local outer heads remain parallel and the deleted-star profile stays
(2,2,3,3).

Thus the already-certified strict Hall subcharts are not the remaining
obstruction.  The honest pre-landing residuals are (i) a unary-only x-spoke
with no compatible endpoint column, (ii) a common-covector/Fitting carrier
with no source-labelled transverse local head, and (iii) the finite
non-strict/triangle Hall locks not meeting a pinned strict closure theorem.
No full-source counterexample is claimed.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "5ddbd0e3d9fcddcc221e585f76cad96ab60a49d0d366db61a664c34bb13b827b"
PINS = {
    "computations/verify_h3_rootless_c5_residual_tail_augmented_visibility.py":
        "5882d7c61c688e9238ba6bf1f971fde73f9af3fda81e5975f1900e1468de2b8c",
    "computations/verify_h3_rootless_c5_first_unmatched_tail_attachment_boundary.py":
        "ef235f2e17b7f62a7160bdc9fccd18efae5842c00ae2fc4ae7d900de34255f0d",
    "computations/verify_uniform_multisite_endpoint_affine_hall_concentration_boundary.py":
        "f24e9bd69ec4baef96104557571c154b399f87f34074edffda27e551f33c2205",
    "computations/verify_h3_axis_target_coloop_proportional_nu_safe_reduction.py":
        "6f27d3585fdc4708026ab6fef6134295dd874f83bb43fd1f480b7314362c56f3",
    "computations/verify_h3_axis_target_coloop_common_covector_synchronization.py":
        "cb834de7584912dc8c4f650a0504326cf8badb7f4c4e9e823bad5068a53e7d31",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "computations/verify_uniform_one_bad_active_minor_rank_completion_boundary.py":
        "8d5958ed772b8f781ee30c91ba743b3af2ce978435edf7770494c1e2d25423b6",
    "computations/verify_uniform_axis_circuit_third_component_rank_guard.py":
        "d9e852bad1b94c1918523fa834029abff04f4c288bde2f97c790def1bef2644f",
    "computations/verify_uniform_hall_terminal_transfer_bistar_curvature_boundary.py":
        "aa1da69a09c3c34f90024a42b27ab0d0a30b0c1263a6a059d256ff085084c048",
    "computations/verify_uniform_hall_k22_outside_endpoint_component_wedge.py":
        "59dd21c4664e8ccd88f771d0191d3db32e5fdb832e2c6de1f169cb197f9a3038",
    "computations/verify_uniform_multisite_hall_star_colocated_unary_wedge_closure.py":
        "195c57ea9d315f685246e38f00a9b14a3fdf62de084ad84313d1fa953a9a9c29",
}


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            ("cannot load dependency", relative))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))


def audit_c5_carrier_and_attachment():
    visibility = load(
        "computations/verify_h3_rootless_c5_residual_tail_augmented_visibility.py",
        "c5_rank_landing_visibility",
    )
    attachment = load(
        "computations/verify_h3_rootless_c5_first_unmatched_tail_attachment_boundary.py",
        "c5_rank_landing_attachment",
    )
    records, degree_histogram = visibility.tail_occurrences()
    visible, visibility_counts = visibility.visibility_records(records)
    chord_types = Counter(
        "offdiagonal" if visibility.MIDDLE[chord[0]]
        != visibility.MIDDLE[chord[1]] else "diagonal"
        for record in records for chord in record["chords"]
    )
    require(chord_types == Counter({"diagonal": 9, "offdiagonal": 6}),
            ("the normalized C5 chord typing changed", chord_types))
    require(len(visible) == 15 and visibility_counts[
        "top_matching_completions"] == 45,
        "the residual carrier inventory changed")

    attachment_ledger, attachment_digest = attachment.audit()
    require(attachment_digest == attachment.EXPECTED_LEDGER_SHA256,
            "the attachment replay changed digest")
    require(attachment_ledger["complete_response_route_counts"] == {
        "different_tail_C4_terms": 40,
        "same_tail_opposite_orientation": 10,
    }, "the complete six-term attachment partition changed")
    return {
        "tail_degree_histogram": dict(sorted(degree_histogram.items())),
        "chord_occurrence_types": dict(sorted(chord_types.items())),
        "complete_q_cell_columns": len(visible),
        "unary_top_completions": visibility_counts[
            "top_matching_completions"],
        "response_q_edge_completions": visibility_counts[
            "response_q_edge_completions"],
        "active_forced_hole_routes": attachment_ledger[
            "complete_response_route_counts"],
    }


def audit_affine_and_hall_boundary():
    affine = load(
        "computations/verify_uniform_multisite_endpoint_affine_hall_concentration_boundary.py",
        "c5_rank_landing_affine",
    )
    hall = affine.audit_cross_intersecting_hall_theorem()
    require(hall["maximal_cross_intersection_types"] == {
        "star": 171, "triangle": 20, "four_site_rectangle": 4950,
    }, "the finite Hall normal forms changed")
    exact_move = affine.audit_exact_affine_replacement()
    require(exact_move["conclusion"]
            == "B(p'_i,s'_j)=B(p_i,s_j) for all i,j",
            "the sequential affine move stopped being exact")
    return {
        "sequential_joint_kernel_move": exact_move,
        "finite_hall_normal_forms": hall,
        "certified_strict_Hall_subcharts": {
            "colocated_star": (
                "unary companion repairs the centre arm and gives the "
                "distinct-head rank-(3,3,3,3) wedge"
            ),
            "endpoint_support_complete_K22": (
                "outside endpoint columns give deletion/wedge; the two "
                "terminal bistar companion identities are localized units"
            ),
            "qualification": (
                "these theorems apply after an effective hole/carrier is "
                "source-typed; they do not create the preceding affine "
                "coordinate-line point and do not claim every non-strict "
                "triangle/anchor-web lock is closed"
            ),
        },
    }


def audit_fitting_and_rank_boundary():
    synchronize = load(
        "computations/verify_h3_axis_target_coloop_common_covector_synchronization.py",
        "c5_rank_landing_synchronization",
    )
    separated = synchronize.audit_separated_literal_words()
    require(not separated["common_literal_word_pair"]
            and separated["common_minor_values"] == ["-1", "-1"],
            "the common-covector fine-word boundary changed")

    rank_guard = load(
        "computations/verify_uniform_axis_circuit_third_component_rank_guard.py",
        "c5_rank_landing_rank_guard",
    )
    guarded = rank_guard.audit_order(3)
    require(guarded["deleted_star_profile"] == [2, 2, 3, 3]
            and guarded["outer_head_span_rank"] == 1
            and guarded["response_column_rank"] == 3,
            "the tail-independent/local-parallel guard changed")
    return {
        "common_covector": separated,
        "minimum_rank_guard": guarded,
        "sharp_implication_failure": (
            "a source-valid common Fitting quotient and independent "
            "complete response tails do not force a transverse local outer "
            "head; the active pair may stay same-head with deleted-star "
            "profile (2,2,3,3)"
        ),
        "guard_scope": (
            "exact linear/tensor rank guard, not a full one-bad source; no "
            "full-source counterguard to the additional companion rows is known"
        ),
    }


def main() -> None:
    pin_dependencies()
    carrier = audit_c5_carrier_and_attachment()
    affine_hall = audit_affine_and_hall_boundary()
    fitting_rank = audit_fitting_and_rank_boundary()
    ledger = {
        "pins": PINS,
        "normalized_C5_carrier": carrier,
        "affine_and_Hall": affine_hall,
        "Fitting_and_rank": fitting_rank,
        "exact_composed_dichotomy": {
            "zero_complete_q_column": (
                "exact anchor-safe chord deletion, impossible at minimum support"
            ),
            "response_carrier": (
                "the six-term row gives unit, same-tail opposite columns, "
                "or a different-tail C4.  Proportional complete same-star "
                "columns delete nu-safely; nonproportional columns give a "
                "source-valid common-covector Fitting carrier.  Different "
                "tails either expose a free arm or enter finite star/triangle/K22 Hall"
            ),
            "unary_only_carrier": (
                "a literal external x-spoke is active, but no existing "
                "theorem pairs it with the coloured endpoint product needed "
                "for an affine response hole"
            ),
        },
        "closed_downstream_strata": (
            "coordinate-line hits concentrate exactly; proportional "
            "complete columns delete; a typed free nonanchor arm has rank "
            "three at both deleted stars; the certified co-located Hall star "
            "and endpoint-support-complete K22 locks land in a four-good "
            "wedge or unit"
        ),
        "sole_rank_residual_after_a_response_carrier": (
            "all active products are trapped in the selected anchor web and "
            "the nonproportional common Fitting carrier has no source-labelled "
            "transverse local head.  Its complete tails may be independent "
            "while the local outer-head span is one and the active deleted-"
            "star profile is only (2,2,3,3)"
        ),
        "finite_Hall_scope_guard": (
            "a different-tail carrier trapped in a non-strict triangle or "
            "larger decorated anchor web remains a finite Hall lock until "
            "its effectiveness and strict companion envelope are proved; "
            "this composition does not silently apply the strict units"
        ),
        "smallest_missing_full_source_statement": (
            "the unary top plus the other diagonal and both crossed response "
            "companions must turn a unary-only spoke or same-head Fitting "
            "carrier into a joint-kernel/coordinate-line move, a transverse "
            "active endpoint arm with the two missing rank-three minors, or "
            "an effective strict Hall lock.  Aggregate column independence "
            "and Hall incidence alone do not imply this"
        ),
        "scope": (
            "exact dependency composition and sharp tensor-rank guard at h=3; "
            "it does not claim global four-good landing and supplies no "
            "full-source counterexample"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("carrier/rank landing ledger changed", digest))
    print("h3 normalized-C5 carrier affine/rank landing: BOUNDARY")
    print("certified strict Hall subcharts: CLOSED after effective carrier")
    print("remaining: unary-only spoke / same-head rank carrier / finite non-strict Hall")
    print("full-source counterguard: NONE")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
