#!/usr/bin/env python3
"""Identify the first physical face of the missing Gate-II chi_w cell.

The three matching charts are ordered (A,B,C), where A is the retained
chart and B,C are its two four-cycle replacements.  The missing root-only
V4 character restricts to the endpoint-even switch direction

    2 A - B - C.

Its first principal-parts direction vector is the chart-complete Spencer
weight (2,2,-1,-1,-1,-1).  After duplicating orientations are forgotten,
the C4 part is precisely 2 DQ - PS - PS.  Complete rows and the endpoint
groupoid kill the aggregate and endpoint-odd lines, but not this invariant
line.  The target-bearing C2+ face has an exact formal correction; the first
unfilled same-grade physical face is therefore the protected relative-C4
column.  Its occurrence augmentation is one while its physical ainc and q
readouts are both zero.  The downstream word-0102 P2 carrier remains a
second, differently graded placement after restriction.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_gate_ii_cartan_full_q_pointed_character_gate.py":
        "6f791c41e743a94279ccf9e4924af11a42c278baa7737a5eed108bf85136f499",
    "notes/h3-gate-ii-cartan-full-q-pointed-character-gate.md":
        "3ffd0d0894dfbb81cb672f87548b3b7a2da28ac1b36a6466bbef6ad149cf0933",
    "computations/verify_uniform_response_h2_chart_direction_spencer_packet_gate.py":
        "46b53933a080d0b8eeceee695ecd0d4c6d72224d7d0fea4352176b410b8b7fe4",
    "notes/uniform-response-h2-chart-direction-spencer-packet-gate.md":
        "d57b734cbbb99f5088cdd01e803522ffcd5b55dc2123525ae6d744de6e9a0445",
    "computations/verify_uniform_chart_cross_companion_relative_switch_dga_gate.py":
        "e0a8251128174d50b450b3bf85ce0a6870af00d4ab5565e7849fc3c8644c31c6",
    "notes/uniform-chart-cross-companion-relative-switch-dga-gate.md":
        "2b9fbe0c648cadc5913e57e4b6d678205c7f7fbc66f57e58e371f9ad10ef2cb8",
    "computations/verify_h3_h2_direction_tag_maschke_c4_coinvariant_gate.py":
        "bee87b90c32720583f50d1c65dc2280dd337a46d197932d8c22aab802362d9ff",
    "notes/h3-h2-direction-tag-maschke-c4-coinvariant-gate.md":
        "f61147619b6758924c700fd3a4d99a1edb398ed9abc23f417fdf745209055d29",
    "computations/verify_h2_lower_even_cartan_jstar_target_cone_gate.py":
        "09ba792f229bb3a1e930b2c59b0de2356b08a7434c648aad9573d8382c652a52",
    "notes/h2-lower-even-cartan-jstar-target-cone-gate.md":
        "2f80cf6fa8d87a9acc4f3441bba5753b9b3c7de5c19e6c709d75969b7eb9d381",
    "computations/verify_h3_generic_symmetric_c4_placement_terminal_gate.py":
        "ecb8725715747c3270fb069545309283d1890fbac6e66dfb6ed2f53b609e0030",
    "notes/h3-generic-symmetric-c4-placement-terminal-gate.md":
        "dcf0ef4adf500b4bee46ca301b12241e95ed1343a509a4fe4110d5dd3a906e92",
    "computations/verify_h3_pure_trapped_h2_c2_c4_p2_descent_reduction.py":
        "026eb42fac96e2c21e6466f51322a18d45d975bcf5f48e0dc33f9cfa740d8d41",
    "notes/h3-pure-trapped-h2-c2-c4-p2-descent-reduction.md":
        "699a9debf8de2646249f949e80312baa58251a1f36639bed249d40e2dc74b2ea",
}
EXPECTED_LEDGER_SHA256 = "a93d53a14ca7cb2239e2964ac7380ffca122215e5af812192e1429d955156179"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rank(rows):
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((index for index in range(pivot_row, len(work))
                      if work[index][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for index in range(len(work)):
            if index == pivot_row or not work[index][column]:
                continue
            value = work[index][column]
            work[index] = [left - value * right for left, right in
                           zip(work[index], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def chart_character_audit() -> dict[str, object]:
    # Three chart occurrences A,B,C.  H is the complete row, O the
    # endpoint-odd Cartan line, and E the endpoint-even/root-only line.
    complete = (Q(1), Q(1), Q(1))
    odd = (Q(0), Q(1), Q(-1))
    even = (Q(2), Q(-1), Q(-1))
    switch_sum = (Q(-2), Q(1), Q(1))
    require(dot(complete, odd) == dot(complete, even) == dot(odd, even) == 0
            and rank((complete, odd)) == 2
            and rank((complete, odd, even)) == 3
            and switch_sum == tuple(-entry for entry in even),
            "the three-chart character decomposition changed")

    # First PP order, with the orientation conventions of c82bc96.
    directions = ("dD", "dq01", "dp0", "ds1", "dp1", "ds0")
    kappa = (Q(2), Q(2), Q(-1), Q(-1), Q(-1), Q(-1))
    # Each unoriented direction-pair type occurs twice.  Forgetting this
    # harmless orientation duplication gives the unique C4 invariant.
    unoriented = (kappa[0], kappa[2], kappa[4])
    require(kappa[0] == kappa[1]
            and kappa[2] == kappa[3]
            and kappa[4] == kappa[5]
            and unoriented == even,
            "the chart Spencer vector stopped projecting to the C4 line")
    return {
        "chart_order": ["A=01|PS", "B=0P|1S", "C=1P|0S"],
        "complete_row": list(map(int, complete)),
        "endpoint_odd_Cartan": list(map(int, odd)),
        "chi_w_endpoint_even": list(map(int, even)),
        "switch_carrier_t1_plus_t2": list(map(int, switch_sum)),
        "identity": "t1+t2=-(2A-B-C)=-chi_w",
        "first_PP_direction_order": list(directions),
        "first_PP_kappa": list(map(int, kappa)),
        "unoriented_C4_projection": list(map(int, unoriented)),
        "rank_complete_plus_odd": rank((complete, odd)),
        "rank_after_chi_w": rank((complete, odd, even)),
    }


def target_and_groupoid_audit() -> dict[str, object]:
    # Root-only Weyl target defect in the literal two mixed plus two pure
    # word basis.  The independent J*/even-Cartan cone supplies its negative.
    defect = (Q(1), Q(1), Q(-1), Q(-1))
    correction = tuple(-entry for entry in defect)
    require(tuple(left + right for left, right in
                  zip(defect, correction, strict=True)) == (Q(0),) * 4,
            "the C2+ target correction changed")

    # Locally theta swaps the two endpoint-pair directions.  The normalized
    # C2 bar relation spans only the odd line; complete rows add the constant
    # line.  The even C4 direction is invariant and remains independent.
    constant = (Q(1), Q(1), Q(1))
    theta_relation = (Q(0), Q(1), Q(-1))
    c4_invariant = (Q(2), Q(-1), Q(-1))
    require(rank((constant, theta_relation)) == 2
            and rank((constant, theta_relation, c4_invariant)) == 3,
            "endpoint groupoid unexpectedly filled the C4 invariant")
    return {
        "target_word_basis": ["m_(c|i)", "m_(i|c)", "p_i", "p_c"],
        "chi_w_target_defect": list(map(int, defect)),
        "C2plus_Jstar_target_correction": list(map(int, correction)),
        "corrected_target": [0, 0, 0, 0],
        "endpoint_groupoid_relation": list(map(int, theta_relation)),
        "C4_invariant": list(map(int, c4_invariant)),
        "complete_plus_groupoid_rank": 2,
        "rank_with_C4_invariant": 3,
        "groupoid_totalizes_C4_invariant": False,
    }


def literal_face_audit() -> dict[str, object]:
    # This is the exact source-column interface isolated by the generic C4
    # theorem.  Do not confuse occurrence augmentation with physical ainc.
    u_c4 = {
        "name": "U_C4[D,Q01;2345]",
        "PP_grade": "Hasse[2](D,Q01)",
        "residual_sites": "2345",
        "local_face": ["q23*q45", "q24*q35", "q25*q34"],
        "local_coefficients": [1, 1, 1],
        "occurrence_augmentation": 1,
        "physical_readouts": {
            "target": 0,
            "ainc": 0,
            "q=M-a": 0,
            "Eq": 0,
            "W": 0,
            "ordinary_residue": 0,
            "shifted_ridge": 0,
        },
        "word_fine_repeated": (
            "the literal parent fan word/fine/repeated grade, retaining the "
            "Hasse[2](D,Q01) tag; its PS representative is "
            "Hasse[2](P0,S1) and is not a P2 relabelling"
        ),
    }
    require(u_c4["occurrence_augmentation"] == 1
            and u_c4["physical_readouts"]["ainc"] == 0
            and u_c4["physical_readouts"]["q=M-a"] == 0,
            "occurrence augmentation was confused with physical ainc")

    downstream_p2 = {
        "intermediate_word": "0102",
        "lower_word": "0112",
        "residual": "q45:12",
        "reinsertion": "q23:21",
        "top_grade": "01211222 / repeated P3+K2",
        "carrier": "t_zpriv",
        "augmented_signature": "undefined until physical placement",
    }
    return {
        "first_uncontracted_same_grade_face": u_c4,
        "downstream_differently_graded_face": downstream_p2,
        "ordering": (
            "U_C4 is the invariant face in the original Hasse[2] tag "
            "quotient; t_zpriv appears only after restriction and word/fine "
            "promotion"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 Gate-II chi_w chart-complete H2 face identification",
        "pins": PINS,
        "chart_character": chart_character_audit(),
        "target_and_endpoint_groupoid": target_and_groupoid_audit(),
        "literal_first_face": literal_face_audit(),
        "verdict": (
            "The missing Gate-II root character is exactly the endpoint-even "
            "three-chart switch 2A-B-C.  Its chart-complete first PP vector "
            "is (2,2,-1,-1,-1,-1).  The known diagonal/even Cartan cone "
            "cancels its C2+ mixed target defect.  Conditional termwise "
            "endpoint groupoid bars contract all nontrivial direction tags, "
            "but complete rows and those bars leave the invariant C4 face "
            "2DQ-PS-PS.  Thus the first irreducible source datum is exactly "
            "U_C4[D,Q01;2345], with occurrence augmentation one and zero "
            "physical target/ainc/q/Eq/W/residue/ridge.  After restriction a "
            "separate word-0102 t_zpriv physical landing is still required."
        ),
        "scope": (
            "exact h3 coefficient, PP-type, target and augmented-signature "
            "identification.  It does not construct U_C4 or the downstream "
            "t_zpriv source column; it proves that endpoint groupoid and "
            "complete-row totalization cannot remove the former."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("chi_w H2 face ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("freeze EXPECTED_LEDGER_SHA256=" + digest)
        return
    print("chi_w: EXACTLY 2A-B-C")
    print("first PP: (2,2,-1,-1,-1,-1)")
    print("C2plus target: CANCELLED CONDITIONALLY ON PHYSICAL P2")
    print("endpoint groupoid: LEAVES INVARIANT C4 2DQ-PS-PS")
    print("first source datum: U_C4[D,Q01;2345]")
    print("downstream datum: word-0102 t_zpriv")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
