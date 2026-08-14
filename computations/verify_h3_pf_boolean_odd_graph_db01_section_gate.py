#!/usr/bin/env python3
"""Test whether the pointed Boolean graph supplies the fixed-source u^-.

The single pointed P_f graph contains carriers u_S only for the marked
orientation.  Its endpoint-transpose copy contains u_{tau S} in the
conjugate word/head object.  In their full relative two-object presentation,
the normalized antisymmetric graph is exactly

    d b_S^- = (1_S-1_{tau S}) - (u_S-u_{tau S})/90.

Thus the doubled relative graph already has the desired presentation-safe
shape and preserves H0: u^- is a retained carrier pair, not a new source
axiom.  Canonical collapse to one transported object sends every such
difference to zero, so it is not a fixed-object W_odd boundary; that collapse
is unnecessary if Phi is defined on the relative carrier object.

Even with the top odd graph and its four labelled first faces, the selected
six-term db01 flag is an independent rank-one extension.  Its
centered 360-flag dual is the exact next obstruction.  Conditional on also
granting db01, the two root-labelled response-to-cap sections remain the
next independent operation block; their recorded source word and operation
are exactly those of this relative carrier domain.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_pointed_occurrence_edge_euler_boolean_cube_gate.py":
        "2b720f2a81d047454e224ec6af7ad62680c6ffeae33b6d7275cf995789bc8b8c",
    "computations/verify_h3_mixed_head_antisymmetric_quadratic_wodd_gate.py":
        "d2092477c3d0414e90bbc8ee9745b66560e72d0306d1e9d66eea0e35c1db3360",
    "computations/verify_h3_quadratic_occurrence_selector_hasse_odd_cut_no_go.py":
        "ac7f88b21976cae557ed6b4cacaeca19d5799ef7a30ac53df6dc0f0ab08b0f93",
    "computations/verify_h3_selected_db01_active_coloop_reinsertion_gate.py":
        "a08598e088c100e4b5116fb2b39717ec639116ea1fa7575062ba9a8f8cf9c683",
    "computations/verify_h3_double_collision_active_fan_hall_prolongation_gate.py":
        "c120ecac81f50b2d418fef91492dd79cb68c5eb5fb65d39dd5e3d7ddce029238",
    "computations/verify_h3_phi_ks_r0_pf_minimal_executable_ansatz_gate.py":
        "d21d776ec53babb4f99693e4dad51d87309e3ed0cccf2e34fb6025e6d74d1009",
}
EXPECTED_LEDGER_SHA256 = (
    "3967fa82057b0693306972462cf52395e505c5388e90718864104d348eca4795"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(coefficient: Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(coefficient) * Q(entry) for entry in vector)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def unit(width: int, index: int) -> tuple[Q, ...]:
    return tuple(Q(position == index) for position in range(width))


def rank(columns: tuple[tuple[Q, ...], ...] | list[tuple[Q, ...]]) -> int:
    if not columns:
        return 0
    columns = tuple(tuple(map(Q, column)) for column in columns)
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


def endpoint_transpose_edge(edge, euler):
    permutation = {euler.P: euler.S, euler.S: euler.P}
    return euler.edge(permutation.get(edge[0], edge[0]),
                      permutation.get(edge[1], edge[1]))


def endpoint_transpose_matching(matching, euler):
    return tuple(sorted(endpoint_transpose_edge(edge, euler)
                        for edge in matching))


def face_name(face, euler) -> str:
    return "|".join(
        "".join(euler.NAMES[vertex] for vertex in edge)
        for edge in face
    )


def boolean_odd_graph_audit(euler) -> tuple[dict[str, object], dict[str, object]]:
    matching_data, centered_faces = euler.matching_and_boolean_face_audit()
    require(matching_data["response_occurrences"] == 90
            and matching_data["nonempty_centered_faces"] == 15,
            "the pointed Boolean face inventory changed")
    occurrences = tuple(euler.OCCURRENCES)
    occurrence_index = {
        matching: index for index, matching in enumerate(occurrences)
    }
    tau = tuple(occurrence_index[endpoint_transpose_matching(matching, euler)]
                for matching in occurrences)
    require(all(tau[tau[index]] == index and tau[index] != index
                for index in range(len(tau))),
            "endpoint transpose stopped acting freely")

    nonempty = tuple(euler.subsets(euler.DIRECTIONS, include_empty=False))
    face_index = {face: index for index, face in enumerate(nonempty)}
    require(len(nonempty) == 15 and euler.DIRECTIONS in face_index,
            "the Boolean carrier index changed")
    complete = (Q(1),) * 90

    plus_centered = tuple(centered_faces[face] for face in nonempty)
    tau_faces = tuple(tuple(sorted(endpoint_transpose_edge(edge, euler)
                                   for edge in face))
                      for face in nonempty)
    tau_centered = []
    odd_indicators = []
    for face, tau_face, centered in zip(
            nonempty, tau_faces, plus_centered, strict=True):
        plus_indicator = euler.indicator(face)
        mate_indicator = euler.indicator(tau_face)
        mate_support = sum(mate_indicator, Q(0))
        plus_support = sum(plus_indicator, Q(0))
        require(mate_support == plus_support,
                (face, plus_support, mate_support))
        mate_centered = add(scale(90, mate_indicator),
                            scale(-mate_support, complete))
        odd = add(plus_indicator, scale(-1, mate_indicator))
        require(add(centered, scale(-1, mate_centered)) == scale(90, odd),
                "the normalized centered odd difference changed")
        tau_centered.append(mate_centered)
        odd_indicators.append(odd)
    tau_centered = tuple(tau_centered)
    odd_indicators = tuple(odd_indicators)

    # The existing single P_f graph has V plus fifteen private carriers.
    # Its columns are R and C_S-u_S and have H0=89.
    single_width = 90 + 15
    single_complete = complete + (Q(0),) * 15
    plus_graphs = tuple(
        centered + scale(-1, unit(15, index))
        for index, centered in enumerate(plus_centered)
    )
    single_columns = (single_complete, *plus_graphs)
    require(rank(single_columns) == 16
            and single_width - rank(single_columns) == 89,
            "the existing single P_f graph changed")

    # The full relative presentation is the direct sum of the two complete
    # mapping cylinders.  Its antisymmetric graph is literally a difference
    # of old columns, so no new source generator is needed.
    relative_width = 2 * single_width
    relative_plus = tuple(column + (Q(0),) * single_width
                          for column in single_columns)
    tau_complete = complete + (Q(0),) * 15
    tau_graphs_single = tuple(
        centered + scale(-1, unit(15, index))
        for index, centered in enumerate(tau_centered)
    )
    relative_tau = tuple((Q(0),) * single_width + column
                         for column in (tau_complete, *tau_graphs_single))
    relative_columns = (*relative_plus, *relative_tau)
    require(rank(relative_columns) == 32
            and relative_width - rank(relative_columns) == 178,
            "the doubled relative Boolean presentation changed")
    relative_odd_graphs = tuple(
        scale(Q(1, 90), add(relative_plus[1 + index],
                            scale(-1, relative_tau[1 + index])))
        for index in range(15)
    )
    require(all(rank((*relative_columns, graph)) == 32
                for graph in relative_odd_graphs),
            "an antisymmetric graph left the relative presentation span")

    # A nontransported fixed-object display uses one occurrence block and
    # two separately labelled carrier blocks.  It is useful as the
    # coefficient shadow, but is not needed for the relative Phi domain.
    doubled_width = 90 + 15 + 15
    doubled_complete = complete + (Q(0),) * 30
    doubled_plus = tuple(
        centered + scale(-1, unit(15, index)) + (Q(0),) * 15
        for index, centered in enumerate(plus_centered)
    )
    doubled_tau = tuple(
        centered + (Q(0),) * 15 + scale(-1, unit(15, index))
        for index, centered in enumerate(tau_centered)
    )
    doubled_columns = (doubled_complete, *doubled_plus, *doubled_tau)
    require(rank(doubled_columns) == 31
            and doubled_width - rank(doubled_columns) == 89,
            "the doubled raw fixed graph stopped preserving H0")

    normalized_odd_graphs = tuple(
        scale(Q(1, 90), add(plus, scale(-1, mate)))
        for plus, mate in zip(doubled_plus, doubled_tau, strict=True)
    )
    for index, graph in enumerate(normalized_odd_graphs):
        expected = (
            odd_indicators[index]
            + scale(Q(-1, 90), unit(15, index))
            + scale(Q(1, 90), unit(15, index))
        )
        require(graph == expected,
                ("the normalized odd graph changed", index))

    # Retain only the top and its four labelled codimension-one faces.  A
    # presentation-safe fixed-source model needs one new odd normal for each.
    top = euler.DIRECTIONS
    first_faces = tuple(tuple(edge for edge in top if edge != deleted)
                        for deleted in top)
    retained = (top, *first_faces)
    retained_indices = tuple(face_index[face] for face in retained)
    require(len(set(retained_indices)) == 5,
            "top/first-face Boolean labels collided")
    minimal_width = single_width + 5
    old_extended = tuple(column + (Q(0),) * 5
                         for column in single_columns)
    primitive_graphs = []
    for new_index, boolean_index in enumerate(retained_indices):
        primitive_graphs.append(
            odd_indicators[boolean_index]
            + (Q(0),) * 15
            + scale(-1, unit(5, new_index))
        )
    require(rank(old_extended) == 16
            and rank((*old_extended, *primitive_graphs)) == 21
            and minimal_width - rank((*old_extended, *primitive_graphs)) == 89,
            "the five-face primitive odd graph stopped preserving H0")

    # Exact single-cube dual: after adjoining an empty coordinate for the
    # proposed top u^-, its coordinate functional kills the entire old cube
    # and reads -1 on the desired primitive graph.
    top_normal_dual = unit(minimal_width, single_width)
    require(all(dot(top_normal_dual, column) == 0
                for column in old_extended)
            and dot(top_normal_dual, primitive_graphs[0]) == -1,
            "the new odd-normal dual changed")

    # In the honest two-object complex each object has its own 105 rows.
    # Canonical transport applies tau to the occurrence block and identifies
    # the corresponding carrier labels.  Every antisymmetric graph pair
    # therefore maps to zero.
    def transport_tau_centered(vector: tuple[Q, ...]) -> tuple[Q, ...]:
        answer = [Q(0)] * 90
        for position, value in enumerate(vector):
            answer[tau[position]] += value
        return tuple(answer)

    canonical_images = []
    for centered, mate in zip(plus_centered, tau_centered, strict=True):
        transported_mate = transport_tau_centered(mate)
        canonical_images.append(add(centered, scale(-1, transported_mate)))
    require(all(not any(image) for image in canonical_images),
            "a two-object odd graph acquired a canonical fixed-source image")

    labels = []
    for face, tau_face in zip(
            (nonempty[index] for index in retained_indices),
            (tau_faces[index] for index in retained_indices), strict=True):
        labels.append({
            "plus_fine": face_name(face, euler),
            "transpose_fine": face_name(tau_face, euler),
            "normalized_boundary": (
                f"1_[{face_name(face, euler)}]-"
                f"1_[{face_name(tau_face, euler)}]-u^-"
            ),
        })

    data = {
        "existing_single_Pf_graph": {
            "coordinates": single_width,
            "columns": len(single_columns),
            "rank": rank(single_columns),
            "H0": single_width - rank(single_columns),
            "carriers": "u_S for 15 nonempty faces of f only",
            "contains_u_minus_by_itself": False,
        },
        "full_relative_plus_transpose_presentation": {
            "coordinates": relative_width,
            "rank": rank(relative_columns),
            "H0": relative_width - rank(relative_columns),
            "normalized_carrier_pair":
                "u_S^-=(u_S,-u_tauS)/90 in O_plus direct-sum O_tau",
            "all_15_odd_graphs_in_existing_column_span": True,
            "presentation_safe": True,
            "new_source_generator_required": False,
        },
        "formal_raw_doubled_graph": {
            "coordinates": doubled_width,
            "rank": rank(doubled_columns),
            "H0": doubled_width - rank(doubled_columns),
            "normalized_carrier": "u_S^-=(u_S-u_tauS)/90",
            "normalized_boundary":
                "d b_S^-=(1_S-1_tauS)-u_S^-",
            "algebraically_constructed": True,
            "role": "nontransported fixed-object coefficient display",
        },
        "honest_two_object_descent": {
            "objects": ["(w,01,Q01)", "(tau w,10,Q10)"],
            "canonical_image_rank_of_all_15_odd_graph_pairs":
                rank(canonical_images),
            "canonical_image": 0,
        },
        "minimal_top_plus_four_face_extension": {
            "new_normals": 5,
            "new_graph_relations": 5,
            "rank_before_after": [16, 21],
            "H0_before_after": [89, 89],
            "retained_labelled_boundaries": labels,
            "top_new_normal_dual_on_old_and_required": [0, -1],
        },
        "source_verdict": (
            "The full relative Boolean presentation already supplies u^- "
            "as the normalized antisymmetric retained carrier pair and "
            "supplies its four first face pairs.  It is not a new source "
            "axiom.  Only a collapse to one fixed transported object would "
            "need a new odd normal; Phi may instead take this relative "
            "carrier itself as its domain."
        ),
    }
    blocks = {
        "minimal_columns": tuple((*old_extended, *primitive_graphs)),
        "minimal_width": minimal_width,
    }
    return data, blocks


def db01_next_dual_audit(db01, db_ledger: dict[str, object],
                         blocks: dict[str, object]) \
        -> tuple[dict[str, object], dict[str, object]]:
    guard = db_ledger["maximal_termwise_full_label_counterguard"]
    require(guard["rank_before_after_selected_db01"] == [181, 182]
            and guard["response_flags"] == 180,
            "the selected-db01 interface changed")

    flag_count = 180
    flag_width = 360
    response_complete = tuple(Q(index < flag_count)
                              for index in range(flag_width))
    target_complete = tuple(Q(index >= flag_count)
                            for index in range(flag_width))
    graphs = tuple(
        add(scale(-1, unit(flag_width, index)),
            unit(flag_width, flag_count + index))
        for index in range(flag_count)
    )
    old = (*graphs, response_complete, target_complete)
    selected = tuple(Q(index < 6) for index in range(flag_width))
    centered_dual = tuple(Q(29 if index % flag_count < 6 else -1)
                          for index in range(flag_width))
    require(rank(old) == 181 and rank((*old, selected)) == 182
            and all(dot(centered_dual, column) == 0 for column in old)
            and dot(centered_dual, selected) == 174,
            "the 360-flag selected-db01 dual changed")

    odd_columns = tuple(blocks["minimal_columns"])
    odd_width = int(blocks["minimal_width"])
    combined_old = tuple(column + (Q(0),) * flag_width
                         for column in odd_columns)
    combined_old += tuple((Q(0),) * odd_width + column for column in old)
    selected_combined = (Q(0),) * odd_width + selected
    combined_dual = (Q(0),) * odd_width + centered_dual
    before = rank(combined_old)
    after = rank((*combined_old, selected_combined))
    require((before, after) == (202, 203)
            and all(dot(combined_dual, column) == 0
                    for column in combined_old)
            and dot(combined_dual, selected_combined) == 174,
            "the odd graph unexpectedly supplied selected db01")
    data = {
        "odd_graph_rank": 21,
        "db01_named_rank": 181,
        "combined_rank_before_after_selected_db01": [before, after],
        "exact_next_dual": {
            "support": (
                "29 on each of the six selected response/carrier flags and "
                "-1 on each of the other 174 flags in both halves"
            ),
            "on_odd_graph_and_all_named_termwise_columns": 0,
            "on_selected_six_term_db01": 174,
        },
        "first_missing_after_formal_odd_graph": (
            "one termwise PP-natural selected six-term db01 incidence of "
            "the same top cell"
        ),
        "root_sections_reached": False,
    }
    return data, {
        "columns_after_conditional_db01":
            tuple((*combined_old, selected_combined)),
        "width_after_conditional_db01": odd_width + flag_width,
    }


def minimal_ps_over_q_constructor_audit(
        db_ledger: dict[str, object],
        collision_ledger: dict[str, object]) -> dict[str, object]:
    physical = db_ledger["literal_PP_and_reinsertion_faces"][
        "physical_endpoint_insertion"]
    recurrence = collision_ledger["committed_recurrence_scope"][
        "double_collision_face_block"]
    survivor = collision_ledger["finite_endpoint_odd_counterguard"]
    require(physical["top_type"] == "P4+2K2"
            and physical["face_counts"]
                == {"endpoint_dp_ds": 6, "tail_q_db01": 6,
                    "dq01_companion": 3}
            and recurrence["live_families"] == {"P4+K2": 6, "4K2": 3}
            and survivor["rank_before_after_selected_B_packet"] == [27, 28],
            "the double-collision constructor interface changed")

    # Nine paired first-jet faces: six tail removals and three dq01 faces.
    # For each face retain source B,C and exit B,C.  The very generous old
    # inventory has recurrence graphs for B and C plus complete even rows at
    # source and exit.  One endpoint-odd source row is the minimal absolute
    # PS/q constructor: together with B+C it gives selected B exactly.
    faces = 9
    width = 4 * faces

    def position(block: int, face: int) -> int:
        return block * faces + face

    def vector(values: dict[int, int]) -> tuple[Q, ...]:
        return tuple(Q(values.get(index, 0)) for index in range(width))

    old = []
    for face in range(faces):
        old.extend((
            vector({position(0, face): -1, position(2, face): 1}),
            vector({position(1, face): -1, position(3, face): 1}),
            vector({position(0, face): 1, position(1, face): 1}),
            vector({position(2, face): 1, position(3, face): 1}),
        ))
    old = tuple(old)
    selected_b = vector({position(0, face): 1 for face in range(faces)})
    odd_source = vector({
        **{position(0, face): 1 for face in range(faces)},
        **{position(1, face): -1 for face in range(faces)},
    })
    complete_source = vector({
        **{position(0, face): 1 for face in range(faces)},
        **{position(1, face): 1 for face in range(faces)},
    })
    require(rank(old) == 27 and rank((*old, selected_b)) == 28
            and rank((*old, odd_source)) == 28
            and rank((*old, odd_source, selected_b)) == 28
            and selected_b == scale(Q(1, 2), add(complete_source, odd_source)),
            "the minimal endpoint-odd constructor stopped filling selected B")

    # Deleting any one of the three physical factor types from the proposed
    # top records the exact first product-rule inventory.  The B and C
    # orientations are paired with opposite sign.
    product_rule = {
        "endpoint_dB_minus_dC": {
            "formula": (
                "[(dp0)s1+p0(ds1)-(dp1)s0-p1(ds0)]*q01*H2345"
            ),
            "literal_flags_per_orientation": 6,
            "signed_pairs": 6,
            "cofactor_type": "P3+2K2",
            "status": "all six signed pairs may be granted fan exits",
        },
        "tail_q01_dH": {
            "formula": "(p0s1-p1s0)*q01*dH2345",
            "literal_flags_per_orientation": 6,
            "signed_pairs": 6,
            "cofactor_type": "P4+K2",
            "status": "not in the existing 3K2/P3+K2 PP fan",
        },
        "dq01_companion": {
            "formula": "(p0s1-p1s0)*dq01*H2345",
            "literal_flags_per_orientation": 3,
            "signed_pairs": 3,
            "cofactor_type": "4K2",
            "status": "not in the existing 3K2/P3+K2 PP fan",
        },
    }
    return {
        "minimal_constructor_API": {
            "name": "PSQJet_01",
            "domain": (
                "the existing relative Boolean odd carrier u_f^- and its "
                "top/four-face packet"
            ),
            "top": "(p0*s1-p1*s0)*q01*H2345",
            "top_type": "endpoint-odd P4+2K2 first jet",
            "word_head": "11:110000 with ordered 01/10 response heads",
            "operation": "absolute PS-over-q01 restriction/insertion",
            "repeated_sites": [0, 1],
            "normalization": "q01*H2345=1",
            "absolute_selected_endpoint": (
                "selected B=(complete (B+C)+odd (B-C))/2; its tail "
                "projection is the six-term db01 packet"
            ),
        },
        "full_first_product_rule": product_rule,
        "exact_rank_certificate": {
            "old_recurrence_even_rank": 27,
            "rank_after_selected_B": 28,
            "rank_after_PSQJet_01_odd_row": 28,
            "rank_after_odd_row_then_selected_B": 28,
            "selected_B_formula": "B=(B+C+B-C)/2",
        },
        "obstruction_classification": {
            "scalar_localization_only": (
                "fails first at the operation idempotent: pure-coloop DQ "
                "does not become selected response PS"
            ),
            "physical_endpoint_insertion": (
                "repairs the operation tag but necessarily enters the "
                "repeated-site P4+2K2 fine block"
            ),
            "termwise_reinsertion": (
                "all relative flag graphs may be granted; they preserve "
                "endpoint orientation and leave the odd class"
            ),
            "first_genuine_missing_atom": (
                "an absolute endpoint-orientation-asymmetric PS/q "
                "restriction-insertion first-jet cell with all six P4+K2 "
                "and three 4K2 signed companion pairs"
            ),
            "primary_failure": "lack of an absolute PS/q restriction cell",
            "not_merely": [
                "a scalar unit", "an unlabelled Kahler identity",
                "another relative reinsertion graph",
                "an ordinary coefficient-support Hall recurrence",
            ],
        },
    }


def conditional_root_section_audit(ansatz, conditional: dict[str, object]) -> dict[str, object]:
    old, sections, paired_dual = ansatz.build_section_block()
    require(rank(old) == 4 and rank((*old, *sections)) == 6
            and all(dot(paired_dual, column) == 0 for column in old)
            and dot(paired_dual, add(*sections)) == 1,
            "the root-section block changed")
    previous_columns = tuple(conditional["columns_after_conditional_db01"])
    previous_width = int(conditional["width_after_conditional_db01"])
    combined_old = tuple(column + (Q(0),) * 10 for column in previous_columns)
    combined_old += tuple((Q(0),) * previous_width + column for column in old)
    section_columns = tuple((Q(0),) * previous_width + column
                            for column in sections)
    global_dual = (Q(0),) * previous_width + paired_dual
    before = rank(combined_old)
    after = rank((*combined_old, *section_columns))
    require(after == before + 2
            and all(dot(global_dual, column) == 0 for column in combined_old)
            and dot(global_dual, add(*section_columns)) == 1,
            "the conditional root-section separator changed")
    return {
        "scope": "conditional on separately granting selected db01",
        "rank_before_after_two_root_sections": [before, after],
        "paired_operation_dual_on_old_and_required": [0, 1],
        "section_word": "11110000 -> 01211222",
        "section_operation": "response occurrence/KS -> AugP2/K_Eq cap r0",
        "relative_u_minus_domain_word": "11110000 = 11:110000",
        "relative_u_minus_domain_operation": "response occurrence/P_f graph",
        "recorded_source_interface_matches": True,
        "interpretation_of_response_identity":
            "the root-labelled copy of the retained antisymmetric u^- carrier",
        "literal_head_fine_map_constructed": False,
        "supplied_by_odd_Boolean_graph": False,
        "consequence": (
            "the minimal Phi sections are exactly the two intended receiving "
            "arrows for the relative u^- domain at the recorded word and "
            "operation interface.  Their columns, including the literal "
            "head/fine incidence, are not supplied by the Boolean graph."
        ),
    }


def dependency_scope_audit() -> dict[str, object]:
    # The dependencies are byte-pinned above.  Their load-bearing
    # interfaces are replayed directly in this checker: the 15 Boolean
    # graph pairs, the 360 db01 flags, the nine-face collision packet, and
    # the two-root section block.  Avoid recursively replaying their full
    # ledgers here; those ledgers import each other and add no new equation.
    return {
        "mixed_head_scalar_target": 0,
        "existing_Pf_cube_status": "H0-preserving formal relative graph",
        "selected_db01_status": "independent termwise full-label flag",
        "root_section_status": "independent operation/word comparison",
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    euler = load(
        "computations/verify_h3_pointed_occurrence_edge_euler_boolean_cube_gate.py",
        "pf_odd_graph_euler",
    )
    db01 = load(
        "computations/verify_h3_selected_db01_active_coloop_reinsertion_gate.py",
        "pf_odd_graph_db01",
    )
    double_collision = load(
        "computations/verify_h3_double_collision_active_fan_hall_prolongation_gate.py",
        "pf_odd_graph_double_collision",
    )
    ansatz = load(
        "computations/verify_h3_phi_ks_r0_pf_minimal_executable_ansatz_gate.py",
        "pf_odd_graph_ansatz",
    )

    boolean_data, blocks = boolean_odd_graph_audit(euler)
    db_ledger, db_digest = db01.audit()
    collision_ledger, collision_digest = double_collision.audit()
    require(db_digest == db01.EXPECTED_LEDGER_SHA256
            and collision_digest == double_collision.EXPECTED_LEDGER_SHA256,
            "a selected-db01 constructor dependency changed")
    db_data, conditional = db01_next_dual_audit(db01, db_ledger, blocks)
    ledger = {
        "theorem": "h3 P_f Boolean odd graph to db01/section gate",
        "pins": PINS,
        "Boolean_carrier_comparison": boolean_data,
        "first_next_full_label_dual": db_data,
        "minimal_selected_db01_constructor":
            minimal_ps_over_q_constructor_audit(db_ledger, collision_ledger),
        "conditional_root_section_gate":
            conditional_root_section_audit(ansatz, conditional),
        "dependency_scope": dependency_scope_audit(),
        "verdict": (
            "The full relative sum of the pointed Boolean graph and its "
            "endpoint-transpose copy already contains the desired u^- and "
            "all four first face graphs as normalized antisymmetric retained "
            "carrier pairs.  This is presentation-safe and needs no new "
            "source generator.  Canonical collapse to one transported object "
            "kills them, but Phi can use the relative carrier as its domain. "
            "The selected six-term db01 block nevertheless raises rank "
            "202 to 203 and is detected by the centered 360-flag dual of "
            "value 174.  The minimal column which kills it is the endpoint-"
            "odd PSQJet_01 row: its P4+2K2 product rule has six signed "
            "P4+K2 tail pairs and three signed 4K2 dq01 pairs.  This "
            "identifies the primary failure as absence of an absolute PS/q "
            "restriction-insertion cell, not absence of another relative "
            "carrier.  Conditional on granting db01, the two root-labelled "
            "response-to-cap sections have exactly the receiving word and "
            "operation type, but their physical head/fine columns remain "
            "independently missing."
        ),
        "shortest_positive_datum": (
            "PSQJet_01, an endpoint-odd absolute PS-over-q01 first-jet map "
            "from the existing relative Boolean carrier.  Its boundary is "
            "the selected six-term db01 incidence plus six P4+K2, three "
            "4K2, and the endpoint product-rule mate families.  After that, "
            "construct the two root-labelled receiving sections from this "
            "carrier to the tied r0 cap."
        ),
        "scope": (
            "exact rational h=3 occurrence/Boolean-carrier, 360-flag db01 "
            "and root-section direct-sum audit.  The raw doubled graph is a "
            "formal construction, not a claimed physical source fold; the "
            "db01 covector is not promoted here to a global terminal."
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
    print("P_f plus transpose relative graph: u^- AND FOUR FACES EXIST")
    print("canonical two-object descent: ZERO")
    print("new relative source generator required: NO")
    print("optional five-normal fixed extension: H0 89 -> 89")
    print("next exact dual: SELECTED db01; rank 202 -> 203; value 174")
    print("conditional next atom: TWO ROOT RESPONSE->CAP SECTIONS")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
