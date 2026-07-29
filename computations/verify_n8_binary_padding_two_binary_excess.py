#!/usr/bin/env python3
"""Classify and obstruct every two-cell binary excess above the n=8 seed.

There are C(99,2)=4,851 choices for two nonzero principal 0/1 cells outside
the fixed thirteen-cell binary support.  Exact unique-monomial propagation
rules out 4,850 choices for arbitrary values/support involving colour 2.
The sole exception is the alternate pure-0 matching cells 47;00 and 56;00.
Seven explicitly checked fibres rule out that exception algebraically.

No SAT solver and no floating-point computation is used.  The result is
valid over every field (and the final bracket argument only needs a field's
no-zero-divisors property).
"""

from __future__ import annotations

from itertools import combinations, product

from verify_n8_binary_padding_one_binary_excess import (
    ABSENT_BINARY_CELLS,
    PROPAGATION_WORDS,
)
from verify_n8_binary_padding_seven_fibre_obstruction import (
    BINARY_SUPPORT,
    MATCHINGS,
    N,
    SEED,
    decorated_term,
)


ALL_CELLS = tuple(
    (u, v, left, right)
    for u, v in combinations(range(N), 2)
    for left, right in product(range(3), repeat=2)
)
CELL_INDEX = {cell: index for index, cell in enumerate(ALL_CELLS)}


def cell_mask(cells) -> int:
    return sum(1 << CELL_INDEX[cell] for cell in cells)


ABSENT_BINARY_MASK = cell_mask(ABSENT_BINARY_CELLS)
SEED_MASK = cell_mask(SEED)


def word(text: str) -> tuple[int, ...]:
    answer = tuple(map(int, text))
    assert len(answer) == N and len(set(answer)) > 1
    return answer


def term_masks(colouring: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        cell_mask(decorated_term(colouring, matching))
        for matching in MATCHINGS
    )


FIRST_STAGE_ROWS = tuple(
    (text, term_masks(word(text))) for text in PROPAGATION_WORDS
)


def propagate(extra_binary_cells, rows):
    """Run exact sole-monomial propagation; return contradiction, trace."""

    extra_mask = cell_mask(extra_binary_cells)
    known_zero = ABSENT_BINARY_MASK & ~extra_mask
    known_nonzero = SEED_MASK | extra_mask
    proof = []
    while True:
        progressed = False
        for text, terms in rows:
            viable_number = None
            number_viable = 0
            for number, term in enumerate(terms):
                if not term & known_zero:
                    viable_number = number
                    number_viable += 1
            if number_viable != 1:
                continue
            term = terms[viable_number]
            unknown = term & ~known_nonzero
            if not unknown:
                proof.append((text, viable_number, None))
                return True, proof
            if unknown.bit_count() == 1:
                known_zero |= unknown
                proof.append((text, viable_number, unknown))
                progressed = True
                break
        if not progressed:
            return False, proof


EXCEPTIONAL_PAIR = (
    (4, 7, 0, 0),
    (5, 6, 0, 0),
)


def viable_terms(text: str):
    colouring = word(text)
    allowed_binary = BINARY_SUPPORT | frozenset(EXCEPTIONAL_PAIR)
    forbidden_binary = ABSENT_BINARY_CELLS - set(EXCEPTIONAL_PAIR)
    return tuple(
        (number, decorated_term(colouring, matching))
        for number, matching in enumerate(MATCHINGS)
        if not decorated_term(colouring, matching) & forbidden_binary
    )


def audit_exceptional_pair() -> None:
    """Check the seven-fibre common-bracket contradiction exactly."""

    bottom_first = frozenset({(4, 6, 0, 0), (5, 7, 0, 0)})
    bottom_second = frozenset({(4, 7, 0, 0), (5, 6, 0, 0)})
    assert bottom_first <= SEED
    assert bottom_second == frozenset(EXCEPTIONAL_PAIR)

    # The pure-0 coefficient is a nonzero seed factor times
    # B = x46;00*x57;00 + x47;00*x56;00.  Hence B is nonzero in an
    # exact realization.
    pure_terms = tuple(
        (number, decorated_term((0,) * N, matching))
        for number, matching in enumerate(MATCHINGS)
        if not decorated_term((0,) * N, matching)
        & (ABSENT_BINARY_CELLS - set(EXCEPTIONAL_PAIR))
    )
    assert [number for number, _term in pure_terms] == [1, 2]
    pure_common = frozenset({(0, 1, 0, 0), (2, 3, 0, 0)})
    assert pure_terms[0][1] == pure_common | bottom_first
    assert pure_terms[1][1] == pure_common | bottom_second
    assert pure_common <= SEED

    # Two mixed equations are a nonzero/unknown upper factor times the same
    # bracket B.  Since B is nonzero, they force 23;12 and 13;12 to zero.
    product_rows = (
        ("00120000", (1, 2),
         frozenset({(0, 1, 0, 0), (2, 3, 1, 2)}),
         (2, 3, 1, 2)),
        ("11020000", (16, 17),
         frozenset({(0, 2, 1, 0), (1, 3, 1, 2)}),
         (1, 3, 1, 2)),
    )
    forced_zero = set()
    for text, numbers, common, killed_cell in product_rows:
        terms = viable_terms(text)
        assert tuple(number for number, _term in terms) == numbers
        assert terms[0][1] == common | bottom_first
        assert terms[1][1] == common | bottom_second
        assert common - {killed_cell} <= SEED
        forced_zero.add(killed_cell)

    # Four unique-monomial fibres force four further cells to zero.
    singleton_rows = (
        ("11120111", 60, (3, 4, 2, 0)),
        ("11121011", 45, (3, 5, 2, 0)),
        ("21110111", 45, (0, 4, 2, 0)),
        ("21111011", 60, (0, 5, 2, 0)),
    )
    for text, expected_number, killed_cell in singleton_rows:
        terms = viable_terms(text)
        assert len(terms) == 1
        number, term = terms[0]
        assert number == expected_number
        assert term - {killed_cell} <= SEED
        forced_zero.add(killed_cell)
    assert len(forced_zero) == 6

    # In the last fibre, terms 31 and 32 are a nonzero seed factor times B.
    # Every other combinatorially viable term contains a forced-zero cell.
    final_terms = viable_terms("21120000")
    assert [number for number, _term in final_terms] == [
        1, 2, 16, 17, 31, 32, 46, 47, 61, 62, 75, 76, 90, 91
    ]
    final_common = frozenset({(0, 3, 2, 2), (1, 2, 1, 1)})
    assert final_common <= SEED
    for number, term in final_terms:
        if number == 31:
            assert term == final_common | bottom_first
        elif number == 32:
            assert term == final_common | bottom_second
        else:
            assert term & forced_zero


def main() -> None:
    assert len(ALL_CELLS) == 252
    assert len(ABSENT_BINARY_CELLS) == 99
    pairs = tuple(combinations(sorted(ABSENT_BINARY_CELLS), 2))
    assert len(pairs) == 4851

    first_stage_unresolved = []
    for pair in pairs:
        contradiction, _proof = propagate(pair, FIRST_STAGE_ROWS)
        if not contradiction:
            first_stage_unresolved.append(pair)
    assert len(first_stage_unresolved) == 39

    all_mixed_rows = tuple(
        ("".join(map(str, colouring)), term_masks(colouring))
        for colouring in product(range(3), repeat=N)
        if len(set(colouring)) > 1
    )
    assert len(all_mixed_rows) == 6558
    unresolved = []
    for pair in first_stage_unresolved:
        contradiction, _proof = propagate(pair, all_mixed_rows)
        if not contradiction:
            unresolved.append(pair)
    assert unresolved == [EXCEPTIONAL_PAIR]

    audit_exceptional_pair()
    print(
        "two-binary-cell padding obstruction: PASS; "
        "pairs=4851 first_stage_resolved=4812 second_stage_resolved=38 "
        f"exception={EXCEPTIONAL_PAIR} algebraically_obstructed=True"
    )


if __name__ == "__main__":
    main()
