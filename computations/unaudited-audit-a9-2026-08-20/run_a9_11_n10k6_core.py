#!/usr/bin/env python3
"""A9-11: (a) N=10 at the TRUE exact level k=6 (the report's in-flight run is
k=4, which at N=10 is a strict relaxation -- EXACT = X_6 there); (b) a minimal
UNSAT core for the N=8 singleton case, to compare with W29's 361/1226.
"""
from __future__ import annotations

import json
import sys
import time

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-audit-a9-2026-08-20")
if BASE not in sys.path:
    sys.path.insert(0, BASE)
import a9_enc as E                                                   # noqa: E402
import run_a9_03_sat as S                                            # noqa: E402

RES = {}
OUT = f"{BASE}/results_a9_11_n10k6_core.json"
T0 = time.time()


def ck(tag=""):
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print(f"   [ck {tag}] {round(time.time() - T0, 1)}s", flush=True)


def n10_k(k, m=12):
    reps = S.orbit_reps(10)
    import random
    rng = random.Random(11)
    pick = [reps[0], reps[-1]] + rng.sample(reps, m)
    out = {"k": k, "checked": len(pick), "n_sat": 0, "sat_cases": [],
           "secs_each": []}
    for Rs in pick:
        t0 = time.time()
        e = E.Enc(10, Rs, k=k).build()
        sat = e.solve_pysat()[0]
        out["secs_each"].append(round(time.time() - t0, 1))
        out["vars"], out["clauses"] = e.nv, len(e.cls)
        if sat:
            out["n_sat"] += 1
            out["sat_cases"].append([list(r) for r in Rs])
        ck(f"n10k{k}-{len(out['secs_each'])}")
    return out


def min_core(n=8, Rs=((), (), ()), k=4):
    """Deletion-based minimal unsatisfiable subset over the tagged clauses."""
    e = E.Enc(n, Rs, k=k).build()
    cls = [list(c) for c in e.cls]
    tags = list(e.tags)
    from pysat.solvers import Solver

    def unsat(idxs):
        with Solver(name="cadical195",
                    bootstrap_with=[cls[i] for i in idxs]) as So:
            return not So.solve()

    keep = list(range(len(cls)))
    assert unsat(keep)
    i = 0
    while i < len(keep):
        trial = keep[:i] + keep[i + 1:]
        if unsat(trial):
            keep = trial
        else:
            i += 1
    fam = {}
    for i in keep:
        fam[tags[i][0]] = fam.get(tags[i][0], 0) + 1
    return {"case": [list(r) for r in Rs], "total_clauses": len(cls),
            "core_clauses": len(keep), "by_family": fam,
            "verified_unsat": unsat(keep)}


def main():
    what = sys.argv[1:] or ["core", "k6"]
    if "core" in what:
        RES["min_core_singleton"] = min_core()
        print("core", RES["min_core_singleton"], flush=True)
        ck("core")
        RES["min_core_full"] = min_core(Rs=((3, 4, 5, 6),) * 3)
        print("core-full", {k: v for k, v in RES["min_core_full"].items()},
              flush=True)
        ck("core2")
    if "k6" in what:
        RES["n10_k6"] = n10_k(6)
        print("n10k6", {k: v for k, v in RES["n10_k6"].items()
                        if k != "sat_cases"}, flush=True)
        ck("k6")
    RES["seconds"] = round(time.time() - T0, 1)
    ck("final")


if __name__ == "__main__":
    main()
