#!/usr/bin/env python3
"""Separate the E14 companion obstruction from cap residue and eta repair.

The canonical E14 first-hit dual pairs with exactly one target monomial,

    (p1_0_1*s1_1_1) u05_01*v13_01*v24_11,

and ignores the promoted decorated core containing u05_01*v34_10.  After the
physical K_Eq lift is added to the primitive cap, the remaining class z_cap
has Q=0 and only scalar cap ordinary residue.  The proposed Omega/rootless
eta mate is a protected terminal readout.  Neither therefore has a principal
coordinate in the word-000101 unary/G11 module.

Even granting z_cap and the eta mate as independent physical columns, the
E14 first-hit class remains a direct-summand rank-one obstruction.  When q13
is killed, its representative moves to one target-normal residual vector
supported on nine coordinates (eight after q04 is killed too).  A unified
landing cell must carry this target-normal face in addition to cap residue;
the cap/eta repair alone cannot do so.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_e14_companion_target_normal_specialization_gate.py":
        "310b2f0b6263d0cb41d82050159ee0ae3a68ea4c1c829025dfe0edd9777890f9",
    "notes/h3-e14-companion-target-normal-specialization-gate.md":
        "1e3212ec37de0cbae51cac83f6e109c8dbecbf00c3473c0a9b9fca8bb087cc2d",
    "computations/verify_h3_augp2_primitive_cap_response_keq_reduction_gate.py":
        "4dabdae7b9060bdb92c0ed32b0016e7e2694750dc176e1857cc9a54cb8176587",
    "notes/h3-augp2-primitive-cap-response-keq-reduction-gate.md":
        "1f8e8a4a5ffc26a8fdcefcb970c3bc35887a1d521ca27ce3173a790b82dfba5d",
    "computations/verify_h3_rootless_e14_companion_core_identification.py":
        "438ae827dba9e8f7a14f011cb5d76631fc284a2a2a8c6d8bcee7003669a1ac45",
    "computations/verify_h3_relative_occurrence_e14_w_carrier_landing_gate.py":
        "37f571234346c8a90465a5e021bb5ed97b0caec68e31a8b80346d25f94c9f337",
    "computations/verify_h3_rootless_clean_separator_repeated_inventory_gate.py":
        "af9a69ad996bd4390ff3fe9139e357a3bb765292ec969350a948612d9b824fa7",
}
EXPECTED_LEDGER_SHA256 = "4844f563352246a30ce9691045bedbed5e95270a2af2bb1864b91c98cd2db72f"


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


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def canonical_and_specialized_audit() -> dict[str, object]:
    special = load(
        "computations/verify_h3_e14_companion_target_normal_specialization_gate.py",
        "cap_eta_e14_special",
    )
    ledger, digest = special.audit()
    require(digest == special.EXPECTED_LEDGER_SHA256,
            "the E14 specialization ledger changed")
    canonical = ledger["canonical_first_hit"]
    silent = ledger["silent_chord_specializations"]
    require(canonical["unique_detected_coordinate"] == [
                ["p1_0_1", "s1_1_1"],
                ["u05_01", "v1301", "v2411"],
            ]
            and canonical["target_coefficient"] == "-1"
            and canonical["dual_coefficient"] == "1"
            and canonical["promoted_dual_coefficient"] == "0",
            "the companion/core dual concentration changed")
    q13 = silent["q13_zero"]
    q0413 = silent["q04_q13_zero"]
    require((q13["rank_Q"], q13["specialized_target_support"],
             q13["reduced_support"]) == (211, 9, 9)
            and (q0413["rank_Q"], q0413["specialized_target_support"],
                 q0413["reduced_support"]) == (185, 8, 8)
            and q13["all_reduced_coordinates_are_unary_target_normal"]
            and q0413["all_reduced_coordinates_are_unary_target_normal"],
            "the silent target-normal residual changed")
    return {
        "canonical_word": "000101",
        "old_columns_rank": [269, 269],
        "target_raises_rank_to": 270,
        "dual_support": 22,
        "unique_dual_visible_target": canonical["unique_detected_coordinate"],
        "visible_target_coefficient_times_dual": "(-1)*(+1)=-1",
        "visible_site_profile": canonical["detected_site_profile"],
        "promoted_decorated_core":
            canonical["promoted_decorated_core_coordinate"],
        "promoted_decorated_core_dual_value": "0",
        "promoted_site_profile": canonical["promoted_site_profile"],
        "q13_zero": {
            "old_rank_then_target_rank": [211, 212],
            "target_normal_residual_support": 9,
        },
        "q04_q13_zero": {
            "old_rank_then_target_rank": [185, 186],
            "target_normal_residual_support": 8,
        },
    }


def cap_and_eta_typing_audit() -> dict[str, object]:
    cap = load(
        "computations/verify_h3_augp2_primitive_cap_response_keq_reduction_gate.py",
        "cap_eta_cap",
    )
    cap_ledger, cap_digest = cap.audit()
    require(cap_digest == cap.EXPECTED_LEDGER_SHA256,
            "the primitive cap reduction ledger changed")
    aggregate = cap_ledger["aggregate_cap_quotient"]
    terminal = cap_ledger["terminal_extension"]
    require(aggregate["identity"] == "p_y=z_cap-n_y"
            and aggregate["pure_cap_residue_z_cap_equals_p_plus_n"]
            == ["0", "0", "0", "0", "0", "-1"]
            and not terminal[
                "normalized_local_dual_extends_with_current_terminal_rows"],
            "the cap/eta reduction changed")

    core = load(
        "computations/verify_h3_rootless_e14_companion_core_identification.py",
        "cap_eta_core",
    )
    core_ledger, core_digest = core.audit()
    require(core_digest == core.EXPECTED_LEDGER_SHA256,
            "the rootless/E14 core ledger changed")
    require(core_ledger["mapped_decorated_2K2_core"]
            == ["u05_01", "v3410"],
            "the mapped decorated core changed")

    # The crucial loss: z_cap is what remains *after* n_y cancels the full Q
    # aggregate.  Hence it has no Q/core coefficient.  The eta mate is a
    # proposed protected terminal readout, not an E14 unary/G11 boundary.
    return {
        "cap_source_word": "01211222",
        "cap_fine_repeated_grade": "t*q_(v,N), P3+K2",
        "p_before_K_Eq": "(-Q_y,-ores_cap)",
        "physical_K_Eq_n": "(+Q_y,0)",
        "z_cap_after_K_Eq": "(Q=0, scalar ores_cap=-1)",
        "z_cap_contains_decorated_2K2_core": False,
        "reason": "the entire Q_y coordinate cancels in p+n",
        "Omega_rootless_eta_mate_type": (
            "protected ridge/terminal comparison with eta_z readout "
            "+(5+u_z/t), target=ores=ainc=0"
        ),
        "eta_mate_is_E14_principal_column": False,
        "known_mapped_Q_core": core_ledger["mapped_decorated_2K2_core"],
        "known_mapped_Q_core_is_dual_visible_companion": False,
        "full_word_grade_identification_constructed": False,
    }


def direct_sum_rank_audit() -> dict[str, object]:
    # Quotient the old E14 module by its 269-column image.  Retain only the
    # one target class detected by lambda_22, scalar cap residue, and the
    # independent Omega/rootless eta-terminal row.  The strongest grant of
    # z_cap and eta mate gives two coordinate columns but no E14 component.
    # Hence the E14 target still raises rank by one.
    z_cap = (Q(0), Q(1), Q(0))
    eta_mate = (Q(0), Q(0), Q(1))
    e14_target = (Q(1), Q(0), Q(0))
    lambda_e14 = (Q(1), Q(0), Q(0))
    candidates = (z_cap, eta_mate)
    require(rank(candidates) == 2
            and rank(candidates + (e14_target,)) == 3
            and all(dot(lambda_e14, column) == 0 for column in candidates)
            and dot(lambda_e14, e14_target) == 1,
            "cap residue/eta unexpectedly filled the E14 quotient")

    # Restoring the old 269-dimensional image gives the literal rank jump.
    return {
        "quotient_basis": [
            "E14 first-hit class", "scalar cap ores", "Omega/r eta terminal",
        ],
        "z_cap": [0, 1, 0],
        "eta_mate": [0, 0, 1],
        "E14_target": [1, 0, 0],
        "quotient_rank_before_after_target": [2, 3],
        "literal_rank_before_after_target_after_strong_grant": [271, 272],
        "surviving_covector": [1, 0, 0],
        "interpretation": (
            "even an independent physical cap-residue cell and a perfect "
            "eta-compatible Omega/rootless mate do not touch the E14 "
            "principal quotient until a word-changing boundary couples them"
        ),
    }


def shortest_mixed_cell_and_terminal_audit() -> dict[str, object]:
    return {
        "smallest_positive_cell": (
            "one endpoint-word-changing augmented P2/E14 cell whose "
            "principal boundary has nonzero lambda_22 value (generically "
            "the u05_01*v13_01*v24_11 companion class), whose cap face is "
            "z_cap, and whose proper target face is the unary target-normal "
            "residual"
        ),
        "generic_required_principal_coordinate": (
            "(p1_0_1*s1_1_1)u05_01*v13_01*v24_11 or another boundary "
            "with the same nonzero 22-support dual value"
        ),
        "silent_branch_required_target_mate": (
            "the one residual unary target-normal class supported on nine "
            "coordinates at q13=0 (eight at q04=q13=0)"
        ),
        "cap_terminal_mate": (
            "Omega/rootless eta-compatible readout +(5+u_z/t); necessary "
            "to promote scalar cap ores, but independent of the E14 class"
        ),
        "E14_terminal_seed": (
            "the 22-support first-hit covector, specializing to the target-"
            "normal residual functional on the silent branch"
        ),
        "full_terminal_not_yet_constructed": True,
        "finite_alternative": (
            "in the complete augmented same-grade map, either the mixed "
            "principal/cap/target-normal vector is in the image, or a left "
            "covector extending both the E14 target-normal seed and the "
            "cap/Omega terminal equations is the physical Fredholm arm"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": "E14 companion / cap-residue / eta-mate separation gate",
        "pins": PINS,
        "canonical_and_silent_E14": canonical_and_specialized_audit(),
        "cap_and_eta_typing": cap_and_eta_typing_audit(),
        "direct_sum_rank_obstruction": direct_sum_rank_audit(),
        "shortest_mixed_cell_or_terminal":
            shortest_mixed_cell_and_terminal_audit(),
        "verdict": (
            "The cap-residue class z_cap and Omega/rootless eta mate do not "
            "supply the dual-visible E14 companion.  z_cap has Q=0 after "
            "K_Eq, and the eta mate is a protected readout rather than a "
            "word-000101 principal boundary.  Even granting both leaves the "
            "E14 target as a new rank-one class.  The next cell must couple "
            "principal companion, scalar cap residue, and the target-normal "
            "proper face; failure must extend two independent terminal "
            "seeds, the cap/Omega eta functional and the E14 target-normal "
            "functional."
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("E14/cap/eta separation ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("z_cap E14 companion content: ZERO (Q cancels after K_Eq)")
    print("Omega/rootless eta mate: TERMINAL READOUT, NOT E14 PRINCIPAL")
    print("strong-grant rank: 271 -> 272 after E14 target")
    print("silent target-normal debt: 9 coordinates; q04=q13: 8")
    print("next: one mixed companion/cap/target-normal cell or full dual")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
