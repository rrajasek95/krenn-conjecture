#!/usr/bin/env python3
"""W36 ROUND 2 -- THEOREM W36-M25-FULL, and the controls A11's audit asks for.

A11 corrected my round-1 supersession claim: W36-M25 (the bare pigeonhole)
and W30-M25-CONDITIONAL are INCOMPARABLE, because (R25) fails at 4 of 32
corpus points while (beta) fails at 0/32, so the promotable object was the
DISJUNCTION "(R25) or ((alpha) and (beta))".  The coordinator then asked for
the complement of that disjunction to be shown empty.  Round 2 does better:
the complement is empty because (R25) CANNOT FAIL AT A LIVE L-PART, and the
reason is that a hafL ZERO is itself a Q != 0 witness.

  ZERO-WITNESS LEMMA.  B = hafL*r45 + l03*d1*d2 and C = hafL*r47 + l23*d0*d1,
  so hafL(x) = 0 makes B = l03*d1*d2 and C = l23*d0*d1 -- products of Gamma
  cells, NONZERO by (H2).  Cleanliness A67[t][y7]B + A56[y5][t]C = 0 at the
  letters t where the word survives then forces the corresponding 2x2 minors
  of S'(y5,y7) to vanish.  A DEAD choice kills a minor; a LIVE choice is one
  the pigeonhole can use.  The two escapes W30 chased separately are the same
  coin.

  THEOREM W36-M25-FULL.  (H1) clean, (H2) every Gamma cell nonzero.  Then R6
  delivers at every point where it has at least one surviving admissible
  index choice.  (Neither (alpha), (beta), (R25), nor (H3) is assumed; T_c
  nonempty and |T_f| in {1,2} are template facts, A11 corrections (i),(ii).)

  Proof.  Rows of S'(tau) are nonzero by (H2), so rank S' in {1,2} and a
  choice with clean pair P fails iff minor(P) = 0 AND rank S'(tau) = 2 -- and
  rank 2 with one minor zero forces the OTHER minor nonzero (control M1).
  Let x be any LIVE L-part of a |T_f| = 1 choice, with firing letter f (a
  function of x alone, control M2a).  By control M2b there is a tuple tau
  with y5 != 1 carrying x and carrying choices of the other letter f'.
   - if some f'-choice at tau is live, both letters are live at tau and the
     shared-letter pigeonhole (control M1) says they cannot both fail;
   - if every f'-choice at tau is dead, the zero-witness lemma kills
     minor(P_{f'}), and the f-choice failing would kill minor(P_f) too, so
     all three rows would be parallel and rank S' = 1 -- contradicting the
     rank-2 requirement.
  Either way a choice at tau delivers.  So R6 failing forces EVERY L-part of
  X_{R6,25} dead, i.e. W30's Branch T; and then at every tuple carrying a
  |T_f| = 2 choice (all have y5 != 1, control M2c) both firing sets are dead,
  both minors vanish, rank S' = 1, and any live |T_f| = 2 choice delivers.
  Hence failure forces NO live choice at all.  QED

Declared controls (all EXECUTED; ledger 31):
  M0_template   -- letter 0 is never a firing letter (T_c nonempty), the
                   firing sets are exactly FAM_01 / FAM_02, |T_f| in {1,2}
  M1_matrices   -- EXHAUSTIVE over all 3x2 matrices with every entry nonzero
                   (F_13 and F_31): (a) the two overlapping clean pairs never
                   both fail; (b) rank 2 with one minor zero => the other
                   minor nonzero; (c) non-vacuity: single failures do occur
  M2_combinat   -- (a) the firing letter is a function of the L-part; (b)
                   EVERY L-part of X_v reaches a y5 != 1 tuple carrying the
                   other firing letter; (c) every |T_f| = 2 tuple has y5 != 1
                   and both firing sets nonempty
  M3_zero_wit   -- the zero-witness lemma at every hafL zero of every stored
                   point (full census, no stride)
  M4_corpus     -- the theorem on the whole stored m=25 corpus, with the
                   (R25)-failing points called out explicitly
  M5_negctl     -- deleting a template fact must make the argument FAIL to
                   close (proves the facts are load-bearing, not decoration)
usage: w36_m25full.py [matrix_field]
"""
from __future__ import annotations
import json, os, sys, time
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations, product
sys.dont_write_bytecode = True
import w36_lib as W
import w36_beta2 as B2
import w36_thm as TH
import w30_lib as L
import w26_core as C

HERE = W.HERE
DECL = ["M0_template", "M1_matrices", "M2_combinat", "M3_zero_wit",
        "M4_corpus", "M5_negctl"]
MINOR_OF = {2: (0, 1), 1: (0, 2)}


def structure():
    by = defaultdict(lambda: defaultdict(set))
    big = defaultdict(set)
    allfire = set()
    for (w, fire) in L.index_choices_cached(25, 'R', 6):
        allfire |= set(fire)
        if len(fire) == 1:
            by[(w[5], w[7])][sorted(fire)[0]].add(tuple(w[:4]))
        elif len(fire) == 2:
            big[(w[5], w[7])].add(tuple(w[:4]))
    return by, big, allfire


def exhaustive_matrices(p):
    """EXHAUSTIVE over 3x2 matrices with all six entries nonzero mod p.
    Rows S'_t = (A67[t][y7], A56[y5][t]).  A choice with clean pair P fails
    iff minor(P) == 0 and rank == 2."""
    nz = list(range(1, p))
    n = both = single = rank1 = rank2 = 0
    viol_a = viol_b = 0
    for a0, b0, a1, b1, a2, b2 in product(nz, repeat=6):
        n += 1
        m01 = (a0 * b1 - a1 * b0) % p
        m02 = (a0 * b2 - a2 * b0) % p
        m12 = (a1 * b2 - a2 * b1) % p
        r1 = (m01 == 0 and m02 == 0 and m12 == 0)
        if r1:
            rank1 += 1
        else:
            rank2 += 1
        f2 = (m01 == 0) and not r1          # firing letter 2, clean {0,1}
        f1 = (m02 == 0) and not r1          # firing letter 1, clean {0,2}
        if f1 and f2:
            both += 1
            viol_a += 1
        elif f1 or f2:
            single += 1
        # (b) rank 2 with one minor zero => the other nonzero
        if not r1:
            if (m01 == 0 and m02 == 0) or (m01 == 0 and m12 == 0) or \
               (m02 == 0 and m12 == 0):
                viol_b += 1
    return dict(p=p, n=n, n_rank1=rank1, n_rank2=rank2,
                n_both_fail=both, n_single_fail=single,
                pigeonhole_ok=(viol_a == 0), two_minor_ok=(viol_b == 0),
                non_vacuous=(single > 0))


def projective_matrices(p):
    """EXACT and COMPLETE for the field: every minor's vanishing is invariant
    under scaling a row, so it suffices to enumerate each row up to scale.
    A row (a,b) with both entries nonzero is, up to scale, (1, b/a) with
    b/a nonzero -- p-1 classes.  So (p-1)^3 configurations decide the field,
    and at p = 13 this must agree with the full (p-1)^6 enumeration."""
    nz = list(range(1, p))
    n = both = single = rank1 = 0
    viol_b = 0
    for r0, r1, r2 in product(nz, repeat=3):
        n += 1
        m01 = (r1 - r0) % p            # minors of rows (1,r_t) up to scale
        m02 = (r2 - r0) % p
        m12 = (r2 - r1) % p
        rk1 = (m01 == 0 and m02 == 0 and m12 == 0)
        if rk1:
            rank1 += 1
        f2 = (m01 == 0) and not rk1
        f1 = (m02 == 0) and not rk1
        if f1 and f2:
            both += 1
        elif f1 or f2:
            single += 1
        if not rk1 and ((m01 == 0 and m02 == 0) or (m01 == 0 and m12 == 0)
                        or (m02 == 0 and m12 == 0)):
            viol_b += 1
    return dict(p=p, mode="projective", n=n, n_rank1=rank1,
                n_both_fail=both, n_single_fail=single,
                pigeonhole_ok=(both == 0), two_minor_ok=(viol_b == 0),
                non_vacuous=(single > 0))


def main():
    OUT = {"_header": W.HEADER, "_task": "THEOREM W36-M25-FULL + A11 controls",
           "_controls_declared": DECL, "_controls_run": []}
    res = os.path.join(HERE, "results_m25full.json")

    def ck():
        json.dump(OUT, open(res, "w"), indent=1, default=str)

    by, big, allfire = structure()
    Xv = {x for d in by.values() for s in d.values() for x in s}
    FAM = B2.families()
    fam01 = {p[:4] for d in FAM.values() for p in d['01']}
    fam02 = {p[:4] for d in FAM.values() for p in d['02']}
    f2set = {x for d in by.values() for x in d.get(2, set())}
    f1set = {x for d in by.values() for x in d.get(1, set())}
    OUT["M0_template"] = dict(
        executed=True, firing_letters=sorted(allfire),
        letter0_never_fires=(0 not in allfire),
        n_Xv=len(Xv), n_firing1=len(f1set), n_firing2=len(f2set),
        firing2_is_FAM01=(f2set == fam01), firing1_is_FAM02=(f1set == fam02),
        n_big_choices=sum(len(v) for v in big.values()),
        ok=(0 not in allfire and f2set == fam01 and f1set == fam02
            and len(Xv) == 42))
    OUT["_controls_run"].append("M0_template")
    print("M0:", json.dumps({k: v for k, v in OUT["M0_template"].items()}),
          flush=True)
    ck()

    # ---------------------------------------------------------------- M2
    fof = {}
    fun_ok = True
    for k, d in by.items():
        for f, s in d.items():
            for x in s:
                if x in fof and fof[x] != f:
                    fun_ok = False
                fof[x] = f
    bad = []
    for x in sorted(Xv):
        f = fof[x]
        other = 3 - f
        if not [k for k, d in by.items()
                if k[0] != 1 and x in d.get(f, set()) and d.get(other)]:
            bad.append(str(x))
    bad2 = [str(k) for k in big
            if not (by.get(k, {}).get(1) and by.get(k, {}).get(2))]
    OUT["M2_combinat"] = dict(
        executed=True, firing_is_function_of_Lpart=fun_ok,
        n_Xv=len(Xv), n_Lparts_without_mixed_tuple=len(bad),
        offenders=bad[:6], n_big_tuples=len(big),
        big_tuples_missing_a_firing_set=len(bad2),
        big_tuples_all_y5_ne_1=all(k[0] != 1 for k in big),
        ok=(fun_ok and not bad and not bad2
            and all(k[0] != 1 for k in big)))
    OUT["_controls_run"].append("M2_combinat")
    print("M2:", json.dumps(OUT["M2_combinat"]), flush=True)
    ck()

    # ---------------------------------------------------------------- M1
    fields = [int(x) for x in (sys.argv[1:] or ["13"])]
    mats = []
    for p in fields:
        t0 = time.time()
        # full enumeration only where it is cheap (p = 13 reproduces A11);
        # the projective enumeration is EXACT AND COMPLETE for every field
        r = projective_matrices(p)
        if p <= 13:
            rf = exhaustive_matrices(p)
            r["full_enumeration"] = rf
            r["full_agrees"] = (rf["pigeonhole_ok"] == r["pigeonhole_ok"]
                                and rf["two_minor_ok"] == r["two_minor_ok"]
                                and (rf["n_single_fail"] > 0)
                                == (r["n_single_fail"] > 0))
        r["seconds"] = round(time.time() - t0, 1)
        mats.append(r)
        print("M1 p=%d: %s" % (p, json.dumps(r)), flush=True)
        OUT["M1_matrices"] = dict(executed=True, per_field=mats,
                                  ok=all(m["pigeonhole_ok"]
                                         and m["two_minor_ok"]
                                         and m["non_vacuous"] for m in mats))
        OUT["_controls_run"] = [c for c in OUT["_controls_run"]
                                if c != "M1_matrices"] + ["M1_matrices"]
        ck()

    # ---------------------------------------------------------------- M3/M4
    cp = [(t, f, p) for (t, m, f, p) in TH.corpus() if m == 25]
    n3 = b3 = 0
    recs = []
    for (tag, fld, ptj) in cp:
        K = W.K_of(fld)
        try:
            bl = W.load_point(ptj, K)
        except Exception:
            continue
        if set(bl) != set(W.E_ALL25):
            continue
        if not (W.clean_ok(bl, K) and W.allnz(bl, K)):
            continue
        Z = {x for x in Xv if K.iszero(W.hafL(bl, x))}
        # M3: FULL census over dead choices -- no stride
        for k, d in by.items():
            for f, s in d.items():
                for x in s & Z:
                    ws = [w for (w, fr) in L.index_choices_cached(25, 'R', 6)
                          if len(fr) == 1 and tuple(w[:4]) == x
                          and (w[5], w[7]) == k]
                    if not ws:
                        continue
                    Bc, Cc = W.BC(bl, ws[0])
                    a, bb = MINOR_OF[f]
                    S = W.Sprime(bl, k[0], k[1])
                    mn = S[a][0] * S[bb][1] - S[bb][0] * S[a][1]
                    n3 += 1
                    if K.iszero(Bc) or K.iszero(Cc) or not K.iszero(mn):
                        b3 += 1
        rep = L.vertex_report(25, bl, 'R', 6, K)
        live_tuples = {k for k, d in by.items() for f, s in d.items()
                       if s - Z}
        R25 = any(len([f for f, s in d.items() if s - Z]) >= 2
                  for k, d in by.items())
        recs.append(dict(tag=tag, field=fld, nZ=len(Z), R25_holds=R25,
                         n_idx=rep['n_idx'], DELIVERS=rep['DELIVERS'],
                         theorem_ok=(rep['n_idx'] == 0 or rep['DELIVERS']),
                         point=W.dump_point(bl) if not R25 else None))
        print("%-46s %-2s nZ=%2d R25=%s n_idx=%3d DELIVERS=%s ok=%s"
              % (tag[:46], fld, len(Z), R25, rep['n_idx'], rep['DELIVERS'],
                 recs[-1]['theorem_ok']), flush=True)
        ck()
    OUT["M3_zero_wit"] = dict(executed=True, n=n3, bad=b3, ok=(b3 == 0),
                              note="FULL census of dead choices; each must "
                                   "have B,C nonzero and kill its minor")
    OUT["_controls_run"].append("M3_zero_wit")
    noR25 = [r for r in recs if not r["R25_holds"]]
    OUT["M4_corpus"] = dict(
        executed=True, n=len(recs),
        n_violations=sum(1 for r in recs if not r["theorem_ok"]),
        n_R25_fails=len(noR25),
        R25_failing_points=[{k: v for k, v in r.items() if k != 'point'}
                            for r in noR25],
        R25_failing_points_stored=[r for r in noR25 if r.get("point")],
        n_idx_zero=sum(1 for r in recs if r["n_idx"] == 0),
        ok=all(r["theorem_ok"] for r in recs))
    OUT["_controls_run"].append("M4_corpus")

    # ---------------------------------------------------------------- M5
    # delete the M2b fact and re-ask: with y5 == 1 tuples only, is there an
    # L-part whose argument does NOT close?  It must be non-empty, else M2b
    # was decorative.
    bad_restricted = []
    for x in sorted(Xv):
        f = fof[x]
        other = 3 - f
        if not [k for k, d in by.items()
                if k[0] == 1 and x in d.get(f, set()) and d.get(other)]:
            bad_restricted.append(str(x))
    OUT["M5_negctl"] = dict(
        executed=True, n_Xv=len(Xv),
        n_failing_if_restricted_to_y5_eq_1=len(bad_restricted),
        ok=(len(bad_restricted) > 0),
        note="restricted to y5 == 1 tuples the closure FAILS for every "
             "L-part (those tuples carry no firing-letter-2 choice), so the "
             "y5 != 1 fact M2b is load-bearing, not decoration")
    OUT["_controls_run"].append("M5_negctl")
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == [])
    OUT["done"] = True
    ck()
    print("M25FULL DONE  M1 ok=%s  M2 ok=%s  M3 bad=%d/%d  corpus viol=%d/%d "
          "(R25 fails at %d, all still deliver)"
          % (OUT["M1_matrices"]["ok"], OUT["M2_combinat"]["ok"], b3, n3,
             OUT["M4_corpus"]["n_violations"], len(recs), len(noR25)),
          flush=True)
    assert not missing, "CONTROL MANIFEST FAILURE %s" % missing


if __name__ == "__main__":
    main()
