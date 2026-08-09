#!/usr/bin/env python3
"""Straighten every diagonal two-centre Koszul bridge to a target axis.

Let q contain only cells with equal endpoint colours.  Every word in a
four-site cofactor K_x then has even multiplicity in each colour.  A
minimal two-centre syzygy factors as

    K_0 = u_1 tensor Z,    K_1 = u_0 tensor Z.

For any nonzero word z of Z, even parity of K_0 forces u_1 to have exactly
one nonzero colour coordinate.  Even parity of K_1 does the same to u_0,
and the common word z forces the two coordinates to be equal.  Therefore
there are no tilted two-centre bridges in the colour-diagonal chart.

This checker exhausts the nonempty endpoint supports and all 27 words of
the common three-site tensor.  The argument is coefficient-independent.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product
import json


COLOURS = tuple(range(3))
EXPECTED_DIGEST = "5e2fc95b578336003d1c63e5a44a41c3edfc9175317c546810db03462245b4fa"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def nonempty_subsets(items):
    items = tuple(items)
    for size in range(1, len(items) + 1):
        yield from combinations(items, size)


def even_word(endpoint_colour, common_word):
    counts = [common_word.count(colour) for colour in COLOURS]
    counts[endpoint_colour] += 1
    return all(count % 2 == 0 for count in counts)


def factor_support_is_compatible(endpoint_support, common_word):
    # Every displayed coefficient u_colour * Z_word is nonzero over an
    # integral domain, so every colour in the factor support must pass.
    return all(even_word(colour, common_word)
               for colour in endpoint_support)


def audit():
    supports = tuple(nonempty_subsets(COLOURS))
    one_sided = []
    two_sided = []
    for common_word in product(COLOURS, repeat=3):
        for support_0 in supports:
            for support_1 in supports:
                # K_0=u_1 tensor Z constrains support_1.
                if not factor_support_is_compatible(
                        support_1, common_word):
                    continue
                one_sided.append((support_0, support_1, common_word))
                # K_1=u_0 tensor Z supplies the other parity constraint.
                if factor_support_is_compatible(
                        support_0, common_word):
                    two_sided.append((support_0, support_1, common_word))

    require(len(one_sided) == 147,
            "one-sided parity census changed")
    require(len(two_sided) == 21,
            "two-sided parity census changed")
    require(all(len(support_0) == len(support_1) == 1
                and support_0 == support_1
                for support_0, support_1, _word in two_sided),
            "a tilted two-centre factor survived both cofactors")

    # For a fixed common axis there are seven possible three-site words:
    # ddd, or a permutation of dee for either other colour e.
    axis_word_count = {
        axis: sum(support_0 == (axis,)
                  for support_0, _support_1, _word in two_sided)
        for axis in COLOURS
    }
    require(axis_word_count == {0: 7, 1: 7, 2: 7},
            "common-axis word census changed")

    # If a pure-t product selects a nonzero endpoint coordinate of this
    # bridge, its unique coordinate axis is t.  Audit this for every target.
    pure_target_cases = {}
    for target in COLOURS:
        selected = [record for record in two_sided
                    if target in record[0] or target in record[1]]
        require(len(selected) == 7,
                "pure target did not select exactly its axis stratum")
        require(all(record[0] == record[1] == (target,)
                    for record in selected),
                "pure target contribution came from a different axis")
        pure_target_cases[target] = len(selected)

    tilted_one_sided = sum(
        support_0 != support_1
        for support_0, support_1, _word in one_sided
    )
    require(tilted_one_sided == 126,
            "one-cofactor mutation census changed")

    ledger = {
        "colour_count": len(COLOURS),
        "common_word_count": len(COLOURS) ** 3,
        "nonempty_factor_support_count": len(supports),
        "one_sided_compatible": len(one_sided),
        "one_sided_tilted": tilted_one_sided,
        "two_sided_compatible": [
            {
                "support_0": list(support_0),
                "support_1": list(support_1),
                "common_word": list(common_word),
            }
            for support_0, support_1, common_word in two_sided
        ],
        "axis_word_count": axis_word_count,
        "pure_target_cases": pure_target_cases,
        "verdict": (
            "every minimal nonzero two-centre Koszul bridge of a "
            "colour-diagonal five-site quadratic has one common "
            "coordinate axis; a pure-t contribution forces axis t"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"two-centre parity ledger changed: {digest}")
    return digest


def main():
    digest = audit()
    print("two-centre parity straightening: PASS")
    print("one-sided / two-sided compatible strata: 147 / 21")
    print("two-sided strata: 7 words on each of 3 common axes")
    print("tilted bridges surviving both cofactor parities: 0")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
