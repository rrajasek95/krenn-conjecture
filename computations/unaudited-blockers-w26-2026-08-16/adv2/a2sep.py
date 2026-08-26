#!/usr/bin/env python3
"""adv2 -- the SEPARABILITY LADDER framework.  UNAUDITED.  EXACT ONLY.

A vertex v is SEPARABLE when every Gamma block at v is constant in v's own
index (this is the gauge-fixed form of A_uv = tau_v (x) B; the gauge
A_uv[a][b] -> t_u(a) t_v(b) A_uv[a][b] multiplies H_w by prod_v t_v(w_v)
and therefore preserves the whole problem).  If S is separable, Phi does
not depend on the letters at S.

Each vertex has a DEACTIVATING letter c_v that switches off every single
at v:   c_0 in {1,2}, c_1 = 2, c_2 = 0, c_3 in {0,1},
        c_4 in {1,2}, c_5 = 2, c_6 = 0, c_7 in {0,1}.
So if S covers every single edge then Phi vanishes identically.  The
"ladder" is indexed by T = V - S:  the singles that can possibly survive
are exactly the singles with BOTH endpoints in T.

  |T|=3, T={1,2,6}: 2 singles  (the previous lane's record)
  |T|=4, T={1,2,5,6}: 3 singles          -> secondary target S1
  |T|=5 ... |T|=8 (S empty): all 12      -> the PRIMARY target

With z supported on the T-singles, H_w depends only on the T-letters, so
the whole system collapses to 3^|T| equations at the representative words
w(tau) = tau on T, deactivating letters on S.

KEY LINEARITY (used by every solver here): for a vertex t, every perfect
matching uses exactly one edge at t, so H_w is LINEAR HOMOGENEOUS in
   {cells of the Gamma blocks at t} u {z_e : e a single at t}
with everything else held fixed.
"""
from __future__ import annotations

import os
import random
import sys
from fractions import Fraction
from itertools import combinations

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a2lib as A                                                 # noqa: E402
import w26_core as C                                              # noqa: E402

F = Fraction
DEACT = {0: (1, 2), 1: (2,), 2: (0,), 3: (0, 1),
         4: (1, 2), 5: (2,), 6: (0,), 7: (0, 1)}


class Sep:
    """the S-separable ansatz at level m."""

    def __init__(self, m, S):
        self.m = m
        self.S = tuple(sorted(S))
        self.T = tuple(v for v in range(8) if v not in self.S)
        self.G = A.Geo(m)
        self.gam = list(self.G.gam)
        self.sing = self.G.sing
        self.live = list(self.G.live)
        # singles with BOTH endpoints in T
        self.tsing = [e for e in self.live
                      if e[0] in self.T and e[1] in self.T]
        # parameter slots: (edge, a', b') with -1 for a collapsed index
        self.params = []
        for e in self.gam:
            u, v = e
            for a in ([-1] if u in self.S else [0, 1, 2]):
                for b in ([-1] if v in self.S else [0, 1, 2]):
                    self.params.append((e, a, b))
        self.pidx = {k: i for i, k in enumerate(self.params)}
        self.by_edge = {}
        for k in self.params:
            self.by_edge.setdefault(k[0], []).append(k)
        # representative words
        self.reps = []
        for tau in _tuples(len(self.T)):
            w = [0] * 8
            for i, v in enumerate(self.T):
                w[v] = tau[i]
            for v in self.S:
                w[v] = DEACT[v][0]
            self.reps.append(tuple(w))
        assert len(set(self.reps)) == 3 ** len(self.T)

    # ---------------------------------------------------------- expansion
    def blocks(self, th):
        bl = {}
        for e in self.gam:
            u, v = e
            M = [[None] * 3 for _ in range(3)]
            for a in range(3):
                for b in range(3):
                    k = (e, -1 if u in self.S else a, -1 if v in self.S else b)
                    M[a][b] = th[self.pidx[k]]
            bl[e] = M
        return bl

    def cells_of(self, k):
        e, a, b = k
        u, v = e
        aa = range(3) if a == -1 else [a]
        bb = range(3) if b == -1 else [b]
        return [(i, j) for i in aa for j in bb]

    def rand_theta(self, rng, lo=-6, hi=6):
        return [F(rng.randint(lo, hi) or 3, rng.randint(1, 3))
                for _ in self.params]

    # ------------------------------------------------------- full hafnian
    def hafM(self, bl, z, w, verts):
        """hafnian of the FULL matrix M(w) (Gamma cells + active singles)
        restricted to `verts`."""
        verts = tuple(sorted(verts))
        if not verts:
            return F(1)
        a = verts[0]
        tot = F(0)
        for i in range(1, len(verts)):
            b = verts[i]
            e = (a, b) if a < b else (b, a)
            if e in self.G.gs:
                c = bl[e][w[e[0]]][w[e[1]]]
            elif e in self.sing and (w[e[0]], w[e[1]]) == self.sing[e]:
                c = z.get(e, F(0))
            else:
                continue
            if c == 0:
                continue
            tot += c * self.hafM(bl, z, w, verts[1:i] + verts[i + 1:])
        return tot

    def H(self, bl, z, w):
        return self.hafM(bl, z, w, tuple(range(8)))

    # ---------------------------------------------- the site linear system
    def site_unknowns(self, t):
        pk = [k for k in self.params if t in k[0]]
        zk = [e for e in self.tsing if t in e]
        return pk, zk

    def site_matrix(self, bl, z, t, words):
        """rows: H_w as a linear form in (site params, site z's).

        Each perfect matching uses vertex t exactly once, so
            H_w = sum_{u != t} M(w)[t][u] * haf(M(w) - t - u)
        is linear homogeneous in these unknowns; haf(M - t - u) never
        involves vertex t, so it is computed once per (word, u)."""
        pk, zk = self.site_unknowns(t)
        pk_by_u = {}
        for i, k in enumerate(pk):
            e = k[0]
            u = e[0] if e[1] == t else e[1]
            pk_by_u.setdefault(u, []).append((i, k))
        n = len(pk) + len(zk)
        nbrs = sorted(set(pk_by_u) | {(e[0] if e[1] == t else e[1])
                                      for e in zk})
        rows = []
        for w in words:
            r = [F(0)] * n
            for u in nbrs:
                K = self.hafM(bl, z, w, tuple(x for x in range(8)
                                              if x != t and x != u))
                if K == 0:
                    continue
                for (i, k) in pk_by_u.get(u, ()):
                    if (w[k[0][0]], w[k[0][1]]) in self.cells_of(k):
                        r[i] += K
                for j, e in enumerate(zk):
                    if (e[0] if e[1] == t else e[1]) != u:
                        continue
                    if (w[e[0]], w[e[1]]) == self.sing[e]:
                        r[len(pk) + j] += K
            if any(r):
                rows.append(r)
        return pk, zk, rows

    def site_solve(self, th, z, t, rng, words=None, tries=600):
        """re-solve vertex t so that H = 0 at every representative word.
        Returns True on success (all new values nonzero)."""
        bl = self.blocks(th)
        words = self.reps if words is None else words
        pk, zk, rows = self.site_matrix(bl, z, t, words)
        n = len(pk) + len(zk)
        K = A.kernel_g(rows, n, F(0), F(1))
        if not K:
            return False
        for _ in range(tries):
            co = [F(rng.randint(-5, 5)) for _ in K]
            v = [sum(co[i] * K[i][j] for i in range(len(K))) for j in range(n)]
            if all(x != 0 for x in v):
                for i, k in enumerate(pk):
                    th[self.pidx[k]] = v[i]
                for j, e in enumerate(zk):
                    z[e] = v[len(pk) + j]
                return True
        return False

    # ------------------------------------------------------------ verdict
    def defect(self, th, z):
        bl = self.blocks(th)
        return sum(1 for w in self.reps if self.H(bl, z, w) != 0)

    def full_defect(self, th, z):
        """H over ALL 6558 mixed words, straight from C.H_word."""
        bl = self.blocks(th)
        T = C.TEMPLATES[self.m]
        zz = {e: z.get(e, F(0)) for e in C.single_edges(T)}
        bad = [w for w in C.MIXED if C.H_word(bl, T, zz, w) != 0]
        cons = [C.H_word(bl, T, zz, (c,) * 8) for c in range(3)]
        return len(bad), (list(bad[0]) if bad else None), [str(x) for x in cons]


def _tuples(k):
    if k == 0:
        return [()]
    out = []
    for t in _tuples(k - 1):
        for c in range(3):
            out.append(t + (c,))
    return out
