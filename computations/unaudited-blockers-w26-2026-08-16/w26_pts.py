#!/usr/bin/env python3
"""W26 -- exact point sources.  UNAUDITED.  Exact only.

(a) stored exact clean points from W20/W21 (data on disk, not code);
(b) an INDEPENDENT exact descent onto the clean layer (site-resolve:
    at a vertex t, the clean equations are LINEAR in the 3x(3*deg) cells
    of the blocks incident to t, split by the letter w_t -- solve each
    letter-block's kernel and pick a kernel vector with all entries
    nonzero).  Different seeding from W24's (random full blocks, then a
    single-site exact repair) so the two descents are not the same map.
"""
from __future__ import annotations

import glob
import json
import os
import random
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w26_core as C                                              # noqa: E402

ROOT = "/Users/rishi/workplace/krenn-conjecture/computations"
W20 = os.path.join(ROOT, "unaudited-lasttwo-w20-2026-08-15")
W21 = os.path.join(ROOT, "unaudited-finishing-w21-2026-08-15")


def _walk(o):
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
            r = _walk(v)
            if r:
                return r
    if isinstance(o, list):
        for v in o:
            r = _walk(v)
            if r:
                return r
    return None


def stored_points():
    out = []
    d = json.load(open(os.path.join(W20, "results_sitesys.json")))
    for m in (26, 27, 28):
        for a in d["m%d" % m]["descent_points"]:
            out.append((m, "W20 " + str(a.get("_tag")), _walk(a["point"])))
    for fn, lab in (("results_break.json", "W21break"),
                    ("results_more.json", "W21more"),
                    ("results_zero2627.json", "W21zero")):
        p = os.path.join(W21, fn)
        if not os.path.exists(p):
            continue
        d = json.load(open(p))
        for m in (26, 27, 28):
            v = d.get("m%d" % m)
            if isinstance(v, list):
                for rec in v:
                    if isinstance(rec, dict) and "point" in rec:
                        out.append((m, "%s %s" % (lab, rec.get(
                            "seed", rec.get("order", "?"))), _walk(rec["point"])))
                    if isinstance(rec, dict):
                        for q in rec.get("zero_factoring_points", []):
                            out.append((m, "%s ZERO" % lab, _walk(q)))
            elif isinstance(v, dict):
                for q in v.get("zero_factoring_points", []):
                    out.append((m, "%s ZERO" % lab, _walk(q)))
    for p in sorted(glob.glob(os.path.join(W21, "tensor",
                                           "results_zero*.json"))):
        out.append((28, "tensorZERO " + os.path.basename(p),
                    _walk(json.load(open(p)))))
    res = []
    for m, t, b in out:
        if not b:
            continue
        if sorted(b.keys()) != sorted(C.gamma_edges(C.TEMPLATES[m])):
            continue
        res.append((m, t, b))
    return res


# ------------------------------------------------------------- own descent
def _site_rows(bl, gs, t, clean):
    nb = sorted({s for e in gs for s in e if t in e and s != t})
    ncols = 3 * len(nb)
    rows = {0: [], 1: [], 2: []}
    for w in clean:
        r = [Fraction(0)] * ncols
        for k, s in enumerate(nb):
            vs = tuple(v for v in range(8) if v != t and v != s)
            r[3 * k + w[s]] += C.haf_on(bl, gs, vs, w)
        if any(r):
            rows[w[t]].append(r)
    return nb, ncols, rows


def _write_site(bl, t, nb, v):
    for k, s in enumerate(nb):
        e = (min(t, s), max(t, s))
        for c in range(3):
            for d in range(3):
                if e[0] == t:
                    bl[e][c][d] = v[c][3 * k + d]
                else:
                    bl[e][d][c] = v[c][3 * k + d]


def descent(m, rng, passes=5, lo=-6, hi=6, bl=None, order=None):
    """returns (blocks, clean_words) or (None, clean)."""
    gam = C.gamma_edges(C.TEMPLATES[m])
    gs = set(gam)
    clean = C.clean_words(m)
    if bl is None:
        bl = {e: [[Fraction(rng.randint(-6, 6) or 3, rng.randint(1, 3))
                   for _ in range(3)] for _ in range(3)] for e in gam}
    order = list(range(8)) if order is None else list(order)
    for _p in range(passes):
        for t in order:
            nb, ncols, rows = _site_rows(bl, gs, t, clean)
            newv, ok = {}, True
            for c in range(3):
                Kb = C.kernel_basis(rows[c], ncols)
                if not Kb:
                    ok = False
                    break
                for _try in range(200):
                    co = [Fraction(rng.randint(lo, hi)) for _ in Kb]
                    v = [sum(co[i] * Kb[i][j] for i in range(len(Kb)))
                         for j in range(ncols)]
                    if all(zz != 0 for zz in v):
                        break
                else:
                    ok = False
                    break
                newv[c] = v
            if not ok:
                continue
            save = {e: [r[:] for r in bl[e]] for e in gam}
            _write_site(bl, t, nb, newv)
            if not all(C.phi(bl, gs, w) == 0 for w in clean):
                for e in gam:
                    bl[e] = save[e]
    return bl, clean


def is_clean_point(m, bl):
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    if not all(bl[e][i][j] != 0 for e in gs for i in range(3)
               for j in range(3)):
        return False
    return all(C.phi(bl, gs, w) == 0 for w in C.clean_words(m))


def vanishing_stratum(m, bl):
    """does haf_Gamma vanish at ALL 6561 words?"""
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    return all(C.phi(bl, gs, w) == 0 for w in C.WORDS)


def fresh_points(m, n, seed0, passes=5, tries=None):
    """n exact clean points with all Gamma cells nonzero."""
    out = []
    tries = tries or 60 * n
    for k in range(tries):
        rng = random.Random(seed0 + 1000 * m + k)
        bl, clean = descent(m, rng, passes=passes)
        if bl is None:
            continue
        if is_clean_point(m, bl):
            out.append(bl)
            if len(out) >= n:
                break
    return out
