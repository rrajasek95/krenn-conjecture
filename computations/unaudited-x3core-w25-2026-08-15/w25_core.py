#!/usr/bin/env python3
"""UNAUDITED PROBE W25 (the X_3 core) -- core module.

Pinned HEAD: see PINNED_HEAD.txt.

INDEPENDENT re-implementation of the matching tensor, the near-constant-word
ladder, the pure-equation identities L1/L2 and the NEW three-off identity L3,
and of the cap error E_pq(K).  Deliberately different code paths from W23:

  * hafnians by a memoised BITMASK DP (W23 enumerates perfect matchings);
  * E_pq(K) by the W22-M CLOSED FORM  E = Haf_U(sA+R) - s^{h-1}(K contract H)
    (W23 uses the subset-sum-over-J expansion) -- so agreement between the two
    is simultaneously an inter-probe control AND a check of W22-M;
  * arithmetic is generic: works over Q (fractions.Fraction) and over
    Q(omega) (class Om below, omega a primitive cube root of unity) -- omega is
    structural in this problem (W22-T), and ledger 19/20 demand it.

SETTING.  N sites (N even), blocks A_uv in V_u (x) V_v, V = C^3, oriented with
A_uv[i][j] = coefficient of colour i at u and colour j at v.

    H_B(A)_w = sum_{M in PM(B)} prod_{(u,v) in M} A_uv[w_u][w_v].

EXACT: H_w = 1 on the three constant words, 0 on every mixed word.

LADDER.  w is k-near-constant if some colour g has |{i : w_i != g}| <= k.
    X_k := {A : H_w = [w constant] for every k-near-constant w}.

All arithmetic exact.  No floats anywhere in this file.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations, product
import os
import subprocess
import tempfile

NCOL = 3
COLORS = (0, 1, 2)


def require(cond, detail):
    if not cond:
        raise AssertionError(detail)


# --------------------------------------------------------------- Q(omega)

class Om:
    """Exact element a + b*omega of Q(omega), omega^2 + omega + 1 = 0."""

    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = Fraction(a)
        self.b = Fraction(b)

    # -- constructors
    @staticmethod
    def coerce(x):
        return x if isinstance(x, Om) else Om(x, 0)

    def __repr__(self):
        return f"Om({self.a},{self.b})"

    def __eq__(self, other):
        if isinstance(other, Om):
            return self.a == other.a and self.b == other.b
        return self.b == 0 and self.a == Fraction(other)

    def __hash__(self):
        return hash((self.a, self.b))

    def __bool__(self):
        return bool(self.a) or bool(self.b)

    def __neg__(self):
        return Om(-self.a, -self.b)

    def __add__(self, other):
        o = Om.coerce(other)
        return Om(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __sub__(self, other):
        o = Om.coerce(other)
        return Om(self.a - o.a, self.b - o.b)

    def __rsub__(self, other):
        return Om.coerce(other) - self

    def __mul__(self, other):
        o = Om.coerce(other)
        a, b, c, d = self.a, self.b, o.a, o.b
        return Om(a * c - b * d, a * d + b * c - b * d)

    __rmul__ = __mul__

    def inv(self):
        n = self.a * self.a - self.a * self.b + self.b * self.b
        require(n != 0, "division by zero in Q(omega)")
        return Om((self.a - self.b) / n, -self.b / n)

    def __truediv__(self, other):
        return self * Om.coerce(other).inv()

    def __rtruediv__(self, other):
        return Om.coerce(other) * self.inv()

    def __pow__(self, k):
        require(isinstance(k, int) and k >= 0, "integer exponent only")
        out = Om(1, 0)
        for _ in range(k):
            out = out * self
        return out

    def conj(self):
        """omega -> omega^2 = -1-omega."""
        return Om(self.a - self.b, -self.b)

    def sing(self):
        """Singular literal in a ring with minpoly w^2+w+1 (integers only)."""
        require(self.a.denominator == 1 and self.b.denominator == 1,
                f"clear denominators first: {self}")
        return f"({self.a.numerator}+({self.b.numerator})*zw)"


OMEGA = Om(0, 1)


def is_om(x):
    return isinstance(x, Om)


def zeroelt(sample):
    return Om(0, 0) if is_om(sample) else Fraction(0)


def oneelt(sample):
    return Om(1, 0) if is_om(sample) else Fraction(1)


# ------------------------------------------------------------ source utils

def ekey(a, b):
    return (a, b) if a < b else (b, a)


def oriented(src, u, v, ncol=NCOL):
    """A_uv with row = colour at u, column = colour at v."""
    if u < v:
        return src[(u, v)]
    m = src[(v, u)]
    return [[m[j][i] for j in range(ncol)] for i in range(ncol)]


def zero_source(n, ncol=NCOL, zero=None):
    z = Fraction(0) if zero is None else zero
    return {(a, b): [[z] * ncol for _ in range(ncol)]
            for a, b in combinations(range(n), 2)}


def copy_source(src):
    return {e: [row[:] for row in m] for e, m in src.items()}


def sites_of(src):
    n = 0
    for (a, b) in src:
        n = max(n, a + 1, b + 1)
    return n


# ------------------------------------------------- hafnians by bitmask DP

def haf_mask(weight, mask, memo, one=None, zero=None):
    """weight(i,j) -> scalar; mask a bitmask of sites; memoised DP.

    Independent of W23's PM enumeration: peel the lowest set bit.
    `one`/`zero` must be the multiplicative/additive units of the coefficient
    ring (defaults Fraction(1)/Fraction(0)).  Odd |mask| gives zero.
    """
    if one is None:
        one = Fraction(1)
    if zero is None:
        zero = Fraction(0)
    if mask == 0:
        return one
    if bin(mask).count("1") % 2:
        return zero
    v = memo.get(mask)
    if v is not None:
        return v
    lo = (mask & -mask).bit_length() - 1
    rest = mask & ~(1 << lo)
    tot = zero
    m = rest
    while m:
        b = (m & -m).bit_length() - 1
        m &= ~(1 << b)
        wv = weight(lo, b)
        if wv == 0:
            continue
        sub = haf_mask(weight, rest & ~(1 << b), memo, one, zero)
        tot = tot + wv * sub
    memo[mask] = tot
    return tot


def _finish(v, sample):
    if v is None:
        return zeroelt(sample)
    return v


def H(src, word, n, ncol=NCOL):
    """H_B(A)_w for a word given as a tuple over range(n)."""
    sample = src[(0, 1)][0][0]
    if n % 2:
        return zeroelt(sample)

    def wt(i, j):
        return oriented(src, i, j, ncol)[word[i]][word[j]]

    v = haf_mask(wt, (1 << n) - 1, {}, oneelt(sample), zeroelt(sample))
    return _finish(v, sample)


def haf_sub(src, word, sites, ncol=NCOL):
    """Haf over a SUBSET of sites at the given word (word indexed by site)."""
    sample = src[(0, 1)][0][0]
    if len(sites) % 2:
        return zeroelt(sample)
    mask = 0
    for s in sites:
        mask |= 1 << s

    def wt(i, j):
        return oriented(src, i, j, ncol)[word[i]][word[j]]

    return _finish(haf_mask(wt, mask, {}, oneelt(sample), zeroelt(sample)),
                   sample)


def colour_slice(src, c, n, ncol=NCOL):
    """w_c(u,v) = A_uv[c][c]."""
    return {ekey(a, b): oriented(src, a, b, ncol)[c][c]
            for a, b in combinations(range(n), 2)}


def haf_scalar(w, sites, sample):
    if len(sites) % 2:
        return zeroelt(sample)
    mask = 0
    for s in sites:
        mask |= 1 << s

    def wt(i, j):
        return w[ekey(i, j)]

    return _finish(haf_mask(wt, mask, {}, oneelt(sample), zeroelt(sample)),
                   sample)


def cofactor(w, n, drop, sample):
    """C_drop = haf(w | B \\ drop)."""
    rest = tuple(x for x in range(n) if x not in drop)
    return haf_scalar(w, rest, sample)


def star_vec(src, a, u, c, ncol=NCOL):
    """sigma^(c)_au[d] = A_au[d][c]."""
    m = oriented(src, a, u, ncol)
    return [m[d][c] for d in range(ncol)]


# --------------------------------------------------------------- the ladder

@lru_cache(maxsize=None)
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
    """min over backgrounds g of |{i : w_i != g}|."""
    n = len(word)
    return min(sum(1 for x in word if x != g) for g in range(ncol))


def in_Xk(src, n, k, ncol=NCOL):
    """Exact membership test for X_k, from the RAW word definition."""
    for w in near_constant_words(n, ncol, k):
        tgt = 1 if len(set(w)) == 1 else 0
        if H(src, w, n, ncol) != tgt:
            return False, w
    return True, None


def pures(src, n, ncol=NCOL):
    return {c: H(src, (c,) * n, n, ncol) for c in range(ncol)}


def mixed_defects(src, n, ncol=NCOL):
    bad = []
    for word in product(range(ncol), repeat=n):
        if len(set(word)) == 1:
            continue
        if H(src, word, n, ncol) != 0:
            bad.append(word)
    return bad


# ------------------------------------------------------------- L1, L2, L3

def l1_residual(src, a, c, n, ncol=NCOL):
    """sum_{y != a} C^(c)_ay sigma^(c)_ay - e_c   in V_a."""
    sample = src[(0, 1)][0][0]
    w = colour_slice(src, c, n, ncol)
    vec = [zeroelt(sample)] * ncol
    for y in range(n):
        if y == a:
            continue
        cof = cofactor(w, n, (a, y), sample)
        if cof == 0:
            continue
        sv = star_vec(src, a, y, c, ncol)
        vec = [vec[d] + cof * sv[d] for d in range(ncol)]
    return [vec[d] - (1 if d == c else 0) for d in range(ncol)]


def l2_residual(src, a, b, c, n, ncol=NCOL):
    """C^(c)_ab A_ab + Phi^(c)_ab - e_c (x) e_c."""
    sample = src[(0, 1)][0][0]
    w = colour_slice(src, c, n, ncol)
    cof = cofactor(w, n, (a, b), sample)
    blk = oriented(src, a, b, ncol)
    out = [[cof * blk[d][e] for e in range(ncol)] for d in range(ncol)]
    rest = [x for x in range(n) if x not in (a, b)]
    for u, v in permutations(rest, 2):
        cf = cofactor(w, n, (a, b, u, v), sample)
        if cf == 0:
            continue
        sa = star_vec(src, a, u, c, ncol)
        sb = star_vec(src, b, v, c, ncol)
        for d in range(ncol):
            if sa[d] == 0:
                continue
            for e in range(ncol):
                if sb[e] == 0:
                    continue
                out[d][e] = out[d][e] + cf * sa[d] * sb[e]
    for d in range(ncol):
        for e in range(ncol):
            if d == c and e == c:
                out[d][e] = out[d][e] - 1
    return out


def l3_T(src, S, tgt, c, n, ncol=NCOL):
    """T^(c)_{S;tgt}[d] := sum_{u not in S} C^(c)_{S + u} sigma^(c)_{tgt,u}[d],
    for S a 3-set of sites and tgt in S (the unmatched member)."""
    sample = src[(0, 1)][0][0]
    w = colour_slice(src, c, n, ncol)
    out = [zeroelt(sample)] * ncol
    for u in range(n):
        if u in S:
            continue
        cf = cofactor(w, n, tuple(S) + (u,), sample)
        if cf == 0:
            continue
        sv = star_vec(src, tgt, u, c, ncol)
        out = [out[d] + cf * sv[d] for d in range(ncol)]
    return out


def l3_Xi(src, S, c, n, ncol=NCOL):
    """Xi^(c)_S[d1][d2][d3] = sum_{u,v,x distinct outside S}
       C^(c)_{S,u,v,x} sigma^(c)_{S0 u}[d1] sigma^(c)_{S1 v}[d2]
                       sigma^(c)_{S2 x}[d3]."""
    sample = src[(0, 1)][0][0]
    zz = zeroelt(sample)
    w = colour_slice(src, c, n, ncol)
    a, b, e = S
    out = [[[zz] * ncol for _ in range(ncol)] for _ in range(ncol)]
    rest = [x for x in range(n) if x not in S]
    for u, v, x in permutations(rest, 3):
        cf = cofactor(w, n, tuple(S) + (u, v, x), sample)
        if cf == 0:
            continue
        sa = star_vec(src, a, u, c, ncol)
        sb = star_vec(src, b, v, c, ncol)
        se = star_vec(src, e, x, c, ncol)
        for d1 in range(ncol):
            if sa[d1] == 0:
                continue
            for d2 in range(ncol):
                if sb[d2] == 0:
                    continue
                for d3 in range(ncol):
                    if se[d3] == 0:
                        continue
                    out[d1][d2][d3] = (out[d1][d2][d3]
                                       + cf * sa[d1] * sb[d2] * se[d3])
    return out


def l3_Psi(src, S, c, n, ncol=NCOL):
    """THE THREE-OFF TENSOR IDENTITY (law L3), left-hand side.

        Psi^(c)_{abe}[d1][d2][d3]
          = A_ab[d1][d2] T^(c)_{S;e}[d3] + A_ae[d1][d3] T^(c)_{S;b}[d2]
          + A_be[d2][d3] T^(c)_{S;a}[d1] + Xi^(c)_S[d1][d2][d3].

    Exactness on the 3-off words pins Psi = e_c (x) e_c (x) e_c."""
    S = tuple(S)
    a, b, e = S
    Ta = l3_T(src, S, a, c, n, ncol)
    Tb = l3_T(src, S, b, c, n, ncol)
    Te = l3_T(src, S, e, c, n, ncol)
    Aab = oriented(src, a, b, ncol)
    Aae = oriented(src, a, e, ncol)
    Abe = oriented(src, b, e, ncol)
    Xi = l3_Xi(src, S, c, n, ncol)
    out = [[[None] * ncol for _ in range(ncol)] for _ in range(ncol)]
    for d1 in range(ncol):
        for d2 in range(ncol):
            for d3 in range(ncol):
                out[d1][d2][d3] = (Aab[d1][d2] * Te[d3]
                                   + Aae[d1][d3] * Tb[d2]
                                   + Abe[d2][d3] * Ta[d1]
                                   + Xi[d1][d2][d3])
    return out


def l3_residual(src, S, c, n, ncol=NCOL):
    P = l3_Psi(src, S, c, n, ncol)
    for d1 in range(ncol):
        for d2 in range(ncol):
            for d3 in range(ncol):
                if d1 == c and d2 == c and d3 == c:
                    P[d1][d2][d3] = P[d1][d2][d3] - 1
    return P


# -------------------------------------------------------------- linear algebra

def _rref(rows, ncols, augmented=False):
    m = [list(r) for r in rows]
    piv = []
    r = 0
    width = ncols + (1 if augmented else 0)
    for c in range(ncols):
        p = None
        for i in range(r, len(m)):
            if m[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        inv = 1 / m[r][c] if not is_om(m[r][c]) else m[r][c].inv()
        m[r] = [x * inv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        piv.append(c)
        r += 1
        if r == len(m):
            break
    return m, piv, r, width


def matrix_rank(rows):
    if not rows:
        return 0
    _, piv, r, _ = _rref(rows, len(rows[0]))
    return r


def nullspace(rows, ncols):
    if not rows:
        rows = [[Fraction(0)] * ncols]
    m, piv, r, _ = _rref(rows, ncols)
    free = [c for c in range(ncols) if c not in piv]
    sample = rows[0][0]
    zz, oo = zeroelt(sample), oneelt(sample)
    basis = []
    for f in free:
        v = [zz] * ncols
        v[f] = oo
        for i, c in enumerate(piv):
            v[c] = -m[i][f]
        basis.append(v)
    return basis


def solve_linear(rows, rhs, ncols=None):
    """Exact solve; returns (particular, kernel basis) or (None, None)."""
    if ncols is None:
        ncols = len(rows[0]) if rows else 0
    sample = rhs[0] if rhs else Fraction(0)
    zz, oo = zeroelt(sample), oneelt(sample)
    m = [list(r) + [b] for r, b in zip(rows, rhs)]
    piv = []
    r = 0
    for c in range(ncols):
        p = None
        for i in range(r, len(m)):
            if m[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        inv = m[r][c].inv() if is_om(m[r][c]) else 1 / m[r][c]
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


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


# ---------------------------------------------------- cap error (W22-M form)

def cap_s(src, p, q, K, ncol=NCOL):
    m = oriented(src, p, q, ncol)
    tot = None
    for i in range(ncol):
        for j in range(ncol):
            if K[i][j] == 0:
                continue
            t = K[i][j] * m[i][j]
            tot = t if tot is None else tot + t
    return _finish(tot, src[(0, 1)][0][0])


def cap_R(src, p, q, K, sites, ncol=NCOL):
    """R_{ab}(ca,cb) = sum_ij K_ij (A_pa[i][ca] A_qb[j][cb]
                                    + A_qa[j][ca] A_pb[i][cb])."""
    sample = src[(0, 1)][0][0]
    zz = zeroelt(sample)
    R = {}
    for a, b in combinations(sorted(sites), 2):
        apa, aqa = oriented(src, p, a, ncol), oriented(src, q, a, ncol)
        apb, aqb = oriented(src, p, b, ncol), oriented(src, q, b, ncol)
        mat = [[zz] * ncol for _ in range(ncol)]
        for ca in range(ncol):
            row = [zz] * ncol
            for cb in range(ncol):
                tot = zz
                for i in range(ncol):
                    for j in range(ncol):
                        k = K[i][j]
                        if k == 0:
                            continue
                        tot = tot + k * (apa[i][ca] * aqb[j][cb]
                                         + aqa[j][ca] * apb[i][cb])
                row[cb] = tot
            mat[ca] = row
        R[(a, b)] = mat
    return R


def _tabentry(tab, a, b, ca, cb):
    return tab[(a, b)][ca][cb] if a < b else tab[(b, a)][cb][ca]


def cap_error(src, p, q, K, sites, ncol=NCOL):
    """E_pq(K) by the W22-M CLOSED FORM

        E_w = Haf_U(sA + R)_w - s^{h-1} * (K contract H_B(A))_w,
        (K contract H)_w = sum_ij K_ij H_B(A)_{w with i at p, j at q}.

    Returns {word on U (tuple in site order) : value} for nonzero values."""
    sample = src[(0, 1)][0][0]
    sites = tuple(sorted(sites))
    h = len(sites) // 2
    s = cap_s(src, p, q, K, ncol)
    R = cap_R(src, p, q, K, sites, ncol)
    n = sites_of(src)
    slot = {a: i for i, a in enumerate(sites)}
    mask = 0
    for a in sites:
        mask |= 1 << a
    out = {}
    for word in product(range(ncol), repeat=len(sites)):
        wd = {a: word[slot[a]] for a in sites}

        def wt(i, j, wd=wd, s=s, R=R):
            return (s * oriented(src, i, j, ncol)[wd[i]][wd[j]]
                    + _tabentry(R, i, j, wd[i], wd[j]))

        first = _finish(haf_mask(wt, mask, {}, oneelt(sample),
                                 zeroelt(sample)), sample)
        # K contract H
        kc = zeroelt(sample)
        for i in range(ncol):
            for j in range(ncol):
                if K[i][j] == 0:
                    continue
                full = dict(wd)
                full[p] = i
                full[q] = j
                fw = tuple(full[t] for t in range(n))
                kc = kc + K[i][j] * H(src, fw, n, ncol)
        val = first - (s ** (h - 1)) * kc
        if val != 0:
            out[word] = val
    return out


def is_admissible(src, p, q, K, ncol=NCOL):
    return cap_s(src, p, q, K, ncol) != 0 and all(K[c][c] != 0
                                                  for c in range(ncol))


def live(src, p, q, ncol=NCOL):
    return any(x != 0 for row in oriented(src, p, q, ncol) for x in row)


# -------------------------------------------------------------------- Singular

def run_singular(script: str, timeout: int = 3600):
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
        raise RuntimeError(f"Singular failed rc={proc.returncode}: {bad[:5]} "
                           f"{proc.stderr[:1500]}")
    return out


def no_shadow_guard(script: str, ringvars):
    """Ledger 13: never name a generator after a ring variable."""
    for ln in script.splitlines():
        t = ln.strip()
        for kw in ("poly ", "ideal ", "int ", "number ", "matrix ", "list ",
                   "vector ", "map "):
            if t.startswith(kw):
                name = t[len(kw):].split("=")[0].split("(")[0].strip()
                if name in ringvars:
                    raise AssertionError(f"shadowing hazard: {ln}")
    return True


# ------------------------------------------------------------ known sources

def delta43():
    src = zero_source(4)
    for c, M in enumerate([((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]):
        for e in M:
            src[e][c][c] = Fraction(1)
    return src


def delta3_N(n, mats=None):
    """Delta^(3)_N: three pairwise disjoint perfect matchings, colour c on the
    c-th, unit weights.  Default: the standard construction on 0..n-1."""
    require(n % 2 == 0 and n >= 6, "need even n >= 6")
    if mats is None:
        mats = default_three_pms(n)
    src = zero_source(n)
    for c, M in enumerate(mats):
        for (a, b) in M:
            src[ekey(a, b)][c][c] = Fraction(1)
    return src


def default_three_pms(n):
    """Three pairwise-disjoint perfect matchings of K_n (n even >= 6):
    take the n-cycle 0-1-...-(n-1)-0.  M0 = even edges, M1 = odd edges,
    M2 = the 'antipodal' matching i -> i + n/2."""
    m0 = [(i, i + 1) for i in range(0, n, 2)]
    m1 = [(i, (i + 1) % n) for i in range(1, n, 2)]
    half = n // 2
    m2 = [(i, i + half) for i in range(half)]
    ms = [m0, m1, m2]
    seen = set()
    for M in ms:
        for e in M:
            k = ekey(*e)
            require(k not in seen, f"matchings not disjoint at {k} (n={n})")
            seen.add(k)
    for M in ms:
        cov = sorted([x for e in M for x in e])
        require(cov == list(range(n)), "not a perfect matching")
    return ms


def near_exact_six_site():
    """The committed near-exact six-site source (W17 t2e certificate)."""
    import json
    path = ("/Users/rishi/workplace/krenn-conjecture/computations/"
            "unaudited-scalar-slice-w17-2026-08-15/"
            "results_t2e_nearexact_certificate.json")
    with open(path) as fh:
        C = json.load(fh)
    src = {}
    for k, m in C["blocks"].items():
        a, b = (int(x) for x in k.replace("(", "").replace(")", "").split(","))
        src[(a, b)] = [[Fraction(str(x)) for x in row] for row in m]
    return src


def w23_allblocked_x2(idx=None):
    """W23's all-blocked X_2 objects (T2f), as exact rational sources."""
    import json
    path = ("/Users/rishi/workplace/krenn-conjecture/computations/"
            "unaudited-pure-core-w23-2026-08-15/results_t2f_x2_allblocked.json")
    with open(path) as fh:
        D = json.load(fh)
    out = []
    for rec in D["all_blocked_found"]:
        src = {}
        for k, m in rec["blocks"].items():
            a, b = (int(x) for x in k.split(","))
            src[(a, b)] = [[Fraction(x) for x in row] for row in m]
        out.append(src)
    return out if idx is None else out[idx]


def clear_denominators(src, ncol=NCOL):
    """Scale the whole source by a common integer (licensed by ledger 22:
    every term of E_pq has total degree 2h, so verdicts are unchanged)."""
    import math
    L = 1
    for m in src.values():
        for row in m:
            for x in row:
                if is_om(x):
                    L = math.lcm(L, x.a.denominator, x.b.denominator)
                else:
                    L = math.lcm(L, Fraction(x).denominator)
    out = {}
    for e, m in src.items():
        if is_om(m[0][0]):
            out[e] = [[Om(x.a * L, x.b * L) for x in row] for row in m]
        else:
            out[e] = [[Fraction(x) * L for x in row] for row in m]
    return out, L


def torus_act(src, lam, n, ncol=NCOL):
    """A_uv[i][j] -> lam[u][i] lam[v][j] A_uv[i][j].  Preserves every X_k when
    prod_u lam[u][c] = 1 for each colour c, and preserves witness/blocked
    status at every pair (conjugate the cap by the same diagonals)."""
    out = {}
    for (a, b), m in src.items():
        out[(a, b)] = [[lam[a][i] * lam[b][j] * m[i][j] for j in range(ncol)]
                       for i in range(ncol)]
    return out


def permute_sites(src, perm, n, ncol=NCOL):
    out = {}
    for a, b in combinations(range(n), 2):
        pa, pb = perm[a], perm[b]
        out[(a, b)] = [row[:] for row in oriented(src, pa, pb, ncol)]
    return out


def permute_colours(src, cp, ncol=NCOL):
    """Simultaneous colour permutation at every site."""
    inv = [0] * ncol
    for i, x in enumerate(cp):
        inv[x] = i
    out = {}
    for e, m in src.items():
        out[e] = [[m[inv[i]][inv[j]] for j in range(ncol)] for i in range(ncol)]
    return out
