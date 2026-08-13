#!/usr/bin/env python3
"""Correct the selected cut-cycle line-lift and physical-anchor scope.

The selected collision vector

    ell = u_024-u_012

has zero coefficients on the three shared repeated-02 labels, so it needs
only one comparison equation rather than a map on all U15.  That reduction
does not prove the equation.  The actual remaining chain condition is

    J_3(M_v) = A J_col(ell).

The pinned one-chain audit gives a hidden-row counterguard: the occurrence
collapse and the complete output census do not determine this equality.
Consequently there is not yet a completed physical selected cycle on which
h_phys can be evaluated.

Conditionally on the equality, M_v has zero physical anchor-incidence, so
h_phys on the completed cycle is exactly its top-grade value.  The ordinary
occurrence marker has value one there, but is an independent covector.  The
smallest remaining anchor law is therefore the single noncollapse scalar

    h_top(A(P_024-P_012)) != 0,

after (and only after) the one-chain equality has been proved.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_selected_lower_one_chain_comparison_reduction.py":
        "c9fc8c847327d0e119264a3a83cf39d0f4c2ff45b4ddd4e048f42a57cac0e887",
    "computations/verify_h3_filtered_common_tail_marked_kernel_lift.py":
        "d7cc4cdbee64cd33f9c351b4ef4fdab8e81dfacc099ce5d917bbdf9c3da1b2d2",
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
    "computations/verify_frame_circuit_complete_source_kernel_lift_gate.py":
        "81738d71a423635da70caf7f3d46ca334cb0ebee7cd8240a0b7a7410c386f76c",
}
EXPECTED_LEDGER_SHA256 = (
    "a40a8a9ffe3f4aadafc82ee7245186a56a32fbb3aa434fde1c34c0a26964ec1a"
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    # Replay the exact hidden-row counterguard pinned in 6fd2412 without
    # rerunning its expensive full physical census.  The first fifteen rows
    # are the disclosed occurrence projection.  The two complete boundary
    # maps agree there and differ only on one hidden/private row detected by
    # the selected lower vector.
    selected_lower = tuple(map(Q, (
        -1, 0, -1, 0, 0, 0, -1, 0, 1, 0, 1, 1, -1, 1, 0,
    )))
    occurrence_rows = tuple(
        tuple(Q(int(row == column)) for column in range(15))
        for row in range(15)
    )
    hidden_zero = (Q(0),) * 15
    detecting_index = next(index for index, value in enumerate(selected_lower)
                           if value == 1)
    hidden_private = tuple(Q(int(index == detecting_index))
                           for index in range(15))
    occurrence_good = tuple(dot(row, selected_lower)
                            for row in occurrence_rows + (hidden_zero,))
    occurrence_bad = tuple(dot(row, selected_lower)
                           for row in occurrence_rows + (hidden_private,))
    require(occurrence_good[:-1] == occurrence_bad[:-1] == selected_lower
            and occurrence_good[-1] == 0
            and occurrence_bad[-1] == 1,
            "the hidden full-row obstruction changed")

    # Once the chain equality is granted, the anchor evaluation is just the
    # sum of its top and correction values.  M_v contributes zero, so the
    # physical question is one top scalar.  The occurrence marker does not
    # determine that scalar: two physical-anchor extensions agree on the
    # correction and every unrelated coordinate, but read 0 and 1 on top.
    # This is only an independence guard, not an assertion that either row
    # has already been realized by the complete physical source packet.
    completed_formal_cycle = (Q(1), Q(1), Q(0))
    occurrence_marker = (Q(1), Q(0), Q(0))
    anchor_dark = (Q(0), Q(0), Q(1))
    anchor_bright = (Q(1), Q(0), Q(1))
    require(dot(occurrence_marker, completed_formal_cycle) == 1
            and dot(anchor_dark, completed_formal_cycle) == 0
            and dot(anchor_bright, completed_formal_cycle) == 1
            and anchor_dark[1] == anchor_bright[1] == 0,
            "the conditional top-anchor independence guard changed")

    ledger = {
        "theorem": "selected cut-cycle line lift and anchor scope correction",
        "pins": PINS,
        "withdrawn_claim": {
            "old_statement": (
                "the twelve-label occurrence collapse and M_v output census "
                "already define an actual chain map on C_sel"
            ),
            "status": "false/not established by the pinned data",
            "reason": (
                "the input audit exposes only the occurrence/collapse "
                "projection of J_col(l); a hidden physical row can change "
                "its value while all disclosed data stay fixed"
            ),
        },
        "exact_selected_frontier": {
            "selected_lower": "l=u_024-u_012",
            "shared_repeated_02_coefficients": ["0", "0", "0"],
            "full_U15_map_needed_locally": False,
            "candidate": "M_v=-O_alpha+K",
            "unproved_equation": "J_3(M_v)=A J_col(l)",
            "hidden_row_values_with_same_occurrence_data": [
                str(occurrence_good[-1]), str(occurrence_bad[-1]),
            ],
            "completed_physical_cycle_exists": False,
        },
        "physical_anchor_status": {
            "current_value_on_completed_cycle": "undefined",
            "why": (
                "the purported completed cycle depends first on the open "
                "full-row equality J_3(M_v)=A J_col(l)"
            ),
            "ordinary_occurrence_marker_value": 1,
            "occurrence_marker_is_h_phys": False,
            "M_v_anchor_incidence": 0,
            "conditional_formula": (
                "if J_3(M_v)=A J_col(l), then "
                "h_phys((A(P_024-P_012),M_v))="
                "h_top(A(P_024-P_012))"
            ),
            "smallest_anchor_comparison": (
                "h_top(A(P_024-P_012)) != 0 in the exact selected "
                "word/fine/repeated physical source grade"
            ),
            "dark_and_bright_extensions_consistent_with_known_data": True,
        },
        "shortest_order_of_proof": [
            "expose the complete protected/source-labelled J_col(l) row",
            "prove the single equality J_3(M_v)=A J_col(l)",
            "evaluate the one physical top-anchor scalar; M_v adds zero",
            "if nonzero, invoke the rectangular marked landing",
        ],
        "scope": (
            "correction of de74a1a.  It neither constructs the missing "
            "one-chain equality nor assigns a physical anchor value to an "
            "uncompleted cycle"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("selected cut-cycle corrected ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 selected cut cycle: PREVIOUS LINE-LIFT CLAIM WITHDRAWN")
    print("first open row: J3(M_v)=A Jcol(l)")
    print("completed physical selected cycle: NOT YET CONSTRUCTED")
    print("h_phys on completed cycle: UNDEFINED")
    print("conditional lower correction ainc: 0")
    print("conditional remaining anchor scalar: h_top(A(P024-P012))")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
