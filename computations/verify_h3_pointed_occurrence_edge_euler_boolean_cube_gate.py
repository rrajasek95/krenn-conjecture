#!/usr/bin/env python3
"""Audit the four-edge Euler resolution of the pointed occurrence selector.

The selected h=3 response packet consists of the 90 perfect matchings of
P,S,0,...,5 which do not contain the direct edge PS.  For

    f = P0 | S1 | 23 | 45

the four commuting edge Euler operators filter the complete response to f.
This checker constructs every Boolean face, its centered occurrence vector,
the label-faithful relative graph which preserves H0, and the squarefree
Koszul/Hasse cube of the four directions.

The distinction certified here is important.  The fourth ordinary
derivative of the response is the unit, exactly as in the known D4 Hasse
calculation.  It is only the scalar associated-graded top.  The evaluated
Euler cube neither supplies a source-valid homotopy for its lower faces nor
turns the pointed class into an absolute boundary.  A monic relative graph
retains one carrier for every labelled face; its top is u_f, with cotangent
face du_f=90 df-dR.  Killing that carrier is new source data and changes H0.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json


BASE_COMMITS = {
    "centered_occurrence_pointed_gate": "657dd06",
    "full_hasse_d4_descent": "5d4b8c5",
    "orbit_relative_d4": "8f9f879",
}
BASE_BLOBS = {
    "657dd06:verify_h3_centered_occurrence_endpoint_matching_maschke_pointed_gate.py":
        "1994697181c6034267d98a26a28ab4c69c3fcb979b657c8d7d06fc81b86650ed",
    "5d4b8c5:verify_h3_full_hasse_cone_d4_descent_obstruction.py":
        "ed2f2b3451074500b39a100da91ffefed27f748636de172d81aabd5cfe394240",
    "8f9f879:verify_h3_e14_orbit_relative_d4_target_cone_gate.py":
        "67d33b03ec52c619f29e76c917fdba9b7e28380b4349291fa37b6b7d511e241c",
}
EXPECTED_LEDGER_SHA256 = (
    "f1f01a32526db3dbeef6035439fe8134f5c496f9d7cb4e0182d6ae260b8cfdd7"
)


Edge = tuple[int, int]
Matching = tuple[Edge, ...]
Vector = tuple[Q, ...]

NAMES = ("P", "S", "0", "1", "2", "3", "4", "5")
P, S, ZERO, ONE, TWO, THREE, FOUR, FIVE = range(8)
VERTICES = tuple(range(8))
DIRECT = tuple(sorted((P, S)))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def edge(left: int, right: int) -> Edge:
    require(left != right, ("loop", left))
    return tuple(sorted((left, right)))


def monomial(*items: Edge) -> Matching:
    return tuple(sorted(items))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield monomial(edge(first, second), *tail)


OCCURRENCES = tuple(sorted(
    matching for matching in perfect_matchings(VERTICES)
    if DIRECT not in matching
))
MARKED = monomial(
    edge(P, ZERO), edge(S, ONE), edge(TWO, THREE), edge(FOUR, FIVE)
)
DIRECTIONS = MARKED
MARKED_INDEX = OCCURRENCES.index(MARKED)


def subsets(items: tuple[Edge, ...], include_empty: bool = True):
    start = 0 if include_empty else 1
    return tuple(face for degree in range(start, len(items) + 1)
                 for face in combinations(items, degree))


def indicator(face: tuple[Edge, ...]) -> Vector:
    selected = frozenset(face)
    return tuple(Q(selected.issubset(matching)) for matching in OCCURRENCES)


def add(*vectors: Vector) -> Vector:
    require(vectors and len({len(value) for value in vectors}) == 1,
            "add width")
    return tuple(sum((value[index] for value in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient: Q, vector: Vector) -> Vector:
    return tuple(Q(coefficient) * value for value in vector)


def dot(left: Vector, right: Vector) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns: tuple[Vector, ...] | list[Vector]) -> int:
    if not columns:
        return 0
    require(len({len(column) for column in columns}) == 1, "rank height")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(len(columns[0]))]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(len(rows)):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def multiply(left: list[list[Q]], right: list[list[Q]]) -> list[list[Q]]:
    require(left and right and len(left[0]) == len(right),
            "matrix product dimensions")
    return [[sum((a * b for a, b in zip(left_row, right_column, strict=True)),
                 Q(0))
             for right_column in zip(*right, strict=True)]
            for left_row in left]


def koszul_matrix(degree: int) -> list[list[Q]]:
    """Wedge by the sum of the four formal edge directions."""
    source = tuple(combinations(range(4), degree))
    target = tuple(combinations(range(4), degree + 1))
    target_index = {face: index for index, face in enumerate(target)}
    matrix = [[Q(0) for _ in source] for _ in target]
    for source_index, face in enumerate(source):
        for direction in range(4):
            if direction in face:
                continue
            target_face = tuple(sorted(face + (direction,)))
            sign = Q((-1) ** target_face.index(direction))
            matrix[target_index[target_face]][source_index] += sign
    return matrix


def matching_and_boolean_face_audit() -> tuple[
        dict[str, object], dict[tuple[Edge, ...], Vector]]:
    require(len(tuple(perfect_matchings(VERTICES))) == 105,
            "eight-vertex matching count changed")
    require(len(OCCURRENCES) == 90 and MARKED in OCCURRENCES,
            "direct-free response packet changed")
    require(all(len(matching) == 4 for matching in OCCURRENCES),
            "response stopped being four-edge squarefree")

    complete = tuple(Q(1) for _ in OCCURRENCES)
    face_vectors = {face: indicator(face) for face in subsets(DIRECTIONS)}
    supports = {face: int(sum(vector))
                for face, vector in face_vectors.items()}
    profile = {
        degree: sorted(support for face, support in supports.items()
                       if len(face) == degree)
        for degree in range(5)
    }
    expected_profile = {
        0: [90],
        1: [12, 12, 15, 15],
        2: [2, 3, 3, 3, 3, 3],
        3: [1, 1, 1, 1],
        4: [1],
    }
    require(profile == expected_profile,
            ("Boolean face support profile changed", profile))

    # E_e is the diagonal filter for occurrence of e.  Their commuting
    # product is therefore the marked occurrence projector.
    top = face_vectors[DIRECTIONS]
    marked_basis = tuple(Q(index == MARKED_INDEX)
                         for index in range(len(OCCURRENCES)))
    require(top == marked_basis, "edge Euler product stopped selecting f")
    centered = add(scale(90, top), scale(-1, complete))
    expected_centered = tuple(Q(89 if index == MARKED_INDEX else -1)
                              for index in range(len(OCCURRENCES)))
    require(centered == expected_centered and sum(centered, Q(0)) == 0,
            "c_f=90e_f-1 changed")

    centered_faces = {
        face: add(scale(90, vector), scale(-supports[face], complete))
        for face, vector in face_vectors.items()
    }
    require(not any(centered_faces[()]), "empty centered face should be zero")
    require(centered_faces[DIRECTIONS] == centered,
            "top centered face stopped being c_f")
    require(all(any(centered_faces[face])
                for face in subsets(DIRECTIONS, include_empty=False)),
            "a nonempty centered face vanished")
    require(all(sum(centered_faces[face], Q(0)) == 0
                for face in centered_faces),
            "a centered lower face left the augmentation ideal")

    triples = tuple(face for face in face_vectors if len(face) == 3)
    require(all(face_vectors[face] == marked_basis for face in triples),
            "three selected matching edges stopped forcing the fourth")
    require(len({centered_faces[face] for face in triples}) == 1,
            "unlabelled codimension-one faces stopped collapsing")
    unlabelled_rank = rank(tuple(centered_faces[face]
                                for face in subsets(
                                    DIRECTIONS, include_empty=False)))
    require(unlabelled_rank == 11,
            ("centered Boolean face span changed", unlabelled_rank))

    return {
        "vertices": list(NAMES),
        "direct_edge_omitted": "PS",
        "response_occurrences": len(OCCURRENCES),
        "marked_matching": "P0|S1|23|45",
        "marked_index": MARKED_INDEX,
        "edge_Euler_projector": "P_f=E_P0 E_S1 E_23 E_45",
        "projector_on_complete_response": "P_f(R)=f",
        "centered_top": "(90 P_f-I)R=90f-R=c_f",
        "centered_profile": [89, -1],
        "support_counts_by_face_order": profile,
        "face_count_by_order": [1, 4, 6, 4, 1],
        "nonempty_centered_faces": 15,
        "proper_nonempty_lower_faces": 14,
        "unlabelled_centered_face_span_rank": unlabelled_rank,
        "codimension_one_coefficient_collapse": (
            "all four three-edge filters equal e_f, because a perfect "
            "matching is forced by any three of its four edges"
        ),
        "labelled_codimension_one_faces_still_distinct": [
            "delete/reinsert P0", "delete/reinsert S1",
            "delete/reinsert q23", "delete/reinsert q45",
        ],
    }, centered_faces


def formal_cube_and_d4_audit() -> dict[str, object]:
    matrices = tuple(koszul_matrix(degree) for degree in range(4))
    ranks = tuple(rank(tuple(tuple(row[column] for row in matrix)
                             for column in range(len(matrix[0]))))
                  for matrix in matrices)
    require(ranks == (1, 3, 3, 1),
            ("four-edge Koszul ranks changed", ranks))
    for degree in range(3):
        composite = multiply(matrices[degree + 1], matrices[degree])
        require(all(not entry for row in composite for entry in row),
                ("d^2 stopped vanishing", degree))
    dimensions = (1, 4, 6, 4, 1)
    require(all(ranks[degree - 1] + ranks[degree] == dimensions[degree]
                for degree in range(1, 4)),
            "proper Boolean cube stopped being exact")

    # An ordinary derivative of a squarefree matching monomial removes an
    # edge.  Exactly one response monomial contains all four marked edges.
    contains_all = tuple(matching for matching in OCCURRENCES
                         if set(DIRECTIONS).issubset(matching))
    require(contains_all == (MARKED,),
            "fourth derivative stopped being the unit")

    return {
        "formal_Boolean_Koszul_dimensions": list(dimensions),
        "formal_Boolean_Koszul_ranks": list(ranks),
        "d_squared": 0,
        "proper_degrees_exact": True,
        "fourth_ordinary_derivative": "partial_P0 partial_S1 partial_23 partial_45 R=1",
        "fourth_edge_Euler_value": "f*partial_f R=f",
        "known_D4_scalar_top_identified": True,
        "known_D4_source_descent_obstruction": [
            "Psi_f(H_m)=1",
            "[d,pi_Delta]=(H_0-u)e_0",
        ],
        "pointed_top_equal_to_bare_D4_class": False,
        "reason": (
            "the D4 unit is the scalar associated-graded top; c_f also "
            "contains the occurrence tag, complete-row subtraction, and "
            "four labelled deletion/reinsertion directions"
        ),
        "orbit_relative_D4_role": (
            "transports a supplied (c_f,P_f) section to c_g; it does not "
            "construct the bottom pointed section"
        ),
    }


def relative_graph_audit(centered_faces: dict[tuple[Edge, ...], Vector]) \
        -> dict[str, object]:
    complete = tuple(Q(1) for _ in OCCURRENCES)
    nonempty = subsets(DIRECTIONS, include_empty=False)
    top = centered_faces[DIRECTIONS]

    old_rank = rank((complete,))
    raw_rank = rank((complete, top))
    require((old_rank, raw_rank) == (1, 2),
            "raw pointed rank comparison changed")
    old_h0 = len(OCCURRENCES) - old_rank
    raw_h0 = len(OCCURRENCES) - raw_rank
    require((old_h0, raw_h0) == (89, 88),
            "raw pointed H0 comparison changed")

    # Label-faithful universal graph: for every nonempty Hasse face S add a
    # private degree-zero carrier u_S and a monic graph column C_S-u_S.
    # The unique carrier coordinate makes each new column independent, so
    # the 15 face attachments preserve H0 exactly.
    width = len(OCCURRENCES) + len(nonempty)
    old_extended = complete + tuple(Q(0) for _ in nonempty)
    graph_columns = []
    for carrier_index, face in enumerate(nonempty):
        carrier = [Q(0) for _ in nonempty]
        carrier[carrier_index] = Q(-1)
        graph_columns.append(centered_faces[face] + tuple(carrier))
    full_rank = rank((old_extended, *graph_columns))
    graph_h0 = width - full_rank
    require((width, full_rank, graph_h0) == (105, 16, 89),
            ("full relative graph H0 changed", width, full_rank, graph_h0))

    # A concrete dual detects the top carrier after every lower graph has
    # been attached.  On the old occurrence block use c_f/<c_f,c_f>.  Its
    # carrier value is its readout on C_S, so it kills C_S-u_S.
    norm = dot(top, top)
    require(norm == 90 * 89, ("centered norm changed", norm))
    old_dual = scale(Q(1, norm), top)
    carrier_readouts = tuple(dot(old_dual, centered_faces[face])
                             for face in nonempty)
    expected_readouts = tuple(
        Q(90 - int(sum(indicator(face), Q(0))), 89)
        for face in nonempty
    )
    require(carrier_readouts == expected_readouts,
            "face carrier dual readouts changed")
    extended_dual = old_dual + carrier_readouts
    require(dot(extended_dual, old_extended) == 0
            and all(dot(extended_dual, column) == 0
                    for column in graph_columns),
            "retained top dual stopped killing the graph image")
    top_carrier_index = nonempty.index(DIRECTIONS)
    top_carrier = tuple(Q(index == len(OCCURRENCES) + top_carrier_index)
                        for index in range(width))
    require(dot(extended_dual, top_carrier) == 1,
            "top carrier stopped surviving")

    # Filling the retained top carrier adds an independent old-source
    # relation and lowers H0 by one.  It is not a consequence of the graph.
    filled_rank = rank((old_extended, *graph_columns, top_carrier))
    require(filled_rank == 17 and width - filled_rank == 88,
            "absolute top fill stopped changing H0")

    return {
        "old_occurrence_complex": {
            "coordinates": 90,
            "boundary_rank": old_rank,
            "H0": old_h0,
        },
        "raw_absolute_c_f_attachment": {
            "boundary_rank": raw_rank,
            "H0": raw_h0,
            "preserves_H0": False,
        },
        "minimal_label_faithful_relative_cube_graph": {
            "face_carriers": 15,
            "proper_lower_face_carriers": 14,
            "coordinates": width,
            "boundary_rank": full_rank,
            "H0": graph_h0,
            "differentials": "d b_S=C_S-u_S for nonempty S subset f",
            "top_differential": "d b_f=c_f-u_f",
            "preserves_H0": True,
        },
        "unlabelled_compression_warning": (
            "the 15 centered coefficient vectors span only rank 11; the "
            "four triple faces coincide with the top coefficient vector, "
            "but may not be identified after deletion/reinsertion labels"
        ),
        "retained_top_dual": {
            "old_block": "c_f/(90*89)",
            "carrier_value_formula": "lambda(u_S)=(90-|supp E_S R|)/89",
            "reads_u_f": 1,
            "kills_complete_response_and_all_15_graph_columns": True,
        },
        "absolute_u_f_fill": {
            "boundary_rank": filled_rank,
            "H0": width - filled_rank,
            "preserves_H0": False,
        },
        "conclusion": (
            "the Boolean resolution has an H0-preserving relative graph, "
            "not an absolute P_f boundary"
        ),
    }


def augmented_face_audit() -> dict[str, object]:
    return {
        "word_and_fine": {
            "coefficient_word": "11:110000",
            "status": (
                "the Euler filters preserve the coefficient word, but each "
                "proper face retains its missing-edge and reinsertion label"
            ),
            "warning": (
                "the later cap/ridge word 01211222 and orbit-D4 top word "
                "111111 are separate graded rows"
            ),
        },
        "scalar_target": {
            "first_face": "90 f(x)",
            "required_correction": "-90 f(x)",
            "source_valid_without_correction": False,
            "reason": (
                "edge Euler operators are coefficient selectors, not "
                "tangent symmetries of the trapped fixed source"
            ),
        },
        "q_and_PP": {
            "four_first_labelled_faces": [
                "d(P0): S1|23|45",
                "d(S1): P0|23|45",
                "d(q23): P0|S1|45",
                "d(q45): P0|S1|23",
            ],
            "matching_projection": "(A+I)c_f=3c_01",
            "centered_selected_PP": "dc_01=30 db_01-dR",
            "selected_db01_terms": 6,
            "supplied_by_aggregate_complete_response": False,
            "missing_property": "termwise PP/reinsertion naturality",
        },
        "anchor": {
            "top_relative_face": "du_f=dc_f=90 df-dR",
            "complete_response_graph_form": "[P_f]=[d(u_f-u)]=-[dG]",
            "absolute_condition": "[d(u_f-u)]=0",
            "proved_by_Boolean_cube": False,
        },
        "known_D4": {
            "formal_lower_faces": "the 4,6,4 proper Koszul blocks are exact",
            "physical_descent": False,
            "first_descent_defect": "(H_0-u)e_0; equivalently Psi_f(H_m)=1",
        },
        "sharp_remaining_positive_datum": (
            "one source-labelled pointed Boolean local system whose top is "
            "d b_f=c_f-u_f, whose fourteen proper faces realize the four "
            "edge deletion/reinsertion families termwise, whose scalar "
            "target face is -90f(x), and whose q projection is the selected "
            "six-term db01 row; then the known D4 cube can transport it"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    matching_data, centered_faces = matching_and_boolean_face_audit()
    ledger = {
        "theorem": "h3 pointed occurrence edge-Euler Boolean cube gate",
        "base_commits": BASE_COMMITS,
        "base_blob_sha256": BASE_BLOBS,
        "matching_and_centered_Boolean_faces": matching_data,
        "formal_cube_and_D4_comparison": formal_cube_and_d4_audit(),
        "minimal_H0_preserving_relative_model":
            relative_graph_audit(centered_faces),
        "word_fine_q_anchor_faces": augmented_face_audit(),
        "verdict": (
            "The four edge Euler filters exactly select f and their 16-face "
            "Boolean packet has the formal Koszul profile 1,4,6,4,1.  A "
            "label-faithful monic graph for all fifteen nonempty centered "
            "faces preserves H0=89, but its exact dual still reads one on "
            "the top carrier u_f.  The scalar fourth derivative is exactly "
            "the known D4 unit; the pointed top is not the bare D4 class, "
            "because it retains occurrence, deletion/reinsertion, target, "
            "and anchor data.  The cube plus complete response therefore "
            "does not make P_f absolute.  Filling u_f lowers H0 to 88."
        ),
        "nonclaims": [
            "a diagonal edge Euler filter is not called a physical homotopy",
            "coincident coefficient faces are not identified across fine labels",
            "formal Koszul exactness is not called physical source descent",
            "the D4 transport cube is not called a construction of bottom P_f",
            "the aggregate complete response is not called termwise PP-natural",
        ],
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
    print("edge-Euler cube: 16 FACES; P_f(R)=f; centered top c_f")
    print("formal Koszul profile: 1,4,6,4,1; D4 scalar top: UNIT")
    print("label-faithful relative graph: H0 89 -> 89; RETAINS u_f")
    print("absolute u_f fill: H0 89 -> 88; NOT SOURCE-PROVENANT")
    print("first physical debts: -90f(x), four PP/reinsertions, selected db01")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
