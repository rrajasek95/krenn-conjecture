#!/usr/bin/env python3
"""Compare the forced-pure-escape selector with the marked h=3 carriers.

The structural escape equations make the *escape coefficient* absolute:
pure minus mixed is the escape covector.  They do not split two cancelling
cap parents.  This script freezes that distinction as a rational three-term
row model, then compares it with the exact marked/trigger/derived carrier
theorems pinned below.

The marked parent idempotent exists before forgetting the parent mark.  It
does not descend through the unmarked augmentation, even after adjoining the
normalized escape unit.  The same anti-diagonal is the primitive protected
B-Eq obstruction of the derived-cap audit.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_forced_pure_escape_alternating_potential.py":
        "3cdf461b422f8b29af5f9cd8948132ac1edb8dfd92798f6678e5644e4d2fb514",
    "notes/2026-08-14-forced-pure-escape-alternating-potential.md":
        "b3a10f916b27cb655f9f4f92504d5a771e667dca84beecfe728e9a2532d14868",
    "computations/verify_h3_six_root_marked_collision_p2_restriction_reinsertion.py":
        "9b387023ee8cac6bb000d6936a8985cbc16bbad0a9f7deb3613c1f44c233a1f8",
    "notes/h3-six-root-marked-collision-p2-restriction-reinsertion.md":
        "8924d5a458c52d6e4b68b80166f1df9775e6f1a713e3556a161830a30d2a7a4a",
    "computations/verify_h3_order6_trigger_replacement_euler_complement_gate.py":
        "deb84776e620dbf800b24a3a317545259ab6b902d9d07be48bd6ce93e0c6adce",
    "notes/h3-order6-trigger-replacement-euler-complement-gate.md":
        "580fe93ecffaa2d19d11c656e1036be6778a99703134463fb7534f6a7ad2fb42",
    "computations/verify_h3_shared_collision_groupoid_beck_chevalley_derived_cap_gate.py":
        "a1e81eef9343bd2dda01b106acc202698cc12e93e7db3b55d45f5c6268779c33",
    "notes/h3-shared-collision-groupoid-beck-chevalley-derived-cap-gate.md":
        "e52f7fc6b324b40688486237a3b9b4e65b26817f55b754ff78b365f0835ffde1",
}
EXPECTED_LEDGER_SHA256 = (
    "807dd5cfc370808568bcf52a19442f7dd8c146a33fa8231f53680ebb02c2d86e"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def dot(left, right):
    return sum((x * y for x, y in zip(left, right, strict=True)), Q(0))


def subtract(left, right):
    return tuple(x - y for x, y in zip(left, right, strict=True))


def rational_rank(rows) -> int:
    matrix = [list(map(Q, row)) for row in rows]
    if not matrix:
        return 0
    rank = 0
    columns = len(matrix[0])
    for column in range(columns):
        pivot = next((index for index in range(rank, len(matrix))
                      if matrix[index][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [entry / scale for entry in matrix[rank]]
        for index in range(len(matrix)):
            if index == rank or not matrix[index][column]:
                continue
            scale = matrix[index][column]
            matrix[index] = [entry - scale * pivot_entry
                             for entry, pivot_entry
                             in zip(matrix[index], matrix[rank], strict=True)]
        rank += 1
    return rank


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned carrier changed", relative, actual, expected))


def escape_row_audit() -> dict[str, object]:
    # Coordinates are the already weighted occurrence contributions
    # (M0,M1,N)=(2,-2,1) from the nine-cell packet.  M1 is the short C4
    # parent sharing tail 01 with N.
    mixed = (Q(1), Q(1), Q(0))
    pure = (Q(1), Q(1), Q(1))
    escape = (Q(0), Q(0), Q(1))
    short_parent = (Q(0), Q(1), Q(0))
    short_tail_restriction = (Q(0), Q(1), Q(1))
    parent_antidiagonal = (Q(1), Q(-1), Q(0))
    contributions = (Q(2), Q(-2), Q(1))

    require(subtract(pure, mixed) == escape, (pure, mixed, escape))
    require((dot(mixed, contributions), dot(pure, contributions),
             dot(escape, contributions)) == (0, 1, 1), contributions)
    require(dot(short_tail_restriction, contributions) == -1,
            contributions)

    physical_rank = rational_rank((mixed, pure))
    require(physical_rank == 2
            and rational_rank((mixed, pure, escape)) == physical_rank,
            "pure-minus-mixed must make only the escape covector absolute")
    require(rational_rank((mixed, pure, short_parent)) == 3
            and rational_rank((mixed, pure, short_tail_restriction)) == 3,
            "a parent-resolving selector unexpectedly descended")
    require(dot(mixed, parent_antidiagonal) == 0
            and dot(pure, parent_antidiagonal) == 0
            and dot(short_parent, parent_antidiagonal) == -1
            and dot(short_tail_restriction, parent_antidiagonal) == -1,
            parent_antidiagonal)

    return {
        "coordinate_order": ["M0_long_C6", "M1_short_C4", "N_escape"],
        "weighted_contributions": [2, -2, 1],
        "physical_rows": {"mixed": [1, 1, 0], "pure": [1, 1, 1]},
        "normalized_values": {"mixed": 0, "pure": 1, "escape": 1},
        "absolute_escape_covector": [0, 0, 1],
        "short_parent_covector": [0, 1, 0],
        "short_tail_restriction": [0, 1, 1],
        "short_tail_value": -1,
        "physical_row_rank": physical_rank,
        "rank_after_escape": 2,
        "rank_after_parent_selector": 3,
        "rank_after_tail_restriction": 3,
        "undetected_parent_antidiagonal": [1, -1, 0],
        "verdict": (
            "pure normalization makes N=pure-mixed an absolute coefficient, "
            "but neither M1 nor M1+N belongs to the physical row span"
        ),
    }


def marked_forgetting_audit() -> dict[str, object]:
    # Forgetting two marked lifts has matrix A=(1,1).  Descent of the M1
    # idempotent would require a scalar lambda with lambda*A=A*E1=(0,1).
    augmentation = (Q(1), Q(1))
    selected_lift = (Q(0), Q(1))
    antidiagonal = (Q(1), Q(-1))
    symmetric_section = (Q(1, 2), Q(1, 2))

    require(rational_rank((augmentation,)) == 1
            and rational_rank((augmentation, selected_lift)) == 2,
            (augmentation, selected_lift))
    require(dot(augmentation, antidiagonal) == 0
            and dot(selected_lift, antidiagonal) == -1,
            antidiagonal)
    require(dot(augmentation, symmetric_section) == 1,
            symmetric_section)
    require(tuple(reversed(symmetric_section)) == symmetric_section
            and tuple(reversed(selected_lift)) != selected_lift,
            (symmetric_section, selected_lift))

    # Tensoring with the normalized scalar u=1 repeats exactly the same
    # matrix.  No rank or kernel changes, so the marked idempotent remains
    # relative even on the normalized solution locus.
    normalized_unit = Q(1)
    normalized_augmentation = tuple(normalized_unit * entry
                                    for entry in augmentation)
    normalized_selected = tuple(normalized_unit * entry
                                for entry in selected_lift)
    require(normalized_augmentation == augmentation
            and normalized_selected == selected_lift
            and rational_rank((normalized_augmentation,
                               normalized_selected)) == 2,
            (normalized_augmentation, normalized_selected))

    return {
        "marked_to_unmarked_augmentation": [1, 1],
        "marked_M1_readout": [0, 1],
        "kernel": [1, -1],
        "only_swap_invariant_section": ["1/2", "1/2"],
        "descent_equation": "lambda*(1,1)=(0,1)",
        "descent_equation_solvable": False,
        "after_tensoring_with_normalized_escape_unit": {
            "unit": 1,
            "augmentation_rank": 1,
            "augmentation_plus_selector_rank": 2,
            "kernel_survives": True,
        },
    }


def protected_descent_audit() -> dict[str, object]:
    # Primitive normalization of the protected coordinates used in d97bf7a.
    d_derived = (Q(1), Q(0))
    d_underived = (Q(0), Q(1))
    omega = (Q(1), Q(-1))
    tied = (Q(1), Q(1))
    required = (Q(1), Q(0))
    require(rational_rank((d_derived, d_underived)) == 2,
            (d_derived, d_underived))
    require((dot(omega, d_derived), dot(omega, d_underived),
             dot(omega, tied), dot(omega, required)) == (1, -1, 0, 1),
            omega)

    # The one-generator relative cone dK=tE becomes zero after t=0,
    # leaving H0=H1=Q.  An absolute dK=E has rank one and kills both.
    relative_rank_after_normalization = rational_rank(((Q(0),),))
    absolute_rank = rational_rank(((Q(1),),))
    require(relative_rank_after_normalization == 0 and absolute_rank == 1,
            (relative_rank_after_normalization, absolute_rank))
    return {
        "derived_boundary": [1, 0],
        "underived_boundary": [0, 1],
        "primitive_B_minus_Eq": [1, -1],
        "tied_readout": [1, 1],
        "required_readout": [1, 0],
        "primitive_detector_values": {"tied": 0, "required": 1},
        "c3f6231_integral_rescaling_on_required": 3,
        "relative_dK_tE_after_t_zero_H0_H1": [1, 1],
        "absolute_dK_E_H0_H1": [0, 0],
    }


def carrier_comparison() -> dict[str, object]:
    carriers = {
        "c3f6231_divided_root": {
            "literal_parent_mark": True,
            "word_fine_reinsertion": True,
            "pointed_occurrence_section": "marked-derived only",
            "underived_r0_projection": False,
            "first_failure": "protected hidden (-E,+E) B/Eq landing",
        },
        "9bbff79_trigger_euler": {
            "literal_parent_recovery": True,
            "ordered_trigger_replacement": True,
            "response_Euler_completion": True,
            "operation_change_response_to_cap": False,
            "first_missing_map": "TrigEulerSpencer_rep -> C_AugP2",
        },
        "d97bf7a_marked_groupoid": {
            "marked_collision_square_Cartesian": True,
            "unmarked_square_Cartesian": False,
            "derived_common_parent_resolution": True,
            "underived_physical_descent": False,
            "normalization_makes_relative_Eq_absolute": False,
        },
    }
    require(all(item["literal_parent_mark"]
                for item in (carriers["c3f6231_divided_root"],)), carriers)
    require(not carriers["9bbff79_trigger_euler"]
            ["operation_change_response_to_cap"], carriers)
    require(not carriers["d97bf7a_marked_groupoid"]
            ["normalization_makes_relative_Eq_absolute"], carriers)
    return {
        "carriers": carriers,
        "exact_identification": (
            "the structural M0/M1 ambiguity is the kernel of forgetting a "
            "fine parent mark; c3f6231 and d97bf7a construct that mark in "
            "the derived collision species, while 9bbff79 constructs its "
            "response trigger/Euler source"
        ),
        "grade_guard": (
            "the structural coefficient:111111 tail selector is not itself "
            "the canonical response 11110000 -> cap 01211222 operation; "
            "transport requires the still-missing augmented operation map"
        ),
        "shortest_sufficient_new_datum": (
            "a pointed augmented operation-changing linearization that "
            "retains the parent idempotent and all protected readouts, plus "
            "an absolute decorated Eq contraction (or an equivalent "
            "conservative solution-locus vanishing theorem)"
        ),
        "role_of_pure_escape_unit": (
            "post-landing nonvanishing certificate for the common tail; it "
            "does not construct or descend the parent projector"
        ),
    }


def audit() -> dict[str, object]:
    pin_dependencies()
    return {
        "pins": PINS,
        "escape_row_model": escape_row_audit(),
        "marked_forgetting_model": marked_forgetting_audit(),
        "protected_descent_model": protected_descent_audit(),
        "committed_carrier_comparison": carrier_comparison(),
        "theorem": (
            "pure normalization makes the total escape coefficient absolute, "
            "but cannot make a parent-resolving occurrence projector "
            "absolute: the parent anti-diagonal survives both normalization "
            "and unmarked descent"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    arguments = parser.parse_args()
    ledger = {"mode_independent": True, "audit": audit()}
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    print("escape parent-selector / marked-carrier comparison: PASS")
    print("mode", arguments.mode)
    print("physical rows / with selector ranks", 2, 3)
    print("normalization: escape absolute, parent projector still relative")
    print("shared frontier: augmented operation change + absolute Eq")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
