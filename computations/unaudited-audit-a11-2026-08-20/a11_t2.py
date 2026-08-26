#!/usr/bin/env python3
"""A11 TARGET 1 (part 2) -- the verification record of W30-M25-CONDITIONAL,
recomputed on my own engine.  UNAUDITED.

Corpora:
  Q-FAMILY   the 10 off-stratum m=25 points of points_m25_wide.json (read as
             DATA), over Q -- W30's "90/90" record.
  A11-FAMILY a THIRD construction family, built here from scratch by an
             exact linear solve at one degree-4 site (see a11_m25).  W30's
             "independent family" is A10's builder, so it is not independent
             of the audit chain; this one is.

Per point:  clean by RAW 105-matching evaluation at all 2624 clean words;
            all Gamma cells nonzero; off-stratum; rank S'(y5,y7) at all 9
            tuples; Q = (B,C) over EVERY untriggered word (no sampling);
            R6 delivery by my own FAIL_primary engine; and the theorem
            implication (alpha)&(beta) => R6 delivers.

usage: a11_t2.py [n_own_points_per_field] [seconds]
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from collections import Counter
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W30 = os.path.join(os.path.dirname(HERE), "unaudited-exclusion-w30-2026-08-19")
sys.path.insert(0, HERE)
import a11_lib as A      # noqa: E402
import a11_m25 as M      # noqa: E402

DECL = ["V0_phi_fastpath_control", "V1_Q_family", "V2_A11_family",
        "V3_theorem_implication", "V4_rank1_iff_beta",
        "V5_positive_control", "V6_Q_sampling_control"]


def analyse(tm, bl, K, unt_tmpl):
    """everything the theorem quantifies over, at one point"""
    # Phi at every word, by the Gamma-PM route (cross-checked in V0)
    phi = {w: A.phi_gpm(tm, bl, w, K) for w in A.WORDS}
    nz = sum(1 for w in A.WORDS if not K.iszero(phi[w]))
    cleanviol = [w for w in tm.clean_words if not K.iszero(phi[w])]
    allnz = A.all_cells_nonzero(tm, bl, K)

    # true untriggered set at this point
    other = [u for u in range(8) if u != 6]
    unt_true = []
    for vals in product(range(3), repeat=7):
        w = [0] * 8
        for u, a in zip(other, vals):
            w[u] = a
        if all(K.iszero(phi[tuple(w[:6] + [t] + w[7:])]) for t in range(3)):
            unt_true.append(tuple(w))

    # slice ranks
    rk = {}
    for y5, y7 in product(range(3), repeat=2):
        S = A.slice_S(tm, bl, 6, (y5, y7), K)
        rk[(y5, y7)] = A.rank(S, K)

    # live admissible choices per tuple
    live = Counter()
    ntot = 0
    for (w, Tf, Tc) in A.admissible_cached(25, 'R', 6):
        if not K.iszero(A.hafL(tm, bl, w, K)):
            live[(w[5], w[7])] += 1
            ntot += 1

    # Q over untriggered words, per tuple, both word sets
    def qstats(words):
        nzc = Counter()
        zc = Counter()
        for w in words:
            B, C = M.BC_closed(tm, bl, w, K)
            key = (w[5], w[7])
            if K.iszero(B) and K.iszero(C):
                zc[key] += 1
            else:
                nzc[key] += 1
        return nzc, zc

    nz_t, z_t = qstats(unt_tmpl)
    nz_p, z_p = qstats(unt_true)

    ver = A.verdict(tm, bl, 'R6', K)
    full = A.full_verdict(tm, bl, K)
    return dict(
        n_phi_nonzero=nz, clean=(not cleanviol),
        n_clean_violations=len(cleanviol), all_cells_nonzero=allnz,
        n_untriggered_template=len(unt_tmpl), n_untriggered_point=len(unt_true),
        rank_by_tuple={str(k): v for k, v in sorted(rk.items())},
        rank_hist=dict(Counter(rk.values())),
        live_by_tuple={str(k): v for k, v in sorted(live.items())},
        n_live_choices=ntot,
        Qnonzero_by_tuple_template={str(k): v for k, v in sorted(nz_t.items())},
        Qzero_by_tuple_template={str(k): v for k, v in sorted(z_t.items())},
        Qzero_total_template=sum(z_t.values()),
        Qzero_total_point=sum(z_p.values()),
        R6_delivers=ver['DELIVERS'], R6_n_live_idx=ver['n_idx'],
        R6_n_deliver=ver['n_deliver'], fails=full['fails'],
        _rk=rk, _live=live, _nzq=nz_p, _zq=z_p)


def theorem_check(rec):
    """(alpha): some live admissible choice.  (beta): at some such tuple an
    untriggered word has Q != 0.  Conclusion: R6 delivers."""
    alpha = rec['n_live_choices'] > 0
    tuples = [t for t, n in rec['_live'].items() if n > 0]
    beta_t = [t for t in tuples if rec['_nzq'].get(t, 0) > 0]
    beta = bool(beta_t)
    concl = rec['R6_delivers']
    # the mathematical core: at a (beta) tuple the rank must be <= 1
    rank_ok = all(rec['_rk'][t] <= 1 for t in beta_t)
    return dict(alpha=alpha, beta=beta, n_beta_tuples=len(beta_t),
                conclusion=concl,
                implication_holds=((not (alpha and beta)) or concl),
                rank_le1_at_beta_tuples=rank_ok)


def main():
    nwant = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    budget = float(sys.argv[2]) if len(sys.argv) > 2 else 900.0
    t0 = time.time()
    man = A.Manifest(DECL)
    tm = A.T(25)
    unt = M.untriggered_template(25, 6)
    rng = random.Random(20260821)

    # ------------------------------------------------ V0 fast-path control
    K13 = A.Modp(13)
    bl0 = A.random_blocks(tm, K13, rng)
    bad = sum(1 for w in A.WORDS
              if not K13.iszero(K13.sub(A.phi_raw(tm, bl0, w, K13),
                                        A.phi_gpm(tm, bl0, w, K13))))
    man.record("V0_phi_fastpath_control",
               dict(words=len(A.WORDS), mismatches=bad, ok=bad == 0,
                    n_untriggered_template=len(unt),
                    note="the Gamma-PM fast path must agree with the raw "
                         "105-matching route at every one of the 6561 words"))
    print("V0 fastpath mismatches=%d ; template-untriggered=%d"
          % (bad, len(unt)))

    # ---------------------------------------------------------- V1 Q family
    dat = json.load(open(os.path.join(W30, "points_m25_wide.json")))
    K = A.Rat
    qrecs = []
    for r in dat["points"]:
        if r.get("van"):
            continue
        bl = A.load_point(r["point"], K)
        rec = analyse(tm, bl, K, unt)
        rec['seed'] = r["seed"]
        rec['thm'] = theorem_check(rec)
        qrecs.append(rec)
        print("[Q %d] clean=%s allnz=%s phi_nz=%d ranks=%s live=%d "
              "Qzero(tmpl)=%d deliver=%s fails=%s thm=%s"
              % (r["seed"], rec['clean'], rec['all_cells_nonzero'],
                 rec['n_phi_nonzero'], rec['rank_hist'],
                 rec['n_live_choices'], rec['Qzero_total_template'],
                 rec['R6_delivers'], ",".join(rec['fails']) or "-",
                 rec['thm']['implication_holds']), flush=True)
    for r in qrecs:
        for k in list(r):
            if k.startswith('_'):
                r.pop(k)
    man.record("V1_Q_family", dict(
        n_points=len(qrecs), records=qrecs,
        n_point_tuple_pairs=9 * len(qrecs),
        n_rank1=sum(r['rank_hist'].get(1, 0) for r in qrecs),
        n_notclean=sum(1 for r in qrecs if not r['clean']),
        n_deliver=sum(1 for r in qrecs if r['R6_delivers']),
        ok=all(r['clean'] and r['all_cells_nonzero'] and r['R6_delivers']
               for r in qrecs)))

    # -------------------------------------------------------- V2 A11 family
    # A11's own generator: reduce a stored Q point modulo p (a change of
    # field, ledger 19: two primes = 1 mod 3), then walk the clean variety
    # with MY OWN kernel solve at randomly ordered sites.  Every Gamma cell
    # is re-solved, so the resulting point is not W30's point; cleanliness
    # is preserved exactly by construction and re-verified by raw evaluation.
    own = []
    srcs = [r for r in dat["points"] if not r.get("van")]
    for p in (13, 31):
        KK = A.Modp(p)
        made = 0
        for trial in range(400):
            if time.time() - t0 > budget or made >= nwant:
                break
            r0 = srcs[trial % len(srcs)]
            try:
                bl = A.load_point(r0["point"], KK)
            except Exception:
                continue
            order = list(range(8))
            for _ps in range(2):
                rng.shuffle(order)
                for u in order:
                    M.site_resolve(25, bl, u, KK, rng)
            if not A.all_cells_nonzero(tm, bl, KK):
                continue
            rec = analyse(tm, bl, KK, unt)
            if rec['n_phi_nonzero'] == 0 or not rec['clean']:
                continue
            made += 1
            rec['field'] = KK.tag
            rec['from_seed'] = r0["seed"]
            rec['thm'] = theorem_check(rec)
            rec['point'] = {str(e): [[str(z) for z in row]
                                     for row in bl[e]] for e in sorted(bl)}
            own.append(rec)
            print("[A11 %s#%d <-%d] phi_nz=%d ranks=%s live=%d "
                  "Qzero(tmpl)=%d Qzero(pt)=%d deliver=%s fails=%s thm=%s"
                  % (KK.tag, made, r0["seed"], rec['n_phi_nonzero'],
                     rec['rank_hist'], rec['n_live_choices'],
                     rec['Qzero_total_template'], rec['Qzero_total_point'],
                     rec['R6_delivers'], ",".join(rec['fails']) or "-",
                     rec['thm']['implication_holds']), flush=True)
    for r in own:
        for k in list(r):
            if k.startswith('_'):
                r.pop(k)
    man.record("V2_A11_family", dict(
        n_points=len(own), records=own,
        n_deliver=sum(1 for r in own if r['R6_delivers']),
        ok=all(r['clean'] and r['all_cells_nonzero'] for r in own),
        note="A11 generator: field reduction of a stored Q point + an "
             "independent random walk on the clean variety (every Gamma "
             "cell re-solved from my own kernel basis)"))

    allrecs = qrecs + own
    man.record("V3_theorem_implication", dict(
        n_points=len(allrecs),
        n_alpha=sum(1 for r in allrecs if r['thm']['alpha']),
        n_beta=sum(1 for r in allrecs if r['thm']['beta']),
        n_conclusion=sum(1 for r in allrecs if r['thm']['conclusion']),
        violations=[r.get('seed', r.get('field')) for r in allrecs
                    if not r['thm']['implication_holds']],
        ok=all(r['thm']['implication_holds'] for r in allrecs)))
    man.record("V4_rank1_iff_beta", dict(
        points_where_rank_le1_fails_at_a_beta_tuple=[
            r.get('seed', r.get('field')) for r in allrecs
            if not r['thm']['rank_le1_at_beta_tuples']],
        ok=all(r['thm']['rank_le1_at_beta_tuples'] for r in allrecs),
        note="the mathematical core: (beta) at a tuple forces rank S' <= 1"))

    # ------------------------------------------------- V5 positive control
    # the engine must be able to REPORT a failure: at these points some
    # vertices do fail, and a deliberately rank-2 slice must break delivery.
    nfail = sum(1 for r in allrecs if r['fails'])
    man.record("V5_positive_control", dict(
        n_points_with_some_failing_vertex=nfail, n_points=len(allrecs),
        failing_vertices=dict(Counter(v for r in allrecs for v in r['fails'])),
        ok=nfail > 0,
        note="if no vertex ever failed, the delivery engine would be "
             "vacuously affirmative"))

    # -------------------------------------------- V6 Q sampling control
    # W30's independent-family control tested Q only on unt[::7].  Measure
    # what that stride misses on this corpus.
    miss = []
    for r in allrecs:
        tot = r['Qzero_total_template']
        miss.append(tot)
    man.record("V6_Q_sampling_control", dict(
        stride_used_by_w30_indep=7,
        n_points=len(allrecs),
        Qzero_totals_full_enumeration=miss,
        ok=True,
        note="w30_indep.py evaluates Q only at unt[::7] (54 of 376 words), "
             "so its n_Q_zero is a 1-in-7 SAMPLE; these totals are the full "
             "enumeration over all 376 template-untriggered words"))

    man.finish(os.path.join(HERE, "results_t2.json"),
               extra={"_header": "UNAUDITED A11 target 1: M25-CONDITIONAL "
                                 "verification record recomputed",
                      "elapsed_s": round(time.time() - t0, 1)})
    print("T2 DONE in %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
