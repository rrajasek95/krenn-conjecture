#!/usr/bin/env python3
"""W40 / T2 -- BRANCH (B1): can the W33-D5 twisted 4+4 be the {0,1}
restriction of an X_4 point at N=8?

TARGET STATEMENT (verbatim; ledger 27 -- the controls below test THIS, not a
relaxation):
    There is no d=3 source A on K_8 with A|_{colours 0,1} equal to the
    W33-D5 twisted-4+4 point of results_t1.json and H_w(A) = [w constant]
    for every w in {0,1,2}^8 with off(w) <= 4.
Because the gauge group G = T x S_3 x S_8 acts on X_4 and its restriction to
a colour pair is exactly the d=2 gauge group (W33-D3), and because the
twisted-4+4 stratum is a SINGLE gauge orbit (W33 t12: stratum dim 8 = gauge
orbit dim 8), a verdict here decides the whole orbit.

PARAMETRISATION.  Fix the {0,1} block.  Words with exactly one site coloured
2 are all imposed at k=4 and are exactly the homogeneous star system of the
background at that site, so the colour-2 star at j ranges over Ker_j -- 20
free parameters for D5 (profile [0,2,6,2,0,2,6,2]; sites 0 and 4 carry NO
colour-2 cross cell at all).  The 28 pure cells A_e[2][2] are free.  48 vars.

CONTROLS (each writes its own ok field; ledger 21/31):
  expander_agreement  the Sym expander vs the INHERITED DP hafnian engine at
                      random rational points of the parametrisation, over
                      all imposed words.
  linear_layer        every single-2 word is identically satisfied by the
                      parametrisation (i.e. Ker_j was imposed correctly), and
                      a DELIBERATELY WRONG star (a non-kernel vector) breaks
                      at least one of them (a must-fire control).
  background_words    every word in {0,1}^8 is satisfied identically.
  calibration         on the Delta^2 background the block-diagonal PM-triple
                      point satisfies ALL k=3 generators (Python and, ledger
                      13b, independently inside Singular) -- so the k=3
                      ideal is NOT unit there -- and violates exactly 2 of
                      the k=4 generators, reproducing W33 t5's
                      k4_nbad_on_X3_point = 2 (two-view, ledger 26).
"""
from __future__ import annotations

import itertools
import json
import os
import random
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w40_core import (  # noqa: E402
    EDG, Manifest, N, PMS, Sym, build_variables, cell_forms,
    completion_generators, d5_point, delta2_point, haf3, haf_sym,
    install_d3, kernel_bases, off, require, singular_decide,
    singular_eval_point, words3,
)

OUT = os.path.join(HERE, "results_t2.json")
SEC = int(sys.argv[1]) if len(sys.argv) > 1 else 7200


def pm_triples():
    """PM triples (M0, M1, M2) with M0, M1 the Delta^2 cycle classes and
    every pairwise union Hamiltonian."""
    M0 = [(0, 1), (2, 3), (4, 5), (6, 7)]
    M1 = [(1, 2), (3, 4), (5, 6), (0, 7)]

    def ham(ma, mb):
        adj = {i: [] for i in range(N)}
        for e in list(ma) + list(mb):
            adj[e[0]].append(e[1])
            adj[e[1]].append(e[0])
        cur, prev, seen = 0, None, [0]
        for _ in range(N - 1):
            nxt = [x for x in adj[cur] if x != prev]
            if not nxt:
                return False
            prev, cur = cur, nxt[0]
            if cur in seen:
                return False
            seen.append(cur)
        return len(seen) == N and 0 in adj[cur]

    used = set(M0) | set(M1)
    for M in PMS:
        if set(M) & used:
            continue
        if ham(M0, M) and ham(M1, M):
            return M0, M1, list(M)
    return None


def rand_point(nv, rng, lo=-4, hi=4):
    return [Fraction(rng.randint(lo, hi), rng.randint(1, 3))
            for _ in range(nv)]


def main():
    t0 = time.time()
    MAN = Manifest(["expander_agreement", "linear_layer", "background_words",
                    "calibration", "main_decision"])
    R = {"status": "UNAUDITED",
         "pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")).read()
         .strip(),
         "target": ("no X_4 point at N=8 whose {0,1} restriction is the "
                    "W33-D5 twisted 4+4 (single gauge orbit)"),
         "_controls_run": []}

    def ran(name):
        MAN.mark(name)
        R["_controls_run"].append(name)

    rng = random.Random(40404)
    bgs = {"D5": d5_point(), "Delta2": delta2_point()}
    data = {}
    for nm, bg in bgs.items():
        kb = kernel_bases(bg)
        names, lamidx, qidx = build_variables(kb)
        cf = cell_forms(bg, kb, lamidx, qidx)
        g3, m3 = completion_generators(cf, 3)
        g4, m4 = completion_generators(cf, 4)
        data[nm] = dict(bg=bg, kb=kb, names=names, lamidx=lamidx,
                        qidx=qidx, cf=cf, g3=g3, m3=m3, g4=g4, m4=m4)
        R.setdefault("systems", {})[nm] = {
            "kernel_profile": [kb[j]["dim"] for j in range(N)],
            "n_vars": len(names), "n_lam": len(lamidx), "n_q": len(qidx),
            "n_gens_k3": len(g3), "n_gens_k4": len(g4),
            "max_degree": max(x.ndeg() for x in g4)}

    # ------------------------------------------------ expander_agreement
    agree = {"checks": 0, "mismatches": 0}
    for nm in bgs:
        D = data[nm]
        for _ in range(3):
            vals = rand_point(len(D["names"]), rng)
            src = install_d3(D["cf"], vals)
            for w, g in zip(D["m4"], D["g4"]):
                tgt = 1 if len(set(w)) == 1 else 0
                lhs = haf3(src, w) - tgt            # inherited DP engine
                rhs = g.evaluate(vals)              # Sym expander
                agree["checks"] += 1
                if lhs != rhs:
                    agree["mismatches"] += 1
    agree["ok"] = agree["mismatches"] == 0
    R["expander_agreement"] = agree
    require(agree["ok"], f"expander disagrees with the engine: {agree}")
    ran("expander_agreement")

    # ----------------------------------------------------- linear_layer
    ll = {}
    for nm in bgs:
        D = data[nm]
        singles = [w for w in words3(4) if list(w).count(2) == 1]
        ll[f"{nm}_single2_words"] = len(singles)
        bad = 0
        for _ in range(3):
            vals = rand_point(len(D["names"]), rng)
            src = install_d3(D["cf"], vals)
            for w in singles:
                if haf3(src, w) != 0:
                    bad += 1
        ll[f"{nm}_single2_violations"] = bad
        # MUST-FIRE: break the kernel constraint at a site with a nonzero
        # kernel by installing an arbitrary star, and check a single-2 word
        # now fails (else the test is vacuous, ledger 28).
        j = next(j for j in range(N) if D["kb"][j]["dim"] < 14)
        vals = rand_point(len(D["names"]), rng)
        src = install_d3(D["cf"], vals)
        r = 1 if j != 1 else 2
        u, v = min(j, r), max(j, r)
        a, b = (2, 0) if j < r else (0, 2)
        src[(u, v)][a][b] += Fraction(1)
        fires = any(haf3(src, w) != 0 for w in singles)
        ll[f"{nm}_mustfire"] = fires
    ll["ok"] = (all(ll[f"{nm}_single2_violations"] == 0 for nm in bgs)
                and all(ll[f"{nm}_mustfire"] for nm in bgs))
    R["linear_layer"] = ll
    require(ll["ok"], f"linear-layer control FAILED: {ll}")
    ran("linear_layer")

    # -------------------------------------------------- background_words
    bw = {}
    for nm in bgs:
        D = data[nm]
        bad = 0
        for _ in range(2):
            vals = rand_point(len(D["names"]), rng)
            src = install_d3(D["cf"], vals)
            for w in itertools.product(range(2), repeat=N):
                tgt = 1 if len(set(w)) == 1 else 0
                if haf3(src, w) != tgt:
                    bad += 1
        bw[nm] = bad
    bw["ok"] = all(bw[nm] == 0 for nm in bgs)
    R["background_words"] = bw
    require(bw["ok"], f"background-word control FAILED: {bw}")
    ran("background_words")

    # ------------------------------------------------------- calibration
    tri = pm_triples()
    require(tri is not None, "no pairwise-Hamiltonian PM triple on Delta^2")
    M0, M1, M2 = tri
    D = data["Delta2"]
    pt = [Fraction(0)] * len(D["names"])
    for e in D["qidx"]:
        pt[D["qidx"][e]] = Fraction(1) if tuple(e) in set(M2) else Fraction(0)
    src = install_d3(D["cf"], pt)
    nbad3 = [w for w in D["m3"] if haf3(src, w) != (1 if len(set(w)) == 1
                                                    else 0)]
    nbad4 = [w for w in D["m4"] if haf3(src, w) != (1 if len(set(w)) == 1
                                                    else 0)]
    # ledger 13(b): the same verdict computed independently inside Singular
    ev3 = singular_eval_point(D["g3"], D["names"], pt)
    ev4 = singular_eval_point(D["g4"], D["names"], pt)
    cal = {"M2": [list(e) for e in M2],
           "k3_violations_python": len(nbad3),
           "k3_nonzero_gens_singular": ev3,
           "k4_violations_python": len(nbad4),
           "k4_nonzero_gens_singular": ev4,
           "k4_violating_words": [list(w) for w in nbad4],
           "W33_t5_k4_nbad_on_X3_point": 2}
    cal["ok"] = (len(nbad3) == 0 and ev3 == 0 and len(nbad4) == 2
                 and ev4 == 2)
    R["calibration"] = cal
    require(cal["ok"], f"CALIBRATION FAILED: {cal}")
    ran("calibration")
    print("calibration OK:", cal["k3_violations_python"], "k3 /",
          cal["k4_violations_python"], "k4 violations", flush=True)
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)

    # ------------------------------------------------------ main decision
    dec = {}
    for nm in ("D5", "Delta2"):
        D = data[nm]
        for k, gs in ((3, D["g3"]), (4, D["g4"])):
            for base in (0, "integer"):
                tag = "Q" if base == 0 else "ZZ"
                key = f"{nm}_k{k}_{tag}"
                left = max(600, int(SEC - (time.time() - t0)))
                try:
                    o = singular_decide(gs, D["names"], base, left,
                                        want_dim=(base == 0))
                    dec[key] = {"unit": o["UNIT"], "dim": o.get("DIM")}
                except Exception as ex:
                    dec[key] = {"error": str(ex)[:200]}
                print(key, dec[key], flush=True)
                R["decision"] = dec
                with open(OUT, "w") as fh:
                    json.dump(R, fh, indent=1, sort_keys=True)
    ran("main_decision")
    R["manifest"] = MAN.assert_complete()
    R["elapsed"] = time.time() - t0
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
