#!/usr/bin/env python3
"""Composite exact audit of the smallest source-labelled N8 Morse fibre."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_source_morse_hpl_screen.json"
DEPENDENCIES = {
    "abstract_hpl": (
        "computations/verify_augmented_hpl_terminal_bockstein_lemma.py",
        "93f041e93f1e0b6e1968c709a4215600b60358066c46885cec9bea00b228f6e4"),
    "literal_fibre": (
        "computations/verify_n8_literal_hafnian_hpl_no_go.py",
        "501f74cb2441c4ce451fc4db2cc8a1d6c13f7a8bc9eec98a14d115d4a406034e"),
    "relative_4d": (
        "computations/verify_n8_chart25_relative_4d_obstruction.py",
        "edc1b143d174ea6ddd0d449080aadc8084b785dce85f9a96c3b0827ec1ffcac4"),
    "signed_lattice": (
        "computations/verify_n8_chart25_signed_source_lattice.py",
        "0ce609a7aaf564f5387d3d4dfb07121a06925a3383bf3b62087cea71aca44165"),
    "schur_bockstein": (
        "computations/verify_n8_chart25_schur_bockstein_dual_lift.py",
        "086bc864911aef6b62d020c2a16ed82203e6ad3ca87005444e942162fd2a7ed4"),
    "relative_frontier": (
        "computations/verify_n8_chart25_pure_anchor_relative_bridge_frontier.py",
        "0de355496d404d578c4762403690dae387eeb627760558376c53ada57caf4d2e"),
    "path_forest": (
        "computations/verify_n8_chart26_path_forest_skeleton.py",
        "69a673706d95c40e838136743d93ba0a1ba13d3542ae7686e6625c8ca9699475"),
    "terminal_face": (
        "computations/verify_n8_chart26_augmented_terminal_chain.py",
        "1c651d1c5b004ec28fa6d158fd12de21ae3b1c4213131617a545cc8e30b9b490"),
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, relative):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def rank(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    answer = 0
    width = len(work[0]) if work else 0
    for column in range(width):
        pivot = next((row for row in range(answer, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry/value for entry in work[answer]]
        for row in range(len(work)):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left-value*right
                         for left, right in zip(work[row], work[answer])]
        answer += 1
    return answer


def dot(left, right):
    return sum(Fraction(a)*Fraction(b) for a, b in zip(left, right))


def minimal_source_chain():
    # Rows A1,A2,A3,A4,D; columns u_i with d(u_i)=A_i+D.
    boundary = [
        [int(row == column) for column in range(4)]
        for row in range(4)
    ] + [[1, 1, 1, 1]]
    separator = [-1, -1, -1, -1, 1]
    require(rank(boundary) == 4, "minimal source rank changed")
    require(all(dot(separator, [boundary[row][column] for row in range(5)]) == 0
                for column in range(4)), "separator stopped killing boundaries")

    # Reverse the four matched arrows u_i -> A_i.  The only remaining arrows
    # are u_i -> D, so every directed path is A_i -> u_i -> D and no cycle is
    # possible.  This is the complete acyclicity proof for the five-cell fibre.
    directed_edges = []
    for index in range(4):
        directed_edges.append((f"A{index+1}", f"u{index+1}"))
        directed_edges.append((f"u{index+1}", "D"))
    topological_order = ([f"A{index}" for index in range(1, 5)]
                         + [f"u{index}" for index in range(1, 5)] + ["D"])
    positions = {item: index for index, item in enumerate(topological_order)}
    require(all(positions[left] < positions[right]
                for left, right in directed_edges), "Morse cycle appeared")

    quotient_packet = [-1, -1, -1, 0, 1]
    literal_packet = [-1, -1, -1, 0, -3]
    relative_cell = [0, 0, 0, 0, 4]
    require(dot(separator, quotient_packet) == 4,
            "quotient packet class changed")
    require(dot(separator, literal_packet) == 0,
            "literal packet left the source image")
    require([quotient_packet[index]-literal_packet[index]
             for index in range(5)] == relative_cell,
            "relative 4D gap changed")
    # literal_packet=d(-u1-u2-u3)
    coefficients = [-1, -1, -1, 0]
    reconstructed = [sum(boundary[row][column]*coefficients[column]
                         for column in range(4)) for row in range(5)]
    require(reconstructed == literal_packet, reconstructed)
    require(rank([row[:] for row in boundary] + []) == 4, "rank guard")
    augmented = [boundary[row]+[quotient_packet[row]] for row in range(5)]
    require(rank(augmented) == 5, "quotient packet entered source image")

    return {
        "C1_basis": [f"u{index}" for index in range(1, 5)],
        "C0_basis": ["A1", "A2", "A3", "A4", "D"],
        "boundary_matrix_rows_C0_columns_C1": boundary,
        "boundary_rank": 4,
        "H0_dimension": 1,
        "acyclic_matching": [f"u{index}<->A{index}" for index in range(1, 5)],
        "topological_order_after_reversal": topological_order,
        "critical_cells": ["D"],
        "critical_dual_character": separator,
        "Morse_reduction_formula": (
            "[sum_i a_i A_i+dD]=(d-sum_i a_i)[D]"
        ),
        "ordinary_quotient_packet": quotient_packet,
        "ordinary_packet_reduction": "4[D]",
        "ordinary_packet_augmented_rank": 5,
        "literal_source_packet": literal_packet,
        "literal_packet_boundary": "d(-u1-u2-u3)",
        "literal_packet_reduction": 0,
        "source_provenance_gap": relative_cell,
    }


def main():
    degree9_note = ROOT / "notes/degree9-bockstein-mod4.md"
    require(sha256(degree9_note.read_bytes()).hexdigest() ==
            "4564efa0338de72d43f1d854900f802a1de268a234acce0afa0bb29c019701d7",
            "degree-nine Bockstein note changed")
    modules = {name: load(f"source_morse_{name}", relative)
               for name, (relative, _digest) in DEPENDENCIES.items()}
    dependency_ledgers = {}
    for name in ("abstract_hpl", "literal_fibre", "schur_bockstein",
                 "relative_4d", "signed_lattice", "relative_frontier",
                 "path_forest", "terminal_face"):
        ledger, digest = modules[name].audit()
        expected = DEPENDENCIES[name][1]
        require(digest == expected, ("dependency digest", name, digest, expected))
        dependency_ledgers[name] = ledger

    chain = minimal_source_chain()
    literal = dependency_ledgers["literal_fibre"]
    require(literal["canonical_five_row_fibre"]
            ["source_column_multiplicities"] == [3, 4, 4, 3],
            "literal label multiplicities changed")
    require(literal["literal_one_pair_HPL"]["forced_second_transfer"] == "-3D"
            and literal["literal_one_pair_HPL"]["desired_second_transfer"] == "+D",
            "HPL transfer gap changed")
    require([record["nonzero_full_rows"]
             for record in literal["lift_difference_records"]]
            == [180, 180, 204], "labelled lift mutation changed")

    hpl = dependency_ledgers["abstract_hpl"]
    require(hpl["second_transfer"] == {"D": 1},
            "abstract Bockstein normalization changed")
    schur = dependency_ledgers["schur_bockstein"]
    require(schur["local_reduced_residual"] == "4D"
            and schur["local_4D_pairing"] == [1, 1],
            "Schur residual changed")
    require(not schur["full_nine_target_side_factorization"]
            ["literal_source_comparison_constructed"],
            "literal cap comparison unexpectedly appeared")
    relative_4d = dependency_ledgers["relative_4d"]
    signed = dependency_ledgers["signed_lattice"]
    require(relative_4d["frozen_fibre"]["rows"] == schur["local_rows"],
            "4D byte representation differs between frozen theorems")
    critical_d_row = relative_4d["frozen_fibre"]["rows"][-1]
    require(signed["canonical_missing_class"]["D_row"] == critical_d_row,
            "signed-lattice D differs from Schur D")
    require(relative_4d["orbit_transfer"] == {
        "group_order": 8,
        "D_orbit_size": 4,
        "reynolds_4D_coefficients": [1, 1, 1, 1],
        "quotient_D_value": 1,
        "transferred_pairing": [1, 1],
        "source_labels_checked": 14,
        "produces_boundary": False,
    }, "4D orbit transfer changed")
    require(signed["saturated_lattice"]["cokernel_torsion"] == []
            and signed["saturated_lattice"]["cokernel_rank"] == 4,
            "signed cokernel stopped being free rank four")

    frontier = dependency_ledgers["relative_frontier"]
    obstruction = frontier["first_neighbour_lift_obstruction"]
    require((obstruction["source_rank"], obstruction["rank_with_4D_tau"],
             obstruction["base_minor_determinant"],
             obstruction["augmented_minor_determinant"])
            == (88, 89, -1, -4), "relative rank obstruction changed")

    forest = dependency_ledgers["path_forest"]
    require((forest["degree5_leads"], forest["degree6_top_terms"],
             forest["degree6_simple_component_join_terms"])
            == (84005, 372, 300), "path-forest census changed")
    require(forest["weighted_degree6_skeleton"] == "P6+P2"
            and forest["old_lex_degree6_type"]
            == "repeated_decorated_coordinate",
            "term-order mutation guard changed")

    terminal = dependency_ledgers["terminal_face"]
    require(terminal["source_scalars_needed"] == 1
            and terminal["local_hpl_realization"]["naive_error_outputs"] == 4
            and terminal["local_hpl_realization"]["corrected_error_outputs"] == 0,
            "chart26 terminal correction changed")

    payload = {
        "status": "PASS exact source-constrained Morse/HPL bounded audit",
        "minimal_chart25_source_complex": chain,
        "schur_bockstein_relative_class": {
            "class": "4[D]",
            "normalized_pairing": 1,
            "abstract_HPL_D2": "+D",
            "literal_HPL_D2": "-3D",
            "relative_gap": "4D",
            "complete_first_neighbour_columns": 88,
            "complete_first_neighbour_rank": 88,
            "rank_after_adjoining_4D_tau": 89,
            "exact_base_minor": -1,
            "exact_augmented_minor": -4,
            "interpretation": (
                "a nonzero relative obstruction exists, but it obstructs the "
                "desired source lift rather than furnishing a boundary"
            ),
            "novelty": (
                "exact byte-for-byte replay of the previously frozen chart25 "
                "4D Schur--Bockstein class; not a new Ext class"
            ),
        },
        "four_D_identity_and_arithmetic": {
            "critical_D_row": critical_d_row,
            "same_rows_as_frozen_relative_4D": True,
            "same_rows_as_frozen_Schur_Bockstein": True,
            "chart_stabilizer_order": relative_4d["orbit_transfer"][
                "group_order"],
            "D_orbit_size": relative_4d["orbit_transfer"]["D_orbit_size"],
            "Reynolds_4D_orbit_coefficients": relative_4d[
                "orbit_transfer"]["reynolds_4D_coefficients"],
            "Reynolds_produces_boundary": False,
            "complete_signed_cokernel": "Z^4, torsion-free",
            "four_chart_sum_character": [1, 1, 1, 1],
            "four_chart_sum_cancels": False,
            "division_by_four": (
                "D is the primitive nonzero cokernel generator; saturation "
                "forbids turning 4D or D into a source boundary"
            ),
            "two_adic_status": (
                "nonzero in the torsion-free Z_2 cokernel; it becomes zero "
                "after reduction mod 4 only because its coefficient is 4, "
                "which loses rather than proves source provenance"
            ),
            "degree9_mod4_Bockstein_same_class": False,
            "degree9_distinction": (
                "the degree9 H27 class lies in a six-site degree-nine Macaulay "
                "module and has target pairing 2 mod 4; chart25 4D lies in a "
                "20-row/56-column torsion-free local cokernel and reduces to "
                "zero mod 4"
            ),
        },
        "critical_cell_test": {
            "critical_cell": "D, the degree-four parallel-pair row",
            "is_literal_clean_pair_cell": False,
            "target_side_cap_factorization_exists": True,
            "literal_source_to_cap_comparison_exists": False,
            "verdict": (
                "the first critical cell is a source-cokernel class, not an "
                "active clean cap or a six-site descent"
            ),
        },
        "source_unsound_mutations": {
            "forget_fourth_leaf": (
                "replacing the literal -3D transfer by the quotient +D transfer "
                "changes the Morse class by 4[D] and raises rank 4 to 5"
            ),
            "forget_source_labels": {
                "local_homotopy_choices": literal["labelled_h_choices"],
                "pairwise_off_support_difference_rows": [180, 180, 204],
                "local_dual_support_difference_rows": 0,
                "meaning": (
                    "locally identical cancellations define different global "
                    "source chains"
                ),
            },
            "ordinary_lex_term_order": {
                "lead": forest["old_lex_degree6_lead"],
                "type": forest["old_lex_degree6_type"],
                "source_weighted_repair": forest["weighted_degree6_lead"],
                "repaired_type": forest["weighted_degree6_skeleton"],
            },
        },
        "path_forest_interface": {
            "degree4_matching_leads": forest["original_degree4_leads"],
            "degree5_path_forest_leads": forest["degree5_leads"],
            "degree6_top_terms": forest["degree6_top_terms"],
            "degree6_forest_terms": forest[
                "degree6_simple_component_join_terms"],
            "uniform_acyclic_matching_constructed": False,
            "transports_4D_orbit_to_clean_pair": False,
            "reason": (
                "the finite weighted lead repairs one degree-six cell only; "
                "72 top terms are nonforest and higher compatibility cells "
                "have no frozen source-labelled matching.  No archived chain "
                "map takes any of the four D-centres to the cap-error module"
            ),
        },
        "positive_chart26_face_control": {
            "terminal_endpoints": terminal["terminal_endpoints"],
            "active_cap_scalar": -1,
            "literal_boundary": "H_01000111=x_02^00",
            "source_scalars": terminal["source_scalars_needed"],
            "cap_error_outputs_before_after": [4, 0],
            "scope": (
                "one normalized coordinate face and one spoke; no simultaneous-"
                "spoke or off-face contraction"
            ),
        },
        "terminal_verdict": {
            "nonzero_terminal_relative_class": True,
            "critical_cell_is_clean_pair": False,
            "source_provenance_survives_ordinary_Morse_cancellation": False,
            "controls_remote_idempotent": False,
            "new_global_cap_theorem": False,
            "smallest_missing_cell": (
                "a balanced-fine-degree, target/ordinary-residue-zero correction "
                "whose boundary cancels the minimum 774-row off-fibre tail"
            ),
            "retire_ordinary_Morse_matching": True,
            "retain_source_constrained_relative_HPL": (
                "only after the missing dual-invisible nullhomotopy is built"
            ),
        },
        "scope": {
            "broad_Macaulay_solve": False,
            "dependency_logical_digests": {
                name: digest for name, (_relative, digest)
                in DEPENDENCIES.items()},
            "degree9_Bockstein_note_sha256":
                "4564efa0338de72d43f1d854900f802a1de268a234acce0afa0bb29c019701d7",
        },
    }
    payload["logical_sha256"] = logical_sha(payload)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")
    print(json.dumps({
        "logical_sha256": payload["logical_sha256"],
        "chain_size": "4 -> 5",
        "boundary_rank": 4,
        "critical_cells": ["D"],
        "relative_class": "4[D]",
        "critical_cell_clean_pair": False,
        "first_neighbour_ranks": [88, 89],
        "chart26_face_errors": [4, 0],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
