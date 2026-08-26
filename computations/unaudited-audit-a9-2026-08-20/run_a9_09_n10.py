#!/usr/bin/env python3
"""A9-09: cross-checks.  (a) the N=10 k=3 calibration (386 orbits must all be
SAT -- if any were UNSAT the encoder would be over-constraining, since the
disjoint-PM X_3 sources exist at every even N); (b) N=10 k=4 spot-check;
(c) all 13 N=6 case ideals by Groebner in five characteristics.
"""
from __future__ import annotations

import json
import random
import sys
import time

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-audit-a9-2026-08-20")
if BASE not in sys.path:
    sys.path.insert(0, BASE)
import a9_enc as E                                                   # noqa: E402
import a9_ctrl as X                                                  # noqa: E402
import run_a9_03_sat as S                                            # noqa: E402
import run_a9_08_t1h_gb as G                                         # noqa: E402

RES = {}
OUT = f"{BASE}/results_a9_09_n10.json"
T0 = time.time()


def ck(tag=""):
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print(f"   [ck {tag}] {round(time.time() - T0, 1)}s", flush=True)


def n10_k3():
    reps = S.orbit_reps(10)
    out = {"n_orbits": len(reps), "n_sat": 0, "unsat_cases": []}
    for i, Rs in enumerate(reps):
        e = E.Enc(10, Rs, k=3).build()
        if i == 0:
            out["vars"], out["clauses"] = e.nv, len(e.cls)
        if e.solve_pysat()[0]:
            out["n_sat"] += 1
        else:
            out["unsat_cases"].append([list(r) for r in Rs])
        if i % 50 == 0:
            ck(f"n10k3-{i}")
    out["PASS"] = out["n_sat"] == len(reps)
    return out


def n10_x3_objects(nobj=6):
    """Real X_3 diagonal sources at N=10 -> the encoder must accept them."""
    rng = random.Random(1010)
    out = {"objects": 0, "site_checks": 0, "violations": 0,
           "normal_form_failures": 0, "cases": {}}
    for Ms in X.disjoint_pm_triples(10, rng, ntries=4000)[:nobj]:
        ts = X.pm_source(10, Ms, [X.unit_product_weights(rng, len(M))
                                  for M in Ms])
        if X.x3_violations(ts, 10):
            continue
        out["objects"] += 1
        for z in range(10):
            r = X.check_point(ts, 10, z, 3)
            out["site_checks"] += 1
            if not r.get("PASS"):
                if "normal_form" in r:
                    out["normal_form_failures"] += 1
                else:
                    out["violations"] += r["n_violations"]
            else:
                out["cases"][str(r["Rs"])] = \
                    out["cases"].get(str(r["Rs"]), 0) + 1
    out["PASS"] = (out["violations"] == 0 and
                   out["normal_form_failures"] == 0 and out["objects"] > 0)
    return out


def n10_k4_spot(m=40):
    reps = S.orbit_reps(10)
    rng = random.Random(5)
    pick = [reps[0], reps[-1]] + rng.sample(reps, m)
    out = {"checked": len(pick), "n_sat": 0, "sat_cases": []}
    for Rs in pick:
        e = E.Enc(10, Rs, k=4).build()
        if e.solve_pysat()[0]:
            out["n_sat"] += 1
            out["sat_cases"].append([list(r) for r in Rs])
    return out


def n6_all_gb():
    reps = G.orbit_reps(6)
    chars = (0, 2, 3, 7, 32003)
    out = {"n_orbits": len(reps), "not_unit": [], "cases": {}}
    for i, Rs in enumerate(reps):
        gens, tags, names = G.case_ideal_strings(6, Rs, kmax=4)
        rec = {"n_gens": len(gens)}
        for ch in chars:
            rec[str(ch)] = G.decide(gens, names, ch)["isunit"]
        out["cases"][str(Rs)] = rec
        if not all(rec[str(ch)] == "1" for ch in chars):
            out["not_unit"].append(str(Rs))
        ck(f"gb6-{i}")
    out["PASS"] = not out["not_unit"]
    return out


def main():
    what = sys.argv[1:] or ["gb6", "x3", "k3", "k4"]
    if "gb6" in what:
        RES["n6_all_13_groebner"] = n6_all_gb()
        print("gb6", RES["n6_all_13_groebner"]["PASS"], flush=True)
    if "x3" in what:
        RES["n10_x3_objects"] = n10_x3_objects()
        print("x3", RES["n10_x3_objects"], flush=True)
        ck("x3")
    if "k3" in what:
        RES["n10_k3"] = n10_k3()
        print("k3", {k: v for k, v in RES["n10_k3"].items()
                     if k != "unsat_cases"}, flush=True)
        ck("k3")
    if "k4" in what:
        RES["n10_k4_spot"] = n10_k4_spot()
        print("k4", RES["n10_k4_spot"], flush=True)
    RES["seconds"] = round(time.time() - T0, 1)
    ck("final")


if __name__ == "__main__":
    main()
