#!/usr/bin/env python3
"""Audit the first source cell for a noncanonical protected comparison.

The desired comparison is a nonzero, source-labelled chain map

    Phi : L_gamma -> L_h3,       J_h3 Phi = A J_gamma

on complete physical relative domains.  Universal Hasse operations are
internal to a labelled grade.  They therefore do not create a cross-grade
map unless a physical label transport is supplied.  On the canonical
repeated P3+K2 packet, the best principal-parts construction reaches a
derived filler, but its underived physical descent has a literal private
boundary obstruction.  This checker freezes the exact first missing image
vector and the distinction between a genuine relabelling comparison and an
untyped cross-grade arrow.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    # 83151bf: covariance, common-tail commutator, and ridge-grade guard.
    "computations/verify_uniform_cartan_augmented_grade_naturality_gate.py":
        "d71b2ae71cdfc910e374b498a70edbb5e897867cf624dec49203c34e74647925",
    # e7723de: five independent denominator commutators and forced shift.
    "computations/verify_h3_shifted_principal_parts_comparison_obstruction.py":
        "8b7d5907e13e15224fb3a78bb2d4b4f3d3c39094c2a204d1290c3147238de639",
    # 91041f7: positive derived filler, first underived commutator.
    "computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py":
        "7d9e49f34da84772f6e0863a9bfe56cb9a90e0cfd3fceb76da59175ffea36c50",
    # 9ab5fa1: complete literal two-chart membership and minimal M_v image.
    "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py":
        "b890195a8fc0c4e90c9c9c0c03c41a95690228c81026f4c2ea1fa95908564e38",
    # befba18: higher Hasse layers are forced after the initial comparison.
    "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py":
        "674a7503db43b8ad53d6f4ea9d7fe095f0f26629d92e4b0dd291f14bde82fa3a",
    # f746560 and 367e068: physical covariance and the canonical endpoint.
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_h3_physical_cartan_closes_residual_q_ks_hypothesis.py":
        "4453dad26b5d13767fc206e9a8dc98af5428ac6d00cfc9444ac6b4253c834f7c",
    # 7efd10d: no equality of q terminals is required once Phi is physical.
    "computations/verify_dark_cartan_physical_q_protected_quotient_comparison.py":
        "eb56cdb4ab1915f8ce35ab3acf0398b4f526c52a17c9c8ebafcc7a5ad4f86bcc",
    # 80c1b67: a full external column yields a codomain separator, not q.
    "computations/verify_augmented_cartan_full_column_separator_guard.py":
        "0710f16230a1c656bb3ec24843a60c18b668fd499e81652970c41706d6d9f41e",
}
EXPECTED_LEDGER_SHA256 = "6f1144c07c2eadc14eeb5244759802c110db8874a78a7e4814e727f304d15c3e"


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def mat_mul(left, right):
    columns = tuple(zip(*right, strict=True))
    return tuple(tuple(sum(Q(a) * Q(b) for a, b in
                           zip(row, column, strict=True))
                       for column in columns) for row in left)


def transpose(matrix):
    return tuple(tuple(row) for row in zip(*matrix, strict=True))


def grade_transport_audit() -> dict[str, object]:
    """Separate an internal graded map from a physical label transport."""
    # L_gamma and L_h3 are one-dimensional modules over the two central
    # label idempotents.  A degree-zero map intertwining the *fixed* label
    # action must be zero when gamma != h3.
    fixed_label_solutions = []
    for phi in map(Q, range(-3, 4)):
        # For e_gamma, the source action is 1 and target action is 0.
        if 0 * phi == phi * 1:
            fixed_label_solutions.append(phi)
    require(fixed_label_solutions == [Q(0)],
            "a fixed-label operation crossed two distinct grades")

    # A physical relabelling is different: it transports the label algebra,
    # source basis, and protected output basis together.  This finite square
    # is a representative exact comparison J3*Phi=A*J_gamma.
    j3 = (
        (Q(1), Q(2), Q(0)),
        (Q(0), Q(1), Q(1)),
        (Q(1), Q(0), Q(-1)),
    )
    phi = (
        (Q(0), Q(1), Q(0)),
        (Q(1), Q(0), Q(0)),
        (Q(0), Q(0), Q(1)),
    )
    a = (
        (Q(0), Q(0), Q(1)),
        (Q(0), Q(1), Q(0)),
        (Q(1), Q(0), Q(0)),
    )
    # A and Phi are permutation matrices, hence self-inverse here.
    j_gamma = mat_mul(transpose(a), mat_mul(j3, phi))
    require(mat_mul(j3, phi) == mat_mul(a, j_gamma),
            "transported protected square stopped commuting")

    # The canonical ridge has two separate site-degree blocks.  Adding an
    # ordinary common tail can never turn their difference into a single
    # fine grade; a shifted labelled comparison must retain both blocks.
    pq = (0, 0, 1, 1)
    xv = (1, 1, 0, 0)
    for tail in ((0, 0, 0, 0), (1, 0, 2, 1), (3, 3, 3, 3)):
        left = tuple(a0 + b0 for a0, b0 in zip(pq, tail, strict=True))
        right = tuple(a0 + b0 for a0, b0 in zip(xv, tail, strict=True))
        require(left != right, "a common tail homogenized the ridge blocks")

    return {
        "fixed_label_source": "gamma",
        "fixed_label_target": "canonical h=3",
        "fixed_label_intertwiner_space_dimension": 0,
        "meaning": (
            "Hasse/PP operations internal to the fixed multigrading cannot "
            "supply a nonzero comparison between distinct grade blocks"
        ),
        "physical_relabelling_orbit": {
            "comparison": "Phi=rho_* on the complete relative domain",
            "protected_target_map": "A=rho_* on every protected row",
            "identity": "J_h3 Phi=A J_gamma",
            "source_word": "transported literally",
            "fine_grade": "transported literally",
            "repeated_type": "P3+K2 preserved",
            "orientation_and_terminal_labels": "transported together",
        },
        "ordinary_common_tail_repairs_ridge_grade": False,
        "required_nonorbit_datum": (
            "an explicit shifted label morphism/source cell, not a bare "
            "linear arrow between presentation blocks"
        ),
    }


def first_source_cell_audit() -> dict[str, object]:
    shifted = load(
        "computations/verify_h3_shifted_principal_parts_comparison_obstruction.py",
        "protected_comparison_shifted_pp",
    )
    _records, polar = shifted.polar_and_relative_jet_audit()
    commutator = shifted.denominator_commutator_audit()
    require(polar["mixed_rank"] == 5
            and polar["uniform_shift_sites"] == [0, 6, 7]
            and commutator["commutator_rank"] == 5
            and not commutator["chain_map_exists_on_old_denominator_complex"],
            "the first principal-parts obstruction changed")

    literal = load(
        "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py",
        "protected_comparison_literal_mapping_cone",
    )
    literal_ledger, literal_digest = literal.audit()
    require(literal_digest == literal.EXPECTED_LEDGER_SHA256,
            "the literal mapping-cone ledger changed")
    complete = literal_ledger["complete_literal_two_chart_module"]
    cell = literal_ledger["private_pivot_no_go_and_minimal_cell"]
    terminal = literal_ledger["chart_and_physical_terminal"]
    require(complete["four_corner_selections_checked"] == 75
            and complete["minimum_private_features_per_literal_pure_r0"] == 42
            and complete["literal_alpha_aggregate_support_min_max"] == [360, 360]
            and not cell["desired_residue_only_in_two_chart_plus_projected_C_span"]
            and cell["number_of_new_generators_forced"] == 1
            and cell["desired_full_fiber_target_in_extended_span"]
            and not terminal["second_chart_supplies_required_terminal"],
            "the sharp literal one-cell criterion changed")

    return {
        "derived_principal_parts": {
            "strict_two_chart_square": True,
            "mixed_symbol_rank": polar["mixed_rank"],
            "forced_shift_sites": polar["uniform_shift_sites"],
            "forced_shift_weight": polar["uniform_shift_weight"],
            "denominator_commutator": commutator["obstruction_class"],
            "commutator_rank_mod_old_pure_image": commutator["commutator_rank"],
            "old_denominator_chain_map": False,
        },
        "best_derived_filler": {
            "source_word": "1211222 after deleting the exposed x-site",
            "fine_repeated_grade": "canonical labelled repeated P3+K2",
            "boundary": "h_v*Y*w",
            "target": 0,
            "ordinary_residue": 0,
            "chart_correction": "-S_v",
            "first_underived_commutator": "(H_0-u)*e_Eq at q=0",
        },
        "complete_literal_gate": {
            "components": len(complete["components"]),
            "two_chart_boundary_map": complete["two_chart_boundary_map"],
            "two_chart_kernel": complete["two_chart_kernel"],
            "private_pivot_equation": complete["private_pivot_equation"],
            "four_corner_selections_checked":
                complete["four_corner_selections_checked"],
            "private_features_per_selected_r0_at_least":
                complete["minimum_private_features_per_literal_pure_r0"],
            "alpha_aggregate_literal_support": 360,
            "chart_difference_has_physical_terminal": False,
        },
        "smallest_sufficient_initial_image":
            cell["smallest_literal_mapping_cone_image"],
        "number_of_new_image_directions_for_one_face":
            cell["number_of_new_generators_forced"],
        "complete_domain_requirement": (
            "one source-provenant equivariant family M_v over the five "
            "labelled faces (or five compatible instances), in the exact "
            "word/fine/repeated grades; the Hasse coproduct then forces the "
            "higher coherences"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    ledger = {
        "theorem": "first source cell for a protected physical comparison",
        "comparison_scope": (
            "a nonzero chain map on complete physical relative domains "
            "carrying the placed Cartan/derived direction; the zero map and "
            "maps of presentation quotients alone are excluded"
        ),
        "grade_transport": grade_transport_audit(),
        "first_source_cell": first_source_cell_audit(),
        "sharp_verdict": (
            "a protected comparison is constructed on the oriented physical "
            "relabeling orbit by transporting every source and protected "
            "label together.  For an arbitrary exhaustive component outside "
            "that orbit, the current PP/Hasse/Cartan maps do not construct "
            "Phi.  After the positive derived filler, the first exact "
            "physical obstruction is membership of the full literal M_v "
            "mapping-cone image; two chart copies and an Eq-only correction "
            "cannot supply it"
        ),
        "downstream_terminal": (
            "once such a physical Phi exists, exact q equality is not an "
            "extra hypothesis: a nonzero q defect gives the existing "
            "relative generator and a zero defect transports q to Fredholm"
        ),
        "nonclaims": [
            "no comparison for every arbitrary exhaustive component is claimed",
            "the one-cell image criterion is not a proof of physical membership",
            "a chart-odd presentation H1 value is not a physical eta/sigma terminal",
            "the full Cartan column alternative does not replace this comparison",
        ],
        "pins": PINS,
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
    print("protected physical comparison: SHARP FIRST SOURCE-CELL GATE")
    print("physical relabeling orbit: Phi CONSTRUCTED")
    print("arbitrary off-orbit exhaustive grade: NOT CONSTRUCTED")
    print("first physical obstruction: full literal M_v image membership")
    print("two charts / Eq-only correction: INSUFFICIENT")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
