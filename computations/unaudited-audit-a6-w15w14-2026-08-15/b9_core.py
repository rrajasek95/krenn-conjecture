#!/usr/bin/env python3
"""A6-B9 (adversarial audit of W14 item 4, "CLOSED FORMS") -- INDEPENDENT engine.

Written from the audit brief's self-contained definitions ONLY.  Nothing is
imported from, or copied out of, the W14 probe: this file uses a different
polynomial representation (exponent vectors, not sorted index multisets), its
own Cauchy map, its own exact linear algebra and its own Singular driver.

Definitions implemented here (K = 3x3 matrix of indeterminates, n = 3i+j):

  s_A(K)        = sum_ij A_ij K_ij                         (linear form)
  Sigma_k       = S^k(C^3) (x) S^k(C^3), basis (mu, nu) of degree-k monomials
  iota_k(mu,nu) = sum_{sigma in S_k} prod_t K_{mu[t], nu[sigma(t)]}
  L_h(A)        = sum_{k=2..h} s^{h-k} iota_k(Sigma_k)      (degree-h forms)
  J_{h+r}(A)    = S^r(C^9) * L_h(A)                         (degree-(h+r) forms)
  <K^a, K^b>    = 0 (a != b),  prod_n a_n!   (a = b)        (apolar pairing)

EXACTNESS POLICY.  Every arithmetic operation is over Z / Q (int, Fraction) or
inside Singular over Q.  The only modular computation is `rank_mod_p`, which is
used exclusively as a *rigorous lower bound* on the rational rank of an integer
matrix (rank_{F_p}(M mod p) <= rank_Q(M) always), hence a rigorous UPPER bound
on the perp dimension.  Lower bounds on perp dimensions always come either from
exactly verified rational perp vectors or from Singular's exact kbase over Q.
No floating point anywhere (numpy is used only with int64 modular entries, with
an explicit overflow guard).
"""

from __future__ import annotations

import os
import subprocess
import tempfile
from fractions import Fraction
from functools import lru_cache
from itertools import combinations_with_replacement, permutations
from math import factorial, gcd

NV = 9
COL = (0, 1, 2)


def vidx(i: int, j: int) -> int:
    return 3 * i + j


def check(cond, msg):
    if not cond:
        raise AssertionError("B9 CHECK FAILED: " + msg)


# --------------------------------------------------------------- monomials

@lru_cache(maxsize=None)
def expos(d: int, n: int = NV) -> tuple:
    """All exponent vectors of length n with total degree d (lex order)."""
    if n == 1:
        return ((d,),)
    out = []
    for e in range(d, -1, -1):
        for tail in expos(d - e, n - 1):
            out.append((e,) + tail)
    return tuple(out)


@lru_cache(maxsize=None)
def expo_index(d: int, n: int = NV) -> dict:
    return {m: i for i, m in enumerate(expos(d, n))}


ZERO = (0,) * NV


def unit(n: int) -> tuple:
    return tuple(1 if t == n else 0 for t in range(NV))


# ------------------------------------------------------------- polynomials
# poly = {exponent-vector (len 9) : coefficient}

def padd(f, g):
    out = dict(f)
    for m, c in g.items():
        out[m] = out.get(m, 0) + c
    return {m: c for m, c in out.items() if c}


def pscale(f, c):
    return {} if c == 0 else {m: v * c for m, v in f.items()}


def pmul(f, g):
    out = {}
    for a, ca in f.items():
        for b, cb in g.items():
            k = tuple(x + y for x, y in zip(a, b))
            out[k] = out.get(k, 0) + ca * cb
    return {m: c for m, c in out.items() if c}


def ppow(f, e):
    out = {ZERO: 1}
    for _ in range(e):
        out = pmul(out, f)
    return out


def plin(vec):
    """The linear form sum_n vec[n] K_n."""
    return {unit(n): v for n, v in enumerate(vec) if v}


def pdeg(f):
    return None if not f else sum(next(iter(f)))


def flat(A):
    return [A[i][j] for i in COL for j in COL]


def s_poly(A):
    return plin(flat(A))


def to_vec(f, d):
    idx = expo_index(d)
    v = [0] * len(idx)
    for m, c in f.items():
        check(sum(m) == d, f"to_vec: term of degree {sum(m)} != {d}")
        v[idx[m]] += c
    return v


def from_vec(v, d):
    return {m: c for m, c in zip(expos(d), v) if c}


# ------------------------------------------------------------- differential
def apply_op(op, f):
    """op(d/dK) applied to f.  Both are polys; exact."""
    out = {}
    for beta, cb in op.items():
        for alpha, ca in f.items():
            if any(b > a for a, b in zip(alpha, beta)):
                continue
            mult = 1
            for a, b in zip(alpha, beta):
                for t in range(a - b + 1, a + 1):
                    mult *= t                       # a!/(a-b)!
            key = tuple(a - b for a, b in zip(alpha, beta))
            out[key] = out.get(key, 0) + cb * ca * mult
    return {m: c for m, c in out.items() if c}


def apolar(f, g):
    """<f, g> for forms of equal degree (0 if the degrees differ)."""
    tot = 0
    for m, cf in f.items():
        cg = g.get(m)
        if cg:
            w = 1
            for e in m:
                w *= factorial(e)
            tot += cf * cg * w
    return tot


# ----------------------------------------------------------- Cauchy / iota

@lru_cache(maxsize=None)
def sigma_basis(k: int) -> tuple:
    ms = tuple(combinations_with_replacement(COL, k))
    return tuple((mu, nu) for mu in ms for nu in ms)


@lru_cache(maxsize=None)
def iota(k: int, mu: tuple, nu: tuple) -> tuple:
    acc = {}
    for sg in permutations(range(k)):
        e = [0] * NV
        for t in range(k):
            e[vidx(mu[t], nu[sg[t]])] += 1
        key = tuple(e)
        acc[key] = acc.get(key, 0) + 1
    return tuple(sorted(acc.items()))


def L_gens(h, A):
    """Spanning set of L_h(A) = sum_{k=2..h} s^{h-k} iota_k(Sigma_k)."""
    sp = s_poly(A)
    out = []
    for k in range(2, h + 1):
        spow = ppow(sp, h - k)
        for mu, nu in sigma_basis(k):
            p = dict(iota(k, mu, nu))
            if h - k:
                p = pmul(p, spow)
            if p:
                out.append(p)
    return out


def J_gens(h, r, A, gens=None):
    """Spanning set of J_{h+r}(A) = S^r(C^9) * L_h(A)."""
    base = L_gens(h, A) if gens is None else gens
    if r == 0:
        return list(base)
    mons = [{m: 1} for m in expos(r)]
    return [pmul(m, g) for m in mons for g in base]


# ------------------------------------------------------------ det / cofactor

def det_poly():
    out = {}
    for pi in permutations(range(3)):
        inv = sum(1 for a in range(3) for b in range(a + 1, 3) if pi[a] > pi[b])
        e = [0] * NV
        for i in range(3):
            e[vidx(i, pi[i])] += 1
        key = tuple(e)
        out[key] = out.get(key, 0) + (-1 if inv % 2 else 1)
    return out


def perm_poly():
    """The PERMANENT (mutation control: det with all signs +1)."""
    out = {}
    for pi in permutations(range(3)):
        e = [0] * NV
        for i in range(3):
            e[vidx(i, pi[i])] += 1
        key = tuple(e)
        out[key] = out.get(key, 0) + 1
    return out


def cof_num(A, i, j):
    """Signed 2x2 cofactor of the numeric matrix A."""
    r = [x for x in range(3) if x != i]
    c = [y for y in range(3) if y != j]
    v = A[r[0]][c[0]] * A[r[1]][c[1]] - A[r[0]][c[1]] * A[r[1]][c[0]]
    return v if (i + j) % 2 == 0 else -v


def cof_poly(i, j):
    """cof_ij(K) as a quadratic form in K."""
    r = [x for x in range(3) if x != i]
    c = [y for y in range(3) if y != j]
    a = tuple(x + y for x, y in zip(unit(vidx(r[0], c[0])),
                                    unit(vidx(r[1], c[1]))))
    b = tuple(x + y for x, y in zip(unit(vidx(r[0], c[1])),
                                    unit(vidx(r[1], c[0]))))
    p = padd({a: 1}, {b: -1})
    return p if (i + j) % 2 == 0 else pscale(p, -1)


def det_num(A):
    return sum(A[0][j] * cof_num(A, 0, j) for j in range(3))


def rank_num(A):
    M = [[Fraction(x) for x in row] for row in A]
    r = 0
    for c in range(3):
        piv = next((i for i in range(r, 3) if M[i][c]), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(3):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        r += 1
    return r


def adj_num(A):
    """adjugate = transpose of the cofactor matrix."""
    return [[cof_num(A, j, i) for j in range(3)] for i in range(3)]


# ---------------------------------------------------------- the closed forms

def q_form(A):
    """q_A(K) = sum_ij A_ij cof_ij(K)   (quadratic in K)."""
    out = {}
    for i in COL:
        for j in COL:
            if A[i][j]:
                out = padd(out, pscale(cof_poly(i, j), A[i][j]))
    return out


def shat_form(A):
    """shat_A(K) = sum_ij cof_ij(A) K_ij   (linear in K)."""
    return plin([cof_num(A, i, j) for i in COL for j in COL])


def phi_form(A):
    """phi_A = q_A^2 - 4 shat_A det K."""
    return padd(pmul(q_form(A), q_form(A)),
                pscale(pmul(shat_form(A), det_poly()), -4))


def matmul_poly(K_is_left, B):
    """N = K*B as a 3x3 matrix of linear forms in K (B numeric)."""
    N = [[{} for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            acc = {}
            for t in range(3):
                if B[t][j]:
                    acc = padd(acc, {unit(vidx(i, t)): B[t][j]})
            N[i][j] = acc
    return N


def char_e(N, r):
    """e_r(N) for a 3x3 matrix N of polynomials: e_1 = tr, e_2 = sum of
    principal 2x2 minors, e_3 = det."""
    if r == 1:
        out = {}
        for i in range(3):
            out = padd(out, N[i][i])
        return out
    if r == 2:
        out = {}
        for i, j in ((0, 1), (0, 2), (1, 2)):
            out = padd(out, padd(pmul(N[i][i], N[j][j]),
                                 pscale(pmul(N[i][j], N[j][i]), -1)))
        return out
    if r == 3:
        out = {}
        for pi in permutations(range(3)):
            inv = sum(1 for a in range(3) for b in range(a + 1, 3)
                      if pi[a] > pi[b])
            t = {ZERO: 1}
            for i in range(3):
                t = pmul(t, N[i][pi[i]])
            out = padd(out, pscale(t, -1 if inv % 2 else 1))
        return out
    raise ValueError(r)


# ------------------------------------------------------------- L-monomials

def l_monomials(d):
    """(a, (b0,b1,b2)) with a + b0 + b1 + b2 = d."""
    out = []
    for a in range(d + 1):
        for b0 in range(d - a + 1):
            for b1 in range(d - a - b0 + 1):
                out.append((a, (b0, b1, d - a - b0 - b1)))
    return sorted(out)


def lmono_name(a, b):
    parts = []
    if a:
        parts.append("s" if a == 1 else f"s^{a}")
    for c in COL:
        if b[c] == 1:
            parts.append(f"k{c}")
        elif b[c] > 1:
            parts.append(f"k{c}^{b[c]}")
    return "".join(parts) if parts else "1"


def lmono_poly(a, b, A):
    p = ppow(s_poly(A), a)
    for c in COL:
        for _ in range(b[c]):
            p = pmul(p, {unit(vidx(c, c)): 1})
    return p


# ------------------------------------------------- exact integer linear algebra

def _content_div(row):
    g = 0
    for x in row:
        if x:
            g = gcd(g, abs(x))
    if g > 1:
        return [x // g for x in row]
    return row


class IntEchelon:
    """Incremental exact echelon basis of an integer row space (no fractions,
    content removed at every step so the entries stay small)."""

    def __init__(self, ncols):
        self.ncols = ncols
        self.rows = []          # integer rows, each with a distinct pivot
        self.piv = []           # pivot column of each row

    def reduce(self, v):
        v = list(v)
        for row, c in zip(self.rows, self.piv):
            if v[c]:
                a, b = row[c], v[c]
                g = gcd(a, b)
                ma, mb = a // g, b // g
                v = [ma * x - mb * y for x, y in zip(v, row)]
                v = _content_div(v)
        return v

    def add(self, v):
        v = self.reduce(v)
        c = next((i for i, x in enumerate(v) if x), None)
        if c is None:
            return False
        self.rows.append(v)
        self.piv.append(c)
        order = sorted(range(len(self.piv)), key=lambda t: self.piv[t])
        self.rows = [self.rows[t] for t in order]
        self.piv = [self.piv[t] for t in order]
        return True

    def rank(self):
        return len(self.rows)

    def contains(self, v):
        return not any(self.reduce(v))


def rank_exact(rows, ncols):
    E = IntEchelon(ncols)
    for r in rows:
        E.add(r)
    return E.rank()


def nullspace_exact(rows, ncols):
    """Exact rational nullspace {x : M x = 0} of an integer matrix, returned as
    integer vectors.  Full Fraction RREF; only for small ncols."""
    M = [[Fraction(x) for x in r] for r in rows]
    piv = []
    r = 0
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
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    free = [c for c in range(ncols) if c not in piv]
    out = []
    for fcol in free:
        x = [Fraction(0)] * ncols
        x[fcol] = Fraction(1)
        for i, c in enumerate(piv):
            x[c] = -M[i][fcol]
        den = 1
        for v in x:
            den = den * v.denominator // gcd(den, v.denominator)
        out.append(_content_div([int(v * den) for v in x]))
    return out


# --------------------------------------------- modular rank (rigorous bound)

_P = 46337          # prime; _P^2 * 2 < 2^63 so int64 never overflows
assert _P * _P < 2 ** 62


def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


assert is_prime(_P)


def rank_mod_p_py(rows, ncols, p=_P):
    """Pure-python modular rank (exact ints).  rank_{F_p} <= rank_Q always."""
    M = [[x % p for x in r] for r in rows]
    r = 0
    for c in range(ncols):
        sel = next((i for i in range(r, len(M)) if M[i][c]), None)
        if sel is None:
            continue
        M[r], M[sel] = M[sel], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [(x * inv) % p for x in M[r]]
        pr = M[r]
        for i in range(r + 1, len(M)):
            f = M[i][c]
            if f:
                M[i] = [(x - f * y) % p for x, y in zip(M[i], pr)]
        r += 1
        if r == len(M):
            break
    return r


def rank_mod_p(rows, ncols, p=_P):
    """numpy int64 modular rank -- exact integer arithmetic mod p, overflow
    impossible because p^2 < 2^62.  Same rigorous bound as the pure-python
    version (they are cross-checked against each other in b9_controls)."""
    import numpy as np
    if not rows:
        return 0
    M = np.array([[x % p for x in r] for r in rows], dtype=np.int64)
    nr = M.shape[0]
    r = 0
    for c in range(ncols):
        if r >= nr:
            break
        col = M[r:, c]
        nz = np.nonzero(col)[0]
        if nz.size == 0:
            continue
        i = r + int(nz[0])
        if i != r:
            M[[r, i]] = M[[i, r]]
        inv = pow(int(M[r, c]), p - 2, p)
        M[r] = (M[r] * inv) % p
        below = M[r + 1:, c]
        act = np.nonzero(below)[0]
        if act.size:
            idx = act + r + 1
            M[idx] = (M[idx] - np.outer(below[act], M[r])) % p
        r += 1
    return r


# --------------------------------------------------------------- Singular

SVARS = [f"k{n}" for n in range(NV)]


def sing_poly(f):
    if not f:
        return "0"
    parts = []
    for m, c in sorted(f.items()):
        t = "*".join(f"{SVARS[n]}^{e}" if e > 1 else SVARS[n]
                     for n, e in enumerate(m) if e)
        parts.append(f"({c})*{t}" if t else f"({c})")
    return "+".join(parts)


def run_singular(script, timeout=3600):
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write(script + "\nquit;\n")
        path = fh.name
    try:
        pr = subprocess.run(["Singular", "-q", "--no-warn", path],
                            capture_output=True, text=True, timeout=timeout)
    finally:
        os.unlink(path)
    if pr.returncode != 0:
        raise RuntimeError("Singular failed: " + pr.stderr[:2000])
    return pr.stdout
