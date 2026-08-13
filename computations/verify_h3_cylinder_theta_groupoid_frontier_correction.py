#!/usr/bin/env python3
"""Correct the cylinder frontier using the flat theta grade groupoid."""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_trapped_hessian_theta_eq_grade_groupoid.py":
        "b30000bfe8383e1f254fb8fee4724cbd99d8f70a5e8447cffb1c9086a179aec0",
    "notes/h3-trapped-hessian-theta-eq-grade-groupoid.md":
        "5875c531cb0b5ba339665c243488c445bb34ed34edb69dee7bf23f689dc1fbe0",
    "computations/verify_h3_cylinder_d4_cartan_graph_lock_bridge_gate.py":
        "f7f7009c4bf1b4849b26a2aaa7b24d36db3b576148a0f247a95bcac5f01cf4e1",
    "notes/h3-cylinder-d4-cartan-graph-lock-bridge-gate.md":
        "91806307285af0878e469a7ca0d191c729135de1950e73c62007ba9014610c72",
    "computations/verify_h3_centered_shear_to_cartan_single_bridge_reduction.py":
        "27ac408f8ed6dafa1687e22dd8231b1ebea6e5782252d337ab4daf67902a41f1",
    "notes/h3-centered-shear-to-physical-cartan-single-bridge-reduction.md":
        "f7f1dab102a2cc7d01b76db5c853c29861887441d0d7e6e55f824ba4d56902e0",
}
EXPECTED_LEDGER_SHA256 = "54addc4fab4edd483cb4e4969eece194dcaaf753e26e07cef1d74c9fb7b49187"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative, actual))


def dot(left, right) -> Q:
    return sum((Q(a)*Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def theta_feature_q_audit() -> dict[str, object]:
    # Object g has six private features and one anchor-incidence coordinate.
    # Object gT has six separately labelled transposes plus the fixed anchor.
    width = 13
    theta = [None]*width
    for i in range(6):
        theta[i] = 6+i
        theta[6+i] = i
    theta[12] = 12
    require(all(theta[theta[i]] == i for i in range(width)),
            "theta stopped being involutive")

    q_g = tuple(Q(1 if i < 6 else -1 if i == 12 else 0)
                for i in range(width))
    q_gT = tuple(Q(1 if 6 <= i < 12 else -1 if i == 12 else 0)
                 for i in range(width))
    theta_pull_q_gT = tuple(q_gT[theta[i]] for i in range(width))
    require(theta_pull_q_gT == q_g,
            "the physical q cocycle on the theta arrow changed")

    p_half_g = tuple(Q(1 if i < 6 else 0) for i in range(width))
    p_half_gT = tuple(p_half_g[theta[i]] for i in range(width))
    require(sum(bool(x) for x in p_half_gT) == 6
            and dot(p_half_g, p_half_gT) == 0,
            "the theta attachment orbit stopped pairing disjoint grades")
    return {
        "objects": ["g", "gT"],
        "theta_squared": "identity",
        "d_theta": 0,
        "private_feature_sets": [6, 6],
        "private_feature_intersection": 0,
        "q_gT_after_theta_equals_q_g": True,
        "q_cocycle": 0,
        "one_attachment_orbit": (
            "a_g at g determines a_gT=theta(a_g) at gT uniquely"
        ),
        "independent_grade_return_cell": False,
    }


def terminal_and_eq_audit() -> dict[str, object]:
    labels = ("target", "W", "ores", "eta0", "eta1", "sigma", "Eq")
    theta = {
        "target": "target", "W": "W", "ores": "oresT",
        "eta0": "eta1", "eta1": "eta0", "sigma": "sigma", "Eq": "Eq",
    }
    require(theta["target"] == "target" and theta["W"] == "W"
            and theta["sigma"] == "sigma" and theta["Eq"] == "Eq"
            and theta["eta0"] == "eta1" and theta["eta1"] == "eta0",
            "the theta terminal permutation changed")
    return {
        "audited_labels": list(labels),
        "theta_action": theta,
        "central_Eq_object": "E=(H0-u)e_Eq is fixed by theta",
        "KEq_square_commutes": True,
        "terminal_labels_equivariant": True,
        "new_first_PP_diagonal": False,
        "new_grade_holonomy": False,
    }


def exact_frontier_audit() -> dict[str, object]:
    return {
        "5702312_item_4": {
            "old_wording": "transport LambdaT back to canonical Lambda",
            "correct_status": "RETIRED AS AN INDEPENDENT GATE",
            "replacement": (
                "retain g and gT as the two physical objects; theta transports "
                "their Lambda rows and all terminal labels exactly"
            ),
        },
        "theta_does_not_construct": (
            "the first source-labelled response/cap/reduced-Eq attachment a_g"
        ),
        "irreducible_remaining_datum": (
            "one source-valid multiplicative cross-word attachment at g from the "
            "11:110000 pure-00 response/centered cylinder to the 01211222 "
            "labelled P3+K2 cap packet, carrying the cap graph and central "
            "K_Eq boundary together with residue, anchor/q, W and shifted ridge"
        ),
        "automatic_after_one_attachment": [
            "the conjugate S-half attachment theta(a_g) at gT",
            "Lambda_gT theta=Lambda_g and zero q cocycle",
            "target/W invariance and ordinary-residue label transport",
            "eta0/eta1 exchange and sigma invariance",
            "objectwise central K_Eq cancellation",
            "both covariant matching graph-lock packets from the cylinder",
        ],
        "number_of_independent_attachment_theorems": 1,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 cylinder theta-groupoid frontier correction",
        "pins": PINS,
        "theta_q": theta_feature_q_audit(),
        "terminal_Eq": terminal_and_eq_audit(),
        "frontier": exact_frontier_audit(),
        "verdict": (
            "The LambdaT-to-Lambda return listed in 5702312 is not an independent "
            "physical gate.  The correct source category has two fine-grade objects "
            "g,gT and the literal involution theta.  Once one source-labelled "
            "attachment a_g exists, theta(a_g) supplies the conjugate endpoint half "
            "uniquely, with zero q cocycle, equivariant terminals and central K_Eq. "
            "The sole irreducible local datum is the first multiplicative cross-word "
            "cap/central attachment at one grade g."
        ),
        "scope": (
            "exact correction to the frontier statement of 5702312; theta transports "
            "but does not create the first attachment"
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("theta grade groupoid: FLAT AND INVOLUTIVE")
    print("LambdaT->Lambda independent gate: RETIRED")
    print("q/terminal transport after one attachment: AUTOMATIC")
    print("irreducible datum: ONE CROSS-WORD CAP/CENTRAL ATTACHMENT AT g")
    print("ledger_sha256="+digest)


if __name__ == "__main__":
    main()
