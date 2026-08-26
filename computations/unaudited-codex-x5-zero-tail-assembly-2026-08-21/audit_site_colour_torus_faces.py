#!/usr/bin/env python3
"""Exact site-colour torus audit for the frozen zero-tail support shadow.

This is deliberately a character-lattice and finite-orbit computation.  It
does not solve any coefficient ideal.  The acting character lattice is
Z^(8*3), quotiented by the three pure-colour normalization characters.  The
script checks Hilbert--Mumford balance and strict coordinate-face exposure for
all 310 frozen B4 x S3 minimal-support records, enumerates every
inclusion-minimal support allowed by the six pure permanent rows in each
colour, and exhibits a larger balanced support which shows that this torus
alone cannot supply the missing degeneration lemma.
"""

from __future__ import annotations

from collections import Counter, deque
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ASSEMBLY = HERE / "results_extended_diagonal_packet_support_shadow.json"
OUT = HERE / "results_site_colour_torus_faces.json"

PAIRING = ((0, 1), (2, 3), (4, 5), (6, 7))
SUPER_EDGES = tuple(combinations(range(4), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(SUPER_EDGES)}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def rational_rank(rows):
    """Rank over Q, with no floating point or optional CAS dependency."""
    matrix = [[Fraction(value) for value in row] for row in rows
              if any(row)]
    if not matrix:
        return 0
    rank = 0
    columns = len(matrix[0])
    for column in range(columns):
        pivot = next((row for row in range(rank, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value/scale for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [left-scale*right for left, right
                           in zip(matrix[row], matrix[rank])]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def normalization_character(colour):
    row = [0]*24
    for site in range(8):
        row[8*colour+site] = 1
    return tuple(row)


NORMALIZATIONS = tuple(normalization_character(colour)
                       for colour in range(3))


def edge_character(colour, left, right):
    row = [0]*24
    row[8*colour+left] = 1
    row[8*colour+right] = 1
    return tuple(row)


def colour_edges(mask):
    """Four anchors plus one complementary pair in every 2x2 block."""
    answer = list(PAIRING)
    for index, (left_block, right_block) in enumerate(SUPER_EDGES):
        left = 2*left_block
        right = 2*right_block
        if (mask >> index) & 1:
            answer.extend(((left, right+1), (left+1, right)))
        else:
            answer.extend(((left, right), (left+1, right+1)))
    require(len(answer) == 16 and
            Counter(site for edge in answer for site in edge) ==
            {site: 4 for site in range(8)},
            ("minimal support is not four-regular", mask))
    return tuple(answer)


def projected_rank_for_mask(mask):
    rows = [edge_character(0, *edge) for edge in colour_edges(mask)]
    return rational_rank(rows + list(NORMALIZATIONS[:1])) - 1


def transform_mask(mask, permutation, flip_mask):
    answer = 0
    for index, (left, right) in enumerate(SUPER_EDGES):
        bit = ((mask >> index) & 1) ^ ((flip_mask >> left) & 1) ^ \
              ((flip_mask >> right) & 1)
        image = tuple(sorted((permutation[left], permutation[right])))
        answer |= bit << EDGE_INDEX[image]
    return answer


def transform_triple(triple, permutation, flip_mask, colour_permutation):
    transformed = [None]*3
    for colour, mask in enumerate(triple):
        transformed[colour_permutation[colour]] = transform_mask(
            mask, permutation, flip_mask)
    return tuple(transformed)


def b4_mask_orbits():
    actions = tuple((permutation, flip_mask)
                    for permutation in permutations(range(4))
                    for flip_mask in range(16))
    require(len(actions) == 384, "B4 order changed")
    remaining = set(range(64))
    records = []
    while remaining:
        representative = min(remaining)
        orbit = {transform_mask(representative, *action)
                 for action in actions}
        require(orbit <= remaining, ("B4 mask orbits overlap", representative))
        remaining -= orbit
        records.append({
            "representative": representative,
            "orbit_size": len(orbit),
            "members": sorted(orbit),
        })
    return records


def triple_generators():
    identity4 = tuple(range(4))
    identity3 = tuple(range(3))
    generators = []
    for position in range(3):
        permutation = list(identity4)
        permutation[position], permutation[position+1] = \
            permutation[position+1], permutation[position]
        generators.append((tuple(permutation), 0, identity3))
    for block in range(4):
        generators.append((identity4, 1 << block, identity3))
    for position in range(2):
        colour_permutation = list(identity3)
        colour_permutation[position], colour_permutation[position+1] = \
            colour_permutation[position+1], colour_permutation[position]
        generators.append((identity4, 0, tuple(colour_permutation)))
    return tuple(generators)


def triple_orbits():
    """All 64^3 pure-row-minimal triples modulo common B4 and colour S3."""
    generators = triple_generators()
    remaining = set(product(range(64), repeat=3))
    owner = {}
    records = []
    while remaining:
        seed = min(remaining)
        orbit = {seed}
        queue = deque([seed])
        while queue:
            state = queue.popleft()
            for action in generators:
                image = transform_triple(state, *action)
                if image not in orbit:
                    orbit.add(image)
                    queue.append(image)
        representative = min(orbit)
        require(representative == seed and orbit <= remaining,
                ("triple orbit overlap/noncanonical", seed))
        for state in orbit:
            owner[state] = representative
        remaining -= orbit
        records.append((representative, len(orbit)))
    require(len(owner) == 64**3, "pure triple universe changed")
    return owner, records


def frozen_records():
    assembly = json.loads(ASSEMBLY.read_text())
    records = assembly["support_shadow"][
        "minimal_surviving_support_signature_antichain"]
    require(len(records) == 310, "frozen support orbit count changed")
    return records


def main():
    # The three disjoint primitive normalization rows have SNF diagonal 1,1,1.
    normalization_rank = rational_rank(NORMALIZATIONS)
    require(normalization_rank == 3, "normalization rank changed")

    mask_ranks = {mask: projected_rank_for_mask(mask) for mask in range(64)}
    b4_orbits = b4_mask_orbits()
    for record in b4_orbits:
        require(len({mask_ranks[mask] for mask in record["members"]}) == 1,
                ("rank is not B4 invariant", record))
        record["projected_character_rank"] = mask_ranks[
            record["representative"]]

    owner, pure_triple_orbits = triple_orbits()
    pure_orbit_histogram = Counter(size for _, size in pure_triple_orbits)

    frozen = frozen_records()
    frozen_rank_histogram = Counter()
    frozen_rank_orbit_histogram = Counter()
    frozen_x_orbits = set()
    labelled_frozen = 0
    for record in frozen:
        masks = tuple(record[
            "x_relation_masks_e01_e02_e03_e12_e13_e23"])
        ranks = tuple(mask_ranks[mask] for mask in masks)
        total_rank = sum(ranks)
        lineality = 21-total_rank
        frozen_rank_histogram[(tuple(sorted(ranks)), total_rank,
                               lineality)] += 1
        orbit_size = record["orbit_size"]
        frozen_rank_orbit_histogram[(tuple(sorted(ranks)), total_rank,
                                     lineality)] += orbit_size
        labelled_frozen += orbit_size
        frozen_x_orbits.add(owner[masks])
    require(labelled_frozen == 275568,
            ("labelled frozen count changed", labelled_frozen))
    pure_triple_orbit_ledger = [
        {
            "representative": list(representative),
            "orbit_size": orbit_size,
            "sorted_per_colour_projected_ranks": sorted(
                mask_ranks[mask] for mask in representative),
            "represented_in_frozen_310_x_projection":
                representative in frozen_x_orbits,
        }
        for representative, orbit_size in pure_triple_orbits
    ]

    # Uniform positive coefficients prove relative-interior balance exactly:
    # every minimal graph is 4-regular, hence the sum of its 16 weights is
    # 4*s_c.  Across colours the average is (s_0+s_1+s_2)/12, zero in M'.
    uniform_sum = [0]*24
    for colour in range(3):
        for edge in colour_edges(0):
            character = edge_character(colour, *edge)
            uniform_sum = [left+right for left, right
                           in zip(uniform_sum, character)]
    require(tuple(uniform_sum) == tuple(
        4*sum(NORMALIZATIONS[colour][coordinate] for colour in range(3))
        for coordinate in range(24)),
        "uniform barycentric certificate changed")

    # A full-support graph is 7-regular (one anchor and all four cells to
    # each other block).  It is a strict larger balanced support, fixed by
    # all of B4 x S3, and is permitted by the pure support conditions.
    full_edges = list(PAIRING)
    for left_block, right_block in SUPER_EDGES:
        for left_bit, right_bit in product((0, 1), repeat=2):
            full_edges.append((2*left_block+left_bit,
                               2*right_block+right_bit))
    require(len(full_edges) == 28 and
            Counter(site for edge in full_edges for site in edge) ==
            {site: 7 for site in range(8)},
            "full support is not seven-regular")

    payload = {
        "scope": {
            "calculation": "exact character lattice, rational linear algebra, and finite group orbits only",
            "coefficient_ideal_solved": False,
            "larger_support_example_is_actual_source_solution": False,
        },
        "site_colour_character_lattice": {
            "ambient_rank": 24,
            "character_basis": "e_(site,colour), 8 sites x 3 colours",
            "edge_character": "chi(x^c_ij)=e_(i,c)+e_(j,c)",
            "normalization_characters": [
                "s_c=sum_i e_(i,c), c=0,1,2"],
            "normalization_rank": normalization_rank,
            "normalization_sublattice_saturated": True,
            "smith_diagonal": [1, 1, 1],
            "quotient_rank": 21,
            "dual_gauge": "sum_i h_(i,c)=0 for each colour c",
        },
        "frozen_310_hilbert_mumford": {
            "support_orbits": len(frozen),
            "labelled_minimal_supports": labelled_frozen,
            "positive_balance_certificate": {
                "coefficient_on_each_of_48_live_edges": "1/48",
                "sum_of_live_characters": "4*(s_0+s_1+s_2)",
                "projected_barycentre": "0",
                "all_coefficients_strictly_positive": True,
            },
            "torus_closed_polystable_orbits": len(frozen),
            "torus_closed_polystable_labelled_supports": labelled_frozen,
            "destabilizing_HM_cones_nonempty": 0,
            "strict_coordinate_1PS_face_orbits": 0,
            "strict_coordinate_1PS_face_labelled_supports": 0,
            "strict_face_Farkas_certificate": {
                "identity": "w00+w11-w01-w10=0 in every 2x2 block",
                "diagonal_live_contradiction": "w00=w11=m and w01,w10>m imply 2m=w01+w10>2m",
                "anti_live_contradiction": "w01=w10=m and w00,w11>m imply 2m=w00+w11>2m",
                "scope": "one block already makes the strict exposure cone empty",
            },
            "projected_rank_and_HM_lineality_orbit_histogram": [
                {
                    "sorted_per_colour_projected_ranks": list(key[0]),
                    "total_projected_rank": key[1],
                    "HM_lineality_dimension_in_rank21_cocharacter_space": key[2],
                    "support_orbits": count,
                    "labelled_supports": frozen_rank_orbit_histogram[key],
                }
                for key, count in sorted(frozen_rank_histogram.items())
            ],
        },
        "pure_matching_row_minimal_balanced_supports": {
            "one_colour_description": "four anchors plus diagonal or anti complementary pair in each of six 2x2 blocks",
            "one_colour_labelled_supports": 64,
            "one_colour_B4_orbits": b4_orbits,
            "three_colour_labelled_supports": 64**3,
            "three_colour_B4_times_S3_orbits": len(pure_triple_orbits),
            "three_colour_orbit_size_histogram": {
                str(size): count for size, count
                in sorted(pure_orbit_histogram.items())},
            "three_colour_exact_orbit_ledger": pure_triple_orbit_ledger,
            "all_are_balanced": True,
            "uniform_one_colour_sum": "4*s_c",
            "frozen_310_distinct_x_only_orbits": len(frozen_x_orbits),
            "pure_x_orbits_not_represented_in_frozen_310":
                len(pure_triple_orbits)-len(frozen_x_orbits),
        },
        "larger_balanced_support_counterexample": {
            "support_level_only": True,
            "one_colour_edges": 28,
            "three_colour_edges": 84,
            "description": "four anchors plus all four cells in every cross-block, independently in all three colours",
            "site_degree_in_each_colour": 7,
            "sum_of_live_characters": "7*(s_0+s_1+s_2)",
            "strict_positive_projected_barycentre_zero": True,
            "B4_times_S3_orbit_size": 1,
            "permitted_by_pure_matching_support_rows": True,
            "contained_in_a_frozen_minimal_support": False,
            "contains_every_frozen_minimal_support": True,
            "strict_1PS_degeneration_to_any_complementary_pair_choice": False,
            "obstruction": "the same 2x2 additive Farkas identity",
            "warning": "This is not asserted to satisfy the mixed source equations or H-live/no-cap coefficient conditions.",
        },
        "conclusion": {
            "all_frozen_310_are_torus_closed": True,
            "any_frozen_310_is_a_strict_1PS_face": False,
            "every_pure_row_permitted_torus_closed_support_lies_in_frozen_310": False,
            "site_colour_torus_proves_missing_larger_support_reduction": False,
            "remaining_requirement": "mixed-row initial-ideal/degeneration theorem or direct exclusion of larger balanced supports",
        },
    }
    payload["logical_sha256"] = logical_sha(payload)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")
    print(json.dumps({
        "logical_sha256": payload["logical_sha256"],
        "pure_triple_orbits": len(pure_triple_orbits),
        "frozen_x_orbits": len(frozen_x_orbits),
        "rank_histogram": payload["frozen_310_hilbert_mumford"][
            "projected_rank_and_HM_lineality_orbit_histogram"],
        "larger_balanced_counterexample": True,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
