#!/usr/bin/env python3
"""Character-only S8 x S3 compression screen for quadratic Macaulay lifts.

No row-times-quadratic polynomial is expanded.  The script computes the two
S8 x S3 target stabilizers (the four B4 targets merge in pairs), decomposes
their induced permutation modules, and uses Frobenius reciprocity to count
the exact symmetry-adapted coefficient spaces inside the full quadratic
row-multiplier permutation module.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from math import factorial
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FROZEN = (ROOT / "computations" /
    "unaudited-codex-tail-remote-orbit-contraction-2026-08-21" /
    "results_tail_remote_orbit_contraction.json")
OUT = HERE / "results_equivariant_syzygy_compression.json"
EXPECTED_FROZEN_LOGICAL = \
    "de3a01efad1c9e20505f938153b9719a07917fa5080b029c87829324c4748e50"

SITES = tuple(range(8))
COLOURS = tuple(range(3))
EDGES = tuple(combinations(SITES, 2))
CELLS = tuple((u, v, left, right) for u, v in EDGES
              for left in COLOURS for right in COLOURS)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


@lru_cache(maxsize=None)
def integer_partitions(total, maximum=None):
    if total == 0:
        return ((),)
    if maximum is None or maximum > total:
        maximum = total
    answer = []
    for first in range(maximum, 0, -1):
        for tail in integer_partitions(total-first, first):
            answer.append((first,)+tail)
    return tuple(answer)


def cells_of_partition(partition):
    return {(row, column) for row, length in enumerate(partition)
            for column in range(length)}


@lru_cache(maxsize=None)
def rim_hook_removals(partition, size):
    target_size = sum(partition)-size
    if target_size < 0:
        return ()
    outer = cells_of_partition(partition)
    answer = []
    for inner in integer_partitions(target_size):
        if len(inner) > len(partition) or any(
                inner[row] > partition[row] for row in range(len(inner))):
            continue
        removed = outer-cells_of_partition(inner)
        if len(removed) != size or not removed:
            continue
        # A border strip is edge-connected and contains no 2x2 square.
        seen = {next(iter(removed))}
        stack = list(seen)
        while stack:
            row, column = stack.pop()
            for neighbour in ((row-1, column), (row+1, column),
                              (row, column-1), (row, column+1)):
                if neighbour in removed and neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        if seen != removed:
            continue
        if any({(row, column), (row+1, column),
                (row, column+1), (row+1, column+1)} <= removed
               for row, column in removed):
            continue
        height = len({row for row, _ in removed})
        answer.append((inner, -1 if height % 2 == 0 else 1))
    return tuple(answer)


@lru_cache(maxsize=None)
def irreducible_character(partition, cycle_type):
    if not cycle_type:
        return 1 if not partition else 0
    size = cycle_type[0]
    return sum(sign*irreducible_character(inner, cycle_type[1:])
               for inner, sign in rim_hook_removals(partition, size))


def class_size(cycle_type):
    counts = Counter(cycle_type)
    denominator = 1
    for length, multiplicity in counts.items():
        denominator *= (length**multiplicity)*factorial(multiplicity)
    return factorial(sum(cycle_type))//denominator


def representative_permutation(cycle_type):
    answer = list(range(sum(cycle_type)))
    start = 0
    for length in cycle_type:
        cycle = list(range(start, start+length))
        for index, value in enumerate(cycle):
            answer[value] = cycle[(index+1) % length]
        start += length
    return tuple(answer)


def cycle_type(permutation):
    seen = set()
    lengths = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        current, length = start, 0
        while current not in seen:
            seen.add(current)
            length += 1
            current = permutation[current]
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def compose(left, right):
    return tuple(left[right[index]] for index in range(len(left)))


def canonical_cell(u, v, left, right):
    return (u, v, left, right) if u < v else (v, u, right, left)


def act_cell(value, site_action, colour_action):
    u, v, left, right = value
    return canonical_cell(site_action[u], site_action[v],
                          colour_action[left], colour_action[right])


def act_word(word, site_action, colour_action):
    image = [None]*8
    for site, colour in enumerate(word):
        image[site_action[site]] = colour_action[colour]
    return tuple(image)


def act_target(target, site_action, colour_action):
    cell, pure_colour = target
    return act_cell(cell, site_action, colour_action), \
        colour_action[pure_colour]


def profile(word):
    return tuple(sorted(Counter(word).values(), reverse=True))


FULL_ROWS = tuple(word for word in product(COLOURS, repeat=8)
                  if profile(word) in ((7, 1), (6, 1, 1), (3, 3, 2)))
require(len(FULL_ROWS) == 48+168+1680 == 1896,
        "full S8 row closure changed")


def target_sets():
    endpoint, third = [], []
    for edge in EDGES:
        for left, right in permutations(COLOURS, 2):
            cell = (edge[0], edge[1], left, right)
            for pure in COLOURS:
                if pure in (left, right):
                    endpoint.append((cell, pure))
                else:
                    third.append((cell, pure))
    require((len(endpoint), len(third)) == (336, 168),
            "S8 target orbit sizes changed")
    return tuple(endpoint), tuple(third)


TARGET_ENDPOINT, TARGET_THIRD = target_sets()
TARGET_REPRESENTATIVES = {
    "endpoint": ((0, 1, 0, 1), 0),
    "third": ((0, 1, 0, 1), 2),
}


def fixed_count(universe, site_action, colour_action, action):
    return sum(action(value, site_action, colour_action) == value
               for value in universe)


def class_characters():
    records = {}
    for site_type in integer_partitions(8):
        site_action = representative_permutation(site_type)
        for colour_type in integer_partitions(3):
            colour_action = representative_permutation(colour_type)
            fixed_cells = fixed_count(CELLS, site_action, colour_action,
                                      act_cell)
            site_square = compose(site_action, site_action)
            colour_square = compose(colour_action, colour_action)
            fixed_cells_square = fixed_count(
                CELLS, site_square, colour_square, act_cell)
            fixed_quadratics = (fixed_cells**2+fixed_cells_square)//2
            fixed_rows = fixed_count(FULL_ROWS, site_action, colour_action,
                                     act_word)
            records[site_type, colour_type] = {
                "class_size": class_size(site_type)*class_size(colour_type),
                "fixed_cells": fixed_cells,
                "fixed_quadratic_cell_monomials": fixed_quadratics,
                "fixed_full_rows": fixed_rows,
                "degree1_domain_character": fixed_rows*fixed_cells,
                "degree2_domain_character": fixed_rows*fixed_quadratics,
                "endpoint_target_character": fixed_count(
                    TARGET_ENDPOINT, site_action, colour_action, act_target),
                "third_target_character": fixed_count(
                    TARGET_THIRD, site_action, colour_action, act_target),
            }
    require(sum(record["class_size"] for record in records.values()) ==
            factorial(8)*factorial(3), "group class sizes changed")
    return records


def validate_character_tables():
    for total in (3, 8):
        partitions = integer_partitions(total)
        for left in partitions:
            for right in partitions:
                inner = sum(class_size(cycle)*
                            irreducible_character(left, cycle)*
                            irreducible_character(right, cycle)
                            for cycle in partitions)
                expected = factorial(total) if left == right else 0
                require(inner == expected,
                        ("character orthogonality failed", total, left,
                         right, inner, expected))


def irrep_decomposition(class_records, character_key):
    group_order = factorial(8)*factorial(3)
    answer = {}
    for site_partition in integer_partitions(8):
        for colour_partition in integer_partitions(3):
            numerator = sum(
                record["class_size"]*record[character_key]
                * irreducible_character(site_partition, site_type)
                * irreducible_character(colour_partition, colour_type)
                for (site_type, colour_type), record
                in class_records.items())
            require(numerator % group_order == 0,
                    ("nonintegral character multiplicity", character_key,
                     site_partition, colour_partition, numerator))
            multiplicity = numerator//group_order
            require(multiplicity >= 0,
                    ("negative character multiplicity", character_key,
                     site_partition, colour_partition, multiplicity))
            if multiplicity:
                answer[site_partition, colour_partition] = multiplicity
    return answer


def irrep_dimension(partition):
    cells = cells_of_partition(partition)
    hook_product = 1
    for row, column in cells:
        right = sum((row, other) in cells
                    for other in range(column+1, partition[row]))
        below = sum((other, column) in cells
                    for other in range(row+1, len(partition)))
        hook_product *= 1+right+below
    return factorial(sum(partition))//hook_product


def check_dimension(decomposition, expected):
    actual = sum(multiplicity*irrep_dimension(site)*irrep_dimension(colour)
                 for (site, colour), multiplicity
                 in decomposition.items())
    require(actual == expected, ("module dimension changed", actual, expected))


def stabilizer_type_histogram(representative):
    histogram = Counter()
    order = 0
    for site_action in permutations(SITES):
        site_type = cycle_type(site_action)
        for colour_action in permutations(COLOURS):
            if act_target(representative, site_action, colour_action) == \
                    representative:
                histogram[site_type, cycle_type(colour_action)] += 1
                order += 1
    return order, histogram


def invariant_dimension_from_stabilizer(histogram, class_records,
                                        character_key, stabilizer_order):
    numerator = sum(count*class_records[key][character_key]
                    for key, count in histogram.items())
    require(numerator % stabilizer_order == 0,
            ("nonintegral stabilizer invariant dimension", character_key,
             numerator, stabilizer_order))
    return numerator//stabilizer_order


def format_irrep(key):
    site, colour = key
    return f"S8{site}xS3{colour}"


def main():
    frozen = json.loads(FROZEN.read_text())
    require(frozen["logical_sha256"] == EXPECTED_FROZEN_LOGICAL,
            "frozen degree-one contraction digest changed")
    validate_character_tables()
    classes = class_characters()

    endpoint_decomp = irrep_decomposition(classes,
                                           "endpoint_target_character")
    third_decomp = irrep_decomposition(classes, "third_target_character")
    degree1_domain = irrep_decomposition(classes,
                                          "degree1_domain_character")
    degree2_domain = irrep_decomposition(classes,
                                          "degree2_domain_character")
    check_dimension(endpoint_decomp, len(TARGET_ENDPOINT))
    check_dimension(third_decomp, len(TARGET_THIRD))
    check_dimension(degree1_domain, len(FULL_ROWS)*len(CELLS))
    check_dimension(degree2_domain,
                    len(FULL_ROWS)*(len(CELLS)*(len(CELLS)+1)//2))

    target_results = {}
    for name, representative in TARGET_REPRESENTATIVES.items():
        target_decomp = endpoint_decomp if name == "endpoint" else third_decomp
        stabilizer_order, stabilizer_histogram = \
            stabilizer_type_histogram(representative)
        expected_stabilizer = (factorial(8)*factorial(3)) // (
            len(TARGET_ENDPOINT) if name == "endpoint"
            else len(TARGET_THIRD))
        require(stabilizer_order == expected_stabilizer,
                ("target stabilizer changed", name, stabilizer_order,
                 expected_stabilizer))
        degree1_invariants = invariant_dimension_from_stabilizer(
            stabilizer_histogram, classes, "degree1_domain_character",
            stabilizer_order)
        degree2_invariants = invariant_dimension_from_stabilizer(
            stabilizer_histogram, classes, "degree2_domain_character",
            stabilizer_order)
        hom_degree2 = sum(multiplicity*degree2_domain.get(irrep, 0)
                          for irrep, multiplicity in target_decomp.items())
        require(hom_degree2 == degree2_invariants,
                ("Frobenius reciprocity failed", name, hom_degree2,
                 degree2_invariants))
        target_results[name] = {
            "representative": {
                "cell": "a_01_01",
                "pure_H_colour": representative[1]},
            "orbit_size": len(TARGET_ENDPOINT) if name == "endpoint"
                else len(TARGET_THIRD),
            "stabilizer_order": stabilizer_order,
            "stabilizer_conjugacy_type_histogram": {
                f"{site}|{colour}": count
                for (site, colour), count
                in sorted(stabilizer_histogram.items())},
            "induced_permutation_module": f"Ind_H^G(1), dimension {len(TARGET_ENDPOINT) if name == 'endpoint' else len(TARGET_THIRD)}",
            "irrep_multiplicities": {
                format_irrep(irrep): multiplicity
                for irrep, multiplicity in sorted(target_decomp.items())},
            "degree1_equivariant_coefficient_dimension": degree1_invariants,
            "degree2_equivariant_coefficient_dimension": degree2_invariants,
            "degree2_target_irrep_block_ledger": [
                {
                    "irrep": format_irrep(irrep),
                    "irrep_dimension":
                        irrep_dimension(irrep[0])*irrep_dimension(irrep[1]),
                    "target_multiplicity": target_multiplicity,
                    "degree2_domain_multiplicity":
                        degree2_domain.get(irrep, 0),
                    "multiplicity_space_entries":
                        target_multiplicity*degree2_domain.get(irrep, 0),
                }
                for irrep, target_multiplicity
                in sorted(target_decomp.items())],
        }

    endpoint_unknowns = target_results["endpoint"][
        "degree2_equivariant_coefficient_dimension"]
    third_unknowns = target_results["third"][
        "degree2_equivariant_coefficient_dimension"]
    payload = {
        "status": "PASS exact S8 x S3 character compression screen",
        "scope": {
            "expanded_polynomial_matrix": False,
            "full_59M_object_matrix_assembled": False,
            "broad_Groebner_basis": False,
            "calculation": "finite character theory, stabilizer Burnside sums, and Frobenius reciprocity",
        },
        "symmetry_correction": {
            "frozen_group": "B4 x S3",
            "requested_group": "S8 x S3",
            "frozen_rows": 1872,
            "S8_closed_rows": len(FULL_ROWS),
            "new_rows_required_for_an_S8_module": 24,
            "new_rows_profile": "the missing 6+1+1 words (144 grows to 168)",
            "degree2_literal_objects_after_S8_closure":
                len(FULL_ROWS)*(len(CELLS)*(len(CELLS)+1)//2),
            "guard": (
                "The frozen 1,872-row set is not S8-stable. Character/isotypic "
                "compression under S8 x S3 is only defined after adjoining "
                "the 24 missing 6+1+1 rows."),
        },
        "target_modules": {
            "B4_four_orbits_merge_under_S8": {
                "same_and_cross_endpoint": "one endpoint target orbit",
                "same_and_cross_third": "one third-colour target orbit",
            },
            "endpoint": target_results["endpoint"],
            "third": target_results["third"],
        },
        "degree2_domain": {
            "module": "Q[full mixed rows] tensor Sym^2(Q[252 cells])",
            "dimension": len(FULL_ROWS)*(len(CELLS)*(len(CELLS)+1)//2),
            "irreps_with_nonzero_multiplicity": len(degree2_domain),
            "irreps_total": len(integer_partitions(8))*len(integer_partitions(3)),
            "target_relevant_irreps": len(set(endpoint_decomp)|set(third_decomp)),
            "endpoint_H_fixed_orbits_equivariant_unknowns": endpoint_unknowns,
            "third_H_fixed_orbits_equivariant_unknowns": third_unknowns,
            "combined_two_target_module_Hom_dimension":
                endpoint_unknowns+third_unknowns,
            "interpretation": (
                "By Frobenius reciprocity these are exact dimensions of "
                "Hom_G(Ind_H^G 1,D2), equivalently H-orbits of quadratic "
                "row-multiplier objects. They are the smallest coefficient "
                "spaces before monomial-row expansion."),
        },
        "homogeneous_degree_guard": {
            "frozen_targets": "a_tail*H_k have ordinary degree 5",
            "quadratic_row_multipliers": "F_w*q have ordinary degree 6",
            "same_Macaulay_grade": False,
            "required_extra_choice": (
                "a linear homogenizer/localizer or a separately specified "
                "quadratic tail target; neither is frozen"),
        },
        "verdict": {
            "materially_smaller_than_25901_orbit_screen":
                endpoint_unknowns+third_unknowns < 25901,
            "export_exact_block_interface": False,
            "retire_symmetry_adapted_degree2_membership": True,
            "reason": (
                "Full S8 symmetry first enlarges the row module, the two "
                "target-induced Hom spaces remain large before monomial "
                "expansion, and degree-two rows do not even share the frozen "
                "degree-five target grade without an unaudited localizer."),
            "certified_comparison_baseline": 25901,
            "recommended_next_step": (
                "Use a source-labelled boundary substitution/localizer to "
                "define a genuinely degree-six target before revisiting "
                "isotypic blocks; character theory alone does not supply it."),
        },
        "pinned_frozen_logical_sha256": EXPECTED_FROZEN_LOGICAL,
    }
    payload["logical_sha256"] = logical_sha(payload)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")
    print(json.dumps({
        "logical_sha256": payload["logical_sha256"],
        "S8_closed_rows": len(FULL_ROWS),
        "endpoint_target_irreps": len(endpoint_decomp),
        "third_target_irreps": len(third_decomp),
        "endpoint_degree2_unknowns": endpoint_unknowns,
        "third_degree2_unknowns": third_unknowns,
        "combined_unknowns": endpoint_unknowns+third_unknowns,
        "materially_smaller": payload["verdict"][
            "materially_smaller_than_25901_orbit_screen"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
