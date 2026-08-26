#!/usr/bin/env python3
"""A10 -- INDEPENDENT ADVERSARIAL AUDIT of W30 (and of W26's predicate).

UNAUDITED AUDIT LANE.  Pinned HEAD: see PINNED_HEAD.txt.
Nothing here is a proved claim of the repository.

EXACT ARITHMETIC ONLY (int mod p, or Fraction).  No floats.

This module is written FROM SCRATCH from the model definition and from an
independent hand re-derivation of the slice relation (see NOTES below).  It
imports NOTHING from w26_*/w30_*; the only data taken from the corpus are
the nine 28-entry template masks, which were independently corroborated
against eight other lanes (w15/w16/w19/w20/w21/w24/a6/a7 cores) -- see
a10_t1_points.py:template_crosscheck().

MODEL
  N = 8, alphabet {0,1,2}, a 3x3 block A_uv per edge uv of K_8.
  H_w(A,z) = sum over the 105 perfect matchings M of K_8 of
             prod_{(u,v) in M} c_uv(w_u, w_v),
  where an edge with mask 511 ("Gamma") contributes A_uv[w_u][w_v], an edge
  with a one-bit mask ("single", cell (a,b)) contributes z_uv if
  (w_u,w_v) = (a,b) and 0 otherwise, and an absent edge contributes 0.
  Phi(w) := the z-free part of H_w  =  sum over PMs lying inside Gamma.

HAND RE-DERIVATION OF THE SLICE ROWS (A10, independent of W26-M):
  L = {0,1,2,3}, R = {4,5,6,7}, sigma = (0<->7, 1<->4, 2<->5, 3<->6).
  Gamma = K_4(L) + R-graph + the present sigma edges, so every Gamma PM uses
  k in {0,2,4} sigma edges and
      Phi = hafL*hafR + sum_{i<j in L} l_ij r_{si,sj} d_p d_q + d_0d_1d_2d_3,
  with {p,q} = L - {i,j}, d_a = A_{a,sigma a}[x_a][y_{sigma a}].
  Fix an R-vertex v, p = sigma^{-1}(v), and vary only the letter t at v:
      Phi(t) = sum_{q != p} r_{v,sigma q}(t) * B_q  +  d_p(t) * A,
      B_q = hafL*r_{sigma i,sigma j} + l_{pq} d_i d_j      ({i,j} = L-{p,q})
      A   = sum_{q != p} l_{ij} r_{sigma i,sigma j} d_q + prod_{q != p} d_q.
  Multiplying by hafL and using  hafL * prod_{q!=p} d_q
        = sum_{q!=p} l_{pq} l_{ij} d_i d_j d_q      (the 3-pairing identity)
  gives the MASTER RELATION
      hafL * Phi(t) = sum_{q != p} B_q * ROW(t)[q],
      ROW(t)[q] = d_p(t) * (d_q * l_{ij})  +  hafL * r_{v,sigma q}(t).
  Dually for an L-vertex p, letter s:
      hafR * Phi(s) = sum_{a != p} X_a * ROW(s)[a],
      X_a = hafR*l_{bc} + r_{sigma p,sigma a} d_b d_c    ({b,c} = L-{p,a})
      ROW(s)[a] = d_p(s) * (d_a * r_{sigma b,sigma c}) + hafR * l_{p,a}(s).
  Both identities are re-verified numerically by a10_check_master().

DELIVERY (the operative predicate, identical in W26 and W30):
  at an index choice (letters on the 7 coordinates != v) let T_f = letters
  at which some LIVE single into v fires, T_c = the rest.  The vertex
  DELIVERS at that index choice iff ROW(t_f) in span{ROW(t) : t in T_c} for
  every t_f in T_f; it FAILS iff it delivers at NO admissible index choice.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations, product

sys.setrecursionlimit(10000)

NV = 8
QQ = 3
FULL = 511

EDG = tuple(combinations(range(NV), 2))
LSIDE = (0, 1, 2, 3)
RSIDE = (4, 5, 6, 7)
SG = {0: 7, 1: 4, 2: 5, 3: 6}
SGI = {v: k for k, v in SG.items()}


# ------------------------------------------------------------ matchings
def _perfect_matchings(vs):
    """all perfect matchings of the complete graph on the vertex tuple vs."""
    if not vs:
        return [()]
    a = vs[0]
    out = []
    for i in range(1, len(vs)):
        b = vs[i]
        rest = vs[1:i] + vs[i + 1:]
        for mm in _perfect_matchings(rest):
            out.append(((a, b),) + mm)
    return out


PM105 = tuple(_perfect_matchings(tuple(range(NV))))
assert len(PM105) == 105, len(PM105)
assert len(set(PM105)) == 105

# the nine template masks, re-typed (cross-checked against 8 other lanes)
TMPL = {
    25: [511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511, 8, 511,
         128, 32, 64, 128, 0, 256, 511, 0, 511, 511, 0, 511],
    26: [511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511, 8, 511,
         128, 32, 64, 128, 511, 256, 511, 0, 511, 511, 0, 511],
    27: [511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511, 8, 511,
         128, 32, 64, 128, 511, 256, 511, 511, 511, 511, 0, 511],
    28: [511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511, 8, 511,
         128, 32, 64, 128, 511, 256, 511, 511, 511, 511, 511, 511],
}

WORDS = tuple(product(range(QQ), repeat=NV))
MIXED = tuple(w for w in WORDS if len(set(w)) > 1)
assert len(WORDS) == 6561 and len(MIXED) == 6558


# ------------------------------------------------------------- structure
class Struct:
    """template combinatorics, computed here from the mask list alone."""

    def __init__(self, m):
        T = TMPL[m]
        assert len(T) == len(EDG)
        self.m = m
        self.T = T
        self.gamma = tuple(e for e, t in zip(EDG, T) if t == FULL)
        self.gs = set(self.gamma)
        self.single = {}
        for e, t in zip(EDG, T):
            if t in (0, FULL):
                continue
            bits = [c for c in range(9) if (t >> c) & 1]
            assert len(bits) == 1, (e, t)
            self.single[e] = (bits[0] // 3, bits[0] % 3)
        self.absent = tuple(e for e, t in zip(EDG, T) if t == 0)
        assert len(self.gamma) + len(self.single) + len(self.absent) == 28
        # LIVE single: Gamma has a perfect matching on V minus its endpoints
        self.live = tuple(sorted(
            e for e in self.single
            if self._has_pm(tuple(v for v in range(NV) if v not in e))))
        self.livelist = [(e, self.single[e]) for e in self.live]
        # clean words: mixed, no LIVE single active
        self.clean = tuple(w for w in MIXED if not self.active_live(w))
        # PMs inside Gamma (for the raw Phi evaluation)
        self.gamma_pms = tuple(M for M in PM105
                               if all(e in self.gs for e in M))

    def _has_pm(self, vs):
        if not vs:
            return True
        a = vs[0]
        for i in range(1, len(vs)):
            b = vs[i]
            e = (a, b) if a < b else (b, a)
            if e in self.gs and self._has_pm(vs[1:i] + vs[i + 1:]):
                return True
        return False

    def active_live(self, w):
        return tuple(e for e in self.live
                     if (w[e[0]], w[e[1]]) == self.single[e])

    def active_any(self, w):
        return tuple(e for e in self.single
                     if (w[e[0]], w[e[1]]) == self.single[e])


_S = {}


def S(m):
    if m not in _S:
        _S[m] = Struct(m)
    return _S[m]


# ------------------------------------------------------------ arithmetic
class Fp:
    def __init__(self, p):
        self.p = p
        self.name = "F_%d" % p

    def z(self, a):
        return int(a) % self.p

    def add(self, a, b):
        return (a + b) % self.p

    def mul(self, a, b):
        return (a * b) % self.p

    def isz(self, a):
        return a % self.p == 0

    def inv(self, a):
        return pow(int(a) % self.p, self.p - 2, self.p)

    zero = 0
    one = 1


class Rat:
    p = 0
    name = "Q"
    zero = Fraction(0)
    one = Fraction(1)

    def z(self, a):
        return Fraction(a)

    def add(self, a, b):
        return a + b

    def mul(self, a, b):
        return a * b

    def isz(self, a):
        return a == 0

    def inv(self, a):
        return Fraction(1) / a


def rank(rows, K):
    """exact rank by Gaussian elimination over K."""
    if not rows:
        return 0
    M = [[K.z(x) for x in r] for r in rows]
    nc = len(M[0])
    r = 0
    for c in range(nc):
        piv = None
        for i in range(r, len(M)):
            if not K.isz(M[i][c]):
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        iv = K.inv(M[r][c])
        M[r] = [K.mul(x, iv) for x in M[r]]
        for i in range(len(M)):
            if i != r and not K.isz(M[i][c]):
                f = M[i][c]
                M[i] = [K.add(a, -K.mul(f, b)) for a, b in zip(M[i], M[r])]
        r += 1
        if r == len(M):
            break
    return r


# ---------------------------------------------------------------- Phi
def cell(bl, gs, u, v, a, b, K):
    """A_uv[a][b] with u,v given in ANY order (a is u's letter)."""
    if u < v:
        e = (u, v)
        if e not in gs:
            return K.zero
        return K.z(bl[e][a][b])
    e = (v, u)
    if e not in gs:
        return K.zero
    return K.z(bl[e][b][a])


def phi_raw(m, bl, w, K):
    """Phi(w) by RAW enumeration of all 105 perfect matchings of K_8:
    a matching contributes 0 unless every one of its four edges is a Gamma
    edge (single / absent edges carry no z-free term)."""
    st = S(m)
    gs = st.gs
    tot = K.zero
    for M in PM105:
        pr = K.one
        for (u, v) in M:
            if (u, v) not in gs:
                pr = K.zero
                break
            pr = K.mul(pr, K.z(bl[(u, v)][w[u]][w[v]]))
            if K.isz(pr):
                break
        tot = K.add(tot, pr)
    return tot


def phi_formula(m, bl, w, K):
    """the sigma-count decomposition (k = 0, 2, 4 sigma edges); an
    INDEPENDENT second route to Phi, used as a cross-check of phi_raw."""
    st = S(m)
    gs = st.gs
    x, y = w[:4], w[4:]

    def c(u, v, a, b):
        return cell(bl, gs, u, v, a, b, K)

    ll = {(a, b): c(a, b, x[a], x[b]) for a, b in combinations(LSIDE, 2)}
    rr = {(a, b): c(a, b, y[a - 4], y[b - 4]) for a, b in combinations(RSIDE, 2)}
    d = {a: c(a, SG[a], x[a], y[SG[a] - 4]) for a in LSIDE}
    hafL = K.add(K.add(K.mul(ll[(0, 1)], ll[(2, 3)]),
                       K.mul(ll[(0, 2)], ll[(1, 3)])),
                 K.mul(ll[(0, 3)], ll[(1, 2)]))
    hafR = K.add(K.add(K.mul(rr[(4, 5)], rr[(6, 7)]),
                       K.mul(rr[(4, 6)], rr[(5, 7)])),
                 K.mul(rr[(4, 7)], rr[(5, 6)]))
    tot = K.mul(hafL, hafR)
    for i, j in combinations(LSIDE, 2):
        pp, qq = [t for t in LSIDE if t not in (i, j)]
        si, sj = min(SG[i], SG[j]), max(SG[i], SG[j])
        tot = K.add(tot, K.mul(K.mul(ll[(i, j)], rr[(si, sj)]),
                               K.mul(d[pp], d[qq])))
    tot = K.add(tot, K.mul(K.mul(d[0], d[1]), K.mul(d[2], d[3])))
    return tot


def coeff_single(m, bl, e, w, K):
    """c_e(w) = haf_Gamma(V - endpoints of e)(w), raw over the 105 PMs of
    K_8 restricted to those containing e."""
    st = S(m)
    gs = st.gs
    tot = K.zero
    for M in PM105:
        if e not in M:
            continue
        pr = K.one
        for (u, v) in M:
            if (u, v) == e:
                continue
            if (u, v) not in gs:
                pr = K.zero
                break
            pr = K.mul(pr, K.z(bl[(u, v)][w[u]][w[v]]))
            if K.isz(pr):
                break
        tot = K.add(tot, pr)
    return tot


def is_clean_point(m, bl, K):
    """Phi = 0 at EVERY clean mixed word (raw 105-matching route)."""
    bad = [w for w in S(m).clean if not K.isz(phi_raw(m, bl, w, K))]
    return (not bad), bad


def all_gamma_cells_nonzero(m, bl, K):
    st = S(m)
    return all(not K.isz(K.z(bl[e][i][j]))
               for e in st.gamma for i in range(3) for j in range(3))


def n_words_phi_nonzero(m, bl, K):
    return sum(1 for w in WORDS if not K.isz(phi_raw(m, bl, w, K)))


# ------------------------------------------------- vertex slice machinery
def singles_at(m, kind, v):
    """[(edge, trigger-coordinate, trigger-value, letter-at-v)] over LIVE
    singles incident to vertex v on the given side."""
    st = S(m)
    out = []
    for e in st.live:
        a, b = st.single[e]
        if kind == 'R' and e[1] == v:
            out.append((e, e[0], a, b))
        elif kind == 'L' and e[0] == v:
            out.append((e, e[1], b, a))
    return out


def gamma_slice_neighbours(m, kind, v):
    """the three column labels of the slice matrix and whether the
    corresponding Gamma edge into v is PRESENT."""
    st = S(m)
    if kind == 'R':
        p = SGI[v]
        cols = [SG[q] for q in LSIDE if q != p]
    else:
        cols = [a for a in LSIDE if a != v]
    pres = []
    for s in cols:
        e = (min(v, s), max(v, s))
        pres.append(e in st.gs)
    return cols, pres


def slice_rows(m, bl, kind, v, w, K):
    """(rows, S_matrix, d, u, scale) at vertex (kind,v) for the ambient word
    w (w[v] ignored).  rows[t][j] = d[t]*u[j] + scale*S[t][j].
    Returns None when the scale (hafL at an R-vertex, hafR at an L-vertex)
    vanishes -- the master relation carries no information there."""
    st = S(m)
    gs = st.gs
    x, y = list(w[:4]), list(w[4:])

    def c(a, b, i, j):
        return cell(bl, gs, a, b, i, j, K)

    ll = {(a, b): c(a, b, x[a], x[b]) for a, b in combinations(LSIDE, 2)}
    hafL = K.add(K.add(K.mul(ll[(0, 1)], ll[(2, 3)]),
                       K.mul(ll[(0, 2)], ll[(1, 3)])),
                 K.mul(ll[(0, 3)], ll[(1, 2)]))
    rr = {(a, b): c(a, b, y[a - 4], y[b - 4]) for a, b in combinations(RSIDE, 2)}
    hafR = K.add(K.add(K.mul(rr[(4, 5)], rr[(6, 7)]),
                       K.mul(rr[(4, 6)], rr[(5, 7)])),
                 K.mul(rr[(4, 7)], rr[(5, 6)]))
    dd = {a: c(a, SG[a], x[a], y[SG[a] - 4]) for a in LSIDE}

    if kind == 'R':
        if K.isz(hafL):
            return None
        p = SGI[v]
        sc = hafL
        d = [c(p, v, x[p], t) for t in range(3)]
        u, Smat = [], [[K.zero] * 3 for _ in range(3)]
        for jc, q in enumerate([q for q in LSIDE if q != p]):
            i, j = [t for t in LSIDE if t not in (p, q)]
            u.append(K.mul(dd[q], ll[(min(i, j), max(i, j))]))
            s = SG[q]
            for t in range(3):
                Smat[t][jc] = c(v, s, t, y[s - 4])
    else:
        if K.isz(hafR):
            return None
        p = v
        sc = hafR
        d = [c(p, SG[p], s, y[SG[p] - 4]) for s in range(3)]
        u, Smat = [], [[K.zero] * 3 for _ in range(3)]
        for jc, a in enumerate([a for a in LSIDE if a != p]):
            b, cc = [t for t in LSIDE if t not in (p, a)]
            u.append(K.mul(dd[a], c(SG[b], SG[cc], y[SG[b] - 4],
                                    y[SG[cc] - 4])))
            for s in range(3):
                Smat[s][jc] = c(p, a, s, x[a])
    rows = [[K.add(K.mul(d[t], u[j]), K.mul(sc, Smat[t][j]))
             for j in range(3)] for t in range(3)]
    return rows, Smat, d, u, sc


def psi_vector(m, bl, kind, v, w, K):
    """the coefficient vector of the master relation (B_q resp. X_a)."""
    st = S(m)
    gs = st.gs
    x, y = list(w[:4]), list(w[4:])

    def c(a, b, i, j):
        return cell(bl, gs, a, b, i, j, K)

    ll = {(a, b): c(a, b, x[a], x[b]) for a, b in combinations(LSIDE, 2)}
    hafL = K.add(K.add(K.mul(ll[(0, 1)], ll[(2, 3)]),
                       K.mul(ll[(0, 2)], ll[(1, 3)])),
                 K.mul(ll[(0, 3)], ll[(1, 2)]))
    rr = {(a, b): c(a, b, y[a - 4], y[b - 4]) for a, b in combinations(RSIDE, 2)}
    hafR = K.add(K.add(K.mul(rr[(4, 5)], rr[(6, 7)]),
                       K.mul(rr[(4, 6)], rr[(5, 7)])),
                 K.mul(rr[(4, 7)], rr[(5, 6)]))
    dd = {a: c(a, SG[a], x[a], y[SG[a] - 4]) for a in LSIDE}
    out = []
    if kind == 'R':
        p = SGI[v]
        for q in [q for q in LSIDE if q != p]:
            i, j = [t for t in LSIDE if t not in (p, q)]
            si, sj = min(SG[i], SG[j]), max(SG[i], SG[j])
            out.append(K.add(K.mul(hafL, rr[(si, sj)]),
                             K.mul(ll[(min(p, q), max(p, q))],
                                   K.mul(dd[i], dd[j]))))
    else:
        p = v
        for a in [a for a in LSIDE if a != p]:
            b, cc = [t for t in LSIDE if t not in (p, a)]
            out.append(K.add(K.mul(hafR, ll[(min(b, cc), max(b, cc))]),
                             K.mul(c(SG[p], SG[a], y[SG[p] - 4],
                                     y[SG[a] - 4]),
                                   K.mul(dd[b], dd[cc]))))
    return out


# --------------------------------------------------- admissible choices
def admissible(m, kind, v, relaxed=False):
    """ALL index choices at (kind,v): letters on the 7 coordinates != v.

    STRICT (= W26's and W30's filter): fire nonempty; no completion is a
    constant word; every clean completion is a clean word; every firing
    completion has all its active live singles incident to v.
    RELAXED (A10's own, strictly more permissive): drop from T_c / T_f the
    letters whose completion is constant or fails its condition, and keep
    the index choice whenever T_f is nonempty.
    Returns [(word7-as-full-word-with-v=0, T_f tuple, T_c tuple)].
    """
    st = S(m)
    mine = singles_at(m, kind, v)
    others = [c for c in range(NV) if c != v]
    out = []
    for vals in product(range(3), repeat=7):
        w = [0] * NV
        for c, a in zip(others, vals):
            w[c] = a
        fire = set()
        for (e, trig, tv, letter) in mine:
            if w[trig] == tv:
                fire.add(letter)
        if not fire:
            continue
        Tc, Tf, ok = [], [], True
        for t in range(3):
            ww = list(w)
            ww[v] = t
            const = len(set(ww)) == 1
            act = st.active_live(tuple(ww))
            if t not in fire:
                good = (not const) and (not act)
                if good:
                    Tc.append(t)
                elif not relaxed:
                    ok = False
                    break
            else:
                good = (not const) and all(
                    (e[1] if kind == 'R' else e[0]) == v for e in act)
                if good:
                    Tf.append(t)
                elif not relaxed:
                    ok = False
                    break
        if not ok or not Tf:
            continue
        out.append((tuple(w), tuple(sorted(Tf)), tuple(sorted(Tc))))
    return out


_ADM = {}


def admissible_cached(m, kind, v, relaxed=False):
    k = (m, kind, v, relaxed)
    if k not in _ADM:
        _ADM[k] = admissible(m, kind, v, relaxed)
    return _ADM[k]


VERTS = ('R4', 'R5', 'R6', 'R7', 'L0', 'L1', 'L2', 'L3')


def vsplit(lab):
    return lab[0], int(lab[1:])


def vertex_verdict(m, bl, kind, v, K, relaxed=False, detail=False):
    """EXHAUSTIVE delivery test.  Returns both failure notions:
      DELIVERS      : delivers at some admissible index choice
      FAIL_primary  : not DELIVERS
      FAIL_star     : at EVERY admissible (nonzero-scale) index choice,
                      rank{clean rows} == 1 and rank{clean+firing} == 2
                      (W26's derived characterisation (*))
    """
    idx = admissible_cached(m, kind, v, relaxed)
    n_scale0 = n_live = n_del = 0
    star = True
    n_star_bad = 0
    dets = []
    for (w, Tf, Tc) in idx:
        sd = slice_rows(m, bl, kind, v, w, K)
        if sd is None:
            n_scale0 += 1
            continue
        rows, Smat, d, u, sc = sd
        n_live += 1
        cleanrows = [rows[t] for t in Tc]
        rc = rank(cleanrows, K)
        ok = all(rank(cleanrows + [rows[t]], K) == rc for t in Tf)
        starhere = (rc == 1) and all(
            rank(cleanrows + [rows[t]], K) == 2 for t in Tf)
        if not starhere:
            star = False
            n_star_bad += 1
        if ok:
            n_del += 1
            if detail:
                dets.append((w, Tf, Tc))
    return dict(n_idx_total=len(idx), n_idx_live=n_live, n_scale0=n_scale0,
                n_deliver=n_del, DELIVERS=n_del > 0,
                FAIL_primary=n_del == 0, FAIL_star=star and n_live > 0,
                n_star_bad=n_star_bad, detail=dets)


def full_verdict(m, bl, K, relaxed=False):
    rec = {}
    for lab in VERTS:
        kind, v = vsplit(lab)
        rec[lab] = vertex_verdict(m, bl, kind, v, K, relaxed)
    rec['fails'] = [l for l in VERTS if rec[l]['FAIL_primary']]
    rec['fails_star'] = [l for l in VERTS if rec[l]['FAIL_star']]
    return rec


# ------------------------------------------------------------- self-check
def check_master(m, bl, K, kind, v, words):
    """numerically verify the hand-derived master relation
       scale * Phi(w with v=t) == <psi, ROW(t)>   for all t."""
    bad = []
    for w in words:
        sd = slice_rows(m, bl, kind, v, w, K)
        if sd is None:
            continue
        rows, Smat, d, u, sc = sd
        ps = psi_vector(m, bl, kind, v, w, K)
        for t in range(3):
            ww = list(w)
            ww[v] = t
            lhs = K.mul(sc, phi_raw(m, bl, tuple(ww), K))
            rhs = K.zero
            for j in range(3):
                rhs = K.add(rhs, K.mul(ps[j], rows[t][j]))
            if not K.isz(K.add(lhs, -rhs)):
                bad.append((tuple(ww), t))
    return bad
