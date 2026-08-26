#!/usr/bin/env python3
"""UNAUDITED PROBE W22 (induction layer, restarted) -- core.

Pinned HEAD: see PINNED_HEAD.txt.

INDEPENDENT re-implementation (from notes/clean-pair-cap-exact-descent-target.md
only) of the GENERAL-cap pair error, plus the W22 structure layer:

  B even, |B| = N = 2h+2, blocks A_uv in V_u (x) V_v, V = C^3.
  Pair (p,q), U = B \\ {p,q}, |U| = 2h.  Cap K in (V_p (x) V_q)^*, a 3x3
  matrix K[i][j] = K(e_i^p, e_j^q).

    s        = <K, A_pq> = sum_ij K_ij A_pq(i,j)
    kappa_c  = K[c][c]
    R_ab     = K |_ (A_{p|a} A_{q|b} + A_{p|b} A_{q|a})  in V_a (x) V_b
             = sum_ij K_ij [ A_pa(i,.) (x) A_qb(j,.) + A_qa(j,.) (x) A_pb(i,.) ]

  E_pq(K) = sum_{k=2}^h s^{h-k} [ r^k / k! exp(x) ]_U
          = sum_{M in PM(U)} sum_{J subset M, |J| >= 2}
                s^{h-|J|} prod_{e in J} R_e  prod_{e in M\\J} A_e      (Lemma W22-M)
          = Haf_U(sA + R) - s^{h-1} (K |_ H_B(A))                      (Lemma W22-H)

  ADMISSIBLE: s != 0 and kappa_0 kappa_1 kappa_2 != 0.
  WITNESS at (p,q): an admissible K with E_pq(K) = 0 (all 3^{2h} components).
  BLOCKED at (p,q): no witness.

All arithmetic exact (int / Fraction).  No floats anywhere in this file.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
import os
import subprocess
import tempfile

COLORS = (0, 1, 2)


def require(cond, detail):
    if not cond:
        raise AssertionError(detail)


def ekey(a, b):
    return (a, b) if a < b else (b, a)


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple) -> tuple:
    if not vertices:
        return ((),)
    first = vertices[0]
    out = []
    for idx in range(1, len(vertices)):
        second = vertices[idx]
        rest = vertices[1:idx] + vertices[idx + 1:]
        for tail in perfect_matchings(rest):
            out.append(((first, second),) + tail)
    return tuple(out)


# --------------------------------------------------------------- source utils

def oriented(source, u, v, ncol=3):
    """Block with row index = colour at u, column index = colour at v."""
    if u < v:
        return source[(u, v)]
    m = source[(v, u)]
    return [[m[j][i] for j in range(ncol)] for i in range(ncol)]


def ghz_coefficient(source, word, n, ncol=3):
    total = Fraction(0)
    for matching in perfect_matchings(tuple(range(n))):
        term = Fraction(1)
        for a, b in matching:
            term *= oriented(source, a, b, ncol)[word[a]][word[b]]
            if term == 0:
                break
        total += term
    return total


def ghz_defects(source, n, ncol=3, colours=None):
    """Words where H_B(A)_w != delta(w constant).  colours: allowed palette."""
    cols = tuple(range(ncol)) if colours is None else tuple(colours)
    bad = []
    for word in product(cols, repeat=n):
        target = 1 if len(set(word)) == 1 else 0
        if ghz_coefficient(source, word, n, ncol) != target:
            bad.append(word)
    return bad


def mixed_defects(source, n, ncol=3, colours=None):
    """Mixed words where H != 0 (mixed-exactness test)."""
    cols = tuple(range(ncol)) if colours is None else tuple(colours)
    bad = []
    for word in product(cols, repeat=n):
        if len(set(word)) == 1:
            continue
        if ghz_coefficient(source, word, n, ncol) != 0:
            bad.append(word)
    return bad


def pures(source, n, ncol=3, colours=None):
    cols = tuple(range(ncol)) if colours is None else tuple(colours)
    return {c: ghz_coefficient(source, (c,) * n, n, ncol) for c in cols}


def matrix_rank(matrix):
    rows = [[Fraction(e) for e in row] for row in matrix]
    if not rows:
        return 0
    rank = 0
    for col in range(len(rows[0])):
        piv = None
        for i in range(rank, len(rows)):
            if rows[i][col] != 0:
                piv = i
                break
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        head = rows[rank]
        for i in range(len(rows)):
            if i != rank and rows[i][col] != 0:
                f = rows[i][col] / head[col]
                rows[i] = [a - f * b for a, b in zip(rows[i], head)]
        rank += 1
    return rank


# ------------------------------------------------------------- cap ingredients

def cap_s(source, p, q, K, ncol=3):
    apq = oriented(source, p, q, ncol)
    return sum(K[i][j] * apq[i][j] for i in range(ncol) for j in range(ncol))


def cap_kappa(K, ncol=3):
    return [K[c][c] for c in range(ncol)]


def cap_R(source, p, q, K, sites, ncol=3):
    """R_ab in V_a (x) V_b for every pair {a,b} of U, as a 3x3 matrix keyed by
    ekey(a,b) with row = colour at min(a,b)."""
    R = {}
    for a, b in combinations(sorted(sites), 2):
        apa = oriented(source, p, a, ncol)
        aqa = oriented(source, q, a, ncol)
        apb = oriented(source, p, b, ncol)
        aqb = oriented(source, q, b, ncol)
        mat = [[0] * ncol for _ in range(ncol)]
        for ca in range(ncol):
            for cb in range(ncol):
                tot = 0
                for i in range(ncol):
                    for j in range(ncol):
                        k = K[i][j]
                        if k == 0:
                            continue
                        tot += k * (apa[i][ca] * aqb[j][cb]
                                    + aqa[j][ca] * apb[i][cb])
                mat[ca][cb] = tot
        R[(a, b)] = mat
    return R


def _entry(table, a, b, ca, cb):
    if a < b:
        return table[(a, b)][ca][cb]
    return table[(b, a)][cb][ca]


# ------------------------------------------------------------- evaluator (I)

def cap_error_direct(source, p, q, K, sites, ncol=3):
    """(I) Lemma W22-M: matching sum with >= 2 R-edges."""
    sites = tuple(sorted(sites))
    h = len(sites) // 2
    s = cap_s(source, p, q, K, ncol)
    R = cap_R(source, p, q, K, sites, ncol)
    A = {(a, b): oriented(source, a, b, ncol)
         for a, b in combinations(sites, 2)}
    slot = {a: n for n, a in enumerate(sites)}
    out = {}
    for word in product(range(ncol), repeat=len(sites)):
        total = 0
        for M in perfect_matchings(sites):
            for size in range(2, h + 1):
                pref = s ** (h - size)
                if pref == 0:
                    continue
                for J in combinations(range(h), size):
                    Jset = set(J)
                    term = pref
                    for n, (a, b) in enumerate(M):
                        ca, cb = word[slot[a]], word[slot[b]]
                        tab = R if n in Jset else A
                        term *= _entry(tab, a, b, ca, cb)
                        if term == 0:
                            break
                    total += term
        if total != 0:
            out[word] = total
    return out


# ------------------------------------------------------------- evaluator (II)

def _haf_tensor(table, sites, word_of, ncol=3):
    total = 0
    for M in perfect_matchings(tuple(sites)):
        term = 1
        for a, b in M:
            term *= _entry(table, a, b, word_of[a], word_of[b])
            if term == 0:
                break
        total += term
    return total


def cap_error_hafnian(source, p, q, K, sites, n, ncol=3):
    """(II) Lemma W22-H: E = Haf_U(sA + R) - s^{h-1} (K |_ H_B(A))."""
    sites = tuple(sorted(sites))
    h = len(sites) // 2
    s = cap_s(source, p, q, K, ncol)
    R = cap_R(source, p, q, K, sites, ncol)
    comb = {}
    for a, b in combinations(sites, 2):
        blk = oriented(source, a, b, ncol)
        comb[(a, b)] = [[s * blk[i][j] + R[(a, b)][i][j] for j in range(ncol)]
                        for i in range(ncol)]
    slot = {a: t for t, a in enumerate(sites)}
    out = {}
    for word in product(range(ncol), repeat=len(sites)):
        word_of = {a: word[slot[a]] for a in sites}
        val = _haf_tensor(comb, sites, word_of, ncol)
        cap = 0
        for i in range(ncol):
            for j in range(ncol):
                if K[i][j] == 0:
                    continue
                full = [0] * n
                for a in sites:
                    full[a] = word_of[a]
                full[p], full[q] = i, j
                cap += K[i][j] * ghz_coefficient(source, tuple(full), n, ncol)
        val -= s ** (h - 1) * cap
        if val != 0:
            out[word] = val
    return out


def cap_error(source, p, q, K, sites, n=None, check=False, ncol=3):
    val = cap_error_direct(source, p, q, K, sites, ncol)
    if check:
        require(n is not None, "hafnian evaluator needs n")
        require(val == cap_error_hafnian(source, p, q, K, sites, n, ncol),
                ("evaluator I != II", p, q))
    return val


def is_admissible(source, p, q, K, ncol=3):
    return (cap_s(source, p, q, K, ncol) != 0
            and all(k != 0 for k in cap_kappa(K, ncol)))


# ------------------------------------------------- support (Lemma W22-M) layer

def support_graphs(source, p, q, K, sites, ncol=3):
    """G_R (edges with R_e != 0) and G_A (edges with A_e != 0) on U."""
    sites = tuple(sorted(sites))
    R = cap_R(source, p, q, K, sites, ncol)
    gr, ga = set(), set()
    for a, b in combinations(sites, 2):
        if any(x != 0 for row in R[(a, b)] for x in row):
            gr.add((a, b))
        blk = oriented(source, a, b, ncol)
        if any(x != 0 for row in blk for x in row):
            ga.add((a, b))
    return gr, ga


def support_clean(source, p, q, K, sites, ncol=3):
    """TRUE if no perfect matching of U has >= 2 G_R edges and the rest in G_A
    (=> E_pq(K) = 0 by Lemma W22-M; the converse can fail: cancellation)."""
    sites = tuple(sorted(sites))
    gr, ga = support_graphs(source, p, q, K, sites, ncol)
    for M in perfect_matchings(sites):
        edges = [ekey(a, b) for a, b in M]
        nr = sum(1 for e in edges if e in gr)
        if nr < 2:
            continue
        # need: choose >=2 R-edges, remaining edges in G_A
        for size in range(2, len(edges) + 1):
            for J in combinations(range(len(edges)), size):
                Js = set(J)
                if all(edges[i] in gr for i in J) and \
                   all(edges[i] in ga for i in range(len(edges)) if i not in Js):
                    return False
    return True


# --------------------------------------------------- rank-one / transfer layer

def alpha_beta(source, p, q, u, v, sites, ncol=3):
    alpha, beta = {}, {}
    for a in sites:
        apa = oriented(source, p, a, ncol)
        aqa = oriented(source, q, a, ncol)
        alpha[a] = [sum(u[i] * apa[i][c] for i in range(ncol))
                    for c in range(ncol)]
        beta[a] = [sum(v[j] * aqa[j][c] for j in range(ncol))
                   for c in range(ncol)]
    return alpha, beta


def outer_K(u, v, ncol=3):
    return [[u[i] * v[j] for j in range(ncol)] for i in range(ncol)]


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]]


def site_rank(al, be):
    if all(x == 0 for x in al) and all(x == 0 for x in be):
        return 0
    if any(x != 0 for x in cross(al, be)):
        return 2
    return 1


def site_ratio(al, be):
    for c in COLORS:
        if al[c] != 0 or be[c] != 0:
            g = al[c] if al[c] != 0 else be[c]
            return (Fraction(al[c], 1) / g, Fraction(be[c], 1) / g)
    return (Fraction(0), Fraction(0))


def ehom(lams, mus, j):
    total = Fraction(0)
    for Bset in combinations(range(len(lams)), j):
        Bs = set(Bset)
        term = Fraction(1)
        for i in range(len(lams)):
            term *= lams[i] if i in Bs else mus[i]
        total += term
    return total


def h2_predicate(source, p, q, u, v, sites, ncol=3):
    """W17.1 re-implemented independently (h = 2 only)."""
    sites = tuple(sorted(sites))
    require(len(sites) == 4, "h=2 predicate needs |U| = 4")
    alpha, beta = alpha_beta(source, p, q, u, v, sites, ncol)
    ranks = {a: site_rank(alpha[a], beta[a]) for a in sites}
    I = [a for a in sites if ranks[a] == 2]
    rest = [a for a in sites if ranks[a] != 2]
    rat = [site_ratio(alpha[a], beta[a]) for a in rest]
    lams = [r[0] for r in rat]
    mus = [r[1] for r in rat]
    ok, cond = True, {}
    for j in range(0, 3):
        if 2 - j <= len(I):
            if j <= len(rest):
                val = ehom(lams, mus, j)
            else:
                val = Fraction(0)
            cond[j] = val
            if val != 0:
                ok = False
    return ok, {"ranks": ranks, "I": I, "rest": rest,
                "lambda": lams, "mu": mus, "conditions": cond}


# -------------------------------------------------------------------- Singular

def run_singular(script: str, timeout: int = 1800):
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write(script + "\nquit;\n")
        path = fh.name
    try:
        proc = subprocess.run(["Singular", "-q", "--no-warn", path],
                              capture_output=True, text=True, timeout=timeout)
    finally:
        os.unlink(path)
    out = proc.stdout
    # ledger item 11: Singular reports errors on stdout with return code 0
    bad = [ln for ln in out.splitlines() if ln.strip().startswith("?")]
    if proc.returncode != 0 or bad:
        raise RuntimeError(f"Singular failed rc={proc.returncode}: "
                           f"{bad[:5]} {proc.stderr[:1500]}")
    return out


def no_shadow_guard(script: str, ringvars):
    """Ledger item 13: never name a generator after a ring variable."""
    for ln in script.splitlines():
        t = ln.strip()
        for kw in ("poly ", "ideal ", "int ", "number ", "matrix ", "list "):
            if t.startswith(kw):
                name = t[len(kw):].split("=")[0].split("(")[0].strip()
                if name in ringvars:
                    raise AssertionError(f"shadowing hazard: {ln}")
    return True


# ------------------------------------------- scalar (monochrome) slice error

def scalar_slice_error(t, p, q, sites):
    """W5's scalar slice error at GENERAL h, by the matching sum:
       E = sum_M sum_{J subset M, |J| >= 2} s^{h-|J|} prod_J r_e prod_{M\\J} t_e
    with s = t_pq, r_ab = t_pa t_qb + t_pb t_qa.  Agrees with
    slice_core.slice_error for h in {2,3} (checked in the controls)."""
    sites = tuple(sorted(sites))
    h = len(sites) // 2
    s = t[ekey(p, q)]
    r = {ekey(a, b): t[ekey(p, a)] * t[ekey(q, b)] + t[ekey(p, b)] * t[ekey(q, a)]
         for a, b in combinations(sites, 2)}
    total = 0
    for M in perfect_matchings(sites):
        for size in range(2, h + 1):
            pref = s ** (h - size)
            if pref == 0:
                continue
            for J in combinations(range(h), size):
                Js = set(J)
                term = pref
                for i, (a, b) in enumerate(M):
                    term *= (r if i in Js else t)[ekey(a, b)]
                    if term == 0:
                        break
                total += term
    return total


# ------------------------------------- exact arithmetic in Z[omega] (Eisenstein)

class Eis:
    """a + b*omega with omega^2 = -1 - omega (a primitive cube root of unity).
    Exact; coefficients are Fractions."""
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = Fraction(a)
        self.b = Fraction(b)

    @staticmethod
    def _c(x):
        return x if isinstance(x, Eis) else Eis(x, 0)

    def __add__(self, o):
        o = Eis._c(o)
        return Eis(self.a + o.a, self.b + o.b)
    __radd__ = __add__

    def __neg__(self):
        return Eis(-self.a, -self.b)

    def __sub__(self, o):
        return self + (-Eis._c(o))

    def __rsub__(self, o):
        return Eis._c(o) + (-self)

    def __mul__(self, o):
        o = Eis._c(o)
        # (a+b w)(c+d w) = ac + (ad+bc) w + bd w^2, w^2 = -1-w
        ac, bd = self.a * o.a, self.b * o.b
        mid = self.a * o.b + self.b * o.a
        return Eis(ac - bd, mid - bd)
    __rmul__ = __mul__

    def __pow__(self, k):
        out = Eis(1, 0)
        for _ in range(k):
            out = out * self
        return out

    def __eq__(self, o):
        o = Eis._c(o)
        return self.a == o.a and self.b == o.b

    def __hash__(self):
        return hash((self.a, self.b))

    def __repr__(self):
        return f"({self.a}+{self.b}w)"


OMEGA = Eis(0, 1)
