#!/usr/bin/env python3
"""W29 D5 -- a THIRD, third-party proof check with drat-trim (found on this
machine at unaudited-hygiene-h1-2026-08-15/tools/drat-trim).  Nothing outside
this directory is written: the CNF and the DRUP proof are emitted here and the
binary is only executed.  Ledger 16: the checker's proof system must match the
solver's, so the proof is produced by glucose42 (no inprocessing => pure RUP,
which drat-trim covers).
"""
import json, subprocess, sys, time
BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-diagclose-w29-2026-08-19")
DRAT = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-hygiene-h1-2026-08-15/tools/drat-trim/drat-trim")
sys.path.insert(0, BASE)
import run_c2_unified as U
import run_h1_higher as H
from pysat.solvers import Solver
n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
nmax = int(sys.argv[2]) if len(sys.argv) > 2 else 6
OUT = f"{BASE}/results_d5_drat_n{n}.json"
RES = {"n": n, "checker": DRAT, "orbits": {}}
Q = tuple(range(3, n - 1))
profs = H.profiles(len(Q))
t0 = time.time()
nver = 0
for i, pr in enumerate(profs[:nmax]):
    Rs = H.triple_of(pr, Q)
    van = U.build_van(n, Rs, z=n - 1)
    cls = [list(c) for c in van.cls]
    with Solver(name="glucose42", bootstrap_with=cls, with_proof=True) as S:
        sat = S.solve(); proof = S.get_proof()
    cnf = f"{BASE}/tmp_d5_n{n}_{i}.cnf"; drp = f"{BASE}/tmp_d5_n{n}_{i}.drup"
    with open(cnf, "w") as fh:
        fh.write(f"p cnf {van.nvars} {len(cls)}\n")
        for c in cls:
            fh.write(" ".join(map(str, c)) + " 0\n")
    with open(drp, "w") as fh:
        for ln in proof:
            fh.write(ln.rstrip() + "\n" if ln.rstrip().endswith("0")
                     else ln.rstrip() + " 0\n")
    p = subprocess.run([DRAT, cnf, drp], capture_output=True, text=True,
                       timeout=1800)
    ok = "s VERIFIED" in p.stdout
    nver += ok
    RES["orbits"][str([list(r) for r in Rs])] = {
        "solver_sat": sat, "drat_trim_VERIFIED": ok,
        "tail": p.stdout.strip().splitlines()[-1:] }
    print(f"  orbit {i} Rs={[list(r) for r in Rs]}: sat={sat} "
          f"drat-trim VERIFIED={ok}", flush=True)
    import os
    os.unlink(cnf); os.unlink(drp)
    json.dump(RES, open(OUT, "w"), indent=1, default=str)
RES["n_checked"] = min(nmax, len(profs)); RES["n_verified"] = nver
RES["secs"] = round(time.time()-t0, 1)
json.dump(RES, open(OUT, "w"), indent=1, default=str)
print(f">>> drat-trim verified {nver}/{RES['n_checked']} orbits")
