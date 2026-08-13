#!/usr/bin/env python3
"""The nonzero E14 private placement cannot be the raw pointed substitution.

The conditional E14 comparison asks for the selected-component assignment

    F=H0-u  ->  1-v04,
    e_Eq    ->  m=(p1*s1)u35*v24,

so that F*e_Eq maps to R=m(1-v04).  A pointed source-algebra map must send
every central equation vanishing at the base point to a function vanishing
at the physical point, modulo the physical source ideal.  Consequently the
displayed assignment is pointed only when v04=1 at the physical point, and
then R=0.  Whenever R is the nonzero private return needed by the E14
landing, the assignment can only be a higher chain/Koszul comparison; it
cannot itself provide the pointed conormal/anchor law.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_e14_cplus_keq_companion_assembly_gate.py":
        "754038f33ae07329e0fc6a8825df9f1695664a40df91afbb77e52dedb1e1aae1",
    "notes/h3-e14-cplus-keq-companion-assembly-gate.md":
        "8548c1db8ec362fce0876c0f67d77efc96f141ebd4c82b6564069e3a089eff3a",
    "computations/verify_h3_e14_keq_private_placement_residue_identification_gate.py":
        "89b0b694b525dba502314e61922cb884ef6ddd2f14fea68b3bafd5215aa40c70",
    "notes/h3-e14-keq-private-placement-residue-identification-gate.md":
        "36828d8503d929427eef55886cb68cbfe7c2431649c38382907835365bd5ed38",
    "computations/verify_h3_anchor_conormal_functoriality_bridge.py":
        "83879756547765878c36944c1ab14827ab77a1f217931bc05db0c72cb0af32a8",
    "notes/h3-anchor-conormal-functoriality-bridge.md":
        "ff21fee754b3de39788dca5c6d024a6a7f539648fb3cc9473c2690239c8bbac8",
    "computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py":
        "c583279d8f4cb7efc24b7fc4784e480b63acb1ca7fe430ae1a7e2db2b854c11b",
    "notes/h3-augmented-p2-section-shortest-conditional-gate.md":
        "ee5da6f0911feb06707106cc6207161bbac7cabd31885f554321698dfbb989d8",
}
EXPECTED_LEDGER_SHA256 = (
    "a6ce04df8d823f67f2caf8ad43c7f6e6113ccaa2abcb886d86e0784010686650"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def audit_dependencies() -> dict[str, object]:
    placement_text = (ROOT / PINS.keys().__iter__().__next__()).read_text()
    require(all(fragment in placement_text for fragment in (
        '"F=H0-u": "1-v04_00"',
        '"e_Eq": "(p1_0_1*s1_1_1)*u35_11*v24_11"',
        '"image": "R_E14"',
        '"source_labelled_map_constructed": False',
    )), "selected placement changed")
    missing = {
        "F=H0-u": "1-v04_00",
        "e_Eq": "(p1_0_1*s1_1_1)*u35_11*v24_11",
        "image": "R_E14",
        "source_labelled_map_constructed": False,
    }

    residue_text = (ROOT /
        "computations/verify_h3_e14_keq_private_placement_residue_identification_gate.py"
    ).read_text()
    require('"exact_residue": "-E=-2 D_root tensor d_even"' in residue_text
            and '"new_direction_if_d_even_granted": False' in residue_text,
            "conditional post-placement residue changed")

    anchor_text = (ROOT /
        "computations/verify_h3_anchor_conormal_functoriality_bridge.py"
    ).read_text()
    require("morphism of pointed source " in anchor_text
            and "presentations and f-Phi_beta" in anchor_text
            and "first-order conormal form " in anchor_text
            and "[d(u_f-u)]=0" in anchor_text,
            "pointed anchor criterion changed")

    return {
        "selected_chain_assignment": missing,
        "post_placement_residue": "-2 D_root tensor d_even",
        "pointed_anchor_requirement": "[d(u_f-u)]=0",
    }


def audit_pointedness() -> dict[str, object]:
    # Evaluation at a physical source point.  All physical source equations
    # G_j vanish, so adding sum c_j G_j to 1-v cannot change the argument.
    cases = []
    for v04 in map(Q, (0, 1, 2, -1)):
        for multiplier in map(Q, (0, 1, 3)):
            image_f = Q(1) - v04
            private_return = multiplier * image_f
            pointed = image_f == 0
            cases.append({
                "v04": str(v04),
                "multiplier": str(multiplier),
                "image_F_mod_source_ideal": str(image_f),
                "R_E14": str(private_return),
                "raw_assignment_pointed": pointed,
            })
            require(not (pointed and private_return != 0),
                    "a pointed raw assignment acquired nonzero private return")
            if multiplier != 0 and private_return != 0:
                require(not pointed,
                        "nonzero private return became pointed")

    # Sharp two-completion guard.  At v=1 the map is pointed but its private
    # face is zero.  At v=0 the private face is a unit but the map is not
    # pointed.  Both have the same formal product factorization R=m(1-v).
    pointed_case = next(case for case in cases
                        if case["v04"] == "1" and case["multiplier"] == "1")
    private_case = next(case for case in cases
                        if case["v04"] == "0" and case["multiplier"] == "1")
    require(pointed_case["raw_assignment_pointed"]
            and pointed_case["R_E14"] == "0"
            and not private_case["raw_assignment_pointed"]
            and private_case["R_E14"] == "1",
            ("sharp pointed/private guard changed", pointed_case, private_case))

    return {
        "lemma": (
            "if F(x)=0 and phi(F)=1-v04 modulo the physical source ideal, "
            "pointedness forces v04(x)=1 and hence "
            "phi(F*e_Eq)(x)=m(x)(1-v04(x))=0"
        ),
        "finite_cases": cases,
        "sharp_guard": {
            "pointed_but_trivial_private_face": pointed_case,
            "nonzero_private_face_but_nonpointed": private_case,
        },
        "robust_modulo_source_ideal": True,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "E14 K_Eq private-placement pointedness gate",
        "pins": PINS,
        "dependencies": audit_dependencies(),
        "pointedness": audit_pointedness(),
        "verdict": (
            "The necessary selected-component factorization "
            "(H0-u)e_Eq -> endpoint*u35*v24*(1-v04) is exact as a "
            "chain-level target, but its raw factor assignment cannot be a "
            "nontrivial pointed source-algebra map.  Pointedness forces "
            "v04=1 and kills R_E14; nonzero R_E14 forces the assignment to "
            "be nonpointed.  Therefore the private placement must be a "
            "higher PP/Koszul comparison, while P_f=[d(u_f-u)] remains an "
            "independent homogeneous face of the same AugP2 totalization."
        ),
        "shortest_positive_target": (
            "one augmented P2 totalization with two distinct homogeneous "
            "faces: a higher chain cell landing (H0-u)e_Eq on R_E14 and a "
            "pointed conormal cell killing d(u_f-u); the raw substitution "
            "cannot supply both"
        ),
        "scope": (
            "This excludes only the displayed raw factor assignment as the "
            "pointed comparison.  It does not exclude a larger augmented "
            "source algebra with an additional homotopy whose total image "
            "contains R_E14, nor does it promote nonpointedness to a physical "
            "terminal."
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("pointedness ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("raw factor assignment gives exact R_E14: YES")
    print("raw assignment pointed with nonzero R_E14: NO")
    print("pointed branch: v04=1, hence R_E14=0")
    print("nonzero private branch: requires higher chain/Koszul comparison")
    print("P_f conormal face remains independent")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
