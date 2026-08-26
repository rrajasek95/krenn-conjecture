"""UNAUDITED PROBE (W3, Route A, 2026-08-15). HEAD 26ba69f7.

Greedy descent from the full coordinate chart.

Random charts all die by M9 (singleton mixed row), so they are not the
census's hard cases.  The hard cases are reached the other way: start from
the full diagonal chart (all 28 blocks, T_uv = {0,1,2}), delete declared
colours one at a time, and keep only deletions that preserve

    M8:  every H_c = {uv : c in T_uv} still contains a perfect matching
    M9:  no mixed word has exactly one live matching

This produces genuine committed-kill survivors.  We then ask, on each
survivor, whether the gauge-balance mechanism O5 fires -- i.e. whether some
H_c has an edge lying in no fractional perfect matching of H_c.
"""

from __future__ import annotations

import itertools
import random
from collections import Counter

from w3_band import ALL_EDGES, N, failing_edges, fpm_exists

_PMS = None


def all_pms():
    global _PMS
    if _PMS is None:
        from w3_core import matchings

        _PMS = [tuple(tuple(sorted(e)) for e in M) for M in matchings(N)]
    return _PMS


def multiplicities(T):
    """word -> number of live (matching, colour-choice) monomials."""
    counts = Counter()
    for M in all_pms():
        if any(not T.get(e) for e in M):
            continue
        for choice in itertools.product(*[sorted(T[e]) for e in M]):
            w = [None] * N
            for (u, v), c in zip(M, choice):
                w[u] = w[v] = c
            counts[tuple(w)] += 1
    return counts


def ok(T):
    """M8 and M9 both silent?"""
    counts = multiplicities(T)
    for c in range(3):
        if counts.get((c,) * N, 0) == 0:
            return False
    for w, m in counts.items():
        if m == 1 and len(set(w)) > 1:
            return False
    return True


def colour_classes(T):
    return [tuple(e for e in T if c in T[e]) for c in range(3)]


def o5_dead(T):
    out = []
    for c, H in enumerate(colour_classes(T)):
        for e in failing_edges(H):
            out.append((e, c))
    return out


def descend(seed=0, max_steps=400):
    rng = random.Random(seed)
    T = {e: {0, 1, 2} for e in ALL_EDGES}
    assert ok(T), "full chart must survive"
    for _ in range(max_steps):
        cand = [(e, c) for e in T for c in sorted(T[e])]
        rng.shuffle(cand)
        moved = False
        for (e, c) in cand:
            new = {k: set(v) for k, v in T.items()}
            new[e].discard(c)
            if not new[e]:
                del new[e]
            if ok(new):
                T = new
                moved = True
                break
        if not moved:
            break
    return T


def summarise(T):
    blocks = len(T)
    cells = sum(len(v) for v in T.values())
    sizes = [len(h) for h in colour_classes(T)]
    dead = o5_dead(T)
    return dict(blocks=blocks, cells=cells, class_sizes=sizes, o5=len(dead), dead=dead)


if __name__ == "__main__":
    print("UNAUDITED PROBE  W3 / Route A  HEAD 26ba69f7")
    print("Greedy descent from the full coordinate chart (28 blocks, 84 cells)")
    print("keeping M8 and M9 silent at every step")
    print("=" * 80)
    tally = Counter()
    minima = []
    for seed in range(12):
        T = descend(seed)
        s = summarise(T)
        minima.append(s)
        tally["o5" if s["o5"] else "stable"] += 1
        print(
            f"seed {seed:2d}: blocks={s['blocks']:2d} diagonal-cells={s['cells']:2d} "
            f"H_c sizes={s['class_sizes']}  O5 dead cells={s['o5']}"
        )
    print()
    print(f"terminal charts: O5 fires on {tally['o5']}, balance-stable {tally['stable']}")
    bl = [s["blocks"] for s in minima]
    ce = [s["cells"] for s in minima]
    print(f"aggregate-support blocks reached: min={min(bl)} max={max(bl)}")
    print(f"diagonal cells reached:           min={min(ce)} max={max(ce)}")
