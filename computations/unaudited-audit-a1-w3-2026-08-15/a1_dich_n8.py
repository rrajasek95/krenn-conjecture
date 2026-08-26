"""AUDIT A1 -- denser n=8 sweep of the A.1 dichotomy (exact)."""

from __future__ import annotations

import itertools
import random

from a1_core import COLS, all_cells
from a1_dichotomy import classify, random_support

if __name__ == "__main__":
    print("AUDIT A1 -- n=8 dichotomy sweep (exact simplex)")
    rng = random.Random(4242)
    for dens in (0.10, 0.20, 0.35, 0.60):
        tally = {}
        for _ in range(8):
            S = random_support(8, rng, dens)
            tag, _ = classify(8, S)
            tally[tag] = tally.get(tag, 0) + 1
        print(f"  density={dens}: {tally}")

    # structured: 'anchor charts' -- one diagonal cell per edge of a random
    # 18-edge min-degree-3 graph, 3-coloured (the band objects W3 uses)
    E = list(itertools.combinations(range(8), 2))
    tally = {}
    for _ in range(12):
        while True:
            es = rng.sample(E, 18)
            deg = [0] * 8
            for u, v in es:
                deg[u] += 1
                deg[v] += 1
            if min(deg) >= 3:
                break
        S = frozenset((u, v, c, c) for (u, v), c in
                      zip(es, [rng.randrange(3) for _ in es]))
        tag, _ = classify(8, S)
        tally[tag] = tally.get(tag, 0) + 1
    print(f"  anchor charts |E|=18, min-deg>=3: {tally}")

    # full support
    tag, _ = classify(8, frozenset(all_cells(8)))
    print(f"  FULL 252-cell support: {tag}")
    tag, _ = classify(6, frozenset(all_cells(6)))
    print(f"  n=6 FULL 135-cell support: {tag}")
