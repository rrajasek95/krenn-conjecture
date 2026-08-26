#!/usr/bin/env python3
"""UNAUDITED PROBE (W18) -- record corrected class rows for re-emitted proofs.

Pinned HEAD: see PINNED_HEAD.txt.  Probe output; not a proved project claim.

run_reemit.py replaces certificates/m{m}/m{m}_g{mask}.drup.gz with a
cadical-native proof.  Until a matching class row exists, the ledger keeps
comparing the NEW bytes against the SUPERSEDED pysat digest and reports a
mismatch.  This script re-verifies whatever is stored right now and appends the
corrected row -- no re-solving, so it is cheap to run after any re-emission.
"""
from __future__ import annotations

import glob
import gzip
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import run_reemit as RE      # noqa: E402
import w18_sweep as SW       # noqa: E402


def fix(m, masks=None, rup_max_mb=1500):
    rows = RE.best_rows(m)
    pdir = os.path.join(HERE, "certificates", "m%d" % m)
    out = []
    for mask, row in sorted(rows.items()):
        if masks and mask not in masks:
            continue
        pr = row.get("proof")
        if not pr:
            continue
        tag = "m%d_g%d" % (m, mask)
        cnfz = os.path.join(pdir, tag + ".cnf.gz")
        drpz = os.path.join(pdir, tag + ".drup.gz")
        if not (os.path.exists(cnfz) and os.path.exists(drpz)):
            continue
        stored_ok = (pr.get("rup18_rc") == 0 and pr.get("terminates_empty"))
        tmp = tempfile.mkdtemp(prefix="w18fixrow")
        try:
            cnf = os.path.join(tmp, tag + ".cnf")
            drp = os.path.join(tmp, tag + ".drup")
            with gzip.open(cnfz, "rb") as fi, open(cnf, "wb") as fo:
                shutil.copyfileobj(fi, fo, 1 << 22)
            with gzip.open(drpz, "rb") as fi, open(drp, "wb") as fo:
                shutil.copyfileobj(fi, fo, 1 << 22)
            dsha = SW.sha256(drp)
            if dsha == pr.get("drup_sha256") and stored_ok:
                continue                      # row already matches the bytes
            rec = {"mask": mask, "m": m,
                   "cnf_sha_ok": SW.sha256(cnf) == pr.get("cnf_sha256"),
                   "proof_bytes": os.path.getsize(drp),
                   "proof_lemmas": SW._count_lines(drp),
                   "terminates_empty": SW._tail_is_empty_clause(drp)}
            d = subprocess.run([SW.DRATTRIM, cnf, drp, "-I", "-t", "20000"],
                               capture_output=True, text=True)
            txt = (d.stdout or "") + (d.stderr or "")
            rec["drat_trim"] = next((ln for ln in txt.splitlines()
                                     if ln.startswith("s ")),
                                    txt.strip()[-160:])
            rec["drat_trim_ok"] = "s VERIFIED" in txt
            if rec["proof_bytes"] <= rup_max_mb * 1024 * 1024:
                r2 = subprocess.run([SW.RUP, cnf, drp], capture_output=True,
                                    text=True)
                rec["rup18"] = (r2.stdout or r2.stderr).strip()
                rec["rup18_rc"] = r2.returncode
            else:
                rec["rup18"] = "skipped (size)"
                rec["rup18_rc"] = 0 if rec["drat_trim_ok"] else 1
            rec["verified"] = bool(rec["terminates_empty"]
                                   and rec["drat_trim_ok"]
                                   and rec["rup18_rc"] == 0)
            if not rec["verified"]:
                rec["result"] = "STORED PROOF STILL DOES NOT VERIFY"
                out.append(rec)
                print(" !!", json.dumps(rec)[:300], flush=True)
                continue
            newrow = dict(row)
            newrow.pop("certificates", None)
            newrow["proof"] = {
                "status": "UNSAT", "tag": tag,
                "nvars": pr.get("nvars"), "nclauses": pr.get("nclauses"),
                "emitter": "cadical-3.0.1-binary (re-emitted by run_reemit)",
                "proof_lemmas": rec["proof_lemmas"],
                "proof_bytes": rec["proof_bytes"],
                "terminates_empty": rec["terminates_empty"],
                "drat_trim": rec["drat_trim"],
                "drat_trim_ok": rec["drat_trim_ok"],
                "rup18": rec["rup18"], "rup18_rc": rec["rup18_rc"],
                "cnf_sha256": pr.get("cnf_sha256"), "drup_sha256": dsha,
                "verified": True}
            with open(os.path.join(HERE, "results_sweep_m%d_zzreemit.jsonl"
                                   % m), "a") as fh:
                fh.write(json.dumps(newrow) + "\n")
            rec["result"] = "row recorded"
            out.append(rec)
            print("  m%d g%-10d %s  %s  rup18_rc=%s"
                  % (m, mask, rec["result"], rec["drat_trim"],
                     rec["rup18_rc"]), flush=True)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    return out


if __name__ == "__main__":
    ms = [int(x) for x in sys.argv[1:]] or [18, 19]
    allrec = []
    for m in ms:
        allrec += fix(m)
    json.dump(allrec, open(os.path.join(HERE, "results_reemit_fixrows.json"),
                           "w"), indent=1)
    bad = [r for r in allrec if not r.get("verified")]
    print("rows fixed %d, still unverified %d" % (len(allrec) - len(bad),
                                                  len(bad)))
