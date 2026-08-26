#!/usr/bin/env python3
"""Exact factored census of the smallest orbit-zero K14 membership block."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
from itertools import product


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OLD = ROOT / "computations/unaudited-codex-n8-orbit0-t2-graded-2026-08-20"
AUDIT_PATH = OLD / "audit_orbit0_chart_target_anchor_telescoping.py"
SPEC = importlib.util.spec_from_file_location("k14_frozen", AUDIT_PATH)
FROZEN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FROZEN)
OUT = HERE / "results_orbit0_k14_interface.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def divides(row, divisor):
    remaining = Counter(row)
    remaining.subtract(divisor)
    return all(value >= 0 for value in remaining.values())


def build_interface():
    raw = json.loads(FROZEN.R8P.read_text())
    residual = Counter({bytes.fromhex(row): Fraction(numerator, denominator)
                        for row, numerator, denominator in raw["residual"]})
    words = tuple(FROZEN.word_from_pair_colours(colours)
                  for colours in FROZEN.PAIR_COLOURS)
    terms = tuple(FROZEN.BASE.word_terms(word) for word in words)
    anchor_terms = tuple(FROZEN.BASE.term_ids(word, FROZEN.M0)
                         for word in words)
    leading_errors = []
    for matching_terms, anchor_term in zip(terms, anchor_terms, strict=True):
        leading_errors.append(Counter({
            term: 1 for term in matching_terms
            if term != anchor_term and FROZEN.row_k_degree(term) == 2
        }))
    require(tuple(map(len, leading_errors)) == (12, 12, 12),
            tuple(map(len, leading_errors)))
    leading_packet = FROZEN.polynomial_product(
        FROZEN.polynomial_product(leading_errors[0], leading_errors[1]),
        leading_errors[2],
    )
    require(len(leading_packet) == 1728, len(leading_packet))
    factor_set = frozenset(anchor_terms)
    factor_stabilizer = tuple(
        action for action in range(len(FROZEN.EXPORT.STABILIZER))
        if frozenset(FROZEN.move_row(term, action) for term in anchor_terms)
        == factor_set
    )
    require(len(factor_stabilizer) == 384, len(factor_stabilizer))

    # Orbit0 has all 3^4-3=78 nonconstant pair-colour words as K0 mixed
    # generators, not only the three factors used to manufacture the K14
    # telescoping identity. Every such row has one unique K0 anchor term and
    # no K1 term, so it is an independent unary gr14 pivot whenever it divides
    # a target monomial.
    all_mixed_anchor_terms = []
    all_mixed_anchor_words = []
    all_mixed_k2_terms = []
    for pair_colours in product(range(3), repeat=4):
        if len(set(pair_colours)) == 1:
            continue
        word = FROZEN.word_from_pair_colours(pair_colours)
        matching_terms = FROZEN.BASE.word_terms(word)
        anchor_term = FROZEN.BASE.term_ids(word, FROZEN.M0)
        profile = Counter(FROZEN.row_k_degree(term)
                          for term in matching_terms)
        require(profile[0] == 1 and profile.get(1, 0) == 0
                and tuple(term for term in matching_terms
                          if FROZEN.row_k_degree(term) == 0) == (anchor_term,),
                (pair_colours, profile))
        all_mixed_anchor_words.append(pair_colours)
        all_mixed_anchor_terms.append(anchor_term)
        all_mixed_k2_terms.append(tuple(
            term for term in matching_terms
            if FROZEN.row_k_degree(term) == 2
        ))
    require(len(set(all_mixed_anchor_terms)) == 78,
            len(set(all_mixed_anchor_terms)))
    require(set(map(len, all_mixed_k2_terms)) == {12},
            set(map(len, all_mixed_k2_terms)))
    anchor_cell_order = tuple(sorted(FROZEN.A))
    mixed_anchor_vectors = tuple(
        tuple(Counter(term)[cell] for cell in anchor_cell_order)
        for term in all_mixed_anchor_terms
    )
    pivot_cache = {}

    def pivots_for_signature(signature):
        if signature not in pivot_cache:
            pivot_cache[signature] = tuple(
                index for index, vector in enumerate(mixed_anchor_vectors)
                if all(left >= right
                       for left, right in zip(signature, vector, strict=True))
            )
        return pivot_cache[signature]

    # Split the 120 full-stabilizer R8' orbits into exact H-orbits, where H is
    # the factorization stabilizer.  This is the lossless 485-row factor side.
    r8_h_representatives = []
    r8_h_orbit_sizes = []
    for representative in residual:
        unseen = set(FROZEN.EXPORT.row_orbit(representative))
        while unseen:
            seed = min(unseen)
            orbit = FROZEN.orbit_under(seed, factor_stabilizer)
            require(orbit <= unseen, "H orbit crossed an R8 full orbit")
            r8_h_representatives.append(seed)
            r8_h_orbit_sizes.append(len(orbit))
            unseen.difference_update(orbit)
    require(len(r8_h_representatives) == 485, len(r8_h_representatives))

    relative_pairs = 0
    unary_pairs = 0
    survivor_pairs = 0
    survivor_rows = set()
    survivor_missing_profile = Counter()
    survivor_distinct_anchor_profile = Counter()
    hostile_degree = Counter()
    all78_unary_pairs = 0
    all78_survivor_pairs = 0
    all78_survivor_rows = set()
    all78_survivor_reason = Counter()
    all78_pivot_multiplicity = Counter()
    K14_anchor_signatures = Counter()
    for r8_row in r8_h_representatives:
        for packet_row in leading_packet:
            target = bytes(sorted(r8_row + packet_row))
            require(len(target) == 24 and FROZEN.row_k_degree(target) == 14,
                    "factored target left K14")
            relative_pairs += 1
            live_pivots = tuple(index for index, anchor_term
                                in enumerate(anchor_terms)
                                if divides(target, anchor_term))
            if live_pivots:
                unary_pairs += 1
            else:
                survivor_pairs += 1
                survivor_rows.add(target)
                multiplicity = Counter(target)
                missing = tuple(sorted(sum(multiplicity[cell] == 0
                                           for cell in anchor_term)
                                       for anchor_term in anchor_terms))
                survivor_missing_profile[missing] += 1
                distinct_anchor_profile = tuple(sorted(
                    sum(multiplicity[cell] > 0 for cell in anchor_term)
                    for anchor_term in anchor_terms
                ))
                survivor_distinct_anchor_profile[distinct_anchor_profile] += 1
                hostile_degree[sum(multiplicity[cell] for cell in FROZEN.A)] += 1

            multiplicity = Counter(target)
            anchor_signature = tuple(multiplicity[cell]
                                     for cell in anchor_cell_order)
            K14_anchor_signatures[anchor_signature] += 1
            all_pivots = pivots_for_signature(anchor_signature)
            all78_pivot_multiplicity[len(all_pivots)] += 1
            if all_pivots:
                all78_unary_pairs += 1
            else:
                all78_survivor_pairs += 1
                all78_survivor_rows.add(target)
                multiplicity = Counter(target)
                available_by_pair = []
                for left, right in FROZEN.M0:
                    available = tuple(colour for colour in range(3)
                                      if multiplicity[FROZEN.BASE.CELL_ID[
                                          (left, right, colour, colour)]] > 0)
                    available_by_pair.append(available)
                if any(not available for available in available_by_pair):
                    reason = "missing_physical_anchor_pair"
                else:
                    assignments = set(product(*available_by_pair))
                    require(assignments and all(len(set(row)) == 1
                                                for row in assignments),
                            (target.hex(), available_by_pair, assignments))
                    reason = "only_pure_pair_colour_assignment"
                all78_survivor_reason[reason] += 1

    require(relative_pairs == 485 * 1728 == 838080, relative_pairs)
    require(unary_pairs + survivor_pairs == relative_pairs,
            (unary_pairs, survivor_pairs, relative_pairs))
    require(all78_unary_pairs + all78_survivor_pairs == relative_pairs,
            (all78_unary_pairs, all78_survivor_pairs, relative_pairs))
    require(all78_survivor_pairs == 0, all78_survivor_pairs)

    # Profile the induced K16 tail on the finite anchor-signature quotient.
    # For each K14 signature, choose the pivot minimizing the number of its
    # twelve K2 tails that lack another mixed K0 anchor divisor. This does not
    # assert coefficient cancellation or full K16 membership; it isolates the
    # smallest exact anchor-support antichain before any polynomial expansion.
    K16_best_survivor_signatures = Counter()
    K16_best_survivor_tail_count = 0
    K16_universally_reducible_K14_signatures = 0
    K16_choice_profiles = Counter()
    for signature, occurrence_count in K14_anchor_signatures.items():
        candidates = []
        for pivot in pivots_for_signature(signature):
            base = tuple(left - right for left, right
                         in zip(signature, mixed_anchor_vectors[pivot], strict=True))
            survivors = []
            for tail in all_mixed_k2_terms[pivot]:
                tail_counts = Counter(tail)
                tail_vector = tuple(tail_counts[cell]
                                    for cell in anchor_cell_order)
                new_signature = tuple(left + right for left, right
                                      in zip(base, tail_vector, strict=True))
                require(sum(new_signature) == 8, new_signature)
                if not pivots_for_signature(new_signature):
                    survivors.append(new_signature)
            candidates.append((len(survivors), pivot, tuple(survivors)))
        require(candidates, signature)
        best_count, best_pivot, best_survivors = min(candidates)
        K16_choice_profiles[best_count] += 1
        if best_count == 0:
            K16_universally_reducible_K14_signatures += 1
        for survivor in best_survivors:
            K16_best_survivor_signatures[survivor] += occurrence_count
            K16_best_survivor_tail_count += occurrence_count

    anchor_position = {cell: index
                       for index, cell in enumerate(anchor_cell_order)}
    signature_permutations = []
    for action in factor_stabilizer:
        transform = FROZEN.EXPORT.TRANSFORMS[action]
        permutation = tuple(anchor_position[transform[cell]]
                            for cell in anchor_cell_order)
        require(len(set(permutation)) == 12, permutation)
        signature_permutations.append(permutation)

    def canonical_signature(signature):
        images = []
        for permutation in signature_permutations:
            moved = [0] * 12
            for old, new in enumerate(permutation):
                moved[new] = signature[old]
            images.append(tuple(moved))
        return min(images)

    K14_signature_orbits = Counter()
    for signature, count in K14_anchor_signatures.items():
        K14_signature_orbits[canonical_signature(signature)] += count
    K16_antichain_orbits = Counter()
    for signature, count in K16_best_survivor_signatures.items():
        K16_antichain_orbits[canonical_signature(signature)] += count
    return {
        "status": "PASS exact factored orbit-zero K14 interface audit",
        "frozen_interface": {
            "identity": "a*T belongs to I_mix + K^14",
            "leading_residual": "-R8prime*E0_2*E1_2*E2_2",
            "R8prime_full_orbits": 120,
            "R8prime_factor_stabilizer_orbits": len(r8_h_representatives),
            "leading_K6_labelled_terms": len(leading_packet),
            "leading_K6_factor_stabilizer_orbits": 22,
            "orbit0_K0_mixed_generators": len(all_mixed_anchor_terms),
            "factor_stabilizer_order": len(factor_stabilizer),
            "old_factored_orbit_pair_upper_bound": 10670,
        },
        "gr14_unary_source_compression": {
            "relative_factored_pairs_tested": relative_pairs,
            "unary_pairs": unary_pairs,
            "surviving_pairs": survivor_pairs,
            "distinct_surviving_relative_rows": len(survivor_rows),
            "unary_rule": (
                "If a K14 target monomial contains one selected K0 anchor "
                "term t_i, multiplication by target/t_i times the mixed "
                "generator H_i has that target as its unique gr_K^14 term; "
                "all E_i tails start two K-degrees later."
            ),
            "survivor_missing_anchor_profile": {
                str(key): value
                for key, value in sorted(survivor_missing_profile.items())
            },
            "survivor_distinct_anchor_profile": {
                str(key): value
                for key, value in sorted(survivor_distinct_anchor_profile.items())
            },
            "survivor_total_anchor_multiplicity": {
                str(key): value for key, value in sorted(hostile_degree.items())
            },
        },
        "all_78_K0_mixed_unary_compression": {
            "unary_pairs": all78_unary_pairs,
            "surviving_pairs": all78_survivor_pairs,
            "distinct_surviving_relative_rows": len(all78_survivor_rows),
            "survivor_reason": dict(sorted(all78_survivor_reason.items())),
            "pivot_multiplicity_histogram": {
                str(key): value
                for key, value in sorted(all78_pivot_multiplicity.items())
            },
            "source_faithful_rule": (
                "Every nonconstant colour assignment on the four M0 pairs "
                "is one of the 78 mixed generators and has a unique K0 "
                "anchor term, with no K1 terms. Divisibility therefore gives "
                "a literal singleton gr14 source column."
            ),
            "promoted_identity": "a*T belongs to I_mix + K^16",
            "promotion_guard": (
                "Subtracting target/t_w times H_w cancels K14. Every other "
                "term of H_w has K-degree at least two, so no K15 term is "
                "created; all new tails have K-degree at least 16."
            ),
            "hostile_mutation": (
                "Restricting the unary family back to the three mixed rows "
                "used in the telescoping identity leaves 582000 relative "
                "pairs, so the full 78-row source family is load-bearing."
            ),
        },
        "K16_anchor_signature_profile": {
            "K14_anchor_signatures": len(K14_anchor_signatures),
            "K14_anchor_signature_orbits_under_factor_stabilizer": len(
                K14_signature_orbits),
            "best_pivot_surviving_tail_count_histogram_per_signature": {
                str(key): value for key, value in sorted(K16_choice_profiles.items())
            },
            "K14_signatures_with_a_pivot_whose_all_K2_tails_are_reducible": (
                K16_universally_reducible_K14_signatures
            ),
            "minimal_K16_anchor_antichain_signatures": len(
                K16_best_survivor_signatures),
            "minimal_K16_anchor_antichain_orbits_under_factor_stabilizer": len(
                K16_antichain_orbits),
            "best_pivot_weighted_surviving_tail_occurrences": (
                K16_best_survivor_tail_count),
            "antichain_signature_occurrence_profile": {
                str(signature): count for signature, count
                in sorted(K16_best_survivor_signatures.items())
            },
            "antichain_orbit_representative_occurrence_profile": {
                str(signature): count for signature, count
                in sorted(K16_antichain_orbits.items())
            },
            "scope_guard": (
                "This optimizes the literal choice of one unary pivot on "
                "each finite anchor signature and tests only whether its K2 "
                "tails admit a further K0 mixed unary pivot. It is not the "
                "collected K16 polynomial and does not use cancellation."
            ),
        },
        "scope": (
            "This is an exact associated-graded K14 source-labelled support "
            "compression. It does not decide coefficient collection on the "
            "remaining rows, hidden initial forms transferred from degrees "
            "below 14, degrees 15 through 24, or the other 30 charts."
        ),
        "pinned_inputs": {
            str(AUDIT_PATH.relative_to(ROOT)): sha256(AUDIT_PATH.read_bytes()).hexdigest(),
            str(FROZEN.R8P.relative_to(ROOT)): sha256(FROZEN.R8P.read_bytes()).hexdigest(),
        },
    }


def main(write_results=False):
    result = build_interface()
    logical = sha256(json.dumps(result, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "logical_sha256": logical,
        **result["gr14_unary_source_compression"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)
