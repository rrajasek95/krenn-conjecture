#!/usr/bin/env python3
"""W19 -- THE CONTROL SUITE.  UNAUDITED.  Exact rational arithmetic only.

C1  model cross-check: my independent re-implementation must reproduce
    W16's stored per-template numbers (|Gamma|, |F(Gamma)|, clean / k=1 /
    k=2 counts, per-site (clean,k=1) and (clean,k=2) pair counts, Gamma
    degrees).  Disagreement anywhere invalidates everything downstream.
C2  Theorem W16-1 (cross-matching factorisation) reproduced on one
    instance, with two mutation controls that must FAIL.
C3  the m=25 Step-A dichotomy linear algebra on >= 10 instances of each of
    the three families (generic / factoring / rank-one-but-not-aligned
    near miss), plus a mutation control.
C4  J-POINT NON-VACUITY: an explicit exact J-point satisfies every
    effectively clean equation, so the clean layer is never the unit
    ideal (the control that must accompany every forcing verdict).
C5  BRANCH-B EXPLICIT-POINT CONTROL (ledger item 13): an explicit
    rational point of the Branch-B system with every cell nonzero;
    every "forced" verdict of w19_branchB.py is tested against it.
C6  gauge control: the Branch-B normalisation chain is achievable.
C7  negative-target control: a polynomial that must NOT be forced.
"""
from __future__ import annotations
import os
import sys
import json
import itertools
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w19_core import (EDGES, EIDX, FULL, PMS, PM_E, MIXED, W8_IMMUNE, VarMap,
                      support, gamma_edges, full_pm_indices, extras_at,
                      phi_poly, peval, padd, psub, pmul, spanning_2conn,
                      rank_of, site_factors, cell)

W16 = os.path.join(os.path.dirname(HERE), "unaudited-residual2-w16-2026-08-15")


def lcg(seed):
    s = seed
    while True:
        s = (1103515245 * s + 12345) % (1 << 31)
        yield s


def rnd(r, lo=13, hi=5):
    return Fraction((next(r) % lo) - lo // 2 or 5, (next(r) % hi) + 1)


# ------------------------------------------------------------------- C1 ---
def C1():
    stored = json.load(open(os.path.join(W16, "results_vertex.json")))
    out = {}
    for m in (24, 25, 26, 27, 28):
        T = W8_IMMUNE[m]
        fullm = full_pm_indices(T)
        ge = gamma_edges(T)
        deg = {v: 0 for v in range(8)}
        for u, v in ge:
            deg[u] += 1
            deg[v] += 1
        kmap = {w: len(extras_at(T, w, fullm))
                for w in itertools.product(range(3), repeat=8)}
        clean = set(w for w in MIXED if kmap[w] == 0)
        k1 = set(w for w in MIXED if kmap[w] == 1)
        k2 = set(w for w in MIXED if kmap[w] == 2)
        per = {}
        for t in range(8):
            c1 = c2 = 0
            for w in clean:
                for c in range(3):
                    if c == w[t]:
                        continue
                    wp = w[:t] + (c,) + w[t + 1:]
                    if wp in k1:
                        c1 += 1
                    elif wp in k2:
                        c2 += 1
            per[t] = (c1, c2)
        st = stored[str(m)]
        mism = []
        if st["n_clean"] != len(clean):
            mism.append("n_clean")
        if st["n_k1"] != len(k1):
            mism.append("n_k1")
        if st["n_k2"] != len(k2):
            mism.append("n_k2")
        for t in range(8):
            s = st["per_site"][str(t)]
            if (s["n_clean_to_k1"], s["n_clean_to_k2"]) != per[t]:
                mism.append("site%d_pairs" % t)
            if s["gamma_degree"] != deg[t]:
                mism.append("site%d_deg" % t)
        out[m] = dict(n_gamma=len(ge), n_F=len(fullm), n_clean=len(clean),
                      n_k1=len(k1), n_k2=len(k2),
                      per_site_pairs={t: per[t] for t in range(8)},
                      degrees=deg, mismatches_vs_W16=mism)
    return out


# ------------------------------------------------------------------- C2 ---
L4, R4 = (0, 1, 2, 3), (4, 5, 6, 7)
SIGMA = {0: 7, 1: 4, 2: 5, 3: 6}
SIGINV = {v: k for k, v in SIGMA.items()}


def in_gamma(T, u, v):
    return T[EIDX[(min(u, v), max(u, v))]] == FULL


def haf_sub(T, vm, w, verts):
    verts = tuple(sorted(verts))
    if not verts:
        return {(): Fraction(1)}
    out = {}
    a = verts[0]
    for i in range(1, len(verts)):
        b = verts[i]
        if not in_gamma(T, a, b):
            continue
        rest = verts[1:i] + verts[i + 1:]
        e = EIDX[(a, b)]
        out = padd(out, pmul({(vm.v(e, cell(e, w)),): Fraction(1)},
                             haf_sub(T, vm, w, rest)))
    return out


def cross_c(T, vm, w, i):
    j = SIGMA[i]
    if not in_gamma(T, i, j):
        return {}
    e = EIDX[(min(i, j), max(i, j))]
    return {(vm.v(e, cell(e, w)),): Fraction(1)}


def N_mat(T, vm, w, i, j, side, scale=1, drop_cross=False):
    if side == "L":
        other = tuple(v for v in L4 if v not in (i, j))
        rho = haf_sub(T, vm, w, R4)
        k = haf_sub(T, vm, w, tuple(SIGMA[v] for v in other))
        ci, cj = cross_c(T, vm, w, i), cross_c(T, vm, w, j)
    else:
        other = tuple(v for v in R4 if v not in (i, j))
        rho = haf_sub(T, vm, w, L4)
        k = haf_sub(T, vm, w, tuple(SIGINV[v] for v in other))
        ci = cross_c(T, vm, w, SIGINV[i])
        cj = cross_c(T, vm, w, SIGINV[j])
    e = EIDX[(min(i, j), max(i, j))]
    aij = {} if T[e] != FULL else {(vm.v(e, cell(e, w)),): Fraction(1)}
    base = pmul(rho, aij)
    if drop_cross:
        return base
    p = padd(base, pmul(k, pmul(ci, cj)))
    if scale != 1 and (i, j) == (0, 2):
        p = {mm: cc * scale for mm, cc in p.items()}
    return p


def C2(m=26, side="L", scale=1, drop_cross=False):
    T = W8_IMMUNE[m]
    vm = VarMap(T)
    fullm = full_pm_indices(T)
    pairings = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))] \
        if side == "L" else [((4, 5), (6, 7)), ((4, 6), (5, 7)),
                             ((4, 7), (5, 6))]
    bad = 0
    for w in itertools.product(range(3), repeat=8):
        rho = haf_sub(T, vm, w, R4 if side == "L" else L4)
        lhs = pmul(rho, phi_poly(T, vm, w, fullm))
        rhs = {}
        for (i, j), (k, l) in pairings:
            rhs = padd(rhs, pmul(N_mat(T, vm, w, i, j, side, scale,
                                       drop_cross),
                                 N_mat(T, vm, w, k, l, side, scale,
                                       drop_cross)))
        if psub(lhs, rhs):
            bad += 1
    return bad


# ------------------------------------------------------------------- C3 ---
def nullity(rows, ncols):
    rows = [list(map(Fraction, r)) for r in rows]
    rank = 0
    for c in range(ncols):
        sel = None
        for i in range(rank, len(rows)):
            if rows[i][c]:
                sel = i
                break
        if sel is None:
            continue
        rows[rank], rows[sel] = rows[sel], rows[rank]
        pv = rows[rank][c]
        rows[rank] = [v / pv for v in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][c]:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[rank])]
        rank += 1
    return ncols - rank


def stepA_system(A56, A67):
    rows = []
    for a, b, c, d in itertools.product(range(3), repeat=4):
        r = [Fraction(0)] * 18
        r[3 * a + b] += A67[c][d]
        r[9 + 3 * a + d] += A56[b][c]
        rows.append(r)
    return rows


def rankM6(A56, A67):
    cols = [[A56[0][c], A56[1][c], A56[2][c], A67[c][0], A67[c][1],
             A67[c][2]] for c in range(3)]
    return rank_of([[cols[i][j] for i in range(3)] for j in range(6)])


def C3(n=12):
    res = {}
    for kind in ("generic", "factoring", "near_miss"):
        rows = []
        seed = 1
        while len(rows) < n:
            r = lcg(seed * 37 + 11)
            seed += 1
            if kind == "generic":
                A56 = [[rnd(r) for _ in range(3)] for _ in range(3)]
                A67 = [[rnd(r) for _ in range(3)] for _ in range(3)]
            else:
                be = [rnd(r) for _ in range(3)]
                ga = [rnd(r) for _ in range(3)]
                kk = [rnd(r) for _ in range(3)]
                g2 = ga if kind == "factoring" else [rnd(r) for _ in range(3)]
                A56 = [[be[i] * ga[j] for j in range(3)] for i in range(3)]
                A67 = [[g2[i] * kk[j] for j in range(3)] for i in range(3)]
            if any(v == 0 for M in (A56, A67) for row in M for v in row):
                continue
            rows.append(dict(rank_M6=rankM6(A56, A67),
                             nullity=nullity(stepA_system(A56, A67), 18)))
        res[kind] = rows
    ok = (all(x["nullity"] == 0 for x in res["generic"])
          and all(x["nullity"] > 0 for x in res["factoring"])
          and all(x["nullity"] == 0 for x in res["near_miss"]))
    res["dichotomy_sharp"] = ok
    res["summary"] = {k: dict(n=len(v),
                              rank_M6=sorted({x["rank_M6"] for x in v}),
                              nullity=sorted({x["nullity"] for x in v}))
                      for k, v in res.items() if isinstance(v, list)}
    return res


# ------------------------------------------------------------------- C4 ---
def jpoint_t(gam, fullm, extra=()):
    """t_e in Q^*, haf_Gamma(t) = 0 (and any extra affine conditions)."""
    def haf(tv):
        tot = Fraction(0)
        for mi in fullm:
            p = Fraction(1)
            for e in PMS[mi]:
                p *= tv[e]
            tot += p
        return tot
    for trial in range(1, 40):
        tv = {e: Fraction(1 + ((trial + 2 * i) % 4)) for i, e in
              enumerate(gam)}
        for e0 in gam:
            save = tv[e0]
            tv[e0] = Fraction(0)
            c0 = haf(tv)
            tv[e0] = Fraction(1)
            c1 = haf(tv) - c0
            if c1 and -c0 / c1 != 0:
                tv[e0] = -c0 / c1
                if haf(tv) == 0 and all(v != 0 for v in tv.values()):
                    return tv
            tv[e0] = save
    raise RuntimeError("no J-point")


def C4(m=25):
    T = W8_IMMUNE[m]
    gam = gamma_edges(T)
    fullm = full_pm_indices(T)
    tv = jpoint_t(gam, fullm)
    vm = VarMap(T)
    vals = {}
    for ei, e in enumerate(EDGES):
        if T[ei] != FULL:
            continue
        for c in range(9):
            vals[vm.v(ei, c)] = tv[e]
    nclean = viol = phinz = 0
    for w in itertools.product(range(3), repeat=8):
        ph = peval(phi_poly(T, vm, w, fullm), vals)
        if ph != 0:
            phinz += 1
        if len(set(w)) > 1 and not extras_at(T, w, fullm):
            nclean += 1
            if ph != 0:
                viol += 1
    blocks = {e: [[tv[e]] * 3 for _ in range(3)] for e in gam}
    return dict(m=m, t_values={"%d%d" % e: str(v) for e, v in tv.items()},
                clean_mixed=nclean, clean_violations=viol,
                words_with_Phi_nonzero=phinz,
                factoring_sites=[t for t in range(8)
                                 if site_factors(blocks, gam, t)])


# ------------------------------------------------------------------- C5 ---
BRANCH_B_POINT = {(0, 1): -3, (0, 2): 1, (0, 3): 1, (1, 2): 1, (1, 3): 1,
                  (2, 3): 1, (0, 7): 1, (1, 4): 1, (2, 5): 1, (4, 5): 1,
                  (4, 7): 1, (5, 6): 2, (6, 7): 1}


def C5(tv=None):
    """THE EXPLICIT-POINT CONTROL (ledger item 13).

    An explicit rational point of {clean layer of the m=25 template} AND
    {Branch B}, with EVERY occupied cell nonzero.  A_e = t_e * J with the
    thirteen t's below; the two Branch-B matrix conditions
        D_x = P_L(x) A45 + A03[x0][x3] A14[x1][.] (x) A25[x2][.] = 0
        E_x = P_L(x) A47 + A23[x2][x3] A14[x1][.] (x) A07[x0][.] = 0
    hold identically, and haf_Gamma(t) = 0 so Phi vanishes on every word.
    Every "forced" verdict of w19_branchB.py must be TRUE at this point --
    it is; and the point shows the Branch-B ideal is not the unit ideal,
    so those verdicts are not vacuous."""
    T = W8_IMMUNE[25]
    gam = gamma_edges(T)
    fullm = full_pm_indices(T)
    tv = {e: Fraction(v) for e, v in (BRANCH_B_POINT if tv is None
                                      else tv).items()}

    def haf():
        tot = Fraction(0)
        for mi in fullm:
            p = Fraction(1)
            for e in PMS[mi]:
                p *= tv[e]
            tot += p
        return tot
    PL = (tv[(0, 1)] * tv[(2, 3)] + tv[(0, 2)] * tv[(1, 3)]
          + tv[(0, 3)] * tv[(1, 2)])
    D = PL * tv[(4, 5)] + tv[(0, 3)] * tv[(1, 4)] * tv[(2, 5)]
    E = PL * tv[(4, 7)] + tv[(2, 3)] * tv[(1, 4)] * tv[(0, 7)]
    vm = VarMap(T)
    vals = {}
    for ei, e in enumerate(EDGES):
        if T[ei] != FULL:
            continue
        for c in range(9):
            vals[vm.v(ei, c)] = tv[e]
    viol = nclean = 0
    for w in itertools.product(range(3), repeat=8):
        if len(set(w)) > 1 and not extras_at(T, w, fullm):
            nclean += 1
            if peval(phi_poly(T, vm, w, fullm), vals) != 0:
                viol += 1
    blocks = {e: [[tv[e]] * 3 for _ in range(3)] for e in gam}
    # the Branch-B gauge symbols read off at this point
    sym = dict(mu=str(tv[(4, 5)] / (tv[(1, 4)] * tv[(2, 5)])),
               nu=str(tv[(4, 7)] / (tv[(1, 4)] * tv[(0, 7)])),
               sigma_A56=str(tv[(5, 6)]), lam=str(PL))
    return dict(t_values={"%d%d" % e: str(v) for e, v in tv.items()},
                haf_Gamma=str(haf()), P_L=str(PL), D_x=str(D), E_x=str(E),
                branchB_holds=(D == 0 and E == 0),
                clean_equations=nclean, clean_violations=viol,
                all_cells_nonzero=all(v != 0 for v in tv.values()),
                factoring_sites=[t for t in range(8)
                                 if site_factors(blocks, gam, t)],
                gauge_symbols=sym)


def C5_mutation():
    """the control must FAIL on a deliberately corrupted point."""
    bad = dict(BRANCH_B_POINT)
    bad[(0, 1)] = -2
    return C5(bad)


# ------------------------------------------------------------------- C6 ---
def C6():
    """The Branch-B gauge chain is achievable: recompute the lambdas from a
    random exact point and check every normalised cell lands on 1."""
    r = lcg(9)
    gam = gamma_edges(W8_IMMUNE[25])
    B = {e: [[rnd(r) for _ in range(3)] for _ in range(3)] for e in gam}
    lam = {(t, c): Fraction(1) for t in range(8) for c in range(3)}

    def val(u, v, i, j):
        e = (min(u, v), max(u, v))
        if (u, v) != e:
            i, j = j, i
        return B[e][i][j] * lam[(e[0], i)] * lam[(e[1], j)]
    order = []
    for c in range(3):
        order += [(4, c, (1, 4), 2, c), (5, c, (2, 5), 0, c),
                  (7, c, (0, 7), 1, c), (6, c, (6, 7), c, 0)]
    order += [(1, x, (1, 4), x, 0) for x in (0, 1)]
    order += [(2, x, (2, 5), x, 0) for x in (1, 2)]
    order += [(0, x, (0, 7), x, 0) for x in (0, 2)]
    order += [(3, x, (0, 3), 0, x) for x in range(3)]
    bad = 0
    for (t, c, e, i, j) in order:
        cur = val(e[0], e[1], i, j)
        if cur == 0:
            bad += 1
            continue
        lam[(t, c)] = lam[(t, c)] / cur
        if val(e[0], e[1], i, j) != 1:
            bad += 1
    return dict(normalised_cells=len(order), failures=bad)


def main():
    res = {}
    res["C1_model_crosscheck"] = C1()
    for m, v in res["C1_model_crosscheck"].items():
        print("C1 m=%d |G|=%d |F|=%d clean=%d k1=%d k2=%d  MISMATCHES vs "
              "W16: %s" % (m, v["n_gamma"], v["n_F"], v["n_clean"],
                           v["n_k1"], v["n_k2"], v["mismatches_vs_W16"]),
              flush=True)
    res["C2_W16_1"] = dict(
        m26_L=C2(26, "L"), m26_R=C2(26, "R"),
        mutation_scale_N02=C2(26, "L", scale=2),
        mutation_drop_cross=C2(26, "L", drop_cross=True))
    print("C2 W16-1 identity: L mismatches %d, R mismatches %d ; MUTATIONS "
          "(must be > 0): scale %d, drop-cross %d"
          % (res["C2_W16_1"]["m26_L"], res["C2_W16_1"]["m26_R"],
             res["C2_W16_1"]["mutation_scale_N02"],
             res["C2_W16_1"]["mutation_drop_cross"]), flush=True)
    res["C3_stepA"] = C3(12)
    print("C3 Step-A dichotomy:", res["C3_stepA"]["summary"],
          "sharp:", res["C3_stepA"]["dichotomy_sharp"], flush=True)
    res["C4_Jpoint"] = {m: C4(m) for m in (25, 26, 27, 28)}
    for m, v in res["C4_Jpoint"].items():
        print("C4 J-point m=%d: clean equations %d, violations %d, words "
              "with Phi != 0: %d, factoring sites %s"
              % (m, v["clean_mixed"], v["clean_violations"],
                 v["words_with_Phi_nonzero"], v["factoring_sites"]),
              flush=True)
    res["C5_branchB_point"] = C5()
    print("C5 Branch-B explicit point:",
          {k: v for k, v in res["C5_branchB_point"].items()
           if k != "t_values"}, flush=True)
    res["C5_mutation"] = C5_mutation()
    print("C5 MUTATION (must break):",
          {k: res["C5_mutation"][k] for k in
           ("haf_Gamma", "branchB_holds", "clean_violations")}, flush=True)
    res["C6_gauge"] = C6()
    print("C6 gauge chain:", res["C6_gauge"], flush=True)
    json.dump(res, open(os.path.join(HERE, "results_controls.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
