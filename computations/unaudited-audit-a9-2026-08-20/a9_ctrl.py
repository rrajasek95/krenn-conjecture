#!/usr/bin/env python3
"""A9 AUDIT -- real diagonal objects, the normal form, and clause validity.

Everything here is written against a9_haf / a9_enc only (no W29 imports).
"""
from __future__ import annotations

import random
from fractions import Fraction
from itertools import combinations

import a9_haf as H
import a9_enc as E


# ------------------------------------------------------------ free sets etc.
def free_set(ts, c, n, z, k=None):
    """F_c^{(k)} = {y in V-z : every even split (S_1,S_2) of V-z-y with
    off-count <= k has haf(t^d|S_1) haf(t^e|S_2) = 0}."""
    d, e = [x for x in range(3) if x != c]
    VP = [x for x in range(n) if x != z]
    out = []
    for y in VP:
        W = tuple(x for x in VP if x != y)
        ok = True
        for m in range(0, len(W) + 1, 2):
            for S1 in combinations(W, m):
                S2 = tuple(x for x in W if x not in S1)
                if k is not None and n - max(2, len(S1), len(S2)) > k:
                    continue
                if H.haf_dp(ts[d], S1) != 0 and H.haf_dp(ts[e], S2) != 0:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            out.append(y)
    return out


def normal_form(ts, n, z, k=None, pick=0):
    """W29-B1/B2 normal form of a real source at site z, computed from
    scratch.  Returns None if it does NOT apply (which would refute B2)."""
    VP = [x for x in range(n) if x != z]
    F = [free_set(ts, c, n, z, k) for c in range(3)]
    ys, cands = [], []
    for c in range(3):
        cand = [y for y in F[c]
                if ts[c].get(H.ek(z, y), 0) != 0
                and H.haf_dp(ts[c], tuple(x for x in VP if x != y)) != 0]
        if not cand:
            return {"FAIL": "no witness y_c", "c": c, "F": F}
        cands.append(cand)
        ys.append(cand[pick % len(cand)])
    if len(set(ys)) != 3:
        return {"FAIL": "y's not distinct", "ys": ys, "F": F}
    Q = [y for y in VP if y not in ys]
    perm = {ys[c]: c for c in range(3)}
    for i, q in enumerate(Q):
        perm[q] = 3 + i
    perm[z] = n - 1
    Rs = tuple(tuple(sorted(perm[y] for y in F[c] if y in Q))
               for c in range(3))
    # F_c must sit inside {y_c} + Q -- B1's conclusion, verified not assumed
    inside = all(set(F[c]) <= set([ys[c]]) | set(Q) for c in range(3))
    return {"ys": ys, "Q": Q, "Rs": Rs, "perm": perm, "F": F,
            "B1_inside": inside, "cands": cands}


def relabel(ts, perm):
    out = [{}, {}, {}]
    for c in range(3):
        for (a, b), v in ts[c].items():
            out[c][H.ek(perm[a], perm[b])] = v
    return out


def check_point(ts, n, z, k, pick=0, use=None):
    """Full pipeline on a real object: normal form -> case -> clauses -> the
    object's own vanishing pattern must satisfy every clause."""
    nf = normal_form(ts, n, z, k, pick)
    if "FAIL" in nf:
        return {"normal_form": nf, "PASS": False}
    ts2 = relabel(ts, nf["perm"])
    kw = {} if use is None else {"use": use}
    e = E.Enc(n, nf["Rs"], k=k, **kw).build()
    A = e.truth(ts2, H.haf_dp)
    viol = e.violations(A)
    sat, _ = e.solve_pysat()
    return {"Rs": [list(r) for r in nf["Rs"]], "ys": nf["ys"],
            "B1_inside": nf["B1_inside"], "n_clauses": len(e.cls),
            "n_violations": len(viol),
            "violations": [(str(t), [str(x) for x in c]) for t, c in viol[:6]],
            "abstraction_SAT": sat,
            "PASS": (not viol) and sat and nf["B1_inside"]}


# ------------------------------------------------------------- real objects
def pm_source(n, Ms, weights=None):
    ts = [{}, {}, {}]
    for c, M in enumerate(Ms):
        for i, e in enumerate(M):
            ts[c][H.ek(*e)] = Fraction(1) if weights is None else weights[c][i]
    return ts


def disjoint_pm_triples(n, rng, ntries=4000):
    pms = H.perfect_matchings(tuple(range(n)))
    out = []
    seen = set()
    for _ in range(ntries):
        i, j, l = rng.sample(range(len(pms)), 3)
        Ms = [pms[i], pms[j], pms[l]]
        if len({e for M in Ms for e in M}) != 3 * (n // 2):
            continue
        key = tuple(sorted((i, j, l)))
        if key in seen:
            continue
        seen.add(key)
        out.append(Ms)
    return out


def unit_product_weights(rng, m):
    ws = [Fraction(rng.randint(1, 7), rng.randint(1, 5)) for _ in range(m - 1)]
    p = Fraction(1)
    for w in ws:
        p *= w
    ws.append(1 / p)
    return ws


def x3_violations(ts, n):
    """X_3 (= X_2) for a diagonal source on K_n: haf(t^c|V) = 1 and
    t^d_{ab} haf(t^c|V-{a,b}) = 0 for c != d."""
    V = tuple(range(n))
    bad = []
    for c in range(3):
        if H.haf_dp(ts[c], V) != 1:
            bad.append(("PURE", c))
    for (a, b) in combinations(V, 2):
        R = tuple(x for x in V if x not in (a, b))
        for c in range(3):
            for d in range(3):
                if c != d and ts[d].get((a, b), 0) != 0 \
                        and H.haf_dp(ts[c], R) != 0:
                    bad.append(("MIX", c, d, (a, b)))
    return bad


def rich_x3_search(n, rng, want=40, ntries=6000, extra=(1, 2, 3)):
    """X_3 sources with support beyond a single perfect matching, so that the
    free sets -- and hence the CASES exercised -- are not all the maximal one.
    """
    V = tuple(range(n))
    alledges = list(combinations(V, 2))
    pms = H.perfect_matchings(V)
    out = []
    for _ in range(ntries):
        if len(out) >= want:
            break
        i, j, l = rng.sample(range(len(pms)), 3)
        Ms = [pms[i], pms[j], pms[l]]
        if len({e for M in Ms for e in M}) != 3 * (n // 2):
            continue
        used = {e for M in Ms for e in M}
        ts = [{}, {}, {}]
        for c, M in enumerate(Ms):
            for e in M:
                ts[c][e] = Fraction(rng.randint(1, 6), rng.randint(1, 4))
            for _ in range(rng.choice(extra)):
                f = rng.choice(alledges)
                if f in used:
                    continue
                ts[c][f] = Fraction(rng.randint(1, 6), rng.randint(1, 4))
                used.add(f)
        # normalise haf(t^c|V) = 1 by scaling one edge (haf is multilinear)
        ok = True
        for c in range(3):
            e0 = Ms[c][0]
            beta = H.haf_dp({k2: v for k2, v in ts[c].items() if k2 != e0}, V)
            alpha = H.haf_dp({k2: v for k2, v in ts[c].items()
                              if k2 != e0}, tuple(x for x in V if x not in e0))
            if alpha == 0:
                ok = False
                break
            ts[c][e0] = (1 - beta) / alpha
            if ts[c][e0] == 0:
                ok = False
                break
        if not ok:
            continue
        if x3_violations(ts, n):
            continue
        out.append(ts)
    return out
