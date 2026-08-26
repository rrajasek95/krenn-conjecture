#!/usr/bin/env python3
"""W21 (RE-AIMED after audit A7) -- THE RESIDUAL LINEAR SYSTEM.
UNAUDITED.  Exact rational arithmetic only.

A7 refuted the clean-layer forcing theorem at m = 25; W21 independently
refuted it at m = 28 (two exact all-nonzero zero-factoring clean points,
reproduced by an independent search).  The corrected target consumes
equations BEYOND the clean layer.  This module implements the cheapest such
consumer and tests it:

  THE RESIDUAL LINEAR TEST.  Fix the Gamma blocks at a point of the clean
  layer.  The remaining unknowns are the cells of the NON-Gamma occupied
  blocks (at m = 25..28 these are twelve one-cell blocks, hence twelve
  scalars z_1..z_12; the C_8 stratum has fat ones too).  Every mixed word w
  then gives H_w(z) = 0, a polynomial of degree <= 4:
      degree 0  <=>  w is effectively clean  (identically satisfied here),
      degree 1  <=>  every extra supported matching of w uses exactly ONE
                     non-Gamma cell        (the "one-extra"/k=1 family),
      degree >= 2 the rest.
  The DEGREE-<=1 part is an INHOMOGENEOUS LINEAR SYSTEM in twelve unknowns.
  If it is inconsistent, the clean point admits NO completion at all --
  in particular none with the occupied cells nonzero.  This is a
  clean-layer-plus-k=1 certificate and it needs no factoring hypothesis.

Controls: w21_extctrl.py (polynomial reconstruction 0/937 mismatches vs a
from-the-definition H engine; mutation control fires; explicit-point control
shows a deliberately CONSISTENT 400x12 system is reported consistent).
LEDGER 18: the explicit points fed to this test are constructed OUTSIDE the
asserted locus -- they include the zero-factoring points, points with one,
two, three and four factoring sites, and A7's m=25 non-factoring witness.
"""
from __future__ import annotations

import glob
import json
import os
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w21_core as K                                            # noqa: E402


def setup(T):
    gam = set(K.gamma_edges(T))
    cells = []
    for ei, e in enumerate(K.EDGES):
        if T[ei] in (0, K.FULL):
            continue
        for c in range(9):
            if (T[ei] >> c) & 1:
                cells.append((e, c // 3, c % 3))
    idx = {x: i for i, x in enumerate(cells)}
    return gam, cells, idx


def poly_of(bl, gam, idx, w):
    """H_w as {sorted tuple of residual-cell ids: coefficient}."""
    out = {}
    for M in K.PMS:
        coef = Fraction(1)
        mon = []
        ok = True
        for (u, v) in M:
            if (u, v) in gam:
                coef *= bl[(u, v)][w[u]][w[v]]
            else:
                key = ((u, v), w[u], w[v])
                if key not in idx:
                    ok = False
                    break
                mon.append(idx[key])
        if not ok or coef == 0:
            continue
        k = tuple(sorted(mon))
        out[k] = out.get(k, Fraction(0)) + coef
        if out[k] == 0:
            del out[k]
    return out


def residual_linear_test(T, bl):
    gam, cells, idx = setup(T)
    n = len(cells)
    rows = []
    deg = {}
    for w in K.MIXED:
        p = poly_of(bl, gam, idx, w)
        d = max([len(k) for k in p], default=-1)
        deg[d] = deg.get(d, 0) + 1
        if d <= 1 and p:
            r = [Fraction(0)] * n
            c = Fraction(0)
            for k, v in p.items():
                if k == ():
                    c = v
                else:
                    r[k[0]] = v
            rows.append(r + [-c])
    if not rows:
        return dict(n_unknowns=n, n_linear=0, inconsistent=False,
                    degree_hist={str(k): v for k, v in sorted(deg.items())})
    R, piv = K.rref(rows, n + 1)
    incons = n in piv
    if incons:
        return dict(n_unknowns=n, n_linear=len(rows), rank=len(piv),
                   inconsistent=True, solution_dim=None,
                   forced_zero_cells=None,
                   degree_hist={str(k): v for k, v in sorted(deg.items())})
    # particular solution + kernel of the homogeneous part
    sol = [Fraction(0)] * n
    for i, pc in enumerate(piv):
        if pc < n:
            sol[pc] = R[i][n]
    ker = K.kernel_basis([r[:n] for r in rows], n)
    freedim = len(ker)
    # a coordinate is IDENTICALLY ZERO on the affine solution set iff the
    # particular solution vanishes there AND every kernel vector does too.
    forced = [i for i in range(n)
              if sol[i] == 0 and all(b[i] == 0 for b in ker)]
    return dict(n_unknowns=n, n_linear=len(rows), rank=len(piv),
                inconsistent=False, solution_dim=freedim,
                forced_zero_cells=[str(cells[i]) for i in forced],
                n_forced_zero=len(forced),
                degree_hist={str(k): v for k, v in sorted(deg.items())})


def load_blocks(obj):
    def walk(o):
        if isinstance(o, dict):
            ks = list(o.keys())
            if ks and all(isinstance(k, str) and k.startswith("(") and "," in k
                          for k in ks):
                try:
                    return {tuple(int(z) for z in k.strip("()").split(",")):
                            [[Fraction(x) for x in row] for row in v]
                            for k, v in o.items()}
                except Exception:
                    pass
            for v in o.values():
                r = walk(v)
                if r:
                    return r
        if isinstance(o, list):
            for v in o:
                r = walk(v)
                if r:
                    return r
        return None
    return walk(obj)


def collect():
    """(m, tag, blocks) for every exact clean point W21 has on disk."""
    out = []
    W20 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
           "unaudited-lasttwo-w20-2026-08-15/results_sitesys.json")
    d = json.load(open(W20))
    for m in (26, 27, 28):
        for a in d["m%d" % m]["descent_points"]:
            out.append((m, "W20 " + a["_tag"], load_blocks(a["point"])))
    for fn, lab in (("results_break.json", "W21 break"),
                    ("results_more.json", "W21 more"),
                    ("results_zero2627.json", "W21 zero-search")):
        p = os.path.join(HERE, fn)
        if not os.path.exists(p):
            continue
        d = json.load(open(p))
        for m in (26, 27, 28):
            for rec in d.get("m%d" % m, []):
                if isinstance(rec, dict) and "point" in rec:
                    out.append((m, "%s %s" % (lab, rec.get("seed", rec.get(
                        "order", "?"))), load_blocks(rec["point"])))
                for q in (rec.get("zero_factoring_points", [])
                          if isinstance(rec, dict) else []):
                    out.append((m, "%s ZERO" % lab, load_blocks(q)))
        for q in d.get("m%d" % 28, {}).get("zero_factoring_points", []) \
                if isinstance(d.get("m28"), dict) else []:
            out.append((28, "%s ZERO" % lab, load_blocks(q)))
    for p in sorted(glob.glob(os.path.join(HERE, "tensor",
                                           "results_zero*.json"))):
        out.append((28, "tensor " + os.path.basename(p),
                    load_blocks(json.load(open(p)))))
    return [(m, t, b) for m, t, b in out if b]


def main():
    res = {"_header": "UNAUDITED W21 residual linear test (clean + k<=1). "
                      "Exact only."}
    rows = []
    for m, tag, bl in collect():
        T = K.W8_IMMUNE[m]
        gam = K.gamma_edges(T)
        if sorted(bl.keys()) != sorted(gam):
            continue
        clean = K.clean_words(T)
        if any(K.phi_value(bl, gam, w) != 0 for w in clean):
            continue
        nz = all(bl[e][i][j] != 0 for e in gam
                 for i in range(3) for j in range(3))
        fac = [t for t in range(8) if K.factors_at(bl, gam, t)]
        r = residual_linear_test(T, bl)
        rows.append(dict(m=m, tag=tag, all_nonzero=nz, factoring=fac, **r))
        print("m=%d %-24s nonzero=%-5s factoring %-16s | linear eqs %4d, "
              "rank %2d, INCONSISTENT=%s | degrees %s"
              % (m, tag, nz, fac, r["n_linear"], r.get("rank", 0),
                 r["inconsistent"], r["degree_hist"]), flush=True)
    res["rows"] = rows
    res["summary"] = dict(
        n_points=len(rows),
        n_inconsistent=sum(1 for r in rows if r["inconsistent"]),
        n_consistent=sum(1 for r in rows if not r["inconsistent"]))
    print("SUMMARY: %d clean points tested, %d killed by the residual linear "
          "system, %d survive it"
          % (res["summary"]["n_points"], res["summary"]["n_inconsistent"],
             res["summary"]["n_consistent"]))
    json.dump(res, open(os.path.join(HERE, "results_resid.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
