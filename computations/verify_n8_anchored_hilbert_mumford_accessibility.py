#!/usr/bin/env python3
"""Exact Hilbert--Mumford character audit around the anchored cylinder germ."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import product

import verify_n8_four_cut_two_cell_orbit_feasibility as orbit
import verify_n8_d1_m10_334_branch63_candidate as d1_candidate
import verify_n8_three_cut_exactness_tangent as tangent


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def signed_ray_key(vector):
    if not vector:
        return ()
    pivot = min(vector)
    scale = abs(vector[pivot])
    return tuple(sorted((index, value / scale) for index, value in vector.items()))


def opposite_key(key):
    return tuple((index, -value) for index, value in key)


def small_destabilizing_cocharacter(support):
    diagonal_edges = {
        colour: tuple(
            (left, right)
            for left, right, left_colour, right_colour in support
            if left_colour == right_colour == colour
        )
        for colour in range(3)
    }
    mixed = tuple(
        coordinate
        for coordinate in support
        if coordinate[2] != coordinate[3]
    )
    for radius in range(1, 4):
        candidates = {}
        for colour in range(3):
            colour_candidates = []
            for prefix in product(range(-radius, radius + 1), repeat=7):
                last = -sum(prefix)
                if not -radius <= last <= radius:
                    continue
                values = prefix + (last,)
                if all(values[left] + values[right] >= 0 for left, right in diagonal_edges[colour]):
                    colour_candidates.append(values)
            candidates[colour] = tuple(colour_candidates)
        for middle in candidates[1]:
            for first in candidates[0]:
                if any(
                    first[left] + middle[right] < 0
                    if left_colour == 0 else
                    middle[left] + first[right] < 0
                    for left, right, left_colour, right_colour in mixed
                    if {left_colour, right_colour} == {0, 1}
                ):
                    continue
                for second in candidates[2]:
                    h = (first, middle, second)
                    weights = tuple(
                        h[left_colour][left] + h[right_colour][right]
                        for left, right, left_colour, right_colour in support
                    )
                    if all(weight >= 0 for weight in weights) and any(weight > 0 for weight in weights):
                        return h, weights
    return None


def main() -> None:
    boundary_shear = tangent.load_boundary_shear()
    dependence = boundary_shear.load_dependence()
    quotient = dependence.load_quotient()
    cached = quotient.load_cached_blocks()
    matrix_cache = cached.load_cache_module()
    palette = matrix_cache.load_palette()
    five = palette.load_five_frontier()
    four = five.load_four_closure()
    bounded = four.load_bounded_frontier()
    data = bounded.prepare()
    module = data["module"]
    one_cell = data["one_cell"]
    support = tuple(sorted(one_cell.support_coordinates(data["base"])))
    absent = tuple(
        coordinate for coordinate in one_cell.all_coordinates() if coordinate not in support
    )
    target_characters = one_cell.target_characters()
    target_basis = module.rational_basis(list(target_characters))
    require(len(target_basis) == 3, "target-character rank changed")

    projected_support = tuple(
        orbit.quotient_remainder(one_cell.coordinate_character(coordinate), target_basis)
        for coordinate in support
    )
    balance_relations, projected_support_rank = tangent.kernel_relations(projected_support)
    destabilizing = small_destabilizing_cocharacter(support)
    require(projected_support_rank == 12, "anchor quotient rank changed")
    require(len(balance_relations) == 4, "anchor balance nullity changed")
    expected_h = (
        (-1, 1, 0, 0, -1, 1, -1, 1),
        (-1, -1, 1, -1, 1, -1, 1, 1),
        (-1, -1, 1, 1, 1, -1, 1, -1),
    )
    expected_weights = (0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)
    require(destabilizing == (expected_h, expected_weights), "anchor HM certificate changed")
    require(all(sum(row) == 0 for row in expected_h), "cocharacter is not target stabilizing")
    positive_coordinate = support[expected_weights.index(1)]
    require(positive_coordinate == (2, 5, 0, 0), "positive anchor coordinate changed")

    # The finite HM limit simply deletes the unique positive-weight cell.  It
    # preserves the three pure target coefficients (their target characters
    # vanish), while mixed coefficients may and do change.
    limit_cells = {
        edge: [
            entry
            for entry in entries
            if (*edge, entry[0], entry[1]) != positive_coordinate
        ]
        for edge, entries in data["base"].items()
    }
    base_tensor = module.matching_tensor(module.B, data["base"])
    limit_tensor = module.matching_tensor(module.B, limit_cells)
    unit_gate = one_cell.load_unit_gate()
    require(unit_gate.pure_tuple(module, base_tensor) == (1, 1, 1), "base anchors changed")
    require(unit_gate.pure_tuple(module, limit_tensor) == (1, 1, 1), "HM limit lost an anchor")
    tensor_difference = one_cell.sparse_difference(limit_tensor, base_tensor)
    limit_cut_status = tuple(
        unit_gate.active_complete(module.cut_record(z, limit_cells))
        for z in unit_gate.THREE_CUTS
    )
    require(len(tensor_difference) == 2, "HM-limit tensor-difference count changed")
    require(limit_cut_status == (True, True, False), "HM-limit cut status changed")

    anchor_constraint_basis = module.rational_basis(
        list(target_characters)
        + [one_cell.coordinate_character(coordinate) for coordinate in support]
    )
    require(len(anchor_constraint_basis) == 15, "anchor character rank changed")
    remainders = {
        coordinate: orbit.quotient_remainder(
            one_cell.coordinate_character(coordinate), anchor_constraint_basis
        )
        for coordinate in absent
    }
    ray_classes = {}
    for coordinate, remainder in remainders.items():
        ray_classes.setdefault(signed_ray_key(remainder), []).append(coordinate)
    invisible = tuple(ray_classes.get((), ()))
    require(
        invisible
        == (
            (2, 4, 2, 0),
            (2, 6, 0, 1),
            (3, 4, 0, 0),
            (3, 7, 0, 2),
            (4, 6, 0, 1),
            (5, 7, 0, 2),
        ),
        "anchor-invisible coordinate ledger changed",
    )

    opposing_pairs = []
    visited = set()
    for key, coordinates in ray_classes.items():
        if not key or key in visited:
            continue
        opposite = opposite_key(key)
        if opposite not in ray_classes:
            continue
        visited.add(key)
        visited.add(opposite)
        for left in coordinates:
            for right in ray_classes[opposite]:
                opposing_pairs.append(tuple(sorted((left, right))))
    opposing_pairs = tuple(sorted(set(opposing_pairs)))
    require(len(ray_classes) - 1 == 136, "signed quotient-ray count changed")
    require(len(opposing_pairs) == 292, "opposing-pair count changed")
    require(
        opposing_pairs[0] == ((0, 1, 0, 1), (1, 4, 0, 1)),
        "first opposing pair changed",
    )

    plane_absent = tuple(dependence.ADMISSIBLE_DIRECTIONS)
    plane_basis = module.rational_basis(
        list(anchor_constraint_basis.values())
        + [one_cell.coordinate_character(coordinate) for coordinate in plane_absent]
    )
    plane_outside = tuple(
        coordinate for coordinate in absent if coordinate not in plane_absent
    )
    plane_quotient_rays = Counter(
        signed_ray_key(
            orbit.quotient_remainder(
                one_cell.coordinate_character(coordinate), plane_basis
            )
        )
        for coordinate in plane_outside
    )
    require(len(plane_basis) == 21, "anchor-plus-plane character rank changed")
    require(len(plane_outside) == 222, "outside-plane coordinate count changed")
    require(plane_quotient_rays.get((), 0) == 111, "plane-invisible count changed")

    # The current D1 m=10 object is a 77-cell semantic chart (its localized
    # coefficient ideal is known empty, so it is not an exact source).  Its
    # support is also HM-unstable, by this integral target cocharacter.
    d1_support = tuple(
        sorted(map(tuple, d1_candidate.build_artifact()["localized_nonzero_cells"]))
    )
    require(len(d1_support) == 77, "D1 semantic support size changed")
    d1_h = (
        (0, 0, 0, 0, 0, 0, 0, 0),
        (0, 1, 0, 1, -1, -1, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0),
    )
    require(all(sum(row) == 0 for row in d1_h), "D1 cocharacter is not target stabilizing")
    d1_weights = tuple(
        d1_h[left_colour][left] + d1_h[right_colour][right]
        for left, right, left_colour, right_colour in d1_support
    )
    require(Counter(d1_weights) == Counter({0: 54, 1: 22, 2: 1}), "D1 HM ledger changed")

    print("N=8 anchored Hilbert--Mumford accessibility audit: exact frontier")
    print(
        "target/anchor projected ranks and stabilizer dimensions: "
        f"target={len(target_basis)}, anchor quotient={projected_support_rank}, "
        f"anchor stabilizer={24-len(anchor_constraint_basis)}"
    )
    print(f"anchor balance nullity: {len(balance_relations)}")
    print("strict positive anchor balance: impossible by the displayed HM certificate")
    print(f"small anchored destabilizing cocharacter/weights: {destabilizing}")
    print(
        "finite HM initial form: delete "
        f"{positive_coordinate}; mixed tensor changes={len(tensor_difference)}; "
        f"pure anchors remain (1,1,1); three-cut status={limit_cut_status}"
    )
    print(f"invisible absent coordinates: {invisible}")
    print(f"signed quotient rays / opposing literal pairs: {len(ray_classes)-1}/{len(opposing_pairs)}")
    print(f"first opposing pair: {opposing_pairs[0] if opposing_pairs else None}")
    print(
        "anchor-plus-plane character rank / residual stabilizer: "
        f"{len(plane_basis)}/{24-len(plane_basis)}"
    )
    print(
        "outside-plane zero/nonzero ray counts: "
        f"{plane_quotient_rays.get((), 0)}/{len(plane_outside)-plane_quotient_rays.get((), 0)}"
    )
    print(
        "D1 m10 semantic support HM weights: "
        f"{dict(sorted(Counter(d1_weights).items()))} (chart is coefficient-empty)"
    )
    print("verdict: target-torus accessibility is not forced by support minimality")


if __name__ == "__main__":
    main()
