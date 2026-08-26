#!/usr/bin/env python3
"""UNAUDITED PROBE (W6) -- the decisive test: is the J.1d floor beta = 3N - m
already incompatible with zero mixed singletons?

Pinned HEAD: 31cefe2b247450d1168abc07f6dc73318c068e44

For each support m we only need to know whether a zero-singleton template
EXISTS with beta = floor(3N - m) single-cell blocks (more single cells only
makes singletons more likely, so beta = floor is the easiest case for the
adversary).  A hit is a certificate that J.1d + O2 alone do NOT close that
support; a miss is evidence for the collision.

Searches BOTH families: arbitrary cell sets (w6_task2_ceiling) warm-started
from "non-single blocks full" (w6_task2_collision8).

Run: python3 w6_task2_focus.py [--size 8] [--budget SECONDS]
"""
from __future__ import annotations
import json, random, sys
from w6_task2_collision8 import geometry
import w6_task2_ceiling as CEIL

def main():
    args = sys.argv[1:]
    size = int(args[args.index("--size") + 1]) if "--size" in args else 8
    budget = float(args[args.index("--budget") + 1]) if "--budget" in args else 40.0
    geo = geometry(size)
    rng = random.Random(20260815)
    edges = size * (size - 1) // 2
    supports = list(range(3 * size // 2, edges + 1))
    print(f"UNAUDITED PROBE (W6) -- focus test at N={size}, HEAD 31cefe2",
          flush=True)
    print("   m  floor  beta tested   best #singletons   verdict")
    rows = []
    for m in supports:
        floor = max(0, 3 * size - m)
        record = {"m": m, "floor": floor, "tests": {}}
        for beta in sorted({floor, min(m, floor + 1)}):
            warm = CEIL.full_warm(geo, rng, m, beta)
            best = CEIL.hunt(geo, rng, m, beta, budget, warm=warm)
            if best is None:
                record["tests"][str(beta)] = None
                verdict = "no valid template"
                value = None
            else:
                value = best[0]
                record["tests"][str(beta)] = {
                    "cost": value, "record": best[1],
                    "template": best[2] if value == 0 else None}
                verdict = ("CERTIFICATE: zero-singleton template exists"
                           if value == 0 else "no zero-singleton found")
            print(f"  {m:2d}   {floor:3d}      {beta:3d}       "
                  f"{'--' if value is None else value:>10}     {verdict}",
                  flush=True)
        rows.append(record)
    with open(f"results_focus_N{size}.json", "w") as handle:
        json.dump({"N": size, "budget": budget, "rows": rows}, handle,
                  indent=1, default=str)
    print(f"wrote results_focus_N{size}.json")

if __name__ == "__main__":
    main()
