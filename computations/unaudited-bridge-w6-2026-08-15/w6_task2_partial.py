#!/usr/bin/env python3
"""UNAUDITED PROBE (W6) -- J.1d part 2: does a PARTIAL monomial regime already
force a mixed singleton?

Pinned HEAD: 31cefe2b247450d1168abc07f6dc73318c068e44

J.1d (this directory, w6_task2_counting.py) gives, on an exact N-site source
of support m,

    beta := #(blocks that are a single coordinate cell)  >=  3N - m + |H|,

so on the committed N = 8 band 19..27 between 5 and 0 blocks are FORCED to be
coordinate cells.  W2 proved J.2 when EVERY block is a single cell (R_cell).
The question this module measures: how many single-cell blocks must a
template carry before a mixed singleton is unavoidable?

TEMPLATE MODEL (support level, gauge-free).  For each of the 28 edges a cell
set S_e subset {0,1,2}^2.  Constraints imposed, all of them consequences of
exactness or of the committed structure:

  (T1) exactly m edges nonempty                              (band support);
  (T2) exactly beta of them are singletons |S_e| = 1         (J.1d floor);
  (T3) every other nonempty S_e has |S_e| >= 2               (non-basis blocks
       cost >= 2 cells -- the cell trade of J.1d);
  (T4) for each colour r some perfect matching has (r,r) in S_e on all its
       edges                                    (constant coefficient = 1);
  (T5) every vertex meets >= 3 nonempty blocks   (weak form of d_R(v) >= 3;
       the true hypothesis is about RANK-ONE neighbours, so (T5) is a
       relaxation and can only make survivors MORE common -- conservative).

A mixed singleton is a non-constant colouring whose compatibility graph has
exactly one perfect matching; its coefficient is then a nonzero monomial and
the template is dead (mechanism O2 of the committed six-site proof).

The hunt MINIMISES the singleton count by annealing.  "survivor" = a template
with zero mixed singletons -- i.e. the partial regime is NOT enough at that
(m, beta, cap).  Reported: the largest beta at which a survivor is found.

Run: python3 w6_task2_partial.py [--budget SECONDS]
"""

from __future__ import annotations

import json
import random
import sys
import time
from itertools import combinations

W2 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
      "unaudited-witness-splitting-w2-2026-08-15")
if W2 not in sys.path:
    sys.path.insert(0, W2)

from w2_monomial import Q, geometry, is_mixed          # noqa: E402
from w2_cells import analyse_cells, cell_fibres        # noqa: E402

SIZE = 8


def singleton_count(geo, cells):
    table = cell_fibres(geo, cells)
    for colour in range(Q):
        if not table.get(tuple([colour] * geo.size)):
            return None, table               # (T4) violated
    return sum(1 for c, m in table.items() if is_mixed(c) and len(m) == 1), table


def valid(geo, cells, m, beta, cap):
    nonempty = [n for n, s in enumerate(cells) if s]
    if len(nonempty) != m:
        return False
    singles = sum(1 for n in nonempty if len(cells[n]) == 1)
    if singles != beta:
        return False
    if any(len(cells[n]) > cap for n in nonempty):
        return False
    if any(len(cells[n]) == 1 for n in nonempty) and singles == 0:
        return False
    degree = [0] * geo.size
    for n in nonempty:
        u, v = geo.edges[n]
        degree[u] += 1
        degree[v] += 1
    return min(degree) >= 3


def seed_template(geo, rng, m, beta, cap):
    """Build a template satisfying (T1)-(T5); the three constant matchings first."""
    for _ in range(400):
        cells = [set() for _ in geo.edges]
        chosen = [rng.randrange(len(geo.matchings)) for _ in range(Q)]
        for colour, number in enumerate(chosen):
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
        # force exactly beta singletons: pad the others up to >= 2 cells
        rng.shuffle(nonempty)
        singles = [n for n in nonempty if len(cells[n]) == 1]
        rng.shuffle(singles)
        keep = set(singles[:beta])
        for n in nonempty:
            if n in keep:
                continue
            while len(cells[n]) < 2:
                cells[n].add((rng.randrange(Q), rng.randrange(Q)))
        out = [frozenset(s) for s in cells]
        if valid(geo, out, m, beta, cap):
            return out
    return None


def neighbour(geo, rng, cells, m, beta, cap):
    out = [set(s) for s in cells]
    nonempty = [n for n, s in enumerate(out) if s]
    kind = rng.random()
    if kind < 0.6:
        big = [n for n in nonempty if len(out[n]) >= 2]
        if not big:
            return None
        n = rng.choice(big)
        cell = (rng.randrange(Q), rng.randrange(Q))
        if rng.random() < 0.5 and len(out[n]) > 2:
            out[n].discard(rng.choice(sorted(out[n])))
        else:
            if len(out[n]) >= cap:
                return None
            out[n].add(cell)
    else:
        empty = [n for n in range(len(geo.edges)) if not out[n]]
        if not empty:
            return None
        source = rng.choice(nonempty)
        target = rng.choice(empty)
        out[target] = set(out[source])
        out[source] = set()
    result = [frozenset(s) for s in out]
    return result if valid(geo, result, m, beta, cap) else None


def hunt(geo, rng, m, beta, cap, seconds, restarts=8):
    best = None
    start = time.time()
    while time.time() - start < seconds:
        cells = seed_template(geo, rng, m, beta, cap)
        if cells is None:
            break
        score, _table = singleton_count(geo, cells)
        if score is None:
            continue
        steps = 0
        while time.time() - start < seconds and steps < 4000:
            steps += 1
            candidate = neighbour(geo, rng, cells, m, beta, cap)
            if candidate is None:
                continue
            value, _t = singleton_count(geo, candidate)
            if value is None:
                continue
            if value <= score:
                cells, score = candidate, value
            if score == 0:
                break
        if best is None or score < best[0]:
            best = (score, [sorted(s) for s in cells])
        if best[0] == 0:
            break
        restarts -= 1
        if restarts <= 0:
            break
    return best


def main():
    args = sys.argv[1:]
    budget = float(args[args.index("--budget") + 1]) if "--budget" in args else 6.0
    print("UNAUDITED PROBE (W6) -- partial monomial regime, HEAD 31cefe2",
          flush=True)
    geo = geometry(SIZE)
    rng = random.Random(20260815)
    report = {"budget_seconds_per_cell": budget, "grid": []}
    print("   m  beta  cap  min#mixed-singletons  survivor(0)?  verdict")
    for m in (19, 21, 23, 25, 27):
        for cap in (2, 3, 9):
            for beta in (0, 2, 4, 6, 8, 12, 16, m):
                if beta > m:
                    continue
                best = hunt(geo, rng, m, beta, cap, budget)
                if best is None:
                    row = {"m": m, "beta": beta, "cap": cap,
                           "min_singletons": None, "note": "no valid template"}
                else:
                    row = {"m": m, "beta": beta, "cap": cap,
                           "min_singletons": best[0],
                           "survivor": best[0] == 0}
                report["grid"].append(row)
                value = row.get("min_singletons")
                mark = ("n/a" if value is None
                        else ("SURVIVOR" if value == 0 else "killed"))
                print(f"  {m:2d}  {beta:4d}  {cap:3d}  "
                      f"{'--' if value is None else value:>20}  "
                      f"{mark}", flush=True)
    with open("results_partial.json", "w") as handle:
        json.dump(report, handle, indent=1, default=str)
    print("wrote results_partial.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
