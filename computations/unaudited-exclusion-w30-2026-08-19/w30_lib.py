#!/usr/bin/env python3
"""W30 -- THE PAIRWISE VERTEX-FAILURE EXCLUSION.  UNAUDITED PROBE.

Pinned HEAD: see PINNED_HEAD.txt.  Nothing here is a proved claim of the
repository.  EXACT ARITHMETIC ONLY (Fraction / int mod p).

Re-implements W26's vertex DELIVER/FAIL predicate but EXHAUSTIVELY over the
3^7 index choices at each vertex (W26 sampled 40-60 random words, which can
only OVER-report failure -- DELIVERS is a disjunction over index choices).

THE SLICE PICTURE (W26-M / W26-M*, re-derived here from w26_disj.analyse):

  R-vertex v, p = sigma^{-1}(v), letter t at coordinate v:
        ROWS[t][q] = D_p(t) * (D_q l_{ij(q)})  +  hafL * r_{v,sigma q}(t)
     i.e.  ROWS = d u^T + hafL * M        (a rank-one update of hafL*M)
     d[t]    = A_{p,v}[x_p][t]                 (the sigma block at p)
     u[q]    = A_{q,sigma q}[x_q][y_{sigma q}] * l_{ij(q)},  q != p
     M[t][q] = A_{v,sigma q}(t, y_{sigma q})   (the R-R slice matrix at v)

  L-vertex p, letter s at coordinate p:
        ROWS[s][a] = D_p(s) * (D_a r_{sigma b,sigma c}) + hafR * l_{p,a}(s)
     d[s]    = A_{p,sigma p}[s][y_{sigma p}]
     u[a]    = A_{a,sigma a}[x_a][y_{sigma a}] * r_{sigma b, sigma c}
     M[s][a] = A_{p,a}(s, x_a)                 (the L-L slice matrix at p)

DELIVERS at an index choice  <=>  every firing row lies in span{clean rows}.
FAILS                        <=>  delivers at NO admissible index choice.
"""
from __future__ import annotations

import os
import sys
from fractions import Fraction
from itertools import combinations, product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import w26_core as C                                              # noqa: E402

VERTS = ('R4', 'R5', 'R6', 'R7', 'L0', 'L1', 'L2', 'L3')


def vkey(lab):
    return (lab[0], int(lab[1:]))


# ------------------------------------------------------------------ rings
class QF:
    """exact rationals"""
    name = "Q"
    p = 0

    @staticmethod
    def n(a):
        return Fraction(a)

    @staticmethod
    def iszero(a):
        return a == 0

    @staticmethod
    def inv(a):
        return Fraction(1) / a


class FP:
    def __init__(self, p):
        self.p = p
        self.name = "F_%d" % p

    def n(self, a):
        return int(a) % self.p

    def iszero(self, a):
        return a % self.p == 0

    def inv(self, a):
        return pow(int(a) % self.p, self.p - 2, self.p)


def rank_rows(rows, K):
    """rank of a list of vectors over ring K (Q or F_p).  Exact."""
    if not rows:
        return 0
    n = len(rows[0])
    M = [list(r) for r in rows]
    if K.p:
        M = [[x % K.p for x in r] for r in M]
    r = 0
    for c in range(n):
        sel = None
        for i in range(r, len(M)):
            if not K.iszero(M[i][c]):
                sel = i
                break
        if sel is None:
            continue
        M[r], M[sel] = M[sel], M[r]
        iv = K.inv(M[r][c])
        if K.p:
            M[r] = [(x * iv) % K.p for x in M[r]]
            for i in range(len(M)):
                if i != r and not K.iszero(M[i][c]):
                    f = M[i][c]
                    M[i] = [(a - f * b) % K.p for a, b in zip(M[i], M[r])]
        else:
            M[r] = [x * iv for x in M[r]]
            for i in range(len(M)):
                if i != r and not K.iszero(M[i][c]):
                    f = M[i][c]
                    M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
        if r == len(M):
            break
    return r


# ------------------------------------------------------- vertex geometry
_G = {}


def geom(m):
    """per-support combinatorics, cached."""
    if m in _G:
        return _G[m]
    T = C.TEMPLATES[m]
    gs = set(C.gamma_edges(T))
    sing = C.single_edges(T)
    lv = set(C.live_singles(m))
    # singles at each vertex, in W26's (edge, trigger-coord, trigger-val,
    # letter-val) form
    at = {}
    for e, (a, b) in sing.items():
        if e not in lv:
            continue
        at.setdefault(('R', e[1]), []).append((e, e[0], a, b))
        at.setdefault(('L', e[0]), []).append((e, e[1], b, a))
    _G[m] = dict(gs=gs, sing=sing, lv=lv, at=at, T=T)
    return _G[m]


def _cl(bl, gs, u, v, a, b, zero):
    e = (u, v) if u < v else (v, u)
    if e not in gs:
        return zero
    return bl[e][a][b] if u < v else bl[e][b][a]


def slice_data(m, bl, kind, v, w, K):
    """the (d, u, M, scale) slice data at vertex (kind,v) for the ambient
    word w (w[v] is IGNORED -- it is the free letter).  Returns None if the
    scale (hafL for R-vertices, hafR for L-vertices) vanishes."""
    G = geom(m)
    gs = G['gs']
    zero = K.n(0)
    x, y = list(w[:4]), list(w[4:])

    def cl(a, b, i, j):
        return _cl(bl, gs, a, b, i, j, zero)

    ll = {(a, b): cl(a, b, x[a], x[b]) for a, b in combinations(range(4), 2)}
    hafL = (ll[(0, 1)] * ll[(2, 3)] + ll[(0, 2)] * ll[(1, 3)]
            + ll[(0, 3)] * ll[(1, 2)])
    hafR = (cl(4, 5, y[0], y[1]) * cl(6, 7, y[2], y[3])
            + cl(4, 6, y[0], y[2]) * cl(5, 7, y[1], y[3])
            + cl(4, 7, y[0], y[3]) * cl(5, 6, y[1], y[2]))
    if kind == 'R':
        if K.iszero(hafL):
            return None
        p = C.SIGINV[v]
        d = [cl(p, v, x[p], t) for t in range(3)]
        uu, MM = [], [[None] * 3 for _ in range(3)]
        for jc, q in enumerate([q for q in range(4) if q != p]):
            i, j = [t for t in range(4) if t not in (p, q)]
            lij = ll[(min(i, j), max(i, j))]
            Dq = cl(q, C.SIG[q], x[q], y[C.SIG[q] - 4])
            uu.append(Dq * lij)
            u2 = C.SIG[q]
            for t in range(3):
                la = t if v < u2 else y[u2 - 4]
                lb = y[u2 - 4] if v < u2 else t
                MM[t][jc] = cl(min(v, u2), max(v, u2), la, lb)
        return d, uu, MM, hafL
    else:
        if K.iszero(hafR):
            return None
        p = v
        d = [cl(p, C.SIG[p], s, y[C.SIG[p] - 4]) for s in range(3)]
        uu, MM = [], [[None] * 3 for _ in range(3)]
        for jc, a in enumerate([a for a in range(4) if a != p]):
            b, c = [t for t in range(4) if t not in (p, a)]
            rbc = cl(C.SIG[b], C.SIG[c], y[C.SIG[b] - 4], y[C.SIG[c] - 4])
            Da = cl(a, C.SIG[a], x[a], y[C.SIG[a] - 4])
            uu.append(Da * rbc)
            for s in range(3):
                MM[s][jc] = (bl[(p, a)][s][x[a]] if p < a
                             else bl[(a, p)][x[a]][s])
        return d, uu, MM, hafR


def index_choices(m, kind, v):
    """ALL combinatorially admissible index choices at vertex (kind,v):
    partial words on the 7 coordinates != v with (fire nonempty; the clean
    completions are clean words; the firing completions carry only singles
    at v).  Returns [(w_full_with_v_set_to_0, frozenset(fire))]."""
    G = geom(m)
    sing, lv, at = G['sing'], G['lv'], G['at']
    mine = at.get((kind, v), [])
    out = []
    others = [c for c in range(8) if c != v]
    for vals in product(range(3), repeat=7):
        w = [0] * 8
        for c, a in zip(others, vals):
            w[c] = a
        fire = set()
        for (e, trig, tv, letter) in mine:
            if w[trig] == tv:
                fire.add(letter)
        if not fire:
            continue
        ok = True
        for t in range(3):
            ww = list(w)
            ww[v] = t
            if len(set(ww)) == 1:
                ok = False
                break
            act = [f for f in lv
                   if ww[f[0]] == sing[f][0] and ww[f[1]] == sing[f][1]]
            if t not in fire:
                if act:
                    ok = False
                    break
            else:
                if any((f[1] if kind == 'R' else f[0]) != v for f in act):
                    ok = False
                    break
        if not ok:
            continue
        out.append((tuple(w), frozenset(fire)))
    return out


_IDX = {}


def index_choices_cached(m, kind, v):
    k = (m, kind, v)
    if k not in _IDX:
        _IDX[k] = index_choices(m, kind, v)
    return _IDX[k]


def vertex_report(m, bl, kind, v, K=QF, want_detail=False, stop_early=True):
    """EXHAUSTIVE delivery test at one vertex."""
    idx = index_choices_cached(m, kind, v)
    n_idx = n_zero_scale = n_collapse = n_deliver = 0
    det = []
    for (w, fire) in idx:
        sd = slice_data(m, bl, kind, v, w, K)
        if sd is None:
            n_zero_scale += 1
            continue
        d, uu, MM, sc = sd
        rows = [[d[t] * uu[j] + sc * MM[t][j] for j in range(3)]
                for t in range(3)]
        clean_ts = [t for t in range(3) if t not in fire]
        cleanrows = [rows[t] for t in clean_ts]
        rc = rank_rows(cleanrows, K)
        if rc <= 1 and len(clean_ts) > 1:
            n_collapse += 1
        ok = all(rank_rows(cleanrows + [rows[t]], K) == rc for t in fire)
        n_idx += 1
        if ok:
            n_deliver += 1
            if want_detail:
                det.append((w, sorted(fire)))
            if stop_early and not want_detail:
                return dict(n_idx_total=len(idx), n_idx=n_idx,
                            n_zero_scale=n_zero_scale, n_collapse=n_collapse,
                            n_deliver=n_deliver, DELIVERS=True, detail=det)
    return dict(n_idx_total=len(idx), n_idx=n_idx, n_zero_scale=n_zero_scale,
                n_collapse=n_collapse, n_deliver=n_deliver,
                DELIVERS=n_deliver > 0, detail=det)


def full_report(m, bl, K=QF, stop_early=True):
    rec = {}
    for lab in VERTS:
        kind, v = vkey(lab)
        rec[lab] = vertex_report(m, bl, kind, v, K, stop_early=stop_early)
    rec['fails'] = [l for l in VERTS if not rec[l]['DELIVERS']]
    rec['DISJUNCTION_holds'] = len(rec['fails']) < 8
    return rec


def fails_only(m, bl, K=QF, which=None):
    """cheap: only the DELIVERS booleans for the requested vertices."""
    out = {}
    for lab in (which or VERTS):
        kind, v = vkey(lab)
        out[lab] = vertex_report(m, bl, kind, v, K)['DELIVERS']
    return out


# --------------------------------------------------------- clean-point IO
def is_clean_point(m, bl, K=QF):
    """Phi = 0 at every clean word, and every Gamma cell nonzero."""
    G = geom(m)
    gs = G['gs']
    zero = K.n(0)
    one = K.n(1)
    for w in C.clean_words(m):
        val = C.haf_on(bl, gs, tuple(range(8)), w, zero, one)
        if not K.iszero(val):
            return False
    return True


def all_cells_nonzero(m, bl, K=QF):
    G = geom(m)
    return all(not K.iszero(bl[e][i][j])
               for e in G['gs'] for i in range(3) for j in range(3))


def vanishing_stratum(m, bl, K=QF):
    """W26/W21's predicate: does some sigma cell D_p vanish identically as a
    function used?  We reuse the standard test: some block of Gamma has a
    zero cell -- recorded separately -- plus hafL/hafR identically zero."""
    G = geom(m)
    gs = G['gs']
    zero = K.n(0)
    # hafL == 0 for all x, hafR == 0 for all y
    hl = []
    for x in product(range(3), repeat=4):
        ll = {(a, b): _cl(bl, gs, a, b, x[a], x[b], zero)
              for a, b in combinations(range(4), 2)}
        hl.append(ll[(0, 1)] * ll[(2, 3)] + ll[(0, 2)] * ll[(1, 3)]
                  + ll[(0, 3)] * ll[(1, 2)])
    hr = []
    for y in product(range(3), repeat=4):
        def r(a, b):
            return _cl(bl, gs, a, b, y[a - 4], y[b - 4], zero)
        hr.append(r(4, 5) * r(6, 7) + r(4, 6) * r(5, 7) + r(4, 7) * r(5, 6))
    return dict(hafL_all_zero=all(K.iszero(z) for z in hl),
                hafR_all_zero=all(K.iszero(z) for z in hr),
                n_hafL_zero=sum(1 for z in hl if K.iszero(z)),
                n_hafR_zero=sum(1 for z in hr if K.iszero(z)))
