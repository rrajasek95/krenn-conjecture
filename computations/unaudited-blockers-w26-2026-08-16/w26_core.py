#!/usr/bin/env python3
"""W26 -- THE THREE BLOCKER STATEMENTS.  UNAUDITED PROBE.

Pinned HEAD: see PINNED_HEAD.txt.  Nothing here is a proved claim of the
repository.  EXACT ARITHMETIC ONLY (int / Fraction / sympy exact / finite
fields).  No floats anywhere.

MODEL (re-typed from the definition; w26_ctrl.py asserts agreement with
w21_core and w24_core):
  N = 8 vertices, alphabet {0,1,2}; 3x3 block A_uv per edge uv of K_8.
  H_w(A) = sum over the 105 perfect matchings M of prod_{(u,v) in M}
           A_uv[w_u][w_v].
  EXACT  <=>  H_w = 1 on the three constant words, 0 on the 6,558 mixed.
  Template T: 9-bit mask per edge; support m = #edges with nonzero mask.

STRUCTURE at m=25..28 (verified in w26_struct):
  L = {0,1,2,3}, R = {4,5,6,7}, sigma = (0<->7, 1<->4, 2<->5, 3<->6).
  Gamma = K_4(L)  u  R-graph  u  {matching edges sigma present at this m};
  the twelve SINGLES are exactly the twelve non-sigma cross edges, each
  carrying one cell.
    m=28: R = K_4,                    all four sigma edges
    m=27: R = K_4 - (5,7),            all four sigma edges
    m=26: R = K_4 - (4,6) - (5,7),    all four sigma edges
    m=25: R = K_4 - (4,6) - (5,7),    sigma edges minus (3,6)
"""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations, product

sys.dont_write_bytecode = True

N = 8
Q = 3
FULL = 511

EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}

L = (0, 1, 2, 3)
R = (4, 5, 6, 7)
SIG = {0: 7, 1: 4, 2: 5, 3: 6}
SIGINV = {v: k for k, v in SIG.items()}
PAIRINGS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def _pms(vs):
    if not vs:
        return [()]
    a, rest = vs[0], vs[1:]
    out = []
    for i, b in enumerate(rest):
        for mm in _pms(rest[:i] + rest[i + 1:]):
            out.append(((a, b),) + mm)
    return out


PMS = tuple(tuple(sorted(m)) for m in _pms(tuple(range(N))))
assert len(PMS) == 105

WORDS = tuple(product(range(Q), repeat=N))
MIXED = tuple(w for w in WORDS if len(set(w)) > 1)
assert len(MIXED) == 6558

# identical literal encoding to W8/W19/W20/W21/W24 (independently re-typed).
TEMPLATES = {
    24: [511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511, 8, 0,
         128, 32, 64, 128, 0, 256, 511, 0, 511, 511, 0, 511],
    25: [511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511, 8, 511,
         128, 32, 64, 128, 0, 256, 511, 0, 511, 511, 0, 511],
    26: [511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511, 8, 511,
         128, 32, 64, 128, 511, 256, 511, 0, 511, 511, 0, 511],
    27: [511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511, 8, 511,
         128, 32, 64, 128, 511, 256, 511, 511, 511, 511, 0, 511],
    28: [511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511, 8, 511,
         128, 32, 64, 128, 511, 256, 511, 511, 511, 511, 511, 511],
}


def gamma_edges(T):
    return tuple(EDGES[i] for i, t in enumerate(T) if t == FULL)


def single_edges(T):
    out = {}
    for i, t in enumerate(T):
        if t in (0, FULL):
            continue
        cs = [c for c in range(9) if (t >> c) & 1]
        assert len(cs) == 1, (EDGES[i], t, cs)
        out[EDGES[i]] = (cs[0] // 3, cs[0] % 3)
    return out


# --------------------------------------------------------------- hafnians
def haf_on(blocks, gam_set, verts, w, zero=None, one=None):
    """sum over perfect matchings of Gamma restricted to `verts`.
    Generic in the coefficient ring (pass zero/one for sympy / GF(p))."""
    if zero is None:
        zero, one = Fraction(0), Fraction(1)
    verts = tuple(sorted(verts))
    if not verts:
        return one
    a = verts[0]
    tot = zero
    for i in range(1, len(verts)):
        b = verts[i]
        e = (a, b) if a < b else (b, a)
        if e not in gam_set:
            continue
        c = blocks[e][w[e[0]]][w[e[1]]]
        tot = tot + c * haf_on(blocks, gam_set, verts[1:i] + verts[i + 1:],
                               w, zero, one)
    return tot


def phi(blocks, gam_set, w, zero=None, one=None):
    return haf_on(blocks, gam_set, tuple(range(N)), w, zero, one)


def coeff(blocks, gam_set, e, w, zero=None, one=None):
    """c_e(w) = haf_Gamma(V - endpoints of e)(w)."""
    rest = tuple(v for v in range(N) if v not in e)
    return haf_on(blocks, gam_set, rest, w, zero, one)


def has_pm(gam_set, verts):
    verts = tuple(sorted(verts))
    if not verts:
        return True
    a = verts[0]
    for i in range(1, len(verts)):
        b = verts[i]
        e = (a, b) if a < b else (b, a)
        if e in gam_set and has_pm(gam_set, verts[1:i] + verts[i + 1:]):
            return True
    return False


def live_singles(m):
    T = TEMPLATES[m]
    gs = set(gamma_edges(T))
    return tuple(sorted(e for e in single_edges(T)
                        if has_pm(gs, tuple(v for v in range(N)
                                            if v not in e))))


def H_word(blocks, T, z, w):
    """H_w from the definition (all 105 matchings)."""
    sing = single_edges(T)
    gs = set(gamma_edges(T))
    tot = Fraction(0)
    for M in PMS:
        p = Fraction(1)
        for (u, v) in M:
            if (u, v) in gs:
                p *= blocks[(u, v)][w[u]][w[v]]
            elif (u, v) in sing and (w[u], w[v]) == sing[(u, v)]:
                p *= z[(u, v)]
            else:
                p = Fraction(0)
            if p == 0:
                break
        tot += p
    return tot


def clean_words(m):
    """mixed words at which NO LIVE single is active."""
    T = TEMPLATES[m]
    sing = single_edges(T)
    lv = set(live_singles(m))
    out = []
    for w in MIXED:
        if all(not (e in lv and w[e[0]] == a and w[e[1]] == b)
               for e, (a, b) in sing.items()):
            out.append(w)
    return tuple(out)


def active_live(m, w):
    T = TEMPLATES[m]
    sing = single_edges(T)
    lv = set(live_singles(m))
    return tuple(e for e in lv
                 if w[e[0]] == sing[e][0] and w[e[1]] == sing[e][1])


# --------------------------------------------------- explicit Phi formula
def phi_formula(bl, m, w, zero=None, one=None):
    """Phi = hafL*hafR + sum_{ij} l_ij r_{sig i, sig j} d_p d_q + d0d1d2d3,
    with absent edges read as 0.  (Identity; checked in w26_struct.)"""
    if zero is None:
        zero, one = Fraction(0), Fraction(1)
    gs = set(gamma_edges(TEMPLATES[m]))
    x, y = w[:4], w[4:]

    def cl(u, v, a, b):
        e = (u, v) if u < v else (v, u)
        if e not in gs:
            return zero
        return bl[e][a][b] if u < v else bl[e][b][a]

    ll = {(a, b): cl(a, b, x[a], x[b]) for a, b in combinations(L, 2)}
    rr = {(a, b): cl(a, b, y[a - 4], y[b - 4]) for a, b in combinations(R, 2)}
    d = {a: cl(a, SIG[a], x[a], y[SIG[a] - 4]) for a in L}
    hafL = sum((ll[p] * ll[q] for p, q in PAIRINGS), zero)
    hafR = (rr[(4, 5)] * rr[(6, 7)] + rr[(4, 6)] * rr[(5, 7)]
            + rr[(4, 7)] * rr[(5, 6)])
    tot = hafL * hafR
    for i, j in combinations(L, 2):
        p, q = [t for t in L if t not in (i, j)]
        si, sj = min(SIG[i], SIG[j]), max(SIG[i], SIG[j])
        tot = tot + ll[(i, j)] * rr[(si, sj)] * d[p] * d[q]
    tot = tot + d[0] * d[1] * d[2] * d[3]
    return tot


# --------------------------------------------- Phi as linear in y6 data
def phi_y6_parts(bl, m, x, y4, y5, y7, zero=None, one=None):
    """Phi(x, (y4,y5,y6,y7)) = A*A36[x3][y6] + B*A67[y6][y7]
                               + Cc*A56[y5][y6] + D*A46[y4][y6],
    returning (A, B, Cc, D).  Absent edges -> the coefficient is unused."""
    if zero is None:
        zero, one = Fraction(0), Fraction(1)
    gs = set(gamma_edges(TEMPLATES[m]))

    def cl(u, v, a, b):
        e = (u, v) if u < v else (v, u)
        if e not in gs:
            return zero
        return bl[e][a][b] if u < v else bl[e][b][a]

    ll = {(a, b): cl(a, b, x[a], x[b]) for a, b in combinations(L, 2)}
    hafL = sum((ll[p] * ll[q] for p, q in PAIRINGS), zero)
    d0 = cl(0, 7, x[0], y7)
    d1 = cl(1, 4, x[1], y4)
    d2 = cl(2, 5, x[2], y5)
    r45 = cl(4, 5, y4, y5)
    r47 = cl(4, 7, y4, y7)
    r57 = cl(5, 7, y5, y7)
    A = (ll[(0, 1)] * d2 * r47 + ll[(0, 2)] * d1 * r57
         + ll[(1, 2)] * d0 * r45 + d0 * d1 * d2)
    B = hafL * r45 + ll[(0, 3)] * d1 * d2
    Cc = hafL * r47 + ll[(2, 3)] * d0 * d1
    D = hafL * r57 + ll[(1, 3)] * d0 * d2
    return A, B, Cc, D


# ---------------------------------------------------------- linear algebra
def rref(rows, ncols, zero=None, one=None):
    if zero is None:
        zero, one = Fraction(0), Fraction(1)
    M = [list(r) for r in rows]
    piv, r = [], 0
    for c in range(ncols):
        sel = None
        for i in range(r, len(M)):
            if M[i][c] != zero:
                sel = i
                break
        if sel is None:
            continue
        M[r], M[sel] = M[sel], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != zero:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    return M[:r], piv


def kernel_basis(rows, ncols):
    if not rows:
        return [[Fraction(int(i == k)) for i in range(ncols)]
                for k in range(ncols)]
    Rw, piv = rref(rows, ncols)
    out = []
    for f in [c for c in range(ncols) if c not in piv]:
        v = [Fraction(0)] * ncols
        v[f] = Fraction(1)
        for i, p in enumerate(piv):
            v[p] = -Rw[i][f]
        out.append(v)
    return out


# --------------------------------------------------- the residual system
def residual_rows(m, bl):
    """(cells, [(w, coeffvec, const)]) over the combinatorial degree-<=1
    words (point-independent skeleton), live singles only."""
    T = TEMPLATES[m]
    gs = set(gamma_edges(T))
    sing = single_edges(T)
    lv = live_singles(m)
    idx = {e: i for i, e in enumerate(lv)}
    out = []
    for w in MIXED:
        act = [e for e in sing
               if w[e[0]] == sing[e][0] and w[e[1]] == sing[e][1]]
        ones = [e for e in act if e in idx]
        if not ones:
            continue
        deg2 = False
        for a, b in combinations(act, 2):
            if len(set(a) | set(b)) != 4:
                continue
            rest = tuple(v for v in range(N) if v not in set(a) | set(b))
            if has_pm(gs, rest):
                deg2 = True
                break
        if deg2:
            continue
        v = [Fraction(0)] * len(lv)
        for e in ones:
            v[idx[e]] = coeff(bl, gs, e, w)
        c = phi(bl, gs, w)
        if any(v) or c != 0:
            out.append((w, v, c))
    return lv, out


def verdict(m, bl):
    cells, rows = residual_rows(m, bl)
    n = len(cells)
    aug = [list(v) + [-c] for _, v, c in rows]
    Rw, piv = rref(aug, n + 1)
    if n in piv:
        return dict(n_unknowns=n, n_rows=len(rows), rank=len(piv),
                    inconsistent=True, forced_zero=[], killed=True)
    sol = [Fraction(0)] * n
    for i, pc in enumerate(piv):
        if pc < n:
            sol[pc] = Rw[i][n]
    ker = kernel_basis([list(v) for _, v, _ in rows], n)
    forced = [str(cells[i]) for i in range(n)
              if sol[i] == 0 and all(b[i] == 0 for b in ker)]
    return dict(n_unknowns=n, n_rows=len(rows), rank=len(piv),
                inconsistent=False, solution_dim=len(ker),
                forced_zero=forced, killed=bool(forced))


def pure_rows(m, bl):
    """[(w, e)] : e-solo words with Phi = 0 and c_e != 0  (the PURE ROWS)."""
    cells, rows = residual_rows(m, bl)
    out = []
    for w, v, c in rows:
        nz = [i for i in range(len(cells)) if v[i] != 0]
        if len(nz) == 1 and c == 0:
            out.append((w, cells[nz[0]]))
    return out
