#!/usr/bin/env python3
"""Audit the literal h=6 five-tail Hasse boundary and protected rows.

The first H2 packet B0 is the alternating boundary of four corrected
deletion triangles

    Theta_0;ijk = T_ijk + Q_0ijk,0 - Q_0ijk,1 + Q_0ijk,2.

This is the primitive third simplicial/divided-Hasse cell on the four tail
edges complementary to the distinguished edge 0.  The checker proves that
the underlying cell is canonical in the complete matching polynomial:
restriction by any selected disjoint edge factors the complete hafnian to
the complete hafnian on the remaining vertices, and every deletion order
agrees.

All thirty one-edge boundaries of B0 cancel in the same literal connector,
with its word, T_S*q_(v,W), removed/reinserted and repeated labels retained.
The complete GHZ target kills every literal mixed word before coarsening and
is group-like on all three pure words.  With a normalized natural Phi, all
known B/Eq/q/W/ores/ridge projections cancel.

These row equations do not themselves construct the physical three-cell.
The identity q=M-ainc admits a T123 impulse whose alternating B0 readout is
-1.  More strongly, after granting every face/external direction except the
literal T123 operation coordinate, its coordinate dual kills the grant and
reads -1/30 on the normalized candidate.  Thus the alternatives are exact:
construct the normalized divided-Hasse comparison cell, or retain this
terminal dual for the present square/objectwise-row grammar.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h6_signed_standard_three_cell_physical_label_gate.py":
        "3f69da78f5d6ed29bd4da22cad9044385bdefa57f736ae7b355b4e5fb79284d3",
    "notes/h6-signed-standard-three-cell-physical-label-gate.md":
        "5f98a001490c6de0e6d680abe6be36c0a23ecb2f49b0224afdf9de293d1fbeff",
    "computations/verify_uniform_johnson_window_hasse_coherence_resolution.py":
        "d10e82c97135106638ba46add3030fb28f716337853c5c2381c4ab0eeb145fe5",
    "notes/uniform-johnson-window-hasse-coherence-resolution.md":
        "e88afb6ebf94508f5ef552a804c888ce3221a07a663c381f3db9332a8a279130",
    "computations/verify_h4_collision_ks_decorated_presentation_mismatch.py":
        "ed0a43db7e9656119bdaf21ebea1d433451cfe1f32f2ce086f3c19dda0275d6a",
    "notes/h4-collision-ks-decorated-presentation-mismatch.md":
        "ef34f5fabc6a9e20210ceafa3f68fa23d959f744694f05509aa16433b0c00ed3",
    "computations/verify_h3_phi_ks_r0_pf_minimal_executable_ansatz_gate.py":
        "d21d776ec53babb4f99693e4dad51d87309e3ed0cccf2e34fb6025e6d74d1009",
    "notes/h3-phi-ks-r0-pf-minimal-executable-ansatz-gate.md":
        "4050dd62663aedd2d07c512317f9e75f53ba566b01a88b949774771fc6e8e9d6",
}
EXPECTED_LEDGER_SHA256 = "0e858b6c909c535ce66135aebac09accffe44f8d296cadaa12756e500455c688"

Edge = tuple[int, int]
Matching = tuple[Edge, ...]
Vector = tuple[Q, ...]
MU = Q(1, 30)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name,
                                                            ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def rank(vectors: tuple[Vector, ...] | list[Vector]) -> int:
    if not vectors:
        return 0
    work = [list(map(Q, vector)) for vector in vectors]
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


def unit(index: int, size: int) -> Vector:
    return tuple(Q(position == index) for position in range(size))


def dot(left: Vector, right: Vector) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((min(first, second), max(first, second)),)
                               + tail))


def odd_double_factorial(value: int) -> int:
    return 1 if value <= 0 else math.prod(range(1, value + 1, 2))


def restrict_polynomial(polynomial: Counter[Matching], selected: Edge) \
        -> Counter[Matching]:
    answer: Counter[Matching] = Counter()
    for matching, coefficient in polynomial.items():
        if selected in matching:
            answer[tuple(edge for edge in matching if edge != selected)] += (
                coefficient
            )
    return +answer


def complete_matching_deletion_audit() -> dict[str, object]:
    vertices = tuple(range(10))
    selected = tuple((2 * index, 2 * index + 1) for index in range(5))
    complete = Counter({matching: 1 for matching in perfect_matchings(vertices)})
    require(len(complete) == odd_double_factorial(9) == 945,
            "ten-site matching census")

    subset_records = []
    for size in range(6):
        for subset in combinations(selected, size):
            expected_vertices = tuple(
                vertex for vertex in vertices
                if all(vertex not in edge for edge in subset)
            )
            expected = Counter({matching: 1 for matching in
                                perfect_matchings(expected_vertices)})
            outcomes = set()
            for order in permutations(subset):
                current = complete
                for edge in order:
                    current = restrict_polynomial(current, edge)
                outcomes.add(tuple(sorted(current.items())))
            require(len(outcomes) == 1 and current == expected,
                    ("complete matching deletion", subset))
            subset_records.append({
                "selected_edge_count": size,
                "selected_edges": [list(edge) for edge in subset],
                "remaining_complete_matching_terms": len(current),
                "expected_terms": odd_double_factorial(9 - 2 * size),
                "all_deletion_orders_equal": True,
            })
    count_profile = Counter(record["remaining_complete_matching_terms"]
                            for record in subset_records)
    require(count_profile == Counter({945: 1, 105: 5, 15: 10,
                                      3: 10, 1: 6}), count_profile)
    return {
        "complete_tail_response": "Hafnian on ten labelled tail sites",
        "complete_matching_terms": len(complete),
        "distinguished_matching": [list(edge) for edge in selected],
        "all_32_selected_subsets_checked": len(subset_records) == 32,
        "term_counts_by_number_of_fixed_edges": [945, 105, 15, 3, 1, 1],
        "every_deletion_order_commutes": True,
        "factorization": (
            "restricting every matching containing S and deleting S gives "
            "the complete hafnian on the remaining vertices with coefficient 1"
        ),
        "source_status": (
            "the primitive deletion cell exists canonically in the complete "
            "matching-response polynomial"
        ),
    }


def corrected_deletion_cell_audit(uniform) -> dict[str, object]:
    model, relations = uniform.canonical_five_relations()
    b0 = tuple(map(Q, relations[0]))
    face_index = {name: index for index, name in enumerate(model.face_names)}
    corrected = {}
    for triple in combinations((1, 2, 3, 4), 3):
        triple_name = "".join(map(str, triple))
        support = "0" + triple_name
        vector = [Q(0)] * len(model.faces)
        vector[face_index["T" + triple_name]] = 1
        for square, coefficient in enumerate((1, -1, 1)):
            vector[face_index[f"Q{support}_{square}"]] = coefficient
        corrected[triple_name] = tuple(vector)

    # Boundary of the oriented simplex [1,2,3,4].
    simplex_terms = (("234", 1), ("134", -1),
                     ("124", 1), ("123", -1))
    assembled = tuple(sum((coefficient * corrected[name][index]
                           for name, coefficient in simplex_terms), Q(0))
                      for index in range(len(model.faces)))
    require(assembled == b0
            and uniform.face_relation_boundary(model, assembled) ==
                (0,) * len(model.edges),
            "corrected deletion boundary stopped being B0")
    numerator_gcd = math.gcd(*[abs(int(value)) for value in assembled
                               if value])
    require(numerator_gcd == 1, "B0 stopped being primitive")
    return {
        "corrected_face_formula": (
            "Theta_(0;ijk)=T_ijk+Q_(0ijk,0)-Q_(0ijk,1)+Q_(0ijk,2)"
        ),
        "primitive_cell": "K_0^del on the oriented complement [1,2,3,4]",
        "boundary_formula": (
            "dK_0^del=Theta_0;234-Theta_0;134+Theta_0;124-Theta_0;123=B0"
        ),
        "nonzero_boundary_faces": sum(bool(value) for value in b0),
        "primitive_integral_gcd": numerator_gcd,
        "normalized_comparison_cell": "K_0^Phi=(1/30)*(K_0^del tensor Phi)",
        "normalized_boundary": "dK_0^Phi=(1/30)B0",
        "five_signed_relabels_span": rank(tuple(map(lambda row: tuple(map(Q, row)),
                                                     relations))),
        "five_relabel_sum": [int(value) for value in
                             uniform.add(*relations)],
        "interpretation": (
            "the Q terms are the three pairwise BC corrections on each "
            "four-support; the cell is a primitive higher deletion simplex, "
            "not a sum of square-only triple cubes"
        ),
    }


def literal_connector_boundary_audit(uniform, physical) -> dict[str, object]:
    model, relations = uniform.canonical_five_relations()
    b0 = relations[0]
    records = []
    for edge_index, (left, right) in enumerate(model.edges):
        contributions = []
        for coefficient, name, boundary in zip(
                b0, model.face_names, model.face_boundaries, strict=True):
            value = coefficient * boundary[edge_index]
            if value:
                contributions.append({"face": name, "coefficient": value})
        require(len(contributions) == 2
                and sum(item["coefficient"] for item in contributions) == 0,
                ("labelled connector cancellation", left, right,
                 contributions))
        left_record = physical.presentation_record(left)
        right_record = physical.presentation_record(right)
        records.append({
            "connector": physical.window_name(left) + "->" +
                         physical.window_name(right),
            "left_word": left_record["word"],
            "right_word": right_record["word"],
            "left_fine": left_record["fine"],
            "right_fine": right_record["fine"],
            "left_removed_reinserted": left_record["removed_edges"],
            "right_removed_reinserted": right_record["removed_edges"],
            "coarse_repeated": "P3+K2",
            "spectator_repeated": "three labelled K2 factors",
            "operation_parent": "Phi-prolonged presentation connector",
            "two_incident_face_contributions": contributions,
            "sum": 0,
        })
    require(len(records) == 30, "literal connector census")
    return {
        "literal_connector_count": len(records),
        "all_connectors_cancel_two_termwise": True,
        "records": records,
        "meaning": (
            "B0 is an exact cycle before forgetting word, fine, removed/"
            "reinserted, repeated or operation-parent labels, provided the "
            "same labelled Phi connector is physical in both incident faces"
        ),
        "conditional_clause": (
            "the ledger identifies identical requested connector labels; it "
            "does not construct the operation-changing Phi connectors"
        ),
    }


def restrict_word(word: str, deleted_tail_indices: tuple[int, ...]) -> str:
    require(len(word) == 14, "h6 word length")
    tail_pairs = tuple(word[4 + 2 * index:6 + 2 * index]
                       for index in range(5))
    return word[:4] + "".join(pair for index, pair in enumerate(tail_pairs)
                               if index not in deleted_tail_indices)


def target_and_protected_readout_audit(uniform, physical) -> dict[str, object]:
    model, relations = uniform.canonical_five_relations()
    b0 = tuple(map(Q, relations[0]))
    presentations = tuple(physical.presentation_record(window)
                          for window in model.vertices)
    literal_words = tuple(sorted({record["word"] for record in presentations}))
    require(len(literal_words) == 4, "literal word census")

    def target(word: str) -> int:
        return int(len(set(word)) == 1)

    mixed_restrictions = []
    for word in literal_words:
        for size in range(6):
            for deleted in combinations(range(5), size):
                restricted = restrict_word(word, deleted)
                require(restricted.startswith("0121") and target(restricted) == 0,
                        ("mixed target survived", word, deleted, restricted))
                mixed_restrictions.append(restricted)
    pure_checks = 0
    for colour in "012":
        word = colour * 14
        for size in range(6):
            for deleted in combinations(range(5), size):
                require(target(restrict_word(word, deleted)) == 1,
                        ("pure target lost group-like deletion", colour,
                         deleted))
                pure_checks += 1

    coefficient_sum = sum(b0)
    triangle_sum = sum(value for value, name in
                       zip(b0, model.face_names, strict=True)
                       if name.startswith("T"))
    square_sum = sum(value for value, name in
                     zip(b0, model.face_names, strict=True)
                     if name.startswith("Q"))
    require(coefficient_sum == triangle_sum == square_sum == 0,
            "B0 coefficient sums")

    cap_signature = {
        "B": MU, "Eq": MU, "target_cap_first_face": MU,
        "M": -MU, "ainc": -MU, "q=M-ainc": Q(0), "P_f": MU,
    }
    cartan_signature = {
        "target_bridge": -MU, "q_bridge": Q(0), "anchor_bridge": Q(0),
        "ores": MU, "W": -MU, "ridge": MU,
    }
    projections = {
        name: str(value * coefficient_sum)
        for name, value in (cap_signature | cartan_signature).items()
    }
    require(all(value == "0" for value in projections.values())
            and cap_signature["q=M-ainc"] ==
                cap_signature["M"] - cap_signature["ainc"],
            "normalized protected projection")

    # q=M-ainc is pointwise and does not enforce cross-face Hasse linearity.
    t123 = model.face_names.index("T123")
    impulse_m = unit(t123, len(model.faces))
    impulse_ainc = (Q(0),) * len(model.faces)
    impulse_q = tuple(left - right for left, right in
                      zip(impulse_m, impulse_ainc, strict=True))
    require(all(q_value == m_value - a_value for q_value, m_value, a_value
                in zip(impulse_q, impulse_m, impulse_ainc, strict=True))
            and dot(b0, impulse_q) == -1,
            "q identity counterguard")

    return {
        "complete_target_word_count": 3 ** 14,
        "pure_target_words": 3,
        "mixed_target_words": 3 ** 14 - 3,
        "literal_mixed_words": list(literal_words),
        "literal_mixed_tail_deletions_checked": len(mixed_restrictions),
        "literal_mixed_target_projection": 0,
        "pure_group_like_tail_deletions_checked": pure_checks,
        "pure_target_B0_projection": int(coefficient_sum),
        "mixed_words_vanish_before_word_or_fine_coarsening": True,
        "normalized_cap_signature": {
            name: str(value) for name, value in cap_signature.items()
        },
        "normalized_bridge_Cartan_signature": {
            name: str(value) for name, value in cartan_signature.items()
        },
        "alternating_B0_projections": projections,
        "B_Eq_W_ores_ridge_all_zero": all(
            projections[name] == "0" for name in
            ("B", "Eq", "W", "ores", "ridge")
        ),
        "target_and_q_compatibility": (
            "complete target is zero termwise on the literal mixed packet "
            "and group-like on pure words; normalized Phi has M=ainc and "
            "therefore q=0 termwise"
        ),
        "q_identity_alone_counterguard": {
            "M": "unit impulse at T123",
            "ainc": 0,
            "q": "M-ainc",
            "alternating_B0_q_readout": -1,
        },
        "logical_conclusion": (
            "complete target plus the pointwise identity q=M-ainc are "
            "compatible with K0 but do not force its cross-face Hasse law"
        ),
    }


def filler_or_terminal_dual_audit(uniform, physical) -> dict[str, object]:
    model, relations = uniform.canonical_five_relations()
    b0 = tuple(map(Q, relations[0]))
    face_rows = tuple(model.face_names)
    protected_rows = (
        "B", "Eq", "target", "M", "ainc", "q", "P_f", "ores",
        "W", "ridge", "eta", "sigma",
    )
    word_rows = tuple("word:" + word for word in sorted({
        physical.presentation_record(window)["word"]
        for window in model.vertices
    }))
    fine_rows = tuple("fine:" + str(
        physical.presentation_record(window)["fine"]
    ) for window in model.vertices)
    repeated_rows = tuple("repeated:" + physical.window_name(window)
                          for window in model.vertices)
    external_rows = protected_rows + word_rows + fine_rows + repeated_rows + (
        "operation:response", "operation:cap", "operation:ordinary-cube",
    )
    row_names = face_rows + external_rows
    width = len(row_names)
    t123 = row_names.index("T123")

    # This is a deliberately stronger grant than the current grammar: every
    # coordinate except the one literal T123 operation-face direction.
    grant = tuple(unit(index, width) for index in range(width)
                  if index != t123)
    candidate = tuple(MU * value for value in b0) + (Q(0),) * len(external_rows)
    detector = unit(t123, width)
    require(rank(grant) == width - 1
            and rank(grant + (candidate,)) == width
            and all(dot(detector, column) == 0 for column in grant)
            and dot(detector, candidate) == -MU,
            "maximal filler-or-terminal gate")
    return {
        "augmented_row_count": width,
        "face_rows": len(face_rows),
        "external_protected_word_fine_repeated_operation_rows":
            len(external_rows),
        "strong_grant": (
            "arbitrary unit fillers on every augmented coordinate except "
            "the literal T123 Phi-presentation face"
        ),
        "rank_grant_then_normalized_K0_boundary": [width - 1, width],
        "terminal_dual": {
            "nonzero_value": "chi(T123)=1",
            "all_other_face_values": 0,
            "all_B_Eq_target_q_W_ores_ridge_values": 0,
            "all_word_fine_repeated_operation_external_values": 0,
            "chi((1/30)B0)": "-1/30",
        },
        "filler_alternative": (
            "adjoin one normalized physical K_0^Phi with "
            "dK_0^Phi=(1/30)B0; its column raises the augmented rank by one"
        ),
        "signed_naturality": (
            "signed S5 transport supplies K_a, sum_a K_a=0, from one K_0"
        ),
        "terminal_scope": (
            "chi is terminal for ordinary square/cube and objectwise "
            "target/q/protected corrections.  It is killed exactly by a "
            "new operation-changing triangle-bearing Hasse three-cell."
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    uniform = load(
        "computations/verify_uniform_johnson_window_hasse_coherence_resolution.py",
        "h6_divided_hasse_uniform_dependency",
    )
    physical = load(
        "computations/verify_h6_signed_standard_three_cell_physical_label_gate.py",
        "h6_divided_hasse_physical_dependency",
    )
    ledger = {
        "theorem": "h6 five-tail divided-Hasse protected boundary gate",
        "pins": PINS,
        "complete_matching_deletion": complete_matching_deletion_audit(),
        "primitive_corrected_deletion_cell":
            corrected_deletion_cell_audit(uniform),
        "literal_word_fine_repeated_boundary":
            literal_connector_boundary_audit(uniform, physical),
        "complete_target_q_and_protected_rows":
            target_and_protected_readout_audit(uniform, physical),
        "exact_filler_or_terminal_dual":
            filler_or_terminal_dual_audit(uniform, physical),
        "verdict": (
            "The response matching species has a canonical primitive "
            "five-tail deletion cell: B0 is the alternating boundary of "
            "four BC-corrected triangles, and all thirty labelled connector "
            "faces cancel without coarsening word, fine, removed/reinserted "
            "or repeated labels.  Complete target equations are compatible: "
            "all literal mixed words vanish before coarsening and pure words "
            "are group-like.  A normalized natural Phi also makes the known "
            "B/Eq/q/W/ores/ridge projections zero.  But target and the "
            "pointwise identity q=M-ainc do not create the comparison "
            "three-cell or force cross-face Hasse-linearity.  The current "
            "square/objectwise grammar retains the exact T123 terminal dual; "
            "the shortest filler is one normalized physical K0^Phi with "
            "boundary (1/30)B0 and signed S5 naturality."
        ),
        "scope": (
            "exact rational complete ten-tail matching polynomial, one "
            "five-edge tail, all ten window presentations, all thirty "
            "labelled connectors, symbolic complete GHZ target, and the "
            "known conditional normalized Phi/cap/Cartan readouts.  The "
            "coefficient deletion cell is constructed; its tensor with Phi "
            "is conditional because the source-labelled operation-changing "
            "Phi and its PP/AugP2 Hasse naturality remain unconstructed."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("h6 divided-Hasse protected ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "matching", "cell",
                                           "labels", "rows", "dual"),
                        default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"h6 divided-Hasse protected boundary ({arguments.mode}): PASS")
        print("complete tail hafnian deletion: 945 terms, all 32 subsets")
        print("literal B0 boundary: 30/30 labelled connectors cancel")
        print("target, normalized B/Eq/q/W/ores/ridge projections: ZERO")
        print("target + q identity force physical K0: NO")
        print("terminal chi(T123): normalized value -1/30")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
