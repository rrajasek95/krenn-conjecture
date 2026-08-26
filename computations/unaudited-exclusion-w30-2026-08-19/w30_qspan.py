#!/usr/bin/env python3
"""W30 THE Q-SPAN MECHANISM -- the uniform (all-m) form of Theorem W30-X.
UNAUDITED.  Exact only.

At any vertex v, ROWS = d u^T + sc*M = phi(S) rowwise, where S is the
3 x |N(v)| trigger-free SLICE matrix and phi : k^{|N|} -> k^3 is

        phi(z) = z_0 * u  +  sc * (z_1,...,z_{|N|-1})       (sigma column
                                                             first).

* |N(v)| = 3 (m <= 27 at the protected vertices): phi is an ISOMORPHISM when
  sc != 0 and u_{q0} != 0, so delivery <=> rank S = rank S|clean.
* |N(v)| = 4 (every vertex at m = 28): phi has a ONE-DIMENSIONAL kernel
        kappa = (sc, -u_1, -u_2, -u_3),
  which MOVES with the triggers.  That is exactly why m=28 has no protected
  vertex.

THE COFACTOR IDENTITY, uniform form.  Phi is multilinear, so
        Phi(w with letter t at v) = < S(tau) row t , Q(w) >,
        Q(w)_j = haf_{Gamma - {v,s_j}}(w).
If all three letters at v give clean words, S(tau) Q(w) = 0, i.e. Q(w) lies
in the RIGHT KERNEL of S(tau).  Hence

    dim span{ Q(w) : w untriggered with slice tuple tau }  >=  r
                        ==>   rank S(tau)  <=  |N(v)| - r.               (*)

At |N| = 4 a Q-span of dimension >= 2 forces rank S(tau) <= 2, which is
exactly the m<=27 situation -- and then a vertex with TWO firing letters
cannot fail (both clean pairs collapse => rank S <= 1 => contradiction).

So the m=28 DISJUNCTION reduces to: at some two-firing-letter vertex
(R5, R6, L1, L2) some two-pair slice tuple has Q-span dimension >= 2.

This file measures the Q-span dimension at every slice tuple of every
vertex, on every point on disk, and correlates it with the observed
failures.  A FAILING two-firing-letter vertex with a Q-span >= 2 at a
two-pair tuple would REFUTE the mechanism (and is checked for explicitly).

usage: w30_qspan.py <pointsfile> [outsuffix]
"""
from __future__ import annotations

import json
import os
import sys
import time
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import w30_lib as L                                               # noqa: E402
import w26_core as C                                              # noqa: E402

F = Fraction
TWO_LETTER = {25: ['R6', 'L2'], 26: ['R5', 'R6', 'L1', 'L2'],
              27: ['R5', 'R6', 'L1', 'L2'], 28: ['R5', 'R6', 'L1', 'L2']}


def nbrs(m, v):
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    return sorted(s for s in range(8) if (min(s, v), max(s, v)) in gs)


def slice_S(m, bl, v, tau, ns):
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    out = []
    for t in range(3):
        row = []
        for j, s in enumerate(ns):
            e = (min(s, v), max(s, v))
            row.append(bl[e][t][tau[j]] if e[0] == v else bl[e][tau[j]][t])
        out.append(row)
    return out


def analyse(m, bl, lab, K):
    kind, v = L.vkey(lab)
    ns = nbrs(m, v)
    G = L.geom(m)
    sing, lv = G['sing'], G['lv']
    gs = G['gs']
    zero, one = K.n(0), K.n(1)
    # untriggered words grouped by slice tuple
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
            if len(set(ww)) == 1:
                ok = False
                break
            if any(ww[f[0]] == sing[f][0] and ww[f[1]] == sing[f][1]
                   for f in lv):
                ok = False
                break
        if ok:
            unt[tuple(w[s] for s in ns)].append(tuple(w))
    # index choices grouped by slice tuple -> which clean pairs
    bytau = defaultdict(set)
    for (w, fire) in L.index_choices_cached(m, kind, v):
        if len(fire) != 1:
            continue
        bytau[tuple(w[s] for s in ns)].add(
            tuple(sorted(t for t in range(3) if t not in fire)))
    # which (tau,pair) actually have a SURVIVING index choice (scale != 0)
    surv = defaultdict(dict)
    for (w, fire) in L.index_choices_cached(m, kind, v):
        if len(fire) != 1:
            continue
        tau = tuple(w[s] for s in ns)
        P = tuple(sorted(t for t in range(3) if t not in fire))
        if L.slice_data(m, bl, kind, v, w, K) is not None:
            surv[tau][P] = True
    recs = []
    for tau, pairs in bytau.items():
        Qs = []
        for w in unt.get(tau, []):
            Q = [C.haf_on(bl, gs, tuple(z for z in range(8)
                                        if z not in (v, s)), w, zero, one)
                 for s in ns]
            if any(not K.iszero(z) for z in Q):
                Qs.append(Q)
        qdim = L.rank_rows(Qs, K) if Qs else 0
        S = slice_S(m, bl, v, tau, ns)
        n_surv_pairs = len(surv.get(tau, {}))
        recs.append(dict(tau=list(tau), n_pairs=len(pairs),
                         n_surviving_pairs=n_surv_pairs,
                         n_untriggered=len(unt.get(tau, [])),
                         n_Q_nonzero=len(Qs), Qspan=qdim,
                         rankS=L.rank_rows(S, K),
                         bound_ok=(L.rank_rows(S, K) <= len(ns) - qdim)))
    r = L.vertex_report(m, bl, kind, v, K, stop_early=False)
    # THE LAW's hypothesis: two-pair tuple, BOTH pairs surviving, and
    # Q-span >= |N(v)| - 2.
    two_pair = [x for x in recs
                if x['n_pairs'] >= 2 and x['n_surviving_pairs'] >= 2]
    return dict(vertex=lab, nN=len(ns),
                DELIVERS=r['DELIVERS'], n_idx=r['n_idx'],
                n_two_pair=len(two_pair),
                max_Qspan_on_two_pair=max([x['Qspan'] for x in two_pair],
                                          default=0),
                n_two_pair_with_Qspan_ge2=sum(1 for x in two_pair
                                              if x['Qspan'] >= len(ns) - 2),
                threshold=len(ns) - 2,
                bound_violations=sum(1 for x in recs if not x['bound_ok']),
                tuples=recs)


def main():
    src = sys.argv[1]
    suf = sys.argv[2] if len(sys.argv) > 2 else ""
    d = json.load(open(os.path.join(HERE, src)))
    res = os.path.join(HERE, "results_qspan%s.json" % suf)
    OUT = {"_header": "UNAUDITED W30 Q-span mechanism",
           "source": src,
           "_controls_declared": ["Q1_kernel_bound", "Q2_mechanism_test",
                                  "Q3_refutation_scan"],
           "_controls_run": [], "recs": []}
    t0 = time.time()
    nviol = nrefute = 0
    refutations = []
    for i, rec in enumerate(d["points"]):
        if rec.get("van"):
            continue
        m = rec.get("m") or d.get("m")
        pp = int(rec.get("p") or d.get("p") or 0)
        if pp:
            bl = {eval(k): [[int(z) % pp for z in row] for row in v]
                  for k, v in rec["point"].items()}
            K = L.FP(pp)
        else:
            bl = {eval(k): [[F(z) for z in row] for row in v]
                  for k, v in rec["point"].items()}
            K = L.QF
        out = dict(m=m, p=pp, tag=str(rec.get("tag", i))[:44], vert={})
        for lab in TWO_LETTER.get(m, []):
            a = analyse(m, bl, lab, K)
            out["vert"][lab] = {k: v2 for k, v2 in a.items() if k != "tuples"}
            nviol += a["bound_violations"]
            # THE REFUTATION TEST: a FAILING two-letter vertex that has a
            # two-pair tuple with Q-span >= 2 would break the mechanism.
            if (not a["DELIVERS"]) and a["n_two_pair_with_Qspan_ge2"] > 0:
                nrefute += 1
                refutations.append(dict(m=m, p=pp, tag=out["tag"],
                                        vertex=lab,
                                        n_bad=a["n_two_pair_with_Qspan_ge2"]))
        OUT["recs"].append(out)
        json.dump(OUT, open(res, "w"), indent=1, default=str)
        if i % 5 == 0:
            print("[%3d] m=%d p=%d %s (%.0fs)"
                  % (i, m, pp,
                     {l: (out["vert"][l]["DELIVERS"],
                          out["vert"][l]["max_Qspan_on_two_pair"],
                          out["vert"][l]["n_two_pair_with_Qspan_ge2"])
                      for l in out["vert"]}, time.time() - t0), flush=True)
    OUT["Q1_kernel_bound"] = dict(
        violations=nviol, ok=(nviol == 0),
        note="rank S(tau) <= |N(v)| - dim span Q  -- the cofactor identity")
    OUT["_controls_run"].append("Q1_kernel_bound")
    OUT["Q2_mechanism_test"] = dict(
        refutations=nrefute, ok=(nrefute == 0),
        note="a FAILING two-firing-letter vertex with a two-pair tuple of "
             "Q-span >= 2 would refute the mechanism")
    OUT["_controls_run"].append("Q2_mechanism_test")
    OUT["Q3_refutation_scan"] = dict(records=refutations[:20],
                                     n=len(refutations))
    OUT["_controls_run"].append("Q3_refutation_scan")
    # aggregate: Q-span distribution split by DELIVERS
    agg = defaultdict(Counter)
    for r in OUT["recs"]:
        for l, a in r["vert"].items():
            agg["m%d_%s_%s" % (r["m"], l, "deliver" if a["DELIVERS"]
                               else "FAIL")][a["max_Qspan_on_two_pair"]] += 1
    OUT["Qspan_distribution"] = {k: dict(v) for k, v in agg.items()}
    OUT["_manifest_ok"] = True
    OUT["done"] = True
    json.dump(OUT, open(res, "w"), indent=1, default=str)
    print("QSPAN DONE %d points; kernel-bound violations=%d; "
          "mechanism refutations=%d  %.0fs"
          % (len(OUT["recs"]), nviol, nrefute, time.time() - t0), flush=True)
    print("distribution:", json.dumps(OUT["Qspan_distribution"], indent=1),
          flush=True)


if __name__ == "__main__":
    main()
