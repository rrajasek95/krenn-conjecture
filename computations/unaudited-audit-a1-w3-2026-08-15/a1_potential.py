"""AUDIT A1 / CLAIMS 3 + 5: the descent measure and the independent-four-set
collapse.

Checks:
  P1  the independent-4-set proposition (W3's w3_indep.py PROPOSITION):
      for H <= K_8 with min degree >= 3, {edges in no fpm} equals
      {edges inside V\\I for some independent 4-set I}.  Exhaustive over the
      min-degree-3 graphs with |E| = 12, 13 (whose COUNT is also checked
      against W3's 537,355) plus random samples at higher |E|.
  P2  the "CONSEQUENCE": an independent set I of size n/2 in the aggregate
      support graph yields w = 1_{V\\I} - 1_I, which is pure-neutral and
      admissible, hence a (D) degeneration.  Verified against the exact
      dichotomy of a1_dichotomy.
  P3  cells-vs-blocks: (D) strictly decreases the CELL count (trivially),
      but does it decrease the BLOCK count (edges of the aggregate support
      graph)?  Explicit counterexamples are hunted.
"""

from __future__ import annotations

import itertools
import random
import sys

from a1_core import COLS, all_cells, nodes_of
from a1_dichotomy import classify, decide_D, decide_P, verify_D
from a1_fpm import edge_in_fpm_lp, failing_edges, fpm_support

VERTS8 = tuple(range(8))
E8 = tuple(itertools.combinations(range(8), 2))


def mindeg(H, n=8):
    d = [0] * n
    for u, v in H:
        d[u] += 1
        d[v] += 1
    return min(d)


def indep4_dead(H):
    out = set()
    for I in itertools.combinations(VERTS8, 4):
        if any(a in I and b in I for (a, b) in H):
            continue
        out.update(e for e in H if e[0] not in I and e[1] not in I)
    return out


def count_mindeg3(sizes=(12, 13)):
    tot = {}
    for k in sizes:
        c = 0
        for H in itertools.combinations(E8, k):
            if mindeg(H) >= 3:
                c += 1
        tot[k] = c
    return tot


def check_prop(sizes=(12, 13), sample=None, seed=0):
    rng = random.Random(seed)
    agree = viol = n = 0
    bad = []
    for k in sizes:
        it = itertools.combinations(E8, k)
        if sample:
            it = (tuple(rng.sample(E8, k)) for _ in range(sample))
        for H in it:
            if mindeg(H) < 3:
                continue
            n += 1
            a = set(failing_edges(H, VERTS8))
            b = indep4_dead(H)
            if a == b:
                agree += 1
            else:
                viol += 1
                if len(bad) < 3:
                    bad.append((sorted(H), sorted(a), sorted(b)))
    return n, agree, viol, bad


def crosscheck_fpm(trials=200, seed=1):
    rng = random.Random(seed)
    bad = 0
    for _ in range(trials):
        k = rng.randint(6, 20)
        H = tuple(sorted(rng.sample(E8, k)))
        sup = fpm_support(H, VERTS8)
        for e in H:
            if (e in sup) != edge_in_fpm_lp(H, VERTS8, e):
                bad += 1
    return bad


def check_consequence(trials=40, seed=3, n=8):
    """P2: an independent n/2-set in the aggregate support graph gives a (D)
    certificate; and the exact classifier must then also say (D)."""
    rng = random.Random(seed)
    good = bad = skipped = 0
    for _ in range(trials):
        k = rng.randint(6, 20)
        H = rng.sample(E8, k)
        I = None
        for cand in itertools.combinations(range(n), n // 2):
            if not any(a in cand and b in cand for (a, b) in H):
                I = set(cand)
                break
        if I is None:
            skipped += 1
            continue
        if not any(u not in I and v not in I for (u, v) in H):
            skipped += 1                       # nothing would die
            continue
        S = frozenset((u, v, c, c) for (u, v) in H for c in COLS)
        w = {(v, c): (-1 if v in I else 1) for v in range(n) for c in COLS}
        ok, msg = verify_D(n, S, w)
        tag, _ = classify(n, S)
        if ok and tag == "D":
            good += 1
        else:
            bad += 1
    return good, bad, skipped


def blocks_of(S):
    return {(k[0], k[1]) for k in S}


def check_cells_vs_blocks(n=8, trials=60, seed=5, density=0.12):
    """P3: under a (D) degeneration the cell count always drops; how often
    does the BLOCK count stay the same?"""
    rng = random.Random(seed)
    same_blocks = drop_blocks = 0
    example = None
    for _ in range(trials):
        S = frozenset(k for k in all_cells(n) if rng.random() < density)
        if not S:
            continue
        ok, w = decide_D(n, S)
        if not ok:
            continue
        good, _ = verify_D(n, S, w)
        if not good:
            continue
        S0 = frozenset(k for k in S if w[nodes_of(k)[0]] + w[nodes_of(k)[1]] == 0)
        assert len(S0) < len(S)                       # cell potential drops
        if blocks_of(S0) == blocks_of(S):
            same_blocks += 1
            if example is None:
                example = (sorted(S), sorted(S0))
        else:
            drop_blocks += 1
    return same_blocks, drop_blocks, example


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "cross"):
        print("[fpm] my polytope-vertex enumeration vs exact LP: "
              f"mismatches = {crosscheck_fpm(60)}")
    if what in ("all", "count"):
        c = count_mindeg3()
        print(f"[count] min-degree-3 graphs on 8 vertices: {c} "
              f"total={sum(c.values())}  (W3 claims 537,355)")
    if what in ("all", "prop"):
        n, agree, viol, bad = check_prop()
        print(f"[P1] exhaustive |E| in 12,13, min-deg 3: tested={n} "
              f"agree={agree} VIOLATIONS={viol}")
        for b in bad:
            print("     ", b)
        n, agree, viol, bad = check_prop(sizes=(14, 16, 18, 20), sample=3000)
        print(f"[P1] sampled |E| in 14,16,18,20: tested={n} agree={agree} "
              f"VIOLATIONS={viol}")
        for b in bad:
            print("     ", b)
        # sharpness: min degree 2 must break it
        rng = random.Random(11)
        tested = dis = 0
        while tested < 4000:
            k = rng.randint(8, 16)
            H = tuple(sorted(rng.sample(E8, k)))
            if mindeg(H) != 2:
                continue
            tested += 1
            if set(failing_edges(H, VERTS8)) != indep4_dead(H):
                dis += 1
        print(f"[P1-sharp] min-degree-2 graphs: tested={tested} "
              f"DISAGREEMENTS={dis} (hypothesis needed: {dis > 0})")
    if what in ("all", "cons"):
        g, b, s = check_consequence()
        print(f"[P2] independent-4-set => (D): good={g} bad={b} skipped={s}")
    if what in ("all", "blocks"):
        same, drop, ex = check_cells_vs_blocks()
        print(f"[P3] (D) degenerations: block count UNCHANGED in {same}, "
              f"dropped in {drop}")
        if ex:
            print(f"     example: |S|={len(ex[0])} -> |S0|={len(ex[1])}, "
                  f"blocks {len(blocks_of(ex[0]))} -> {len(blocks_of(ex[1]))}")
