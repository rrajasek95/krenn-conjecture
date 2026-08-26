#!/usr/bin/env python3
"""W36 adversarial builders against the CORRECTED m=25 targets.

W30's round-10 (beta) target ("A45 and A47 rank one with a common column
direction shared with A14") is reached at W30's own r10 best points over
F_13, F_31 and Q -- and the (beta) escape score there is 0.000 (not one of
the 376 untriggered words has Q = 0).  So that target is necessary at best
and gives no gradient.  The EXACT targets are:

 mode 'beta'  : some (y5,y7) class with Q = (B,C) == 0 on FAM_ALL and on one
                of FAM_01 / FAM_02  <=>  rank S'(y5,y7) = 2  <=>  the (beta)
                hypothesis fails there.  Score in [0,2].
 mode 'alpha' : hafL == 0 on all 42 words of X_{R6,25} (Branch T).  Score
                0..42, with the forced-structure diagnostics recorded at
                every record so the PLATEAU can be characterised.

Declared controls: A1_clean A2_offstratum A3_allnz A4_target_exact
usage: w36_build.py <beta|alpha> <p|Q> <seed> <seconds>
"""
from __future__ import annotations
import json, os, random, sys, time
from fractions import Fraction as F
from itertools import combinations, product
sys.dont_write_bytecode = True
import w36_lib as W
import w36_beta2 as B2
import w30_lib as L
import w30_hunt as H
import w26_core as C
import w26_fast as FA

HERE = W.HERE
DECL = ["A1_clean", "A2_offstratum", "A3_allnz", "A4_target_exact"]
FAM = B2.families()


def Xv():
    X = set()
    for (w, fire) in L.index_choices_cached(25, 'R', 6):
        if len(fire) == 1:
            X.add(tuple(w[:4]))
    return sorted(X)


XV = Xv()


def beta_score(bl, K):
    """max over classes of  (frac Q-zero on FAM_ALL) + max(frac on 01, 02).
    == 2.0 exactly when rank S' = 2 there."""
    best = -1.0
    bk = None
    bd = None
    for k, d in FAM.items():
        f = {}
        for nm in ('ALL', '01', '02'):
            n = len(d[nm])
            if n == 0:
                f[nm] = None
                continue
            z = sum(1 for pat in d[nm]
                    if all(K.iszero(t) for t in W.BC(bl, B2.word_of(pat))))
            f[nm] = z / n
        sub = [f[nm] for nm in ('01', '02') if f[nm] is not None]
        s = (f['ALL'] or 0.0) + (max(sub) if sub else 0.0)
        if s > best:
            best, bk, bd = s, k, f
    return best, bk, bd


def alpha_score(bl, K):
    return sum(1 for x in XV if K.iszero(W.hafL(bl, x)))


def alpha_struct(bl, K):
    """the forced structure that many hafL-zeros imply (this lane).
    At a clean word with hafL(x) = 0 we get B = l03*d1*d2 and C = l23*d0*d1,
    both nonzero, so  A56[y5][t]/A67[t][y7] = -A03[x0][x3]A25[x2][y5] /
    (A23[x2][x3]A07[x0][y7])  -- and the LHS does not depend on x.  Hence
    over the zero set Z the ratio must be constant, which (varying y5, y7)
    forces rows of A25 / A07 parallel and A03 proportional to A23."""
    Z = [x for x in XV if K.iszero(W.hafL(bl, x))]
    p0 = sorted({x[0] for x in Z})
    p2 = sorted({x[2] for x in Z})
    p3 = sorted({x[3] for x in Z})
    r07 = L.rank_rows([bl[(0, 7)][a] for a in p0], K) if p0 else 0
    r25 = L.rank_rows([bl[(2, 5)][a] for a in p2] , K) if p2 else 0
    r03 = L.rank_rows([bl[(0, 3)][a] for a in p0], K) if p0 else 0
    r23 = L.rank_rows([bl[(2, 3)][a] for a in p2], K) if p2 else 0
    rboth = L.rank_rows([bl[(0, 3)][a] for a in p0]
                        + [bl[(2, 3)][a] for a in p2], K) if (p0 and p2) else 0
    return dict(nZ=len(Z), pi0=p0, pi2=p2, pi3=p3, rank_A07_on_pi0=r07,
                rank_A25_on_pi2=r25, rank_A03_on_pi0=r03,
                rank_A23_on_pi2=r23, rank_A03A23_joint=rboth,
                rank_A07=L.rank_rows(bl[(0, 7)], K),
                rank_A25=L.rank_rows(bl[(2, 5)], K))


def main():
    mode, fld = sys.argv[1], sys.argv[2]
    seed, secs = int(sys.argv[3]), float(sys.argv[4])
    p = 0 if fld == 'Q' else int(fld)
    K = W.K_of(fld)
    res = os.path.join(HERE, "results_build_%s_%s.json" % (mode, fld))
    OUT = {"_header": W.HEADER, "mode": mode, "field": fld, "seed": seed,
           "_controls_declared": DECL, "_controls_run": [], "best": None,
           "hits": [], "trace": []}

    def ck():
        json.dump(OUT, open(res, "w"), indent=1, default=str)

    rng = random.Random(seed)
    mdl = FA.Model(25) if p == 0 else None
    t0 = time.time()
    best = -1.0
    nres = 0
    TARGET = 2.0 if mode == 'beta' else float(len(XV))

    def sc(b):
        if mode == 'beta':
            s, k, d = beta_score(b, K)
            return s, dict(cls=str(k), frac=d)
        s = alpha_score(b, K)
        return float(s), dict(nz=s, of=len(XV))

    # warm starts: every stored m=25 object of this field that is already
    # clean / all-nonzero / off-stratum.  Random seeding at m=25 lands off
    # the stratum only rarely, so cold restarts waste the budget.
    import w36_sprime as SP
    warm = []
    pool = list(SP.load_corpus())
    # this lane's own records, so a restart never loses ground (ledger 31:
    # every cited point is stored, so every stored point is re-usable)
    import glob as _g
    for q in _g.glob(os.path.join(HERE, "results_build_*.json")) + \
            _g.glob(os.path.join(HERE, "results_joint_hunt_*.json")):
        try:
            dd = json.load(open(q))
        except Exception:
            continue
        if dd.get("field") == fld and isinstance(dd.get("best"), dict) \
                and isinstance(dd["best"].get("point"), dict):
            pool.append((os.path.basename(q), fld, dd["best"]["point"]))
    for (tag, f2, ptj) in pool:
        if f2 != fld:
            continue
        try:
            b = W.load_point(ptj, K)
        except Exception:
            continue
        if set(b) != set(W.E_ALL25):
            continue
        if W.clean_ok(b, K) and W.allnz(b, K) and H.offstratum_cheap(25, b, K):
            warm.append((tag, b))
    OUT["n_warm_starts"] = len(warm)
    print("warm starts available: %d (%s)"
          % (len(warm), ",".join(t for t, _ in warm[:8])), flush=True)
    ck()

    while time.time() - t0 < secs:
        nres += 1
        bl = None
        if warm and (nres % 3 or not p):
            tag, b = warm[rng.randrange(len(warm))]
            bl = {e: [r[:] for r in b[e]] for e in b}
            for _ in range(rng.randrange(1, 6)):
                H.site_move_p(25, bl, rng.choice([0, 1, 2, 3, 4, 5, 7]),
                              rng, p) if p else \
                    H.site_move_q(mdl, bl, rng.choice([0, 1, 2, 3, 4, 5, 7]),
                                  rng)
        elif p:
            bl = H.seed_point_p(25, rng, p)
        else:
            import w26_wide as WD
            for _ in range(30):
                order = list(range(8))
                rng.shuffle(order)
                bl = WD.make(mdl, rng, passes=4, order=order)
                if bl is not None:
                    break
        if bl is None or not H.offstratum_cheap(25, bl, K):
            continue
        cur, _d = sc(bl)
        for _s in range(20000):
            if time.time() - t0 > secs:
                break
            # site 6 only moves A56/A67, which provably cannot change either
            # target -- steer away from it
            t = rng.choice([0, 1, 2, 3, 4, 5, 7])
            save = {e: [r[:] for r in bl[e]] for e in bl}
            moved = (H.site_move_p(25, bl, t, rng, p) if p
                     else H.site_move_q(mdl, bl, t, rng))
            if not moved or not H.offstratum_cheap(25, bl, K):
                for e in save:
                    bl[e] = save[e]
                continue
            new, det = sc(bl)
            if new >= cur:
                cur = new
                if cur > best:
                    best = cur
                    rep = L.vertex_report(25, bl, 'R', 6, K)
                    rec = dict(score=cur, restart=nres, step=_s, detail=det,
                               R6_delivers=rep['DELIVERS'],
                               R6_n_idx=rep['n_idx'],
                               alpha_nz=alpha_score(bl, K),
                               struct=alpha_struct(bl, K),
                               rank_Sp=[L.rank_rows(W.Sprime(bl, a, b), K)
                                        for a in range(3) for b in range(3)],
                               point=W.dump_point(bl))
                    OUT["best"] = rec
                    OUT["trace"].append({k: v for k, v in rec.items()
                                         if k != 'point'})
                    if cur >= TARGET:
                        OUT["hits"].append(rec)
                        print("*** TARGET REACHED %s %s" % (mode, fld),
                              flush=True)
                    ck()
                    print("%s %s r%d s%d score=%.4f R6=%s alphaNZ=%d "
                          "rankSp=%s struct=%s"
                          % (mode, fld, nres, _s, cur, rep['DELIVERS'],
                             rec['alpha_nz'], rec['rank_Sp'],
                             {k: v for k, v in rec['struct'].items()
                              if k.startswith('rank') or k == 'nZ'}),
                          flush=True)
            else:
                for e in save:
                    bl[e] = save[e]
    # ---- ledger 31: controls are EXECUTED on the stored points, never
    # asserted.  ok is None (not True) if nothing was stored to check.
    ctl, npts = W.executed_point_controls(OUT, K)
    OUT.update(ctl)
    for c in ("A1_clean", "A2_offstratum", "A3_allnz"):
        OUT["_controls_run"].append(c)
    tgt = None
    if OUT.get("best"):
        b2 = W.load_point(OUT["best"]["point"], K)
        tgt = sc(b2)[0]
    OUT["A4_target_exact"] = dict(
        executed=(tgt is not None), target=TARGET, best_reported=best,
        best_recomputed=tgt, n_points_checked=npts,
        agrees=(tgt is not None and abs(tgt - best) < 1e-9),
        n_hits=len(OUT["hits"]),
        ok=(None if tgt is None else abs(tgt - best) < 1e-9),
        note="the score is RECOMPUTED from the stored best point; beta "
             "target = Q == 0 on FAM_ALL and on one of FAM_01/FAM_02 in a "
             "single (y5,y7) class (equivalently rank S' = 2); alpha target "
             "= hafL == 0 on all of X_{R6,25}")
    OUT["_controls_run"].append("A4_target_exact")
    OUT["_manifest_ok"] = (sorted(OUT["_controls_run"]) == sorted(DECL))
    OUT["restarts"] = nres
    OUT["done"] = True
    ck()
    print("BUILD %s %s DONE best=%.4f hits=%d restarts=%d (%.0fs)"
          % (mode, fld, best, len(OUT["hits"]), nres, time.time() - t0),
          flush=True)


if __name__ == "__main__":
    main()
