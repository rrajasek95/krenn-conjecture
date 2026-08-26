#!/usr/bin/env python3
"""Measure the cost of the NO-SYMMETRY route: all 4096 cases, CNF + LRAT.

The 87-orbit route needs a symmetry-transport layer in Lean. The alternative
is to skip it and embed a CNF+LRAT pair for every one of the 4096 cases of the
free-set-triple normal form. This script measures exactly what that would cost
in bytes, so architecture.md can make the call on numbers instead of guesses.

Also measures the SHARED CLAUSE PREFIX across cases, since a shared-prefix
design (as used by algal's krenn-gu-6x3-certificate) changes the CNF side of
the arithmetic substantially.

Checkpointed: appends one JSON line per case to measure_4096.jsonl, so a
machine sleep loses at most one case and the run can resume.
"""
import os, sys, json, subprocess, tempfile, time

ROOT = "/Users/rishi/workplace/krenn-conjecture"
PKG = f"{ROOT}/computations/unaudited-promotion-diag-2026-08-20/certified_package"
WORK = f"{ROOT}/computations/unaudited-lean-l1-2026-08-20/work"
CAD = f"{ROOT}/computations/unaudited-hygiene-h1-2026-08-15/tools/cadical/build/cadical"
sys.path.insert(0, os.path.join(PKG, "encoders"))
sys.path.insert(0, PKG)
import a9_enc as E
import orbit_ledger as L

OUT = os.path.join(WORK, "measure_4096.jsonl")
done = set()
if os.path.exists(OUT):
    for line in open(OUT):
        try:
            done.add(json.loads(line)["idx"])
        except Exception:
            pass

cases = L.all_cases(8)
print(f"cases: {len(cases)}; already done: {len(done)}", flush=True)

tmp = tempfile.mkdtemp(prefix="m4096_")
common = None
t0 = time.time()
with open(OUT, "a") as fh:
    for idx, Rs in enumerate(cases):
        if idx in done:
            continue
        enc = E.Enc(8, Rs, k=4).build()
        cnf_path = os.path.join(tmp, "c.cnf")
        lrat_path = os.path.join(tmp, "c.lrat")
        with open(cnf_path, "w") as f:
            f.write(enc.dimacs())
        r = subprocess.run([CAD, cnf_path, lrat_path, "--lrat=true",
                            "--no-binary", "--checkproof=2"],
                           capture_output=True, text=True)
        rec = {"idx": idx, "case": [list(R) for R in Rs],
               "vars": enc.nv, "clauses": len(enc.cls),
               "rc": r.returncode,
               "cnf_bytes": os.path.getsize(cnf_path),
               "lrat_bytes": os.path.getsize(lrat_path) if os.path.exists(lrat_path) else 0}
        fh.write(json.dumps(rec) + "\n")
        if idx % 50 == 0:
            fh.flush()
            print(f"{idx}/{len(cases)}  {time.time()-t0:.0f}s", flush=True)
        # shared-prefix tracking on the clause multiset
        cs = set(tuple(sorted(c)) for c in enc.cls)
        common = cs if common is None else (common & cs)
        for p in (cnf_path, lrat_path):
            if os.path.exists(p):
                os.unlink(p)

print(f"COMMON CLAUSES ACROSS ALL CASES: {len(common)}", flush=True)
json.dump({"common_clauses": len(common)},
          open(os.path.join(WORK, "measure_4096_common.json"), "w"))
print("DONE", time.time() - t0, flush=True)
