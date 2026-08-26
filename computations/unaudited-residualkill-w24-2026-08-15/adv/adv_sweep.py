#!/usr/bin/env python3
"""ADVERSARIAL W24 -- route 1: mass descent sweep at m=25..28, many seeds and
random site orders, classifying EVERY landed point by regime and by how many
of the 12 cells survive unforced.  EXACT (Fraction) only.

Goal: find a clean point whose residual linear system is CONSISTENT and
leaves all twelve z_e free/nonzero.  Records near-misses.
UNAUDITED probe output; nothing here is a repository claim.
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from fractions import Fraction

sys.dont_write_bytecode = True
W24 = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-residualkill-w24-2026-08-15"
sys.path.insert(0, W24)
HERE = os.path.dirname(os.path.abspath(__file__))
import w24_core as C                                              # noqa: E402
import w24_pts as P                                               # noqa: E402
import w24_resid as RS                                            # noqa: E402


def classify(m, bl):
    """full adversarial verdict at a point."""
    T = C.TEMPLATES[m]
    gam = C.gamma_edges(T)
    gam_set = set(gam)
    nz = all(bl[e][i][j] != 0 for e in gam for i in range(3) for j in range(3))
    clean = P.w21_clean(m)
    cv = sum(1 for w in clean if C.phi(bl, gam_set, w) != 0)
    nphi = sum(1 for w in C.WORDS if C.phi(bl, gam_set, w) != 0)
    d = RS.verdict(m, bl, want_detail=True)
    d["all_cells_nonzero"] = nz
    d["clean_violations"] = cv
    d["n_words_phi_nonzero"] = nphi
    d["regime"] = "A" if nphi == 0 else "B"
    d["survivor"] = bool(nz and cv == 0 and not d["inconsistent"]
                         and not d["forced_zero"])
    return d


def main():
    t0 = time.time()
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 900.0
    out = {"_header": "ADVERSARIAL sweep, UNAUDITED, exact only",
           "runs": []}
    stats = {}
    survivors = []
    best = {}
    seed = 0
    while time.time() - t0 < budget:
        seed += 1
        for m in (25, 26, 27, 28):
            if time.time() - t0 > budget:
                break
            rng = random.Random(1000 * m + seed)
            order = list(range(8))
            rng.shuffle(order)
            lo, hi = rng.choice([(-7, 7), (-3, 3), (-1, 1), (-15, 15)])
            try:
                bl, clean = P.descent(m, rng, order=order,
                                      passes=rng.choice([2, 3, 4]),
                                      lo=lo, hi=hi)
            except Exception as ex:                       # pragma: no cover
                continue
            if bl is None:
                continue
            gam = C.gamma_edges(C.TEMPLATES[m])
            gs = set(gam)
            if not all(bl[e][i][j] != 0 for e in gam
                       for i in range(3) for j in range(3)):
                stats.setdefault(m, {}).setdefault("zero_cell", 0)
                stats[m]["zero_cell"] += 1
                continue
            if any(C.phi(bl, gs, w) != 0 for w in clean):
                stats.setdefault(m, {}).setdefault("not_clean", 0)
                stats[m]["not_clean"] += 1
                continue
            d = classify(m, bl)
            k = stats.setdefault(m, {})
            k.setdefault("regime" + d["regime"], 0)
            k["regime" + d["regime"]] += 1
            nfree = 12 - len(d["forced_zero"])
            rec = dict(m=m, seed=seed, order=order, lo=lo, hi=hi,
                       regime=d["regime"], inconsistent=d["inconsistent"],
                       n_forced=len(d["forced_zero"]), rank=d["rank"],
                       nphi=d["n_words_phi_nonzero"],
                       n_pure=d["n_pure_monomial"], survivor=d["survivor"])
            out["runs"].append(rec)
            key = (m, d["inconsistent"])
            score = (0 if d["inconsistent"] else nfree)
            if key not in best or score > best[key][0]:
                best[key] = (score, rec,
                             {str(e): [[str(x) for x in r] for r in bl[e]]
                              for e in gam})
            if d["survivor"]:
                survivors.append((m, seed,
                                  {str(e): [[str(x) for x in r] for r in bl[e]]
                                   for e in gam}, d))
                print("*** SURVIVOR *** m=%d seed=%d" % (m, seed), flush=True)
            print("m=%d s=%-4d reg=%s incons=%-5s forced=%2d nphi=%4d "
                  "pure=%4d" % (m, seed, d["regime"], d["inconsistent"],
                                len(d["forced_zero"]),
                                d["n_words_phi_nonzero"],
                                d["n_pure_monomial"]), flush=True)
    out["stats"] = {str(k): v for k, v in stats.items()}
    out["n_survivors"] = len(survivors)
    out["survivors"] = survivors
    out["best"] = {str(k): (v[0], v[1]) for k, v in best.items()}
    json.dump(out, open(os.path.join(HERE, "results_sweep.json"), "w"),
              indent=1, default=str)
    print("STATS", out["stats"], flush=True)
    print("SURVIVORS", len(survivors), flush=True)


if __name__ == "__main__":
    main()
