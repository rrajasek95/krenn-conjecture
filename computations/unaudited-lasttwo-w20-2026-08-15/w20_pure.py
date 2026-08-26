#!/usr/bin/env python3
"""W20 -- THE SITE-LINEAR PURE-COEFFICIENT TEST (mechanism W20-Z).
UNAUDITED.  Exact rational arithmetic only.

Every perfect matching of K_8 covers a site t exactly once, so for a fixed
site t and colour c the map

    v  =  ( occupied cells of the blocks at t in "row c" )   |-->   H_w(v)

is LINEAR for every word w with w_t = c, with coefficients that involve only
the blocks AWAY from t.  Collect

    M_c   = rows of the 2186 MIXED words with w_t = c,
    a_c   = the row of the CONSTANT word c^8               (also w_t = c).

An exact source needs  M_c v = 0  and  a_c . v != 0.  Hence

    THE TEMPLATE IS DEAD as soon as   a_c  lies in the row space of  M_c,

because then a_c . v = 0 for every v killing the mixed words -- the mixed
system forces the pure coefficient to vanish (W15's mechanism, organised by
the site-linearity so that it becomes ordinary LINEAR ALGEBRA over the field
of rational functions in the remaining blocks).  Two weaker kills are tested
en route: ker M_c = 0 (all cells at t in row c forced to zero) and
rank M_c = #unknowns - 1 with the unique kernel direction having a zero
coordinate.

The coefficients depend on the OTHER blocks; the test is run at random exact
rational specialisations of them.  A hit at a random specialisation is a
generic statement (the rank conditions are Zariski-closed / open), and is
then re-checked at further independent specialisations.

CALIBRATION: the same test is run on W8's m = 24 template, which W15/A6
killed exactly by "the mixed system forces a pure coefficient to vanish".
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w20_core as C                                            # noqa: E402
from w20_forcing import rref, kernel_basis                       # noqa: E402


def site_unknowns(T, t):
    out = {c: [] for c in range(3)}
    for ei, (u, v) in enumerate(C.EDGES):
        if t != u and t != v:
            continue
        for cc in range(9):
            if not (T[ei] >> cc) & 1:
                continue
            i, j = cc // 3, cc % 3
            out[i if u == t else j].append((ei, cc))
    return out


def random_blocks(T, t, rng, lo=-9, hi=9):
    """exact rational values for every occupied cell NOT at site t."""
    vals = {}
    for ei, (u, v) in enumerate(C.EDGES):
        if t == u or t == v:
            continue
        for cc in range(9):
            if (T[ei] >> cc) & 1:
                vals[(ei, cc)] = Fraction(rng.randint(lo, hi) or 5,
                                          rng.randint(1, 4))
    return vals


def rows_for(T, t, c, vals, unk, words):
    pos = {u: k for k, u in enumerate(unk)}
    out = []
    for w in words:
        row = [Fraction(0)] * len(unk)
        nz = False
        for mi in C.support(T, w):
            key = None
            p = Fraction(1)
            for e in C.PM_E[mi]:
                cc = C.cell_index(e, w)
                if (e, cc) in pos:
                    key = (e, cc)
                else:
                    p *= vals[(e, cc)]
            if key is not None:
                row[pos[key]] += p
                nz = True
        if nz:
            out.append(row)
    return out


def test_template(T, tag, seeds=(1, 2, 3), sites=range(8)):
    res = {}
    su = site_unknowns(T, 0)
    for t in sites:
        su = site_unknowns(T, t)
        for c in range(3):
            unk = su[c]
            if not unk:
                continue
            key = "site%d_col%d" % (t, c)
            per_seed = []
            for sd in seeds:
                rng = random.Random(1000 * sd + 17 * t + c)
                vals = random_blocks(T, t, rng)
                mixed = [w for w in C.MIXED if w[t] == c]
                M = rows_for(T, t, c, vals, unk, mixed)
                a = rows_for(T, t, c, vals, unk, [(c,) * 8])
                n = len(unk)
                rM = len(rref(M, n)[0]) if M else 0
                rMa = len(rref(M + a, n)[0]) if M else (1 if a and any(a[0])
                                                       else 0)
                K = kernel_basis(M, n) if M else []
                forced_zero_coords = []
                if len(K) == 1:
                    forced_zero_coords = [i for i in range(n)
                                          if K[0][i] == 0]
                per_seed.append(dict(seed=sd, n_unknowns=n, rank_M=rM,
                                     rank_M_with_pure=rMa,
                                     pure_in_rowspace=(rM == rMa),
                                     kernel_dim=len(K),
                                     kernel_forced_zeros=len(
                                         forced_zero_coords)))
            res[key] = dict(n_unknowns=len(unk), per_seed=per_seed,
                            KILL_pure_forced=all(p["pure_in_rowspace"]
                                                 for p in per_seed),
                            KILL_kernel_zero=all(p["kernel_dim"] == 0
                                                 for p in per_seed),
                            KILL_kernel_has_zero=all(
                                p["kernel_dim"] == 1
                                and p["kernel_forced_zeros"] > 0
                                for p in per_seed))
    res["_any_kill"] = any(v["KILL_pure_forced"] or v["KILL_kernel_zero"]
                           or v["KILL_kernel_has_zero"]
                           for k, v in res.items() if k.startswith("site"))
    res["_tag"] = tag
    return res


def summarise(r, tag):
    kills = [k for k, v in r.items()
             if k.startswith("site") and (v["KILL_pure_forced"]
                                          or v["KILL_kernel_zero"]
                                          or v["KILL_kernel_has_zero"])]
    print("%s: any kill = %s; killing (site,colour) slots: %s"
          % (tag, r["_any_kill"], kills[:10]), flush=True)
    for k in sorted(x for x in r if x.startswith("site"))[:24]:
        v = r[k]
        p = v["per_seed"][0]
        print("   %-14s n=%2d rank_M=%2d rank_[M;pure]=%2d kerdim=%d "
              "pure_in_rowspace=%s" % (k, p["n_unknowns"], p["rank_M"],
                                       p["rank_M_with_pure"], p["kernel_dim"],
                                       p["pure_in_rowspace"]), flush=True)


def main():
    res = {"_header": "UNAUDITED W20 site-linear pure-coefficient test. "
                      "Exact rational arithmetic only."}
    print("=== POSITIVE CALIBRATION: W8's m=24 template (killed by W15/A6) ===",
          flush=True)
    r24 = test_template(C.W8_IMMUNE[24], "m24")
    res["m24_calibration"] = r24
    summarise(r24, "m=24")
    print("=== the C_8 member (residual 2) ===", flush=True)
    rc8 = test_template(C.C8_MEMBER, "C8")
    res["C8"] = rc8
    summarise(rc8, "C_8 member")
    for m in (25, 26, 27, 28):
        rm = test_template(C.W8_IMMUNE[m], "m%d" % m)
        res["m%d" % m] = rm
        summarise(rm, "m=%d" % m)
    json.dump(res, open(os.path.join(HERE, "results_pure.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
