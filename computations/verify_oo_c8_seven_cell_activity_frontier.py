#!/usr/bin/env python3
"""Three-cell repair CEGAR for seven-cell active C8 OO completions."""

from collections import Counter, defaultdict
from functools import reduce
from itertools import combinations

import verify_oo_c8_six_cell_activity_frontier as six
import verify_oo_c8_four_cell_activity_frontier as four
import verify_oo_c8_two_cell_activity_frontier as frontier
import verify_oo_doubly_good_two_anchor_counterguard as base


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def candidate_triples(seed_options, available):
    triples = set()
    for option in seed_options:
        if len(option) == 3:
            triples.add(option)
        elif len(option) == 2:
            for cell in available - option:
                triples.add(option | {cell})
    return triples


def main():
    blocks = base.build_packet()
    four_supports = four.four_cell_completions(blocks)
    all_candidates = set(frontier.all_unoccupied_cells(blocks))

    parents_seen = 0
    triple_seed_histogram = Counter()
    simultaneous_repair_histogram = Counter()
    full_tensor_tests = 0
    terminal_pair_blockers = Counter()
    hall_certificate_sizes = Counter()
    first_multiclass = None
    first_parent_signature = None
    for support in four_supports:
        parents_seen += 1
        residuals = frontier.target_residuals(
            frontier.tensor_polynomials(blocks, support)
        )
        unit_words = tuple(
            word for word, polynomial in residuals.items()
            if len(polynomial) == 1
        )
        available = all_candidates - set(support)
        options = tuple(
            six.mate_options(blocks, support, word, available, maximum=3)
            for word in unit_words
        )
        terminal = next(
            index
            for index, word_options in enumerate(options)
            if not any(len(option) == 1 for option in word_options)
        )
        seed_triples = tuple(sorted(candidate_triples(options[terminal], available), key=lambda triple: tuple(sorted(triple))))
        triple_seed_histogram[len(seed_triples)] += 1

        containment = defaultdict(int)
        for triple_index, triple in enumerate(seed_triples):
            triple_tuple = tuple(triple)
            for size in (1, 2, 3):
                for subset in combinations(triple_tuple, size):
                    containment[frozenset(subset)] |= 1 << triple_index

        compatible = {
            index: reduce(
                int.__or__, (containment.get(option, 0) for option in options[index]), 0
            )
            for index in range(len(options))
            if index != terminal
        }
        pair_blockers = tuple(index for index, choices in compatible.items() if choices == 0)
        terminal_pair_blockers[len(pair_blockers)] += 1
        if pair_blockers:
            hall_certificate_sizes[2] += 1
        else:
            certificate_size = None
            other_indices = tuple(compatible)
            for size in range(2, len(other_indices) + 1):
                for selected in combinations(other_indices, size):
                    intersection = (1 << len(seed_triples)) - 1
                    for index in selected:
                        intersection &= compatible[index]
                    if not intersection:
                        certificate_size = size + 1  # include the terminal row
                        break
                if certificate_size is not None:
                    break
            require(certificate_size is not None, "missing Hall certificate")
            hall_certificate_sizes[certificate_size] += 1

        simultaneous_bits = (1 << len(seed_triples)) - 1
        for choices in compatible.values():
            simultaneous_bits &= choices
        simultaneous_count = simultaneous_bits.bit_count()
        simultaneous_repair_histogram[simultaneous_count] += 1
        simultaneous = tuple(
            triple
            for index, triple in enumerate(seed_triples)
            if simultaneous_bits & (1 << index)
        )
        if simultaneous and first_parent_signature is None:
            first_parent_signature = (support, len(unit_words), len(seed_triples), simultaneous[0])

        for triple in simultaneous:
            added = tuple(sorted(support + tuple(triple)))
            active = tuple(
                arm
                for arm in frontier.ARMS
                if frontier.is_support_active(blocks, added, arm)
            )
            if active != frontier.ARMS:
                continue
            full_tensor_tests += 1
            seven_residuals = frontier.target_residuals(
                frontier.tensor_polynomials(blocks, added)
            )
            unit_rows = tuple(
                (word, polynomial)
                for word, polynomial in seven_residuals.items()
                if len(polynomial) == 1
            )
            if not unit_rows:
                first_multiclass = (added, seven_residuals)
                break
        if first_multiclass is not None:
            break

    print("alternating-C8 seven-cell active frontier: PASS")
    print(f"four-cell parents processed={parents_seen}/{len(four_supports)}")
    print(f"seed-triple histogram={dict(sorted(triple_seed_histogram.items()))}")
    print(f"simultaneous-repair histogram={dict(sorted(simultaneous_repair_histogram.items()))}")
    print(f"terminal-row pair-blocker histogram={dict(sorted(terminal_pair_blockers.items()))}")
    print(f"minimal Hall-certificate sizes={dict(sorted(hall_certificate_sizes.items()))}")
    print(f"first parent admitting a simultaneous repair={first_parent_signature}")
    print(f"full both-active tensor tests={full_tensor_tests}")
    if first_multiclass is None:
        print("no seven-cell no-monomial support found in the processed census")
    else:
        support, residuals = first_multiclass
        row_sizes = Counter(len(polynomial) for polynomial in residuals.values())
        print(f"first no-monomial support={support}")
        print(f"residual rows={len(residuals)}; term-count histogram={dict(sorted(row_sizes.items()))}")
        print("residual ledger:")
        for word, polynomial in sorted(residuals.items()):
            print(word, sorted(polynomial.items()))

    require(
        triple_seed_histogram == Counter({2852: 7200}),
        "terminal three-cell repair census changed",
    )
    require(
        simultaneous_repair_histogram == Counter({0: 7200}),
        "a three-cell simultaneous repair survived",
    )
    require(
        hall_certificate_sizes == Counter({2: 6905, 3: 293, 4: 2}),
        "minimal three-cell Hall-certificate census changed",
    )


if __name__ == "__main__":
    main()
