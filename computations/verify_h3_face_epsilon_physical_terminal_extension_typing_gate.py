#!/usr/bin/env python3
"""Test whether the physical Cartan terminal promotes the face epsilon.

There is an exact numerical coincidence:

    sum_v K_v(eta_z) = 5 + u_z/t,

which is the negative of the clean Omega separator's eta response.  This is
the physical compensation law, including the sigma response.  It does not,
however, promote the face-Tor covector epsilon to a physical annihilator.
The two objects have different variance and live in different spaces:

* epsilon is a covector on the five selected denominator face projections;
* K_v (and M_v=-O_alpha+K_v) is a source column with a 360-feature literal
  boundary, four Eq entries, and terminal output.

Thus K adds annihilator equations; it does not supply the missing pullback
from the 15 collision labels to the literal output.  The coincidence becomes
a cancellation only after granting the physical Omega/r comparison map that
the Gate-I input construction is meant to provide.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_cut_swap_shared_repair_face3_tor_obstruction.py":
        "e43d537e9c321d5ab0b61632aa16673dfb58d5709943e1d2b7ff26032f9df8ca",
    "computations/verify_h3_rootless_clean_separator_repeated_inventory_gate.py":
        "af9a69ad996bd4390ff3fe9139e357a3bb765292ec969350a948612d9b824fa7",
    "computations/verify_h3_rootless_eta_cyclic_compensation_boundary.py":
        "9beab390c8ed2c89f1a8f62ee54857c03199fecd5ad9a69ab6f29d6a04140b6d",
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
    "computations/verify_h3_cut_swap_odd_prism_kdu_typing_gate.py":
        "a1c7868bee94baf12f0f4915305bb1e21cdc3f6732ccec9adf3d68768d3d90b0",
    "computations/verify_unaudited_gate1_phi_probe_status_audit.py":
        "6358f30c24cc2b73d34fc8e922a97b543f3b253be9e67d07e099f792a12ac6eb",
}
EXPECTED_LEDGER_SHA256 = (
    "57b8ee4a80739da5bb9d192d4dde2b2410dbfdea948fd4e26f653ca35fdc0ba4"
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))


def affine(constant=0, **entries):
    return (Q(constant),) + tuple(Q(entries.get(f"u{site}", 0))
                                  for site in range(1, 6))


def add(*values):
    return tuple(sum(value[index] for value in values)
                 for index in range(len(values[0])))


def scale(coefficient, value):
    return tuple(Q(coefficient) * entry for entry in value)


def terminal_algebra() -> dict[str, object]:
    records = []
    for z in range(1, 6):
        facewise = [affine(1, **{f"u{z}": 1}) if v == z else affine(1)
                    for v in range(1, 6)]
        cartan_aggregate = add(*facewise)
        omega_aggregate = affine(-5, **{f"u{z}": -1})
        require(cartan_aggregate == affine(5, **{f"u{z}": 1})
                and add(cartan_aggregate, omega_aggregate) == affine(),
                ("the eta compensation identity changed", z))
        records.append({
            "eta": f"eta_{z}",
            "K_facewise": [
                "1+u_z/t" if v == z else "1" for v in range(1, 6)
            ],
            "sum_K": f"5+u_{z}/t",
            "sum_dOmega": f"-5-u_{z}/t",
            "formal_sum": 0,
        })
    # Every physical K_v has sigma=-q_pq^22, the opposite of dOmega_v.
    sigma_k = -5
    sigma_omega = 5
    require(sigma_k + sigma_omega == 0,
            "the cyclic sigma compensation changed")
    return {
        "eta_records": records,
        "sigma_sum_K_in_qpq22_units": sigma_k,
        "sigma_sum_dOmega_in_qpq22_units": sigma_omega,
        "conditional_cancellation": True,
        "condition": (
            "the five K terminal packets must be identified as the rootless "
            "comparison response paired facewise with the five Omega rows"
        ),
    }


def pinned_typing_facts() -> dict[str, object]:
    face = (ROOT / "computations/verify_h3_cut_swap_shared_repair_face3_tor_obstruction.py").read_text()
    mv = (ROOT / "computations/verify_h3_literal_mv_cap_cartan_composition.py").read_text()
    kdu = (ROOT / "computations/verify_h3_cut_swap_odd_prism_kdu_typing_gate.py").read_text()
    probe = (ROOT / "computations/verify_unaudited_gate1_phi_probe_status_audit.py").read_text()
    separator = (ROOT / "computations/verify_h3_rootless_clean_separator_repeated_inventory_gate.py").read_text()
    require('"epsilon_on_required_e3": 1' in face
            and '"Gate_I_assembly_now": False' in face,
            "the face epsilon theorem changed")
    require('"literal_boundary_support": 360' in mv
            and '"Eq": [int(value) for value in alpha]' in mv
            and '"eta_z": "1+delta_(vz)*u_z/t"' in mv
            and '"sigma": "-q_pq^22"' in mv,
            "the literal M_v output theorem changed")
    require('require(len(all_labels) == 15 and len(l) == 12' in kdu
            and 'require(len(literal_boundary) == 360' in kdu
            and '"equality_Kd_u012_equals_M_v_well_typed": False' in kdu,
            "the 15-to-360 typing guard changed")
    require('"terminal_only_cokernel_and_terminal_separator"' in probe
            and '"status": "false/superseded for the physical inventory"' in probe
            and '"literal_input_Phi_open": "still open' in probe,
            "the probe status theorem changed")
    require('"physical_terminal_annihilator_constructed": False' in separator,
            "a physical clean separator appeared")
    return {
        "face_projection_space": {
            "dimension": 5,
            "covector": "epsilon=(1,1,1,1,1)",
            "epsilon_on_required_e3": 1,
        },
        "collision_occurrence_space": {
            "dimension": 15,
            "rho_shared_orbits": "one fixed plus one pair",
        },
        "literal_Mv_lower_space": {
            "feature_count": 360,
            "additional_outputs": "four Eq entries and eta/sigma terminal",
            "source_variance": "K_v and M_v are columns, not covectors",
        },
        "typed_maps": {
            "denominator_kernel_to_face_projection": "constructed",
            "collision_U15_to_literal_L360": "not constructed",
            "face_epsilon_to_complete_physical_cokernel": "not constructed",
        },
    }


def audit():
    pin_dependencies()
    terminal = terminal_algebra()
    typing = pinned_typing_facts()
    ledger = {
        "theorem": "face epsilon / physical Cartan terminal extension typing gate",
        "pins": PINS,
        "terminal_response": terminal,
        "variance_and_spaces": typing,
        "what_271df91_changes": (
            "it exactly supplies the eta/sigma output packet and therefore "
            "kills the old terminal-only cokernel claim"
        ),
        "what_it_does_not_change": (
            "it does not define a pullback of epsilon through a physical Phi, "
            "nor a dual lift annihilating the complete source map"
        ),
        "dual_extension_equations": (
            "a physical lift epsilon_tilde must restrict to epsilon and obey "
            "J_phys^*(epsilon_tilde)=0; every K_v/M_v column is an additional "
            "equation on epsilon_tilde, not a definition of epsilon_tilde"
        ),
        "verdict": (
            "the Cartan terminal cancels the eta/sigma polynomial formally "
            "after a facewise Omega/r identification, but that identification "
            "is exactly the missing typed comparison; the face obstruction "
            "cannot yet be promoted to a physical separator"
        ),
        "remaining_frontier": (
            "construct d_fixed,d_pair / Phi, or construct directly a dual "
            "lift on the complete physical 360-feature plus terminal codomain"
        ),
        "physical_terminal_separator_constructed": False,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("face epsilon extension ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 face epsilon physical terminal extension: NOT YET TYPED")
    print("sum_v K_v(eta_z)=5+u_z/t: YES")
    print("sum_v K_v(sigma) cancels sum_v dOmega_v(sigma): YES")
    print("epsilon F5 -> physical cokernel: NO MAP")
    print("15 collision labels -> 360 literal features: STILL OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
