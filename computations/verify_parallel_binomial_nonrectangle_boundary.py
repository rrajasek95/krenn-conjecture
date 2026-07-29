#!/usr/bin/env python3
"""Verify a phase-consistent binomial support with no literal rectangle.

This six-site support is a counterexample to the proposed local statement
that two pure matching terms, together with the 0/2 mixed-fibre condition,
must create a two-vertex recolouring rectangle using the same two underlying
matchings at all four corners.

Every nonempty fibre has two terms.  Giving all nine decorations of the
underlying edge 14 weight -1 and every other supported cell weight +1
cancels all 126 fibres, so the mixed binomial signs are globally consistent.
Nevertheless, exhaustive enumeration finds no literal rectangle.  Three
mixed rows still force each pure binomial to cancel, but the underlying
matching pair is allowed to change between corners.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product


N = 6
COLORS = tuple(range(3))
VERTICES = tuple(range(N))

SUPPORT = frozenset({
    (0, 1, 0, 0), (0, 1, 0, 1), (0, 1, 0, 2),
    (0, 2, 0, 2), (0, 2, 1, 1),
    (0, 3, 0, 0), (0, 3, 2, 2),
    (0, 4, 1, 0), (0, 4, 1, 1), (0, 4, 1, 2),
    (0, 5, 0, 0), (0, 5, 1, 2),
    (1, 2, 0, 1), (1, 2, 1, 1), (1, 2, 2, 1),
    (1, 4, 0, 0), (1, 4, 0, 1), (1, 4, 0, 2),
    (1, 4, 1, 0), (1, 4, 1, 1), (1, 4, 1, 2),
    (1, 4, 2, 0), (1, 4, 2, 1), (1, 4, 2, 2),
    (1, 5, 0, 2), (1, 5, 1, 2), (1, 5, 2, 2),
    (2, 3, 0, 0), (2, 3, 1, 1),
    (2, 4, 2, 0), (2, 4, 2, 1), (2, 4, 2, 2),
    (2, 5, 1, 0), (2, 5, 2, 2),
    (3, 5, 0, 0), (3, 5, 1, 1), (3, 5, 2, 2),
    (4, 5, 0, 0), (4, 5, 1, 0), (4, 5, 2, 0),
})

# Exactly the cells on underlying edge 14 are negative.
NEGATIVE = frozenset(cell for cell in SUPPORT if cell[:2] == (1, 4))


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
    answer = []
    for matching in MATCHINGS:
        term = decorated(matching, coloring)
        if set(term) <= SUPPORT:
            answer.append(term)
    return tuple(answer)


def underlying(term):
    return frozenset((u, v) for u, v, _a, _b in term)


def sign(term):
    return -1 if sum(cell in NEGATIVE for cell in term) % 2 else 1


def exponent_difference(left, right):
    answer = [0] * len(CELLS)
    for cell in left:
        answer[CELL_INDEX[cell]] += 1
    for cell in right:
        answer[CELL_INDEX[cell]] -= 1
    return tuple(answer)


def literal_rectangles(fibres):
    """Enumerate same-pair two-vertex recolouring rectangles.

    Vertices v,w are required not to be paired in either pure matching.
    Thus recolouring them changes two distinct edge cells independently,
    which is precisely the hypothesis behind the elementary rectangle
    exponent identity.
    """

    answer = []
    for color in COLORS:
        pure_coloring = (color,) * N
        pure = fibres[pure_coloring]
        for left, right in combinations(pure, 2):
            pair = {underlying(left), underlying(right)}
            for v, w in combinations(VERTICES, 2):
                if any((v, w) in matching for matching in pair):
                    continue
                for v_color in COLORS:
                    if v_color == color:
                        continue
                    for w_color in COLORS:
                        if w_color == color:
                            continue
                        corners = []
                        for v_bit, w_bit in ((1, 0), (0, 1), (1, 1)):
                            coloring = [color] * N
                            if v_bit:
                                coloring[v] = v_color
                            if w_bit:
                                coloring[w] = w_color
                            corners.append(tuple(coloring))
                        if all(
                            len(fibres[coloring]) == 2
                            and {underlying(term)
                                 for term in fibres[coloring]} == pair
                            for coloring in corners
                        ):
                            answer.append((color, v, w, v_color, w_color))
    return tuple(answer)


# The deterministic MATCHINGS order fixes every row orientation.  These
# identities express each pure exponent difference as an odd combination
# of three mixed differences.  The color-0 identity uses the three coloring
# corners of a rectangle, but switches from matching pair (0,14) to (6,7).
CERTIFICATES = {
    0: (
        ((0, 0, 0, 0, 1, 0), +1),
        ((0, 0, 1, 0, 1, 0), -1),
        ((0, 0, 1, 0, 0, 0), +1),
    ),
    1: (
        ((0, 0, 0, 0, 1, 0), +1),
        ((1, 1, 1, 0, 1, 0), +1),
        ((0, 0, 1, 1, 1, 0), -1),
    ),
    2: (
        ((0, 0, 0, 0, 1, 0), +1),
        ((0, 2, 2, 0, 2, 2), +1),
        ((0, 0, 1, 1, 1, 0), -1),
    ),
}


def main():
    assert len(SUPPORT) == 40
    assert len(MATCHINGS) == 15
    assert len(NEGATIVE) == 9

    fibres = {
        coloring: fibre(coloring)
        for coloring in product(COLORS, repeat=N)
    }
    distribution = Counter(map(len, fibres.values()))
    assert distribution == Counter({0: 603, 2: 126})
    assert all(len(fibres[(color,) * N]) == 2 for color in COLORS)
    assert sum(
        bool(terms) and len(set(coloring)) > 1
        for coloring, terms in fibres.items()
    ) == 123

    # This one signing proves exact phase consistency of all mixed rows.
    # In fact it cancels the three pure fibres as well.
    assert all(
        sorted(sign(term) for term in terms) == [-1, +1]
        for terms in fibres.values() if terms
    )

    # Exhaustive support-level audit of the proposed local rectangle.
    assert literal_rectangles(fibres) == ()

    # Despite the absence of a literal rectangle, translated three-row
    # identities force all three complete pure binomials to vanish under
    # every nonzero complex solution of the mixed equations.
    for color, certificate in CERTIFICATES.items():
        pure_difference = exponent_difference(
            *fibres[(color,) * N]
        )
        mixed_differences = []
        coefficients = []
        for coloring, coefficient in certificate:
            assert len(set(coloring)) > 1
            assert len(fibres[coloring]) == 2
            mixed_differences.append(exponent_difference(*fibres[coloring]))
            coefficients.append(coefficient)
        reconstructed = tuple(
            sum(coefficient * difference[column]
                for coefficient, difference in zip(
                    coefficients, mixed_differences
                ))
            for column in range(len(CELLS))
        )
        assert reconstructed == pure_difference
        assert sum(coefficients) % 2 == 1
        assert (-1) ** sum(coefficients) == -1

    # Make the matching-pair switch in the first translated rectangle
    # explicit; this is exactly why the literal same-pair lemma misses it.
    pure_pair = {
        underlying(term) for term in fibres[(0,) * N]
    }
    first, diagonal, second = (
        coloring for coloring, _coefficient in CERTIFICATES[0]
    )
    assert {underlying(term) for term in fibres[first]} == pure_pair
    assert (
        {underlying(term) for term in fibres[diagonal]}
        == {underlying(term) for term in fibres[second]}
        != pure_pair
    )

    print(
        "verified nonrectangle toric boundary: 40 cells, 603 empty + "
        "126 binomial fibres (123 mixed), globally consistent +/-1 phases"
    )
    print(
        "literal same-matching-pair recolouring rectangles: 0; translated "
        "three-row identities nevertheless force C_0=C_1=C_2=0"
    )


if __name__ == "__main__":
    main()
