#!/usr/bin/env python3
"""Extract minimal-ish UNSAT cores of the 87 canonical orbit CNFs, and LRAT for them.

UNAUDITED — lane L1. Writes only into the lane directory (`cores/n8z0/`).

WHY
---
Two independent wins, both large:

1. TRUST. `#4659` sets the bar at axiom closure {propext, Classical.choice,
   Quot.sound} — no `native_decide`. Our LRAT replay currently uses
   `native_decide` to execute Lean's verified checker, which adds
   `Lean.ofReduceBool` and `Lean.trustCompiler`. Kernel `decide` on a full
   orbit stack-overflows. A core is ~50x smaller and may be within kernel reach.

2. LEDGER SIZE. The semantic-ledger layer must justify every clause it feeds
   the checker from the nine clause families. Justifying ~250 clauses instead
   of ~13,900 is a proportional saving in the most labour-intensive component
   of the whole project.

SOUNDNESS. The core is a SUBSET of the encoder's clause set, and a subset being
unsatisfiable implies the superset is. So using cores never strengthens the
claim; it only reduces what has to be justified. `core_is_subset` below checks
the subset property explicitly for every orbit, and the driver refuses to
proceed unless all 87 pass.

Usage: python3 emit_cores.py
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time

ROOT = "/Users/rishi/workplace/krenn-conjecture"
LANE = f"{ROOT}/computations/unaudited-lean-l1-2026-08-20"
SRC = f"{LANE}/canonical/n8z0"
OUT = f"{LANE}/cores/n8z0"
CAD = f"{ROOT}/computations/unaudited-hygiene-h1-2026-08-15/tools/cadical/build/cadical"
DT = f"{ROOT}/computations/unaudited-hygiene-h1-2026-08-15/tools/drat-trim/drat-trim"
LC = f"{ROOT}/computations/unaudited-hygiene-h1-2026-08-15/tools/drat-trim/lrat-check"


def read_cnf(path):
    cls = []
    nv = 0
    for line in open(path):
        line = line.strip()
        if not line or line[0] == "c":
            continue
        if line[0] == "p":
            nv = int(line.split()[2])
            continue
        lits = tuple(sorted(int(t) for t in line.split()[:-1]))
        if line.split()[-1] != "0":
            raise SystemExit(f"malformed clause in {path}: {line}")
        cls.append(lits)
    return nv, cls


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    os.makedirs(OUT, exist_ok=True)
    prog = os.path.join(OUT, "PROGRESS.txt")
    recs = []
    t0 = time.time()
    with open(prog, "w") as fh:
        for i in range(87):
            full = f"{SRC}/n8z0k4_{i}.cnf"
            drat = f"{OUT}/tmp_{i}.drat"
            core = f"{OUT}/core_{i}.cnf"
            lrat = f"{OUT}/core_{i}.lrat"
            r1 = subprocess.run([CAD, full, drat, "--no-binary"],
                                capture_output=True, text=True)
            subprocess.run([DT, full, drat, "-c", core],
                           capture_output=True, text=True)
            os.unlink(drat)
            if not os.path.exists(core):
                sys.exit(f"orbit {i}: no core produced")
            r2 = subprocess.run([CAD, core, lrat, "--lrat=true", "--no-binary",
                                 "--checkproof=2"], capture_output=True, text=True)
            lc = subprocess.run([LC, core, lrat], capture_output=True, text=True)
            verified = "VERIFIED" in lc.stdout and "NOT VERIFIED" not in lc.stdout
            # SOUNDNESS GATE: every core clause must occur in the full formula
            nvf, clsf = read_cnf(full)
            nvc, clsc = read_cnf(core)
            setf = set(clsf)
            missing = [c for c in clsc if c not in setf]
            if missing:
                sys.exit(f"orbit {i}: {len(missing)} core clauses NOT in the full CNF")
            rec = {"orbit": i, "full_clauses": len(clsf), "core_clauses": len(clsc),
                   "full_vars": nvf, "cadical_rc": r2.returncode,
                   "lratcheck": verified,
                   "core_bytes": os.path.getsize(core),
                   "lrat_bytes": os.path.getsize(lrat),
                   "core_sha256": sha(core), "lrat_sha256": sha(lrat)}
            recs.append(rec)
            fh.write(f"orbit {i} core={len(clsc)}/{len(clsf)} lrat={rec['lrat_bytes']} "
                     f"rc={r2.returncode} lratcheck={verified} subset=OK\n")
            fh.flush()
            if r2.returncode != 20 or not verified:
                sys.exit(f"orbit {i}: rc={r2.returncode} verified={verified}")
    json.dump(recs, open(f"{OUT}/index.json", "w"), indent=1)
    with open(f"{OUT}/SHA256SUMS.txt", "w") as f:
        for r in recs:
            f.write(f"{r['core_sha256']}  core_{r['orbit']}.cnf\n")
            f.write(f"{r['lrat_sha256']}  core_{r['orbit']}.lrat\n")
    tc = sum(r["core_bytes"] for r in recs)
    tl = sum(r["lrat_bytes"] for r in recs)
    cc = sum(r["core_clauses"] for r in recs)
    print(f"DONE 87 orbits in {time.time()-t0:.1f}s")
    print(f"core clauses: total {cc}, min {min(r['core_clauses'] for r in recs)}, "
          f"max {max(r['core_clauses'] for r in recs)}, "
          f"mean {cc//87}  (full: {recs[0]['full_clauses']}-ish each)")
    print(f"payload: cores {tc/2**20:.3f} MiB + lrat {tl/2**20:.3f} MiB "
          f"= {(tc+tl)/2**20:.3f} MiB")
    print(f"all rc==20: {all(r['cadical_rc']==20 for r in recs)}; "
          f"all lrat-check verified: {all(r['lratcheck'] for r in recs)}; "
          f"all cores are subsets of their full CNF: True")


if __name__ == "__main__":
    main()
