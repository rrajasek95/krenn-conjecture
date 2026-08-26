"""AUDIT A1 / claim 4 -- exploration: what do singleton-free supports look
like, and where should the general/unit gap live?

Counting heuristic (n sites, |S| cells, F nonempty mixed fibres):
  phase gauge acts by theta_s -> theta_s + phi_{u,i} + phi_{v,j}  (3n params)
  general system:  2|S| - 6n real unknowns vs 2F real equations
  unit system  :   |S|  - 3n real unknowns vs 2F real equations
so the interesting window is   (|S| - 3n)/2  <  F  <=  |S| - 3n.
"""

from __future__ import annotations

import random
import sys

from a1_phase import (
    fibres,
    gen_matching_union,
    gen_random,
    is_mixed,
    no_singleton_mixed,
    repair_singletons,
    feasible,
)

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 77)
    rows = []
    for trial in range(120):
        k = rng.randint(12, 48)
        S0 = gen_random(n, rng, k)
        S, fib = repair_singletons(n, S0, rng)
        if not no_singleton_mixed(fib):
            continue
        F = sum(1 for w, t in fib.items() if is_mixed(w))
        if F == 0:
            continue
        sizes = {}
        for w, t in fib.items():
            if is_mixed(w):
                sizes[len(t)] = sizes.get(len(t), 0) + 1
        rows.append((len(S), F, sizes))
    rows.sort(key=lambda r: -(r[1]))
    print(f"n={n}: {len(rows)} singleton-free supports")
    print(f"{'|S|':>5} {'F':>4}  window ((|S|-3n)/2, |S|-3n]   fibre sizes")
    for ls, F, sizes in rows[:25]:
        lo, hi = (ls - 3 * n) / 2, ls - 3 * n
        mark = "  <== IN WINDOW" if lo < F <= hi else ""
        print(f"{ls:5d} {F:4d}  ({lo:6.1f},{hi:5d}]   {sizes}{mark}")
