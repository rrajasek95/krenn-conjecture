#!/usr/bin/env python3
"""W21 MOVE 1 -- the site machinery (independent re-implementation of W20-L
and W20-R) plus an exact descent that lands ON the clean layer.
UNAUDITED.  Exact rational arithmetic only.

Vocabulary (fixed here, used by every W21 move-1 script):
  N(t)          Gamma-neighbours of t;  deg t = |N(t)|
  g^t_s(w)      = haf(Gamma - t - s)(w)   -- the W20-L coefficient; it does
                  not depend on w_t and does not depend on w_s
  common word   a clean word w such that all three recolourings of site t
                  are also clean
  M_cap^(t)     the matrix with one row per common word w, entry
                  g^t_s(w) in column (s, w_s); K_cap = ker M_cap
  V_c           the site-t vector (A_ts[c][d])_{s,d} in C^{3 deg t}
  Then V_0,V_1,V_2 in K_cap, so  dim K_cap = 1  =>  site t FACTORS.
  W(t) = row space of M_cap;  dim K_cap = 3 deg t - dim W(t).
  B(p)[c][i] = A_{t s_i}[c][p_i]   (3 x deg t) for a pattern p
  U(p)       = span of the coefficient vectors g^t(w) over common words w
               with w|_{N(t)} = p;   rowspace B(p) perp U(p), so
               rank B(p) <= deg t - dim U(p).
  p REGULAR  <=>  dim U(p) = deg t - 1  =>  rank B(p) = 1  =>  the deg t
               columns a_{s,p_s} of the site are pairwise proportional.
  site t factors  <=>  all 3 deg t columns a_{s,d} in C^3 are pairwise
               proportional  <=>  rank B(p) = 1 for every pattern p.
"""
from __future__ import annotations

import random
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
import w21_core as K


def common_words(clean, t):
    cl = set(clean)
    return [w for w in clean
            if all(tuple(c if i == t else w[i] for i in range(8)) in cl
                   for c in range(3))]


def coeff_rows(blocks, gam, t, words):
    """(nbr, ncols, rows-by-colour, raw coefficient vectors)."""
    nb = K.neighbours(gam, t)
    ncols = 3 * len(nb)
    ES = set(gam)
    rows = {0: [], 1: [], 2: []}
    raw = []
    for w in words:
        g = []
        for s in nb:
            vs = [v for v in range(8) if v != t and v != s]
            g.append(K.haf_verts(blocks, ES, vs, w))
        raw.append((w, g))
        r = [Fraction(0)] * ncols
        for k, s in enumerate(nb):
            r[3 * k + w[s]] += g[k]
        if any(r):
            rows[w[t]].append(r)
    return nb, ncols, rows, raw


def site_report(blocks, gam, t, clean):
    nb = K.neighbours(gam, t)
    deg = len(nb)
    cw = common_words(clean, t)
    _, ncols, rows, raw = coeff_rows(blocks, gam, t, cw)
    allrows = []
    seen = set()
    for c in range(3):
        for r in rows[c]:
            k = tuple(r)
            if k not in seen:
                seen.add(k)
                allrows.append(r)
    dimW = K.rank_of(allrows, ncols)
    Kcap = ncols - dimW
    # patterns
    pats = {}
    for w, g in raw:
        pats.setdefault(tuple(w[s] for s in nb), []).append(g)
    reg, nonreg = [], []
    for p, gs in pats.items():
        (reg if K.rank_of(gs, deg) == deg - 1 else nonreg).append(p)
    # column proportionality classes
    _, cols = K.site_columns(blocks, gam, t)
    slots = [(s, d) for s in nb for d in range(3)]
    par = {sl: sl for sl in slots}

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            par[ra] = rb

    for i in range(len(slots)):
        for j in range(i + 1, len(slots)):
            if K.proportional(cols[slots[i]], cols[slots[j]]):
                union(slots[i], slots[j])
    classes = {}
    for sl in slots:
        classes.setdefault(find(sl), []).append(sl)
    # merge graph induced by the REGULAR patterns only (W20-R chaining)
    par2 = {sl: sl for sl in slots}

    def find2(a):
        while par2[a] != a:
            par2[a] = par2[par2[a]]
            a = par2[a]
        return a

    for p in reg:
        base = (nb[0], p[0])
        for k in range(1, deg):
            ra, rb = find2(base), find2((nb[k], p[k]))
            if ra != rb:
                par2[ra] = rb
    comp2 = len({find2(sl) for sl in slots})
    return dict(site=t, deg=deg, n_common=len(cw), dimW=dimW,
                dim_Kcap=Kcap, factors=K.factors_at(blocks, gam, t),
                n_patterns=len(pats), n_regular=len(reg),
                n_nonregular=len(nonreg),
                nonregular=[list(p) for p in sorted(nonreg)],
                regular_merge_components=comp2,
                criterion_proves_factoring=(comp2 == 1),
                n_column_classes=len(classes),
                column_class_sizes=sorted(len(v) for v in classes.values()),
                column_classes=[sorted([list(s) for s in v])
                                for v in classes.values()],
                block_ranks={str(s): K.rank_of(
                    [[blocks[(min(t, s), max(t, s))][a][b] for b in range(3)]
                     for a in range(3)] if t < s else
                    [[blocks[(min(t, s), max(t, s))][b][a] for b in range(3)]
                     for a in range(3)], 3) for s in nb})


# --------------------------------------------------------------- descent
def jpoint(gam, rng, tries=400):
    F = K.pms_inside(gam)
    for _ in range(tries):
        t = {e: Fraction(rng.randint(-9, 9) or 3, rng.randint(1, 4))
             for e in gam}
        e0 = gam[rng.randrange(len(gam))]
        a = b = Fraction(0)
        for mi in F:
            m = K.PMS[mi]
            p = Fraction(1)
            has = False
            for e in m:
                if e == e0:
                    has = True
                else:
                    p *= t[e]
            if has:
                a += p
            else:
                b += p
        if a == 0:
            continue
        t[e0] = -b / a
        if all(v != 0 for v in t.values()):
            return {e: [[t[e]] * 3 for _ in range(3)] for e in gam}
    return None


def write_site(blocks, gam, t, nb, v):
    for k, s in enumerate(nb):
        e = (min(t, s), max(t, s))
        for c in range(3):
            for d in range(3):
                if e[0] == t:
                    blocks[e][c][d] = v[c][3 * k + d]
                else:
                    blocks[e][d][c] = v[c][3 * k + d]


def descent(gam, clean, rng, order=None, passes=4, blocks=None):
    """exact block-coordinate descent inside the clean layer."""
    if blocks is None:
        blocks = jpoint(gam, rng)
    if blocks is None:
        return None
    order = list(range(8)) if order is None else list(order)
    for _ in range(passes):
        for t in order:
            nb, ncols, rows, _ = coeff_rows(blocks, gam, t, clean)
            newv, ok = {}, True
            for c in range(3):
                Kb = K.kernel_basis(rows[c], ncols)
                if not Kb:
                    ok = False
                    break
                for _try in range(120):
                    coef = [Fraction(rng.randint(-7, 7)) for _ in Kb]
                    v = [sum(coef[i] * Kb[i][j] for i in range(len(Kb)))
                         for j in range(ncols)]
                    if all(z != 0 for z in v):
                        break
                else:
                    ok = False
                    break
                newv[c] = v
            if not ok:
                continue
            save = {e: [r[:] for r in blocks[e]] for e in gam}
            write_site(blocks, gam, t, nb, newv)
            if not all(K.phi_value(blocks, gam, w) == 0 for w in clean):
                for e in gam:
                    blocks[e] = save[e]
    return blocks
