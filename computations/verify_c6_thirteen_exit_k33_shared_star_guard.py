#!/usr/bin/env python3
"""Exact shared-star audit of the minimum thirteen-exit hard core.

The signed degree-four C6 parent chain has thirteen matching exits.  This
checker classifies its minimum two- and three-channel cancellation supports.
Every singleton-free two-channel support has an active clean cap.  Among
tail-free three-channel supports the first exception is a K3,3 support.

An explicit all-nonzero 3x3 weight matrix on that K3,3 has permanent zero
and every 2x2 permanental cofactor nonzero.  It therefore gives four exact
mixed rows, obeys every literal shared-star rank identity, and has no active
clean cap.  It is not a full GHZ source: all three pure rows are absent, and
all 15^3 minimum pure-witness completions expose a mixed singleton.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_c6_unspecialized_eqsystem_parent_antidiagonal_spair.py":
        "584c36d076224fcc437b70998a43091ffa0f19b35bfbe73fea0caf1d7ae9865a",
    "notes/2026-08-14-c6-unspecialized-eqsystem-parent-antidiagonal-spair.md":
        "b15dd110cf28826751e5f32e162c91c7990cf119ed4a1c0361403dcf4ad0a369",
    "computations/verify_n8_common_edge_dirty_signature_realization_no_go.py":
        "3ec852cc796040e29189f72ecc02152cd43db7cee1abfd7aad636ea41fe16530",
    "notes/2026-08-14-n8-common-edge-dirty-signature-realization-no-go.md":
        "1dc67039e32eaa0087f59a80b99adc89f306b3a0d5ef2e5662baa10d1af66427",
}

N = 6
COLOURS = tuple(range(3))
SITES = tuple(range(N))
EDGES = tuple(combinations(SITES, 2))
WORDS = tuple(product(COLOURS, repeat=N))
WORD_SECTIONS = (
    (1, 1, 1, 0, 0, 1),
    (1, 1, 1, 2, 2, 1),
)
MAJORITY = frozenset((0, 1, 2, 5))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


MATCHINGS = tuple(sorted(perfect_matchings(SITES)))
M0 = tuple(sorted(((0, 5), (1, 2), (3, 4))))
M1 = tuple(sorted(((0, 1), (2, 5), (3, 4))))
EXITS = tuple(matching for matching in MATCHINGS if matching not in (M0, M1))
CAP_COMPLEMENT = tuple(sorted(((0, 2), (1, 5), (3, 4))))

# This is one parity class of the six perfect matchings of the K3,3 with
# shores {0,1,5}|{2,3,4}.  Its edge union automatically supports the other
# parity class as well.
K33_FACTORS = (
    tuple(sorted(((0, 2), (1, 3), (4, 5)))),
    tuple(sorted(((0, 3), (1, 4), (2, 5)))),
    tuple(sorted(((0, 4), (1, 2), (3, 5)))),
)
K33_LEFT = (0, 1, 5)
K33_RIGHT = (2, 3, 4)


def matching_name(matching):
    return "|".join(f"{left}{right}" for left, right in matching)


def word_name(word):
    return "".join(map(str, word))


def occurrence_cells(matching, word):
    return tuple((left, right, word[left], word[right])
                 for left, right in matching)


def cell_name(cell):
    left, right, alpha, beta = cell
    return f"{left}{right};{alpha}{beta}"


def matching_triangles(matchings):
    edges = set().union(*(set(matching) for matching in matchings))
    return tuple(vertices for vertices in combinations(SITES, 3)
                 if all(tuple(sorted(edge)) in edges
                        for edge in combinations(vertices, 2)))


def exit_classes():
    classes = defaultdict(list)
    for matching in EXITS:
        common0 = set(matching) & set(M0)
        common1 = set(matching) & set(M1)
        if (3, 4) in matching:
            label = "cap_complement"
        elif common0 and not common1:
            label = "one_tail_M0"
        elif common1 and not common0:
            label = "one_tail_M1"
        else:
            label = "transverse_C6"
        classes[label].append(matching)
    counts = {label: len(items) for label, items in sorted(classes.items())}
    require(counts == {
        "cap_complement": 1,
        "one_tail_M0": 4,
        "one_tail_M1": 4,
        "transverse_C6": 4,
    }, counts)
    require(classes["cap_complement"] == [CAP_COMPLEMENT], classes)

    independent = {}
    for size in range(2, 6):
        families = tuple(family for family in combinations(EXITS, size)
                         if all(not (set(left) & set(right))
                                for left, right in combinations(family, 2)))
        independent[size] = {
            "all_exit_families": len(families),
            "cap34_avoiding_families": sum(
                all((3, 4) not in matching for matching in family)
                for family in families
            ),
        }
    require(independent == {
        2: {"all_exit_families": 44, "cap34_avoiding_families": 36},
        3: {"all_exit_families": 48, "cap34_avoiding_families": 32},
        4: {"all_exit_families": 14, "cap34_avoiding_families": 6},
        5: {"all_exit_families": 2, "cap34_avoiding_families": 0},
    }, independent)
    return {"class_counts": counts, "tail_free_family_counts": independent}


def block_value(weights, left, right, alpha, beta):
    if left > right:
        left, right, alpha, beta = right, left, beta, alpha
    return weights.get((left, right, alpha, beta), Q(0))


def complete_rows(weights):
    answer = {}
    for word in WORDS:
        occurrences = []
        for matching in MATCHINGS:
            cells = occurrence_cells(matching, word)
            if not all(cell in weights for cell in cells):
                continue
            value = Q(1)
            for cell in cells:
                value *= weights[cell]
            occurrences.append((matching, value))
        answer[word] = tuple(occurrences)
    return answer


def canonical_family_weights(family, channel_values=None):
    """Put a constant channel value on one fixed all-1 edge per factor."""
    if channel_values is None:
        channel_values = tuple([Q(1)] * (len(family) - 1)
                               + [Q(1 - len(family))])
    require(len(channel_values) == len(family)
            and sum(channel_values, Q(0)) == 0, channel_values)
    weights = {}
    for matching in family:
        for word in WORD_SECTIONS:
            for cell in occurrence_cells(matching, word):
                weights[cell] = Q(1)
    for matching, value in zip(family, channel_values, strict=True):
        fixed_edges = tuple(edge for edge in matching
                            if set(edge) <= MAJORITY)
        require(fixed_edges, matching)
        edge = fixed_edges[0]
        weights[(edge[0], edge[1], 1, 1)] = value
    return weights


def balanced_pair_weights(first, second):
    """Realize values +1,-1 in every word where both fines occur."""
    weights = {}
    for matching in (first, second):
        for word in WORD_SECTIONS:
            for cell in occurrence_cells(matching, word):
                weights[cell] = Q(1)
    exclusive = next(edge for edge in second if edge not in first)
    for word in WORD_SECTIONS:
        left, right = exclusive
        weights[(left, right, word[left], word[right])] = Q(-1)
    return weights


def cap_scalar(weights, cap, covector):
    left, right = cap
    return sum(covector[alpha][beta]
               * block_value(weights, left, right, alpha, beta)
               for alpha, beta in product(COLOURS, repeat=2))


def response(weights, cap, covector):
    p, q = cap
    residual = tuple(site for site in SITES if site not in cap)
    answer = {}
    for a, b in combinations(residual, 2):
        for alpha, beta in product(COLOURS, repeat=2):
            value = sum(
                covector[i][j] * (
                    block_value(weights, p, a, i, alpha)
                    * block_value(weights, q, b, j, beta)
                    + block_value(weights, p, b, i, beta)
                    * block_value(weights, q, a, j, alpha)
                )
                for i, j in product(COLOURS, repeat=2)
            )
            if value:
                answer[(a, b, alpha, beta)] = value
    return residual, answer


def response_square_zero(residual, response_cells):
    for word_colours in product(COLOURS, repeat=4):
        word = dict(zip(residual, word_colours, strict=True))
        coefficient = Q(0)
        for matching in perfect_matchings(residual):
            product_value = Q(1)
            for left, right in matching:
                product_value *= response_cells.get(
                    (left, right, word[left], word[right]), Q(0)
                )
            coefficient += product_value
        if coefficient:
            return False
    return True


def active_covector(weights, cap):
    covector = [[Q(int(left == right)) for right in COLOURS]
                for left in COLOURS]
    scalar = cap_scalar(weights, cap, covector)
    if not scalar:
        direct = next(((alpha, beta, value)
                       for alpha, beta in product(COLOURS, repeat=2)
                       if (value := block_value(weights, *cap, alpha, beta))),
                      None)
        require(direct is not None, (cap, weights))
        alpha, beta, _ = direct
        covector[alpha][beta] += 1
        scalar = cap_scalar(weights, cap, covector)
    require(scalar and all(covector[colour][colour]
                           for colour in COLOURS), (cap, covector, scalar))
    return tuple(tuple(row) for row in covector), scalar


def two_channel_census():
    histogram = Counter()
    examples = {}
    for first, second in combinations(EXITS, 2):
        weights = balanced_pair_weights(first, second)
        rows = complete_rows(weights)
        mixed_singletons = tuple(word for word, occurrences in rows.items()
                                 if len(set(word)) > 1
                                 and len(occurrences) == 1)
        for word, occurrences in rows.items():
            if len(set(word)) > 1 and len(occurrences) == 2:
                require(sum(value for _, value in occurrences) == 0,
                        (first, second, word, occurrences))
        common_tail = tuple(sorted(set(first) & set(second)))
        if mixed_singletons:
            outcome = "mixed_singleton"
            require(len(mixed_singletons) == 2, (first, second,
                                                  mixed_singletons))
        else:
            if common_tail:
                cap = common_tail[0]
            else:
                require((3, 4) not in first and (3, 4) not in second,
                        (first, second))
                cap = next(edge for edge in first if set(edge) <= MAJORITY)
            covector, scalar = active_covector(weights, cap)
            residual, cap_response = response(weights, cap, covector)
            require(response_square_zero(residual, cap_response),
                    (first, second, cap, cap_response))
            outcome = "active_clean_cap"
            examples.setdefault(outcome, {
                "family": (matching_name(first), matching_name(second)),
                "cap": f"{cap[0]}{cap[1]}",
                "s": str(scalar),
            })
        histogram[("common_tail" if common_tail else "disjoint", outcome)] += 1
    require(histogram == Counter({
        ("common_tail", "active_clean_cap"): 30,
        ("common_tail", "mixed_singleton"): 4,
        ("disjoint", "active_clean_cap"): 36,
        ("disjoint", "mixed_singleton"): 8,
    }), histogram)
    return {
        "all_unordered_exit_pairs": sum(histogram.values()),
        "classification": {f"{geometry}:{outcome}": count
                           for (geometry, outcome), count
                           in sorted(histogram.items())},
        "verdict": "every two-exit packet has a singleton or active clean cap",
        "clean_example": examples["active_clean_cap"],
    }


def three_channel_geometry():
    families = tuple(family for family in combinations(EXITS, 3)
                     if all(not (set(left) & set(right))
                            for left, right in combinations(family, 2))
                     and all((3, 4) not in matching for matching in family))
    prism = tuple(family for family in families if matching_triangles(family))
    k33 = tuple(family for family in families if not matching_triangles(family))
    require((len(families), len(prism), len(k33)) == (32, 24, 8),
            (len(families), len(prism), len(k33)))

    # For every prism, some occupied cap has response support of matching
    # number at most one, hence an exact clean cap for the canonical weights.
    clean_prisms = 0
    for family in prism:
        weights = canonical_family_weights(family)
        found = False
        for cap in set().union(*(set(matching) for matching in family)):
            covector, _ = active_covector(weights, cap)
            residual, cap_response = response(weights, cap, covector)
            if response_square_zero(residual, cap_response):
                found = True
                break
        require(found, family)
        clean_prisms += 1

    edge_supports = {
        frozenset().union(*(frozenset(matching) for matching in family))
        for family in k33
    }
    require(len(edge_supports) == 4, edge_supports)

    # The word-section stabilizer S4 x S2 is transitive on the eight
    # parity-labelled K3,3 factor triples.
    representative = k33[0]
    orbit = set()
    for majority_permutation in permutations(tuple(MAJORITY)):
        for cap_permutation in permutations((3, 4)):
            relabel = dict(zip(tuple(MAJORITY), majority_permutation,
                               strict=True))
            relabel.update(zip((3, 4), cap_permutation, strict=True))
            image = tuple(sorted(
                tuple(sorted(tuple(sorted((relabel[left], relabel[right])))
                             for left, right in matching))
                for matching in representative
            ))
            if image in k33:
                orbit.add(image)
    require(orbit == set(k33), (len(orbit), len(k33)))
    return {
        "tail_free_cap34_avoiding_triples": len(families),
        "triangular_prism": {
            "count": len(prism),
            "active_clean_for_canonical_physical_weights": clean_prisms,
        },
        "K3,3": {
            "parity_factor_triples": len(k33),
            "distinct_edge_supports": len(edge_supports),
            "one_orbit_under_word_section_stabilizer": True,
            "status": "first support geometry not forced clean",
        },
    }


def determinant3(matrix):
    answer = Q(0)
    for permutation in permutations(COLOURS):
        inversions = sum(permutation[left] > permutation[right]
                         for left in COLOURS
                         for right in range(left + 1, 3))
        term = Q(-1 if inversions % 2 else 1)
        for row in COLOURS:
            term *= matrix[row][permutation[row]]
        answer += term
    return answer


def matrix_rank(matrix):
    rows = [list(map(Q, row)) for row in matrix]
    rank = 0
    for column in range(3):
        pivot = next((row for row in range(rank, 3)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [entry / scale for entry in rows[rank]]
        for row in range(3):
            if row == rank or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [entry - scale * pivot_entry
                         for entry, pivot_entry in
                         zip(rows[row], rows[rank], strict=True)]
        rank += 1
    return rank


def permanent(matrix):
    return sum((matrix[0][permutation[0]]
                * matrix[1][permutation[1]]
                * matrix[2][permutation[2]])
               for permutation in permutations(COLOURS))


def permanent2(matrix, deleted_row, deleted_column):
    rows = tuple(row for row in COLOURS if row != deleted_row)
    columns = tuple(column for column in COLOURS if column != deleted_column)
    return (matrix[rows[0]][columns[0]] * matrix[rows[1]][columns[1]]
            + matrix[rows[0]][columns[1]] * matrix[rows[1]][columns[0]])


def k33_guard():
    matrix = (
        (Q(1), Q(1), Q(1)),
        (Q(-2), Q(1), Q(1)),
        (Q(1), Q(1), Q(1)),
    )
    require(permanent(matrix) == 0, permanent(matrix))
    cofactors = tuple(permanent2(matrix, row, column)
                      for row in COLOURS for column in COLOURS)
    require(all(cofactors), cofactors)

    weights = {}
    for row, left in enumerate(K33_LEFT):
        for column, right in enumerate(K33_RIGHT):
            edge = tuple(sorted((left, right)))
            for word in WORD_SECTIONS:
                a, b = edge
                weights[(a, b, word[a], word[b])] = matrix[row][column]
    require(len(weights) == 15, weights)

    rows = complete_rows(weights)
    live = tuple((word, occurrences) for word, occurrences in rows.items()
                 if occurrences)
    require(tuple(word for word, _ in live) == (
        (1, 1, 1, 0, 0, 1),
        (1, 1, 1, 0, 2, 1),
        (1, 1, 1, 2, 0, 1),
        (1, 1, 1, 2, 2, 1),
    ), tuple(word_name(word) for word, _ in live))
    for word, occurrences in live:
        require(len(occurrences) == 6, (word, occurrences))
        require(sum(value for _, value in occurrences) == 0,
                (word, occurrences))
        require(all((0, 1) not in matching and (3, 4) not in matching
                    for matching, _ in occurrences), occurrences)
        # Every exit sign in the a01 deletion relation is +1 here, so the
        # signed exit sum is the same zero permanent.
        require(sum(value for _, value in occurrences) == 0,
                ("signed exit sum", word, occurrences))

    pure_failures = tuple(word_name(word) for word in WORDS
                          if len(set(word)) == 1 and not rows[word])
    require(pure_failures == ("000000", "111111", "222222"),
            pure_failures)

    # Literal shared-star audit: every response slice is a sum of two
    # rank-one 3x3 matrices and hence has rank <=2/determinant zero.
    slice_ranks = Counter()
    for cap in EDGES:
        residual = tuple(site for site in SITES if site not in cap)
        p, q = cap
        for a, b in combinations(residual, 2):
            for alpha, beta in product(COLOURS, repeat=2):
                response_slice = tuple(tuple(
                    block_value(weights, p, a, i, alpha)
                    * block_value(weights, q, b, j, beta)
                    + block_value(weights, p, b, i, beta)
                    * block_value(weights, q, a, j, alpha)
                    for j in COLOURS) for i in COLOURS)
                require(determinant3(response_slice) == 0,
                        (cap, a, b, alpha, beta, response_slice))
                slice_ranks[matrix_rank(response_slice)] += 1
    require(sum(slice_ranks.values()) == 15 * 6 * 9, slice_ranks)

    # No active clean cap.  An absent direct edge has s=0.  At an occupied
    # K3,3 edge, the four star products form the complementary K2,2.  Its
    # clean error is a nonzero 2x2 permanent cofactor times s^2.
    occupied = set((tuple(sorted((left, right))))
                   for left in K33_LEFT for right in K33_RIGHT)
    cap_records = []
    for cap in EDGES:
        if cap not in occupied:
            require(all(not block_value(weights, *cap, alpha, beta)
                        for alpha, beta in product(COLOURS, repeat=2)), cap)
            cap_records.append({"cap": f"{cap[0]}{cap[1]}",
                                "status": "inactive:s=0"})
            continue
        left = next(site for site in cap if site in K33_LEFT)
        right = next(site for site in cap if site in K33_RIGHT)
        row = K33_LEFT.index(left)
        column = K33_RIGHT.index(right)
        cofactor = permanent2(matrix, row, column)
        require(cofactor, (cap, cofactor))
        cap_records.append({
            "cap": f"{cap[0]}{cap[1]}",
            "status": "active_implies_dirty",
            "direct_weight": str(matrix[row][column]),
            "complementary_K2,2_permanent": str(cofactor),
            "clean_error": (
                "nonzero scalar times s(K)^2; shared-star K2,2 response"
            ),
        })
    require(Counter(record["status"] for record in cap_records) ==
            Counter({"active_implies_dirty": 9, "inactive:s=0": 6}),
            cap_records)

    return {
        "shores": (K33_LEFT, K33_RIGHT),
        "weight_matrix": tuple(tuple(map(str, row)) for row in matrix),
        "permanent": "0",
        "all_nine_permanental_cofactors_nonzero": tuple(map(str, cofactors)),
        "decorated_support_cells": tuple(sorted(map(cell_name, weights))),
        "decorated_support_size": len(weights),
        "live_mixed_rows": tuple(word_name(word) for word, _ in live),
        "occurrences_per_live_row": 6,
        "all_live_mixed_rows_exact": True,
        "signed_thirteen_exit_sum": "0 (all six live fines have sign +)",
        "shared_star_slice_rank_histogram": dict(sorted(slice_ranks.items())),
        "cap_records": tuple(cap_records),
        "active_clean_cap_exists": False,
        "pure_row_failures": pure_failures,
        "permanent_triangle_warning": (
            "both parity classes are already live in the same six-term rows; "
            "the three private binomial hypotheses of 90e5faf are absent"
        ),
        "weights": weights,
    }


def support_mask_inventory():
    cell_index = {
        (edge, alpha, beta): index
        for index, (edge, alpha, beta) in enumerate(
            (edge, alpha, beta)
            for edge in EDGES
            for alpha, beta in product(COLOURS, repeat=2)
        )
    }

    def occurrence_mask(matching, word):
        answer = 0
        for left, right in matching:
            answer |= 1 << cell_index[((left, right), word[left], word[right])]
        return answer

    mixed_words = tuple(word for word in WORDS if len(set(word)) > 1)
    mixed_occurrences = {
        word: tuple(occurrence_mask(matching, word) for matching in MATCHINGS)
        for word in mixed_words
    }
    pure = tuple(tuple(occurrence_mask(matching, (colour,) * N)
                       for matching in MATCHINGS)
                 for colour in COLOURS)
    return occurrence_mask, mixed_occurrences, pure


def pure_completion_census(guard_weights):
    occurrence_mask, mixed_occurrences, pure = support_mask_inventory()
    base = 0
    for cell in guard_weights:
        left, right, alpha, beta = cell
        # Reconstruct the same deterministic index used above.
        edge_position = EDGES.index((left, right))
        index = 9 * edge_position + 3 * alpha + beta
        base |= 1 << index
    require(base.bit_count() == 15, base.bit_count())

    singleton_histogram = Counter()
    support_size_histogram = Counter()
    first_singleton_histogram = Counter()
    for first, second, third in product(range(15), repeat=3):
        support = base | pure[0][first] | pure[1][second] | pure[2][third]
        support_size_histogram[support.bit_count()] += 1
        singleton_count = 0
        first_word = None
        for word, occurrence_masks in mixed_occurrences.items():
            multiplicity = sum((mask & support) == mask
                               for mask in occurrence_masks)
            if multiplicity == 1:
                singleton_count += 1
                if first_word is None:
                    first_word = word_name(word)
        require(singleton_count and first_word is not None,
                (first, second, third, support.bit_count()))
        singleton_histogram[singleton_count] += 1
        first_singleton_histogram[first_word] += 1

    require(sum(singleton_histogram.values()) == 15 ** 3,
            singleton_histogram)
    require(min(singleton_histogram) == 10, singleton_histogram)
    require(support_size_histogram == Counter({23: 2025, 24: 1350}),
            support_size_histogram)
    expected_singleton_histogram = Counter({
        10: 66, 11: 192, 12: 84, 13: 324, 14: 288, 15: 264,
        16: 210, 17: 180, 18: 243, 19: 204, 20: 246, 21: 96,
        22: 102, 23: 180, 24: 210, 25: 48, 26: 96, 27: 72,
        28: 18, 29: 24, 30: 102, 31: 24, 32: 24, 33: 24,
        36: 18, 38: 12, 40: 12, 42: 6, 48: 6,
    })
    require(singleton_histogram == expected_singleton_histogram,
            singleton_histogram)
    return {
        "pure_witness_triples_tested": 15 ** 3,
        "support_size_histogram": dict(sorted(support_size_histogram.items())),
        "mixed_singleton_count_histogram":
            dict(sorted(singleton_histogram.items())),
        "minimum_mixed_singletons": min(singleton_histogram),
        "singleton_free_completions": 0,
        "first_singleton_word_histogram":
            dict(sorted(first_singleton_histogram.items())),
        "meaning": (
            "every one-witness-per-colour support completion has a literal "
            "mixed singleton; a larger source must add at least one mate"
        ),
    }


def build_ledger():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    guard = k33_guard()
    weights = guard.pop("weights")
    return {
        "theorem": "C6 thirteen-exit shared-star K3,3 gate",
        "pins": PINS,
        "exit_matching_geometry": exit_classes(),
        "minimum_two_channel_classification": two_channel_census(),
        "tail_free_three_channel_classification": three_channel_geometry(),
        "minimum_literal_no_clean_guard": guard,
        "pure_normalization_gate": pure_completion_census(weights),
        "verdict": (
            "two exits always give a singleton or active clean cap; the "
            "smallest shared-star-valid no-clean cancellation support is a "
            "15-cell K3,3 permanent-zero guard.  It is not a full-source "
            "counterexample: all pure rows fail, and every minimum pure "
            "completion creates mixed singleton debt.  Recursive mate "
            "closure is the remaining hypothesis."
        ),
    }


EXPECTED_LEDGER_SHA256 = (
    "d20758f5c1b8a571f523e074f88f0b6037d29389e86fd6a89d3bb57c1f7b0d03"
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    parser.add_argument("--dump-ledger", action="store_true")
    arguments = parser.parse_args()
    ledger = build_ledger()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256:
        require(digest == EXPECTED_LEDGER_SHA256,
                ("K3,3 exit ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    if arguments.dump_ledger:
        print(json.dumps(ledger, indent=2, sort_keys=True))
    print("C6 thirteen-exit K3,3 shared-star guard: PASS")
    print("mode", arguments.mode)
    print("ledger_sha256", digest)
    print("two-channel exit packets: 12 singleton, 66 active-clean")
    print("first no-clean geometry: 15-cell K3,3 permanent-zero guard")
    print("minimum pure completions: 3375 tested, all have singleton debt")


if __name__ == "__main__":
    main()
