#!/usr/bin/env python3
"""UNAUDITED PROBE W13 -- Task 2 (R1b): second-generation hunt.

Finding from hunt 1: the singleton-free stratum at N = 10 inside R_cell is
ISOLATED -- none of the 4 x 135 single-cell neighbours of A3's certificates is
singleton-free, and only 2-5 of each 8,910 two-cell neighbours are.  So
stratum-confined local search cannot move.  This script therefore uses

  (A) exhaustive THREE-cell neighbourhoods of every certificate;
  (B) penalised annealing (leaving the stratum is allowed, singletons cost 6)
      from certificate seeds and from random seeds;
  (C) the STRUCTURED family suggested by every known certificate and by A3's
      F_n: one colour class is a single perfect matching (so its pure fibre
      is exactly 1), the other two colours partition a subset of the rest.
      Annealed at N = 10 and N = 12.

Every singleton-free three-pure template met is decided for R1b, and every
odd relation is re-verified from scratch.
"""

from __future__ import annotations

import json
import random
import sys
import time
from itertools import combinations

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from w13_rcell import (census, diagonal_labels, diagonal_sizes, edges,
                       perfect_matchings, verdict, verify_odd_relation)
from w13_task2_hunt import certificates

OUT = {"scanned": 0, "singleton_free": [], "counterexamples": [],
       "neighbourhood3": {}, "anneal": [], "structured": []}
SEEN = set()


def require(cond, detail):
    if not cond:
        raise AssertionError(detail)


def sets_from_assign(N, a):
    out = [[], [], []]
    for e, r in a.items():
        if r is not None:
            out[r].append(e)
    return out


def diag_score(N, sets):
    sizes, mixed, pures = diagonal_sizes(N, sets)
    if any(p == 0 for p in pures):
        return None
    ms = sizes[mixed]
    return int((ms == 1).sum()), int((ms == 2).sum()), [int(p) for p in pures]


def decide(N, sets, tag):
    key = (N, tuple(tuple(sorted(map(tuple, s))) for s in sets))
    if key in SEEN:
        return None
    SEEN.add(key)
    OUT["scanned"] += 1
    labels = diagonal_labels(N, sets)
    c = census(N, labels)
    if any(p == 0 for p in c["pures"]) or c["singletons"]:
        return None
    v = verdict(N, labels, c)
    rec = {"N": N, "tag": tag, "support": sum(len(s) for s in sets),
           "pures": v["pures"], "n_binomials": v["n_binomials"],
           "hist": v["hist"], "O1_dead": v["O1_dead"],
           "colour_edges": [sorted(map(list, s)) for s in sets]}
    if v["R1b_counterexample"]:
        OUT["counterexamples"].append(rec)
        print("\n*** R1b COUNTEREXAMPLE FOUND ***")
        print(json.dumps(rec, indent=1)[:2500])
    else:
        require(verify_odd_relation(N, c["binomials"], v["odd_relation"]), rec)
        OUT["singleton_free"].append(rec)
        print(f"    singleton-free: {tag} m={rec['support']} pures "
              f"{rec['pures']} binomials {rec['n_binomials']} "
              f"hist {rec['hist']}")
    return rec


# ------------------------------------------------------------------ (A)

def neighbourhood3(N, colour_sets, tag):
    es = list(edges(N))
    base = {e: None for e in es}
    for r, s in enumerate(colour_sets):
        for e in s:
            base[tuple(e)] = r
    alphabet = [None, 0, 1, 2]
    scanned = found = 0
    for pos in combinations(range(len(es)), 3):
        opts = [[x for x in alphabet if x != base[es[p]]] for p in pos]
        for x0 in opts[0]:
            for x1 in opts[1]:
                for x2 in opts[2]:
                    a = dict(base)
                    a[es[pos[0]]] = x0
                    a[es[pos[1]]] = x1
                    a[es[pos[2]]] = x2
                    scanned += 1
                    sets = sets_from_assign(N, a)
                    sc = diag_score(N, sets)
                    if sc is None or sc[0] != 0:
                        continue
                    if decide(N, sets, f"{tag}-nbhd3") is not None:
                        found += 1
    return scanned, found


# ------------------------------------------------------------------ (B)

def anneal(N, rng, steps, seed_sets, tag, singleton_weight=6):
    es = list(edges(N))
    a = {e: None for e in es}
    for r, s in enumerate(seed_sets):
        for e in s:
            a[tuple(e)] = r

    def score(x):
        sc = diag_score(N, sets_from_assign(N, x))
        if sc is None:
            return None, None
        return singleton_weight * sc[0] + sc[1], sc

    cur, sc = score(a)
    require(cur is not None, "seed empties a pure")
    best = cur
    T0, T1 = 14.0, 0.3
    for step in range(steps):
        T = T0 * (T1 / T0) ** (step / max(1, steps - 1))
        nmoves = 1 if rng.random() < 0.6 else 2
        picks = [es[rng.randrange(len(es))] for _ in range(nmoves)]
        old = [a[e] for e in picks]
        for e in picks:
            a[e] = rng.choice([x for x in [None, 0, 1, 2] if x != a[e]])
        new, sc2 = score(a)
        if new is None:
            for e, o in zip(picks, old):
                a[e] = o
            continue
        if new <= cur or rng.random() < pow(2.718281828, -(new - cur) / T):
            cur, sc = new, sc2
            best = min(best, cur)
            if sc[0] == 0:
                decide(N, sets_from_assign(N, a), tag)
        else:
            for e, o in zip(picks, old):
                a[e] = o
    return best


# ------------------------------------------------------------------ (C)

def structured_anneal(N, rng, steps, tag):
    """One colour class = a single perfect matching (pure fibre exactly 1);
    the other two colours partition a subset of the remaining edges."""
    es = list(edges(N))
    M = perfect_matchings(tuple(range(N)))[rng.randrange(
        len(perfect_matchings(tuple(range(N)))))]
    M = set(tuple(sorted(e)) for e in M)
    free = [e for e in es if e not in M]
    a = {e: 1 for e in M}
    for e in free:
        a[e] = rng.choice([None, 0, 2])

    def score(x):
        sc = diag_score(N, sets_from_assign(N, x))
        if sc is None:
            return None, None
        return 6 * sc[0] + sc[1], sc

    cur, sc = score(a)
    tries = 0
    while cur is None and tries < 300:
        e = free[rng.randrange(len(free))]
        a[e] = rng.choice([0, 2])
        cur, sc = score(a)
        tries += 1
    if cur is None:
        return None
    best = cur
    T0, T1 = 14.0, 0.3
    for step in range(steps):
        T = T0 * (T1 / T0) ** (step / max(1, steps - 1))
        e = free[rng.randrange(len(free))]
        old = a[e]
        a[e] = rng.choice([x for x in [None, 0, 2] if x != old])
        new, sc2 = score(a)
        if new is None:
            a[e] = old
            continue
        if new <= cur or rng.random() < pow(2.718281828, -(new - cur) / T):
            cur, sc = new, sc2
            best = min(best, cur)
            if sc[0] == 0:
                decide(N, sets_from_assign(N, a), tag)
        else:
            a[e] = old
    return best


def main():
    rng = random.Random(555777)
    certs = certificates()
    N = 10
    for support, cs in certs:
        decide(N, cs, f"A3-cert-{support}")

    print("== (C) structured family: one colour = a perfect matching ==")
    for NN, runs, steps in ((10, 30, 6000), (12, 8, 1500)):
        bests = []
        for run in range(runs):
            t0 = time.time()
            b = structured_anneal(NN, rng, steps, f"struct-N{NN}-{run}")
            bests.append(b)
            if run < 4 or b == min(x for x in bests if x is not None):
                print(f"  N={NN} run {run}: best penalised cost {b} "
                      f"[{time.time() - t0:.0f}s]")
        OUT["structured"].append({"N": NN, "runs": runs, "steps": steps,
                                  "best_costs": bests})
        good = [b for b in bests if b is not None]
        print(f"  N={NN}: {runs} runs, best cost {min(good) if good else None}")

    print("\n== (B) penalised annealing from certificate and random seeds ==")
    for support, cs in certs:
        for run in range(4):
            t0 = time.time()
            b = anneal(N, rng, 12000, cs, f"anneal-{support}-{run}")
            print(f"  from m={support} run {run}: best penalised cost {b} "
                  f"[{time.time() - t0:.0f}s]")
            OUT["anneal"].append({"seed": support, "run": run, "best": b})

    print("\n== (A) exhaustive 3-cell neighbourhoods of the certificates ==")
    for support, cs in certs:
        t0 = time.time()
        s3, f3 = neighbourhood3(N, cs, f"c{support}")
        OUT["neighbourhood3"][support] = {"scanned": s3, "singleton_free": f3}
        print(f"  certificate m={support}: {s3} three-cell neighbours, "
              f"{f3} singleton-free  [{time.time() - t0:.0f}s]")

    sf = OUT["singleton_free"]
    print("\n== summary ==")
    print(f"  candidate templates reaching the R1b decision: {OUT['scanned']}")
    print(f"  singleton-free with three pures: {len(sf) + len(OUT['counterexamples'])}")
    print(f"  O1-dead (odd relation re-verified): {len(sf)}")
    print(f"  R1b COUNTEREXAMPLES: {len(OUT['counterexamples'])}")
    if sf:
        nb = sorted(r["n_binomials"] for r in sf)
        print(f"  binomial-fibre counts: min {nb[0]} max {nb[-1]}")
        print(f"  supports realised: {sorted(set(r['support'] for r in sf))}")
    with open(__file__.rsplit("/", 1)[0] + "/results_task2_hunt2.json",
              "w") as fh:
        json.dump(OUT, fh, indent=1, default=str)
    print("wrote results_task2_hunt2.json")


if __name__ == "__main__":
    main()
