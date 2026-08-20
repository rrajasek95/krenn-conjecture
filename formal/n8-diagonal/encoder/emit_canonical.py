#!/usr/bin/env python3
"""Emit the canonical-numbering CNF + native LRAT for the Lean pipeline.

UNAUDITED — lane L1. Writes ONLY into the lane directory
(`canonical/n8/`, `canonical/n6/`). The committed
`unaudited-promotion-diag-2026-08-20/certified_package/` is not touched.

For each orbit representative:
  1. build the CNF with the canonical variable numbering (`l1_enc.CanonEnc`),
  2. check it is the audit encoder's clause set under the variable bijection,
  3. solve with CaDiCaL emitting native LRAT (`--lrat=true --checkproof=2`),
     which is the only LRAT dialect Lean's checker accepts (see feasibility.md),
  4. re-check the LRAT independently with drat-trim's `lrat-check`,
  5. write a varmap and a gate table for the Lean ledger layer.

Single process, checkpointed one line per orbit to PROGRESS.txt, so a machine
sleep loses at most one orbit and a rerun resumes.

Usage:  python3 emit_canonical.py 8 | 6
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
ROOT = "/Users/rishi/workplace/krenn-conjecture"
PKG = f"{ROOT}/computations/unaudited-promotion-diag-2026-08-20/certified_package"
CAD = f"{ROOT}/computations/unaudited-hygiene-h1-2026-08-15/tools/cadical/build/cadical"
LC = f"{ROOT}/computations/unaudited-hygiene-h1-2026-08-15/tools/drat-trim/lrat-check"

sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(PKG, "encoders"))
sys.path.insert(0, PKG)
import l1_enc as L1  # noqa: E402
import orbit_ledger as LED  # noqa: E402


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main(n, z0=False):
    k = 4
    tag = f"n{n}z0" if z0 else f"n{n}"
    out = os.path.join(LANE, "canonical", tag)
    os.makedirs(out, exist_ok=True)
    prog = os.path.join(out, "PROGRESS.txt")
    done = set()
    if os.path.exists(prog):
        for line in open(prog):
            if line.startswith("orbit "):
                done.add(int(line.split()[1]))

    z = 0 if z0 else n - 1
    ys = (1, 2, 3) if z0 else (0, 1, 2)
    VP = [x for x in range(n) if x != z]
    Q = [x for x in VP if x not in ys]
    ren = dict(zip(range(3, n - 1), Q))
    reps = [tuple(tuple(sorted(ren[q] for q in R)) for R in t)
            for t, _ in LED.orbit_reps(n)]
    sizes = [sz for _, sz in LED.orbit_reps(n)]
    assert sum(sizes) == 8 ** (n - 4), (sum(sizes), 8 ** (n - 4))
    print(f"n={n}: {len(reps)} orbits, sizes sum {sum(reps and sizes)} "
          f"= 8^{n-4} = {8**(n-4)}; already done {len(done)}", flush=True)

    recs = []
    t0 = time.time()
    with open(prog, "a") as fh:
        for i, Rs in enumerate(reps):
            base = os.path.join(out, f"{tag}k{k}_{i}")
            cnf, lrat = base + ".cnf", base + ".lrat"
            if i in done and os.path.exists(cnf) and os.path.exists(lrat):
                continue
            ok, msg = (True, "skip") if z0 else L1.verify_equivalence(n, Rs, k)
            if not ok:
                fh.write(f"orbit {i} EQUIV_FAIL {msg}\n")
                fh.flush()
                sys.exit(f"equivalence failed at orbit {i}: {msg}")
            enc = L1.CanonEnc(n, Rs, k=k, z=z, ys=ys).build()
            with open(cnf, "w") as f:
                f.write(enc.dimacs())
            with open(base + ".varmap", "w") as f:
                f.write("\n".join(enc.varmap_lines()) + "\n")
            r = subprocess.run(
                [CAD, cnf, lrat, "--lrat=true", "--no-binary", "--checkproof=2"],
                capture_output=True, text=True)
            lcok = subprocess.run([LC, cnf, lrat], capture_output=True, text=True)
            verified = "VERIFIED" in lcok.stdout and "NOT VERIFIED" not in lcok.stdout
            rec = {"orbit": i, "case": [list(R) for R in Rs],
                   "orbit_size": sizes[i],
                   "vars": enc.nv, "base_vars": enc.n_base,
                   "gates": enc.nv - enc.n_base,
                   "clauses": len(enc.cls), "cadical_rc": r.returncode,
                   "lratcheck": verified,
                   "cnf_bytes": os.path.getsize(cnf),
                   "lrat_bytes": os.path.getsize(lrat),
                   "cnf_sha256": sha(cnf), "lrat_sha256": sha(lrat)}
            recs.append(rec)
            fh.write(f"orbit {i} rc={r.returncode} vars={enc.nv} base={enc.n_base} "
                     f"clauses={len(enc.cls)} lrat={rec['lrat_bytes']} "
                     f"lratcheck={verified}\n")
            fh.flush()
            if r.returncode != 20 or not verified:
                sys.exit(f"orbit {i}: rc={r.returncode} lratcheck={verified}")
    dt = time.time() - t0
    idx = os.path.join(out, "index.json")
    old = json.load(open(idx)) if os.path.exists(idx) else []
    byorb = {r["orbit"]: r for r in old}
    for r in recs:
        byorb[r["orbit"]] = r
    allrecs = [byorb[i] for i in sorted(byorb)]
    json.dump(allrecs, open(idx, "w"), indent=1)
    with open(os.path.join(out, "SHA256SUMS.txt"), "w") as f:
        for r in allrecs:
            f.write(f"{r['cnf_sha256']}  {tag}k{k}_{r['orbit']}.cnf\n")
            f.write(f"{r['lrat_sha256']}  {tag}k{k}_{r['orbit']}.lrat\n")
    tot_c = sum(r["cnf_bytes"] for r in allrecs)
    tot_l = sum(r["lrat_bytes"] for r in allrecs)
    print(f"DONE n={n}: {len(allrecs)} orbits in {dt:.1f}s; "
          f"cnf {tot_c/2**20:.2f} MiB, lrat {tot_l/2**20:.2f} MiB, "
          f"combined {(tot_c+tot_l)/2**20:.2f} MiB", flush=True)
    print(f"all rc==20: {all(r['cadical_rc']==20 for r in allrecs)}; "
          f"all lrat-check verified: {all(r['lratcheck'] for r in allrecs)}", flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 8,
         z0=(len(sys.argv) > 2 and sys.argv[2] == "z0"))
