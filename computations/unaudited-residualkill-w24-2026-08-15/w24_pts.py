#!/usr/bin/env python3
"""W24 -- point sources: (a) load the exact clean points stored by W20/W21/A7,
(b) an INDEPENDENT exact descent onto the clean layer (own code).
UNAUDITED.  Exact only."""
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
import w24_core as C                                              # noqa: E402

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
    """[(m, tag, blocks)] -- exact clean points on disk (data, not code)."""
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
                            "seed", rec.get("order", "?"))),
                            _walk(rec["point"])))
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
        gam = C.gamma_edges(C.TEMPLATES[m])
        if sorted(b.keys()) != sorted(gam):
            continue
        res.append((m, t, b))
    return res


# ------------------------------------------------------- own exact descent
def _common_rows(bl, gam_set, gam, t, words):
    nb = sorted({s for e in gam for s in e if t in e and s != t})
    ncols = 3 * len(nb)
    rows = {0: [], 1: [], 2: []}
    for w in words:
        r = [Fraction(0)] * ncols
        for k, s in enumerate(nb):
            vs = tuple(v for v in range(8) if v != t and v != s)
            r[3 * k + w[s]] += C.haf_on(bl, gam_set, vs, w)
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


def seed_point(gam, gam_set, rng, tries=400):
    """rank-one-ish start: all cells of a block equal, one block solved."""
    for _ in range(tries):
        t = {e: Fraction(rng.randint(-9, 9) or 3, rng.randint(1, 4))
             for e in gam}
        e0 = gam[rng.randrange(len(gam))]
        a = b = Fraction(0)
        for M in C.PMS:
            if not all(e in gam_set for e in M):
                continue
            p = Fraction(1)
            has = False
            for e in M:
                if e == e0:
                    has = True
                else:
                    p *= t[e]
            if has:
                a += p
            else:
                b += p
        if a == 0:
            continue
        t[e0] = -b / a
        if all(v != 0 for v in t.values()):
            return {e: [[t[e]] * 3 for _ in range(3)] for e in gam}
    return None


def descent(m, rng, order=None, passes=4, bl=None, lo=-7, hi=7):
    T = C.TEMPLATES[m]
    gam = C.gamma_edges(T)
    gam_set = set(gam)
    clean = [w for w in C.MIXED
             if all(C.haf_on(bl or {}, gam_set, (), w) is not None
                    for _ in ())] if False else None
    # W21's clean set = words all of whose SUPPORTED matchings lie in Gamma
    sing = C.single_edges(T)
    clean = []
    for w in C.MIXED:
        ok = True
        for e, (a, b) in sing.items():
            if w[e[0]] == a and w[e[1]] == b and C.has_pm(
                    gam_set, tuple(v for v in range(8) if v not in e)):
                ok = False
                break
        if ok:
            clean.append(w)
    if bl is None:
        bl = seed_point(gam, gam_set, rng)
    if bl is None:
        return None, clean
    order = list(range(8)) if order is None else list(order)
    for _ in range(passes):
        for t in order:
            nb, ncols, rows = _common_rows(bl, gam_set, gam, t, clean)
            newv, ok = {}, True
            for c in range(3):
                Kb = C.kernel_basis(rows[c], ncols)
                if not Kb:
                    ok = False
                    break
                for _try in range(120):
                    coef = [Fraction(rng.randint(lo, hi)) for _ in Kb]
                    v = [sum(coef[i] * Kb[i][j] for i in range(len(Kb)))
                         for j in range(ncols)]
                    if all(z != 0 for z in v):
                        break
                else:
                    ok = False
                    break
                newv[c] = v
            if not ok:
                continue
            save = {e: [r[:] for r in bl[e]] for e in gam}
            _write_site(bl, t, nb, newv)
            if not all(C.phi(bl, gam_set, w) == 0 for w in clean):
                for e in gam:
                    bl[e] = save[e]
    return bl, clean


def w21_clean(m):
    T = C.TEMPLATES[m]
    gam_set = set(C.gamma_edges(T))
    sing = C.single_edges(T)
    out = []
    for w in C.MIXED:
        ok = True
        for e, (a, b) in sing.items():
            if w[e[0]] == a and w[e[1]] == b and C.has_pm(
                    gam_set, tuple(v for v in range(8) if v not in e)):
                ok = False
                break
        if ok:
            out.append(w)
    return out
