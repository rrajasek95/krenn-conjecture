#!/usr/bin/env python3
"""A8 -- INDEPENDENT construction of the sigma-symmetric diagonal slice and of
the colour-0 free-site ideals.  Written from the definitions, not from W28.

SETTING (re-derived).  N = 8, solve site z = 7, background sites V' = {0..6}.
For a word w on the 8 sites,

    H_w = sum_{y in V'} A_{yz}[w_y][w_z] * C_y(w|V'),
    C_y(u) = sum over PMs of V' - y of prod B_uv[u_u][u_v].

Write x^{(c)}_{y,d} = A_{yz}[d][c].  The colour-c system is LINEAR:

    sum_y x^{(c)}_{y, u_y} C_y(u) = [u == c const]      (u a word on V')

DIAGONAL BACKGROUND: B_uv = diag(t^0_uv, t^1_uv, t^2_uv), so
    C_y(u) = prod_c haf(t^c | S_c(u) - y),   S_c(u) = u^{-1}(c) inside V'.
Nonzero forces |S_d| odd for the colour d = u_y and |S_c| even for c != d.
Since |V'| = 7 is odd, either exactly one class is odd (then only the sites of
that class contribute) or all three are (then NO site contributes and the
equation is 0 = 0, because the constant word has one odd class).  Hence the
21 unknowns of one colour system SPLIT into three blocks of 7 indexed by d
[this is W28-DEC], and the inhomogeneous equation (u == 0) sits in the d = 0
block, so colour-0 feasibility <=> that 7-unknown block is consistent.

Writing x_y := x^{(0)}_{y,0}, P(S1,S2) := haf(t^1|S1) haf(t^2|S2), and
q(S0) := sum_{y in S0} haf(t^0|S0 - y) x_y, the block is

    q(V')                = 1                                   (constant word)
    P(S1,S2) * q(S0)     = 0    for every partition V' = S0+S1+S2 with |S0|
                                odd < 7, |S1|,|S2| even, and the 8-word
                                (0 on S0 and z, 1 on S1, 2 on S2) of
                                off-count <= k.

|S0| = 1 gives P(S1,S2) x_y = 0: y is FREE iff every even split of V' - y has
P = 0.  q(V') = 1 needs some x_y != 0, hence a nonempty free set [W28-FREE].
"""
from __future__ import annotations

from itertools import combinations, product

NS = 7
VP = tuple(range(NS))
Z = 7
EP = [tuple(sorted(e)) for e in combinations(VP, 2)]


# ------------------------------------------------------------ sparse polys

class P:
    """Sparse polynomial over Z: dict {exponent tuple: int}."""

    __slots__ = ("n", "t")

    def __init__(self, n, t=None):
        self.n = n
        self.t = {k: v for k, v in (t or {}).items() if v}

    @staticmethod
    def const(n, c):
        return P(n, {(0,) * n: c} if c else {})

    @staticmethod
    def var(n, i):
        e = [0] * n
        e[i] = 1
        return P(n, {tuple(e): 1})

    def __add__(self, o):
        t = dict(self.t)
        for k, v in o.t.items():
            t[k] = t.get(k, 0) + v
        return P(self.n, t)

    def __sub__(self, o):
        t = dict(self.t)
        for k, v in o.t.items():
            t[k] = t.get(k, 0) - v
        return P(self.n, t)

    def __mul__(self, o):
        t = {}
        for k1, v1 in self.t.items():
            for k2, v2 in o.t.items():
                k = tuple(a + b for a, b in zip(k1, k2))
                t[k] = t.get(k, 0) + v1 * v2
        return P(self.n, t)

    def __bool__(self):
        return bool(self.t)

    def deg(self):
        return max((sum(k) for k in self.t), default=-1)

    def evaluate(self, vals, mod=None):
        s = 0
        for k, v in self.t.items():
            m = v
            for i, e in enumerate(k):
                if e:
                    m *= vals[i] ** e
            s += m
        return s % mod if mod else s

    def to_singular(self, names):
        if not self.t:
            return "0"
        out = []
        for k in sorted(self.t, reverse=True):
            v = self.t[k]
            parts = [str(abs(v))] if abs(v) != 1 or all(e == 0 for e in k) else []
            for i, e in enumerate(k):
                if e == 1:
                    parts.append(names[i])
                elif e > 1:
                    parts.append(f"{names[i]}^{e}")
            out.append(("-" if v < 0 else "+") + "*".join(parts))
        s = "".join(out)
        return s[1:] if s[0] == "+" else s


# --------------------------------------------------- the sigma-slice params

SIGMA = {0: 1, 1: 2, 2: 0, 3: 4, 4: 5, 5: 3, 6: 6}
RHO = {0: 1, 1: 2, 2: 0}


def slice_orbits(sigma=SIGMA, rho=RHO):
    """Orbits of (colour, edge) under (c,e) -> (rho c, sigma e).  Returns
    (orbit list, index map {(c,e): orbit index})."""
    seen = {}
    orbits = []
    for c in range(3):
        for e in EP:
            if (c, e) in seen:
                continue
            orb = []
            cc, ee = c, e
            for _ in range(3):
                orb.append((cc, ee))
                cc, ee = rho[cc], tuple(sorted((sigma[ee[0]], sigma[ee[1]])))
            orb = sorted(set(orb))
            idx = len(orbits)
            for x in orb:
                seen[x] = idx
            orbits.append(orb)
    return orbits, seen


ORBITS, ORBIDX = slice_orbits()
NPAR = len(ORBITS)


def sym_t(names_only=False, nvar=None):
    """t[c][edge] as a polynomial in the orbit parameters."""
    nv = nvar if nvar is not None else NPAR
    t = [{}, {}, {}]
    for c in range(3):
        for e in EP:
            t[c][e] = P.var(nv, ORBIDX[(c, e)])
    return t


def full_t(nvar=None):
    """the UNRESTRICTED diagonal family: 63 independent parameters."""
    nv = nvar if nvar is not None else 63
    t = [{}, {}, {}]
    i = 0
    for c in range(3):
        for e in EP:
            t[c][e] = P.var(nv, i)
            i += 1
    return t


# --------------------------------------------------------------- hafnians

_PMC = {}


def pms(S):
    S = tuple(sorted(S))
    if S in _PMC:
        return _PMC[S]
    if len(S) % 2:
        r = []
    elif not S:
        r = [()]
    else:
        r = []
        u = S[0]
        for i in range(1, len(S)):
            v = S[i]
            sub = S[1:i] + S[i + 1:]
            for m in pms(sub):
                r.append(((u, v),) + m)
    _PMC[S] = r
    return r


def haf_poly(tc, S, nv):
    S = tuple(sorted(S))
    if len(S) % 2:
        return P.const(nv, 0)
    out = P.const(nv, 0)
    for m in pms(S):
        p = P.const(nv, 1)
        for e in m:
            p = p * tc[tuple(sorted(e))]
        out = out + p
    return out


def offcount8(w):
    return min(8 - w.count(g) for g in range(3))


def even_splits(W):
    out = []
    W = tuple(W)
    for m in range(0, len(W) + 1, 2):
        for S1 in combinations(W, m):
            out.append((S1, tuple(x for x in W if x not in S1)))
    return out


def word8(S1, S2):
    """the 8-word: colour 0 on S0 and on z, 1 on S1, 2 on S2."""
    w = [0] * 8
    for u in S1:
        w[u] = 1
    for u in S2:
        w[u] = 2
    return tuple(w)


def build_ideal(t, nv0, Y, kmax=4):
    """Generators of I_Y (colour-0, free set contains Y, x supported on Y).

    Variables: 0..nv0-1 the weight parameters, then |Y| star unknowns."""
    Y = tuple(sorted(Y))
    nv = nv0 + len(Y)
    pos = {y: nv0 + i for i, y in enumerate(Y)}

    def lift(p):
        return P(nv, {k + (0,) * len(Y): v for k, v in p.t.items()})

    cache = {}

    def hc(c, S):
        S = tuple(sorted(S))
        if (c, S) not in cache:
            cache[(c, S)] = lift(haf_poly(t[c], S, nv0))
        return cache[(c, S)]

    gens = []
    tags = []
    # FREE conditions
    for y in Y:
        W = tuple(x for x in VP if x != y)
        for (S1, S2) in even_splits(W):
            if offcount8(word8(S1, S2)) > kmax:
                continue
            g = hc(1, S1) * hc(2, S2)
            if g:
                gens.append(g)
                tags.append(("FREE", y, S1, S2))
    # MIXED conditions and the constant equation
    const_eq = None
    for s in range(1, NS + 1, 2):
        for S0 in combinations(VP, s):
            inY = [y for y in S0 if y in pos]
            T = tuple(x for x in VP if x not in S0)
            for (S1, S2) in even_splits(T):
                if offcount8(word8(S1, S2)) > kmax:
                    continue
                q = P.const(nv, 0)
                for y in inY:
                    q = q + hc(0, tuple(x for x in S0 if x != y)) * P.var(nv, pos[y])
                if s == NS:
                    const_eq = q - P.const(nv, 1)
                    continue
                if not q:
                    continue
                pp = hc(1, S1) * hc(2, S2)
                if not pp:
                    continue
                g = pp * q
                if g:
                    gens.append(g)
                    tags.append(("MIX", S0, S1, S2))
    assert const_eq is not None, "constant equation missing"
    return gens, tags, const_eq, nv
