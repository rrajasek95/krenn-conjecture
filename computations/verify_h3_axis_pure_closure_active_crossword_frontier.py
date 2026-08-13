#!/usr/bin/env python3
"""Update the h=3 frontier after global axis-pure emptiness.

This is a dependency/scope correction.  The global minimum-support census
and the support-27 coefficient certificate remove the axis-pure escape left
by the old Segre-bright and centered-shear alternatives.  They do not build
the centered cross-word attachment.  In the remaining active-fan branch,
four-good is landed and only a literal-coloop/trapped-Hall packet still needs
the fan-grade physical comparison.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_pure_global_min_support_census.py":
        "4b88379419c94aa21f8a457b89821fb107d4b841c17ffa38ec10516e48426156",
    "notes/h3-axis-pure-global-min-support-census.md":
        "8889c50a1bbeb6049f8c06b61f451e84cd60a1185fd3ad8407390ff5a3a9098d",
    "computations/verify_h3_axis_pure_support27_coefficient_inconsistency.py":
        "5069cc76a5fbfbba115177ab1895c180346b15d4826ca5b419ca7753aabedb65",
    "notes/h3-axis-pure-support27-coefficient-inconsistency.md":
        "98710742a10bc584eff02936dc3b49bdd407fbf122aa08331a936334c007c37e",
    "computations/verify_h3_segre_bright_full_row_min_support_completion_gate.py":
        "3db99d9141e3015c6199da76c0619a235bb6fb95f364e3d2dce338fa2d428572",
    "notes/h3-segre-bright-full-row-min-support-completion-gate.md":
        "26f94fac7c66405eff04406c95935da910d26cdecf135b05a212e469506cbfc9",
    "computations/verify_h3_centered_shear_to_cartan_single_bridge_reduction.py":
        "27ac408f8ed6dafa1687e22dd8231b1ebea6e5782252d337ab4daf67902a41f1",
    "notes/h3-centered-shear-to-physical-cartan-single-bridge-reduction.md":
        "f7f1dab102a2cc7d01b76db5c853c29861887441d0d7e6e55f824ba4d56902e0",
    "computations/verify_h3_active_fan_coloop_or_four_good.py":
        "93030f2994e2e6a2052a09a5fefd179c99e0b8fb55cd0c77bee2cb9f8dbc6bb4",
    "notes/h3-active-fan-coloop-or-four-good.md":
        "9be8996264fa2070a8f5d7f725f3fcb154b6ee2df2b3e5d3ccd4a6412ec5b03a",
    "computations/verify_h3_active_fan_coloop_gate_ii_assembly_boundary.py":
        "22e1e7a6a933b1ba71bbd95bb605b1351e823506e495682cccff312cd3df3b15",
    "notes/h3-active-fan-coloop-gate-ii-assembly-boundary.md":
        "bacb7b4b138882c0cc07f13767f2e4ead86aa630c55cf1a946943141b7cee7a7",
    "computations/verify_h3_cross_word_cap_central_attachment_first_face_gate.py":
        "6f1dc2d4baece91046f8834418a7ce7b2fa84a9a3f1acc867cdf33353a807eea",
    "notes/h3-cross-word-cap-central-attachment-first-face-gate.md":
        "79a9cfda1261163fd0039e2fed9d8bbe84218c04b3ca78096f7db8f238c79022",
    "computations/verify_h3_centered_pointed_face_existing_conormal_cap_terminal_gate.py":
        "dabaf6c5132f835c6d681d1ecb30611eae8b0920b2c97272e487bcb9c9f068c9",
    "notes/h3-centered-pointed-face-existing-conormal-cap-terminal-gate.md":
        "9f41f22cc232beefca120c770c5815faa2aff0b80c738069cfd18a5c3557fa17",
}
EXPECTED_LEDGER_SHA256 = "23f56cd2640635a9bf063aa2d9e74cb5ff5b0ea934de1f72803323d32354fd90"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def audit_axis_pure_supersession():
    global_census = load(
        "computations/verify_h3_axis_pure_global_min_support_census.py",
        "axis_global_census",
    )
    coefficient = load(
        "computations/verify_h3_axis_pure_support27_coefficient_inconsistency.py",
        "axis_support27_coefficients",
    )
    # Rebuild the complete Boolean presentation in this lightweight
    # dependency checker, but do not rerun native SAT backends.  Their exact
    # six-model/UNSAT certificate is frozen by the pinned checker and note;
    # importing a Python-3.13 native extension from another interpreter
    # would make normal/-O/-I-S modes spuriously environment-dependent.
    base = global_census.load_base()
    formula = global_census.build_formula(base)
    coefficient_ledger, coefficient_digest = coefficient.audit()
    require(global_census.EXPECTED_LEDGER_SHA256
            == "89c67e45a7ba5e05cba4dfbef988957d14ffd996bc8b3a53739c9dff9692d3b9"
            and len(formula["cell_vars"]) == 69
            and len(formula["terms"]) == 3645
            and len(formula["term_ids_by_fibre"]) == 849
            and coefficient_digest
            == "7f07fd0b9cfe7deec07920b0078ba6e9dc34573246df3e440dfb977716e2363c",
            (global_census.EXPECTED_LEDGER_SHA256, coefficient_digest,
             len(formula["cell_vars"]), len(formula["terms"]),
             len(formula["term_ids_by_fibre"])))
    require(coefficient_ledger["symmetry_and_consequence"]
            ["all_support27_closures_inconsistent"],
            coefficient_ledger["symmetry_and_consequence"])
    return {
        "unrestricted_F0_normalized_minimum_support_models": 6,
        "model_support_sizes": [27]*6,
        "model_type": "F0 + bright K2,2 + bright K2,4",
        "after_projected_blocks": "UNSAT",
        "coefficient_lifts": 0,
        "conclusion": "canonical h=3 axis-pure exact-source branch is empty",
        "supersedes": [
            "80732b0 larger axis-purified cancellation packet",
            "d7765f6 parallel axis-pure multi-term support escape",
            "dbee33d arbitrary-coloop caveat above support 27 in this branch",
        ],
    }


def audit_old_branch_and_active_split():
    bright = load(
        "computations/verify_h3_segre_bright_full_row_min_support_completion_gate.py",
        "old_bright_branch",
    )
    shear = load(
        "computations/verify_h3_centered_shear_to_cartan_single_bridge_reduction.py",
        "old_shear_branch",
    )
    fan = load(
        "computations/verify_h3_active_fan_coloop_or_four_good.py",
        "active_fan_split",
    )
    gate = load(
        "computations/verify_h3_active_fan_coloop_gate_ii_assembly_boundary.py",
        "active_fan_gate_ii",
    )
    bright_ledger, _ = bright.audit()
    shear_ledger, _ = shear.audit()
    ternary = fan.audit_ternary_rank_alternative()
    gate_assembly = gate.audit_branch_assembly()
    require("four-good or a literal pure-colour coloop" in
            bright_ledger["routed_and_open_branches"]["offdiagonal_enlargement"]
            and shear_ledger["full_row_branching"]["offdiagonal_completion"]
            == "routes to private-site fan then four-good/coloop",
            (bright_ledger["routed_and_open_branches"],
             shear_ledger["full_row_branching"]))
    require(ternary["four_good_assignments"] == 1
            and ternary["literal_coloop_assignments"] == 26
            and gate_assembly["only_nonterminal_after_saturation"]
            == "single missing fan-grade physical Phi/q packet",
            (ternary, gate_assembly))
    return {
        "h3_full_row_alternative_after_axis_closure": {
            "axis_pure": "empty",
            "offdiagonal": "source-provenant private-site active fan",
        },
        "active_fan_split": {
            "all_pure_supports_avoid_both_fan_edges":
                "four-good; existing landing, no cross-word attachment",
            "some_fan_edge_is_a_pure_support_coloop":
                "literal-coloop/trapped-Hall branch",
        },
        "only_open_active_comparison": (
            "fan-grade physical odd Phi with J0*Phi=A*J and literal q=M-a "
            "on the trapped coloop packet"
        ),
        "termination_after_comparison": "already finite/exhaustive",
    }


def audit_crossword_scope():
    cross = load(
        "computations/verify_h3_cross_word_cap_central_attachment_first_face_gate.py",
        "crossword_attachment",
    )
    centered = load(
        "computations/verify_h3_centered_pointed_face_existing_conormal_cap_terminal_gate.py",
        "centered_pointed_face",
    )
    cross_ledger, cross_digest = cross.audit()
    centered_ledger, _ = centered.audit()
    require(cross_digest
            == "a0bb53ea0c5c3f683c2e815c2d8e83a2afa63857d0e945b1fc80b32d13bf50d8"
            and not cross_ledger["selected_fibre"]
            ["db01_in_old_complete_response_PP_span"]
            and cross_ledger["mixed_square"]
            ["mixed_two_cell_in_current_literal_inventory"] is False,
            (cross_digest, cross_ledger))
    require("scaled pointed centered-response attachment" in
            centered_ledger["shortest_positive_interface"]["name"],
            centered_ledger["shortest_positive_interface"])
    return {
        "centered_attachment_status": "still open",
        "first_faces": [
            "scaled centered conormal 90df-dR",
            "selected six-term db01 principal-parts face",
            "central Eq/D4 comparison Phi_orb(E)=R_E14",
            "cross-word cap/rooted B1+B4 face",
        ],
        "active_branch_that_needs_comparison": (
            "only the pure-colour-coloop/trapped-Hall outcome, not four-good"
        ),
        "typing_caution": (
            "the centered cross-word attachment is a candidate master cell, "
            "but no pinned theorem yet identifies its restriction with Gate "
            "II's fan-grade Phi; that factorization remains part of the "
            "physical comparison theorem"
        ),
        "independent_of_axis_census": (
            "the attachment belongs to the unpurified centered/cap grade and "
            "is not constructed by excluding axis-pure coefficient supports"
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": "h3 axis-pure closure / active cross-word frontier correction",
        "pins": PINS,
        "axis_pure_supersession": audit_axis_pure_supersession(),
        "surviving_active_split": audit_old_branch_and_active_split(),
        "crossword_scope": audit_crossword_scope(),
        "corrected_shortest_map": [
            "canonical h3 full-row bright/centered packet",
            "axis-pure arm -> impossible by global census plus coefficient certificate",
            "offdiagonal arm -> private-site active fan",
            "four-good -> existing landing",
            "literal coloop -> trapped Hall packet -> missing fan-grade physical Phi",
            "after Phi -> q defect / target circuit / normalized coloop closures",
        ],
        "verdict": (
            "The h=3 axis-pure support escape is completely closed, including "
            "all larger inclusion-minimal supports; it must be deleted from "
            "the 80732b0/d7765f6 frontier.  This does not close uniform entry "
            "or build the centered attachment.  In the remaining h=3 active "
            "fan, four-good is already landed.  Only the literal pure-colour "
            "coloop trapped in a closed Hall shore needs a new physical "
            "comparison, immediately the fan-grade Phi/q packet.  Identifying "
            "that Phi as a restriction of the master cross-word attachment is "
            "plausible but is not yet a proved dependency."
        ),
        "scope": (
            "canonical h=3 axis-purified five-tensor branch over characteristic "
            "zero and the already-entered h=3 active-fan packet; no all-h axis "
            "theorem and no global entry into the centered packet"
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                (digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 axis-pure support escape: CLOSED")
    print("remaining active split: four-good CLOSED / coloop Phi OPEN")
    print("centered cross-word attachment: STILL OPEN, not yet identified with Phi")
    print("uniform/all-h entry: OUT OF SCOPE")
    print("ledger_sha256="+digest)


if __name__ == "__main__":
    main()
