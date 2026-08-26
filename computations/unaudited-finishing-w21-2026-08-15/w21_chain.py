#!/usr/bin/env python3
"""W21 MOVE 1 -- THE CHAIN IDENTITY AND THE CROSS-SITE RANK INEQUALITY.
UNAUDITED.  Exact rational arithmetic only.

THEOREM W21-C (proved here; verified exactly below).
Let t be a site and u a FAR site (u != t, u not in N_Gamma(t)).  Let w be a
word and w^(c) the word w with the colour at u changed to c.  Write
  zeta^t(w)_s = haf(Gamma - t - s)(w)          (s in N(t))   [the W20-L
                                                coefficients]
  H^{t,u}(w)_{s,v} = haf(Gamma - t - s - u - v)(w)  if v not in {t, s}
                   = 0                              otherwise
                     (rows s in N(t), columns v in N(u))
  a_c(v) = A_{uv}[c][w_v]        (v in N(u))     [ = row c of B^u(q) ]
Then, IDENTICALLY (no clean hypothesis needed),
        zeta^t(w^(c)) = H^{t,u}(w) . a_c                       (CHAIN)
because expanding haf(Gamma-t-s) at the site u is exactly the site-linear
expansion and u is a vertex of Gamma-t-s (u != t and u != s, the latter
because s in N(t) while u is not).

CONSEQUENCE.  All three w^(c) share the neighbour pattern p = w|_{N(t)}
(since u is not a neighbour of t), so U^t(p) contains H.a_0, H.a_1, H.a_2,
hence
        dim U^t(p)  >=  rank( H . B^u(q)^T )
                    >=  rank H + rank B^u(q) - deg(u)      (Sylvester)
and since rank B^t(p) <= deg(t) - dim U^t(p)  (W20-R),

   *** rank B^t(p) + rank B^u(q) <= deg t + deg u - rank H^{t,u}(w) ***

At m = 28 all degrees are 4, so rank H = 4 gives
   rank B^t(p) + rank B^u(q) <= 4 for every far pair and every word.
In particular rank B^t(p) = 3 forces the far site u to have rank B^u(q) = 1,
i.e. the four columns a_{v,q_v} at u are pairwise PROPORTIONAL.

Reminder of the dictionary: rank B^t(p) = 1 for every pattern p  <=>  site t
FACTORS;  rank V^t := max_p rank B^t(p) in {1,2,3}.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w21_core as K                                            # noqa: E402
import w21_site as SI                                           # noqa: E402
from w21_pf import load_w20_points                              # noqa: E402


def far_sites(gam, t):
    nb = set(K.neighbours(gam, t))
    return [u for u in range(8) if u != t and u not in nb]


def zeta(blocks, gam, t, w):
    ES = set(gam)
    return [K.haf_verts(blocks, ES, [v for v in range(8) if v != t and v != s],
                        w) for s in K.neighbours(gam, t)]


def Hmat(blocks, gam, t, u, w):
    ES = set(gam)
    nt, nu = K.neighbours(gam, t), K.neighbours(gam, u)
    H = []
    for s in nt:
        row = []
        for v in nu:
            if v == t or v == s:
                row.append(Fraction(0))
            else:
                vs = [z for z in range(8) if z not in (t, s, u, v)]
                row.append(K.haf_verts(blocks, ES, vs, w))
        H.append(row)
    return H


def avec(blocks, gam, u, w, c):
    out = []
    for v in K.neighbours(gam, u):
        e = (min(u, v), max(u, v))
        out.append(blocks[e][c][w[v]] if e[0] == u else blocks[e][w[v]][c])
    return out


def matvec(H, a):
    return [sum(H[i][j] * a[j] for j in range(len(a))) for i in range(len(H))]


def main():
    res = {"_header": "UNAUDITED W21 chain identity + cross-site rank "
                      "inequality (move 1). Exact only."}
    pts = load_w20_points()
    rng = random.Random(7)
    for m in (26, 27, 28):
        T = K.W8_IMMUNE[m]
        gam = K.gamma_edges(T)
        clean = set(K.clean_words(T))
        entry = {}

        # (1) CHAIN IDENTITY -- holds identically, so test at RANDOM points
        #     (this is a polynomial identity, not a variety statement).
        bad = 0
        tested = 0
        for _ in range(3):
            bl = {e: [[Fraction(rng.randint(-9, 9) or 5, rng.randint(1, 4))
                       for _ in range(3)] for _ in range(3)] for e in gam}
            for t in range(8):
                for u in far_sites(gam, t):
                    for _k in range(4):
                        w = tuple(rng.randrange(3) for _ in range(8))
                        H = Hmat(bl, gam, t, u, w)
                        for c in range(3):
                            wc = tuple(c if i == u else w[i] for i in range(8))
                            lhs = zeta(bl, gam, t, wc)
                            rhs = matvec(H, avec(bl, gam, u, w, c))
                            tested += 1
                            if lhs != rhs:
                                bad += 1
        entry["chain_identity_mismatches"] = bad
        entry["chain_identity_tested"] = tested
        print("m=%d  CHAIN identity: %d mismatches / %d exact tests"
              % (m, bad, tested))

        # MUTATION CONTROL for the chain checker: corrupt one H entry
        H = Hmat(bl, gam, 0, far_sites(gam, 0)[0], (0,) * 8)
        H[0][0] = H[0][0] + 1
        w0 = (0,) * 8
        u0 = far_sites(gam, 0)[0]
        mut = sum(1 for c in range(3)
                  if zeta(bl, gam, 0, tuple(c if i == u0 else w0[i]
                                            for i in range(8)))
                  != matvec(H, avec(bl, gam, u0, w0, c)))
        entry["chain_mutation_control_firings"] = mut
        print("     MUTATION control (corrupt one H entry): %d/3 firings" % mut)

        # (2) at the exact clean points: ranks, the inequality, rank H
        pt = []
        for tag, bl in pts[m]:
            assert all(K.phi_value(bl, gam, w) == 0 for w in clean)
            cw = {t: SI.common_words(sorted(clean), t) for t in range(8)}
            # rank V^t and the pattern rank profile
            prof = {}
            for t in range(8):
                nb = K.neighbours(gam, t)
                rk = {}
                for w in cw[t]:
                    p = tuple(w[s] for s in nb)
                    if p not in rk:
                        rk[p] = K.rank_of(K.site_matrix(bl, gam, t, p), len(nb))
                _, cols = K.site_columns(bl, gam, t)
                V = [[cols[(s, d)][c] for s in nb for d in range(3)]
                     for c in range(3)]
                prof[t] = dict(deg=len(nb), rankV=K.rank_of(V, 3 * len(nb)),
                               maxrankB=max(rk.values()),
                               rankB_hist={str(r): sum(1 for v in rk.values()
                                                       if v == r)
                                           for r in sorted(set(rk.values()))},
                               factors=K.factors_at(bl, gam, t))
            # the inequality, over far pairs and a sample of common words
            viol = 0
            checks = 0
            rankH = {}
            for t in range(8):
                for u in far_sites(gam, t):
                    ws = [w for w in cw[t] if w in set(cw[u])]
                    for w in ws[:40]:
                        H = Hmat(bl, gam, t, u, w)
                        rh = K.rank_of(H, len(K.neighbours(gam, u)))
                        rankH[rh] = rankH.get(rh, 0) + 1
                        p = tuple(w[s] for s in K.neighbours(gam, t))
                        q = tuple(w[s] for s in K.neighbours(gam, u))
                        rb = K.rank_of(K.site_matrix(bl, gam, t, p),
                                       len(K.neighbours(gam, t)))
                        rc = K.rank_of(K.site_matrix(bl, gam, u, q),
                                       len(K.neighbours(gam, u)))
                        checks += 1
                        if rb + rc > (len(K.neighbours(gam, t))
                                      + len(K.neighbours(gam, u)) - rh):
                            viol += 1
            pt.append(dict(tag=tag, profile=prof, inequality_violations=viol,
                           inequality_checks=checks,
                           rankH_hist={str(k): v for k, v in
                                       sorted(rankH.items())}))
            print("     %s: rankV per site %s | factoring %s"
                  % (tag, [prof[t]["rankV"] for t in range(8)],
                     [t for t in range(8) if prof[t]["factors"]]))
            print("        inequality violations %d / %d | rank H histogram %s"
                  % (viol, checks, sorted(rankH.items())))
        entry["points"] = pt
        res["m%d" % m] = entry
    json.dump(res, open(os.path.join(HERE, "results_chain.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
