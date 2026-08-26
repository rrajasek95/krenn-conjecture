#!/usr/bin/env python3
"""W29 D4 -- RUP-verify the UNSAT of EVERY orbit of the N=8 ledger.

For each of the 87 profile orbits: build the unified abstraction, get a DRUP
proof from glucose42 (no inprocessing, so the proof is pure RUP), and replay
every lemma with the checker written in run_d3_rup -- which is itself
controlled (accepts a valid proof, rejects an invalid one, and detects a
TRUNCATED one, the ledger-5 hazard).
"""
import json, sys, time
BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-diagclose-w29-2026-08-19")
sys.path.insert(0, BASE)
import run_c2_unified as U
import run_h1_higher as H
from run_d3_rup import rup_check
from pysat.solvers import Solver
n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
OUT = f"{BASE}/results_d4_rupall_n{n}.json"
RES = {"n": n, "orbits": {}}
# checker control, re-run here so it cannot be skipped (ledger 21)
tiny = [[1, 2], [-1, 2], [1, -2], [-1, -2]]
RES["checker_control"] = {
    "valid_proof_accepted": rup_check(tiny, [[2], [-2], []]) == (True, True),
    "invalid_proof_rejected": rup_check(tiny, [[3], []])[0] is False,
    "truncated_proof_detected": rup_check(tiny, [[2]]) == (True, False)}
assert all(RES["checker_control"].values()), RES["checker_control"]
print(f"[checker control] {RES['checker_control']}", flush=True)
Q = tuple(range(3, n - 1))
profs = H.profiles(len(Q))
t0 = time.time()
nbad = 0
for i, pr in enumerate(profs):
    Rs = H.triple_of(pr, Q)
    van = U.build_van(n, Rs, z=n - 1)
    cls = [list(c) for c in van.cls]
    with Solver(name="glucose42", bootstrap_with=cls, with_proof=True) as S:
        sat = S.solve(); proof = S.get_proof()
    lem = []
    for ln in proof:
        t = ln.split()
        if t and t[0] == "d": continue
        if t and t[-1] == "0": t = t[:-1]
        lem.append([int(x) for x in t])
    ok, empty = rup_check(cls, lem)
    good = (sat is False) and ok and empty
    if not good: nbad += 1
    RES["orbits"][str([list(r) for r in Rs])] = {
        "sat": sat, "n_lemmas": len(lem), "all_RUP": ok,
        "empty_clause": empty, "VERIFIED_UNSAT": good}
    if (i + 1) % 10 == 0 or not good:
        print(f"  ... {i+1}/{len(profs)} orbits, {nbad} not verified "
              f"({round(time.time()-t0,1)}s)", flush=True)
        json.dump(RES, open(OUT, "w"), indent=1, default=str)
RES["n_orbits"] = len(profs)
RES["n_not_verified"] = nbad
RES["VERDICT"] = ("ALL ORBITS RUP-VERIFIED UNSAT" if nbad == 0
                  else f"{nbad} orbits NOT verified")
RES["secs"] = round(time.time() - t0, 1)
json.dump(RES, open(OUT, "w"), indent=1, default=str)
print(">>> " + RES["VERDICT"] + f" ({RES['secs']}s)")
