"""AUDIT A1 / claim 4 -- try to extend the 13-cell witness core to a support
on which BOTH of W3's modulus mechanisms are silent (no singleton mixed
fibre = M9 silent, all three pure rows live = M8 silent), while leaving the
four core fibres untouched.

Cells that are live for one of the four core words are FORBIDDEN additions,
so the core fibres can never grow and the forcing derivation survives.
"""

from __future__ import annotations

import random
import sys

from a1_core import cellkey
from a1_phase import fibres, is_mixed, perfect_matchings

N = 8
CORE = frozenset({
    (0, 1, 0, 1), (1, 2, 1, 0), (2, 3, 0, 1), (3, 4, 1, 0), (4, 5, 0, 1),
    (5, 6, 1, 0), (6, 7, 0, 1), (0, 7, 0, 1), (0, 4, 0, 0), (2, 6, 0, 0),
    (0, 3, 0, 1), (3, 7, 0, 0), (1, 5, 0, 0),
})
CORE_WORDS = [
    (0, 1, 0, 1, 0, 1, 0, 1),
    (0, 1, 0, 0, 0, 1, 0, 0),
    (0, 0, 0, 1, 0, 0, 0, 1),
    (0,) * 8,
]
MS = list(perfect_matchings(tuple(range(N))))


def forbidden(cell):
    u, v, i, j = cell
    for w in CORE_WORDS:
        if w[u] == i and w[v] == j:
            return True
    return False


def repair(S, rng, budget=120):
    S = set(S)
    for _ in range(budget):
        fib = fibres(N, S)
        bad = [(w, t) for w, t in fib.items() if is_mixed(w) and len(t) == 1]
        missing = [c for c in range(3) if (c,) * N not in fib]
        if not bad and not missing:
            return frozenset(S), fib, True
        if missing:
            c = missing[0]
            M = rng.choice(MS)
            new = {cellkey(u, v, c, c) for (u, v) in M}
            if any(forbidden(k) for k in new):
                continue
            S |= new
            continue
        w, terms = rng.choice(bad)
        cur = set(terms[0])
        cands = []
        for M in MS:
            ks = frozenset(cellkey(u, v, w[u], w[v]) for (u, v) in M)
            if ks == cur or any(forbidden(k) for k in ks - S):
                continue
            cands.append((len(ks - S), ks - S))
        if not cands:
            return frozenset(S), fib, False
        cands.sort(key=lambda t: t[0])
        S |= rng.choice(cands[: max(1, min(4, len(cands)))])[1]
        if len(S) > 130:
            return frozenset(S), fibres(N, S), False
    return frozenset(S), fibres(N, S), False


if __name__ == "__main__":
    best = None
    for seed in range(int(sys.argv[1]) if len(sys.argv) > 1 else 40):
        rng = random.Random(seed)
        S, fib, ok = repair(CORE, rng)
        nsing = sum(1 for w, t in fib.items() if is_mixed(w) and len(t) == 1)
        npure = sum(1 for w in fib if not is_mixed(w))
        core_ok = all(len(fib.get(w, [])) == n_
                      for w, n_ in zip(CORE_WORDS, (3, 2, 2, 1)))
        if ok and core_ok:
            print(f"seed {seed}: SUCCESS |S|={len(S)} pures={npure} "
                  f"singletons={nsing} core intact={core_ok}")
            best = S
            break
        print(f"seed {seed}: |S|={len(S)} pures={npure} singletons={nsing} "
              f"core={core_ok} done={ok}")
    if best:
        print("SUPPORT:")
        for s in sorted(best):
            print("   ", s, "(core)" if s in CORE else "")
