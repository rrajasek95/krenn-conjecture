#!/usr/bin/env python3
"""Tiny exact audit for the four-site arbitrary-superposition theorem.

The uniform proof is in the companion note.  This dependency-free checker
audits its finite incidence ledger, the complementary-pair bookkeeping,
and the canonical rank-two two-star block.
"""

from fractions import Fraction
from itertools import combinations, product


SITES = range(4)
COLOURS = range(3)
PAIRS = tuple(combinations(SITES, 2))
OUTSIDE_SETS = tuple(
    frozenset(chosen)
    for size in range(3)
    for chosen in combinations(SITES, size)
)


def rational_rank(matrix):
    rows = [[Fraction(value) for value in row] for row in matrix]
    rank = 0
    for column in range(len(rows[0])):
        pivot = next(
            (row for row in range(rank, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][column]
        rows[rank] = [value / pivot_value for value in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                left - factor * right
                for left, right in zip(rows[row], rows[rank])
            ]
        rank += 1
    return rank


def audit_pair_channels():
    for outside_size in range(5):
        for outside in combinations(SITES, outside_size):
            disjoint_pairs = [
                pair for pair in PAIRS if not set(pair) & set(outside)
            ]
            if outside_size >= 3:
                assert not disjoint_pairs
            if outside_size == 2:
                expected = tuple(site for site in SITES if site not in outside)
                assert disjoint_pairs == [expected]


def audit_rank_two_block():
    # After independent changes of bases on two rank-two local spans,
    # (T,V)=(e_0,e_1) at both ends.  The block is the exchange matrix.
    exchange = (
        (0, 1),
        (1, 0),
    )
    assert rational_rank(exchange) == 2

    # Non-coordinate rational pairs give the same exact rank.
    left_t = (1, 2, 3)
    left_v = (2, -1, 1)
    right_t = (1, 0, 2)
    right_v = (-1, 3, 1)
    block = tuple(
        tuple(
            left_t[row] * right_v[column]
            + left_v[row] * right_t[column]
            for column in COLOURS
        )
        for row in COLOURS
    )
    assert rational_rank((left_t, left_v)) == 2
    assert rational_rank((right_t, right_v)) == 2
    assert rational_rank(block) == 2


def ledger_is_admissible(ranks, outside_by_colour):
    # A rank-r local space contains at most r target coordinate lines.
    for site in SITES:
        inside_count = sum(
            site not in outside_by_colour[colour] for colour in COLOURS
        )
        if inside_count > ranks[site]:
            return False

    # Lemma 3.1: an exact two-site outside set cannot leave two rank-two
    # sites in the complementary multiplier block.
    for outside in outside_by_colour:
        if len(outside) != 2:
            continue
        complement = [site for site in SITES if site not in outside]
        if ranks[complement[0]] == ranks[complement[1]] == 2:
            return False
    return True


def audit_all_incidence_ledgers():
    profiles_reaching_six = set()
    ledgers = 0
    for ranks in product(range(3), repeat=4):
        if sum(ranks) >= 6:
            profiles_reaching_six.add(tuple(sorted(ranks, reverse=True)))
        for outside_by_colour in product(OUTSIDE_SETS, repeat=3):
            ledgers += 1
            assert not ledger_is_admissible(ranks, outside_by_colour), (
                ranks,
                outside_by_colour,
            )

    assert profiles_reaching_six == {
        (2, 2, 2, 2),
        (2, 2, 2, 1),
        (2, 2, 2, 0),
        (2, 2, 1, 1),
    }
    return ledgers


def audit_binary_sharpness():
    # Coordinate words use -1 for a missing site.  Multiplication simply
    # fills disjoint sites and discards collisions.
    t = ((0, 0), (1, 1))
    v = ((1, 0), (2, 1))
    q_zero = ((2, 0), (3, 0))
    q_one = ((3, 1), (0, 1))

    def surviving_words(quadratic):
        answer = []
        for t_site, t_colour in t:
            for v_site, v_colour in v:
                cells = ((t_site, t_colour), (v_site, v_colour)) + quadratic
                sites = [site for site, _ in cells]
                if len(set(sites)) != 4:
                    continue
                word = [-1] * 4
                for site, colour in cells:
                    word[site] = colour
                answer.append(tuple(word))
        return answer

    assert surviving_words(q_zero) == [(0, 0, 0, 0)]
    assert surviving_words(q_one) == [(1, 1, 1, 1)]


def main():
    audit_pair_channels()
    audit_rank_two_block()
    ledgers = audit_all_incidence_ledgers()
    audit_binary_sharpness()
    print(
        "four-site arbitrary-superposition obstruction: PASS; "
        f"pairs={len(PAIRS)}, outside ledgers={ledgers}, "
        "rank profiles=4, binary bound sharp"
    )


if __name__ == "__main__":
    main()
