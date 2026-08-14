#!/usr/bin/env python3
"""Carry the pure-safe balanced dual through the Gate-II relative ladder.

The balanced detector from 0a684ce differs from the earlier delta detector
only on pure target/Eq correction rows.  This checker proves that those new
entries do not change the occurrence/PP ladder:

* R01/L01 extend over the monic relative three-cap graphs with forced carrier
  values (-1,+1); an absolute carrier is the filler arm.
* selected db01 extends only over dz01-db01; the desired absolute db01 column
  raises rank 2 -> 3, and target=Eq=0 on this face.
* after granting db01 and U_C4, the eighteen direction faces retain the
  primitive chart charge (2,-1,-1).  Every literal tag-preserving root edge
  and complete response row kills it.  The first physical source-label family
  that can break it is the pair DQ<->P0S1, DQ<->P1S0.
* the downstream relative P2 graph forces C*d=12*d, then dq/Q cancellation
  leaves occurrence-labelled ores -35/72; the committed response-gauge plus
  d_even calculation closes that residue only under its explicit physical
  landing hypotheses.

An exact block-gluing shadow constructs one normalized covector across the
old augmented, selected-db01, direction and word-0102 quotients.  It is a
terminal if those blocks and their audited normalized identifications are an
exhaustive same-grade physical map.  That exhaustiveness/gluing hypothesis is
not currently proved, so no unconditional full physical terminal is claimed.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_balanced_square_pointed_full_q_cone_gate.py":
        "10c2ca7ca9168d41f25f428b628710c0eaf8bc2aa910e23100da161869fdc72e",
    "notes/h3-balanced-square-pointed-full-q-cone-gate.md":
        "a81873b5e6f9b5c7c2e220b39dabd4fc74a7e1914690516b7727b578b04b9248",
    "computations/verify_h3_gate_ii_chiw_nonfill_full_augmented_dual.py":
        "c62ca38edf160f706d7aed237a923737ca46fe7b906fb0bb48bdf400e2ea7854",
    "computations/verify_h3_gate_ii_three_cap_relative_tate_carrier_obstruction.py":
        "0be2bde12d3d4b85cad67b4a647b4cb4f7e89ed1a04bff14f6091eb257224dcc",
    "notes/h3-gate-ii-three-cap-relative-tate-carrier-obstruction.md":
        "a4c19d4c5f28da42ec1a4af29e2008bd85eee131e7f4d787cb0f8ace14f88ec0",
    "computations/verify_h3_selected_db01_normalized_gl3_bar_companion_gate.py":
        "620b3e54e8e6ee09a0b616d0259c8d109b0359645b20d35db5fb876c8e7e0311",
    "notes/h3-selected-db01-normalized-gl3-bar-companion-gate.md":
        "46aa4e74c52160cfaa74089727defb1a0d6c4d0051130374ec12dcc887de09de",
    "computations/verify_h3_gate_ii_primitive_c4_joint_cobar_label_gate.py":
        "d77f4fd853673c434d4a0bb4027bf9ba046f1bb7ea4d752028a609e832255f44",
    "notes/h3-gate-ii-primitive-c4-joint-cobar-label-gate.md":
        "1adefa3bf3427a8f0c9c415376561bdd6b56c2f358fb236260b9956e7d7b0e62",
    "computations/verify_h3_physical_pp_hasse_toric_tate_cofibrancy_gate.py":
        "1fb82a919cbf70c5d3323d441c1a1feefd83361d70cc1cdc65e2d0f2c1eca0a9",
    "notes/h3-physical-pp-hasse-toric-tate-cofibrancy-gate.md":
        "ae52988050207d59a597d0e3852fe24f59c6cffdbcd2e0a5cebb7581a57ac867",
    "computations/verify_h3_gate_ii_psidelta_same_grade_extension_chain.py":
        "d5628f66ffbf94e2de37318ab136adda96af5e114e2bea8dce22542ec9f30cb1",
    "notes/h3-gate-ii-psidelta-same-grade-extension-chain.md":
        "2e7aea9a551ddc2ab845fb2c0717cbffb8f7db772c329fb3c11d6bdc3dc34fae",
    "computations/verify_h3_p2_labelled_ores_cut_even_deven_gauge_gate.py":
        "0a4215db2b91843753cc636b489a81f8e30a8c3de234979c74c9f852d74e3d8a",
    "notes/h3-p2-labelled-ores-cut-even-deven-gauge-gate.md":
        "0477f14ab8725708711ff098c68ae29f10625516024cc2a93413c780ea466054",
}
EXPECTED_LEDGER_SHA256 = (
    "89b68179775d0677fe50e836ebbcfd02bd46b416ff9dd9cfb939edcec78bc2ef"
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


def dot(left, right):
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


def vector(width: int, values: dict[int, int | Q]):
    return tuple(Q(values.get(index, 0)) for index in range(width))


def pure_safe_start(balance, nonfill) -> dict[str, object]:
    guard = balance.pure_safe_full_row_counterguard(nonfill)
    require(guard["rank_before_balanced_face"] == 15
            and guard["rank_after_balanced_face"] == 16
            and guard["detector_value_on_balanced_B_face"] == "4"
            and guard["primitive_detector_signature"]["M_ainc_q_Pf"]
                == [0, 0, 0, 0]
            and guard["primitive_detector_signature"]["ridge_eta_sigma"]
                == [0, 0, 0, 0],
            guard)
    return {
        "old_columns": guard["column_count"],
        "old_rank": guard["rank_before_balanced_face"],
        "rank_with_z": guard["rank_after_balanced_face"],
        "primitive_value_on_z": guard[
            "detector_value_on_balanced_B_face"],
        "normalized_value_on_z": "1",
        "signature": guard["primitive_detector_signature"],
        "important_change_from_old_delta_dual": (
            "Eq=(0,0,1,1) and the pure target/W/ores correction is supported "
            "only on the two mixed corners; B remains delta"
        ),
    }


def relative_top_and_lower_ladder(relative) -> dict[str, object]:
    ledger, digest = relative.audit()
    require(digest == relative.EXPECTED_LEDGER_SHA256,
            "the relative-three-cap ledger changed")
    top = ledger["top_three_cap"]
    first_pp = ledger["first_PP"]
    lower = ledger["downstream_P2"]
    require(top["forced_relative_dual"]["carrier_values_t_R_t_L"]
                == ["-1", "1"]
            and top["absoluteization_rank_test"][
                "graph_plus_complete_response"] == 3
            and top["absoluteization_rank_test"]["after_t_R_zero"] == 4
            and top["absoluteization_rank_test"][
                "after_t_R_and_t_L_zero"] == 5
            and first_pp["normalized_dual_values"]["tail_18"] == "0"
            and first_pp["normalized_dual_values"][
                "endpoint_direction_18"] == "1"
            and lower["forced_carrier_dual"]["formula"] == "C*d=12*d"
            and lower["dq_Q_ores_ladder"]["dq23_detector"] == "35/72"
            and lower["dq_Q_ores_ladder"][
                "remaining_labelled_ores_detector"] == "-35/72"
            and lower["dq_Q_ores_ladder"]["scalar_ordinary_ores"] == 0,
            (top, first_pp, lower))
    return {
        "R01_UC4_stage": {
            "relative_boundaries": top[
                "presentation_safe_relative_graph"]["boundaries"],
            "forced_dual_tR_tL": [-1, 1],
            "absoluteization_ranks": [3, 4, 5],
            "interpretation": (
                "a physical absolute t_R/t_L or reinserted U_C4/R01 column "
                "breaks the dual and is the filler arm; the monic relative "
                "graphs preserve H0 and carry the dual"
            ),
        },
        "first_PP": {
            "relative_graphs": first_pp["relative_differentiated_graph"],
            "dL01_support": first_pp["dL01_support"],
            "tail_18_value": first_pp["normalized_dual_values"]["tail_18"],
            "direction_18_value": first_pp[
                "normalized_dual_values"]["endpoint_direction_18"],
        },
        "word_0102_and_q_tail": {
            "relative_P2_boundary": lower["relative_P2_graph"]["boundary"],
            "local_detector": lower["local_detector"],
            "forced_carrier_dual": lower["forced_carrier_dual"]["formula"],
            "dq23_value": lower["dq_Q_ores_ladder"]["dq23_detector"],
            "best_Q_value": lower["dq_Q_ores_ladder"][
                "best_formal_labelled_p_Q_cancellation"],
            "remaining_labelled_ores": lower["dq_Q_ores_ladder"][
                "remaining_labelled_ores_detector"],
            "scalar_ores": lower["dq_Q_ores_ladder"][
                "scalar_ordinary_ores"],
            "conditional_ores_closure": lower[
                "conditional_labelled_ores_closure"],
        },
    }


def selected_db01_stage(selected_db, pp_tate) -> dict[str, object]:
    db_ledger, db_digest = selected_db.audit()
    pp_ledger, pp_digest = pp_tate.audit()
    require(db_digest == selected_db.EXPECTED_LEDGER_SHA256
            and pp_digest == pp_tate.EXPECTED_LEDGER_SHA256,
            "a selected-db01 dependency changed")
    graph = db_ledger["graph_and_bicomplex"]
    pp_face = pp_ledger["physical_faces"]["matching_PP_audit"]
    require(graph["rank_before_then_after_db01"] == [2, 3]
            and graph["primitive_dual"] == [1, 1, 0]
            and graph["literal_graph_PP_column"] == [-1, 1, 0]
            and "target=Eq=0" in pp_face,
            (graph, pp_face))
    graph_column = tuple(map(Q, graph["literal_graph_PP_column"]))
    all_d = tuple(map(Q, graph["retained_all_D_endpoint"]))
    candidate = tuple(map(Q, graph["desired_selected_db01"]))
    dual = tuple(map(Q, graph["primitive_dual"]))
    require(dot(dual, graph_column) == dot(dual, all_d) == 0
            and dot(dual, candidate) == 1,
            "the selected-db01 extension values changed")
    return {
        "literal_terms": db_ledger["literal_support"][
            "selected_db01_term_count"],
        "target_and_central_Eq": [0, 0],
        "relative_graph": "dz01-db01",
        "relative_graph_dual_values_db01_dz01": [1, 1],
        "old_rank_then_absolute_db01_rank": [2, 3],
        "all_D_is_the_graph_companion": False,
        "first_absolute_PP_column": (
            "selected db01, equivalently dc01=30db01-dR"
        ),
        "consequence_for_pure_safe_correction": (
            "the new Eq2/Eq3 and pure-target correction have zero pairing "
            "on db01, so the old occurrence separator extends unchanged"
        ),
    }


def direction_source_label_stage(joint) -> dict[str, object]:
    ledger, digest = joint.audit()
    require(digest == joint.EXPECTED_LEDGER_SHA256,
            "the joint primitive-C4 ledger changed")
    guard = ledger["smallest_complete_row_counterguard"]
    labels = ledger["physical_source_label_gate"]
    switches = guard["chart_switch_test"]
    require(guard["root_edge_rank"] == 9
            and guard["rank_after_complete_response_rows"] == 10
            and guard["rank_after_L01_direction_charge"] == 11
            and guard["dual"]["constant_chart_values_A_B_C"] == [2, -1, -1]
            and guard["dual"]["value_on_candidate"] == "6"
            and labels["root_cobar_edges_realized"] == 0
            and labels["profile_violations"] == 4
            and switches["only_A_plus_B_rank_then_with_candidate"] == [11, 12]
            and switches["only_A_plus_C_rank_then_with_candidate"] == [11, 12]
            and switches["both_switches_rank_then_with_candidate"] == [12, 12],
            (guard, labels))
    return {
        "direction_face_support": ledger["eighteen_direction_faces"]["support"],
        "chart_charge_A_B_C": [2, -1, -1],
        "tag_preserving_root_rank": 9,
        "rank_after_all_complete_rows": 10,
        "rank_with_direction_charge": 11,
        "normalized_detector_value": 1,
        "first_mixed_source_label_family": labels[
            "first_missing_physical_labels"],
        "one_switch_is_not_enough": True,
        "both_switches_fill_coefficient_charge": True,
        "rank_tests": switches,
        "why_current_root_square_cannot_supply_them": (
            "all four proposed edges change D/P/S/Q profile from DQ to PS; "
            "literal site-root edges preserve that profile"
        ),
        "first_unavoidable_rank_raising_family_after_strong_grants": (
            "the two source-provenant mixed chart arrows DQ<->P0S1 and "
            "DQ<->P1S0 on one fixed tail/window"
        ),
    }


def associated_graded_gluing_shadow(nonfill, psidelta) -> dict[str, object]:
    # Build one exact direct-sum covector on four audited quotient blocks.
    # Each bridge identifies the normalized balanced class with the normalized
    # representative in another block.  This proves the conditional terminal
    # statement once these are the actual exhaustive restriction maps; it does
    # not assert that the formal bridges are source-valid physical columns.

    # Old pure-safe augmented block.
    old_columns = tuple(value for _name, value in nonfill.cap_cartan_columns())
    old_columns += (nonfill.vector(target2=1), nonfill.vector(target3=1))
    z = nonfill.vector(**{
        **{f"B{corner}": nonfill.DELTA[corner] for corner in range(4)}
    })
    old_dual = nonfill.vector(**{
        **{f"B{corner}": nonfill.DELTA[corner] for corner in range(4)},
        "Eq2": 1, "Eq3": 1,
        "target0": -1, "target1": -1,
        "W0": -1, "W1": -1,
        "ores0": 1, "ores1": 1,
    })
    old_dual = tuple(value / 4 for value in old_dual)
    require(all(dot(old_dual, column) == 0 for column in old_columns)
            and dot(old_dual, z) == 1,
            "the normalized old block changed")

    # Selected db01 block.
    db_columns = ((Q(-1), Q(1), Q(0)), (Q(0), Q(0), Q(1)))
    db_candidate = (Q(1), Q(0), Q(0))
    db_dual = (Q(1), Q(1), Q(0))

    # Direction block: four words times chart tags A,B,C.
    words = ("00", "10", "01", "11")
    charts = ("A", "B", "C")
    coordinates = tuple((word, chart) for chart in charts for word in words)
    index = {coordinate: position for position, coordinate in enumerate(coordinates)}
    width = len(coordinates)
    root_edges = (("00", "10"), ("00", "01"),
                  ("10", "11"), ("01", "11"))
    direction_columns = []
    for chart in charts:
        for source, target in root_edges:
            direction_columns.append(vector(width, {
                index[(source, chart)]: -1,
                index[(target, chart)]: 1,
            }))
    for word in words:
        direction_columns.append(vector(width, {
            index[(word, chart)]: 1 for chart in charts
        }))
    direction_columns = tuple(direction_columns)
    direction_candidate = vector(width, {
        index[("00", "A")]: 2,
        index[("00", "B")]: -1,
        index[("00", "C")]: -1,
    })
    direction_dual = tuple(Q((2, -1, -1)[charts.index(chart)], 6)
                           for chart in charts for _word in words)
    require(all(dot(direction_dual, column) == 0
                for column in direction_columns)
            and dot(direction_dual, direction_candidate) == 1,
            "the normalized direction block changed")

    # Word-0102 occurrence block.
    chain_ledger, chain_digest = psidelta.audit()
    require(chain_digest == psidelta.EXPECTED_LEDGER_SHA256,
            "the psidelta chain changed")
    word = chain_ledger["downstream_word_0102"]
    private = tuple(map(Q, word["representative_private_vector"]))
    complete = (Q(1),) * len(private)
    word_raw_dual = tuple(Q(index in (0, 3)) - Q(index in (1, 6))
                          for index in range(len(private)))
    word_dual = tuple(Q(-6, 13) * value for value in word_raw_dual)
    require(dot(word_raw_dual, private) == Q(-13, 6)
            and dot(word_dual, complete) == 0
            and dot(word_dual, private) == 1,
            "the normalized word-0102 block changed")

    # Verify the direct-sum extension and three normalized bridge columns.
    widths = (len(z), len(db_candidate), len(direction_candidate), len(private))
    offsets = (0, widths[0], widths[0] + widths[1],
               widths[0] + widths[1] + widths[2])
    total = sum(widths)

    def embed(block: int, value):
        answer = [Q(0)] * total
        start = offsets[block]
        answer[start:start + widths[block]] = value
        return tuple(answer)

    full_dual = (old_dual + db_dual + direction_dual + word_dual)
    base = tuple(embed(0, value) for value in old_columns) \
        + tuple(embed(1, value) for value in db_columns) \
        + tuple(embed(2, value) for value in direction_columns) \
        + (embed(3, complete),)
    bridges = (
        tuple(a - b for a, b in zip(embed(0, z), embed(1, db_candidate),
                                    strict=True)),
        tuple(a - b for a, b in zip(embed(0, z),
                                    embed(2, direction_candidate), strict=True)),
        tuple(a - b for a, b in zip(embed(0, z), embed(3, private),
                                    strict=True)),
    )
    require(all(dot(full_dual, column) == 0 for column in base + bridges)
            and dot(full_dual, embed(0, z)) == 1,
            "the associated-graded glued terminal shadow changed")
    return {
        "blocks": [
            "cap/Cartan + both pure targets",
            "selected db01 relative graph",
            "tag-preserving direction square + complete rows",
            "word-0102 complete response line",
        ],
        "normalized_stage_values": [1, 1, 1, 1],
        "formal_normalized_bridges_annihilated": len(bridges),
        "global_shadow_dual_value_on_z": "1",
        "conditional_terminal_hypotheses": [
            "the four displayed blocks are exhaustive in the selected same word/fine/repeated/common-tail grade",
            "the only cross-block restriction/reinsertion columns are the audited normalized bridges and relative graph/product-rule columns",
            "R01/U_C4 and db01 occur relatively; no absolute carrier column is present",
            "the direction block contains no DQ<->PS mixed chart-switch column",
            "the lower P2/Q/ores block is exactly the committed relative graph plus the conditional response-gauge/d_even/scalar closure",
        ],
        "under_hypotheses": (
            "the displayed normalized covector is an exhaustive same-grade "
            "augmented terminal detecting z"
        ),
        "hypotheses_proved_for_full_physical_source": False,
        "first_way_to_break_shadow": (
            "an absolute carrier/db01 column, or a source-provenant DQ<->PS "
            "mixed chart-switch arrow"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    balance = load(
        "computations/verify_h3_balanced_square_pointed_full_q_cone_gate.py",
        "balanced_z_terminal_balance",
    )
    nonfill = load(
        "computations/verify_h3_gate_ii_chiw_nonfill_full_augmented_dual.py",
        "balanced_z_terminal_nonfill",
    )
    relative = load(
        "computations/verify_h3_gate_ii_three_cap_relative_tate_carrier_obstruction.py",
        "balanced_z_terminal_relative",
    )
    selected_db = load(
        "computations/verify_h3_selected_db01_normalized_gl3_bar_companion_gate.py",
        "balanced_z_terminal_db",
    )
    pp_tate = load(
        "computations/verify_h3_physical_pp_hasse_toric_tate_cofibrancy_gate.py",
        "balanced_z_terminal_pp",
    )
    joint = load(
        "computations/verify_h3_gate_ii_primitive_c4_joint_cobar_label_gate.py",
        "balanced_z_terminal_joint",
    )
    psidelta = load(
        "computations/verify_h3_gate_ii_psidelta_same_grade_extension_chain.py",
        "balanced_z_terminal_psidelta",
    )
    ledger = {
        "theorem": "h3 balanced-z relative ladder / conditional terminal gate",
        "pins": PINS,
        "pure_safe_start": pure_safe_start(balance, nonfill),
        "relative_top_PP_and_q_ladder":
            relative_top_and_lower_ladder(relative),
        "selected_db01": selected_db01_stage(selected_db, pp_tate),
        "direction_source_label_gate": direction_source_label_stage(joint),
        "conditional_exhaustive_terminal_shadow":
            associated_graded_gluing_shadow(nonfill, psidelta),
        "verdict": (
            "The pure-safe balanced detector extends unchanged through every "
            "currently constructed presentation-safe relative family.  At "
            "R01/U_C4 it is forced onto (t_R,t_L)=(-1,1); at selected db01 "
            "it is forced equally onto dz01; the first-PP value is entirely "
            "on the eighteen direction terms; the word-0102 graph forces "
            "C*d=12*d; and dq/Q cancellation leaves labelled ores -35/72 "
            "before the conditional response-gauge/d_even closure.  Absolute "
            "R01 or db01 is already the filler arm.  After granting their "
            "relative versions, the first source-provenant rank-raising "
            "family is the pair of mixed chart arrows DQ<->P0S1 and "
            "DQ<->P1S0.  Without those arrows the tag-preserving direction "
            "block has an exact normalized terminal detector.  A full "
            "augmented terminal follows under the displayed exhaustive "
            "same-grade gluing hypotheses, which remain unproved physically"
        ),
        "scope": (
            "exact canonical h3 rational cap/Cartan, selected first-PP, "
            "direction-square and word-0102 quotients, plus pinned relative "
            "P2/dq/Q/ores calculations.  The global glued covector is a "
            "conditional exhaustive terminal theorem, not a completed GHZ "
            "source terminal or counterexample"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("balanced-z terminal ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("freeze EXPECTED_LEDGER_SHA256=" + digest)
        return
    print("balanced z pure-safe dual: EXTENDS THROUGH RELATIVE LADDER")
    print("absolute R01/db01: FILLER ARM / BREAKS DUAL")
    print("first source-label rank raiser: TWO MIXED DQ<->PS ARROWS")
    print("0102 -> dq/Q/ores: FORCED VALUES, CONDITIONAL PHYSICAL GLUING")
    print("full terminal: CONDITIONAL ON EXHAUSTIVE SAME-GRADE GLUING")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
