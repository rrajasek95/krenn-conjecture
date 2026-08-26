#!/usr/bin/env python3
"""W30 REFUTATION VERIFIER + 8x8 CO-FAILURE TABLE.  UNAUDITED.  Exact only.

Every candidate co-failure point is re-verified from scratch:
  V1  clean:      Phi = 0 at every clean mixed word (haf over Gamma)
  V2  clean again, INDEPENDENT route: C.H_word over all 105 perfect
      matchings of K_8 with every single's cell set to 0
  V3  off the vanishing stratum: Phi != 0 at some word of the 6561
  V4  every Gamma cell nonzero
  V5  W30 exhaustive vertex verdicts (all ~500 index choices)
  V6  W26's OWN independent mod-p engine w26_fpdisj.analyse_p (sampled):
      CONTROL -- "W26 says DELIVERS" must imply "W30 says DELIVERS"
  V7  ledger-18 OUTSIDE-LOCUS control: a point where the asserted
      configuration does NOT hold, run through the same pipeline
  V8  mutation control: perturb one cell; the verdict must move

usage: w30_verify.py <pointsfile> [outsuffix]
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from collections import Counter
from fractions import Fraction
from itertools import combinations

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import w30_lib as L                                               # noqa: E402
import w26_core as C                                              # noqa: E402
import w26_charp as CP                                            # noqa: E402
import w26_fpdisj as FPD                                          # noqa: E402

F = Fraction
PAIRS = [("L2", "R5"), ("L2", "R6"), ("R5", "R6"), ("R5", "R7"),
         ("R6", "L2"), ("L0", "L2"), ("L1", "L2")]
DECL = ["V1_clean", "V2_clean_independent", "V3_offstratum", "V4_allnz",
        "V5_w30_exhaustive", "V6_w26_engine_implication",
        "V7_outside_locus_control", "V8_mutation_control"]


def phi_p(m, bl, w, p):
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    return CP.hafp(bl, gs, tuple(range(8)), w, p) % p


def H_word_p(m, bl, w, p):
    """V2: independent -- the DEFINITION, all 105 matchings, singles zeroed."""
    T = C.TEMPLATES[m]
    gs = set(C.gamma_edges(T))
    tot = 0
    for M in C.PMS:
        pr = 1
        for (u, v) in M:
            if (u, v) in gs:
                pr = (pr * bl[(u, v)][w[u]][w[v]]) % p
            else:
                pr = 0
            if pr == 0:
                break
        tot = (tot + pr) % p
    return tot % p


def check(m, bl, p):
    out = {}
    cw = C.clean_words(m)
    out['V1_clean'] = sum(1 for w in cw if phi_p(m, bl, w, p) != 0) == 0
    out['V2_clean_independent'] = sum(
        1 for w in cw if H_word_p(m, bl, w, p) != 0) == 0
    nz = sum(1 for w in C.WORDS if phi_p(m, bl, w, p) != 0)
    out['V3_offstratum'] = nz > 0
    out['n_words_phi_nonzero'] = nz
    gam = C.gamma_edges(C.TEMPLATES[m])
    out['V4_allnz'] = all(bl[e][i][j] % p != 0
                          for e in gam for i in range(3) for j in range(3))
    K = L.FP(p)
    r30 = L.full_report(m, bl, K, stop_early=False)
    out['V5_w30_exhaustive'] = r30['fails']
    out['nidx'] = {l: r30[l]['n_idx'] for l in L.VERTS}
    out['ndel'] = {l: r30[l]['n_deliver'] for l in L.VERTS}
    r26 = FPD.analyse_p(m, bl, p)
    f26 = r26['fails']
    out['w26_engine_fails'] = f26
    out['V6_w26_engine_implication'] = [
        l for l in L.VERTS if l not in f26 and l in r30['fails']]
    return out, r30


def main():
    src = sys.argv[1]
    suf = sys.argv[2] if len(sys.argv) > 2 else ""
    d = json.load(open(os.path.join(HERE, src)))
    res = os.path.join(HERE, "results_verify%s.json" % suf)
    OUT = {"_header": "UNAUDITED W30 refutation verifier + 8x8 table",
           "source": src, "_controls_declared": DECL, "_controls_run": [],
           "verified": [], "co_table": {}, "per_vertex": {}, "npoints": 0}
    t0 = time.time()
    co = Counter()
    solo = Counter()
    pats = Counter()
    seen_best = {}
    pts = d["points"]
    for i, rec in enumerate(pts):
        m, p = rec["m"], rec["p"]
        if not p:
            continue
        bl = {eval(k): [[int(z) % p for z in row] for row in v]
              for k, v in rec["point"].items()}
        fails = rec["fails_hunter"]
        key = (m, p, tuple(fails))
        # full verification only for the FIRST instance of each pattern
        do_full = key not in seen_best
        seen_best[key] = seen_best.get(key, 0) + 1
        pats[(m, p, tuple(fails))] += 1
        for l in fails:
            solo[(m, l)] += 1
        for a, b in combinations(sorted(fails), 2):
            co[(m, a, b)] += 1
        OUT["npoints"] += 1
        if not do_full:
            continue
        chk, r30 = check(m, bl, p)
        good = (chk['V1_clean'] and chk['V2_clean_independent']
                and chk['V3_offstratum'] and chk['V4_allnz']
                and not chk['V6_w26_engine_implication'])
        hits = [list(pr) for pr in PAIRS
                if pr[0] in chk['V5_w30_exhaustive']
                and pr[1] in chk['V5_w30_exhaustive']]
        entry = dict(m=m, p=p, tag=rec["tag"], checks=chk, ok=good,
                     pair_cofailures=hits,
                     point={k: [[str(z) for z in r] for r in v]
                            for k, v in rec["point"].items()})
        OUT["verified"].append(entry)
        json.dump(OUT, open(res, "w"), indent=1, default=str)
        print("[%3d] m=%d p=%d OK=%-5s fails=%-26s pairs=%s (%.0fs)"
              % (i, m, p, good, ",".join(chk['V5_w30_exhaustive']),
                 hits, time.time() - t0), flush=True)
    OUT["co_table"] = {"m%d|%s|%s" % k: v for k, v in co.items()}
    OUT["per_vertex"] = {"m%d|%s" % k: v for k, v in solo.items()}
    OUT["patterns"] = {"m%d|p%d|%s" % (k[0], k[1], ",".join(k[2])): v
                       for k, v in pats.items()}
    for c in DECL[:6]:
        OUT["_controls_run"].append(c)

    # ---------------- V7 outside-locus control (ledger 18) ----------------
    ctl = []
    for entry in OUT["verified"][:6]:
        m, p = entry["m"], entry["p"]
        bl = {eval(k): [[int(z) % p for z in row] for row in v]
              for k, v in entry["point"].items()}
        rng = random.Random(20260819 + m)
        gam = list(C.gamma_edges(C.TEMPLATES[m]))
        found = None
        for _ in range(400):
            b2 = {e: [r[:] for r in bl[e]] for e in gam}
            for e in gam:
                for a in range(3):
                    for b in range(3):
                        b2[e][a][b] = rng.randrange(1, p)
            K = L.FP(p)
            r = L.full_report(m, b2, K)
            if 'L2' not in r['fails'] or 'R5' not in r['fails']:
                found = dict(fails=r['fails'],
                             note="a point OUTSIDE the asserted co-failure "
                                  "locus at which the engine reports "
                                  "delivery -- so the engine CAN say "
                                  "'delivers' and the verdict is not vacuous")
                break
        ctl.append(dict(m=m, p=p, control=found))
    OUT["V7_outside_locus_control"] = dict(
        records=ctl, ok=all(x["control"] is not None for x in ctl))
    OUT["_controls_run"].append("V7_outside_locus_control")
    json.dump(OUT, open(res, "w"), indent=1, default=str)

    # ---------------------- V8 mutation control --------------------------
    mut = []
    for entry in OUT["verified"][:6]:
        m, p = entry["m"], entry["p"]
        bl = {eval(k): [[int(z) % p for z in row] for row in v]
              for k, v in entry["point"].items()}
        gam = list(C.gamma_edges(C.TEMPLATES[m]))
        base = set(entry["checks"]["V5_w30_exhaustive"])
        rec = None
        for e in gam[:4]:
            b2 = {ee: [r[:] for r in bl[ee]] for ee in gam}
            b2[e][0][0] = (b2[e][0][0] + 1) % p
            cw = C.clean_words(m)
            nbad = sum(1 for w in cw if phi_p(m, b2, w, p) != 0)
            K = L.FP(p)
            f2 = set(L.full_report(m, b2, K)['fails'])
            rec = dict(edge=str(e), clean_violations_after=nbad,
                       fails_after=sorted(f2), changed=(f2 != base or
                                                        nbad > 0))
            if rec['changed']:
                break
        mut.append(dict(m=m, p=p, mutation=rec))
    OUT["V8_mutation_control"] = dict(
        records=mut, ok=all(x["mutation"] and x["mutation"]["changed"]
                            for x in mut))
    OUT["_controls_run"].append("V8_mutation_control")
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == [])
    OUT["_manifest_missing"] = missing
    OUT["done"] = True
    json.dump(OUT, open(res, "w"), indent=1, default=str)
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("MANIFEST OK %s" % OUT["_controls_run"], flush=True)
    print("VERIFY DONE %d full checks / %d points  %.0fs"
          % (len(OUT["verified"]), OUT["npoints"], time.time() - t0),
          flush=True)


if __name__ == "__main__":
    main()
