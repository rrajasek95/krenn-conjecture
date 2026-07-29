#!/usr/bin/env python3
"""Direct exact audit of the ten-orbit joint-C3 F3 near-realization.

The point realizes all three pure coefficients and kills every mixed
coefficient except one coupled C3 orbit of three colourings.  It is not a
counterexample; the verifier records the exact singleton obstruction that an
extension would have to cancel.
"""

from itertools import product

import search_f3_c3_equivariant_n8 as core


ENTRIES = tuple(map(int, (
    "1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,"
    "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,"
    "0,0,0,1,1,2,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0"
).split(",")))

BAD_REPRESENTATIVE_INDEX = 68
BAD_REPRESENTATIVE = (0, 0, 0, 0, 2, 1, 1, 2)


def supported_terms(colouring):
    answer = []
    for matching in core.MATCHINGS:
        values = tuple(
            ENTRIES[core.CELL_TO_INDEX[(u, v, colouring[u], colouring[v])]]
            for u, v in matching
        )
        if all(values):
            product_value = 1
            for value in values:
                product_value = product_value * value % core.Q
            answer.append((matching, values, product_value))
    return tuple(answer)


def main():
    assert len(ENTRIES) == len(core.CELL_KEYS) == 84
    nonzero = tuple(index for index, value in enumerate(ENTRIES) if value)
    assert len(nonzero) == 10
    assert core.COLOURING_REPS[BAD_REPRESENTATIVE_INDEX] == BAD_REPRESENTATIVE

    bad = []
    for colouring in product(range(core.Q), repeat=core.N):
        obtained = core.evaluate_direct(ENTRIES, colouring)
        expected = 1 if len(set(colouring)) == 1 else 0
        if obtained != expected:
            bad.append((colouring, obtained, expected))
    expected_bad_colourings = set(core.colouring_orbit(BAD_REPRESENTATIVE))
    assert {colouring for colouring, _obtained, _expected in bad} == expected_bad_colourings
    assert all(obtained == 1 and expected == 0
               for _colouring, obtained, expected in bad)

    pure_terms = supported_terms((0,) * core.N)
    assert pure_terms == ((
        core.PURE_MATCHING_REPS[1], (1, 1, 1, 1), 1,
    ),)
    bad_terms = supported_terms(BAD_REPRESENTATIVE)
    assert len(bad_terms) == 1 and bad_terms[0][2] == 1

    # The orbit-reduced evaluator independently has exactly the same lone
    # bad representative.
    bad_representatives = tuple(
        index
        for index, terms in enumerate(core.REPRESENTATIVE_TERMS)
        if core.evaluate_terms(ENTRIES, terms) != core.TARGETS[index]
    )
    assert bad_representatives == (BAD_REPRESENTATIVE_INDEX,)
    print(
        "PASS ten-cell F3 C3 near-point: pure orbit exact, "
        "2186/2187 representative coefficients exact, one mixed C3 orbit "
        f"({len(bad)} raw colourings) has a singleton value-1 term; "
        f"nonzero_cell_indices={nonzero}"
    )


if __name__ == "__main__":
    main()
