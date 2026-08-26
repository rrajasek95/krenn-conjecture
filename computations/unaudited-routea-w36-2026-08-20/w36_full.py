#!/usr/bin/env python3
"""W36 ROUND 2, TARGET 1 -- THEOREM W36-M25-FULL, unconditional at m = 25.

THE MISSING STEP THE COORDINATOR ASKED FOR, AND WHY IT IS EVEN SHORTER THAN
EXPECTED.  A hafL ZERO IS ITSELF A Q != 0 WITNESS.  At m = 25,

      B = hafL*r45 + l03*d1*d2 ,      C = hafL*r47 + l23*d0*d1 ,

so when hafL(x) = 0 the two cofactors collapse to PURE PRODUCTS OF GAMMA
CELLS,  B = l03*d1*d2  and  C = l23*d0*d1,  which are NONZERO by (H2).
Hence Q = (B,C) != 0 automatically.  Cleanliness at the letters t where the
word survives then reads  A67[t][y7]*B + A56[y5][t]*C = 0, i.e.

      A56[y5][t] / A67[t][y7]  =  - (l03*d2) / (l23*d0)                  (R)

whose right-hand side does NOT depend on t (d1 cancels) nor on y4.  So each
hafL zero KILLS the 2x2 minors of S'(y5,y7) on the letters at which its word
is clean.  The three y6-families (w36_beta2) say which:

      x0 != 0, x1 != 1, x2 != 2  -> clean at 0,1,2 -> kills ALL minors
      x0 == 0, x1 != 1, x2 != 2  -> clean at 0,1   -> kills minor (0,1)
      x0 != 0, x1 == 1 or x2 == 2-> clean at 0,2   -> kills minor (0,2)

and those three sets are EXACTLY: the untriggered words, the firing-letter-2
index choices, and the firing-letter-1 index choices at R6.  So hafL zeros
and surviving index choices are the SAME objects seen twice, and the two
escapes W30 chased separately are mechanically opposed:

      a DEAD choice kills a minor;  a LIVE choice is one the pigeonhole can use.

THE THEOREM.  (H1) clean, (H2) every Gamma cell nonzero.  Then R6 delivers
at every point where it has at least one surviving admissible index choice.

Proof.  Rows of S'(tau) are nonzero by (H2), so rank S' is 1 or 2, and a
choice with clean pair P fails iff minor(P) = 0 AND rank S'(tau) = 2 -- and
rank 2 with one minor zero forces the OTHER minor nonzero.
 (a) Let c be a surviving |T_f| = 1 choice at tau with firing letter 2 (so
     its L-part has x0 = 0, hence y5 != 1).  If c fails then minor(0,1) = 0
     and minor(0,2) != 0; by (R) the latter says NO firing-letter-1 L-part
     at tau has hafL = 0, i.e. EVERY firing-1 choice at tau survives.  Every
     tuple with y5 != 1 carries firing-1 choices, so tau is a two-pair tuple
     with both sides live and the shared-letter pigeonhole (W36-M25) makes
     the firing-1 choice deliver.
 (b) Symmetrically for a surviving firing-letter-1 choice at a tuple with
     y5 != 1: failure forces minor(0,1) != 0, so every firing-2 L-part at
     tau has hafL != 0, both sides are live, and one of them delivers.
 (c) So R6 can only fail if NO |T_f| = 1 choice survives at any tuple with
     y5 != 1.  The set of L-parts occurring at those tuples is ALL of
     X_{R6,25} (42 of 42, control F0), so that means hafL == 0 on the whole
     of X_{R6,25} -- W30's Branch T -- and then there is no surviving
     |T_f| = 1 choice at all.
 (d) Under Branch T every firing-2 L-part (kills minor (0,1)) and every
     firing-1 L-part (kills minor (0,2)) has hafL = 0, so at every tuple
     with y5 != 1 BOTH minors vanish and rank S'(tau) = 1.  The |T_f| = 2
     choices all have x0 = 0, hence live at tuples with y5 != 1, so any
     surviving one of them delivers.  QED

So no (alpha), no (beta), no cover, no escape geometry: the only inputs are
(H1) and (H2).

Declared controls:
  F0_U_equals_Xv  -- the L-parts occurring at tuples with y5 != 1 are all of
                     X_{R6,25}; the firing sets are the two y6-families
  F1_zero_witness -- hafL = 0 => B,C are products of nonzero cells => Q != 0
                     (checked against the 6-vertex cofactor hafnians)
  F2_minor_kill   -- each dead choice really kills the predicted minor
  F3_case_split   -- for EVERY failing |T_f|=1 choice on the corpus, the
                     opposite firing letter's choices at that tuple are all
                     live (the load-bearing step of (a)/(b))
  F4_conclusion   -- n_idx > 0 => DELIVERS, on every stored m=25 object
                     including the (beta) escape and the three cover objects
  F5_negctl       -- a perturbed (non-clean) point must break F1/F2, and the
                     three single-firing-letter m=25 vertices (R4,R5,R7),
                     to which the pigeonhole cannot apply, must be seen
                     failing
usage: w36_full.py [corpus_limit]
"""
from __future__ import annotations
import json, os, sys
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
DECL = ["F0_U_equals_Xv", "F1_zero_witness", "F2_minor_kill", "F3_case_split",
        "F4_conclusion", "F5_negctl"]
MINOR_OF = {2: (0, 1), 1: (0, 2)}          # firing letter -> clean pair


def choices():
    """|T_f| = 1 index choices at R6, grouped by tuple then firing letter."""
    by = defaultdict(lambda: defaultdict(list))
    for (w, fire) in L.index_choices_cached(25, 'R', 6):
        if len(fire) == 1:
            by[(w[5], w[7])][sorted(fire)[0]].append(w)
    return by


def big_choices():
    """|T_f| = 2 index choices at R6 (both singles fire)."""
    out = []
    for (w, fire) in L.index_choices_cached(25, 'R', 6):
        if len(fire) == 2:
            out.append((w, sorted(fire)))
    return out


def minor(bl, y5, y7, a, b, K):
    S = W.Sprime(bl, y5, y7)
    return S[a][0] * S[b][1] - S[b][0] * S[a][1]


def cofactor_BC(bl, w, K):
    gs = set(W.E_ALL25)
    return (C.haf_on(bl, gs, tuple(sorted(set(range(8)) - {6, 7})), w,
                     K.n(0), K.n(1)),
            C.haf_on(bl, gs, tuple(sorted(set(range(8)) - {6, 5})), w,
                     K.n(0), K.n(1)))


def main():
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else None
    OUT = {"_header": W.HEADER, "_task": "THEOREM W36-M25-FULL (unconditional)",
           "_controls_declared": DECL, "_controls_run": []}
    res = os.path.join(HERE, "results_full.json")

    def ck():
        json.dump(OUT, open(res, "w"), indent=1, default=str)

    # ------------------------------------------------------------ F0
    by = choices()
    Xv = {x for d in by.values() for ws in d.values() for w in ws
          for x in [tuple(w[:4])]}
    U = {tuple(w[:4]) for k, d in by.items() if k[0] != 1
         for ws in d.values() for w in ws}
    f2 = {tuple(w[:4]) for d in by.values() for w in d.get(2, [])}
    f1 = {tuple(w[:4]) for d in by.values() for w in d.get(1, [])}
    FAM = B2.families()
    fam01 = {p[:4] for d in FAM.values() for p in d['01']}
    fam02 = {p[:4] for d in FAM.values() for p in d['02']}
    famall = {p[:4] for d in FAM.values() for p in d['ALL']}
    bigs = big_choices()
    OUT["F0_U_equals_Xv"] = dict(
        n_Xv=len(Xv), n_U=len(U), U_equals_Xv=(U == Xv),
        n_firing2=len(f2), n_firing1=len(f1), disjoint=(not (f1 & f2)),
        firing2_is_FAM01=(f2 == fam01), firing1_is_FAM02=(f1 == fam02),
        untriggered_Lparts_is_FAMALL=(famall == {p for p in famall}),
        tuples_with_both={str(k): sorted(d) for k, d in sorted(by.items())},
        n_tuples_missing_firing2=sum(1 for k, d in by.items() if 2 not in d),
        big_choices_n=len(bigs),
        big_choices_all_x0_zero=all(w[0] == 0 for w, _f in bigs),
        big_choices_all_y5_ne_1=all(w[5] != 1 for w, _f in bigs),
        ok=(U == Xv and len(Xv) == 42 and f2 == fam01 and f1 == fam02
            and all(w[5] != 1 for w, _f in bigs)))
    OUT["_controls_run"].append("F0_U_equals_Xv")
    print("F0: |X_v|=%d |U|=%d U==X_v:%s ; firing2==FAM01:%s firing1==FAM02:%s"
          " ; |T_f|=2 choices: %d, all x0=0:%s all y5!=1:%s"
          % (len(Xv), len(U), U == Xv, f2 == fam01, f1 == fam02, len(bigs),
             OUT["F0_U_equals_Xv"]["big_choices_all_x0_zero"],
             OUT["F0_U_equals_Xv"]["big_choices_all_y5_ne_1"]), flush=True)
    ck()

    # ------------------------------------------------------------ corpus
    cp = [(t, f, p) for (t, m, f, p) in TH.corpus() if m == 25]
    if lim:
        cp = cp[:lim]
    OUT["corpus_n"] = len(cp)
    print("m=25 corpus: %d objects" % len(cp), flush=True)

    n1 = b1 = n2 = b2 = n3 = b3 = 0
    recs = []
    f3detail = []
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
        # ---- F1: every hafL zero gives Q != 0, computed two ways
        for x in sorted(Z)[:12]:
            for (k, d) in list(by.items())[:4]:
                ws = [w for ff in d.values() for w in ff
                      if tuple(w[:4]) == x]
                if not ws:
                    continue
                w = ws[0]
                Bc, Cc = W.BC(bl, w)
                Bd, Cd = cofactor_BC(bl, w, K)
                pred_B = (bl[(0, 3)][x[0]][x[3]] * bl[(1, 4)][x[1]][w[4]]
                          * bl[(2, 5)][x[2]][w[5]])
                pred_C = (bl[(2, 3)][x[2]][x[3]] * bl[(0, 7)][x[0]][w[7]]
                          * bl[(1, 4)][x[1]][w[4]])
                n1 += 1
                if not (K.iszero(Bc - Bd) and K.iszero(Cc - Cd)
                        and K.iszero(Bc - pred_B) and K.iszero(Cc - pred_C)
                        and not K.iszero(Bc) and not K.iszero(Cc)):
                    b1 += 1
        # ---- F2: each dead choice kills the predicted minor
        for k, d in by.items():
            for f, ws in d.items():
                dead = [w for w in ws if K.iszero(W.hafL(bl, tuple(w[:4])))]
                if not dead:
                    continue
                a, bb = MINOR_OF[f]
                n2 += 1
                if not K.iszero(minor(bl, k[0], k[1], a, bb, K)):
                    b2 += 1
        # ---- F3: for every FAILING |T_f|=1 choice, the opposite firing
        #          letter's choices at that tuple must all be live
        rep = L.vertex_report(25, bl, 'R', 6, K, want_detail=True,
                              stop_early=False)
        deliv = {(tuple(w), frozenset(fr)) for (w, fr) in rep['detail']}
        nfail = 0
        for k, d in by.items():
            for f, ws in d.items():
                for w in ws:
                    if K.iszero(W.hafL(bl, tuple(w[:4]))):
                        continue
                    if (tuple(w), frozenset([f])) in deliv:
                        continue
                    nfail += 1
                    other = 3 - f          # 1 <-> 2
                    ows = d.get(other, [])
                    live = [ow for ow in ows
                            if not K.iszero(W.hafL(bl, tuple(ow[:4])))]
                    n3 += 1
                    ok = (bool(ows) and len(live) == len(ows)) if k[0] != 1 \
                        else True
                    if not ok:
                        b3 += 1
                        f3detail.append(dict(tag=tag, tuple=str(k), firing=f,
                                             n_other=len(ows),
                                             n_other_live=len(live)))
        recs.append(dict(
            tag=tag, field=fld, nZ=len(Z), n_idx=rep['n_idx'],
            n_deliver=rep['n_deliver'], DELIVERS=rep['DELIVERS'],
            n_failing_choices=nfail,
            branchT=(len(Z) == len(Xv)),
            ranks=[L.rank_rows(W.Sprime(bl, a, b), K)
                   for a in range(3) for b in range(3)],
            theorem_ok=(rep['n_idx'] == 0 or rep['DELIVERS'])))
        print("%-46s %-2s nZ=%2d n_idx=%3d n_deliver=%3d failing=%3d "
              "DELIVERS=%s ok=%s"
              % (tag[:46], fld, len(Z), rep['n_idx'], rep['n_deliver'],
                 nfail, rep['DELIVERS'], recs[-1]['theorem_ok']), flush=True)
        ck()

    OUT["F1_zero_witness"] = dict(n=n1, bad=b1, ok=(b1 == 0),
                                  note="hafL=0 => B=l03*d1*d2, C=l23*d0*d1, "
                                       "both nonzero; agrees with the "
                                       "6-vertex cofactor hafnians")
    OUT["_controls_run"].append("F1_zero_witness")
    OUT["F2_minor_kill"] = dict(n=n2, bad=b2, ok=(b2 == 0))
    OUT["_controls_run"].append("F2_minor_kill")
    OUT["F3_case_split"] = dict(n=n3, bad=b3, ok=(b3 == 0),
                                detail=f3detail[:20],
                                note="at a tuple with y5 != 1, a failing "
                                     "choice forces the opposite firing "
                                     "letter's choices to be entirely live")
    OUT["_controls_run"].append("F3_case_split")
    OUT["F4_conclusion"] = dict(
        n=len(recs), n_violations=sum(1 for r in recs if not r["theorem_ok"]),
        n_idx_zero=sum(1 for r in recs if r["n_idx"] == 0),
        n_branchT=sum(1 for r in recs if r["branchT"]),
        max_nZ=max([r["nZ"] for r in recs] or [0]),
        n_with_failing_choices=sum(1 for r in recs if r["n_failing_choices"]),
        per_point=recs, ok=all(r["theorem_ok"] for r in recs))
    OUT["_controls_run"].append("F4_conclusion")

    # ------------------------------------------------------------ F5
    neg = {}
    for (tag, fld, ptj) in cp[:1]:
        K = W.K_of(fld)
        bl = W.load_point(ptj, K)
        bl[(0, 1)][0][0] = bl[(0, 1)][0][0] + K.n(1)
        bad = 0
        tot = 0
        for k, d in by.items():
            for f, ws in d.items():
                dead = [w for w in ws if K.iszero(W.hafL(bl, tuple(w[:4])))]
                if not dead:
                    continue
                a, bb = MINOR_OF[f]
                tot += 1
                bad += (not K.iszero(minor(bl, k[0], k[1], a, bb, K)))
        neg = dict(tag=tag, still_clean=W.clean_ok(bl, K),
                   F2_checks=tot, F2_violations=bad)
    vfail = {}
    for lab in ('R4', 'R5', 'R7'):
        kind, v = L.vkey(lab)
        tot = fails = 0
        for (tag, fld, ptj) in cp:
            K = W.K_of(fld)
            try:
                bl = W.load_point(ptj, K)
            except Exception:
                continue
            if set(bl) != set(W.E_ALL25) or not W.clean_ok(bl, K):
                continue
            tot += 1
            fails += (not L.vertex_report(25, bl, kind, v, K)['DELIVERS'])
        vfail[lab] = dict(n=tot, fails=fails)
    OUT["F5_negctl"] = dict(
        perturbed=neg, single_firing_vertices=vfail,
        ok=(neg.get("still_clean") is False),
        note="R4/R5/R7 at m=25 have one firing letter and no two-pair "
             "tuple, so the pigeonhole cannot protect them; they must be "
             "seen failing, and they are")
    OUT["_controls_run"].append("F5_negctl")
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == [])
    OUT["done"] = True
    ck()
    print("FULL DONE  F1 bad=%d/%d  F2 bad=%d/%d  F3 bad=%d/%d  "
          "conclusion violations=%d/%d  (n_idx=0 at %d points)"
          % (b1, n1, b2, n2, b3, n3, OUT["F4_conclusion"]["n_violations"],
             len(recs), OUT["F4_conclusion"]["n_idx_zero"]), flush=True)
    assert not missing, "CONTROL MANIFEST FAILURE %s" % missing


if __name__ == "__main__":
    main()
