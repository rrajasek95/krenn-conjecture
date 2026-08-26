#!/usr/bin/env python3
"""A11 closing checks.  UNAUDITED.

P1  the LAST link of M25-CONDITIONAL's conclusion chain: "R6 delivers =>
    pure row".  A delivering index choice buys a genuine pure row only when
    a firing completion has EXACTLY ONE active live single whose coefficient
    haf_{Gamma - e} is nonzero (and no degree-2 z-term).  Measured on the
    whole m=25 corpus; this step is a CONTROL in the spine (HGAP), never a
    proof, and M25-CONDITIONAL inherits that status.

P2  trace of the blind test's CONVERSE exceptions (rank 3 yet delivering):
    which mechanism delivers there.

P3  escape completion fractions at the live r10 F_31 point.
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from collections import Counter, defaultdict
from itertools import combinations, product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W30 = os.path.join(os.path.dirname(HERE), "unaudited-exclusion-w30-2026-08-19")
sys.path.insert(0, HERE)
import a11_lib as A      # noqa: E402
import a11_m25 as M      # noqa: E402

DECL = ["P1_pure_row", "P1_pure_row_control", "P2_converse_traces",
        "P3_escape_fraction"]


def active_any(tm, w):
    return tuple(e for e in sorted(tm.single)
                 if (w[e[0]], w[e[1]]) == tm.single[e])


def has_deg2(tm, w):
    act = active_any(tm, w)
    for a, b in combinations(act, 2):
        vs = set(a) | set(b)
        if len(vs) != 4:
            continue
        if tm._gamma_pm_exists(tuple(u for u in range(8) if u not in vs)):
            return True
    return False


def pure_row_at(tm, bl, w, K):
    """(has_pure_row, reason) for a completed word w"""
    act = tm.fired(w)
    if len(act) != 1:
        return False, "n_active_live=%d" % len(act)
    if has_deg2(tm, w):
        return False, "degree-2 z-term"
    e = act[0]
    coef = A.gamma_haf_minus(tm, bl, w, e, K)
    if K.iszero(coef):
        return False, "zero single coefficient"
    return True, "ok"


def main():
    t0 = time.time()
    man = A.Manifest(DECL)
    rng = random.Random(2718281)
    tm = A.T(25)

    # --------------------------------------------------------- P1 pure row
    pts = []
    dq = json.load(open(os.path.join(W30, "points_m25_wide.json")))
    for r in dq["points"]:
        if not r.get("van"):
            pts.append(("Q_%d" % r["seed"], A.Rat, r["point"]))
    t2 = json.load(open(os.path.join(HERE, "results_t2.json")))
    for r in t2["V2_A11_family"]["records"]:
        K = A.Modp(13) if r["field"] == "F_13" else A.Modp(31)
        pts.append(("A11_%s_%d" % (r["field"], r["from_seed"]), K, r["point"]))
    for fn in ("results_r10_beta_13.json", "results_r10_beta_31.json"):
        d = json.load(open(os.path.join(W30, fn)))
        K = A.Modp(13) if "13" in fn else A.Modp(31)
        pts.append((fn, K, d["best"]["point"]))

    recs = []
    for (tag, K, ptj) in pts:
        bl = A.load_point(ptj, K)
        ver = A.verdict(tm, bl, 'R6', K, detail=True)
        npure = 0
        reasons = Counter()
        for (w, Tf, Tc, ok) in ver['recs']:
            if not ok:
                continue
            got = False
            for t in Tf:
                ww = tuple(w[:6] + (t,) + w[7:])
                p, why = pure_row_at(tm, bl, ww, K)
                if p:
                    got = True
                else:
                    reasons[why] += 1
            npure += 1 if got else 0
        recs.append(dict(tag=tag, delivers=ver['DELIVERS'],
                         n_deliver=ver['n_deliver'],
                         n_deliver_with_pure_row=npure,
                         no_pure_reasons=dict(reasons)))
        print("[P1 %s] deliver=%d with pure row=%d" %
              (tag, ver['n_deliver'], npure), flush=True)
    man.record("P1_pure_row", dict(
        n_points=len(recs), records=recs,
        n_points_delivering_without_any_pure_row=sum(
            1 for r in recs if r['delivers'] and
            r['n_deliver_with_pure_row'] == 0),
        ok=all((not r['delivers']) or r['n_deliver_with_pure_row'] > 0
               for r in recs),
        note="reproduces the spine's HGAP control (n_deliver_no_pure = 0) "
             "at m=25/R6 on my own engine.  It is a MEASUREMENT, not a "
             "proof: M25-CONDITIONAL's '=> pure row' step has exactly the "
             "same empirical status as it does in Lemma W30-Y."))

    # control: the pure-row test must be able to say NO
    nno = 0
    for (tag, K, ptj) in pts[:3]:
        bl = A.load_point(ptj, K)
        for w in tm.clean_words[:400]:
            p, why = pure_row_at(tm, bl, w, K)
            if not p:
                nno += 1
    man.record("P1_pure_row_control", dict(
        n_negative_answers=nno, ok=nno > 0,
        note="clean words have no active live single, so the tester must "
             "reject them -- it is not a constant-true predicate"))
    print("P1 control negatives %d" % nno)

    # --------------------------------------------------- P2 converse traces
    dat = json.load(open(os.path.join(W30, "points_hunt.json")))
    pool = [r for r in dat["points"]]
    rng.shuffle(pool)
    traces = []
    seen = 0
    for r in pool:
        if len(traces) >= 8 or time.time() - t0 > 500:
            break
        m = int(r["m"])
        K = A.Rat if int(r["p"]) == 0 else A.Modp(int(r["p"]))
        tmm = A.T(m)
        bl = A.load_point(r["point"], K)
        for lab in A.VLAB:
            kind, v = A.vsplit(lab)
            letters = sorted({l for (_e, _t, _tv, l)
                              in A.singles_into(tmm, kind, v)})
            if len(letters) < 2:
                continue
            ver = A.verdict(tmm, bl, lab, K, detail=True)
            if not ver['DELIVERS']:
                continue
            ranks = set()
            for tau in product(range(3), repeat=len(tmm.nbr[v])):
                ranks.add(A.rank(A.slice_S(tmm, bl, v, tau, K), K))
            if min(ranks) != 3:
                continue
            seen += 1
            # it delivers with EVERY tuple at rank 3: how?
            mech = Counter()
            for (w, Tf, Tc, ok) in ver['recs']:
                if not ok:
                    continue
                rows, coef, sc, cols = A.master_rows(tmm, bl, kind, v, w, K)
                tau = tuple(w[s] for s in tmm.nbr[v])
                S = A.slice_S(tmm, bl, v, tau, K)
                rphi = A.rank(rows, K)
                rS = A.rank(S, K)
                if all(K.iszero(z) for t in Tf for z in rows[t]):
                    mech['firing_ROW_is_zero_(ker_phi)'] += 1
                elif rphi < rS:
                    mech['phi_drops_rank_(D2)'] += 1
                else:
                    mech['other'] += 1
            traces.append(dict(tag=r["tag"], m=m, p=int(r["p"]), vertex=lab,
                               ranks=sorted(ranks), n_deliver=ver['n_deliver'],
                               mechanisms=dict(mech)))
            print("[P2] %s %s ranks=%s n_deliver=%d mech=%s"
                  % (r["tag"][:40], lab, sorted(ranks), ver['n_deliver'],
                     dict(mech)), flush=True)
    man.record("P2_converse_traces", dict(
        n_traced=len(traces), traces=traces, ok=True,
        note="rank 3 at EVERY tuple and the vertex still delivers: these are "
             "the CONVERSE failures.  W30-Z does not claim the converse; "
             "round 4 refuted it; the blind-test line 'FAIL at rank 3 "
             "112/114' measures a false statement."))

    # ------------------------------------------------ P3 escape fractions
    d = json.load(open(os.path.join(W30, "results_r10_beta_31.json")))
    K = A.Modp(31)
    bl = A.load_point(d["best"]["point"], K)
    phi = {w: A.phi_gpm(tm, bl, w, K) for w in A.WORDS}
    other = [u for u in range(8) if u != 6]
    per = defaultdict(lambda: [0, 0])
    for vals in product(range(3), repeat=7):
        w = [0] * 8
        for u, a in zip(other, vals):
            w[u] = a
        if not all(K.iszero(phi[tuple(w[:6] + [t] + w[7:])])
                   for t in range(3)):
            continue
        ww = tuple(w)
        B, C = M.BC_closed(tm, bl, ww, K)
        key = (ww[5], ww[7])
        per[key][1] += 1
        if K.iszero(B) and K.iszero(C):
            per[key][0] += 1
    live = Counter()
    for (w, Tf, Tc) in A.admissible_cached(25, 'R', 6):
        if not K.iszero(A.hafL(tm, bl, w, K)):
            live[(w[5], w[7])] += 1
    frac = {str(k): dict(Q0=v[0], untriggered=v[1], live_choices=live.get(k, 0),
                         escape_complete=(v[0] == v[1] and v[1] > 0))
            for k, v in sorted(per.items())}
    man.record("P3_escape_fraction", dict(
        per_tuple=frac,
        n_tuples_fully_escaped=sum(1 for v in frac.values()
                                   if v['escape_complete']),
        best_fraction=max((v['Q0'] / float(v['untriggered'])
                           for v in frac.values()), default=0.0),
        ok=True,
        note="the escape needs Q = 0 at EVERY untriggered word of at least "
             "one live tuple; this is the completion fraction reached"))
    print("P3 escape fractions %s" % frac)

    man.finish(os.path.join(HERE, "results_t6.json"),
               extra={"_header": "UNAUDITED A11 closing checks",
                      "elapsed_s": round(time.time() - t0, 1)})
    print("T6 DONE in %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
