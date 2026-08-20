#!/usr/bin/env python3
"""Regenerate, solve and proof-check the N = 8 case ledger.

For every one of the 87 S_Q x S_3 orbit representatives of the free-set-triple
normal form (Theorem 3.3 / Proposition 4.1 of
`proofs/eight-site-diagonal-obstruction.md`) this script

  1. rebuilds the CNF with the audit encoder `encoders/a9_enc.py` at level
     k = 4 (= EXACT at N = 8, Lemma 2.3),
  2. solves it with an external CaDiCaL, emitting a solver-native DRAT proof,
  3. verifies that proof with drat-trim, requiring the literal string
     "s VERIFIED" on stdout,

and refuses to report success unless all 87 come back UNSAT and VERIFIED.

Three deliberately broken proofs are checked first (ledger item 5: a checker
that accepts anything is worthless) -- truncated, corrupted, and cross-case --
and all three must be REJECTED.  A k = 3 instance must come back SAT.

Solver binaries default to the H1-built pair; override with the environment
variables CADICAL and DRATTRIM.

Usage
-----
    python3 replay_orbits.py [--mode all|orbits|controls|n6] [--out FILE]
                             [--work DIR] [--limit N] [--keep]

Exit status is 0 only when every requested check passes.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "encoders"))
import a9_enc as E                                                # noqa: E402

DEFAULT_TOOLS = ("/Users/rishi/workplace/krenn-conjecture/computations/"
                 "unaudited-hygiene-h1-2026-08-15/tools")
CADICAL = os.environ.get("CADICAL", f"{DEFAULT_TOOLS}/cadical/build/cadical")
DRATTRIM = os.environ.get("DRATTRIM", f"{DEFAULT_TOOLS}/drat-trim/drat-trim")
E.CADICAL = CADICAL
E.DRATTRIM = DRATTRIM

sys.path.insert(0, HERE)
import orbit_ledger as L                                          # noqa: E402


def require(cond, detail):
    if not cond:
        raise AssertionError(detail)


def tool_banner():
    def ver(cmd, args):
        try:
            p = subprocess.run([cmd] + args, capture_output=True, text=True,
                               timeout=30)
            return (p.stdout + p.stderr).strip().splitlines()[0][:120]
        except Exception as exc:                                  # noqa: BLE001
            return f"<unavailable: {exc}>"
    return {"cadical_path": CADICAL, "cadical_version": ver(CADICAL,
                                                            ["--version"]),
            "drat_trim_path": DRATTRIM,
            "drat_trim_present": os.path.exists(DRATTRIM),
            "python": sys.version.split()[0]}


def one_case(n, Rs, k, work, name, keep):
    enc = E.Enc(n, Rs, k=k).build()
    cnf = os.path.join(work, f"{name}.cnf")
    drat = os.path.join(work, f"{name}.drat")
    verdict, _ = enc.solve_cadical(cnf, drat)
    rec = {"case": [list(R) for R in Rs], "verdict": verdict,
           "vars": enc.nv, "clauses": len(enc.cls)}
    if verdict == "UNSAT":
        ok, tail = enc.drat_check(cnf, drat)
        rec["drat_verified"] = ok
        rec["drat_tail"] = tail
        rec["cnf_bytes"] = os.path.getsize(cnf)
        rec["drat_bytes"] = os.path.getsize(drat)
    if not keep:
        for path in (cnf, drat):
            if os.path.exists(path):
                os.unlink(path)
    return rec


def run_controls(work):
    """Ledger item 5 / ledger item 16: the checker must reject bad proofs."""
    enc = E.Enc(8, ((), (), ()), k=4).build()
    cnf = os.path.join(work, "ctrl.cnf")
    drat = os.path.join(work, "ctrl.drat")
    verdict, _ = enc.solve_cadical(cnf, drat)
    base_ok, _ = enc.drat_check(cnf, drat)
    lines = open(drat).read().splitlines()
    out = {"base_verdict": verdict, "base_verified": base_ok,
           "proof_lines": len(lines)}

    trunc = os.path.join(work, "ctrl_trunc.drat")
    with open(trunc, "w") as fh:
        fh.write("\n".join(lines[:max(1, len(lines) // 2)]) + "\n")
    out["truncated_verified"], _ = enc.drat_check(cnf, trunc)

    rng = random.Random(3)
    corrupt = os.path.join(work, "ctrl_corrupt.drat")
    new = []
    for i, line in enumerate(lines):
        parts = line.split()
        if i % 7 == 0 and len(parts) > 2 and parts[0] != "d":
            j = rng.randrange(len(parts) - 1)
            parts[j] = str(-int(parts[j]))
        new.append(" ".join(parts))
    with open(corrupt, "w") as fh:
        fh.write("\n".join(new) + "\n")
    out["corrupted_verified"], _ = enc.drat_check(cnf, corrupt)

    other = E.Enc(8, ((3, 4, 5, 6), (3, 4), (5,)), k=4).build()
    cnf2 = os.path.join(work, "ctrl2.cnf")
    drat2 = os.path.join(work, "ctrl2.drat")
    other.solve_cadical(cnf2, drat2)
    out["crosscase_verified"], _ = enc.drat_check(cnf, drat2)

    sat_probe = E.Enc(8, ((), (), ()), k=3).build()
    out["k3_verdict"], _ = sat_probe.solve_cadical(
        os.path.join(work, "ctrl3.cnf"), os.path.join(work, "ctrl3.drat"))

    out["PASS"] = (out["base_verdict"] == "UNSAT" and out["base_verified"]
                   and not out["truncated_verified"]
                   and not out["corrupted_verified"]
                   and not out["crosscase_verified"]
                   and out["k3_verdict"] == "SAT")
    return out


def run_sweep(n, k, cases, work, prefix, keep, label):
    out = {"n": n, "k": k, "label": label, "n_cases": len(cases),
           "unsat": 0, "verified": 0, "failures": [], "cases": []}
    t0 = time.time()
    for i, Rs in enumerate(cases):
        rec = one_case(n, Rs, k, work, f"{prefix}{i}", keep)
        rec["index"] = i
        out["cases"].append(rec)
        if rec["verdict"] == "UNSAT":
            out["unsat"] += 1
        if rec.get("drat_verified"):
            out["verified"] += 1
        else:
            out["failures"].append(rec)
        if i % 10 == 0:
            print(f"   [{label} {i}/{len(cases)}] "
                  f"{round(time.time() - t0, 1)}s", flush=True)
    out["secs"] = round(time.time() - t0, 1)
    out["PASS"] = (out["unsat"] == len(cases)
                   and out["verified"] == len(cases))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="all",
                    choices=("all", "orbits", "controls", "n6"))
    ap.add_argument("--out", default=os.path.join(HERE, "replay_results.json"))
    ap.add_argument("--work", default=os.path.join(HERE, "replay_work"))
    ap.add_argument("--limit", type=int, default=0,
                    help="only the first N orbits (smoke test)")
    ap.add_argument("--keep", action="store_true",
                    help="keep the regenerated CNF/DRAT files")
    args = ap.parse_args()
    os.makedirs(args.work, exist_ok=True)

    res = {"tools": tool_banner(), "mode": args.mode,
           "started": time.strftime("%Y-%m-%dT%H:%M:%S")}
    require(os.path.exists(CADICAL), f"cadical not found at {CADICAL}")
    require(os.path.exists(DRATTRIM), f"drat-trim not found at {DRATTRIM}")

    def flush(tag):
        with open(args.out, "w") as fh:
            json.dump(res, fh, indent=1, default=str)
        print(f"   [checkpoint {tag}]", flush=True)

    if args.mode in ("all", "controls"):
        res["controls"] = run_controls(args.work)
        print("controls:", {k: v for k, v in res["controls"].items()
                            if k != "proof_lines"}, flush=True)
        flush("controls")

    if args.mode in ("all", "orbits"):
        reps = [trip for trip, _ in L.orbit_reps(8)]
        require(len(reps) == 87, f"expected 87 orbits, got {len(reps)}")
        if args.limit:
            reps = reps[:args.limit]
        res["n8_k4_orbits"] = run_sweep(8, 4, reps, args.work, "n8k4_",
                                        args.keep, "N8 k=4 orbits")
        print("N8:", {k: v for k, v in res["n8_k4_orbits"].items()
                      if k not in ("cases", "failures")}, flush=True)
        flush("n8")

    if args.mode in ("all", "n6"):
        cases = L.all_cases(6)
        require(len(cases) == 64, f"expected 64 cases, got {len(cases)}")
        if args.limit:
            cases = cases[:args.limit]
        res["n6_k4_all"] = run_sweep(6, 4, cases, args.work, "n6k4_",
                                     args.keep, "N6 k=4 all")
        print("N6:", {k: v for k, v in res["n6_k4_all"].items()
                      if k not in ("cases", "failures")}, flush=True)
        flush("n6")

    blocks = [v for k, v in res.items()
              if isinstance(v, dict) and "PASS" in v]
    res["ALL_PASS"] = bool(blocks) and all(b["PASS"] for b in blocks)
    flush("final")
    print("ALL_PASS =", res["ALL_PASS"])
    return 0 if res["ALL_PASS"] else 1


if __name__ == "__main__":
    sys.exit(main())
