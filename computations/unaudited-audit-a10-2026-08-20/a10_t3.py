#!/usr/bin/env python3
"""A10 TARGET 3 -- the sampling-artifact claim.  UNAUDITED AUDIT LANE.

W30 claims W26's failure counts over-report because W26 sampled 40-60
ambient WORDS against 243-823 admissible index choices, and DELIVERS is a
disjunction over index choices.

Checked here:
  G1  coverage arithmetic, recomputed from A10's own admissible-index
      enumeration (no W26/W30 code)
  G2  a re-implementation of W26's sampler ON TOP OF A10's own engine
      (same RNG protocol: one random.Random(seed), 8 letters per draw,
      vertices consuming the stream in order) -- the sampled verdict is
      compared with A10's exhaustive verdict on the same blocks.  Only
      one direction of disagreement is possible if the claim is right:
      sampled says FAIL where exhaustive says DELIVERS.
  G3  the two corrected patterns: m=28 'W21break 777' and m=28
      'tensorZERO', vertex L1 -- exhaustive pass, plus an explicit
      delivering index choice and a direct check that Phi vanishes at
      its firing letter and that a genuine PURE ROW results.
Controls: G4 mutation (the sampled engine must be able to report
DELIVERS), G5 the exhaustive verdict must reproduce the sampled one
whenever the sample happens to be exhaustive (tiny index sets).
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a10_lib as A                                                # noqa: E402

W30DIR = os.path.join(os.path.dirname(HERE),
                      "unaudited-exclusion-w30-2026-08-19")
RES = os.path.join(HERE, "results_t3.json")
DECL = ["G1_coverage", "G2_sampled_vs_exhaustive", "G3_corrected_patterns",
        "G4_mutation", "G5_degenerate_agreement"]
OUT = {"_header": "UNAUDITED A10 target-3 sampling-artifact audit",
       "_controls_declared": DECL, "_controls_run": []}


def ck():
    json.dump(OUT, open(RES, "w"), indent=1, default=str)


def sampled_verdict(m, bl, K, nsample, seed):
    """W26's protocol, re-implemented on A10's engine: one RNG stream, 8
    letters per draw, the eight vertices consuming it in order; an index
    choice counts only if it passes the same admissibility filter."""
    rng = random.Random(seed)
    out = {}
    st = A.S(m)
    for lab in A.VERTS:
        kind, v = A.vsplit(lab)
        mine = A.singles_at(m, kind, v)
        deliv = False
        nadm = nlive = 0
        for _ in range(nsample):
            w = [rng.randrange(3) for _ in range(8)]
            fire = set(letter for (e, trig, tv, letter) in mine
                       if w[trig] == tv)
            if not fire:
                continue
            ok = True
            Tc, Tf = [], []
            for t in range(3):
                ww = list(w)
                ww[v] = t
                if len(set(ww)) == 1:
                    ok = False
                    break
                act = st.active_live(tuple(ww))
                if t not in fire:
                    if act:
                        ok = False
                        break
                    Tc.append(t)
                else:
                    if any((e[1] if kind == 'R' else e[0]) != v
                           for e in act):
                        ok = False
                        break
                    Tf.append(t)
            if not ok:
                continue
            nadm += 1
            sd = A.slice_rows(m, bl, kind, v, tuple(w), K)
            if sd is None:
                continue
            nlive += 1
            rows = sd[0]
            cr = [rows[t] for t in Tc]
            rc = A.rank(cr, K)
            if all(A.rank(cr + [rows[t]], K) == rc for t in Tf):
                deliv = True
        out[lab] = dict(DELIVERS=deliv, n_admissible_sampled=nadm,
                        n_live_sampled=nlive)
    return out


def load(tagsub, m):
    d = json.load(open(os.path.join(W30DIR, "points_stored.json")))
    for e in d["points"]:
        if e["m"] == m and tagsub in str(e["tag"]):
            return e, {eval(k): [[Fraction(z) for z in r] for r in v]
                       for k, v in e["point"].items()}
    return None, None


def main():
    t0 = time.time()
    KQ = A.Rat()

    # ---------------------------------------------------------------- G1
    cov = {}
    for m in (25, 26, 27, 28):
        for lab in A.VERTS:
            kind, v = A.vsplit(lab)
            n = len(A.admissible_cached(m, kind, v, False))
            cov["m%d|%s" % (m, lab)] = dict(
                n_admissible=n, frac_of_3pow7=round(n / 2187.0, 4),
                expected_hits_at_40=round(40 * n / 2187.0, 2),
                expected_hits_at_60=round(60 * n / 2187.0, 2),
                coverage_at_60=round(60 * n / 2187.0 / n, 5))
    OUT["G1_coverage"] = dict(
        table=cov,
        note="W26 draws nsample WORDS from 3^8 and keeps the admissible "
             "ones; the effective number of admissible index choices "
             "tested is nsample * n_admissible/2187, i.e. 40-60 * 11-38% "
             "= 4.5-23 of 243-823.  Coverage per index choice is "
             "nsample/2187 = 1.8-2.7%, independent of the vertex.",
        coverage_at_40=round(40 / 2187.0, 5),
        coverage_at_60=round(60 / 2187.0, 5),
        ok=True)
    OUT["_controls_run"].append("G1_coverage")
    print("G1 coverage: 40/2187=%.3f%%  60/2187=%.3f%%"
          % (4000 / 2187.0, 6000 / 2187.0), flush=True)
    ck()

    # ---------------------------------------------------------------- G2
    recs = []
    wrong_dir = 0
    rng = random.Random(7)
    pts = []
    d = json.load(open(os.path.join(W30DIR, "points_stored.json")))
    for e in d["points"]:
        if e.get("van"):
            continue
        pts.append((e["m"], str(e["tag"]),
                    {eval(k): [[Fraction(z) for z in r] for r in v]
                     for k, v in e["point"].items()}))
    for (m, tag, bl) in pts:
        okc, _ = A.is_clean_point(m, bl, KQ)
        ex = {l: A.vertex_verdict(m, bl, *A.vsplit(l), KQ)['DELIVERS']
              for l in A.VERTS}
        for ns, sd in ((40, 5), (60, 17), (60, 5)):
            sa = sampled_verdict(m, bl, KQ, ns, sd)
            dis = [l for l in A.VERTS if sa[l]['DELIVERS'] != ex[l]]
            bad = [l for l in dis if sa[l]['DELIVERS'] and not ex[l]]
            wrong_dir += len(bad)
            recs.append(dict(m=m, tag=tag, clean=okc, nsample=ns, seed=sd,
                             exhaustive_fails=[l for l in A.VERTS
                                               if not ex[l]],
                             sampled_fails=[l for l in A.VERTS
                                            if not sa[l]['DELIVERS']],
                             spurious_failures=[l for l in dis
                                                if not sa[l]['DELIVERS']],
                             impossible_direction=bad,
                             mean_admissible_sampled=round(
                                 sum(sa[l]['n_admissible_sampled']
                                     for l in A.VERTS) / 8.0, 2)))
        print("G2 m=%d %-28s clean=%s exh_fails=%s" %
              (m, tag[:28], okc, recs[-1]['exhaustive_fails']), flush=True)
        ck()
    nspur = sum(len(r['spurious_failures']) for r in recs)
    OUT["G2_sampled_vs_exhaustive"] = dict(
        records=recs, n_runs=len(recs),
        n_spurious_failures=nspur,
        n_impossible_direction=wrong_dir,
        ok=(wrong_dir == 0),
        note="a sampled run can only MISS deliveries; a sampled DELIVERS "
             "with exhaustive FAIL would be a logic error and must be 0")
    OUT["_controls_run"].append("G2_sampled_vs_exhaustive")
    ck()

    # ---------------------------------------------------------------- G3
    g3 = []
    for tagsub in ("W21break 777", "tensorZERO"):
        e, bl = load(tagsub, 28)
        if bl is None:
            g3.append(dict(tag=tagsub, found=False))
            continue
        okc, badw = A.is_clean_point(28, bl, KQ)
        allnz = A.all_gamma_cells_nonzero(28, bl, KQ)
        nz = A.n_words_phi_nonzero(28, bl, KQ)
        st = A.S(28)
        rec = dict(tag=str(e["tag"]), found=True, clean=okc,
                   n_clean_violations=len(badw), allnz=allnz,
                   n_words_phi_nonzero=nz)
        r = A.vertex_verdict(28, bl, 'L', 1, KQ, detail=True)
        rec['L1'] = dict(n_idx_total=r['n_idx_total'],
                         n_idx_live=r['n_idx_live'],
                         n_deliver=r['n_deliver'], DELIVERS=r['DELIVERS'])
        wit = None
        for (w, Tf, Tc) in r['detail']:
            for t in Tf:
                ww = list(w)
                ww[1] = t
                act = st.active_live(tuple(ww))
                ph = A.phi_raw(28, bl, tuple(ww), KQ)
                if len(act) == 1 and ph == 0:
                    ce = A.coeff_single(28, bl, act[0], tuple(ww), KQ)
                    if ce != 0:
                        wit = dict(word=list(ww), firing_letter=t,
                                   single=str(act[0]), phi=str(ph),
                                   c_e=str(ce))
                        break
            if wit:
                break
        rec['witness_pure_row'] = wit
        # what the sampled protocol says at this point
        for ns, sd in ((40, 5), (60, 17), (60, 5)):
            rec['sampled_%d_%d' % (ns, sd)] = sampled_verdict(
                28, bl, KQ, ns, sd)['L1']
        rec['fails_exhaustive'] = [
            l for l in A.VERTS
            if not A.vertex_verdict(28, bl, *A.vsplit(l), KQ)['DELIVERS']]
        g3.append(rec)
        print("G3 %-30s clean=%s L1 delivers=%s (%d/%d) witness=%s"
              % (tagsub, okc, rec['L1']['DELIVERS'], rec['L1']['n_deliver'],
                 rec['L1']['n_idx_live'], bool(wit)), flush=True)
        ck()
    OUT["G3_corrected_patterns"] = dict(
        records=g3,
        ok=all(x.get('found') and x['L1']['DELIVERS'] and
               x['witness_pure_row'] for x in g3))
    OUT["_controls_run"].append("G3_corrected_patterns")
    ck()

    # ---------------------------------------------------------------- G4
    e, bl = load("W21break 777", 28)
    sa = sampled_verdict(28, bl, KQ, 600, 99)
    OUT["G4_mutation"] = dict(
        note="the sampled engine is not stuck on FAIL: with a large "
             "sample it reports DELIVERS where the exhaustive engine does",
        sampled_600_fails=[l for l in A.VERTS if not sa[l]['DELIVERS']],
        exhaustive_fails=[l for l in A.VERTS
                          if not A.vertex_verdict(28, bl, *A.vsplit(l),
                                                  KQ)['DELIVERS']],
        ok=any(sa[l]['DELIVERS'] for l in A.VERTS))
    OUT["_controls_run"].append("G4_mutation")

    # ---------------------------------------------------------------- G5
    sa = sampled_verdict(28, bl, KQ, 20000, 3)
    ex = [l for l in A.VERTS
          if not A.vertex_verdict(28, bl, *A.vsplit(l), KQ)['DELIVERS']]
    sf = [l for l in A.VERTS if not sa[l]['DELIVERS']]
    OUT["G5_degenerate_agreement"] = dict(
        note="with a sample large enough to hit essentially every index "
             "choice the sampled verdict must converge to the exhaustive "
             "one",
        sampled_20000_fails=sf, exhaustive_fails=ex, ok=(sf == ex))
    OUT["_controls_run"].append("G5_degenerate_agreement")
    print("G5 sampled(20000)=%s exhaustive=%s" % (sf, ex), flush=True)

    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = missing == []
    OUT["_manifest_missing"] = missing
    OUT["elapsed_s"] = round(time.time() - t0, 1)
    OUT["done"] = True
    ck()
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("T3 DONE spurious=%d impossible=%d (%.0fs)"
          % (nspur, wrong_dir, time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
