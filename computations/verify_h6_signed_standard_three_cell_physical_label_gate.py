#!/usr/bin/env python3
"""Test the first h=6 signed-standard coherence in physical labels.

The uniform Johnson calculation gives one explicit H2 cycle B0 on five tail
edges.  This checker decorates its ten window vertices by the literal h=4
word template, the full three-spectator fine degree, removed/reinserted tail
labels, repeated grade and operation parent.

B0 has sixteen nonzero two-faces: four inherited h=4 presentation triangles
and twelve disjoint-edge Beck--Chevalley squares.  A fixed-window ordinary
triple Koszul/Beck--Chevalley cube has six square faces, stays in one window
fine idempotent and has no presentation-triangle component.  Even granting
the entire fifteen-dimensional square-face space, B0 raises rank 15 -> 16;
the T123 coordinate is an exact separator of value -1.

Thus the required K0 is not an ordinary triple spectator cube.  It is the
first new physical Hasse-linearity/coherence cell tying already known h4
triangles to BC squares.  Constant protected readouts cancel on B0.  After
the label lift, the first rowwise debt is one alternating four-support
identity; physical Hasse-linearity must prove it for target, B/Eq, q/anchor,
residue, W, P_f and ridge/eta/sigma.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_johnson_window_hasse_coherence_resolution.py":
        "d10e82c97135106638ba46add3030fb28f716337853c5c2381c4ab0eeb145fe5",
    "notes/uniform-johnson-window-hasse-coherence-resolution.md":
        "e88afb6ebf94508f5ef552a804c888ce3221a07a663c381f3db9332a8a279130",
    "computations/verify_h5_pointed_phi_two_spectator_beck_chevalley_coherence.py":
        "55f363146627bf44974d28556bd669b4c1908cab9bb187b9a389e2cbd23fd650",
    "notes/h5-pointed-phi-two-spectator-beck-chevalley-coherence.md":
        "c56d667abc5e4d5396a76972c383e87412dd74ebdb25b029e2d8e8a08307f365",
    "computations/verify_h4_collision_ks_three_presentation_connection_grammar_gate.py":
        "6307e4444bae24785206608758590bff3c37432532dfe5c641138edb162b02ff",
    "notes/h4-collision-ks-three-presentation-connection-grammar-gate.md":
        "2bd22746c6dc68f82664cd50111a00162d51f90135be48b3f69adc48fba62761",
    "computations/verify_h4_collision_ks_physical_site_permutation_tree_gate.py":
        "7245dadf4e358efb3a6b63bfb4d33508c031ef468ff50f3eefdc60a000d41228",
    "notes/h4-collision-ks-physical-site-permutation-tree-gate.md":
        "0dc83a1457e6531851e7b907a27bddde74ad0f34ee7cc0be93e3b14123839562",
}
EXPECTED_LEDGER_SHA256 = "7e7955d491ef83be8585b75515e4f2b5ca71345d867b35b485e4b937e5682a1c"

TAIL_EDGES = ("23", "45", "67", "89", "AB")
PREFIX = "0121"
PROTECTED_ROWS = (
    "target", "private B", "reduced Eq", "M", "ainc", "q=M-ainc",
    "W", "pointed P_f", "labelled ordinary residue", "ridge", "eta",
    "sigma",
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def rank(vectors) -> int:
    vectors = tuple(tuple(map(Q, vector)) for vector in vectors)
    if not vectors:
        return 0
    work = [list(vector) for vector in vectors]
    width = len(work[0])
    require(all(len(vector) == width for vector in work), "rank width")
    pivot_row = 0
    for column in range(width):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [entry - value * base for entry, base in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def unit(index: int, size: int):
    return tuple(Q(position == index) for position in range(size))


def window_name(window: tuple[int, int]) -> str:
    return "v_" + "".join(map(str, window))


def literal_word(window: tuple[int, int]) -> str:
    # The h4 template has prefix 0121, one tail edge of colour 12 at the
    # smaller window index, and every other tail edge of colour 22.  It
    # reproduces 0121221222 and 0121122222 on every three-edge restriction.
    marked = min(window)
    answer = PREFIX + "".join("12" if index == marked else "22"
                              for index in range(5))
    require(len(answer) == 14, ("h6 word length", answer))
    return answer


def presentation_record(window: tuple[int, int]) -> dict[str, object]:
    complement = tuple(index for index in range(5) if index not in window)
    window_edges = tuple(TAIL_EDGES[index] for index in window)
    spectator_edges = tuple(TAIL_EDGES[index] for index in complement)
    return {
        "window": window_name(window),
        "window_edges": list(window_edges),
        "word": literal_word(window),
        "fine": (
            "T_[" + "|".join(spectator_edges) + "]*q_(v," +
            "|".join(window_edges) + ")"
        ),
        "spectator_tail": list(spectator_edges),
        "removed_edges": list(spectator_edges),
        "reinserted_edges": list(spectator_edges),
        "coarse_repeated": "P3+K2",
        "spectator_repeated_grade": "3 labelled K2 spectator factors",
        "operation": "Phi_KS,r0/P_f-prolonged PP/AugP2 presentation",
    }


def h4_word_template_restriction_audit() -> dict[str, object]:
    # Every three-set must reproduce the h4 pattern: the bc presentation has
    # 12 on b, while ac and ab have 12 on a.  All other tail pairs are 22.
    records = []
    for a in range(3):
        for b in range(a + 1, 4):
            for c in range(b + 1, 5):
                windows = ((b, c), (a, c), (a, b))
                marked = tuple(literal_word(window)[4:].index("12") // 2
                               for window in windows)
                require(marked == (b, a, a),
                        ("h4 word template", (a, b, c), marked))
                records.append({
                    "triple": [a, b, c],
                    "p0_window_bc_word": literal_word((b, c)),
                    "p1_window_ac_word": literal_word((a, c)),
                    "p2_window_ab_word": literal_word((a, b)),
                    "marked_12_edge_indices": list(marked),
                })
    presentations = tuple(presentation_record(window)
                          for window in combinations(range(5), 2))
    require(len({record["fine"] for record in presentations}) == 10
            and len({record["word"] for record in presentations}) == 4,
            "literal h6 word/fine separation changed")
    return {
        "tail_edges": list(TAIL_EDGES),
        "site_word_length": 14,
        "three_edge_restrictions": records,
        "ten_presentations": list(presentations),
        "literal_fine_idempotent_count": 10,
        "literal_word_idempotent_count": 4,
        "word_rule": (
            "prefix 0121; colour-pair 12 on min(window), 22 on all other "
            "tail edges"
        ),
    }


def signed_standard_face_packet_audit(uniform) -> dict[str, object]:
    model, relations = uniform.canonical_five_relations()
    b0 = relations[0]
    require(uniform.face_relation_boundary(model, b0) ==
                (0,) * len(model.edges),
            "B0 stopped being a two-cycle")
    records = []
    used_windows = set()
    used_words = set()
    used_fines = set()
    triangle_coefficients = []
    square_coefficients = []
    for coefficient, name, face in zip(b0, model.face_names, model.faces,
                                       strict=True):
        if not coefficient:
            continue
        kind = "h4 presentation triangle" if name.startswith("T") else (
            "disjoint-edge Beck-Chevalley square"
        )
        presentations = [presentation_record(window) for window in face]
        for presentation in presentations:
            used_windows.add(presentation["window"])
            used_words.add(presentation["word"])
            used_fines.add(presentation["fine"])
        (triangle_coefficients if name.startswith("T") else
         square_coefficients).append(int(coefficient))
        records.append({
            "face": name,
            "coefficient": int(coefficient),
            "kind": kind,
            "window_cycle": [window_name(window) for window in face],
            "literal_presentations": presentations,
            "operation_parent": (
                "three-window Cech/Phi coherence" if name.startswith("T")
                else "two-order restriction/reinsertion BC interchange"
            ),
        })
    require(len(records) == 16
            and len(triangle_coefficients) == 4
            and len(square_coefficients) == 12
            and triangle_coefficients == [-1, 1, -1, 1]
            and sum(triangle_coefficients) == sum(square_coefficients) == 0
            and len(used_windows) == len(used_fines) == 10
            and len(used_words) == 4,
            "literal B0 packet changed")
    return {
        "cell": "K_0 on tail 23|45|67|89|AB",
        "boundary": "d K_0=B_0",
        "nonzero_two_faces": records,
        "support_counts": {
            "h4_presentation_triangles": 4,
            "BC_squares": 12,
            "total": 16,
        },
        "triangle_coefficients": triangle_coefficients,
        "square_coefficient_sum": sum(square_coefficients),
        "window_idempotents_used": sorted(used_windows),
        "word_idempotents_used": sorted(used_words),
        "fine_idempotent_count": len(used_fines),
        "coarse_repeated_parent": "P3+K2 with three labelled spectators",
    }


def ordinary_triple_cube_counterguard(uniform) -> dict[str, object]:
    model, relations = uniform.canonical_five_relations()
    b0 = tuple(map(Q, relations[0]))
    square_indices = tuple(index for index, name in enumerate(model.face_names)
                           if name.startswith("Q"))
    triangle_indices = tuple(index for index, name in enumerate(model.face_names)
                             if name.startswith("T"))
    all_square_space = tuple(unit(index, len(model.faces))
                             for index in square_indices)
    require(len(square_indices) == 15 and len(triangle_indices) == 10
            and rank(all_square_space) == 15
            and rank(all_square_space + (b0,)) == 16,
            "square-only cube counterguard changed")

    t123 = model.face_names.index("T123")
    detector = unit(t123, len(model.faces))
    detector_value = sum(left * right for left, right in
                         zip(detector, b0, strict=True))
    require(detector_value == -1
            and all(sum(left * right for left, right in
                        zip(detector, square, strict=True)) == 0
                    for square in all_square_space),
            "T123 separator changed")
    return {
        "ordinary_fixed_window_triple_cube": {
            "spectator_directions": 3,
            "codimension_one_square_faces": 6,
            "word_idempotents": 1,
            "fine_window_idempotents": 1,
            "presentation_triangle_faces": 0,
            "operation_parent": "fixed-window cubical Koszul/BC",
        },
        "generous_grant": "all 15 BC-square coordinate directions",
        "rank_square_space_then_B0": [15, 16],
        "primitive_separator": "coefficient of T123",
        "separator_on_all_square_only_cube_boundaries": 0,
        "separator_on_B0": int(detector_value),
        "B0_is_one_ordinary_triple_cube": False,
        "B0_in_span_of_all_square_only_cubes": False,
        "first_mismatch": (
            "operation/window face type: B0 has four h4 Cech/Phi triangle "
            "parents, while an ordinary fixed-window cube has squares only"
        ),
        "conclusion": (
            "K0 is a new mixed triangle-square Hasse-linearity cell, not a "
            "renaming of the ordinary triple spectator Koszul cube"
        ),
    }


def protected_readout_audit(uniform) -> dict[str, object]:
    model, relations = uniform.canonical_five_relations()
    b0 = relations[0]
    triangle_sum = sum(coefficient for coefficient, name in
                       zip(b0, model.face_names, strict=True)
                       if name.startswith("T"))
    square_sum = sum(coefficient for coefficient, name in
                     zip(b0, model.face_names, strict=True)
                     if name.startswith("Q"))
    require(triangle_sum == square_sum == sum(b0) == 0,
            "constant protected readout stopped cancelling")

    # If all three Q types on a four-set have one common readout, their
    # signed coefficient collapses to -,+,-,+ on supports 0123,0124,0134,
    # 0234.  The triangles have the identical support-sign pattern on the
    # complementary four-set inside {1,2,3,4}.
    support_signs = {
        "123": -1, "124": 1, "134": -1, "234": 1,
        "0123": -1, "0124": 1, "0134": -1, "0234": 1,
    }
    r0 = tuple(map(Q, (1, 1, 1, -1, -1, 0, 1, 0, 0, 0, 0, 0)))
    constant_aggregate = tuple(sum(b0) * value for value in r0)
    require(constant_aggregate == (Q(0),) * len(r0),
            "constant r0 face readout changed")
    return {
        "protected_rows": list(PROTECTED_ROWS),
        "triangle_coefficient_sum": triangle_sum,
        "square_coefficient_sum": square_sum,
        "constant_face_readout_on_B0": 0,
        "conditional_constant_r0_aggregate": list(map(int,
                                                        constant_aggregate)),
        "first_rowwise_Hasse_linearity_debt": (
            "-R_T(123)+R_T(124)-R_T(134)+R_T(234) "
            "-R_Q(0123)+R_Q(0124)-R_Q(0134)+R_Q(0234)=0"
        ),
        "support_signs": support_signs,
        "status": (
            "constant/equal transported values give no scalar obstruction; "
            "the displayed alternating identity is unproved for literal "
            "physical target/q/anchor/residue/ridge rows because K0 is not "
            "yet a physical cell"
        ),
        "first_failure_order": (
            "word/fine/operation-parent lift fails before a nonzero protected "
            "readout is forced"
        ),
    }


def minimal_physical_axiom() -> dict[str, object]:
    return {
        "new_cell_schema": (
            "five oriented K_a cells on every labelled five-edge tail, "
            "dK_a=B_a, sum_a K_a=0 modulo the next coherence, with "
            "sigma K_a=sgn(sigma)K_sigma(a)"
        ),
        "literal_requirements": [
            "all ten T_S*q_(v,W) fine/window idempotents",
            "the four inherited word-changing h4 triangle faces",
            "the twelve signed disjoint-edge BC square faces of B_a",
            "removed/reinserted three-edge spectator labels",
            "P3+K2 plus three labelled spectator repeated factors",
            "the rowwise alternating Hasse identity on every protected row",
        ],
        "already_ordinary_triple_BC_cube": False,
        "new_response_to_cap_operation_switch": False,
        "classification": (
            "new higher naturality/coherence axiom for the one Phi schema; "
            "it does not introduce a second Phi-type operation"
        ),
        "shortest_positive_test": (
            "construct one literal K0 with the sixteen-face boundary and "
            "verify the alternating protected-row identity; S5 signed "
            "naturality then supplies the other four instances"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    uniform = load(
        "computations/verify_uniform_johnson_window_hasse_coherence_resolution.py",
        "h6_physical_uniform_dependency",
    )
    ledger = {
        "theorem": "h6 signed-standard three-cell physical label gate",
        "pins": PINS,
        "literal_h6_presentations": h4_word_template_restriction_audit(),
        "signed_standard_K0_boundary":
            signed_standard_face_packet_audit(uniform),
        "ordinary_triple_cube_counterguard":
            ordinary_triple_cube_counterguard(uniform),
        "protected_readout_debt": protected_readout_audit(uniform),
        "minimal_physical_axiom": minimal_physical_axiom(),
        "verdict": (
            "The first h6 signed-standard boundary can be decorated "
            "explicitly on tail 23|45|67|89|AB.  It uses all ten window/fine "
            "idempotents, four literal word idempotents, four inherited h4 "
            "presentation triangles and twelve BC squares.  An ordinary "
            "fixed-window triple Koszul cube has six square faces and no "
            "triangle component.  Even granting every BC-square direction, "
            "B0 raises rank 15->16 and is detected by T123=-1.  Therefore "
            "the filler is a genuinely new higher Hasse-linearity cell for "
            "the one Phi schema, not an ordinary cube and not a new Phi-type "
            "operation switch.  Constant protected readouts cancel; the "
            "first unresolved readout is the displayed alternating "
            "triangle/square support identity."
        ),
        "scope": (
            "exact rational one-five-tail label/support/rank audit obtained "
            "by relabelling the committed h4 word template.  It identifies "
            "the required physical K0 boundary and first protected-row law, "
            "but does not construct K0 in the decorated source, assign "
            "nonconstant physical two-face readouts, prove the other S5 "
            "instances physical, or establish full matching-cover descent."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("h6 signed-standard physical label ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "words", "faces", "cube",
                                           "readouts", "axiom"), default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"h6 signed-standard physical label gate ({arguments.mode}): PASS")
        print("K0 boundary: 4 h4 triangles + 12 BC squares; 10 fine windows")
        print("ordinary triple cube after all-square grant: rank 15 -> 16")
        print("primitive separator: T123(B0)=-1")
        print("constant protected readout: 0")
        print("physical K0: NEW HASSE-LINEARITY AXIOM, NOT CONSTRUCTED")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
