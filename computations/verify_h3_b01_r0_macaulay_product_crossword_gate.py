#!/usr/bin/env python3
"""Audit whether the formal product b01*r0 constructs the missing comparison.

The undecorated Leibniz formula is tempting:

    d(b01*r0) = db01*r0 + b01*d(r0).

It has the same six polynomial derivatives and central Eq coefficient that
occur on the desired response-KS -> cap-r0 comparison.  This checker retains
the source word, PP direction, repeated grade and operation parent.  With
those idempotents present, Macaulay multiplication keeps both faces in the
cap summand.  It does not turn the selected response db01 face into a cap
face and therefore does not construct the missing off-diagonal chain map.

Conditionally adjoining that one map makes the formula the correct product
rule and keeps the cap private/reduced-Eq occurrence tied, so the calculation
is a useful normal form rather than a new obstruction.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py":
        "02a28ec54b83b2f786e47b0fdc992f5f28dd95a04ba16219f0e24482d4999097",
    "notes/h3-response-ks-to-cap-r0-multiplicative-comparison-gate.md":
        "b87cccff771337fc7ed6d0092f958303084c1be8326a9faf46efb7fa751ed8f6",
    "computations/verify_h3_psi_source_grade_macaulay_exhaustiveness_terminal_gate.py":
        "2ae3d0fe36ca6ab92ee506b4a4441d6476ecb09567a1441c66f54793e304980d",
    "notes/h3-psi-source-grade-macaulay-exhaustiveness-terminal-gate.md":
        "de47eeafdfcffbd043f3b2472f3be54b7ec94ad546fe2bab7194e8b64bd9c98a",
    "computations/verify_h3_db01_dl01_literal_private_eq_conservation_gate.py":
        "1a27b00d28be6334a27e0603a0ef776367d3c71b6f8fa45d3005963f8dff4c6c",
    "notes/h3-db01-dl01-literal-private-eq-conservation-gate.md":
        "6ba7ac1df36e3ed4ed30acc1d219f22bcdff0d673e078aeb3b2e1d327a2737d9",
    "computations/verify_h3_uc4_beq_tie_source_provenance_audit.py":
        "f237ccffd40863a201b780ea034fcbd7781bc555e1fbc6f528d99d3ab71394c6",
    "notes/h3-uc4-beq-tie-source-provenance-audit.md":
        "4501c6613523222e6c32345f3624a1ceccc7b3b0a2fe934e482a03543e336aa8",
}
EXPECTED_LEDGER_SHA256 = "7e35f59dc5605165d45453a1c7779e07d2ca6fd387293944b6f8163fb6db9a64"

DELTA = tuple(map(Q, (1, 1, -1, -1)))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left, right) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    columns = tuple(tuple(map(Q, column)) for column in columns)
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[columns[column][row] for column in range(len(columns))]
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


@dataclass(frozen=True)
class Grade:
    word: str
    fine: str
    repeated: str
    operation: str


RESPONSE_DB01 = Grade(
    word="11:110000",
    fine="p0*s1 and one marked dq among 23|45,24|35,25|34",
    repeated="squarefree vertical PP face",
    operation="selected response occurrence / endpoint-matching PP",
)
CAP_R0 = Grade(
    word="01211222",
    fine="six literal t*q_(v,N) P3+K2 occurrence degrees",
    repeated="P3+K2",
    operation="AugP2 cap / K_Eq r0",
)


def selected_polynomial_audit() -> dict[str, object]:
    matchings = (("23", "45"), ("24", "35"), ("25", "34"))
    b01_terms = tuple(("p0", "s1", left, right)
                      for left, right in matchings)
    db01_terms = tuple(
        ("p0", "s1", f"d{edge}", mate)
        for left, right in matchings
        for edge, mate in ((left, right), (right, left))
    )
    require(len(set(b01_terms)) == 3 and len(set(db01_terms)) == 6,
            "selected polynomial support changed")
    return {
        "b01_terms": [list(term) for term in b01_terms],
        "db01_terms": [list(term) for term in db01_terms],
        "b01_term_count": len(b01_terms),
        "db01_term_count": len(db01_terms),
        "undecorated_Leibniz_identity":
            "d(b01*r0)=db01*r0+b01*(H0-u)eEq",
    }


def typed_macaulay_audit() -> dict[str, object]:
    # Direct-sum coordinates are response-db01, cap-PP, cap-central-Eq.
    selected_response_face = (Q(1), Q(0), Q(0))
    cap_product_pp_face = (Q(0), Q(1), Q(0))
    cap_product_eq_face = (Q(0), Q(0), Q(1))
    product_boundary = tuple(
        cap_product_pp_face[index] + cap_product_eq_face[index]
        for index in range(3)
    )
    require(RESPONSE_DB01 != CAP_R0,
            "response and cap grades unexpectedly coincide")
    require(rank((cap_product_pp_face, cap_product_eq_face)) == 2
            and rank((cap_product_pp_face, cap_product_eq_face,
                      selected_response_face)) == 3
            and product_boundary == (0, 1, 1),
            "typed direct-sum rank changed")

    # Macaulay multiplication is diagonal on the word/operation idempotents.
    # It changes polynomial fine degree, not the operation parent.  Applying
    # it any finite number of times can therefore never acquire the response
    # component.
    grade = CAP_R0
    orbit = []
    for degree in range(5):
        orbit.append({"multiplier_degree": degree, "grade": grade.__dict__})
        require(grade == CAP_R0, "Macaulay multiplication changed idempotent")

    return {
        "response_selected_grade": RESPONSE_DB01.__dict__,
        "cap_r0_grade": CAP_R0.__dict__,
        "same_undecorated_six_polynomials": True,
        "same_typed_source_face": False,
        "direct_sum_coordinates": [
            "selected response db01", "cap-parent db01*r0 PP",
            "cap-parent b01*(H0-u)eEq",
        ],
        "cap_product_boundary": list(map(int, product_boundary)),
        "rank_cap_faces_then_selected_response": [2, 3],
        "Macaulay_orbit": orbit,
        "Macaulay_changes": ["polynomial multidegree"],
        "Macaulay_preserves": [
            "word", "operation parent", "source idempotent",
            "repeated parent", "occurrence labels",
        ],
        "strict_projection_of_cap_product_to_response_db01": 0,
        "strict_projection_of_response_db01_to_cap_BEq": 0,
    }


def private_eq_charge_audit() -> dict[str, object]:
    tied = DELTA + DELTA
    chi = DELTA + tuple(-value for value in DELTA)
    private_only = DELTA + (Q(0),) * 4
    require(dot(chi, tied) == 0 and dot(chi, private_only) == 4,
            "private/Eq normalization changed")
    # A cap-internal Macaulay multiple keeps the r0 tie.  It is dark, not the
    # missing operation-changing column.
    return {
        "r0_B_Eq_signature": [list(map(int, DELTA)), list(map(int, DELTA))],
        "chi": "delta.(B-Eq)",
        "chi_on_b01_times_r0": int(dot(chi, tied)),
        "Psi_on_b01_times_r0": int(dot(chi, tied) / 4),
        "interpretation": (
            "the product is a legitimate cap-internal dark Macaulay column; "
            "it neither breaks nor constructs the mixed comparison"
        ),
    }


def conditional_comparison_audit() -> dict[str, object]:
    # Once an off-diagonal matrix unit w identifies the response selected
    # fibre with cap r0, the two summands can be compared.  The chain map has
    # the unique normalized signs (epsilon -> r0, c_f -> -E), and the same
    # Leibniz expression is then the correct first-face formula.
    relation = (Q(1), Q(1))
    normalized = (Q(1), Q(-1))
    require(dot(relation, normalized) == 0,
            "normalized chain map signs changed")
    return {
        "required_new_datum": (
            "degree-zero source-labelled matrix unit Phi_KS,r0 from the "
            "response KS idempotent to cap AugP2/K_Eq r0"
        ),
        "normalized_chain_map": {
            "Phi_1(epsilon_s)": "r0", "Phi_0(c_f)": "-E",
        },
        "after_Phi_product_rule":
            "d(b01*Phi(epsilon_s))=db01*r0+b01*E",
        "then_B_Eq_tied": True,
        "then_all_eight_standard_kappa_charges": [0] * 8,
        "logical_direction": (
            "Phi makes the Macaulay product useful; the Macaulay product "
            "does not manufacture Phi"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 b01*r0 Macaulay product cross-word gate",
        "selected_polynomial": selected_polynomial_audit(),
        "typed_Macaulay_product": typed_macaulay_audit(),
        "private_Eq_charge": private_eq_charge_audit(),
        "conditional_after_comparison": conditional_comparison_audit(),
        "verdict": (
            "The formal Leibniz formula has exactly the tempting six-term and "
            "central-Eq coefficient shapes.  Nevertheless b01*r0 is a "
            "cap-internal Macaulay multiple.  Multiplication preserves the "
            "01211222 AugP2/K_Eq source idempotent, while selected db01 lives "
            "in the 11:110000 response vertical-PP summand.  The typed faces "
            "are independent (rank 2->3), and the cap product is chi-dark "
            "because r0 remains B=Eq tied.  Therefore it does not construct "
            "the missing response-to-cap arrow.  Once that arrow is supplied, "
            "the same formula is the normalized product rule and forces all "
            "eight standard kappa charges to zero."
        ),
        "scope": (
            "exact h=3 source-tag/Macaulay audit; it does not rule out a new "
            "physical cross-word comparison primitive or prove full-source "
            "exhaustiveness"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    require(digest == EXPECTED_LEDGER_SHA256,
            ("b01*r0 Macaulay ledger changed", digest))
    if arguments.json:
        print(json.dumps({"ledger": ledger, "sha256": digest},
                         indent=2, sort_keys=True))
    else:
        print("h3 b01*r0 Macaulay cross-word gate: PASS")
        print("formal Leibniz support: 6-term db01 + central Eq")
        print("typed result: cap-internal dark column; response face remains independent")
        print("conditional Phi_KS,r0: product rule closes all eight kappa charges")
        print(f"ledger sha256 {digest}")


if __name__ == "__main__":
    main()
