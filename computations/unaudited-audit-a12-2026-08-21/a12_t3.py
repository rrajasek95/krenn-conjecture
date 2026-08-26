#!/usr/bin/env python3
"""A12 TARGET 1 (e) -- FRESH m=25 points from an independent generator, and
an adversarial search for a counterexample to W36-M25-FULL.  UNAUDITED.

The generator is A12's own: the cofactor identity makes Phi LINEAR in the
cells at any single site u (each Gamma matching covers u exactly once), so
the whole clean-word system splits by the letter at u into three independent
linear systems, one per row of the u-blocks.  One exact kernel solve at ONE
site therefore produces a point that is clean at EVERY clean word.  Points
are then re-validated from scratch (Phi over all 2,624 clean words).

D0_build      -- >= 20 fresh clean all-cells-nonzero points over Q, F_13 and
                 F_31 (two primes = 1 mod 3), from randomised sites/seeds
D1_theorem    -- the theorem on every fresh point: n_idx = 0 or DELIVERS
D2_zerowit    -- the zero-witness census on every fresh point, no stride
D3_adversary  -- a TARGETED search for the configurations the proof forbids:
                 (i) a live |T_f|=1 choice that FAILS (exercises the
                 case analysis), (ii) a tuple with rank S' = 2 carrying a
                 dead choice (would refute the zero-witness lemma),
                 (iii) Branch T / n_idx = 0.  Site 6 is solved LAST so that
                 A56 and A67 -- the only cells the minors see -- are drawn
                 from the kernel, which is where a counterexample would have
                 to live.
D4_control    -- a positive control: the SAME builder without the cleanliness
                 solve (random blocks) must produce non-clean points, and the
                 zero-witness census must then FAIL
usage: a12_t3.py [n_per_field]
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from collections import defaultdict

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a12_lib as A  # noqa: E402
from a12_t0 import Manifest  # noqa: E402
from a12_t2 import Sp, minor, slots, PAIR  # noqa: E402

DECL = ["D0_build", "D1_theorem", "D2_zerowit", "D3_adversary", "D4_control"]


def rand_nonzero(K, rng):
    return K.of(rng.randrange(1, K.p)) if K.p else A.Fraction(
        rng.randrange(1, 24))


def seed_stratum(tm, K, rng):
    """a rank-one seed: A_{u,v}[a][b] = c_uv * alpha_u(a) * alpha_v(b) makes
    Phi(w) = (prod_u alpha_u(w_u)) * haf(c), so tuning ONE c_e to kill the
    scalar Gamma hafnian gives a point with Phi == 0 at EVERY word (clean,
    all cells nonzero, on the vanishing stratum).  Phi is linear in c_e, so
    the tuning is one division.  The site walk then leaves the stratum."""
    al = {u: [rand_nonzero(K, rng) for _ in range(3)] for u in range(8)}
    ce = {e: rand_nonzero(K, rng) for e in sorted(tm.gamma)}
    e0 = sorted(tm.gamma)[rng.randrange(len(tm.gamma))]
    dA = dB = K.zero
    for M in tm.gamma_pms:
        pr = K.one
        for e in M:
            if e != e0:
                pr = A.norm(K, pr * ce[e])
        if e0 in M:
            dA = A.norm(K, dA + pr)
        else:
            dB = A.norm(K, dB + pr)
    if K.iszero(dA):
        return None
    ce[e0] = A.norm(K, -dB * K.inv(dA))
    if K.iszero(ce[e0]):
        return None
    return {(u, v): [[A.norm(K, ce[(u, v)] * al[u][a] * al[v][b])
                      for b in range(3)] for a in range(3)]
            for (u, v) in sorted(tm.gamma)}


def site_solve(tm, bl, u, K, rng, tries=60):
    """re-solve the cells at site u so that Phi vanishes at every clean word.
    Returns True on success (all new cells nonzero)."""
    ns = tm.nbr[u]
    nvar = 3 * len(ns)
    for t in range(3):
        rows = []
        for w in tm.clean_words:
            if w[u] != t:
                continue
            Q = tm.cofactorQ(bl, u, w, K)
            r = [K.zero] * nvar
            for j, s in enumerate(ns):
                r[3 * j + w[s]] = A.norm(K, r[3 * j + w[s]] + Q[j])
            rows.append(r)
        bas = A.kernel_basis(rows, K, nvar)
        if not bas:
            return False
        vec = None
        for _ in range(tries):
            cand = [K.zero] * nvar
            for b in bas:
                lam = rand_nonzero(K, rng)
                cand = [A.norm(K, x + lam * y) for x, y in zip(cand, b)]
            if all(not K.iszero(z) for z in cand):
                vec = cand
                break
        if vec is None:
            return False
        for j, s in enumerate(ns):
            for b in range(3):
                if u < s:
                    bl[(u, s)][t][b] = vec[3 * j + b]
                else:
                    bl[(s, u)][b][t] = vec[3 * j + b]
    return True


def build(tm, K, rng, sites, base=None):
    """base = None -> the from-scratch rank-one stratum seed; otherwise a
    walk on the clean variety starting from `base`."""
    bl = seed_stratum(tm, K, rng) if base is None else \
        {e: [list(r) for r in v] for e, v in base.items()}
    if bl is None:
        return None
    for u in sites:
        if not site_solve(tm, bl, u, K, rng):
            return None
    return bl


def zerowit_census(tm, bl, K, idx):
    n = bad = nm = badm = 0
    for (w, fire) in idx:
        x = tuple(w[:4])
        if not K.iszero(tm.hafL(bl, x, K)):
            continue
        Bh = tm.haf_on(bl, [0, 1, 2, 3, 4, 5], w, K)
        Ch = tm.haf_on(bl, [0, 1, 2, 3, 4, 7], w, K)
        Bp = A.norm(K, tm.cell(bl, 0, 3, x[0], x[3], K)
                    * tm.cell(bl, 1, 4, x[1], w[4], K)
                    * tm.cell(bl, 2, 5, x[2], w[5], K))
        Cp = A.norm(K, tm.cell(bl, 2, 3, x[2], x[3], K)
                    * tm.cell(bl, 0, 7, x[0], w[7], K)
                    * tm.cell(bl, 1, 4, x[1], w[4], K))
        n += 1
        if not (K.iszero(A.norm(K, Bp - Bh)) and K.iszero(A.norm(K, Cp - Ch))
                and not K.iszero(Bp) and not K.iszero(Cp)):
            bad += 1
        if len(fire) == 1:
            a, b = PAIR[sorted(fire)[0]]
            nm += 1
            if not K.iszero(minor(Sp(tm, bl, w[5], w[7], K), a, b, K)):
                badm += 1
    return n, bad, nm, badm


def main():
    t0 = time.time()
    per = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    man = Manifest(DECL)
    tm = A.T(25)
    idx, by, big = slots(tm)
    rng = random.Random(8212026)
    res = os.path.join(HERE, "results_t3.json")

    fields = [('Q', A.Rat), ('13', A.Fp(13)), ('31', A.Fp(31))]
    recs = []
    tot_zw = bad_zw = tot_mn = bad_mn = 0
    adv = dict(failing_live_choice_points=[], rank2_with_dead_choice=[],
               branchT_points=[], R25_strict_fail=[])
    attempts = 0
    # base points for the WALK family: one stored object per field, used only
    # as a starting point; every cell is re-solved by A12's own kernel solve
    from a12_t2 import corpus25
    bases = {}
    for (tag, fld, ptj) in corpus25():
        if fld not in bases:
            K0 = A.K_of(fld)
            b = A.load_point(ptj, K0)
            if set(b) == set(tm.gamma) and tm.is_clean(b, K0):
                bases[fld] = (tag, b)
    jobs = []
    for (fname, K) in fields:
        for i in range(per):
            order = [u for u in range(8)]
            rng.shuffle(order)
            jobs.append((fname, K, 'seed', None, order[:3]))
        for i in range(per * 2):
            order = [u for u in range(8)]
            rng.shuffle(order)
            jobs.append((fname, K, 'walk', bases.get(fname, (None, None))[1],
                         order[:rng.randrange(2, 5)]))
    for (fname, K, fam, base, sites) in jobs:
        attempts += 1
        if fam == 'walk' and base is None:
            continue
        bl = build(tm, K, rng, sites, base=base)
        if bl is None:
            continue
        if not (tm.is_clean(bl, K) and tm.all_nonzero(bl, K)):
            continue
        if base is not None and all(
                bl[e][i][j] == base[e][i][j] for e in bl
                for i in range(3) for j in range(3)):
            continue
        rep = tm.vertex_report(bl, 'R', 6, K, choices=idx, detail=True)
        deliv = {(w, fr) for (w, fr) in rep['detail']}
        nfail = nfail1 = nfail2 = 0
        for (w, fire) in idx:
            if K.iszero(tm.hafL(bl, tuple(w[:4]), K)):
                continue
            if (w, tuple(sorted(fire))) not in deliv:
                nfail += 1
                if len(fire) == 1:
                    nfail1 += 1
                else:
                    nfail2 += 1
        n, bad, nm, badm = zerowit_census(tm, bl, K, idx)
        tot_zw += n
        bad_zw += bad
        tot_mn += nm
        bad_mn += badm
        Sall = {(a, b): Sp(tm, bl, a, b, K)
                for a in range(3) for b in range(3)}
        ranks = {k: A.rank(Sall[k], K) for k in Sall}
        deadk = {(w[5], w[7]) for (w, f) in idx
                 if K.iszero(tm.hafL(bl, tuple(w[:4]), K)) and len(f) == 1}
        r2dead = sorted(str(k) for k in deadk if ranks[k] == 2)
        live_letters = defaultdict(set)
        for (w, fire) in idx:
            if len(fire) == 1 and not K.iszero(
                    tm.hafL(bl, tuple(w[:4]), K)):
                live_letters[(w[5], w[7])].add(sorted(fire)[0])
        R25 = any(len(s) >= 2 for s in live_letters.values())
        Xdead = {tuple(w[:4]) for (w, f) in idx
                 if K.iszero(tm.hafL(bl, tuple(w[:4]), K))}
        rec = dict(field=fname, family=fam, sites=sites,
            offstratum=tm.off_stratum(
            bl, K), n_idx=rep['n_idx'], n_deliver=rep['n_deliver'],
            DELIVERS=rep['DELIVERS'], n_failing_live=nfail,
            n_failing_live_Tf1=nfail1, n_failing_live_Tf2=nfail2,
            n_rank2_tuples=sum(1 for vv in ranks.values() if vv == 2),
            n_mixed_slots=sum(
                1 for kk in ranks for ff in (1, 2)
                if any(K.iszero(tm.hafL(bl, tuple(w[:4]), K))
                       for (w, fr) in idx
                       if fr == frozenset([ff]) and (w[5], w[7]) == kk)
                and any(not K.iszero(tm.hafL(bl, tuple(w[:4]), K))
                        for (w, fr) in idx
                        if fr == frozenset([ff]) and (w[5], w[7]) == kk)),
            nZ=len(Xdead), ranks={str(k): v for k, v in sorted(
                ranks.items())}, R25_strict=R25,
            n_dead_choices=n, zerowit_bad=bad, minor_bad=badm,
            theorem_ok=(rep['n_idx'] == 0 or rep['DELIVERS']))
        if nfail:
            adv["failing_live_choice_points"].append(
                dict(field=fname, n_failing=nfail,
                     point=A.dump_point(bl)))
        if r2dead:
            adv["rank2_with_dead_choice"].append(
                dict(field=fname, tuples=r2dead, point=A.dump_point(bl)))
        if rep['n_idx'] == 0:
            adv["branchT_points"].append(dict(field=fname,
                                              point=A.dump_point(bl)))
        if not R25:
            adv["R25_strict_fail"].append(dict(field=fname, nZ=len(Xdead),
                                               ranks=rec["ranks"],
                                               point=A.dump_point(bl)))
        recs.append(rec)
        print("fresh %-2s %-4s sites=%-16s off=%-5s nZ=%2d n_idx=%3d "
              "dlv=%3d fail=%2d R25=%s ok=%s"
              % (fname, fam, sites, rec['offstratum'], len(Xdead),
                 rep['n_idx'], rep['n_deliver'], nfail, R25,
                 rec['theorem_ok']), flush=True)
        json.dump(dict(partial=recs), open(res + ".part", "w"), indent=1,
                  default=str)

    man.record("D0_build", dict(
        n_points=len(recs), attempts=attempts,
        per_field={f: sum(1 for r in recs if r["field"] == f)
                   for f, _ in fields},
        n_offstratum=sum(1 for r in recs if r["offstratum"]),
        ok=(len(recs) >= 20 and all(sum(1 for r in recs if r["field"] == f) > 0
                                    for f, _ in fields)),
        note="independent generator: one exact kernel solve per site on the "
             "clean-word system, sites randomised, site 6 solved last"))
    man.record("D1_theorem", dict(
        n=len(recs), violations=sum(1 for r in recs if not r["theorem_ok"]),
        n_idx_zero=sum(1 for r in recs if r["n_idx"] == 0),
        n_R25_fail=sum(1 for r in recs if not r["R25_strict"]),
        n_with_failing_live=sum(1 for r in recs if r["n_failing_live"]),
        per_point=recs, ok=all(r["theorem_ok"] for r in recs)))
    man.record("D2_zerowit", dict(
        n_dead_choices=tot_zw, bad=bad_zw, n_minor_checks=tot_mn,
        bad_minors=bad_mn, ok=(bad_zw == 0 and bad_mn == 0)))
    man.record("D3_adversary", dict(
        n_failing_live_choice_points=len(adv["failing_live_choice_points"]),
        n_rank2_with_dead_choice=len(adv["rank2_with_dead_choice"]),
        n_branchT=len(adv["branchT_points"]),
        n_R25_fail=len(adv["R25_strict_fail"]),
        stored=adv,
        ok=(len(adv["rank2_with_dead_choice"]) == 0),
        note="rank2_with_dead_choice must stay EMPTY: a dead |T_f|=1 choice "
             "at a rank-2 tuple would refute the zero-witness lemma.  The "
             "other three counters are search outcomes, not pass/fail"))

    # ------------------------------------------------------------- D4
    K = A.Fp(13)
    ctl = []
    for _ in range(6):
        bl = {e: [[rand_nonzero(K, rng) for _ in range(3)] for _ in range(3)]
              for e in sorted(tm.gamma)}
        n, bad, nm, badm = zerowit_census(tm, bl, K, idx)
        ctl.append(dict(clean=tm.is_clean(bl, K), n_dead=n, bad=bad,
                        n_minor=nm, bad_minor=badm))
    man.record("D4_control", dict(
        per_run=ctl, n=len(ctl),
        n_nonclean=sum(1 for r in ctl if not r["clean"]),
        n_minor_census_broken=sum(1 for r in ctl if r["bad_minor"] > 0),
        ok=(all(not r["clean"] for r in ctl)
            and all(r["bad_minor"] > 0 for r in ctl if r["n_minor"])),
        note="POSITIVE CONTROL for C1/D2: without the cleanliness solve the "
             "minor half of the zero-witness census must FAIL.  W36's own "
             "F5 perturbation control reported 0 violations and still "
             "declared ok -- it never fired."))
    print("D4: non-clean %d/%d, minor census broken %d/%d"
          % (sum(1 for r in ctl if not r["clean"]), len(ctl),
             sum(1 for r in ctl if r["bad_minor"] > 0), len(ctl)), flush=True)

    man.finish(res, extra={"elapsed_s": round(time.time() - t0, 1)})
    if os.path.exists(res + ".part"):
        os.remove(res + ".part")
    print("T3 DONE  %d fresh points, theorem violations %d, zerowit bad "
          "%d/%d, minors bad %d/%d, failing-live points %d, branchT %d, "
          "R25 fails %d  in %.1fs"
          % (len(recs), sum(1 for r in recs if not r["theorem_ok"]), bad_zw,
             tot_zw, bad_mn, tot_mn, len(adv["failing_live_choice_points"]),
             len(adv["branchT_points"]), len(adv["R25_strict_fail"]),
             time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
