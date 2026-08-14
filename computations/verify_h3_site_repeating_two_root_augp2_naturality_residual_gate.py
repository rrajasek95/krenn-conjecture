#!/usr/bin/env python3
"""Joint AB/AC audit after the 159-row site-repeating enrichment.

The 159 new rows repair a target-coordinate support obstruction.  They do
not add a response-to-cap operation.  The physical two-word carrier shadow
has a 21-dimensional lift fibre; all committed readouts have rank 14 on it,
leaving seven exact shadow-zero directions.  For separately labelled AB and
AC roots this gives residual dimension 14.  Even granting the strongest
root-covariance graph identifies only the two copies and leaves a diagonal
seven-dimensional residual.

The literal 180-coordinate H_w/private-full-nine identity is injective on
that residual, but it becomes a cap readout only after the missing natural
jet-to-AugP2 dg augmentation is defined.  The nearest existing polynomial
H_w*r0 Koszul S-pair is cap-internal, off-grade here, and target-locked; it
does not define the missing map.
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
    "computations/verify_h3_order6_site_repeating_target_enrichment_current_tree.py":
        "f1bc7a9f8fdb9148fde5c4d79a4b7f59a3bd03cd6ff00dc1c2fb3c0e7f511ea9",
    "computations/verify_h3_reduced_site_repeating_mixed_jet_augp2_enrichment_rhs_gate.py":
        "eaacaae06ec0ba00aab1e13abd62079022d25aa034ed404a3155216e504e4803",
    "computations/verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py":
        "8be3bc5bf85f8d633e77e2a0bdd18aea6d481c81f5fb6a6a947cbaf82f862302",
    "computations/verify_unaudited_repair1_order6_scope_audit.py":
        "0d5be2b2d5c90d5aff04545e7a0712701ef5364266a3ac53f41d7b81da8f530a",
    "computations/verify_h3_rootless_c5_first_higher_anchor_spair.py":
        "3f9c39e8505da148d85a2d5125cefc502321f3652af2d9c0d12cd65aa41d469c",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
}
EXPECTED_LEDGER_SHA256 = (
    "39aef26317c181880c098a929ec8716ef19d3afaa1bafd222b93cc77edf6236e"
)

ROOT_LABELS = ("AB", "AC")
FIBRE_DIMENSION = 21
COMMITTED_READOUT_RANK = 14
RESIDUAL_DIMENSION = FIBRE_DIMENSION - COMMITTED_READOUT_RANK


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
        require(not expected.startswith("TO_BE_"),
                ("unfrozen dependency pin", relative))
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(coefficient: int | Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(coefficient) * entry for entry in vector)


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
    enrichment = load(
        "computations/verify_h3_reduced_site_repeating_mixed_jet_augp2_enrichment_rhs_gate.py",
        "two_root_enrichment",
    )
    receiving = load(
        "computations/verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py",
        "two_root_receiving",
    )
    scope = load(
        "computations/verify_unaudited_repair1_order6_scope_audit.py",
        "two_root_scope",
    )

    enriched_ledger, enriched_digest = enrichment.audit()
    require(enriched_digest == enrichment.EXPECTED_LEDGER_SHA256,
            ("enrichment ledger changed", enriched_digest))
    site = enriched_ledger[
        "site_repeating_target_and_termwise_faithfulness"]
    landing = enriched_ledger["cap_landing_and_exact_missing_axiom"]
    jet = enriched_ledger["universal_reduced_mixed_jet"]
    require(site["current_tree_full_replay"] == {
                "operator_columns": 8580,
                "dim_constrained_universal_D2": 488,
                "site_repeating_pair_coordinates": 159,
                "site_repeating_projection_rank_at_both_primes": 153,
                "direct_free_intersection_dimension": 335,
                "primes": [1_000_003, 999_983],
                "owned_checker": (
                    "verify_h3_order6_site_repeating_target_enrichment_current_tree.py"
                ),
            }
            and site["two_word_root_carrier_fibre"] == 21
            and site["all_committed_readout_rank"] == 14
            and site["residual_root_carrier_freedom"] == 7
            and not site["root_labelled_carrier_maps_to_r0_from_current_data"]
            and landing["Hom0_response_cap_after_row_enlargement"] == 0
            and not landing["Phi_or_root_section_constructed"]
            and jet["termwise_jet_readout_kernel"] == 0,
            (site, landing, jet))

    receiving_ledger, receiving_digest = receiving.audit()
    require(receiving_digest == receiving.EXPECTED_LEDGER_SHA256,
            ("receiving-section ledger changed", receiving_digest))
    sections = receiving_ledger["literal_two_root_sections"]
    require(sections["cokernel_dimension_before_sections"] == 2
            and sections["cokernel_dimension_after_one_labelled_section"] == 1
            and sections["cokernel_dimension_after_both_labelled_sections"] == 0,
            sections)

    scope_ledger, scope_digest = scope.audit()
    require(scope_digest == scope.EXPECTED_LEDGER_SHA256,
            ("order-six scope ledger changed", scope_digest))
    ambiguity = scope_ledger["K_indeterminacy"]
    require(ambiguity == {
        "raw_shadow_fibre": 21,
        "committed_readout_rank": 14,
        "residual_shadow_zero_freedom": 7,
        "meaning": (
            "pair shadow, parity, corner residue, and the encoded coarse "
            "readouts do not pin a termwise physical K; a full-nine or "
            "equivalent higher readout is required"
        ),
    }, ambiguity)
    return {
        "site_repeating_rows": 159,
        "constrained_projection_rank_two_primes": 153,
        "site_rows_are_target_coordinates_not_operation_arrows": True,
        "Hom0_after_enrichment": 0,
        "per_root_shadow_fibre_readout_rank_residual": [21, 14, 7],
        "universal_PS_Q_first_jet_termwise_kernel": 0,
        "receiving_section_Hom_cokernel": 2,
        "missing_axiom": landing["precise_missing_axiom"],
    }


def paired_root_residual_and_covariance_audit() -> dict[str, object]:
    width = len(ROOT_LABELS) * FIBRE_DIMENSION

    def at(root: int, coordinate: int) -> tuple[Q, ...]:
        return unit(width, root * FIBRE_DIMENSION + coordinate)

    # Put the rank-14 committed readout into rational normal form on each
    # root fibre.  Rank and kernel dimensions are invariant under this basis
    # change.  The last seven coordinates are the exact shadow-zero residual.
    committed = tuple(
        at(root, coordinate)
        for root in range(2)
        for coordinate in range(COMMITTED_READOUT_RANK)
    )
    covariance = tuple(
        add(at(0, coordinate), scale(-1, at(1, coordinate)))
        for coordinate in range(FIBRE_DIMENSION)
    )
    termwise_ab = tuple(
        at(0, coordinate)
        for coordinate in range(COMMITTED_READOUT_RANK, FIBRE_DIMENSION)
    )
    termwise_ac = tuple(
        at(1, coordinate)
        for coordinate in range(COMMITTED_READOUT_RANK, FIBRE_DIMENSION)
    )

    committed_rank = rank(committed)
    with_covariance_rank = rank(committed + covariance)
    ab_without_covariance_rank = rank(committed + termwise_ab)
    both_without_covariance_rank = rank(
        committed + termwise_ab + termwise_ac)
    natural_one_representative_rank = rank(
        committed + covariance + termwise_ab)
    require((committed_rank, with_covariance_rank,
             ab_without_covariance_rank, both_without_covariance_rank,
             natural_one_representative_rank)
            == (28, 35, 35, 42, 42),
            "paired root residual ranks changed")

    # A basis for the residual after the maximal covariance grant is the
    # diagonal copy of the last seven axes.
    diagonal_residual = tuple(
        add(at(0, coordinate), at(1, coordinate))
        for coordinate in range(COMMITTED_READOUT_RANK, FIBRE_DIMENSION)
    )
    require(rank(diagonal_residual) == 7,
            "diagonal root residual stopped having dimension seven")
    return {
        "two_labelled_raw_fibres": 42,
        "committed_readout_rank_on_two_fibres": committed_rank,
        "joint_residual_without_root_covariance": width - committed_rank,
        "maximal_AB_AC_covariance_relations": len(covariance),
        "rank_after_committed_readouts_and_covariance": with_covariance_rank,
        "joint_residual_after_maximal_covariance": width - with_covariance_rank,
        "residual_description": (
            "the diagonal copy of the seven shadow-zero, s-odd, w-odd, "
            "corner-zero physical K directions"
        ),
        "one_root_termwise_identity_without_covariance": {
            "rank": ab_without_covariance_rank,
            "residual": width - ab_without_covariance_rank,
            "meaning": "an ad hoc AB landing leaves the AC residual seven",
        },
        "both_separate_termwise_identities_without_covariance": {
            "rank": both_without_covariance_rank,
            "residual": width - both_without_covariance_rank,
        },
        "one_representative_termwise_identity_with_full_naturality": {
            "rank": natural_one_representative_rank,
            "residual": width - natural_one_representative_rank,
            "meaning": (
                "one injective seven-coordinate readout can determine both "
                "roots only when the full AB<->AC covariance graph is part of the map"
            ),
        },
        "termwise_Hw_private_coordinate_dimension_per_root": 180,
        "termwise_identity_rank_on_residual_per_root": 7,
        "termwise_identity_currently_a_cap_readout": False,
    }


def existing_termwise_hw_candidate_audit() -> dict[str, object]:
    spair = load(
        "computations/verify_h3_rootless_c5_first_higher_anchor_spair.py",
        "two_root_hw_spair",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "two_root_hw_base",
    )
    spair.pin_dependencies()
    ledger = spair.audit(base)
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    require(digest == spair.EXPECTED_LEDGER_SHA256, digest)
    generator = ledger["kernel_generator"]
    require(generator["formula"] == "H_w*r0-(H_0-u)*r_w"
            and generator["typed_readout_ainc_w_tgt_ores"]
                == ["-H_w", 0, "H_w", 0]
            and ledger["complete_component"]["rank"] == 180
            and ledger["complete_component"]["kernel_dimension"] == 1,
            ledger)
    return {
        "strongest_existing_polynomial_termwise_pattern": generator["formula"],
        "complete_component_columns_rank_kernel": [181, 180, 1],
        "typed_ainc_word_target_ores":
            generator["typed_readout_ainc_w_tgt_ores"],
        "operation_corner": "cap -> cap",
        "literal_word": ledger["words"]["hamming_one"],
        "desired_section_words": "11110000 -> 01211222",
        "same_literal_grade_as_receiving_sections": False,
        "target_zero_forces_Hw_zero_and_anchor_zero": True,
        "defines_termwise_readout_on_response_residual": False,
        "constructs_e_C_A_e_R": False,
        "conclusion": (
            "termwise H_w multiplication and r0 coexist in an actual source "
            "Koszul relation, but only in the cap diagonal corner; it cannot "
            "be repurposed as the missing jet-to-cap augmentation"
        ),
    }


def exact_stopping_datum_audit() -> dict[str, object]:
    return {
        "unconditional_construction": False,
        "first_operation_failure": (
            "Hom^0(response mixed-jet envelope, AugP2/K_Eq cap)=0 in the "
            "current source-derived operation graph"
        ),
        "exact_carrier_residual_after_maximal_root_covariance": {
            "dimension": 7,
            "properties": [
                "zero pair shadow", "zero committed coarse readouts",
                "s-odd", "w-odd", "zero four-corner residue",
                "diagonal under AB<->AC covariance",
            ],
        },
        "shortest_positive_schema": {
            "name": "A_Gamma,root",
            "map": (
                "J_red,rep_PS/q(EqSystem) -> C_AugP2,Gamma"
            ),
            "instances": ["A/B root", "A/C root"],
            "requirements": [
                "a genuine degree-zero e_C A e_R operation",
                "naturality for the full AB<->AC covariance graph",
                "monic epsilon_s->r0 and c_f->-E normalization",
                "all 159 site-repeating rows retained",
                "the 180-coordinate termwise H_w/private-full-nine readout is defined and rank seven on the residual",
                "literal word/head/fine/repeated tags of both receiving sections",
            ],
        },
        "conditional_effect": (
            "termwise injectivity kills the diagonal residual seven and the "
            "natural schema supplies both root-labelled sections; without the "
            "augmentation, coordinate enrichment alone proves neither"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 site-repeating two-root AugP2 naturality residual gate",
        "pins": PINS,
        "dependency_scope": dependency_scope_audit(),
        "paired_root_residual_and_covariance":
            paired_root_residual_and_covariance_audit(),
        "existing_termwise_Hw_candidate": existing_termwise_hw_candidate_audit(),
        "exact_stopping_datum": exact_stopping_datum_audit(),
        "verdict": (
            "The 159 site-repeating second-jet rows remove the whole-module "
            "coordinate-support debt but contain no degree-zero response-to-cap "
            "map.  Each root-labelled physical lift retains seven exact "
            "shadow-zero directions.  With AB and AC separate the residual is "
            "14; granting the strongest root-covariance graph identifies the "
            "copies but leaves a diagonal residual seven.  The literal "
            "180-coordinate H_w/private identity would be injective on that "
            "residual, but no current cap construction defines it as a readout "
            "of the response carrier.  The existing H_w*r0 Koszul S-pair is "
            "cap-internal, off-grade and target-locked.  Therefore the first "
            "new datum remains one termwise-faithful natural jet-to-AugP2 dg "
            "augmentation, instantiated on both root labels"
        ),
        "scope": (
            "exact rational two-root residual normal form from the pinned "
            "21/14/7 carrier audit, exact root-covariance ranks, and the "
            "current two-prime 159/153 support replay.  The two-prime rank is "
            "not promoted to a rational rank theorem, and the missing "
            "augmentation is specified rather than constructed"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("two-root site-repeating ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "residual", "termwise", "schema"),
                        default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"h3 site-repeating two-root AugP2 gate ({arguments.mode}): PASS")
        print("159-row enrichment changes Hom(response,cap): NO")
        print("AB+AC residual: 14; after maximal covariance: 7")
        print("termwise H_w/private identity on residual: RANK 7, NOT LANDED")
        print("existing H_w*r0 S-pair: CAP-INTERNAL AND TARGET-LOCKED")
        print("missing datum: NATURAL TERMWISE-FAITHFUL JET->AugP2 AUGMENTATION")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
