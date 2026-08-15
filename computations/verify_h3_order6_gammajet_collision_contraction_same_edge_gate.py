#!/usr/bin/env python3
"""Test the 159-pair collision contraction as a literal GammaJet enrichment.

The proposed map sends a pair of coloured edge cells sharing one site to a
``P3+K2`` AugP2 occurrence, then uses the uniform 1/6 full-star average.  The
full-star core is exact on parent-labelled perfect matchings.  It is not a
map on the complete order-six pair target: 11 of the 159 site-repeating rows
reuse the same uncoloured edge and have no P3 spine.

On the constrained image ``S=D2 ker(D0,D1)``, the shared-one-site projection
has rank 142 while the same-edge projection has rank 11 at both pinned
primes.  Since the full rank is 153, an 11-dimensional family of genuine
D0/D1 cycles has only same-edge D2 boundary.  The first missing coordinate
is ``(07:11,07:11)``.  Thus the proposed contraction fails before defining a
response-to-cap operation component.

The minimal honest coefficient repair adjoins seven divided squares
``gamma_2(x_e)`` and four mixed same-edge products.  The order-six D2
constructor already uses unordered pairs, so its diagonal coefficients are
binomial coefficients and map integrally to the divided-square basis.  This
restores the complete rank-153 pair target, but those 11 targets have
parallel-edge topology, not P3+K2 topology, and have no physical AugP2 cap
landing.  The 1020 deleted-factor cylinders, homogenizer/Eq carrier and all
127 protected rows do not change that conclusion.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from math import comb
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_order6_site_repeating_target_enrichment_current_tree.py":
        "f1bc7a9f8fdb9148fde5c4d79a4b7f59a3bd03cd6ff00dc1c2fb3c0e7f511ea9",
    "computations/verify_h3_order6_seed_source_automorphism_orbit_gate.py":
        "d140995b0b35b84f052662595a0a68bcd2b47db826d8e559bb99a96b0eb9b61e",
    "computations/verify_h3_order6_first_forbidden_face_exact_seed_cycle_gate.py":
        "0c3367ab48327bfbe308dc81191019d094eec054a04c3d1f2bd38f0e69faa2e9",
    "computations/verify_h3_first_collision_full_star_completion_gate.py":
        "ea45302b71998ca6ba3928a29f1e75eebc0ba360d1c234f73bd70dfb9b29d317",
    "computations/verify_h3_full_star_minimal_protected_homogenizer_cylinder_gate.py":
        "ab7471a38683da113723ea9a073e3dc2a3c76d4576b9e575a0983ab1054c5d58",
    "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py":
        "bd3f008eb2faf00bbebccb09ef9692908f2e0ae4a795706de2c32f0b2ef342af",
    "computations/verify_h3_actual_source_primitive_terminal_reduction_gate.py":
        "5754c85f7ae4b714777cdbb0f941672ade1977c5568f332a0dc8e317e4952927",
    "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py":
        "6c42cd4dc7dca1544dc0b675f5f4543ec348f1fba34b7ea14bf80cc6a20b9cf1",
    "computations/verify_h3_declared_divided_weyl_trigger_gamma_terminal_gate.py":
        "acb8a4eedc7c708ce63618a82cb45359111daa1f2c8c71a33796fc02238c5a32",
    "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py":
        "674a7503db43b8ad53d6f4ea9d7fe095f0f26629d92e4b0dd291f14bde82fa3a",
    "computations/verify_h3_normalized_eq_base_change_tor_gate.py":
        "b7c409db8cff0141a153816d0d14525464c4fcadb0607b97da06181435059d50",
}
EXPECTED_FULL_LEDGER_SHA256 = (
    "bb7f0251d56d5da92d849e2c38ca20cfe39beda05412520957f8202346d641f3"
)
EXPECTED_STRUCTURAL_LEDGER_SHA256 = (
    "02589fe29848090379c035a5e3d5bccd086fd1e0628b92b5f0ca58ce9afa4fa0"
)

CAP_WORD = "01211222"
SOURCE_WORDS = ("11111111", "11211211")
FIRST_SAME_EDGE = (2, ((0, 7, 1, 1), (0, 7, 1, 1)))


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


def word_of_shift(shift) -> str:
    word = []
    for site in range(8):
        block = tuple(shift[3 * site:3 * site + 3])
        require(block.count(-1) == 1 and block.count(0) == 2,
                ("not a negative word shift", site, block))
        word.append(str(block.index(-1)))
    return "".join(word)


def pair_shape(row) -> str:
    require(row[0] == 2 and len(row[1]) == 2, row)
    left, right = row[1]
    left_sites = frozenset(left[:2])
    right_sites = frozenset(right[:2])
    if len(left_sites & right_sites) == 1:
        return "shared_one_site_P3"
    if left_sites == right_sites and left == right:
        return "diagonal_same_edge_gamma2"
    if left_sites == right_sites:
        return "colour_distinct_same_edge_product"
    raise RuntimeError(("unexpected nonphysical pair shape", row))


def build_current_tree():
    site = load(
        "computations/verify_h3_order6_site_repeating_target_enrichment_current_tree.py",
        "gammajet_site",
    )
    orbit = load(
        "computations/verify_h3_order6_seed_source_automorphism_orbit_gate.py",
        "gammajet_orbit",
    )
    seed = load(
        "computations/verify_h3_order6_first_forbidden_face_exact_seed_cycle_gate.py",
        "gammajet_seed",
    )
    loaded = site.modules()
    loaded["site"] = site
    columns, shifts = site.build_operator_columns(loaded)
    metadata = seed.ordered_metadata(loaded, columns, shifts)
    require(len(columns) == len(shifts) == len(metadata) == 8580,
            "the order-six block changed")
    return site, orbit, loaded, columns, shifts, metadata


def literal_pair_inventory(site, loaded, columns, shifts) -> tuple[dict, dict]:
    pair_shifts = defaultdict(set)
    pair_columns = Counter()
    for column, shift in zip(columns, shifts, strict=True):
        for row, value in column.items():
            if (row[0] == 2 and value
                    and not site.physical_pair(
                        row[1], loaded["base"].DIRECT_FREE_PAIR)):
                pair_shifts[row].add(shift)
                pair_columns[row] += 1
    rows = set(pair_shifts)
    by_shape = defaultdict(set)
    for row in rows:
        by_shape[pair_shape(row)].add(row)
    shared = by_shape["shared_one_site_P3"]
    diagonal = by_shape["diagonal_same_edge_gamma2"]
    mixed = by_shape["colour_distinct_same_edge_product"]
    same_edge = diagonal | mixed
    require((len(rows), len(shared), len(diagonal), len(mixed), len(same_edge))
            == (159, 148, 7, 4, 11),
            {key: len(value) for key, value in by_shape.items()})
    require(FIRST_SAME_EDGE == min(same_edge, key=repr),
            (FIRST_SAME_EDGE, min(same_edge, key=repr)))

    occurrence_histogram = Counter(
        word_of_shift(shift)
        for row_shifts in pair_shifts.values() for shift in row_shifts
    )
    same_edge_occurrences = sum(len(pair_shifts[row]) for row in same_edge)
    require(sum(map(len, pair_shifts.values())) == 271
            and occurrence_histogram == {
                "11111111": 159, "11211211": 112,
            }
            and same_edge_occurrences == 18,
            (sum(map(len, pair_shifts.values())), occurrence_histogram,
             same_edge_occurrences))
    require(len(pair_shifts[FIRST_SAME_EDGE]) == 2
            and pair_columns[FIRST_SAME_EDGE] == 345,
            (pair_shifts[FIRST_SAME_EDGE], pair_columns[FIRST_SAME_EDGE]))
    shared_sites = Counter()
    for row in shared:
        left, right = row[1]
        shared_sites[next(iter(set(left[:2]) & set(right[:2])))] += 1
    require(sum(shared_sites.values()) == 148, shared_sites)
    public = {
        "operator_columns": len(columns),
        "coarsened_site_repeating_coordinates": len(rows),
        "labelled_pair_shift_occurrences": 271,
        "source_word_occurrences": dict(sorted(occurrence_histogram.items())),
        "shared_one_site_P3_coordinates": len(shared),
        "shared_site_histogram": {
            str(key): value for key, value in sorted(shared_sites.items())
        },
        "same_uncoloured_edge_coordinates": len(same_edge),
        "same_edge_labelled_occurrences": same_edge_occurrences,
        "diagonal_divided_square_coordinates": len(diagonal),
        "colour_distinct_same_edge_coordinates": len(mixed),
        "first_unmapped_coordinate": repr(FIRST_SAME_EDGE),
        "columns_hitting_first_unmapped_coordinate":
            pair_columns[FIRST_SAME_EDGE],
        "source_words_on_first_unmapped_coordinate": sorted(
            word_of_shift(shift) for shift in pair_shifts[FIRST_SAME_EDGE]),
        "cap_word": CAP_WORD,
        "pair_shadow_retains_word_fine_labels": False,
        "reason": (
            "159 rows are the union after forgetting 271 word/fine-shift "
            "occurrences; 112 rows occur in both source words"
        ),
    }
    private = {
        "all": rows, "shared": shared, "same_edge": same_edge,
        "diagonal": diagonal, "mixed": mixed,
    }
    return public, private


def projected_rank(site, basis, rows, prime) -> int:
    projected = {}
    for vector in basis.values():
        site.insert({row: value for row, value in vector.items() if row in rows},
                    projected, prime)
    return len(projected)


def rational_rank(columns) -> int:
    columns = tuple(tuple(map(Q, column)) for column in columns)
    if not columns:
        return 0
    rows = [[columns[column][row] for column in range(len(columns))]
            for row in range(len(columns[0]))]
    answer = 0
    for column in range(len(columns)):
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


def simplex_boundary(slot_count: int, size: int):
    from itertools import combinations
    source = tuple(combinations(range(slot_count), size))
    target = tuple(combinations(range(slot_count), size - 1))
    target_index = {face: index for index, face in enumerate(target)}
    columns = []
    for face in source:
        column = [Q(0)] * len(target)
        for position in range(size):
            subface = face[:position] + face[position + 1:]
            column[target_index[subface]] += Q(-1 if position % 2 else 1)
        columns.append(tuple(column))
    return tuple(columns)


def compose(left_columns, right_columns):
    return tuple(
        tuple(sum((Q(left_columns[mid][row]) * Q(column[mid])
                   for mid in range(len(left_columns))), Q(0))
              for row in range(len(left_columns[0])))
        for column in right_columns
    )


def d3_exactness_audit(hasse) -> dict[str, object]:
    require(hasse.ORDER == 6, hasse.ORDER)
    masks = tuple(range(1 << hasse.ORDER))
    require(all(hasse.coassociative(mask) for mask in masks),
            "the pinned Hasse coproduct stopped being coassociative")
    require(all(not hasse.apply_cobar(hasse.apply_cobar(
                    Counter({(mask,): 1})))
                for mask in masks[1:]),
            "the pinned Hasse cobar stopped squaring to zero")
    down_factors = [hasse.positional_down_factor(size)
                    for size in range(hasse.ORDER)]
    require(down_factors == [6, 5, 4, 3, 2, 1], down_factors)

    # L1, L2 and L3 are the singleton, pair and triple faces of the augmented
    # 5-simplex on six labelled derivative occurrences.
    d1 = simplex_boundary(6, 1)
    d2 = simplex_boundary(6, 2)
    d3 = simplex_boundary(6, 3)
    require((len(d1), len(d2), len(d3)) == (6, 15, 20),
            (len(d1), len(d2), len(d3)))
    require(rational_rank(d1) == 1
            and rational_rank(d2) == 5
            and rational_rank(d3) == 10,
            (rational_rank(d1), rational_rank(d2), rational_rank(d3)))
    composite = compose(d2, d3)
    require(all(not any(column) for column in composite),
            "the labelled D3-to-D2-to-D1 boundary stopped squaring to zero")
    pair_cycle_dimension = len(d2) - rational_rank(d2)
    require(pair_cycle_dimension == rational_rank(d3) == 10,
            (pair_cycle_dimension, rational_rank(d3)))
    return {
        "labelled_derivative_slots": 6,
        "augmented_5_simplex_face_dimensions_L1_L2_L3": [6, 15, 20],
        "boundary_ranks_d1_d2_d3": [1, 5, 10],
        "pinned_symmetrized_down_factors": down_factors,
        "pair_cycle_dimension": pair_cycle_dimension,
        "D3_image_dimension": rational_rank(d3),
        "H1_pair_layer": 0,
        "repeated_direction_symmetrization": (
            "coinvariants by a finite slot-permutation group; exact over Q by "
            "Reynolds averaging, with gamma_2 as the diagonal basis"
        ),
        "same_edge_D0_D1_cycles_are_D3_exact_in_canonical_source": True,
        "consequence": (
            "the 11 same-edge targets are mandatory for a literal chain-level "
            "159-coordinate comparison, but may be sent to zero by a derived "
            "comparison which includes the canonical D3 homotopy"
        ),
        "does_not_prove": (
            "that the shared-P3 cap contraction extends through every labelled "
            "D3 face; only the site-0 parent-labelled collision triangles are "
            "currently constructed"
        ),
        "physical_D3_to_AugP2_homotopy_constructed": False,
    }


def constrained_rank_audit(site, orbit, loaded, columns, shifts,
                           shapes) -> list[dict[str, object]]:
    records = []
    for prime in site.PRIMES:
        basis, hit, shadow_rank = orbit.projected_constrained_basis(
            site, columns, shifts, loaded["base"].DIRECT_FREE_PAIR, prime)
        require(hit == shapes["all"] and shadow_rank == 488
                and len(basis) == 153,
                (prime, len(hit), shadow_rank, len(basis)))
        ranks = {
            "shared_one_site": projected_rank(
                site, basis, shapes["shared"], prime),
            "same_edge": projected_rank(
                site, basis, shapes["same_edge"], prime),
            "diagonal_gamma2": projected_rank(
                site, basis, shapes["diagonal"], prime),
            "colour_distinct_same_edge": projected_rank(
                site, basis, shapes["mixed"], prime),
        }
        require(ranks == {
            "shared_one_site": 142,
            "same_edge": 11,
            "diagonal_gamma2": 7,
            "colour_distinct_same_edge": 4,
        }, (prime, ranks))
        kernel_dimension = len(basis) - ranks["shared_one_site"]
        require(kernel_dimension == ranks["same_edge"] == 11,
                (prime, kernel_dimension, ranks))
        records.append({
            "prime": prime,
            "dim_constrained_S": shadow_rank,
            "full_site_repeating_projection_rank": len(basis),
            "shared_one_site_projection_rank": ranks["shared_one_site"],
            "same_edge_projection_rank": ranks["same_edge"],
            "diagonal_gamma2_rank": ranks["diagonal_gamma2"],
            "colour_distinct_same_edge_rank":
                ranks["colour_distinct_same_edge"],
            "kernel_after_forgetting_same_edge_targets": kernel_dimension,
            "meaning": (
                "there are 11 independent D0/D1 cycles whose D2 boundary "
                "has no shared-one-site coordinate"
            ),
        })
    return records


def divided_hasse_repair_audit(columns, metadata, shapes) -> dict[str, object]:
    nonzero_diagonal_incidents = 0
    nonzero_mixed_incidents = 0
    for column, (_coefficient, directions) in zip(
            columns, metadata, strict=True):
        multiplicity = Counter(directions)
        for row in shapes["diagonal"]:
            cell = row[1][0]
            expected = comb(multiplicity[cell], 2)
            observed = column.get(row, 0)
            require(observed == expected,
                    ("gamma2 normalization changed", row, observed, expected))
            nonzero_diagonal_incidents += bool(observed)
        for row in shapes["mixed"]:
            left, right = row[1]
            expected = multiplicity[left] * multiplicity[right]
            observed = column.get(row, 0)
            require(observed == expected,
                    ("mixed divided-Hasse normalization changed",
                     row, observed, expected))
            nonzero_mixed_incidents += bool(observed)
    require(nonzero_diagonal_incidents > 0 and nonzero_mixed_incidents > 0,
            (nonzero_diagonal_incidents, nonzero_mixed_incidents))
    controls = {
        row: (f"gamma_2({row[1][0]!r})"
              if row in shapes["diagonal"]
              else f"gamma_1({row[1][0]!r})*gamma_1({row[1][1]!r})")
        for row in sorted(shapes["same_edge"], key=repr)
    }
    return {
        "new_coefficient_target_rows": len(controls),
        "diagonal_targets": len(shapes["diagonal"]),
        "diagonal_basis": "gamma_2(x_e), not x_e^2",
        "diagonal_normalization": (
            "the D2 constructor chooses unordered direction positions; a cell "
            "of multiplicity m has coefficient C(m,2), already divided-Hasse"
        ),
        "diagonal_nonzero_column_incidents_checked":
            nonzero_diagonal_incidents,
        "mixed_same_edge_targets": len(shapes["mixed"]),
        "mixed_basis": "gamma_1(x_e^a)*gamma_1(x_e^b)",
        "mixed_nonzero_column_incidents_checked": nonzero_mixed_incidents,
        "first_control": controls[FIRST_SAME_EDGE],
        "D0_D1_status": "unchanged; the target is applied to D2 ker(D0,D1)",
        "D2_rank_before_repair": 142,
        "D2_rank_added_by_same_edge_targets": 11,
        "D2_rank_after_repair": 153,
        "coefficient_pair_target_repaired": True,
        "physical_cap_differential_defined": False,
    }


def full_star_core_and_branch_audit(collision, protected, base) \
        -> dict[str, object]:
    star = collision.full_star_collision_audit(base)
    euler = collision.euler_and_triangle_audit(base)
    require(star["pair_collisions"] == 21
            and star["pair_output_rank_per_root"] == 7
            and star["pair_output_rank_two_root_direct_sum"] == 14
            and star["each_cap_term_pair_multiplicity"] == 6
            and star["coefficient_debt_after_natural_full_star_action"] == 0
            and euler["source_boundary_telescope"]
            and not euler["cap_K_Eq_projection_constructed"],
            (star, euler))

    cylinders = protected.ambiguity_and_deleted_cylinder_audit(base)
    require(cylinders["deleted_factor_squares"] == 1020
            and cylinders[
                "presentation_safe_deleted_factor_cylinders"] == 1020
            and cylinders[
                "deleted_factor_projection_rank_on_24_branches"] == 24,
            cylinders)

    # Rebuild every branch and check that it is a genuine missing/doubled P3
    # branch, never a parallel same-edge square.
    row = tuple(frozenset(monomial) for monomial in base.full_row((1,) * 8))
    left_parents = tuple(monomial for monomial in row if protected.A in monomial)
    right_parents = tuple(monomial for monomial in row if protected.B in monomial)
    branches = set()
    for left in left_parents:
        for right in right_parents:
            branches.add((left - {protected.A}) | {protected.B})
            branches.add((right - {protected.B}) | {protected.A})
    require(len(branches) == 24, len(branches))
    for branch in branches:
        uncoloured = [cell[:2] for cell in branch]
        multiplicity = Counter(site for edge in uncoloured for site in edge)
        require(len(set(uncoloured)) == len(uncoloured) == 4
                and sorted(multiplicity.values()) == [1, 1, 1, 1, 1, 1, 2]
                and len(multiplicity) == 7,
                (branch, uncoloured, multiplicity))

    return {
        "parent_labelled_full_star_core": {
            "unordered_pairs": star["pair_collisions"],
            "rank_per_root": star["pair_output_rank_per_root"],
            "two_root_rank": star["pair_output_rank_two_root_direct_sum"],
            "multiplicity_each_of_90_parents":
                star["each_cap_term_pair_multiplicity"],
            "normalization": "1/6",
            "complete_90_term_augmentation": True,
            "source_collision_triangle_telescope": True,
        },
        "deleted_factor_totalization": {
            "squares": cylinders["deleted_factor_squares"],
            "relative_cylinders": cylinders[
                "presentation_safe_deleted_factor_cylinders"],
            "branch_projection_rank": cylinders[
                "deleted_factor_projection_rank_on_24_branches"],
            "unique_branch_topologies_checked": len(branches),
            "every_branch_is_missing_doubled_P3_not_parallel_edge": True,
            "same_edge_target_rank_supplied": 0,
        },
        "operation_status": euler["operation_parent"],
        "cap_K_Eq_projection_constructed": False,
    }


def topology_word_and_packaging_audit(packaging, shapes) -> dict[str, object]:
    packaging.pin_dependencies()
    words = packaging.word_and_fine_grade_audit()
    package = packaging.augmented_packaging_audit()
    require(words["response_word_full"] == "11110000"
            and words["canonical_cap_word"] == CAP_WORD
            and words["all_six_fine_degrees_change"]
            and not words["literal_grade_preserving_map"]
            and package["rank_before_mixed_cell"] == 2
            and package["rank_after_mixed_cell"] == 3
            and package["rank_after_labelled_ridge"] == 4,
            (words, package))

    selected_edges = []
    for record in words["selected_P3K2_decorations"]:
        labels = tuple(record["undecorated"].split("*"))
        edges = tuple(packaging.EDGE_SITES[label] for label in labels)
        require(len(set(edges)) == 3, edges)
        degrees = Counter(site for edge in edges for site in edge)
        require(sorted(degrees.values()) == [1, 1, 1, 1, 2], degrees)
        selected_edges.append(edges)

    # A same-edge divided square has both endpoints doubled.  Even after a
    # disjoint remote K2 is appended, its degree profile is 2,2,1,1, not the
    # P3+K2 profile 2,1,1,1,1.
    for row in shapes["same_edge"]:
        edge = row[1][0][:2]
        require(row[1][1][:2] == edge, row)
        doubled_profile = Counter(site for copy in (edge, edge)
                                  for site in copy)
        require(sorted(doubled_profile.values()) == [2, 2],
                (row, doubled_profile))

    return {
        "existing_cap_topology": "P3+K2: three distinct uncoloured edges",
        "selected_cap_occurrences_checked": len(selected_edges),
        "selected_cap_site_degree_profile": [2, 1, 1, 1, 1],
        "same_edge_repair_topology": (
            "gamma_2(K2) for 7 rows and two colour-labelled parallel K2 "
            "factors for 4 rows"
        ),
        "same_edge_site_degree_profile_before_remote_K2": [2, 2],
        "same_edge_site_degree_profile_after_disjoint_remote_K2": [2, 2, 1, 1],
        "same_edge_is_P3_plus_K2": False,
        "source_pair_words": list(SOURCE_WORDS),
        "cap_word": CAP_WORD,
        "labelled_pair_shift_occurrences": 271,
        "literal_word_fine_map": False,
        "root_status": (
            "the order-six pair target has no AB/AC cap root idempotent; a "
            "physical receiving family would require two natural instances"
        ),
        "shared_collision_packaging_rank_ladder": [2, 3, 4],
        "shared_collision_first_post_word_debt":
            package["first_post_word_obstruction"],
        "shared_collision_first_ridge_debt":
            package["first_ridge_obstruction"],
        "minimal_new_cap_topology": (
            "a divided-square/parallel-edge AugP2 receiving object with its "
            "own word/fine/root and restriction-insertion faces"
        ),
    }


def beck_chevalley_and_keq_bypass_audit(collision, topology, base) \
        -> dict[str, object]:
    """Separate the coefficient star from its missing operation-labelled face.

    The two ordered DQ/PS branches and the two root sections form a K2,2
    packet.  Its edge boundary has rank three and the alternating four-edge
    cycle is the unique relative H1 class.  Objectwise restriction,
    reinsertion and K_Eq actions supply edges only.  In particular, applying
    K_Eq after the response-side I_i D_j reinsertion stays in the response
    operation corner; making it land on cap r0 is precisely the missing
    Beck--Chevalley/mixed mapping face, not a bypass around that face.
    """
    star = collision.full_star_collision_audit(base)
    require(star["pair_collisions"] == 21
            and star["pair_output_rank_per_root"] == 7
            and star["each_cap_term_pair_multiplicity"] == 6,
            star)

    # Vertices are (ordered branch, receiving root), and the four mate edges
    # are the ordinary K2,2 incidence edges.  Their only relation is the
    # alternating square boundary.
    edge_columns = (
        tuple(map(Q, (-1, 1, 0, 0))),
        tuple(map(Q, (-1, 0, 1, 0))),
        tuple(map(Q, (0, -1, 0, 1))),
        tuple(map(Q, (0, 0, -1, 1))),
    )
    square_cycle = tuple(map(Q, (1, -1, 1, -1)))
    require(rational_rank(edge_columns) == 3
            and all(sum(square_cycle[index] * edge_columns[index][row]
                        for index in range(4)) == 0
                    for row in range(4)),
            (edge_columns, square_cycle))

    require(topology["source_pair_words"] == list(SOURCE_WORDS)
            and topology["cap_word"] == CAP_WORD
            and not topology["literal_word_fine_map"]
            and topology["shared_collision_packaging_rank_ladder"]
                == [2, 3, 4], topology)
    return {
        "coefficient_groupoid_shadow": {
            "star_vertices": 7,
            "unordered_pair_objects": star["pair_collisions"],
            "incidence_rank_per_root": star["pair_output_rank_per_root"],
            "multiplicity_per_parent":
                star["each_cap_term_pair_multiplicity"],
            "groupoid_cardinality_normalization": "1/6",
            "complete_parent_augmentation": True,
        },
        "first_DQ_PS_root_packet": {
            "mate_edges": 4,
            "edge_boundary_rank": rational_rank(edge_columns),
            "relative_H1_dimension_without_BC_face": 1,
            "primitive_cycle": [int(value) for value in square_cycle],
            "current_operation_changing_BC_faces": 0,
        },
        "coefficient_incidence_and_groupoid_cardinality_test_passes": True,
        "coefficient_test_alone_proves_homotopy_Cartesian": False,
        "homotopy_Cartesian_in_literal_source_operation_category": False,
        "reason": (
            "the coefficient/groupoid-cardinality square closes, but its "
            "unique K2,2 Beck--Chevalley cycle has no response-to-cap "
            "operation-labelled filler"
        ),
        "KEq_after_response_reinsertion_bypass": {
            "I_i_D_j_output":
                "the original parent matching in the response common-V copy",
            "existing_KEq_action": "objectwise; preserves the operation corner",
            "output_operation_corner": "e_R A e_R, not e_C A e_R",
            "supplies_tied_cap_B_Eq": False,
            "supplies_cap_target_normalization": False,
            "equivalent_missing_datum":
                "the same mixed Beck--Chevalley/K_Eq mapping face",
        },
        "first_literal_bypass_failure": {
            "order_six_response_words": list(SOURCE_WORDS),
            "canonical_first_face_response_word": "11110000",
            "cap_word": topology["cap_word"],
            "all_six_selected_fine_degrees_change_on_canonical_face": True,
            "cap_word_in_response_D4_cube": False,
            "packaging_rank_ladder":
                topology["shared_collision_packaging_rank_ladder"],
            "face": topology["shared_collision_first_post_word_debt"],
        },
        "excess_Euler_interpretation": (
            "(H0-u)e_Eq is the relative obstruction carried by the absent "
            "mixed face; its coefficient shadow does not manufacture that face"
        ),
    }


def homogenizer_and_protected_audit(protected, base, local, normalized) \
        -> dict[str, object]:
    common = protected.common_parent_occurrence_augmentation(base)
    face = protected.first_literal_noncommuting_face(base)
    require(common["common_matching_augmentation_is_exact"]
            and common["common_base_difference_rank"] == 0
            and face["source_composite_nonzero"]
            and face["target_composite_zero"],
            (common, face))

    families = (local.top_projection_columns()
                + local.lower_face_and_reinsertion_columns()
                + local.external_augmented_columns())
    require(len(families) == 138
            and len({name for name, _column in families}) == 138,
            len(families))
    dark = tuple(column for _name, column in families)
    integral = local.integral_terminal_dual()
    omega = tuple(Q(value, 12) for value in integral)
    eq_orbit = local.balanced_top("Eq")
    rhs = local.balanced_top("B")
    dot = lambda left, right: sum((a * b for a, b in
                                   zip(left, right, strict=True)), Q(0))
    rank_dark = local.rank(dark)
    rank_with_eq = local.rank(dark + (eq_orbit,))
    require(len(integral) == 127
            and rank_dark == 126 and rank_with_eq == 127
            and all(dot(omega, column) == 0 for column in dark)
            and dot(omega, eq_orbit) == -1
            and dot(omega, rhs) == 1,
            (len(integral), rank_dark, rank_with_eq,
             dot(omega, eq_orbit), dot(omega, rhs)))

    normalized_ledger, normalized_digest = normalized.audit()
    require(normalized_digest == normalized.EXPECTED_LEDGER_SHA256,
            normalized_digest)
    normalized_comparison = normalized_ledger["normalized_comparison"]
    filler = normalized_ledger["relative_versus_absolute_filler"]
    require(normalized_comparison["mapping_cone_homology_H0_H1_H2"]
                == [1, 0, 0]
            and normalized_comparison["surviving_class"] == "E=e_Eq"
            and filler["relative_cap_homology_H0_H1"] == [1, 1]
            and filler["absolute_cap_homology_H0_H1"] == [0, 0],
            (normalized_comparison, filler))

    # Retain all 127 rows and append the eleven topology debts as a direct
    # labelled target summand.  Existing protected columns and the proposed
    # shared-P3 contraction have zero on that summand.  Formal same-edge
    # controls raise rank by exactly eleven, but are not source operations.
    topology_dimension = 11
    current_rank = rank_dark
    after_formal_same_edge_controls = current_rank + topology_dimension
    total_dimension = len(integral) \
        + topology_dimension
    require((current_rank, after_formal_same_edge_controls, total_dimension)
            == (126, 137, 138),
            (current_rank, after_formal_same_edge_controls, total_dimension))
    return {
        "homogenizer_and_common_V": {
            "common_base": common["common_base"],
            "response_and_cap_augmentations_equal": True,
            "common_base_difference_rank": 0,
            "homogenizer_closes_response_boundary": "H-u",
            "same_edge_divided_targets_in_common_V": False,
        },
        "first_existing_deleted_factor_face": {
            "factor": face["first_restriction_factor_q"],
            "source_composite": face["source_composite"],
            "target_composite": face["target_composite"],
            "commutator": face["commutator_value"],
        },
        "protected_local_packet": {
            "rows": len(integral),
            "literal_columns": len(dark),
            "current_rank": rank_dark,
            "rank_after_Eq_control": rank_with_eq,
            "omega_on_Eq": str(dot(omega, eq_orbit)),
            "omega_on_private_RHS": str(dot(omega, rhs)),
        },
        "protected_plus_topology_debt": {
            "row_dimension": total_dimension,
            "current_rank": current_rank,
            "rank_after_11_formal_same_edge_controls":
                after_formal_same_edge_controls,
            "same_edge_controls_are_physical_columns": False,
            "normalized_first_topology_dual": (
                "lambda_DP07=coefficient of gamma_2(x_07:11); it kills all "
                "shared-P3/full-star/1020-cylinder/current-127-row columns "
                "and reads one on the first required same-edge control"
            ),
        },
        "Eq_target_operation_status": (
            "the common V equality forgets Eq, target and operation; no "
            "same-edge Eq/AugP2 differential or nonzero e_C A e_R is defined"
        ),
        "normalization_Tor_guard": {
            "t=H0-u_base_change_makes_top_chain_map": True,
            "mapping_cone_homology_H0_H1_H2":
                normalized_comparison["mapping_cone_homology_H0_H1_H2"],
            "surviving_absolute_class": normalized_comparison[
                "surviving_class"],
            "relative_dK=tE_after_base_change": "an H1 cycle",
            "relative_filler_homology_H0_H1":
                filler["relative_cap_homology_H0_H1"],
            "absolute_dK=E_homology_H0_H1":
                filler["absolute_cap_homology_H0_H1"],
            "D3_exactness_is_sufficient_for_physical_comparison": False,
            "additional_requirement": (
                "the labelled D3 image must contain an absolute decorated "
                "Eq preimage, or Eq must be contractible in the full target"
            ),
        },
    }


def audit(full: bool) -> tuple[dict[str, object], str]:
    pin_dependencies()
    site, orbit, loaded, columns, shifts, metadata = build_current_tree()
    inventory, shapes = literal_pair_inventory(
        site, loaded, columns, shifts)

    collision = load(
        "computations/verify_h3_first_collision_full_star_completion_gate.py",
        "gammajet_collision",
    )
    protected = load(
        "computations/verify_h3_full_star_minimal_protected_homogenizer_cylinder_gate.py",
        "gammajet_protected",
    )
    packaging = load(
        "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py",
        "gammajet_packaging",
    )
    local = load(
        "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py",
        "gammajet_local",
    )
    hasse = load(
        "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py",
        "gammajet_hasse",
    )
    normalized = load(
        "computations/verify_h3_normalized_eq_base_change_tor_gate.py",
        "gammajet_normalized",
    )

    full_star_packet = full_star_core_and_branch_audit(
        collision, protected, loaded["base"])
    topology_packet = topology_word_and_packaging_audit(packaging, shapes)
    ledger = {
        "theorem": "h3 order-six GammaJet collision contraction same-edge gate",
        "pins": PINS,
        "full_two_prime_elimination_performed": full,
        "literal_8580_pair_inventory": inventory,
        "minimal_divided_Hasse_coefficient_repair":
            divided_hasse_repair_audit(columns, metadata, shapes),
        "augmented_5_simplex_D3_exactness": d3_exactness_audit(hasse),
        "parent_labelled_full_star_and_1020_faces":
            full_star_packet,
        "physical_topology_word_fine_root_gate":
            topology_packet,
        "restriction_insertion_Beck_Chevalley_and_KEq_bypass_gate":
            beck_chevalley_and_keq_bypass_audit(
                collision, topology_packet, loaded["base"]),
        "homogenizer_Eq_and_127_protected_rows":
            homogenizer_and_protected_audit(
                protected, loaded["base"], local, normalized),
    }
    if full:
        ledger["two_prime_D0_D1_D2_rank_test"] = constrained_rank_audit(
            site, orbit, loaded, columns, shifts, shapes)
    ledger.update({
        "verdict": (
            "The 1/6 full-star collision contraction is exact on its parent-"
            "labelled perfect-matching core, and the 1020 relative cylinders "
            "retain all deleted-factor faces. It is not a map on the complete "
            "159-row order-six pair target. Exactly 11 rows are same-edge "
            "divided-square/parallel-colour faces rather than shared-one-site "
            "P3 faces; in full mode they contribute independent rank 11 and "
            "leave an 11-dimensional D0/D1-cycle kernel after the proposed "
            "projection at both primes. Adjoining seven gamma_2 plus four mixed "
            "same-edge coefficient targets restores rank 153 and has the "
            "correct integral Hasse normalization. In the canonical augmented "
            "5-simplex source these 11 D0/D1 cycles are D3-exact, so a derived "
            "comparison may kill them rather than assign a cap value, but only "
            "after supplying the labelled D3 homotopy. This is not sufficient "
            "by itself: after t=H0-u=0 a relative dK=t*Eq face becomes a "
            "cycle and the absolute Eq class survives, so the D3 image must "
            "contain an absolute decorated Eq preimage (or contract Eq in the "
            "full target). No literal same-edge "
            "target has P3+K2 topology or a physical AugP2 word/fine/root/Eq "
            "landing, and the current shared contraction has no complete D3 "
            "extension. Therefore no nonzero e_C A e_R is defined. The next "
            "constructor is either that complete derived D3 comparison plus "
            "the operation-labelled Beck--Chevalley/K_Eq face or, for "
            "a strict 159-coordinate lift, a divided-square/parallel-edge AugP2 "
            "receiving object; dropping the 11 rows without either is invalid."
        ),
        "scope": (
            "current-tree literal 8580 order-six columns; exact combinatorial "
            "159=148+7+4 inventory and Hasse normalization; exact parent-"
            "labelled 21-pair/1/6 full-star, 1020 deleted-factor cylinders, "
            "homogenizer/common V, canonical D3 exactness, the normalization "
            "Tor guard, packaging and all 127 protected rows, and the finite "
            "K2,2 Beck--Chevalley/KEq-bypass "
            "test. Full "
            "mode adds the pinned two-prime 153=142+7+4 rank theorem. No "
            "no-orphan axiom or formal off-diagonal operation is granted."
        ),
    })
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    expected = (EXPECTED_FULL_LEDGER_SHA256 if full
                else EXPECTED_STRUCTURAL_LEDGER_SHA256)
    if expected != "TO_BE_PINNED":
        require(digest == expected,
                ("GammaJet collision ledger changed", full, digest, expected))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("full", "structural"), default="full")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    full = arguments.mode == "full"
    ledger, digest = audit(full)
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"h3 order-six GammaJet collision gate ({arguments.mode}): PASS")
        print("pair inventory: 159 = 148 shared-P3 + 7 gamma2 + 4 mixed-same-edge")
        if full:
            print("constrained ranks at both primes: 153 = 142 + 7 + 4")
        print("minimal coefficient repair: 11 divided-Hasse targets; rank 153")
        print("physical same-edge AugP2 landing: ABSENT")
        print("nonzero e_C A e_R from collision candidate: NO")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
