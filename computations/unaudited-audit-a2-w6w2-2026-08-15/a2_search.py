#!/usr/bin/env python3
"""AUDIT A2 -- independent template search (existence hunts).

Search only ever PROPOSES; every hit is re-verified by the pure-python
subset-DP hafnian in a2_core (exact integers).  The move set, cost function,
seeding and acceptance rule are written from scratch here; nothing is taken
from W6's annealers.

Families
  restricted : beta blocks are a single cell, every other support block
               carries all nine cells   (W6's collision8 family)
  general    : arbitrary cell sets, at least 2 cells on the non-single blocks
  diagonal   : every block a subset of the three diagonal cells

Structural constraints imposed (identical to W6's structural_ok, so that a
hit/miss is comparable): exactly m nonempty blocks, exactly beta single-cell
blocks, min support degree >= 3, all 3N (vertex,colour) slots covered, and
all three constant fibres nonempty.
"""

from __future__ import annotations

import json
import math
import random
import sys
import time

import numpy as np

from a2_core import (COLORS, audit_template, fibre_counts_dp_numpy,
                     fibre_counts_dp_python, geom, normalise_template)

CELLS = [(a, b) for a in COLORS for b in COLORS]
FULL = frozenset(CELLS)
DIAG = [(c, c) for c in COLORS]


def structural(g, t, m, beta):
    ne = [i for i, s in enumerate(t) if s]
    if len(ne) != m:
        return False
    if sum(1 for i in ne if len(t[i]) == 1) != beta:
        return False
    deg = [0] * g.n
    slots = set()
    for i in ne:
        u, v = g.edges[i]
        deg[u] += 1
        deg[v] += 1
        for a, b in t[i]:
            slots.add((u, a))
            slots.add((v, b))
    return min(deg) >= 3 and len(slots) == 3 * g.n


def score(g, t, m, beta):
    if not structural(g, t, m, beta):
        return None, None
    counts = fibre_counts_dp_numpy(g, t)
    missing = sum(1 for r in g.const_rows if counts[r] == 0)
    singles = int(np.count_nonzero((counts == 1) & g.mixed))
    return 1000 * missing + singles, {"missing": missing, "singletons": singles,
                                      "sigma": sum(len(s) for s in t)}


def cells_for(family, rng):
    if family == "restricted":
        return FULL
    if family == "diagonal":
        k = rng.choice([2, 3])
        return frozenset(rng.sample(DIAG, k))
    k = rng.choice([2, 3, 4, 5, 6, 9])
    return frozenset(rng.sample(CELLS, k))


def single_for(family, rng):
    if family == "diagonal":
        c = rng.randrange(3)
        return frozenset({(c, c)})
    return frozenset({rng.choice(CELLS)})


def seed(g, rng, m, beta, family, tries=4000):
    for _ in range(tries):
        chosen = rng.sample(range(len(g.edges)), m)
        singles = set(rng.sample(chosen, beta))
        t = [frozenset() for _ in g.edges]
        for i in chosen:
            t[i] = single_for(family, rng) if i in singles else cells_for(family, rng)
        if structural(g, t, m, beta):
            return t
    return None


def neighbour(g, rng, t, m, beta, family):
    out = [set(s) for s in t]
    ne = [i for i, s in enumerate(out) if s]
    singles = [i for i in ne if len(out[i]) == 1]
    multi = [i for i in ne if len(out[i]) >= 2]
    pool = CELLS if family != "diagonal" else DIAG
    r = rng.random()
    if r < 0.40 and singles:                       # recolour a single cell
        i = rng.choice(singles)
        out[i] = set(single_for(family, rng))
    elif r < 0.55 and singles and multi:           # exchange roles
        i, j = rng.choice(singles), rng.choice(multi)
        keep = set(out[j])
        out[i] = keep
        out[j] = set(single_for(family, rng))
    elif r < 0.75:                                 # relocate an edge
        empty = [i for i in range(len(g.edges)) if not out[i]]
        if not empty:
            return None
        src, dst = rng.choice(ne), rng.choice(empty)
        out[dst] = set(out[src])
        out[src] = set()
    elif family == "restricted":                   # nothing else to vary
        i = rng.choice(singles) if singles else rng.choice(ne)
        out[i] = set(single_for(family, rng)) if len(out[i]) == 1 else set(FULL)
    else:                                          # add / drop a cell
        if not multi:
            return None
        i = rng.choice(multi)
        if rng.random() < 0.5 and len(out[i]) < len(pool):
            out[i].add(rng.choice(pool))
        elif len(out[i]) > 2:
            out[i].discard(rng.choice(sorted(out[i])))
        else:
            return None
    return [frozenset(s) for s in out]


def hunt(g, rng, m, beta, family, seconds, t0=15.0, cool=0.9995):
    start = time.time()
    best = None
    while time.time() - start < seconds:
        t = seed(g, rng, m, beta, family)
        if t is None:
            return None, "no valid seed"
        cur, rec = score(g, t, m, beta)
        if cur is None:
            continue
        if best is None or cur < best[0]:
            best = (cur, rec, [sorted(s) for s in t])
        temp = t0
        while time.time() - start < seconds:
            temp = max(temp * cool, 0.05)
            cand = neighbour(g, rng, t, m, beta, family)
            if cand is None:
                continue
            val, rc = score(g, cand, m, beta)
            if val is None:
                continue
            if val <= cur or rng.random() < math.exp(-(val - cur) / temp):
                t, cur, rec = cand, val, rc
            if cur < best[0]:
                best = (cur, rec, [sorted(s) for s in t])
            if best[0] == 0:
                return best, "hit"
    return best, "budget exhausted"


def verify_hit(g, template):
    """Authoritative re-check with pure-python exact integer DP."""
    t = normalise_template(g, [[tuple(c) for c in s] for s in template])
    return audit_template(g, t, exact=True)


def main():
    args = sys.argv[1:]

    def opt(flag, default, cast=str):
        return cast(args[args.index(flag) + 1]) if flag in args else default

    n = opt("--size", 8, int)
    family = opt("--family", "general")
    budget = opt("--budget", 60.0, float)
    seed0 = opt("--seed", 20260815, int)
    jobs = opt("--jobs", "")            # "m:beta,m:beta,..."
    out = opt("--out", f"results_hunt_{family}_N{n}.json")
    g = geom(n)
    rng = random.Random(seed0)
    rows = []
    print(f"AUDIT A2 hunt: N={n} family={family} budget={budget}s seed={seed0}",
          flush=True)
    for job in jobs.split(","):
        m, beta = (int(x) for x in job.split(":"))
        best, status = hunt(g, rng, m, beta, family, budget)
        row = {"m": m, "beta": beta, "family": family, "status": status,
               "best_cost": None if best is None else best[0],
               "record": None if best is None else best[1]}
        if best is not None and best[0] == 0:
            row["template"] = best[2]
            row["independent_verification"] = verify_hit(g, best[2])
        rows.append(row)
        print(f"  m={m} beta={beta}: cost={row['best_cost']} "
              f"rec={row['record']} {status}"
              + ("  *** ZERO-SINGLETON CERTIFICATE ***"
                 if row.get("template") else ""), flush=True)
        with open(out, "w") as h:
            json.dump({"N": n, "family": family, "budget": budget,
                       "seed": seed0, "rows": rows}, h, indent=1, default=str)
    print(f"wrote {out}")


if __name__ == "__main__":
    sys.exit(main())
