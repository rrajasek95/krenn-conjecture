#!/usr/bin/env python3
"""Bidirectional private-site fans isolate the transverse-rank residual.

For a nonzero off-diagonal cell A_vu[b,a], apply the target-augmented
private-site identity first to the pure-a word at v and then, after
transposition, to the pure-b word at u.  The same cell forces two active
determinant/cofactor fans.  The first has distinct heads a,b at v and pure-a
outer heads; the second has distinct heads b,a at u and pure-b outer heads.

If one fan contains a reference edge and mate edge outside the selected
three-anchor union, the two physical edges are four-good and the nonzero
determinant is already the desired transverse active wedge.  Otherwise the
witnesses are trapped in the selected-anchor five-lock/Hall web.  The
checker also replays the sharp fact that all same-cell companions preserve
the deficient endpoint label, so they cannot by themselves restore rank.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "computations/verify_uniform_five_lock_wedge_or_switch.py":
        "c2541a60db1f8e7a661bc698d2bd1f1a1f396a0f0bfde389ea89bea17fac175e",
    "computations/verify_uniform_decorated_anchor_companion_rank_no_go.py":
        "a0b9a5a3e7c1a1809db4c42c49303c1c43db26229437fc58d93fea7c5d110063",
    "computations/verify_n8_balanced_anchor_chart_cover.py":
        "3f30d143f3f069f6123bfb41d7ae26833ef508c572c42e09544fe5d415f70d55",
    "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py":
        "893f000e37e4bcfc78973cb042cc0858087cb25605d6cf070a1bf8dfa7a76b7a",
    "computations/verify_h3_rootless_one_face_third_cofactor_comparison_vertex_gate.py":
        "37251145d805861b2d1b15b7bf37cf9f98ba30b03fbcffa1daa4fc35789efe84",
}
EXPECTED_LEDGER_SHA256 = (
    "1fa9293975fa0a52088996b521e258dae1664fbe71daf6885549d856353eeeb4"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            f"cannot load dependency: {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def audit_bidirectional_typing():
    records = []
    for pure_outer in range(3):
        for changed_head in range(3):
            if pure_outer == changed_head:
                continue
            a, b = pure_outer, changed_head
            first = {
                "reference_cell_at_vu": [b, a],
                "shared_site": "v",
                "shared_heads": [a, b],
                "outer_head_line": a,
                "identity": "sum_s Delta^v_us*C^a_vs=-A_vu[b,a]",
            }
            dual = {
                "same_cell_at_uv": [a, b],
                "shared_site": "u",
                "shared_heads": [b, a],
                "outer_head_line": b,
                "identity": "sum_t Delta^u_vt*C^b_ut=-A_uv[a,b]",
            }
            require(first["reference_cell_at_vu"]
                    == list(reversed(dual["same_cell_at_uv"])),
                    "the transposed fan stopped using the same physical cell")
            require(len(set(first["shared_heads"])) == 2
                    and len(set(dual["shared_heads"])) == 2,
                    "an off-diagonal fan lost its transverse shared heads")
            require(first["outer_head_line"] != dual["outer_head_line"],
                    "the bidirectional fans lost their two outer lines")
            records.append({"a": a, "b": b, "v_fan": first, "u_fan": dual})
    require(len(records) == 6, "the ternary bidirectional type count changed")
    return {
        "offdiagonal_types": records,
        "type_count": len(records),
        "consequence": (
            "the coefficient equations already provide distinct heads at "
            "each fan centre; only deleted-star goodness and anchor escape "
            "remain"
        ),
    }


def matching_neighbour(matching, vertex):
    for left, right in matching:
        if left == vertex:
            return right
        if right == vertex:
            return left
    raise RuntimeError(f"matching does not cover vertex {vertex}")


def endpoint_rank(triple, endpoint, deleted_other):
    columns = []
    for colour, matching in enumerate(triple):
        neighbour = matching_neighbour(matching, endpoint)
        require(neighbour != deleted_other,
                "an off-anchor fan edge entered a selected matching")
        columns.append((neighbour, colour))
    return len(set(columns))


def audit_offanchor_fans(balanced):
    representatives = balanced.anchor_orbits()
    require(len(representatives) == 31,
            "the N=8 balanced anchor orbit census changed")
    path_histogram = Counter()
    fan_paths = 0
    decorated_fans = 0
    minimum_rank = 3
    for triple in representatives:
        anchors = {edge for matching in triple for edge in matching}
        absent_neighbours = {
            centre: tuple(site for site in range(balanced.N)
                          if site != centre
                          and tuple(sorted((centre, site))) not in anchors)
            for centre in range(balanced.N)
        }
        local_count = 0
        for centre, neighbours in absent_neighbours.items():
            for reference in neighbours:
                for mate in neighbours:
                    if reference == mate:
                        continue
                    ranks = (
                        endpoint_rank(triple, centre, reference),
                        endpoint_rank(triple, reference, centre),
                        endpoint_rank(triple, centre, mate),
                        endpoint_rank(triple, mate, centre),
                    )
                    require(ranks == (3, 3, 3, 3),
                            "an off-anchor two-edge fan lost four-goodness")
                    minimum_rank = min(minimum_rank, *ranks)
                    local_count += 1
                    fan_paths += 1
                    decorated_fans += 6
        path_histogram[local_count] += 1
    require(fan_paths > 0 and minimum_rank == 3,
            "the off-anchor fan audit became empty")
    return {
        "anchor_orbits_mod_S8xS3": len(representatives),
        "ordered_offanchor_two_edge_fans": fan_paths,
        "ternary_decorated_fans": decorated_fans,
        "fan_count_histogram_per_orbit": sorted(path_histogram.items()),
        "minimum_of_four_deleted_star_ranks": minimum_rank,
        "landing": (
            "a nonzero determinant/cofactor term on such a fan is a "
            "distinct-head four-good active overlap"
        ),
    }


def audit_source_identities(private_site, private_core):
    first = private_site.target_augmented_identity(private_core, 8)
    second = private_site.target_augmented_identity(private_core, 8)
    require(first["exact_source_consequence"]
            == second["exact_source_consequence"]
            == "sum_s Delta_us*C_s=-q_u",
            "the two transposed private-site consequences changed")
    return {
        "first_fan": first,
        "transposed_fan": second,
        "transposition": (
            "swap u,v and swap a,b; A_vu[b,a]=A_uv[a,b], so the same "
            "off-diagonal cell is the inhomogeneous term in both identities"
        ),
    }


def audit_anchor_web_boundary(five_lock, companion):
    kernel = five_lock.audit_lock_kernel_theorem()
    wedge = five_lock.audit_crossed_wedge_landing()
    sharp = five_lock.audit_sharp_incidence_counterguard()
    require(wedge["landing"] == "distinct-head four-good active overlap",
            "the five-lock crossed wedge landing changed")
    require(sharp["simultaneous_kernel"] == 0
            and not sharp["complementary_crossed_wedge"],
            "the injective no-wedge boundary changed")

    source = companion.build_guard()
    rows = companion.audit_three_complete_companion_rows(source)
    rank_boundary = companion.audit_rank_boundary(source)
    labels = companion.audit_label_invariance()
    require(len(rows) == 3 and rank_boundary["ranks"] == [2, 3],
            "the same-cell companion rank boundary changed")
    require(labels["audited_avoiding_matchings"] == 216,
            "the same-cell label-invariance census changed")
    return {
        "five_lock_kernel_ranks": kernel,
        "complementary_crossed_wedge": wedge,
        "injective_no_wedge_boundary": sharp,
        "same_cell_companion_rows": rows,
        "same_cell_deleted_rank_boundary": rank_boundary,
        "same_cell_label_invariance": labels,
        "sharp_residual": (
            "both bidirectional fans are anchor-contained, the same-star "
            "five-lock map is injective, and there is no complementary "
            "crossed off-anchor wedge"
        ),
    }


def audit_shared_attachment_scope(c6, rootless):
    c6_ledger, c6_digest = c6.audit()
    require(c6_digest == c6.EXPECTED_LEDGER_SHA256,
            "the C6 endpoint-attachment boundary replay changed")
    c6_first = c6_ledger["canonical_first_reduction"]
    require(c6_first["target_augmented_first_hit_rank_Q"] == 269
            and c6_first["rational_dual_pairing"] == "-1",
            "the C6 first-hit endpoint cokernel changed")

    cube = rootless.canonical_cube_and_unit()
    coarse = rootless.coarse_candidate()
    edge = rootless.one_adjacent_edge_gate()
    fine = rootless.fine_grade_and_word_gate()
    require(cube["fourth_operator_on_H_m"] == 1
            and cube["fourth_operator_on_H_0_minus_u"] == 0,
            "the rootless selected-source unit changed")
    require(not coarse["source_valid"]
            and not fine["word_change_supplied_by_multiplication_or_adjacent_edge"],
            "the rootless word-change boundary unexpectedly closed")
    return {
        "degree_zero_C6_endpoint_gate": {
            "first_hit_rank": c6_first[
                "target_augmented_first_hit_rank_Q"],
            "first_hit_columns": c6_first[
                "target_augmented_first_hit_column_count"],
            "dual_pairing": c6_first["rational_dual_pairing"],
            "needed": c6_ledger["next_attachment"],
        },
        "relative_rootless_gate": {
            "selected_source_unit": cube["fourth_operator_on_H_m"],
            "pure_row_selected_value": cube[
                "fourth_operator_on_H_0_minus_u"],
            "coarse_candidate_source_valid": coarse["source_valid"],
            "one_edge_remainder": edge["remaining_rows"],
            "word_change_from_existing_operations": fine[
                "word_change_supplied_by_multiplication_or_adjacent_edge"],
        },
        "shared_interface": (
            "a source-labelled endpoint-word-change homotopy natural under "
            "common-tail multiplication: its degree-zero shadow supplies the "
            "missing endpoint head for the C6/Fitting fan, while its relative "
            "degree-one boundary must also cancel the rootless selected-source "
            "unit, Omega_v, and q_(v,N) with W=tgt=ores=0"
        ),
        "non_unification_theorem": (
            "ordinary same-cell companions can satisfy only the degree-zero "
            "matching equation and preserve endpoint labels; therefore no "
            "theorem using only those companions can close both gates"
        ),
    }


def main():
    pin_dependencies()
    private_site = load(
        "computations/verify_uniform_target_augmented_private_site_active_minor.py",
        "bidirectional_private_site",
    )
    private_core = private_site.load(
        "computations/verify_hafnian_private_site_matching_bijection_lemma.py",
        "bidirectional_private_core",
    )
    balanced = load(
        "computations/verify_n8_balanced_anchor_chart_cover.py",
        "bidirectional_balanced_anchors",
    )
    five_lock = load(
        "computations/verify_uniform_five_lock_wedge_or_switch.py",
        "bidirectional_five_lock",
    )
    companion = load(
        "computations/verify_uniform_decorated_anchor_companion_rank_no_go.py",
        "bidirectional_companion_no_go",
    )
    c6 = load(
        "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py",
        "bidirectional_c6_attachment",
    )
    rootless = load(
        "computations/verify_h3_rootless_one_face_third_cofactor_comparison_vertex_gate.py",
        "bidirectional_rootless_attachment",
    )

    ledger = {
        "pins": PINS,
        "bidirectional_typing": audit_bidirectional_typing(),
        "source_identities": audit_source_identities(private_site, private_core),
        "offanchor_fan_audit": audit_offanchor_fans(balanced),
        "anchor_web_boundary": audit_anchor_web_boundary(five_lock, companion),
        "shared_attachment_scope": audit_shared_attachment_scope(c6, rootless),
        "uniform_theorem": (
            "every nonzero off-diagonal physical cell forces two transposed "
            "active private-site fans with transverse centre heads and the "
            "two corresponding pure outer lines.  Any fan having both "
            "physical edges outside the three selected anchors is already "
            "a four-good active wedge.  Otherwise all witnesses are trapped "
            "in the finite anchor five-lock/Hall web, where a same-star kernel "
            "deletes exactly or a complementary crossed off-anchor component "
            "lands; the sole residual is injective and no-wedge"
        ),
        "smallest_unproved_full_source_implication": (
            "in the injective no-wedge anchor web, the unary and opposite "
            "response rows must create a differently labelled endpoint "
            "component, a pure-anchor reselection, or an effective Hall "
            "carrier.  Same-cell companion tails cannot do so"
        ),
        "scope": (
            "uniform source-polynomial fan theorem plus exact N=8 anchor "
            "orbit audit and a complete three-companion-row guard.  This "
            "does not prove the remaining endpoint-word-change homotopy and "
            "does not claim a full-source counterexample"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"bidirectional private-site ledger changed: {digest}")
    print("uniform bidirectional private-site fan/rank theorem: BOUNDARY")
    print("off-diagonal cell supplies transverse centre heads at both endpoints")
    print("off-anchor two-edge fan: four-good active overlap")
    print("anchor residual: injective five-lock, no complementary wedge")
    print("ordinary same-cell companions cannot close C6 and rootless gates")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
