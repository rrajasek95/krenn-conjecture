#!/usr/bin/env python3
"""W40 / T1 -- inherited-engine controls and the W33-D5 reproduction.

Declared controls (ledger 21/31: the manifest is asserted at the end and
every ok field below is written by the control that computed it):
  engine_xcheck    haf (DP) vs haf_pm (explicit PM) on the objects used.
  d5_exact         the stored D5 point is an exact d=2 source over Q, F13,
                   F31 (ledger 19: two primes = 1 mod 3).
  d5_mutation      perturbing any single stored cell BREAKS exactness
                   (guards against a vacuous/degenerate seed).
  d5_support       the diagonal support is two disjoint 4-cycles, i.e. the
                   colour-0 and colour-1 PMs have NON-Hamiltonian union
                   (this is what puts the point in branch (B1)).
  d5_kernels       the star-kernel profile and null graph reproduce W33 t12
                   ([0,2,6,2,0,2,6,2]; null pairs [[1,3],[2,6],[5,7]]).
  delta2_kernels   the calibration background's profile is all-6 (W33 t1).
  gauge_orbit      the D5 point's gauge orbit is nontrivial and support
                   invariants are gauge invariants (spot check).
"""
from __future__ import annotations

import itertools
import json
import os
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w40_core import (  # noqa: E402
    D5_CROSS, EDG, Fp, Manifest, N, apply_perm, apply_torus, cell,
    copy_source, d5_point, defects2, delta2_point, haf, haf_pm, is_exact2,
    kernel_bases, n_cross, require, setcell, star_kernel, support, words2,
)

OUT = os.path.join(HERE, "results_t1.json")


def cycles_of_union(m0, m1):
    adj = {i: [] for i in range(N)}
    for e in list(m0) + list(m1):
        adj[e[0]].append(e[1])
        adj[e[1]].append(e[0])
    seen, cyc = set(), []
    for s in range(N):
        if s in seen:
            continue
        cur, prev, comp = s, None, [s]
        seen.add(s)
        while True:
            nxt = [x for x in adj[cur] if x != prev]
            if not nxt:
                break
            prev, cur = cur, nxt[0]
            if cur == s:
                break
            comp.append(cur)
            seen.add(cur)
        cyc.append(len(comp))
    return sorted(cyc)


def main():
    t0 = time.time()
    MAN = Manifest(["engine_xcheck", "d5_exact", "d5_mutation", "d5_support",
                    "d5_kernels", "delta2_kernels", "gauge_orbit"])
    R = {"status": "UNAUDITED",
         "pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")).read()
         .strip(),
         "_controls_run": []}

    def ran(name):
        MAN.mark(name)
        R["_controls_run"].append(name)

    # ------------------------------------------------ engine cross-check
    src = d5_point()
    mism = 0
    checks = 0
    for w in words2(N):
        a = haf(src, w, n=N, sample=Fraction(0))
        b = haf_pm(src, w, n=N, sample=Fraction(0))
        checks += 1
        if a != b:
            mism += 1
    d2 = delta2_point()
    for w in words2(N):
        a = haf(d2, w, n=N, sample=Fraction(0))
        b = haf_pm(d2, w, n=N, sample=Fraction(0))
        checks += 1
        if a != b:
            mism += 1
    R["engine_xcheck"] = {"checks": checks, "mismatches": mism,
                          "ok": mism == 0}
    require(mism == 0, "engine cross-check FAILED")
    ran("engine_xcheck")

    # ------------------------------------------------------- D5 exactness
    ex = {}
    okQ, bad = is_exact2(src, N)
    ex["Q"] = okQ
    okQ2, _ = is_exact2(src, N, engine=haf_pm)
    ex["Q_control_engine"] = okQ2
    for p in (13, 31):                       # ledger 19: both = 1 mod 3
        s = d5_point(sample=Fp(0, p))
        okp, _ = is_exact2(s, N)
        ex[f"F{p}"] = okp
    ex["ok"] = all(ex.values())
    R["d5_exact"] = ex
    require(ex["ok"], f"D5 not exact: {ex} first bad {bad}")
    ran("d5_exact")

    # -------------------------------------------------------- mutation
    mut = {}
    for (e, a, b) in support(src):
        s2 = copy_source(src)
        s2[e][a][b] = s2[e][a][b] + Fraction(1)
        okm, _ = is_exact2(s2, N)
        mut[str((e, a, b))] = (not okm)
    mut["ok"] = all(v for k, v in mut.items() if k != "ok")
    R["d5_mutation"] = mut
    require(mut["ok"], "mutation control FAILED (a cell is inert)")
    ran("d5_mutation")

    # --------------------------------------------------------- support
    m0 = [e for (e, a, b) in support(src) if (a, b) == (0, 0)]
    m1 = [e for (e, a, b) in support(src) if (a, b) == (1, 1)]
    cyc = cycles_of_union(m0, m1)
    sup = {"M0": [list(e) for e in m0], "M1": [list(e) for e in m1],
           "M0_is_PM": sorted(x for e in m0 for x in e) == list(range(N)),
           "M1_is_PM": sorted(x for e in m1 for x in e) == list(range(N)),
           "union_cycle_type": cyc, "n_cross": n_cross(src),
           "cross_cells": [str(c) for c in D5_CROSS]}
    sup["ok"] = (sup["M0_is_PM"] and sup["M1_is_PM"] and cyc == [4, 4]
                 and sup["n_cross"] == 4)
    R["d5_support"] = sup
    require(sup["ok"], f"support control FAILED: {sup}")
    ran("d5_support")

    # --------------------------------------------------------- kernels
    kb = kernel_bases(src)
    prof = [kb[j]["dim"] for j in range(N)]
    # NULL GRAPH Z(B) (W33-K1): {j,r} is a null pair iff the cofactor
    # hafnian haf(B | V-j-r, u) vanishes for EVERY u, i.e. the star column
    # pair (r,0),(r,1) at j is identically zero.  (Symmetric in j,r; the
    # control below checks the symmetry.)  This is the graph in which a
    # cross cell of a third colour may live for free; dim Ker_j
    # = 2 deg_Z(j) + s_j.
    nullj = {j: {r for (r, e) in kb[j]["zcols"] if (r, 1 - e)
                 in kb[j]["zcols"]} for j in range(N)}
    null = sorted([u, v] for (u, v) in EDG if v in nullj[u])
    require(all((u in nullj[v]) == (v in nullj[u]) for (u, v) in EDG),
            "null graph not symmetric")
    R["null_degrees"] = [len(nullj[j]) for j in range(N)]
    R["syzygy_dims"] = [kb[j]["dim"] - 2 * len(nullj[j]) for j in range(N)]
    kd = {"profile": prof, "profile_W33": [0, 2, 6, 2, 0, 2, 6, 2],
          "null_graph": null, "null_graph_W33": [[1, 3], [2, 6], [5, 7]],
          "zero_star_sites": [j for j in range(N) if kb[j]["dim"] == 0],
          "zcols": {str(j): [str(c) for c in kb[j]["zcols"]]
                    for j in range(N)}}
    kd["ok"] = (prof == [0, 2, 6, 2, 0, 2, 6, 2]
                and null == [[1, 3], [2, 6], [5, 7]])
    R["d5_kernels"] = kd
    require(kd["ok"], f"kernel control FAILED: profile {prof} null {null}")
    ran("d5_kernels")

    kb2 = kernel_bases(d2)
    prof2 = [kb2[j]["dim"] for j in range(N)]
    R["delta2_kernels"] = {"profile": prof2, "ok": prof2 == [6] * N}
    require(prof2 == [6] * N, f"delta2 kernel control FAILED: {prof2}")
    ran("delta2_kernels")

    # ----------------------------------------------------------- gauge
    # a torus element in T (prod alpha = prod delta = 1) preserves
    # exactness; the support (hence the kernel profile) is invariant.
    al = [Fraction(2), Fraction(1, 2), Fraction(3), Fraction(1, 3),
          Fraction(1), Fraction(1), Fraction(1), Fraction(1)]
    de = [Fraction(1, 5), Fraction(5), Fraction(1), Fraction(1),
          Fraction(7), Fraction(1, 7), Fraction(1), Fraction(1)]
    g = apply_torus(src, al, de)
    okg, _ = is_exact2(g, N)
    perm = [1, 2, 3, 0, 5, 6, 7, 4]
    gp = apply_perm(src, perm, N)
    okp, _ = is_exact2(gp, N)
    kbg = kernel_bases(g)
    profg = [kbg[j]["dim"] for j in range(N)]
    # a torus element OUTSIDE T must break exactness (the group is exactly G)
    bad_al = [Fraction(2)] + [Fraction(1)] * 7
    gb = apply_torus(src, bad_al, [Fraction(1)] * 8)
    okb, _ = is_exact2(gb, N)
    ga = {"torus_preserves": okg, "perm_preserves": okp,
          "profile_invariant": profg == prof, "offT_breaks": (not okb)}
    ga["ok"] = all(ga.values())
    R["gauge_orbit"] = ga
    require(ga["ok"], f"gauge control FAILED: {ga}")
    ran("gauge_orbit")

    R["manifest"] = MAN.assert_complete()
    R["elapsed"] = time.time() - t0
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    print("profile", prof, "null", null, "zero-star sites",
          kd["zero_star_sites"])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
