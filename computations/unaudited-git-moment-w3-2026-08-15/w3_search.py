"""UNAUDITED PROBE (W3, Route A, 2026-08-15). HEAD 26ba69f7.

The decisive search for the floor-lift gap.

QUESTION.  Is there a coordinate chart (diagonal cells only, declared
colour subsets T_uv) on which the committed support kills are silent

    M8: every H_c = {uv : c in T_uv} contains a perfect matching
    M9: no mixed word has exactly one live monomial

but the gauge mechanism of Theorem A.1 fires

    O5: some H_c has an edge lying in no fractional perfect matching of H_c

?  Such a chart is exactly a place where Route A strictly improves on the
committed floor machinery.  Conversely, if no such chart exists, O5's
marginal value over M9 in the coordinate regime is nil.

Two annealing runs:
  (A) minimise the number of aggregate blocks subject to M8+M9 silent, and
      report whether O5 ever fires on the way down;
  (B) directly maximise "M8+M9 silent" among charts on which O5 fires.
"""

from __future__ import annotations

import itertools
import math
import random
from collections import Counter

from w3_band import ALL_EDGES, N, failing_edges

_PMS = None


def all_pms():
    global _PMS
    if _PMS is None:
        from w3_core import matchings

        _PMS = [tuple(tuple(sorted(e)) for e in M) for M in matchings(N)]
    return _PMS


def analyse(T):
    """Return (n_missing_pure, n_singleton_mixed)."""
    counts = Counter()
    for M in all_pms():
        ok = True
        for e in M:
            if not T.get(e):
                ok = False
                break
        if not ok:
            continue
        for choice in itertools.product(*[T[e] for e in M]):
            w = [0] * N
            for (u, v), c in zip(M, choice):
                w[u] = c
                w[v] = c
            counts[tuple(w)] += 1
    miss = sum(1 for c in range(3) if counts.get((c,) * N, 0) == 0)
    sing = sum(1 for w, m in counts.items() if m == 1 and len(set(w)) > 1)
    return miss, sing


def colour_classes(T):
    return [tuple(e for e in T if c in T[e]) for c in range(3)]


def o5_count(T):
    n = 0
    for c, H in enumerate(colour_classes(T)):
        n += len(failing_edges(H))
    return n


def as_tuple(T):
    return tuple(sorted((e, tuple(sorted(v))) for e, v in T.items() if v))


def neighbours(T, rng, k=1):
    new = {e: list(v) for e, v in T.items() if v}
    for _ in range(k):
        e = rng.choice(ALL_EDGES)
        c = rng.randrange(3)
        cur = set(new.get(e, []))
        if c in cur:
            cur.discard(c)
        else:
            cur.add(c)
        if cur:
            new[e] = sorted(cur)
        else:
            new.pop(e, None)
    return new


def run_A(steps=4000, seed=0, verbose=False):
    """Minimise block count subject to M8+M9 silent; log O5 along the way."""
    rng = random.Random(seed)
    T = {e: [0, 1, 2] for e in ALL_EDGES}
    best = None
    seen_gap = []
    cur_cost = None
    for step in range(steps):
        cand = neighbours(T, rng, k=1 if rng.random() < 0.8 else 2)
        miss, sing = analyse(cand)
        blocks = len(cand)
        cells = sum(len(v) for v in cand.values())
        cost = 1000 * miss + 100 * sing + blocks + 0.05 * cells
        if cur_cost is None:
            cur_cost = cost
            T = cand
            continue
        temp = max(0.02, 3.0 * (1 - step / steps))
        if cost <= cur_cost or rng.random() < math.exp((cur_cost - cost) / temp):
            T, cur_cost = cand, cost
            if miss == 0 and sing == 0:
                d = o5_count(T)
                if best is None or blocks < best[0]:
                    best = (blocks, cells, d, {k: list(v) for k, v in T.items()})
                if d:
                    seen_gap.append((blocks, cells, d))
    return best, seen_gap


def run_B(steps=6000, seed=0):
    """Among charts on which O5 fires, minimise (missing pure, singletons)."""
    rng = random.Random(seed)
    # start from a chart where O5 surely fires: one colour class = PM + 1 edge
    Ms = all_pms()
    P = Ms[0]
    T = {e: [0, 1, 2] for e in ALL_EDGES}
    # thin colour 0 down to P plus one extra edge
    extra = next(e for e in ALL_EDGES if e not in P)
    for e in ALL_EDGES:
        if e not in P and e != extra:
            T[e] = [c for c in T[e] if c != 0]
    best = None
    cur = None
    for step in range(steps):
        cand = neighbours(T, rng, k=1 if rng.random() < 0.75 else 2)
        d = o5_count(cand)
        if d == 0:
            continue                                # must keep O5 alive
        miss, sing = analyse(cand)
        cost = 50 * miss + sing
        if cur is None or cost <= cur or rng.random() < math.exp(
            (cur - cost) / max(0.05, 2.0 * (1 - step / steps))
        ):
            T, cur = cand, cost
            if best is None or cost < best[0]:
                best = (cost, miss, sing, d, len(cand),
                        {k: list(v) for k, v in cand.items()})
            if miss == 0 and sing == 0:
                return best, True
    return best, False


if __name__ == "__main__":
    print("UNAUDITED PROBE  W3 / Route A  HEAD 26ba69f7")
    print("=" * 80)
    print("RUN A: minimise aggregate blocks with M8+M9 silent; does O5 ever fire?")
    for seed in range(4):
        best, gap = run_A(steps=2500, seed=seed)
        if best is None:
            print(f"  seed {seed}: no M8+M9-silent chart reached")
            continue
        blocks, cells, d, _ = best
        print(
            f"  seed {seed}: best M8+M9-silent chart has blocks={blocks} "
            f"cells={cells}  O5 dead cells there={d};  "
            f"M8+M9-silent charts seen with O5 firing: {len(gap)}"
        )
    print()
    print("RUN B: force O5 to fire, then try to silence M8+M9")
    for seed in range(4):
        best, found = run_B(steps=3000, seed=seed)
        if best is None:
            print(f"  seed {seed}: search stuck")
            continue
        cost, miss, sing, d, blocks, T = best
        verdict = "GAP FOUND" if found else "no gap"
        print(
            f"  seed {seed}: best = missing-pure {miss}, mixed singletons {sing}, "
            f"O5 dead {d}, blocks {blocks}   -> {verdict}"
        )
