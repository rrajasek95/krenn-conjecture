#!/usr/bin/env python3
"""W29 C2 -- the UNIFIED abstraction, its calibration, and the full N = 8 run.

CALIBRATION FIRST (ledger 13/18/19/21).  The whole machine is exercised at the
orders where a diagonal exact source is KNOWN to exist -- N = 4 (the three
perfect matchings of K_4) and, if one exists, N = 6.  There the abstraction
MUST be satisfiable, AND the real object's own vanishing pattern must satisfy
every single clause.  A pipeline that kills N = 4 is broken, full stop.

Then the k = 3 calibration at N = 8 (must be satisfiable: three-colour X_3
diagonal sources exist), and only then the k = 4 run over the case ledger.

argv: [what] in {calib, n8k3, n8k4, everything}
"""
from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, permutations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-diagclose-w29-2026-08-19")
W28 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
       "unaudited-x4empty-w28-2026-08-18")
for p in (BASE, W28):
    if p not in sys.path:
        sys.path.insert(0, p)
import w29_core as C                                                # noqa: E402
import w29_k8van as KV                                              # noqa: E402

RES, RAN = {}, []
OUT = None


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


# --------------------------------------------------------------- structure
def free_set(ts, c, n, z, kmax=None):
    """{y in V-z : every even split of V-z-y kills haf(t^d)haf(t^e)}."""
    d, e = [x for x in range(3) if x != c]
    VP = [x for x in range(n) if x != z]
    out = []
    for y in VP:
        W = tuple(x for x in VP if x != y)
        ok = True
        for m in range(0, len(W) + 1, 2):
            for S1 in combinations(W, m):
                S2 = tuple(x for x in W if x not in S1)
                if kmax is not None and n - max(2, len(S1), len(S2)) > kmax:
                    continue
                if C.haf(ts[d], S1) != 0 and C.haf(ts[e], S2) != 0:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            out.append(y)
    return out


def case_of(ts, n, z, kmax=None):
    """(ys, Rs, relabelling) of a real source, per W29-B2; None if it has no
    such normal form (which would itself refute W29-B2)."""
    VP = [x for x in range(n) if x != z]
    ys = []
    for c in range(3):
        F = free_set(ts, c, n, z, kmax)
        cand = [y for y in F
                if C.haf(ts[c], tuple(x for x in VP if x != y)) != 0
                and ts[c].get(C.ekey(z, y), 0) != 0]
        if not cand:
            return None
        ys.append(cand[0])
    if len(set(ys)) != 3:
        return None
    Q = [y for y in VP if y not in ys]
    perm = {}
    for c in range(3):
        perm[ys[c]] = c
    for i, q in enumerate(Q):
        perm[q] = 3 + i
    perm[z] = n - 1
    Fs = [free_set(ts, c, n, z, kmax) for c in range(3)]
    Rs = tuple(tuple(sorted(perm[y] for y in Fs[c] if y in Q))
               for c in range(3))
    return {"ys": ys, "Rs": [list(r) for r in Rs], "perm": perm,
            "free_sets": {c: Fs[c] for c in range(3)}}


def relabel(ts, perm):
    out = [{}, {}, {}]
    for c in range(3):
        for (a, b), v in ts[c].items():
            out[c][C.ekey(perm[a], perm[b])] = v
    return out


def z_assign(van, ts):
    A = {}
    for key, v in van.lit.items():
        if key[0] == "z":
            _, c, S = key
            A[v] = (C.haf(ts[c], S) == 0)
        elif key[0] == "q":
            _, c, S, w, u = key
            rest = tuple(x for x in S if x not in (w, u))
            A[v] = (ts[c].get(C.ekey(w, u), 0) != 0
                    and C.haf(ts[c], rest) != 0)
        else:
            A[v] = False
    viol = []
    for (tag, cl) in van.tagged:
        if not any((lit > 0) == A.get(abs(lit), False) for lit in cl):
            viol.append((str(tag), [str(van.names.get(abs(l))) for l in cl]))
    return viol


def build_van(n, Rs, kmax=None, z=None, use=("case", "free", "xfree")):
    z = n - 1 if z is None else z
    pf = None
    if kmax is not None:
        pf = (lambda parts: n - max(len(p) for p in parts) <= kmax)
    van = KV.K8Van(n=n, prof_filter=pf).build()
    if "case" in use:
        van.add_case(Rs, ys=(0, 1, 2), z=z)
    if "free" in use:
        vanfree(van, Rs, n, z, kmax)
    if "xfree" in use:
        van.add_xfree(Rs, ys=(0, 1, 2), z=z)
    return van


def vanfree(van, Rs, n, z, kmax):
    VP = tuple(x for x in range(n) if x != z)
    for c in range(3):
        d, e = [x for x in range(3) if x != c]
        for y in sorted(set([c]) | set(Rs[c])):
            W = tuple(x for x in VP if x != y)
            for m in range(0, len(W) + 1, 2):
                for S1 in combinations(W, m):
                    S2 = tuple(x for x in W if x not in S1)
                    if kmax is not None and \
                            n - max(2, len(S1), len(S2)) > kmax:
                        continue
                    cl = []
                    if S1:
                        cl.append(van.z(d, S1))
                    if S2:
                        cl.append(van.z(e, S2))
                    if cl:
                        van.add(("FREE", c, y, S1, S2), cl)
    return van


# ------------------------------------------------------------- known objects
def pm_decomp_source(n, mats):
    ts = [{}, {}, {}]
    for c, M in enumerate(mats):
        for e in M:
            ts[c][C.ekey(*e)] = Fraction(1)
    return ts


def find_exact(n, tries=200000, seed=1):
    """Search for a diagonal EXACT source on K_n among 0/1 PM-unions."""
    V = tuple(range(n))
    pms = C.pm_list(V)
    rng = random.Random(seed)
    seen = set()
    for _ in range(tries):
        idx = tuple(sorted(rng.sample(range(len(pms)), 3)))
        if idx in seen:
            continue
        seen.add(idx)
        ts = pm_decomp_source(n, [pms[i] for i in idx])
        if not C.exact_violations(ts, n):
            return ts, idx
    return None, None


def calib():
    print("=== C2 CALIBRATION ===", flush=True)
    rec = {}
    for n in (4, 6):
        ts, idx = find_exact(n, tries=20000 if n == 4 else 200000)
        r = {"n": n, "found_exact_source": ts is not None}
        if ts is None:
            print(f"[calib n={n}] no diagonal exact source among PM triples",
                  flush=True)
            rec[f"n{n}"] = r
            continue
        r["source"] = {c: [list(e) for e in ts[c]] for c in range(3)}
        r["exact_violations"] = len(C.exact_violations(ts, n, stop=False))
        z = n - 1
        co = case_of(ts, n, z)
        r["case"] = co
        if co is None:
            r["W29B2_PASS"] = False
            print(f"[calib n={n}] W29-B2 FAILS on a real exact source!",
                  flush=True)
        else:
            r["W29B2_PASS"] = True
            ts2 = relabel(ts, co["perm"])
            Rs = tuple(tuple(x) for x in co["Rs"])
            van = build_van(n, Rs)
            sat = not van.is_unsat()
            viol = z_assign(van, ts2)
            r["abstraction_SAT"] = sat
            r["real_point_violations"] = len(viol)
            r["violation_examples"] = viol[:5]
            r["PASS"] = sat and not viol
            print(f"[calib n={n}] exact source found (PMs {idx}); case "
                  f"Rs={co['Rs']}; abstraction SAT={sat}; the real point "
                  f"violates {len(viol)} clauses (want 0)", flush=True)
        rec[f"n{n}"] = r
        RAN.append(f"calib_n{n}")
    return rec


def n8_k3():
    """Three-colour X_3 diagonal sources exist -- k=3 must NOT be killed."""
    print("=== C2 k=3 CALIBRATION at N=8 ===", flush=True)
    allR = [tuple(S) for k in range(5) for S in combinations((3, 4, 5, 6), k)]
    nsat, n = 0, 0
    sats = []
    t0 = time.time()
    for R0 in allR:
        for R1 in allR:
            for R2 in allR:
                van = build_van(8, (R0, R1, R2), kmax=3)
                n += 1
                if not van.is_unsat():
                    nsat += 1
                    if len(sats) < 20:
                        sats.append([list(R0), list(R1), list(R2)])
    print(f"[k=3] {n} cases, {nsat} satisfiable ({round(time.time()-t0,1)}s) "
          f"-- MUST be > 0", flush=True)
    return {"n_cases": n, "n_sat": nsat, "sat_examples": sats,
            "PASS": nsat > 0, "secs": round(time.time() - t0, 1)}


def n8_k4():
    print("=== C2 THE N=8 RUN (k=4 = EXACT for diagonal sources) ===",
          flush=True)
    allR = [tuple(S) for k in range(5) for S in combinations((3, 4, 5, 6), k)]
    out = {"n_cases": 0, "n_sat": 0, "sat_cases": []}
    t0 = time.time()
    for R0 in allR:
        for R1 in allR:
            for R2 in allR:
                van = build_van(8, (R0, R1, R2))
                out["n_cases"] += 1
                if not van.is_unsat():
                    out["n_sat"] += 1
                    out["sat_cases"].append([list(R0), list(R1), list(R2)])
        print(f"    ... {out['n_cases']}/4096, {out['n_sat']} SAT "
              f"({round(time.time()-t0,1)}s)", flush=True)
    out["secs"] = round(time.time() - t0, 1)
    return out


def main():
    global OUT
    what = sys.argv[1] if len(sys.argv) > 1 else "everything"
    OUT = f"{BASE}/results_c2_unified_{what}.json"
    t0 = time.time()
    if what in ("calib", "everything"):
        RES["calibration"] = calib()
        RAN.append("calibration")
        ck("calib")
    if what in ("n8k3", "everything"):
        RES["n8_k3"] = n8_k3()
        RAN.append("n8_k3")
        ck("n8k3")
    if what in ("n8k4", "everything"):
        RES["n8_k4"] = n8_k4()
        RAN.append("n8_k4")
        ck("n8k4")
    ok = (RES.get("calibration", {}).get("n4", {}).get("PASS") and
          RES.get("n8_k3", {}).get("PASS"))
    RES["CONCLUSION"] = (
        "W29-T1 [PROVED-HERE]: no diagonal exact source on K_8 -- every one of "
        "the 4096 free-set-triple cases is UNSAT in the vanishing-pattern "
        "abstraction (characteristic-free)"
        if ok and RES.get("n8_k4", {}).get("n_sat") == 0 else
        "NOT established -- see the records")
    RES["seconds"] = round(time.time() - t0, 1)
    ck("final")
    print(">>> " + RES["CONCLUSION"])
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()
