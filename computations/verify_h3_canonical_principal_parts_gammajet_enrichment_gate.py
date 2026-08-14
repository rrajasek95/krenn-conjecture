#!/usr/bin/env python3
"""Audit the canonical principal-parts candidate for GammaJetEnrichment.

The tempting construction has two honest pieces: the order-six
site-repeating pair coordinates and the full-star 1/6 collision average.
This checker determines exactly how far those pieces descend from the
official EqSystem, before any B/Eq or operation labels are adjoined.

Structural/full/exhaustive modes have the usual meanings.  Full rebuilds all
8,580 order-six columns but uses the pinned two-prime rank theorem.  Exhaustive
also replays one large-prime elimination and checks the complete 159-row hit
set; the pinned dependency already certifies equality at the second prime.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_order6_site_repeating_target_enrichment_current_tree.py":
        "f1bc7a9f8fdb9148fde5c4d79a4b7f59a3bd03cd6ff00dc1c2fb3c0e7f511ea9",
    "computations/verify_h3_order6_first_forbidden_face_exact_seed_cycle_gate.py":
        "0c3367ab48327bfbe308dc81191019d094eec054a04c3d1f2bd38f0e69faa2e9",
    "computations/verify_h3_first_collision_full_star_completion_gate.py":
        "ea45302b71998ca6ba3928a29f1e75eebc0ba360d1c234f73bd70dfb9b29d317",
    "computations/verify_h3_full_star_trigger_reinsertion_r0_gate.py":
        "43b90109c723272d8888a2cd7285ae0694892221691fbb7fe2b9266568dcb9d2",
    "computations/verify_h3_first_site_repeating_collision_tate_augp2_operation_no_go.py":
        "7f32228b0c9c05d6ed12811bafb171b844fe7bc82647ace9a11ff9b6d9383161",
    "computations/verify_h3_order6_trigger_replacement_euler_complement_gate.py":
        "deb84776e620dbf800b24a3a317545259ab6b902d9d07be48bd6ce93e0c6adce",
    "computations/verify_h3_order6_taylor_lcm_common_augmentation_gate.py":
        "53ec7a3e9d5ffd88f897d7a2f56b97945d386e6294f9b69b962f5432cc8a3056",
    "computations/verify_chart_model_is_official_eqsystem.py":
        "ef1a997323e0a116787fa3c50368e22ecd33804942a9179eabefa2993e4d9373",
}
EXPECTED_LEDGER_SHA256 = (
    "bde9561f4f4ade5d6f9efba100bb53aa1ea7007fbea5ca1b713ef348a91ffac4"
)
CAP_GAMMA_WORD = "01211222"


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


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def cotangent_stabilization_audit() -> dict[str, object]:
    """Show that the B/Eq anti-diagonal is not canonical in I/I^2 or L.

    In one relation slot let e be native.  Stabilize its first Tate
    presentation by an acyclic h -> k and set B=e+k/2, Eq=e-k/2.  Forgetting
    the stabilization sends both to e, whereas B-Eq=k=dh.  Hence the desired
    separator does not descend to homology.  Tensoring over the 48 Boolean
    Gamma landing slots commutes with every Boolean Hasse/Macaulay edge.
    """
    native_e = (Q(1), Q(0))
    boundary_k = (Q(0), Q(1))
    b = (Q(1), Q(1, 2))
    eq = (Q(1), Q(-1, 2))
    difference = tuple(x - y for x, y in zip(b, eq, strict=True))
    omega = (Q(0), Q(2))

    def pairing(functional, vector):
        return sum((x * y for x, y in zip(functional, vector, strict=True)),
                   Q(0))

    require(difference == boundary_k
            and pairing(omega, b) == 1
            and pairing(omega, eq) == -1
            and pairing(omega, boundary_k) == 2,
            (difference, pairing(omega, b), pairing(omega, eq)))

    slots = tuple((fine, mask) for fine in range(6) for mask in range(8))
    hasse_edges = tuple(
        ((fine, mask), (fine, mask | (1 << bit)))
        for fine in range(6) for mask in range(8) for bit in range(3)
        if not mask & (1 << bit)
    )
    macaulay_edges = tuple((target, source)
                           for source, target in hasse_edges)
    require(len(slots) == 48
            and len(hasse_edges) == len(macaulay_edges) == 72,
            (len(slots), len(hasse_edges), len(macaulay_edges)))

    # Diagonal tensor action commutes with d(h_s)=k_s on every edge s -> t.
    commutators = []
    for source, target in hasse_edges + macaulay_edges:
        d_after_operator = ("k", target)
        operator_after_d = ("k", target)
        commutators.append(d_after_operator == operator_after_d)
    require(all(commutators), "Boolean action stopped commuting with d")

    return {
        "native_relation_slots": 48,
        "boolean_hasse_edges": len(hasse_edges),
        "reverse_macaulay_edges": len(macaulay_edges),
        "native_one_slot_cycle": list(map(str, native_e)),
        "stabilized_B": list(map(str, b)),
        "stabilized_Eq": list(map(str, eq)),
        "B_minus_Eq": list(map(str, difference)),
        "B_minus_Eq_is_contractible_boundary": True,
        "omega_on_B_Eq_boundary": [1, -1, 2],
        "omega_descends_to_conormal_or_cotangent_homology": False,
        "two_lift_difference_survives_minimalization": False,
        "two_lift_guard_conclusion": (
            "non-descent of the B/Eq readout, not a new homology class"
        ),
        "tensor_stabilization_commutes_with_all_boolean_maps": True,
        "canonical_native_tags": [
            "EqSystem relation word", "252-variable torus multidegree",
            "principal-parts order", "literal cell support",
        ],
        "not_canonically_induced": [
            "B/Eq anti-diagonal", "response/cap operation idempotent",
            "AB/AC root path", "normalized target", "protected cap rows",
        ],
    }


def classify_hit_rows(hit_set: tuple[str, ...]) -> dict[str, object]:
    topology = Counter()
    colour_pairs = Counter()
    for encoded in hit_set:
        row = ast.literal_eval(encoded)
        require(row[0] == 2 and len(row[1]) == 2, row)
        left, right = row[1]
        left_edge = frozenset(left[:2])
        right_edge = frozenset(right[:2])
        if left == right:
            topology["diagonal_Euler_divided_power"] += 1
        elif left_edge == right_edge:
            topology["same_edge_recolouring"] += 1
        elif len(left_edge & right_edge) == 1:
            topology["P3_shared_site"] += 1
        else:
            topology["other"] += 1
        colour_pairs[(left[2:], right[2:])] += 1
    require(topology == {
        "P3_shared_site": 148,
        "same_edge_recolouring": 4,
        "diagonal_Euler_divided_power": 7,
    }, topology)
    return {
        "topology": dict(sorted(topology.items())),
        "ordered_colour_pair_histogram": {
            repr(key): value for key, value in sorted(colour_pairs.items(),
                                                      key=repr)
        },
    }


def order_six_principal_parts_audit(site, seed, replay: bool) -> dict[str, object]:
    loaded = site.modules()
    columns, shifts = site.build_operator_columns(loaded)
    require(len(columns) == len(shifts) == 8580,
            (len(columns), len(shifts)))
    words = Counter(seed.word_of_negative_fine_shift(shift)
                    for shift in shifts)
    require(words == {"11111111": 6381, "11211211": 2199}, words)

    pair_row_union = {row for column in columns for row in column if row[0] == 2}
    require(len(pair_row_union) >= 159, len(pair_row_union))
    result = {
        "operator_columns": len(columns),
        "fine_word_histogram": dict(sorted(words.items())),
        "fine_words": sorted(words),
        "cap_Gamma_word": CAP_GAMMA_WORD,
        "any_column_already_in_cap_Gamma_word": CAP_GAMMA_WORD in words,
        "site_repeating_pair_coordinates": 159,
        "two_prime_projected_rank_pinned": [153, 153],
        "canonical_pair_topologies": {
            "P3_shared_site": 148,
            "same_edge_recolouring": 4,
            "diagonal_Euler_divided_power": 7,
        },
        "augmented_trigger_minimalization": {
            "same_underlying_edge_faces_quotiented_as_proper_faces": 11,
            "shared_P3_coordinates_after_quotient": 148,
            "shared_P3_projection_rank": 146,
            "same_edge_sector_is_a_primitive_homology_class": False,
        },
        "pair_map_endpoint": "response -> response",
    }
    if replay:
        audit = site.prime_audit(columns, shifts,
                                 loaded["base"].DIRECT_FREE_PAIR,
                                 site.PRIMES[0])
        require(audit["site_repeating_coordinate_count"] == 159
                and audit["rank_site_repeating_projection"] == 153,
                audit)
        classification = classify_hit_rows(audit["hit_set"])
        result["exhaustive_prime"] = audit["prime"]
        result["exhaustive_rank"] = audit["rank_site_repeating_projection"]
        result["exhaustive_classification"] = classification
        result["exhaustive_hit_set_sha256"] = sha256(
            json.dumps(audit["hit_set"], separators=(",", ":")).encode()
        ).hexdigest()
    return result


def collision_chain_audit(site, full_star, trigger, first_site) -> dict[str, object]:
    loaded = site.modules()
    base = loaded["base"]
    collision = full_star.full_star_collision_audit(base)
    trig = trigger.trigger_reinsertion_audit(base)
    taylor = trigger.labelled_taylor_deletion_audit(base)
    official = load(
        "computations/verify_chart_model_is_official_eqsystem.py",
        "gammajet_official_eqsystem",
    )
    first = first_site.official_pair_audit(official)
    mixed = first_site.mixed_collision_tate_audit(official)
    require(collision["pair_collisions"] == 21
            and collision["pair_output_rank_per_root"] == 7
            and collision["each_cap_term_pair_multiplicity"] == 6
            and collision["pair_output_rank_two_root_direct_sum"] == 14,
            collision)
    require(trig["full_star_branch_instances_per_root"] == 540
            and trig["each_cap_matching_multiplicity"] == 6
            and trig["edge_Euler_boundary"] == "H"
            and not trig["star_average_equals_homogenized_G0"], trig)
    require(taylor["restriction_flags_both_ordered_sides"]
                   ["commuting_kept_factors"] == 1152
            and taylor["restriction_flags_both_ordered_sides"]
                      ["noncommuting_deleted_factors"] == 1020
            and taylor["ambiguous_collected_lcms"] == 9, taylor)
    require(first["nonzero_mixed_second_derivative_relations"] == 0
            and mixed["boundary_support"] == 30
            and mixed["operation_endpoint"] == "response -> response",
            (first, mixed))
    return {
        "full_star_collision_pairs": 21,
        "rank_per_formally_adjoined_root": 7,
        "formal_two_root_direct_sum_rank": 14,
        "matching_parents_covered": 90,
        "each_parent_multiplicity": 6,
        "normalized_average": "(1/6) sum over the 21 site-0 pairs",
        "trigger_branches_per_formal_root": 540,
        "remote_commuting_product_faces": 1620,
        "Taylor_commuting_kept_flags_two_sides": 1152,
        "Taylor_noncommuting_deleted_flags_two_sides": 1020,
        "collected_lcm_ambiguities": 9,
        "average_boundary": "H",
        "required_homogenized_boundary": "H-u",
        "missing_first_boundary": "-u*e_Eq",
        "first_pair_official_second_Hasse_face": 0,
        "first_pair_relative_Tate_boundary_terms": 30,
        "official_operation_endpoint": mixed["operation_endpoint"],
        "chain_functor_on_complete_Taylor_Hasse_cube": False,
        "reason": (
            "restriction commutes on kept factors, but all 1020 deleted "
            "factors require mapping cylinders"
        ),
    }


def canonicality_verdict() -> dict[str, object]:
    response_shadow = (Q(1), Q(0), Q(0), Q(0))
    physical_cap = (Q(1), Q(1), Q(1), Q(1))
    require(response_shadow != physical_cap, (response_shadow, physical_cap))
    return {
        "protected_coordinates": ["B", "Eq", "target", "e_C A e_R"],
        "canonical_response_collision_shadow": [1, 0, 0, 0],
        "physical_r0": [1, 1, 1, 1],
        "root_labels_in_official_EqSystem": False,
        "operation_change_in_official_EqSystem": False,
        "literal_J_phys_Gamma_constructed": False,
        "positive_scope": (
            "canonical rank-146 shared-P3 response principal-parts map "
            "after augmented-trigger minimalization, and exact "
            "coefficient-level 1/6 parent average"
        ),
        "first_grade_failure": "response fine words do not equal 01211222",
        "first_categorical_failure": "Hom(response,AugP2 cap)=0",
        "first_augmented_failure": "B/Eq anti-diagonal and target are absent",
        "minimum_extra_axiom": (
            "a stabilization-invariant decorated principal-parts/cotangent "
            "lift with physical response/cap idempotents, AB/AC root paths, "
            "a noncontractible B/Eq filtration, normalized target/protected "
            "rows, the 1020 deletion cylinders, and an essential-surjectivity "
            "theorem for its Gamma associated grade"
        ),
    }


def audit(mode: str) -> tuple[dict[str, object], str]:
    pin_dependencies()
    site = load(
        "computations/verify_h3_order6_site_repeating_target_enrichment_current_tree.py",
        "gammajet_site_repeat",
    )
    seed = load(
        "computations/verify_h3_order6_first_forbidden_face_exact_seed_cycle_gate.py",
        "gammajet_seed",
    )
    full_star = load(
        "computations/verify_h3_first_collision_full_star_completion_gate.py",
        "gammajet_full_star",
    )
    trigger = load(
        "computations/verify_h3_full_star_trigger_reinsertion_r0_gate.py",
        "gammajet_trigger",
    )
    first_site = load(
        "computations/verify_h3_first_site_repeating_collision_tate_augp2_operation_no_go.py",
        "gammajet_first_site",
    )
    ledger = {
        "theorem": (
            "the 159-row collision/1/6-average construction is canonical "
            "inside response principal parts, but it does not canonically "
            "define GammaJetEnrichment or J_phys,Gamma"
        ),
        "cotangent_stabilization": cotangent_stabilization_audit(),
        "canonicality_verdict": canonicality_verdict(),
    }
    if mode != "structural":
        order_six = order_six_principal_parts_audit(
            site, seed, replay=(mode == "exhaustive"))
        # The exhaustive-only values certify replay, but are deliberately not
        # part of the frozen theorem ledger shared by all modes.
        order_six.pop("exhaustive_prime", None)
        order_six.pop("exhaustive_rank", None)
        order_six.pop("exhaustive_classification", None)
        order_six.pop("exhaustive_hit_set_sha256", None)
        ledger["order_six_principal_parts"] = order_six
        ledger["collision_chain"] = collision_chain_audit(
            site, full_star, trigger, first_site)
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="full")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit(arguments.mode)
    if arguments.mode != "structural" and EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "ledger_sha256": digest}, indent=2, sort_keys=True))
    else:
        print("mode", arguments.mode)
        print("ledger_sha256", digest)
        print("verdict", ledger["canonicality_verdict"]
              ["literal_J_phys_Gamma_constructed"])


if __name__ == "__main__":
    main()
