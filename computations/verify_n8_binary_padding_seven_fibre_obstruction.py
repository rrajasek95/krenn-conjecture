#!/usr/bin/env python3
"""Audit the seven-fibre obstruction to padding the rational binary source.

All thirteen cells in ``BINARY_SUPPORT`` and all four cells in
``THIRD_MATCHING`` are assumed nonzero.  Every other cell whose two endpoint
colours lie in {0,1} is zero, while cells involving colour 2 are arbitrary.
Six mixed colourings then force six colour-2 cells to vanish.  A seventh
mixed colouring has a nonzero seed monomial, and every possible cancellation
mate contains one of those six forced-zero cells.

The verifier exhausts all 105 perfect matchings for each of the seven
colourings.  It is support-only and therefore valid over every field and for
arbitrary nonzero weights on the fixed cells.
"""

from __future__ import annotations

from itertools import combinations


N = 8

BINARY_SUPPORT = frozenset({
    (0, 1, 0, 0), (0, 1, 1, 0),
    (2, 3, 0, 0), (1, 3, 0, 0), (0, 2, 1, 0),
    (0, 5, 1, 1), (1, 2, 1, 1), (3, 4, 1, 1),
    (0, 4, 1, 1), (3, 5, 1, 1),
    (4, 6, 0, 0), (5, 7, 0, 0), (6, 7, 1, 1),
})

THIRD_MATCHING = frozenset({
    (0, 3, 2, 2), (1, 2, 2, 2),
    (4, 7, 2, 2), (5, 6, 2, 2),
})

SEED = BINARY_SUPPORT | THIRD_MATCHING


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


MATCHINGS = tuple(perfect_matchings(tuple(range(N))))


def decorated_term(colouring: tuple[int, ...], matching):
    return frozenset(
        (u, v, colouring[u], colouring[v]) for u, v in matching
    )


def compatible_with_fixed_binary_zero_pattern(term) -> bool:
    return all(
        not (left < 2 and right < 2) or cell in BINARY_SUPPORT
        for cell in term
        for _u, _v, left, right in (cell,)
    )


def viable_terms(colouring: tuple[int, ...]):
    return tuple(
        (number, decorated_term(colouring, matching))
        for number, matching in enumerate(MATCHINGS)
        if compatible_with_fixed_binary_zero_pattern(
            decorated_term(colouring, matching)
        )
    )


def word(text: str) -> tuple[int, ...]:
    answer = tuple(map(int, text))
    assert len(answer) == N
    return answer


def main() -> None:
    assert len(MATCHINGS) == 105
    assert len(BINARY_SUPPORT) == 13
    assert len(THIRD_MATCHING) == 4

    # Each row has exactly one matching compatible with the fixed binary
    # zero pattern.  All but the displayed cell lie in the nonzero seed, so
    # vanishing of that mixed coefficient forces the displayed cell to zero.
    forcing_rows = (
        ("00120000", 1, (2, 3, 1, 2)),
        ("11020000", 16, (1, 3, 1, 2)),
        ("11120100", 62, (3, 7, 2, 0)),
        ("11120111", 60, (3, 4, 2, 0)),
        ("11121000", 46, (3, 6, 2, 0)),
        ("11121011", 45, (3, 5, 2, 0)),
    )
    forced_zero = set()
    for text, expected_number, killed_cell in forcing_rows:
        terms = viable_terms(word(text))
        assert len(terms) == 1
        number, term = terms[0]
        assert number == expected_number
        assert term - SEED == {killed_cell}
        assert term - {killed_cell} <= SEED
        forced_zero.add(killed_cell)

    assert len(forced_zero) == 6

    # The final mixed coefficient has seven combinatorially possible terms.
    # Matching 31 is wholly supported on the fixed nonzero seed.  Every other
    # term contains one of the six cells already forced to zero.
    final_terms = viable_terms(word("21120000"))
    assert [number for number, _term in final_terms] == [1, 16, 31, 46, 62, 75, 91]
    base_terms = [term for number, term in final_terms if number == 31]
    assert len(base_terms) == 1
    assert base_terms[0] <= SEED
    for number, term in final_terms:
        if number != 31:
            assert term & forced_zero

    print("seven-fibre binary-padding obstruction: PASS")
    print("forced zero cells:", sorted(forced_zero))
    print("final viable matching numbers:", [n for n, _term in final_terms])


if __name__ == "__main__":
    main()
