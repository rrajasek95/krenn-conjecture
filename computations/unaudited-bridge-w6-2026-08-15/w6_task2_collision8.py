#!/usr/bin/env python3
"""UNAUDITED PROBE (W6) -- the J.1d / singleton COLLISION at N = 8 (fast).

Pinned HEAD: 31cefe2b247450d1168abc07f6dc73318c068e44

Same measurement as w6_task2_collision.py, with an exact vectorised fibre
counter so that N = 8 (6,561 colourings, 105 matchings) is searchable.

FAMILY.  beta blocks are a single cell; every other nonzero block carries ALL
NINE cells; the remaining blocks are zero.  Then a matching M is compatible
with a colouring c exactly when every SINGLE-CELL edge uv in M has
(c_u, c_v) equal to its cell, so

        fibre(c) = #{ M subset support : cell(e) = (c_u,c_v) for every
                      single-cell e in M },

computed for all 3^N colourings at once by boolean masks.  Everything is
exact integer arithmetic (numpy int32 counts, no floats in the verdict).

Verdicts: "0 singletons" = a certificate that beta single cells are NOT
enough to force O2; "no zero-singleton template found" = evidence for the
collision at that (m, beta).

CONTROL.  beta = 0 (every nonzero block full) must give 0 mixed singletons;
beta = m at N = 8, m <= 27 (R_cell) must give >= 1 (W2's exhaustion).

Run: python3 w6_task2_collision8.py [--size 8] [--budget SECONDS]
"""

from __future__ import annotations

import json
import math
import random
import sys
import time
from itertools import combinations

import numpy as np


def perfect_matchings(vertices):
    if not vertices:
        return [()]
    first = vertices[0]
    out = []
    for index in range(1, len(vertices)):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            out.append(((first, vertices[index]),) + tail)
    return out


class Geo:
    def __init__(self, size):
        self.size = size
        self.edges = tuple(combinations(range(size), 2))
        self.index = {e: n for n, e in enumerate(self.edges)}
        self.matchings = tuple(perfect_matchings(tuple(range(size))))
        self.matching_edges = tuple(tuple(self.index[e] for e in m)
                                    for m in self.matchings)
        colours = np.indices((3,) * size).reshape(size, -1).T
        self.colour = np.ascontiguousarray(colours.astype(np.int8))
        self.mixed = (self.colour != self.colour[:, :1]).any(axis=1)
        self.constant_rows = [int(np.ravel_multi_index(
            tuple([r] * size), (3,) * size)) for r in range(3)]


GEO = {}


def geometry(size):
    if size not in GEO:
        GEO[size] = Geo(size)
    return GEO[size]


def fibres(geo, edges, singles):
    """Exact fibre counts for every colouring, as an int32 array."""
    total = np.zeros(len(geo.colour), dtype=np.int32)
    edgeset = edges
    for number, indices in enumerate(geo.matching_edges):
        if any(n not in edgeset for n in indices):
            continue
        mask = None
        for n, (u, v) in zip(indices, geo.matchings[number]):
            cell = singles.get(n)
            if cell is None:
                continue
            piece = (geo.colour[:, u] == cell[0]) & (geo.colour[:, v] == cell[1])
            mask = piece if mask is None else (mask & piece)
        if mask is None:
            total += 1
        else:
            total += mask
    return total


def evaluate(geo, edges, singles):
    counts = fibres(geo, edges, singles)
    missing = sum(1 for row in geo.constant_rows if counts[row] == 0)
    singletons = int(np.count_nonzero((counts == 1) & geo.mixed))
    return missing, singletons


def degrees_ok(geo, edges):
    degree = [0] * geo.size
    for n in edges:
        u, v = geo.edges[n]
        degree[u] += 1
        degree[v] += 1
    return min(degree) >= 3


def slots_ok(geo, edges, singles):
    slots = set()
    for n in edges:
        u, v = geo.edges[n]
        cell = singles.get(n)
        if cell is None:
            for a in range(3):
                slots.add((u, a))
                slots.add((v, a))
        else:
            slots.add((u, cell[0]))
            slots.add((v, cell[1]))
    return len(slots) == geo.size * 3


def cost(geo, edges, singles):
    if not slots_ok(geo, edges, singles):
        return 10 ** 6, None
    missing, singletons = evaluate(geo, edges, singles)
    return 500 * missing + singletons, {"missing": missing,
                                        "singletons": singletons}


def seed(geo, rng, m, beta, tries=800):
    universe = list(range(len(geo.edges)))
    for _ in range(tries):
        edges = frozenset(rng.sample(universe, m))
        if not degrees_ok(geo, edges):
            continue
        chosen = rng.sample(sorted(edges), beta)
        singles = {n: (rng.randrange(3), rng.randrange(3)) for n in chosen}
        return edges, singles
    return None, None


def move(geo, rng, m, beta, edges, singles):
    edges = set(edges)
    singles = dict(singles)
    style = rng.random()
    if style < 0.55 and singles:
        n = rng.choice(sorted(singles))
        singles[n] = (rng.randrange(3), rng.randrange(3))
    elif style < 0.8 and singles and len(edges) > beta:
        old = rng.choice(sorted(singles))
        candidates = [n for n in edges if n not in singles]
        if not candidates:
            return None
        new = rng.choice(candidates)
        singles[new] = singles.pop(old)
    else:
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
    return frozenset(edges), singles


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
            temperature = max(temperature * 0.9993, 0.05)
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
    size = int(args[args.index("--size") + 1]) if "--size" in args else 8
    budget = float(args[args.index("--budget") + 1]) if "--budget" in args else 6.0
    print(f"UNAUDITED PROBE (W6) -- collision at N={size}, HEAD 31cefe2",
          flush=True)
    geo = geometry(size)
    rng = random.Random(20260815)
    edge_count = size * (size - 1) // 2
    supports = (list(range(3 * size // 2, edge_count + 1)) if size == 6
                else [12, 13, 14, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28])
    report = {"N": size, "budget": budget, "rows": []}
    print("   m   floor(3N-m)   beta* (max beta with 0 singletons)   collision?")
    for m in supports:
        floor = max(0, 3 * size - m)
        detail = {}
        feasible = []
        for beta in range(0, m + 1):
            seconds = budget * (3.0 if beta >= floor else 1.0)
            best = hunt(geo, rng, m, beta, seconds)
            if best is None:
                continue
            detail[beta] = best[1]
            if best[0] == 0:
                feasible.append(beta)
        star = max(feasible) if feasible else None
        row = {"m": m, "floor": floor, "beta_star": star,
               "feasible_betas": feasible,
               "per_beta": {str(k): v for k, v in detail.items()},
               "collision": floor > 0 and (star is None or star < floor)}
        report["rows"].append(row)
        print(f"  {m:2d}      {floor:3d}                 "
              f"{'none' if star is None else star:>5}"
              f"                        "
              f"{'YES' if row['collision'] else 'no'}", flush=True)
    with open(f"results_collision8_N{size}.json", "w") as handle:
        json.dump(report, handle, indent=1, default=str)
    print(f"wrote results_collision8_N{size}.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
