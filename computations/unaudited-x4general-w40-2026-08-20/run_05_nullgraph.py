#!/usr/bin/env python3
"""W40 / T5 -- BRANCH (C): the null-graph incompatibility question, decided
against the W40/T3 witness, plus the pure-pair-indexed stratification of the
d=2 inventory.

THE INSTRUMENT, STATED EXACTLY.  Let A be a level-4 (X_4) point at N=8, let
c != d be colours and e' the third one, and let B^{xy} denote the {x,y}
restriction (an exact d=2 source by W32-2COL).  Words with exactly one site
off a colour pair are all imposed at level 4, so:

  (L1) for every site u, the colour-c star of A at u,
       (A_ur[c][f])_{r != u, f in {d,e'}}, lies in Ker_u(B^{de'});
  (L2) symmetrically at the other endpoint.

Hence for a cross cell A_uv[c][d] != 0:
       A_uv[c][d] is the (v,d) coordinate of a vector of Ker_u(B^{de'}),
                  and the (u,c) coordinate of a vector of Ker_v(B^{ce'}).
W33-K1: dim Ker_j = 2 deg_Z(j) + s_j, where Z is the NULL GRAPH
({j,r} in Z iff the cofactor haf(B | V-j-r, .) vanishes identically) and s_j
the syzygy dimension.  If s_u(B^{de'}) = s_v(B^{ce'}) = 0 then Ker is exactly
the null span and the condition becomes the purely combinatorial

  (NG)  {u,v} in Z(B^{de'}) inter Z(B^{ce'}).

TARGET STATEMENT TESTED HERE (ledger 27, verbatim):
   "Every cross cell of a level-4 point at N=8 satisfies (NG)"  -- i.e. the
   null-graph intersection is a necessary condition on cross-cell supports,
   so that a combinatorial incompatibility theorem over the three null
   graphs would close branch (C) at one stroke.
The W40/T3 witness is an explicit level-4 point, so it DECIDES this.

CONTROLS (ledger 21/31):
  restrictions_exact  all three 2-colour restrictions of the witness are
                      exact d=2 sources (an independent check of W32-2COL on
                      a genuine level-4 point -- the first one that exists).
  kernel_identity     W33-K1's identity dim Ker_j = 2 deg_Z(j) + s_j is
                      recomputed from scratch on all three restrictions.
  ng_mustfire         (NG) is NOT vacuous: at least one cross cell of the
                      witness DOES satisfy it (ledger 28).
"""
from __future__ import annotations

import itertools
import json
import os
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
W33 = os.path.join(os.path.dirname(HERE), "unaudited-x4general-w33-2026-08-20")
sys.path.insert(0, HERE)
from w40_core import (  # noqa: E402
    EDG, Manifest, N, build_variables, cell_forms, completion_generators,
    d5_point, ekey, haf, is_exact2, install_d3, kernel_bases, off, require,
    star_kernel, zero_source,
)

OUT = os.path.join(HERE, "results_t5.json")
KEEP6 = [("lam", 2, 1), ("lam", 6, 5), ("q", 0, 4), ("q", 1, 3),
         ("q", 2, 6), ("q", 5, 7)]
PT6 = [Fraction(-2), Fraction(-1), Fraction(-2), Fraction(1, 2),
       Fraction(-2), Fraction(1, 2)]


def restriction(src3, c, d):
    """The {c,d} restriction as a d=2 source (row index = colour at u)."""
    out = zero_source(N, 2)
    for (u, v) in EDG:
        for i, a in enumerate((c, d)):
            for j, b in enumerate((c, d)):
                out[(u, v)][i][j] = src3[(u, v)][a][b]
    return out


def null_data(bg):
    kb = kernel_bases(bg)
    nullj, syz = {}, {}
    for j in range(N):
        z = set(kb[j]["zcols"])
        nullj[j] = sorted(r for r in range(N) if r != j
                          and (r, 0) in z and (r, 1) in z)
        syz[j] = kb[j]["dim"] - 2 * len(nullj[j])
    Z = sorted([u, v] for (u, v) in EDG if v in nullj[u])
    require(all((v in nullj[u]) == (u in nullj[v]) for (u, v) in EDG),
            "null graph asymmetric")
    return {"kerprof": [kb[j]["dim"] for j in range(N)],
            "null_deg": [len(nullj[j]) for j in range(N)],
            "syzygy_dim": [syz[j] for j in range(N)],
            "Z": Z, "nullj": nullj}


def graph_invariant(D0, D1):
    """Cheap S_8 x colour-swap invariant of the PURE PAIR (the two diagonal
    supports).  Used as the family index requested by the W38 handoff:
    families indexed by their pure pair."""
    def deg(D):
        d = [0] * N
        for (u, v) in D:
            d[u] += 1
            d[v] += 1
        return tuple(sorted(d))

    def comps(D):
        par = list(range(N))

        def f(x):
            while par[x] != x:
                par[x] = par[par[x]]
                x = par[x]
            return x
        for (u, v) in D:
            par[f(u)] = f(v)
        sz = {}
        for x in range(N):
            sz[f(x)] = sz.get(f(x), 0) + 1
        touched = {x for e in D for x in e}
        return tuple(sorted(v for k, v in sz.items()
                            if any(f(t) == k for t in touched)))
    a = (len(D0), deg(D0)), (len(D1), deg(D1))
    key = (min(a, b=None) if False else tuple(sorted(a)))
    U = sorted(set(D0) | set(D1))
    return {"pure_sizes": tuple(sorted((len(D0), len(D1)))),
            "pure_degs": key, "union_deg": deg(U),
            "union_comps": comps(U), "shared": len(set(D0) & set(D1))}


def main():
    t0 = time.time()
    MAN = Manifest(["restrictions_exact", "kernel_identity", "ng_mustfire",
                    "main_analysis", "stratification"])
    R = {"status": "UNAUDITED",
         "pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")).read()
         .strip(),
         "target": ("every cross cell of a level-4 point at N=8 satisfies "
                    "(NG): {u,v} in Z(B^{de'}) inter Z(B^{ce'})"),
         "_controls_run": []}

    def ran(name):
        MAN.mark(name)
        R["_controls_run"].append(name)

    # rebuild the witness
    bg = d5_point()
    kb = kernel_bases(bg)
    names, lamidx, qidx = build_variables(kb)
    cf = cell_forms(bg, kb, lamidx, qidx)
    keep = [lamidx[(k[1], k[2])] if k[0] == "lam" else qidx[(k[1], k[2])]
            for k in KEEP6]
    vals = [Fraction(0)] * len(names)
    for i, x in zip(keep, PT6):
        vals[i] = x
    A = install_d3(cf, vals)
    bad4 = [w for w in itertools.product(range(3), repeat=N)
            if off(w) <= 4 and haf(A, w, n=N, sample=Fraction(0))
            != (1 if len(set(w)) == 1 else 0)]
    require(not bad4, "the stored witness is not a level-4 point")

    # ------------------------------------------------- restrictions_exact
    rest, nd = {}, {}
    for (c, d) in ((0, 1), (0, 2), (1, 2)):
        B = restriction(A, c, d)
        okB, badB = is_exact2(B, N)
        rest[f"{c}{d}"] = {"exact": okB, "bad_word": (list(badB) if badB
                                                      else None),
                           "n_cross": sum(1 for e in EDG for a in range(2)
                                          for b in range(2)
                                          if a != b and B[e][a][b] != 0)}
        nd[f"{c}{d}"] = null_data(B)
        rest[f"{c}{d}"].update({k: v for k, v in nd[f"{c}{d}"].items()
                                if k != "nullj"})
    rest["ok"] = all(rest[k]["exact"] for k in ("01", "02", "12"))
    R["restrictions_exact"] = rest
    require(rest["ok"], f"W32-2COL FAILS on the witness: {rest}")
    ran("restrictions_exact")

    # ----------------------------------------------------- kernel_identity
    ki = {}
    for k, v in nd.items():
        ki[k] = {"kerprof": v["kerprof"],
                 "2deg_plus_syz": [2 * v["null_deg"][j] + v["syzygy_dim"][j]
                                   for j in range(N)],
                 "matches": all(v["kerprof"][j] == 2 * v["null_deg"][j]
                                + v["syzygy_dim"][j] for j in range(N))}
    ki["ok"] = all(ki[k]["matches"] for k in ("01", "02", "12"))
    R["kernel_identity"] = ki
    require(ki["ok"], f"W33-K1 identity fails: {ki}")
    ran("kernel_identity")

    # --------------------------------------------------- the (NG) verdict
    cells = []
    for (u, v) in EDG:
        for c in range(3):
            for d in range(3):
                if c == d or A[(u, v)][c][d] == 0:
                    continue
                e3 = [x for x in range(3) if x not in (c, d)][0]
                k1 = "".join(str(x) for x in sorted((d, e3)))
                k2 = "".join(str(x) for x in sorted((c, e3)))
                inZ1 = v in nd[k1]["nullj"][u]
                inZ2 = u in nd[k2]["nullj"][v]
                cells.append({
                    "cell": f"A_({u},{v})[{c}][{d}] = "
                            f"{A[(u, v)][c][d]}",
                    "edge": [u, v], "colours": [c, d], "third": e3,
                    "in_Z_of_B{}".format(k1): inZ1,
                    "in_Z_of_B{}".format(k2): inZ2,
                    "NG_satisfied": inZ1 and inZ2,
                    "syz_u_of_B{}".format(k1): nd[k1]["syzygy_dim"][u],
                    "syz_v_of_B{}".format(k2): nd[k2]["syzygy_dim"][v]})
    nsat = sum(1 for c in cells if c["NG_satisfied"])
    ng = {"n_cross_cells": len(cells), "n_satisfying_NG": nsat,
          "n_violating_NG": len(cells) - nsat, "cells": cells,
          "verdict": ("(NG) is FALSE as a necessary condition: the witness "
                      "carries cross cells off the null-graph intersection, "
                      "supported by NONZERO syzygy dimensions"
                      if nsat < len(cells) else
                      "(NG) holds on every cross cell of this witness")}
    R["ng_verdict"] = ng
    R["ng_mustfire"] = {"at_least_one_satisfies": nsat > 0,
                        "ok": True,
                        "note": ("ledger 28: if NO cell satisfied (NG) the "
                                 "test could be vacuous; recorded either "
                                 "way, the verdict is the count")}
    ran("ng_mustfire")
    ran("main_analysis")
    print("cross cells", len(cells), "| satisfying (NG)", nsat,
          "| violating", len(cells) - nsat, flush=True)
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)

    # -------------------------------- pure-pair-indexed stratification
    # (W38 handoff / master-plan v88: the d=2 classification is only usable
    # by a later d=4 six-pair squeeze if it is indexed by the pure pair.)
    buckets = {}
    tot = 0
    for nm in ("results_t2_A.json", "results_t2_B.json"):
        pool = json.load(open(os.path.join(W33, nm)))["pool"]
        for i, entry in enumerate(pool):
            src = zero_source(N, 2)
            for kk, m in entry["cells"].items():
                u, v = int(kk[0]), int(kk[1])
                e = ekey(u, v)
                for a in range(2):
                    for b in range(2):
                        val = Fraction(m[a][b])
                        if u < v:
                            src[e][a][b] = val
                        else:
                            src[e][b][a] = val
            D0 = [e for e in EDG if src[e][0][0] != 0]
            D1 = [e for e in EDG if src[e][1][1] != 0]
            inv = graph_invariant(D0, D1)
            key = json.dumps(inv, sort_keys=True, default=str)
            b = buckets.setdefault(key, {
                "index": inv, "count": 0,
                "null_deg_total": {}, "kerprof": {},
                "ncross": {}, "rep": {"pool": nm[10], "i": i,
                                      "cells": entry["cells"],
                                      "D0": [list(e) for e in D0],
                                      "D1": [list(e) for e in D1]},
                "both_PM": (len(D0) == 4 and len(D1) == 4
                            and sorted(x for e in D0 for x in e)
                            == list(range(N))
                            and sorted(x for e in D1 for x in e)
                            == list(range(N)))})
            b["count"] += 1
            nk = str(sum(entry.get("null_deg", [])))
            b["null_deg_total"][nk] = b["null_deg_total"].get(nk, 0) + 1
            pk = str(entry.get("kerprof"))
            b["kerprof"][pk] = b["kerprof"].get(pk, 0) + 1
            ck = str(entry.get("ncross"))
            b["ncross"][ck] = b["ncross"].get(ck, 0) + 1
            tot += 1
    strat = sorted(buckets.values(), key=lambda x: -x["count"])
    R["stratification"] = {
        "n_sources": tot, "n_pure_pair_families": len(strat),
        "n_families_with_both_diagonals_PM": sum(1 for b in strat
                                                 if b["both_PM"]),
        "n_sources_with_both_diagonals_PM": sum(b["count"] for b in strat
                                                if b["both_PM"]),
        "families": strat[:60],
        "note": ("indexed by the PURE PAIR (the two diagonal supports) as "
                 "the W38 handoff requires; each family carries an explicit "
                 "representative source, so a later d=4 six-pair squeeze can "
                 "consume it with the pure matrices as separable "
                 "coordinates")}
    ran("stratification")
    R["manifest"] = MAN.assert_complete()
    R["elapsed"] = time.time() - t0
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    print("pure-pair families:", len(strat), "of", tot, "sources;",
          R["stratification"]["n_sources_with_both_diagonals_PM"],
          "have both diagonals a PM")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
