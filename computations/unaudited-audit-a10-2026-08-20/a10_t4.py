#!/usr/bin/env python3
"""A10 TARGET 2-EXT -- audit of THEOREM W30-Y (the Q-span law), of the
escape object that refuted the (H)-containment, and of the single m=28/L2
exception.  UNAUDITED AUDIT LANE.  Exact only, own engine.

A10's hand derivation of W30-Y:
  At an untriggered word w with slice tuple tau (all three completions of
  v clean), the cofactor identity gives S'(tau).Q(w) = 0, so every such
  Q(w) lies in the RIGHT KERNEL of S'(tau).  Rank-nullity:

      rank S'(tau)  <=  |N(v)| - dim span{ Q(w) : w untriggered at tau }.

  Separately, for ANY linear P with ROWS[t] = P.S'[t] (P need NOT be
  injective), span-membership in S' implies span-membership in ROWS, so
  NON-delivery in ROWS implies non-membership in S'.  Hence two index
  choices at a common tau with |fire| = 1, distinct firing letters, both
  surviving (scale != 0) and both non-delivering force rank S'(tau) = 3
  (the doubly-clean row S'_{t3} is nonzero because every Gamma cell is).
  So dim span Q >= |N(v)| - 2  =>  rank S' <= 2  =>  contradiction  =>
  v DELIVERS.  NOTE: unlike W30-X, no |N| <= 3, no GL_3 isomorphism and
  no u_{q0} != 0 hypothesis is needed -- only the trivial direction of
  the transfer is used.

Checks (manifest asserted):
  Y1  the kernel/rank bound at every slice tuple of every vertex
  Y2  the delivery conclusion: hypothesis met => DELIVERS (scan for a
      counterexample: a FAILING vertex whose hypothesis is met)
  Y3  the escape object (m=27/F_13): clean by A10's raw 105-PM route,
      off-stratum, all Gamma cells nonzero, hafL zero count, the COVER
      property recomputed from A10's own admissible enumeration, and all
      eight vertices delivering
  Y4  the m=28 failing two-firing-letter vertices: is every failure
      explained by the hypothesis failing (Q-span too small OR a clean
      pair with no surviving index choice)?
  Y5  mutation control: the bound checker must be able to fail
  Y6  independent escape objects found by A10 (points where the
      two-firing-letter realisation is destroyed by scale zeros)
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from collections import defaultdict
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a10_lib as A                                                # noqa: E402
from a10_t2 import Sprime, Qvec, nbrs, load_all                    # noqa: E402

W30DIR = os.path.join(os.path.dirname(HERE),
                      "unaudited-exclusion-w30-2026-08-19")
RES = os.path.join(HERE, "results_t4.json")
DECL = ["Y1_kernel_bound", "Y2_delivery_conclusion", "Y3_escape_object",
        "Y4_m28_diagnosis", "Y5_mutation", "Y6_independent_escapes"]
OUT = {"_header": "UNAUDITED A10 audit of Theorem W30-Y (Q-span law)",
       "_controls_declared": DECL, "_controls_run": []}
TWO_LETTER = {25: ['R6', 'L2'], 26: ['R5', 'R6', 'L1', 'L2'],
              27: ['R5', 'R6', 'L1', 'L2'], 28: ['R5', 'R6', 'L1', 'L2']}


def ck():
    json.dump(OUT, open(RES, "w"), indent=1, default=str)


def untriggered_by_tau(m, v, ns):
    st = A.S(m)
    unt = defaultdict(list)
    others = [c for c in range(8) if c != v]
    for vals in product(range(3), repeat=7):
        w = [0] * 8
        for c, a in zip(others, vals):
            w[c] = a
        ok = True
        for t in range(3):
            ww = list(w)
            ww[v] = t
            if len(set(ww)) == 1 or st.active_live(tuple(ww)):
                ok = False
                break
        if ok:
            unt[tuple(w[s] for s in ns)].append(tuple(w))
    return unt


def qspan_vertex(m, bl, lab, K):
    kind, v = A.vsplit(lab)
    ns = nbrs(m, v)
    unt = untriggered_by_tau(m, v, ns)
    # index choices with a single firing letter, grouped by tau, marking
    # which have a SURVIVING (scale != 0) representative
    bytau = defaultdict(set)
    surv = defaultdict(set)
    for (w, Tf, Tc) in A.admissible_cached(m, kind, v, False):
        if len(Tf) != 1:
            continue
        tau = tuple(w[s] for s in ns)
        bytau[tau].add(Tf[0])
        if A.slice_rows(m, bl, kind, v, w, K) is not None:
            surv[tau].add(Tf[0])
    tuples = []
    nviol = 0
    for tau in sorted(set(list(bytau) + list(unt))):
        Sp = Sprime(m, bl, v, tau, ns, K)
        Qs = []
        for w in unt.get(tau, []):
            Q = Qvec(m, bl, v, w, ns, K)
            if any(not K.isz(z) for z in Q):
                Qs.append(Q)
        qd = A.rank(Qs, K) if Qs else 0
        rk = A.rank(Sp, K)
        ok = rk <= len(ns) - qd
        if not ok:
            nviol += 1
        tuples.append(dict(tau=list(tau), rankS=rk, Qspan=qd,
                           n_untriggered=len(unt.get(tau, [])),
                           n_letters=len(bytau.get(tau, ())),
                           n_surviving_letters=len(surv.get(tau, ())),
                           bound_ok=ok))
    thr = len(ns) - 2
    hyp = [x for x in tuples
           if x['n_surviving_letters'] >= 2 and x['Qspan'] >= thr]
    ver = A.vertex_verdict(m, bl, kind, v, K)
    return dict(vertex=lab, nN=len(ns), threshold=thr,
                n_tuples=len(tuples), bound_violations=nviol,
                n_two_letter_taus=sum(1 for x in tuples
                                      if x['n_letters'] >= 2),
                n_two_surviving_taus=sum(1 for x in tuples
                                         if x['n_surviving_letters'] >= 2),
                n_hypothesis_taus=len(hyp),
                max_Qspan_on_two_surviving=max(
                    [x['Qspan'] for x in tuples
                     if x['n_surviving_letters'] >= 2], default=-1),
                max_Qspan_on_two_letter=max(
                    [x['Qspan'] for x in tuples if x['n_letters'] >= 2],
                    default=-1),
                DELIVERS=ver['DELIVERS'], n_deliver=ver['n_deliver'],
                LAW_OK=(not hyp) or ver['DELIVERS'],
                tuples=tuples)


def main():
    t0 = time.time()
    pts = load_all()
    print("loaded %d off-stratum points" % len(pts), flush=True)
    recs = []
    nb = nlaw = 0
    seen = set()
    for (m, p, tag, bl) in pts:
        key = (m, p, tag)
        if key in seen:
            continue
        seen.add(key)
        if len(recs) >= 40 and m == 28 and "verify#" not in tag:
            continue
        K = A.Rat() if p == 0 else A.Fp(p)
        okc, _ = A.is_clean_point(m, bl, K)
        if not okc:
            continue
        allnz = A.all_gamma_cells_nonzero(m, bl, K)
        out = dict(m=m, p=p, tag=tag, allnz=allnz, vert={})
        for lab in A.VERTS:
            r = qspan_vertex(m, bl, lab, K)
            nb += r['bound_violations']
            nlaw += (0 if r['LAW_OK'] else 1)
            out['vert'][lab] = {k: v for k, v in r.items() if k != 'tuples'}
        recs.append(out)
        if len(recs) % 4 == 0 or len(recs) < 4:
            print("[%3d] m=%d p=%-2d %-28s fails=%s bviol=%d lawviol=%d "
                  "(%.0fs)"
                  % (len(recs), m, p, tag[:28],
                     [l for l in A.VERTS if not out['vert'][l]['DELIVERS']],
                     nb, nlaw, time.time() - t0), flush=True)
            OUT['points'] = recs
            ck()
        if time.time() - t0 > 1500:
            print("time budget reached, stopping the sweep", flush=True)
            break
    OUT['points'] = recs
    OUT['Y1_kernel_bound'] = dict(violations=nb, n_points=len(recs),
                                  ok=nb == 0)
    OUT['Y2_delivery_conclusion'] = dict(violations=nlaw, ok=nlaw == 0)
    OUT['_controls_run'] += ["Y1_kernel_bound", "Y2_delivery_conclusion"]
    ck()

    # ------------------------------------------------------ Y3 escape obj
    d = json.load(open(os.path.join(W30DIR, "results_escverify.json")))
    o = d["objects"][0]
    m, p = o["m"], o["p"]
    K = A.Fp(p)
    bl = {eval(k): [[int(z) % p for z in r] for r in v]
          for k, v in o["point"].items()}
    okc, badw = A.is_clean_point(m, bl, K)
    nz = A.n_words_phi_nonzero(m, bl, K)
    allnz = A.all_gamma_cells_nonzero(m, bl, K)
    st = A.S(m)
    # hafL over the 81 L-words
    nzero = 0
    hafzero = set()
    for x in product(range(3), repeat=4):
        ll = {(a, b): A.cell(bl, st.gs, a, b, x[a], x[b], K)
              for a in range(4) for b in range(4) if a < b}
        h = (ll[(0, 1)] * ll[(2, 3)] + ll[(0, 2)] * ll[(1, 3)]
             + ll[(0, 3)] * ll[(1, 2)]) % p
        if h == 0:
            nzero += 1
            hafzero.add(x)
    # COVER: at vertex R5, is every two-firing-letter tau killed by hafL
    # zeros?  recomputed from A10's own admissible enumeration
    v = 5
    ns = nbrs(m, v)
    bytau = defaultdict(set)
    surv = defaultdict(set)
    for (w, Tf, Tc) in A.admissible_cached(m, 'R', v, False):
        if len(Tf) != 1:
            continue
        tau = tuple(w[s] for s in ns)
        bytau[tau].add(Tf[0])
        if tuple(w[:4]) not in hafzero:
            surv[tau].add(Tf[0])
    two = [t for t in bytau if len(bytau[t]) >= 2]
    covered = [t for t in two if len(surv.get(t, ())) < 2]
    fails = [l for l in A.VERTS
             if not A.vertex_verdict(m, bl, *A.vsplit(l), K)['DELIVERS']]
    OUT['Y3_escape_object'] = dict(
        m=m, p=p, vertex="R5", clean=okc, n_clean_violations=len(badw),
        n_words_phi_nonzero=nz, allnz=allnz,
        n_hafL_zero_of_81=nzero,
        n_two_letter_taus=len(two), n_taus_covered_by_hafL_zeros=len(covered),
        escape_cover=(len(two) > 0 and len(covered) == len(two)),
        fails=fails, all_deliver=(fails == []),
        w30_claimed=dict(nzero_hafL=o['nzero_hafL'],
                         escape_cover=o['escape_cover'],
                         n_words_phi_nonzero=o['n_words_phi_nonzero'],
                         fails=o['fails']),
        ok=(okc and allnz and nz > 0 and fails == [] and
            len(two) > 0 and len(covered) == len(two)))
    OUT['_controls_run'].append("Y3_escape_object")
    print("Y3 escape object: clean=%s allnz=%s nz=%d hafLzero=%d/81 "
          "two=%d covered=%d fails=%s"
          % (okc, allnz, nz, nzero, len(two), len(covered), fails),
          flush=True)
    ck()

    # -------------------------------------------------- Y4 m=28 diagnosis
    diag = []
    for r in recs:
        if r['m'] != 28:
            continue
        for lab in TWO_LETTER[28]:
            vv = r['vert'][lab]
            if vv['DELIVERS']:
                continue
            diag.append(dict(tag=r['tag'], p=r['p'], vertex=lab,
                             nN=vv['nN'], threshold=vv['threshold'],
                             n_two_letter_taus=vv['n_two_letter_taus'],
                             n_two_surviving_taus=vv['n_two_surviving_taus'],
                             max_Qspan_two_letter=vv[
                                 'max_Qspan_on_two_letter'],
                             max_Qspan_two_surviving=vv[
                                 'max_Qspan_on_two_surviving'],
                             n_hypothesis_taus=vv['n_hypothesis_taus'],
                             explained_by_Qspan=(
                                 vv['max_Qspan_on_two_surviving'] <
                                 vv['threshold']),
                             explained_by_scale=(
                                 vv['n_two_surviving_taus'] <
                                 vv['n_two_letter_taus'] and
                                 vv['max_Qspan_on_two_letter'] >=
                                 vv['threshold'])))
    OUT['Y4_m28_diagnosis'] = dict(
        records=diag, n=len(diag),
        n_unexplained=sum(1 for x in diag if x['n_hypothesis_taus'] > 0),
        n_explained_by_scale_only=sum(
            1 for x in diag if not x['explained_by_Qspan'] and
            x['explained_by_scale']),
        ok=all(x['n_hypothesis_taus'] == 0 for x in diag))
    OUT['_controls_run'].append("Y4_m28_diagnosis")
    ck()

    # ------------------------------------------------------- Y5 mutation
    K = A.Fp(31)
    rng = random.Random(4242)
    bl2 = {e: [[rng.randrange(1, 31) for _ in range(3)] for _ in range(3)]
           for e in A.S(28).gamma}
    r = qspan_vertex(28, bl2, 'R5', K)
    OUT['Y5_mutation'] = dict(
        note="on a NON-clean random point the untriggered words no longer "
             "annihilate S', so the kernel bound must be violated -- the "
             "checker is not vacuously true",
        bound_violations_on_random_point=r['bound_violations'],
        ok=r['bound_violations'] > 0)
    OUT['_controls_run'].append("Y5_mutation")
    print("Y5 mutation: bound violations on random non-clean point = %d"
          % r['bound_violations'], flush=True)

    # --------------------------------------------- Y6 independent escapes
    esc = []
    for r in recs:
        for lab in TWO_LETTER.get(r['m'], []):
            vv = r['vert'][lab]
            if (vv['n_two_letter_taus'] > 0 and
                    vv['n_two_surviving_taus'] == 0):
                esc.append(dict(m=r['m'], p=r['p'], tag=r['tag'],
                                vertex=lab, DELIVERS=vv['DELIVERS'],
                                n_two_letter_taus=vv['n_two_letter_taus']))
    OUT['Y6_independent_escapes'] = dict(
        records=esc[:20], n=len(esc),
        note="points at which the two-firing-letter realisation is "
             "destroyed by scale zeros at EVERY tuple -- the (H) escape "
             "geometry, found independently by A10",
        n_still_delivering=sum(1 for x in esc if x['DELIVERS']),
        ok=True)
    OUT['_controls_run'].append("Y6_independent_escapes")

    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = missing == []
    OUT["_manifest_missing"] = missing
    OUT["elapsed_s"] = round(time.time() - t0, 1)
    OUT["done"] = True
    ck()
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("T4 DONE bound_viol=%d law_viol=%d escapes=%d (%.0fs)"
          % (nb, nlaw, len(esc), time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
