#!/usr/bin/env python3
"""W26 DECISIVE ADVERSARIAL LANE (adv2) -- independent exact machinery.

UNAUDITED PROBE.  EXACT ARITHMETIC ONLY (fractions.Fraction, the exact
extension rings Q2 = Q[t]/(t^2+t+1) and Qi = Q[t]/(t^2+1), or F_p).
NO FLOATS ANYWHERE.

Everything here is RE-DERIVED independently of adv/ and cross-checked
against w26_core's from-the-definition engine (C.H_word, 105 matchings).

Notation (re-derived from the L-subset expansion, verified in a2_setup):
   L = {0,1,2,3}, R = {4,5,6,7}, sigma = 0<->7, 1<->4, 2<->5, 3<->6.
   D_p     = A_{p,sigma p}[x_p][y_{sigma p}]       (0 if that edge absent)
   Lam_ij  = A_ij[x_i][x_j]         (i<j in L; K_4 always present)
   Rho_jk  = A_jk[y_j][y_k]         (0 off the R-graph)
   Phi = D0 D1 D2 D3
       + sum_{i<j in L} Lam_ij * Rho_{sig i, sig j} * D_p D_q   ({p,q}=L-{i,j})
       + hafL * hafR
   c_{(p,j)} = D_{r1} Lam_{q,r2} Rho_{sig p, sig r2}
             + D_{r2} Lam_{q,r1} Rho_{sig p, sig r1}
       where q = sigma^{-1}(j) and {r1,r2} = L - {p,q}.
"""
from __future__ import annotations

import os
import sys
from fractions import Fraction
from itertools import combinations, product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
UP = os.path.dirname(HERE)
sys.path.insert(0, UP)
sys.path.insert(0, os.path.join(UP, "adv"))
sys.path.insert(0, HERE)
import w26_core as C                                              # noqa: E402
import w26_fast as FA                                             # noqa: E402
import w26_sub as SB                                             # noqa: E402
import w26_pts as PT                                              # noqa: E402
import adv_lib as AL                                              # noqa: E402

F = Fraction
Q2 = AL.Q2          # Q(omega), omega^2 + omega + 1 = 0
Qi = AL.Qi          # Q(i)
Fp = AL.Fp

L = (0, 1, 2, 3)
R = (4, 5, 6, 7)
SIG = {0: 7, 1: 4, 2: 5, 3: 6}
SIGI = {v: k for k, v in SIG.items()}
LPAIRS = tuple(combinations(L, 2))
# (i,j) in L  ->  (R-pair, complementary L-pair)
DUAL = {}
for _i, _j in LPAIRS:
    _p, _q = [t for t in L if t not in (_i, _j)]
    _a, _b = sorted((SIG[_i], SIG[_j]))
    DUAL[(_i, _j)] = ((_a, _b), (_p, _q))


def ring_of(bl):
    x = bl[sorted(bl)[0]][0][0]
    if isinstance(x, Fp):
        return Fp(0, x.p), Fp(1, x.p)
    if isinstance(x, AL._Ext):
        return type(x)(0, 0), type(x)(1, 0)
    return F(0), F(1)


class Geo:
    """per-m geometry: Gamma edges, singles + cells, live singles, clean
    words, solo word families, residual-row skeleton."""

    _cache = {}

    def __new__(cls, m):
        if m in cls._cache:
            return cls._cache[m]
        self = super().__new__(cls)
        self.m = m
        self.T = C.TEMPLATES[m]
        self.gam = tuple(C.gamma_edges(self.T))
        self.gs = set(self.gam)
        self.sing = C.single_edges(self.T)          # edge -> (a,b)
        self.live = tuple(C.live_singles(m))
        self.clean = tuple(C.clean_words(m))
        self.solo = {e: tuple(SB.solo_words(m, e)) for e in self.live}
        cls._cache[m] = self
        return self

    def active(self, e, w):
        a, b = self.sing[e]
        return w[e[0]] == a and w[e[1]] == b

    def active_set(self, w):
        return tuple(e for e in self.live if self.active(e, w))


# ------------------------------------------------------- fast exact Phi/c
def parts(bl, G, w):
    """(D, Lam, Rho) at the word w, ring-generic."""
    z, _ = ring_of(bl)
    x, y = w[:4], w[4:]
    D = {}
    for p in L:
        e = (p, SIG[p]) if p < SIG[p] else (SIG[p], p)
        D[p] = bl[e][x[p]][y[SIG[p] - 4]] if e in G.gs else z
    Lam = {(i, j): bl[(i, j)][x[i]][x[j]] for i, j in LPAIRS}
    Rho = {}
    for j, k in combinations(R, 2):
        Rho[(j, k)] = bl[(j, k)][y[j - 4]][y[k - 4]] if (j, k) in G.gs else z
    return D, Lam, Rho


def phi2(bl, G, w):
    z, _ = ring_of(bl)
    D, Lam, Rho = parts(bl, G, w)
    hafL = (Lam[(0, 1)] * Lam[(2, 3)] + Lam[(0, 2)] * Lam[(1, 3)]
            + Lam[(0, 3)] * Lam[(1, 2)])
    hafR = (Rho[(4, 5)] * Rho[(6, 7)] + Rho[(4, 6)] * Rho[(5, 7)]
            + Rho[(4, 7)] * Rho[(5, 6)])
    tot = D[0] * D[1] * D[2] * D[3] + hafL * hafR
    for ij in LPAIRS:
        rp, (p, q) = DUAL[ij]
        tot = tot + Lam[ij] * Rho[rp] * D[p] * D[q]
    return tot


def coef2(bl, G, e, w):
    """c_e(w) for a cross single e=(p,j)."""
    p, j = e
    q = SIGI[j]
    r1, r2 = [t for t in L if t not in (p, q)]
    D, Lam, Rho = parts(bl, G, w)

    def term(ra, rb):
        lp = (min(q, rb), max(q, rb))
        rr = tuple(sorted((SIG[p], SIG[rb])))
        return D[ra] * Lam[lp] * Rho[rr]
    return term(r1, r2) + term(r2, r1)


# ------------------------------------------------------------- predicates
def all_cells_nonzero(bl, G=None):
    ed = bl if G is None else G.gam
    return all(bl[e][i][j] != 0 for e in ed for i in range(3)
               for j in range(3))


def is_clean(m, bl):
    G = Geo(m)
    if not all_cells_nonzero(bl, G):
        return False
    return all(phi2(bl, G, w) == 0 for w in G.clean)


def on_stratum(m, bl):
    G = Geo(m)
    return all(phi2(bl, G, w) == 0 for w in C.WORDS)


def phi_support(m, bl):
    G = Geo(m)
    return tuple(w for w in C.WORDS if phi2(bl, G, w) != 0)


def solo_verdict(m, bl, e):
    """the e-solo family verdict, re-derived (not SB.solo_report)."""
    G = Geo(m)
    z, _ = ring_of(bl)
    pure = badconst = 0
    ratios = set()
    ex_pure = None
    for w in G.solo[e]:
        c = coef2(bl, G, e, w)
        ph = phi2(bl, G, w)
        if c == 0:
            if ph != 0:
                badconst += 1
            continue
        r = (z - ph) / c
        ratios.add(r)
        if r == 0:
            pure += 1
            if ex_pure is None:
                ex_pure = w
    surv = (pure == 0 and badconst == 0 and len(ratios) == 1
            and not any(r == 0 for r in ratios))
    return dict(e=str(e), n_solo=len(G.solo[e]), n_pure=pure,
                n_badconst=badconst, n_ratios=len(ratios),
                ratios=sorted(str(r) for r in ratios)[:4],
                survives=surv, example_pure=list(ex_pure) if ex_pure else None,
                ratio=(str(list(ratios)[0]) if len(ratios) == 1 else None))


def solo_survivors(m, bl):
    return [e for e in Geo(m).live if solo_verdict(m, bl, e)["survives"]]


# ------------------------------------------- residual system (independent)
def resid_rows(m, bl):
    """my own build of the degree-<=1 residual rows.
    Returns (live, [(w, coeffvec, const)])."""
    G = Geo(m)
    z, _ = ring_of(bl)
    idx = {e: i for i, e in enumerate(G.live)}
    n = len(G.live)
    out = []
    for w in C.MIXED:
        act = [e for e in G.sing if G.active(e, w)]
        ones = [e for e in act if e in idx]
        if not ones:
            continue
        deg2 = False
        for a, b in combinations(act, 2):
            if len(set(a) | set(b)) != 4:
                continue
            rest = tuple(v for v in range(8) if v not in set(a) | set(b))
            if C.has_pm(G.gs, rest):
                deg2 = True
                break
        if deg2:
            continue
        v = [z] * n
        for e in ones:
            v[idx[e]] = coef2(bl, G, e, w)
        c = phi2(bl, G, w)
        if any(t != 0 for t in v) or c != 0:
            out.append((w, v, c))
    return G.live, out


def rref_g(rows, ncols, z, o):
    M = [list(r) for r in rows]
    piv, r = [], 0
    for c in range(ncols):
        sel = None
        for i in range(r, len(M)):
            if M[i][c] != z:
                sel = i
                break
        if sel is None:
            continue
        M[r], M[sel] = M[sel], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != z:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    return M[:r], piv


def kernel_g(rows, ncols, z, o):
    if not rows:
        return [[(o if i == k else z) for i in range(ncols)]
                for k in range(ncols)]
    Rw, piv = rref_g(rows, ncols, z, o)
    out = []
    for f in [c for c in range(ncols) if c not in piv]:
        v = [z] * ncols
        v[f] = o
        for i, p in enumerate(piv):
            v[p] = z - Rw[i][f]
        out.append(v)
    return out


def full_verdict(m, bl):
    """my own clone of C.verdict, plus an explicit z solution if alive."""
    z, o = ring_of(bl)
    cells, rows = resid_rows(m, bl)
    n = len(cells)
    aug = [list(v) + [z - c] for _, v, c in rows]
    Rw, piv = rref_g(aug, n + 1, z, o)
    if n in piv:
        return dict(n_unknowns=n, n_rows=len(rows), rank=len(piv),
                    inconsistent=True, killed=True, forced_zero=[], zsol=None)
    sol = [z] * n
    for i, pc in enumerate(piv):
        if pc < n:
            sol[pc] = Rw[i][n]
    ker = kernel_g([list(v) for _, v, _ in rows], n, z, o)
    forced = [str(cells[i]) for i in range(n)
              if sol[i] == 0 and all(b[i] == 0 for b in ker)]
    return dict(n_unknowns=n, n_rows=len(rows), rank=len(piv),
                inconsistent=False, solution_dim=len(ker),
                forced_zero=forced, killed=bool(forced),
                zsol={str(cells[i]): str(sol[i]) for i in range(n)},
                zsol_raw=sol, cells=[str(c) for c in cells],
                kernel=[[str(t) for t in b] for b in ker], kernel_raw=ker)


def pure_row_singles(m, bl):
    """which live singles carry at least one PURE row (Phi=0, c_e!=0)."""
    G = Geo(m)
    out = {}
    for e in G.live:
        n = 0
        for w in G.solo[e]:
            if phi2(bl, G, w) == 0 and coef2(bl, G, e, w) != 0:
                n += 1
        out[str(e)] = n
    return out


# --------------------------------------- FINAL independent verification
def raw_verify(m, bl, zmap):
    """evaluate H_w straight from C.H_word (105 matchings) at every one of
    the 6558 mixed words.  Returns (n_nonzero, first_bad_word, H_const)."""
    T = C.TEMPLATES[m]
    z = {e: zmap[e] for e in C.single_edges(T)}
    bad = 0
    first = None
    for w in C.MIXED:
        h = C.H_word(bl, T, z, w)
        if h != 0:
            bad += 1
            if first is None:
                first = list(w)
    cons = [str(C.H_word(bl, T, z, (c,) * 8)) for c in range(3)]
    return bad, first, cons


def dump(bl):
    return {str(e): [[str(x) for x in row] for row in bl[e]]
            for e in sorted(bl)}


def load(d):
    return {tuple(int(t) for t in k.strip("()").split(",")):
            [[F(x) for x in row] for row in v] for k, v in d.items()}


def to_fp(bl, p):
    return {e: [[Fp(int(x.numerator) * pow(int(x.denominator), p - 2, p), p)
                 for x in row] for row in bl[e]] for e in bl}


def outer(u, v):
    return [[u[i] * v[j] for j in range(3)] for i in range(3)]
