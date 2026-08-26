#!/usr/bin/env python3
"""W30 POINT FACTORY.  UNAUDITED.  Exact only.

Generates exact clean points (all Gamma cells nonzero) and WRITES THEM TO
DISK so that no later stage has to re-run the slow descent.  Detached,
checkpointed after every point: safe against machine sleep.

usage:  w30_factory.py <m> <tag> <nwanted> <seed0> [mode]
mode: 'wide'   (W26's rank-one seeded descent, w26_wide.make)
      'rand'   (w26_fast.make_point: random blocks + site descent)
"""
from __future__ import annotations

import json
import os
import random
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import w26_core as C                                              # noqa: E402
import w26_fast as FA                                             # noqa: E402
import w26_wide as W                                              # noqa: E402


def enc(bl):
    return {str(k): [[str(z) for z in row] for row in v]
            for k, v in bl.items()}


def main():
    m = int(sys.argv[1])
    tag = sys.argv[2]
    nwant = int(sys.argv[3])
    seed0 = int(sys.argv[4])
    mode = sys.argv[5] if len(sys.argv) > 5 else 'wide'
    res = os.path.join(HERE, "points_m%d_%s.json" % (m, tag))
    out = {"_header": "UNAUDITED W30 exact clean points", "m": m,
           "mode": mode, "seed0": seed0, "points": []}
    mdl = FA.Model(m)
    t0 = time.time()
    tried = 0
    for kk in range(200000):
        tried += 1
        rng = random.Random(seed0 + kk)
        order = list(range(8))
        rng.shuffle(order)
        try:
            if mode == 'wide':
                bl = W.make(mdl, rng, passes=4, order=order)
            else:
                bl = FA.make_point(mdl, rng, passes=5, order=order)
        except Exception:                                    # noqa: BLE001
            continue
        if bl is None:
            continue
        van = mdl.vanishing(bl)
        out["points"].append(dict(seed=seed0 + kk, van=van, point=enc(bl)))
        out["tried"] = tried
        json.dump(out, open(res, "w"), indent=1)
        print("[%3d/%3d] seed=%d van=%s tried=%d (%.0fs)"
              % (len(out["points"]), nwant, seed0 + kk, van, tried,
                 time.time() - t0), flush=True)
        if len(out["points"]) >= nwant:
            break
    out["done"] = True
    json.dump(out, open(res, "w"), indent=1)
    print("FACTORY DONE m=%d %s: %d points, %d tries, %.0fs"
          % (m, tag, len(out["points"]), tried, time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
