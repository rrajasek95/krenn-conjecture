#!/usr/bin/env python3
"""Exact propagation proof for one-cell binary excess above the n=8 seed.

Keep the seventeen nonzero seed cells from the rational binary source plus
the chosen colour-2 matching.  At most one of the other 99 principal 0/1
cells may be nonzero; every cell involving colour 2 is otherwise arbitrary.

For each of the 100 cases (no extra binary cell, or one specified nonzero
extra cell), thirteen fixed mixed fibres suffice for the following exact
propagation.  If all but one matching in a mixed fibre contain an already
zero cell, and the remaining monomial has only one factor not already known
nonzero, that factor is forced to zero.  Every case reaches a fibre whose
sole possible monomial consists entirely of known nonzero factors.

The calculation uses only products and the fact that a field has no zero
divisors.  It is independent of the values/support of all other colour-2
cells and does not call a SAT solver.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product

from verify_n8_binary_padding_seven_fibre_obstruction import (
    BINARY_SUPPORT,
    MATCHINGS,
    N,
    SEED,
    decorated_term,
)


ALL_BINARY_CELLS = frozenset(
    (u, v, left, right)
    for u, v in combinations(range(N), 2)
    for left, right in product(range(2), repeat=2)
)
ABSENT_BINARY_CELLS = ALL_BINARY_CELLS - BINARY_SUPPORT

# This fixed list is an inclusion-minimal subset of an eighteen-fibre SAT
# core for the deterministic monomial propagation used below.
PROPAGATION_WORDS = (
    "00120000",
    "11020000",
    "11120100",
    "11120111",
    "11121000",
    "11121011",
    "20100000",
    "21000000",
    "21110100",
    "21110111",
    "21111000",
    "21111011",
    "21120000",
)


def word(text: str) -> tuple[int, ...]:
    answer = tuple(map(int, text))
    assert len(answer) == N and len(set(answer)) > 1
    return answer


TERMS = {
    text: tuple(decorated_term(word(text), matching) for matching in MATCHINGS)
    for text in PROPAGATION_WORDS
}


def propagate(extra_binary_cell):
    known_zero = set(ABSENT_BINARY_CELLS)
    known_nonzero = set(SEED)
    if extra_binary_cell is not None:
        known_zero.remove(extra_binary_cell)
        known_nonzero.add(extra_binary_cell)

    proof = []
    while True:
        progressed = False
        for text in PROPAGATION_WORDS:
            viable = tuple(
                (number, term)
                for number, term in enumerate(TERMS[text])
                if not term & known_zero
            )
            if len(viable) != 1:
                continue
            number, term = viable[0]
            unknown_factors = term - known_nonzero
            if not unknown_factors:
                proof.append((text, number, None))
                return proof
            if len(unknown_factors) == 1:
                forced_zero = next(iter(unknown_factors))
                assert forced_zero not in known_nonzero
                known_zero.add(forced_zero)
                proof.append((text, number, forced_zero))
                progressed = True
                break
        assert progressed, (
            "the claimed propagation certificate stalled",
            extra_binary_cell,
            proof,
        )


def main() -> None:
    assert len(ALL_BINARY_CELLS) == 112
    assert len(ABSENT_BINARY_CELLS) == 99
    assert len(PROPAGATION_WORDS) == 13
    assert all(len(terms) == 105 for terms in TERMS.values())

    lengths = Counter()
    cases = (None,) + tuple(sorted(ABSENT_BINARY_CELLS))
    for extra_binary_cell in cases:
        proof = propagate(extra_binary_cell)
        text, number, forced_zero = proof[-1]
        assert forced_zero is None
        assert text in PROPAGATION_WORDS
        assert 0 <= number < 105
        lengths[len(proof)] += 1

    assert lengths == {11: 10, 12: 12, 13: 78}
    print(
        "one-binary-cell padding obstruction: PASS; "
        f"cases={len(cases)} proof_lengths={dict(sorted(lengths.items()))}"
    )


if __name__ == "__main__":
    main()
