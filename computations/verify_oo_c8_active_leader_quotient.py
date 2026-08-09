#!/usr/bin/env python3
"""Active-cofactor leader quotient on the 114 Hall compound regressions."""

from collections import Counter, defaultdict
from functools import reduce
from itertools import combinations

import verify_oo_c8_seven_cell_activity_frontier as seven
import verify_oo_c8_six_cell_activity_frontier as six
import verify_oo_c8_four_cell_activity_frontier as four
import verify_oo_c8_two_cell_activity_frontier as frontier
import verify_oo_doubly_good_two_anchor_counterguard as base


COMMON = (1, 3, 5, 6, 7)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def rows_compound(words, endpoints):
    rows = tuple((word[endpoints[0]], word[endpoints[1]]) for word in words)
    return any(
        first[0] != second[0] and first[1] != second[1]
        for first, second in combinations(rows, 2)
    )


def no_compound_regressions(blocks):
    candidates = set(frontier.all_unoccupied_cells(blocks))
    regressions = []
    for support in four.four_cell_completions(blocks):
        active = tuple(
            arm
            for arm in frontier.ARMS
            if frontier.is_support_active(blocks, support, arm)
        )
        if active != frontier.ARMS:
            continue
        residuals = frontier.target_residuals(
            frontier.tensor_polynomials(blocks, support)
        )
        unit_words = tuple(
            word for word, polynomial in residuals.items()
            if len(polynomial) == 1
        )
        available = candidates - set(support)
        options = tuple(
            six.mate_options(blocks, support, word, available, maximum=3)
            for word in unit_words
        )
        terminal = next(
            index
            for index, word_options in enumerate(options)
            if not any(len(option) == 1 for option in word_options)
        )
        seed_triples = tuple(
            seven.candidate_triples(options[terminal], available)
        )
        containment = defaultdict(int)
        for triple_index, triple in enumerate(seed_triples):
            triple_tuple = tuple(triple)
            for size in (1, 2, 3):
                for subset in combinations(triple_tuple, size):
                    containment[frozenset(subset)] |= 1 << triple_index
        compatible = {
            index: reduce(
                int.__or__,
                (containment.get(option, 0) for option in word_options),
                0,
            )
            for index, word_options in enumerate(options)
            if index != terminal
        }
        blockers = tuple(index for index, choices in compatible.items() if choices == 0)
        if not blockers:
            continue
        hall_pairs = tuple(
            (unit_words[terminal], unit_words[index])
            for index in blockers
        )
        if all(
            not rows_compound(words, (base.P, base.Q))
            and not rows_compound(words, (base.P, base.R))
            for words in hall_pairs
        ):
            regressions.append(support)
    require(len(regressions) == 114, "Hall compound regression count changed")
    return tuple(regressions)


def leading_record(blocks, support, arm):
    word, mask, matching, coefficient = four.leading_matching(blocks, support, arm)
    residual = tuple(vertex for vertex in base.VERTICES if vertex not in arm)
    word_by_vertex = dict(zip(residual, word, strict=True))
    polynomial = frontier.cofactor_polynomials(blocks, support, arm)[word]
    pure = word[0] if len(set(word)) == 1 else None
    direct = base.direct_matrix(blocks, *arm)
    nonzero_rows = {
        row for row in base.COLORS for column in base.COLORS if direct[row][column]
    }
    nonzero_columns = {
        column for row in base.COLORS for column in base.COLORS if direct[row][column]
    }
    require(len(nonzero_rows) == len(nonzero_columns) == 1, "direct arm left rank-one coordinate form")
    target_response_rank_bound = 2 if (
        pure is not None
        and pure not in nonzero_rows
        and pure not in nonzero_columns
    ) else int(bool(polynomial))
    return {
        "word": word,
        "common": tuple(word_by_vertex[vertex] for vertex in COMMON),
        "mask": mask,
        "matching": matching,
        "coefficient": coefficient,
        "polynomial": polynomial,
        "pure": pure,
        "direct_row": next(iter(nonzero_rows)),
        "direct_column": next(iter(nonzero_columns)),
        "target_response_rank_bound": target_response_rank_bound,
    }


def main():
    blocks = base.build_packet()
    regressions = no_compound_regressions(blocks)

    rank_pairs = Counter()
    purity_pairs = Counter()
    term_count_pairs = Counter()
    common_hamming = Counter()
    exponent_pairs = Counter()
    branches = Counter()
    first_annihilated = None
    first_proportional = None
    for support in regressions:
        records = tuple(
            leading_record(blocks, support, arm)
            for arm in frontier.ARMS
        )
        rank_pair = tuple(record["target_response_rank_bound"] for record in records)
        rank_pairs[rank_pair] += 1
        purity_pairs[tuple(record["pure"] for record in records)] += 1
        term_count_pairs[
            tuple(len(record["polynomial"]) for record in records)
        ] += 1
        common_hamming[
            sum(first != second for first, second in zip(
                records[0]["common"], records[1]["common"], strict=True
            ))
        ] += 1
        exponent_pairs[
            (
                records[0]["mask"].bit_count(),
                records[1]["mask"].bit_count(),
                (records[0]["mask"] & records[1]["mask"]).bit_count(),
            )
        ] += 1
        if 2 in rank_pair:
            branches["nonzero_compound_response"] += 1
        elif records[0]["common"] == records[1]["common"]:
            branches["rankone_common_word_proportional"] += 1
            if first_proportional is None:
                first_proportional = (support, records)
        else:
            branches["rankone_annihilated_distinct_common_words"] += 1
            if first_annihilated is None:
                first_annihilated = (support, records)

    print("alternating-C8 active leader quotient: PASS")
    print(f"Hall no-compound regressions={len(regressions)}")
    print(f"leader cofactor term-count pairs={dict(sorted(term_count_pairs.items()))}")
    print(f"leader pure-colour pairs={dict(sorted(purity_pairs.items(), key=str))}")
    print(f"formal target-response rank-bound pairs={dict(sorted(rank_pairs.items()))}")
    print(f"common-five word Hamming distances={dict(sorted(common_hamming.items()))}")
    print(f"leader exponent (degree,degree,overlap)={dict(sorted(exponent_pairs.items()))}")
    print(f"leader quotient branches={dict(sorted(branches.items()))}")
    print(f"common-word proportional guard={first_proportional}")
    print(f"first annihilated/distinct guard={first_annihilated}")

    require(term_count_pairs == Counter({(1, 1): 114}), "a chosen cofactor ceased to be monomial")
    require(rank_pairs == Counter({(1, 1): 114}), "a transverse rank-two target response appeared")
    require(
        branches
        == Counter({"rankone_annihilated_distinct_common_words": 113,
                    "rankone_common_word_proportional": 1}),
        "leader quotient branch census changed",
    )


if __name__ == "__main__":
    main()
