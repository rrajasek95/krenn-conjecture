#!/usr/bin/env python3
"""A11 TARGET 2 -- THEOREM W30-Z.  UNAUDITED.

W30-Z as transcribed (REPORT, round 3):

  "At a two-firing-letter vertex with a two-pair tuple whose both clean
   pairs survive and S_{t1} not in ker phi: rank S(tau) <= 2 => the vertex
   DELIVERS; failure requires rank S(tau) = 3."

Hand re-derivation (spine Remark 3.3 + 5.0).  Write ROWS[t] = P.S'(tau)[t],
P linear.  Let t1 != t2 be the two firing letters realised at the common
tuple tau by admissible choices i1 (T_f = {t1}, T_c = {t2,t3}) and i2
(T_f = {t2}, T_c = {t1,t3}), both of nonzero scale.  rank S'(tau) <= 2 gives
a nontrivial dependency a1 S'[t1] + a2 S'[t2] + a3 S'[t3] = 0; applying P,
a1 R1 + a2 R2 + a3 R3 = 0.

  * a1 != 0  =>  R1 in span{R2,R3}  =>  v delivers at i1.
  * a2 != 0  =>  v delivers at i2.
  * a1 = a2 = 0  =>  a3 S'[t3] = 0 with a3 != 0  =>  S'[t3] = 0.

So the implication needs exactly ONE side condition: the doubly-clean row
S'[t3] is nonzero -- which is what "all Gamma cells nonzero" buys (it is
A10's fix to W30-X step (2), inherited verbatim by spine Lemma 5.1).  The
transcribed side condition "S_{t1} not in ker phi" is a different statement:
it is IMPLIED by failure at i1 (failure needs R1 != 0), so as a hypothesis
of this direction it is redundant, and it does NOT cover the S'[t3] = 0 hole.

STEPS
  Z1  template facts: firing letters / |N| / two-pair tuples per (m,vertex),
      and the negative control "two firing letters AND |N| <= 3 selects
      exactly the protected set".
  Z2  the implication, machine-checked on synthetic slice data, WITH and
      WITHOUT each side condition (so each is shown load-bearing or not).
  Z3  blind test on a stored point corpus, my own engine, with every
      exception traced.
usage: a11_t3.py [n_m28_points] [seconds]
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from collections import Counter, defaultdict
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W30 = os.path.join(os.path.dirname(HERE), "unaudited-exclusion-w30-2026-08-19")
sys.path.insert(0, HERE)
import a11_lib as A      # noqa: E402

DECL = ["Z1_template_facts", "Z1_negative_control", "Z2_implication",
        "Z2_side_condition_necessity", "Z2_kerphi_redundancy",
        "Z3_blind_test", "Z3_exception_traces"]

PROTECTED = {25: ['R6'], 26: ['R5', 'R6'], 27: ['R5'], 28: []}


def two_pair_structure(m, lab):
    """tuples tau at which two DISTINCT firing letters are realised by
    |T_f| = 1 admissible choices -- W30's 'two-pair tuple'."""
    tm = A.T(m)
    kind, v = A.vsplit(lab)
    ns = tm.nbr[v]
    by = defaultdict(dict)
    for (w, Tf, Tc) in A.admissible_cached(m, kind, v):
        if len(Tf) != 1:
            continue
        tau = tuple(w[s] for s in ns)
        by[tau].setdefault(Tf[0], []).append((w, Tc))
    return {tau: d for tau, d in by.items() if len(d) >= 2}


def scale_of(tm, bl, kind, v, w, K):
    return A.hafL(tm, bl, w, K) if kind == 'R' else A.hafR(tm, bl, w, K)


def delivers_at(tm, bl, kind, v, w, Tf, Tc, K):
    rows, coef, sc, cols = A.master_rows(tm, bl, kind, v, w, K)
    if K.iszero(sc):
        return None
    base = [rows[t] for t in Tc]
    rb = A.rank(base, K)
    return all(A.rank(base + [rows[t]], K) == rb for t in Tf)


def main():
    n28 = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    budget = float(sys.argv[2]) if len(sys.argv) > 2 else 900.0
    t0 = time.time()
    man = A.Manifest(DECL)
    rng = random.Random(31415926)

    # ------------------------------------------------------- Z1 template
    facts = {}
    for m in (25, 26, 27, 28):
        tm = A.T(m)
        for lab in A.VLAB:
            kind, v = A.vsplit(lab)
            sing = A.singles_into(tm, kind, v)
            letters = sorted({l for (_e, _t, _tv, l) in sing})
            tp = two_pair_structure(m, lab)
            facts["%d_%s" % (m, lab)] = dict(
                nN=tm.deg(v), neighbours=list(tm.nbr[v]),
                live_singles=[[str(e), trig, tv, l]
                              for (e, trig, tv, l) in sing],
                firing_letters=letters, n_two_firing=len(letters),
                n_two_pair_tuples=len(tp),
                protected=(lab in PROTECTED[m]))
    man.record("Z1_template_facts", dict(facts=facts, ok=True))
    sel = sorted(k for k, f in facts.items()
                 if f['n_two_firing'] >= 2 and f['nN'] <= 3)
    prot = sorted("%d_%s" % (m, l) for m in PROTECTED for l in PROTECTED[m])
    man.record("Z1_negative_control", dict(
        selected_by_criterion=sel, protected_set=prot,
        matches=(sel == prot), ok=(sel == prot),
        note="round 3's control: 'two firing letters AND |N|<=3' must select "
             "EXACTLY the protected set"))
    print("Z1 criterion selects %s ; protected %s ; match=%s"
          % (sel, prot, sel == prot))

    # ------------------------------------------------- Z2 the implication
    # synthetic: random n, random S' of rank <= 2, random P of the shape
    # P(z)[q] = z_sigma*u[q] + sc*z_{sigma q}
    K = A.Modp(31)
    tests = 0
    viol_with = 0
    viol_without = []
    kerphi_when_fail = 0
    fail_cases = 0
    for _ in range(40000):
        n = rng.choice([2, 3, 4])
        # rank <= 2 rows
        b1 = [K.of(rng.randrange(31)) for _ in range(n)]
        b2 = [K.of(rng.randrange(31)) for _ in range(n)]
        S = []
        for _t in range(3):
            c1, c2 = K.of(rng.randrange(31)), K.of(rng.randrange(31))
            S.append([K.add(K.mul(c1, x), K.mul(c2, y))
                      for x, y in zip(b1, b2)])
        if A.rank(S, K) > 2:
            continue
        # P: pick a "sigma" column index (or none) and u, sc
        sig = rng.randrange(n) if rng.random() < 0.7 else None
        sc = K.of(1 + rng.randrange(30))
        u = [K.of(rng.randrange(31)) for _ in range(3)]
        cols = [j for j in range(n) if j != sig]

        def P(z):
            out = [K.zero] * 3
            for q in range(3):
                val = K.mul(z[sig], u[q]) if sig is not None else K.zero
                if q < len(cols):
                    val = K.add(val, K.mul(sc, z[cols[q]]))
                out[q] = val
            return out

        R = [P(S[t]) for t in range(3)]
        t1, t2, t3 = 0, 1, 2
        d1 = A.in_span(R[t1], [R[t2], R[t3]], K)
        d2 = A.in_span(R[t2], [R[t1], R[t3]], K)
        tests += 1
        s3nz = any(not K.iszero(z) for z in S[t3])
        if s3nz and not (d1 or d2):
            viol_with += 1
        if not s3nz and not (d1 or d2):
            if len(viol_without) < 5:
                viol_without.append(dict(S=[[str(z) for z in r] for r in S],
                                         u=[str(z) for z in u], sc=str(sc),
                                         sigma_col=sig))
        if not (d1 or d2):
            fail_cases += 1
            if all(K.iszero(z) for z in R[t1]):
                kerphi_when_fail += 1
    man.record("Z2_implication", dict(
        tests=tests, violations_with_S_t3_nonzero=viol_with,
        ok=viol_with == 0,
        statement="rank S'(tau) <= 2 AND S'[t3] != 0  =>  delivery at i1 or i2",
        note="synthetic over F_31, random n in {2,3,4}, random transfer map P"))
    man.record("Z2_side_condition_necessity", dict(
        n_counterexamples_when_S_t3_zero=len(viol_without),
        examples=viol_without, ok=len(viol_without) > 0,
        note="without S'[t3] != 0 the implication is FALSE -- these are "
             "explicit rank-2 slices with a zero doubly-clean row at which "
             "neither firing row lies in its clean span"))
    man.record("Z2_kerphi_redundancy", dict(
        n_non_delivering_configs=fail_cases,
        n_of_those_with_R_t1_zero=kerphi_when_fail,
        ok=(kerphi_when_fail == 0),
        note="'S_{t1} not in ker phi' is implied by non-delivery at i1 "
             "(R1 must be nonzero), so as a hypothesis of the rank<=2 "
             "direction it is redundant"))
    print("Z2 implication: %d tests, %d violations with S'[t3]!=0; "
          "%d counterexamples when S'[t3]=0; ker-phi redundancy ok=%s"
          % (tests, viol_with, len(viol_without), kerphi_when_fail == 0))

    # ------------------------------------------------------ Z3 blind test
    dat = json.load(open(os.path.join(W30, "points_hunt.json")))
    pool = dat["points"]
    small = [r for r in pool if int(r["m"]) in (25, 26, 27)]
    big = [r for r in pool if int(r["m"]) == 28]
    rng.shuffle(big)
    chosen = small + big[:n28]
    rows = []
    exceptions = []
    for r in chosen:
        if time.time() - t0 > budget:
            break
        m = int(r["m"])
        p = int(r["p"])
        K = A.Rat if p == 0 else A.Modp(p)
        tm = A.T(m)
        bl = A.load_point(r["point"], K)
        cleanok = A.is_clean_point(tm, bl, K)
        allnz = A.all_cells_nonzero(tm, bl, K)
        offs = A.n_phi_nonzero(tm, bl, K) > 0
        for lab in A.VLAB:
            kind, v = A.vsplit(lab)
            sing = A.singles_into(tm, kind, v)
            letters = sorted({l for (_e, _t, _tv, l) in sing})
            if len(letters) < 2:
                continue
            tp = two_pair_structure(m, lab)
            ver = A.verdict(tm, bl, lab, K)
            # tuples where two clean pairs SURVIVE (nonzero scale)
            good = []
            for tau, d in tp.items():
                surv = {}
                for t, lst in d.items():
                    for (w, Tc) in lst:
                        if not K.iszero(scale_of(tm, bl, kind, v, w, K)):
                            surv[t] = (w, Tc)
                            break
                if len(surv) >= 2:
                    good.append((tau, surv))
            for (tau, surv) in good:
                S = A.slice_S(tm, bl, v, tau, K)
                rk = A.rank(S, K)
                ts = sorted(surv)[:2]
                t3 = [t for t in range(3) if t not in ts]
                s3nz = (not t3) or any(not K.iszero(z) for z in S[t3[0]])
                loc = []
                for t in ts:
                    w, Tc = surv[t]
                    loc.append(delivers_at(tm, bl, kind, v, w, (t,), Tc, K))
                rec = dict(tag=r["tag"], m=m, p=p, vertex=lab,
                           tau=list(tau), rank=rk, S_t3_nonzero=s3nz,
                           local_delivers=[bool(x) for x in loc],
                           vertex_delivers=ver['DELIVERS'],
                           clean=cleanok, all_cells_nonzero=allnz,
                           off_stratum=offs)
                rows.append(rec)
                if rk <= 2 and s3nz and not any(loc):
                    exceptions.append(dict(rec, why="RANK<=2 BUT NO LOCAL "
                                                    "DELIVERY -- W30-Z "
                                                    "COUNTEREXAMPLE"))
                if rk <= 2 and s3nz and not ver['DELIVERS']:
                    exceptions.append(dict(rec, why="RANK<=2 BUT VERTEX FAILS"))
    # per (point,vertex) summary in the shape of W30's blind-test record
    byv = defaultdict(list)
    for x in rows:
        byv[(x['tag'], x['vertex'])].append(x)
    le2_tot = le2_del = r3_tot = r3_fail = 0
    for k, xs in byv.items():
        ranks = {x['rank'] for x in xs}
        dl = xs[0]['vertex_delivers']
        if max(ranks) <= 2:
            le2_tot += 1
            le2_del += 1 if dl else 0
        if min(ranks) == 3:
            r3_tot += 1
            r3_fail += 1 if not dl else 0
    man.record("Z3_blind_test", dict(
        n_points=len(chosen), n_measurements=len(rows),
        n_point_vertex_pairs=len(byv),
        deliver_at_rank_le2="%d/%d" % (le2_del, le2_tot),
        fail_at_rank3="%d/%d" % (r3_fail, r3_tot),
        n_W30Z_counterexamples=len(exceptions),
        rank_hist=dict(Counter(x['rank'] for x in rows)),
        n_measurements_on_nonclean_points=sum(1 for x in rows
                                              if not x['clean']),
        n_measurements_with_a_zero_cell=sum(1 for x in rows
                                            if not x['all_cells_nonzero']),
        ok=(len(exceptions) == 0),
        note="rank<=2 => delivers is W30-Z; rank 3 => fails is its CONVERSE, "
             "which round 4 itself refuted -- reported separately"))
    man.record("Z3_exception_traces", dict(
        n=len(exceptions), traces=exceptions[:20], ok=True))
    print("Z3 blind test: %d measurements over %d (point,vertex) pairs; "
          "deliver@rank<=2 %d/%d ; fail@rank3 %d/%d ; W30-Z counterexamples %d"
          % (len(rows), len(byv), le2_del, le2_tot, r3_fail, r3_tot,
             len(exceptions)))

    man.finish(os.path.join(HERE, "results_t3.json"),
               extra={"_header": "UNAUDITED A11 target 2: THEOREM W30-Z",
                      "elapsed_s": round(time.time() - t0, 1),
                      "measurements": rows[:400]})
    print("T3 DONE in %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
