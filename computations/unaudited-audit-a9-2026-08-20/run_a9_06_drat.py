#!/usr/bin/env python3
"""A9-06: third-party proof checking of the UNSAT verdicts (link 4).

For every N=8 k=4 orbit representative (87) and every N=6 k=4 case (64):
  external cadical -> DRAT proof -> drat-trim must print "s VERIFIED".

Ledger-5 hazard (a checker that says VERIFIED on anything) is controlled by
three deliberately broken proofs: truncated, corrupted, and cross-case.
"""
from __future__ import annotations

import json
import os
import random
import subprocess
import sys
import time

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-audit-a9-2026-08-20")
if BASE not in sys.path:
    sys.path.insert(0, BASE)
import a9_enc as E                                                   # noqa: E402
import run_a9_03_sat as S                                            # noqa: E402

WORK = f"{BASE}/proofs"
OUT = f"{BASE}/results_a9_06_drat.json"
os.makedirs(WORK, exist_ok=True)
RES = {}
T0 = time.time()


def ck(tag=""):
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print(f"   [ck {tag}] {round(time.time() - T0, 1)}s", flush=True)


def one(n, Rs, k, name):
    e = E.Enc(n, Rs, k=k).build()
    cnf = f"{WORK}/{name}.cnf"
    prf = f"{WORK}/{name}.drat"
    verdict, _ = e.solve_cadical(cnf, prf)
    if verdict != "UNSAT":
        return {"verdict": verdict, "verified": None}
    ok, tail = e.drat_check(cnf, prf)
    return {"verdict": verdict, "verified": ok, "tail": tail,
            "cnf_bytes": os.path.getsize(cnf),
            "proof_bytes": os.path.getsize(prf),
            "vars": e.nv, "clauses": len(e.cls)}


def sweep(n, k, cases, prefix):
    out = {"n": n, "k": k, "n_cases": len(cases), "unsat": 0, "verified": 0,
           "failures": []}
    for i, Rs in enumerate(cases):
        r = one(n, Rs, k, f"{prefix}{i}")
        if r["verdict"] == "UNSAT":
            out["unsat"] += 1
        if r.get("verified"):
            out["verified"] += 1
        else:
            out["failures"].append({"case": [list(x) for x in Rs], **r})
        if i % 20 == 0:
            ck(f"{prefix}{i}")
    out["PASS"] = out["verified"] == len(cases)
    return out


def broken_proof_controls():
    """A checker that verifies anything is useless -- make sure it does not."""
    e = E.Enc(8, ((), (), ()), k=4).build()
    cnf = f"{WORK}/ctrl.cnf"
    prf = f"{WORK}/ctrl.drat"
    v, _ = e.solve_cadical(cnf, prf)
    base_ok, _ = e.drat_check(cnf, prf)
    lines = open(prf).read().splitlines()
    out = {"base_verdict": v, "base_verified": base_ok,
           "proof_lines": len(lines)}
    # (a) truncated proof
    tr = f"{WORK}/ctrl_trunc.drat"
    with open(tr, "w") as fh:
        fh.write("\n".join(lines[:max(1, len(lines) // 2)]) + "\n")
    ok, tail = e.drat_check(cnf, tr)
    out["truncated_verified"] = ok
    # (b) corrupted proof: flip a literal in every 7th lemma
    rng = random.Random(3)
    cor = f"{WORK}/ctrl_corrupt.drat"
    new = []
    for i, ln in enumerate(lines):
        parts = ln.split()
        if i % 7 == 0 and len(parts) > 2 and parts[0] != "d":
            j = rng.randrange(len(parts) - 1)
            parts[j] = str(-int(parts[j]))
        new.append(" ".join(parts))
    with open(cor, "w") as fh:
        fh.write("\n".join(new) + "\n")
    ok2, _ = e.drat_check(cnf, cor)
    out["corrupted_verified"] = ok2
    # (c) cross-case: another case's proof against this CNF
    e2 = E.Enc(8, ((3, 4, 5, 6), (3, 4), (5,)), k=4).build()
    cnf2, prf2 = f"{WORK}/ctrl2.cnf", f"{WORK}/ctrl2.drat"
    e2.solve_cadical(cnf2, prf2)
    ok3, _ = e.drat_check(cnf, prf2)
    out["crosscase_verified"] = ok3
    # (d) a SAT instance must not come back UNSAT
    e3 = E.Enc(8, ((), (), ()), k=3).build()
    v3, _ = e3.solve_cadical(f"{WORK}/ctrl3.cnf", f"{WORK}/ctrl3.drat")
    out["k3_verdict"] = v3
    out["PASS"] = (base_ok and not ok and not ok2 and not ok3
                   and v3 == "SAT")
    return out


def main():
    RES["controls"] = broken_proof_controls()
    print("controls", RES["controls"], flush=True)
    ck("controls")
    RES["n8_k4_orbits"] = sweep(8, 4, S.orbit_reps(8), "n8k4_")
    print("n8", {k: v for k, v in RES["n8_k4_orbits"].items()
                 if k != "failures"}, flush=True)
    ck("n8")
    RES["n6_k4_all"] = sweep(6, 4, S.all_cases(6), "n6k4_")
    print("n6", {k: v for k, v in RES["n6_k4_all"].items()
                 if k != "failures"}, flush=True)
    RES["seconds"] = round(time.time() - T0, 1)
    ck("final")


if __name__ == "__main__":
    main()
