"""AUDIT A1 / CLAIM 4 -- randomized singleton repair around the witness core,
looking for a singleton-free support where the general mixed system is
solvable (bounded moduli) but the unit-modulus one is not."""

from __future__ import annotations

import random
import sys

from a1_core import cellkey
from a1_phase import feasible, fibres, is_mixed, perfect_matchings
from a1_phase_witness import SUPPORT, N

MS = list(perfect_matchings(tuple(range(N))))


def add_repair_random(S, rng, max_steps=60):
    S = set(S)
    for _ in range(max_steps):
        fib = fibres(N, S)
        bad = [(w, t) for w, t in fib.items() if is_mixed(w) and len(t) == 1]
        if not bad:
            return frozenset(S), fib, True
        w, terms = rng.choice(bad)
        cur = set(terms[0])
        cands = []
        for M in MS:
            ks = frozenset(cellkey(u, v, w[u], w[v]) for (u, v) in M)
            if ks == cur:
                continue
            cands.append((len(ks - S), ks - S))
        if not cands:
            return frozenset(S), fib, False
        cands.sort(key=lambda t: t[0])
        pick = rng.choice(cands[: max(1, min(6, len(cands)))])
        S |= pick[1]
        if len(S) > 40:
            return frozenset(S), fibres(N, S), False
    return frozenset(S), fibres(N, S), False


if __name__ == "__main__":
    hits = []
    for seed in range(int(sys.argv[1]) if len(sys.argv) > 1 else 60):
        rng = random.Random(seed)
        S, fib, ok = add_repair_random(frozenset(SUPPORT), rng)
        if not ok:
            continue
        mixed = {w: t for w, t in fib.items() if is_mixed(w)}
        okU, resU, _ = feasible(N, S, fib, unit=True, tries=30, seed=seed)
        if okU:
            continue
        okG, resG, pG = feasible(N, S, fib, unit=False, tries=30, seed=seed)
        print(f"seed {seed:3d}: |S|={len(S):3d} fibres={len(mixed):3d} "
              f"unitOK={okU} ({resU:.2e})  genOK={okG} ({resG:.2e})"
              + ("   *** GAP ***" if okG and not okU else ""))
        if okG and not okU:
            hits.append((seed, S, fib))
            if len(hits) >= 3:
                break
    print(f"\n{len(hits)} gap witnesses found")
    for seed, S, fib in hits:
        print(f"--- seed {seed}: support ({len(S)} cells)")
        for s in sorted(S):
            print("   ", s)
        break
