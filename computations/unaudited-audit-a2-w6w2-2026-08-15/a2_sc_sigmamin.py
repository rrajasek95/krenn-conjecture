#!/usr/bin/env python3
"""AUDIT A2 -- Sigma_min under the SHARP slice-cover condition (SC).

Both W6 and W9 measured Sigma_min over templates that satisfy (T1)-(T6) but
NOT (SC) (see a2_slicecover.py: 0 of their 30 saved certificates satisfies it).
This module re-measures the singleton-free cell price inside the admissible
class:

    (T1) exactly m nonzero blocks
    (T4) all three constant fibres nonempty
    (T5) min support degree >= 3
    (SC) every (vertex,colour) slot is served by an incident block whose cells
         all carry that colour at the FAR endpoint
    (S)  no mixed singleton fibre

beta is NOT pinned (the budget only bounds it from below, and (SC) implies the
bound).  Cost = 400*(missing constants) + 40*(singletons) + 8*(unserved slots)
+ Sigma; the reported number is the smallest Sigma seen at zero cost on the
first three terms, re-verified exactly.
"""

from __future__ import annotations

import json
import math
import random
import sys
import time

import numpy as np

from a2_core import (COLORS, audit_template, fibre_counts_dp_numpy, geom,
                     normalise_template)
from a2_slicecover import slice_cover_report

CELLS = [(a, b) for a in COLORS for b in COLORS]


def evaluate(g, t, m):
    ne = [i for i, s in enumerate(t) if s]
    if len(ne) != m:
        return None, None
    deg = [0] * g.n
    for i in ne:
        u, v = g.edges[i]
        deg[u] += 1
        deg[v] += 1
    if min(deg) < 3:
        return None, None
    sc = slice_cover_report(g, t)
    counts = fibre_counts_dp_numpy(g, t)
    missing = sum(1 for r in g.const_rows if counts[r] == 0)
    singles = int(np.count_nonzero((counts == 1) & g.mixed))
    sigma = sum(len(s) for s in t)
    cost = 400 * missing + 40 * singles + 8 * sc["n_missing"] + sigma
    return cost, {"missing": missing, "singletons": singles,
                  "unserved": sc["n_missing"], "sigma": sigma}


def seed(g, rng, m):
    for _ in range(3000):
        chosen = rng.sample(range(len(g.edges)), m)
        t = [frozenset() for _ in g.edges]
        for i in chosen:
            k = rng.choice([1, 1, 1, 2, 2, 3])
            if k == 1:
                t[i] = frozenset({rng.choice(CELLS)})
            else:
                col = rng.randrange(3)
                rows = rng.sample(range(3), k)
                if rng.random() < 0.5:
                    t[i] = frozenset((r, col) for r in rows)
                else:
                    t[i] = frozenset((col, r) for r in rows)
        c, _ = evaluate(g, t, m)
        if c is not None:
            return t
    return None


def neighbour(g, rng, t, m):
    out = [set(s) for s in t]
    ne = [i for i, s in enumerate(out) if s]
    r = rng.random()
    if r < 0.45:
        i = rng.choice(ne)
        k = rng.choice([1, 1, 2, 3])
        if k == 1:
            out[i] = {rng.choice(CELLS)}
        else:
            col = rng.randrange(3)
            rows = rng.sample(range(3), k)
            out[i] = ({(x, col) for x in rows} if rng.random() < 0.5
                      else {(col, x) for x in rows})
    elif r < 0.7:
        i = rng.choice(ne)
        if len(out[i]) > 1 and rng.random() < 0.5:
            out[i].discard(rng.choice(sorted(out[i])))
        else:
            out[i].add(rng.choice(CELLS))
    else:
        empty = [i for i in range(len(g.edges)) if not out[i]]
        if not empty:
            return None
        src, dst = rng.choice(ne), rng.choice(empty)
        out[dst], out[src] = set(out[src]), set()
    return [frozenset(s) for s in out]


def hunt(g, rng, m, seconds):
    start = time.time()
    best = None
    while time.time() - start < seconds:
        t = seed(g, rng, m)
        if t is None:
            return None
        cur, rec = evaluate(g, t, m)
        temp = 30.0
        while time.time() - start < seconds:
            temp = max(temp * 0.9997, 0.4)
            cand = neighbour(g, rng, t, m)
            if cand is None:
                continue
            val, rc = evaluate(g, cand, m)
            if val is None:
                continue
            if val <= cur or rng.random() < math.exp(-(val - cur) / temp):
                t, cur, rec = cand, val, rc
            if (rc["missing"] == 0 and rc["singletons"] == 0
                    and rc["unserved"] == 0):
                if best is None or rc["sigma"] < best[0]:
                    best = (rc["sigma"], [sorted(s) for s in cand])
    return best


def main():
    args = sys.argv[1:]
    budget = float(args[args.index("--budget") + 1]) if "--budget" in args else 120.0
    ms = ([int(x) for x in args[args.index("--m") + 1].split(",")]
          if "--m" in args else [19, 22, 24, 27])
    seed0 = int(args[args.index("--seed") + 1]) if "--seed" in args else 909
    out = args[args.index("--out") + 1] if "--out" in args else "results_sc_sigmamin.json"
    g = geom(8)
    rng = random.Random(seed0)
    rows = []
    print(f"AUDIT A2 -- Sigma_min under (SC), budget {budget}s/support")
    for m in ms:
        best = hunt(g, rng, m, budget)
        row = {"m": m, "sigma_min_SC_upper": None if best is None else best[0]}
        if best is not None:
            t = normalise_template(g, [[tuple(c) for c in s] for s in best[1]])
            row["verification"] = audit_template(g, t, exact=True)
            row["slice_cover"] = slice_cover_report(g, t)
            row["template"] = best[1]
        rows.append(row)
        print(f"  m={m}: Sigma_min under (SC) <= {row['sigma_min_SC_upper']}"
              + ("" if best is None else
                 f"  [verified: singletons "
                 f"{row['verification']['mixed_singletons']}, "
                 f"beta {row['verification']['beta']}, "
                 f"SC ok {row['slice_cover']['SC_ok']}]"), flush=True)
        with open(out, "w") as h:
            json.dump({"rows": rows, "budget": budget}, h, indent=1, default=str)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
