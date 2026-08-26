#!/usr/bin/env python3
"""UNAUDITED PROBE (W21) -- the two finishing moves.

Pinned HEAD: see PINNED_HEAD.txt.  Nothing here is a proved claim of the
repository.  Every verdict uses exact arithmetic (Python int / Fraction /
exact sparse polynomials / Singular over Q).  Floats are used NOWHERE.

This module is the W21 shared core.  It re-implements the pieces of the
model it needs (hafnians, Pfaffians, the sub-Pfaffian adjugate, the
site-linear systems) INDEPENDENTLY of W20 and cross-checks against
W20's engine in w21_controls.py.

THE PFAFFIAN FRAME (the new object of W21).
  For a word w let S(w) be the 8x8 antisymmetric matrix
      S(w)[u][v] = eps_uv * A_uv[w_u][w_v]   for uv in Gamma (u < v),
      S(w)[u][v] = 0                          otherwise,
  where eps is a PFAFFIAN SIGNING of Gamma (all perfect matchings of
  Gamma get the same sign) -- so Phi_w = +/- Pf(S(w)).
  Let Q(w) be the PFAFFIAN ADJUGATE,
      Q[a][b] = (-1)^(a+b+1) Pf(S with rows/cols a,b deleted)   (a < b),
  antisymmetric.  Classical facts used (all re-verified exactly here):
      (P1)  S Q = Q S = Pf(S) * Id,
      (P2)  Q_ij Q_kl - Q_ik Q_jl + Q_il Q_jk = Pf(S) * Pf(S_{ijkl deleted}),
      (P3)  for uv in Gamma, Pf(S_{u,v deleted}) = +/- haf(Gamma-u-v)(w)
            with a sign depending only on the pair uv.
  CONSEQUENCE (the W21 identity network): on the clean layer Pf(S(w)) = 0,
  so by (P2) the antisymmetric matrix Q(w) satisfies every Pluecker
  relation, i.e.  rank Q(w) <= 2.  By (P3) the row of Q at site t,
  restricted to N_Gamma(t), is exactly W20-L's coefficient vector
  C^t_s(w) up to fixed signs.  So the coefficient vectors of ALL EIGHT
  sites at one clean word are the rows of a single rank-<=2 form.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations, product

sys.dont_write_bytecode = True

N = 8
Q3 = 3
FULL = 511

EDGES = tuple(combinations(range(N), 2))
NE = len(EDGES)
EIDX = {e: i for i, e in enumerate(EDGES)}


def _pms(vs):
    if not vs:
        return [()]
    a, rest = vs[0], vs[1:]
    out = []
    for i, b in enumerate(rest):
        sub = rest[:i] + rest[i + 1:]
        for m in _pms(sub):
            out.append(((a, b),) + m)
    return out


PMS = tuple(tuple(sorted(m)) for m in _pms(tuple(range(N))))
assert len(PMS) == 105

WORDS = tuple(product(range(Q3), repeat=N))
MIXED = tuple(w for w in WORDS if len(set(w)) > 1)
CONSTS = tuple((c,) * N for c in range(Q3))

# ---- templates (same encoding as W8/W15/W16/W19/W20) ----------------------
W8_IMMUNE = {
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
C8_MEMBER = [1, 16, 256, 511, 511, 503, 447, 256, 16, 510, 495, 511, 511, 1,
             383, 511, 510, 511, 511, 255, 511, 383, 1, 16, 256, 256, 16, 1]


def cell_index(ei, w):
    u, v = EDGES[ei]
    return 3 * w[u] + w[v]


def support(T, w):
    return [mi for mi, m in enumerate(PMS)
            if all((T[EIDX[e]] >> cell_index(EIDX[e], w)) & 1 for e in m)]


def gamma_edges(T):
    return [EDGES[i] for i, t in enumerate(T) if t == FULL]


def pms_inside(edges):
    S = set(edges)
    return [mi for mi, m in enumerate(PMS) if all(e in S for e in m)]


def clean_words(T):
    """mixed words at which every supported matching lies inside Gamma."""
    F = set(pms_inside(gamma_edges(T)))
    return [w for w in MIXED if all(mi in F for mi in support(T, w))]


# ---------------------------------------------------------- linear algebra
def rref(rows, ncols):
    M = [list(r) for r in rows]
    piv, r = [], 0
    for c in range(ncols):
        sel = None
        for i in range(r, len(M)):
            if M[i][c]:
                sel = i
                break
        if sel is None:
            continue
        M[r], M[sel] = M[sel], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    return M[:r], piv


def rank_of(rows, ncols=None):
    if not rows:
        return 0
    if ncols is None:
        ncols = len(rows[0])
    return len(rref(rows, ncols)[0])


def kernel_basis(rows, ncols):
    if not rows:
        return [[Fraction(int(i == k)) for i in range(ncols)]
                for k in range(ncols)]
    R, piv = rref(rows, ncols)
    out = []
    for f in [c for c in range(ncols) if c not in piv]:
        v = [Fraction(0)] * ncols
        v[f] = Fraction(1)
        for i, p in enumerate(piv):
            v[p] = -R[i][f]
        out.append(v)
    return out


# --------------------------------------------------------------- hafnians
def haf_verts(blocks, edgeset, verts, w):
    """sum over perfect matchings of `edgeset` on the vertex list `verts`."""
    verts = tuple(sorted(verts))
    if not verts:
        return Fraction(1)
    a = verts[0]
    tot = Fraction(0)
    for i in range(1, len(verts)):
        b = verts[i]
        e = (a, b) if a < b else (b, a)
        if e not in edgeset:
            continue
        tot += (blocks[e][w[e[0]]][w[e[1]]]
                * haf_verts(blocks, edgeset, verts[1:i] + verts[i + 1:], w))
    return tot


def phi_value(blocks, gam, w):
    return haf_verts(blocks, set(gam), tuple(range(N)), w)


# -------------------------------------------------------------- Pfaffians
def pf_sign(m):
    """sign of the permutation (a1 b1 a2 b2 ...) for the matching m."""
    seq = [x for e in m for x in e]
    s, seen = 1, list(seq)
    # count inversions
    inv = 0
    for i in range(len(seen)):
        for j in range(i + 1, len(seen)):
            if seen[i] > seen[j]:
                inv += 1
    return -1 if inv % 2 else 1


def pfaffian(M, idx):
    """Pfaffian of the antisymmetric matrix M restricted to the index list."""
    idx = tuple(idx)
    n = len(idx)
    if n == 0:
        return Fraction(1)
    if n % 2:
        return Fraction(0)
    a = idx[0]
    tot = Fraction(0)
    for i in range(1, n):
        b = idx[i]
        if M[a][b]:
            sub = idx[1:i] + idx[i + 1:]
            sgn = -1 if (i - 1) % 2 else 1
            tot += sgn * M[a][b] * pfaffian(M, sub)
    return tot


def pf_adjugate(M):
    """Q[a][b] = (-1)^(a+b+1) Pf(M with a,b deleted)  (a<b), antisymmetric."""
    n = len(M)
    Q = [[Fraction(0)] * n for _ in range(n)]
    for a in range(n):
        for b in range(a + 1, n):
            idx = [i for i in range(n) if i != a and i != b]
            v = pfaffian(M, idx)
            s = -1 if (a + b) % 2 == 0 else 1     # (-1)^(a+b+1)
            Q[a][b] = s * v
            Q[b][a] = -s * v
    return Q


def pfaffian_signing(gam):
    """signs eps_e in {1,-1} making all perfect matchings of gam agree, i.e.
    haf(gam) = +/- Pf.  Returns (eps dict, common sign) or (None, None)."""
    F = [PMS[mi] for mi in pms_inside(gam)]
    if not F:
        return {e: 1 for e in gam}, 1
    # GF(2) system: sum_{e in M} x_e = (1-sgn(M))/2 + c    (c an unknown)
    ids = {e: i for i, e in enumerate(gam)}
    ncol = len(gam) + 1
    rows = []
    for m in F:
        r = [0] * ncol
        for e in m:
            r[ids[e]] ^= 1
        r[len(gam)] = 1                       # the unknown constant c
        rows.append((r, 0 if pf_sign(m) == 1 else 1))
    # gaussian elimination over GF(2)
    A = [r[:] + [b] for r, b in rows]
    piv = []
    rr = 0
    for c in range(ncol):
        sel = None
        for i in range(rr, len(A)):
            if A[i][c]:
                sel = i
                break
        if sel is None:
            continue
        A[rr], A[sel] = A[sel], A[rr]
        for i in range(len(A)):
            if i != rr and A[i][c]:
                A[i] = [x ^ y for x, y in zip(A[i], A[rr])]
        piv.append(c)
        rr += 1
    for i in range(rr, len(A)):
        if A[i][ncol]:
            return None, None                 # inconsistent: not Pfaffian
    sol = [0] * ncol
    for i, c in enumerate(piv):
        sol[c] = A[i][ncol]
    eps = {e: (-1 if sol[ids[e]] else 1) for e in gam}
    common = -1 if sol[len(gam)] else 1
    return eps, common


def smat(blocks, gam, eps, w):
    """the signed antisymmetric matrix S(w)."""
    S = [[Fraction(0)] * N for _ in range(N)]
    for (u, v) in gam:
        x = eps[(u, v)] * blocks[(u, v)][w[u]][w[v]]
        S[u][v] = x
        S[v][u] = -x
    return S


# ------------------------------------------------- site-linearity (W20-L)
def neighbours(gam, t):
    return sorted(s for e in gam for s in e if t in e and s != t)


def coeff_vector(blocks, gam, t, w):
    """C^t_s(w) = haf(Gamma - t - s)(w), s in N(t)  (W20-L coefficients)."""
    ES = set(gam)
    out = []
    for s in neighbours(gam, t):
        vs = [v for v in range(N) if v != t and v != s]
        out.append(haf_verts(blocks, ES, vs, w))
    return out


def site_matrix(blocks, gam, t, p):
    """B(p)[c][i] = A_{t s_i}[c][p_i]  (3 x deg t)."""
    nb = neighbours(gam, t)
    B = []
    for c in range(3):
        row = []
        for i, s in enumerate(nb):
            e = (min(t, s), max(t, s))
            row.append(blocks[e][c][p[i]] if e[0] == t else blocks[e][p[i]][c])
        B.append(row)
    return B


def site_columns(blocks, gam, t):
    """the 3*deg(t) column vectors a_{s,d} in C^3 at site t."""
    nb = neighbours(gam, t)
    cols = {}
    for s in nb:
        e = (min(t, s), max(t, s))
        for d in range(3):
            cols[(s, d)] = [blocks[e][c][d] if e[0] == t else blocks[e][d][c]
                            for c in range(3)]
    return nb, cols


def proportional(u, v):
    for i in range(len(u)):
        for j in range(i + 1, len(u)):
            if u[i] * v[j] - u[j] * v[i]:
                return False
    return True


def factors_at(blocks, gam, t):
    """site t factors: every Gamma block at t is rank one with the SAME
    t-side vector.  Equivalently all 3*deg(t) columns are proportional."""
    nb, cols = site_columns(blocks, gam, t)
    ks = list(cols)
    base = None
    for k in ks:
        if any(cols[k]):
            base = cols[k]
            break
    if base is None:
        return True
    return all(proportional(base, cols[k]) for k in ks)
