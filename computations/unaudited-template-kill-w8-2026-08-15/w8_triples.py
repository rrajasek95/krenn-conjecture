#!/usr/bin/env python3
"""UNAUDITED PROBE (W8) -- orbits of ordered triples of perfect matchings of
K_8 under S_8 x S_3 (the constant-witness case split).

Pinned HEAD: a1196b4dca9f83452483734a3273c0c43d5cf3b5

Every admissible template supports at least one perfect matching in each of
the three diagonal graphs G_c = {e : cell (c,c) occupied}; choosing one gives
an ORDERED triple (W_0, W_1, W_2) of perfect matchings (they may share
edges -- unlike the R_cell case of the committed
computations/search_monomial_no_singleton_sat.py, a block may carry two or
three diagonal cells).  Fixing a triple orbit representative and forcing its
diagonal cells is a sound and complete case split.

Method: S_8 is transitive on perfect matchings, so put W_0 = (01)(23)(45)(67)
and quotient the remaining pair by Stab(W_0) (order 384) together with the
six colour permutations (which permute the roles of the three matchings).
"""

from __future__ import annotations

import json
import sys
from itertools import permutations, product

import w8_core as C


def stabilizer(size=8):
    half = size // 2
    out = []
    for pair_perm in permutations(range(half)):
        for flips in product(range(2), repeat=half):
            perm = [0] * size
            for pair in range(half):
                for bit in range(2):
                    perm[2 * pair + bit] = 2 * pair_perm[pair] + (bit ^ flips[pair])
            out.append(tuple(perm))
    return out


def matching_action(geo, perm):
    """index -> index map induced on perfect matchings."""
    lookup = {m: n for n, m in enumerate(geo.matchings)}
    out = []
    for matching in geo.matchings:
        image = tuple(sorted(tuple(sorted((perm[u], perm[v])))
                             for u, v in matching))
        out.append(lookup[image])
    return tuple(out)


def to_canonical_map(geo):
    """For each matching P, a permutation sending P to the canonical matching."""
    canonical = tuple((2 * k, 2 * k + 1) for k in range(4))
    out = []
    for matching in geo.matchings:
        perm = [0] * 8
        for k, (u, v) in enumerate(matching):
            perm[u], perm[v] = canonical[k]
        out.append(tuple(perm))
    return out


def orbits(geo):
    stab = stabilizer(8)
    stab_action = [matching_action(geo, p) for p in stab]
    to_can = [matching_action(geo, p) for p in to_canonical_map(geo)]
    canonical_index = geo.matchings.index(tuple((2 * k, 2 * k + 1)
                                                for k in range(4)))
    reps = {}
    for first in range(len(geo.matchings)):
        for second in range(len(geo.matchings)):
            triple = (canonical_index, first, second)
            best = None
            for order in permutations(range(3)):
                a, b, c = (triple[order[0]], triple[order[1]], triple[order[2]])
                move = to_can[a]
                b1, c1 = move[b], move[c]
                for action in stab_action:
                    key = (action[b1], action[c1])
                    if best is None or key < best:
                        best = key
            reps.setdefault(best, []).append((first, second))
    return reps


def main():
    geo = C.geometry(8)
    reps = orbits(geo)
    print(f"ordered PM triples with W_0 canonical: {105 * 105}")
    print(f"orbits under S_8 x S_3: {len(reps)}")
    rows = []
    for key, members in sorted(reps.items()):
        first, second = key
        shared01 = len(set(geo.matchings[0]) & set(geo.matchings[first]))
        rows.append({"rep": [0, first, second], "size": len(members),
                     "W1": geo.matchings[first], "W2": geo.matchings[second]})
    print("orbit sizes:", sorted({r['size'] for r in rows}))
    json.dump({"orbits": len(reps), "rows": rows},
              open("results_triples.json", "w"), indent=1, default=str)
    print("wrote results_triples.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
