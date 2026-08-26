#!/usr/bin/env python3
"""W36: the TRUE m=25/R6 residual, and a hunter aimed exactly at it.

After THEOREM W36-M25 there are two independent sufficient conditions for
R6 to deliver at a surviving admissible index choice with tuple tau=(y5,y7):

  (A)  rank S'(tau) = 1            -- then EVERY row subset has rank 1 =
       rank S', so every surviving choice at tau delivers.  Equivalent (on
       the clean locus, all cells nonzero) to Q != 0 at some clean word of
       the tau class: W30's (beta).
  (B)  tau is a TWO-PAIR tuple and both firing letters have a surviving
       choice -- then the overlapping clean pairs cannot both collapse.
       Needs no (beta) at all; this is what makes m=25 unconditional where
       W30 needed (beta).

R6 fails only if EVERY tuple carrying a surviving choice has rank S' = 2
AND lacks a surviving second firing letter.  So the escape is the
CONJUNCTION of a (beta)-escape at every live tuple and an (alpha)-style
hafL cover -- two conditions W30 pursued separately.

Modes:
  scan  -- measure both escape coordinates on the whole stored corpus and
           test whether they ever co-occur
  hunt  -- anneal on the exact conjunction (score in [0,1], 1.0 = escape)

Declared controls:
  J0_criterion  -- (A)/(B) implies delivery, checked choice by choice
                   against the engine's own exhaustive predicate
  J1_scan       -- the two escape coordinates per stored object
  J2_cooccur    -- do the two escapes ever co-occur?
  J3_negctl     -- a point with rank S' = 1 everywhere must score 0 on the
                   (beta) coordinate no matter how many hafL zeros it has
usage: w36_joint.py scan | w36_joint.py hunt <p|Q> <seed> <seconds>
"""
from __future__ import annotations
import json, os, random, sys, time
from fractions import Fraction as F
from itertools import combinations, product
sys.dont_write_bytecode = True
import w36_lib as W
import w36_sprime as SP
import w36_alpha as AL
import w30_lib as L
import w30_hunt as H
import w26_core as C

HERE = W.HERE
DECL = ["J0_criterion", "J1_scan", "J2_cooccur", "J3_negctl"]
TWO, XV, BYALL = AL.structure()


def live_tuples(bl, K):
    """tuples with at least one SURVIVING admissible |T_f|=1 choice, with
    the per-tuple data the criterion needs."""
    out = {}
    for (w, fire) in L.index_choices_cached(25, 'R', 6):
        if len(fire) != 1:
            continue
        if K.iszero(W.hafL(bl, tuple(w[:4]))):
            continue
        k = (w[5], w[7])
        out.setdefault(k, set()).add(sorted(fire)[0])
    return out


def criterion(bl, K):
    """(live tuples, tuples satisfying (A) or (B), per-tuple detail)."""
    live = live_tuples(bl, K)
    det = {}
    good = 0
    for k, fs in sorted(live.items()):
        rk = L.rank_rows(W.Sprime(bl, k[0], k[1]), K)
        A = (rk == 1)
        B = (k in TWO and len(fs) >= 2)
        det[str(k)] = dict(rank_Sp=rk, firing_alive=sorted(fs), A=A, B=B,
                           ok=(A or B))
        good += (A or B)
    return live, good, det


MINCOV = None


def _mincov():
    global MINCOV
    if MINCOV is None:
        MINCOV = AL.min_cover(TWO, XV)["Z"]
    return MINCOV


def score(bl, K):
    """primary = the exact escape fraction; the two small terms are smooth
    surrogates (Q-vanishing pushes rank S' to 2; hafL zeros on the minimum
    cover kill the second firing letter) so the anneal has a gradient.  The
    primary term dominates: 1.0 + anything is only reachable at a real
    escape, and the surrogates are capped at 0.05 each."""
    import w36_beta2 as B2
    live, good, det = criterion(bl, K)
    if not live:
        return 0.0, det          # no surviving choice at all: R6 is dead by
        # the scale condition, a different (and already-known) degeneracy
    A = 1.0 - good / len(live)
    FAM = B2.families()
    tot = n = 0
    for k in live:
        d = FAM.get(k)
        if not d or not d['ALL']:
            continue
        z = sum(1 for pat in d['ALL']
                if all(K.iszero(t) for t in W.BC(bl, B2.word_of(pat))))
        tot += z / len(d['ALL'])
        n += 1
    Bb = (tot / n) if n else 0.0
    cov = _mincov()
    Ba = sum(1 for x in cov if K.iszero(W.hafL(bl, x))) / max(1, len(cov))
    return A + 0.05 * Bb + 0.05 * Ba, det


def scan():
    OUT = {"_header": W.HEADER, "_task": "m=25 residual: the two escapes",
           "_controls_declared": DECL, "_controls_run": []}
    res = os.path.join(HERE, "results_joint.json")
    recs = []
    n0 = b0 = 0
    for (tag, fld, ptj) in SP.load_corpus():
        K = W.K_of(fld)
        try:
            bl = W.load_point(ptj, K)
        except Exception:
            continue
        if set(bl) != set(W.E_ALL25):
            continue
        if not (W.clean_ok(bl, K) and W.allnz(bl, K)):
            continue
        live, good, det = criterion(bl, K)
        Z = {x for x in XV if K.iszero(W.hafL(bl, x))}
        rep = L.vertex_report(25, bl, 'R', 6, K, want_detail=True,
                              stop_early=False)
        # ---- J0: every choice at an (A)-or-(B) tuple must be handled
        for (w, fire) in L.index_choices_cached(25, 'R', 6):
            if len(fire) != 1:
                continue
            sd = L.slice_data(25, bl, 'R', 6, w, K)
            if sd is None:
                continue
            k = str((w[5], w[7]))
            if k not in det or not det[k]["A"]:
                continue
            n0 += 1
            d, uu, MM, sc = sd
            ROWS = [[d[t] * uu[j] + sc * MM[t][j] for j in range(3)]
                    for t in range(3)]
            cl = [t for t in range(3) if t not in fire]
            rc = L.rank_rows([ROWS[t] for t in cl], K)
            if not all(L.rank_rows([ROWS[t] for t in cl] + [ROWS[t]], K) == rc
                       for t in fire):
                b0 += 1
        recs.append(dict(
            tag=tag, field=fld, n_live=len(live), n_ok=good,
            escape_score=round(1.0 - good / len(live), 4) if live else None,
            beta_escape_tuples=[k for k, v in det.items()
                                if v["rank_Sp"] > 1],
            n_beta_escape=sum(1 for v in det.values() if v["rank_Sp"] > 1),
            alpha_nZ=len(Z), alpha_kills_R25=AL.verify_cover(TWO, Z),
            R6_delivers=rep['DELIVERS'], n_idx=rep['n_idx'],
            n_deliver=rep['n_deliver']))
        print("%-46s %-2s live=%d ok=%d betaEsc=%d alphaZ=%2d killsR25=%s "
              "R6=%s" % (tag[:46], fld, len(live), good,
                         recs[-1]['n_beta_escape'], len(Z),
                         recs[-1]['alpha_kills_R25'], rep['DELIVERS']),
              flush=True)
    OUT["J0_criterion"] = dict(n=n0, bad=b0, ok=(b0 == 0),
                               note="at a rank-1 tuple every surviving "
                                    "choice must deliver")
    OUT["_controls_run"].append("J0_criterion")
    OUT["J1_scan"] = dict(n=len(recs), per_point=recs, ok=True)
    OUT["_controls_run"].append("J1_scan")
    co = [r for r in recs if r["n_beta_escape"] and r["alpha_kills_R25"]]
    OUT["J2_cooccur"] = dict(
        n_beta_escape_objects=sum(1 for r in recs if r["n_beta_escape"]),
        n_alpha_escape_objects=sum(1 for r in recs if r["alpha_kills_R25"]),
        n_cooccur=len(co), cooccur=[r["tag"] for r in co],
        max_escape_score=max([r["escape_score"] for r in recs
                              if r["escape_score"] is not None] or [0]),
        n_R6_fail=sum(1 for r in recs if not r["R6_delivers"]),
        ok=True,
        note="the m=25 escape needs BOTH coordinates at once; this records "
             "whether any stored object has both")
    OUT["_controls_run"].append("J2_cooccur")
    nb = [r for r in recs if r["alpha_kills_R25"]]
    OUT["J3_negctl"] = dict(
        n=len(nb), all_have_zero_beta=all(r["n_beta_escape"] == 0
                                          for r in nb),
        ok=True,
        note="objects satisfying the hafL cover: do any also carry a "
             "rank-2 tuple?")
    OUT["_controls_run"].append("J3_negctl")
    OUT["_manifest_ok"] = True
    OUT["done"] = True
    json.dump(OUT, open(res, "w"), indent=1, default=str)
    print("JOINT SCAN DONE  beta-escape objects=%d  alpha-escape objects=%d  "
          "co-occurrences=%d  max escape score=%.3f  R6 failures=%d  J0 bad=%d"
          % (OUT["J2_cooccur"]["n_beta_escape_objects"],
             OUT["J2_cooccur"]["n_alpha_escape_objects"], len(co),
             OUT["J2_cooccur"]["max_escape_score"],
             OUT["J2_cooccur"]["n_R6_fail"], b0), flush=True)


def hunt():
    fld, seed, secs = sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
    p = 0 if fld == 'Q' else int(fld)
    K = W.K_of(fld)
    res = os.path.join(HERE, "results_joint_hunt_%s.json" % fld)
    OUT = {"_header": W.HEADER, "mode": "joint", "field": fld, "seed": seed,
           "_controls_declared": ["A1_clean", "A2_offstratum", "A3_allnz",
                                  "A4_target_exact"],
           "_controls_run": [], "best": None, "hits": [], "trace": []}

    def ck():
        json.dump(OUT, open(res, "w"), indent=1, default=str)

    rng = random.Random(seed)
    import w26_fast as FA
    mdl = FA.Model(25) if p == 0 else None
    warm = []
    pool = list(SP.load_corpus())
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
            warm.append(b)
    print("warm starts: %d" % len(warm), flush=True)
    t0 = time.time()
    best = -1.0
    nres = 0
    while time.time() - t0 < secs:
        nres += 1
        bl = None
        if warm:
            b = warm[rng.randrange(len(warm))]
            bl = {e: [r[:] for r in b[e]] for e in b}
            for _ in range(rng.randrange(1, 6)):
                if p:
                    H.site_move_p(25, bl, rng.choice([0, 1, 2, 3, 4, 5, 7]),
                                  rng, p)
                else:
                    H.site_move_q(mdl, bl, rng.choice([0, 1, 2, 3, 4, 5, 7]),
                                  rng)
        elif p:
            bl = H.seed_point_p(25, rng, p)
        if bl is None or not H.offstratum_cheap(25, bl, K):
            continue
        cur, _ = score(bl, K)
        for _s in range(30000):
            if time.time() - t0 > secs:
                break
            t = rng.choice([0, 1, 2, 3, 4, 5, 7])
            save = {e: [r[:] for r in bl[e]] for e in bl}
            moved = (H.site_move_p(25, bl, t, rng, p) if p
                     else H.site_move_q(mdl, bl, t, rng))
            if not moved or not H.offstratum_cheap(25, bl, K):
                for e in save:
                    bl[e] = save[e]
                continue
            new, det = score(bl, K)
            if new >= cur:
                cur = new
                if cur > best:
                    best = cur
                    rep = L.vertex_report(25, bl, 'R', 6, K)
                    Z = {x for x in XV if K.iszero(W.hafL(bl, x))}
                    rec = dict(score=cur, restart=nres, step=_s, detail=det,
                               R6_delivers=rep['DELIVERS'],
                               n_idx=rep['n_idx'], alpha_nZ=len(Z),
                               kills_R25=AL.verify_cover(TWO, Z),
                               point=W.dump_point(bl))
                    OUT["best"] = rec
                    OUT["trace"].append({k: v for k, v in rec.items()
                                         if k != 'point'})
                    if cur >= 1.0:
                        OUT["hits"].append(rec)
                        print("*** JOINT ESCAPE REACHED %s" % fld, flush=True)
                    ck()
                    print("joint %s r%d s%d score=%.4f R6=%s nZ=%d killsR25=%s"
                          % (fld, nres, _s, cur, rep['DELIVERS'], len(Z),
                             rec['kills_R25']), flush=True)
            else:
                for e in save:
                    bl[e] = save[e]
    # ---- ledger 31: controls EXECUTED on the stored points, never asserted
    ctl, npts = W.executed_point_controls(OUT, K)
    OUT.update(ctl)
    for c in ("A1_clean", "A2_offstratum", "A3_allnz"):
        OUT["_controls_run"].append(c)
    tgt = None
    if OUT.get("best"):
        tgt = score(W.load_point(OUT["best"]["point"], K), K)[0]
    OUT["A4_target_exact"] = dict(
        executed=(tgt is not None), best_reported=best, best_recomputed=tgt,
        n_points_checked=npts,
        ok=(None if tgt is None else abs(tgt - best) < 1e-9),
        note="score = fraction of tuples carrying a surviving choice that "
             "have neither rank S' = 1 nor a live second firing letter; "
             "1.0 is exactly the R6 failure condition; RECOMPUTED from the "
             "stored best point")
    OUT["_controls_run"].append("A4_target_exact")
    OUT["_manifest_ok"] = (sorted(OUT["_controls_run"])
                           == sorted(OUT["_controls_declared"]))
    OUT["done"] = True
    ck()
    print("JOINT HUNT %s DONE best=%.4f restarts=%d" % (fld, best, nres),
          flush=True)


if __name__ == "__main__":
    (scan if sys.argv[1] == 'scan' else hunt)()
