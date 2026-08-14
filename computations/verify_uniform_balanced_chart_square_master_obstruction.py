#!/usr/bin/env python3
"""Identify the common balanced-square obstruction at the proof frontier.

This checker is deliberately a representation/typing reduction, not a
physical construction.  It verifies that three independently obtained
frontier classes are the same four-coordinate character:

* the ordered lift of the h=3 Gate-II charge (2,-1,-1);
* the centered K2,2 complete-row projection obstruction; and
* chart-sign tensor matching-constant in the two-chart operation module.

It also freezes the exact rank-one filler/dual alternative.  A physical
theorem must still place this character with one fixed word, C4 window,
tail, repeated/Hasse grade, and every augmented readout.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_gate_ii_switch_weyl_product_rule_idempotent_gate.py":
        "fbd4815eb5c6d46b8dbcd018f6e75237f004e3f52b1ccf47631479b698f9db35",
    "notes/h3-gate-ii-switch-weyl-product-rule-idempotent-gate.md":
        "432a612161538958c069de828b1f0f0a3321e5bdaa758be104942140df768b7d",
    "computations/verify_uniform_recurrent_core_complete_row_projection_boundary.py":
        "3dc0ee0a0fbb7f0c1c1ea779bd6f3ee54114fece4f00a70877df8b2904cada2d",
    "notes/uniform-recurrent-core-complete-row-projection-boundary.md":
        "5305846b4377fba058725da7b40733522fed31d50ff78010e8b0763e24e80347",
    "computations/verify_uniform_chart_odd_matching_exchange_operation_tag_tor_gate.py":
        "a835e816347b15f8c88c7f9995374468cd421cd68a64650bda128eda75ae8f39",
    "notes/uniform-chart-odd-matching-exchange-operation-tag-tor-gate.md":
        "050191376b790ec1f7092f3ff3ef3f1f20f44bdcc9403e96048c598a27ce9493",
    "computations/verify_h3_chart_odd_gate_ii_augmented_filler_terminal_fork.py":
        "cd445864a1440b89b213229c6795b409a9c49b84bf388dc4a476ed2030077e91",
    "notes/h3-chart-odd-gate-ii-augmented-filler-terminal-fork.md":
        "fdb07cd655a0bd4dfa519c8c7faed8cafac105345737f44902b8127324f24a2a",
}
EXPECTED_LEDGER_SHA256 = (
    "b51c050afb2c9ee57eecf93714a62595e4575bb0c2261003d2f21b91ee0dcfab"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


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
            rows[row] = [a - value * b for a, b in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()

    # Coordinate order: two ordered copies of the direct chart, followed by
    # the two endpoint charts.  The flat K2,2 mate rows are signless edges.
    charge = (Q(1), Q(1), Q(-1), Q(-1))
    mate_rows = (
        (Q(1), Q(0), Q(1), Q(0)),  # A_ab + B
        (Q(0), Q(1), Q(0), Q(1)),  # A_ba + C
        (Q(1), Q(0), Q(0), Q(1)),  # A_ab + C
        (Q(0), Q(1), Q(1), Q(0)),  # A_ba + B
    )
    require(rank(mate_rows) == 3, "flat square rank changed")
    require(all(dot(charge, row) == 0 for row in mate_rows),
            "balanced charge stopped annihilating mate rows")
    require(rank(mate_rows + (charge,)) == 4,
            "balanced charge stopped being the unique missing direction")

    # Identifying the two ordered direct copies is the literal Gate-II
    # projection A_[a|b],A_[b|a] -> A.
    gate_projection = (
        charge[0] + charge[1], charge[2], charge[3]
    )
    require(gate_projection == (Q(2), Q(-1), Q(-1)),
            "Gate-II projection changed")

    # The same vector is chart-sign tensor matching-constant.
    chart_sign = (Q(1), Q(-1))
    matching_constant = (Q(1), Q(1))
    tensor = tuple(a * b for a in chart_sign for b in matching_constant)
    require(tensor == charge, "operation-tag factorization changed")

    # Complete-row recurrent-core model.  Rows are indexed by A0,A1,B0,B1
    # and columns by the four companion variables z00,z01,z10,z11.
    companion_columns = (
        (Q(1), Q(0), Q(1), Q(0)),
        (Q(1), Q(0), Q(0), Q(1)),
        (Q(0), Q(1), Q(1), Q(0)),
        (Q(0), Q(1), Q(0), Q(1)),
    )
    require(rank(companion_columns) == 3, "K2,2 incidence rank changed")
    require(all(dot(charge, column) == 0 for column in companion_columns),
            "K2,2 charge stopped being the left-kernel")
    core_row = (Q(1), Q(1), Q(1), Q(1))
    weighted_core_row = (Q(1), Q(2), Q(1), Q(1))
    require(dot(charge, core_row) == 0
            and dot(charge, weighted_core_row) == 1,
            "projection ideal pairing changed")

    # The exact balanced counterpoint F_v=C+sum_{e incident v} z_e=0.
    C = Q(1)
    z = (Q(-1, 2),) * 4
    equations = tuple(C + sum(z[index] for index, column in
                              enumerate(companion_columns) if column[row])
                      for row in range(4))
    require(equations == (Q(0),) * 4,
            "balanced K2,2 counterpoint changed")

    normalized_dual = tuple(value / 4 for value in charge)
    require(dot(normalized_dual, charge) == 1
            and all(dot(normalized_dual, row) == 0 for row in mate_rows),
            "normalized primitive dual changed")

    ledger = {
        "theorem": "balanced chart-square master obstruction",
        "pins": PINS,
        "four_coordinates": ["A_[a|b]", "A_[b|a]", "B", "C"],
        "balanced_charge": [str(value) for value in charge],
        "flat_mate_rank": rank(mate_rows),
        "rank_after_charge": rank(mate_rows + (charge,)),
        "gate_II_projection": [str(value) for value in gate_projection],
        "operation_factorization": {
            "chart_sign": [str(value) for value in chart_sign],
            "matching_constant": [str(value) for value in matching_constant],
            "tensor": [str(value) for value in tensor],
        },
        "recurrent_core_projection": {
            "companion_incidence_rank": rank(companion_columns),
            "balanced_core_pairing": str(dot(charge, core_row)),
            "uncentered_core_pairing": str(dot(charge, weighted_core_row)),
            "balanced_exact_point": {
                "C": str(C), "z_edges": [str(value) for value in z],
                "complete_rows": [str(value) for value in equations],
            },
        },
        "primitive_dual": [str(value) for value in normalized_dual],
        "single_remaining_schema": (
            "a tail-covariant, same-word/fine/repeated, chart-odd balanced-"
            "square saturation cell with boundary charge tensor the fixed "
            "C4 tail; or extension of charge/4 to the complete augmented "
            "physical terminal"
        ),
        "three_outputs_if_placed": [
            "closes the 18 Gate-II DQ/PS direction faces",
            "kills the centered recurrent-core K2,2 projection obstruction",
            "kills the overlapping-chart Bianchi operation-sign class and permits dGamma=r-2q",
        ],
        "scope_guard": (
            "the equality is exact in the common coefficient/character "
            "module.  It does not identify different physical words, tails, "
            "C4 windows, or repeated/Hasse idempotents; the required theorem "
            "is a natural labelled family, not one untyped column"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("Gate-II ordered charge = recurrent K2,2 charge = chart-sign tensor matching-constant")
    print("existing balanced-square rows: rank 3; adjoining charge: rank 4")
    print("remaining datum: ONE NATURAL LABELLED BALANCED-SQUARE SATURATION FAMILY")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
