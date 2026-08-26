#!/usr/bin/env python3
"""UNAUDITED PROBE W17 -- T1d: SOURCE-LEVEL refutation of the rank-one
re-basing at h = 2.

The induction step needs ONE pair of the source to carry an admissible
clean cap.  The re-basing replaces "cap" by "rank-one cap".  A source-level
counterexample is a source with

    some pair carrying an admissible clean cap  (so the descent applies)
    AND no pair carrying an admissible clean RANK-ONE cap  (so the re-based
        induction stalls).

Five such six-site sources were found in P2's fleet (T1).  Here each is
re-decided at ALL 15 pairs, with:
  * the rank-one decision over Q and modulo two primes, and by the
    structural branch decomposition of Theorem W17.1;
  * an independent general-cap witness decision (own quadric code path);
  * the pair blocks recorded for reproduction.
"""

from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
P2DIR = os.path.abspath(os.path.join(HERE, "..",
                                     "unaudited-witness-splitting-p2-2026-08-15"))
sys.path.insert(0, P2DIR)

import w17_h2 as H2
from run_t1b_losses import (general_witness_query, parse_tagged,
                            find_rational_witness)
from w17_core import oriented, run_singular

SEEDS = [(1013, "sparse"), (1127, "sparse"), (1139, "sparse"),
         (1169, "sparse"), (1223, "sparse")]


def main():
    import random
    from run_a_dichotomy import build_source
    rng = random.Random(99)
    t0 = time.time()
    print("== W17 T1d: source-level losses (h = 2) ==")
    out = []
    for seed, mode in SEEDS:
        src = build_source(seed, mode)
        blocks = {k: [[Fraction(x) for x in row] for row in v]
                  for k, v in src.blocks.items()}
        rows = []
        for p, q in combinations(range(6), 2):
            U = tuple(a for a in range(6) if a not in (p, q))
            apq = oriented(blocks, p, q)
            live = any(apq[i][j] != 0 for i in range(3) for j in range(3))
            tag = f"S{seed}p{p}{q}"
            rk1 = H2.decide_rank_one(blocks, p, q, U, tag) if live else False
            branches = (H2.decide_branches(blocks, p, q, U, tag) if live
                        else {})
            gen = (parse_tagged(run_singular(
                general_witness_query(blocks, p, q, U, tag), timeout=300),
                "GEN", tag) if live else False)
            mods = []
            if live:
                for prime in (32003, 1000003):
                    script = H2.direct_query(blocks, p, q, U, tag).replace(
                        "ring RQ=0,", f"ring RQ={prime},")
                    mods.append(H2.parse_rk1(run_singular(script, timeout=300),
                                             tag))
            rows.append({"pair": [p, q], "live": live,
                         "general_witness": gen, "rank_one": rk1,
                         "rank_one_branchwise": any(bool(v) for v in
                                                    branches.values()),
                         "rank_one_modular": mods})
        nwit = sum(1 for r in rows if r["general_witness"])
        nrk1 = sum(1 for r in rows if r["rank_one"])
        consistent = all(
            (r["rank_one"] == r["rank_one_branchwise"]) and
            all(m == r["rank_one"] for m in r["rank_one_modular"])
            for r in rows if r["live"])
        witness_pairs = [r["pair"] for r in rows if r["general_witness"]]
        explicit = None
        for r in rows:
            if r["general_witness"]:
                p, q = r["pair"]
                U = tuple(a for a in range(6) if a not in (p, q))
                explicit = find_rational_witness(blocks, p, q, U, rng,
                                                 attempts=250)
                if explicit:
                    explicit["pair"] = [p, q]
                    break
        print(f"  seed {seed} ({mode}): general-cap witness pairs {nwit} "
              f"{witness_pairs}, rank-one witness pairs {nrk1}, "
              f"cross-checks consistent {consistent}, explicit cap "
              f"{'yes rank ' + str(explicit['rank_K']) if explicit else 'none over Q'}"
              f" [{time.time() - t0:.0f}s]")
        out.append({"seed": seed, "mode": mode, "rows": rows,
                    "general_witness_pairs": nwit,
                    "rank_one_witness_pairs": nrk1,
                    "cross_checks_consistent": consistent,
                    "explicit_witness": explicit,
                    "blocks": {f"{a},{b}": [[str(x) for x in row]
                                            for row in blocks[(a, b)]]
                               for a, b in combinations(range(6), 2)}})
    good = sum(1 for r in out if r["general_witness_pairs"] > 0
               and r["rank_one_witness_pairs"] == 0
               and r["cross_checks_consistent"])
    print(f"\n  source-level counterexamples confirmed: {good}/{len(out)}")
    with open(os.path.join(HERE, "results_t1d_source_losses.json"), "w") as fh:
        json.dump({"confirmed": good, "sources": out}, fh, indent=1,
                  default=str)
    print(f"wrote results_t1d_source_losses.json [{time.time() - t0:.0f}s]")


if __name__ == "__main__":
    main()
