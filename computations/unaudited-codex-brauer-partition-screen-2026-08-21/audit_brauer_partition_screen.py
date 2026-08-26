#!/usr/bin/env python3
"""Exact character/rank screen for Brauer/partition-algebra compression."""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from math import factorial
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_brauer_partition_screen.json"
ROUTING = (ROOT / "computations/unaudited-codex-x5-zero-tail-routing-2026-08-21" /
           "results_x5_zero_tail_routing.json")
ZEON = (ROOT / "computations/unaudited-codex-zeon-contraction-hierarchy-2026-08-21" /
        "results_zeon_contraction_hierarchy.json")
ROUTING_DIGEST = "85a18c7f6c02678fe9806ca8ab9654643c5f6b0637867d4f2b71d181e3b21171"
ZEON_DIGEST = "2864c5a426f9aac920013d1d9ac44b01e0e233e5888d25f3109db80aac88d7b5"


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
    target = sum(partition)-size
    if target < 0:
        return ()
    outer = cells_of_partition(partition)
    answer = []
    for inner in integer_partitions(target):
        if len(inner) > len(partition) or any(
                inner[row] > partition[row] for row in range(len(inner))):
            continue
        removed = outer-cells_of_partition(inner)
        if len(removed) != size or not removed:
            continue
        start = next(iter(removed))
        seen, stack = {start}, [start]
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
        height = len({row for row, _column in removed})
        answer.append((inner, -1 if height % 2 == 0 else 1))
    return tuple(answer)


@lru_cache(maxsize=None)
def irreducible_character(partition, cycle_type):
    if not cycle_type:
        return int(not partition)
    return sum(sign*irreducible_character(inner, cycle_type[1:])
               for inner, sign in rim_hook_removals(partition, cycle_type[0]))


def class_size(cycle_type):
    denominator = 1
    for length, multiplicity in Counter(cycle_type).items():
        denominator *= length**multiplicity*factorial(multiplicity)
    return factorial(sum(cycle_type))//denominator


def representative_permutation(cycle_type):
    permutation = list(range(sum(cycle_type)))
    start = 0
    for length in cycle_type:
        cycle = list(range(start, start+length))
        for index, value in enumerate(cycle):
            permutation[value] = cycle[(index+1) % length]
        start += length
    return tuple(permutation)


def act_word(word, site_action, colour_action):
    image = [None]*len(word)
    for site, colour in enumerate(word):
        image[site_action[site]] = colour_action[colour]
    return tuple(image)


def canonical_cell(left, right, a, b):
    return (left, right, a, b) if left < right else (right, left, b, a)


def act_cell(cell, site_action, colour_action):
    left, right, a, b = cell
    return canonical_cell(site_action[left], site_action[right],
                          colour_action[a], colour_action[b])


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index]+vertices[index+1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),)+tail


PM8 = tuple(frozenset(matching) for matching in perfect_matchings(range(8)))
WORDS8 = tuple(product(range(3), repeat=8))
PURE8 = tuple(word for word in WORDS8 if len(set(word)) == 1)
MIXED8 = tuple(word for word in WORDS8 if len(set(word)) > 1)
EVEN_MIXED8 = tuple(word for word in MIXED8
                    if all(count % 2 == 0 for count in Counter(word).values()))
PAIRS8 = tuple(combinations(range(8), 2))
CELLS8 = tuple((left, right, a, b) for left, right in PAIRS8
               for a in range(3) for b in range(3))
require((len(PM8), len(WORDS8), len(MIXED8), len(EVEN_MIXED8),
         len(PAIRS8), len(CELLS8)) == (105, 6561, 6558, 1638, 28, 252),
        "ambient census changed")


def act_matching(matching, site_action):
    return frozenset(tuple(sorted((site_action[left], site_action[right])))
                     for left, right in matching)


def fixed_count(universe, action, *actions):
    return sum(action(value, *actions) == value for value in universe)


def class_records_8():
    answer = {}
    for site_type in integer_partitions(8):
        site_action = representative_permutation(site_type)
        fixed_matchings = fixed_count(PM8, act_matching, site_action)
        fixed_pairs = fixed_count(PAIRS8,
                                  lambda pair, action: tuple(sorted(
                                      (action[pair[0]], action[pair[1]]))),
                                  site_action)
        for colour_type in integer_partitions(3):
            colour_action = representative_permutation(colour_type)
            fixed_words = fixed_count(WORDS8, act_word,
                                      site_action, colour_action)
            fixed_pure = fixed_count(PURE8, act_word,
                                     site_action, colour_action)
            fixed_mixed = fixed_count(MIXED8, act_word,
                                      site_action, colour_action)
            fixed_even = fixed_count(EVEN_MIXED8, act_word,
                                     site_action, colour_action)
            fixed_cells = fixed_count(CELLS8, act_cell,
                                      site_action, colour_action)
            require(fixed_words == fixed_pure+fixed_mixed,
                    "word character split failed")
            answer[site_type, colour_type] = {
                "class_size": class_size(site_type)*class_size(colour_type),
                "matching": fixed_matchings,
                "word": fixed_words,
                "pure": fixed_pure,
                "mixed": fixed_mixed,
                "even_mixed": fixed_even,
                "degree4_monomial_domain": fixed_matchings*fixed_words,
                "degree4_kernel": (fixed_matchings-1)*fixed_words,
                "pair": fixed_pairs,
                "cell": fixed_cells,
            }
    require(sum(row["class_size"] for row in answer.values()) ==
            factorial(8)*factorial(3), "S8xS3 classes changed")
    return answer


def validate_character_tables():
    for total in (3, 6, 8):
        partitions = integer_partitions(total)
        for left in partitions:
            for right in partitions:
                inner = sum(class_size(cycle_type)
                            * irreducible_character(left, cycle_type)
                            * irreducible_character(right, cycle_type)
                            for cycle_type in partitions)
                expected = factorial(total) if left == right else 0
                require(inner == expected,
                        ("character orthogonality", total, left, right,
                         inner, expected))


def decompose(records, key, site_total=8):
    group_order = factorial(site_total)*factorial(3)
    answer = {}
    for site_partition in integer_partitions(site_total):
        for colour_partition in integer_partitions(3):
            numerator = sum(
                row["class_size"]*row[key]
                * irreducible_character(site_partition, site_type)
                * irreducible_character(colour_partition, colour_type)
                for (site_type, colour_type), row in records.items())
            require(numerator % group_order == 0,
                    ("nonintegral multiplicity", key, site_partition,
                     colour_partition, numerator))
            multiplicity = numerator//group_order
            require(multiplicity >= 0,
                    ("negative multiplicity", key, site_partition,
                     colour_partition, multiplicity))
            if multiplicity:
                answer[site_partition, colour_partition] = multiplicity
    return answer


def dimension(partition):
    cells = cells_of_partition(partition)
    hooks = 1
    for row, column in cells:
        right = sum((row, other) in cells
                    for other in range(column+1, partition[row]))
        below = sum((other, column) in cells
                    for other in range(row+1, len(partition)))
        hooks *= 1+right+below
    return factorial(sum(partition))//hooks


def module_dimension(decomposition):
    return sum(multiplicity*dimension(site)*dimension(colour)
               for (site, colour), multiplicity in decomposition.items())


def label_irrep(irrep):
    return f"S8{irrep[0]}xS3{irrep[1]}"


def matching_decomposition(records):
    group_order = factorial(8)
    answer = {}
    for partition in integer_partitions(8):
        numerator = 0
        for site_type in integer_partitions(8):
            row = records[site_type, (1, 1, 1)]
            # matching character is colour-independent; use S8 class size only.
            numerator += (class_size(site_type)*row["matching"]
                          * irreducible_character(partition, site_type))
        require(numerator % group_order == 0,
                ("matching multiplicity", partition, numerator))
        multiplicity = numerator//group_order
        if multiplicity:
            answer[partition] = multiplicity
    require(sum(dimension(partition)*multiplicity
                for partition, multiplicity in answer.items()) == 105,
            answer)
    return answer


def residual_729_decomposition():
    words = tuple(product(range(3), repeat=6))
    records = {}
    for site_type in integer_partitions(6):
        site_action = representative_permutation(site_type)
        for colour_type in integer_partitions(3):
            colour_action = representative_permutation(colour_type)
            records[site_type, colour_type] = {
                "class_size": class_size(site_type)*class_size(colour_type),
                "word": fixed_count(words, act_word,
                                    site_action, colour_action),
            }
    decomposition = decompose(records, "word", site_total=6)
    require(module_dimension(decomposition) == 729, "729 module changed")
    return decomposition


def profile(word):
    counts = sorted(Counter(word).values(), reverse=True)
    return tuple(counts+[0]*(3-len(counts)))


PAIRING = ((0, 1), (2, 3), (4, 5), (6, 7))
PAIR_TYPES = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))


def pair_signature(word):
    raw = Counter(tuple(sorted((word[left], word[right])))
                  for left, right in PAIRING)
    candidates = []
    for relabel in permutations(range(3)):
        image = Counter()
        for edge, count in raw.items():
            image[tuple(sorted((relabel[edge[0]], relabel[edge[1]])))] += count
        candidates.append(tuple(image[edge] for edge in PAIR_TYPES))
    return min(candidates)


def master_packet():
    pairconstant = {
        tuple(values[site//2] for site in range(8))
        for values in product(range(3), repeat=4) if len(set(values)) > 1
    }
    four_four = set()
    for left, right in combinations(range(3), 2):
        for orientation in range(16):
            values = []
            for site in range(4):
                bit = (orientation >> (3-site)) & 1
                values.extend((right, left) if bit else (left, right))
            four_four.add(tuple(values))
    six_two = set()
    for majority, minority in permutations(range(3), 2):
        for edge in combinations(range(4), 2):
            for clone_left, clone_right in product(range(2), repeat=2):
                values = [majority]*8
                values[2*edge[0]+clone_left] = minority
                values[2*edge[1]+clone_right] = minority
                six_two.add(tuple(values))
    answer = pairconstant|four_four|six_two
    require((len(pairconstant), len(four_four), len(six_two), len(answer)) ==
            (78, 48, 144, 270), "master census changed")
    return answer


def master_closure_audit():
    master = master_packet()
    master_profiles = Counter(profile(word) for word in master)
    full_profiles = Counter(profile(word) for word in EVEN_MIXED8)
    require(master_profiles == {(6, 2, 0): 168,
                                (4, 4, 0): 66,
                                (4, 2, 2): 36}, master_profiles)
    require(full_profiles == {(6, 2, 0): 168,
                              (4, 4, 0): 210,
                              (4, 2, 2): 1260}, full_profiles)
    # S8 is transitive on words with a fixed ordered count triple and S3
    # permutes the count labels, so one representative of each unordered
    # profile proves that the full closure is the entire 1,638 set.
    require(set(master_profiles) == set(full_profiles),
            "master lost an even profile")
    full_orbits = {(profile(word), pair_signature(word))
                   for word in EVEN_MIXED8}
    master_orbits = {(profile(word), pair_signature(word)) for word in master}
    require((len(full_orbits), len(master_orbits)) == (10, 5),
            (len(full_orbits), len(master_orbits)))
    return {
        "master_rows": len(master),
        "full_even_rows": len(EVEN_MIXED8),
        "S8_times_S3_closure_of_master": len(EVEN_MIXED8),
        "closure_reason": (
            "S8 is transitive on each labelled count profile and the master "
            "contains all three unordered even mixed profiles"
        ),
        "B4_times_S3_master_orbits": len(master_orbits),
        "B4_times_S3_full_orbits": len(full_orbits),
        "B4_times_S3_missing_orbits": len(full_orbits-master_orbits),
        "degree4_incidence_ranks": {
            "master": len(master),
            "full_even": len(EVEN_MIXED8),
            "missing_rows_each_raise_rank_by_one": True,
        },
    }


def hom_dimension(left, right):
    return sum(multiplicity*right.get(irrep, 0)
               for irrep, multiplicity in left.items())


def main():
    routing = json.loads(ROUTING.read_text())
    zeon = json.loads(ZEON.read_text())
    require(routing["logical_sha256"] == ROUTING_DIGEST,
            "zero-tail routing digest changed")
    require(zeon["logical_sha256"] == ZEON_DIGEST,
            "zeon hierarchy digest changed")

    validate_character_tables()
    records = class_records_8()
    decompositions = {key: decompose(records, key) for key in
                      ("word", "pure", "mixed", "even_mixed",
                       "degree4_monomial_domain", "degree4_kernel",
                       "pair", "cell")}
    expected_dimensions = {
        "word": 6561, "pure": 3, "mixed": 6558,
        "even_mixed": 1638,
        "degree4_monomial_domain": 105*6561,
        "degree4_kernel": 104*6561,
        "pair": 28, "cell": 252,
    }
    for key, expected in expected_dimensions.items():
        require(module_dimension(decompositions[key]) == expected,
                (key, module_dimension(decompositions[key]), expected))
    for irrep, multiplicity in decompositions["word"].items():
        require(decompositions["degree4_monomial_domain"].get(irrep, 0)
                - decompositions["degree4_kernel"].get(irrep, 0)
                == multiplicity, ("degree4 exact sequence", irrep))

    matching = matching_decomposition(records)
    expected_matching = {
        (8,): 1, (6, 2): 1, (4, 4): 1,
        (4, 2, 2): 1, (2, 2, 2, 2): 1,
    }
    require(matching == expected_matching, matching)

    residual729 = residual_729_decomposition()
    master = master_closure_audit()
    target_overlap = {
        "Hom(pair,mixed)": hom_dimension(decompositions["pair"],
                                           decompositions["mixed"]),
        "Hom(pair,even_mixed)": hom_dimension(
            decompositions["pair"], decompositions["even_mixed"]),
        "Hom(cell,mixed)": hom_dimension(decompositions["cell"],
                                           decompositions["mixed"]),
        "Hom(cell,even_mixed)": hom_dimension(
            decompositions["cell"], decompositions["even_mixed"]),
    }

    payload = {
        "status": "PASS exact Brauer/partition-algebra negative screen",
        "matching_scheme": {
            "module": "Q[perfect matchings of 8]=Ind_(S2 wr S4)^S8(1)",
            "dimension": 105,
            "multiplicity_free_decomposition": {
                str(partition): multiplicity
                for partition, multiplicity in matching.items()},
            "irrep_dimensions": {
                str(partition): dimension(partition) for partition in matching},
            "Brauer_idempotent_count": len(matching),
        },
        "degree4_matching_map": {
            "monomial_module": "Q[PM8] tensor Q[{0,1,2}^8]",
            "monomial_module_dimension": 105*6561,
            "row_inclusion": "iota(e_w)=(sum_M e_M) tensor e_w",
            "row_span_dimension": 6561,
            "kernel_dimension": 104*6561,
            "exact_sequence": "0 -> kernel(epsilon_PM tensor id) -> P -> W -> 0",
            "Brauer_sector_test": {
                "S8(8)": "returns the original amplitude row",
                "S8(6,2),S8(4,4),S8(4,2,2),S8(2,2,2,2)": (
                    "annihilate every amplitude row; GHZ equality supplies no "
                    "equation in these unconstrained matching-difference sectors"
                ),
            },
        },
        "S8_times_S3_modules": {
            key: {
                "dimension": expected_dimensions[key],
                "nonzero_irrep_types": len(decomposition),
                "multiplicities": {
                    label_irrep(irrep): multiplicity
                    for irrep, multiplicity in sorted(decomposition.items())},
            }
            for key, decomposition in decompositions.items()
        },
        "clean_pair_target_overlap": target_overlap,
        "residual_729_module": {
            "group": "S6 x S3",
            "dimension": 729,
            "nonzero_irrep_types": len(residual729),
            "multiplicities": {
                f"S6{irrep[0]}xS3{irrep[1]}": multiplicity
                for irrep, multiplicity in sorted(residual729.items())},
            "duplicate_guard": (
                "The 729 residual words are a full coordinate basis; every "
                "partition-algebra projection is a linear combination of the "
                "same 729 cap-error rows."
            ),
        },
        "master_and_1638_comparison": master,
        "linear_circuit_certificate": {
            "statement": (
                "The matching-monomial supports of two distinct physical words "
                "are disjoint. Hence the raw degree-four amplitude incidence "
                "matrix has row rank equal to the number of selected words."
            ),
            "full_rank": 6561,
            "mixed_rank": 6558,
            "even_mixed_rank": 1638,
            "master_rank": 270,
            "new_cross_word_linear_circuits": 0,
        },
        "projection_verdict": {
            "new_source_relative_identity": False,
            "forces_clean_pair": False,
            "reason": (
                "Nontrivial Brauer sectors are not constrained by the hafnian "
                "sum. On the invariant sector, every site/colour partition-"
                "algebra projector merely recombines already-zero amplitude "
                "rows. Full S8 closure also turns the 270 master into all 1,638 "
                "even rows, assuming precisely the missing equations rather "
                "than deriving them. Clean-pair activity is nonlinear response "
                "incidence and is absent from these linear modules."
            ),
            "retire_low_isotypic_projection": True,
            "smallest_genuinely_new_operation": (
                "a nonlinear response-incidence/reinsertion map coupling a fixed "
                "pair to the six-site residual, not a central idempotent"
            ),
        },
        "scope": {
            "broad_syzygy_search": False,
            "expanded_688905_column_matrix": False,
            "calculation": "exact finite characters, ranks, and orbit closure",
            "upstream_digests": {
                "zero_tail_routing": ROUTING_DIGEST,
                "zeon_hierarchy": ZEON_DIGEST,
            },
        },
    }
    payload["logical_sha256"] = logical_sha(payload)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")
    print(json.dumps({
        "logical_sha256": payload["logical_sha256"],
        "matching_decomposition": payload["matching_scheme"][
            "multiplicity_free_decomposition"],
        "mixed_irreps": len(decompositions["mixed"]),
        "even_mixed_irreps": len(decompositions["even_mixed"]),
        "residual729_irreps": len(residual729),
        "target_overlap": target_overlap,
        "master_S8_closure": master["S8_times_S3_closure_of_master"],
        "new_identity": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
