#!/usr/bin/env python3
"""UNAUDITED PROBE (W6) -- J.1d RE-TARGETED (plan v6): the cell cost of
eliminating every mixed singleton.

Pinned HEAD: 31cefe2b247450d1168abc07f6dc73318c068e44

W1 re-axed route I: the useful conclusion is not "coordinate blocks" but
"some mixed class is a SINGLETON" (then O2 kills).  W1 proved the monomial
six-site case (every monomial source with nonzero pures has a singleton mixed
class) and exhibited a SIX-SITE falsifier that kills all singletons with ONE
noncoordinate block.  This module quantifies the cost at N = 8:

    How many multi-cell blocks, and how many cells, does a support-m template
    need before ZERO mixed singletons becomes achievable?

TWO INSTRUMENTS.

(I) AN EXACT COUNTING BOUND (no search).  For a cell template T let

        W(T)  = sum over perfect matchings M of  prod_{e in M} |S_e|
              = total number of (matching, cell-choice) pairs,
        A(T)  = number of colourings with a nonempty fibre.

    Every colouring in the support of the fibre map has fibre >= 1, so
        W = sum_c fibre(c) >= 2 A - #singletons, i.e.

        #singletons(T)  >=  2 A(T) - W(T).                            (SING)

    (SING) is exact and free; it is the honest "f" of the counting lemma.
    In R_cell (all |S_e| = 1) W = PM(G), the number of perfect matchings of
    the support graph, so
        #singletons >= 2 A - PM(G),
    and killing singletons requires the fibre map to be at least 2-to-1.

(II) AN ANNEALED HUNT minimising the singleton count at fixed
     (support m, total cells Sigma, per-block cap), with the exactness-forced
     constraints:
       * three constant colourings have a supported matching       (pures = 1);
       * every (vertex, colour) slot carries a cell -- i.e. every row of every
         vertex star is nonempty, which is the star identity
             e_k^{(x)(B\\p)} = sum_j (A_pj[k][.])^{(j)} (x) C_pj
         being nontrivial for each colour                            (rows);
       * every vertex meets >= 3 nonempty blocks                     (d_R >= 3
         relaxed to nonzero degree -- conservative).

CALIBRATION.  At m = 28 with every block a single cell (R_cell, Sigma = 28)
W2 found exactly 28 singleton-free templates; the hunt must reproduce
singleton-free survivors there and must NOT find them at m <= 27 in R_cell.

Run: python3 w6_task2_singleton_cost.py [--budget SECONDS]
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

SIZE = 8


# ------------------------------------------------------------- instrument (I)


def weight_and_reach(geo, cells):
    """W(T) and A(T) of (SING), plus the exact singleton count."""
    table = cell_fibres(geo, cells)
    total = 0
    for matching in geo.matchings:
        product = 1
        for u, v in matching:
            product *= len(cells[geo.index[(u, v)]])
            if product == 0:
                break
        total += product
    reach = len(table)
    singles = sum(1 for c, m in table.items() if is_mixed(c) and len(m) == 1)
    constants_present = all(table.get(tuple([r] * geo.size))
                            for r in range(Q))
    return {"W": total, "A": reach, "bound_2A_minus_W": 2 * reach - total,
            "singletons": singles, "constants_present": constants_present,
            "table": table}


# ------------------------------------------------------------ instrument (II)


def slots_covered(geo, cells):
    """Does every (vertex, colour) slot carry a cell?"""
    seen = set()
    for n, support in enumerate(cells):
        u, v = geo.edges[n]
        for a, b in support:
            seen.add((u, a))
            seen.add((v, b))
    return len(seen) == geo.size * Q


def structural_ok(geo, cells, m, sigma, cap):
    nonempty = [n for n, s in enumerate(cells) if s]
    if len(nonempty) != m:
        return False
    if sum(len(cells[n]) for n in nonempty) != sigma:
        return False
    if any(len(cells[n]) > cap for n in nonempty):
        return False
    degree = [0] * geo.size
    for n in nonempty:
        u, v = geo.edges[n]
        degree[u] += 1
        degree[v] += 1
    if min(degree) < 3:
        return False
    return slots_covered(geo, cells)


def score(geo, cells):
    """Objective: singletons, with a penalty for a missing constant fibre."""
    table = cell_fibres(geo, cells)
    penalty = sum(400 for r in range(Q)
                  if not table.get(tuple([r] * geo.size)))
    singles = sum(1 for c, ms in table.items() if is_mixed(c) and len(ms) == 1)
    return singles + penalty


def seed(geo, rng, m, sigma, cap, tries=600):
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
        nonempty = [n for n, s in enumerate(cells) if s]
        if len(nonempty) != m:
            continue
        guard = 0
        while sum(len(cells[n]) for n in nonempty) < sigma and guard < 4000:
            guard += 1
            n = rng.choice(nonempty)
            if len(cells[n]) >= cap:
                continue
            cells[n].add((rng.randrange(Q), rng.randrange(Q)))
        out = [frozenset(s) for s in cells]
        if structural_ok(geo, out, m, sigma, cap):
            return out
    return None


def move(geo, rng, cells, m, sigma, cap):
    out = [set(s) for s in cells]
    nonempty = [n for n, s in enumerate(out) if s]
    style = rng.random()
    if style < 0.7:                       # relocate one cell inside the same edge
        candidates = [n for n in nonempty if len(out[n]) >= 1]
        n = rng.choice(candidates)
        old = rng.choice(sorted(out[n]))
        out[n].discard(old)
        for _ in range(12):
            new = (rng.randrange(Q), rng.randrange(Q))
            if new not in out[n]:
                out[n].add(new)
                break
        else:
            out[n].add(old)
    elif style < 0.9:                     # move a cell between two edges
        donors = [n for n in nonempty if len(out[n]) >= 2]
        if not donors:
            return None
        src = rng.choice(donors)
        dst = rng.choice(nonempty)
        if dst == src or len(out[dst]) >= cap:
            return None
        cell = rng.choice(sorted(out[src]))
        out[src].discard(cell)
        if cell in out[dst]:
            return None
        out[dst].add(cell)
    else:                                 # relocate a whole edge
        empty = [n for n in range(len(geo.edges)) if not out[n]]
        if not empty:
            return None
        src, dst = rng.choice(nonempty), rng.choice(empty)
        out[dst], out[src] = set(out[src]), set()
    result = [frozenset(s) for s in out]
    return result if structural_ok(geo, result, m, sigma, cap) else None


def anneal(geo, rng, m, sigma, cap, seconds):
    start = time.time()
    best = None
    while time.time() - start < seconds:
        cells = seed(geo, rng, m, sigma, cap)
        if cells is None:
            return None
        current = score(geo, cells)
        if best is None or current < best[0]:
            best = (current, cells)
        temperature = 3.0
        while time.time() - start < seconds:
            temperature *= 0.9995
            candidate = move(geo, rng, cells, m, sigma, cap)
            if candidate is None:
                continue
            value = score(geo, candidate)
            if value <= current or rng.random() < math.exp(
                    -(value - current) / max(temperature, 1e-3)):
                cells, current = candidate, value
            if current < best[0]:
                best = (current, cells)
            if best[0] == 0:
                return best
    return best


def main():
    args = sys.argv[1:]
    budget = float(args[args.index("--budget") + 1]) if "--budget" in args else 8.0
    print("UNAUDITED PROBE (W6) -- singleton-elimination cost, HEAD 31cefe2",
          flush=True)
    geo = geometry(SIZE)
    rng = random.Random(20260815)
    report = {"budget_seconds_per_cell": budget, "grid": [],
              "calibration": {}}

    print("== calibration: R_cell (Sigma = m, cap 1) ==", flush=True)
    for m in (24, 26, 27, 28):
        best = anneal(geo, rng, m, m, 1, budget * 2)
        value = None if best is None else best[0]
        report["calibration"][f"m{m}"] = {
            "min_singletons": value,
            "survivor": value == 0,
            "template": None if best is None or value != 0
            else [sorted(s) for s in best[1]]}
        print(f"  m={m} R_cell: min singletons {value} "
              f"({'SURVIVOR' if value == 0 else 'killed'})", flush=True)

    print("== grid: support m x total cells Sigma (cap 9) ==", flush=True)
    print("   m  Sigma  multi-cell blocks(min)  min#singletons  verdict")
    for m in (19, 21, 23, 25, 27):
        for extra in (0, 2, 4, 6, 8, 12, 16, 24, 32):
            sigma = m + extra
            if sigma > 9 * m:
                continue
            best = anneal(geo, rng, m, sigma, 9, budget)
            if best is None:
                continue
            value = best[0]
            multi = sum(1 for s in best[1] if len(s) >= 2)
            row = {"m": m, "sigma": sigma, "extra_cells": extra,
                   "multi_cell_blocks": multi, "min_singletons": value,
                   "survivor": value == 0}
            if value == 0:
                stats = weight_and_reach(geo, best[1])
                row["W"] = stats["W"]
                row["A"] = stats["A"]
                row["bound_2A_minus_W"] = stats["bound_2A_minus_W"]
                row["template"] = [sorted(s) for s in best[1]]
            report["grid"].append(row)
            print(f"  {m:2d}  {sigma:5d}  {multi:20d}  {value:14d}  "
                  f"{'SURVIVOR' if value == 0 else 'killed'}", flush=True)
            if value == 0:
                break            # minimal Sigma for this m located
    with open("results_singleton_cost.json", "w") as handle:
        json.dump(report, handle, indent=1, default=str)
    print("wrote results_singleton_cost.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
