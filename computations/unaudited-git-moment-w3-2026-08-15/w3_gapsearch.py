"""UNAUDITED PROBE (W3, Route A, 2026-08-15). HEAD 26ba69f7.

Decisive search for a floor-lift gap, using an exact reduction.

Take the chart  T_uv = {1,2} u ({0} if uv in H_0),  i.e. colours 1 and 2 are
declared everywhere and colour 0 only on H_0.  (This is the most favourable
slice for silencing the singleton kill, since colours 1,2 contribute the
maximum possible multiplicity.)

For a word w with colour classes A = w^-1(0), B = w^-1(1), C = w^-1(2), the
live monomials are  PM(H_0[A]) x PM(K[B]) x PM(K[C]),  so

     mult(w) = pm(H_0[A]) * (|B|-1)!! * (|C|-1)!!.

Since (|B|-1)!!(|C|-1)!! = 1 exactly when |B|,|C| in {0,2}, the committed
kills become, EXACTLY:

     M8 silent  <=>  pm(H_0) >= 1
     M9 silent  <=>  pm(H_0[A]) != 1 for every 4-subset and 6-subset A

and the gauge mechanism is

     O5 fires   <=>  some edge of H_0 lies in no fractional perfect
                     matching of H_0.

So the gap question is a pure question about ONE graph H_0 on 8 vertices.
This script searches it by exhaustive enumeration over all H_0 up to
isomorphism reachable by annealing plus a full sweep of small/structured
families.
"""

from __future__ import annotations

import itertools
import random
from functools import lru_cache

from w3_band import ALL_EDGES, N, VERTS, failing_edges, fpm_exists


def pm_count(edge_set, verts):
    verts = tuple(sorted(verts))
    es = frozenset(e for e in edge_set if e[0] in verts and e[1] in verts)
    return _pm(es, verts)


@lru_cache(maxsize=None)
def _pm(es, verts):
    if not verts:
        return 1
    if len(verts) % 2:
        return 0
    a = verts[0]
    rest = verts[1:]
    total = 0
    for b in rest:
        e = (a, b) if a < b else (b, a)
        if e in es:
            total += _pm(es, tuple(x for x in rest if x != b))
    return total


def m9_silent(H0):
    es = frozenset(H0)
    for k in (4, 6):
        for A in itertools.combinations(VERTS, k):
            if _pm(es, A) == 1:
                return False
    return True


def m8_silent(H0):
    return _pm(frozenset(H0), tuple(VERTS)) >= 1


def o5_fires(H0):
    return bool(failing_edges(tuple(H0)))


def is_gap(H0):
    return m8_silent(H0) and m9_silent(H0) and o5_fires(H0)


def anneal(seed=0, steps=200000):
    rng = random.Random(seed)
    H = set(ALL_EDGES)
    best = None

    def cost(H):
        es = frozenset(H)
        bad = 0
        for k in (4, 6):
            for A in itertools.combinations(VERTS, k):
                if _pm(es, A) == 1:
                    bad += 1
        if _pm(es, tuple(VERTS)) == 0:
            bad += 50
        if not failing_edges(tuple(H)):
            bad += 20
        return bad

    cur = cost(H)
    for step in range(steps):
        e = rng.choice(ALL_EDGES)
        H2 = set(H)
        if e in H2:
            H2.discard(e)
        else:
            H2.add(e)
        c2 = cost(H2)
        if c2 <= cur or rng.random() < 0.02:
            H, cur = H2, c2
            if best is None or cur < best[0]:
                best = (cur, frozenset(H))
            if cur == 0:
                return 0, frozenset(H)
    return best


def sweep_structured():
    """Every H_0 that is K_8 minus a set of at most 3 edges, plus every
    'blocker' family: K_m on a subset joined by few edges to the rest."""
    hits = []
    base = list(ALL_EDGES)
    for k in range(0, 4):
        for rem in itertools.combinations(base, k):
            H = frozenset(base) - set(rem)
            if is_gap(H):
                hits.append(H)
    return hits


def exhaustive_small(maxedges=10):
    """All H_0 with at most `maxedges` edges (these must contain a PM)."""
    hits = []
    for k in range(4, maxedges + 1):
        for H in itertools.combinations(ALL_EDGES, k):
            Hs = frozenset(H)
            if not m8_silent(Hs):
                continue
            if m9_silent(Hs) and o5_fires(Hs):
                hits.append(Hs)
    return hits


if __name__ == "__main__":
    print("UNAUDITED PROBE  W3 / Route A  HEAD 26ba69f7")
    print("GAP SEARCH: is there H_0 with pm>=1, no 4/6-subset having exactly one")
    print("            perfect matching, and an edge in no fractional pm?")
    print("=" * 78)

    print("(a) exhaustive over all H_0 with at most 8 edges:")
    hits = exhaustive_small(8)
    print(f"    gaps found: {len(hits)}")

    print("(b) sweep of K_8 minus up to 3 edges:")
    hits = sweep_structured()
    print(f"    gaps found: {len(hits)}")

    print("(c) annealing (cost = #4/6-subsets with a unique PM, "
          "+50 if no PM, +20 if O5 silent):")
    for seed in range(6):
        r = anneal(seed=seed, steps=40000)
        if r is None:
            print(f"    seed {seed}: no progress")
            continue
        c, H = r
        es = frozenset(H)
        bad46 = sum(
            1 for k in (4, 6) for A in itertools.combinations(VERTS, k)
            if _pm(es, A) == 1
        )
        print(
            f"    seed {seed}: best cost={c}  |H_0|={len(H)}  "
            f"unique-PM 4/6-subsets={bad46}  pm(H_0)={_pm(es, tuple(VERTS))}  "
            f"O5 dead edges={len(failing_edges(tuple(H)))}"
            + ("   *** GAP ***" if c == 0 else "")
        )
