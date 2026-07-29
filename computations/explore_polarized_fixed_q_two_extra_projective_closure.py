#!/usr/bin/env python3
"""Projective singleton closure for polarized two-extra-cell families.

Discovery only.  Enumerate all unordered pairs of the 99 individually
z-invisible cells.  Retain precisely those with z*e*f*q=0, so the same z
keeps the polarized target for arbitrary nonzero parameters t,u.  For each
family, derive literal monomial singleton Gram zeros and branch on the pure
Gram contributors, then apply the exact two-dimensional projective parity
criterion.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product

from explore_polarized_fixed_q_two_extra_frontier import cross_debt
from verify_polarized_eight_site_single_invisible_cell_projective_closure_independent import (
    ALL_CELLS,
    BASE_Q,
    COLOURS,
    DELTA_WORDS,
    DISPLAYED_Z,
    PURE_WORDS,
    cells_are_disjoint,
    normalized_gram_edge,
    partial_word,
    polarized_derivative,
    projective_certificate,
)


def forms(extra_left, extra_right):
    weighted = tuple((cell, 0) for cell in BASE_Q) + (
        (extra_left, 1), (extra_right, 2),
    )
    f = defaultdict(Counter)
    for chosen in combinations(weighted, 3):
        cells = tuple(cell for cell, _tag in chosen)
        if not cells_are_disjoint(cells):
            continue
        tag = 0
        for _cell, item_tag in chosen:
            tag |= item_tag
        base = partial_word(cells)
        missing = tuple(index for index, value in enumerate(base) if value == -1)
        assert len(missing) == 2
        for first_colour, second_colour in product(COLOURS, repeat=2):
            word = list(base)
            word[missing[0]] = first_colour
            word[missing[1]] = second_colour
            edge = normalized_gram_edge(
                (missing[0], first_colour), (missing[1], second_colour)
            )
            f[tuple(word)][edge, tag] += 1

    q4 = defaultdict(Counter)
    for chosen in combinations(weighted, 4):
        cells = tuple(cell for cell, _tag in chosen)
        if not cells_are_disjoint(cells):
            continue
        tag = 0
        for _cell, item_tag in chosen:
            tag |= item_tag
        word = tuple(partial_word(cells))
        assert -1 not in word
        q4[word][tag] += 1
    return dict(f), dict(q4)


def singleton_zeros(f, q4):
    zeros = set()
    for word, terms in f.items():
        if word in DELTA_WORDS or q4.get(word) or len(terms) != 1:
            continue
        (edge, _tag), coefficient = next(iter(terms.items()))
        assert coefficient > 0
        zeros.add(edge)
    return frozenset(zeros)


def pure_options(f, q4):
    options = []
    for word in PURE_WORDS:
        if q4.get(word):
            return None
        edges = tuple(sorted({edge for edge, _tag in f.get(word, {})}))
        if not edges:
            return None
        options.append(edges)
    return tuple(options)


def closes(extra_left, extra_right):
    f, q4 = forms(extra_left, extra_right)
    options = pure_options(f, q4)
    if options is None:
        return False, 0, "pure_direct"
    zeros = singleton_zeros(f, q4)
    branches = 0
    for required in product(*options):
        branches += 1
        certificate, _restricted = projective_certificate(required, zeros)
        if certificate is None:
            return False, branches, "open_branch"
    return True, branches, "closed"


def main():
    invisible = tuple(cell for cell in ALL_CELLS if not polarized_derivative(cell))
    assert len(invisible) == 99
    compatible = tuple(
        (left, right) for left, right in combinations(invisible, 2)
        if not cross_debt(left, right)
    )
    assert len(compatible) == 3960

    ledger = Counter()
    branch_hist = Counter()
    survivors = []
    for left, right in compatible:
        closed, branches, reason = closes(left, right)
        same_pair = left[:2] == right[:2]
        overlap = len(set(left[:2]) & set(right[:2]))
        kind = (
            "dd" if left[2] == left[3] and right[2] == right[3]
            else "aa" if left[2] != left[3] and right[2] != right[3]
            else "da"
        )
        ledger[closed, same_pair, overlap, kind, reason] += 1
        branch_hist[branches] += 1
        if not closed:
            survivors.append((left, right, reason, branches))

    print("two-extra projective reconnaissance: PASS")
    print("compatible pairs:", len(compatible))
    print("closed / open:",
          sum(count for key, count in ledger.items() if key[0]),
          len(survivors))
    print("branch histogram:", dict(sorted(branch_hist.items())))
    print("ledger:")
    for key, count in sorted(ledger.items(), key=lambda item: repr(item[0])):
        print(key, count)
    print("first 40 survivors:")
    for survivor in survivors[:40]:
        print(survivor)


if __name__ == "__main__":
    main()
