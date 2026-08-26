#!/usr/bin/env python3
"""UNAUDITED PROBE W17 -- T2(b): rank-one losslessness on W1's NEAR-EXACT
six-site stall points (the exactness end of the axis, h = 2).

W1's push is deterministic given (family, seed), so its stall points are
rebuilt here exactly and then, for every live pair:

  * P2's general-cap witness verdict (`classify_source`, Singular over Q);
  * the rank-one (scalar-slice) verdict of this probe.

Losslessness of the W14 re-basing on near-exact data is "witness => rank-one
witness".  W17's T1 already refutes it on P2's random fleet; this measures
the loss rate where it matters -- close to exactness.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import time
from collections import Counter
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
W1DIR = os.path.join(REPO, "unaudited-witness-splitting-w1-2026-08-15")
sys.path.insert(0, W1DIR)
sys.path.insert(0, os.path.join(REPO, "unaudited-witness-splitting-p2-2026-08-15"))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


W17 = load_module("w17_core", os.path.join(HERE, "w17_core.py"))
H2 = load_module("w17_h2", os.path.join(HERE, "w17_h2.py"))

from w1_core import (classify_source, exactness_metrics, push_cycle,
                     structure_metrics)
from run_w1_nearexact import build
FAMILIES = ("generic", "sparse", "lowrank", "census", "anchored", "anchored6P1")


def main(per_family=6, rounds=2):
    t0 = time.time()
    stats = Counter()
    rows = []
    losses = []
    print("== W17 T2(b): rank-one losslessness on W1 near-exact stalls ==")
    for family in FAMILIES:
        for k in range(per_family):
            seed = 90000 + 137 * k + 1000 * ("generic", "sparse", "lowrank", "census", "anchored", "purematching", "anchored6P1").index(family)
            try:
                source, name = build(family, seed)
            except Exception as exc:                       # noqa: BLE001
                print(f"  build failed {family} {seed}: {exc}")
                continue
            if source is None:
                continue
            final, _keep, _trace = push_cycle(source, rounds=rounds)
            ex = exactness_metrics(final)
            frac = ex["mixed_satisfied_fraction"]
            report = classify_source(final, max_degree=4, timeout=60)
            blocks = {k2: [[Fraction(x) for x in row] for row in v]
                      for k2, v in final.blocks.items()}
            per_pair = []
            for pair, record in report.items():
                if not record["live"]:
                    continue
                p, q = pair
                U = tuple(a for a in range(6) if a not in (p, q))
                tag = f"n{seed}{p}{q}"
                rk1 = H2.decide_rank_one(blocks, p, q, U, tag, timeout=120)
                wit = record["witness"]
                key = (("W" if wit else ("U" if wit is None else "B"))
                       + ("+R1" if rk1 else "-R1"))
                stats[key] += 1
                per_pair.append({"pair": [p, q], "witness": wit,
                                 "rank_one": rk1})
                if wit is True and rk1 is False:
                    losses.append({"family": family, "seed": seed,
                                   "stratum": name, "fraction": frac,
                                   "pair": [p, q]})
            rows.append({"family": family, "seed": seed, "stratum": name,
                         "fraction": round(frac, 6),
                         "pairs": per_pair})
            print(f"  [{time.time() - t0:5.0f}s] {family:14s} seed {seed} "
                  f"frac {frac:.4f} live {len(per_pair)} "
                  f"witness {sum(1 for r in per_pair if r['witness'])} "
                  f"rank-one {sum(1 for r in per_pair if r['rank_one'])}")
    print(f"\n  totals: {dict(stats)}")
    print(f"  losses (witness but no rank-one witness): {len(losses)}")
    for row in losses[:15]:
        print("   ", row)
    with open(os.path.join(HERE, "results_t2b_w1_nearexact.json"), "w") as fh:
        json.dump({"stats": dict(stats), "losses": losses, "rows": rows}, fh,
                  indent=1, default=str)
    print(f"\nwrote results_t2b_w1_nearexact.json [{time.time() - t0:.0f}s]")


if __name__ == "__main__":
    main(per_family=int(sys.argv[1]) if len(sys.argv) > 1 else 6)
