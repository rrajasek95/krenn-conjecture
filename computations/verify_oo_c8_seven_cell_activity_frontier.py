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
    hall_pq_row_signatures = Counter()
    hall_pr_row_signatures = Counter()
    hall_pqr_signatures = Counter()
    hall_activity_sizes = Counter()
    compound_flags = Counter()
    compound_availability = Counter()
    size_four_records = []
    no_compound_active_profiles = Counter()
    no_compound_active_samples = []
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
            certificate_indices = (terminal, pair_blockers[0])
            minimal_choices = tuple((terminal, index) for index in pair_blockers)
        else:
            certificate_size = None
            certificate_indices = None
            other_indices = tuple(compatible)
            for size in range(2, len(other_indices) + 1):
                for selected in combinations(other_indices, size):
                    intersection = (1 << len(seed_triples)) - 1
                    for index in selected:
                        intersection &= compatible[index]
                    if not intersection:
                        certificate_size = size + 1  # include the terminal row
                        certificate_indices = (terminal,) + selected
                        break
                if certificate_size is not None:
                    break
            require(certificate_size is not None, "missing Hall certificate")
            hall_certificate_sizes[certificate_size] += 1
            minimal_choices = []
            for selected in combinations(other_indices, certificate_size - 1):
                intersection = (1 << len(seed_triples)) - 1
                for index in selected:
                    intersection &= compatible[index]
                if not intersection:
                    minimal_choices.append((terminal,) + selected)
            minimal_choices = tuple(minimal_choices)
            require(minimal_choices, "minimal Hall choices disappeared")
        certificate_words = tuple(unit_words[index] for index in certificate_indices)
        parent_active = tuple(
            arm
            for arm in frontier.ARMS
            if frontier.is_support_active(blocks, support, arm)
        )
        hall_activity_sizes[(len(certificate_words), parent_active)] += 1

        def indices_have_compound(indices, endpoints):
            rows = tuple(
                (unit_words[index][endpoints[0]], unit_words[index][endpoints[1]])
                for index in indices
            )
            return any(
                first[0] != second[0] and first[1] != second[1]
                for first, second in combinations(rows, 2)
            )

        choice_flags = tuple(
            (
                indices_have_compound(choice, (base.P, base.Q)),
                indices_have_compound(choice, (base.P, base.R)),
            )
            for choice in minimal_choices
        )
        compound_availability[
            (
                len(certificate_words),
                parent_active,
                any(pq or pr for pq, pr in choice_flags),
                any(pq and pr for pq, pr in choice_flags),
            )
        ] += 1
        if (
            parent_active == frontier.ARMS
            and not any(pq or pr for pq, pr in choice_flags)
        ):
            leading = tuple(
                four.leading_matching(blocks, support, arm)
                for arm in frontier.ARMS
            )
            profile = (
                tuple(sorted(frontier.shore_type(cell) for cell in support)),
                four.matching_union_type(leading[0][2], leading[1][2]),
                sum(cell[2:] != (1, 1) for cell in support),
            )
            no_compound_active_profiles[profile] += 1
            if len(no_compound_active_samples) < 5:
                no_compound_active_samples.append(
                    (support, profile, tuple(unit_words[index] for index in minimal_choices[0]))
                )
        pq_signature = tuple(sorted((word[base.P], word[base.Q]) for word in certificate_words))
        pr_signature = tuple(sorted((word[base.P], word[base.R]) for word in certificate_words))
        pqr_signature = tuple(
            sorted((word[base.P], word[base.Q], word[base.R]) for word in certificate_words)
        )
        hall_pq_row_signatures[(len(certificate_words), pq_signature)] += 1
        hall_pr_row_signatures[(len(certificate_words), pr_signature)] += 1
        hall_pqr_signatures[(len(certificate_words), pqr_signature)] += 1

        def has_compound(endpoints):
            rows = tuple((word[endpoints[0]], word[endpoints[1]]) for word in certificate_words)
            return any(
                first[0] != second[0] and first[1] != second[1]
                for first, second in combinations(rows, 2)
            )

        def has_diagonal_pair(endpoints):
            labels = {
                word[endpoints[0]]
                for word in certificate_words
                if word[endpoints[0]] == word[endpoints[1]]
            }
            return len(labels) >= 2

        flags = (
            has_compound((base.P, base.Q)),
            has_compound((base.P, base.R)),
            has_diagonal_pair((base.P, base.Q)),
            has_diagonal_pair((base.P, base.R)),
        )
        compound_flags[(len(certificate_words), parent_active, flags)] += 1
        if len(certificate_words) == 4:
            leading_union = None
            if parent_active == frontier.ARMS:
                leading = tuple(
                    four.leading_matching(blocks, support, arm)
                    for arm in frontier.ARMS
                )
                leading_union = four.matching_union_type(leading[0][2], leading[1][2])
            size_four_records.append(
                (support, parent_active, leading_union, certificate_words)
            )

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
    print("most common pq row signatures:", hall_pq_row_signatures.most_common(10))
    print("most common pr row signatures:", hall_pr_row_signatures.most_common(10))
    print("most common pqr signatures:", hall_pqr_signatures.most_common(10))
    print(f"Hall size/activity census={dict(sorted(hall_activity_sizes.items(), key=str))}")
    print(f"compound/diagonal flag census={dict(sorted(compound_flags.items(), key=str))}")
    print(f"minimal-certificate compound availability={dict(sorted(compound_availability.items(), key=str))}")
    print(f"no-compound both-active profiles={dict(sorted(no_compound_active_profiles.items()))}")
    print(f"no-compound both-active samples={no_compound_active_samples}")
    print(f"size-four Hall cores={size_four_records}")
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
    require(
        hall_activity_sizes
        == Counter({
            (2, frontier.ARMS): 4940,
            (2, (frontier.ARMS[1],)): 1408,
            (2, (frontier.ARMS[0],)): 527,
            (2, ()): 30,
            (3, frontier.ARMS): 170,
            (3, (frontier.ARMS[1],)): 120,
            (3, (frontier.ARMS[0],)): 3,
            (4, (frontier.ARMS[1],)): 2,
        }),
        "Hall size/activity census changed",
    )
    require(
        compound_availability[(2, frontier.ARMS, False, False)] == 114
        and compound_availability[(2, frontier.ARMS, True, False)] == 720
        and compound_availability[(2, frontier.ARMS, True, True)] == 4106
        and compound_availability[(3, frontier.ARMS, True, False)] == 8
        and compound_availability[(3, frontier.ARMS, True, True)] == 162,
        "both-active compound availability changed",
    )


if __name__ == "__main__":
    main()
