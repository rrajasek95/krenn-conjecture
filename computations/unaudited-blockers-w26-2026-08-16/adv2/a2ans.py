#!/usr/bin/env python3
"""adv2 -- UNIFIED REFINEMENT ANSATZ.  UNAUDITED.  EXACT ONLY.

A point is described by a GROUPING: for each vertex v a partition
groups[v] of the alphabet {0,1,2}; every Gamma block is constant inside
each group.   groups[v] = [{0,1,2}]           -> v is SEPARABLE
                        = [{s},{0,1,2}-{s}]   -> v is "2-state"
                        = [{0},{1},{2}]       -> v is unconstrained.
The gauge A_uv[a][b] -> t_u(a)t_v(b)A_uv[a][b] multiplies H_w by
prod_v t_v(w_v), so "separable" is exactly the gauge-fixed form of
A_uv = tau_v (x) B and nothing is lost by writing it this way.

z_e may be nonzero only when BOTH endpoints of the single e have their
firing letter as a SINGLETON group; then H_w depends on w only through
the group pattern, and "H_w = 0 at all 6558 mixed words" is exactly
"H = 0 at every group pattern that has a mixed completion".

THE LADDER: refine one vertex at a time (1 -> 2 -> 3 states), switching
on the newly-legal z's.  Every refinement embeds the previous solution
(the new blocks are constant across the split), so the site system --
which is LINEAR HOMOGENEOUS in {blocks at t} u {z_e : t in e} because
every perfect matching uses vertex t exactly once -- always has the old
solution in its kernel.  The question at each rung is whether that
kernel is BIGGER than the old solution.
"""
from __future__ import annotations

import os
import sys
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a2lib as A                                                 # noqa: E402
import w26_core as C                                              # noqa: E402

F = Fraction
SEP = [frozenset({0, 1, 2})]


class QRing:
    """the default coefficient ring: Q."""
    name = "Q"
    zero = F(0)
    one = F(1)

    @staticmethod
    def rand(rng, lo=-6, hi=6):
        return F(rng.randint(lo, hi) or 3, rng.randint(1, 3))

    @staticmethod
    def small(rng):
        return F(rng.randint(-6, 6))


class ExtRing:
    """Q(omega) = Q[t]/(t^2+t+1) or Q(i) = Q[t]/(t^2+1), exact."""

    def __init__(self, cls, name):
        self.cls = cls
        self.name = name
        self.zero = cls(0, 0)
        self.one = cls(1, 0)

    def rand(self, rng, lo=-4, hi=4):
        while True:
            x = self.cls(rng.randint(lo, hi), rng.randint(lo, hi))
            if x != self.zero:
                return x

    def small(self, rng):
        return self.cls(rng.randint(-3, 3), rng.randint(-3, 3))


class FpRing:
    """F_p, exact (HEURISTIC ONLY -- a hit over F_p is not a hit over Q)."""

    def __init__(self, p):
        self.p = p
        self.name = "F_%d" % p
        self.zero = None
        self.one = None

    def _mk(self):
        import adv_lib as _AL
        self.zero = _AL.Fp(0, self.p)
        self.one = _AL.Fp(1, self.p)

    def rand(self, rng, lo=None, hi=None):
        import adv_lib as _AL
        return _AL.Fp(rng.randrange(1, self.p), self.p)

    def small(self, rng):
        import adv_lib as _AL
        return _AL.Fp(rng.randrange(self.p), self.p)
FULL = [frozenset({0}), frozenset({1}), frozenset({2})]


def two(s):
    return [frozenset({s}), frozenset({0, 1, 2} - {s})]


class Ans:
    def __init__(self, m, groups, ring=None):
        self.m = m
        self.R = ring or QRing
        self.groups = [list(g) for g in groups]
        self.G = A.Geo(m)
        self.gam = list(self.G.gam)
        self.sing = self.G.sing
        self.live = list(self.G.live)
        self.gi = []                       # gi[v][letter] = group index
        for v in range(8):
            d = {}
            for i, g in enumerate(self.groups[v]):
                for c in g:
                    d[c] = i
            assert len(d) == 3, groups[v]
            self.gi.append(d)
        self.params = []
        for e in self.gam:
            u, v = e
            for i in range(len(self.groups[u])):
                for j in range(len(self.groups[v])):
                    self.params.append((e, i, j))
        self.pidx = {k: i for i, k in enumerate(self.params)}
        # singles whose z may be switched on
        self.tsing = []
        for e in self.live:
            a, b = self.sing[e]
            if (self.groups[e[0]][self.gi[e[0]][a]] == frozenset({a})
                    and self.groups[e[1]][self.gi[e[1]][b]] == frozenset({b})):
                self.tsing.append(e)
        # representative words, one per group pattern with a mixed word
        self.reps = []
        for pat in product(*[range(len(g)) for g in self.groups]):
            gg = [sorted(self.groups[v][pat[v]]) for v in range(8)]
            if all(len(x) == 1 for x in gg) and len({x[0] for x in gg}) == 1:
                continue                       # only constant words: skip
            w = tuple(g[0] for g in gg)
            if len(set(w)) == 1:               # pick a mixed representative
                v0 = max(range(8), key=lambda v: len(gg[v]))
                w = tuple(gg[v][-1] if v == v0 else gg[v][0]
                          for v in range(8))
            assert len(set(w)) > 1, (pat, w)
            self.reps.append(w)

    # ------------------------------------------------------------- blocks
    def blocks(self, th):
        bl = {}
        for e in self.gam:
            u, v = e
            bl[e] = [[th[self.pidx[(e, self.gi[u][a], self.gi[v][b])]]
                      for b in range(3)] for a in range(3)]
        return bl

    def rand_theta(self, rng, lo=-6, hi=6):
        return [self.R.rand(rng) for _ in self.params]

    # ------------------------------------------------------------ hafnian
    def hafM(self, bl, z, w, verts):
        if not verts:
            return self.R.one
        a = verts[0]
        tot = self.R.zero
        for i in range(1, len(verts)):
            b = verts[i]
            e = (a, b) if a < b else (b, a)
            if e in self.G.gs:
                c = bl[e][w[e[0]]][w[e[1]]]
            elif e in self.sing and (w[e[0]], w[e[1]]) == self.sing[e]:
                c = z.get(e, self.R.zero)
            else:
                continue
            if c == 0:
                continue
            tot += c * self.hafM(bl, z, w, verts[1:i] + verts[i + 1:])
        return tot

    def H(self, bl, z, w):
        return self.hafM(bl, z, w, tuple(range(8)))

    def defect(self, th, z):
        bl = self.blocks(th)
        return sum(1 for w in self.reps if self.H(bl, z, w) != 0)

    def bad_reps(self, th, z):
        bl = self.blocks(th)
        return [w for w in self.reps if self.H(bl, z, w) != 0]

    # -------------------------------------------------------- site solving
    def site_unknowns(self, t):
        pk = [k for k in self.params if t in k[0]]
        zk = [e for e in self.tsing if t in e]
        return pk, zk

    def site_matrix(self, bl, z, t, words):
        pk, zk = self.site_unknowns(t)
        by_u = {}
        for i, k in enumerate(pk):
            e = k[0]
            u = e[0] if e[1] == t else e[1]
            by_u.setdefault(u, []).append((i, k))
        n = len(pk) + len(zk)
        nbrs = sorted(set(by_u) | {(e[0] if e[1] == t else e[1])
                                   for e in zk})
        rows = []
        for w in words:
            r = [self.R.zero] * n
            for u in nbrs:
                K = self.hafM(bl, z, w, tuple(x for x in range(8)
                                              if x != t and x != u))
                if K == 0:
                    continue
                for (i, k) in by_u.get(u, ()):
                    e = k[0]
                    if (self.gi[e[0]][w[e[0]]] == k[1]
                            and self.gi[e[1]][w[e[1]]] == k[2]):
                        r[i] += K
                for j, e in enumerate(zk):
                    if (e[0] if e[1] == t else e[1]) != u:
                        continue
                    if (w[e[0]], w[e[1]]) == self.sing[e]:
                        r[len(pk) + j] += K
            if any(r):
                rows.append(r)
        return pk, zk, rows

    def site_kernel(self, th, z, t):
        pk, zk, rows = self.site_matrix(self.blocks(th), z, t, self.reps)
        K = A.kernel_g(rows, len(pk) + len(zk), self.R.zero, self.R.one)
        return pk, zk, rows, K

    def write_site(self, th, z, t, pk, zk, v):
        for i, k in enumerate(pk):
            th[self.pidx[k]] = v[i]
        for j, e in enumerate(zk):
            z[e] = v[len(pk) + j]

    def site_solve(self, th, z, t, rng, tries=800, want=()):
        """pick a kernel vector with EVERY entry nonzero (so all Gamma
        cells and all site z's stay nonzero)."""
        pk, zk, rows, K = self.site_kernel(th, z, t)
        if not K:
            return False
        for _ in range(tries):
            co = [self.R.small(rng) for _ in K]
            v = [sum((co[i] * K[i][j] for i in range(len(K))), self.R.zero)
                 for j in range(len(pk) + len(zk))]
            if all(x != 0 for x in v):
                self.write_site(th, z, t, pk, zk, v)
                return True
        return False


def refine(an, th, z, v, newgroups):
    """carry a solution over to a finer grouping at vertex v."""
    g2 = [list(x) for x in an.groups]
    g2[v] = list(newgroups)
    an2 = Ans(an.m, g2, an.R)
    bl = an.blocks(th)
    th2 = [None] * len(an2.params)
    for k in an2.params:
        e, i, j = k
        a = sorted(an2.groups[e[0]][i])[0]
        b = sorted(an2.groups[e[1]][j])[0]
        th2[an2.pidx[k]] = bl[e][a][b]
    z2 = {e: z.get(e, an.R.zero) for e in an2.tsing}
    return an2, th2, z2
