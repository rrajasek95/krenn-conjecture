#!/usr/bin/env python3
"""UNAUDITED PROBE (W6) -- the singleton CEILING over ARBITRARY cell templates.

Pinned HEAD: 31cefe2b247450d1168abc07f6dc73318c068e44

w6_task2_collision8.py searched the restricted family "non-single blocks are
FULL"; that gives only a LOWER bound on the ceiling

    beta*(N, m) = max { beta : some support-m cell template with exactly beta
                        single-cell blocks has NO mixed singleton }.

Here the search runs over ARBITRARY cell sets, so the estimate of beta* is as
strong as the annealer can make it.  Exact vectorised fibre counting:

    allowed_e[c] = 1 iff (c_u, c_v) is a cell of the block on e,
    fibre(c)     = #{ perfect matchings M : allowed_e[c] for every e in M },

computed for all 3^N colourings at once with integer/boolean numpy arrays.

Constraints imposed (all forced on an exact source):
  (T1) exactly m nonzero blocks;
  (T2) exactly beta of them a single cell;
  (T4) each constant colouring has a supported matching;
  (T6) every (vertex, colour) slot carries a cell;
  (T5) every vertex meets >= 3 nonzero blocks.

Reading the output.  beta* >= floor(3N - m) is a CERTIFICATE that the J.1d
floor is not by itself enough to force a mixed singleton at that support.
beta* < floor is EVIDENCE for the collision, never a proof (the search may
have missed a template).

Run: python3 w6_task2_ceiling.py [--size 8] [--budget SECONDS] [--only M,M,..]
"""

from __future__ import annotations

import json
import math
import random
import sys
import time

import numpy as np

from w6_task2_collision8 import Geo, geometry           # noqa: E402

CELLS = tuple((a, b) for a in range(3) for b in range(3))


def allowed_arrays(geo, template):
    """Boolean array per edge: which colourings the block permits."""
    out = []
    for n, support in enumerate(template):
        u, v = geo.edges[n]
        if not support:
            out.append(None)
            continue
        table = np.zeros((3, 3), dtype=bool)
        for a, b in support:
            table[a, b] = True
        out.append(table[geo.colour[:, u], geo.colour[:, v]])
    return out


def evaluate(geo, template):
    allowed = allowed_arrays(geo, template)
    total = np.zeros(len(geo.colour), dtype=np.int32)
    for indices in geo.matching_edges:
        mask = None
        ok = True
        for n in indices:
            if allowed[n] is None:
                ok = False
                break
            mask = allowed[n] if mask is None else (mask & allowed[n])
        if ok:
            total += mask
    missing = sum(1 for row in geo.constant_rows if total[row] == 0)
    singletons = int(np.count_nonzero((total == 1) & geo.mixed))
    return missing, singletons


def structural_ok(geo, template, m, beta):
    nonempty = [n for n, s in enumerate(template) if s]
    if len(nonempty) != m:
        return False
    if sum(1 for n in nonempty if len(template[n]) == 1) != beta:
        return False
    degree = [0] * geo.size
    slots = set()
    for n in nonempty:
        u, v = geo.edges[n]
        degree[u] += 1
        degree[v] += 1
        for a, b in template[n]:
            slots.add((u, a))
            slots.add((v, b))
    return min(degree) >= 3 and len(slots) == geo.size * 3


def cost(geo, template, m, beta):
    if not structural_ok(geo, template, m, beta):
        return None, None
    missing, singletons = evaluate(geo, template)
    return 500 * missing + singletons, {"missing": missing,
                                        "singletons": singletons,
                                        "sigma": sum(len(s) for s in template)}


def seed(geo, rng, m, beta, tries=600):
    universe = list(range(len(geo.edges)))
    for _ in range(tries):
        edges = rng.sample(universe, m)
        singles = set(rng.sample(edges, beta))
        template = [frozenset() for _ in geo.edges]
        for n in edges:
            if n in singles:
                template[n] = frozenset({rng.choice(CELLS)})
            else:
                size = rng.choice([2, 3, 4, 6, 9, 9])
                template[n] = frozenset(rng.sample(CELLS, size))
        value, record = cost(geo, template, m, beta)
        if value is not None:
            return template, value, record
    return None, None, None


def move(geo, rng, template, m, beta):
    out = [set(s) for s in template]
    nonempty = [n for n, s in enumerate(out) if s]
    multi = [n for n in nonempty if len(out[n]) >= 2]
    singles = [n for n in nonempty if len(out[n]) == 1]
    style = rng.random()
    if style < 0.35 and multi:                     # add a cell to a multi block
        n = rng.choice(multi)
        if len(out[n]) >= 9:
            return None
        out[n].add(rng.choice(CELLS))
    elif style < 0.6 and multi:                    # drop a cell (keep >= 2)
        n = rng.choice(multi)
        if len(out[n]) <= 2:
            return None
        out[n].discard(rng.choice(sorted(out[n])))
    elif style < 0.8 and singles:                  # recolour a single cell
        n = rng.choice(singles)
        out[n] = {rng.choice(CELLS)}
    elif style < 0.9 and singles and multi:        # swap single/multi roles
        a, b = rng.choice(singles), rng.choice(multi)
        keep = sorted(out[b])
        out[a] = set(rng.sample(keep, max(2, len(keep) - 1))
                     if len(keep) > 2 else keep)
        out[b] = {rng.choice(CELLS)}
    else:                                          # relocate a whole edge
        empty = [n for n in range(len(geo.edges)) if not out[n]]
        if not empty:
            return None
        src, dst = rng.choice(nonempty), rng.choice(empty)
        out[dst], out[src] = set(out[src]), set()
    return [frozenset(s) for s in out]


def hunt(geo, rng, m, beta, seconds, warm=None):
    start = time.time()
    best = None
    first = True
    while time.time() - start < seconds:
        if first and warm is not None:
            template = warm
            value, record = cost(geo, template, m, beta)
            first = False
            if value is None:
                continue
        else:
            template, value, record = seed(geo, rng, m, beta)
            if template is None:
                return None
        current = value
        if best is None or current < best[0]:
            best = (current, record, [sorted(s) for s in template])
        temperature = 10.0
        while time.time() - start < seconds:
            temperature = max(temperature * 0.9993, 0.05)
            candidate = move(geo, rng, template, m, beta)
            if candidate is None:
                continue
            value, record = cost(geo, candidate, m, beta)
            if value is None:
                continue
            if value <= current or rng.random() < math.exp(
                    -(value - current) / temperature):
                template, current = candidate, value
            if current < best[0]:
                best = (current, record, [sorted(s) for s in template])
            if best[0] == 0:
                return best
    return best


def full_warm(geo, rng, m, beta):
    """The 'non-single blocks full' configuration, used as a warm start."""
    universe = list(range(len(geo.edges)))
    for _ in range(300):
        edges = rng.sample(universe, m)
        singles = set(rng.sample(edges, beta))
        template = [frozenset() for _ in geo.edges]
        for n in edges:
            template[n] = (frozenset({rng.choice(CELLS)}) if n in singles
                           else frozenset(CELLS))
        if structural_ok(geo, template, m, beta):
            return template
    return None


def main():
    args = sys.argv[1:]
    size = int(args[args.index("--size") + 1]) if "--size" in args else 8
    budget = float(args[args.index("--budget") + 1]) if "--budget" in args else 6.0
    only = ([int(x) for x in args[args.index("--only") + 1].split(",")]
            if "--only" in args else None)
    print(f"UNAUDITED PROBE (W6) -- singleton ceiling (arbitrary cells), "
          f"N={size}, HEAD 31cefe2", flush=True)
    geo = geometry(size)
    rng = random.Random(20260815)
    edge_count = size * (size - 1) // 2
    supports = only or (list(range(3 * size // 2, edge_count + 1)) if size == 6
                        else [12, 16, 19, 21, 23, 25, 27, 28])
    report = {"N": size, "budget": budget, "rows": []}
    print("   m   floor(3N-m)   beta*   feasible betas at 0 singletons")
    for m in supports:
        floor = max(0, 3 * size - m)
        feasible = []
        detail = {}
        for beta in range(0, m + 1):
            seconds = budget * (3.0 if beta >= floor else 1.0)
            warm = full_warm(geo, rng, m, beta)
            best = hunt(geo, rng, m, beta, seconds, warm=warm)
            if best is None:
                continue
            detail[beta] = best[1]
            if best[0] == 0:
                feasible.append(beta)
        star = max(feasible) if feasible else None
        row = {"m": m, "floor": floor, "beta_star": star,
               "feasible_betas": feasible,
               "per_beta": {str(k): v for k, v in detail.items()},
               "collision_evidence": floor > 0 and (star is None
                                                    or star < floor)}
        report["rows"].append(row)
        print(f"  {m:2d}      {floor:3d}       "
              f"{'none' if star is None else star:>4}    {feasible}",
              flush=True)
    with open(f"results_ceiling_N{size}.json", "w") as handle:
        json.dump(report, handle, indent=1, default=str)
    print(f"wrote results_ceiling_N{size}.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
