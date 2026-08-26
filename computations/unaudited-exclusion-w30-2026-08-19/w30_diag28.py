#!/usr/bin/env python3
"""W30 m=28 BLOCKED-STEP DIAGNOSIS.  UNAUDITED.  Exact only.

The Q-span hunters drove Theorem W30-Y's hypothesis to ZERO simultaneously
for {L1,L2} and for {R5,R6} at m=28 -- and NEITHER vertex failed.  So a
SECOND mechanism protects those points.  This file finds it.

At every delivering index choice of the target vertex we record which step
of the failure definition breaks:

  D0  no admissible index choice at all (vacuous failure)  -- n_idx = 0
  D1  rank S(tau) <= 2 anyway, i.e. the slice matrix is degenerate for a
      reason OTHER than the cofactor bound (Q-span < |N| - 2).  THIS is the
      candidate second mechanism: something else makes S drop rank.
  D2  rank S(tau) = 3 but the clean rows already have rank 2 and phi kills
      the difference -- delivery through the kernel kappa of phi rather
      than through S.
  D3  letter collapse happened but the firing row is INSIDE the collapsed
      line (rank of all three rows equals the clean rank).

Recall ROWS = phi(S) with phi(z) = z_0 u + sc*(z_1,z_2,z_3) and
ker phi = <kappa>, kappa = (sc, -u_1, -u_2, -u_3).  Delivery is
rank phi(S) = rank phi(S|clean), which can hold with rank S = 3 when kappa
meets the row space -- that is D2, and it is TRIGGER-DEPENDENT.

usage: w30_diag28.py <outsuffix>
"""
from __future__ import annotations

import glob
import json
import os
import sys
import time
from collections import Counter, defaultdict
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import w30_lib as L                                               # noqa: E402
import w30_qspan as QS                                            # noqa: E402
import w30_qhunt as QH                                            # noqa: E402
import w26_core as C                                              # noqa: E402

F = Fraction
DECL = ["G1_endpoint_hypothesis_is_zero", "G2_step_classification_total",
        "G3_outside_locus_control"]


def qdim_map(m, bl, lab, K):
    """Q-span dimension at EVERY slice tuple (not only two-pair ones)."""
    v, ns, unt, _two = QH.tuple_data(m, lab)
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    zero, one = K.n(0), K.n(1)
    out = {}
    for tau, ws in unt.items():
        Qs = []
        for w in ws:
            Q = [C.haf_on(bl, gs, tuple(z for z in range(8)
                                        if z not in (v, s)), w, zero, one)
                 for s in ns]
            if any(not K.iszero(z) for z in Q):
                Qs.append(Q)
        out[tau] = L.rank_rows(Qs, K) if Qs else 0
    return out


def diagnose(m, bl, lab, K):
    kind, v = L.vkey(lab)
    ns = QS.nbrs(m, v)
    qmap = qdim_map(m, bl, lab, K)
    npairs = defaultdict(set)
    for (w2, fr2) in L.index_choices_cached(m, kind, v):
        if len(fr2) == 1:
            npairs[tuple(w2[s] for s in ns)].add(
                tuple(sorted(t for t in range(3) if t not in fr2)))
    idx = L.index_choices_cached(m, kind, v)
    cls = Counter()
    detail = []
    n_idx = 0
    for (w, fire) in idx:
        sd = L.slice_data(m, bl, kind, v, w, K)
        if sd is None:
            cls['zero_scale'] += 1
            continue
        n_idx += 1
        d, uu, MM, sc = sd
        rows = [[d[t] * uu[j] + sc * MM[t][j] for j in range(3)]
                for t in range(3)]
        tau = tuple(w[s] for s in ns)
        S = QS.slice_S(m, bl, v, tau, ns)
        rS = L.rank_rows(S, K)
        clean_ts = [t for t in range(3) if t not in fire]
        rSc = L.rank_rows([S[t] for t in clean_ts], K)
        rphi = L.rank_rows(rows, K)
        rphic = L.rank_rows([rows[t] for t in clean_ts], K)
        deliv = all(L.rank_rows([rows[t] for t in clean_ts] + [rows[t2]], K)
                    == rphic for t2 in fire)
        if not deliv:
            cls['NON_DELIVER'] += 1
            continue
        qd = qmap.get(tau, 0)
        npr = len(npairs.get(tau, ()))
        if rS <= 2 and rSc == rS:
            if qd >= len(ns) - 2:
                cls['D1a_same_mechanism_qspan_ok_npairs%d' % npr] += 1
            else:
                cls['D1b_NEW_rank_drop_qspan%d' % qd] += 1
        elif rS == 3 and rphi < 3:
            cls['D2_phi_kernel_meets_rowspace'] += 1
        elif rphic <= 1 and rphi == rphic:
            cls['D3_firing_row_inside_line'] += 1
        else:
            cls['D4_other'] += 1
        if len(detail) < 6:
            detail.append(dict(tau=list(tau), fire=sorted(fire),
                               rank_S=rS, rank_S_clean=rSc,
                               rank_phiS=rphi, rank_phiS_clean=rphic))
    return dict(vertex=lab, nN=len(ns), n_idx=n_idx,
                classes=dict(cls), sample=detail)


def main():
    suf = sys.argv[1] if len(sys.argv) > 1 else ""
    res = os.path.join(HERE, "results_diag28%s.json" % suf)
    OUT = {"_header": "UNAUDITED W30 m=28 blocked-step diagnosis",
           "_controls_declared": DECL, "_controls_run": [], "endpoints": []}
    t0 = time.time()
    agg = Counter()
    nz = 0
    for f in sorted(glob.glob(os.path.join(HERE, "results_qhunt_m28_*.json"))):
        d = json.load(open(f))
        b = d.get("best")
        if not b:
            continue
        p = 0 if d["field"] == 'Q' else int(d["field"])
        K = L.QF if p == 0 else L.FP(p)
        if p:
            bl = {eval(k): [[int(z) % p for z in row] for row in v]
                  for k, v in b["point"].items()}
        else:
            bl = {eval(k): [[F(z) for z in row] for row in v]
                  for k, v in b["point"].items()}
        rec = dict(source=os.path.basename(f), field=d["field"],
                   targets=d["targets"], qspan_total=b.get("qspan_total"),
                   per_target=b.get("per_target"), fails=b.get("fails"),
                   diag={})
        for lab in d["targets"]:
            if b.get("per_target", {}).get(lab, 1) != 0:
                continue          # only endpoints where the hypothesis is 0
            nz += 1
            dg = diagnose(28, bl, lab, K)
            rec["diag"][lab] = dg
            for k, v2 in dg["classes"].items():
                agg[k] += v2
        if rec["diag"]:
            OUT["endpoints"].append(rec)
            json.dump(OUT, open(res, "w"), indent=1, default=str)
            print("%-40s targets=%s per_target=%s fails=%s"
                  % (rec["source"][:40], d["targets"], rec["per_target"],
                     ",".join(rec["fails"]) or "-"), flush=True)
            for lab, dg in rec["diag"].items():
                print("     %-3s |N|=%d n_idx=%-4d %s"
                      % (lab, dg["nN"], dg["n_idx"], dg["classes"]),
                      flush=True)
    OUT["aggregate_classes"] = dict(agg)
    OUT["G1_endpoint_hypothesis_is_zero"] = dict(
        n_vertices_diagnosed=nz, ok=nz > 0,
        note="only vertices whose W30-Y hypothesis count is 0 are diagnosed")
    OUT["_controls_run"].append("G1_endpoint_hypothesis_is_zero")
    tot = sum(agg.values())
    OUT["G2_step_classification_total"] = dict(
        total=tot, unclassified=agg.get("D4_other", 0),
        ok=(agg.get("D4_other", 0) == 0),
        note="every delivering index choice must fall in D1/D2/D3")
    OUT["_controls_run"].append("G2_step_classification_total")
    # ledger 18: a point OUTSIDE the asserted locus -- a genuine m=28
    # co-failure point, where the vertex DOES fail -- must classify as
    # NON_DELIVER throughout, else the classifier is vacuous.
    ctl = None
    hp = os.path.join(HERE, "points_hunt.json")
    if os.path.exists(hp):
        dd = json.load(open(hp))
        for r in dd["points"]:
            if r["m"] != 28 or not r["p"]:
                continue
            if "L2" not in r["fails_hunter"] or "R5" not in r["fails_hunter"]:
                continue
            p = r["p"]
            bl = {eval(k): [[int(z) % p for z in row] for row in v]
                  for k, v in r["point"].items()}
            dg = diagnose(28, bl, "L2", L.FP(p))
            ctl = dict(tag=r["tag"][:40], classes=dg["classes"],
                       only_nondeliver=(set(dg["classes"]) <=
                                        {"NON_DELIVER", "zero_scale"}),
                       note="a verified co-failure point: L2 must show NO "
                            "delivering index choice")
            break
    OUT["G3_outside_locus_control"] = ctl or dict(ok=False, note="not run")
    if ctl:
        OUT["G3_outside_locus_control"]["ok"] = ctl["only_nondeliver"]
    OUT["_controls_run"].append("G3_outside_locus_control")
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == [])
    OUT["done"] = True
    json.dump(OUT, open(res, "w"), indent=1, default=str)
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("AGGREGATE:", dict(agg), flush=True)
    print("G3 outside-locus control:", ctl, flush=True)
    print("DIAG DONE %.0fs" % (time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
