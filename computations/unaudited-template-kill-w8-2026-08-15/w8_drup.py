#!/usr/bin/env python3
"""UNAUDITED PROBE (W8) -- DRUP proofs for the headline UNSAT verdicts.

Pinned HEAD: a1196b4dca9f83452483734a3273c0c43d5cf3b5

The CEGAR adds clauses lazily; each added clause is a logical consequence of
the requirement it encodes (the exact "|fibre(w)| != 1" constraint, or a
kill-certificate nogood that was VERIFIED before it was added).  This script
re-runs an orbit, records EVERY clause, and then re-solves the accumulated
formula from scratch with proof logging, writing

    certificates/w8_m<m>_<mode>_o<orbit>.cnf     (DIMACS, the exact formula)
    certificates/w8_m<m>_<mode>_o<orbit>.drup.gz (cadical's DRUP proof)

so the UNSAT half is machine-checkable.  The clause-generation half is
justified by w8_sat.py / w8_cert.py (and by the controls in w8_sat_control.py
and w8_enc_control.py).

Run: python3 w8_drup.py --m 15 --mode nosingleton [--only 3]
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import sys
import time

import w8_core as C
from pysat.solvers import Solver
from w8_band import solve_orbit_recording
from w8_triples import orbits


def write_cnf(path, clauses, top):
    with gzip.open(path, "wt") as handle:
        handle.write(f"p cnf {top} {len(clauses)}\n")
        for clause in clauses:
            handle.write(" ".join(str(x) for x in clause) + " 0\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--m", type=int, default=15)
    parser.add_argument("--mode", default="nosingleton")
    parser.add_argument("--only", type=int, default=None)
    parser.add_argument("--seconds", type=float, default=900.0)
    parser.add_argument("--outdir", default="certificates")
    args = parser.parse_args()

    geo = C.geometry(8)
    reps = sorted(orbits(geo))
    canonical = geo.matchings.index(tuple((2 * k, 2 * k + 1) for k in range(4)))
    os.makedirs(args.outdir, exist_ok=True)
    rows = []
    for number, (a, b) in enumerate(reps):
        if args.only is not None and number != args.only:
            continue
        start = time.time()
        row, clauses, top = solve_orbit_recording(
            geo, args.m, (canonical, a, b), args.mode, args.seconds)
        if row["status"] != "UNSAT":
            print(f"  orbit {number}: {row['status']} -- no proof emitted",
                  flush=True)
            rows.append({"orbit": number, **row, "proof": None})
            continue
        stem = f"{args.outdir}/w8_m{args.m}_{args.mode}_o{number}"
        write_cnf(stem + ".cnf.gz", clauses, top)
        with Solver(name="cadical153", bootstrap_with=clauses,
                    with_proof=True) as solver:
            verdict = solver.solve()
            proof = solver.get_proof() if verdict is False else None
        if verdict is not False:
            print(f"  orbit {number}: REPLAY DISAGREES ({verdict})", flush=True)
            rows.append({"orbit": number, "status": "replay-disagreement"})
            continue
        with gzip.open(stem + ".drup.gz", "wt") as handle:
            handle.write("\n".join(proof) + "\n")
        size = os.path.getsize(stem + ".drup.gz")
        print(f"  orbit {number}: UNSAT, {len(clauses)} clauses, "
              f"{len(proof)} proof lines, {size/1024:.0f} KB gz "
              f"[{time.time()-start:.1f}s]", flush=True)
        rows.append({"orbit": number, "status": "UNSAT",
                     "clauses": len(clauses), "vars": top,
                     "proof_lines": len(proof), "proof_bytes": size,
                     "rounds": row["rounds"], "verdicts": row["verdicts"]})
    name = f"results_drup_m{args.m}_{args.mode}.json"
    json.dump({"m": args.m, "mode": args.mode, "rows": rows},
              open(name, "w"), indent=1)
    print(f"wrote {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
