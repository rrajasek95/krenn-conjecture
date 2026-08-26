#!/usr/bin/env python3
"""H1 / BLOCKER 1 -- upgrade the N = 10 run of the m = 3N/2 + 1 corollary
from a strided sample to an EXHAUSTIVE sweep.

UNAUDITED.  Hygiene agent H1, 2026-08-15.  Exact integer arithmetic.

Every one of the 159,232 properly 3-edge-coloured cubic charts at N = 10,
times every one of the 30 non-chart edges, times each of the 3 colour
classes it can join = 14,330,880 templates.  For each: the added edge must
not create an even cycle (a matching plus one edge is acyclic), and the
word read off the fourth matching must be mixed with fibre size exactly 1.
"""
import json, os, time
import h1_b1_fourth_matching as B1

HERE = os.path.dirname(os.path.abspath(__file__))
t0 = time.time()
r = B1.t6_floor_plus_one(10, direct_stride=200000, chart_stride=1)
r["seconds"] = round(time.time() - t0, 1)
print(json.dumps(r, indent=1, default=str))
with open(os.path.join(HERE, "results_b1_n10_exhaustive.json"), "w") as fh:
    json.dump({"agent": "H1", "blocker": "1-N10-exhaustive", "T6_N10": r},
              fh, indent=1, default=str)
print("wrote results_b1_n10_exhaustive.json")
