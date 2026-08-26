#!/usr/bin/env python3
"""A6 AUDIT -- independent engine for the cap-error algebra (W14 target).

Written from notes/clean-pair-cap-exact-descent-target.md alone.  Nothing
here imports w13_*/w14_*/p2 code.  Two INDEPENDENT routes to E_w:
  (S) the square-free ("site-square-zero") algebra with the note's
      factorials  E = sum_{k=2}^h s^{h-k} r^k x^{h-k} / (k! (h-k)!),
      full-U-support component  -- eq (4) LITERALLY, factorials included;
  (M) the matching-sum expansion.
Agreement of (S) and (M) is the factorial-normalisation check.

Conventions: p = 0, q = 1, U = (2, ..., 2h+1).  Blocks src[(u,v)] with
u < v, row index = colour at u.  Cap variables K_ij -> index 3i+j.
"""
from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, permutations, product

COL = (0, 1, 2)
NK = 9


def kx(i, j):
    return 3 * i + j


# ------------------------------------------------------------ polynomials
def padd(a, b):
    o = dict(a)
    for m, c in b.items():
        n = o.get(m, 0) + c
        if n:
            o[m] = n
        else:
            o.pop(m, None)
    return o


def pmul(a, b):
    o = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            k = tuple(sorted(ma + mb))
            n = o.get(k, 0) + ca * cb
            if n:
                o[k] = n
            else:
                o.pop(k, None)
    return o


def pscale(a, c):
    return {} if c == 0 else {m: v * c for m, v in a.items()}


def ppow(a, n):
    o = {(): 1}
    for _ in range(n):
        o = pmul(o, a)
    return o


def pev(a, pt):
    t = Fraction(0)
    for m, c in a.items():
        x = Fraction(c)
        for v in m:
            x *= pt[v]
        t += x
    return t


@lru_cache(maxsize=None)
def monos(nv, d):
    return tuple(combinations_with_replacement(range(nv), d))


@lru_cache(maxsize=None)
def midx(nv, d):
    return {m: i for i, m in enumerate(monos(nv, d))}


def prow(f, d, nv=NK):
    ix = midx(nv, d)
    v = [0] * len(ix)
    for m, c in f.items():
        assert len(m) == d, (m, d)
        v[ix[m]] += c
    return v


# ------------------------------------------------------------- structure
def sites(h):
    return 0, 1, tuple(range(2, 2 + 2 * h))


@lru_cache(maxsize=None)
def pms(vs):
    """perfect matchings of a tuple of sites"""
    if not vs:
        return ((),)
    out = []
    a = vs[0]
    for i in range(1, len(vs)):
        rest = vs[1:i] + vs[i + 1:]
        for t in pms(rest):
            out.append(((a, vs[i]),) + t)
    return tuple(out)


@lru_cache(maxsize=None)
def partial_ms(vs, k):
    """sets of k disjoint pairs from vs"""
    if k == 0:
        return ((),)
    if len(vs) < 2 * k:
        return ()
    out = []
    for i in range(len(vs)):
        for j in range(i + 1, len(vs)):
            a, b = vs[i], vs[j]
            rest = tuple(v for v in vs if v not in (a, b))
            for t in partial_ms(rest, k - 1):
                if t and (a, b) > t[0]:
                    continue
                out.append(((a, b),) + t)
    return tuple(out)


def blk(src, u, v, cu, cv):
    return src[(u, v)][cu][cv] if u < v else src[(v, u)][cv][cu]


def s_form(src):
    """the linear form s = <K, A_pq>"""
    A = src[(0, 1)]
    return {(kx(i, j),): A[i][j] for i in COL for j in COL if A[i][j]}


def R_form(src, h, a, b, ca, cb):
    """R_ab(ca,cb) as a linear form in K"""
    f = {}
    for i in COL:
        for j in COL:
            val = (blk(src, 0, a, i, ca) * blk(src, 1, b, j, cb)
                   + blk(src, 0, b, i, cb) * blk(src, 1, a, j, ca))
            if val:
                key = (kx(i, j),)
                f[key] = f.get(key, 0) + val
    return {m: c for m, c in f.items() if c}


# --------------------------------------------- route (M): matching sums
def Ew_matchings(src, h, word):
    """E_w by the matching-sum expansion (factorials cleared)."""
    _, _, U = sites(h)
    slot = {a: n for n, a in enumerate(U)}
    sp = s_form(src)
    tot = {}
    for M in pms(U):
        Rs = {e: R_form(src, h, e[0], e[1], word[slot[e[0]]], word[slot[e[1]]])
              for e in M}
        xs = {e: blk(src, e[0], e[1], word[slot[e[0]]], word[slot[e[1]]])
              for e in M}
        for js in range(0, h - 1):          # |J| = js  <=>  k = h - js >= 2
            for J in combinations(M, js):
                wgt = 1
                for e in J:
                    wgt *= xs[e]
                if wgt == 0:
                    continue
                term = {(): wgt}
                for e in M:
                    if e in J:
                        continue
                    term = pmul(term, Rs[e])
                    if not term:
                        break
                if not term:
                    continue
                if js:
                    term = pmul(term, ppow(sp, js))
                tot = padd(tot, term)
    return tot


# ----------------------------- route (S): the square-free algebra, eq (4)
# element: dict  (frozenset-as-sorted-tuple of sites, tuple of colours) -> poly
def sf_mul(A, B, maxsup):
    out = {}
    for (T1, c1), p1 in A.items():
        s1 = set(T1)
        for (T2, c2), p2 in B.items():
            if s1 & set(T2):
                continue
            if len(T1) + len(T2) > maxsup:
                continue
            merged = sorted(zip(T1 + T2, c1 + c2))
            key = (tuple(t for t, _ in merged), tuple(c for _, c in merged))
            pr = pmul(p1, p2)
            if pr:
                out[key] = padd(out.get(key, {}), pr)
    return {k: v for k, v in out.items() if v}


def sf_x(src, h):
    _, _, U = sites(h)
    out = {}
    for a, b in combinations(U, 2):
        for ca in COL:
            for cb in COL:
                v = blk(src, a, b, ca, cb)
                if v:
                    out[((a, b), (ca, cb))] = {(): v}
    return out


def sf_r(src, h):
    _, _, U = sites(h)
    out = {}
    for a, b in combinations(U, 2):
        for ca in COL:
            for cb in COL:
                f = R_form(src, h, a, b, ca, cb)
                if f:
                    out[((a, b), (ca, cb))] = f
    return out


def Ew_squarefree(src, h):
    """eq (4) LITERALLY, with the note's 1/k! and 1/(h-k)! -> dict word->poly."""
    _, _, U = sites(h)
    n = 2 * h
    x = sf_x(src, h)
    r = sf_r(src, h)
    sp = s_form(src)
    total = {}
    for k in range(2, h + 1):
        rk = {((), ()): {(): 1}}
        for _ in range(k):
            rk = sf_mul(rk, r, n)
        xj = {((), ()): {(): 1}}
        for _ in range(h - k):
            xj = sf_mul(xj, x, n)
        pr = sf_mul(rk, xj, n)
        fk = 1
        for t in range(2, k + 1):
            fk *= t
        fh = 1
        for t in range(2, h - k + 1):
            fh *= t
        den = Fraction(1, fk * fh)
        spow = ppow(sp, h - k)
        for (T, c), poly in pr.items():
            if len(T) != n:
                continue
            assert tuple(T) == U
            term = pmul(poly, spow)
            term = {m: Fraction(cc) * den for m, cc in term.items()}
            total[c] = padd(total.get(c, {}), term)
    return total


# --------------------------------------------- rank-one slices / levels
def alpha_of(src, u, v):
    A = src[(0, 1)]
    return sum(u[i] * v[j] * A[i][j] for i in COL for j in COL)


def slice_R(src, h, word, u, v, a, b):
    slot = {x: n for n, x in enumerate(sites(h)[2])}
    ua = sum(u[i] * blk(src, 0, a, i, word[slot[a]]) for i in COL)
    ub = sum(u[i] * blk(src, 0, b, i, word[slot[b]]) for i in COL)
    va = sum(v[j] * blk(src, 1, a, j, word[slot[a]]) for j in COL)
    vb = sum(v[j] * blk(src, 1, b, j, word[slot[b]]) for j in COL)
    return ua * vb + ub * va


def haf_slice(src, h, word, u, v, subset):
    tot = 0
    for M in pms(tuple(subset)):
        t = 1
        for a, b in M:
            t *= slice_R(src, h, word, u, v, a, b)
            if t == 0:
                break
        tot += t
    return tot


def haf_slice_closed(src, h, word, u, v, subset):
    """A6's proof of W14.1: k! * sum_{|S|=k} prod_S <u,P> prod_{S^c} <v,Q>."""
    slot = {x: n for n, x in enumerate(sites(h)[2])}
    subset = tuple(subset)
    k = len(subset) // 2
    up = {a: sum(u[i] * blk(src, 0, a, i, word[slot[a]]) for i in COL)
          for a in subset}
    vq = {a: sum(v[j] * blk(src, 1, a, j, word[slot[a]]) for j in COL)
          for a in subset}
    tot = 0
    for S in combinations(subset, k):
        t = 1
        for a in S:
            t *= up[a]
        for b in subset:
            if b not in S:
                t *= vq[b]
        tot += t
    f = 1
    for t in range(2, k + 1):
        f *= t
    return f * tot


def G_level(src, h, word, u, v, j):
    _, _, U = sites(h)
    slot = {x: n for n, x in enumerate(U)}
    tot = 0
    for J in partial_ms(U, j):
        wgt = 1
        for a, b in J:
            wgt *= blk(src, a, b, word[slot[a]], word[slot[b]])
            if wgt == 0:
                break
        if wgt == 0:
            continue
        used = {a for e in J for a in e}
        free = tuple(a for a in U if a not in used)
        tot += wgt * haf_slice(src, h, word, u, v, free)
    return tot


# ------------------------------------------------------- Sigma_k, iota_k
@lru_cache(maxsize=None)
def sigma_pairs(k):
    ms = monos(3, k)
    return tuple((mu, nu) for mu in ms for nu in ms)


@lru_cache(maxsize=None)
def iota(k, mu, nu):
    acc = {}
    for sg in permutations(range(k)):
        key = tuple(sorted(kx(mu[t], nu[sg[t]]) for t in range(k)))
        acc[key] = acc.get(key, 0) + 1
    return tuple(sorted(acc.items()))


def iota_poly(k, mu, nu):
    return dict(iota(k, mu, nu))


def L_rows(h, A):
    """rows spanning L_h(A) = sum_{k=2}^h s^{h-k} iota_k(Sigma_k)."""
    sp = {(kx(i, j),): A[i][j] for i in COL for j in COL if A[i][j]}
    rows, tags = [], []
    for k in range(2, h + 1):
        sp2 = ppow(sp, h - k)
        for mu, nu in sigma_pairs(k):
            f = iota_poly(k, mu, nu)
            if h - k:
                f = pmul(f, sp2)
            rows.append(prow(f, h) if f else [0] * len(midx(NK, h)))
            tags.append((k, mu, nu))
    return rows, tags


# --------------------------------------------------- exact linear algebra
def rref(rows):
    M = [[Fraction(x) for x in r] for r in rows]
    nc = len(M[0]) if M else 0
    piv, rr = [], 0
    for c in range(nc):
        p = None
        for r in range(rr, len(M)):
            if M[r][c]:
                p = r
                break
        if p is None:
            continue
        M[rr], M[p] = M[p], M[rr]
        iv = 1 / M[rr][c]
        M[rr] = [z * iv for z in M[rr]]
        pr = M[rr]
        for r in range(len(M)):
            if r != rr and M[r][c]:
                f = M[r][c]
                M[r] = [a - f * b for a, b in zip(M[r], pr)]
        piv.append(c)
        rr += 1
        if rr == len(M):
            break
    return M[:rr], piv


def in_span(basis, piv, tgt):
    v = [Fraction(x) for x in tgt]
    for r, c in enumerate(piv):
        if v[c]:
            f = v[c]
            v = [a - f * b for a, b in zip(v, basis[r])]
    return all(x == 0 for x in v)


def rank_mod_p(rows, p=(1 << 61) - 1):
    M = [[x % p for x in r] for r in rows]
    nc = len(M[0]) if M else 0
    rr = 0
    for c in range(nc):
        piv = None
        for r in range(rr, len(M)):
            if M[r][c] % p:
                piv = r
                break
        if piv is None:
            continue
        M[rr], M[piv] = M[piv], M[rr]
        iv = pow(M[rr][c], p - 2, p)
        M[rr] = [(z * iv) % p for z in M[rr]]
        for r in range(len(M)):
            if r != rr and M[r][c] % p:
                f = M[r][c]
                M[r] = [(a - f * b) % p for a, b in zip(M[r], M[rr])]
        rr += 1
        if rr == len(M):
            break
    return rr


def det3(A):
    return (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
            - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
            + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))


def rank3(A):
    return len(rref([[Fraction(x) for x in r] for r in A])[1])


def rnd_source(h, rng, lo=-4, hi=4):
    P, Q, U = sites(h)
    return {(u, v): [[rng.randint(lo, hi) for _ in COL] for _ in COL]
            for u, v in combinations((P, Q) + U, 2)}


def l_mono_poly(a, b, A):
    """s^a * prod_c kappa_c^{b_c}"""
    sp = {(kx(i, j),): A[i][j] for i in COL for j in COL if A[i][j]}
    f = ppow(sp, a)
    for c in COL:
        for _ in range(b[c]):
            f = pmul(f, {(kx(c, c),): 1})
    return f
