#!/usr/bin/env python3
"""A10 -- claim (c): the single W30-Y exception at m=28 / L2.

UNAUDITED AUDIT LANE.  Exact only, own engine.

W30 reports one apparent counterexample to the Q-span law and traces it
to the SCALE side condition.  A10 locates it independently (it is the
only failing vertex in results_qspan_hunt.json with
n_two_pair_with_Qspan_ge2 > 0: m=28 / F_13 / L2, tag
results_hunt_m28_13_r6.json|s1035) and re-verifies from scratch:

  X1  the point is a genuine clean, off-stratum, all-cells-nonzero point
  X2  L2 really FAILS exhaustively
  X3  there really are slice tuples with two clean pairs and Q-span >= 2
  X4  at EVERY such tuple, one of the two clean pairs has NO surviving
      index choice -- and the reason is hafR = 0 at all of them
  X5  control: at a tuple where both pairs DO survive, the Q-span is
      below threshold (so the law's hypothesis is genuinely unmet)
"""
from __future__ import annotations

import json
import os
import sys
from collections import defaultdict
from itertools import combinations, product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a10_lib as A                                                # noqa: E402
from a10_t2 import Sprime, Qvec, nbrs                              # noqa: E402
from a10_t4 import untriggered_by_tau                              # noqa: E402

W30DIR = os.path.join(os.path.dirname(HERE),
                      "unaudited-exclusion-w30-2026-08-19")
DECL = ["X1_point", "X2_fails", "X3_tuples", "X4_scale_explains",
        "X5_control"]
OUT = {"_header": "UNAUDITED A10: the m=28/L2 Q-span-law exception",
       "_controls_declared": DECL, "_controls_run": []}
RES = os.path.join(HERE, "results_t5.json")


def hafR(m, bl, y, K):
    st = A.S(m)

    def c(a, b):
        return A.cell(bl, st.gs, a, b, y[a - 4], y[b - 4], K)
    return K.add(K.add(K.mul(c(4, 5), c(6, 7)), K.mul(c(4, 6), c(5, 7))),
                 K.mul(c(4, 7), c(5, 6)))


def main():
    d = json.load(open(os.path.join(W30DIR, "points_hunt.json")))
    tgt = None
    for e in d["points"]:
        if e["m"] == 28 and e["p"] == 13 and "m28_13_r6" in str(e["tag"]):
            tgt = e
            break
    if tgt is None:
        OUT["error"] = "target point not found on disk"
        json.dump(OUT, open(RES, "w"), indent=1, default=str)
        print("TARGET POINT NOT FOUND")
        return
    m, p = 28, 13
    K = A.Fp(p)
    bl = {eval(k): [[int(z) for z in r] for r in v]
          for k, v in tgt["point"].items()}
    okc, badw = A.is_clean_point(m, bl, K)
    nz = A.n_words_phi_nonzero(m, bl, K)
    allnz = A.all_gamma_cells_nonzero(m, bl, K)
    OUT["X1_point"] = dict(tag=tgt["tag"], clean=okc,
                           n_clean_violations=len(badw),
                           n_words_phi_nonzero=nz, allnz=allnz,
                           ok=okc and allnz and nz > 0)
    OUT["_controls_run"].append("X1_point")
    print("X1 clean=%s nz=%d allnz=%s" % (okc, nz, allnz), flush=True)

    v = 2
    kind = 'L'
    ver = A.vertex_verdict(m, bl, kind, v, K)
    fails = [l for l in A.VERTS
             if not A.vertex_verdict(m, bl, *A.vsplit(l), K)['DELIVERS']]
    OUT["X2_fails"] = dict(L2_fails=ver['FAIL_primary'], all_fails=fails,
                           n_idx_total=ver['n_idx_total'],
                           n_idx_live=ver['n_idx_live'],
                           n_deliver=ver['n_deliver'],
                           ok=ver['FAIL_primary'])
    OUT["_controls_run"].append("X2_fails")
    print("X2 L2 FAIL=%s fails=%s" % (ver['FAIL_primary'], fails), flush=True)

    ns = nbrs(m, v)
    unt = untriggered_by_tau(m, v, ns)
    bytau = defaultdict(set)
    surv = defaultdict(set)
    words = defaultdict(lambda: defaultdict(list))
    for (w, Tf, Tc) in A.admissible_cached(m, kind, v, False):
        if len(Tf) != 1:
            continue
        tau = tuple(w[s] for s in ns)
        bytau[tau].add(Tf[0])
        words[tau][Tf[0]].append(w)
        if A.slice_rows(m, bl, kind, v, w, K) is not None:
            surv[tau].add(Tf[0])
    thr = len(ns) - 2
    tup = []
    for tau in sorted(bytau):
        Sp = Sprime(m, bl, v, tau, ns, K)
        Qs = [Qvec(m, bl, v, w, ns, K) for w in unt.get(tau, [])]
        Qs = [q for q in Qs if any(not K.isz(z) for z in q)]
        qd = A.rank(Qs, K) if Qs else 0
        tup.append(dict(tau=list(tau), n_letters=len(bytau[tau]),
                        n_surviving=len(surv.get(tau, ())),
                        Qspan=qd, rankS=A.rank(Sp, K),
                        bound_ok=A.rank(Sp, K) <= len(ns) - qd))
    hi = [x for x in tup if x['n_letters'] >= 2 and x['Qspan'] >= thr]
    hi_surv = [x for x in hi if x['n_surviving'] >= 2]
    OUT["X3_tuples"] = dict(nN=len(ns), threshold=thr, n_tuples=len(tup),
                            n_two_letter=sum(1 for x in tup
                                             if x['n_letters'] >= 2),
                            n_two_letter_Qspan_ge_thr=len(hi),
                            n_of_those_with_two_surviving=len(hi_surv),
                            bound_violations=sum(1 for x in tup
                                                 if not x['bound_ok']),
                            ok=len(hi) > 0)
    OUT["_controls_run"].append("X3_tuples")
    print("X3 two-letter tuples with Qspan>=%d: %d, of which both pairs "
          "survive: %d" % (thr, len(hi), len(hi_surv)), flush=True)

    # X4: WHY does the pair not survive?  hafR = 0 at every index choice
    diag = []
    for x in hi:
        tau = tuple(x['tau'])
        dead = [t for t in bytau[tau] if t not in surv.get(tau, ())]
        rec = dict(tau=list(tau), dead_letters=dead, letters=sorted(bytau[tau]))
        allh = []
        for t in dead:
            hz = all(K.isz(hafR(m, bl, list(w[4:]), K))
                     for w in words[tau][t])
            allh.append(hz)
        rec['every_choice_has_hafR_zero'] = all(allh) if allh else None
        diag.append(rec)
    OUT["X4_scale_explains"] = dict(
        records=diag[:12], n=len(diag),
        all_explained=(len(hi_surv) == 0 and
                       all(x['every_choice_has_hafR_zero'] for x in diag)),
        ok=(len(hi_surv) == 0 and
            all(x['every_choice_has_hafR_zero'] for x in diag)))
    OUT["_controls_run"].append("X4_scale_explains")
    print("X4 all high-Qspan tuples explained by hafR=0: %s"
          % OUT["X4_scale_explains"]["all_explained"], flush=True)

    both = [x for x in tup if x['n_surviving'] >= 2]
    OUT["X5_control"] = dict(
        n_tuples_with_two_surviving=len(both),
        max_Qspan_there=max([x['Qspan'] for x in both], default=-1),
        threshold=thr,
        note="the law's hypothesis needs BOTH pairs surviving AND "
             "Qspan >= threshold; here the two conditions are never "
             "simultaneously met, so the law is not violated",
        ok=all(x['Qspan'] < thr for x in both))
    OUT["_controls_run"].append("X5_control")
    print("X5 tuples with two surviving pairs: %d, max Qspan there = %d "
          "(threshold %d)" % (len(both), OUT["X5_control"]['max_Qspan_there'],
                              thr), flush=True)
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = missing == []
    OUT["done"] = True
    json.dump(OUT, open(RES, "w"), indent=1, default=str)
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("MANIFEST OK %s" % OUT["_controls_run"], flush=True)


if __name__ == "__main__":
    main()
