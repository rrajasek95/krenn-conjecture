#!/usr/bin/env python3
"""UNAUDITED PROBE W28 (the X_4-emptiness attacks) -- core engine.

Pinned HEAD: see PINNED_HEAD.txt.  All arithmetic exact (Fraction / Cyc =
Q(omega) / sparse polynomials / mod p as a SCREEN only).

INDEPENDENT re-implementations (deliberately different code paths from
w25_core and w27_core, which are imported ONLY for cross-checks):

  * hafnians by recursion on the LOWEST remaining site with a dict memo keyed
    by the frozen tuple of remaining sites (W25 uses a bitmask DP, W27 a PM
    enumeration);
  * Q(omega) as class Cyc (own arithmetic, cross-checked against w25_core.Om);
  * the X_k site systems at a site z built from scratch;
  * the diagonal-stratum conditions (A)/(B)/(C)/(D) at N = 8 built from the
    word definition, not from W27's combinatorial shortcuts.

THE REDUCTION USED THROUGHOUT (W27-R1, re-derived and re-verified here):
site-linearity  H_w = sum_{y != z} A_zy[w_z][w_y] Haf_{V-z-y}(A)_w  says that
membership in X_k is, at a fixed site z, three independent inhomogeneous linear
systems in the 3(N-1) star unknowns, whose coefficients depend only on the
BACKGROUND (the source restricted to V - z).  So

    X_k(N) nonempty  <=>  some background on K_{N-1} makes all three systems
                          consistent
                      <=>  for each colour c, r_const^(c) is NOT in the row
                           span of the mixed rows.

W28-SYM (the averaging lemma, proved in run_t1a): if the background is
invariant under a site group H acting transitively on V - z with TRIVIAL
colour action, then the colour-c system is feasible iff it has an H-invariant
solution; for H transitive that means x_{y,d} = x_d -- THREE unknowns.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from fractions import Fraction
from itertools import combinations, product

NCOL = 3


def require(cond, detail):
    if not cond:
        raise AssertionError(detail)


# ------------------------------------------------------------------ Q(omega)

class Cyc:
    """a + b*w, w^2 = -w - 1 (primitive cube root of unity).  Own arithmetic."""

    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = Fraction(a)
        self.b = Fraction(b)

    @staticmethod
    def of(x):
        return x if isinstance(x, Cyc) else Cyc(x, 0)

    def __repr__(self):
        return f"Cyc({self.a},{self.b})"

    def __eq__(self, o):
        if isinstance(o, Cyc):
            return self.a == o.a and self.b == o.b
        return self.b == 0 and self.a == Fraction(o)

    def __hash__(self):
        return hash((self.a, self.b))

    def __bool__(self):
        return bool(self.a) or bool(self.b)

    def __neg__(self):
        return Cyc(-self.a, -self.b)

    def __add__(self, o):
        o = Cyc.of(o)
        return Cyc(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __sub__(self, o):
        o = Cyc.of(o)
        return Cyc(self.a - o.a, self.b - o.b)

    def __rsub__(self, o):
        return Cyc.of(o) - self

    def __mul__(self, o):
        o = Cyc.of(o)
        # (a + b w)(c + d w) = ac + (ad + bc) w + bd w^2, w^2 = -1 - w
        a, b, c, d = self.a, self.b, o.a, o.b
        return Cyc(a * c - b * d, a * d + b * c - b * d)

    __rmul__ = __mul__

    def inv(self):
        n = self.a * self.a - self.a * self.b + self.b * self.b
        require(n != 0, "Cyc: division by zero")
        return Cyc((self.a - self.b) / n, -self.b / n)

    def __truediv__(self, o):
        return self * Cyc.of(o).inv()

    def __rtruediv__(self, o):
        return Cyc.of(o) * self.inv()


OMEGA = Cyc(0, 1)


def is_cyc(x):
    return isinstance(x, Cyc)


def zeroe(sample):
    return Cyc(0, 0) if is_cyc(sample) else Fraction(0)


def onee(sample):
    return Cyc(1, 0) if is_cyc(sample) else Fraction(1)


# ------------------------------------------------------------- sources / haf

def ekey(a, b):
    return (a, b) if a < b else (b, a)


def oriented(src, u, v, ncol=NCOL):
    if u < v:
        return src[(u, v)]
    m = src[(v, u)]
    return [[m[j][i] for j in range(ncol)] for i in range(ncol)]


def zero_source(n, ncol=NCOL, zero=None):
    z = Fraction(0) if zero is None else zero
    return {(a, b): [[z] * ncol for _ in range(ncol)]
            for a, b in combinations(range(n), 2)}


def copy_source(src):
    return {e: [r[:] for r in m] for e, m in src.items()}


def haf_rec(wt, sites, memo, one, zero):
    """Hafnian over `sites` (sorted tuple), recursion on the LOWEST site.

    Deliberately not W25's bitmask DP: the memo key is the tuple of remaining
    sites.  wt(i, j) is the (symmetric) edge weight."""
    if not sites:
        return one
    if len(sites) % 2:
        return zero
    v = memo.get(sites)
    if v is not None:
        return v
    head, rest = sites[0], sites[1:]
    tot = zero
    for k in range(len(rest)):
        w = wt(head, rest[k])
        if w == 0:
            continue
        sub = haf_rec(wt, rest[:k] + rest[k + 1:], memo, one, zero)
        if sub == 0:
            continue
        tot = tot + w * sub
    memo[sites] = tot
    return tot


def H_word(src, word, n, ncol=NCOL):
    """H_B(A)_w from the word definition."""
    sample = src[(0, 1)][0][0]

    def wt(i, j):
        return oriented(src, i, j, ncol)[word[i]][word[j]]

    return haf_rec(wt, tuple(range(n)), {}, onee(sample), zeroe(sample))


def haf_on(src, word, sites, ncol=NCOL):
    sample = src[(0, 1)][0][0]

    def wt(i, j):
        return oriented(src, i, j, ncol)[word[i]][word[j]]

    return haf_rec(wt, tuple(sorted(sites)), {}, onee(sample), zeroe(sample))


def haf_w(w, sites, zero=None, one=None):
    """Hafnian of a scalar edge-weight dict w[(a,b)] (a<b) over `sites`."""
    if zero is None:
        zero = Fraction(0)
    if one is None:
        one = Fraction(1)

    def wt(i, j):
        return w.get(ekey(i, j), zero)

    return haf_rec(wt, tuple(sorted(sites)), {}, one, zero)


def all_pms(sites):
    sites = tuple(sites)
    if not sites:
        return [()]
    out = []
    h = sites[0]
    for k in range(1, len(sites)):
        rest = sites[1:k] + sites[k + 1:]
        for t in all_pms(rest):
            out.append(((h, sites[k]),) + t)
    return out


def npm(edgeset, sites):
    """# perfect matchings of the edge set inside `sites`."""
    sites = tuple(sorted(sites))
    if len(sites) % 2:
        return 0
    es = set(edgeset)
    return sum(1 for M in all_pms(sites)
               if all(ekey(*e) in es for e in M))


# ------------------------------------------------------------------- ladder

def near_constant_words(n, ncol=NCOL, k=2):
    out = set()
    for g in range(ncol):
        base = (g,) * n
        out.add(base)
        for size in range(1, k + 1):
            for S in combinations(range(n), size):
                for vals in product(range(ncol), repeat=size):
                    w = list(base)
                    for i, s in enumerate(S):
                        w[s] = vals[i]
                    out.add(tuple(w))
    return tuple(sorted(out))


def offcount(word, ncol=NCOL):
    return min(sum(1 for x in word if x != g) for g in range(ncol))


def in_Xk(src, n, k, ncol=NCOL):
    for w in near_constant_words(n, ncol, k):
        tgt = 1 if len(set(w)) == 1 else 0
        if H_word(src, w, n, ncol) != tgt:
            return False, w
    return True, None


def pures(src, n, ncol=NCOL):
    return {c: H_word(src, (c,) * n, n, ncol) for c in range(ncol)}


# ---------------------------------------------- site systems (W27-R1, W28 copy)

def constrained_words(n, z, c, k, ncol=NCOL):
    """The k-near-constant words with w_z = c (constant word first)."""
    out = [w for w in near_constant_words(n, ncol, k) if w[z] == c]
    out.sort(key=lambda w: (len(set(w)) != 1, w))
    return out


def site_rows_exact(src, z, c, n, k, ncol=NCOL, words=None):
    """(rows, rhs, tags, cols): the colour-c linear system at site z."""
    sample = src[(0, 1)][0][0]
    zz, oo = zeroe(sample), onee(sample)
    cols = [(y, d) for y in range(n) if y != z for d in range(ncol)]
    idx = {t: i for i, t in enumerate(cols)}
    if words is None:
        words = constrained_words(n, z, c, k, ncol)
    rows, rhs, tags = [], [], []
    for w in words:
        row = [zz] * len(cols)
        for y in range(n):
            if y == z:
                continue
            U = tuple(x for x in range(n) if x not in (z, y))
            cof = haf_on(src, {a: w[a] for a in U}, U, ncol)
            j = idx[(y, w[y])]
            row[j] = row[j] + cof
        rows.append(row)
        rhs.append(oo if len(set(w)) == 1 else zz)
        tags.append(w)
    return rows, rhs, tags, cols


def rref_solve(rows, rhs, ncols):
    """Exact solve.  Returns (particular, kernel basis) or (None, None)."""
    sample = rhs[0] if rhs else Fraction(0)
    zz, oo = zeroe(sample), onee(sample)
    m = [list(r) + [b] for r, b in zip(rows, rhs)]
    piv, r = [], 0
    for c in range(ncols):
        p = None
        for i in range(r, len(m)):
            if m[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        inv = m[r][c].inv() if is_cyc(m[r][c]) else 1 / m[r][c]
        m[r] = [x * inv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        piv.append(c)
        r += 1
    for i in range(len(m)):
        if m[i][ncols] != 0 and all(x == 0 for x in m[i][:ncols]):
            return None, None
    part = [zz] * ncols
    for i, c in enumerate(piv):
        part[c] = m[i][ncols]
    kern = []
    for f in [c for c in range(ncols) if c not in piv]:
        v = [zz] * ncols
        v[f] = oo
        for i, c in enumerate(piv):
            v[c] = -m[i][f]
        kern.append(v)
    return part, kern


def apply_star(src, z, sols, cols, n, ncol=NCOL):
    out = copy_source(src)
    for c in range(ncol):
        for kk, (y, d) in enumerate(cols):
            v = sols[c][kk]
            if z < y:
                out[(z, y)][c][d] = v
            else:
                out[(y, z)][d][c] = v
    return out


# ------------------------------------------------------------- mod-p screens

def inv_mod(a, p):
    return pow(a % p, p - 2, p)


def src_to_mod(src, p, n, ncol=NCOL):
    out = {}
    for (a, b), m in src.items():
        out[(a, b)] = [[(Fraction(x).numerator % p
                         * inv_mod(Fraction(x).denominator, p)) % p
                        for x in row] for row in m]
    return out


class Ech:
    """Incremental echelon over F_p on augmented rows."""

    __slots__ = ("p", "nc", "basis", "rank")

    def __init__(self, nc, p):
        self.p, self.nc = p, nc
        self.basis = [None] * nc
        self.rank = 0

    def add(self, row, rhs=0):
        p, nc = self.p, self.nc
        v = [x % p for x in row] + [rhs % p]
        for c in range(nc):
            if v[c]:
                b = self.basis[c]
                if b is None:
                    inv = inv_mod(v[c], p)
                    self.basis[c] = [x * inv % p for x in v]
                    self.rank += 1
                    return "PIVOT"
                f = v[c]
                v = [(x - f * y) % p for x, y in zip(v, b)]
        return "INCONSISTENT" if v[nc] else "ZERO"


def feasible_from_rows(rows, rhs, ncols, p):
    """(consistent?, rank(mixed), rank(all)).  Mixed rows first."""
    E = Ech(ncols, p)
    consts = []
    for r, b in zip(rows, rhs):
        if b % p:
            consts.append((r, b))
        else:
            E.add(r, 0)
    rmix = E.rank
    ok = True
    for r, b in consts:
        if E.add(r, b) == "INCONSISTENT":
            ok = False
            break
    return ok, rmix, E.rank


# ------------------------------------------------------ sparse polynomials

class Poly:
    """Sparse multivariate polynomial: dict exponent-tuple -> Fraction."""

    __slots__ = ("nv", "t")

    def __init__(self, nv, t=None):
        self.nv = nv
        self.t = {} if t is None else {k: v for k, v in t.items() if v != 0}

    @staticmethod
    def const(nv, c):
        c = Fraction(c)
        return Poly(nv, {(0,) * nv: c} if c != 0 else {})

    @staticmethod
    def var(nv, i):
        e = [0] * nv
        e[i] = 1
        return Poly(nv, {tuple(e): Fraction(1)})

    def __bool__(self):
        return bool(self.t)

    def __eq__(self, o):
        if isinstance(o, Poly):
            return self.t == o.t
        return self.t == Poly.const(self.nv, o).t

    def __add__(self, o):
        if not isinstance(o, Poly):
            o = Poly.const(self.nv, o)
        t = dict(self.t)
        for k, v in o.t.items():
            nv = t.get(k, Fraction(0)) + v
            if nv:
                t[k] = nv
            else:
                t.pop(k, None)
        return Poly(self.nv, t)

    __radd__ = __add__

    def __neg__(self):
        return Poly(self.nv, {k: -v for k, v in self.t.items()})

    def __sub__(self, o):
        if not isinstance(o, Poly):
            o = Poly.const(self.nv, o)
        return self + (-o)

    def __rsub__(self, o):
        return (-self) + o

    def __mul__(self, o):
        if not isinstance(o, Poly):
            o = Poly.const(self.nv, o)
        t = {}
        for k1, v1 in self.t.items():
            for k2, v2 in o.t.items():
                k = tuple(a + b for a, b in zip(k1, k2))
                nv = t.get(k, Fraction(0)) + v1 * v2
                if nv:
                    t[k] = nv
                else:
                    t.pop(k, None)
        return Poly(self.nv, t)

    __rmul__ = __mul__

    def deg(self):
        return max((sum(k) for k in self.t), default=-1)

    def subs_num(self, vals):
        tot = Fraction(0)
        for k, v in self.t.items():
            m = v
            for i, e in enumerate(k):
                if e:
                    m *= Fraction(vals[i]) ** e
            tot += m
        return tot

    def sing(self, names):
        """Singular literal with INTEGER coefficients (clear denominators
        first; ledger 22)."""
        if not self.t:
            return "0"
        parts = []
        for k, v in sorted(self.t.items()):
            require(v.denominator == 1, f"clear denominators first: {v}")
            mono = [f"({v.numerator})"]
            for i, e in enumerate(k):
                if e == 1:
                    mono.append(names[i])
                elif e > 1:
                    mono.append(f"{names[i]}^{e}")
            parts.append("*".join(mono))
        return "(" + "+".join(parts) + ")"


def clear_denoms(polys):
    import math
    L = 1
    for p in polys:
        for v in p.t.values():
            L = math.lcm(L, v.denominator)
    if L == 1:
        return polys, 1
    return [Poly(p.nv, {k: v * L for k, v in p.t.items()}) for p in polys], L


# ---------------------------------------------------------------- Singular

def run_singular(script, timeout=3600):
    """Ledger 6/11/14: parse stdout for '?' lines; RC 0 is not enough."""
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
    """Ledger 13: never name a generator after a ring variable."""
    kws = ("poly ", "ideal ", "int ", "number ", "matrix ", "list ", "map ",
           "vector ", "def ", "ring ", "intvec ")
    for ln in script.splitlines():
        t = ln.strip()
        for kw in kws:
            if t.startswith(kw):
                name = t[len(kw):].split("=")[0].split("(")[0].split(",")[0]
                name = name.strip().rstrip(";")
                if name in ringvars:
                    raise AssertionError(f"ledger-13 shadowing hazard: {ln}")
    return True


# --------------------------------------------------------- known objects

def delta3_pms(n):
    m0 = [(i, i + 1) for i in range(0, n, 2)]
    m1 = [(i, (i + 1) % n) for i in range(1, n, 2)]
    half = n // 2
    m2 = [(i, i + half) for i in range(half)]
    return [[ekey(*e) for e in M] for M in (m0, m1, m2)]


def delta3_source(n, mats=None):
    mats = delta3_pms(n) if mats is None else mats
    src = zero_source(n)
    for c, M in enumerate(mats):
        for e in M:
            src[ekey(*e)][c][c] = Fraction(1)
    return src


def build_diag(n, Ls, wts):
    """Ls[c] = edge list; wts[(c, e)] = weight."""
    src = zero_source(n)
    for c, L in enumerate(Ls):
        for e in L:
            src[ekey(*e)][c][c] = wts[(c, ekey(*e))]
    return src


def load_F8():
    """W25's OBJECT_W25-F8 (an N=8 all-blocked X_3 source)."""
    import json
    p = ("/Users/rishi/workplace/krenn-conjecture/computations/"
         "unaudited-x3core-w25-2026-08-15/OBJECT_W25-F8_n8_allblocked_X3.json")
    with open(p) as fh:
        D = json.load(fh)
    blocks = D["blocks"] if "blocks" in D else D["source"]["blocks"]
    src = {}
    for k, m in blocks.items():
        a, b = (int(x) for x in k.replace("(", "").replace(")", "")
                .replace(" ", "").split(","))
        src[(a, b)] = [[Fraction(str(x)) for x in row] for row in m]
    return src


__all__ = [n for n in dir() if not n.startswith("_")]
