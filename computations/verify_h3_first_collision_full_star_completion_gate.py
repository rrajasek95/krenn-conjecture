#!/usr/bin/env python3
"""Classify and complete the first-collision 66-term cap complement.

The direct-free 90-term row partitions by its unique site-0 edge into seven
sectors S_i.  The first collision lands S_1+S_7 and leaves the five sectors
S_2+...+S_6, of total size 66.

For every i<j, the literal collision

    C_ij = x_0j iota_0i(e) - x_0i iota_0j(e)

has two signed branches.  Private deletion/reinsertion uses the same sign a
second time and hence lands signlessly on S_i+S_j.  The 21 outputs have rank
seven and their uniform average (1/6) sum_{i<j}(S_i+S_j) is the complete
90-term row.  The 66 complement itself has a minimal four-column expression

    (S_3+S_6) + 1/2[(S_2+S_4)+(S_2+S_5)+(S_4+S_5)].

This closes the coefficient debt conditional on one natural full-star
response-to-cap operation.  It does not construct that operation: unary
Euler and relative Taylor/collision cells remain response-internal, while
the cap receiving section is in AugP2/K_Eq.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_order6_first_forbidden_face_exact_seed_cycle_gate.py":
        "0c3367ab48327bfbe308dc81191019d094eec054a04c3d1f2bd38f0e69faa2e9",
    "computations/verify_h3_primitive_c4_covariance_pointed_bridge_gate.py":
        "a14339fee59134b28229fb17fcae2292bc544264ea829db60c953875f96fef41",
    "computations/verify_h3_phi_ks_r0_word_operation_reachability_no_go.py":
        "3b2cf3aa1cd6ee46f60c0e3621342f4eb15420d6d5d302546b2403d966703ba8",
    "computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py":
        "2ac01c9ba571338b4c7b779dbc70d5d0eaacb2fe01a4035833970fa6b9826fe0",
    "computations/verify_h3_termwise_private_full_nine_augp2_linear_landing_gate.py":
        "9c182f13ba4da4f2dd3ff49fd9ebf60dd1a218f53cbf4416e82a63236f57404f",
    "computations/verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py":
        "8be3bc5bf85f8d633e77e2a0bdd18aea6d481c81f5fb6a6a947cbaf82f862302",
}
EXPECTED_LEDGER_SHA256 = "8e4f2fb184acd9c346619de7d077bf3dd3e4945d83dbc332da7ef37cf5297c28"

SITES = tuple(range(8))
STAR_PARTNERS = tuple(range(1, 8))
OLD = frozenset((1, 7))
REMOTE_TAIL = frozenset((2, 4, 5))
DIRECT_ROOT = frozenset((3, 6))
ROOT_LABELS = ("AB", "AC")
PURE_WORD = (1,) * 8
SECOND_SEED_WORD = (1, 1, 2, 1, 1, 2, 1, 1)


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


def sparse_rank(vectors) -> int:
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
                residual = vector.get(key, Q(0)) - coefficient * value
                if residual:
                    vector[key] = residual
                else:
                    vector.pop(key, None)
    return len(basis)


def in_span(target, vectors) -> bool:
    return sparse_rank(vectors) == sparse_rank(tuple(vectors) + (target,))


def add_vectors(weighted_vectors):
    answer = Counter()
    for weight, vector in weighted_vectors:
        for key, value in vector.items():
            answer[key] += Q(weight) * Q(value)
    return {key: value for key, value in answer.items() if value}


def star_cell(partner: int, word):
    return 0, partner, word[0], word[partner]


def remove_one(monomial, cell):
    terms = list(monomial)
    require(cell in terms, ("missing selected star cell", cell, monomial))
    terms.remove(cell)
    return tuple(sorted(terms))


def site_multiplicities(monomial):
    counts = Counter(site for cell in monomial for site in cell[:2])
    return tuple(counts.get(site, 0) for site in SITES)


def word_degree(word):
    degree = [0] * 24
    for site, colour in enumerate(word):
        degree[3 * site + colour] += 1
    return tuple(degree)


def shifted_branch_degree(word, missing: int, doubled: int):
    degree = list(word_degree(word))
    degree[3 * missing + word[missing]] -= 1
    degree[3 * doubled + word[doubled]] += 1
    return tuple(degree)


def matching_vector(monomials, tag="cap"):
    return {(tag, monomial): Q(1) for monomial in monomials}


def star_partition(base, word):
    row = tuple(base.full_row(word))
    sectors = {}
    for partner in STAR_PARTNERS:
        cell = star_cell(partner, word)
        sectors[partner] = tuple(
            monomial for monomial in row if cell in monomial)
    union = set().union(*(set(sector) for sector in sectors.values()))
    require(len(row) == len(set(row)) == 90
            and union == set(row)
            and sum(map(len, sectors.values())) == len(row),
            "site-0 sectors stopped partitioning the direct-free row")
    require([len(sectors[index]) for index in STAR_PARTNERS]
            == [12, 12, 15, 12, 12, 15, 12],
            [len(sectors[index]) for index in STAR_PARTNERS])
    return row, sectors


def classify_residual_symmetry(base):
    row, sectors = star_partition(base, PURE_WORD)
    first = set(sectors[1]) | set(sectors[7])
    complement = set(row) - first
    require(len(first) == 24 and len(complement) == 66,
            (len(first), len(complement)))

    group = []
    for old_image in ((1, 7), (7, 1)):
        for root_image in ((3, 6), (6, 3)):
            for tail_image in permutations(sorted(REMOTE_TAIL)):
                group.append({
                    0: 0,
                    1: old_image[0], 7: old_image[1],
                    3: root_image[0], 6: root_image[1],
                    **dict(zip(sorted(REMOTE_TAIL), tail_image, strict=True)),
                })
    require(len(group) == 24, len(group))

    def transport(monomial, permutation):
        cells = []
        for left, right, a, b in monomial:
            left = permutation[left]
            right = permutation[right]
            cells.append((left, right, a, b) if left < right
                         else (right, left, b, a))
        return tuple(sorted(cells))

    def kind(site):
        if site in OLD:
            return "O"
        if site in DIRECT_ROOT:
            return "R"
        require(site in REMOTE_TAIL, site)
        return "T"

    unseen = set(complement)
    orbits = []
    while unseen:
        representative = min(unseen)
        orbit = {transport(representative, permutation)
                 for permutation in group}
        require(orbit <= complement, (representative, orbit - complement))
        unseen -= orbit
        star = next(cell for cell in representative if 0 in cell[:2])
        partner = star[1] if star[0] == 0 else star[0]
        residual_edges = []
        for left, right, _a, _b in representative:
            if 0 in (left, right):
                continue
            residual_edges.append("".join(sorted((kind(left), kind(right)))))
        orbits.append({
            "size": len(orbit),
            "star_partner_type": kind(partner),
            "remaining_edge_types": "+".join(sorted(residual_edges)),
            "representative": repr(representative),
        })
    orbits.sort(key=lambda record: record["representative"])
    require([(record["size"], record["star_partner_type"],
              record["remaining_edge_types"]) for record in orbits] == [
        (6, "T", "OR+OR+TT"),
        (24, "T", "OR+OT+RT"),
        (6, "T", "OO+RT+RT"),
        (12, "R", "OR+OT+TT"),
        (12, "R", "OT+OT+RT"),
        (6, "R", "OO+RT+TT"),
    ], orbits)
    return {
        "residual_symmetry_group":
            "S_{1,7} x S_{3,6} x S_{2,4,5}",
        "group_order": len(group),
        "coarse_star_partner_orbits": [
            {"partners": sorted(REMOTE_TAIL), "terms": 36},
            {"partners": sorted(DIRECT_ROOT), "terms": 30},
        ],
        "literal_matching_orbits": orbits,
        "literal_orbit_sizes": [record["size"] for record in orbits],
        "first_pair_terms": len(first),
        "complement_terms": len(complement),
    }


def pair_collision(base, word, sectors, left_partner, right_partner):
    left_cell = star_cell(left_partner, word)
    right_cell = star_cell(right_partner, word)
    boundary = Counter()
    landed = Counter()
    records = []
    for branch, selected_partner, inserted_partner, sign in (
        (f"{left_partner}|{right_partner}", left_partner, right_partner, 1),
        (f"{right_partner}|{left_partner}", right_partner, left_partner, -1),
    ):
        selected = star_cell(selected_partner, word)
        inserted = star_cell(inserted_partner, word)
        for cap_monomial in sectors[selected_partner]:
            remainder = remove_one(cap_monomial, selected)
            source_monomial = tuple(sorted((inserted,) + remainder))
            multiplicities = site_multiplicities(source_monomial)
            missing = tuple(site for site, value in enumerate(multiplicities)
                            if value == 0)
            doubled = tuple(site for site, value in enumerate(multiplicities)
                            if value == 2)
            require(missing == (selected_partner,)
                    and doubled == (inserted_partner,)
                    and base.fine_degree_of_edge_monomial(source_monomial)
                        == shifted_branch_degree(
                            word, selected_partner, inserted_partner),
                    (branch, missing, doubled, source_monomial))
            boundary[source_monomial] += Q(sign)
            # Deleting the inserted star edge and reinserting the selected
            # one reconstructs the parent cap matching.  Map sign equals the
            # boundary sign, so the cap coefficient is positive.
            reconstructed = tuple(sorted((selected,) + remove_one(
                source_monomial, inserted)))
            require(reconstructed == cap_monomial,
                    (branch, reconstructed, cap_monomial))
            landed[reconstructed] += Q(sign * sign)
            records.append((branch, repr(source_monomial), sign,
                            missing[0], doubled[0]))
    boundary = {key: value for key, value in boundary.items() if value}
    landed = {key: value for key, value in landed.items() if value}
    expected_support = set(sectors[left_partner]) | set(sectors[right_partner])
    require(len(boundary) == len(expected_support)
            and set(boundary.values()) == {Q(-1), Q(1)}
            and landed == {monomial: Q(1) for monomial in expected_support},
            (left_partner, right_partner, len(boundary), len(landed)))
    return {
        "pair": (left_partner, right_partner),
        "left_cell": repr(left_cell),
        "right_cell": repr(right_cell),
        "boundary": boundary,
        "landing": landed,
        "records": records,
    }


def full_star_collision_audit(base):
    row, sectors = star_partition(base, PURE_WORD)
    collisions = {
        pair: pair_collision(base, PURE_WORD, sectors, *pair)
        for pair in combinations(STAR_PARTNERS, 2)
    }
    outputs = tuple(record["landing"] for record in collisions.values())
    require(len(collisions) == 21 and sparse_rank(outputs) == 7,
            (len(collisions), sparse_rank(outputs)))
    uniform = add_vectors((Q(1, 6), vector) for vector in outputs)
    complete = {monomial: Q(1) for monomial in row}
    require(uniform == complete, "full-star pair average stopped being Euler")
    multiplicity = Counter()
    for vector in outputs:
        multiplicity.update(vector)
    require(set(multiplicity.values()) == {Q(6)}
            and len(multiplicity) == 90,
            (len(multiplicity), set(multiplicity.values())))

    first = collisions[(1, 7)]["landing"]
    residual = {
        monomial: Q(1) for partner in sorted(REMOTE_TAIL | DIRECT_ROOT)
        for monomial in sectors[partner]
    }
    natural_pairs = ((3, 6), (2, 4), (2, 5), (4, 5))
    natural_columns = tuple(collisions[pair]["landing"]
                            for pair in natural_pairs)
    natural_weights = (Q(1), Q(1, 2), Q(1, 2), Q(1, 2))
    require(sparse_rank(natural_columns) == 4
            and add_vectors(zip(natural_weights, natural_columns,
                                strict=True)) == residual,
            "root-pair plus tail-triangle residual formula changed")
    pair_items = tuple(collisions.items())
    for size in range(1, 4):
        require(not any(in_span(
            residual, tuple(pair_items[index][1]["landing"]
                            for index in indices))
            for indices in combinations(range(len(pair_items)), size)),
            ("66-term residual acquired a smaller pair expression", size))

    # The complete K8 row has 15 terms in every site-0 sector.  Removing the
    # 36 edge removes three terms in sectors not incident to 3 or 6 and no
    # whole sector.
    complete_unrestricted = tuple(base.matching_monomial(
        matching, dict(enumerate(PURE_WORD)))
        for matching in base.matchings(SITES))
    unrestricted_counts = [sum(star_cell(partner, PURE_WORD) in monomial
                               for monomial in complete_unrestricted)
                           for partner in STAR_PARTNERS]
    direct_free_counts = [len(sectors[partner])
                          for partner in STAR_PARTNERS]
    deleted_counts = [left - right for left, right in
                      zip(unrestricted_counts, direct_free_counts, strict=True)]
    require(unrestricted_counts == [15] * 7
            and deleted_counts == [3, 3, 0, 3, 3, 0, 3]
            and all(direct_free_counts),
            (unrestricted_counts, direct_free_counts, deleted_counts))

    root_outputs = tuple({(root, monomial): value
                          for monomial, value in output.items()}
                         for root in ROOT_LABELS for output in outputs)
    require(sparse_rank(root_outputs) == 14,
            sparse_rank(root_outputs))
    return {
        "site0_sector_sizes_direct_free": direct_free_counts,
        "site0_sector_sizes_before_direct_free": unrestricted_counts,
        "terms_deleted_by_36_restriction_per_sector": deleted_counts,
        "entire_site0_sectors_deleted": 0,
        "pair_collisions": len(collisions),
        "literal_signed_branch_faces_per_root": sum(
            len(record["records"]) for record in collisions.values()),
        "pair_output_rank_per_root": sparse_rank(outputs),
        "pair_output_rank_two_root_direct_sum": sparse_rank(root_outputs),
        "each_cap_term_pair_multiplicity": 6,
        "uniform_full_star_formula":
            "(1/6) sum_{1<=i<j<=7} Phi(d C_ij)=H_direct-free",
        "first_pair_support": len(first),
        "residual_support": len(residual),
        "minimum_pair_columns_for_residual": 4,
        "minimal_residual_symmetry_family": [list(pair)
                                              for pair in natural_pairs],
        "minimal_residual_weights": [str(weight)
                                      for weight in natural_weights],
        "minimal_residual_family_rank": sparse_rank(natural_columns),
        "coefficient_debt_after_natural_full_star_action": 0,
    }


def euler_and_triangle_audit(base):
    row, sectors = star_partition(base, PURE_WORD)
    sector_vectors = {
        partner: {monomial: Q(1) for monomial in sector}
        for partner, sector in sectors.items()
    }
    complete = {monomial: Q(1) for monomial in row}
    require(add_vectors((Q(1), vector)
                        for vector in sector_vectors.values()) == complete,
            "site-0 Euler partition changed")

    # Test the universal raw collision triangle at the symbolic coefficient
    # level.  D_ij=x_j*d_i-x_i*d_j, and
    # x_k D_ij-x_j D_ik+x_i D_jk=0 term by term.
    for i, j, k in combinations(STAR_PARTNERS, 3):
        symbolic = Counter()
        for outer, pair, sign in (
            (k, (i, j), 1),
            (j, (i, k), -1),
            (i, (j, k), 1),
        ):
            left, right = pair
            symbolic[(tuple(sorted((outer, right))), left)] += Q(sign)
            symbolic[(tuple(sorted((outer, left))), right)] -= Q(sign)
        require(not {key: value for key, value in symbolic.items() if value},
                (i, j, k, symbolic))

    euler_with_homogenizer = Counter({("matching", repr(monomial)): Q(1)
                                      for monomial in row})
    euler_with_homogenizer[("homogenizer", "u")] = Q(-1)
    relation = Counter({("matching", repr(monomial)): Q(1)
                        for monomial in row})
    relation[("homogenizer", "u")] = Q(-1)
    require(euler_with_homogenizer == relation,
            "homogenized vertex Euler boundary changed")
    return {
        "vertex_Euler_identity":
            "sum_i x_0i partial_0i H = H",
        "homogenized_Tate_generator":
            "G0=sum_i x_0i iota_0i(e)+(u iota_u(e))",
        "homogenized_boundary": "dG0=H-u",
        "raw_collision_triangle_identity":
            "x_0k dC_ij-x_0j dC_ik+x_0i dC_jk=0",
        "triangles_checked": len(tuple(combinations(STAR_PARTNERS, 3))),
        "source_boundary_telescope": True,
        "Euler_coefficient_projection_equals_full_star_average": True,
        "operation_parent": "EqSystem/response -> response",
        "cap_K_Eq_projection_constructed": False,
    }


def second_seed_and_complete_response_guard(base):
    pure_row, pure_sectors = star_partition(base, PURE_WORD)
    mixed_row, mixed_sectors = star_partition(base, SECOND_SEED_WORD)
    pure_residual = set(pure_row) - set(pure_sectors[1]) - set(pure_sectors[7])
    mixed_collision = pair_collision(
        base, SECOND_SEED_WORD, mixed_sectors, 1, 7)
    mixed_landing = set(mixed_collision["landing"])
    require(len(pure_residual) == 66 and len(mixed_landing) == 24
            and not pure_residual & mixed_landing
            and set(pure_row).isdisjoint(mixed_row),
            (len(pure_residual), len(mixed_landing),
             len(pure_residual & mixed_landing)))

    first = matching_vector(pure_sectors[1] + pure_sectors[7])
    residual = matching_vector(pure_residual)
    complete_untyped = matching_vector(pure_row)
    require(add_vectors(((Q(1), complete_untyped),
                         (Q(-1), first))) == residual,
            "ordinary full row stopped filling the untyped complement")

    tagged_first = matching_vector(
        pure_sectors[1] + pure_sectors[7], "cap/AugP2_K_Eq")
    tagged_residual = matching_vector(pure_residual, "cap/AugP2_K_Eq")
    tagged_complete = matching_vector(
        pure_row, "response/EqSystem_complete")
    require(sparse_rank((tagged_first, tagged_complete)) == 2
            and sparse_rank((tagged_first, tagged_complete,
                             tagged_residual)) == 3,
            "operation tagging stopped separating the complete response")
    return {
        "second_exact_seed_cycle_word": "11211211",
        "first_complement_word": "11111111",
        "second_seed_first_pair_landing_terms": len(mixed_landing),
        "literal_word_fine_intersection_with_pure_complement": 0,
        "second_seed_operation_parent": "response -> response",
        "second_seed_cap_r0_projection": 0,
        "ordinary_complete_response_untyped_formula":
            "residual_66=H_pure-(S_1+S_7)",
        "untyped_rank_first_then_complete": [1, 2],
        "typed_rank_first_complete_then_cap_residual": [1, 2, 3],
        "ordinary_complete_response_fills_cap_K_Eq_residual": False,
        "reason": (
            "the second seed is a different literal word/fine summand and "
            "the ordinary complete row retains the response operation idempotent"
        ),
    }


def first_pair_taylor_lcm_audit(base):
    row, sectors = star_partition(base, PURE_WORD)
    left_cell = star_cell(1, PURE_WORD)
    right_cell = star_cell(7, PURE_WORD)
    left_parents = tuple(frozenset(monomial) for monomial in sectors[1])
    right_parents = tuple(frozenset(monomial) for monomial in sectors[7])
    lcms = tuple(left | right for left in left_parents
                 for right in right_parents)
    degree_histogram = Counter(map(len, lcms))
    common_histogram = Counter(
        len(left & right) for left in left_parents for right in right_parents)
    collision = pair_collision(base, PURE_WORD, sectors, 1, 7)
    branch_monomials = {frozenset(monomial)
                        for monomial in collision["boundary"]}
    require(len(left_parents) == len(right_parents) == 12
            and len(lcms) == 144
            and degree_histogram == {6: 12, 7: 42, 8: 90}
            and common_histogram == {2: 12, 1: 42, 0: 90}
            and len(set(lcms)) == 135
            and len(branch_monomials) == 24
            and set(map(len, branch_monomials)) == {4}
            and not branch_monomials & set(lcms),
            (len(left_parents), len(right_parents), degree_histogram,
             common_histogram, len(set(lcms)), len(branch_monomials),
             len(branch_monomials & set(lcms))))

    # Ordinary matching lcms are squarefree sets of decorated cells.  A
    # diagonal pair (a,a) has multiplicity one, so its ordinary second Hasse
    # face is zero and requires a divided-power enlargement.
    require(all(len(parent) == 4 and len(set(parent)) == 4
                and int(left_cell in parent) <= 1
                for parent in left_parents),
            "a matching parent stopped being squarefree")
    return {
        "first_pair_parent_occurrences_each_side": [
            len(left_parents), len(right_parents)],
        "cross_parent_pairs": len(lcms),
        "distinct_squarefree_lcms": len(set(lcms)),
        "lcm_cell_degree_histogram": {
            str(key): value for key, value in sorted(degree_histogram.items())
        },
        "parent_common_cell_histogram": {
            str(key): value for key, value in sorted(common_histogram.items())
        },
        "collision_branch_monomials": len(branch_monomials),
        "collision_branch_cell_degree": 4,
        "collision_branch_intersection_with_literal_matching_lcms": 0,
        "offdiagonal_pair_label_is_visible_in_Taylor_lcm":
            all(left_cell in lcm and right_cell in lcm for lcm in lcms),
        "four_mates_are_literal_boundary_of_one_Taylor_lcm_cell": False,
        "first_additional_relative_face": (
            "a labelled Taylor-to-Spencer deletion/contraction lowering the "
            "6/7/8-cell lcm packet to the 4-cell missing/doubled branches"
        ),
        "diagonal_guard": (
            "ordinary squarefree lcm has decorated-cell multiplicity one, "
            "so diagonal (a,a) rows require divided-power gamma_2(iota_a)"
        ),
    }


def mate_and_taylor_operation_gate(bridge, reachability, fixed_window,
                                   landing, sections):
    bridge_ledger, bridge_digest = bridge.audit()
    require(bridge_digest == bridge.EXPECTED_LEDGER_SHA256, bridge_digest)
    chart = bridge_ledger["literal_chart_covariance"]
    require(chart["mate_incidence_rank"] == 3
            and chart["all_four_K22_mates_from_one_natural_schema"], chart)

    reach_ledger, reach_digest = reachability.audit()
    require(reach_digest == reachability.EXPECTED_LEDGER_SHA256,
            reach_digest)
    operation = reach_ledger["fixed_window_operation_gate"]
    require(operation["cross_profile_edges_present_in_internal_constructor"]
            == 0, operation)

    columns, _detector, candidate_h, candidate_r, packet = (
        fixed_window.audit_cartesian_physical_packet())
    switch = fixed_window.audit_operation_switch_boundary(
        columns, candidate_h, candidate_r)
    require(packet["internal_rank"] == 46
            and switch["operation_profile_changing_edges"] == 4
            and switch["rank_base_one_switch_candidate"] == [46, 47, 48],
            (packet, switch))

    landing_ledger, landing_digest = landing.audit()
    require(landing_digest == landing.EXPECTED_LEDGER_SHA256,
            landing_digest)
    literal = landing_ledger["literal_two_word_residual"]
    private = landing_ledger["private_insertion_restriction"]
    linear = landing_ledger["most_general_two_root_linear_augmentation"]
    physical = landing_ledger["physical_obstruction_after_linear_solution"]
    require(literal == {
                "literal_full_nine_monomials": 180,
                "pair_shadow_rank": 159,
                "raw_pair_shadow_fibre": 21,
                "all_committed_readout_rank": 14,
                "residual_dimension": 7,
            }
            and private["rank_on_residual"] == 7
            and linear["unique_tied_solution_exists_in_linear_enriched_category"]
            and physical["first_typed_obstruction"]
                ["current_operation_algebra_value"] == "e_C A e_R=0",
            (literal, private, linear, physical))

    sections_ledger, sections_digest = sections.audit()
    require(sections_digest == sections.EXPECTED_LEDGER_SHA256,
            sections_digest)
    operation_algebra = sections_ledger["root_Weyl_cap_operation_algebra"]
    two_roots = sections_ledger["literal_two_root_sections"]
    require(operation_algebra["generated_Hom_response_cap"] == 0
            and two_roots["cokernel_dimension_before_sections"] == 2
            and two_roots["cokernel_dimension_after_both_labelled_sections"]
                == 0,
            (operation_algebra, two_roots))
    return {
        "relative_Taylor_boundary_coefficient_shadow": (
            "the offdiagonal pair label (x_0i,x_0j), not the literal "
            "four-cell missing/doubled collision branch"
        ),
        "first_pair_four_DQ_PS_mates":
            "two ordered branches times the two AB/AC receiving roots",
        "four_mate_incidence_rank": chart["mate_incidence_rank"],
        "implemented_operation_changing_mates": 0,
        "full_star_natural_schema_instances":
            "21 unordered pairs x 2 ordered branches x 2 roots = 84",
        "full_star_schema_restricts_to_original_four_mates": True,
        "Taylor_cell_operation_parent": "response -> response",
        "required_relative_cell_operation_parent":
            "response -> cap AugP2/K_Eq",
        "four_mates_are_current_Taylor_boundary": False,
        "word_covariance_to_cap_Hom_dimension":
            operation_algebra["generated_Hom_response_cap"],
        "root_labelled_Hom_quotient_dimension":
            two_roots["cokernel_dimension_before_sections"],
        "common_two_word_private_module": {
            "literal_matching_coordinates": literal[
                "literal_full_nine_monomials"],
            "pair_shadow_rank": literal["pair_shadow_rank"],
            "pair_shadow_fibre": literal["raw_pair_shadow_fibre"],
            "committed_readout_rank_on_fibre": literal[
                "all_committed_readout_rank"],
            "residual_dimension": literal["residual_dimension"],
            "private_rank_on_residual": private["rank_on_residual"],
        },
        "formal_comparison_after_one_natural_Hom":
            "unique, root-tied, residual zero, B=Eq",
        "first_factorization_failure": (
            "a literal Taylor-to-Spencer contraction is still required, and "
            "target-zero word/covariance and Taylor differentials remain in "
            "e_R A e_R; they do not create the required e_C A e_R map"
        ),
        "smallest_new_constructor": (
            "one root-natural full-star mixed divided-Hasse/Taylor-to-AugP2 "
            "module action; its 84 labelled instances include the old four mates"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "full_star_base",
    )
    bridge = load(
        "computations/verify_h3_primitive_c4_covariance_pointed_bridge_gate.py",
        "full_star_bridge",
    )
    reachability = load(
        "computations/verify_h3_phi_ks_r0_word_operation_reachability_no_go.py",
        "full_star_reachability",
    )
    fixed_window = load(
        "computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py",
        "full_star_fixed_window",
    )
    landing = load(
        "computations/verify_h3_termwise_private_full_nine_augp2_linear_landing_gate.py",
        "full_star_landing",
    )
    sections = load(
        "computations/verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py",
        "full_star_sections",
    )
    ledger = {
        "theorem": "h3 first-collision full-star completion gate",
        "pins": PINS,
        "residual_endpoint_root_tail_symmetry":
            classify_residual_symmetry(base),
        "literal_full_star_collision_completion":
            full_star_collision_audit(base),
        "vertex_Euler_and_source_telescope": euler_and_triangle_audit(base),
        "second_seed_and_ordinary_complete_response_guard":
            second_seed_and_complete_response_guard(base),
        "first_pair_Taylor_lcm_gate": first_pair_taylor_lcm_audit(base),
        "relative_Taylor_private_module_operation_gate":
            mate_and_taylor_operation_gate(
                bridge, reachability, fixed_window, landing, sections),
        "verdict": (
            "The 66-term complement has two coarse star-partner orbits and "
            "six literal matching orbits.  Coefficientwise it is generated "
            "by a minimal four-collision family: C_36 plus the three remote-"
            "tail pairs C_24,C_25,C_45 with weights 1,1/2,1/2,1/2.  More "
            "naturally, the 21-pair full-star family has rank seven and its "
            "uniform 1/6 average is the complete 90-term row, for each root.  "
            "The unary Euler generator and collision triangles construct the "
            "same aggregate internally on the response side.  The second "
            "seed word is fine-disjoint, and an ordinary complete-response "
            "row fills the complement only after operation tags are forgotten.  "
            "The first-pair Taylor label is visible, but its literal lcm "
            "packet has cell degree 6--8 while the collision branches have "
            "degree four, so a labelled Taylor-to-Spencer contraction is also "
            "part of the needed comparison.  The remaining debt is one natural "
            "full-star response-to-AugP2/K_Eq module action: Taylor/covariance "
            "cells remain response-internal, although the existing 7D private-module "
            "uniqueness theorem makes such a comparison unique if constructed"
        ),
        "scope": (
            "exact rational canonical h=3 direct-free 90-term row, all seven "
            "site-0 sectors, both AB/AC root labels, pure and second-seed words, "
            "literal fine/missing/doubled labels, response versus AugP2/K_Eq "
            "operation idempotents, and the pinned two-word private module"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("full-star completion ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=(
        "all", "symmetry", "star", "euler", "typed", "taylor"),
        default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        star = ledger["literal_full_star_collision_completion"]
        typed = ledger["relative_Taylor_private_module_operation_gate"]
        print(f"h3 first-collision full-star completion ({arguments.mode}): PASS")
        print("66 complement: TWO COARSE / SIX LITERAL ORBITS")
        print("minimal pair completion: RANK", star[
            "minimal_residual_family_rank"], "on 4 columns")
        print("21-pair average: exact 90-term Euler row; rank",
              star["pair_output_rank_per_root"])
        print("physical full-star Hom:",
              typed["word_covariance_to_cap_Hom_dimension"])
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
