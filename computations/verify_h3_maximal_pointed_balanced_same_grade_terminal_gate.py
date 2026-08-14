#!/usr/bin/env python3
"""Assemble the maximal named h=3 pointed/balanced literal map.

This checker keeps four literal blocks distinct:

* the 90-occurrence pointed Boolean response presentation;
* the selected db01 principal-parts graph;
* the 48-coordinate fixed-window word/chart/matching packet; and
* the 27-coordinate augmented cap packet.

The first three live in response or intermediate word/fine/repeated grades.
They have zero projection to the final augmented rows (B0,...,B3,
Eq0,...,Eq3) until a physical word-changing placement is supplied.  The
known cap packet has projected rank seven and unique primitive detector

    Psi = delta.(B-Eq),       delta=(1,1,-1,-1).

Every named literal family kills Psi.  Thus the normalized balanced dual
extends across the maximal named map.  The exact finite test on any omitted
column c is the one scalar delta.(B(c)-Eq(c)).  The first unmodeled family
which can make that scalar nonzero is the occurrence-local response-to-
AugP2 PP mapping cylinder, specifically its mixed reduced-Eq/private
incidence.  A bare response R01/L01/db01 or direction face is off-grade and
does not count as such a column.

The checker also constructs the exact normalized occurrence dual on the
relative Boolean graph, extends it through the direct-free R01/L01 and
selected-fibre graphs, and verifies a blockwise normalized compatibility
covector.  That compatibility covector is not called a physical terminal:
the cross-word column which would identify its blocks is exactly what is
missing.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_pointed_occurrence_edge_euler_boolean_cube_gate.py":
        "2b720f2a81d047454e224ec6af7ad62680c6ffeae33b6d7275cf995789bc8b8c",
    "computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py":
        "2ac01c9ba571338b4c7b779dbc70d5d0eaacb2fe01a4035833970fa6b9826fe0",
    "computations/verify_h3_balanced_square_private_eq_projection_gate.py":
        "bbfb690a73844169574351ad019171a6d9c5fe332e59cc9694a1f67dcf31cf8e",
    "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py":
        "bd3f008eb2faf00bbebccb09ef9692908f2e0ae4a795706de2c32f0b2ef342af",
    "computations/verify_h3_selected_db01_normalized_gl3_bar_companion_gate.py":
        "620b3e54e8e6ee09a0b616d0259c8d109b0359645b20d35db5fb876c8e7e0311",
    "computations/verify_h3_gate_ii_three_cap_relative_tate_carrier_obstruction.py":
        "0be2bde12d3d4b85cad67b4a647b4cb4f7e89ed1a04bff14f6091eb257224dcc",
}
EXPECTED_LEDGER_SHA256 = "6e223c587ea94e9544c5ddf711fc16dabc786158da5f9930643e7411dee2afb0"


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


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


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


def embed(vector, before, after):
    return (Q(0),) * before + tuple(map(Q, vector)) + (Q(0),) * after


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def pointed_boolean_and_top_faces(boolean, relative):
    matching_ledger, centered_faces = (
        boolean.matching_and_boolean_face_audit()
    )
    graph_ledger = boolean.relative_graph_audit(centered_faces)
    require(matching_ledger["response_occurrences"] == 90
            and matching_ledger["nonempty_centered_faces"] == 15
            and graph_ledger["minimal_label_faithful_relative_cube_graph"]
                ["boundary_rank"] == 16,
            "the pointed Boolean presentation changed")

    nonempty = boolean.subsets(boolean.DIRECTIONS, include_empty=False)
    complete = (Q(1),) * len(boolean.OCCURRENCES)
    top = centered_faces[boolean.DIRECTIONS]
    top_norm = dot(top, top)
    require(top_norm == 90 * 89, top_norm)
    old_dual = scale(Q(1, top_norm), top)
    carrier_values = tuple(dot(old_dual, centered_faces[face])
                           for face in nonempty)

    width = len(boolean.OCCURRENCES) + len(nonempty)
    complete_column = complete + (Q(0),) * len(nonempty)
    boolean_graphs = []
    for carrier, face in enumerate(nonempty):
        tail = [Q(0)] * len(nonempty)
        tail[carrier] = -1
        boolean_graphs.append(centered_faces[face] + tuple(tail))
    boolean_dual = old_dual + carrier_values
    require(dot(boolean_dual, complete_column) == 0
            and all(dot(boolean_dual, column) == 0
                    for column in boolean_graphs),
            "the normalized pointed dual stopped extending over the cube")
    top_carrier = nonempty.index(boolean.DIRECTIONS)
    require(carrier_values[top_carrier] == 1,
            "the pointed top normalization changed")

    # Restrict the full local three-chart top to the direct-free response.
    # A=D*q01 is the omitted direct-edge chart.  B and C are the two
    # endpoint fibres, each with three residual C4 matchings.
    P, S, ZERO, ONE = 0, 1, 2, 3
    p0, s1 = boolean.edge(P, ZERO), boolean.edge(S, ONE)
    p1, s0 = boolean.edge(P, ONE), boolean.edge(S, ZERO)
    b01 = tuple(Q(p0 in matching and s1 in matching)
                for matching in boolean.OCCURRENCES)
    c10 = tuple(Q(p1 in matching and s0 in matching)
                for matching in boolean.OCCURRENCES)
    require(sum(b01, Q(0)) == sum(c10, Q(0)) == 3
            and dot(b01, c10) == 0,
            "the two endpoint fibres changed")
    r01_restricted = add(b01, c10)
    l01_restricted = scale(-1, r01_restricted)
    values = {
        "b01": dot(old_dual, b01),
        "c10": dot(old_dual, c10),
        "R01_restricted": dot(old_dual, r01_restricted),
        "L01_restricted": dot(old_dual, l01_restricted),
    }
    require(values == {
        "b01": Q(29, 2670),
        "c10": Q(-1, 2670),
        "R01_restricted": Q(14, 1335),
        "L01_restricted": Q(-14, 1335),
    }, values)

    # Add presentation-safe retained coordinates t_R,t_L,t_B.  These are
    # coefficient graphs, not physical absolute R01/L01/db01 columns.
    added = 3
    extended_width = width + added
    extend_old = lambda value: tuple(value) + (Q(0),) * added
    columns = [extend_old(complete_column)]
    columns.extend(extend_old(column) for column in boolean_graphs)
    for offset, response_value in enumerate(
            (r01_restricted, l01_restricted, b01)):
        entries = list(response_value) + [Q(0)] * len(nonempty) + [Q(0)] * added
        entries[width + offset] = -1
        columns.append(tuple(entries))
    extended_dual = (boolean_dual
                     + (values["R01_restricted"],
                        values["L01_restricted"], values["b01"]))
    require(len(columns) == 19
            and rank(tuple(columns)) == 19
            and extended_width - rank(tuple(columns)) == 89
            and all(dot(extended_dual, column) == 0 for column in columns),
            "the pointed top/RL/B graph extension changed")

    relative_ledger, relative_digest = relative.audit()
    require(relative_digest == relative.EXPECTED_LEDGER_SHA256
            and relative_ledger["top_three_cap"]
                ["presentation_safe_relative_graph"]["graph_rank"] == 2
            and relative_ledger["first_PP"]["dL01_support"] == 36
            and relative_ledger["first_PP"]["normalized_dual_values"]
                ["endpoint_direction_18"] == "1",
            "the complete R01/L01/18-face packet changed")

    return tuple(columns), extended_dual, {
        "coordinates": extended_width,
        "columns": len(columns),
        "rank": rank(tuple(columns)),
        "H0": extended_width - rank(tuple(columns)),
        "response_occurrences": 90,
        "Boolean_face_carriers": 15,
        "extra_retained_carriers": ["t_R", "t_L", "t_B"],
        "normalized_pointed_dual_reads_u_f": "1",
        "forced_values": {name: str(value) for name, value in values.items()},
        "complete_three_cap": {
            "R01_L01_graphs": 2,
            "complete_PP_coordinates": relative_ledger["first_PP"]
                ["complete_PP_coordinates"],
            "dL01_support": relative_ledger["first_PP"]["dL01_support"],
            "split": relative_ledger["first_PP"]["split"],
        },
        "scope": (
            "the direct-free restriction sees B+C and omits the direct A "
            "chart; all retained top faces are relative coefficient graphs"
        ),
    }


def selected_db01_block(db01):
    ledger, digest = db01.audit()
    require(digest == db01.EXPECTED_LEDGER_SHA256
            and ledger["graph_and_bicomplex"]["rank_before_then_after_db01"]
                == [2, 3],
            "the selected db01 graph changed")
    # Coordinate order (db01,dz01,all-D).  The relative graph and all-D
    # endpoint are old columns; absolute db01 is the first PP filler.
    graph = (Q(-1), Q(1), Q(0))
    all_d = (Q(0), Q(0), Q(1))
    candidate = (Q(1), Q(0), Q(0))
    dual = (Q(1), Q(1), Q(0))
    require(rank((graph, all_d)) == 2
            and rank((graph, all_d, candidate)) == 3
            and dot(dual, graph) == dot(dual, all_d) == 0
            and dot(dual, candidate) == 1,
            "the normalized db01 dual changed")
    return (graph, all_d), dual, {
        "coordinates": 3,
        "columns": 2,
        "rank": 2,
        "selected_db01_terms": ledger["literal_support"]
            ["selected_db01_term_count"],
        "normalized_dual_on_absolute_db01": "1",
        "absolute_db01_constructed": False,
    }


def fixed_window_block(k22):
    columns, detector, candidate_h, candidate_r, packet = (
        k22.audit_cartesian_physical_packet()
    )
    direction = k22.audit_direction_routing(detector, candidate_h, candidate_r)
    switches = k22.audit_operation_switch_boundary(
        columns, candidate_h, candidate_r)
    values = tuple(value for _name, value in columns)
    normalized = scale(Q(1, 6), detector)
    require(len(values) == 100 and rank(values) == 46
            and all(dot(normalized, value) == 0 for value in values)
            and dot(normalized, candidate_h) == 1
            and direction["detector_value_before_after_relative_transport"]
                == ["12", "12"],
            "the normalized fixed-window detector changed")
    return values, normalized, {
        "coordinates": packet["physical_output_coordinates"],
        "columns": packet["internal_boundary_columns"],
        "rank": packet["internal_rank"],
        "cokernel_dimension": packet["cokernel_dimension"],
        "families": [
            "all tag-preserving two-root word edges",
            "both C4 matching differences",
            "all complete response rows",
            "all relative H-r graphs and their word/response faces",
        ],
        "R01_L01_chart_basis": ["A=D*q01", "B=p0*s1", "C=p1*s0"],
        "direction_terms": 18,
        "direction_primitive_profile": [2, 2, -1, -1, -1, -1],
        "normalized_detector_on_L_times_H": "1",
        "normalized_detector_on_18_direction_terms": "2",
        "operation_switch_boundary": switches["projected_missing_row_families"],
        "rank_base_one_switch_candidate": switches[
            "rank_base_one_switch_candidate"],
        "rank_base_two_switches_candidate": switches[
            "rank_base_two_switches_candidate"],
    }


def cap_named_columns(private_eq):
    columns = []
    names = []
    for corner in range(4):
        e = tuple(1 if index == corner else 0 for index in range(4))
        columns.extend((
            private_eq.vec(B=e, Eq=e, target=e, M=-1, ainc=-1, Pf=1),
            private_eq.vec(target=e, W=tuple(-value for value in e)),
            private_eq.vec(W=e, ores=e),
        ))
        names.extend((f"r0_{corner}", f"T_{corner}", f"rho_{corner}"))
    alpha = (-1, 1, 1, -1)
    columns.append(private_eq.vec(ores=alpha, ridge=1, eta=1, sigma=-1))
    names.append("Cartan")
    for positive in (0, 1):
        for negative in (2, 3):
            shore_edge = tuple(1 if index in (positive, negative) else 0
                               for index in range(4))
            columns.append(private_eq.vec(B=shore_edge))
            names.append(f"companion_{positive}_{negative}")
    columns.extend((
        private_eq.vec(target=(0, 0, 1, 0)),
        private_eq.vec(target=(0, 0, 0, 1)),
        private_eq.vec(M=1, ainc=-1, q=-1),
        private_eq.vec(Pf=1),
        private_eq.vec(ridge=1),
        private_eq.vec(eta=1),
        private_eq.vec(sigma=1),
        private_eq.vec(B=alpha, Eq=alpha, ores=alpha,
                       ridge=1, eta=1, sigma=-1),
    ))
    names.extend(("pure_target_2", "pure_target_3", "literal_q_identity",
                  "pointed_anchor", "ridge_only", "eta_only", "sigma_only",
                  "M_v"))
    require(len(columns) == len(names) == 25, len(columns))
    return tuple(columns), tuple(names)


def augmented_private_eq_block(private_eq):
    ledger, digest = private_eq.audit()
    require(digest == private_eq.EXPECTED_LEDGER_SHA256
            and ledger["projection"]["old_projection_rank"] == 7,
            "the private/Eq projection theorem changed")
    columns, names = cap_named_columns(private_eq)
    delta = (1, 1, -1, -1)
    psi = scale(Q(1, 4), private_eq.vec(
        B=delta, Eq=tuple(-value for value in delta)))
    balanced = private_eq.vec(B=delta)
    require(len(columns[0]) == 27
            and rank(columns) == 23
            and all(dot(psi, column) == 0 for column in columns)
            and dot(psi, balanced) == 1
            and rank(columns + (balanced,)) == 24,
            "the full named cap map/private-Eq dual changed")

    # Rebuild the exact eight-row projection to freeze rank 7 -> 8.
    projected = []
    for column in columns:
        projected.append(column[:8])
    psi8 = scale(Q(1, 4), tuple(map(Q, (*delta,
                                           *(-value for value in delta)))))
    balanced8 = tuple(map(Q, (*delta, 0, 0, 0, 0)))
    require(rank(tuple(projected)) == 7
            and all(dot(psi8, column) == 0 for column in projected)
            and dot(psi8, balanced8) == 1
            and rank(tuple(projected) + (balanced8,)) == 8,
            "the named maximal B/Eq projection changed")
    return columns, psi, {
        "coordinates": 27,
        "columns": len(columns),
        "rank": rank(columns),
        "B_Eq_projection_rank": rank(tuple(projected)),
        "B_Eq_projection_dimension": 8,
        "named_families": list(names),
        "canonical_normalized_dual": "delta.(B-Eq)/4",
        "normalized_value_on_balanced_B_delta": "1",
        "all_target_W_ores_q_anchor_ridge_eta_sigma_coefficients": 0,
    }


def typed_projection_and_missing_family(boolean_data, db_data, window_data,
                                        cap_data, packaging):
    packaging_ledger, packaging_digest = packaging.audit()
    require(packaging_digest == packaging.EXPECTED_LEDGER_SHA256,
            "the response-to-AugP2 packaging theorem changed")
    word = packaging_ledger["literal_word_and_fine_map"]
    augmented = packaging_ledger["augmented_packaging"]
    require(word["response_word_display"] == "11:110000"
            and word["canonical_cap_word"] == "01211222"
            and word["word_hamming_distance"] == 6
            and not word["literal_grade_preserving_map"]
            and not augmented["existing_AugP2_status"]
                ["constructed_literal_source_object"]
            and augmented["rank_before_mixed_cell"] == 2
            and augmented["rank_after_mixed_cell"] == 3
            and augmented["rank_after_labelled_ridge"] == 4,
            "the literal cross-word frontier changed")

    # All response/intermediate families are literally outside the AugP2
    # B/Eq row block.  Their projection is therefore zero, not an assigned
    # cancellation.  Only the 25 cap columns have nonzero B/Eq entries.
    response_column_count = (
        boolean_data["columns"] + db_data["columns"] + window_data["columns"]
    )
    zero8 = (Q(0),) * 8
    response_projections = (zero8,) * response_column_count
    require(response_column_count == 121
            and rank(response_projections) == 0,
            response_column_count)

    delta = tuple(map(Q, (1, 1, -1, -1)))
    psi8 = scale(Q(1, 4), delta + scale(-1, delta))
    eq_only = (Q(0),) * 4 + delta
    b_only = delta + (Q(0),) * 4
    tied = delta + delta
    require(dot(psi8, eq_only) == -1
            and dot(psi8, b_only) == 1
            and dot(psi8, tied) == 0,
            "the primitive bright/dark controls changed")

    return {
        "literal_projection_rule": (
            "project only columns in word 01211222 and its exact fine/"
            "repeated AugP2 grade to (B0..B3,Eq0..Eq3); every differently "
            "tagged response/intermediate column projects to zero"
        ),
        "off_grade_named_columns_with_zero_B_Eq_projection":
            response_column_count,
        "response_word": word["response_word_display"],
        "cap_word": word["canonical_cap_word"],
        "word_hamming_distance": word["word_hamming_distance"],
        "all_six_selected_fine_degrees_change":
            word["all_six_fine_degrees_change"],
        "cap_word_in_existing_D4_cube": word["cap_word_in_existing_D4_cube"],
        "unconditional_finite_column_test": (
            "chi(c)=delta dot (B(c)-Eq(c)); the normalized terminal extends "
            "over an exhaustive literal map iff chi(c)=0 for every column"
        ),
        "primitive_projection_controls": {
            "B_only_delta": "1",
            "Eq_only_delta": "-1",
            "tied_B_equals_Eq_delta": "0",
        },
        "first_unmodeled_literal_arrow": word["first_required_arrow"],
        "first_unmodeled_chi_bright_family": (
            "the mixed response-to-AugP2 mapping-cylinder/Tate incidence "
            "which places the selected db01/18-direction packet and gives "
            "a delta-weighted private/reduced-Eq mismatch"
        ),
        "smallest_missing_projected_column": (
            "one primitive B-only delta or Eq-only delta column; either "
            "raises the B/Eq rank 7->8"
        ),
        "physical_family_must_also_carry": [
            "the 11:110000 -> 01211222 word/fine diagonal",
            "all six P3+K2 and six sibling 3K2 faces",
            "the reduced-Eq/cap label descent",
            "gamma=-dOmega and the -d(q_xv^01) connection face",
        ],
        "post_word_packaging_ranks": [
            augmented["rank_before_mixed_cell"],
            augmented["rank_after_mixed_cell"],
            augmented["rank_after_labelled_ridge"],
        ],
    }


def direct_sum_maximal_map(pointed_columns, pointed_dual,
                           db_columns, db_dual,
                           window_columns, window_dual,
                           cap_columns, cap_dual):
    blocks = (
        (pointed_columns, pointed_dual),
        (db_columns, db_dual),
        (window_columns, window_dual),
        (cap_columns, cap_dual),
    )
    dimensions = [len(dual) for _columns, dual in blocks]
    total = sum(dimensions)
    embedded_columns = []
    before = 0
    for (columns, _dual), dimension in zip(blocks, dimensions, strict=True):
        after = total - before - dimension
        embedded_columns.extend(embed(column, before, after)
                                for column in columns)
        before += dimension
    combined_dual = tuple(value for _columns, dual in blocks for value in dual)
    block_ranks = [rank(columns) for columns, _dual in blocks]
    require(dimensions == [108, 3, 48, 27]
            and block_ranks == [19, 2, 46, 23]
            and len(embedded_columns) == 146
            and rank(tuple(embedded_columns)) == sum(block_ranks) == 90
            and all(dot(combined_dual, column) == 0
                    for column in embedded_columns),
            "the maximal named direct-sum map changed")
    return {
        "block_dimensions": dimensions,
        "block_column_counts": [len(columns) for columns, _dual in blocks],
        "block_ranks": block_ranks,
        "total_coordinates": total,
        "total_named_columns": len(embedded_columns),
        "total_rank": rank(tuple(embedded_columns)),
        "one_blockwise_normalized_compatibility_covector_exists": True,
        "compatibility_covector_is_physical_cross_word_terminal": False,
        "reason": (
            "the literal blocks are a direct sum until the missing physical "
            "word/fine/repeated mapping cylinder supplies cross-block columns"
        ),
    }


def audit():
    pin_dependencies()
    boolean = load(
        "computations/verify_h3_pointed_occurrence_edge_euler_boolean_cube_gate.py",
        "maximal_named_boolean",
    )
    relative = load(
        "computations/verify_h3_gate_ii_three_cap_relative_tate_carrier_obstruction.py",
        "maximal_named_relative",
    )
    db01 = load(
        "computations/verify_h3_selected_db01_normalized_gl3_bar_companion_gate.py",
        "maximal_named_db01",
    )
    k22 = load(
        "computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py",
        "maximal_named_k22",
    )
    private_eq = load(
        "computations/verify_h3_balanced_square_private_eq_projection_gate.py",
        "maximal_named_private_eq",
    )
    packaging = load(
        "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py",
        "maximal_named_packaging",
    )

    pointed_columns, pointed_dual, pointed_data = (
        pointed_boolean_and_top_faces(boolean, relative)
    )
    db_columns, db_dual, db_data = selected_db01_block(db01)
    window_columns, window_dual, window_data = fixed_window_block(k22)
    cap_columns, cap_dual, cap_data = augmented_private_eq_block(private_eq)
    ledger = {
        "theorem": "h3 maximal pointed/balanced same-grade terminal gate",
        "pins": PINS,
        "pointed_Boolean_and_RL_top": pointed_data,
        "selected_db01_PP": db_data,
        "fixed_window_switch_Weyl_response_RL_18face": window_data,
        "known_AugP2_cap_private_Eq": cap_data,
        "maximal_named_literal_map": direct_sum_maximal_map(
            pointed_columns, pointed_dual,
            db_columns, db_dual,
            window_columns, window_dual,
            cap_columns, cap_dual,
        ),
        "typed_projection_and_first_unmodeled_family":
            typed_projection_and_missing_family(
                pointed_data, db_data, window_data, cap_data, packaging),
        "verdict": (
            "The maximal named h3 packet has 186 literal coordinates, 146 "
            "named columns and rank 90 before any unconstructed cross-word "
            "gluing.  The normalized pointed occurrence dual extends over "
            "all fifteen Boolean faces and the relative R01/L01/selected-"
            "fibre graphs.  On the final augmented map, every named family "
            "has zero delta-weighted B-Eq mismatch, so the balanced terminal "
            "reduces canonically to Psi=delta.(B-Eq)/4.  Response R01/L01/"
            "db01 and the eighteen C4 faces are not counterexamples: their "
            "literal word/fine/repeated rows are disjoint from AugP2 B/Eq. "
            "The first unmodeled bright family is the physical cross-word "
            "PP mapping-cylinder mixed incidence.  Its exact finite test is "
            "delta.(B-Eq)!=0; a primitive B-only or Eq-only delta column "
            "raises the projected rank from seven to eight."
        ),
        "scope": (
            "exact union of the committed relative Boolean, selected db01, "
            "fixed-window switch/Weyl/complete-response/RL/direction, and "
            "named AugP2/cap matrices over Q.  This proves the finite "
            "exhaustiveness criterion and identifies the first absent "
            "bright physical family.  It does not prove that the named "
            "families exhaust every source column or manufacture the "
            "missing word-changing mapping cylinder."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("maximal pointed/balanced ledger changed", digest))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    maximal = ledger["maximal_named_literal_map"]
    print("h3 maximal named pointed/balanced map: PASS")
    print("coordinates/columns/rank: {}/{}/{}".format(
        maximal["total_coordinates"], maximal["total_named_columns"],
        maximal["total_rank"]))
    print("all named cap projections: delta.(B-Eq)=0")
    print("canonical normalized terminal projection: delta.(B-Eq)/4")
    print("first unmodeled bright family: CROSS-WORD MIXED PP/EQ INCIDENCE")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
