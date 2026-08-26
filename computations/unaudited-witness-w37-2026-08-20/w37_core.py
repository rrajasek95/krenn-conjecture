"""W37 core engine -- UNAUDITED probe lane (2026-08-20).

Written from scratch from the statements in
  proofs/clean-pair-cap-exact-descent.md   (the descent + cap error)
  notes/2026-08-15-conventions-and-hazards.md  (off-count, X_k)
so that it is an INDEPENDENT second family against
  computations/unaudited-x3core-w25-2026-08-15/w25_core.py.

Nothing here imports W25/W27 code.  Cross-family agreement is checked in
run_a0_controls.py.

Conventions (pinned to OBJECT_W25-F8's `orientation` field):
  A source on N sites is  src[(u,v)] = 3x3 matrix, u < v, with
  src[(u,v)][i][j] = coefficient of colour i at site u, colour j at site v.
  H_w(A) = sum over perfect matchings M of K_N of prod_{(u,v) in M} A_uv[w_u][w_v].

  off(w) = N - max_c |w^{-1}(c)|;  X_k imposes  H_w = 1 on the three
  constant words and H_w = 0 on every mixed word with off(w) <= k.

Cap error, h = |U|/2, U = V - {p,q}:
  s      = <K, A_pq>                                   (linear in K)
  R_ab[ca][cb] = sum_ij K_ij (A_pa[i][ca] A_qb[j][cb]
                            + A_qa[j][ca] A_pb[i][cb])  (linear in K)
  E_pq(K)_w = sum_{k=2}^{h} s^{h-k} [ r^k/k! exp(x) ]_U
            = sum over perfect matchings M of U of
                 sum_{J subset M, |J| >= 2} s^{h-|J|}
                     prod_{f in J} R_f(w) prod_{f in M-J} A_f(w).
  (the |J| = 0,1 terms are exactly the cap contribution -- see the
   W22-M identity re-derived in NOTES.md)
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import json
import os

NCOL = 3

# ----------------------------------------------------------------- utilities


def ekey(u, v):
    return (u, v) if u < v else (v, u)


def block(src, u, v, ncol=NCOL):
    """A_uv with FIRST index = colour at u, second = colour at v (any order)."""
    if u < v:
        return src[(u, v)]
    m = src[(v, u)]
    return [[m[j][i] for j in range(ncol)] for i in range(ncol)]


def sites_of(src):
    return 1 + max(max(k) for k in src)


def is_live(src, u, v, ncol=NCOL):
    return any(x != 0 for row in block(src, u, v, ncol) for x in row)


def zeros(n, ncol=NCOL, zero=Fraction(0)):
    return {(u, v): [[zero] * ncol for _ in range(ncol)]
            for u, v in combinations(range(n), 2)}


def parse_source(blocks_json, n, conv=Fraction):
    src = {}
    for key, mat in blocks_json.items():
        u, v = (int(t) for t in key.split(","))
        src[ekey(u, v)] = [[conv(x) for x in row] for row in mat]
    for u, v in combinations(range(n), 2):
        src.setdefault((u, v), [[conv(0)] * NCOL for _ in range(NCOL)])
    return src


# ------------------------------------------------------- perfect matchings

_PM_CACHE: dict[tuple, tuple] = {}


def perfect_matchings(sites):
    """All perfect matchings of the complete graph on `sites` (a tuple)."""
    sites = tuple(sites)
    if sites in _PM_CACHE:
        return _PM_CACHE[sites]
    if not sites:
        out = ((),)
    else:
        a, rest = sites[0], sites[1:]
        out = tuple(((a, rest[i]),) + m
                    for i in range(len(rest))
                    for m in perfect_matchings(rest[:i] + rest[i + 1:]))
    _PM_CACHE[sites] = out
    return out


def haf_word(src, word, sites=None, ncol=NCOL, zero=Fraction(0)):
    """H_w restricted to `sites` (default all).  word is a dict or a tuple
    indexed by absolute site number."""
    if sites is None:
        sites = tuple(range(len(word)))
    tot = zero
    for M in perfect_matchings(sites):
        term = None
        for (u, v) in M:
            val = block(src, u, v, ncol)[word[u]][word[v]]
            term = val if term is None else term * val
            if term == 0:
                break
        if term is not None and term != 0:
            tot = tot + term
    return tot


# ------------------------------------------------------------- the ladder


def offcount(word, ncol=NCOL):
    return len(word) - max(word.count(c) for c in range(ncol))


def all_words(n, ncol=NCOL):
    return product(range(ncol), repeat=n)


def profile(word, ncol=NCOL):
    return tuple(sorted((word.count(c) for c in range(ncol)), reverse=True))


def defects(src, n, ncol=NCOL, kmax=None):
    """Every mixed word (with off(w) <= kmax if given) on which H_w != 0,
    plus the three pure values.  Returns (pures, {word: value})."""
    pures = []
    for c in range(ncol):
        pures.append(haf_word(src, (c,) * n, tuple(range(n)), ncol))
    bad = {}
    for w in all_words(n, ncol):
        if len(set(w)) == 1:
            continue
        if kmax is not None and offcount(w, ncol) > kmax:
            continue
        h = haf_word(src, w, tuple(range(n)), ncol)
        if h != 0:
            bad[w] = h
    return pures, bad


def in_Xk(src, n, k, ncol=NCOL):
    pures, bad = defects(src, n, ncol, kmax=k)
    return all(p == 1 for p in pures) and not bad


# ------------------------------------------------------------- cap algebra


def cap_s(src, p, q, K, ncol=NCOL):
    A = block(src, p, q, ncol)
    tot = 0
    for i in range(ncol):
        for j in range(ncol):
            if K[i][j] != 0 and A[i][j] != 0:
                tot = tot + K[i][j] * A[i][j]
    return tot


def cap_R(src, p, q, K, sites, ncol=NCOL, zero=Fraction(0)):
    """R_ab as a dict keyed by unordered pair, first index = colour at the
    SMALLER site."""
    R = {}
    for a, b in combinations(sorted(sites), 2):
        Apa, Aqa = block(src, p, a, ncol), block(src, q, a, ncol)
        Apb, Aqb = block(src, p, b, ncol), block(src, q, b, ncol)
        mat = [[zero] * ncol for _ in range(ncol)]
        for ca in range(ncol):
            for cb in range(ncol):
                tot = zero
                for i in range(ncol):
                    for j in range(ncol):
                        k = K[i][j]
                        if k == 0:
                            continue
                        t = Apa[i][ca] * Aqb[j][cb] + Aqa[j][ca] * Apb[i][cb]
                        if t != 0:
                            tot = tot + k * t
                mat[ca][cb] = tot
        R[(a, b)] = mat
    return R


def _get(tab, u, v, cu, cv):
    return tab[(u, v)][cu][cv] if u < v else tab[(v, u)][cv][cu]


def cap_error_def(src, p, q, K, sites, ncol=NCOL, zero=Fraction(0)):
    """E_pq(K) BY THE DEFINITION (sum over matchings of U, over subsets J of
    the matching with |J| >= 2 carrying the R edge)."""
    sites = tuple(sorted(sites))
    h = len(sites) // 2
    s = cap_s(src, p, q, K, ncol)
    R = cap_R(src, p, q, K, sites, ncol, zero)
    out = {}
    for w in all_words(len(sites), ncol):
        wd = {a: w[i] for i, a in enumerate(sites)}
        tot = zero
        for M in perfect_matchings(sites):
            rv = [_get(R, u, v, wd[u], wd[v]) for (u, v) in M]
            av = [block(src, u, v, ncol)[wd[u]][wd[v]] for (u, v) in M]
            for size in range(2, h + 1):
                for J in combinations(range(h), size):
                    term = s ** (h - size)
                    if term == 0:
                        continue
                    for idx in range(h):
                        term = term * (rv[idx] if idx in J else av[idx])
                        if term == 0:
                            break
                    if term != 0:
                        tot = tot + term
        if tot != 0:
            out[w] = tot
    return out


def cap_error_wm(src, p, q, K, sites, n=None, ncol=NCOL, zero=Fraction(0)):
    """E_pq(K) BY THE W22-M CLOSED FORM
         E_w = Haf_U(sA + R)_w - s^{h-1} sum_ij K_ij H_B(w, i@p, j@q).
    Independent code path; must agree with cap_error_def."""
    sites = tuple(sorted(sites))
    h = len(sites) // 2
    if n is None:
        n = sites_of(src)
    s = cap_s(src, p, q, K, ncol)
    R = cap_R(src, p, q, K, sites, ncol, zero)
    out = {}
    for w in all_words(len(sites), ncol):
        wd = {a: w[i] for i, a in enumerate(sites)}
        first = zero
        for M in perfect_matchings(sites):
            term = None
            for (u, v) in M:
                val = (s * block(src, u, v, ncol)[wd[u]][wd[v]]
                       + _get(R, u, v, wd[u], wd[v]))
                term = val if term is None else term * val
                if term == 0:
                    break
            if term is not None and term != 0:
                first = first + term
        kc = zero
        for i in range(ncol):
            for j in range(ncol):
                if K[i][j] == 0:
                    continue
                full = dict(wd)
                full[p], full[q] = i, j
                fw = tuple(full[t] for t in range(n))
                hv = haf_word(src, fw, tuple(range(n)), ncol)
                if hv != 0:
                    kc = kc + K[i][j] * hv
        val = first - (s ** (h - 1)) * kc
        if val != 0:
            out[w] = val
    return out


def admissible(src, p, q, K, ncol=NCOL):
    return all(K[c][c] != 0 for c in range(ncol)) and cap_s(src, p, q, K, ncol) != 0


# ------------------------------------------- symbolic cap error (K unknown)
# A polynomial in the 9 cap unknowns k00..k22 is a dict
#   {exponent-tuple(9) : coefficient}

KVARS = [f"k{i}{j}" for i in range(NCOL) for j in range(NCOL)]


def _pmul(f, g):
    out = {}
    for e1, c1 in f.items():
        for e2, c2 in g.items():
            e = tuple(a + b for a, b in zip(e1, e2))
            out[e] = out.get(e, 0) + c1 * c2
    return {e: c for e, c in out.items() if c != 0}


def _padd(f, g):
    out = dict(f)
    for e, c in g.items():
        out[e] = out.get(e, 0) + c
        if out[e] == 0:
            del out[e]
    return out


def _pconst(c):
    return {} if c == 0 else {(0,) * 9: c}


def _pvar(idx, coef=1):
    e = [0] * 9
    e[idx] = 1
    return {} if coef == 0 else {tuple(e): coef}


def sym_cap_system(src, p, q, sites, ncol=NCOL):
    """The full E_pq(K) system as polynomials in k00..k22, plus s.

    Returns (polys, s_poly) where polys is a list over the 3^|U| words."""
    sites = tuple(sorted(sites))
    h = len(sites) // 2
    n = sites_of(src)
    A = block(src, p, q, ncol)
    s = {}
    for i in range(ncol):
        for j in range(ncol):
            if A[i][j] != 0:
                s = _padd(s, _pvar(i * ncol + j, A[i][j]))
    R = {}
    for a, b in combinations(sites, 2):
        Apa, Aqa = block(src, p, a, ncol), block(src, q, a, ncol)
        Apb, Aqb = block(src, p, b, ncol), block(src, q, b, ncol)
        mat = [[{} for _ in range(ncol)] for _ in range(ncol)]
        for ca in range(ncol):
            for cb in range(ncol):
                acc = {}
                for i in range(ncol):
                    for j in range(ncol):
                        t = Apa[i][ca] * Aqb[j][cb] + Aqa[j][ca] * Apb[i][cb]
                        if t != 0:
                            acc = _padd(acc, _pvar(i * ncol + j, t))
                mat[ca][cb] = acc
        R[(a, b)] = mat
    spow = [_pconst(1)]
    for _ in range(h):
        spow.append(_pmul(spow[-1], s))
    polys = []
    for w in all_words(len(sites), ncol):
        wd = {a: w[i] for i, a in enumerate(sites)}
        tot = {}
        for M in perfect_matchings(sites):
            rv = [_get(R, u, v, wd[u], wd[v]) for (u, v) in M]
            av = [block(src, u, v, ncol)[wd[u]][wd[v]] for (u, v) in M]
            for size in range(2, h + 1):
                for J in combinations(range(h), size):
                    term = spow[h - size]
                    for idx in range(h):
                        if idx in J:
                            term = _pmul(term, rv[idx])
                        else:
                            if av[idx] == 0:
                                term = {}
                            else:
                                term = {e: c * av[idx] for e, c in term.items()}
                        if not term:
                            break
                    if term:
                        tot = _padd(tot, term)
        if tot:
            polys.append((w, tot))
    return polys, s


def poly_str(f, names=None):
    names = names or KVARS
    parts = []
    for e, c in sorted(f.items()):
        mon = "*".join(f"{names[i]}^{k}" if k > 1 else names[i]
                       for i, k in enumerate(e) if k)
        num = Fraction(c)
        cs = f"({num.numerator}/{num.denominator})" if num.denominator != 1 \
            else f"({num.numerator})"
        parts.append(cs + ("*" + mon if mon else ""))
    return " + ".join(parts) if parts else "0"


# ---------------------------------------------------------------- checkpoint


def ckpt(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(obj, fh, indent=1, default=str)
    os.replace(tmp, path)
