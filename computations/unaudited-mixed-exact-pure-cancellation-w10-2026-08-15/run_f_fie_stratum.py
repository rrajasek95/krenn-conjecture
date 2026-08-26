#!/usr/bin/env python3
"""W10 task F -- the REOPENED question: the (FIE) stratum.

Task E showed the only template condition the W10 witnesses violate is (FIE)
(equivalently W6's input (S1)).  So the ceiling question survives exactly on
the stratum

    ADM+ := (T4) and (T5) and (T6) and (S) and (FIE).

Two things are measured here.

 F1  Is ADM+ NONEMPTY at the band supports?  (a randomised template search;
     the objective is combinatorial and every reported template is re-audited
     exactly with W10's own auditor and W8's.)  A search miss is reported as
     "not found", never as "empty".

 F2  W6/W9's Sigma_min certificates: do they lie in ADM+?  (Task E: NO, 0/9.)
     So the campaign's target number Sigma_min(m) is a minimum over a class
     STRICTLY LARGER than the templates an exact source can have -- it is an
     under-estimate of the honest target.  F1's Sigma values bound the honest
     target Sigma_min^+(m) from above.
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from itertools import combinations

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (HERE,
          os.path.join(REPO, "computations", "unaudited-template-kill-w8-2026-08-15"),
          os.path.join(REPO, "computations", "unaudited-bridge-w6-2026-08-15")):
    if p not in sys.path:
        sys.path.insert(0, p)

import w10_core as w10                                            # noqa: E402
from w10_core import COLORS                                       # noqa: E402
import w8_core as w8                                              # noqa: E402

N = 8
GEO = w8.geometry(N)
EDGES = GEO.edges
OUT = {}
log = []


def say(s="", flush=True):
    print(s, flush=flush)
    log.append(s)


def cost(masks):
    """0 iff the template is in ADM+ at its own support."""
    compat = w8.compat_matrix(GEO, masks)
    sizes = compat.sum(axis=0, dtype=np.int64)
    sing = int(((sizes == 1) & GEO.mixed).sum())
    missing_pure = sum(1 for r in GEO.constant_rows if sizes[r] == 0)
    deg = [0] * N
    slots = set()
    for n, mask in enumerate(masks):
        if not mask:
            continue
        u, v = EDGES[n]
        deg[u] += 1
        deg[v] += 1
        for (i, j) in w8.cells(mask):
            slots.add((u, i))
            slots.add((v, j))
    degbad = sum(max(0, 3 - d) for d in deg)
    slotbad = 3 * N - len(slots)
    fie = w8.fie_demands(GEO, masks)
    fiebad = sum(1 for k, v in fie.items() if not v)
    return (10 * missing_pure + 10 * fiebad + 5 * degbad + 5 * slotbad + sing,
            {"singletons": sing, "missing_pure": missing_pure,
             "fie_unserved": fiebad, "deg_bad": degbad, "slot_bad": slotbad})


def sigma(masks):
    return sum(bin(m).count("1") for m in masks)


def anneal(m, seed, steps=25000, t0=3.0):
    """SEARCH (integer objective, no floats in any verdict).  Fixed support m."""
    rng = random.Random(seed)
    live = rng.sample(range(len(EDGES)), m)
    masks = [0] * len(EDGES)
    for e in live:
        masks[e] = rng.randrange(1, 512)
    best = None
    c, _ = cost(masks)
    for step in range(steps):
        T = t0 * (1.0 - step / steps) + 0.02
        n = rng.choice(live)
        old = masks[n]
        move = rng.random()
        if move < 0.45:                        # toggle one cell
            bit = rng.randrange(9)
            new = old ^ (1 << bit)
        elif move < 0.75:                      # make the block thin at one end
            end = rng.randrange(2)
            col = rng.randrange(3)
            new = 0
            for k in range(3):
                if rng.random() < 0.75:
                    new |= 1 << ((3 * k + col) if end else (3 * col + k))
        else:                                  # random block
            new = rng.randrange(1, 512)
        if new == 0 or new == old:
            continue
        masks[n] = new
        c2, _ = cost(masks)
        # tie-break on Sigma once feasible
        key = (c, sigma(masks) if c == 0 else 0)
        key2 = (c2, sigma(masks) if c2 == 0 else 0)
        if c2 <= c or rng.random() < pow(2.718281828, -(c2 - c) / T):
            c = c2
            if c2 == 0 and (best is None or sigma(masks) < best[0]):
                best = (sigma(masks), list(masks))
        else:
            masks[n] = old
    return best, c


say("=" * 94)
say("F1  is ADM+ = (T4)+(T5)+(T6)+(S)+(FIE) nonempty on the band?  [SEARCH]")
say("=" * 94)
say(f"{'m':>3} {'best Sigma in ADM+':>19} {'Sigma_min (W6, no FIE)':>23} "
    f"{'C_best(m) (W9 Thm C2)':>22}")
SIGMA_MIN_W6 = {19: 61, 20: 64, 21: 68, 22: 70, 23: 77, 24: 82, 25: 85,
                26: 99, 27: 98}
C_BEST = {m: m + 96 - 8 * max(0, 24 - m) for m in range(19, 28)}
rows = []
t_start = time.time()
for m in (19, 21, 24, 27):
    best = None
    for seed in range(8):
        b, c = anneal(m, 1000 * m + seed, steps=int(os.environ.get("W10_STEPS", 12000)))
        if b is not None and (best is None or b[0] < best[0]):
            best = b
        if time.time() - t_start > 900:
            break
    if best is None:
        say(f"{m:>3} {'NOT FOUND':>19} {SIGMA_MIN_W6[m]:>23} {C_BEST[m]:>22}")
        rows.append({"m": m, "best_sigma": None, "found": False})
        continue
    S, masks = best
    tpl = {EDGES[n]: frozenset(w8.cells(masks[n])) for n in range(len(EDGES))}
    aud = w10.audit(tpl, N)
    a8 = w8.audit(GEO, masks)
    ok = (aud["ADMISSIBLE"] and a8["fie"] and aud["Sigma"] == S
          and aud["m"] == m)
    say(f"{m:>3} {S:>19} {SIGMA_MIN_W6[m]:>23} {C_BEST[m]:>22}"
        f"   [re-audit {'OK' if ok else 'MISMATCH'}, beta={aud['beta']}, "
        f"fibres={aud['T4_pure_fibres']}]")
    rows.append({"m": m, "best_sigma": S, "found": True,
                 "reaudit_ok": bool(ok), "beta": aud["beta"],
                 "pure_fibres": aud["T4_pure_fibres"],
                 "template": {f"{u},{v}": sorted(map(list, tpl[(u, v)]))
                              for (u, v) in EDGES if tpl[(u, v)]}})
OUT["F1"] = rows
say()
say("  A found Sigma is a SEARCH UPPER BOUND on Sigma_min^+(m) (the honest")
say("  singleton-free price on the stratum an exact source can actually")
say("  inhabit).  A NOT FOUND is a search outcome only.")
say("  Note the direction: Sigma_min^+ >= Sigma_min, so restricting to (FIE)")
say("  RAISES the H4 target -- the one correction in the plan's favour.")

with open(os.path.join(HERE, "results_f_fie_stratum.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, "log_f_fie_stratum.txt"), "w") as fh:
    fh.write("\n".join(log) + "\n")
say("F DONE")
