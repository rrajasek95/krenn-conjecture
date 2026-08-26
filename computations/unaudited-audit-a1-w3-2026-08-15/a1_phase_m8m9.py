"""AUDIT A1 / claim 4 -- strengthen the witness: can the 13-cell core be
embedded in a support on which BOTH of W3's mechanisms are silent
(M9: no singleton mixed fibre; M8: all three pure rows live)?

Start from the MAXIMAL core-preserving extension (every cell that is not
live for one of the four core words -- 207 cells) and delete non-core cells
to kill singletons, with an incremental fibre index so this is fast.
"""

from __future__ import annotations

import random
import sys

from a1_core import all_cells
from a1_phase import fibres, is_mixed
from a1_phase_certify import S as CORE

N = 8
CORE_WORDS = [
    (0, 1, 0, 1, 0, 1, 0, 1),
    (0, 1, 0, 0, 0, 1, 0, 0),
    (0, 0, 0, 1, 0, 0, 0, 1),
    (0,) * 8,
]
CORE_COUNTS = (3, 2, 2, 1)


def forbidden(c):
    u, v, i, j = c
    return any(w[u] == i and w[v] == j for w in CORE_WORDS)


def build():
    extra = [c for c in all_cells(N) if not forbidden(c)]
    S = frozenset(CORE) | frozenset(extra)
    fib = {w: [frozenset(t) for t in ts] for w, ts in fibres(N, S).items()}
    index = {}
    for w, ts in fib.items():
        for t in ts:
            for k in t:
                index.setdefault(k, []).append((w, t))
    return set(S), fib, index


def repair(seed):
    rng = random.Random(seed)
    S, fib, index = build()
    for step in range(2000):
        sing = [(w, ts[0]) for w, ts in fib.items()
                if is_mixed(w) and len(ts) == 1]
        pures = {w[0] for w, ts in fib.items() if not is_mixed(w) and ts}
        if not sing:
            return S, fib, len(pures) == 3, step
        rng.shuffle(sing)
        chosen = None
        for w, M in sing:
            cand = [k for k in M if k not in CORE]
            rng.shuffle(cand)
            for k in cand:
                # deleting k must leave every pure row nonempty
                bad = False
                for c in range(3):
                    ts = fib.get((c,) * N, [])
                    if ts and all(k in t for t in ts):
                        bad = True
                        break
                if not bad:
                    chosen = k
                    break
            if chosen is not None:
                break
        if chosen is None:
            return S, fib, False, step
        S.discard(chosen)
        for (ww, t) in index.get(chosen, []):
            lst = fib.get(ww)
            if lst is not None and t in lst:
                lst.remove(t)
                if not lst:
                    del fib[ww]
    return S, fib, False, -1


if __name__ == "__main__":
    for seed in range(int(sys.argv[1]) if len(sys.argv) > 1 else 8):
        S, fib, ok, step = repair(seed)
        sing = sum(1 for w, ts in fib.items() if is_mixed(w) and len(ts) == 1)
        pures = sorted({w[0] for w, ts in fib.items() if not is_mixed(w) and ts})
        core = tuple(len(fib.get(w, [])) for w in CORE_WORDS)
        good = (sing == 0 and pures == [0, 1, 2] and core == CORE_COUNTS)
        print(f"seed {seed}: |S|={len(S):3d} steps={step:4d} singletons={sing:3d} "
              f"pures={pures} core fibres={core} "
              + ("*** M8 AND M9 BOTH SILENT ***" if good else ""))
        if good:
            import json
            json.dump(sorted(map(list, S)), open("witness_m8m9_silent.json", "w"))
            print("  written to witness_m8m9_silent.json")
            break
