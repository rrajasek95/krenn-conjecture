#!/usr/bin/env python3
"""W29 G1 -- THE END-TO-END SOUNDNESS CONTROL AT N = 8 ITSELF.

The W29-T1 verdict is "the abstraction is UNSAT for every case at k = 4".  The
control that can actually falsify a bad encoder is: take a REAL diagonal
object at N = 8 one rung down (an X_3 source, which exists), push it through
the SAME pipeline at k = 3 -- W29-B2 normal form, case identification, clause
generation -- and check that its own vanishing pattern satisfies EVERY clause.
If the encoder over-constrains anywhere, this control fires.

X_3 for a diagonal source at N = 8 is exactly

    haf(t^c|V) = 1     and     t^d_{ab} haf(t^c|V-{a,b}) = 0   (c != d)

(the only even profiles with off-count <= 3 are (8,0,0) and (6,2,0)).
"""
from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from itertools import combinations

import numpy as np
from scipy.optimize import least_squares

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-diagclose-w29-2026-08-19")
if BASE not in sys.path:
    sys.path.insert(0, BASE)
import w29_core as C                                                # noqa: E402
import run_c2_unified as U                                          # noqa: E402
import run_e1_builder as B                                          # noqa: E402

RES, RAN = {}, []
OUT = f"{BASE}/results_g1_x3control.json"
N = 8


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def x3_violations(ts, n=N):
    V = tuple(range(n))
    bad = []
    for c in range(3):
        if C.haf(ts[c], V) != 1:
            bad.append(("PURE", c))
    for (a, b) in combinations(V, 2):
        R = tuple(x for x in V if x not in (a, b))
        for c in range(3):
            for d in range(3):
                if c == d:
                    continue
                if ts[d].get((a, b), 0) != 0 and C.haf(ts[c], R) != 0:
                    bad.append(("MIX", c, d, (a, b)))
    return bad


def residual_k3(n=N):
    V, E, idx, pms, parts = B.setup(n)
    ne = len(E)
    keep = [p for p in parts if n - max(len(q) for q in p) <= 3]

    def F(v):
        t = (v[:3 * ne] + 1j * v[3 * ne:]).reshape(3, ne)
        H = {S: B.hafs(t, S, pms) for S in pms}
        r = [H[V][c] - 1.0 for c in range(3)]
        for (S0, S1, S2) in keep:
            r.append(H[S0][0] * H[S1][1] * H[S2][2])
        r = np.array(r)
        return np.concatenate([r.real, r.imag])
    return F, ne, len(keep)


def structured_x3():
    """An exact X_3 diagonal source built by hand: t^c supported on a single
    perfect matching of K_8, the three matchings pairwise disjoint."""
    V = tuple(range(N))
    pms = C.pm_list(V)
    for i in range(len(pms)):
        for j in range(i + 1, len(pms)):
            for k in range(j + 1, len(pms)):
                Ms = [pms[i], pms[j], pms[k]]
                if len(set(Ms[0]) | set(Ms[1]) | set(Ms[2])) != 12:
                    continue
                ts = [{e: Fraction(1) for e in M} for M in Ms]
                if not x3_violations(ts):
                    return ts, (i, j, k)
    return None, None


def main():
    t0 = time.time()
    print("=== W29 G1: the X_3 end-to-end control at N = 8 ===", flush=True)
    ts, idx = structured_x3()
    RES["structured_x3"] = {"found": ts is not None, "pm_indices": idx}
    if ts is None:
        F, ne, nk = residual_k3()
        rng = np.random.default_rng(7)
        best = (np.inf, None)
        for s in range(400):
            sol = least_squares(F, rng.normal(0, 1, 6 * ne), method="lm",
                                max_nfev=4000)
            c = float(np.max(np.abs(F(sol.x))))
            if c < best[0]:
                best = (c, sol.x.copy())
            if c < 1e-10:
                cand = B.rationalise(sol.x, ne, N)
                if cand is not None and not x3_violations(cand):
                    ts = cand
                    break
        RES["numeric_x3"] = {"best_residual": best[0], "found": ts is not None}
    if ts is None:
        RES["PASS"] = None
        RES["note"] = "no exact X_3 diagonal source constructed; control not run"
        print(">>> control NOT exercised (no X_3 object found)")
        ck("final")
        return
    RES["x3_source"] = {c: [list(e) for e in ts[c]] for c in range(3)}
    RES["x3_violations"] = len(x3_violations(ts))
    print(f"  X_3 source: {RES['x3_source']} (violations "
          f"{RES['x3_violations']})", flush=True)
    RAN.append("x3_object")
    ck("x3")

    ok_all = True
    per = {}
    for z in range(N):
        co = U.case_of(ts, N, z, kmax=3)
        if co is None:
            per[z] = {"W29B2_normal_form": False}
            ok_all = False
            continue
        ts2 = U.relabel(ts, co["perm"])
        Rs = tuple(tuple(x) for x in co["Rs"])
        van = U.build_van(N, Rs, kmax=3, z=N - 1)
        viol = U.z_assign(van, ts2)
        sat = not van.is_unsat()
        per[z] = {"W29B2_normal_form": True, "Rs": co["Rs"],
                  "free_sets": co["free_sets"], "abstraction_SAT": sat,
                  "real_point_violations": len(viol),
                  "examples": viol[:4]}
        if viol or not sat:
            ok_all = False
        print(f"  [z={z}] case Rs={co['Rs']}, abstraction SAT={sat}, "
              f"the real X_3 source violates {len(viol)} clauses (want 0)",
              flush=True)
    RES["per_site"] = per
    RES["PASS"] = ok_all
    RAN.append("per_site")

    # and the same object must be REJECTED at k = 4 (it is not exact)
    z = 0
    co = U.case_of(ts, N, z, kmax=4)
    if co is not None:
        ts2 = U.relabel(ts, co["perm"])
        van4 = U.build_van(N, tuple(tuple(x) for x in co["Rs"]), kmax=4,
                           z=N - 1)
        v4 = U.z_assign(van4, ts2)
        RES["k4_rejects_the_x3_object"] = {"violations": len(v4),
                                           "PASS": len(v4) > 0}
        print(f"  [k=4] the same X_3 object violates {len(v4)} clauses "
              f"(want > 0)", flush=True)
    RES["seconds"] = round(time.time() - t0, 1)
    ck("final")
    print(f">>> G1 PASS = {RES['PASS']}")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()
