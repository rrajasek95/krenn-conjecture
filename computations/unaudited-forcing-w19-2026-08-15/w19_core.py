#!/usr/bin/env python3
"""UNAUDITED PROBE (W19) -- the forcing theorem + the (R) census at N = 8.

Pinned HEAD: see PINNED_HEAD.txt.  Nothing here is a proved claim of the
repository.  Every verdict uses exact arithmetic (Python int / Fraction /
exact sparse polynomials / Singular over Q).  NO FLOATS anywhere.

INDEPENDENT RE-IMPLEMENTATION written from the model definition (not
imported from W8/W15/W16); w19_controls.py cross-checks it against W16's
stored numbers, so agreement is a genuine control.

MODEL.  N = 8 sites, each C^3.  One 3x3 block A_uv per edge u<v of K_8;
row index = colour at u, column index = colour at v.  For w in {0,1,2}^8

    H_w(A) = sum_{M a perfect matching of K_8} prod_{uv in M} A_uv[w_u][w_v]

EXACT SOURCE with template T: all cells occupied by T nonzero, all others
zero, H_w = 0 on all 6558 mixed words, H_w != 0 on the three constants.

TEMPLATE ENCODING: T[e] a 9-bit mask, bit 3*i+j set <=> cell (i,j)
occupied; e indexes combinations(range(8),2) lexicographically.

VOCABULARY (this probe).
  Gamma(T)          the graph of FULL (nine-cell) blocks.
  F(Gamma)          the perfect matchings of K_8 lying inside Gamma;
                    every one of them is supported at EVERY word.
  Phi_w             sum over F(Gamma) of the matching monomial at w.
  extras(w)         supported matchings NOT inside Gamma.
  effectively clean  extras(w) = empty, i.e. H_w == Phi_w.
  clean layer       { Phi_w = 0 : w mixed and effectively clean }.
  site t factors    every Gamma-block at t is rank one with the SAME
                    t-side vector: A_ts[c][.] = gamma_c * u^{(s)}[.].
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

N = 8
Q = 3
FULL = 511

EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}


def _pm_rec(verts):
    if not verts:
        yield ()
        return
    a = verts[0]
    for i in range(1, len(verts)):
        b = verts[i]
        rest = verts[1:i] + verts[i + 1:]
        for tail in _pm_rec(rest):
            yield ((a, b),) + tail


PMS = tuple(tuple(sorted(m)) for m in _pm_rec(tuple(range(N))))
PM_E = tuple(tuple(EIDX[e] for e in m) for m in PMS)
assert len(PMS) == 105

WORDS = tuple(product(range(Q), repeat=N))
CONSTS = tuple((c,) * N for c in range(Q))
MIXED = tuple(w for w in WORDS if len(set(w)) > 1)
assert len(MIXED) == 6558


def cell(ei, w):
    u, v = EDGES[ei]
    return 3 * w[u] + w[v]


def support(T, w):
    out = []
    for mi, es in enumerate(PM_E):
        if all((T[e] >> cell(e, w)) & 1 for e in es):
            out.append(mi)
    return out


# --------------------------------------------------------------- Gamma ----

def gamma_edges(T):
    return [EDGES[i] for i, t in enumerate(T) if t == FULL]


def pms_inside(edgeset):
    E = set(tuple(sorted(e)) for e in edgeset)
    return [mi for mi, m in enumerate(PMS)
            if all(tuple(sorted(e)) in E for e in m)]


def full_pm_indices(T):
    return pms_inside(gamma_edges(T))


def extras_at(T, w, fullm=None):
    fs = set(full_pm_indices(T) if fullm is None else fullm)
    return [mi for mi in support(T, w) if mi not in fs]


def effectively_clean(T, w, fullm=None):
    return not extras_at(T, w, fullm)


def spanning_2conn(edges, n=N):
    vs = set()
    for u, v in edges:
        vs.add(u)
        vs.add(v)
    if vs != set(range(n)):
        return False

    def conn(skip):
        adj = {v: [] for v in range(n) if v != skip}
        for u, v in edges:
            if u != skip and v != skip:
                adj[u].append(v)
                adj[v].append(u)
        st = [next(iter(adj))]
        seen = set(st)
        while st:
            a = st.pop()
            for b in adj[a]:
                if b not in seen:
                    seen.add(b)
                    st.append(b)
        return len(seen) == len(adj)

    return conn(-1) and all(conn(s) for s in range(n))


# ------------------------------------------------- block taxonomy / (SC) ---

def cells_of(mask):
    return [(c // 3, c % 3) for c in range(9) if (mask >> c) & 1]


def block_class(mask):
    if mask == 0:
        return "zero"
    cs = cells_of(mask)
    if len(cs) == 1:
        return "single"
    rows = set(i for i, _ in cs)
    cols = set(j for _, j in cs)
    if mask == FULL:
        return "full"
    if len(rows) == 1 or len(cols) == 1:
        return "thin"
    return "fat"


def far_thin_colour(mask, at_second):
    """The unique colour seen at the far endpoint, if unique; else None.

    Block S_uv serves demand (u, r) iff every occupied cell of S_uv has
    far-colour r at v  (so that colour r at v is *forced* whenever the
    block is used from u)."""
    if not mask:
        return None
    seen = set(j if at_second else i for i, j in cells_of(mask))
    return seen.pop() if len(seen) == 1 else None


def sc_servers(T):
    out = {}
    for p in range(N):
        for r in range(Q):
            servers = []
            for ei, (u, v) in enumerate(EDGES):
                if p not in (u, v):
                    continue
                if far_thin_colour(T[ei], at_second=(u == p)) == r:
                    servers.append(ei)
            out[(p, r)] = servers
    return out


def sc_ok(T):
    return all(v for v in sc_servers(T).values())


def in_R(T):
    """(R): (SC)-admissible, 3 constant fibres nonempty, no mixed singleton,
    every mixed fibre >= 3, Gamma spanning 2-connected."""
    if not sc_ok(T):
        return False
    if not all(support(T, w) for w in CONSTS):
        return False
    ge = gamma_edges(T)
    if not spanning_2conn(ge):
        return False
    for w in MIXED:
        if len(support(T, w)) < 3:
            return False
    return True


# ------------------------------------------ exact sparse polynomials -------
# poly = dict monomial(sorted tuple of var ids) -> Fraction

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


def phi_poly(T, vm, w, fullm=None):
    if fullm is None:
        fullm = full_pm_indices(T)
    o = {}
    for mi in fullm:
        m = tuple(sorted(vm.v(e, cell(e, w)) for e in PM_E[mi]))
        o[m] = o.get(m, Fraction(0)) + 1
    return o


def H_poly(T, vm, w):
    o = {}
    for mi in support(T, w):
        m = tuple(sorted(vm.v(e, cell(e, w)) for e in PM_E[mi]))
        o[m] = o.get(m, Fraction(0)) + 1
    return o


# ---------------------------------------------------- numeric evaluation ---

def phi_value(blocks, fullm, w):
    """blocks: dict edge -> 3x3 list of Fractions (Gamma edges only)."""
    tot = Fraction(0)
    for mi in fullm:
        p = Fraction(1)
        for u, v in PMS[mi]:
            p *= blocks[(u, v)][w[u]][w[v]]
        tot += p
    return tot


def H_value(allblocks, T, w):
    tot = Fraction(0)
    for mi in support(T, w):
        p = Fraction(1)
        for u, v in PMS[mi]:
            p *= allblocks[(u, v)][w[u]][w[v]]
        tot += p
    return tot


# ------------------------------------------------- factoring-site predicate

def rank_of(M):
    M = [[Fraction(x) for x in row] for row in M]
    r = 0
    nr, nc = len(M), len(M[0])
    for c in range(nc):
        piv = None
        for i in range(r, nr):
            if M[i][c]:
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(nr):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
        if r == nr:
            break
    return r


def site_factors(blocks, gam, t):
    """all Gamma blocks at t rank one with a COMMON t-vector <=> the
    3 x (3*deg) matrix of t-columns has rank 1."""
    cols = []
    for (u, v) in gam:
        if u == t:
            for j in range(3):
                cols.append([blocks[(u, v)][i][j] for i in range(3)])
        elif v == t:
            for j in range(3):
                cols.append([blocks[(u, v)][j][i] for i in range(3)])
    if not cols:
        return False
    M = [[cols[k][i] for k in range(len(cols))] for i in range(3)]
    return rank_of(M) == 1


# ------------------------------------------------------- W8's (R) ladder ---
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
