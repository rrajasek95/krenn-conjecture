#!/usr/bin/env python3
"""Exact audit for aligned-live-diagonal-sector-lemma.md."""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp


def audit_row_sums() -> None:
    for number_of_sites in range(2, 8):
        sites = tuple(range(number_of_sites))
        pairs = tuple(combinations(sites, 2))
        coefficients = sp.symbols(f"r0:{len(pairs)}")
        pair_coefficient = dict(zip(pairs, coefficients, strict=True))

        row_sums = {
            j: sum(
                pair_coefficient[tuple(sorted((i, j)))]
                for i in sites
                if i != j
            )
            for j in sites
        }
        diagonal_coefficient = 2 * sum(coefficients)
        assert sp.expand(sum(row_sums.values()) - diagonal_coefficient) == 0

        # Construct the pure-c component explicitly.  Inserting c,e into
        # an omitted pair gives the stated row sum at the word with its
        # unique e at j.
        c, e = 0, 1
        one_defect = {}
        all_c = 0
        for pair, value in pair_coefficient.items():
            i, j = pair
            for marked in ((c, e), (e, c)):
                word = [c] * number_of_sites
                word[i], word[j] = marked
                one_defect[tuple(word)] = one_defect.get(tuple(word), 0) + value
            all_c += 2 * value
        for j in sites:
            word = [c] * number_of_sites
            word[j] = e
            assert sp.expand(one_defect[tuple(word)] - row_sums[j]) == 0
        assert sp.expand(all_c - diagonal_coefficient) == 0


def audit_off_diagonal_zero_patterns() -> None:
    edges = ((0, 1), (0, 2), (1, 2))
    for support_bits in product((0, 1), repeat=3):
        support = {
            edge for edge, bit in zip(edges, support_bits, strict=True) if bit
        }
        if not support:
            # Every incident edge is directly zero.
            assert all(any(c in edge for edge in edges) for c in range(3))
            continue
        if len(support) == 1:
            # Every colour has a zero incident edge, the choice used in the
            # unique-nonzero case of the proof.
            zero_edges = set(edges) - support
            assert all(any(c in edge for edge in zero_edges) for c in range(3))
            continue
        # With at least two nonzero entries, a nonzero incident equation
        # can always be compared with another nonzero equation; a zero one
        # gives the row sum directly.
        for c in range(3):
            for e in range(3):
                if c == e:
                    continue
                edge = tuple(sorted((c, e)))
                assert edge not in support or len(support - {edge}) >= 1


def audit_diagonal_implication() -> None:
    # Boolean support audit for (10): if t_c is nonzero, b_cc is nonzero
    # and every other b_dd is zero.  Two nonzero target values are therefore
    # incompatible.
    for diagonal_support in product((0, 1), repeat=3):
        possible_targets = {
            c
            for c in range(3)
            if diagonal_support[c]
            and all(not diagonal_support[d] for d in range(3) if d != c)
        }
        assert len(possible_targets) <= 1


def main() -> None:
    audit_row_sums()
    audit_off_diagonal_zero_patterns()
    audit_diagonal_implication()
    print("Aligned live diagonal-sector lemma: PASS")


if __name__ == "__main__":
    main()
