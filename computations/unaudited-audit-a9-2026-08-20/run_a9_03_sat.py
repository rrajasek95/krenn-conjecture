#!/usr/bin/env python3
"""A9-03: the independent UNSAT/SAT sweep (link 4).

Own encoder (a9_enc), own variable layout, inverted polarity.  Sub-runs:

  n4      -- the single N=4 case: MUST be SAT (the exceptional source exists)
  n6      -- all 64 cases at N=6, k=4 (= EXACT): expect UNSAT; k=3 for shape
  n8k4    -- all 4096 cases at N=8, k=4 (= EXACT): expect UNSAT
  n8k3    -- all 4096 cases at N=8, k=3: MUST be SAT (X_3 sources exist)
  ablate  -- which clause families are load-bearing (87 orbit reps)
  multi   -- three independent SAT engines agree on the 87 orbit reps

argv: sub-run names, or "all".
"""
from __future__ import annotations

import json
import sys
import time
from itertools import combinations, permutations, product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-audit-a9-2026-08-20")
if BASE not in sys.path:
    sys.path.insert(0, BASE)
import a9_enc as E                                                   # noqa: E402

RES = {}
OUT = f"{BASE}/results_a9_03_sat.json"


def ck(tag=""):
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print(f"   [ck {tag}] {round(time.time() - T0, 1)}s", flush=True)


T0 = time.time()


def all_cases(n):
    Q = tuple(range(3, n - 1))
    allR = [tuple(S) for k in range(len(Q) + 1) for S in combinations(Q, k)]
    return [(R0, R1, R2) for R0 in allR for R1 in allR for R2 in allR]


def orbit_reps(n):
    Q = tuple(range(3, n - 1))
    allR = [tuple(S) for k in range(len(Q) + 1) for S in combinations(Q, k)]
    seen, reps = set(), []
    for trip in product(allR, repeat=3):
        if trip in seen:
            continue
        orb = set()
        for sig in permutations(Q):
            m = dict(zip(Q, sig))
            img = tuple(tuple(sorted(m[y] for y in R)) for R in trip)
            for pi in permutations(range(3)):
                orb.add(tuple(img[pi[i]] for i in range(3)))
        seen |= orb
        reps.append(trip)
    return reps


def sweep(n, k, cases, solver="cadical195", label=""):
    t0 = time.time()
    nsat, sat_examples, sizes = 0, [], []
    for i, Rs in enumerate(cases):
        e = E.Enc(n, Rs, k=k).build()
        if i == 0:
            sizes = [e.nv, len(e.cls)]
        sat, _ = e.solve_pysat(solver)
        if sat:
            nsat += 1
            if len(sat_examples) < 8:
                sat_examples.append([list(r) for r in Rs])
    return {"n": n, "k": k, "n_cases": len(cases), "n_sat": nsat,
            "n_unsat": len(cases) - nsat, "solver": solver,
            "first_case_vars_clauses": sizes,
            "sat_examples": sat_examples,
            "secs": round(time.time() - t0, 1), "label": label}


def run_n4():
    out = {}
    for k in (2, None):
        out[f"k{k}"] = sweep(4, k, [((), (), ())], label="N4")
    out["MUST_BE_SAT"] = all(out[f"k{k}"]["n_sat"] == 1 for k in (2, None))
    return out


def run_n6():
    out = {}
    cases = all_cases(6)
    reps = orbit_reps(6)
    out["n_cases"] = len(cases)
    out["n_orbits"] = len(reps)
    out["k4_all"] = sweep(6, 4, cases, label="N6 k=4 all")
    out["k4_orbits"] = sweep(6, 4, reps, label="N6 k=4 orbit reps")
    out["k3_all"] = sweep(6, 3, cases, label="N6 k=3 all")
    out["k2_all"] = sweep(6, 2, cases, label="N6 k=2 all")
    out["VERDICT_k4_all_unsat"] = out["k4_all"]["n_sat"] == 0
    return out


def run_n8k4():
    cases = all_cases(8)
    reps = orbit_reps(8)
    out = {"n_cases": len(cases), "n_orbits": len(reps)}
    out["orbits"] = sweep(8, 4, reps, label="N8 k=4 orbit reps")
    ck("n8k4-orbits")
    out["all"] = sweep(8, 4, cases, label="N8 k=4 all 4096")
    out["VERDICT_all_unsat"] = out["all"]["n_sat"] == 0
    return out


def run_n8k3():
    cases = all_cases(8)
    out = {"all": sweep(8, 3, cases, label="N8 k=3 all 4096")}
    out["MUST_BE_ALL_SAT"] = out["all"]["n_sat"] == len(cases)
    return out


FAMS = ("A0", "A1", "A2", "A3", "C0", "Cnz", "Ch", "FR", "XF")


def run_ablate():
    reps = orbit_reps(8)
    out = {}
    subsets = {
        "CASE_only": ("A0", "A1", "A2", "A3", "C0", "Cnz", "Ch"),
        "CASE+FREE": ("A0", "A1", "A2", "A3", "C0", "Cnz", "Ch", "FR"),
        "CASE+FREE+XF": FAMS,
        "no_A3": ("A0", "A1", "A2", "C0", "Cnz", "Ch", "FR", "XF"),
        "no_A2": ("A0", "A1", "A3", "C0", "Cnz", "Ch", "FR", "XF"),
        "no_A0": ("A1", "A2", "A3", "C0", "Cnz", "Ch", "FR", "XF"),
        "no_A1": ("A0", "A2", "A3", "C0", "Cnz", "Ch", "FR", "XF"),
        "no_C0": ("A0", "A1", "A2", "A3", "Cnz", "Ch", "FR", "XF"),
        "no_Cnz": ("A0", "A1", "A2", "A3", "C0", "Ch", "FR", "XF"),
        "no_Ch": ("A0", "A1", "A2", "A3", "C0", "Cnz", "FR", "XF"),
        "no_FR": ("A0", "A1", "A2", "A3", "C0", "Cnz", "Ch", "XF"),
        "no_XF": ("A0", "A1", "A2", "A3", "C0", "Cnz", "Ch", "FR"),
    }
    for name, use in subsets.items():
        t0 = time.time()
        nsat = 0
        for Rs in reps:
            e = E.Enc(8, Rs, k=4, use=use).build()
            if e.solve_pysat()[0]:
                nsat += 1
        out[name] = {"n_orbits": len(reps), "n_sat": nsat,
                     "secs": round(time.time() - t0, 1)}
        print(f"   ablate {name}: {nsat}/{len(reps)} SAT", flush=True)
        ck(f"ablate-{name}")
    return out


def run_multi():
    reps = orbit_reps(8)
    out = {}
    for solver in ("cadical195", "minisat22", "glucose42", "maplesat",
                   "lingeling"):
        t0 = time.time()
        nsat = 0
        try:
            for Rs in reps:
                e = E.Enc(8, Rs, k=4).build()
                if e.solve_pysat(solver)[0]:
                    nsat += 1
            out[solver] = {"n_sat": nsat, "n": len(reps),
                           "secs": round(time.time() - t0, 1)}
        except Exception as exc:                                # noqa: BLE001
            out[solver] = {"error": str(exc)[:200]}
        print(f"   solver {solver}: {out[solver]}", flush=True)
        ck(f"multi-{solver}")
    return out


def main():
    what = sys.argv[1:] or ["all"]
    if what == ["all"]:
        what = ["n4", "n6", "n8k3", "n8k4", "ablate", "multi"]
    for w in what:
        RES[w] = {"n4": run_n4, "n6": run_n6, "n8k4": run_n8k4,
                  "n8k3": run_n8k3, "ablate": run_ablate,
                  "multi": run_multi}[w]()
        print(f"== {w}: {json.dumps(RES[w], default=str)[:400]}", flush=True)
        ck(w)
    RES["seconds"] = round(time.time() - T0, 1)
    ck("final")


if __name__ == "__main__":
    main()
