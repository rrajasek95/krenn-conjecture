#!/usr/bin/env python3
"""W19 -- THE SECOND-ORDER OBSTRUCTION AT A J-POINT.  UNAUDITED, exact.

Theorem W19-A gives the first-order picture; this module computes the next
order, which is where a forcing proof must live when min deg_Gamma >= 3.

SET-UP.  A_e = t_e J + eps dA_e + eps^2 dA'_e + ...,  haf_Gamma(t) = 0.
    Phi_w = eps * sum_e c_e dA_e[w_u][w_v]
          + eps^2 * ( sum_e c_e dA'_e[w] + sum_{e,f disjoint} c_{ef}
                        dA_e[w] dA_f[w] ) + O(eps^3),
    c_e   = sum_{M in F, e in M} prod_{M \\ e} t,
    c_ef  = sum_{M in F, {e,f} in M} prod_{M \\ {e,f}} t   (0 if e,f meet).
Order 1 is Theorem W19-A: dA_e[i][j] = (mu_e + a_e(i) + b_e(j))/c_e with
sum_e mu_e = 0 and sum_{e at t} a_e^(t) = 0 for every site t.

ORDER 2, ALL WORDS (proved here by the ANOVA calculus).  The quadratic term
Q(w) = sum_{e,f disjoint} c_ef dA_e[w] dA_f[w] must be absorbable by the
linear map z -> sum_e c_e z_e[w_u][w_v], whose image is exactly the span of
functions with all interactions of order <= 2 and supported on GAMMA pairs.
Each dA_e is ADDITIVE (no 2-way interaction), and for disjoint e, f the
ANOVA components of the product multiply, so Q has NO interaction of order
>= 3 and its order-2 components sit on pairs {u, x} with u in e, x in f.
Therefore the obstruction is exactly:

   for every pair {u,x} that is NOT a Gamma edge,
        sum_{e at u, f at x, e cap f = empty} c_ef * G_e^(u) (x) G_f^(x) = 0
   where G_e^(t) := a_e^(t)/c_e is the (centred) t-side function of dA_e.

together with the first-order conditions  sum_{e at t} c_e G_e^(t) = 0.
"Site t factors at first order" is G_e^(t) = t_e * g for one common g.

QUESTION DECIDED HERE: do the first- and second-order conditions already
force alignment at some site?  Answer by exact Groebner dimension counts.
"""
from __future__ import annotations
import os
import sys
import json
import itertools
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w19_core import EDGES, PMS, W8_IMMUNE, gamma_edges, pms_inside
from w19_tangent import jpoint, c_coeffs
from w19_sing import run_singular, check_no_shadowing


def c_pairs(gam, fullm, tv):
    out = {}
    for i, e in enumerate(gam):
        for f in gam[i + 1:]:
            if set(e) & set(f):
                continue
            tot = Fraction(0)
            for mi in fullm:
                M = PMS[mi]
                if e in M and f in M:
                    p = Fraction(1)
                    for h in M:
                        if h not in (e, f):
                            p *= tv[h]
                    tot += p
            if tot:
                out[(e, f)] = tot
                out[(f, e)] = tot
    return out


def build(gam, fullm, tv, c, cef):
    """variables: G_e^(t) = (x_{e,t,0}, x_{e,t,1}, x_{e,t,2}) with sum 0,
    parametrised by two free coordinates."""
    names = {}
    for e in gam:
        for t in e:
            for k in (0, 1):
                names[(e, t, k)] = "u%d%d_%d_%d" % (e[0], e[1], t, k)

    def comp(e, t, i):
        """component i of G_e^(t) in the sum-zero parametrisation."""
        if i == 0:
            return names[(e, t, 0)]
        if i == 1:
            return names[(e, t, 1)]
        return "(-%s-%s)" % (names[(e, t, 0)], names[(e, t, 1)])

    eqs = []
    # first order: sum_{e at t} c_e G_e^(t) = 0
    for t in range(8):
        at = [e for e in gam if t in e]
        for i in (0, 1):
            terms = []
            for e in at:
                num, den = c[e].numerator, c[e].denominator
                terms.append("%s%d/%d*%s" % ("+" if num > 0 else "-",
                                             abs(num), den, comp(e, t, i)))
            eqs.append("".join(terms).lstrip("+"))
    # second order: non-Gamma pairs
    gset = set(gam)
    n_pairs = 0
    for u in range(8):
        for x in range(u + 1, 8):
            if (u, x) in gset:
                continue
            terms_by_cell = {}
            for e in gam:
                if u not in e:
                    continue
                for f in gam:
                    if x not in f or set(e) & set(f):
                        continue
                    co = cef.get((e, f))
                    if not co:
                        continue
                    for i in (0, 1):
                        for j in (0, 1):
                            terms_by_cell.setdefault((i, j), []).append(
                                (co, comp(e, u, i), comp(f, x, j)))
            if not terms_by_cell:
                continue
            n_pairs += 1
            for (i, j), lst in terms_by_cell.items():
                terms = []
                for co, a, b in lst:
                    num, den = co.numerator, co.denominator
                    terms.append("%s%d/%d*%s*%s" % ("+" if num > 0 else "-",
                                                    abs(num), den, a, b))
                eqs.append("".join(terms).lstrip("+"))
    return names, comp, eqs, n_pairs


def align_eqs(gam, comp, c, tv, t):
    """G_e^(t) = t_e * g for a COMMON g: cross conditions between edges."""
    at = [e for e in gam if t in e]
    out = []
    e0 = at[0]

    def term(co, sym, lead=False):
        num, den = Fraction(co).numerator, Fraction(co).denominator
        s = "" if (lead and num > 0) else ("+" if num > 0 else "-")
        return "%s%d/%d*%s" % (s, abs(num), den, sym)
    for e in at[1:]:
        for i in (0, 1):
            out.append(term(tv[e], comp(e0, t, i), lead=True)
                       + term(-tv[e0], comp(e, t, i)))
    return out


def dim_of(names, eqs, extra=(), timeout=1800):
    ring = sorted(set(names.values()))
    gens = ["zzg%d" % i for i in range(1, len(eqs) + len(extra) + 1)]
    check_no_shadowing(ring, gens + ["zzI", "zzGB"])
    ll = ['LIB "elim.lib";', "ring r = 0,(%s),dp;" % ",".join(ring)]
    allq = list(eqs) + list(extra)
    for i, e in enumerate(allq, 1):
        ll.append("poly zzg%d = %s;" % (i, e))
    ll.append("ideal zzI = %s;" % ",".join(gens))
    ll.append("ideal zzGB = groebner(zzI);")
    ll.append('"DIM:"; dim(zzGB);')
    ll.append('"UNIT:"; (zzGB[1]==1);')
    ll.append("quit;")
    t0 = time.time()
    out, st = run_singular("\n".join(ll) + "\n", timeout=timeout)
    if st == "TIMEOUT":
        return dict(dim=None, secs=timeout, n_eqs=len(allq),
                    n_vars=len(ring))
    return dict(dim=int(out.split("DIM:")[1].strip().split()[0]),
                unit=out.split("UNIT:")[1].strip().split()[0] == "1",
                n_eqs=len(allq), n_vars=len(ring),
                secs=round(time.time() - t0, 1))


def analyse(gam, name, timeout=1800):
    fullm = pms_inside(gam)
    tv = jpoint(gam, fullm)
    c = c_coeffs(gam, fullm, tv)
    cef = c_pairs(gam, fullm, tv)
    names, comp, eqs, npairs = build(gam, fullm, tv, c, cef)
    res = dict(name=name, n_gamma=len(gam), n_vars=len(set(names.values())),
               n_eqs=len(eqs), n_nonGamma_pairs_used=npairs)
    res["order1_only"] = dim_of(names, eqs[:16], timeout=timeout)
    res["order1_and_2"] = dim_of(names, eqs, timeout=timeout)
    per = {}
    for t in range(8):
        per[t] = dim_of(names, eqs, align_eqs(gam, comp, c, tv, t),
                        timeout=timeout)
    res["per_site_aligned"] = per
    d = res["order1_and_2"].get("dim")
    res["escapes_every_site"] = (d is not None and
                                 all(p.get("dim") is not None and
                                     p["dim"] < d for p in per.values()))
    return res


def main():
    out = {}
    for m in (25, 26, 27, 28):
        gam = gamma_edges(W8_IMMUNE[m])
        r = analyse(gam, "W8 Gamma m=%d" % m)
        out["m%d" % m] = r
        print("m=%d |G|=%d vars=%d eqs=%d nonGamma-pairs=%d | dim(order1)=%s"
              " dim(order1+2)=%s | per-site aligned dims %s | strictly "
              "smaller at every site: %s"
              % (m, r["n_gamma"], r["n_vars"], r["n_eqs"],
                 r["n_nonGamma_pairs_used"], r["order1_only"].get("dim"),
                 r["order1_and_2"].get("dim"),
                 {t: r["per_site_aligned"][t].get("dim") for t in range(8)},
                 r["escapes_every_site"]), flush=True)
    json.dump(out, open(os.path.join(HERE, "results_order2.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
