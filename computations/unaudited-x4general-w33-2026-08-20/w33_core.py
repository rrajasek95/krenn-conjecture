#!/usr/bin/env python3
"""UNAUDITED PROBE W33 (Route B: general X_4-emptiness at N=8) -- core engine.

Pinned HEAD: see PINNED_HEAD.txt.  Exact arithmetic throughout (Fraction over
Q, own F_p); mod-p only ever as a screen with exact re-checks.

INDEPENDENT re-implementation.  Deliberately different code paths from
w32_core (explicit cached PM enumeration):
  * hafnians by a BITMASK SUBSET DP over vertex subsets (lowest set bit
    peeled), no matching lists ever materialised;
  * sources stored as a dict edge -> d x d tuple-of-lists, with the
    A_vu = A_uv^T convention read through cell();
  * the two engines are cross-checked against each other in run_01 on random
    sources over Q and over F_p (ledger 12/19: structured strata too).

SETTING (as in W32).  A d-colour source on K_N assigns to each edge {u,v}
(u<v) a d x d matrix A_uv, A_vu = A_uv^T.  For w in {0,..,d-1}^N,

    H_w(A) = sum_{M in PM(K_N)} prod_{{u,v} in M} A_uv[w_u][w_v] .

An EXACT d=2 source on K_N: H_w = 1 for the two constant words and H_w = 0
for all other w in {0,1}^N.  (W32-2COL: every 2-colour restriction of an X_4
point at N=8 is such a source; W32-RES: X_4 = three exact d=2 restrictions +
4116 trichromatic imposed words vanishing.)

GENERATING FORM.  Phi_A(xi) = haf(M(xi)), M(xi)_ij = xi_i^T A_ij xi_j.
Exactness = Phi_A(xi) = prod_i xi_i[0] + prod_i xi_i[1].
Dehomogenised (xi_i = (1, t_i)): haf(N(t)) = 1 + t_1...t_N with
N_ij(t) = a_ij + b_ij t_j + c_ij t_i + d_ij t_i t_j biaffine.

GAUGE.  The symmetry group of the exact-d=2 variety is
    G = T x Z_2 x S_N,   T = {(alpha,delta) in (C*)^N x (C*)^N :
                              prod alpha = prod delta = 1}   (dim 2N-2),
acting by  A_uv[a][b] -> g_u[a] A_uv[a][b] g_v[b]  (g_u = (alpha_u, delta_u)),
Z_2 = colour swap  A_uv[a][b] -> A_uv[1-a][1-b],  S_N = site relabelling.
Only these preserve the target polynomial, so cell supports, cross-cell
counts and kernel-dimension profiles are gauge INVARIANTS.
"""
from __future__ import annotations

import itertools
import os
import subprocess
import tempfile
from fractions import Fraction
from functools import lru_cache


def require(cond, detail):
    if not cond:
        raise AssertionError(detail)


# ------------------------------------------------------------------ fields

class Fp:
    """F_p element; p carried per element (two-primes discipline, ledger 19)."""

    __slots__ = ("v", "p")

    def __init__(self, v, p):
        self.v = int(v) % p
        self.p = p

    def __repr__(self):
        return f"Fp({self.v},{self.p})"

    def _c(self, o):
        return o if isinstance(o, Fp) else Fp(int(o), self.p)

    def __eq__(self, o):
        return (self.v == o.v) if isinstance(o, Fp) else (
            self.v == int(o) % self.p)

    def __hash__(self):
        return hash((self.v, self.p))

    def __bool__(self):
        return self.v != 0

    def __neg__(self):
        return Fp(-self.v, self.p)

    def __add__(self, o):
        return Fp(self.v + self._c(o).v, self.p)

    __radd__ = __add__

    def __sub__(self, o):
        return Fp(self.v - self._c(o).v, self.p)

    def __rsub__(self, o):
        return self._c(o) - self

    def __mul__(self, o):
        return Fp(self.v * self._c(o).v, self.p)

    __rmul__ = __mul__

    def inv(self):
        require(self.v % self.p != 0, "Fp inverse of 0")
        return Fp(pow(self.v, self.p - 2, self.p), self.p)

    def __truediv__(self, o):
        return self * self._c(o).inv()

    def __rtruediv__(self, o):
        return self._c(o) * self.inv()


def zero_like(x):
    return Fp(0, x.p) if isinstance(x, Fp) else Fraction(0)


def one_like(x):
    return Fp(1, x.p) if isinstance(x, Fp) else Fraction(1)


# ------------------------------------------------------------ combinatorics

def ekey(a, b):
    return (a, b) if a < b else (b, a)


def edges(n):
    return list(itertools.combinations(range(n), 2))


@lru_cache(maxsize=None)
def pm_list(mask):
    """All perfect matchings of the vertex set given by `mask` (bitmask), each
    a tuple of ekeys.  Only used by the CONTROL engine (haf_pm)."""
    if mask == 0:
        return ((),)
    lo = (mask & -mask).bit_length() - 1
    rest = mask & ~(1 << lo)
    out = []
    m = rest
    while m:
        b = m & -m
        v = b.bit_length() - 1
        m ^= b
        for M in pm_list(rest & ~b):
            out.append((ekey(lo, v),) + M)
    return tuple(out)


# ---------------------------------------------------------------- sources

def cell(src, u, v, a, b):
    if u < v:
        return src[(u, v)][a][b]
    return src[(v, u)][b][a]


def setcell(src, u, v, a, b, val):
    if u < v:
        src[(u, v)][a][b] = val
    else:
        src[(v, u)][b][a] = val


def zero_source(n, d=2, sample=None):
    z = Fraction(0) if sample is None else zero_like(sample)
    return {e: [[z] * d for _ in range(d)] for e in edges(n)}


def copy_source(src):
    return {e: [r[:] for r in m] for e, m in src.items()}


# ------------------------------------------------------ hafnian, engine A
# BITMASK SUBSET DP (peel the lowest set bit).  Independent of W32's cached
# explicit PM enumeration.

def haf_dp(src, word, mask, zz, oo):
    memo = {0: oo}

    def go(m):
        r = memo.get(m)
        if r is not None:
            return r
        lo = (m & -m).bit_length() - 1
        rest = m & ~(1 << lo)
        tot = zz
        mm = rest
        while mm:
            b = mm & -mm
            v = b.bit_length() - 1
            mm ^= b
            c = cell(src, lo, v, word[lo], word[v])
            if c != 0:
                sub = go(rest & ~b)
                if sub != 0:
                    tot = tot + c * sub
        memo[m] = tot
        return tot

    return go(mask)


def haf(src, word, sites=None, n=None, sample=None):
    """H_w over `sites` (default all n).  word: indexable by site."""
    if sample is None:
        sample = src[next(iter(src))][0][0]
    zz, oo = zero_like(sample), one_like(sample)
    if sites is None:
        require(n is not None, "haf: need n or sites")
        sites = range(n)
    mask = 0
    cnt = 0
    for s in sites:
        mask |= 1 << s
        cnt += 1
    if cnt % 2:
        return zz
    return haf_dp(src, word, mask, zz, oo)


# ------------------------------------------------------ hafnian, engine B
# explicit PM enumeration -- the CONTROL engine (cross-checked in run_01).

def haf_pm(src, word, sites=None, n=None, sample=None):
    if sample is None:
        sample = src[next(iter(src))][0][0]
    zz, oo = zero_like(sample), one_like(sample)
    if sites is None:
        sites = range(n)
    mask = 0
    for s in sites:
        mask |= 1 << s
    if bin(mask).count("1") % 2:
        return zz
    tot = zz
    for M in pm_list(mask):
        pr = oo
        for (u, v) in M:
            c = cell(src, u, v, word[u], word[v])
            if c == 0:
                pr = zz
                break
            pr = pr * c
        if pr != 0:
            tot = tot + pr
    return tot


# ------------------------------------------------------------ d=2 exactness

def words2(n):
    return list(itertools.product(range(2), repeat=n))


def is_exact2(src, n, engine=haf):
    """(bool, first bad word).  Exact d=2 source test."""
    sample = src[next(iter(src))][0][0]
    for w in words2(n):
        tgt = 1 if len(set(w)) == 1 else 0
        if engine(src, w, n=n, sample=sample) != tgt:
            return False, w
    return True, None


def defects2(src, n, engine=haf):
    sample = src[next(iter(src))][0][0]
    out = []
    for w in words2(n):
        tgt = 1 if len(set(w)) == 1 else 0
        v = engine(src, w, n=n, sample=sample)
        if v != tgt:
            out.append((w, v))
    return out


# --------------------------------------------------- star matrix at a site
# Rows u in {0,1}^{V-j}; columns (r, e) for r != j, e in {0,1}:
#     M[u][(r,e)] = [u_r = e] * haf(B | V - j - r, u).
# The SAME matrix governs (i) the d=2 completion of a background at j
# (inhomogeneous, per colour) and (ii) the third-colour star kernel Ker_j.

def star_matrix(src, j, n, sample=None):
    """Returns (cols, rows) with rows a list of (u, rowvector)."""
    if sample is None:
        sample = src[next(iter(src))][0][0]
    zz = zero_like(sample)
    VP = [x for x in range(n) if x != j]
    cols = [(r, e) for r in VP for e in range(2)]
    cidx = {c: i for i, c in enumerate(cols)}
    rows = []
    for u in itertools.product(range(2), repeat=n - 1):
        wd = {}
        for i, y in enumerate(VP):
            wd[y] = u[i]
        wd[j] = 0
        row = [zz] * len(cols)
        for i, r in enumerate(VP):
            S = [x for x in range(n) if x != j and x != r]
            row[cidx[(r, u[i])]] = haf(src, wd, sites=S, sample=sample)
        rows.append((u, row))
    return cols, rows


def rref(mat, rhs, ncols):
    """Exact RREF; returns (pivots, augmented matrix, consistent)."""
    m = [list(r) + [b] for r, b in zip(mat, rhs)]
    piv, rr = [], 0
    for c in range(ncols):
        p = None
        for i in range(rr, len(m)):
            if m[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        m[rr], m[p] = m[p], m[rr]
        x = m[rr][c]
        inv = x.inv() if hasattr(x, "inv") else Fraction(1) / x
        m[rr] = [y * inv for y in m[rr]]
        for i in range(len(m)):
            if i != rr and m[i][c] != 0:
                f = m[i][c]
                m[i] = [y - f * z for y, z in zip(m[i], m[rr])]
        piv.append(c)
        rr += 1
    ok = all(not (m[i][ncols] != 0 and all(x == 0 for x in m[i][:ncols]))
             for i in range(len(m)))
    return piv, m, ok


def nullspace(mat, ncols, sample):
    piv, m, _ = rref(mat, [zero_like(sample)] * len(mat), ncols)
    zz, oo = zero_like(sample), one_like(sample)
    basis = []
    for f in [c for c in range(ncols) if c not in piv]:
        v = [zz] * ncols
        v[f] = oo
        for i, c in enumerate(piv):
            v[c] = -m[i][f]
        basis.append(v)
    return basis, piv


def star_kernel(src, j, n, sample=None):
    """dim, basis, zero-columns of Ker_j (the homogeneous star system)."""
    if sample is None:
        sample = src[next(iter(src))][0][0]
    cols, rows = star_matrix(src, j, n, sample)
    mat = [r for _, r in rows if any(x != 0 for x in r)]
    basis, piv = nullspace(mat, len(cols), sample)
    zcols = [cols[i] for i in range(len(cols))
             if all(r[i] == 0 for _, r in rows)]
    return len(basis), basis, cols, zcols


def complete_site(src, j, n, sample=None):
    """Given src (whose star at j is ignored), solve the two inhomogeneous
    systems for the star at j making the source exact.  Returns
    (feasible, particular[c], kernel_basis, cols)."""
    if sample is None:
        sample = src[next(iter(src))][0][0]
    zz, oo = zero_like(sample), one_like(sample)
    cols, rows = star_matrix(src, j, n, sample)
    mat = [r for _, r in rows]
    part = {}
    for c in range(2):
        rhs = []
        for (u, _r) in rows:
            const = (len(set(u)) == 1 and u[0] == c)
            rhs.append(oo if const else zz)
        piv, m, ok = rref(mat, rhs, len(cols))
        if not ok:
            return False, None, None, cols
        sol = [zz] * len(cols)
        for i, cc in enumerate(piv):
            sol[cc] = m[i][len(cols)]
        part[c] = sol
    basis, _ = nullspace(mat, len(cols), sample)
    return True, part, basis, cols


def install_star(src, j, n, cols, vecs):
    """vecs[c] = coefficient vector over cols for colour c at site j."""
    for c in range(2):
        for i, (r, e) in enumerate(cols):
            setcell(src, j, r, c, e, vecs[c][i])
    return src


# ------------------------------------------------------- standard sources

def cycle_pm_pair(n, perm=None, wa=None, wd=None, sample=None):
    """Delta^2: the Hamiltonian-cycle / PM-pair diagonal source.
    Cycle perm[0]-perm[1]-...-perm[n-1]-perm[0]; even cycle edges carry
    colour 0 on the (0,0) cell, odd cycle edges colour 1 on (1,1)."""
    perm = list(range(n)) if perm is None else list(perm)
    src = zero_source(n, 2, sample)
    oo = Fraction(1) if sample is None else one_like(sample)
    for i in range(n):
        u, v = perm[i], perm[(i + 1) % n]
        a = 0 if i % 2 == 0 else 1
        w = oo
        if a == 0 and wa is not None:
            w = wa[i // 2]
        if a == 1 and wd is not None:
            w = wd[i // 2]
        setcell(src, u, v, a, a, w)
    return src


def support(src, tol=None):
    return sorted((e, a, b) for e, m in src.items()
                  for a in range(len(m)) for b in range(len(m))
                  if m[a][b] != 0)


def n_cross(src):
    return sum(1 for e, m in src.items() for a in range(len(m))
               for b in range(len(m)) if a != b and m[a][b] != 0)


# ------------------------------------------------------------------ gauge

def apply_perm(src, perm, n):
    """perm: site i -> perm[i]."""
    out = {}
    for (u, v), m in src.items():
        pu, pv = perm[u], perm[v]
        if pu < pv:
            out[(pu, pv)] = [r[:] for r in m]
        else:
            out[(pv, pu)] = [[m[a][b] for a in range(len(m))]
                             for b in range(len(m))]
    return out


def apply_swap(src):
    out = {}
    for e, m in src.items():
        d = len(m)
        out[e] = [[m[d - 1 - a][d - 1 - b] for b in range(d)]
                  for a in range(d)]
    return out


def apply_torus(src, alpha, delta):
    g = [(alpha[i], delta[i]) for i in range(len(alpha))]
    out = {}
    for (u, v), m in src.items():
        out[(u, v)] = [[g[u][a] * m[a][b] * g[v][b] for b in range(len(m))]
                       for a in range(len(m))]
    return out


def support_signature(src, n):
    """Canonical form of the SUPPORT under S_n x colour swap (exact, by
    brute force over the group).  Cheap invariants are computed first by
    callers; this is the exact test."""
    best = None
    sup0 = frozenset(support(src))
    for sw in range(2):
        s = apply_swap(src) if sw else src
        for perm in itertools.permutations(range(n)):
            t = apply_perm(s, perm, n)
            key = tuple(sorted((e[0], e[1], a, b) for (e, a, b) in support(t)))
            if best is None or key < best:
                best = key
    return best, len(sup0)


def cheap_invariants(src, n):
    """S_n x swap invariants that do not need the group: degree sequences."""
    sup = support(src)
    ncell = len(sup)
    ncr = sum(1 for (_e, a, b) in sup if a != b)
    deg = [0] * n
    for (e, _a, _b) in sup:
        deg[e[0]] += 1
        deg[e[1]] += 1
    ecells = {}
    for (e, a, b) in sup:
        ecells.setdefault(e, []).append((a, b))
    pat = {}
    for e, L in ecells.items():
        k1 = tuple(sorted(L))
        k2 = tuple(sorted(((1 - a, 1 - b) for (a, b) in L)))
        pat[e] = min(k1, k2)
    patct = {}
    for e, k in pat.items():
        patct[k] = patct.get(k, 0) + 1
    return {"ncell": ncell, "ncross": ncr, "deg": tuple(sorted(deg)),
            "patterns": tuple(sorted(patct.items()))}


# --------------------------------------------------------------- Singular

def run_singular(script, timeout=3600):
    """Ledger 6/11/14: RC 0 is not enough -- parse stdout for '?' lines."""
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write(script + "\nquit;\n")
        path = fh.name
    try:
        proc = subprocess.run(["Singular", "-q", "--no-warn", path],
                              capture_output=True, text=True, timeout=timeout)
    finally:
        os.unlink(path)
    out = proc.stdout
    bad = [ln for ln in out.splitlines() if ln.strip().startswith("?")]
    if proc.returncode != 0 or bad:
        raise RuntimeError(f"Singular rc={proc.returncode} bad={bad[:6]} "
                           f"stderr={proc.stderr[:1200]}")
    return out


def no_shadow_guard(script, ringvars):
    """Ledger 13: never name a generator after a ring variable; zz-prefix."""
    kws = ("poly ", "ideal ", "int ", "number ", "matrix ", "list ", "map ",
           "vector ", "def ", "intvec ", "string ", "module ")
    for ln in script.splitlines():
        t = ln.strip()
        for kw in kws:
            if t.startswith(kw):
                name = t[len(kw):].split("=")[0].split("(")[0].split(",")[0]
                name = name.strip().rstrip(";")
                if name in ringvars:
                    raise AssertionError(f"ledger-13 shadowing hazard: {ln}")
                if not name.startswith("zz") and name not in ("R", "r"):
                    raise AssertionError(f"ledger-13 zz-prefix rule: {ln}")
    return True


# -------------------------------------------------------------- manifests

class Manifest:
    """Ledger 21: a control file must fail loudly if a control never ran."""

    def __init__(self, declared):
        self.declared = list(declared)
        self.ran = []

    def mark(self, name):
        require(name in self.declared, f"undeclared control {name}")
        self.ran.append(name)

    def assert_complete(self):
        missing = [c for c in self.declared if c not in self.ran]
        require(not missing, f"CONTROLS NEVER RAN: {missing}")
        return {"declared": self.declared, "ran": self.ran, "complete": True}
