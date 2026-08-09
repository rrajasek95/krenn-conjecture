#!/usr/bin/env python3
"""Two-cell mate CEGAR for six-cell active C8 OO completions."""

from collections import Counter

import verify_oo_c8_five_cell_activity_frontier as five
import verify_oo_c8_four_cell_activity_frontier as four
import verify_oo_c8_two_cell_activity_frontier as frontier
import verify_oo_doubly_good_two_anchor_counterguard as base


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def mate_options(blocks, support, word, candidates, maximum=2):
    """Missing-cell sets of size 1..maximum that create a term of ``word``."""

    occupied = set(blocks) | set(support)
    options = set()
    for matching in base.perfect_matchings(base.VERTICES):
        required = frozenset(
            base.key(u, v, word[u], word[v])
            for u, v in matching
            if base.key(u, v, word[u], word[v]) not in occupied
        )
        if 1 <= len(required) <= maximum and required <= candidates:
            options.add(required)
    return tuple(sorted(options, key=lambda option: (len(option), tuple(sorted(option)))))


def main():
    blocks = base.build_packet()
    four_supports = four.four_cell_completions(blocks)
    all_candidates = set(frontier.all_unoccupied_cells(blocks))

    terminal_option_histogram = Counter()
    candidate_pair_histogram = Counter()
    tested_six = set()
    activity = Counter()
    disposition = Counter()
    first_multiclass = None
    for support in four_supports:
        residuals = frontier.target_residuals(
            frontier.tensor_polynomials(blocks, support)
        )
        unit_words = tuple(
            word for word, polynomial in residuals.items()
            if len(polynomial) == 1
        )
        available = all_candidates - set(support)
        options = tuple(
            mate_options(blocks, support, word, available)
            for word in unit_words
        )
        terminal = next(
            index
            for index, word in enumerate(unit_words)
            if not five.one_cell_mates(blocks, support, word, available)
        )
        seed_pairs = tuple(option for option in options[terminal] if len(option) == 2)
        terminal_option_histogram[len(seed_pairs)] += 1

        surviving_pairs = []
        for pair in seed_pairs:
            if all(
                any(option <= pair for option in word_options)
                for word_options in options
            ):
                surviving_pairs.append(pair)
        candidate_pair_histogram[len(surviving_pairs)] += 1

        for pair in surviving_pairs:
            added = tuple(sorted(support + tuple(pair)))
            if added in tested_six:
                continue
            tested_six.add(added)
            active = tuple(
                arm
                for arm in frontier.ARMS
                if frontier.is_support_active(blocks, added, arm)
            )
            activity[active] += 1
            if active != frontier.ARMS:
                continue
            six_residuals = frontier.target_residuals(
                frontier.tensor_polynomials(blocks, added)
            )
            unit_rows = tuple(
                (word, polynomial)
                for word, polynomial in six_residuals.items()
                if len(polynomial) == 1
            )
            if unit_rows:
                disposition["new_monomial_unit"] += 1
                continue
            disposition["no_monomial_unit"] += 1
            if first_multiclass is None:
                first_multiclass = (added, six_residuals)

    print("alternating-C8 six-cell active frontier: PASS")
    print(f"four-cell parents={len(four_supports)}")
    print(f"two-cell options for selected terminal row={dict(sorted(terminal_option_histogram.items()))}")
    print(f"surviving-pair count per parent={dict(sorted(candidate_pair_histogram.items()))}")
    print(f"distinct six-cell candidates={len(tested_six)}")
    print(f"candidate activity={dict(sorted(activity.items(), key=str))}")
    print(f"both-active disposition={dict(sorted(disposition.items()))}")
    if first_multiclass is None:
        print("no six-cell support mates every inherited unit row")
    else:
        support, residuals = first_multiclass
        print(f"first no-monomial support={support}")
        print(f"residual rows={len(residuals)}")

    require(
        terminal_option_histogram == Counter({12: 7200}),
        "selected terminal two-cell mate-option census changed",
    )
    require(
        candidate_pair_histogram == Counter({0: 7200}),
        "a two-cell mate pair survived every inherited private row",
    )
    require(not tested_six, "a six-cell candidate survived inherited private rows")


if __name__ == "__main__":
    main()
