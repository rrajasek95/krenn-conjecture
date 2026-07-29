#!/usr/bin/env python3
"""Exact audit of the exceptional-box boundary-word witnesses."""

from itertools import combinations, permutations, product


FIELDS = (0, 1, 2)
GOOD = (0, 1, 2, 3)
SITES = GOOD + (4, 5)
PAIRS = tuple(combinations(SITES, 2))
TRANSVERSE = 3

REPRESENTATIVES = (
    (1, 2, 3, 4),
    (1, 2, 3, 8),
    (1, 2, 3, 12),
    (1, 2, 4, 7),
    (1, 2, 5, 5),
    (1, 3, 3, 8),
    (1, 3, 3, 12),
    (1, 6, 6, 6),
    (3, 3, 3, 8),
    (3, 3, 3, 12),
)

EXPECTED_CENTRES = (
    (0, 1),
    (0, 1),
    (0, 1),
    (0, 1, 2),
    (0, 2),
    (0, 1),
    (0, 1),
    (1, 2),
    (0, 1),
    (0, 1),
)


def values(mask):
    return tuple(symbol for symbol in range(4) if mask & (1 << symbol))


def box_words(box):
    return tuple(product(*(values(mask) for mask in box)))


def unique_centre(word):
    centres = [
        field
        for field in FIELDS
        if word.count(field) == 2
        and all(
            word.count(other) < 2
            for other in FIELDS
            if other != field
        )
    ]
    assert len(centres) <= 1
    return centres[0] if centres else None


def formal_contributors(word):
    """Retain field, missing pair, and ordered row endpoints."""
    terms = []
    for field in FIELDS:
        deviations = {
            site for site, symbol in enumerate(word) if symbol != field
        }
        for pair in PAIRS:
            if deviations.issubset(pair):
                for row_order in permutations(pair, 2):
                    terms.append((field, frozenset(pair), row_order))
    return terms


def main():
    witness_total = 0
    formal_term_total = 0

    for orbit, (box, expected) in enumerate(
        zip(REPRESENTATIVES, EXPECTED_CENTRES), start=1
    ):
        witnesses = {}
        for word in box_words(box):
            centre = unique_centre(word)
            if centre is not None and centre not in witnesses:
                witnesses[centre] = word

        assert tuple(sorted(witnesses)) == expected

        for centre in expected:
            word = witnesses[centre]
            deviations = frozenset(
                site
                for site, symbol in enumerate(word)
                if symbol != centre
            )
            assert len(deviations) == 2
            assert deviations.issubset(GOOD)

            terms = formal_contributors(word)
            assert len(terms) == 2
            assert {
                (field, pair)
                for field, pair, _ in terms
            } == {(centre, deviations)}
            assert {
                order for _, _, order in terms
            } == set(permutations(tuple(sorted(deviations)), 2))

            witness_total += 1
            formal_term_total += len(terms)

        if orbit == 4:
            assert len(expected) == 3
        else:
            assert len(expected) == 2

    assert witness_total == 21
    assert formal_term_total == 42
    print("two-deficient exceptional boundary words: PASS")
    print(f"exceptional support orbits: {len(REPRESENTATIVES)}")
    print(f"unique-centre witnesses: {witness_total}")
    print(f"ordered response terms: {formal_term_total}")


if __name__ == "__main__":
    main()
