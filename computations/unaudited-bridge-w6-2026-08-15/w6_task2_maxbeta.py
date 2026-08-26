#!/usr/bin/env python3
"""UNAUDITED PROBE (W6) -- the decisive form of J.1d (plan v6.1).

Pinned HEAD: 31cefe2b247450d1168abc07f6dc73318c068e44

THE COLLISION.  Two independent budgets act on the same integer:

  beta := #(aggregate blocks that are a SINGLE cell)  ("basis edges").

  * J.1d FLOOR (this directory, w6_task2_counting.py; from slice-cover's
    forced-incidence theorem):  an exact N-site source of support m has
                beta >= 3N - m  (indeed >= 3N - |R| = 3N - m + |H|).
  * SINGLETON CEILING (W1's re-axing; W2/W1 exhaustions):  killing every
    mixed singleton costs multi-cell blocks, i.e. it CAPS beta from above.

If  max{ beta : template of support m has NO mixed singleton }  <  3N - m
for every m, then every exact source has a mixed singleton, O2 fires, and
route I closes at that N without any coordinate hypothesis.

This module measures the ceiling.  For each (N, m) it anneals over cell
templates minimising

        50 * (#mixed singleton colourings)  +  (#multi-cell blocks),

subject to the exactness-forced structure
  (T4) each constant colouring has a supported perfect matching;
  (T6) every (vertex, colour) slot carries a cell   (each row of each vertex
       star is nonempty -- the star identity for that colour is nontrivial);
  (T5) every vertex meets >= 3 nonzero blocks.
and reports the best (singletons, beta) frontier found, against the floor.

CAUTION.  This is a SEARCH: "no zero-singleton template found with beta >= b"
is evidence, not proof.  The N = 6 monomial case (beta = m) is proved by W1
exhaustively; the calibration below must reproduce it.

Run: python3 w6_task2_maxbeta.py [--size 6|8] [--budget SECONDS]
"""

from __future__ import annotations

import json
import math
import random
import sys
import time

W2 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
      "unaudited-witness-splitting-w2-2026-08-15")
if W2 not in sys.path:
    sys.path.insert(0, W2)

from w2_monomial import Q, geometry, is_mixed          # noqa: E402
from w2_cells import cell_fibres                       # noqa: E402


def profile(geo, cells):
    table = cell_fibres(geo, cells)
    missing = sum(1 for r in range(Q)
                  if not table.get(tuple([r] * geo.size)))
    singles = sum(1 for c, ms in table.items() if is_mixed(c) and len(ms) == 1)
    nonempty = [n for n, s in enumerate(cells) if s]
    beta = sum(1 for n in nonempty if len(cells[n]) == 1)
    return {"missing_constants": missing, "singletons": singles,
            "m": len(nonempty), "beta": beta,
            "sigma": sum(len(cells[n]) for n in nonempty),
            "multi": len(nonempty) - beta}


def structural_ok(geo, cells, m):
    nonempty = [n for n, s in enumerate(cells) if s]
    if len(nonempty) != m:
        return False
    degree = [0] * geo.size
    slots = set()
    for n in nonempty:
        u, v = geo.edges[n]
        degree[u] += 1
        degree[v] += 1
        for a, b in cells[n]:
            slots.add((u, a))
            slots.add((v, b))
    return min(degree) >= 3 and len(slots) == geo.size * Q


def cost(geo, cells):
    rec = profile(geo, cells)
    return (400 * rec["missing_constants"] + 50 * rec["singletons"]
            + rec["multi"]), rec


def seed(geo, rng, m, tries=800):
    for _ in range(tries):
        cells = [set() for _ in geo.edges]
        for colour in range(Q):
            number = rng.randrange(len(geo.matchings))
            for edge in geo.matchings[number]:
                cells[geo.index[edge]].add((colour, colour))
        used = [n for n, s in enumerate(cells) if s]
        if len(used) > m:
            continue
        free = [n for n in range(len(geo.edges)) if not cells[n]]
        rng.shuffle(free)
        for n in free[:m - len(used)]:
            cells[n].add((rng.randrange(Q), rng.randrange(Q)))
        out = [frozenset(s) for s in cells]
        if structural_ok(geo, out, m):
            return out
    return None


def move(geo, rng, cells, m):
    out = [set(s) for s in cells]
    nonempty = [n for n, s in enumerate(out) if s]
    style = rng.random()
    if style < 0.45:                       # add a cell
        n = rng.choice(nonempty)
        if len(out[n]) >= 9:
            return None
        out[n].add((rng.randrange(Q), rng.randrange(Q)))
    elif style < 0.8:                      # drop a cell
        big = [n for n in nonempty if len(out[n]) >= 2]
        if not big:
            return None
        n = rng.choice(big)
        out[n].discard(rng.choice(sorted(out[n])))
    elif style < 0.93:                     # relocate a cell inside an edge
        n = rng.choice(nonempty)
        old = rng.choice(sorted(out[n]))
        out[n].discard(old)
        out[n].add((rng.randrange(Q), rng.randrange(Q)))
        if not out[n]:
            out[n].add(old)
    else:                                  # move a whole edge
        empty = [n for n in range(len(geo.edges)) if not out[n]]
        if not empty:
            return None
        src, dst = rng.choice(nonempty), rng.choice(empty)
        out[dst], out[src] = set(out[src]), set()
    result = [frozenset(s) for s in out]
    return result if structural_ok(geo, result, m) else None


def anneal(geo, rng, m, seconds):
    start = time.time()
    best = None                    # (cost, record, cells)
    best_zero = None               # best beta among zero-singleton templates
    while time.time() - start < seconds:
        cells = seed(geo, rng, m)
        if cells is None:
            return None, None
        current, rec = cost(geo, cells)
        temperature = 20.0
        while time.time() - start < seconds:
            temperature = max(temperature * 0.9997, 0.05)
            candidate = move(geo, rng, cells, m)
            if candidate is None:
                continue
            value, record = cost(geo, candidate)
            if value <= current or rng.random() < math.exp(
                    -(value - current) / temperature):
                cells, current, rec = candidate, value, record
            if best is None or current < best[0]:
                best = (current, rec, [sorted(s) for s in cells])
            if (rec["singletons"] == 0 and rec["missing_constants"] == 0
                    and (best_zero is None or rec["beta"] > best_zero[0])):
                best_zero = (rec["beta"], dict(rec),
                             [sorted(s) for s in cells])
    return best, best_zero


def main():
    args = sys.argv[1:]
    size = int(args[args.index("--size") + 1]) if "--size" in args else 6
    budget = float(args[args.index("--budget") + 1]) if "--budget" in args else 20.0
    print(f"UNAUDITED PROBE (W6) -- max beta at zero singletons, N={size}, "
          "HEAD 31cefe2", flush=True)
    geo = geometry(size)
    rng = random.Random(20260815)
    floor = 3 * size
    supports = (range(3 * size // 2, size * (size - 1) // 2 + 1)
                if size == 6 else (12, 14, 16, 18, 19, 20, 21, 22, 23,
                                   24, 25, 26, 27, 28))
    report = {"N": size, "budget": budget, "rows": []}
    print("   m   J.1d floor beta>=   best zero-singleton beta   min singletons"
          "   COLLISION?")
    for m in supports:
        best, best_zero = anneal(geo, rng, m, budget)
        if best is None:
            continue
        needed = max(0, floor - m)
        zero_beta = None if best_zero is None else best_zero[0]
        collision = (zero_beta is None or zero_beta < needed) and needed > 0
        row = {"m": m, "floor_beta": needed,
               "max_beta_at_zero_singletons": zero_beta,
               "best_cost_record": best[1],
               "collision": collision}
        if best_zero is not None:
            row["zero_singleton_record"] = best_zero[1]
            row["zero_singleton_template"] = best_zero[2]
        report["rows"].append(row)
        print(f"  {m:2d}       {needed:3d}                "
              f"{'none' if zero_beta is None else zero_beta:>8}"
              f"              {best[1]['singletons']:4d}          "
              f"{'YES' if collision else 'no'}", flush=True)
    with open(f"results_maxbeta_N{size}.json", "w") as handle:
        json.dump(report, handle, indent=1, default=str)
    print(f"wrote results_maxbeta_N{size}.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
