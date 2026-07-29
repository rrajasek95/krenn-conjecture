#!/usr/bin/env python3
"""Support-only Gram reconnaissance for a full invisible physical block.

For each of the eleven physical pairs on which every endpoint-colour cell
is invisible to z*(-)*q^[2], replace the zero q-block by an arbitrary 3x3
matrix.  On each nonzero support stratum, use only literal singleton mixed
coordinates and a branch on contributors to the three pure coordinates.
The calculation reports which support masks are already contradictory by
the elementary two-dimensional orthogonality closure.

This is a discovery script; a promoted theorem would require a standalone
certificate replay and an independent audit.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import product

from explore_polarized_fixed_q_one_extra_rank_constraints import (
    COLOURS,
    Q0,
    SELECTED_WORDS,
    f_map,
    orthogonality_closes,
    q4_map,
    z_times_extra_q2,
)


INVISIBLE_PAIRS = (
    (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
    (1, 2), (1, 3), (1, 5), (1, 7), (2, 5), (3, 4),
)


def base_maps():
    # Use an arbitrary absent cell and retain only its exponent-zero terms.
    fmap = f_map((0, 3, 0, 0))
    qmap = q4_map((0, 3, 0, 0))
    base_f = {
        word: tuple((entry, "base") for entry, exp in contributors if exp == 0)
        for word, contributors in fmap.items()
    }
    base_f = {word: terms for word, terms in base_f.items() if terms}
    base_q = {word for word, exponents in qmap.items() if exponents.get(0)}
    return base_f, base_q


def cell_variations(cell):
    fmap = f_map(cell)
    qmap = q4_map(cell)
    vf = {
        word: tuple((entry, cell) for entry, exp in contributors if exp == 1)
        for word, contributors in fmap.items()
    }
    vf = {word: terms for word, terms in vf.items() if terms}
    vq = {word for word, exponents in qmap.items() if exponents.get(1)}
    return vf, vq


def merge_maps(base_f, base_q, active, variations):
    fmap = defaultdict(list)
    for word, terms in base_f.items():
        fmap[word].extend(terms)
    qsupport = set(base_q)
    for cell in active:
        vf, vq = variations[cell]
        for word, terms in vf.items():
            fmap[word].extend(terms)
        qsupport.update(vq)
    return dict(fmap), qsupport


def singleton_zero_edges(fmap, qsupport):
    edges = set()
    for word, contributors in fmap.items():
        if len(set(word)) == 1 or word in qsupport or len(contributors) != 1:
            continue
        edges.add(contributors[0][0])
    return edges


def mask_closes(fmap, qsupport):
    pure_options = []
    for word in SELECTED_WORDS[:3]:
        # q^[4] must not contaminate a pure coordinate.  If it does, the
        # support-only branch argument deliberately refuses to certify it.
        if word in qsupport:
            return False, 0
        entries = tuple(entry for entry, _ in fmap.get(word, ()))
        if not entries:
            return False, 0
        pure_options.append(entries)
    zeros = singleton_zero_edges(fmap, qsupport)
    branches = 0
    for selected in product(*pure_options):
        branches += 1
        if not orthogonality_closes(list(selected), zeros):
            return False, branches
    return True, branches


def main():
    base_f, base_q = base_maps()
    global_hist = Counter()
    survivor_examples = {}
    for pair in INVISIBLE_PAIRS:
        cells = tuple((pair[0], pair[1], cu, cv)
                      for cu in COLOURS for cv in COLOURS)
        assert all(not z_times_extra_q2(cell) for cell in cells)
        variations = {cell: cell_variations(cell) for cell in cells}
        pair_hist = Counter()
        survivors = []
        total_branches = 0
        for mask in range(1 << 9):
            active = tuple(cell for index, cell in enumerate(cells)
                           if mask & (1 << index))
            fmap, qsupport = merge_maps(base_f, base_q, active, variations)
            closes, branches = mask_closes(fmap, qsupport)
            total_branches += branches
            pair_hist["closed" if closes else "open"] += 1
            if not closes:
                survivors.append(mask)
        global_hist.update(pair_hist)
        survivor_examples[pair] = tuple(survivors[:12])
        print(pair, dict(pair_hist), "branches", total_branches,
              "first open masks", survivors[:12])
        if survivors:
            bit_counts = [sum(bool(mask & (1 << bit)) for mask in survivors)
                          for bit in range(9)]
            minimal = [mask for mask in survivors if not any(
                other != mask and (other & mask) == other for other in survivors
            )]
            print(" bit counts", bit_counts, "minimal open", minimal)
    print("full invisible-block support reconnaissance: PASS")
    print("global mask ledger:", dict(global_hist))
    print("pairs fully closed:",
          sum(1 for pair in INVISIBLE_PAIRS if not survivor_examples[pair]),
          "/", len(INVISIBLE_PAIRS))


if __name__ == "__main__":
    main()
