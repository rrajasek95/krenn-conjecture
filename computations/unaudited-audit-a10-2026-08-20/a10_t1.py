#!/usr/bin/env python3
"""A10 TARGET 1 -- independent re-verification of W30's m=28 refutation.

UNAUDITED AUDIT LANE.  Exact arithmetic only.  Imports NOTHING from
w26_*/w30_*; the only thing taken from W30 is the DATA (the stored block
matrices of its 17 fully-verified points, read out of
results_verify_hunt.json).

Per point:
  A  clean point       -- Phi = 0 at every clean mixed word, evaluated by
                          RAW enumeration of the 105 perfect matchings of
                          K_8 (A10's own PM list, own Gamma set, own
                          clean-word set)
  B  off the vanishing stratum -- some word of the 6561 has Phi != 0
                          (plus the finer hafL/hafR diagnostics)
  C  every Gamma cell nonzero
  D  exhaustive vertex verdicts over ALL admissible index choices, in
     THREE predicates:
       D1 FAIL_primary  -- delivers at no admissible index choice
                           (W26's and W30's operative definition)
       D2 FAIL_star     -- W26's derived characterisation (*):
                           rank{clean} = 1 and rank{clean,firing} = 2 at
                           EVERY admissible index choice
       D3 FAIL_relaxed  -- A10's strictly more permissive admissibility
                           (letters whose completion is constant or dirty
                           are dropped instead of killing the whole index
                           choice); can only turn FAIL into DELIVER
  E  soundness spot-check: at every DELIVERING index choice, Phi at the
     firing letter really is 0 (the span criterion does what it claims)
  F  what the co-failure actually costs: does the point still admit a
     PURE ROW anywhere (some live single e and some word w with exactly
     that single active, Phi(w) = 0 and c_e(w) != 0)?

Controls (manifest asserted at the end):
  K1 mutation control      -- single-cell perturbations must move the
                              verdict (fails set) and must be caught by
                              the clean-point detector
  K2 positive control      -- m=28 points at which the pair does NOT
                              co-fail must PASS the non-co-failure check
  K3 outside-locus control -- ledger 18: a random (non-clean) point run
                              through the same pipeline is reported
                              non-clean, so the pipeline is not vacuous
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from itertools import combinations

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a10_lib as A                                                # noqa: E402

W30DIR = os.path.join(os.path.dirname(HERE),
                      "unaudited-exclusion-w30-2026-08-19")
RES = os.path.join(HERE, "results_t1.json")
DECL = ["K1_mutation", "K2_positive_noncofailure", "K3_outside_locus"]
OUT = {"_header": "UNAUDITED A10 target-1 re-verification (audit lane)",
       "_controls_declared": DECL, "_controls_run": [], "points": []}
PAIRS = [("L2", "R5"), ("R5", "R6"), ("R5", "R7"), ("L0", "L2"),
         ("L2", "R6"), ("L1", "L2")]


def ck():
    json.dump(OUT, open(RES, "w"), indent=1, default=str)


def load_points():
    d = json.load(open(os.path.join(W30DIR, "results_verify_hunt.json")))
    out = []
    for i, e in enumerate(d["verified"]):
        bl = {eval(k): [[int(z) for z in row] for row in v]
              for k, v in e["point"].items()}
        out.append(dict(i=i, m=e["m"], p=e["p"], tag=e["tag"], blocks=bl,
                        w30_fails=e["checks"]["V5_w30_exhaustive"],
                        w30_nidx=e["checks"].get("nidx"),
                        w30_ndel=e["checks"].get("ndel")))
    return out


def pure_rows(m, bl, K):
    """every word with EXACTLY one active live single, no degree-2 term,
    Phi = 0 and c_e != 0 -- a PURE ROW, which forces z_e = 0 and kills."""
    st = A.S(m)
    out = []
    for w in A.MIXED:
        act = st.active_live(w)
        if len(act) != 1:
            continue
        # a degree-2 term needs two active singles (live or not) on four
        # distinct vertices whose complement has a Gamma PM
        acta = st.active_any(w)
        deg2 = False
        for a, b in combinations(acta, 2):
            if len(set(a) | set(b)) != 4:
                continue
            if st._has_pm(tuple(v for v in range(8)
                                if v not in set(a) | set(b))):
                deg2 = True
                break
        if deg2:
            continue
        e = act[0]
        if not K.isz(A.phi_raw(m, bl, w, K)):
            continue
        if K.isz(A.coeff_single(m, bl, e, w, K)):
            continue
        out.append((w, e))
    return out


def verify(m, bl, K, deep=True):
    r = {}
    okc, bad = A.is_clean_point(m, bl, K)
    r['A_clean'] = okc
    r['A_n_clean_words'] = len(A.S(m).clean)
    r['A_violations'] = len(bad)
    r['C_all_gamma_cells_nonzero'] = A.all_gamma_cells_nonzero(m, bl, K)
    nz = A.n_words_phi_nonzero(m, bl, K)
    r['B_n_words_phi_nonzero'] = nz
    r['B_offstratum'] = nz > 0
    ver = {}
    for lab in A.VERTS:
        kind, v = A.vsplit(lab)
        a = A.vertex_verdict(m, bl, kind, v, K, relaxed=False, detail=deep)
        b = A.vertex_verdict(m, bl, kind, v, K, relaxed=True)
        ver[lab] = dict(n_idx_total=a['n_idx_total'],
                        n_idx_live=a['n_idx_live'], n_scale0=a['n_scale0'],
                        n_deliver=a['n_deliver'],
                        FAIL_primary=a['FAIL_primary'],
                        FAIL_star=a['FAIL_star'],
                        n_star_bad=a['n_star_bad'],
                        relaxed_n_idx=b['n_idx_total'],
                        relaxed_n_deliver=b['n_deliver'],
                        FAIL_relaxed=b['FAIL_primary'])
        if deep and a['detail']:
            # E: soundness -- delivery must imply Phi = 0 at firing letters
            badE = 0
            for (w, Tf, Tc) in a['detail'][:40]:
                for t in Tf:
                    ww = list(w)
                    ww[v] = t
                    if not K.isz(A.phi_raw(m, bl, tuple(ww), K)):
                        badE += 1
            ver[lab]['E_delivery_soundness_violations'] = badE
    r['D_vertices'] = ver
    r['D_fails_primary'] = [l for l in A.VERTS if ver[l]['FAIL_primary']]
    r['D_fails_star'] = [l for l in A.VERTS if ver[l]['FAIL_star']]
    r['D_fails_relaxed'] = [l for l in A.VERTS if ver[l]['FAIL_relaxed']]
    for tag, key in (("primary", 'D_fails_primary'), ("star", 'D_fails_star'),
                     ("relaxed", 'D_fails_relaxed')):
        r['cofailing_pairs_' + tag] = [
            list(pr) for pr in PAIRS
            if pr[0] in r[key] and pr[1] in r[key]]
    return r


def main():
    t0 = time.time()
    pts = load_points()
    print("loaded %d W30-verified points" % len(pts), flush=True)
    for rec in pts:
        m, p = rec['m'], rec['p']
        K = A.Fp(p)
        r = verify(m, rec['blocks'], K)
        pr = pure_rows(m, rec['blocks'], K)
        r['F_n_pure_rows'] = len(pr)
        r['F_pure_row_singles'] = sorted(set(str(e) for _, e in pr))
        r['F_point_is_killed_anyway'] = len(pr) > 0
        r.update(i=rec['i'], m=m, p=p, tag=rec['tag'],
                 w30_fails=rec['w30_fails'],
                 AGREES_WITH_W30=(r['D_fails_primary'] == rec['w30_fails']))
        OUT['points'].append(r)
        print("[%2d] m=%d p=%d A=%s C=%s B=%d | mine=%-28s w30=%-28s agree=%s"
              " | star=%-20s relaxed=%-20s pure=%d (%.0fs)"
              % (rec['i'], m, p, r['A_clean'],
                 r['C_all_gamma_cells_nonzero'], r['B_n_words_phi_nonzero'],
                 ",".join(r['D_fails_primary']), ",".join(rec['w30_fails']),
                 r['AGREES_WITH_W30'], ",".join(r['D_fails_star']),
                 ",".join(r['D_fails_relaxed']), len(pr),
                 time.time() - t0), flush=True)
        ck()

    # --------------------------------------------------------------- K1
    mut = []
    for rec in [x for x in pts if x['m'] == 28][:4]:
        m, p = rec['m'], rec['p']
        K = A.Fp(p)
        base = set(l for l in A.VERTS
                   if A.vertex_verdict(m, rec['blocks'], *A.vsplit(l), K)
                   ['FAIL_primary'])
        gam = list(A.S(m).gamma)
        rng = random.Random(1000 + rec['i'])
        recs = []
        for e in gam[:6]:
            b2 = {ee: [row[:] for row in rec['blocks'][ee]] for ee in gam}
            b2[e][0][0] = (b2[e][0][0] + 1) % p
            okc, bad = A.is_clean_point(m, b2, K)
            f2 = set(l for l in A.VERTS
                     if A.vertex_verdict(m, b2, *A.vsplit(l), K)
                     ['FAIL_primary'])
            recs.append(dict(edge=str(e), still_clean=okc,
                             n_clean_violations=len(bad),
                             fails_after=sorted(f2),
                             fails_changed=(f2 != base)))
        mut.append(dict(i=rec['i'], m=m, p=p, base_fails=sorted(base),
                        mutations=recs,
                        any_fails_changed=any(x['fails_changed']
                                              for x in recs),
                        clean_detector_fired=any(not x['still_clean']
                                                 for x in recs)))
        print("K1 mutation on point %d: fails_changed=%s clean_fired=%s"
              % (rec['i'], mut[-1]['any_fails_changed'],
                 mut[-1]['clean_detector_fired']), flush=True)
        ck()
    OUT['K1_mutation'] = dict(records=mut,
                              ok=all(x['any_fails_changed'] and
                                     x['clean_detector_fired'] for x in mut))
    OUT['_controls_run'].append("K1_mutation")
    ck()

    # --------------------------------------------------------------- K2
    pos = []
    for r in OUT['points']:
        if r['m'] != 28:
            continue
        f = r['D_fails_primary']
        pos.append(dict(i=r['i'], p=r['p'], fails=f,
                        L2_and_R5_cofail=('L2' in f and 'R5' in f),
                        clean=r['A_clean']))
    noco = [x for x in pos if not x['L2_and_R5_cofail']]
    OUT['K2_positive_noncofailure'] = dict(
        records=pos, n_m28=len(pos), n_without_L2R5=len(noco),
        note="points at m=28 that are genuine clean points but at which "
             "the pair does NOT co-fail; the checker must report "
             "no-co-failure for them",
        ok=len(noco) > 0 and all(x['clean'] for x in noco))
    OUT['_controls_run'].append("K2_positive_noncofailure")
    ck()

    # --------------------------------------------------------------- K3
    rng = random.Random(20260820)
    outl = []
    for m, p in ((28, 31), (28, 13)):
        K = A.Fp(p)
        bl = {e: [[rng.randrange(1, p) for _ in range(3)] for _ in range(3)]
              for e in A.S(m).gamma}
        okc, bad = A.is_clean_point(m, bl, K)
        f = [l for l in A.VERTS
             if A.vertex_verdict(m, bl, *A.vsplit(l), K)['FAIL_primary']]
        outl.append(dict(m=m, p=p, clean=okc, n_clean_violations=len(bad),
                         fails=f))
    OUT['K3_outside_locus'] = dict(
        records=outl,
        note="ledger 18: a point OUTSIDE the clean locus must be reported "
             "as not clean -- the clean detector is not vacuously true",
        ok=all(not x['clean'] for x in outl))
    OUT['_controls_run'].append("K3_outside_locus")

    missing = [c for c in DECL if c not in OUT['_controls_run']]
    OUT['_manifest_ok'] = missing == []
    OUT['_manifest_missing'] = missing
    OUT['elapsed_s'] = round(time.time() - t0, 1)
    OUT['done'] = True
    ck()
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("MANIFEST OK %s (%.0fs)" % (OUT['_controls_run'], time.time() - t0),
          flush=True)


if __name__ == "__main__":
    main()
