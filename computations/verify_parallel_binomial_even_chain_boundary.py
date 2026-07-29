#!/usr/bin/env python3
"""Verify that an arbitrary extra pure matching need not cancel its anchor.

This six-site support has 388 mixed binomial fibres, two pure binomial
fibres, and one four-term pure fibre.  Its mixed signs are globally
consistent.  In the four-term fibre, the selected matching M_0 and the
extra matching M_7 are forced to have the *same* ratio, because their
exponent difference is the sum of two mixed-binomial differences.  Thus an
alternating-cycle mate supplied only by parity need not be the mate that
cancels the selected pure term; the whole even pure fibre matters.
"""

from __future__ import annotations

from collections import Counter
from itertools import product


N = 6
COLORS = tuple(range(3))
VERTICES = tuple(range(N))

SUPPORT = frozenset({
    (0, 1, 0, 0), (0, 1, 1, 1), (0, 1, 1, 2),
    (0, 1, 2, 1), (0, 1, 2, 2),
    (0, 2, 0, 0), (0, 2, 1, 1), (0, 2, 1, 2),
    (0, 2, 2, 1), (0, 2, 2, 2),
    (0, 3, 0, 0), (0, 3, 0, 1), (0, 3, 0, 2),
    (0, 4, 1, 0), (0, 4, 2, 0),
    (1, 2, 0, 1), (1, 2, 0, 2),
    (1, 4, 0, 0), (1, 4, 1, 0), (1, 4, 1, 1),
    (1, 4, 1, 2), (1, 4, 2, 0), (1, 4, 2, 1),
    (1, 4, 2, 2),
    (1, 5, 1, 1), (1, 5, 1, 2), (1, 5, 2, 1),
    (1, 5, 2, 2),
    (2, 3, 0, 0), (2, 3, 1, 0), (2, 3, 1, 1),
    (2, 3, 1, 2), (2, 3, 2, 0), (2, 3, 2, 1),
    (2, 3, 2, 2),
    (2, 5, 0, 0), (2, 5, 0, 1), (2, 5, 0, 2),
    (3, 4, 0, 0), (3, 4, 0, 1), (3, 4, 0, 2),
    (3, 5, 0, 0), (3, 5, 1, 0), (3, 5, 1, 1),
    (3, 5, 1, 2), (3, 5, 2, 0), (3, 5, 2, 1),
    (3, 5, 2, 2),
    (4, 5, 0, 0), (4, 5, 1, 0), (4, 5, 1, 1),
    (4, 5, 1, 2), (4, 5, 2, 0), (4, 5, 2, 1),
    (4, 5, 2, 2),
})

# One exact global phase assignment found by binary Gaussian elimination.
NEGATIVE = frozenset({
    (0, 1, 0, 0),
    (0, 2, 0, 0), (0, 2, 1, 1), (0, 2, 1, 2),
    (0, 2, 2, 1), (0, 2, 2, 2),
    (2, 3, 0, 0),
})


def perfect_matchings(vertices=VERTICES):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


MATCHINGS = tuple(perfect_matchings())
CELLS = tuple(sorted(SUPPORT))
CELL_INDEX = {cell: index for index, cell in enumerate(CELLS)}


def decorated(matching, coloring):
    return tuple(
        (u, v, coloring[u], coloring[v]) for u, v in matching
    )


def fibre(coloring):
    return tuple(
        (number, term)
        for number, matching in enumerate(MATCHINGS)
        if set(term := decorated(matching, coloring)) <= SUPPORT
    )


def sign(term):
    return -1 if sum(cell in NEGATIVE for cell in term) % 2 else 1


def exponent_difference(left, right):
    answer = [0] * len(CELLS)
    for cell in left:
        answer[CELL_INDEX[cell]] += 1
    for cell in right:
        answer[CELL_INDEX[cell]] -= 1
    return tuple(answer)


def main():
    assert len(SUPPORT) == 55
    assert NEGATIVE <= SUPPORT
    assert len(MATCHINGS) == 15

    fibres = {
        coloring: fibre(coloring)
        for coloring in product(COLORS, repeat=N)
    }
    nonempty_distribution = Counter(
        len(terms) for terms in fibres.values() if terms
    )
    assert nonempty_distribution == Counter({2: 390, 4: 1})

    mixed = [
        (coloring, terms)
        for coloring, terms in fibres.items()
        if len(set(coloring)) > 1 and terms
    ]
    assert len(mixed) == 388
    assert all(len(terms) == 2 for _coloring, terms in mixed)
    assert all(
        sorted(sign(term) for _number, term in terms) == [-1, +1]
        for _coloring, terms in mixed
    )

    pure = [fibres[(color,) * N] for color in COLORS]
    assert [len(terms) for terms in pure] == [4, 2, 2]
    assert [[number for number, _term in terms] for terms in pure] == [
        [0, 2, 4, 7], [0, 4], [0, 4]
    ]
    assert [
        [sign(term) for _number, term in terms] for terms in pure
    ] == [[+1, -1, -1, +1], [+1, -1], [+1, -1]]
    assert [
        sum(sign(term) for _number, term in terms) for terms in pure
    ] == [0, 0, 0]

    # The two mixed fibres form an even cancellation chain
    # M_0 --(-1)--> M_2 --(-1)--> M_7.
    first_coloring = (1, 1, 0, 0, 0, 0)
    second_coloring = (0, 0, 0, 0, 0, 1)
    assert [number for number, _term in fibres[first_coloring]] == [0, 2]
    assert [number for number, _term in fibres[second_coloring]] == [2, 7]

    term_0 = pure[0][0][1]
    term_7 = pure[0][3][1]
    difference_07 = exponent_difference(term_0, term_7)
    difference_02 = exponent_difference(
        fibres[first_coloring][0][1], fibres[first_coloring][1][1]
    )
    difference_27 = exponent_difference(
        fibres[second_coloring][0][1], fibres[second_coloring][1][1]
    )
    assert difference_07 == tuple(
        left + right for left, right in zip(difference_02, difference_27)
    )

    # Under any nonzero complex weighting cancelling the two mixed
    # binomials, x^d02=x^d27=-1, hence x^d07=+1.  The selected M_0 and
    # extra M_7 pure terms therefore reinforce rather than cancel.
    assert (-1) * (-1) == +1

    print(
        "verified even-chain boundary: 55 cells, 388 mixed binomials, "
        "pure-fibre sizes (4,2,2), globally consistent +/-1 phases"
    )
    print(
        "d_pure(0,7)=d_110000(0,2)+d_000001(2,7), so mixed "
        "cancellation universally forces pure ratio M_0/M_7=+1"
    )


if __name__ == "__main__":
    main()
