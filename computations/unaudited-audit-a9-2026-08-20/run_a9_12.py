#!/usr/bin/env python3
"""A9-12: N=10 at the TRUE exact level (k=6) + a drat-trim UNSAT core at N=8.
Detached, per-item JSON checkpoints."""
import json, os, random, sys, time
BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-audit-a9-2026-08-20")
sys.path.insert(0, BASE)
import a9_enc as E
import run_a9_03_sat as S
OUT = f"{BASE}/results_a9_12.json"
RES = {"n10_k6": {"k": 6, "items": []}, "cores": {}}
T0 = time.time()
def ck(tag=""):
    RES["seconds"] = round(time.time() - T0, 1)
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print(f"   [ck {tag}] {RES['seconds']}s", flush=True)

# --- drat-trim cores at N=8 (cheap, per case)
for name, Rs in (("singleton", ((), (), ())),
                 ("full", ((3, 4, 5, 6),) * 3),
                 ("mixed", ((3,), (3, 4), (5, 6)))):
    e = E.Enc(8, Rs, k=4).build()
    cnf = f"{BASE}/proofs/core_{name}.cnf"
    prf = f"{BASE}/proofs/core_{name}.drat"
    v, _ = e.solve_cadical(cnf, prf)
    import subprocess
    core = f"{BASE}/proofs/core_{name}.core"
    pr = subprocess.run([E.DRATTRIM, cnf, prf, "-c", core, "-f"],
                        capture_output=True, text=True, timeout=1200)
    ok = "s VERIFIED" in pr.stdout
    ncore = None
    if os.path.exists(core):
        with open(core) as fh:
            ncore = sum(1 for ln in fh if ln.strip() and not ln.startswith("p"))
    # which families the core touches
    RES["cores"][name] = {"verdict": v, "verified": ok,
                          "clauses": len(e.cls), "core_clauses": ncore}
    ck(f"core-{name}")

# --- N=10 at k=6 (EXACT at N=10), orbit reps sampled
reps = S.orbit_reps(10)
rng = random.Random(11)
pick = [reps[0], reps[-1]] + rng.sample(reps, 14)
for i, Rs in enumerate(pick):
    t0 = time.time()
    e = E.Enc(10, Rs, k=6).build()
    sat = e.solve_pysat()[0]
    RES["n10_k6"]["items"].append({"Rs": [list(r) for r in Rs], "sat": sat,
                                   "vars": e.nv, "clauses": len(e.cls),
                                   "secs": round(time.time() - t0, 1)})
    ck(f"n10k6-{i}")
RES["n10_k6"]["n_sat"] = sum(1 for x in RES["n10_k6"]["items"] if x["sat"])
RES["n10_k6"]["n"] = len(RES["n10_k6"]["items"])
ck("final")
