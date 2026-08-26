#!/usr/bin/env python3
"""AUDIT A2 -- targeted hunt for a (SC)-admissible zero-singleton template at
support <= 27, warm-started from W2's 28 full-support templates (which ARE
(SC)-admissible and singleton-free at m = 28).  Deleting edges and repairing
with extra cells is the most promising route to a band certificate that the
committed slice-cover input actually allows."""
from __future__ import annotations
import json, math, random, sys, time
import numpy as np
from a2_core import COLORS, audit_template, fibre_counts_dp_numpy, geom, normalise_template
from a2_slicecover import slice_cover_report

CELLS = [(a, b) for a in COLORS for b in COLORS]
W2 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
      "unaudited-witness-splitting-w2-2026-08-15/hunt8_models.json")

def bases(g):
    blob = json.load(open(W2))
    out = []
    for res in blob["results"].values():
        for mod in res["models"]:
            out.append([frozenset() if x is None else frozenset({tuple(x)})
                        for x in mod["labels"]])
    return out

def evaluate(g, t, m):
    ne = [i for i, s in enumerate(t) if s]
    if len(ne) != m:
        return None, None
    sc = slice_cover_report(g, t)
    counts = fibre_counts_dp_numpy(g, t)
    missing = sum(1 for r in g.const_rows if counts[r] == 0)
    singles = int(np.count_nonzero((counts == 1) & g.mixed))
    sigma = sum(len(s) for s in t)
    return 400*missing + 40*singles + 20*sc["n_missing"] + sigma, \
        {"missing": missing, "singletons": singles, "unserved": sc["n_missing"],
         "sigma": sigma}

def neighbour(g, rng, t, m):
    out = [set(s) for s in t]
    ne = [i for i, s in enumerate(out) if s]
    r = rng.random()
    if r < 0.5:
        i = rng.choice(ne)
        if len(out[i]) > 1 and rng.random() < 0.5:
            out[i].discard(rng.choice(sorted(out[i])))
        else:
            out[i].add(rng.choice(CELLS))
    elif r < 0.75:
        i = rng.choice(ne)
        out[i] = {rng.choice(CELLS)}
    else:
        empty = [i for i in range(len(g.edges)) if not out[i]]
        if not empty:
            return None
        src, dst = rng.choice(ne), rng.choice(empty)
        out[dst], out[src] = set(out[src]), set()
    return [frozenset(s) for s in out]

def main():
    a = sys.argv[1:]
    m = int(a[a.index("--m")+1]) if "--m" in a else 27
    budget = float(a[a.index("--budget")+1]) if "--budget" in a else 200.0
    g = geom(8); rng = random.Random(int(a[a.index("--seed")+1]) if "--seed" in a else 4)
    B = bases(g)
    print(f"seeded (SC) hunt at m={m}, {len(B)} warm starts, budget {budget}s")
    best = None; start = time.time()
    while time.time() - start < budget:
        t = [set(s) for s in rng.choice(B)]
        ne = [i for i, s in enumerate(t) if s]
        for i in rng.sample(ne, 28 - m):
            t[i] = set()
        t = [frozenset(s) for s in t]
        cur, rec = evaluate(g, t, m)
        if cur is None: continue
        temp = 25.0
        while time.time() - start < budget:
            temp = max(temp*0.9997, 0.4)
            cand = neighbour(g, rng, t, m)
            if cand is None: continue
            val, rc = evaluate(g, cand, m)
            if val is None: continue
            if val <= cur or rng.random() < math.exp(-(val-cur)/temp):
                t, cur, rec = cand, val, rc
            if best is None or (rc["missing"], rc["singletons"], rc["unserved"], rc["sigma"]) < best[0]:
                best = ((rc["missing"], rc["singletons"], rc["unserved"], rc["sigma"]),
                        [sorted(s) for s in cand])
    print(f"  best (missing, singletons, unserved slots, sigma) = {best[0]}")
    out = {"m": m, "best": best[0], "template": best[1]}
    if best[0][0] == 0 and best[0][1] == 0 and best[0][2] == 0:
        tt = normalise_template(g, [[tuple(c) for c in s] for s in best[1]])
        out["verification"] = audit_template(g, tt, exact=True)
        print("  *** (SC)-ADMISSIBLE ZERO-SINGLETON CERTIFICATE ***")
    json.dump(out, open(f"results_sc_seeded_m{m}.json", "w"), indent=1, default=str)

if __name__ == "__main__":
    main()
