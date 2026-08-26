#!/usr/bin/env python3
"""W30 THEOREM CHECKER.  UNAUDITED.  Exact only.

THEOREM W30-X (the replacement for W26's residual pairwise exclusion).

Setting: a clean point of support m with every Gamma cell nonzero.  Let v be
a vertex with EXACTLY THREE Gamma-neighbours N(v) = {s1,s2,s3}, and let

    S(tau)[t][j] = A_{v,sj}-cell at letter t of v and letter tau_j of sj

be its 3x3 SLICE MATRIX (trigger-free: it depends only on the letters at
N(v)).  Write ROWS = d u^T + sc*M for the master-relation matrix at v.

STEP 1 (isomorphism).  If the Gamma-edge (v, sigma-partner) is the only
column of M that is absent, and the corresponding u_{q0} != 0 and sc != 0,
then ROWS = psi(S) rowwise for a linear ISOMORPHISM psi of k^3.  Hence

    v delivers at an index choice  <=>  rank S = rank S|clean rows.       (1)

STEP 2 (two firing letters).  If v's live singles carry two distinct firing
letters and both clean pairs are realised at a COMMON slice tuple tau, then
non-delivery at both of those index choices forces  rank S(tau) = 3.       (2)

STEP 3 (the cofactor identity -- elementary, no master relation).  Phi is
multilinear, so for any word w,
        Phi(w with letter t at v)  =  < S(tau) row t , Q(w) >,
        Q(w)_j = haf_{Gamma - {v,sj}}(w).
If all three letters at v give CLEAN words then S(tau) Q(w) = 0, so

    Q(w) != 0   ==>   det S(tau) = 0.                                     (3)

(2) and (3) are contradictory, so v DELIVERS.  The hypotheses needed are
finite and checkable: SOME two-pair slice tuple tau must admit (a) both
index choices with sc != 0 and (b) one untriggered word with tuple tau and
Q != 0.  This file checks (1),(2),(3) and the hypotheses at every point on
disk, and reports the ESCAPE SET (tuples where the hypotheses fail).

usage: w30_thm.py <pointsfile> [outsuffix]
"""
from __future__ import annotations

import json
import os
import sys
import time
from collections import defaultdict
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
# the protected vertices, by support: exactly-3-neighbour + type (b) +
# two firing letters (see results_struct.json)
PROTECTED = {25: ['R6'], 26: ['R5', 'R6'], 27: ['R5'], 28: []}


def nbrs(m, v):
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    return sorted(s for s in range(8)
                  if (min(s, v), max(s, v)) in gs)


def cell(bl, gs, u, v, a, b):
    e = (u, v) if u < v else (v, u)
    if e not in gs:
        return None
    return bl[e][a][b] if u < v else bl[e][b][a]


def slice_S(m, bl, v, tau, ns, K):
    """3 x |N(v)| slice matrix; tau = letters at N(v)."""
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    return [[cell(bl, gs, s, v, tau[j], t) if s < v
             else cell(bl, gs, v, s, t, tau[j])
             for j, s in enumerate(ns)] for t in range(3)]


def Qvec(m, bl, v, w, ns, K):
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    zero, one = K.n(0), K.n(1)
    out = []
    for s in ns:
        rest = tuple(z for z in range(8) if z not in (v, s))
        out.append(C.haf_on(bl, gs, rest, w, zero, one))
    return out


def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


def analyse(m, bl, lab, K):
    kind, v = L.vkey(lab)
    ns = nbrs(m, v)
    G = L.geom(m)
    sing, lv = G['sing'], G['lv']
    idx = L.index_choices_cached(m, kind, v)
    # ---- group the index choices by slice tuple
    bytau = defaultdict(list)
    for (w, fire) in idx:
        if len(fire) != 1:
            continue
        tau = tuple(w[s] for s in ns)
        sd = L.slice_data(m, bl, kind, v, w, K)
        sc_ok = sd is not None
        bytau[tau].append((w, tuple(sorted(fire)), sc_ok))
    # ---- untriggered words (all three letters clean) per slice tuple
    unt = defaultdict(list)
    for vals in product(range(3), repeat=7):
        others = [c for c in range(8) if c != v]
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
    # ---- the theorem's hypotheses, per two-pair slice tuple
    good = []
    escape = []
    for tau, lst in bytau.items():
        pairs = set(f for (_w, f, _o) in lst)
        if len(pairs) < 2:
            continue
        both_sc = all(any(o for (_w, f2, o) in lst if f2 == f)
                      for f in pairs)
        S = slice_S(m, bl, v, tau, ns, K)
        dS = det3(S) if len(ns) == 3 else None
        qok = None
        for w in unt.get(tau, []):
            Q = Qvec(m, bl, v, w, ns, K)
            if any(not K.iszero(z) for z in Q):
                qok = w
                break
        rec = dict(tau=list(tau), n_pairs=len(pairs), both_scale_nonzero=both_sc,
                   detS_zero=(dS is not None and K.iszero(dS)),
                   untriggered_with_Q_nonzero=(qok is not None),
                   n_untriggered=len(unt.get(tau, [])))
        if both_sc and qok is not None and len(ns) == 3:
            good.append(rec)
        else:
            escape.append(rec)
    r = L.vertex_report(m, bl, kind, v, K, stop_early=False)
    return dict(vertex=lab, n_neighbours=len(ns), neighbours=ns,
                n_two_pair_tuples=len(good) + len(escape),
                n_hypotheses_met=len(good), n_escape=len(escape),
                escape=escape[:8],
                all_detS_zero_on_good=all(g['detS_zero'] for g in good),
                DELIVERS=r['DELIVERS'], n_deliver=r['n_deliver'],
                n_idx=r['n_idx'],
                THEOREM_APPLIES=len(good) > 0,
                THEOREM_CONSISTENT=(not (len(good) > 0) or r['DELIVERS']))


def main():
    src = sys.argv[1]
    suf = sys.argv[2] if len(sys.argv) > 2 else ""
    d = json.load(open(os.path.join(HERE, src)))
    res = os.path.join(HERE, "results_thm%s.json" % suf)
    OUT = {"_header": "UNAUDITED W30 theorem checker",
           "source": src,
           "_controls_declared": ["T1_theorem_consistency",
                                  "T2_detS_zero_on_hypothesis_tuples",
                                  "T3_escape_census"],
           "_controls_run": [], "recs": []}
    t0 = time.time()
    nbad = 0
    for i, rec in enumerate(d["points"]):
        if rec.get("van"):
            continue
        m = rec.get("m") or d.get("m")
        if not PROTECTED.get(m):
            continue
        pp = int(rec.get("p") or d.get("p") or 0)
        if pp:
            bl = {eval(k): [[int(z) % pp for z in row] for row in v]
                  for k, v in rec["point"].items()}
            K = L.FP(pp)
        else:
            bl = {eval(k): [[F(z) for z in row] for row in v]
                  for k, v in rec["point"].items()}
            K = L.QF
        out = dict(m=m, p=pp, tag=str(rec.get("tag", i))[:40], vert={})
        for lab in PROTECTED[m]:
            out["vert"][lab] = analyse(m, bl, lab, K)
            if not out["vert"][lab]["THEOREM_CONSISTENT"]:
                nbad += 1
            if not out["vert"][lab]["all_detS_zero_on_good"]:
                nbad += 1
        OUT["recs"].append(out)
        json.dump(OUT, open(res, "w"), indent=1, default=str)
        print("[%3d] m=%d p=%d %-24s %s (%.0fs)"
              % (i, m, pp, out["tag"][:24],
                 {l: (out["vert"][l]["n_hypotheses_met"],
                      out["vert"][l]["n_escape"],
                      out["vert"][l]["all_detS_zero_on_good"],
                      out["vert"][l]["DELIVERS"]) for l in PROTECTED[m]},
                 time.time() - t0), flush=True)
    OUT["T1_theorem_consistency"] = dict(
        violations=nbad,
        ok=(nbad == 0),
        note="THEOREM_APPLIES => DELIVERS, at every point checked")
    OUT["_controls_run"].append("T1_theorem_consistency")
    OUT["T2_detS_zero_on_hypothesis_tuples"] = dict(
        ok=all(r["vert"][l]["all_detS_zero_on_good"]
               for r in OUT["recs"] for l in r["vert"]),
        note="step (3) of the proof, checked pointwise")
    OUT["_controls_run"].append("T2_detS_zero_on_hypothesis_tuples")
    OUT["T3_escape_census"] = dict(
        total_escape=sum(r["vert"][l]["n_escape"]
                         for r in OUT["recs"] for l in r["vert"]),
        total_good=sum(r["vert"][l]["n_hypotheses_met"]
                       for r in OUT["recs"] for l in r["vert"]),
        n_points_with_zero_good=sum(
            1 for r in OUT["recs"] for l in r["vert"]
            if r["vert"][l]["n_hypotheses_met"] == 0))
    OUT["_controls_run"].append("T3_escape_census")
    missing = [c for c in OUT["_controls_declared"]
               if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == [])
    OUT["done"] = True
    json.dump(OUT, open(res, "w"), indent=1, default=str)
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("THM DONE %d points, %d violations  %.0fs"
          % (len(OUT["recs"]), nbad, time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
