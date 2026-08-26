#!/usr/bin/env python3
"""W40 / T10 -- the WHOLE exact-d=2 variety on a 4+4 diagonal support.

Motivation.  W40/T9 found that NONE of W33's 19,528 stored exact d=2
sources has a 4+4 (non-Hamiltonian) disjoint-PM diagonal support -- the
stratum is invisible to sampling -- so the level-5 sweep does not cover
branch (B1).  W33-D5 settled only the sub-case with exactly 4 cross cells.
This file decides the sub-case-free question in one computation.

TARGET STATEMENT (ledger 27, verbatim):
    Let D0 = {01,23,45,67} and D1 = {03,12,47,56} (two disjoint 4-cycles
    0-1-2-3-0 and 4-5-6-7-4, alternating colours).  Consider all d=2 sources
    whose colour-0 diagonal is supported inside D0 with all four weights
    NONZERO, whose colour-1 diagonal is supported inside D1 with all four
    weights NONZERO, and whose cross cells A_e[0][1], A_e[1][0] are FREE on
    every one of the 28 edges (56 cross variables, 64 in all).  Impose exact
    d=2-ness (all 256 words).  QUESTION: what is the dimension of the
    saturated variety?
If it equals the gauge-orbit dimension 8, the W33-D5 twisted 4+4 orbit is
the ENTIRE 4+4 stratum and branch (B1) closes completely, because W40/T3b
already killed that orbit at full exactness.

Singular hygiene: zz-prefix + no-shadow guard, LIB "elim.lib" before sat,
`list L = sat(I,J); ideal S = L[1];` (ledger 11/14), '?'-parse in
run_singular, integer coefficients only.

CONTROLS (ledger 21/31):
  point_control   the stored W33-D5 point must satisfy EVERY generator (it
                  is an exact source on this support) -- so the ideal is not
                  unit and the computation is not vacuous (ledger 28).
  mutation        a mutated D5 point must NOT satisfy them all.
  engine_agree    the symbolic generators, evaluated at the D5 point, agree
                  with the inherited DP hafnian engine word by word.
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
    EDG, Manifest, N, PMS, Sym, d5_point, haf, no_shadow_guard, require,
    run_singular, words2,
)

OUT = os.path.join(HERE, "results_t10_44variety.json")
SEC = int(sys.argv[1]) if len(sys.argv) > 1 else 10800

D0 = [(0, 1), (2, 3), (4, 5), (6, 7)]
D1 = [(0, 3), (1, 2), (4, 7), (5, 6)]


def build():
    names, idx = [], {}

    def newvar(tag):
        idx[tag] = len(names)
        names.append(f"zzv({len(names) + 1})")
        return Sym.var(idx[tag])

    cf = {e: [[Sym() for _ in range(2)] for _ in range(2)] for e in EDG}
    for e in D0:
        cf[e][0][0] = newvar(("a", e))
    for e in D1:
        cf[e][1][1] = newvar(("b", e))
    for e in EDG:
        cf[e][0][1] = newvar(("x", e))
        cf[e][1][0] = newvar(("y", e))
    return names, idx, cf


def haf_sym2(cf, w):
    tot = Sym()
    for M in PMS:
        pr = Sym.const(1)
        for (u, v) in M:
            f = cf[(u, v)][w[u]][w[v]]
            if not f:
                pr = Sym()
                break
            pr = pr * f
        if pr:
            tot = tot + pr
    return tot


def main():
    t0 = time.time()
    MAN = Manifest(["engine_agree", "point_control", "mutation",
                    "main_decision"])
    R = {"status": "UNAUDITED",
         "pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")).read()
         .strip(),
         "target": ("dimension of the saturated exact-d=2 variety on the "
                    "4+4 diagonal support with all 56 cross cells free"),
         "_controls_run": []}

    def ran(n):
        MAN.mark(n)
        R["_controls_run"].append(n)

    names, idx, cf = build()
    gens, meta = [], []
    for w in words2(N):
        tgt = 1 if len(set(w)) == 1 else 0
        g = haf_sym2(cf, w).subtract_const(tgt)
        if g.t:
            gens.append(g)
            meta.append(w)
    R["system"] = {"n_vars": len(names), "n_gens": len(gens),
                   "n_monomials": sum(len(g.t) for g in gens),
                   "max_degree": max(g.ndeg() for g in gens)}
    print("system:", R["system"], flush=True)

    # ---- the D5 point in these coordinates
    D5 = d5_point()
    pt = [Fraction(0)] * len(names)
    for e in D0:
        pt[idx[("a", e)]] = D5[e][0][0]
    for e in D1:
        pt[idx[("b", e)]] = D5[e][1][1]
    for e in EDG:
        pt[idx[("x", e)]] = D5[e][0][1]
        pt[idx[("y", e)]] = D5[e][1][0]

    # ---- engine_agree + point_control
    mism, bad = 0, 0
    for w, g in zip(meta, gens):
        tgt = 1 if len(set(w)) == 1 else 0
        lhs = haf(D5, w, n=N, sample=Fraction(0)) - tgt
        rhs = g.evaluate(pt)
        if lhs != rhs:
            mism += 1
        if rhs != 0:
            bad += 1
    R["engine_agree"] = {"checks": len(gens), "mismatches": mism,
                         "ok": mism == 0}
    require(mism == 0, "symbolic generators disagree with the DP engine")
    ran("engine_agree")
    R["point_control"] = {"nonzero_generators_at_D5": bad, "ok": bad == 0}
    require(bad == 0, "the D5 point does not satisfy the generators")
    ran("point_control")

    pt2 = list(pt)
    pt2[idx[("x", (0, 4))]] += Fraction(1)
    bad2 = sum(1 for g in gens if g.evaluate(pt2) != 0)
    R["mutation"] = {"nonzero_generators_at_mutated_D5": bad2,
                     "ok": bad2 > 0}
    require(bad2 > 0, "mutation control FAILED (the cell is inert)")
    ran("mutation")
    print("controls OK (point satisfies all", len(gens), "generators)",
          flush=True)
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)

    # ---- the decision
    body = ",\n ".join(g.to_singular(names) for g in gens)
    prod = "*".join([names[idx[("a", e)]] for e in D0]
                    + [names[idx[("b", e)]] for e in D1])
    script = ('LIB "elim.lib";\n'
              f"ring R = 0, (zzv(1..{len(names)})), dp;\n"
              f"ideal zzI = {body};\n"
              f"poly zzD = {prod};\n"
              "list zzL = sat(zzI, zzD);\n"
              "ideal zzS = zzL[1];\n"
              "ideal zzG = std(zzS);\n"
              '"UNIT:", (size(zzG) == 1 && zzG[1] == 1);\n'
              '"DIM:", dim(zzG);\n'
              '"NGB:", size(zzG);\n')
    no_shadow_guard(script, set(names))
    try:
        txt = run_singular(script, timeout=max(600, SEC - int(time.time()
                                                              - t0)))
        out = {}
        for ln in txt.splitlines():
            for k in ("UNIT", "DIM", "NGB"):
                if ln.strip().startswith(k + ":"):
                    out[k] = ln.split(":", 1)[1].strip()
        R["decision"] = out
        R["decision"]["gauge_orbit_dim_W33"] = 8
        R["decision"]["reading"] = (
            "DIM == 8 means the twisted-4+4 gauge orbit is the ENTIRE 4+4 "
            "stratum, so branch (B1) closes with W40/T3b; DIM > 8 means "
            "further 4+4 sources exist and (B1) keeps a live sub-case of "
            "that dimension.")
    except Exception as ex:
        R["decision"] = {"status": "unchecked", "err": str(ex)[:300]}
    print("decision:", R["decision"], flush=True)
    ran("main_decision")
    R["manifest"] = MAN.assert_complete()
    R["elapsed"] = time.time() - t0
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
