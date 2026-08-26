#!/usr/bin/env python3
"""W20 -- RESIDUAL 1: the PATTERN-RANK criterion.  UNAUDITED.  Exact only.

THEOREM W20-R (proved here).  Fix a site t and a point of the effectively-
clean layer with all Gamma cells nonzero.  For a colour-pattern
p in {0,1,2}^{N_Gamma(t)} of the Gamma-neighbours of t let

    Cf(p) = { ( haf_{Gamma-t-s}(w) )_{s in N(t)}  :  w a clean word with
              w|_{N(t)} = p and (w with t recoloured) clean for all three
              colours at t }                            (vectors in C^deg t)

Every clean equation with that neighbour pattern reads
    sum_{s in N(t)} A_ts[c][p_s] * haf_{Gamma-t-s}(w) = 0,
so the vector  V_c(p) := ( A_ts[c][p_s] )_s  is orthogonal to span Cf(p),
for each of the three colours c.  Since all cells are nonzero, V_c(p) != 0,
so rank Cf(p) <= deg(t) - 1 ALWAYS (a derived determinantal condition on the
blocks away from t).  If rank Cf(p) = deg(t) - 1 then V_0(p), V_1(p), V_2(p)
are pairwise PROPORTIONAL.

COROLLARY.  Call p regular when rank Cf(p) = deg(t) - 1.  Build the graph on
regular patterns joining p, p' that differ in one coordinate.  If the regular
patterns are connected and meet every (s, d), then site t FACTORS: the
per-pattern proportionality constants chain together (the shared coordinates
force the ratios to be colour-independent), so V_0, V_1, V_2 are proportional
as full vectors in C^{3 deg t}.

This module MEASURES rank Cf(p) at exact points of the clean layer and
decides the corollary's hypothesis.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w20_core as C                                            # noqa: E402
from w20_forcing import (kernel_basis, haf_at, site_system, blocks_from_site,
                         site_vectors, factors_at, jpoint, rref)  # noqa: E402
from w20_sitesys import common_rows, descent_point               # noqa: E402


def pattern_data(blocks, gam, t, words):
    nbr = sorted(s for e in gam for s in e if t in e and s != t)
    others = [e for e in gam if t not in e]
    pats = {}
    for w in words:
        p = tuple(w[s] for s in nbr)
        row = []
        for s in nbr:
            vs = [v for v in range(8) if v != t and v != s]
            row.append(haf_at(blocks, others, vs, w))
        pats.setdefault(p, []).append(row)
    return nbr, pats


def analyse_site(blocks, gam, t, crows):
    nbr, pats = pattern_data(blocks, gam, t, crows)
    deg = len(nbr)
    ranks = {}
    for p, rows in pats.items():
        ranks[p] = len(rref(rows, deg)[0])
    reg = [p for p, r in ranks.items() if r == deg - 1]
    # connectivity of the regular patterns under single-coordinate moves
    idx = {p: i for i, p in enumerate(reg)}
    par = list(range(len(reg)))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    for p in reg:
        for k in range(deg):
            for d in range(3):
                if d == p[k]:
                    continue
                q = p[:k] + (d,) + p[k + 1:]
                if q in idx:
                    ra, rb = find(idx[p]), find(idx[q])
                    if ra != rb:
                        par[ra] = rb
    comps = len({find(i) for i in range(len(reg))}) if reg else 0
    covered = set()
    for p in reg:
        for k, s in enumerate(nbr):
            covered.add((s, p[k]))
    return dict(site=t, deg=deg, n_patterns=len(pats),
                rank_hist={str(r): sum(1 for v in ranks.values() if v == r)
                           for r in sorted(set(ranks.values()))},
                n_regular=len(reg), n_components=comps,
                covers_all_sd=(len(covered) == 3 * deg),
                corollary_applies=(comps == 1 and len(covered) == 3 * deg),
                factors=factors_at(blocks, gam, t))


def main():
    res = {"_header": "UNAUDITED W20 pattern-rank criterion (residual 1). "
                      "Exact only."}
    for m in (26, 27, 28):
        T = C.W8_IMMUNE[m]
        gam = C.gamma_edges(T)
        fullm = C.full_pm_indices(T)
        clean = [w for w in C.MIXED if not C.extras_at(T, w, fullm)]
        crows = {t: common_rows(T, fullm, t, clean) for t in range(8)}
        entry = {}
        rng = random.Random(4000 + m)
        _, jb = jpoint(gam, rng)
        entry["J_point"] = [analyse_site(jb, gam, t, crows[t])
                            for t in range(8)]
        print("m=%d  J-point pattern ranks:" % m, flush=True)
        for d in entry["J_point"]:
            print("   site %d deg=%d pats=%d ranks=%s regular=%d comps=%d "
                  "covers=%s => corollary %s (factors=%s)"
                  % (d["site"], d["deg"], d["n_patterns"], d["rank_hist"],
                     d["n_regular"], d["n_components"], d["covers_all_sd"],
                     d["corollary_applies"], d["factors"]), flush=True)
        pts = []
        for seed in (11, 23):
            T2, gam2, fullm2, clean2, blocks, tr = descent_point(m, seed)
            a = [analyse_site(blocks, gam2, t, crows[t]) for t in range(8)]
            pts.append(a)
            print("m=%d  descent seed %d pattern ranks:" % (m, seed),
                  flush=True)
            for d in a:
                print("   site %d deg=%d pats=%d ranks=%s regular=%d comps=%d "
                      "covers=%s => corollary %s (factors=%s)"
                      % (d["site"], d["deg"], d["n_patterns"], d["rank_hist"],
                         d["n_regular"], d["n_components"], d["covers_all_sd"],
                         d["corollary_applies"], d["factors"]), flush=True)
        entry["descent"] = pts
        res["m%d" % m] = entry
    json.dump(res, open(os.path.join(HERE, "results_pattern.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
