#!/usr/bin/env python3
"""UNAUDITED PROBE (W16) -- residual family (R) endgame at N = 8.

Pinned HEAD: see PINNED_HEAD.txt.  Nothing here is a proved claim of the
repository.  Every verdict uses exact arithmetic (Python int / Fraction /
exact sparse polynomials / Singular over Q).  NO FLOATS anywhere.

INDEPENDENT RE-IMPLEMENTATION (written from the model definition, not
imported from W8/W12/W15), so that agreement with their stored numbers is
a genuine cross-check.

MODEL.  N = 8 sites, each C^3.  One 3x3 block A_uv per edge u<v of K_8;
row index = colour at u, column index = colour at v.  For w in {0,1,2}^8

    H_w(A) = sum_{M a perfect matching of K_8} prod_{uv in M} A_uv[w_u][w_v]

EXACT SOURCE with template T: all cells occupied by T nonzero, all others
zero, H_w = 0 on all 6558 mixed words, H_w != 0 on the three constants.
(W10-G no-slack: a feasible point of that system IS a counterexample.)

TEMPLATE ENCODING: T[e] a 9-bit mask, bit 3*i+j set <=> cell (i,j)
occupied; e indexes combinations(range(8),2) lexicographically.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

N = 8
Q = 3
FULL = 511                                  # (1<<9)-1

EDGES = tuple(combinations(range(N), 2))    # 28
EIDX = {e: i for i, e in enumerate(EDGES)}


def _pms(verts):
    if not verts:
        yield ()
        return
    a = verts[0]
    for i in range(1, len(verts)):
        b = verts[i]
        rest = verts[1:i] + verts[i + 1:]
        for tail in _pms(rest):
            yield ((a, b),) + tail


PMS = tuple(tuple(sorted(m)) for m in _pms(tuple(range(N))))     # 105
PM_E = tuple(tuple(EIDX[e] for e in m) for m in PMS)

WORDS = tuple(product(range(Q), repeat=N))
CONSTS = tuple(tuple([c] * N) for c in range(Q))
MIXED = tuple(w for w in WORDS if len(set(w)) > 1)


def cell(ei, w):
    u, v = EDGES[ei]
    return 3 * w[u] + w[v]


def occ(T, ei, c):
    return (T[ei] >> c) & 1


def support(T, w):
    """indices of perfect matchings supported at word w"""
    out = []
    for mi, es in enumerate(PM_E):
        good = True
        for e in es:
            if not (T[e] >> cell(e, w)) & 1:
                good = False
                break
        if good:
            out.append(mi)
    return out


def audit(T):
    m = sum(1 for t in T if t)
    sigma = sum(bin(t).count("1") for t in T)
    hist = {}
    for w in MIXED:
        s = len(support(T, w))
        hist[s] = hist.get(s, 0) + 1
    return dict(m=m, sigma=sigma, hist=hist,
                min_mixed=min(hist),
                consts=[len(support(T, w)) for w in CONSTS],
                full=[EDGES[i] for i, t in enumerate(T) if t == FULL],
                singles={EDGES[i]: t.bit_length() - 1
                         for i, t in enumerate(T)
                         if t and bin(t).count("1") == 1},
                other={EDGES[i]: t for i, t in enumerate(T)
                       if t and t != FULL and bin(t).count("1") != 1})


# ---------------------------------------------------------------- Gamma

def gamma_edges(T):
    return [EDGES[i] for i, t in enumerate(T) if t == FULL]


def spanning_2conn(edges, n=N):
    vs = set()
    for u, v in edges:
        vs.add(u); vs.add(v)
    if vs != set(range(n)):
        return False
    def conn(skip):
        adj = {v: [] for v in range(n) if v != skip}
        for u, v in edges:
            if u != skip and v != skip:
                adj[u].append(v); adj[v].append(u)
        if not adj:
            return False
        st = [next(iter(adj))]; seen = set(st)
        while st:
            a = st.pop()
            for b in adj[a]:
                if b not in seen:
                    seen.add(b); st.append(b)
        return len(seen) == len(adj)
    if not conn(-1):
        return False
    return all(conn(s) for s in range(n))


def pms_of_graph(edges, n=N):
    """perfect matchings of the graph with the given edge set"""
    E = set(tuple(sorted(e)) for e in edges)
    out = []
    for mi, m in enumerate(PMS):
        if all(tuple(sorted(e)) in E for e in m):
            out.append(mi)
    return out


# ------------------------------------------ exact sparse polynomials
# poly = dict: monomial (sorted tuple of int var ids, w/ repetition)
#              -> Fraction coefficient (nonzero)

def padd(a, b):
    o = dict(a)
    for m, c in b.items():
        n = o.get(m, Fraction(0)) + c
        if n:
            o[m] = n
        else:
            o.pop(m, None)
    return o


def psub(a, b):
    return padd(a, {m: -c for m, c in b.items()})


def pmul(a, b):
    o = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            m = tuple(sorted(ma + mb))
            n = o.get(m, Fraction(0)) + ca * cb
            if n:
                o[m] = n
            else:
                o.pop(m, None)
    return o


def pscale(a, c):
    c = Fraction(c)
    return {} if c == 0 else {m: v * c for m, v in a.items()}


def pmon(vars_, coef=1):
    return {tuple(sorted(vars_)): Fraction(coef)}


def peval(a, val):
    t = Fraction(0)
    for m, c in a.items():
        p = c
        for v in m:
            p *= val[v]
        t += p
    return t


class VarMap:
    def __init__(self, T):
        self.T = tuple(T)
        self.ids = {}
        self.names = []
        for e in range(len(EDGES)):
            for c in range(9):
                if (T[e] >> c) & 1:
                    self.ids[(e, c)] = len(self.names)
                    u, v = EDGES[e]
                    self.names.append("A%d%d_%d%d" % (u, v, c // 3, c % 3))

    def v(self, ei, c):
        return self.ids[(ei, c)]

    def __len__(self):
        return len(self.names)


def H_poly(T, vm, w):
    o = {}
    for mi in support(T, w):
        m = tuple(sorted(vm.v(e, cell(e, w)) for e in PM_E[mi]))
        o[m] = o.get(m, Fraction(0)) + 1
    return o


def H_monomials(T, vm, w):
    return [tuple(sorted(vm.v(e, cell(e, w)) for e in PM_E[mi]))
            for mi in support(T, w)]


# ------------------------------------------------- template family (R)
# W8's immunity templates, re-read from
# computations/unaudited-template-kill-w8-2026-08-15/results_immunity.json
# by w16_calib.py (which asserts equality with the copy below).

W8_IMMUNE = {
    20: [511, 0, 511, 1, 2, 4, 0, 511, 0, 0, 8, 16, 4, 511, 8, 0, 128, 32,
         64, 128, 0, 256, 511, 0, 511, 511, 0, 511],
    21: [511, 511, 511, 1, 2, 4, 0, 511, 0, 0, 8, 16, 4, 511, 8, 0, 128, 32,
         64, 128, 0, 256, 511, 0, 511, 511, 0, 511],
    22: [511, 511, 511, 1, 2, 4, 511, 511, 0, 0, 8, 16, 4, 511, 8, 0, 128,
         32, 64, 128, 0, 256, 511, 0, 511, 511, 0, 511],
    23: [511, 511, 511, 1, 2, 4, 511, 511, 511, 0, 8, 16, 4, 511, 8, 0, 128,
         32, 64, 128, 0, 256, 511, 0, 511, 511, 0, 511],
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


def singles(T):
    """edge index -> ((u,colour_u),(v,colour_v)) for single-cell blocks"""
    o = {}
    for e, t in enumerate(T):
        if t and bin(t).count("1") == 1:
            c = t.bit_length() - 1
            u, v = EDGES[e]
            o[e] = ((u, c // 3), (v, c % 3))
    return o


def word_clean(T, w, act=None):
    """no single-cell block is ACTIVE at w (its cell matches the word)"""
    if act is None:
        act = singles(T)
    for e, ((u, cu), (v, cv)) in act.items():
        if w[u] == cu and w[v] == cv:
            return False
    return True


def full_pm_indices(T):
    return [mi for mi, es in enumerate(PM_E) if all(T[e] == FULL for e in es)]


def phi_poly(T, vm, w, fullm=None):
    if fullm is None:
        fullm = full_pm_indices(T)
    o = {}
    for mi in fullm:
        m = tuple(sorted(vm.v(e, cell(e, w)) for e in PM_E[mi]))
        o[m] = o.get(m, Fraction(0)) + 1
    return o


def extras_at(T, w, fullm=None):
    if fullm is None:
        fullm = full_pm_indices(T)
    fs = set(fullm)
    return [mi for mi in support(T, w) if mi not in fs]


def effectively_clean(T, w, fullm=None):
    """fibre lies entirely inside F(Gamma): H_w == Phi_w"""
    return not extras_at(T, w, fullm)
