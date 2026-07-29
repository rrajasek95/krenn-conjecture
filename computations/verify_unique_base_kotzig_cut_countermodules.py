#!/usr/bin/env python3
"""Exact audits for the unique-base/Kotzig-cut countermodules.

The checks are dependency-free and use only integer/Fraction arithmetic.
They verify:

* an exact binary GHZ source with a unique 00 matching but a non-tight
  Kotzig shore;
* the pairwise-exact ternary prism with its unique ternary residual;
* all fourteen possible first cancellation mates of that residual; and
* a smallest two-stage repair chain on which cut complexity stalls at one.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import product


VERTICES = tuple(range(6))
COLORS = tuple(range(3))
SHORE = frozenset((0, 1, 5))


def perfect_matchings(vertices=VERTICES):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        remaining = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remaining):
            yield tuple(sorted(((u, v),) + tail))


PERFECT_MATCHINGS = tuple(perfect_matchings())

P0 = tuple(sorted(((0, 1), (2, 3), (4, 5))))
P1 = tuple(sorted(((0, 5), (1, 2), (3, 4))))
P2 = tuple(sorted(((0, 3), (1, 5), (2, 4))))
RESIDUAL = tuple(sorted(((0, 3), (1, 2), (4, 5))))
RESIDUAL_WORD = (2, 1, 1, 2, 0, 0)


def decorate(matching, coloring):
    return frozenset((u, v, coloring[u], coloring[v]) for u, v in matching)


def term_value(matching, coloring, weights):
    occurrences = decorate(matching, coloring)
    if not occurrences <= weights.keys():
        return None
    answer = Fraction(1)
    for occurrence in occurrences:
        answer *= weights[occurrence]
    return answer


def fibre(coloring, support):
    return tuple(
        matching
        for matching in PERFECT_MATCHINGS
        if decorate(matching, coloring) <= support
    )


def coefficient(coloring, weights):
    return sum(
        (
            value
            for matching in PERFECT_MATCHINGS
            if (value := term_value(matching, coloring, weights)) is not None
        ),
        Fraction(0),
    )


def crossing_count(matching, shore=SHORE):
    return sum((u in shore) != (v in shore) for u, v in matching)


def pure_prism_weights():
    return {
        occurrence: Fraction(1)
        for color, matching in enumerate((P0, P1, P2))
        for occurrence in decorate(matching, (color,) * len(VERTICES))
    }


def mixed_singletons(support):
    answer = {}
    for coloring in product(COLORS, repeat=len(VERTICES)):
        if len(set(coloring)) == 1:
            continue
        terms = fibre(coloring, support)
        if len(terms) == 1:
            answer[coloring] = terms[0]
    return answer


def verify_binary_countermodule():
    """Full binary equations do not tighten the unique-vacuum cut."""
    weights = {
        (0, 1, 0, 0): Fraction(1),
        (2, 3, 0, 0): Fraction(1),
        (2, 3, 1, 1): Fraction(1),
        (0, 2, 0, 1): Fraction(-1),
        (1, 3, 0, 1): Fraction(1),
        (4, 5, 0, 0): Fraction(1),
        (0, 5, 1, 1): Fraction(1),
        (1, 2, 1, 1): Fraction(1),
        (3, 4, 1, 1): Fraction(1),
    }
    support = frozenset(weights)
    mixed_matching = tuple(sorted(((0, 2), (1, 3), (4, 5))))

    for coloring in product(range(2), repeat=len(VERTICES)):
        expected = int(coloring == (0,) * 6 or coloring == (1,) * 6)
        assert coefficient(coloring, weights) == expected

    assert fibre((0,) * 6, support) == (P0,)
    pair_support = frozenset((u, v) for u, v, _a, _b in support)
    pair_matchings = tuple(
        matching
        for matching in PERFECT_MATCHINGS
        if set(matching) <= pair_support
    )
    assert set(pair_matchings) == {P0, mixed_matching, P1}
    assert tuple(crossing_count(matching) for matching in (P0, mixed_matching, P1)) == (
        1,
        3,
        1,
    )

    # The unique 00 crossing occurrence is 45.  The mixed word 001100 is
    # cancelled by a one-cross and a three-cross matching.
    zero_zero_crossings = {
        (u, v)
        for u, v, a, b in support
        if a == b == 0 and ((u in SHORE) != (v in SHORE))
    }
    assert zero_zero_crossings == {(4, 5)}
    word = (0, 0, 1, 1, 0, 0)
    assert fibre(word, support) == (P0, mixed_matching)
    assert [term_value(matching, word, weights) for matching in fibre(word, support)] == [
        Fraction(1),
        Fraction(-1),
    ]


def verify_pairwise_ternary_countermodule():
    """All binary faces are exact; precisely one ternary word survives."""
    weights = pure_prism_weights()
    support = frozenset(weights)

    nonzero = {}
    for coloring in product(COLORS, repeat=len(VERTICES)):
        value = coefficient(coloring, weights)
        if value:
            nonzero[coloring] = value
    assert nonzero == {
        (0,) * 6: Fraction(1),
        (1,) * 6: Fraction(1),
        (2,) * 6: Fraction(1),
        RESIDUAL_WORD: Fraction(1),
    }

    for color, matching in enumerate((P0, P1, P2)):
        assert fibre((color,) * 6, support) == (matching,)
    for coloring in product(COLORS, repeat=len(VERTICES)):
        if len(set(coloring)) <= 2 and len(set(coloring)) > 1:
            assert coefficient(coloring, weights) == 0

    assert fibre(RESIDUAL_WORD, support) == (RESIDUAL,)
    pair_support = frozenset((u, v) for u, v, _a, _b in support)
    pair_matchings = tuple(
        matching
        for matching in PERFECT_MATCHINGS
        if set(matching) <= pair_support
    )
    assert set(pair_matchings) == {P0, P1, P2, RESIDUAL}
    assert tuple(crossing_count(matching) for matching in (P0, P1, P2, RESIDUAL)) == (
        1,
        1,
        1,
        3,
    )
    zero_zero_crossings = {
        (u, v)
        for u, v, a, b in support
        if a == b == 0 and ((u in SHORE) != (v in SHORE))
    }
    assert zero_zero_crossings == {(4, 5)}


def verify_first_mate_classification():
    """Classify all fourteen possible underlying mates of the residual."""
    base_weights = pure_prism_weights()
    base_support = frozenset(base_weights)
    statistics = Counter()

    for mate in PERFECT_MATCHINGS:
        if mate == RESIDUAL:
            continue
        mate_occurrences = decorate(mate, RESIDUAL_WORD)
        new_occurrences = mate_occurrences - base_support
        support = base_support | mate_occurrences

        # No mate introduces a 00 cell, and all three pure fibers remain
        # singleton normalized fibers.
        assert fibre((0,) * 6, support) == (P0,)
        assert fibre((1,) * 6, support) == (P1,)
        assert fibre((2,) * 6, support) == (P2,)
        assert set(fibre(RESIDUAL_WORD, support)) == {RESIDUAL, mate}
        assert len(new_occurrences) in (2, 3)

        # Normalize this mate to weight -1.  Existing shared occurrences
        # have weight +1, so one new coordinate can carry the minus sign.
        weights = dict(base_weights)
        for occurrence in new_occurrences:
            weights[occurrence] = Fraction(1)
        weights[min(new_occurrences)] = Fraction(-1)
        assert coefficient(RESIDUAL_WORD, weights) == 0

        singletons = mixed_singletons(support)
        assert RESIDUAL_WORD not in singletons
        assert len(singletons) in (2, 3, 5)
        assert all(crossing_count(matching) == 1 for matching in singletons.values())
        statistics[(crossing_count(mate), len(new_occurrences), len(singletons))] += 1

    assert statistics == Counter(
        {
            (1, 2, 2): 3,
            (3, 2, 2): 3,
            (3, 3, 3): 2,
            (1, 3, 5): 6,
        }
    )


def verify_minimal_stalled_repair():
    """A 13-cell exact two-step repair stalls at cut complexity one."""
    weights = pure_prism_weights()

    # First square: cancel the three-cross residual by the one-cross P0.
    weights[(0, 1, 2, 1)] = Fraction(-1)
    weights[(2, 3, 1, 2)] = Fraction(1)

    first_repair_word = (0, 0, 1, 2, 0, 0)
    other_first_defect = (2, 1, 0, 0, 0, 0)
    first_support = frozenset(weights)
    assert set(fibre(RESIDUAL_WORD, first_support)) == {RESIDUAL, P0}
    assert coefficient(RESIDUAL_WORD, weights) == 0
    assert mixed_singletons(first_support) == {
        first_repair_word: P0,
        other_first_defect: P0,
    }

    # Second square: repair the crossing-one word with the three-cross
    # matching 02|13|45.  The new defects remain at complexity one.
    second_mate = tuple(sorted(((0, 2), (1, 3), (4, 5))))
    weights[(0, 2, 0, 1)] = Fraction(-1)
    weights[(1, 3, 0, 2)] = Fraction(1)
    support = frozenset(weights)
    assert len(support) == 13
    assert set(fibre(first_repair_word, support)) == {P0, second_mate}
    assert coefficient(first_repair_word, weights) == 0
    assert crossing_count(P0) == 1 and crossing_count(second_mate) == 3
    assert fibre((0,) * 6, support) == (P0,)

    new_defects = {
        (0, 2, 1, 1, 1, 2): tuple(sorted(((0, 2), (1, 5), (3, 4)))),
        (1, 0, 2, 2, 2, 1): tuple(sorted(((0, 5), (1, 3), (2, 4)))),
    }
    expected_singletons = {other_first_defect: P0, **new_defects}
    assert mixed_singletons(support) == expected_singletons
    assert all(crossing_count(matching) == 1 for matching in expected_singletons.values())

    # Every coefficient is audited.  Besides the three target constants,
    # exactly the three displayed crossing-one singleton errors survive;
    # the two repaired mixed fibers are exact zero binomials.
    nonzero_coefficients = {}
    nonempty_fibres = set()
    for coloring in product(COLORS, repeat=len(VERTICES)):
        terms = fibre(coloring, support)
        if terms:
            nonempty_fibres.add(coloring)
        value = coefficient(coloring, weights)
        if value:
            nonzero_coefficients[coloring] = value
    assert nonempty_fibres == {
        (0,) * 6,
        (1,) * 6,
        (2,) * 6,
        RESIDUAL_WORD,
        first_repair_word,
        other_first_defect,
        *new_defects,
    }
    assert nonzero_coefficients == {
        (0,) * 6: Fraction(1),
        (1,) * 6: Fraction(1),
        (2,) * 6: Fraction(1),
        other_first_defect: Fraction(-1),
        (0, 2, 1, 1, 1, 2): Fraction(-1),
        (1, 0, 2, 2, 2, 1): Fraction(1),
    }

    # Exhaustively certify the support-minimality assertion used in the
    # note.  A first residual mate needs at least two new cells.  After any
    # such repair, repairing one of its crossing-one singleton fibers while
    # preserving the unique all-zero matching and creating another
    # singleton needs at least four new cells in total.  The displayed
    # source attains four.
    base_support = frozenset(pure_prism_weights())
    minimum_total_new = 10**9
    for first_mate in PERFECT_MATCHINGS:
        if first_mate == RESIDUAL:
            continue
        support_one = base_support | decorate(first_mate, RESIDUAL_WORD)
        assert len(support_one - base_support) >= 2
        old_singletons = mixed_singletons(support_one)
        for word, sole_matching in old_singletons.items():
            if crossing_count(sole_matching) != 1:
                continue
            for second_candidate in PERFECT_MATCHINGS:
                if second_candidate == sole_matching:
                    continue
                support_two = support_one | decorate(second_candidate, word)
                if len(fibre(word, support_two)) < 2:
                    continue
                if fibre((0,) * 6, support_two) != (P0,):
                    continue
                new_singleton_words = (
                    set(mixed_singletons(support_two)) - set(old_singletons)
                )
                if not new_singleton_words:
                    continue
                minimum_total_new = min(
                    minimum_total_new, len(support_two - base_support)
                )
    assert minimum_total_new == 4
    assert len(support - base_support) == minimum_total_new


def main():
    assert len(PERFECT_MATCHINGS) == 15
    verify_binary_countermodule()
    verify_pairwise_ternary_countermodule()
    verify_first_mate_classification()
    verify_minimal_stalled_repair()
    print("unique-base Kotzig-cut countermodules: PASS")
    print("binary exact source: unique 00 matching, cut counts 1/3/1")
    print("ternary prism: all binary faces exact, one three-cross residual")
    print("all 14 first mates create 2, 3, or 5 crossing-one singleton fibers")
    print("smallest two-stage repair uses 4 new cells and stalls at complexity one")


if __name__ == "__main__":
    main()
