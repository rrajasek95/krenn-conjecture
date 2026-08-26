#!/usr/bin/env python3
"""A3 Task 2 (second half) -- how far ABOVE the floor m = 3N/2 does the
singleton mechanism still kill every DIAGONAL monomial template?

For each support m we anneal over diagonal templates with exactly m live
edges and all three constant fibres nonempty, minimising the number of mixed
singleton fibres.  Support m is "singleton-clear" if the search finds a
template with 0 singletons (a real obstruction to the mechanism, certified
exactly by the product formula), and "singleton-forced (not falsified)"
otherwise.

N = 8 recalibrates against W6/W2 (their answer: diagonal templates are
singleton-free ONLY at full support 28).  N = 10 is the new measurement.
Exact throughout: fibre sizes are integers from the subset-DP product
formula  |fibre(c)| = prod_r pm(G_r[c^{-1}(r)]).
"""

from __future__ import annotations

import json
import math
import random
import sys
import time
from itertools import combinations

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from a3_core import DiagonalTemplate, colour_partitions


class Frame:
    def __init__(self, n):
        self.n = n
        self.edges = list(combinations(range(n), 2))
        self.parts = colour_partitions(n)
        # vectorised word table: masks and a 'constant word' flag
        self.m0 = np.array([p[1] for p in self.parts], dtype=np.int64)
        self.m1 = np.array([p[2] for p in self.parts], dtype=np.int64)
        self.m2 = np.array([p[3] for p in self.parts], dtype=np.int64)
        full = (1 << n) - 1
        self.constant = ((self.m0 == full) | (self.m1 == full)
                         | (self.m2 == full))
        self.mixed = ~self.constant
        self.full = full

    def score(self, colouring):
        """colouring[e] in {None,0,1,2}.  (score, singletons, pures)."""
        ce = [set(), set(), set()]
        for e, c in enumerate(colouring):
            if c is not None:
                ce[c].add(self.edges[e])
        if any(not s for s in ce):
            return 10 ** 6, None, [0, 0, 0]
        tpl = DiagonalTemplate(self.n, ce)
        p0 = np.array(tpl.pm[0], dtype=np.int64)
        p1 = np.array(tpl.pm[1], dtype=np.int64)
        p2 = np.array(tpl.pm[2], dtype=np.int64)
        size = p0[self.m0] * p1[self.m1] * p2[self.m2]
        pures = [int(p0[self.full]), int(p1[self.full]), int(p2[self.full])]
        s = int(np.count_nonzero((size == 1) & self.mixed))
        missing = sum(1 for p in pures if p == 0)
        return 50 * missing + s, s, pures


def anneal_at_support(fr, rng, m, steps, t0=8.0, t1=0.3):
    ne = len(fr.edges)
    live = rng.sample(range(ne), m)
    col = [None] * ne
    for e in live:
        col[e] = rng.randrange(3)
    cur, sing, pures = fr.score(col)
    best, best_state = cur, list(col)
    for t in range(steps):
        if best == 0:
            break
        temp = t0 * (t1 / t0) ** (t / max(1, steps - 1))
        if rng.random() < 0.5:
            e = rng.choice([i for i in range(ne) if col[i] is not None])
            old = col[e]
            col[e] = rng.randrange(3)
            if col[e] == old:
                continue
            back = (e, old)
        else:                                       # move a live edge
            on = [i for i in range(ne) if col[i] is not None]
            off = [i for i in range(ne) if col[i] is None]
            if not off:
                continue
            a, b = rng.choice(on), rng.choice(off)
            back = ("swap", a, b, col[a])
            col[b], col[a] = col[a], None
        val, sg, pu = fr.score(col)
        if val <= cur or rng.random() < math.exp(-min(60, (val - cur) / temp)):
            cur = val
            if val < best:
                best, best_state = val, list(col)
        else:
            if back[0] == "swap":
                _, a, b, c = back
                col[a], col[b] = c, None
            else:
                col[back[0]] = back[1]
    return best, best_state


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    steps = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    restarts = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    fr = Frame(n)
    rng = random.Random(20260815)
    full = n * (n - 1) // 2
    floor = 3 * n // 2
    rows = []
    t0 = time.time()
    for m in range(floor, full + 1):
        best = 10 ** 9
        state = None
        for _ in range(restarts):
            v, st = anneal_at_support(fr, rng, m, steps)
            if v < best:
                best, state = v, st
            if best == 0:
                break
        _, sg, pu = fr.score(state)
        rows.append(dict(m=m, best_score=best, singletons=sg, pures=pu,
                         singleton_free=(best == 0)))
        print(f"N={n} m={m:3d}: best score={best:5d} singletons={sg} "
              f"pures={pu}  {'<== SINGLETON-FREE' if best == 0 else ''}"
              f"  [{time.time()-t0:.0f}s]")
    clear = [r["m"] for r in rows if r["singleton_free"]]
    out = dict(N=n, steps=steps, restarts=restarts, floor=floor,
               full_support=full, rows=rows, singleton_free_supports=clear,
               seconds=round(time.time() - t0, 1))
    path = __file__.rsplit("/", 1)[0] + f"/results_reach_N{n}.json"
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"\nN={n}: singleton-free supports found = {clear}")
    print("wrote", path)


if __name__ == "__main__":
    main()
