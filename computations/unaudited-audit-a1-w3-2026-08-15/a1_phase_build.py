"""AUDIT A1 / CLAIM 4 -- build a singleton-free support around the witness
core, then compare general-modulus vs unit-modulus solvability.

Repair strategy: singleton mixed fibres are killed by ADDING cells (giving
the offending word a second live matching), never by deleting, so the
witness core survives.
"""

from __future__ import annotations

import itertools
import random
import sys

from a1_core import cellkey
from a1_phase import feasible, fibres, is_mixed, perfect_matchings
from a1_phase_witness import SUPPORT, N

MS = list(perfect_matchings(tuple(range(N))))


def add_repair(S, rng, max_steps=200, forbid=()):
    S = set(S)
    for step in range(max_steps):
        fib = fibres(N, S)
        bad = [(w, t) for w, t in fib.items() if is_mixed(w) and len(t) == 1]
        if not bad:
            return frozenset(S), fib, True
        w, terms = bad[0]
        cur = set(terms[0])
        best = None
        for M in MS:
            ks = frozenset(cellkey(u, v, w[u], w[v]) for (u, v) in M)
            if ks == cur:
                continue
            new = ks - S
            if any(k in forbid for k in new):
                continue
            if best is None or len(new) < len(best[1]):
                best = (ks, new)
        if best is None:
            return frozenset(S), fib, False
        S |= best[1]
    return frozenset(S), fibres(N, S), False


def structure(S):
    fib = fibres(N, S)
    mixed = {w: t for w, t in fib.items() if is_mixed(w)}
    pures = [w for w in fib if not is_mixed(w)]
    sizes = {}
    for w, t in mixed.items():
        sizes[len(t)] = sizes.get(len(t), 0) + 1
    return fib, mixed, pures, sizes


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    rng = random.Random(seed)
    S0 = frozenset(SUPPORT)
    S, fib, ok = add_repair(S0, rng)
    fib, mixed, pures, sizes = structure(S)
    print(f"repaired: |S|={len(S)} singleton-free={ok} mixed fibres={len(mixed)}"
          f" sizes={sizes} pure rows live={sorted(p[0] for p in pures)}")
    okU, resU, _ = feasible(N, S, fib, unit=True, tries=60, seed=1)
    okG, resG, pG = feasible(N, S, fib, unit=False, tries=60, seed=1)
    print(f"  unit-modulus mixed system feasible: {okU}  (best resid {resU:.3e})")
    print(f"  general      mixed system feasible: {okG}  (best resid {resG:.3e})")
    if okG and not okU:
        print("  *** GAP FOUND: general solvable, unit NOT ***")
    print("support:")
    for s in sorted(S):
        print("   ", s, "(core)" if s in S0 else "")
