#!/usr/bin/env python3
"""UNAUDITED PROBE (W6) -- the J.1d / singleton COLLISION, measured properly.

Pinned HEAD: 31cefe2b247450d1168abc07f6dc73318c068e44

beta = #(blocks that are a single cell)  =  #basis edges.

  FLOOR   (J.1d, from slice-cover):    beta >= 3N - m   on an exact source of
                                       support m.
  CEILING (this module):               beta*(N, m) := max { beta : some
                                       support-m template with beta single
                                       cells has NO mixed singleton }.

If beta*(N, m) < 3N - m for every m the two budgets collide and every exact
source carries a mixed singleton (O2 kills it).

SEARCH DESIGN (why this is close to extremal).  At fixed beta, the way to make
mixed fibres large -- and hence singletons rare -- is to give every NON-single
block as many cells as possible.  We therefore search over

    * which m edges are nonzero,
    * which beta of them are single cells and which cell each carries,

with every other nonzero block carrying ALL NINE cells.  Adding cells to a
block can only enlarge each existing fibre, so this is the natural extremal
family at fixed beta; a zero-singleton template found here is a genuine
certificate, and a failure here is strong (not conclusive) evidence that
beta is above the ceiling.  Sanity anchors: beta = 0 with every block full
must give 0 singletons; beta = m (R_cell) at N = 6 must give >= 1 (W1's
exhaustive monomial result) and at N = 8, m <= 27 must give >= 1 (W2).

Run: python3 w6_task2_collision.py [--size 6|8] [--budget SECONDS]
"""

from __future__ import annotations

import json
import math
import random
import sys
import time
from itertools import product

W2 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
      "unaudited-witness-splitting-w2-2026-08-15")
if W2 not in sys.path:
    sys.path.insert(0, W2)

from w2_monomial import Q, geometry, is_mixed          # noqa: E402
from w2_cells import cell_fibres                       # noqa: E402

FULL = frozenset((a, b) for a in range(Q) for b in range(Q))


def build(geo, edges, singles):
    """edges: set of nonzero edge indices; singles: {index: (a,b)}."""
    cells = []
    for n in range(len(geo.edges)):
        if n not in edges:
            cells.append(frozenset())
        elif n in singles:
            cells.append(frozenset({singles[n]}))
        else:
            cells.append(FULL)
    return cells


def evaluate(geo, cells):
    table = cell_fibres(geo, cells)
    missing = sum(1 for r in range(Q)
                  if not table.get(tuple([r] * geo.size)))
    singles = sum(1 for c, ms in table.items() if is_mixed(c) and len(ms) == 1)
    return missing, singles


def degrees_ok(geo, edges):
    degree = [0] * geo.size
    for n in edges:
        u, v = geo.edges[n]
        degree[u] += 1
        degree[v] += 1
    return min(degree) >= 3


def slots_ok(geo, cells):
    slots = set()
    for n, support in enumerate(cells):
        u, v = geo.edges[n]
        for a, b in support:
            slots.add((u, a))
            slots.add((v, b))
    return len(slots) == geo.size * Q


def cost(geo, edges, singles):
    cells = build(geo, edges, singles)
    if not slots_ok(geo, cells):
        return 10 ** 6, None
    missing, singletons = evaluate(geo, cells)
    return 500 * missing + singletons, {"missing": missing,
                                        "singletons": singletons}


def seed(geo, rng, m, beta, tries=400):
    universe = list(range(len(geo.edges)))
    for _ in range(tries):
        edges = set(rng.sample(universe, m))
        if not degrees_ok(geo, edges):
            continue
        chosen = rng.sample(sorted(edges), beta)
        singles = {n: (rng.randrange(Q), rng.randrange(Q)) for n in chosen}
        return edges, singles
    return None, None


def move(geo, rng, m, beta, edges, singles):
    edges = set(edges)
    singles = dict(singles)
    style = rng.random()
    if style < 0.55 and singles:            # recolour one single cell
        n = rng.choice(sorted(singles))
        singles[n] = (rng.randrange(Q), rng.randrange(Q))
    elif style < 0.8 and singles and len(edges) > beta:   # move the single slot
        old = rng.choice(sorted(singles))
        candidates = [n for n in edges if n not in singles]
        if not candidates:
            return None
        new = rng.choice(candidates)
        value = singles.pop(old)
        singles[new] = value
    else:                                   # move a nonzero edge
        outside = [n for n in range(len(geo.edges)) if n not in edges]
        if not outside:
            return None
        drop = rng.choice(sorted(edges))
        add = rng.choice(outside)
        edges.discard(drop)
        edges.add(add)
        if drop in singles:
            singles[add] = singles.pop(drop)
        if not degrees_ok(geo, edges):
            return None
    return edges, singles


def hunt(geo, rng, m, beta, seconds):
    start = time.time()
    best = None
    while time.time() - start < seconds:
        edges, singles = seed(geo, rng, m, beta)
        if edges is None:
            return None
        current, record = cost(geo, edges, singles)
        if best is None or current < best[0]:
            best = (current, record, sorted(edges), dict(singles))
        temperature = 12.0
        while time.time() - start < seconds:
            temperature = max(temperature * 0.9995, 0.05)
            candidate = move(geo, rng, m, beta, edges, singles)
            if candidate is None:
                continue
            value, rec = cost(geo, *candidate)
            if value <= current or rng.random() < math.exp(
                    -(value - current) / temperature):
                edges, singles = candidate
                current, record = value, rec
            if current < best[0]:
                best = (current, rec, sorted(edges), dict(singles))
            if best[0] == 0:
                return best
    return best


def main():
    args = sys.argv[1:]
    size = int(args[args.index("--size") + 1]) if "--size" in args else 6
    budget = float(args[args.index("--budget") + 1]) if "--budget" in args else 10.0
    print(f"UNAUDITED PROBE (W6) -- J.1d/singleton collision, N={size}, "
          "HEAD 31cefe2", flush=True)
    geo = geometry(size)
    rng = random.Random(20260815)
    edge_count = size * (size - 1) // 2
    supports = (list(range(3 * size // 2, edge_count + 1)) if size == 6
                else [12, 16, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28])
    report = {"N": size, "budget": budget, "rows": []}
    print("   m   floor(3N-m)   beta*(max beta at 0 singletons)   collision?")
    for m in supports:
        star = None
        detail = {}
        feasible = []
        floor = max(0, 3 * size - m)
        # scan every beta (no early break: the feasible set need not be an
        # interval), but spend the budget where it matters -- at and above the
        # J.1d floor.
        for beta in range(0, m + 1):
            seconds = budget * (3.0 if beta >= floor else 1.0)
            best = hunt(geo, rng, m, beta, seconds)
            if best is None:
                continue
            detail[beta] = best[1]
            if best[0] == 0:
                feasible.append(beta)
                star = beta if star is None else max(star, beta)
        row = {"m": m, "floor": floor, "beta_star": star,
               "feasible_betas": feasible,
               "per_beta": {str(k): v for k, v in detail.items()},
               "collision": floor > 0 and (star is None or star < floor)}
        report["rows"].append(row)
        print(f"  {m:2d}      {floor:3d}                    "
              f"{'none' if star is None else star:>4}"
              f"                       "
              f"{'YES' if row['collision'] else 'no'}", flush=True)
    with open(f"results_collision_N{size}.json", "w") as handle:
        json.dump(report, handle, indent=1, default=str)
    print(f"wrote results_collision_N{size}.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
