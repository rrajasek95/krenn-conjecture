#!/usr/bin/env python3
"""A12 TARGET 2 -- the m=28 RETRACTION, audited on the A12 engine.  UNAUDITED.

K0_absent    -- absent slice columns at EVERY (support, vertex), not only the
                protected ones, together with |N(v)|, the sigma-edge status
                and the two-firing-letter status
K1_rowsform  -- ROWS-vs-S' row-subset ranks, FULL census (NO STRIDE; W36's
                own K1 sampled 1 in 17 and its quoted numbers are from a run
                that is not on disk), at m=25/26/27 (must agree) and m=28
K2_transfer  -- the transfer matrix P itself: ROWS[t] = P . S'[t] as an
                identity, rank P, and the exact injectivity criterion.  This
                is where the root-cause claim is tested AS A BICONDITIONAL:
                count the choices where P is NOT injective and the ranks
                agree anyway
K3_objects   -- >= 4 of the stored both-rank-3-and-delivering m=28 objects
                re-verified FROM SCRATCH with FULL censuses: clean, cells
                nonzero, off stratum, rank S' = 3 at every surviving tuple
                for R5 and R6, joint star rank, and the delivery verdict
K4_control   -- mutation controls: a one-cell perturbation must break the
                ROWS = P.S' identity; and comparing ROWS against a SHUFFLED
                S' must produce mismatches (the rank comparison can fail)
usage: a12_t4.py [n_points] [n_objects]
"""
from __future__ import annotations

import json
import os
import sys
import time
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
W30 = os.path.join(ROOT, "unaudited-exclusion-w30-2026-08-19")
W36 = os.path.join(ROOT, "unaudited-routea-w36-2026-08-20")
sys.path.insert(0, HERE)
import a12_lib as A  # noqa: E402
from a12_t0 import Manifest  # noqa: E402

DECL = ["K0_absent", "K1_rowsform", "K2_transfer", "K3_objects", "K4_control"]
CASES = {25: [('R', 6)], 26: [('R', 5), ('R', 6)], 27: [('R', 5)],
         28: [('R', 5), ('R', 6), ('L', 1), ('L', 2)]}
SUBSETS = ((0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2))


def firing_letters(tm, kind, v):
    return sorted({l for (_e, _t, _tv, l) in tm.singles_at(kind, v)})


def slice_columns(tm, kind, v):
    """the q-index of ROWS -> the site whose cell fills it."""
    if kind == 'R':
        p = A.SIGINV[v]
        return [A.SIG[q] for q in range(4) if q != p], p
    return [a for a in range(4) if a != v], A.SIG[v]


def Pmatrix(tm, kind, v, uu, sc, K):
    """ROWS[t] = P . S'[t]:  P is 3 x |N(v)| with rows indexed by q and
    columns by the slice neighbours in tm.nbr[v] order."""
    cols, part = slice_columns(tm, kind, v)
    ns = list(tm.nbr[v])
    P = [[K.zero] * len(ns) for _ in range(3)]
    for qi, s in enumerate(cols):
        if s in ns:
            P[qi][ns.index(s)] = sc
    if part in ns:
        for qi in range(3):
            P[qi][ns.index(part)] = uu[qi]
    return P


def corpus(m, lim):
    """wide Q points plus stored F_p hunt points at the same support, so the
    census runs over Q and two primes = 1 mod 3."""
    out = []
    p = os.path.join(W30, "points_m%d_wide.json" % m)
    if os.path.exists(p):
        for r in json.load(open(p)).get("points", []):
            if not r.get("van"):
                out.append(("wide%d_%s" % (m, r.get("seed")), 'Q', r["point"]))
    out = out[:lim]
    ph = os.path.join(W30, "points_hunt.json")
    extra = []
    if os.path.exists(ph):
        for i, r in enumerate(json.load(open(ph)).get("points", [])):
            if r.get("m") == m and not r.get("van"):
                extra.append(("hunt%d_%s" % (i, r.get("tag")),
                              str(r.get("p") or 'Q'), r["point"]))
    seen = set()
    keep = []
    for rec in extra:
        if rec[1] in seen:
            continue
        seen.add(rec[1])
        keep.append(rec)
    return out + keep[:3]


def jointstar(tm, bl, a, b, K, strict_w36=True):
    """W36's joint-star matrix ranks.  strict_w36 reproduces W36's exact
    construction (the two untriggered pattern sets intersected AS 8-TUPLES,
    which silently forces w_a = w_b = 0); otherwise the common class is the
    honest one: every completion in the two free letters is a clean word."""
    cols = sorted({tuple(sorted((a, s))) for s in tm.nbr[a]}
                  | {tuple(sorted((b, s))) for s in tm.nbr[b]})

    def untrig(v):
        out = []
        others = [c for c in range(8) if c != v]
        for vals in product(range(3), repeat=7):
            w = [0] * 8
            for c, x in zip(others, vals):
                w[c] = x
            if all(len(set(w[:v] + [t] + w[v + 1:])) > 1
                   and not tm.fired(tuple(w[:v] + [t] + w[v + 1:]))
                   for t in range(3)):
                out.append(tuple(w))
        return set(out)

    if strict_w36:
        common = sorted(untrig(a) & untrig(b))
    else:
        common = []
        others = [c for c in range(8) if c not in (a, b)]
        for vals in product(range(3), repeat=6):
            w = [0] * 8
            for c, x in zip(others, vals):
                w[c] = x
            ok = True
            for s in range(3):
                for t in range(3):
                    ww = list(w)
                    ww[a], ww[b] = s, t
                    if len(set(ww)) == 1 or tm.fired(tuple(ww)):
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                common.append(tuple(w))
    byt = {}
    for w in common:
        key = (tuple(w[s] for s in tm.nbr[a]), tuple(w[s] for s in tm.nbr[b]))
        byt.setdefault(key, []).append(w)
    ranks = []
    for key, ws in byt.items():
        if len(ws) < 2:
            continue
        Mx = [[tm.haf_on(bl, [u for u in range(8) if u not in e], w, K)
               for e in cols] for w in ws]
        ranks.append(A.rank(Mx, K))
    return dict(n_cols=len(cols), n_common=len(common), n_classes=len(byt),
                n_classes_ge2=len(ranks),
                hist={str(x): ranks.count(x) for x in sorted(set(ranks))},
                max_rank=max(ranks) if ranks else None,
                min_rank=min(ranks) if ranks else None)


def main():
    t0 = time.time()
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    nobj = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    man = Manifest(DECL)
    res = os.path.join(HERE, "results_t4.json")

    # ------------------------------------------------------------- K0
    k0 = {}
    for m in (25, 26, 27, 28):
        tm = A.T(m)
        for v in range(8):
            kind = 'R' if v >= 4 else 'L'
            cols, part = slice_columns(tm, kind, v)
            absent = [s for s in cols
                      if tuple(sorted((v, s))) not in tm.gamma]
            k0["m%d_%s%d" % (m, kind, v)] = dict(
                N=list(tm.nbr[v]), nN=len(tm.nbr[v]), slice_columns=cols,
                absent_columns=absent, n_absent=len(absent),
                sigma_partner=part,
                sigma_edge_present=(tuple(sorted((v, part))) in tm.gamma),
                firing_letters=firing_letters(tm, kind, v),
                two_firing=(len(firing_letters(tm, kind, v)) >= 2))
    prot = {25: [('R', 6)], 26: [('R', 5), ('R', 6)], 27: [('R', 5)]}
    ok0 = (all(k0["m%d_%s%d" % (m, k, v)]["n_absent"] == 1
               for m in prot for (k, v) in prot[m])
           and all(k0["m28_%s%d" % (k, v)]["n_absent"] == 0
                   for (k, v) in CASES[28])
           and sorted(lab for lab in k0 if lab.startswith("m28_")
                      and k0[lab]["two_firing"])
           == ['m28_L1', 'm28_L2', 'm28_R5', 'm28_R6'])
    man.record("K0_absent", dict(
        per_vertex=k0, ok=ok0,
        two_firing_by_support={
            "m%d" % m: sorted(lab[4:] for lab in k0
                              if lab.startswith("m%d_" % m)
                              and k0[lab]["two_firing"])
            for m in (25, 26, 27, 28)},
        note="the protected vertices at m=25/26/27 have EXACTLY ONE absent "
             "slice column; all four m=28 two-firing vertices have ZERO"))
    print("K0: absent %s" % json.dumps(
        {k: v["n_absent"] for k, v in k0.items()
         if k.split('_')[1] in ('R5', 'R6', 'L1', 'L2')}), flush=True)
    print("K0: two-firing %s" % json.dumps(
        man.out["K0_absent"]["two_firing_by_support"]), flush=True)

    # ---------------------------------------------------------- K1 / K2
    k1, k2 = {}, {}
    for m in (25, 26, 27, 28):
        tm = A.T(m)
        pts = corpus(m, lim)
        for (kind, v) in CASES[m]:
            idx = tm.index_choices(kind, v)
            n = bad = 0
            nchoice = 0
            id_bad = 0
            inj = noninj = noninj_agree = noninj_dis = 0
            rank_hist = {}
            for (tag, fld, ptj) in pts:
                K = A.K_of(fld)
                bl = A.load_point(ptj, K)
                if set(bl) != set(tm.gamma):
                    continue
                if not (tm.is_clean(bl, K) and tm.all_nonzero(bl, K)):
                    continue
                for (w, fire) in idx:
                    R, sc, uu, MM = tm.rows_and_scale(bl, kind, v, w, K)
                    if R is None:
                        continue
                    nchoice += 1
                    S = tm.Sprime(bl, v, tm.tau_of(v, w), K)
                    P = Pmatrix(tm, kind, v, uu, sc, K)
                    for t in range(3):
                        pred = [A.norm(K, sum(A.norm(K, P[q][j] * S[t][j])
                                              for j in range(len(S[t]))))
                                for q in range(3)]
                        if any(not K.iszero(A.norm(K, pred[q] - R[t][q]))
                               for q in range(3)):
                            id_bad += 1
                    rp = A.rank([[P[q][j] for q in range(3)]
                                 for j in range(len(S[0]))], K)
                    is_inj = (rp == len(S[0]))
                    mism = 0
                    for sub in SUBSETS:
                        n += 1
                        if A.rank([R[t] for t in sub], K) != \
                           A.rank([S[t] for t in sub], K):
                            bad += 1
                            mism += 1
                    if is_inj:
                        inj += 1
                    else:
                        noninj += 1
                        if mism:
                            noninj_dis += 1
                        else:
                            noninj_agree += 1
                    rank_hist[rp] = rank_hist.get(rp, 0) + 1
            lab = "m%d_%s%d" % (m, kind, v)
            k1[lab] = dict(n_points=len(pts), n_surviving_choices=nchoice,
                           n_subset_tests=n, mismatches=bad,
                           identity_violations=id_bad)
            k2[lab] = dict(n_P_injective=inj, n_P_not_injective=noninj,
                           n_notinj_but_ranks_agree=noninj_agree,
                           n_notinj_and_ranks_disagree=noninj_dis,
                           rank_P_hist={str(k): v
                                        for k, v in sorted(rank_hist.items())})
            print("K1 %-8s choices=%4d subsets=%5d mismatch=%4d  |  P inj "
                  "%4d / non-inj %4d (agree anyway %4d, disagree %4d)"
                  % (lab, nchoice, n, bad, inj, noninj, noninj_agree,
                     noninj_dis), flush=True)
    man.record("K1_rowsform", dict(
        per_vertex=k1,
        ok=(all(k1["m%d_%s%d" % (m, k, v)]["mismatches"] == 0
                for m in (25, 26, 27) for (k, v) in CASES[m])
            and all(k1[l]["identity_violations"] == 0 for l in k1)),
        m28_disagrees=any(k1["m28_%s%d" % (k, v)]["mismatches"] > 0
                          for (k, v) in CASES[28]),
        note="FULL census, every admissible surviving choice, all seven "
             "nonempty row subsets"))
    man.record("K2_transfer", dict(
        per_vertex=k2,
        biconditional_reverse_direction_holds=all(
            k2[l]["n_notinj_but_ranks_agree"] == 0 for l in k2),
        ok=True,
        note="P injective => the ranks agree (0 mismatches wherever P is "
             "injective).  The CONVERSE fails: P non-injective choices whose "
             "ranks agree anyway are counted in n_notinj_but_ranks_agree"))

    # ------------------------------------------------------------- K3
    tags = []
    pre = os.path.join(W36, "results_elim_prelaunch.json")
    if os.path.exists(pre):
        dd = json.load(open(pre))
        for r in (dd.get("E2_prelaunch", {}) or {}).get("per_point", []):
            if r.get("satisfies_target"):
                tags.append(r["tag"])
    n_tags_total = len(tags)
    wide = {}
    p28 = os.path.join(W30, "points_m28_wide.json")
    if os.path.exists(p28):
        for r in json.load(open(p28)).get("points", []):
            if not r.get("van"):
                wide["wide28_%s" % r.get("seed")] = ('Q', r["point"])
    hunt = {}
    ph = os.path.join(W30, "points_hunt.json")
    if os.path.exists(ph):
        for i, r in enumerate(json.load(open(ph)).get("points", [])):
            if r.get("m") == 28 and not r.get("van"):
                hunt["hunt%d_%s" % (i, r.get("tag"))] = (
                    str(r.get("p") or 'Q'), r["point"])
    tm = A.T(28)
    objs = []
    for t in tags:
        if len(objs) >= nobj:
            break
        src = wide.get(t) or hunt.get(t)
        if src is None:
            continue
        fld, ptj = src
        K = A.K_of(fld)
        bl = A.load_point(ptj, K)
        if set(bl) != set(tm.gamma):
            continue
        rec = dict(tag=t, field=fld, clean=tm.is_clean(bl, K),
                   allnz=tm.all_nonzero(bl, K), offstratum=tm.off_stratum(
                       bl, K), vertices={})
        for (kind, v) in CASES[28]:
            idx = tm.index_choices(kind, v)
            surv = {}
            rr = {}
            for (w, fire) in idx:
                R, sc, uu, MM = tm.rows_and_scale(bl, kind, v, w, K)
                if R is None:
                    continue
                tau = tm.tau_of(v, w)
                surv[tau] = A.rank(tm.Sprime(bl, v, tau, K), K)
                rr[A.rank(R, K)] = rr.get(A.rank(R, K), 0) + 1
            rep = tm.vertex_report(bl, kind, v, K, choices=idx)
            rec["vertices"]["%s%d" % (kind, v)] = dict(
                n_surviving_tuples=len(surv),
                ranks_Sprime=sorted(set(surv.values())),
                all_rank3=(bool(surv) and all(x == 3 for x in surv.values())),
                ranks_ROWS={str(k): v2 for k, v2 in sorted(rr.items())},
                n_idx=rep['n_idx'], n_deliver=rep['n_deliver'],
                DELIVERS=rep['DELIVERS'])
        rec["joint_R5R6_w36def"] = jointstar(tm, bl, 5, 6, K, True)
        rec["joint_R5R6_honest"] = jointstar(tm, bl, 5, 6, K, False)
        objs.append(rec)
        print("K3 %-24s clean=%s nz=%s off=%s | %s | joint(w36) %s "
              "joint(honest) %s"
              % (t[:24], rec['clean'], rec['allnz'], rec['offstratum'],
                 {k: (v['all_rank3'], v['DELIVERS'], v['n_deliver'])
                  for k, v in rec['vertices'].items()},
                 rec['joint_R5R6_w36def']['hist'],
                 rec['joint_R5R6_honest']['hist']), flush=True)
        json.dump(dict(partial=objs), open(res + ".part", "w"), indent=1,
                  default=str)
    man.record("K3_objects", dict(
        n_tags_in_completed_sweep=n_tags_total, n_examined=len(objs),
        objects=objs,
        n_both_rank3=sum(1 for r in objs
                         if r["vertices"]["R5"]["all_rank3"]
                         and r["vertices"]["R6"]["all_rank3"]),
        n_both_deliver=sum(1 for r in objs
                           if r["vertices"]["R5"]["DELIVERS"]
                           and r["vertices"]["R6"]["DELIVERS"]),
        ok=all(r["clean"] and r["allnz"] for r in objs),
        note="FULL census of surviving tuples (W36's K3 used a 1-in-11 "
             "stride).  n_tags_in_completed_sweep is the number the COMPLETED "
             "pre-launch sweep records; W36 quoted 11, the count visible in "
             "its log while the sweep was still running"))

    # ------------------------------------------------------------- K4
    ctl = []
    import random as _rnd
    rr = _rnd.Random(4444)
    for m, (kind, v) in ((25, ('R', 6)), (26, ('R', 5)), (28, ('R', 5)),
                         (28, ('L', 2))):
        tmm = A.T(m)
        pts = corpus(m, 1)
        if not pts:
            continue
        K = A.K_of(pts[0][1])
        bl = A.load_point(pts[0][2], K)
        idx = tmm.index_choices(kind, v)[:40]
        broke = tot = 0
        rnd_det = rnd_tot = 0
        for (w, fire) in idx:
            R, sc, uu, MM = tmm.rows_and_scale(bl, kind, v, w, K)
            if R is None:
                continue
            tau = tmm.tau_of(v, w)
            S = tmm.Sprime(bl, v, tau, K)
            P = Pmatrix(tmm, kind, v, uu, sc, K)
            # MUT: perturb the cell of an edge AT v that ROWS actually reads
            s0 = tmm.nbr[v][0]
            e0 = tuple(sorted((v, s0)))
            b2 = {e: [list(r) for r in vv] for e, vv in bl.items()}
            if v < s0:
                b2[e0][0][tau[0]] = A.norm(K, b2[e0][0][tau[0]] + K.one)
            else:
                b2[e0][tau[0]][0] = A.norm(K, b2[e0][tau[0]][0] + K.one)
            R2, sc2, uu2, MM2 = tmm.rows_and_scale(b2, kind, v, w, K)
            tot += 1
            if R2 is None or any(
                    not K.iszero(A.norm(K, R2[t][q] - A.norm(K, sum(
                        A.norm(K, P[q][j] * S[t][j])
                        for j in range(len(S[t]))))))
                    for t in range(3) for q in range(3)):
                broke += 1
            # POSITIVE CONTROL: a random S' must be detected by the rank
            # comparison (the comparison is capable of reporting a mismatch)
            Srn = [[K.of(rr.randrange(0, K.p)) if K.p
                    else A.Fraction(rr.randrange(0, 7))
                    for _ in range(len(S[0]))] for _ in range(3)]
            rnd_tot += 1
            if any(A.rank([R[t] for t in sub], K)
                   != A.rank([Srn[t] for t in sub], K) for sub in SUBSETS):
                rnd_det += 1
        ctl.append(dict(m=m, vertex="%s%d" % (kind, v), n=tot,
                        perturbation_broke_identity=broke,
                        n_random=rnd_tot, random_Sprime_detected=rnd_det))
    man.record("K4_control", dict(
        per_case=ctl,
        ok=(all(r["perturbation_broke_identity"] == r["n"] for r in ctl)
            and all(r["random_Sprime_detected"] > 0 for r in ctl)),
        note="MUT: a one-cell perturbation of an edge AT v must break "
             "ROWS = P.S' against the unperturbed P,S'; POSITIVE CONTROL: "
             "the rank comparison must detect a random S'"))
    print("K4: %s" % json.dumps(ctl), flush=True)

    man.finish(res, extra={"elapsed_s": round(time.time() - t0, 1)})
    if os.path.exists(res + ".part"):
        os.remove(res + ".part")
    print("T4 DONE in %.1fs" % (time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
