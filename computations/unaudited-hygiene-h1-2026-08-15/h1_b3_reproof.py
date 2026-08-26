#!/usr/bin/env python3
"""H1 / BLOCKER 3 step (c) -- SOLVER-NATIVE re-proof of a failing orbit.

UNAUDITED.  Hygiene agent H1, 2026-08-15.

When a stored proof fails to replay, the stored artifact is discarded and
the orbit is re-decided from its CNF by running **cadical as a binary with
a proof-file argument** -- never through `pysat`'s `get_proof()`, which is
the truncation hazard of ledger item 5 that produced the failure in the
first place.  The fresh proof is then replayed with drat-trim (the same
DRAT-capable checker used for the originals, ledger item 16) and stored
here as the verified replacement.

The CNF is NOT regenerated: it is the byte-for-byte formula W8 stored, so
the replacement certifies exactly the statement the original claimed.  If
cadical returns SAT the orbit's kill is REFUTED, and that is reported as
such rather than papered over.

Usage:  python3 h1_b3_reproof.py <orbit> [<orbit> ...]
Writes  reproofs/w8_m17_closure_o<K>.cadical.drat.gz
        results_b3_reproof.json
"""

from __future__ import annotations

import gzip
import json
import os
import re
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CADICAL = os.path.join(HERE, "tools", "cadical", "build", "cadical")
DRAT = os.path.join(HERE, "tools", "drat-trim", "drat-trim")
CERTS = os.path.join(ROOT, "computations",
                     "unaudited-template-kill-w8-2026-08-15", "certificates")
OUTDIR = os.path.join(HERE, "reproofs")
SCRATCH = os.environ.get(
    "H1_SCRATCH",
    "/private/tmp/claude-501/-Users-rishi/f8396279-dd28-41de-876d-5c03a4d8d65a/scratchpad/reproof")


class CheckFailure(Exception):
    pass


def require(cond, msg):
    if not cond:
        raise CheckFailure(msg)


def gunzip(src, dst):
    with gzip.open(src, "rb") as fi, open(dst, "wb") as fo:
        shutil.copyfileobj(fi, fo, 1 << 22)


def gzip_to(src, dst):
    with open(src, "rb") as fi, gzip.open(dst, "wb") as fo:
        shutil.copyfileobj(fi, fo, 1 << 22)


def reproof(orbit):
    os.makedirs(SCRATCH, exist_ok=True)
    os.makedirs(OUTDIR, exist_ok=True)
    base = f"w8_m17_closure_o{orbit}"
    cnf_gz = os.path.join(CERTS, base + ".cnf.gz")
    require(os.path.exists(cnf_gz), f"missing {cnf_gz}")
    cnf = os.path.join(SCRATCH, base + ".cnf")
    proof = os.path.join(SCRATCH, base + ".cadical.drat")
    rec = {"orbit": orbit, "cnf_src": cnf_gz,
           "solver": "cadical (binary, --no-binary DRAT proof file argument)"}
    try:
        gunzip(cnf_gz, cnf)
        # --- SOLVER-NATIVE: cadical writes the proof itself.
        t0 = time.time()
        p = subprocess.run([CADICAL, "--no-binary", cnf, proof],
                           capture_output=True, text=True, timeout=7200)
        rec["solve_s"] = round(time.time() - t0, 2)
        rec["cadical_returncode"] = p.returncode      # 10 = SAT, 20 = UNSAT
        out = p.stdout + p.stderr
        sat = bool(re.search(r"^s SATISFIABLE", out, re.M))
        unsat = bool(re.search(r"^s UNSATISFIABLE", out, re.M))
        rec["cadical_verdict"] = ("SAT" if sat else
                                  "UNSAT" if unsat else "UNKNOWN")
        rec["cadical_tail"] = [l for l in out.strip().splitlines()
                               if l.startswith("s ") or "conflicts" in l][-4:]
        if not unsat:
            rec["result"] = "ORBIT KILL REFUTED OR UNDECIDED"
            return rec
        rec["proof_bytes"] = os.path.getsize(proof)
        with open(proof) as fh:
            n = 0
            last = ""
            for n, last in enumerate(fh, 1):
                pass
        rec["proof_lines"] = n
        rec["proof_last_line"] = repr(last[-40:])
        rec["terminates_in_empty_clause"] = last.strip() == "0"
        # --- replay the FRESH proof with the same checker
        t0 = time.time()
        q = subprocess.run([DRAT, cnf, proof, "-t", "3600"],
                           capture_output=True, text=True, timeout=3900)
        rec["replay_s"] = round(time.time() - t0, 2)
        rout = q.stdout + q.stderr
        rec["replay_verified"] = bool(re.search(r"^s VERIFIED", rout, re.M))
        m = re.search(r"c (\d+) RAT lemmas in core", rout)
        rec["rat_lemmas_in_core"] = int(m.group(1)) if m else None
        rec["replay_tail"] = rout.strip().splitlines()[-6:]
        rec["result"] = ("REPLACEMENT VERIFIED" if rec["replay_verified"]
                         else "REPLACEMENT FAILED TO REPLAY")
        if rec["replay_verified"]:
            dst = os.path.join(OUTDIR, base + ".cadical.drat.gz")
            gzip_to(proof, dst)
            rec["stored"] = os.path.relpath(dst, ROOT)
            rec["stored_bytes"] = os.path.getsize(dst)
    except Exception as exc:                             # noqa: BLE001
        rec["result"] = "ERROR"
        rec["error"] = f"{type(exc).__name__}: {exc}"
    finally:
        for p_ in (cnf, proof):
            if os.path.exists(p_):
                os.remove(p_)
    return rec


def main():
    orbits = [int(x) for x in sys.argv[1:]] or [13]
    out = {"agent": "H1", "blocker": "3c-solver-native-reproof",
           "pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")
                               ).read().split()[0],
           "cadical": CADICAL, "checker": DRAT, "orbits": {}}
    for k in orbits:
        print(f"=== orbit {k}: re-solving solver-native with cadical ===",
              flush=True)
        r = reproof(k)
        out["orbits"][str(k)] = r
        print(f"    cadical: {r.get('cadical_verdict')} in "
              f"{r.get('solve_s')}s; proof {r.get('proof_lines')} lines; "
              f"replay VERIFIED={r.get('replay_verified')} in "
              f"{r.get('replay_s')}s -> {r.get('result')}", flush=True)
    with open(os.path.join(HERE, "results_b3_reproof.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print("wrote results_b3_reproof.json")


if __name__ == "__main__":
    main()
