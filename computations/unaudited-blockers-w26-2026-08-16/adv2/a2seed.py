#!/usr/bin/env python3
"""adv2 -- GENERIC rung-3 seed constructor.  UNAUDITED.  EXACT ONLY.

Target: T = {a,b,j}, a,b in L, j in R, with (a,j) and (b,j) both singles
FIRING AT THE SAME LETTER of j.  Everything outside T is separable, so
   Phi(tau) = N[tau_j] . V(tau_a,tau_b),
   N[c]_u = A_{ju}[c][.]  (u runs over j's Gamma-neighbours, all in S),
   V_u    = haf(Gamma - j - u).
Split off the (a,b) block:  V(tau) = Lam_ab(tau) * cvec + Wv(tau) with
   cvec_u = haf(Gamma - j - u - a - b)   (a constant vector),
   Wv(tau) = V(tau) evaluated at Lam_ab = 0.

RECIPE
 1. impose BRANCH (i) at a: the vertex-a data at a's two DEACTIVATING
    letters are proportional (factor lam_a).  Wv is linear in the
    vertex-a data, so Wv(d0,.) = lam_a Wv(d1,.) and the four CLEAN
    tau's contribute only TWO independent Wv vectors.
 2. pick n with all entries nonzero and n.cvec != 0, and solve
       Lam_ab(tau) = -(n.Wv(tau)) / (n.cvec)      ==>  n.V == 0.
 3. pick 0 != mvec in {cvec, Wv(clean)}^perp  (>= 1-dimensional by step 1).
 4. set N[d0_j] = mu*n, N[d1_j] = n, N[act_j] = cp*n + cc*mvec.
    Then Phi = cc * (mvec.Wv)(tau_a,tau_b) at tau_j = act and 0 elsewhere,
    which vanishes exactly on the clean tau's.
 5. Branch (i) at a also makes BOTH Phi and c_{(b,j)} proportional across
    a's two deactivating letters, so the (b,j)-solo ratio is automatically
    a single constant: the (b,j)-solo family SURVIVES.
"""
from __future__ import annotations

import os
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a2lib as A                                                 # noqa: E402
import a2sep as SP                                                # noqa: E402
import w26_core as C                                              # noqa: E402

F = Fraction


def rung_deact(sp, v):
    """letters at v deactivating every T-single at v."""
    fires = {sp.sing[e][0 if e[0] == v else 1] for e in sp.tsing if v in e}
    return [c for c in range(3) if c not in fires], sorted(fires)


def seed3(m, a, b, j, rng, tries=60, lo=-5, hi=5):
    """returns (sp, theta, z, blocks, info) or None."""
    S = [v for v in range(8) if v not in (a, b, j)]
    sp = SP.Sep(m, S)
    ea, eb = (min(a, j), max(a, j)), (min(b, j), max(b, j))
    assert sorted(sp.tsing) == sorted([ea, eb]), sp.tsing
    dj, fj = rung_deact(sp, j)
    da, fa = rung_deact(sp, a)
    db, fb = rung_deact(sp, b)
    assert len(dj) == 2 and len(da) == 2 and len(db) == 2
    actj, alpha_a, alpha_b = fj[0], fa[0], fb[0]
    nbj = sorted({u for e in sp.gam for u in e if j in e} - {j})
    eab = (min(a, b), max(a, b))
    Vset = tuple(range(8))

    def rnd():
        return F(rng.randint(lo, hi) or 2, rng.randint(1, 2))

    for _try in range(tries):
        th = sp.rand_theta(rng, lo, hi)
        # --- branch (i) at vertex a : rows da[0] = lam_a * rows da[1]
        lam = F(rng.randint(1, 4))
        for k in sp.params:
            e, ia, ib = k
            if a not in e:
                continue
            if e[0] == a and ia == da[0]:
                k2 = (e, da[1], ib)
                th[sp.pidx[k]] = lam * th[sp.pidx[k2]]
            if e[1] == a and ib == da[0]:
                k2 = (e, ia, da[1])
                th[sp.pidx[k]] = lam * th[sp.pidx[k2]]
        # --- Wv(tau) and cvec
        th0 = list(th)
        for k in sp.by_edge[eab]:
            th0[sp.pidx[k]] = F(0)
        bl0 = sp.blocks(th0)
        z0 = {}
        Wv = {}
        for wi, w in enumerate(sp.reps):
            key = (w[a], w[b])
            if key in Wv:
                continue
            Wv[key] = [sp.hafM(bl0, z0, w,
                               tuple(x for x in Vset if x != j and x != u))
                       for u in nbj]
        w0 = sp.reps[0]
        cvec = [sp.hafM(bl0, z0, w0,
                        tuple(x for x in Vset
                              if x not in (j, u, a, b))) for u in nbj]
        if all(x == 0 for x in cvec):
            continue
        # --- n
        n = None
        for _ in range(80):
            cand = [F(rng.randint(1, hi)) for _ in nbj]
            if sum((cand[i] * cvec[i] for i in range(len(nbj))), F(0)) != 0:
                n = cand
                break
        if n is None:
            continue
        kn = sum((n[i] * cvec[i] for i in range(len(nbj))), F(0))
        # --- solve Lam_ab
        okL = True
        for xa in range(3):
            for xb in range(3):
                rn = sum((n[i] * Wv[(xa, xb)][i] for i in range(len(nbj))),
                         F(0))
                val = -rn / kn
                if val == 0:
                    okL = False
                k = (eab, xa if eab[0] == a else xb,
                     xb if eab[1] == b else xa)
                th[sp.pidx[k]] = val
        if not okL:
            continue
        # --- mvec in the perp of cvec and the clean Wv's
        rows = [cvec[:]] + [Wv[(xa, xb)][:] for xa in da for xb in db]
        K = A.kernel_g(rows, len(nbj), F(0), F(1))
        if not K:
            continue
        mvec = None
        for _ in range(200):
            co = [F(rng.randint(-4, 4)) for _ in K]
            v = [sum((co[i] * K[i][t] for i in range(len(K))), F(0))
                 for t in range(len(nbj))]
            if any(x != 0 for x in v):
                # must be non-degenerate on the 5 non-clean tau's
                bad = False
                for xa in range(3):
                    for xb in range(3):
                        nz = (xa == alpha_a) or (xb == alpha_b)
                        val = sum((v[i] * Wv[(xa, xb)][i]
                                   for i in range(len(nbj))), F(0))
                        if nz and val == 0:
                            bad = True
                if not bad:
                    mvec = v
                    break
        if mvec is None:
            continue
        # --- vertex-j blocks
        got = None
        for mu in (F(2), F(3), F(-1), F(5), F(-2)):
            for cp in (F(1), F(2), F(-1), F(3)):
                for cc in (F(1), F(2), F(-1)):
                    N = {dj[0]: [mu * x for x in n], dj[1]: list(n),
                         actj: [cp * n[i] + cc * mvec[i]
                                for i in range(len(nbj))]}
                    if all(N[c][i] != 0 for c in range(3)
                           for i in range(len(nbj))):
                        got = (N, mu, cp, cc)
                        break
                if got:
                    break
            if got:
                break
        if not got:
            continue
        N, mu, cp, cc = got
        for i, u in enumerate(nbj):
            e = (min(j, u), max(j, u))
            for c in range(3):
                for d in range(3):
                    k = (e, c if e[0] == j else (-1 if u in sp.S else d),
                         c if e[1] == j else (-1 if u in sp.S else d))
                    if k in sp.pidx:
                        th[sp.pidx[k]] = N[c][i]
        bl = sp.blocks(th)
        if not A.all_cells_nonzero(bl, A.Geo(m)):
            continue
        if not A.is_clean(m, bl):
            continue
        if A.on_stratum(m, bl):
            continue
        # --- z from the (b,j) solo family; try (a,j) too
        z = {ea: F(0), eb: F(0)}
        sv = {}
        for e in (ea, eb):
            r = A.solo_verdict(m, bl, e)
            sv[e] = r
            if r["survives"]:
                z[e] = F(r["ratio"])
        if not any(z[e] != 0 for e in z):
            continue
        info = dict(a=a, b=b, j=j, lam=str(lam), n=[str(x) for x in n],
                    mvec=[str(x) for x in mvec], cvec=[str(x) for x in cvec],
                    mu=str(mu), cp=str(cp), cc=str(cc), nbj=nbj,
                    tries=_try + 1,
                    solo={str(e): sv[e]["survives"] for e in sv})
        return sp, th, z, bl, info
    return None
