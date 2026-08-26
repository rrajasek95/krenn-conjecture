#!/usr/bin/env python3
"""A3 Task 1 -- is there a singleton-free monomial template at N = 10?

N = 10 is the first case of N = 2 mod 4 above the proved N = 6.  The A3
family F_n covers every N = 0 mod 4 (N >= 8); the parity obstruction in the
4th-matching theorem (step 4a) suggests N = 2 mod 4 may be genuinely harder.
This is the search that decides the question empirically.

Model: FULL general monomial template (ordered labels, so off-diagonal cells
are allowed, exactly W2's R_cell), evaluated by direct bucketing of the 945
perfect matchings of K_10 -- the definition, no shortcut.

Objective  score = 4*(#missing pures) + (#mixed singleton fibres).
score = 0 would be a singleton-free template with all three pures live.

Anneal + restarts, plus structured seeds.  Search is heuristic; the VERDICT
statements it supports are only "not found by this budget".
"""

from __future__ import annotations

import json
import random
import sys
import time
from itertools import combinations

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from a3_core import geometry

N = 10
GEO = geometry(N)
NEDGE = len(GEO.edges)
NMATCH = len(GEO.matchings)
# per-matching list of (edge index, u, v)
MDATA = tuple(tuple((GEO.index[(u, v)], u, v) for (u, v) in m)
              for m in GEO.matchings)
STATES = [None] + [(a, b) for a in range(3) for b in range(3)]   # 10 states


def evaluate(labels):
    """(score, singletons, pures, histogram) -- direct bucketing."""
    buckets = {}
    for md in MDATA:
        word = [-1] * N
        ok = True
        for e, u, v in md:
            lab = labels[e]
            if lab is None:
                ok = False
                break
            word[u], word[v] = lab
        if ok:
            w = tuple(word)
            buckets[w] = buckets.get(w, 0) + 1
    pures = [buckets.get(tuple([r] * N), 0) for r in range(3)]
    singles = 0
    hist = {}
    for w, c in buckets.items():
        if len(set(w)) == 1:
            continue
        hist[c] = hist.get(c, 0) + 1
        if c == 1:
            singles += 1
    missing = sum(1 for p in pures if p == 0)
    return 4 * missing + singles, singles, pures, hist


def seed_random(rng, diagonal_bias=0.85, absent_prob=0.0):
    labels = []
    for _ in range(NEDGE):
        if rng.random() < absent_prob:
            labels.append(None)
        elif rng.random() < diagonal_bias:
            c = rng.randrange(3)
            labels.append((c, c))
        else:
            labels.append((rng.randrange(3), rng.randrange(3)))
    return labels


def seed_structured(kind):
    """Structured starts: the A3 family idea forced onto 10 sites."""
    lab = [None] * NEDGE
    if kind == "X6Y4":
        X, Y = [0, 1, 2, 3, 4, 5], [6, 7, 8, 9]
    elif kind == "X8Y2":
        X, Y = list(range(8)), [8, 9]
    else:
        X, Y = [0, 2, 4, 6, 8], [1, 3, 5, 7, 9]
    MX = [(X[2 * i], X[2 * i + 1]) for i in range(len(X) // 2)]
    MY = [(Y[2 * i], Y[2 * i + 1]) for i in range(len(Y) // 2)]
    M = {tuple(sorted(e)) for e in MX + MY}
    for (u, v) in GEO.edges:
        e = GEO.index[(u, v)]
        if (u in X) != (v in X):
            lab[e] = (0, 0)
        elif (u, v) in M:
            lab[e] = (1, 1)
        else:
            lab[e] = (2, 2)
    return lab


def anneal(rng, labels, steps, t0=2.0, t1=0.02, diagonal_only=False):
    cur = list(labels)
    score, singles, pures, _ = evaluate(cur)
    best, best_labels = score, list(cur)
    choices = ([None] + [(c, c) for c in range(3)]) if diagonal_only else STATES
    for t in range(steps):
        if best == 0:
            break
        temp = t0 * (t1 / t0) ** (t / max(1, steps - 1))
        e = rng.randrange(NEDGE)
        old = cur[e]
        new = rng.choice(choices)
        if new == old:
            continue
        cur[e] = new
        s, sg, pu, _ = evaluate(cur)
        if s <= score or rng.random() < pow(2.718281828, -(s - score) / temp):
            score = s
            if s < best:
                best, best_labels = s, list(cur)
        else:
            cur[e] = old
    return best, best_labels


def main():
    budget_steps = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    restarts = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    rng = random.Random(20260815)
    t_start = time.time()
    log = []
    overall_best = (10 ** 9, None, None)

    seeds = [("struct-" + k, seed_structured(k))
             for k in ("X6Y4", "X8Y2", "alt")]
    for i in range(restarts):
        seeds.append((f"rand{i}", seed_random(rng, diagonal_bias=0.9)))
    for i in range(restarts // 2):
        seeds.append((f"randmix{i}", seed_random(rng, diagonal_bias=0.5)))

    for name, lab in seeds:
        s0, sg0, pu0, _ = evaluate(lab)
        diag_only = name.startswith(("struct", "rand")) and "mix" not in name
        best, blab = anneal(rng, lab, budget_steps, diagonal_only=diag_only)
        s, sg, pu, hist = evaluate(blab)
        log.append(dict(seed=name, start_score=s0, best_score=s,
                        singletons=sg, pures=pu,
                        diagonal_only=diag_only,
                        support=sum(1 for x in blab if x is not None)))
        if s < overall_best[0]:
            overall_best = (s, blab, name)
        print(f"{name:12s} start={s0:5d} -> best={s:4d} "
              f"(singletons={sg}, pures={pu})  [{time.time()-t_start:.0f}s]")
        if s == 0:
            print("  *** SINGLETON-FREE TEMPLATE FOUND AT N=10 ***")
            break

    s, blab, name = overall_best
    _, sg, pu, hist = evaluate(blab)
    out = dict(N=N, budget_steps=budget_steps, restarts=len(seeds),
               best_score=s, best_seed=name, best_singletons=sg,
               best_pures=pu, best_histogram={str(k): v for k, v in
                                              sorted(hist.items())},
               best_labels=[list(x) if x else None for x in blab],
               runs=log, seconds=round(time.time() - t_start, 1))
    with open(__file__.rsplit("/", 1)[0] + "/results_hunt10.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"\nBEST over all seeds: score={s} singletons={sg} pures={pu} "
          f"(seed {name}); {time.time()-t_start:.0f}s")
    print("wrote results_hunt10.json")


if __name__ == "__main__":
    main()
