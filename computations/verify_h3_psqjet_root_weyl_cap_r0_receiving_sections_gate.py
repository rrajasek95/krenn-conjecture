#!/usr/bin/env python3
"""Audit the two root-labelled ``d(q01*u^-) -> r0`` receiving sections.

The relative Boolean/Kahler presentation already supplies the source jet.
This checker gives the strongest root/Weyl plus cap-r0 candidate every
diagonal tag repair and asks only for the operation-changing matrix units.

There are two independent units, one for the A/B root and one for the A/C
root.  Root/Weyl operations are response-internal and r0 is cap-internal, so
their generated operation algebra is diagonal.  A single labelled section,
or one unlabelled sum of the sections, raises rank by only one.  Rootwise
naturality needs both independent columns.

The surviving Hom covectors are not the terminal counterguard omega_0102.
The sections are degree-zero, cross-word, carrier-visible maps landing in a
tied B=Eq r0.  Omega_0102 is a degree-one same-Gamma primitive with zero
canonical shadow and untied boundary (delta,0).
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
    "computations/verify_h3_psqjet01_divided_hasse_relative_dga_gate.py":
        "35ff02f00b3babe7710319f184894681a08d6c035435be949eccb2579aa8d978",
    "computations/verify_h3_phi_ks_r0_pf_minimal_executable_ansatz_gate.py":
        "d21d776ec53babb4f99693e4dad51d87309e3ed0cccf2e34fb6025e6d74d1009",
    "computations/verify_h3_hyperbolic_root_pair_cross_word_eq_ridge_gate.py":
        "0760703ace1498cc9c255dd8a2017395ece9a7750ab6a21c88233518e1314bba",
    "computations/verify_h3_gate_ii_signed_weyl_telescope_matching_constant_gate.py":
        "092c90da62c9bd900939388a1ec7110de28f50c7b070d5029069ea3c3c9373a1",
    "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py":
        "02a28ec54b83b2f786e47b0fdc992f5f28dd95a04ba16219f0e24482d4999097",
    "computations/verify_h3_gamma_star_source_derived_free_closure_census.py":
        "a479ac8759bf7a18b43ee91d8b1ab7d0b432c48a7787b065cac68403ace3df3a",
    "computations/verify_h3_gate_ii_chiw_nonfill_full_augmented_dual.py":
        "c62ca38edf160f706d7aed237a923737ca46fe7b906fb0bb48bdf400e2ea7854",
}
EXPECTED_LEDGER_SHA256 = (
    "d65cf3b7c2e7528badc87c6e7c36cd1d17e1be11f2cbc6e812225cbf590ee229"
)

ROOTS = (
    {"name": "AB", "root": "0<->1", "repair": "A/B"},
    {"name": "AC", "root": "0<->2", "repair": "A/C"},
)
TAGS = (
    "id_response", "id_cap", "Hom_response_cap",
    "word_response", "word_cap",
    "head_response", "head_cap",
    "fine_response", "fine_cap",
    "repeated_response", "repeated_cap",
    "operation_response", "operation_cap",
)


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


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(coefficient: int | Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(coefficient) * entry for entry in vector)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def unit(width: int, index: int) -> tuple[Q, ...]:
    return tuple(Q(position == index) for position in range(width))


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    columns = tuple(tuple(map(Q, column)) for column in columns)
    if not columns:
        return 0
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


def dependency_scope_audit() -> dict[str, object]:
    psqjet = load(
        "computations/verify_h3_psqjet01_divided_hasse_relative_dga_gate.py",
        "receiving_psqjet",
    )
    ansatz = load(
        "computations/verify_h3_phi_ks_r0_pf_minimal_executable_ansatz_gate.py",
        "receiving_ansatz",
    )
    cross_word = load(
        "computations/verify_h3_hyperbolic_root_pair_cross_word_eq_ridge_gate.py",
        "receiving_cross_word",
    )
    telescope = load(
        "computations/verify_h3_gate_ii_signed_weyl_telescope_matching_constant_gate.py",
        "receiving_telescope",
    )
    comparison = load(
        "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py",
        "receiving_comparison",
    )
    gamma = load(
        "computations/verify_h3_gamma_star_source_derived_free_closure_census.py",
        "receiving_gamma",
    )

    psq_ledger, psq_digest = psqjet.audit()
    require(psq_digest == psqjet.EXPECTED_LEDGER_SHA256,
            "PSQJet ledger changed")
    domain = psq_ledger["domain_and_next_landing"]
    require(domain["relative_u_minus_and_four_faces_present"]
            and domain["relative_PSQJet_present_by_DGA_product"]
            and not domain["literal_head_fine_section_constructed"], domain)

    old, sections, paired_dual = ansatz.build_section_block()
    require(rank(old) == 4 and rank(old + sections) == 6
            and dot(paired_dual, add(*sections)) == 1,
            "ansatz section block changed")

    word = cross_word.word_section_rank_audit()
    require(word["old_relative_cross_word_rank"] == 0
            and word["rank_after_one_paired_two_root_arrow"] == 1
            and word["rank_after_two_root_labelled_arrows"] == 2, word)

    telescope_ledger, telescope_digest = telescope.audit()
    require(telescope_digest == telescope.EXPECTED_LEDGER_SHA256,
            "signed-Weyl ledger changed")
    provenance = telescope_ledger["physical_provenance"]
    require("underlying site matching" in provenance["colour_action_preserves"]
            and "repeated-edge label" in provenance["colour_action_preserves"]
            and not provenance["connected_SL3_or_Weyl_changes_B_label"],
            provenance)

    comparison_ledger, comparison_digest = comparison.audit()
    require(comparison_digest == comparison.EXPECTED_LEDGER_SHA256,
            "response/cap comparison ledger changed")
    hom = comparison_ledger["literal_idempotent_Hom"]
    require(hom["Hom_degree0_response_to_cap_in_current_grammar"] == 0,
            hom)

    exotic = gamma.exotic_search_audit()["smallest_unexcluded_extension"]
    require(exotic == {
        "name": "omega_0102",
        "operation_type": "response->cap",
        "relative_degree": 1,
        "canonical_shadow": 0,
        "B_Eq_boundary": "(delta,0)",
        "all_external_rows": 0,
        "chi": 4,
        "quotient_rank_effect": "8->9",
        "source_provenant_operation_asserted": False,
    }, exotic)
    return {
        "relative_source_jet": domain["next_required_absolute_map"],
        "literal_head_fine_section_constructed": False,
        "old_cross_word_rank": word["old_relative_cross_word_rank"],
        "one_paired_arrow_rank": word[
            "rank_after_one_paired_two_root_arrow"],
        "two_labelled_arrows_rank": word[
            "rank_after_two_root_labelled_arrows"],
        "signed_Weyl_preserves": provenance["colour_action_preserves"],
        "existing_Hom0_response_cap": 0,
        "terminal_control": exotic,
    }


def matrix_multiply(left: tuple[tuple[Q, Q], tuple[Q, Q]],
                    right: tuple[tuple[Q, Q], tuple[Q, Q]]):
    return tuple(tuple(sum((left[row][middle] * right[middle][column]
                            for middle in range(2)), Q(0))
                       for column in range(2)) for row in range(2))


def root_weyl_cap_operation_algebra_audit() -> dict[str, object]:
    # Matrix rows are targets and columns are sources, ordered (R,C).
    e_response = ((Q(1), Q(0)), (Q(0), Q(0)))
    e_cap = ((Q(0), Q(0)), (Q(0), Q(1)))
    response_to_cap = ((Q(0), Q(0)), (Q(1), Q(0)))
    zero = ((Q(0), Q(0)), (Q(0), Q(0)))
    require(matrix_multiply(e_cap, e_response) == zero
            and matrix_multiply(e_response, e_cap) == zero
            and matrix_multiply(e_cap, response_to_cap) == response_to_cap
            and matrix_multiply(response_to_cap, e_response)
                == response_to_cap,
            "operation idempotent multiplication changed")

    # Root/Weyl and the carrier jet are in e_R A e_R; r0 and all its cap
    # normalizers are in e_C A e_C.  Their generated algebra is diagonal.
    diagonal_coordinates = (
        tuple(map(Q, (1, 0, 0))),
        tuple(map(Q, (0, 1, 0))),
    )
    desired = tuple(map(Q, (0, 0, 1)))
    operation_dual = desired
    require(rank(diagonal_coordinates) == 2
            and rank(diagonal_coordinates + (desired,)) == 3
            and all(dot(operation_dual, value) == 0
                    for value in diagonal_coordinates)
            and dot(operation_dual, desired) == 1,
            "diagonal/off-diagonal operation split changed")
    return {
        "objects": ["response occurrence/PSQJet carrier", "AugP2/K_Eq cap r0"],
        "root_Weyl_corner": "e_R A e_R",
        "cap_r0_corner": "e_C A e_C",
        "mixed_products_eC_eR_and_eR_eC": 0,
        "generated_operation_algebra": "Q*e_R direct-sum Q*e_C",
        "generated_Hom_response_cap": 0,
        "formal_external_tensor_product_is_physical_composition": False,
        "missing_matrix_unit": "e_C w e_R",
        "normalized_operation_dual": [0, 0, 1],
        "consequence": (
            "root/Weyl may transport the response word and r0 supplies a "
            "complete tied cap endpoint, but their product cannot change the "
            "source operation object"
        ),
    }


def literal_two_root_section_audit() -> dict[str, object]:
    width_per_root = len(TAGS)
    width = len(ROOTS) * width_per_root

    def at(root: int, tag: str) -> tuple[Q, ...]:
        return unit(width, root * width_per_root + TAGS.index(tag))

    # This is stronger than the physical candidate: grant every diagonal
    # word/head/fine/repeated/operation coordinate independently and omit
    # only the response->cap matrix unit.  Failure here implies failure for
    # the actual root/Weyl plus r0 subspan.
    strong_base = tuple(
        at(root, tag)
        for root in range(len(ROOTS))
        for tag in TAGS if tag != "Hom_response_cap"
    )
    sections = []
    hom_duals = []
    for root in range(len(ROOTS)):
        section = at(root, "Hom_response_cap")
        for kind in ("word", "head", "fine", "repeated", "operation"):
            section = add(section, scale(-1, at(root, f"{kind}_response")),
                          at(root, f"{kind}_cap"))
        sections.append(section)
        hom_duals.append(at(root, "Hom_response_cap"))
    sections = tuple(sections)
    hom_duals = tuple(hom_duals)
    paired = add(*sections)
    paired_dual = scale(Q(1, 2), add(*hom_duals))
    anti_diagonal_dual = scale(Q(1, 2), add(hom_duals[0],
                                                  scale(-1, hom_duals[1])))

    base_rank = rank(strong_base)
    rank_ab = rank(strong_base + (sections[0],))
    rank_ac = rank(strong_base + (sections[1],))
    rank_paired = rank(strong_base + (paired,))
    rank_both = rank(strong_base + sections)
    require((base_rank, rank_ab, rank_ac, rank_paired, rank_both)
            == (24, 25, 25, 25, 26),
            "two-root receiving-section ranks changed")
    require(all(dot(dual, column) == 0 for dual in hom_duals
                for column in strong_base)
            and dot(hom_duals[0], sections[0]) == 1
            and dot(hom_duals[0], sections[1]) == 0
            and dot(hom_duals[1], sections[0]) == 0
            and dot(hom_duals[1], sections[1]) == 1
            and dot(paired_dual, paired) == 1
            and dot(anti_diagonal_dual, paired) == 0
            and dot(anti_diagonal_dual, sections[0]) == Q(1, 2)
            and dot(anti_diagonal_dual, sections[1]) == Q(-1, 2),
            "root-labelled Hom duals changed")

    root_records = []
    for root in ROOTS:
        root_records.append({
            **root,
            "domain": {
                "word": "11110000 = 11:110000",
                "head": "ordered mixed response heads 01/10",
                "fine": "six P4+K2 tail pairs plus three 4K2 dq01 pairs",
                "repeated": "relative occurrence carrier at sites 0,1",
                "operation": "response occurrence/P_f; PS-over-q01 jet",
            },
            "target": {
                "word": "01211222",
                "head": root["repair"] + " root-labelled cap section",
                "fine": "six t*q_(v,N) occurrence degrees",
                "repeated": "P3+K2",
                "operation": "AugP2/K_Eq cap r0",
            },
        })
    return {
        "root_records": root_records,
        "tag_basis_per_root": list(TAGS),
        "strong_grant": (
            "all diagonal word/head/fine/repeated/operation repairs are "
            "adjoined independently; only Hom(response,cap) is withheld"
        ),
        "rank_base_one_AB_one_AC_one_unlabelled_pair_both": [
            base_rank, rank_ab, rank_ac, rank_paired, rank_both,
        ],
        "cokernel_dimension_before_sections": 2,
        "cokernel_dimension_after_one_labelled_section": 1,
        "cokernel_dimension_after_one_unlabelled_paired_section": 1,
        "cokernel_dimension_after_both_labelled_sections": 0,
        "individual_normalized_duals": [
            "omega_AB^Hom", "omega_AC^Hom",
        ],
        "paired_detector": "(omega_AB^Hom+omega_AC^Hom)/2",
        "survivor_after_unlabelled_pair":
            "(omega_AB^Hom-omega_AC^Hom)/2",
        "first_exact_failure": (
            "two independent root-labelled response-to-cap operation matrix "
            "units; a single section or a root-forgetting aggregate is rank-insufficient"
        ),
    }


def terminal_omega_comparison_audit() -> dict[str, object]:
    delta = tuple(map(Q, (1, 1, -1, -1)))
    psi = delta + tuple(-value for value in delta)
    tied_r0 = delta + delta
    bright_omega = delta + (Q(0),) * 4
    require(dot(psi, tied_r0) == 0
            and dot(psi, bright_omega) == 4,
            "tied/bright B-Eq comparison changed")
    distinctions = {
        "relative_degree": [0, 1],
        "word": ["11110000 -> 01211222", "Gamma_* / 0102"],
        "canonical_carrier_shadow": [
            "d(q01*u^-) with selected db01 incidence", "0"],
        "B_Eq_landing_or_boundary": ["(delta,delta)", "(delta,0)"],
        "Psi_charge": [0, 4],
        "root_multiplicity": ["two labelled A/B,A/C sections", "one exotic class"],
    }
    require(all(left != right for left, right in distinctions.values()),
            "a section signature collided with omega_0102")
    return {
        "section_family": {
            "type": "degree-zero Phi_KS,r0 receiving maps",
            "canonical_shadow": "nonzero relative PSQJet carrier",
            "cap_landing_B_Eq": "(delta,delta)",
            "Psi": 0,
            "standard_degree_one_products": (
                "the eight K_Eq naturality interchanges, all tied/Psi-dark"
            ),
        },
        "terminal_control": {
            "name": "omega_0102",
            "type": "independently primitive Hom^1_Gamma*(response,cap)",
            "canonical_shadow": 0,
            "boundary_B_Eq": "(delta,0)",
            "Psi": 4,
            "source_provenant": False,
        },
        "signature_distinctions": distinctions,
        "coincides_with_bright_omega_0102": False,
        "precise_relation": (
            "both require an off-diagonal response-to-cap operation type, "
            "but the receiving sections are the missing degree-zero parent "
            "of the eight dark kappa cells; omega_0102 is the independent "
            "bright ninth-degree-one counterguard which the section does not fill or exclude"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 PSQJet root/Weyl plus cap-r0 receiving-section gate",
        "pins": PINS,
        "dependency_scope": dependency_scope_audit(),
        "root_Weyl_cap_operation_algebra":
            root_weyl_cap_operation_algebra_audit(),
        "literal_two_root_sections": literal_two_root_section_audit(),
        "terminal_omega_comparison": terminal_omega_comparison_audit(),
        "verdict": (
            "The strongest source-provenant root/Weyl plus r0 candidate does "
            "not construct either receiving section.  Root/Weyl remains in "
            "the response diagonal corner and r0 remains in the cap diagonal "
            "corner, so every product has zero response-to-cap matrix-unit "
            "coordinate.  Even after granting every word, head, fine, repeated "
            "and operation-boundary repair, the two root-labelled Hom axes form "
            "a two-dimensional quotient.  One labelled section or one "
            "root-forgetting aggregate raises rank by only one; both A/B and "
            "A/C sections are required.  Their exact Hom dual is not the "
            "terminal bright omega_0102: the sections are degree-zero, "
            "carrier-visible and land in tied B=Eq r0, whereas omega_0102 is "
            "degree-one, shadow-free and has untied (delta,0) boundary"
        ),
        "shortest_positive_datum": (
            "one source constructor/API for Phi_KS,r0 natural in the root "
            "label, with two literal instances on A/B and A/C and with the "
            "displayed word/head/fine/repeated boundary incidences"
        ),
        "scope": (
            "exact h=3 relative PSQJet domain, signed-Weyl provenance, tied "
            "balanced cap r0, two-root labelled tag quotient and comparison "
            "with the formal omega_0102 terminal control.  This does not prove "
            "global nonexistence of an unregistered operation-changing source cell"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("receiving-section ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "candidate", "sections", "terminal"),
                        default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"h3 PSQJet -> r0 receiving sections ({arguments.mode}): PASS")
        print("root/Weyl + r0 Hom(response,cap): ZERO")
        print("two root-labelled section quotient: DIMENSION TWO")
        print("one labelled or unlabelled-paired section: RANK-INSUFFICIENT")
        print("first exact dual: root-labelled Hom operation character")
        print("same as terminal bright omega_0102: NO")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
