#!/usr/bin/env python3
"""Test the corrected balanced-z dual on the root-return collision packet.

There are three different statements which must not be conflated.

1.  The four first collision monomials are new, independent output
    coordinates.  Even after graphing them over the complete known
    cap/Cartan packet, the pure-safe balanced dual extends with value zero on
    all four collision coordinates.  They do not fill z.
2.  The two projected opposite-root returns are A-B and A-C.  The normalized
    direction dual (2,-1,-1)/6 reads 1/2 on each and 1 on their sum z.  One
    return raises rank but does not fill z; both returns do.
3.  The committed collision packet has no literal word/fine map to the
    canonical AugP2 cap packet.  Consequently the second item is an exact
    coefficient-level filler criterion, not an already constructed physical
    source filler.

The checker freezes both the small operation-space ranks and the complete
four-word direction quotient ranks, and rechecks the corrected cap dual on
all old r0/T/rho/K and pure-target columns.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_balanced_c4_hyperbolic_root_return_gate.py":
        "f52c7a8b447a63ee34b3b41e7bbab713409366e7a5a1a16087032a205da2fa9f",
    "notes/h3-balanced-c4-hyperbolic-root-return-gate.md":
        "c4fcd6505401b413bb45aa5fcdc2e3e04f7e38d555250c3cfbee7c643fe1cbcc",
    "computations/verify_h3_balanced_z_relative_ladder_terminal_gate.py":
        "2d3e15052295a5724d2ba81ae00fc4c26a8e9aebbb2589feca25023479b012b4",
    "notes/h3-balanced-z-relative-ladder-terminal-gate.md":
        "eea2472bf05d926f15ae82aec159575792a319ae66107d57d965c449e3caa0ca",
    "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py":
        "bd3f008eb2faf00bbebccb09ef9692908f2e0ae4a795706de2c32f0b2ef342af",
    "notes/h3-shear-collision-augp2-packaging-map-gate.md":
        "9d5918605dd94d08d18c099966e5956fa0f1c62855b97fd81bf9ada54f2f45ad",
    "computations/verify_h3_gate_ii_chiw_nonfill_full_augmented_dual.py":
        "c62ca38edf160f706d7aed237a923737ca46fe7b906fb0bb48bdf400e2ea7854",
    "computations/verify_h3_balanced_square_pointed_full_q_cone_gate.py":
        "10c2ca7ca9168d41f25f428b628710c0eaf8bc2aa910e23100da161869fdc72e",
}
EXPECTED_LEDGER_SHA256 = (
    "8775723e36bd54f9a729ca313cc97efc42f69d77e5afe03fd4ea6949bf3126dd"
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


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left, right) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(height):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def vector(width: int, entries: dict[int, int | Q]) -> tuple[Q, ...]:
    return tuple(Q(entries.get(index, 0)) for index in range(width))


def small_operation_collision_audit() -> dict[str, object]:
    # Coordinates A,B,C,F01,F10,F02,F20.  Signs of the first faces are part
    # of their names; changing a basis sign does not affect the rank test.
    width = 7
    complete = vector(width, {0: 1, 1: 1, 2: 1})
    collision_faces = tuple(vector(width, {index: 1})
                            for index in range(3, 7))
    return_ab = vector(width, {0: 1, 1: -1})
    return_ac = vector(width, {0: 1, 2: -1})
    z = vector(width, {0: 2, 1: -1, 2: -1})
    detector = (Q(1, 3), Q(-1, 6), Q(-1, 6), Q(0), Q(0), Q(0), Q(0))

    first = (complete,) + collision_faces
    one_ab = first + (return_ab,)
    one_ac = first + (return_ac,)
    both = first + (return_ab, return_ac)
    require(rank((complete,)) == 1
            and rank(first) == 5 and rank(first + (z,)) == 6
            and (rank(one_ab), rank(one_ab + (z,))) == (6, 7)
            and (rank(one_ac), rank(one_ac + (z,))) == (6, 7)
            and (rank(both), rank(both + (z,))) == (7, 7),
            "the operation-space collision/return ranks changed")
    require(dot(detector, complete) == 0
            and all(dot(detector, face) == 0 for face in collision_faces)
            and dot(detector, return_ab) == dot(detector, return_ac) == Q(1, 2)
            and dot(detector, z) == 1,
            "the normalized operation detector values changed")
    return {
        "row_order": ["A=DQ", "B=P0S1", "C=P1S0",
                      "F01=-D*S1", "F10=P0*Q01",
                      "F02=-D*S0", "F20=P1*Q01"],
        "complete_response_rank": 1,
        "after_four_first_faces_rank_then_with_z": [5, 6],
        "after_only_A_minus_B_rank_then_with_z": [6, 7],
        "after_only_A_minus_C_rank_then_with_z": [6, 7],
        "after_both_returns_rank_then_with_z": [7, 7],
        "normalized_dual": [str(value) for value in detector],
        "values": {
            "four_collision_first_faces": ["0", "0", "0", "0"],
            "A_minus_B": "1/2",
            "A_minus_C": "1/2",
            "z=(A-B)+(A-C)": "1",
        },
    }


def full_direction_collision_audit() -> dict[str, object]:
    # Reconstruct the complete four-word direction quotient from 037ac9f.
    words = ("00", "10", "01", "11")
    charts = ("A", "B", "C")
    old_coordinates = tuple((word, chart)
                            for chart in charts for word in words)
    old_index = {coordinate: index for index, coordinate in
                 enumerate(old_coordinates)}
    old_width = len(old_coordinates)
    root_edges = (("00", "10"), ("00", "01"),
                  ("10", "11"), ("01", "11"))
    old_base = []
    for chart in charts:
        for source, target in root_edges:
            old_base.append(vector(old_width, {
                old_index[(source, chart)]: -1,
                old_index[(target, chart)]: 1,
            }))
    for word in words:
        old_base.append(vector(old_width, {
            old_index[(word, chart)]: 1 for chart in charts
        }))
    old_base = tuple(old_base)
    old_z = vector(old_width, {
        old_index[("00", "A")]: 2,
        old_index[("00", "B")]: -1,
        old_index[("00", "C")]: -1,
    })
    old_ab = vector(old_width, {
        old_index[("00", "A")]: 1,
        old_index[("00", "B")]: -1,
    })
    old_ac = vector(old_width, {
        old_index[("00", "A")]: 1,
        old_index[("00", "C")]: -1,
    })
    old_dual = tuple(Q((2, -1, -1)[charts.index(chart)], 6)
                     for chart in charts for _word in words)

    width = old_width + 4
    embed = lambda value: tuple(value) + (Q(0),) * 4
    collision_faces = tuple(vector(width, {old_width + index: 1})
                            for index in range(4))
    base = tuple(embed(column) for column in old_base) + collision_faces
    z, return_ab, return_ac = map(embed, (old_z, old_ab, old_ac))
    dual = old_dual + (Q(0),) * 4

    require(rank(old_base) == 10
            and rank(old_base + (old_z,)) == 11
            and rank(base) == 14 and rank(base + (z,)) == 15
            and (rank(base + (return_ab,)),
                 rank(base + (return_ab, z))) == (15, 16)
            and (rank(base + (return_ac,)),
                 rank(base + (return_ac, z))) == (15, 16)
            and (rank(base + (return_ab, return_ac)),
                 rank(base + (return_ab, return_ac, z))) == (16, 16),
            "the full direction collision/return ranks changed")
    require(all(dot(dual, column) == 0 for column in base)
            and dot(dual, return_ab) == dot(dual, return_ac) == Q(1, 2)
            and dot(dual, z) == 1,
            "the full direction detector values changed")
    return {
        "old_tag_preserving_plus_complete_rank": 10,
        "after_four_private_collision_faces_rank": 14,
        "after_four_faces_rank_then_with_z": [14, 15],
        "after_one_return_rank_then_with_z": [15, 16],
        "after_both_returns_rank_then_with_z": [16, 16],
        "normalized_chart_values_A_B_C": ["1/3", "-1/6", "-1/6"],
        "collision_values": ["0", "0", "0", "0"],
        "return_values": ["1/2", "1/2"],
        "z_value": "1",
    }


def corrected_cap_graph_audit(balance, nonfill) -> dict[str, object]:
    guard = balance.pure_safe_full_row_counterguard(nonfill)
    require(guard["rank_before_balanced_face"] == 15
            and guard["rank_after_balanced_face"] == 16,
            "the corrected pure-safe cap ranks changed")
    old_columns_named = nonfill.cap_cartan_columns()
    old_columns = tuple(value for _name, value in old_columns_named) + (
        nonfill.vector(target2=1), nonfill.vector(target3=1),
    )
    z = nonfill.vector(**{
        **{f"B{corner}": nonfill.DELTA[corner] for corner in range(4)}
    })
    primitive = nonfill.vector(**{
        **{f"B{corner}": nonfill.DELTA[corner] for corner in range(4)},
        "Eq2": 1, "Eq3": 1,
        "target0": -1, "target1": -1,
        "W0": -1, "W1": -1,
        "ores0": 1, "ores1": 1,
    })
    normalized = tuple(value / 4 for value in primitive)
    require(rank(old_columns) == 15 and rank(old_columns + (z,)) == 16
            and all(dot(normalized, column) == 0 for column in old_columns)
            and dot(normalized, z) == 1,
            "the normalized corrected cap dual changed")

    # Strongest harmless formal grant: graph each private collision coordinate
    # over one complete r0 cap image.  The corner assignment is bookkeeping;
    # every permutation has the same conclusion because every r0_j is killed.
    old_width = len(z)
    width = old_width + 4
    embed = lambda value: tuple(value) + (Q(0),) * 4
    r0 = tuple(dict(old_columns_named)[f"r0_{corner}"]
               for corner in range(4))
    collision_graphs = tuple(tuple(a + b for a, b in zip(
        embed(r0[corner]), vector(width, {old_width + corner: 1}), strict=True
    )) for corner in range(4))
    base = tuple(embed(column) for column in old_columns)
    z_full = embed(z)
    dual = normalized + (Q(0),) * 4
    require(rank(base) == 15 and rank(base + collision_graphs) == 19
            and rank(base + collision_graphs + (z_full,)) == 20
            and all(dot(dual, column) == 0
                    for column in base + collision_graphs)
            and dot(dual, z_full) == 1,
            "the cap-graphed collision extension changed")
    return {
        "corrected_normalized_signature": {
            "B": ["1/4", "1/4", "-1/4", "-1/4"],
            "Eq": ["0", "0", "1/4", "1/4"],
            "target": ["-1/4", "-1/4", "0", "0"],
            "W": ["-1/4", "-1/4", "0", "0"],
            "ordinary_residue": ["1/4", "1/4", "0", "0"],
            "M_ainc_q_Pf_ridge_eta_sigma": "0",
        },
        "known_cap_Cartan_plus_pure_target_rank": 15,
        "rank_after_four_collision_graphs": 19,
        "rank_after_collision_graphs_and_z": 20,
        "collision_coordinate_values": ["0", "0", "0", "0"],
        "known_images_tested": "r0_0,...,r0_3 with all T/rho/K retained",
        "all_known_cap_Cartan_and_pure_target_columns_annihilated": True,
        "invariance": (
            "the same zero-value extension works for a collision graph over "
            "any tail in the span of the known augmented columns"
        ),
    }


def physical_attachment_gate(packaging) -> dict[str, object]:
    ledger, digest = packaging.audit()
    require(digest == packaging.EXPECTED_LEDGER_SHA256,
            "the collision packaging ledger changed")
    words = ledger["literal_word_and_fine_map"]
    augmented = ledger["augmented_packaging"]
    require(not words["literal_grade_preserving_map"]
            and not augmented["existing_AugP2_status"]
                ["constructed_literal_source_object"]
            and augmented["rank_before_mixed_cell"] == 2
            and augmented["rank_after_mixed_cell"] == 3
            and augmented["rank_after_labelled_ridge"] == 4,
            "the physical collision attachment gate changed")
    return {
        "collision_response_word": words["response_word_display"],
        "canonical_cap_word": words["canonical_cap_word"],
        "word_hamming_distance": words["word_hamming_distance"],
        "literal_collision_to_cap_map_exists": False,
        "post_word_packaging_ranks": [2, 3, 4],
        "missing_after_collision_lower_face": [
            "mixed mapping-square incidence / reduced-Eq cap-label descent",
            "labelled shifted ridge and connection face",
        ],
        "consequence": (
            "the two pure return columns are not existing physical source "
            "columns; adjoining them would assume the missing totalized "
            "collision-to-cap/root-return bicomplex"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    balance = load(
        "computations/verify_h3_balanced_square_pointed_full_q_cone_gate.py",
        "balanced_collision_balance",
    )
    nonfill = load(
        "computations/verify_h3_gate_ii_chiw_nonfill_full_augmented_dual.py",
        "balanced_collision_nonfill",
    )
    packaging = load(
        "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py",
        "balanced_collision_packaging",
    )
    ledger = {
        "theorem": "h3 balanced-z hyperbolic collision terminal/filler gate",
        "pins": PINS,
        "small_operation_complex": small_operation_collision_audit(),
        "full_four_word_direction_quotient": full_direction_collision_audit(),
        "corrected_pure_safe_cap_extension":
            corrected_cap_graph_audit(balance, nonfill),
        "physical_source_attachment": physical_attachment_gate(packaging),
        "verdict": (
            "The corrected balanced terminal extends over all four private "
            "collision first faces and over their strongest currently "
            "available cap/Cartan graph shadows, with collision value zero. "
            "The projected opposite-root returns are different: the "
            "normalized dual reads 1/2 on A-B and 1/2 on A-C, and both "
            "returns make z=(A-B)+(A-C) lie in the image.  They are exactly "
            "the desired coefficient-level filler, but no committed "
            "word/fine/repeated source map packages the collision faces, "
            "mixed cap incidence and shifted ridge into those return columns."
        ),
        "sharp_fork": {
            "current_literal_packet": (
                "dual survives; collision faces plus known augmented tails "
                "raise rank only in private collision coordinates"
            ),
            "if_physical_two_root_totalization_is_constructed": (
                "both return columns are present and z is filled exactly"
            ),
            "first_missing_source_datum": (
                "one source-labelled two-root collision mapping bicomplex "
                "containing both DQ<->P0S1 and DQ<->P1S0 returns, the four "
                "collision first faces, word/fine transport, mixed reduced-Eq "
                "cap incidence, and the labelled shifted ridge"
            ),
        },
        "scope": (
            "exact canonical h=3 coefficient and complete four-word direction "
            "packets, plus the committed cap/Cartan and collision packaging "
            "interfaces; not a constructed full decorated GHZ source cell "
            "and not an all-h terminal theorem"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("balanced collision ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("balanced z through four collision first faces: EXTENDS (value 0)")
    print("cap/Cartan graph rank: 15 -> 19; with z: 20")
    print("return values: 1/2, 1/2; both-return rank: 16 -> 16 with z")
    print("physical two-root source totalization: NOT CONSTRUCTED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
