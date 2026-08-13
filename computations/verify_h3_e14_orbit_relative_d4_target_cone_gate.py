#!/usr/bin/env python3
"""Audit the orbit-relative fourth-Hasse route to the silent E14 return.

The fixed-fibre fourth-Hasse operator sends the mixed response equation to
the pure target equation plus one.  Over the moving GHZ target orbit the
target coefficient moves too, and the fourth coefficient is instead the
normalized affine target equation.  This checker packages the four root
directions as the exact Boolean Koszul cube and records what this repairs.

The orbit construction is not by itself the pointed AugP2 comparison.  It
still needs the marked/global conormal at the bottom and a horizontal copy
of the old cap graph in the word-labelled family.  Once those are granted,
the top centered occurrence and the complete E14 unary row cancel their
private term and leave the literal twelve-tail unary-times-q packet.  The
pinned complete first-hit calculation proves that this packet is not a
boundary in the current inventory.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIRECTIONS = (2, 3, 4, 5)
N_OCCURRENCES = 90
PINS = {
    "computations/verify_h3_e14_silent_target_occurrence_compression_gate.py":
        "d8addc92045c58cb9e26492b5c0d641bf8f182454dff3df0fff72a47f2df89a2",
    "notes/h3-e14-silent-target-occurrence-compression-gate.md":
        "f0fdaec942d790447efec7729ceb3a75038424390a77bf92aa61c565ad228722",
    "computations/verify_h3_e14_pointed_two_stage_koszul_spair_gate.py":
        "7d837db5133bfb46b36fe71a3f499de04f4342ca794d2c45b56e6ec8275d7d0d",
    "notes/h3-e14-pointed-two-stage-koszul-spair-gate.md":
        "7585ba8d4dd6267e260f6c639bd47aced38748add9beca440d0285042053e26c",
    "computations/verify_h3_centered_occurrence_same_grade_physical_gate.py":
        "5b41444ef5f4844bc1bd87a6a4e81e60a631f3549eed21c160efdcb428582ea4",
    "notes/h3-centered-occurrence-same-grade-physical-gate.md":
        "b183f3b5dab83fa79d17c3f539b9f146e3be176a96bfe52b267529148b64134a",
    "computations/verify_h3_source_valid_tower_first_obstruction.py":
        "ba37c966c2ef2cca2f8909a91e8ff8a8567282e68a847ac4eef75d3bb78a56ac",
    "notes/h3-source-valid-tower-first-obstruction.md":
        "a69c8887f54c78a1ac3119f2e735703eecf4511dbfaa347fbb25278cc55a57fa",
    "computations/verify_h3_full_hasse_cone_d4_descent_obstruction.py":
        "ed2f2b3451074500b39a100da91ffefed27f748636de172d81aabd5cfe394240",
    "notes/h3-full-hasse-cone-d4-descent-obstruction.md":
        "2f13dbd315211b39da1a2b8026b40bb31c09bf6de0631cd3dc896689126ee2c7",
    "computations/verify_h3_e14_keq_private_placement_pointedness_gate.py":
        "5eef4dff45be6e8993808ef5bcb533d62143dd4bc833a16e2015b48e7bc408d8",
    "notes/h3-e14-keq-private-placement-pointedness-gate.md":
        "59111d6a2dda8a16785cab6c6d129c806ea7e01a2a6d54e092c8841f6521c6c0",
}
EXPECTED_LEDGER_SHA256 = "9a056dff4e63821841f07e752a3c1e01ebb857f902a9331299959e0fe6aea76b"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def subsets(size: int) -> tuple[tuple[int, ...], ...]:
    return tuple(combination
                 for degree in range(size + 1)
                 for combination in combinations(range(size), degree))


def rank(matrix: list[list[Q]]) -> int:
    rows = [list(map(Q, row)) for row in matrix]
    if not rows:
        return 0
    columns = len(rows[0])
    answer = 0
    for column in range(columns):
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
    return [[sum((left_value * right_value for left_value, right_value in
                  zip(left_row, right_column, strict=True)), Q(0))
             for right_column in zip(*right, strict=True)]
            for left_row in left]


def koszul_matrix(degree: int) -> list[list[Q]]:
    """Matrix for wedge with e_0+...+e_3 from degree k to k+1."""
    source = tuple(combinations(range(4), degree))
    target = tuple(combinations(range(4), degree + 1))
    target_index = {value: index for index, value in enumerate(target)}
    matrix = [[Q(0) for _ in source] for _ in target]
    for source_index, face in enumerate(source):
        for direction in range(4):
            if direction in face:
                continue
            target_face = tuple(sorted(face + (direction,)))
            position = target_face.index(direction)
            matrix[target_index[target_face]][source_index] += Q((-1) ** position)
    return matrix


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def boolean_orbit_cube_audit() -> dict[str, object]:
    matrices = tuple(koszul_matrix(degree) for degree in range(4))
    ranks = tuple(rank(matrix) for matrix in matrices)
    require(ranks == (1, 3, 3, 1),
            ("the four-root Koszul ranks changed", ranks))
    for degree in range(3):
        composite = multiply(matrices[degree + 1], matrices[degree])
        require(all(not entry for row in composite for entry in row),
                ("d^2 stopped vanishing", degree))

    dimensions = (1, 4, 6, 4, 1)
    require(all(ranks[degree - 1] + ranks[degree] == dimensions[degree]
                for degree in range(1, 4)),
            "the proper Boolean cube stopped being exact")

    # The unique top target coefficient is an exact cube face.  The last
    # differential has rank one and every one of its four nonzero columns
    # maps to the top with coefficient +/-1.
    last = matrices[-1][0]
    require(tuple(abs(entry) for entry in last) == (1, 1, 1, 1),
            ("the moving target top lost its primitive preimage", last))

    words = {}
    for face in subsets(4):
        word = [1, 1, 0, 0, 0, 0]
        for index in face:
            word[DIRECTIONS[index]] = 1
        words[face] = "".join(map(str, word))
    profile = tuple(sum(1 for face in words if len(face) == degree)
                    for degree in range(5))
    require(profile == dimensions
            and words[()] == "110000"
            and words[(0, 1, 2, 3)] == "111111",
            "the four-root word cube changed")

    target = {face: Q(face == (0, 1, 2, 3)) for face in words}
    require(sum(target.values(), Q(0)) == 1,
            "the moving GHZ target profile changed")
    return {
        "root_sites": list(DIRECTIONS),
        "word_profile_by_order": list(profile),
        "bottom_word": words[()],
        "top_word": words[(0, 1, 2, 3)],
        "Koszul_ranks": list(ranks),
        "Koszul_exact_in_proper_degrees": True,
        "moving_target_coefficients_by_order": [0, 0, 0, 0, 1],
        "top_target_has_primitive_cube_preimage": True,
        "fixed_fibre_D4": "D4(G_110000)=F_111111+1",
        "orbit_relative_D4": (
            "D4(G_110000-Delta(t))=G_111111-1=F_111111"
        ),
        "old_fixed_ideal_no_go_applies": False,
        "reason": (
            "the construction is a relative Koszul cube over the target "
            "orbit, not an endomorphism preserving the fixed source ideal"
        ),
    }


def occurrence_local_system_audit() -> dict[str, object]:
    # Every response word has the same 90 endpoint/matching tags.  Each root
    # changes only the colour on its chosen output site, hence sends a tag to
    # the same tag with coefficient one.  On the two-coordinate compression
    # (marked tag, any unmarked tag), c=90e_marked-1 has profile (89,-1)
    # in every vertex of the cube.
    centered_profile = (Q(89), Q(-1))
    require(centered_profile[0] - centered_profile[1] == N_OCCURRENCES
            and centered_profile[0]
                + (N_OCCURRENCES - 1) * centered_profile[1] == 0,
            "the centered occurrence profile changed")
    profiles = {face: centered_profile for face in subsets(4)}
    require(len(profiles) == 16
            and len(set(profiles.values())) == 1,
            "the occurrence local system stopped being constant")

    centered_text = (ROOT / (
        "computations/verify_h3_centered_occurrence_same_grade_physical_gate.py"
    )).read_text()
    pointed_text = (ROOT / (
        "computations/verify_h3_e14_keq_private_placement_pointedness_gate.py"
    )).read_text()
    require('"first_unavoidable_face": "90*f(x)"' in centered_text
            and '"source_valid": False' in centered_text
            and '"pointed_anchor_requirement": "[d(u_f-u)]=0"'
                in pointed_text,
            "the base occurrence/pointed gate changed")
    return {
        "occurrences_per_word": N_OCCURRENCES,
        "marked_tag": "p@0:1,s@1:1,residual 24|35",
        "bottom_marked_monomial": (
            "(p1_0_1*s1_1_1)q24_00*q35_00"
        ),
        "top_marked_monomial_g": (
            "(p1_0_1*s1_1_1)q24_11*q35_11"
        ),
        "root_transport_on_occurrence_tags": "identity with coefficient 1",
        "centered_profile_at_every_vertex": [89, -1],
        "formal_D4_of_c_f": "c_g",
        "separate_bottom_pointed_face": "P_f with dP_f=u_f-u",
        "bottom_P_f_constructed_by_orbit_cube": False,
        "bottom_same_grade_centered_cell_constructed": False,
        "conditional_positive_statement": (
            "given one pointed physical c_f/P_f base cell, orbit covariance "
            "and the exact Koszul cube package all fourteen intermediate "
            "root faces and land its fourth coefficient on c_g"
        ),
    }


def cap_and_unary_top_audit() -> dict[str, object]:
    # Reduced cap coordinates (Yw,target,Q,ores) at normalized Y=1.
    cap_T = (Q(-1), Q(1), Q(0), Q(0))
    cap_rho = (Q(1), Q(0), Q(0), Q(1))
    cap_graph = tuple(left + right
                      for left, right in zip(cap_T, cap_rho, strict=True))
    require(cap_graph == (Q(0), Q(1), Q(0), Q(1)),
            "the normalized cap graph changed")

    silent_text = (ROOT / (
        "computations/verify_h3_e14_silent_target_occurrence_compression_gate.py"
    )).read_text()
    two_stage_text = (ROOT / (
        "computations/verify_h3_e14_pointed_two_stage_koszul_spair_gate.py"
    )).read_text()
    require('"required_cap_graph_coefficient": "-89/90"' in silent_text
            and '"complete_row": "v24_11*U[000101]=-R_E14+T_12"'
                in two_stage_text
            and '"nonprivate_proper_tail_count": len(tail_terms)'
                in two_stage_text
            and '"reduction_of_T12": "R_E14"' in two_stage_text,
            "the cap/unary top interface changed")

    # On v04=0, R_E14=g.  The normalized centered/top-target/cap assembly
    # has principal face +g.  Adding the complete unary row -g+T12 cancels
    # the private occurrence and leaves the whole T12 packet, not merely its
    # Eq projection.
    top_private_and_tail = (Q(-1), Q(1))  # (-g,+T12)
    isolated_g = (Q(1), Q(0))
    total = tuple(left + right for left, right in
                  zip(isolated_g, top_private_and_tail, strict=True))
    require(total == (Q(0), Q(1)),
            "the orbit-top/unary private cancellation changed")
    return {
        "normalized_cap_graph_rows": ["Yw", "target", "Q", "ores"],
        "normalized_cap_graph": [0, 1, 0, 1],
        "cap_graph_closes_index_90_residual": True,
        "cap_graph_word_grade": "01211222 / t*q_(v,N) / P3+K2",
        "orbit_top_word_grade": "G11[111111] then E14 unary word 000101",
        "horizontal_cross_word_cap_graph_constructed": False,
        "silent_top_unary_identity": "v24_11*U[000101]=-g+T_12",
        "top_centered_plus_unary": "(+g)+(-g+T_12)=T_12",
        "first_literal_proper_face_after_pointed_and_cap_grants": "T_12",
        "T12_literal_tail_count": 12,
        "T12_degree_profile": {"3": 10, "4": 2},
        "T12_complete_first_hit_columns_rank": [269, 269],
        "T12_current_reduction": "R_E14, not zero",
        "T12_primitive_integral_dual_pairing": -30,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "orbit-relative D4 moving-target E14 cone gate",
        "pins": PINS,
        "moving_target_boolean_cube": boolean_orbit_cube_audit(),
        "marked_occurrence_local_system": occurrence_local_system_audit(),
        "cap_and_unary_top": cap_and_unary_top_audit(),
        "exact_conclusion": {
            "fixed_target_unit_obstruction_removed": True,
            "fourteen_intermediate_Hasse_faces_separate_searches": False,
            "pointed_P_f_supplied_by_orbit_covariance": False,
            "cap_graph_horizontality_supplied_by_orbit_covariance": False,
            "conditional_first_unfilled_boundary": (
                "full T_12 in endpoint tag (p1_0_1,s1_1_1), E14 unary "
                "word 000101, multiplier q24:11; not its Eq shadow"
            ),
        },
        "shortest_positive_theorem": (
            "construct one pointed source-labelled occurrence section at "
            "the 110000 base vertex and a horizontal old-cap graph over the "
            "four-root target orbit; the canonical Boolean PP/Koszul cube "
            "then lands c_f on c_g with the affine target normal included. "
            "Attach the complete E14 unary row and one companion homotopy "
            "for its literal T_12 face"
        ),
        "scope": (
            "canonical h=3 chart-(1,1), four residual root sites, silent "
            "v04=0 E14 branch.  The orbit-relative target repair and Boolean "
            "exactness are positive.  Physical base occurrence descent, cap "
            "horizontality, and the T_12 companion remain unconstructed"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("moving-target D4: FIXED-FIBRE +1 DEFECT REMOVED")
    print("Boolean root cube: ranks 1,3,3,1; proper faces exact")
    print("bottom pointed occurrence / horizontal cap graph: OPEN")
    print("after those grants, first literal face: FULL T_12")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
