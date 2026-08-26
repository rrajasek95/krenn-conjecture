#!/usr/bin/env python3
"""W29 E1 -- THE ADVERSARIAL BUILDER (ledger 20).

An independent lane whose only job is to BUILD the object W29-T1 says cannot
exist: a diagonal exact source on K_8 over C.  Different from W28's builders:
this one attacks the FULL exact system (all even partition products plus the
three pure equations) directly by complex Levenberg-Marquardt from random
starts, with no X_k ladder and no free-site structure, and it is CALIBRATED at
N = 4, where a source exists and the builder must find it.

Any N = 8 hit is verified EXACTLY (rationalised / re-evaluated in Fractions)
before anything is claimed.

argv: [n ...] [starts]
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

RES, RAN = {}, []
OUT = f"{BASE}/results_e1_builder.json"


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def setup(n):
    V = tuple(range(n))
    E = list(combinations(V, 2))
    idx = {e: i for i, e in enumerate(E)}
    pms = {}
    for m in range(0, n + 1, 2):
        for S in combinations(V, m):
            pms[S] = [[idx[e] for e in M] for M in C.pm_list(S)]
    parts = []
    for m0 in range(0, n + 1, 2):
        for S0 in combinations(V, m0):
            R = [x for x in V if x not in S0]
            for m1 in range(0, len(R) + 1, 2):
                for S1 in combinations(R, m1):
                    S2 = tuple(x for x in R if x not in S1)
                    if max(len(S0), len(S1), len(S2)) == n:
                        continue
                    parts.append((S0, S1, S2))
    return V, E, idx, pms, parts


def hafs(t, S, pms):
    """t: (3, |E|) complex array; returns the vector of haf(t^c|S)."""
    out = np.ones(3, dtype=complex)
    ms = pms[S]
    if not ms:
        return np.zeros(3, dtype=complex)
    if len(S) == 0:
        return out
    tot = np.zeros(3, dtype=complex)
    for M in ms:
        p = np.ones(3, dtype=complex)
        for e in M:
            p = p * t[:, e]
        tot = tot + p
    return tot


def residual_fn(n):
    V, E, idx, pms, parts = setup(n)
    ne = len(E)

    def F(v):
        t = (v[:3 * ne] + 1j * v[3 * ne:]).reshape(3, ne)
        H = {S: hafs(t, S, pms) for S in pms}
        r = []
        for c in range(3):
            r.append(H[V][c] - 1.0)
        for (S0, S1, S2) in parts:
            r.append(H[S0][0] * H[S1][1] * H[S2][2])
        r = np.array(r)
        return np.concatenate([r.real, r.imag])
    return F, ne, len(parts)


def build(n, starts=400, seed=0, scale=1.0):
    F, ne, npart = residual_fn(n)
    rng = np.random.default_rng(seed)
    best = (np.inf, None)
    hits = []
    for s in range(starts):
        v0 = rng.normal(0, scale, 6 * ne)
        sol = least_squares(F, v0, method="lm", max_nfev=4000)
        cost = float(np.max(np.abs(F(sol.x))))
        if cost < best[0]:
            best = (cost, sol.x.copy())
        if cost < 1e-9:
            hits.append(sol.x.copy())
            if len(hits) >= 3:
                break
    return best, hits, ne, npart


def rationalise(v, ne, n, tol=1e-7, dens=(1, 2, 3, 4, 6, 8, 12)):
    """Try to snap a numerical hit to exact rationals and RE-VERIFY exactly."""
    t = (v[:3 * ne] + 1j * v[3 * ne:]).reshape(3, ne)
    E = list(combinations(range(n), 2))
    ts = [{}, {}, {}]
    for c in range(3):
        for i, e in enumerate(E):
            z = t[c, i]
            if abs(z.imag) > tol:
                return None
            x = z.real
            snapped = None
            for d in dens:
                cand = Fraction(round(x * d), d)
                if abs(float(cand) - x) < tol:
                    snapped = cand
                    break
            if snapped is None:
                return None
            if snapped != 0:
                ts[c][e] = snapped
    return ts


def main():
    args = [int(a) for a in sys.argv[1:]]
    ns = [a for a in args if a < 100] or [4, 6, 8]
    starts = ([a for a in args if a >= 100] or [400])[0]
    for n in ns:
        t0 = time.time()
        print(f"=== E1 builder at n = {n} ({starts} starts) ===", flush=True)
        (cost, v), hits, ne, npart = build(n, starts=starts, seed=11 * n)
        rec = {"n": n, "starts": starts, "n_edges": ne,
               "n_partition_equations": npart,
               "best_max_residual": cost, "n_numerical_hits": len(hits)}
        print(f"  best max|residual| = {cost:.3e}; numerical hits: "
              f"{len(hits)}", flush=True)
        exact = None
        for h in hits:
            ts = rationalise(h, ne, n)
            if ts is not None and not C.exact_violations(ts, n):
                exact = ts
                break
        rec["EXACT_SOURCE_FOUND"] = exact is not None
        if exact is not None:
            rec["source"] = {c: {str(list(e)): str(v2)
                                 for e, v2 in exact[c].items()}
                             for c in range(3)}
            print(f"  *** EXACT DIAGONAL SOURCE at n={n}: {rec['source']}",
                  flush=True)
        rec["secs"] = round(time.time() - t0, 1)
        RES.setdefault("orders", {})[str(n)] = rec
        RAN.append(f"builder_n{n}")
        ck(f"n{n}")
    c4 = RES.get("orders", {}).get("4", {})
    RES["CALIBRATION_PASS"] = bool(c4.get("EXACT_SOURCE_FOUND"))
    RES["ESCALATE"] = bool(RES.get("orders", {}).get("8", {})
                           .get("EXACT_SOURCE_FOUND"))
    ck("final")
    print(f">>> calibration (n=4 source found): {RES['CALIBRATION_PASS']}; "
          f"ESCALATE (n=8 source found): {RES['ESCALATE']}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
