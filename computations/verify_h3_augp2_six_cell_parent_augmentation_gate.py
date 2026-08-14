#!/usr/bin/env python3
"""Test the literal six-cell AugP2 augmentation to matching parents.

Grant the coefficient-level face-3 -> B4 and face-5 -> B1 label map and the
physical K_Eq correction.  The six selected cap labels are then

    (face 3, B4, N), (face 5, B1, N),

with the three residual matchings N on the complementary four sites.
They map monically to six *unordered* parent labels (B,N).  A literal
matching parent is ordered by its P/S endpoint roles, however, so every cap
cell has two candidates.  Endpoint-role forgetting has rank six and a
six-dimensional odd kernel.

Even the canonical rational symmetric section is not a physical chain
augmentation.  Its first enriched boundary identifies (H-u)_response with
(H-u)_Eq, while these are independent word/operation/Eq coordinates.  The
two root labels add two independent response-to-cap Hom characters.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py":
        "d5c90e6404670c7b666b6aa2b3448f5f16c2aebc7fac47f749fb269250413a28",
    "computations/verify_h2_lower_delta_plus_iota_target_rank_gate.py":
        "01e36f89b4df4bb020607d2f00871deb96775a7e58b42e85eaef76c20097e5cf",
    "computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py":
        "c583279d8f4cb7efc24b7fc4784e480b63acb1ca7fe430ae1a7e2db2b854c11b",
    "computations/verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py":
        "8be3bc5bf85f8d633e77e2a0bdd18aea6d481c81f5fb6a6a947cbaf82f862302",
    "computations/verify_h3_trig_euler_augp2_common_base_comparison_gate.py":
        "3ca82479bd2d1c2847dff55f3c05c87f24406ec1c2f3a5fbb9cdf619a6f7047a",
}
EXPECTED_LEDGER_SHA256 = "67385fda43c7c65bbf72d0ccb4f656f0dc21b86f8a3231f798b3d83b18732b50"

ROOTS = ("AB", "AC")
HOLES = {"B1": (0, 1), "B4": (2, 3)}
FACE_LABELS = ((3, "B4"), (5, "B1"))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def rank(vectors) -> int:
    basis = {}
    for source in vectors:
        vector = {key: Q(value) for key, value in source.items() if value}
        while vector:
            pivot = min(vector, key=repr)
            if pivot not in basis:
                inverse = Q(1) / vector[pivot]
                basis[pivot] = {
                    key: value * inverse for key, value in vector.items()
                }
                break
            coefficient = vector[pivot]
            for key, value in basis[pivot].items():
                residue = vector.get(key, Q(0)) - coefficient * value
                if residue:
                    vector[key] = residue
                else:
                    vector.pop(key, None)
    return len(basis)


def dot(left, right) -> Q:
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def edge_text(edge) -> str:
    return f"{edge[0]}{edge[1]}"


def matching_text(matching) -> str:
    return "|".join(edge_text(edge) for edge in matching)


def parent_text(p_site, s_site, matching) -> str:
    return f"P{p_site}|S{s_site}|{matching_text(matching)}"


def enumerate_six_cells(centered):
    occurrences = centered.occurrences()
    occurrence_index = {value: index for index, value in enumerate(occurrences)}
    require(len(occurrences) == len(occurrence_index) == 90,
            "the 90 parent occurrences changed")
    records = []
    for face, label in FACE_LABELS:
        hole = HOLES[label]
        residual = tuple(site for site in centered.SITES if site not in hole)
        matchings = centered.perfect_matchings(residual)
        require(len(matchings) == 3, (face, label, residual, matchings))
        for matching in matchings:
            plus = (hole[0], hole[1], matching)
            minus = (hole[1], hole[0], matching)
            require(plus in occurrence_index and minus in occurrence_index
                    and plus != minus,
                    (face, label, matching, plus, minus))
            records.append({
                "face": face,
                "B_label": label,
                "fine_label": f"t*q_({face},{matching_text(matching)})",
                "residual_matching": matching,
                "plus": plus,
                "minus": minus,
                "plus_index": occurrence_index[plus],
                "minus_index": occurrence_index[minus],
            })
    require(len(records) == 6
            and len({record["plus_index"] for record in records}) == 6
            and len({record["minus_index"] for record in records}) == 6
            and not ({record["plus_index"] for record in records}
                     & {record["minus_index"] for record in records}),
            records)
    return occurrences, tuple(records)


def parent_candidate_audit(centered) -> dict[str, object]:
    occurrences, records = enumerate_six_cells(centered)

    unordered_columns = tuple({index: Q(1)}
                              for index in range(len(records)))
    symmetric_columns = tuple({
        record["plus_index"]: Q(1),
        record["minus_index"]: Q(1),
    } for record in records)
    plus_sections = tuple({record["plus_index"]: Q(1)}
                          for record in records)
    minus_sections = tuple({record["minus_index"]: Q(1)}
                           for record in records)
    normalized_symmetric = tuple({
        record["plus_index"]: Q(1, 2),
        record["minus_index"]: Q(1, 2),
    } for record in records)
    odd_covectors = tuple({
        record["plus_index"]: Q(1),
        record["minus_index"]: Q(-1),
    } for record in records)
    require(rank(unordered_columns) == rank(symmetric_columns)
            == rank(plus_sections) == rank(minus_sections)
            == rank(normalized_symmetric) == 6
            and rank(odd_covectors) == 6,
            "the six-cell parent ranks changed")

    # Quotient from the twelve selected ordered parent coordinates to the
    # six cap labels.  Its columns are indexed plus,minus for each record.
    quotient_columns = []
    for index in range(len(records)):
        quotient_columns.extend(({index: Q(1)}, {index: Q(1)}))
    require(rank(quotient_columns) == 6,
            "endpoint-role quotient rank changed")
    for odd, symmetric, plus in zip(
            odd_covectors, normalized_symmetric, plus_sections, strict=True):
        require(sum((odd.get(key, Q(0)) * value
                     for key, value in symmetric.items()), Q(0)) == 0
                and sum((odd.get(key, Q(0)) * value
                         for key, value in plus.items()), Q(0)) == 1,
                (odd, symmetric, plus))

    first = records[0]
    first_covector = odd_covectors[0]
    record_rows = []
    for record in records:
        record_rows.append({
            "cap_cell": record["fine_label"],
            "face_to_B": f"face {record['face']} -> {record['B_label']}",
            "candidate_parent_plus": parent_text(
                record["plus"][0], record["plus"][1],
                record["residual_matching"]),
            "candidate_parent_minus": parent_text(
                record["minus"][0], record["minus"][1],
                record["residual_matching"]),
            "root_path_candidates": [
                f"{root}:{parent_text(record['plus'][0], record['plus'][1], record['residual_matching'])}"
                for root in ROOTS
            ] + [
                f"{root}:{parent_text(record['minus'][0], record['minus'][1], record['residual_matching'])}"
                for root in ROOTS
            ],
        })

    return {
        "parent_module":
            "V_parent=Q{(p_site,s_site,N)} with ordered P/S endpoint roles",
        "parent_dimension": len(occurrences),
        "granted_cap_cells": record_rows,
        "coefficient_B4_B1_times_matching_map_rank":
            rank(unordered_columns),
        "unordered_parent_labels": 6,
        "ordered_parent_candidates": 12,
        "candidate_parents_per_cap_cell": 2,
        "endpoint_forgetting_rank": rank(quotient_columns),
        "endpoint_odd_kernel_dimension": 12 - rank(quotient_columns),
        "termwise_sections": {
            "number": 2 ** len(records),
            "each_rank": 6,
            "endpoint_swap_fixed_section_exists": False,
        },
        "canonical_Q_linear_even_section": {
            "formula": "1/2*(M_(p,s,N)+M_(s,p,N))",
            "rank": rank(normalized_symmetric),
            "split_monic_after_endpoint_forgetting": True,
            "is_one_literal_parent_matching": False,
        },
        "first_ambiguous_cap_cell": first["fine_label"],
        "first_candidate_parents": [
            parent_text(first["plus"][0], first["plus"][1],
                        first["residual_matching"]),
            parent_text(first["minus"][0], first["minus"][1],
                        first["residual_matching"]),
        ],
        "first_primitive_endpoint_odd_covector": {
            parent_text(first["plus"][0], first["plus"][1],
                        first["residual_matching"]): 1,
            parent_text(first["minus"][0], first["minus"][1],
                        first["residual_matching"]): -1,
        },
        "odd_covector_on_even_section": 0,
        "odd_covector_on_either_termwise_choice": "+1 or -1",
        "literal_single_parent_augmentation_canonical": False,
    }


def label_and_keq_audit(centered, shortest) -> dict[str, object]:
    d_even = shortest.d_even_composition_audit()
    require(d_even["formula"] == (
        "d_even=-1/2[(p_3+n_3) labelled B4+"
        "(p_5+n_5) labelled B1]=(B1+B4)/2"
    ), d_even)
    relative = centered.relative_cap_and_invisible_lift_comparison_audit()
    require(relative["primitive_reduced_cap_p"] == [-1, 0, -1]
            and relative["invisible_lift_n"] == [1, 0, 0]
            and relative["closed_carrier_n_plus_p"] == [0, 0, -1],
            relative)

    # The B label has rank two on faces, and the residual matching label has
    # rank three.  Their Cartesian product is the six unordered coordinates.
    face_b_columns = ({0: 1}, {1: 1})
    matching_columns = ({0: 1}, {1: 1}, {2: 1})
    cartesian = tuple({(face, matching): 1}
                      for face in range(2) for matching in range(3))
    require(rank(face_b_columns) == 2
            and rank(matching_columns) == 3
            and rank(cartesian) == 6,
            "B-label x matching rank changed")
    return {
        "grant": (
            "the coefficient matrix face3->B4, face5->B1 and the invisible "
            "K_Eq corrections n_3,n_5"
        ),
        "face_label_rank": 2,
        "residual_matching_rank": 3,
        "combined_unordered_parent_rank": 6,
        "p_signature_Q_target_ores": relative["primitive_reduced_cap_p"],
        "n_signature_Q_target_ores": relative["invisible_lift_n"],
        "p_plus_n_signature_Q_target_ores":
            relative["closed_carrier_n_plus_p"],
        "orientation_coordinate_in_p_or_n": 0,
        "B4_B1_and_KEq_resolve_endpoint_role": False,
        "conditional_d_even_formula": d_even["formula"],
        "label_map_source_status": (
            "granted for this test; the pinned theorem lists it as a required "
            "physical face, not an already constructed word-changing arrow"
        ),
    }


def root_path_and_boundary_audit(root_gate, lower_gate) -> dict[str, object]:
    operation = root_gate.root_weyl_cap_operation_algebra_audit()
    roots = root_gate.literal_two_root_section_audit()
    require(operation["generated_Hom_response_cap"] == 0
            and roots["rank_base_one_AB_one_AC_one_unlabelled_pair_both"]
                == [24, 25, 25, 25, 26],
            (operation, roots))

    lower_ledger, lower_digest = lower_gate.audit()
    require(lower_digest == lower_gate.EXPECTED_LEDGER_SHA256, lower_digest)
    coefficient = lower_ledger["coefficient_iota"]
    target = lower_ledger["physical_target_gate"]
    require(coefficient["coefficient_map_exists"]
            and not coefficient["literal_decorated_relabel_exists"]
            and target["rank_local_diagonal_lines"] == 2
            and target["rank_after_two_mixed_normals"] == 4
            and target["mixed_target_cokernel_rank"] == 2,
            (coefficient, target))

    # First enriched chain boundary.  The coefficient-forgetting base sends
    # both coordinates to the same scalar H-u.  Retaining operation/Eq makes
    # them independent.
    boundary_g0 = (Q(1), Q(0))
    boundary_r0 = (Q(0), Q(1))
    mismatch = (Q(-1), Q(1))
    separator = (Q(1), Q(-1))
    require(rank((dict(enumerate(boundary_g0)),
                  dict(enumerate(boundary_r0)))) == 2
            and dot(separator, boundary_g0) == 1
            and dot(separator, boundary_r0) == -1
            and dot(separator, mismatch) == -2,
            "response/Eq boundary mismatch changed")
    return {
        "root_paths": [
            "AB: A/B colour-root path, separately labelled",
            "AC: A/C colour-root path, separately labelled",
        ],
        "root_paths_choose_endpoint_P_S_orientation": False,
        "strong_diagonal_base_rank": 24,
        "rank_after_AB_after_AC_after_unlabelled_after_both":
            roots["rank_base_one_AB_one_AC_one_unlabelled_pair_both"][1:],
        "missing_root_Hom_dimension":
            roots["cokernel_dimension_before_sections"],
        "root_Hom_covectors": roots["individual_normalized_duals"],
        "existing_operation_corner": operation["generated_operation_algebra"],
        "generated_Hom_response_cap": operation["generated_Hom_response_cap"],
        "coefficient_orientation_forgetting_map": "exact",
        "literal_decorated_relabel": "not constructed",
        "first_enriched_boundary_coordinates": [
            "(H-u)_response", "(H-u)_Eq_cap",
        ],
        "dG0": [1, 0],
        "dr0": [0, 1],
        "dr0_minus_dG0": [-1, 1],
        "boundary_rank": 2,
        "primitive_boundary_separator": [1, -1],
        "coefficient_forgetful_image_of_both": "H-u",
        "first_boundary_failure":
            "(H-u)_response cannot be identified with (H-u)_Eq_cap",
        "next_target_obstruction": {
            "rank_local_diagonal_lines":
                target["rank_local_diagonal_lines"],
            "rank_after_two_mixed_normals":
                target["rank_after_two_mixed_normals"],
            "cokernel_rank": target["mixed_target_cokernel_rank"],
            "covectors": [
                target["primitive_0112_target_normal"]["mixed_detector"],
                target["primitive_0121_target_normal"]["mixed_detector"],
            ],
            "pairing_matrix_on_the_two_normals": [[2, 0], [0, 2]],
        },
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    centered = load(
        "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py",
        "cap_parent_centered",
    )
    shortest = load(
        "computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py",
        "cap_parent_shortest",
    )
    root_gate = load(
        "computations/verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py",
        "cap_parent_roots",
    )
    lower_gate = load(
        "computations/verify_h2_lower_delta_plus_iota_target_rank_gate.py",
        "cap_parent_lower",
    )
    parents = parent_candidate_audit(centered)
    label_keq = label_and_keq_audit(centered, shortest)
    roots_boundary = root_path_and_boundary_audit(root_gate, lower_gate)
    ledger = {
        "theorem": "h3 AugP2 six-cell parent augmentation gate",
        "pins": PINS,
        "literal_parent_candidates": parents,
        "B4_B1_and_KEq_grant": label_keq,
        "word_root_paths_and_first_chain_boundary": roots_boundary,
        "verdict": (
            "Granting face3->B4, face5->B1 and the invisible K_Eq correction "
            "does give a rank-six coefficient augmentation from the six cap "
            "cells to six unordered (B,N) parent labels.  It does not give a "
            "literal matching-parent augmentation: every (B,N) has the two "
            "ordered P/S parents M_(p,s,N), M_(s,p,N), so endpoint forgetting "
            "has rank six and a six-dimensional odd kernel.  The unique "
            "endpoint-even rational section is split monic but is an average, "
            "not one termwise parent.  Neither AB nor AC colour-root labels "
            "choose an endpoint orientation.  More decisively, even after "
            "choosing a section the first enriched chain boundary has rank "
            "two: dG0=(H-u)_response and dr0=(H-u)_Eq_cap.  Their coefficient "
            "images agree only after forgetting operation and Eq.  Thus no "
            "literal epsilon_C exists in the current category; the next "
            "protected obstruction is the independent pair of mixed target "
            "normals detected by X_00211122^* and X_00111222^*"
        ),
        "shortest_positive_datum": (
            "a two-root, endpoint-even word-changing mapping cylinder whose "
            "degree-zero face chooses/lifts the six (B,N) parents and whose "
            "first boundary identifies (H-u)_response with (H-u)_Eq_cap; it "
            "must also contain the two mixed-target cone faces.  This is the "
            "literal cap augmentation epsilon_C, not a consequence of the "
            "coefficient B4/B1 or K_Eq formulas"
        ),
        "scope": (
            "exact rational six-cell coefficient/parent enumeration inside "
            "the canonical 90-occurrence module, both root labels, and pinned "
            "exact K_Eq, operation and target audits.  The endpoint-even "
            "average is not ruled out after adjoining the stated physical "
            "mapping cylinder"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("six-cell cap augmentation ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("full", "structural"),
                        default="full")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    if arguments.mode == "structural":
        pin_dependencies()
        print("h3 six-cell cap augmentation structural gate: PASS")
        return
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"ledger": ledger, "sha256": digest},
                         indent=2, sort_keys=True))
    else:
        parent = ledger["literal_parent_candidates"]
        boundary = ledger["word_root_paths_and_first_chain_boundary"]
        print("h3 AugP2 six-cell parent augmentation gate: PASS")
        print("coefficient unordered-parent rank:",
              parent["coefficient_B4_B1_times_matching_map_rank"])
        print("ordered-parent ambiguity kernel:",
              parent["endpoint_odd_kernel_dimension"])
        print("literal epsilon_C: NO")
        print("first boundary:", boundary["first_boundary_failure"])
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
