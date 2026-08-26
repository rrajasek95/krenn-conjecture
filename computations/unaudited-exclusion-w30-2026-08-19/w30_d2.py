#!/usr/bin/env python3
"""W30 D2 DIAGNOSIS on the escape objects.  UNAUDITED.  Exact.

A10's reframe: at every escape point the vertices STILL deliver, by a
mechanism W30-Y does not supply.  The diagnosis (results_diag28_ep2.json)
named it D2: rank S'(tau) = |N(v)| - 1 but ker phi meets the row space.

CLOSED FORM (derived here).  ROWS = phi(S') rowwise with
    phi(z) = z_0 * u  +  sc * (z_1, .., z_{|N|-1}),   sigma column FIRST,
    ker phi = <kappa>,  kappa = (sc, -u_1, ..., -u_{|N|-1}).
The cofactor identity gives rowspace(S') orthogonal to Q(w).  So when
rank S' = |N| - 1 and Q != 0, rowspace(S') = Q^perp EXACTLY, hence

    D2 fires   <=>   kappa in rowspace(S')   <=>   <kappa, Q(w)> = 0
               <=>   sc*Q_0  =  sum_{j>=1} u_j * Q_j                  (D2*)

with Q_0 the SIGMA-neighbour cofactor.  (D2*) is a scalar identity in the
blocks -- no rank test -- and it is exactly the vanishing of the master
relation's coefficient vector paired against Q.  This file TESTS (D2*)
against the observed D2 events, on the escape objects and on the m=28 / Q
object where R6 has slice rank 3 at all 81 tuples and still delivers.
"""
from __future__ import annotations
import json, os, sys
from fractions import Fraction as F
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path: sys.path.insert(0, _p)
import w30_lib as L, w30_qspan as QS, w26_core as C
DECL = ["D2a_closed_form_matches", "D2b_positive_control",
        "D2c_outside_locus_control"]

def sigma_first(m, v, kind):
    """the neighbour order used by w30_lib.slice_data: the sigma column
    FIRST (phi's z_0), then the cross columns in the engine's own q-order.
    Absent edges are kept as placeholders and dropped from the pairing."""
    if kind == 'R':
        p = C.SIGINV[v]
        return [p] + [C.SIG[q] for q in range(4) if q != p]
    p = v
    return [C.SIG[p]] + [a for a in range(4) if a != p]

def analyse(m, bl, lab, K, cap=400):
    kind, v = L.vkey(lab)
    ns = sigma_first(m, v, kind)
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    zero, one = K.n(0), K.n(1)
    G = L.geom(m); sing, lv = G['sing'], G['lv']
    out = dict(n_D2=0, n_D2_pred=0, n_agree=0, n_checked=0, samples=[])
    for (w, fire) in L.index_choices_cached(m, kind, v):
        if len(fire) != 1: continue
        sd = L.slice_data(m, bl, kind, v, w, K)
        if sd is None: continue
        d, uu, MM, sc = sd
        rows = [[d[t]*uu[j] + sc*MM[t][j] for j in range(3)] for t in range(3)]
        tau = tuple(w[s] for s in ns)
        S = [[d[t]] + [MM[t][j] for j in range(3)] for t in range(3)]
        rS = L.rank_rows(S, K)
        nreal = len([j for j, s in enumerate(ns)
                     if (min(s, v), max(s, v)) in gs])
        ct = [t for t in range(3) if t not in fire]
        rphi = L.rank_rows(rows, K)
        rphic = L.rank_rows([rows[t] for t in ct], K)
        deliv = all(L.rank_rows([rows[t] for t in ct]+[rows[t2]], K) == rphic
                    for t2 in fire)
        isD2 = deliv and rphi < rS
        # (D2*) prediction: <kappa, Q(w)> = 0 for a Q at this tuple
        real = [j for j, s in enumerate(ns)
                if (min(s, v), max(s, v)) in gs]
        Q = [(C.haf_on(bl, gs, tuple(z for z in range(8)
                                     if z not in (v, ns[j])), w, zero, one)
              if j in real else K.n(0)) for j in range(len(ns))]
        kap = [sc] + [K.n(0) - x for x in uu]
        ip = sum((kap[j] * Q[j] for j in real), K.n(0))
        pred = K.iszero(ip) and any(not K.iszero(Q[j]) for j in real)
        out['n_checked'] += 1
        if isD2: out['n_D2'] += 1
        if pred: out['n_D2_pred'] += 1
        if isD2 == pred: out['n_agree'] += 1
        elif len(out['samples']) < 6:
            out['samples'].append(dict(tau=list(tau), rank_S=rS, rank_phi=rphi,
                                       observed_D2=isD2, predicted=pred,
                                       Q_nonzero=any(not K.iszero(q) for q in Q)))
        if out['n_checked'] >= cap: break
    out['agreement'] = (out['n_agree'], out['n_checked'])
    return out

def main():
    res = os.path.join(HERE, "results_d2.json")
    OUT = {"_header": "UNAUDITED W30 D2 closed-form diagnosis",
           "_controls_declared": DECL, "_controls_run": [], "objects": []}
    jobs = []
    # A10's m=25 / Q realisation-failure point
    d = json.load(open(os.path.join(HERE, "points_m25_wide.json")))
    for r in d["points"]:
        if r["seed"] == 925024:
            jobs.append(("A10_m25_Q_925024", 25, 0, r["point"], ["R6","R5","L2"]))
    # W30's m=27 / F_13 escape-cover object
    ev = json.load(open(os.path.join(HERE, "results_escverify.json")))
    for o in ev["objects"]:
        jobs.append(("W30_m27_F13_escape", o["m"], o["p"], o["point"],
                     ["R5","R6","L1","L2"]))
    # the m=28 / Q object with R6 slice rank 3 everywhere
    rr = json.load(open(os.path.join(HERE, "results_r6rank_Q_R6.json")))
    if rr.get("best"):
        jobs.append(("W30_m28_Q_R6rank3", 28, 0, rr["best"]["point"],
                     ["R6","R5","L1","L2"]))
    tot_ag = tot_n = 0
    for (tag, m, p, ptj, labs) in jobs:
        K = L.QF if not p else L.FP(p)
        bl = ({eval(k): [[int(z) % p for z in row] for row in v]
               for k, v in ptj.items()} if p else
              {eval(k): [[F(z) for z in row] for row in v]
               for k, v in ptj.items()})
        rec = dict(tag=tag, m=m, p=p, vert={})
        for lab in labs:
            a = analyse(m, bl, lab, K)
            rec["vert"][lab] = a
            tot_ag += a['n_agree']; tot_n += a['n_checked']
        OUT["objects"].append(rec)
        json.dump(OUT, open(res, "w"), indent=1, default=str)
        print("%-24s m=%d p=%d  %s" % (tag, m, p,
              {l: (rec["vert"][l]['n_D2'], rec["vert"][l]['n_D2_pred'],
                   rec["vert"][l]['agreement']) for l in labs}), flush=True)
    OUT["D2a_closed_form_matches"] = dict(
        agree=tot_ag, checked=tot_n, ok=(tot_ag == tot_n),
        note="(D2*) <kappa,Q> = 0 must agree with the observed D2 events")
    OUT["_controls_run"].append("D2a_closed_form_matches")
    OUT["D2b_positive_control"] = dict(
        ok=any(r["vert"][l]['n_D2'] > 0 for r in OUT["objects"]
               for l in r["vert"]),
        note="at least one genuine D2 event must occur, else the test is vacuous")
    OUT["_controls_run"].append("D2b_positive_control")
    OUT["D2c_outside_locus_control"] = dict(
        ok=any(r["vert"][l]['n_D2'] < r["vert"][l]['n_checked']
               for r in OUT["objects"] for l in r["vert"]),
        note="D2 must NOT fire everywhere, else (D2*) is trivially true")
    OUT["_controls_run"].append("D2c_outside_locus_control")
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == []); OUT["done"] = True
    json.dump(OUT, open(res, "w"), indent=1, default=str)
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("D2 closed form agrees %d/%d ; manifest %s"
          % (tot_ag, tot_n, OUT["_controls_run"]), flush=True)
if __name__ == "__main__": main()
