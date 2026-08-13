#!/usr/bin/env python3
"""Classify the unaudited Gate-I probe against later literal theorems.

The probe's cap-plus-Cartan identity is now independently proved, including
literal private rows and the eta/sigma terminal.  Its terminal-only cokernel
was an artefact of modelling the Cartan column with terminal zero and is
therefore false for the committed physical inventory.  Its input-side
occurrence identities remain coarse: they do not construct the shifted
15-label map or the two shared labelled-residue sections.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/unaudited-gate1-phi-probe-2026-08-12/REPORT.md":
        "998d0e40cc66b4e75623cab05b94a18c55e7bb3fdcef2370d149462b4dbd5e90",
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
    "computations/verify_h3_cut_swap_odd_prism_kdu_typing_gate.py":
        "a1c7868bee94baf12f0f4915305bb1e21cdc3f6732ccec9adf3d68768d3d90b0",
    "computations/verify_h3_cut_swap_shared_repair_source_scope_guard.py":
        "96280ef01c70b4f3381e6d85d2c9fb64b1620850305a4346601fccbd7d63dc44",
    "computations/verify_h3_cut_swap_shared_repair_face3_tor_obstruction.py":
        "e43d537e9c321d5ab0b61632aa16673dfb58d5709943e1d2b7ff26032f9df8ca",
    "computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py":
        "db23eb4e760dd84934426a80516aad355486e947626da1849454718b512efb2d",
}
EXPECTED_LEDGER_SHA256 = "0f79205dc288d1495c193a1b45201977d049b52bde0232d85d744367e66dfa7a"


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


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    report = (ROOT / "computations/unaudited-gate1-phi-probe-2026-08-12/REPORT.md").read_text()
    for headline in (
        "residue/private/Eq part of J(M_v) is ALREADY a boundary",
        "pairs +1 with the KS corner column D_w + R_w",
        "What persists is purely terminal",
        "pullbacks from the 15-label quotient",
    ):
        require(headline in report, ("probe report headline changed", headline))

    mv = load(
        "computations/verify_h3_literal_mv_cap_cartan_composition.py",
        "probe_status_mv",
    )
    kdu = load(
        "computations/verify_h3_cut_swap_odd_prism_kdu_typing_gate.py",
        "probe_status_kdu",
    )
    scope = load(
        "computations/verify_h3_cut_swap_shared_repair_source_scope_guard.py",
        "probe_status_scope",
    )
    face3 = load(
        "computations/verify_h3_cut_swap_shared_repair_face3_tor_obstruction.py",
        "probe_status_face3",
    )

    # These four pinned files are themselves three-mode frozen theorem
    # checkers.  Re-running their deep order-six eliminations here would make
    # this status classifier needlessly cubic.  Verify their frozen ledger
    # constants and the exact theorem fields used below; the hashes above pin
    # the complete implementations and their dependency lists.
    mv_source = (ROOT / next(relative for relative in PINS
                             if relative.endswith(
                                 "literal_mv_cap_cartan_composition.py"))).read_text()
    require(mv.EXPECTED_LEDGER_SHA256
            == "84904cfd9f434eb8ff36548a0b2e0b2e68b8ec562c6559a89acdefb94500eb64"
            and '"literal_boundary_support": 360' in mv_source
            and '"ordinary_residue": [0, 0, 0, 0]' in mv_source
            and '"D_W_target_ainc": [0, 0, 0, 0]' in mv_source
            and '"eta_z": "1+delta_(vz)*u_z/t"' in mv_source
            and '"sigma": "-q_pq^22"' in mv_source
            and '"source_provenant": True' in mv_source
            and '"literal_source_output": operator["literal_source_output"]' in mv_source
            and '"first_Spencer_output": operator["first_transfer_support"]' in mv_source,
            "the exact cap/Cartan output theorem changed")

    kdu_source = (ROOT / next(relative for relative in PINS
                              if relative.endswith(
                                  "cut_swap_odd_prism_kdu_typing_gate.py"))).read_text()
    require(kdu.EXPECTED_LEDGER_SHA256
            == "86c90e8001f6a7bb7153602183813759cdccb362040eb88567727bd8e6b84982"
            and '"collision_basis_size": len(all_labels)' in kdu_source
            and '"M_v_literal_support": len(literal_boundary)' in kdu_source
            and '"equality_Kd_u012_equals_M_v_well_typed": False' in kdu_source
            and 'require(len(all_labels) == 15 and len(l) == 12' in kdu_source
            and 'require(len(literal_boundary) == 360' in kdu_source,
            "the input/output typing gap changed")

    scope_source = (ROOT / next(relative for relative in PINS
                                if relative.endswith(
                                    "shared_repair_source_scope_guard.py"))).read_text()
    require(scope.EXPECTED_LEDGER_SHA256
            == "bdad46b583b0fcab4065314bf8bb957bd79b5b502e2e76680d438519857b671a"
            and '"source_provenant": True' in scope_source
            and '"six_multiplier_label_section_constructed": False' in scope_source
            and '"Gate_I_assembly_now": False' in scope_source,
            "the labelled-residue scope changed")

    face_source = (ROOT / next(relative for relative in PINS
                               if relative.endswith(
                                   "shared_repair_face3_tor_obstruction.py"))).read_text()
    require(face3.EXPECTED_LEDGER_SHA256
            == "ef2c8f58a5fd0fe33082fd79460477fbdacabb9c7d1ef1628a0487c7eccc0253"
            and '"epsilon_on_required_e3": 1' in face_source
            and '"Gate_I_assembly_now": False' in face_source,
            "the face-3 Tor frontier changed")

    ledger = {
        "theorem": "status audit of the unaudited Gate-I Phi probe",
        "pins": PINS,
        "headline_classification": {
            "cap_plus_Cartan_identity": {
                "status": "independently proved, in stronger literal form",
                "proof": "271df91",
                "exact_scope": (
                    "normalized Y=1 canonical repeated component; 360 literal "
                    "features, private/Eq signs, protected zero, and physical "
                    "eta/sigma all checked"
                ),
            },
            "old_private_minus_W_minus_target_plus_R_separator": {
                "status": "correctly eliminated, but the probe model is not the proof",
                "proof": (
                    "271df91 supplies a physical Cartan residue alpha with zero "
                    "private/W/target, so the corner separator pairs nontrivially"
                ),
                "scope_warning": (
                    "the probe's freely embedded KS/corner inventory is coarse; "
                    "this does not eliminate the later physical anchor separator"
                ),
            },
            "terminal_only_cokernel_and_terminal_separator": {
                "status": "false/superseded for the physical inventory",
                "reason": (
                    "the probe entered K with terminal zero.  The physical K in "
                    "271df91 carries all five eta constants, eta1_U1, and sigma, "
                    "so M_v=-O_alpha+K is already a committed source image"
                ),
            },
            "output_side_is_terminal_realizability": {
                "status": "false/superseded",
                "current_status": "output-side membership is closed by 271df91",
            },
        },
        "reconstruction_and_coherence": {
            "18_to_15_rank_and_three_overlap_directions": (
                "valid occurrence-level reconstruction; independently frozen "
                "by the later cutwise descent checker"
            ),
            "u_support_12_and_occurrence_shadow": (
                "valid only in the 15-label occurrence module; def89a3 proves "
                "that calling it the complete protected J_col is ill-typed"
            ),
            "288_576_rank_claim": (
                "presentation-rank information only; it supplies neither "
                "augmented terminal rows nor a source comparison Phi"
            ),
            "rho_equivariance_makes_coherence_automatic": (
                "false as a construction claim: rho reduces the three shared "
                "labels to one fixed orbit plus one paired orbit, but e5eb1fe "
                "still requires their two labelled residue sections"
            ),
        },
        "frontier_effect": {
            "changes_two_labelled_residue_sections": False,
            "reason": (
                "the probe evaluates no real Phi candidate and has no shifted "
                "tail/fine-grade map.  It neither constructs d_fixed,d_pair nor "
                "changes their source scope"
            ),
            "latest_refinement": (
                "4f91155 identifies the favorable B0,B4,B5 assignment with "
                "q34*h3 and obstructs its standard denominator/PP/bar lift by "
                "the clean epsilon face dual"
            ),
            "current_missing_object": (
                "a higher physical occurrence-splitting relative cell, or a "
                "physical terminal extension of the face obstruction"
            ),
        },
        "probe_honest_limits_after_audit": {
            "Cartan_private_open": "resolved: literal source and D1 outputs are zero",
            "Cartan_terminal_open": "resolved: exact eta/sigma packet is nonzero and correct",
            "literal_input_Phi_open": "still open and now localized to the shared repair",
        },
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("unaudited probe status ledger changed", digest))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("unaudited Gate-I Phi probe: STATUS AUDITED")
    print("cap+Cartan identity: PROVED LITERALLY by 271df91")
    print("terminal-only obstruction: FALSE/SUPERSEDED")
    print("input occurrence shadow: NOT A PHYSICAL PHI")
    print("two labelled-residue sections frontier: UNCHANGED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
