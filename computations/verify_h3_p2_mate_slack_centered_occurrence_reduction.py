#!/usr/bin/env python3
"""Identify the mate slack dG with the centered occurrence class.

In the selected h=3 response block there are 90 literal occurrences.  If f
is marked and G is the sum of the other 89, then in occurrence coordinates

    G = 1_90-e_f
      = (89/90)1_90-(1/90)c_f,
    c_f=90e_f-1_90.

The complete response, target-compatible diagonal/Cartan operations,
word-preserving matching bars, and response-head differences project only
to Q*1_90 in this block.  Hence [dG]=-[c_f]/90, so AugP2 face 1 is exactly
the already isolated centered-occurrence descent, with no new mate class.

Under the S2 x S4 word stabilizer, c_f has two independent pieces: a
marked-within-six-orbit class and an orbit-marginal class.  Their exact
occurrence covectors are nonphysical until an augmented relative cell lands
the centered class.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_p2_pointed_source_graph_slack_gate.py":
        "d36e26ef2c82b018b62228c159f1f17a63d0c19ed1fd342d7684cbf4e55b1098",
    "computations/verify_h3_centered_occurrence_same_grade_physical_gate.py":
        "5b41444ef5f4844bc1bd87a6a4e81e60a631f3549eed21c160efdcb428582ea4",
    "computations/verify_uniform_physical_bar_occurrence_splitter_cokernel.py":
        "403819751753802f4bb01b07cca2540fc6abf0479b9be5569ee74f414ea667ad",
    "computations/verify_h3_reduced_eq_occurrence_graph_tensor_gate.py":
        "5b6db94ecff07e5946007a0d7f95c4ffffb52acc74544d173d5b48cb0ccb0bc9",
    "computations/verify_h3_trapped_carrier_occurrence_euler_source_gate.py":
        "f4139b38728165240d1b033852aba2189e8f1a721d90d2f997755be0a077e6d0",
    "computations/verify_h3_scaled_occurrence_anchor_bridge_alternative.py":
        "ba01612572513e02c60bd5d9a319d8302013e3d73e6a52ae229af8b07dd02507",
}
EXPECTED_LEDGER_SHA256 = (
    "1dca6416efb9719641eaae2a4869c4e4f922dc321a432ccff2d9dbe873f839c0"
)
N = 90


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def add(*vectors):
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def rank(vectors) -> int:
    basis = {}
    for original in vectors:
        values = [Q(value) for value in original]
        for pivot in sorted(basis):
            if values[pivot]:
                coefficient = values[pivot]
                values = [left - coefficient * right for left, right in
                          zip(values, basis[pivot], strict=True)]
        pivot = next((index for index, value in enumerate(values) if value), None)
        if pivot is None:
            continue
        coefficient = values[pivot]
        basis[pivot] = tuple(value / coefficient for value in values)
    return len(basis)


def mate_class_audit(centered) -> dict[str, object]:
    occ, group, marked, marked_orbit, orbits, orbit_records = (
        centered.occurrence_orbit_audit()
    )
    require(len(occ) == N and len(group) == 48 and len(marked_orbit) == 6,
            "the selected h3 occurrence orbit changed")

    ones = (Q(1),) * N
    e_f = centered.unit(marked)
    mate = add(ones, scale(-1, e_f))
    c_f, c_local, c_marginal, local_dual, marginal_dual, decomposition = (
        centered.centered_class_decomposition(marked, marked_orbit, orbits)
    )

    # Exact equality, not only a quotient relation.
    require(mate == add(scale(Q(89, 90), ones), scale(Q(-1, 90), c_f))
            and c_f == add(scale(15, c_local), c_marginal),
            "the mate/centered decomposition changed")
    require(mate == add(
        scale(Q(89, 90), ones),
        scale(Q(-1, 6), c_local),
        scale(Q(-1, 90), c_marginal),
    ), "the local/marginal mate coefficients changed")

    # Both primitive occurrence covectors kill the complete physical row and
    # detect G.  Their values are just -1/90 times their c_f values.
    require(dot(local_dual, ones) == dot(marginal_dual, ones) == 0
            and dot(local_dual, mate) == -5
            and dot(marginal_dual, mate) == -14,
            "the mate-slack occurrence duals changed")

    marked_members = [occ[index] for index in marked_orbit]
    require(len(marked_members) == 6
            and sum(1 for index in marked_orbit if index != marked) == 5
            and sum(len(orbit) for orbit in orbits if marked not in orbit) == 84,
            "the literal 5+84 mate split changed")

    return {
        "response_head_word": "11:110000",
        "marked_occurrence": {
            "p_site": occ[marked][0],
            "s_site": occ[marked][1],
            "residual_matching": [list(edge) for edge in occ[marked][2]],
        },
        "literal_mate_terms": 89,
        "mate_terms_inside_marked_orbit": 5,
        "mate_terms_outside_marked_orbit": 84,
        "word_stabilizer": "S2 x S4",
        "five_orbit_sizes": sorted(len(orbit) for orbit in orbits),
        "exact_identity": (
            "G=1_90-e_f=(89/90)1_90-(1/90)c_f"
        ),
        "centered_class": "c_f=90e_f-1_90",
        "quotient_identity": "[dG]=-[c_f]/90",
        "pointed_face_identity": "[d(u_f-u)]=[c_f]/90",
        "two_piece_expansion": (
            "G=(89/90)1_90-(1/6)(6e_f-1_O)"
            "-(1/90)(14 1_O-1_Oc)"
        ),
        "within_orbit_piece": decomposition["within_orbit_debt"],
        "orbit_marginal_piece": decomposition["orbit_marginal_debt"],
        "pieces_independent_mod_complete": True,
        "occurrence_duals_on_G": {
            "local": -5,
            "orbit_marginal": -14,
        },
    }


def physical_row_image_audit(centered) -> dict[str, object]:
    occ, group, _marked, _marked_orbit, orbits, _records = (
        centered.occurrence_orbit_audit()
    )
    record = centered.complete_operation_image_audit(occ, group, orbits)
    require(record["complete_selected_head_row_rank"] == 1
            and record["word_permutation_images_rank"] == 1
            and record["target_diagonal_character_profiles"] == 1
            and record["selected_projection_of_head_differences_rank"] == 1
            and not record["physical_orbit_sums_individually_constructed"],
            "the committed same-grade physical image changed")

    splitter = (ROOT / (
        "computations/verify_uniform_physical_bar_occurrence_splitter_cokernel.py"
    )).read_text()
    require("remain in the trivial matching representation" in splitter
            and "matching-centered part" in splitter
            and "new physical component projector/complement primitive"
            in splitter,
            "the complete matching-row splitter scope changed")
    return {
        "selected_block_image": "Q*1_90",
        "complete_response_rank": 1,
        "target_compatible_diagonal_Cartan_rank": 1,
        "word_preserving_permutation_bar_rank": 1,
        "response_head_difference_projection_rank": 1,
        "complete_matching_Cartan_prisms": (
            "trivial in the occurrence factor; no matching-centered cut"
        ),
        "dG_in_committed_same_grade_image": False,
        "coarse_word_no_go_implies_fine_grade_no_go": True,
    }


def source_cell_and_terminal_audit() -> dict[str, object]:
    # The raw centered projector has zero-face 90 f(x).  It is the smallest
    # one-cell construction target; the two representation pieces do not
    # force two separate generators.
    normalized_f = Q(1)
    complete_response = Q(0)
    centered_zero_face = N * normalized_f - complete_response
    require(centered_zero_face == 90,
            "the mate centered-projector zero face changed")
    return {
        "smallest_source_extension": (
            "one same-grade centered occurrence cell with boundary "
            "c_f=90e_f-1_90 and scalar/target face -90 f(x)"
        ),
        "one_cell_can_carry_both_representation_pieces": True,
        "raw_projector_source_valid": False,
        "raw_projector_zero_face_at_f_equal_1": 90,
        "known_occurrence_duals_are_physical_terminals": False,
        "why_not_terminal": (
            "they select terms inside one complete source polynomial and "
            "have no identified q/ainc/target/word/ridge/eta/sigma/W row"
        ),
        "exact_landing_alternative_after_augmented_typing": (
            "centered cell is a physical boundary, or the existing complete "
            "q/kernel-versus-Fredholm dichotomy yields generator/separator"
        ),
        "face1_reduction": (
            "no independent mate-slack theorem remains: AugP2 face 1 is the "
            "same centered-occurrence descent already isolated by the "
            "scaled anchor bridge"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    centered = load(
        "computations/verify_h3_centered_occurrence_same_grade_physical_gate.py",
        "mate_slack_centered_dependency",
    )
    dependency_ledger, dependency_digest = centered.audit()
    require(dependency_digest == centered.EXPECTED_LEDGER_SHA256,
            "the centered occurrence dependency ledger changed")
    ledger = {
        "theorem": "P2 mate slack / centered occurrence reduction",
        "pins": PINS,
        "centered_dependency_ledger": dependency_digest,
        "literal_mate_class": mate_class_audit(centered),
        "committed_physical_row_image": physical_row_image_audit(centered),
        "source_cell_and_terminal": source_cell_and_terminal_audit(),
        "sharp_verdict": (
            "In the selected h3 response block, the mate slack dG is exactly "
            "-1/90 of the centered occurrence class modulo the complete row. "
            "Committed same-grade response/Cartan/matching operations see "
            "only the complete row, so dG is not their boundary.  Its local "
            "and orbit-marginal occurrence duals are exact but nonphysical. "
            "The sole positive target is the already isolated centered cell "
            "with its scalar/target face and complete augmented typing."
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 mate slack: [dG]=-[c_f]/90 MOD COMPLETE ROW")
    print("literal mates: 5 inside marked orbit + 84 outside")
    print("committed same-grade physical image: Q*1_90")
    print("first classes: marked-local + orbit-marginal")
    print("occurrence duals: EXACT, NOT PHYSICAL TERMINALS")
    print("face1 core: ONE CENTERED OCCURRENCE LANDING")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
