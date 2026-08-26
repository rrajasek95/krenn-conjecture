#!/usr/bin/env python3
"""UNAUDITED PROBE (W6) -- the budget in W5's DIAGONAL regime.

Pinned HEAD: 31cefe2b247450d1168abc07f6dc73318c068e44

W5's diagonal-regime corollary (proved on 330 exact instances): an exact
DIAGONAL source has, for every (colour, site), a colour-exclusive incident
edge, hence

        beta_diag := #(colour-exclusive edges)  >=  12   at N = 8,          (W5)

and <= 16 full-rank pairs.  A colour-exclusive edge in the diagonal regime is
exactly a single DIAGONAL cell, so (W5) is a much stronger floor than J.1d's
beta >= 3N - m -- and it is uniform in m.  (Both are the same count: three
colours at each of N sites, each edge serving at most two, giving >= 3N/2.)

In the diagonal regime a block carries a SUBSET of {0,1,2} (the colours c
with A_e(c,c) != 0), a colouring is compatible with a matching iff it is
constant on every matched pair with that colour available, and

        Sigma = sum_e |colours(e)|  <=  3m.

This module measures, exactly, the largest beta_diag compatible with ZERO
mixed singletons at each support -- i.e. whether (W5) and the singleton law
collide inside the diagonal regime.

Run: python3 w6_task2_diagonal.py [--budget SECONDS]
"""

from __future__ import annotations

import json
import math
import random
import sys
import time

import numpy as np

from w6_task2_collision8 import geometry


def allowed(geo, colours):
    out = []
    for n, palette in enumerate(colours):
        u, v = geo.edges[n]
        if not palette:
            out.append(None)
            continue
        mask = geo.colour[:, u] == geo.colour[:, v]
        pick = np.zeros(len(geo.colour), dtype=bool)
        for c in palette:
            pick |= (geo.colour[:, u] == c)
        out.append(mask & pick)
    return out


def evaluate(geo, colours):
    arrays = allowed(geo, colours)
    total = np.zeros(len(geo.colour), dtype=np.int32)
    for indices in geo.matching_edges:
        mask = None
        ok = True
        for n in indices:
            if arrays[n] is None:
                ok = False
                break
            mask = arrays[n] if mask is None else (mask & arrays[n])
        if ok:
            total += mask
    missing = sum(1 for row in geo.constant_rows if total[row] == 0)
    singletons = int(np.count_nonzero((total == 1) & geo.mixed))
    return missing, singletons


def structural_ok(geo, colours, m, beta):
    nonempty = [n for n, s in enumerate(colours) if s]
    if len(nonempty) != m:
        return False
    if sum(1 for n in nonempty if len(colours[n]) == 1) != beta:
        return False
    degree = [0] * geo.size
    slots = set()
    for n in nonempty:
        u, v = geo.edges[n]
        degree[u] += 1
        degree[v] += 1
        for c in colours[n]:
            slots.add((u, c))
            slots.add((v, c))
    return min(degree) >= 3 and len(slots) == geo.size * 3


def cost(geo, colours, m, beta):
    if not structural_ok(geo, colours, m, beta):
        return None, None
    missing, singletons = evaluate(geo, colours)
    sigma = sum(len(s) for s in colours)
    return 500 * missing + singletons, {"missing": missing,
                                        "singletons": singletons,
                                        "sigma": sigma}


def seed(geo, rng, m, beta, tries=800):
    universe = list(range(len(geo.edges)))
    for _ in range(tries):
        edges = rng.sample(universe, m)
        singles = set(rng.sample(edges, beta))
        colours = [frozenset() for _ in geo.edges]
        for n in edges:
            if n in singles:
                colours[n] = frozenset({rng.randrange(3)})
            else:
                colours[n] = frozenset(rng.sample([0, 1, 2],
                                                  rng.choice([2, 2, 3])))
        if cost(geo, colours, m, beta)[0] is not None:
            return colours
    return None


def move(geo, rng, colours, m, beta):
    out = [set(s) for s in colours]
    nonempty = [n for n, s in enumerate(out) if s]
    singles = [n for n in nonempty if len(out[n]) == 1]
    multi = [n for n in nonempty if len(out[n]) >= 2]
    style = rng.random()
    if style < 0.4 and singles:
        n = rng.choice(singles)
        out[n] = {rng.randrange(3)}
    elif style < 0.7 and multi:
        n = rng.choice(multi)
        if len(out[n]) == 3:
            out[n].discard(rng.choice(sorted(out[n])))
        else:
            out[n].add(rng.randrange(3))
            if len(out[n]) < 2:
                return None
    elif style < 0.85 and singles and multi:
        a, b = rng.choice(singles), rng.choice(multi)
        out[a], out[b] = set(out[b]), {rng.randrange(3)}
    else:
        empty = [n for n in range(len(geo.edges)) if not out[n]]
        if not empty:
            return None
        src, dst = rng.choice(nonempty), rng.choice(empty)
        out[dst], out[src] = set(out[src]), set()
    return [frozenset(s) for s in out]


def hunt(geo, rng, m, beta, seconds):
    start = time.time()
    best = None
    while time.time() - start < seconds:
        colours = seed(geo, rng, m, beta)
        if colours is None:
            return None
        current, record = cost(geo, colours, m, beta)
        if best is None or current < best[0]:
            best = (current, record, [sorted(s) for s in colours])
        temperature = 12.0
        while time.time() - start < seconds:
            temperature = max(temperature * 0.9994, 0.05)
            candidate = move(geo, rng, colours, m, beta)
            if candidate is None:
                continue
            value, rec = cost(geo, candidate, m, beta)
            if value is None:
                continue
            if value <= current or rng.random() < math.exp(
                    -(value - current) / temperature):
                colours, current, record = candidate, value, rec
            if current < best[0]:
                best = (current, rec, [sorted(s) for s in colours])
            if best[0] == 0:
                return best
    return best


def main():
    args = sys.argv[1:]
    budget = float(args[args.index("--budget") + 1]) if "--budget" in args else 12.0
    geo = geometry(8)
    rng = random.Random(20260815)
    print("UNAUDITED PROBE (W6) -- diagonal regime (W5 corollary), "
          "HEAD 31cefe2", flush=True)
    print("   m   W5 floor beta>=12   beta* (max colour-exclusive edges at "
          "0 singletons)   collision?")
    rows = []
    for m in range(12, 29):
        feasible = []
        detail = {}
        for beta in range(0, m + 1):
            best = hunt(geo, rng, m, beta, budget if beta >= 10 else budget / 3)
            if best is None:
                continue
            detail[beta] = best[1]
            if best[0] == 0:
                feasible.append(beta)
        star = max(feasible) if feasible else None
        row = {"m": m, "w5_floor": 12, "beta_star": star,
               "feasible_betas": feasible,
               "per_beta": {str(k): v for k, v in detail.items()},
               "collision_evidence": star is None or star < 12}
        rows.append(row)
        print(f"  {m:2d}          12                    "
              f"{'none' if star is None else star:>4}"
              f"                              "
              f"{'YES' if row['collision_evidence'] else 'no'}", flush=True)
    with open("results_diagonal_N8.json", "w") as handle:
        json.dump({"N": 8, "budget": budget, "rows": rows}, handle, indent=1,
                  default=str)
    print("wrote results_diagonal_N8.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
