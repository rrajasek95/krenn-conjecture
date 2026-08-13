#!/usr/bin/env python3
"""Identify the residue after the conditional E14 K_Eq private placement.

The canonical E14 S-pair has B=U+R, with

    R=(p1*s1)u35*v24*(1-v04).

After the conditional placement (H0-u)e_Eq -> R, the old unary U supplies
the full E14 target and the nearest physical K_Eq lift leaves root-word
ordinary residue -E.  This checker proves

    -E = -2 D_root tensor d_even,

so a same-grade root decoration of the pure d_even section cancels it.  The
scalar cap residue z_cap is retained as an independent direct-sum row and
cannot cancel any root-word residue coordinate.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_e14_cplus_keq_companion_assembly_gate.py":
        "754038f33ae07329e0fc6a8825df9f1695664a40df91afbb77e52dedb1e1aae1",
    "notes/h3-e14-cplus-keq-companion-assembly-gate.md":
        "8548c1db8ec362fce0876c0f67d77efc96f141ebd4c82b6564069e3a089eff3a",
    "computations/verify_h3_cplus_conditional_physical_dressing_assembly.py":
        "e8014fdfd2263a8eb6bffff11e31c339b5b7965989a61324f8d118a91f791f46",
    "notes/h3-cplus-conditional-physical-dressing-assembly.md":
        "b3afd746e6c275ca23e0b3ee5f26dfbc763301ed7371be4377612709904c19c0",
    "computations/verify_h3_cplus_root_even_labelled_ores_sigma_cartan_gate.py":
        "144d1fd64d8a733f3ec737edd301c540e66d545c9d72adf1abba5f7ed4764ce1",
    "notes/h3-cplus-root-even-labelled-ores-sigma-cartan-gate.md":
        "ed585718710ac755de36ce6eb40cf0900674059a37255c261fa6ae386913c7a6",
    "computations/verify_h3_augp2_primitive_cap_response_keq_reduction_gate.py":
        "4dabdae7b9060bdb92c0ed32b0016e7e2694750dc176e1857cc9a54cb8176587",
    "notes/h3-augp2-primitive-cap-response-keq-reduction-gate.md":
        "1f8e8a4a5ffc26a8fdcefcb970c3bc35887a1d521ca27ce3173a790b82dfba5d",
    "computations/verify_h3_p2_labelled_ores_cut_even_deven_gauge_gate.py":
        "0a4215db2b91843753cc636b489a81f8e30a8c3de234979c74c9f852d74e3d8a",
    "notes/h3-p2-labelled-ores-cut-even-deven-gauge-gate.md":
        "0477f14ab8725708711ff098c68ae29f10625516024cc2a93413c780ea466054",
}
EXPECTED_LEDGER_SHA256 = (
    "c4f7850fc66736cc5494131c67ee510483d4898f46330e2904c0a602a2f4d160"
)


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


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(scalar: Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(scalar) * entry for entry in vector)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    require(columns, "rank needs columns")
    width = len(columns[0])
    require(all(len(column) == width for column in columns), "rank width")
    matrix = [list(row) for row in zip(*columns, strict=True)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, width)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[answer], matrix[pivot] = matrix[pivot], matrix[answer]
        value = matrix[answer][column]
        matrix[answer] = [entry / value for entry in matrix[answer]]
        for row in range(width):
            if row == answer or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right in
                           zip(matrix[row], matrix[answer], strict=True)]
        answer += 1
    return answer


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def audit_conditional_companion() -> dict[str, object]:
    assembly = load(
        "computations/verify_h3_e14_cplus_keq_companion_assembly_gate.py",
        "residue_id_e14_assembly",
    )
    ledger, digest = assembly.audit()
    require(digest == assembly.EXPECTED_LEDGER_SHA256,
            "E14 Cplus/K_Eq assembly changed")
    identity = ledger["canonical_E14_S_pair"]
    placed = ledger["conditional_physical_assembly"]
    require(identity["exact_identity"] ==
                "B_E14=U[000101]*v24_11+R_E14"
            and identity["dual_values"] == {"U": 0, "R": -1, "B": -1}
            and placed["missing_occurrence_map"] == {
                "F=H0-u": "1-v04_00",
                "e_Eq": "(p1_0_1*s1_1_1)*u35_11*v24_11",
                "image": "R_E14",
                "source_labelled_map_constructed": False,
            }
            and placed["old_unary_plus_R_equals_full_E14_target"],
            ("conditional E14 private placement changed", identity, placed))
    require(placed["first_row_after_occurrence_placement"] ==
                "word-resolved labelled ordinary residue -E"
            and placed["anchor_on_nearest_lift"] == 0
            and placed["W_on_nearest_lift"] == 0
            and placed["target_on_nearest_lift"] == 0,
            ("post-placement first residue changed", placed))
    return {
        "exact_identity": identity["exact_identity"],
        "R_E14": identity["private_return"],
        "conditional_placement": placed["missing_occurrence_map"],
        "lambda_values": identity["dual_values"],
        "old_unary_plus_placed_return_is_full_target": True,
        "first_remaining_main_row":
            "word-resolved labelled ordinary residue -E",
        "scope": "one normalized nonzero root/label component",
    }


def audit_residue_identification() -> dict[str, object]:
    dressing = load(
        "computations/verify_h3_cplus_conditional_physical_dressing_assembly.py",
        "residue_id_dressing",
    )
    dressing.pin_inputs()
    dressing_ledger, dressing_digest = dressing.audit()
    require(dressing_digest == dressing.EXPECTED_LEDGER_SHA256,
            "conditional Cplus dressing changed")
    core = dressing_ledger["core_assembly"]

    d_root = tuple(map(Q, (-1, 1, -1, 1)))
    d_even = tuple(map(Q, (0, Q(1, 2), 0, 0, Q(1, 2), 0)))
    e = tuple(2 * root * label for root in d_root for label in d_even)
    minus_e = scale(Q(-1), e)
    require(len(e) == 24 and set(e) == {Q(-1), Q(0), Q(1)}
            and sum(value != 0 for value in e) == 8,
            "root-decorated d_even packet changed")
    require(add(minus_e, e) == (Q(0),) * 24,
            "root-decorated d_even stopped cancelling -E")

    # Forgetting the four root words makes -E dark because sum D_root=0.
    coarse = tuple(sum((minus_e[6 * root + label]
                        for root in range(4)), Q(0))
                   for label in range(6))
    require(coarse == (Q(0),) * 6,
            "word-resolved residue stopped being coarse-dark")
    require(core["clean_K_Eq_factorization"] ==
                "P2_hidden(-E,0,0)+O_-E(E,E,-E)+"
                "2D_root*d_even(0,0,E)=(0,E,0)"
            and core["assembled_core"]["word_resolved_root_ores_debt"] == 0,
            ("committed root-residue cancellation changed", core))

    # Keep three honest residue summands: 24 root-word labels, six unrooted
    # B-labels, and one scalar cap residue.  They must not be identified.
    zero24 = (Q(0),) * 24
    zero6 = (Q(0),) * 6
    residual = minus_e + zero6 + (Q(0),)
    rooted_d_even = e + zero6 + (Q(0),)
    unrooted_d_even = zero24 + d_even + (Q(0),)
    z_cap = zero24 + zero6 + (Q(1),)
    require(add(residual, rooted_d_even) == (Q(0),) * 31,
            "rooted d_even failed in separated residue module")
    require(add(residual, unrooted_d_even) != (Q(0),) * 31
            and add(residual, z_cap) != (Q(0),) * 31,
            "an unrelated residue block cancelled -E")
    require(rank((rooted_d_even, unrooted_d_even, z_cap)) == 3,
            "the three residue sectors stopped being independent")

    scalar_cap_dual = (Q(0),) * 30 + (Q(1),)
    fixed_label_dual = (Q(0),) * 24 + tuple(
        map(Q, (0, 1, -1, 0, 1, -1))) + (Q(0),)
    require(dot(scalar_cap_dual, residual) == 0
            and dot(scalar_cap_dual, rooted_d_even) == 0
            and dot(scalar_cap_dual, unrooted_d_even) == 0
            and dot(scalar_cap_dual, z_cap) == 1,
            "z_cap scalar dual changed")
    require(dot(fixed_label_dual, residual) == 0
            and dot(fixed_label_dual, rooted_d_even) == 0
            and dot(fixed_label_dual, unrooted_d_even) == 1
            and dot(fixed_label_dual, z_cap) == 0,
            "unrooted d_even dual changed")

    return {
        "definitions": {
            "D_root": [str(value) for value in d_root],
            "d_even_B0_to_B5": [str(value) for value in d_even],
            "E": "2 D_root tensor d_even",
            "nonzero_root_word_coordinates": 8,
        },
        "exact_residue": "-E=-2 D_root tensor d_even",
        "cancelling_section": "+2 D_root tensor d_even",
        "coarse_six_label_shadow_of_minus_E": [0, 0, 0, 0, 0, 0],
        "new_coefficient_direction_beyond_d_even": False,
        "root_decoration_required": True,
        "residue_sector_rank": {
            "root_decorated_d_even_unrooted_d_even_zcap": 3,
            "zcap_cancels_minus_E": False,
            "unrooted_d_even_without_root_decoration_cancels_minus_E": False,
        },
    }


def audit_source_scope() -> dict[str, object]:
    root_gate = load(
        "computations/verify_h3_cplus_root_even_labelled_ores_sigma_cartan_gate.py",
        "residue_id_root_gate",
    )
    root_gate.pin_inputs()
    root_ledger = root_gate.audit()
    root_relation = root_ledger["relation_to_denominator_Tor"]
    require(root_relation["current_root_even_weakest_gate"] ==
                "one physical membership for d_even with ores=(B1+B4)/2 "
                "and all lower/Eq/W/target/ainc/terminal rows zero"
            and root_ledger["sharp_frontier"].startswith(
                "construct one same-grade sigma-covariant d_even section"),
            ("d_even source scope changed", root_ledger))

    cap = load(
        "computations/verify_h3_augp2_primitive_cap_response_keq_reduction_gate.py",
        "residue_id_cap",
    )
    cap_ledger, cap_digest = cap.audit()
    require(cap_digest == cap.EXPECTED_LEDGER_SHA256,
            "z_cap reduction changed")
    cap_face = cap_ledger["expanded_face_independence"]
    require(cap_face["separating_covector"] ==
                "scalar cap-ores coordinate"
            and cap_face["d_even_has_scalar_cap_ores"] == 0,
            ("z_cap/d_even separation changed", cap_face))

    p2 = load(
        "computations/verify_h3_p2_labelled_ores_cut_even_deven_gauge_gate.py",
        "residue_id_p2",
    )
    p2_ledger, p2_digest = p2.audit()
    require(p2_digest == p2.EXPECTED_LEDGER_SHA256,
            "P2 d_even gauge changed")
    hypotheses = p2_ledger["conditional_closure"]["hypotheses"]
    require(any("pure protected-zero d_even" in item for item in hypotheses),
            ("P2 d_even stopped being a conditional input", hypotheses))

    return {
        "coefficient_verdict": (
            "the remaining -E is exactly a connected-root decoration of "
            "d_even, hence not a fourth residue source type"
        ),
        "physical_verdict": (
            "closure is conditional on one same-grade pure d_even section "
            "stable under the connected root decoration; this section is "
            "not constructed by Cartan parity or by the coefficient identity"
        ),
        "z_cap": (
            "independent scalar ordinary residue in the cap word/grade; it "
            "remains necessary for primitive-cap landing but has zero value "
            "on all 24 root-word residue coordinates"
        ),
        "new_direction_if_d_even_granted": False,
        "new_direction_in_current_unconditional_image": (
            "the primitive root-word d_even dual survives until the physical "
            "same-grade section and decoration map are supplied"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "E14 K_Eq private-placement residue identification gate",
        "pins": PINS,
        "conditional_E14_companion": audit_conditional_companion(),
        "word_residue_identification": audit_residue_identification(),
        "source_scope": audit_source_scope(),
        "verdict": (
            "Conditional on H0-u -> 1-v04 and e_Eq -> endpoint*u35*v24, "
            "the exact identity B_E14=U+R makes the old unary U plus the "
            "placed private return equal the full E14 target.  The sole "
            "remaining main residue is -E=-2D_root tensor d_even.  It is "
            "cancelled exactly by the same-grade root decoration of d_even, "
            "so it is not a new coefficient direction.  This remains a "
            "physical hypothesis because the pure d_even section and its "
            "decoration are not constructed.  z_cap is a distinct scalar "
            "cap-residue coordinate and cannot cancel -E."
        ),
        "scope": (
            "Canonical h=3 word-000101 E14 first-hit packet and the eight "
            "nonzero root/label components of the generic Cplus dressing.  "
            "The occurrence placement, pure d_even source section, connected "
            "root decoration, z_cap placement, and terminal rows remain "
            "hypotheses where indicated."
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("E14 residue-identification ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("placed private return + old unary = full E14 target: YES")
    print("remaining word residue: -E=-2 D_root tensor d_even")
    print("root-decorated d_even cancels it: YES, CONDITIONALLY PHYSICAL")
    print("z_cap cancels it: NO (independent scalar cap-residue block)")
    print("new residue source type after d_even grant: NO")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
