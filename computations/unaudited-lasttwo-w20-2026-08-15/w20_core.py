#!/usr/bin/env python3
"""UNAUDITED PROBE (W20) -- the last two N=8 residuals.

Pinned HEAD: see PINNED_HEAD.txt.  Nothing here is a proved claim of the
repository.  Every verdict uses exact arithmetic (Python int / Fraction /
exact sparse polynomials / Singular over Q).  NO FLOATS anywhere.

INDEPENDENT RE-IMPLEMENTATION of the N=8 model, written from the definition.
w20_controls.py cross-checks it against W19's stored numbers and against
W19's own engine, so agreement is a genuine control.

MODEL.  N = 8 sites, each C^3.  One 3x3 block A_uv per edge u<v of K_8;
row index = colour at u, column index = colour at v.  For w in {0,1,2}^8

    H_w(A) = sum_{M a perfect matching of K_8} prod_{uv in M} A_uv[w_u][w_v]

EXACT SOURCE with template T: all cells occupied by T nonzero, all others
zero, H_w = 0 on all 6558 mixed words, H_w != 0 on the three constants.

TEMPLATE ENCODING (same as W8/W15/W16/W19 so stored templates load):
T[e] a 9-bit mask, bit 3*i+j set <=> cell (i,j) occupied; e indexes
combinations(range(8),2) lexicographically.

VOCABULARY.
  Gamma(T)           the graph of FULL (nine-cell) blocks.
  F(Gamma)           perfect matchings of K_8 inside Gamma; supported at
                     EVERY word (all their cells are occupied).
  Phi_w              sum over F(Gamma) of the matching monomial at w.
  extras(w)          supported matchings NOT inside Gamma;  k(w) = #extras.
  effectively clean  k(w) = 0, i.e. H_w == Phi_w.
  site t factors     every Gamma-block at t is rank one with the SAME
                     t-side vector.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

N = 8
Q = 3
FULL = 511

EDGES = tuple(combinations(range(N), 2))
NE = len(EDGES)
EIDX = {e: i for i, e in enumerate(EDGES)}


def _perfect_matchings(vs):
    """all perfect matchings of the complete graph on the vertex list vs."""
    if not vs:
        return [()]
    a, rest = vs[0], vs[1:]
    out = []
    for i, b in enumerate(rest):
        sub = rest[:i] + rest[i + 1:]
        for m in _perfect_matchings(sub):
            out.append(((a, b),) + m)
    return out


PMS = tuple(tuple(sorted(m)) for m in _perfect_matchings(tuple(range(N))))
PM_E = tuple(tuple(EIDX[e] for e in m) for m in PMS)
assert len(PMS) == 105, len(PMS)

WORDS = tuple(product(range(Q), repeat=N))
CONSTS = tuple((c,) * N for c in range(Q))
MIXED = tuple(w for w in WORDS if len(set(w)) > 1)
assert len(WORDS) == 6561 and len(MIXED) == 6558


def cell_index(ei, w):
    u, v = EDGES[ei]
    return 3 * w[u] + w[v]


def support(T, w):
    """indices of perfect matchings all of whose cells are occupied at w."""
    return [mi for mi, es in enumerate(PM_E)
            if all((T[e] >> cell_index(e, w)) & 1 for e in es)]


def gamma_edges(T):
    return [EDGES[i] for i, t in enumerate(T) if t == FULL]


def pms_inside(edgeset):
    S = set(tuple(sorted(e)) for e in edgeset)
    return [mi for mi, m in enumerate(PMS) if all(e in S for e in m)]


def full_pm_indices(T):
    return pms_inside(gamma_edges(T))


def extras_at(T, w, fullm=None):
    fs = set(full_pm_indices(T) if fullm is None else fullm)
    return [mi for mi in support(T, w) if mi not in fs]


def k_of(T, w, fullm=None):
    return len(extras_at(T, w, fullm))


def effectively_clean(T, w, fullm=None):
    return not extras_at(T, w, fullm)


# ------------------------------------------------------------ admissibility
def spanning_2connected(edges, n=N):
    vs = set()
    for u, v in edges:
        vs.add(u)
        vs.add(v)
    if vs != set(range(n)):
        return False
    adj = {v: set() for v in range(n)}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    def connected(skip):
        keep = [v for v in range(n) if v != skip]
        if not keep:
            return True
        st, seen = [keep[0]], {keep[0]}
        while st:
            a = st.pop()
            for b in adj[a]:
                if b != skip and b not in seen:
                    seen.add(b)
                    st.append(b)
        return len(seen) == len(keep)

    return connected(-1) and all(connected(s) for s in range(n))


def cells_of(mask):
    return [(c // 3, c % 3) for c in range(9) if (mask >> c) & 1]


def block_class(mask):
    if mask == 0:
        return "zero"
    cs = cells_of(mask)
    if len(cs) == 1:
        return "single"
    if mask == FULL:
        return "full"
    rows = {i for i, _ in cs}
    cols = {j for _, j in cs}
    return "thin" if (len(rows) == 1 or len(cols) == 1) else "fat"


def forced_far_colour(mask, p_is_first):
    """the colour forced at the FAR endpoint, if unique (else None)."""
    if not mask:
        return None
    seen = {(j if p_is_first else i) for i, j in cells_of(mask)}
    return seen.pop() if len(seen) == 1 else None


def sc_ok(T):
    for p in range(N):
        need = set(range(Q))
        for ei, (u, v) in enumerate(EDGES):
            if p != u and p != v:
                continue
            r = forced_far_colour(T[ei], p_is_first=(u == p))
            if r is not None:
                need.discard(r)
        if need:
            return False
    return True


def in_R(T):
    if not sc_ok(T):
        return False
    if not all(support(T, w) for w in CONSTS):
        return False
    if not spanning_2connected(gamma_edges(T)):
        return False
    return all(len(support(T, w)) >= 3 for w in MIXED)


def audit(T):
    ge = gamma_edges(T)
    fib = [len(support(T, w)) for w in WORDS]
    mixedfib = [len(support(T, w)) for w in MIXED]
    cls = {}
    for t in T:
        cls[block_class(t)] = cls.get(block_class(t), 0) + 1
    return dict(m=sum(1 for t in T if t),
                sigma=sum(bin(t).count("1") for t in T),
                n_gamma=len(ge), gamma=[list(e) for e in ge],
                n_F=len(pms_inside(ge)),
                gamma_span2conn=spanning_2connected(ge),
                min_mixed_fibre=min(mixedfib), max_mixed_fibre=max(mixedfib),
                min_const_fibre=min(len(support(T, w)) for w in CONSTS),
                sc=sc_ok(T), classes=cls, in_R=in_R(T),
                n_eff_clean=sum(1 for w in MIXED
                                if effectively_clean(T, w, pms_inside(ge))),
                total_fibre=sum(fib))


# ------------------------------------------- exact sparse polynomials -------
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
    """one variable per OCCUPIED cell of the template."""

    def __init__(self, T):
        self.T = tuple(T)
        self.ids = {}
        self.names = []
        for e in range(NE):
            for c in range(9):
                if (T[e] >> c) & 1:
                    self.ids[(e, c)] = len(self.names)
                    u, v = EDGES[e]
                    self.names.append("A%d%d_%d%d" % (u, v, c // 3, c % 3))

    def v(self, ei, c):
        return self.ids[(ei, c)]

    def name(self, i):
        return self.names[i]

    def __len__(self):
        return len(self.names)


def monomial_of(vm, mi, w):
    return tuple(sorted(vm.v(e, cell_index(e, w)) for e in PM_E[mi]))


def H_poly(T, vm, w):
    o = {}
    for mi in support(T, w):
        m = monomial_of(vm, mi, w)
        o[m] = o.get(m, Fraction(0)) + 1
    return o


def phi_poly(T, vm, w, fullm=None):
    if fullm is None:
        fullm = full_pm_indices(T)
    o = {}
    for mi in fullm:
        m = monomial_of(vm, mi, w)
        o[m] = o.get(m, Fraction(0)) + 1
    return o


# ---------------------------------------------------- numeric evaluation ---
def H_value(blocks, T, w):
    tot = Fraction(0)
    for mi in support(T, w):
        p = Fraction(1)
        for u, v in PMS[mi]:
            p *= blocks[(u, v)][w[u]][w[v]]
        tot += p
    return tot


def phi_value(blocks, fullm, w):
    tot = Fraction(0)
    for mi in fullm:
        p = Fraction(1)
        for u, v in PMS[mi]:
            p *= blocks[(u, v)][w[u]][w[v]]
        tot += p
    return tot


def rank_of(M):
    M = [[Fraction(x) for x in row] for row in M]
    r, nr, nc = 0, len(M), len(M[0]) if M else 0
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
    cols = []
    for (u, v) in gam:
        if u == t:
            cols += [[blocks[(u, v)][i][j] for i in range(3)]
                     for j in range(3)]
        elif v == t:
            cols += [[blocks[(u, v)][j][i] for i in range(3)]
                     for j in range(3)]
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

# W19's explicit |Gamma| = 8 (Gamma = C_8) member of (R): m = 28, Sigma = 148,
# |F(Gamma)| = 2, min mixed fibre 6, ZERO effectively-clean words.
# (census/results_low.json, stratum_i_members[0]["template"])
C8_MEMBER = [1, 16, 256, 511, 511, 503, 447, 256, 16, 510, 495, 511, 511, 1,
             383, 511, 510, 511, 511, 255, 511, 383, 1, 16, 256, 256, 16, 1]
