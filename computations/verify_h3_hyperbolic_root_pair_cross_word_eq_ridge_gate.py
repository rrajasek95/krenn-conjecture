#!/usr/bin/env python3
"""Compose the hyperbolic root pair with the known word/cap interfaces.

The local Pfaffian roots and the fixed-window matching repair give the two
correct coefficient returns A-B and A-C.  This checker asks whether the
committed D4, signed-Weyl and cap graphs turn those returns into physical
cross-word columns from response 11:110000 to cap 01211222.

They do not.  D4 and signed Weyl preserve the source operation/matching and
repeated-grade tags; the cap graph is only a flat spectator in a formal
tensor product.  After the strongest formal grant of a word/fine section,
the first augmented obstruction is the mixed reduced-Eq naturality-square
incidence, not the shifted ridge.  Pairing the two roots cannot cancel it:
the two incidences are independently root-labelled, and after forgetting
that label the z-producing orientation maps their sum to 2E.  The labelled
shifted ridges form a subsequent independent diagonal class.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_balanced_c4_hyperbolic_root_return_gate.py":
        "f52c7a8b447a63ee34b3b41e7bbab713409366e7a5a1a16087032a205da2fa9f",
    "computations/verify_h3_hyperbolic_collision_fixed_window_matching_routing_gate.py":
        "b8d02d77213bbb21d68dbad0aa4d6d1263625de012e413547723999d8d87fada",
    "notes/h3-hyperbolic-collision-fixed-window-matching-routing-gate.md":
        "9ee72f85c69d08b8998f7061a52be2450a9f6e3bb843b8951777961471e16f2a",
    "computations/verify_h3_hyperbolic_root_collision_tate_cobar_totalization_gate.py":
        "c0c6c075388a2eb2d5dad6d133166a3f211dd268183d3e2a5433d922e2ea8ceb",
    "notes/h3-hyperbolic-root-collision-tate-cobar-totalization-gate.md":
        "673722b62a59f10b00aa20796236146df052a4d45eda0764053737bca401e95a",
    "computations/verify_h3_balanced_z_hyperbolic_collision_terminal_gate.py":
        "c68e12a1eac991e676765e89898f53374c419140a6b8bfde20db511dbfe0cd39",
    "computations/verify_h3_cylinder_d4_cartan_graph_lock_bridge_gate.py":
        "f7f7009c4bf1b4849b26a2aaa7b24d36db3b576148a0f247a95bcac5f01cf4e1",
    "notes/h3-cylinder-d4-cartan-graph-lock-bridge-gate.md":
        "91806307285af0878e469a7ca0d191c729135de1950e73c62007ba9014610c72",
    "computations/verify_h3_e14_cap_graph_two_parameter_flat_transport_gate.py":
        "42bf68eeb963d568d1c8d9156d4176bec31a114b6fe804744833364fe3633475",
    "notes/h3-e14-cap-graph-two-parameter-flat-transport-gate.md":
        "61c093eed30cd2fff1be086e6069d344e76a583ee31f93528a31aebe76c5c5d6",
    "computations/verify_h3_e14_pointed_orbit_keq_mapping_cylinder_gate.py":
        "2e4b1a1b9bb5b5be8d0997132b49b95576a28dc6ccb9cfd83db808ace8f52f3e",
    "notes/h3-e14-pointed-orbit-keq-mapping-cylinder-gate.md":
        "f5008f5b7e892b5ce5270faacee4ec9f2bffc2630b8dd15a55cb8f5c6800cb21",
    "computations/verify_h3_gate_ii_signed_weyl_telescope_matching_constant_gate.py":
        "092c90da62c9bd900939388a1ec7110de28f50c7b070d5029069ea3c3c9373a1",
    "computations/verify_h3_gate_ii_switch_weyl_product_rule_idempotent_gate.py":
        "fbd4815eb5c6d46b8dbcd018f6e75237f004e3f52b1ccf47631479b698f9db35",
}
EXPECTED_LEDGER_SHA256 = (
    "af131bf8e657a0ba49cf2a8a0fb8f109698ea239e2d76408551117d4a29efb51"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left, right) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(height):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def dependency_scope_audit(root, routing, totalization, d4, cap_flat, mixed, weyl
                           ) -> dict[str, object]:
    root_ledger, root_digest = root.audit()
    route_ledger, route_digest = routing.audit()
    total_ledger, total_digest = totalization.audit()
    d4_ledger, d4_digest = d4.audit()
    cap_ledger, cap_digest = cap_flat.audit()
    mixed_ledger, mixed_digest = mixed.audit()
    weyl_ledger, weyl_digest = weyl.audit()
    require(root_digest == root.EXPECTED_LEDGER_SHA256
            and route_digest == routing.EXPECTED_LEDGER_SHA256
            and total_digest == totalization.EXPECTED_LEDGER_SHA256
            and d4_digest == d4.EXPECTED_LEDGER_SHA256
            and cap_digest == cap_flat.EXPECTED_LEDGER_SHA256
            and mixed_digest == mixed.EXPECTED_LEDGER_SHA256
            and weyl_digest == weyl.EXPECTED_LEDGER_SHA256,
            "a dependency ledger changed")

    route = route_ledger["h3_fixed_window"]
    d4_word = d4_ledger["cap_word_and_grade"]
    cap_word = cap_ledger["literal_physical_descent"]
    cylinder = mixed_ledger["mapping_cylinder"]
    provenance = weyl_ledger["physical_provenance"]
    require(route_ledger["root_return_to_required_switches"][
                "return_sum"] == "2A-B-C"
            and route_ledger["smallest_exact_source_guard"][
                "h3_selected_collision_monomials"] == 12
            and len(total_ledger["complete_response_boundaries"][
                "records"]) == 4
            and all(record["complete_root_residual_terms"] == 24
                    for record in total_ledger[
                        "complete_response_boundaries"]["records"])
            and total_ledger["unary_and_root_order_boundaries"][
                "sum_of_two_square_commutators"] == "2*q01*H2345"
            and not d4_word["physical_cross_word_cap_transport"]
            and not cap_word["formal_tensor_top_is_physical_source_cell"]
            and cylinder["physical_source_typed_quotient"][
                "available_rank"] == 2
            and cylinder["physical_source_typed_quotient"][
                "rank_with_required_comparison"] == 3
            and "underlying site matching" in provenance[
                "colour_action_preserves"],
            (route, d4_word, cap_word, cylinder, provenance))
    return {
        "local_Pfaffian_returns": root_ledger["two_returns"],
        "fixed_window_matching_repairs": route["collision_occurrences"],
        "fixed_window_collision_source_status": (
            "12 collision sectors remain outside the squarefree source"
        ),
        "earlier_complete_response_obstruction": (
            "four signed 24-term collision splitters, one in each 45-term "
            "missing/doubled sector"
        ),
        "earlier_unary_order_obstruction": "2*q01*H2345, not zero",
        "D4_Cartan_words": {
            "bottom": d4_ledger["literal_tail_transport"]["bottom_word"],
            "D4_top": d4_ledger["literal_tail_transport"]["D4_top_word"],
            "tail_Cartan": d4_ledger["literal_tail_transport"][
                "tail_Cartan_word"],
            "physical_cap": d4_word["physical_cap_word"],
        },
        "D4_Cartan_matching_packet_rank": d4_ledger[
            "literal_tail_transport"]["matching_packet_rank"],
        "signed_Weyl_preserves": provenance["colour_action_preserves"],
        "formal_cap_over_D4_is_flat": cap_ledger[
            "formal_C_times_D4_cap_local_system"][
                "formal_flat_local_system_exists"],
        "literal_cross_word_section_exists": False,
        "mapping_square_rank_before_after_mixed_cell": [2, 3],
    }


def collision_residual_vs_signed_weyl_audit(totalization) -> dict[str, object]:
    # The signed-Weyl telescope is matching-constant: in the literal
    # operation-monomial factor it stays on the 105 squarefree perfect
    # matchings.  Compare that entire marginal with the four complete
    # missing/doubled collision sectors and their signed root residuals.
    # The calculation uses the literal monomial bases, not a declared
    # abstract idempotent.
    telescope = totalization.RESPONSE
    sectors = tuple(totalization.complete_collision_sector(*root["sector"])
                    for root in totalization.ROOTS)
    residuals = tuple(totalization.derivation(
        totalization.RESPONSE, root["replacements"]
    ) for root in totalization.ROOTS)
    universe = tuple(sorted(set(telescope).union(
        *(set(sector) for sector in sectors)
    )))
    require(len(universe) == 105 + 4 * 45,
            ("operation idempotent sectors overlapped", len(universe)))

    def coordinates(polynomial):
        return tuple(Q(polynomial[value]) for value in universe)

    telescope_vector = coordinates(telescope)
    sector_vectors = tuple(coordinates(sector) for sector in sectors)
    residual_vectors = tuple(coordinates(residual) for residual in residuals)
    old = (telescope_vector,) + sector_vectors
    require(rank(old) == 5 and rank(old + residual_vectors) == 9,
            "the pure-Weyl/collision residual rank split changed")
    values = []
    for index, residual in enumerate(residual_vectors):
        detector = scale(Q(1, 24), residual)
        require(dot(detector, telescope_vector) == 0
                and all(dot(detector, sector) == 0
                        for sector in sector_vectors)
                and all(dot(detector, other) == Q(index == other_index)
                        for other_index, other in enumerate(residual_vectors)),
                ("a collision detector stopped separating the Weyl marginal",
                 index))
        values.append({
            "root": totalization.ROOTS[index]["name"],
            "on_pure_Weyl_matching_constant": "0",
            "on_all_symmetric_collision_rows": ["0", "0", "0", "0"],
            "on_own_24_term_residual": "1",
        })
    return {
        "literal_coordinate_count": len(universe),
        "squarefree_matching_coordinates": 105,
        "four_collision_sector_coordinates": 4 * 45,
        "rank_pure_Weyl_plus_four_symmetric_collision_rows": 5,
        "rank_after_four_signed_24_term_residuals": 9,
        "detector_values": values,
        "pure_Weyl_Cartan_marginal_fills_residual": False,
        "exact_reason": (
            "the telescope preserves the squarefree operation matching and "
            "is constant on its 105 matching labels; each residual lies in "
            "a distinct missing/doubled operation sector and is centered "
            "against that sector's symmetric 45-term row"
        ),
    }


def word_section_rank_audit() -> dict[str, object]:
    # Retain one primitive response and one primitive cap class for each root.
    # Old D4/Weyl and cap graphs are block diagonal, hence zero in this
    # relative two-word quotient.  A cross-word arrow is (-response,+cap).
    response_word = tuple(map(int, "11110000"))
    cap_word = tuple(map(int, "01211222"))
    differing = tuple(index for index, pair in enumerate(
        zip(response_word, cap_word, strict=True)) if pair[0] != pair[1])
    require(differing == (0, 2, 4, 5, 6, 7), differing)

    arrow_ab = tuple(map(Q, (-1, 1, 0, 0)))
    arrow_ac = tuple(map(Q, (0, 0, -1, 1)))
    paired = add(arrow_ab, arrow_ac)
    require(rank(()) == 0 and rank((paired,)) == 1
            and rank((arrow_ab, arrow_ac)) == 2,
            "the two-root word-section quotient changed")
    common_duals = (
        tuple(map(Q, (1, 1, 0, 0))),
        tuple(map(Q, (0, 0, 1, 1))),
    )
    require(all(dot(dual, arrow) == 0 for dual, arrow in
                zip(common_duals, (arrow_ab, arrow_ac), strict=True)),
            "a common word class stopped killing its cross arrow")
    return {
        "full_response_word": "11110000 = 11:110000",
        "full_cap_word": "01211222",
        "differing_sites_in_P_S_0_1_2_3_4_5_order": list(differing),
        "hamming_distance": len(differing),
        "old_relative_cross_word_rank": 0,
        "rank_after_one_paired_two_root_arrow": 1,
        "rank_after_two_root_labelled_arrows": 2,
        "interpretation": (
            "a paired cell could carry one diagonal word section, but rootwise "
            "naturality requires both labelled arrows; neither is supplied by "
            "the block-diagonal D4/Weyl/cap inventory"
        ),
    }


def paired_reduced_eq_and_ridge_audit() -> dict[str, object]:
    # Two copies of the exact pointed-orbit/K_Eq source-typed quotient.
    # Per root the rows are (return R, clean central Eq E, mixed-square
    # incidence kappa, shifted ridge gamma).
    #
    # D4 and the clean Koszul edge give the first two coordinate axes.  The
    # cap graph is zero here.  The required physical comparison has the first
    # three entries, and its Kähler face is the fourth axis.
    r1 = tuple(map(Q, (1, 0, 0, 0, 0, 0, 0, 0)))
    e1 = tuple(map(Q, (0, 1, 0, 0, 0, 0, 0, 0)))
    r2 = tuple(map(Q, (0, 0, 0, 0, 1, 0, 0, 0)))
    e2 = tuple(map(Q, (0, 0, 0, 0, 0, 1, 0, 0)))
    base = (r1, e1, r2, e2)
    phi1 = tuple(map(Q, (1, 1, 1, 0, 0, 0, 0, 0)))
    phi2 = tuple(map(Q, (0, 0, 0, 0, 1, 1, 1, 0)))
    gamma1 = tuple(map(Q, (0, 0, 0, 1, 0, 0, 0, 0)))
    gamma2 = tuple(map(Q, (0, 0, 0, 0, 0, 0, 0, 1)))
    paired_phi = add(phi1, phi2)
    paired_gamma = add(gamma1, gamma2)
    mixed_detector = tuple(map(Q, (0, 0, Q(1, 2), 0,
                                   0, 0, Q(1, 2), 0)))
    ridge_detector = tuple(map(Q, (0, 0, 0, Q(1, 2),
                                   0, 0, 0, Q(1, 2))))

    require(rank(base) == 4
            and rank(base + (paired_phi,)) == 5
            and rank(base + (paired_phi, paired_gamma)) == 6
            and rank(base + (phi1, phi2)) == 6
            and rank(base + (phi1, phi2, gamma1, gamma2)) == 8,
            "the paired Eq/ridge ranks changed")
    require(all(dot(mixed_detector, column) == 0 for column in base)
            and dot(mixed_detector, paired_phi) == 1
            and dot(mixed_detector, paired_gamma) == 0
            and all(dot(ridge_detector, column) == 0
                    for column in base + (paired_phi,))
            and dot(ridge_detector, paired_gamma) == 1,
            "the paired Eq/ridge detector values changed")

    # Root labels make cancellation impossible for every sign choice.  Even
    # after forgetting labels, the orientation which produces z is (+,+),
    # so the two mixed and ridge coefficients become 2 rather than zero.
    signed_records = []
    for sign1, sign2 in product((-1, 1), repeat=2):
        signed_phi = add(scale(sign1, phi1), scale(sign2, phi2))
        signed_gamma = add(scale(sign1, gamma1), scale(sign2, gamma2))
        require(rank(base + (signed_phi,)) == 5
                and rank(base + (signed_phi, signed_gamma)) == 6,
                ("a labelled sign choice canceled", sign1, sign2))
        signed_records.append({
            "root_signs": [sign1, sign2],
            "labelled_mixed_rank": rank(base + (signed_phi,)),
            "labelled_after_ridge_rank": rank(
                base + (signed_phi, signed_gamma)),
            "unlabelled_mixed_coefficient": sign1 + sign2,
            "produces_z": (sign1, sign2) == (1, 1),
        })
    require(next(record for record in signed_records
                 if record["produces_z"])["unlabelled_mixed_coefficient"] == 2,
            "the z-producing pair stopped doubling the mixed face")
    return {
        "per_root_rows": [
            "D4/private return R", "clean reduced Eq E",
            "mixed naturality-square incidence kappa", "shifted ridge gamma",
        ],
        "strong_grant_base_rank": 4,
        "rank_after_paired_mixed_comparison": 5,
        "rank_after_paired_shifted_ridge": 6,
        "rank_with_two_individual_mixed_cells": 6,
        "rank_with_all_individual_mixed_and_ridge_faces": 8,
        "normalized_diagonal_detector_values": {
            "paired_mixed_reduced_Eq": "1",
            "paired_shifted_ridge_after_mixed_grant": "1",
        },
        "all_labelled_orientation_signs": signed_records,
        "z_orientation_after_forgetting_root_label": {
            "signs": [1, 1],
            "mixed_Eq_coefficient": 2,
            "ridge_coefficient_if_coarsely_identified": 2,
        },
        "first_augmented_obstruction": (
            "mixed reduced-Eq naturality-square incidence; the clean Eq edge "
            "and D4 return have the right coefficient sum but no mixed 2-cell"
        ),
        "second_augmented_obstruction": (
            "the labelled shifted ridge; formal flatness removes curvature "
            "but does not place gamma or its -d(q_xv^01) connection face"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    root = load(
        "computations/verify_h3_balanced_c4_hyperbolic_root_return_gate.py",
        "root_pair_cross_word_root",
    )
    routing = load(
        "computations/verify_h3_hyperbolic_collision_fixed_window_matching_routing_gate.py",
        "root_pair_cross_word_routing",
    )
    totalization = load(
        "computations/verify_h3_hyperbolic_root_collision_tate_cobar_totalization_gate.py",
        "root_pair_cross_word_totalization",
    )
    d4 = load(
        "computations/verify_h3_cylinder_d4_cartan_graph_lock_bridge_gate.py",
        "root_pair_cross_word_d4",
    )
    cap_flat = load(
        "computations/verify_h3_e14_cap_graph_two_parameter_flat_transport_gate.py",
        "root_pair_cross_word_cap",
    )
    mixed = load(
        "computations/verify_h3_e14_pointed_orbit_keq_mapping_cylinder_gate.py",
        "root_pair_cross_word_mixed",
    )
    weyl = load(
        "computations/verify_h3_gate_ii_signed_weyl_telescope_matching_constant_gate.py",
        "root_pair_cross_word_weyl",
    )
    ledger = {
        "theorem": "h3 hyperbolic root-pair cross-word Eq/ridge gate",
        "pins": PINS,
        "committed_composite_scope": dependency_scope_audit(
            root, routing, totalization, d4, cap_flat, mixed, weyl),
        "signed_24_term_residual_vs_Weyl":
            collision_residual_vs_signed_weyl_audit(totalization),
        "degree_zero_word_section": word_section_rank_audit(),
        "conditional_paired_augmented_test":
            paired_reduced_eq_and_ridge_audit(),
        "verdict": (
            "The local Pfaffian root squares, fixed-window matching repairs, "
            "D4 graph-lock transport, signed-Weyl telescope and flat cap "
            "graph do not construct a physical 11:110000-to-01211222 "
            "word/fine/repeated-grade section.  After formally granting that "
            "section and even granting the clean K_Eq edge, the first "
            "uncancelled augmented face is the mixed reduced-Eq naturality "
            "square.  The two z-oriented roots add this face rather than "
            "canceling it.  The shifted ridge is a second independent face "
            "after the mixed cell is granted; its connection is flat but "
            "still not physically placed."
        ),
        "shortest_positive_object": (
            "one root-labelled paired collision mapping bicomplex whose two "
            "cross-word arrows are natural for the A/B and A/C matching "
            "repairs, whose diagonal two-cell supplies both mixed K_Eq "
            "incidences, and whose proper Kähler faces place both shifted "
            "ridges and -d(q_xv^01) connections in the canonical cap grade"
        ),
        "scope": (
            "exact canonical h=3 fixed-window root pair and the committed "
            "D4/Weyl/cap/K_Eq interfaces; a conditional quotient no-go for "
            "pair cancellation, not an all-resolution or all-h no-go"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("root-pair cross-word ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("physical 11:110000 -> 01211222 section: NOT CONSTRUCTED")
    print("after word-section grant, first obstruction: MIXED REDUCED-EQ")
    print("paired ranks: base 4 -> mixed 5 -> shifted ridge 6")
    print("z-oriented pair coarsens to Eq/ridge coefficients 2/2, not zero")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
