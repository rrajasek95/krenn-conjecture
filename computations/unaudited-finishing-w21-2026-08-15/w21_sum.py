#!/usr/bin/env python3
"""W21 MOVE 1 -- THE FAR-IMAGE SUM CRITERION.  UNAUDITED.  Exact only.

COROLLARY W21-D (proved here from the chain identity W21-C).
Fix a clean point with all Gamma cells nonzero, a site t, and a clean word w
whose three t-recolourings are clean.  Let p = w|_{N(t)}.  For each FAR site
u of t let q_u = w|_{N(u)} and

    Im_u(w) = H^{t,u}(w) . { column span of B^u(q_u)^T }   (a subspace of
                                                            C^{N(t)})

(the chain identity says Im_u(w) is spanned by the three vectors
zeta^t(w with the colour at u set to c), c = 0,1,2, all of which lie in
U^t(p) because u is not a neighbour of t).  Hence

        dim U^t(p)  >=  dim ( sum over far u of Im_u(w) )     (SUM)

and, because U^t(p) is orthogonal to the three NONZERO rows of B^t(p),
dim U^t(p) <= deg(t) - rank B^t(p).  Therefore

   *** dim sum_u Im_u(w) = deg t - 1   =>   rank B^t(p) = 1,
       i.e. the deg t columns a^t_{s,p_s} are pairwise proportional. ***

So NON-FACTORING at t forces, at every bad pattern, the far images to pile
up into a subspace of dimension <= deg t - 2.  This module measures
dim U^t(p), the individual dim Im_u, and dim sum_u Im_u at exact clean
points, and checks the corollary and the tightness of (SUM).
"""
from __future__ import annotations

import json
import os
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w21_core as K                                            # noqa: E402
import w21_site as SI                                           # noqa: E402
from w21_chain import far_sites, zeta, Hmat, avec, matvec       # noqa: E402
from w21_pf import load_w20_points                              # noqa: E402


def analyse_point(bl, gam, clean, tag, maxpat=None):
    out = {}
    for t in range(8):
        nb = K.neighbours(gam, t)
        deg = len(nb)
        cw = SI.common_words(clean, t)
        cwset = set(cw)
        # one base word per pattern (the first), plus the true U(p)
        bypat = {}
        for w in cw:
            bypat.setdefault(tuple(w[s] for s in nb), []).append(w)
        far = far_sites(gam, t)
        rows = []
        for p, ws in sorted(bypat.items()):
            Up = [zeta(bl, gam, t, w) for w in ws]
            dimU = K.rank_of(Up, deg)
            rkB = K.rank_of(K.site_matrix(bl, gam, t, p), deg)
            # far images -- ONLY at recolourings that are themselves COMMON
            # words at t (otherwise the image vectors need NOT lie in U^t(p)).
            # Choose the base word maximising the number of admissible
            # far-recolourings.
            best = None
            for w in ws:
                adm = {u: [c for c in range(3)
                           if tuple(c if i == u else w[i] for i in range(8))
                           in cwset] for u in far}
                score = sum(len(v) for v in adm.values())
                if best is None or score > best[0]:
                    best = (score, w, adm)
            _, base, adm = best
            ims, allv = {}, []
            for u in far:
                H = Hmat(bl, gam, t, u, base)
                vs = [matvec(H, avec(bl, gam, u, base, c)) for c in adm[u]]
                ims[u] = K.rank_of(vs, deg) if vs else 0
                allv += vs
            dsum = K.rank_of(allv, deg) if allv else 0
            rows.append(dict(p=list(p), n_words=len(ws), dimU=dimU,
                             rankB=rkB, dim_far_sum=dsum,
                             n_admissible=[len(adm[u]) for u in far],
                             dim_far=[ims[u] for u in far],
                             corollary_ok=(dsum <= dimU),
                             sum_tight=(dsum == dimU)))
        out[t] = dict(deg=deg, factors=K.factors_at(bl, gam, t),
                      n_patterns=len(rows),
                      n_regular=sum(1 for r in rows if r["dimU"] == deg - 1),
                      maxrankB=max(r["rankB"] for r in rows),
                      rankB_hist={str(v): sum(1 for r in rows
                                              if r["rankB"] == v)
                                  for v in sorted({r["rankB"] for r in rows})},
                      dimU_hist={str(v): sum(1 for r in rows
                                             if r["dimU"] == v)
                                 for v in sorted({r["dimU"] for r in rows})},
                      far_sum_hist={str(v): sum(1 for r in rows
                                                if r["dim_far_sum"] == v)
                                    for v in sorted({r["dim_far_sum"]
                                                     for r in rows})},
                      n_sum_tight=sum(1 for r in rows if r["sum_tight"]),
                      corollary_violations=sum(1 for r in rows
                                               if not r["corollary_ok"]),
                      adm_hist={str(v): sum(1 for r in rows
                                            if sum(r["n_admissible"]) == v)
                                for v in sorted({sum(r["n_admissible"])
                                                 for r in rows})},
                      patterns=rows[:maxpat] if maxpat else rows)
    return out


def main():
    res = {"_header": "UNAUDITED W21 far-image sum criterion (move 1). "
                      "Exact only."}
    pts = load_w20_points()
    extra = {}
    p2 = os.path.join(HERE, "results_break.json")
    if os.path.exists(p2):
        d = json.load(open(p2))
        for m in (26, 27, 28):
            for rec in d.get("m%d" % m, []):
                if "point" in rec:
                    bl = {}
                    for k, v in rec["point"].items():
                        e = tuple(int(x) for x in k.strip("()").split(","))
                        bl[e] = [[Fraction(x) for x in row] for row in v]
                    extra.setdefault(m, []).append(
                        ("break seed %d (fac %s)" % (rec["seed"],
                                                     rec["factoring"]), bl))
    for m in (26, 27, 28):
        T = K.W8_IMMUNE[m]
        gam = K.gamma_edges(T)
        clean = K.clean_words(T)
        entry = []
        todo = [pts[m][0]] + extra.get(m, [])
        for tag, bl in todo:
            assert all(K.phi_value(bl, gam, w) == 0 for w in clean)
            a = analyse_point(bl, gam, clean, tag, maxpat=0)
            entry.append(dict(tag=tag, sites=a))
            print("=== m=%d  %s" % (m, tag), flush=True)
            for t in range(8):
                d = a[t]
                print("  site %d deg=%d fac=%-5s maxrankB=%d rankB %s | dimU "
                      "%s | far-sum %s | tight %d/%d | corollary viol %d (admissible far-recolour hist %s)"
                      % (t, d["deg"], d["factors"], d["maxrankB"],
                         d["rankB_hist"], d["dimU_hist"], d["far_sum_hist"],
                         d["n_sum_tight"], d["n_patterns"],
                         d["corollary_violations"], d["adm_hist"]),
                      flush=True)
        res["m%d" % m] = entry
    json.dump(res, open(os.path.join(HERE, "results_sum.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
