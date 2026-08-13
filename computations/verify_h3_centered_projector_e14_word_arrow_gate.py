#!/usr/bin/env python3
"""Audit the centered-projector route to the selected E14 word arrow.

For any occurrencewise transport W, the centered occurrence projector gives
an exact formula for a selected arrow, conditional on the aggregate line.
No such W to the E14 unary/G11 S-pair is currently physical.  The committed
normalized covariance interval lands instead in the all-zero response word.
The physical five-face lift also lacks the aggregate line: its cap shadow is
the primitive p detected by epsilon.  Finally, the centered columns have no
E14 coordinate, so the pinned E14 first-hit dual detects the desired
cross-word cell and kills the entire proposed centered inventory.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py":
        "d5c90e6404670c7b666b6aa2b3448f5f16c2aebc7fac47f749fb269250413a28",
    "computations/verify_h3_centered_occurrence_same_grade_physical_gate.py":
        "5b41444ef5f4844bc1bd87a6a4e81e60a631f3549eed21c160efdcb428582ea4",
    "computations/verify_h3_rootless_e14_companion_core_identification.py":
        "438ae827dba9e8f7a14f011cb5d76631fc284a2a2a8c6d8bcee7003669a1ac45",
    "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py":
        "893f000e37e4bcfc78973cb042cc0858087cb25605d6cf070a1bf8dfa7a76b7a",
    "computations/verify_h3_gl3_normalized_bar_word_change_obstruction.py":
        "ed3c1baafd7d83819c1b6842857611b5b540c57ef95c8ca8a450de357312670a",
    "computations/verify_h3_direct_free_normals_e14_pointed_composition_gate.py":
        "ea8cb46d5ee84b1973cb062df73b75c0704a0a31823b53e7187e737175964d53",
    "computations/verify_h3_degree4_reset_five_face_aggregate_gate.py":
        "01961c9ae83b91dad31ba859ea2f8a2d5775d73d7ad591aa0a369e7d971f8079",
    "computations/verify_uniform_centered_occurrence_restriction_insertion_gate.py":
        "cb328adc1f23b38f6f9f9305635ddbaef888178633f8db91c205fdfbdca1ff34",
    "notes/uniform-centered-occurrence-restriction-insertion-gate.md":
        "c3161b740606a19d1fb238921986a6ab3b9c2f9cec9d7bc9a9410059f8c213da",
}
EXPECTED_LEDGER_SHA256 = (
    "c656ea22974f5935ca0f840d266f33753769e7460f4f75403b1ef32bac516127"
)
N = 90


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def load(relative: str, name: str):
    spec = spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            ("cannot load", relative))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rank(columns: list[list[Fraction]]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [list(row) for row in zip(*columns, strict=True)]
    answer = 0
    for column in range(len(columns)):
        pivot = next(
            (row for row in range(answer, height) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [
                left - value * right
                for left, right in zip(rows[row], rows[answer], strict=True)
            ]
        answer += 1
    return answer


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(left, right, strict=True)),
               Fraction(0))


def centered_selected_arrow_audit() -> dict[str, object]:
    # Conditional algebra: if an occurrencewise map W from the root response
    # block to the E14 S-pair block exists, let d_i=W(S_i)-S_i.  The centered
    # operator is C=N*I-J.  It gives C d_f; the missing aggregate is sum_i d_i.
    ones = [Fraction(1)] * N
    centered = []
    for selected in range(N):
        column = [Fraction(-1)] * N
        column[selected] += N
        centered.append(column)
    selected_arrow = [Fraction(0)] * N
    selected_arrow[0] = Fraction(1)
    aggregate_arrow = list(ones)
    require(rank(centered) == N - 1,
            "the centered arrow space stopped having rank 89")
    require(rank(centered + [selected_arrow]) == N,
            "the selected arrow entered the centered image")
    require(rank(centered + [aggregate_arrow]) == N,
            "the aggregate arrow stopped completing the centered image")
    reconstructed = [
        (left + right) / N
        for left, right in zip(centered[0], aggregate_arrow, strict=True)
    ]
    require(reconstructed == selected_arrow,
            "the centered-plus-aggregate arrow formula changed")
    augmentation = list(ones)
    require(all(dot(augmentation, column) == 0 for column in centered)
            and dot(augmentation, selected_arrow) == 1
            and dot(augmentation, aggregate_arrow) == N,
            "the occurrence augmentation dual changed")
    return {
        "difference_basis": "d_i=W(S_i)-S_i, i=1,...,90 (conditional on W)",
        "centered_operator": "C=90*I-J",
        "centered_arrow_rank": N - 1,
        "selected_arrow_in_centered_image": False,
        "identity": "d_f=(C*d_f+sum_i d_i)/90",
        "missing_coefficient_line": "aggregate sum_i d_i",
        "primitive_coefficient_dual": "augmentation sum_i lambda_i",
        "characteristic_zero_denominator": N,
        "occurrencewise_E14_transport_assumed": True,
        "interpretation": (
            "if an occurrencewise E14 transport W is supplied, the centered "
            "projector gives the selected arrow coefficientwise only after "
            "the common aggregate occurrence line is also supplied"
        ),
    }


def decorated_core_and_bar_audit() -> dict[str, object]:
    companion = load(
        "computations/verify_h3_rootless_e14_companion_core_identification.py",
        "centered_arrow_companion",
    )
    core, core_digest = companion.audit()
    require(core_digest == companion.EXPECTED_LEDGER_SHA256,
            "the decorated E14 core ledger changed")
    require(core["mapped_decorated_2K2_core"] == ["u05_01", "v3410"]
            and core["canonical_E14_core_coefficient"] == "1",
            "the selected decorated core stopped hitting E14")
    promoted = tuple(core["canonical_E14_promoted_term"])
    require(promoted == tuple(sorted((
        "p1_0_1", "s1_1_1", "u05_01", "v2411", "v3410"
    ))), "the promoted E14 monomial changed")

    bar = load(
        "computations/verify_h3_gl3_normalized_bar_word_change_obstruction.py",
        "centered_arrow_bar",
    )
    cube = bar.cube_audit(7, audit_all_shuffles=False)
    require(cube["normalized_ez_boundary"] == "allL-allD"
            and cube["endpoint_augmentation"] == 1
            and cube["boundary_augmentation"] == 0,
            "the normalized seven-site covariance interval changed")
    acted = tuple(site for site, colour in enumerate(bar.FULL_WORD) if colour)
    colours = tuple(bar.FULL_WORD[site] for site in acted)
    require(len(acted) == 7 and set(colours) == {1, 2}
            and bar.lowering_target(colours, 8, acted) == {},
            "the complete word arrow acquired a GHZ target")
    lowered_word = tuple(
        0 if site in acted else colour
        for site, colour in enumerate(bar.FULL_WORD)
    )
    require(lowered_word == (0,) * 8,
            "the normalized covariance endpoint stopped being all-zero")
    require(tuple(map(int, core["E14_unary_word"])) != lowered_word[:6],
            "the all-zero response endpoint collided with the E14 unary word")
    return {
        "root_source_word": "01211222",
        "E14_unary_word": core["E14_unary_word"],
        "mapped_root_core": core["mapped_decorated_2K2_core"],
        "promotion_factor": core["canonical_E14_promotion_factor"],
        "promoted_target_monomial": list(promoted),
        "target_core_coefficient": 1,
        "normalized_covariance_boundary": "allL(all-zero response)-allD",
        "normalized_covariance_target_word": "00000000",
        "complete_seven_site_target": 0,
        "normalized_bar_constructs_01211222_to_00000000": True,
        "normalized_bar_constructs_E14_unary_G11_S_pair_transport": False,
        "selected_promoted_occurrence_arrow_constructed": False,
        "reason": (
            "the covariance bar acts on a complete response row and lands "
            "in the all-zero response word.  The E14 target is a unary/G11 "
            "S-pair based at word 000101.  Selecting the promoted occurrence "
            "and changing this operation type require a new chain map"
        ),
    }


def physical_projector_and_e14_dual_audit() -> dict[str, object]:
    projector = load(
        "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py",
        "centered_arrow_projector",
    )
    endpoint, endpoint_digest = projector.audit()
    require(endpoint_digest == projector.EXPECTED_LEDGER_SHA256,
            "the endpoint projector ledger changed")
    coefficient = endpoint["coefficient_projector"]
    cap = endpoint["physical_cap_quotient"]
    require(coefficient["occurrences"] == N
            and coefficient["coefficient_centered_projector_exists"]
            and not coefficient["source_chain_lift_constructed"]
            and coefficient["scalar_zero_face_after_rational_normalization"]
            == "90*f(x)",
            "the centered source-lift gate changed")
    require(cap["Cartan_rank"] == 4
            and cap["remaining_cokernel"]
            == "Z generated by epsilon=sum_v lambda_v"
            and cap["primitive_epsilon"] == -1
            and cap["full_source_word"] == "01211222"
            and cap["first_common_fine_degree"]
            == "t*q_(v,N), repeated P3+K2",
            "the physical primitive cap gate changed")

    first = load(
        "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py",
        "centered_arrow_e14_first",
    )
    first_ledger, first_digest = first.audit()
    require(first_digest == first.EXPECTED_LEDGER_SHA256,
            "the E14 first-hit ledger changed")
    canonical = first_ledger["canonical_first_reduction"]
    require(canonical["target_augmented_first_hit_column_count"] == 269
            and canonical["target_augmented_first_hit_rank_Q"] == 269
            and canonical["rational_dual_support"] == 22
            and canonical["rational_dual_pairing"] == "-1"
            and canonical["primitive_integral_dual_pairing"] == "-30",
            "the E14 target dual changed")

    # On the two primitive word quotients (root,E14), the desired arrow is
    # g=(-1,+1).  The centered five-face columns have projection (0,0): they
    # stay in the root word and have zero cap augmentation.  One arrow cell
    # identifies the two classes but leaves the common aggregate detected by
    # (1,1).  A primitive cap p=(-1,0) completes the lattice with determinant
    # one.  Neither new column is currently physical.
    g = [Fraction(-1), Fraction(1)]
    p = [Fraction(-1), Fraction(0)]
    common_dual = [Fraction(1), Fraction(1)]
    target_dual = [Fraction(0), Fraction(1)]
    require(dot(common_dual, g) == 0
            and dot(target_dual, g) == 1,
            "the primitive word-arrow duals changed")
    determinant = g[0] * p[1] - p[0] * g[1]
    require(determinant == 1,
            "word arrow plus primitive cap stopped being an integral basis")
    return {
        "centered_projector_source_chain_lift": False,
        "centered_projector_first_scalar_face": "90*f(x)",
        "centered_projector_E14_word_projection": 0,
        "five_face_physical_standard_rank": 4,
        "five_face_missing_primitive": "p=(-Q,-ores), epsilon(p)=-1",
        "E14_first_hit": {
            "columns": 269,
            "rank_Q": 269,
            "rational_dual_support": 22,
            "rational_dual_pairing_on_target": -1,
            "primitive_integral_pairing_on_target": -30,
        },
        "extended_E14_dual_on_centered_inventory": 0,
        "extended_E14_dual_on_desired_arrow": -1,
        "primitive_two_word_quotient": {
            "basis": ["root_cap_class", "E14_first_hit_class"],
            "desired_arrow_g": [-1, 1],
            "common_aggregate_dual_after_g": [1, 1],
            "primitive_cap_p": [-1, 0],
            "determinant_g_p": int(determinant),
        },
        "verdict": (
            "the five-face centered projector does not supply the arrow.  "
            "It has no E14-word coordinate and its physical lift stops at "
            "the primitive cap aggregate; the E14 first-hit dual detects the "
            "missing cross-word column"
        ),
    }


def minimal_extension_audit() -> dict[str, object]:
    return {
        "new_family": "one pointed promoted-occurrence covariance totalization G_f",
        "required_principal_boundary": (
            "the promoted E14 monomial in word 000101 minus the relabelled "
            "decorated 2K2 occurrence tagged by source word 01211222"
        ),
        "required_occurrence_face": "90*e_f-sum_M e_M",
        "required_scalar_face": "cancel 90*f(x)",
        "required_cap_face": "p=(-Q_(v,N),-ores), epsilon=+/-1",
        "required_fine_grade": "labelled repeated P3+K2",
        "required_other_faces": [
            "endpoint Cartan product-rule faces",
            "pairwise second-Hasse faces",
            "mixed endpoint/matching faces",
            "cubic Hasse face",
            "rootless ridge and physical-q transport",
            "Eq, W, target, anchor, eta, sigma zero or committed boundaries",
        ],
        "coefficientwise_construction": (
            "conditional formula using C=90I-J and the common aggregate "
            "line, after an occurrencewise root-response to E14-S-pair "
            "transport W has been supplied"
        ),
        "physical_construction": False,
        "smallest_duals": [
            "E14 first-hit rational dual (pairing -1)",
            "five-face primitive cap epsilon=sum_v lambda_v",
        ],
        "scope": (
            "these are source-presentation/cap cokernel duals; they become "
            "physical terminals only after the complete augmented comparison "
            "map is supplied"
        ),
    }


def lower_centered_convergence_audit() -> dict[str, object]:
    # The exact restriction theorem gives, on either of the two marked
    # residual edges at r=3,
    #   D_e c_(f,3)=(15/2)c_(f/e,2)+(13/2)1.
    # The supplied Gamma_1 raw calculation has centered coefficient -5/8 on
    # each of the same two faces.  Therefore +(1/12) of a centered-arrow base
    # cell cancels both centered debts simultaneously.  The constant 13/24
    # remains and must land in the common H0 line.
    n3, n2 = Fraction(90), Fraction(12)
    alpha = n3 / n2
    centered_coefficient = alpha
    constant_coefficient = alpha - 1
    gamma_coefficient = Fraction(-5, 8)
    arrow_scale = -gamma_coefficient / centered_coefficient
    residual_centered = gamma_coefficient + arrow_scale * centered_coefficient
    residual_constant = arrow_scale * constant_coefficient
    require(alpha == Fraction(15, 2)
            and constant_coefficient == Fraction(13, 2),
            "the h3 lower-centered restriction coefficients changed")
    require(arrow_scale == Fraction(1, 12)
            and residual_centered == 0
            and residual_constant == Fraction(13, 24),
            "the Gamma1/base-cell convergence coefficients changed")
    return {
        "marked_residual_edges": 2,
        "literal_lower_cuts": [
            {
                "deleted_edge": "23",
                "lower_word": "0112",
                "reinsertion_tail": "q23:21",
            },
            {
                "deleted_edge": "45",
                "lower_word": "0121",
                "reinsertion_tail": "q45:12",
            },
        ],
        "required_orientation": "p/s-odd",
        "reinserted_grade": "01211222 / labelled repeated P3+K2",
        "restriction_face_each": "(15/2)*c_lower+(13/2)*H0",
        "Gamma1_shifted_raw_centered_face_each": "(-5/8)*c_lower",
        "common_arrow_scale": "1/12",
        "centered_residual_after_addition": 0,
        "remaining_constant_each": "13/24*H0",
        "exact_convergence_scope": (
            "yes in the order-two centered occurrence quotient: the two "
            "marked proper faces forced by a centered 01211222-to-E14 base "
            "cell are exactly the two c_lower classes seen by Gamma1"
        ),
        "physical_scope": (
            "the equality does not identify the full word/fine/repeated, "
            "Eq, target, residue, q, anchor, eta/sigma, or W rows; the "
            "remaining 13/24 constants require the common H0 base-change"
        ),
        "common_base_cell_theorem": (
            "construct p/s-odd physical order-two centered cells in mixed "
            "words 0112 and 0121, with q23:21 and q45:12 reinsertion into "
            "01211222/repeated-P3+K2, as the two marked faces of one pointed "
            "E14 comparison G_f.  Require D_e G_f=(15/2)c_lower+(13/2)H0 "
            "in the complete augmented grade.  Unscaled they lift the "
            "primitive carrier; adding (1/12)G_f to the shifted Gamma1 "
            "packet cancels both centered debts, leaving 13/24 H0 per face"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 centered-projector to E14 selected word-arrow gate",
        "pins": PINS,
        "coefficient_arrow": centered_selected_arrow_audit(),
        "decorated_core_and_bar": decorated_core_and_bar_audit(),
        "physical_projector_and_dual": physical_projector_and_e14_dual_audit(),
        "minimal_extension": minimal_extension_audit(),
        "lower_centered_convergence": lower_centered_convergence_audit(),
        "verdict": (
            "The five-face centered projector identifies the correct "
            "conditional coefficient architecture but does not construct the "
            "physical arrow.  The committed covariance bar lands in the "
            "all-zero response word, not the E14 unary/G11 S-pair.  Even after "
            "an occurrencewise E14 transport is posited, centered columns span "
            "only the 89-dimensional augmentation-zero differences and need "
            "the aggregate line.  Physically that line is the missing primitive "
            "cap p, while the E14 first-hit dual detects the absent cross-word "
            "column.  One promoted-occurrence comparison totalization carrying "
            "both faces is the minimal new family.  Its two marked restriction "
            "faces are exactly (15/2)c_lower+(13/2)H0; one twelfth cancels the "
            "two -5/8 c_lower faces of the shifted Gamma1 packet."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("centered-projector/E14 word-arrow ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("decorated E14 core: UNIT HIT")
    print("centered + aggregate: CONDITIONAL COEFFICIENT ARROW FORMULA")
    print("old covariance endpoint: 00000000, not E14 unary/G11")
    print("five-face centered physical projector: NO CROSS-WORD COLUMN")
    print("first duals: E14 first-hit and primitive cap epsilon")
    print("Gamma1 c_lower convergence: +(1/12) base cell cancels both faces")
    print("minimal extension: one promoted-occurrence covariance totalization")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
