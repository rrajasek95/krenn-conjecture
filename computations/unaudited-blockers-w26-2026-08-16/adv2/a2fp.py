#!/usr/bin/env python3
"""adv2 -- F_p search engine (HEURISTIC ONLY: a hit over F_p is NOT a
counterexample over Q; it must be lifted).  EXACT integer arithmetic mod p.

Key structural fact used everywhere (re-derived, checked in a2_pos.py):
  H_w = sum_{u != t} M(w)[t][u] * haf(M(w) - t - u)
so for FIXED z and fixed blocks not incident to t, every equation H_w = 0
is AFFINE-LINEAR in the 9*deg(t) Gamma cells at vertex t, and splits by
the letter w_t into three independent subsystems.  The "clean layer"
subsystem (Phi = 0 on clean words) is the z-free part of it.
"""
from __future__ import annotations

import os
import sys
from itertools import combinations

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a2lib as A                                                 # noqa: E402
import a2fast as FT                                               # noqa: E402
import w26_core as C                                              # noqa: E402

WIDX = FT.WIDX


# ------------------------------------------------------- F_p linear algebra
def rref_p(rows, ncols, p):
    M = [r[:] for r in rows]
    piv, r = [], 0
    for c in range(ncols):
        sel = None
        for i in range(r, len(M)):
            if M[i][c] % p:
                sel = i
                break
        if sel is None:
            continue
        M[r], M[sel] = M[sel], M[r]
        iv = pow(M[r][c], p - 2, p)
        M[r] = [(x * iv) % p for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] % p:
                f = M[i][c]
                M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    return M[:r], piv


def kernel_p(rows, ncols, p):
    if not rows:
        return [[int(i == k) for i in range(ncols)] for k in range(ncols)]
    Rw, piv = rref_p(rows, ncols, p)
    out = []
    for f in [c for c in range(ncols) if c not in piv]:
        v = [0] * ncols
        v[f] = 1
        for i, pc in enumerate(piv):
            v[pc] = (-Rw[i][f]) % p
        out.append(v)
    return out


def solve_affine_p(rows, rhs, ncols, p):
    """returns (particular solution, kernel basis) or (None, None)."""
    aug = [rows[i] + [rhs[i] % p] for i in range(len(rows))]
    Rw, piv = rref_p(aug, ncols + 1, p)
    if ncols in piv:
        return None, None
    sol = [0] * ncols
    for i, pc in enumerate(piv):
        sol[pc] = Rw[i][ncols]
    ker = kernel_p([r[:] for r in rows], ncols, p)
    return sol, ker


# ----------------------------------------------------------- geometry bits
class GeoP:
    _c = {}

    def __new__(cls, m):
        if m in cls._c:
            return cls._c[m]
        s = super().__new__(cls)
        s.m = m
        s.fm = FT.Fastm(m)
        s.G = A.Geo(m)
        s.nbr = {t: sorted({u for e in s.G.gam for u in e if t in e}
                           - {t}) for t in range(8)}
        # active singles per word index
        s.act = []
        for w in FT.WORDS:
            s.act.append(tuple(e for e in s.G.live if s.G.active(e, w)))
        # compiled hafnian tables for V - S, S a disjoint single set
        s.phi_t = s.fm.phi_tab()
        s.co_t = {e: s.fm.coef_tab(e) for e in s.G.live}
        s.mixed_i = [WIDX[w] for w in C.MIXED]
        s.clean_i = [WIDX[w] for w in s.G.clean]
        s.solo_i = {e: [WIDX[w] for w in s.G.solo[e]] for e in s.G.live}
        # z-monomial structure for the FULL H:  per word, list of
        # (tuple of singles, haf-table-key)
        s.hterms = None
        cls._c[m] = s
        return s

    def build_hterms(self):
        """for each mixed word: list of (single-tuple, index-tuple-list)."""
        if self.hterms is not None:
            return self.hterms
        out = {}
        for wi in self.mixed_i:
            w = FT.WORDS[wi]
            ac = self.act[wi]
            terms = []
            for k in range(0, len(ac) + 1):
                for S in combinations(ac, k):
                    vs = set()
                    ok = True
                    for e in S:
                        if e[0] in vs or e[1] in vs:
                            ok = False
                            break
                        vs.add(e[0])
                        vs.add(e[1])
                    if not ok:
                        continue
                    rest = tuple(v for v in range(8) if v not in vs)
                    tab = self.fm.haf_table(rest)[wi]
                    if not tab and rest:
                        continue
                    terms.append((S, tab))
            out[wi] = terms
        self.hterms = out
        return out


def ev_p(P, terms, p):
    t = 0
    for mono in terms:
        q = 1
        for i in mono:
            q = q * P[i] % p
        t += q
    return t % p


def phi_at(gp, P, wi, p):
    return ev_p(P, gp.phi_t[wi], p)


def coef_at(gp, P, e, wi, p):
    return ev_p(P, gp.co_t[e][wi], p)


def H_at(gp, P, z, wi, p):
    """full H_w over F_p from the disjoint-single-set expansion."""
    tot = 0
    for S, tab in gp.build_hterms()[wi]:
        c = 1
        for e in S:
            c = c * z[e] % p
        if c == 0:
            continue
        tot += c * ev_p(P, tab, p)
    return tot % p


# ------------------------------------------------------------ site solving
def site_rows_clean(gp, P, t, p):
    """rows of the clean system at vertex t, split by letter."""
    nb = gp.nbr[t]
    nc = 3 * len(nb)
    tabs = [gp.fm.haf_table(tuple(v for v in range(8)
                                  if v != t and v != u)) for u in nb]
    rows = {0: [], 1: [], 2: []}
    for wi in gp.clean_i:
        w = FT.WORDS[wi]
        r = [0] * nc
        for k, u in enumerate(nb):
            r[3 * k + w[u]] = (r[3 * k + w[u]] + ev_p(P, tabs[k][wi], p)) % p
        if any(r):
            rows[w[t]].append(r)
    return nb, nc, rows


def write_site(gp, P, t, nb, newv):
    for k, u in enumerate(nb):
        e = (min(t, u), max(t, u))
        for c in range(3):
            for d in range(3):
                if e[0] == t:
                    P[gp.fm.slot(e, c, d)] = newv[c][3 * k + d]
                else:
                    P[gp.fm.slot(e, d, c)] = newv[c][3 * k + d]


def rand_pt(gp, rng, p):
    return [rng.randrange(1, p) for _ in range(gp.fm.n)]


def site_solve_clean(gp, P, t, p, rng, tries=400):
    """re-solve vertex t's blocks so the whole clean layer holds exactly."""
    nb, nc, rows = site_rows_clean(gp, P, t, p)
    newv = {}
    for c in range(3):
        Kb = kernel_p(rows[c], nc, p)
        if not Kb:
            return False
        got = None
        for _ in range(tries):
            co = [rng.randrange(p) for _ in Kb]
            v = [sum(co[i] * Kb[i][j] for i in range(len(Kb))) % p
                 for j in range(nc)]
            if all(v):
                got = v
                break
        if got is None:
            return False
        newv[c] = got
    write_site(gp, P, t, nb, newv)
    return True


def make_clean(gp, rng, p, t=None, order=None):
    """random blocks + one site solve  ->  an exactly clean F_p point."""
    P = rand_pt(gp, rng, p)
    order = order or [t if t is not None else rng.randrange(8)]
    for tt in order:
        if not site_solve_clean(gp, P, tt, p, rng):
            return None
    if not all(P):
        return None
    for wi in gp.clean_i:
        if phi_at(gp, P, wi, p):
            return None
    return P


# ------------------------------------------------------------- diagnostics
def solo_fp(gp, P, e, p):
    pure = bad = 0
    rats = set()
    for wi in gp.solo_i[e]:
        c = coef_at(gp, P, e, wi, p)
        ph = phi_at(gp, P, wi, p)
        if c == 0:
            if ph:
                bad += 1
            continue
        r = (-ph) * pow(c, p - 2, p) % p
        rats.add(r)
        if r == 0:
            pure += 1
    return dict(n_pure=pure, n_bad=bad, n_rat=len(rats),
                survives=(pure == 0 and bad == 0 and len(rats) == 1
                          and 0 not in rats),
                ratio=(list(rats)[0] if len(rats) == 1 else None))


def resid_rows_fp(gp, P, p):
    live = gp.G.live
    idx = {e: i for i, e in enumerate(live)}
    n = len(live)
    out = []
    for wi in gp.mixed_i:
        ac = gp.act[wi]
        if not ac:
            continue
        deg2 = False
        for a, b in combinations(ac, 2):
            if len(set(a) | set(b)) != 4:
                continue
            rest = tuple(v for v in range(8) if v not in set(a) | set(b))
            if C.has_pm(gp.G.gs, rest):
                deg2 = True
                break
        if deg2:
            continue
        v = [0] * n
        for e in ac:
            v[idx[e]] = coef_at(gp, P, e, wi, p)
        c = phi_at(gp, P, wi, p)
        if any(v) or c:
            out.append((wi, v, c))
    return live, out


def verdict_fp(gp, P, p):
    live, rows = resid_rows_fp(gp, P, p)
    n = len(live)
    aug = [list(v) + [(-c) % p] for _, v, c in rows]
    Rw, piv = rref_p(aug, n + 1, p)
    if n in piv:
        return dict(n=n, rows=len(rows), rank=len(piv), inconsistent=True,
                    killed=True, forced=[], z=None)
    sol = [0] * n
    for i, pc in enumerate(piv):
        if pc < n:
            sol[pc] = Rw[i][n]
    ker = kernel_p([list(v) for _, v, _ in rows], n, p)
    forced = [str(live[i]) for i in range(n)
              if sol[i] == 0 and all(b[i] == 0 for b in ker)]
    return dict(n=n, rows=len(rows), rank=len(piv), inconsistent=False,
                dim=len(ker), forced=forced, killed=bool(forced),
                z={str(live[i]): sol[i] for i in range(n)},
                zvec=sol, ker=ker, live=[str(e) for e in live])


def profile(gp, P, p):
    """one-line profile of a clean F_p point."""
    van = all(phi_at(gp, P, WIDX[w], p) == 0 for w in FT.WORDS)
    surv = [str(e) for e in gp.G.live if solo_fp(gp, P, e, p)["survives"]]
    v = verdict_fp(gp, P, p)
    return dict(stratum=van, solo_surv=surv, killed=v["killed"],
                inconsistent=v.get("inconsistent"), rank=v["rank"],
                forced=v.get("forced"))
