#!/usr/bin/env python3
"""W36 shared library.  UNAUDITED PROBE.  PINNED_HEAD in PINNED_HEAD.txt.

Nothing here is a proved claim of the repository.  EXACT ARITHMETIC ONLY.
Reads W30's engines read-only; writes only into this directory.
"""
from __future__ import annotations
import json, os, sys
from fractions import Fraction as F
from itertools import combinations, product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
W30 = os.path.join(ROOT, "unaudited-exclusion-w30-2026-08-19")
W26 = os.path.join(ROOT, "unaudited-blockers-w26-2026-08-16")
for _p in (W30, W26, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import w30_lib as L          # noqa: E402
import w26_core as C         # noqa: E402

QF, FP, rank_rows = L.QF, L.FP, L.rank_rows
VERTS = L.VERTS

HEADER = "UNAUDITED W36 (Route A residual, successor of W30)"


def K_of(fld):
    return QF if fld in ('Q', '0', 0) else FP(int(fld))


def load_point(ptj, K):
    """block dict from a JSON {'(a, b)': [[str,..],..]} record."""
    out = {}
    for k, v in ptj.items():
        e = eval(k) if isinstance(k, str) else k
        out[tuple(e)] = [[(F(z) if K.p == 0 else int(z) % K.p) for z in row]
                         for row in v]
    return out


def dump_point(bl):
    return {str(k): [[str(z) for z in row] for row in v] for k, v in bl.items()}


# ---------------------------------------------------------------- m=25 / R6
# Gamma edges at m=25:
#   L: 01 02 03 12 13 23 ; sigma: 07 14 25 (36 ABSENT) ; R: 45 47 56 67
# N(6) = {5,7}.  Phi(w | y6=t) = A67[t][y7]*B(w) + A56[y5][t]*C(w)
#   B = hafL*r45 + l03*d1*d2 ,  C = hafL*r47 + l23*d0*d1
# with l03=A03[x0][x3], l23=A23[x2][x3], d0=A07[x0][y7], d1=A14[x1][y4],
#      d2=A25[x2][y5], r45=A45[y4][y5], r47=A47[y4][y7].

E_L = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
E_SIG = [(0, 7), (1, 4), (2, 5)]
E_R = [(4, 5), (4, 7), (5, 6), (6, 7)]
E_ALL25 = E_L + E_SIG + E_R


def hafL(bl, x):
    return (bl[(0, 1)][x[0]][x[1]] * bl[(2, 3)][x[2]][x[3]]
            + bl[(0, 2)][x[0]][x[2]] * bl[(1, 3)][x[1]][x[3]]
            + bl[(0, 3)][x[0]][x[3]] * bl[(1, 2)][x[1]][x[2]])


def BC(bl, w):
    """the pair Q = (B, C) at word w = (x0,x1,x2,x3,y4,y5,y6,y7)."""
    x, y = w[:4], w[4:]
    hl = hafL(bl, x)
    B = hl * bl[(4, 5)][y[0]][y[1]] + bl[(0, 3)][x[0]][x[3]] \
        * bl[(1, 4)][x[1]][y[0]] * bl[(2, 5)][x[2]][y[1]]
    Cc = hl * bl[(4, 7)][y[0]][y[3]] + bl[(2, 3)][x[2]][x[3]] \
        * bl[(0, 7)][x[0]][y[3]] * bl[(1, 4)][x[1]][y[0]]
    return B, Cc


_UNT = None


def untriggered25():
    """the 376 index patterns at v=6 whose three completions are all clean.
    w[6] is a placeholder 0 (B and C do not depend on y6)."""
    global _UNT
    if _UNT is not None:
        return _UNT
    G = L.geom(25)
    sing, lv = G['sing'], G['lv']
    out = []
    others = [c for c in range(8) if c != 6]
    for vals in product(range(3), repeat=7):
        w = [0] * 8
        for c, a in zip(others, vals):
            w[c] = a
        ok = True
        for t in range(3):
            ww = list(w)
            ww[6] = t
            if len(set(ww)) == 1 or any(ww[f[0]] == sing[f][0]
                                        and ww[f[1]] == sing[f][1]
                                        for f in lv):
                ok = False
                break
        if ok:
            out.append(tuple(w))
    _UNT = out
    return out


def classes25():
    """untriggered words grouped by (y5, y7) -- the data S'(y5,y7) sees."""
    by = {}
    for w in untriggered25():
        by.setdefault((w[5], w[7]), []).append(w)
    return by


def admissible_y5y7(m=25, lab='R6'):
    """(y5,y7) values carried by admissible |T_f| index choices at R6."""
    kind, v = L.vkey(lab)
    out = {}
    for (w, fire) in L.index_choices_cached(m, kind, v):
        out.setdefault((w[5], w[7]), []).append((w, fire))
    return out


def Sprime(bl, y5, y7):
    """the 3x2 slice S'(y5,y7):  rows t -> (A67[t][y7], A56[y5][t])."""
    return [[bl[(6, 7)][t][y7], bl[(5, 6)][y5][t]] for t in range(3)]


def qzero_profile(bl, K):
    """per-(y5,y7) count of untriggered words with Q = (B,C) = 0, plus the
    rank of S' there.  The EXACT (beta) object."""
    prof = {}
    for k, ws in sorted(classes25().items()):
        nz = 0
        for w in ws:
            B, Cc = BC(bl, w)
            if K.iszero(B) and K.iszero(Cc):
                nz += 1
        prof[k] = dict(n=len(ws), n_Qzero=nz, all_zero=(nz == len(ws)),
                       rank_Sp=rank_rows(Sprime(bl, k[0], k[1]), K))
    return prof


def beta_escape_score(bl, K):
    """max over classes of (#untriggered words with Q=0) / class size.
    == 1.0 in some class  <=>  the (beta) hypothesis fails at that class."""
    best = 0.0
    bestk = None
    for k, ws in classes25().items():
        nz = sum(1 for w in ws if all(K.iszero(z) for z in BC(bl, w)))
        r = nz / len(ws)
        if r > best:
            best, bestk = r, k
    return best, bestk


def offstratum(bl, K):
    """Phi != 0 at some word (W30's cheap test uses a constant word)."""
    G = L.geom(25)
    gs = G['gs']
    zero, one = K.n(0), K.n(1)
    for w in [(0,) * 8, (1,) * 8, (2,) * 8, (0, 1, 2, 0, 1, 2, 0, 1)]:
        if not K.iszero(C.haf_on(bl, gs, tuple(range(8)), w, zero, one)):
            return True
    return False


def clean_ok(bl, K):
    return L.is_clean_point(25, bl, K)


def allnz(bl, K):
    return all(not K.iszero(bl[e][i][j]) for e in bl
               for i in range(3) for j in range(3))


# ------------------------------------------------------------ ledger 31
# A11 found five inherited W30 files carrying ok=True with _controls_run
# empty -- controls DECLARED but never EXECUTED.  Every W36 engine must
# obtain its ok fields from a function that actually recomputes something
# on the STORED objects, never by fiat.  This is that function.
def executed_point_controls(OUT, K, recs_keys=("best", "hits"), m=25):
    """re-verify (H1) clean, (H2) all cells nonzero, (H3) off stratum FROM
    SCRATCH on every point the run actually stored, and return the control
    dicts.  Returns (controls, n_points_checked)."""
    pts = []
    for k in recs_keys:
        v = OUT.get(k)
        if isinstance(v, dict) and isinstance(v.get("point"), dict):
            pts.append((k, v["point"]))
        elif isinstance(v, list):
            for i, r in enumerate(v):
                if isinstance(r, dict) and isinstance(r.get("point"), dict):
                    pts.append(("%s[%d]" % (k, i), r["point"]))
    out = []
    for (tag, ptj) in pts:
        try:
            bl = load_point(ptj, K)
        except Exception as e:
            out.append(dict(tag=tag, error=str(e)))
            continue
        out.append(dict(tag=tag, clean=clean_ok(bl, K), allnz=allnz(bl, K),
                        offstratum=offstratum(bl, K)))
    def _all(f):
        return bool(out) and all(r.get(f) is True for r in out)
    ctl = {
        "A1_clean": dict(executed=True, n_points=len(out), ok=_all("clean"),
                         per_point=[r.get("clean") for r in out],
                         note="recomputed on every STORED point, not asserted"),
        "A2_offstratum": dict(executed=True, n_points=len(out),
                              ok=_all("offstratum"),
                              per_point=[r.get("offstratum") for r in out]),
        "A3_allnz": dict(executed=True, n_points=len(out), ok=_all("allnz"),
                         per_point=[r.get("allnz") for r in out]),
    }
    if not out:
        for k in ctl:
            ctl[k].update(ok=None, note="NO POINT STORED -- control vacuous, "
                                        "reported as None not True")
    return ctl, len(out)
