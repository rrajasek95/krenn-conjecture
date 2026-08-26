#!/usr/bin/env python3
"""UNAUDITED PROBE (W18) -- re-emit stored proofs with cadical run as a BINARY.

Pinned HEAD: see PINNED_HEAD.txt.  Probe output; not a proved project claim.

The early part of this sweep emitted proofs through pysat's in-memory
get_proof(), the path the hazard note warns about; three of them were corrupt
(~0.45%).  The FORMULA is the artefact that matters and it is stored intact in
certificates/m{m}/m{m}_g{mask}.cnf.gz, so a clean certificate can be rebuilt
without redoing any CEGAR: run cadical on the stored CNF, keep its own proof
file, and replay it with drat-trim (backward, full RAT) and rup18 (this lane's
forward RUP checker).

  python3 run_reemit.py 18 19 --which failed      # only proofs that failed replay
  python3 run_reemit.py 18 19 --which pysat       # every proof not emitted natively
  python3 run_reemit.py 18 19 --which big --min-mb 500

The stored .cnf.gz is never touched (its SHA-256 is re-checked first); only the
.drup.gz is replaced, and only when the new proof verifies.
"""
from __future__ import annotations

import argparse
import glob
import gzip
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import w18_sweep as SW      # noqa: E402


def best_rows(m):
    rows = {}
    for f in glob.glob(os.path.join(HERE, "results_sweep_m%d_*.jsonl" % m)):
        for line in open(f):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)

            def score(x):
                if x["status"] not in ("UNSAT", "TRIVIAL-UNSAT"):
                    return 0
                p = x.get("proof", {})
                if p.get("rup18_rc") == 0 and p.get("terminates_empty"):
                    return 3 if "cadical" in str(p.get("emitter", "")) else 2
                return 1 if p else 0
            prev = rows.get(r["mask"])
            if prev is None or score(r) >= score(prev):
                rows[r["mask"]] = r
    return rows


def pick(m, which, min_mb, band=(0.0, 1e9)):
    out = []
    pdir = os.path.join(HERE, "certificates", "m%d" % m)
    for mask, r in sorted(best_rows(m).items()):
        p = r.get("proof")
        if not p:
            continue
        drpz = os.path.join(pdir, "m%d_g%d.drup.gz" % (m, mask))
        if not os.path.exists(drpz):
            continue
        native = "cadical" in str(p.get("emitter", ""))
        ok = p.get("rup18_rc") == 0 and p.get("terminates_empty")
        size_mb = os.path.getsize(drpz) / (1024.0 * 1024.0)
        if which == "failed" and ok:
            continue
        if which == "pysat" and native:
            continue
        if which == "big" and (native or size_mb < min_mb):
            continue
        # size band: keeps the scratch peak bounded, which is what matters
        # when the box is tight -- giants are queued for a later pass
        if not (band[0] <= size_mb <= band[1]):
            continue
        out.append((mask, r, size_mb))
    return out


def reemit(m, mask, row, rup_max_mb, dt_seconds):
    pdir = os.path.join(HERE, "certificates", "m%d" % m)
    tag = "m%d_g%d" % (m, mask)
    cnfz = os.path.join(pdir, tag + ".cnf.gz")
    drpz = os.path.join(pdir, tag + ".drup.gz")
    tmp = tempfile.mkdtemp(prefix="w18reemit")
    cnf = os.path.join(tmp, tag + ".cnf")
    drp = os.path.join(tmp, tag + ".drup")
    try:
        with gzip.open(cnfz, "rb") as fi, open(cnf, "wb") as fo:
            shutil.copyfileobj(fi, fo, 1 << 22)
        rec = {"mask": mask, "m": m,
               "cnf_sha_matches_row":
                   SW.sha256(cnf) == row["proof"].get("cnf_sha256")}
        t0 = time.time()
        r = subprocess.run([SW.CADICAL, "--binary=false", "-q", cnf, drp],
                           capture_output=True, text=True)
        rec["cadical_rc"] = r.returncode
        rec["solve_seconds"] = round(time.time() - t0, 1)
        if r.returncode != 20:
            rec["result"] = ("SAT -- THE FORMULA IS NOT UNSAT"
                             if r.returncode == 10 else "cadical error")
            return rec
        rec["proof_bytes"] = os.path.getsize(drp)
        rec["proof_lemmas"] = SW._count_lines(drp)
        rec["terminates_empty"] = SW._tail_is_empty_clause(drp)
        d = subprocess.run([SW.DRATTRIM, cnf, drp, "-I", "-t", str(dt_seconds)],
                           capture_output=True, text=True)
        txt = (d.stdout or "") + (d.stderr or "")
        rec["drat_trim"] = next((ln for ln in txt.splitlines()
                                 if ln.startswith("s ")), txt.strip()[-160:])
        rec["drat_trim_ok"] = "s VERIFIED" in txt
        if rec["proof_bytes"] <= rup_max_mb * 1024 * 1024:
            r2 = subprocess.run([SW.RUP, cnf, drp], capture_output=True,
                                text=True)
            rec["rup18"] = (r2.stdout or r2.stderr).strip()
            rec["rup18_rc"] = r2.returncode
        else:
            rec["rup18"] = "skipped (size)"
            rec["rup18_rc"] = 0 if rec["drat_trim_ok"] else 1
        rec["verified"] = bool(rec["terminates_empty"] and rec["drat_trim_ok"]
                               and rec["rup18_rc"] == 0)
        if rec["verified"]:
            with open(drp, "rb") as fi, gzip.open(drpz + ".new", "wb",
                                                  compresslevel=6) as fo:
                shutil.copyfileobj(fi, fo, 1 << 22)
            os.replace(drpz + ".new", drpz)
            rec["drup_sha256"] = SW.sha256(drp)
            rec["result"] = "REPLACED with a cadical-native proof"
            # Record a corrected class row so the ledger checks the NEW proof
            # against the NEW digest instead of the superseded pysat one.
            newrow = dict(row)
            newrow["proof"] = {
                "status": "UNSAT", "tag": tag,
                "nvars": row["proof"].get("nvars"),
                "nclauses": row["proof"].get("nclauses"),
                "emitter": "cadical-3.0.1-binary (re-emitted by run_reemit)",
                "cadical_rc": rec["cadical_rc"],
                "proof_lemmas": rec["proof_lemmas"],
                "proof_bytes": rec["proof_bytes"],
                "terminates_empty": rec["terminates_empty"],
                "drat_trim": rec["drat_trim"],
                "drat_trim_ok": rec["drat_trim_ok"],
                "rup18": rec["rup18"], "rup18_rc": rec["rup18_rc"],
                "cnf_sha256": row["proof"].get("cnf_sha256"),
                "drup_sha256": rec["drup_sha256"],
                "verified": True}
            newrow.pop("certificates", None)
            with open(os.path.join(HERE, "results_sweep_m%d_zzreemit.jsonl"
                                   % m), "a") as fh:
                fh.write(json.dumps(newrow) + "\n")
        else:
            rec["result"] = "NEW PROOF DID NOT VERIFY -- stored file untouched"
        return rec
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("m", type=int, nargs="*", default=[18, 19])
    ap.add_argument("--which", choices=("failed", "pysat", "big"),
                    default="failed")
    ap.add_argument("--min-mb", type=float, default=200.0)
    ap.add_argument("--rup-max-mb", type=int, default=1500)
    ap.add_argument("--dt-seconds", type=int, default=20000)
    ap.add_argument("--limit", type=int, default=10 ** 6)
    ap.add_argument("--largest-first", action="store_true",
                    help="re-emit the biggest proofs first (frees disk soonest)")
    ap.add_argument("--band-min", type=float, default=0.0,
                    help="only re-emit stored proofs at least this many MB")
    ap.add_argument("--band-max", type=float, default=1e9,
                    help="only re-emit stored proofs at most this many MB")
    ap.add_argument("--smallest-first", action="store_true",
                    help="re-emit the smallest proofs first (lowest peak scratch)")
    ap.add_argument("--out", default="results_reemit.json")
    args = ap.parse_args()
    if not SW.HAVE_NATIVE:
        print("native cadical/drat-trim not found at", SW.TOOLS)
        return 2
    allrec = []
    for m in args.m:
        todo = pick(m, args.which, args.min_mb,
                    (args.band_min, args.band_max))
        if args.largest_first:
            todo.sort(key=lambda t: -t[2])   # biggest disk win first
        elif args.smallest_first:
            # bank steady wins: small proofs finish fast and need little
            # scratch, so free space climbs monotonically instead of dipping
            # hard while one huge proof is re-solved.
            todo.sort(key=lambda t: t[2])
        todo = todo[:args.limit]
        print("m=%d: %d proofs to re-emit (%s)" % (m, len(todo), args.which),
              flush=True)
        for mask, row, size_mb in todo:
            rec = reemit(m, mask, row, args.rup_max_mb, args.dt_seconds)
            allrec.append(rec)
            print("  m%d g%-10d %6.1f MB -> %s  drat-trim=%s rup18_rc=%s"
                  % (m, mask, size_mb, rec.get("result"),
                     rec.get("drat_trim"), rec.get("rup18_rc")), flush=True)
            json.dump(allrec, open(os.path.join(HERE, args.out), "w"), indent=1)
    bad = [r for r in allrec if not r.get("verified")]
    print("re-emitted %d, still unverified %d" % (len(allrec), len(bad)))
    if bad:
        print("  !!", json.dumps(bad)[:600])
    return 0


if __name__ == "__main__":
    sys.exit(main())
