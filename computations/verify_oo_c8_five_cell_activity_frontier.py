#!/usr/bin/env python3
"""Private-row CEGAR for five-cell active C8 OO completions."""

from collections import Counter
from itertools import combinations

import verify_oo_c8_four_cell_activity_frontier as four
import verify_oo_c8_two_cell_activity_frontier as frontier
import verify_oo_doubly_good_two_anchor_counterguard as base


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def one_cell_mates(blocks, support, word, candidates):
    """Cells which add a second matching monomial to ``word``."""

    occupied = set(blocks) | set(support)
    mates = set()
    for matching in base.perfect_matchings(base.VERTICES):
        required = tuple(
            base.key(u, v, word[u], word[v])
            for u, v in matching
        )
        missing = tuple(cell for cell in required if cell not in occupied)
        if len(missing) == 1 and missing[0] in candidates:
            mates.add(missing[0])
    return mates


def smallest_empty_intersection(mate_sets):
    for size in range(1, len(mate_sets) + 1):
        for indices in combinations(range(len(mate_sets)), size):
            if not set.intersection(*(mate_sets[index] for index in indices)):
                return indices
    raise AssertionError("the full mate intersection is nonempty")


def main():
    blocks = base.build_packet()
    four_supports = four.four_cell_completions(blocks)
    all_candidates = set(frontier.all_unoccupied_cells(blocks))

    mate_count_histogram = Counter()
    mate_certificate_sizes = Counter()
    active_union_certificates = Counter()
    terminal_count_histogram = Counter()
    terminal_one_site_histogram = Counter()
    parent_max_terminal_ones = Counter()
    four_activity = Counter()
    tested_five = set()
    five_activity = Counter()
    disposition = Counter()
    first_multiclass = None
    for support in four_supports:
        active_arms = tuple(
            arm
            for arm in frontier.ARMS
            if frontier.is_support_active(blocks, support, arm)
        )
        four_activity[active_arms] += 1
        residuals = frontier.target_residuals(
            frontier.tensor_polynomials(blocks, support)
        )
        unit_words = tuple(
            word for word, polynomial in residuals.items()
            if len(polynomial) == 1
        )
        require(unit_words, "a four-cell support escaped the private-row layer")

        mate_sets = [
            one_cell_mates(blocks, support, word, all_candidates - set(support))
            for word in unit_words
        ]
        terminal_indices = tuple(index for index, mates in enumerate(mate_sets) if not mates)
        terminal_count_histogram[len(terminal_indices)] += 1
        terminal_ones = [sum(colour == 1 for colour in unit_words[index]) for index in terminal_indices]
        terminal_one_site_histogram.update(terminal_ones)
        parent_max_terminal_ones[max(terminal_ones)] += 1
        common_mates = set.intersection(*mate_sets)
        mate_count_histogram[len(common_mates)] += 1
        if not common_mates:
            certificate = smallest_empty_intersection(mate_sets)
            mate_certificate_sizes[len(certificate)] += 1
            if active_arms == frontier.ARMS:
                leading = tuple(
                    four.leading_matching(blocks, support, arm)
                    for arm in frontier.ARMS
                )
                union_type = four.matching_union_type(leading[0][2], leading[1][2])
                active_union_certificates[(union_type, len(certificate))] += 1
        for cell in common_mates:
            added = tuple(sorted(support + (cell,)))
            if added in tested_five:
                continue
            tested_five.add(added)
            active = tuple(
                arm
                for arm in frontier.ARMS
                if frontier.is_support_active(blocks, added, arm)
            )
            five_activity[active] += 1
            if active != frontier.ARMS:
                continue
            five_residuals = frontier.target_residuals(
                frontier.tensor_polynomials(blocks, added)
            )
            unit_rows = tuple(
                (word, polynomial)
                for word, polynomial in five_residuals.items()
                if len(polynomial) == 1
            )
            if unit_rows:
                disposition["new_monomial_unit"] += 1
                continue
            disposition["no_monomial_unit"] += 1
            if first_multiclass is None:
                first_multiclass = (added, five_residuals)

    print("alternating-C8 five-cell active frontier: PASS")
    print(f"four-cell parents={len(four_supports)}")
    print(f"four-parent activity={dict(sorted(four_activity.items(), key=str))}")
    print(f"common-mate-count histogram={dict(sorted(mate_count_histogram.items()))}")
    print(f"minimal empty-intersection sizes={dict(sorted(mate_certificate_sizes.items()))}")
    print(f"terminal-row-count histogram={dict(sorted(terminal_count_histogram.items()))}")
    print(f"terminal row number-of-1-sites={dict(sorted(terminal_one_site_histogram.items()))}")
    print(f"parent max terminal 1-sites={dict(sorted(parent_max_terminal_ones.items()))}")
    print(f"active union/certificate census={dict(sorted(active_union_certificates.items()))}")
    print(f"distinct five-cell candidates after exact mate intersection={len(tested_five)}")
    print(f"candidate activity={dict(sorted(five_activity.items(), key=str))}")
    print(f"both-active disposition={dict(sorted(disposition.items()))}")
    if first_multiclass is None:
        print("no five-cell support mates every inherited unit row")
    else:
        support, residuals = first_multiclass
        print(f"first no-monomial support={support}")
        print(f"residual rows={len(residuals)}")

    require(mate_count_histogram == Counter({0: 7200}), "a four-parent has a common mate")
    require(
        mate_certificate_sizes == Counter({1: 7200}),
        "a parent lost its completely unmateable private row",
    )
    require(
        sum(terminal_count_histogram.values()) == 7200
        and min(terminal_count_histogram) == 2
        and max(terminal_count_histogram) == 11,
        "terminal private-row range changed",
    )
    require(
        active_union_certificates
        == Counter({((2, (2, 2)), 1): 2955,
                    ((4, (2,)), 1): 1853,
                    ((6, ()), 1): 302}),
        "active union/certificate census changed",
    )
    require(not tested_five, "a five-cell candidate survived inherited private rows")


if __name__ == "__main__":
    main()
