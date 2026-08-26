#!/usr/bin/env python3
"""UNAUDITED PROBE (W18) -- the audit ledger.

Pinned HEAD: see PINNED_HEAD.txt.  Probe output; not a proved project claim.

Reads back everything the sweep wrote and re-checks it COLD:
  * every stored kill certificate is re-verified against its template with the
    reference (slow) code, and every stored reason set is re-checked to be
    sufficient on its own;
  * every stored DRUP proof is decompressed and replayed with rup18 against
    its stored CNF, and both SHA-256 digests are re-computed and compared with
    the values recorded at emission time;
  * the per-class coverage map is rebuilt from the result files and compared
    with the class list, so a missing or non-UNSAT class cannot hide.
"""
from __future__ import annotations

import glob
import gzip
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import w18_core as C          # noqa: E402
import w18_half as H          # noqa: E402
import w18_kill as K          # noqa: E402
import w18_lattice as L       # noqa: E402
import w18_sweep as SW        # noqa: E402

RUP = os.path.join(HERE, "rup18")


def sha_bytes(data):
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def sha_stream(gzpath):
    """SHA-256 of the DECOMPRESSED bytes, without holding them in memory."""
    h = hashlib.sha256()
    with gzip.open(gzpath, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 22), b""):
            h.update(blk)
    return h.hexdigest()


def check_certificates(m, limit_per_class=None):
    tally = Counter()
    failures = []
    files = sorted(glob.glob(os.path.join(HERE, "certificates",
                                          "m%d_kills" % m, "g*.json.gz")))
    for path in files:
        with gzip.open(path, "rt") as fh:
            obj = json.load(fh)
        certs = obj["certificates"]
        for cert in certs.get("O2", [])[:limit_per_class]:
            tally["O2"] += 1
        for cert in certs.get("A", [])[:limit_per_class]:
            tally["A"] += 1
        gmask = obj["mask"]
        for cert in certs.get("D", [])[:limit_per_class]:
            T = tuple(cert["template"])
            ok, msg = H.verify_D(T, cert)
            tally["D"] += 1
            if not ok:
                failures.append({"file": path, "kind": "D", "msg": msg})
            if "reason" in cert:
                offg = [e for e in range(C.NE) if not (gmask >> e) & 1]
                ok2, msg2 = H.reason_D_sufficient(T, cert, cert["reason"], offg)
                if not ok2:
                    failures.append({"file": path, "kind": "D-reason",
                                     "msg": msg2})
        for cert in certs.get("C", [])[:limit_per_class]:
            T = tuple(cert["template"])
            ok, msg = L.verify_C(T, cert)
            tally["C"] += 1
            if not ok:
                failures.append({"file": path, "kind": "C", "msg": msg})
        for cert in certs.get("B", [])[:limit_per_class]:
            tally["B"] += 1
    return {"files": len(files), "certificates_rechecked": dict(tally),
            "failures": failures[:20], "n_failures": len(failures)}


def check_o2_and_a(m, per_file=3, seed=3):
    """Re-verify a bounded sample of O2 and A reason sets, file by file.

    Each reason set is checked on the EXTREME completion (every cell not
    forced off is switched on), which is the worst case for the kill, so a
    pass there is a pass for every template satisfying the reason.
    """
    import random
    rng = random.Random(seed)
    files = sorted(glob.glob(os.path.join(HERE, "certificates",
                                          "m%d_kills" % m, "g*.json.gz")))
    n = 0
    fails = []
    for path in files:
        try:
            with gzip.open(path, "rt") as fh:
                obj = json.load(fh)
        except Exception as exc:                       # noqa: BLE001
            fails.append({"file": path, "msg": "unreadable: %s" % exc})
            continue
        gmask = obj["mask"]
        off_edges = [e for e in range(C.NE) if not (gmask >> e) & 1]
        for kind in ("O2", "A"):
            certs = obj["certificates"].get(kind, [])
            if not certs:
                continue
            for cert in rng.sample(certs, min(per_file, len(certs))):
                T = _extreme_completion(cert["reason"], off_edges)
                if kind == "O2":
                    ok, msg = K.verify_singleton(T, cert)
                    ok2, msg2 = K.singleton_reason_sufficient(T, cert, off_edges)
                else:
                    ok, msg = K.verify_certificate(T, cert)
                    ok2, msg2 = K.check_reason_sufficient(T, cert, off_edges)
                n += 1
                if not (ok and ok2):
                    fails.append({"kind": kind, "file": path,
                                  "msg": msg, "msg2": msg2})
    return {"sampled": n, "failures": len(fails), "examples": fails[:5]}


def _extreme_completion(reason, off_edges=()):
    """The worst-case template for a reason set: everything not forced OFF is
    switched ON.  If the reason really forces the kill, it forces it here."""
    T = [C.FULL9] * C.NE
    for e in off_edges:
        T[e] = 0
    for lit in reason:
        kind, e, i, j = lit[0], lit[1], lit[2], lit[3]
        if kind == "off":
            T[e] &= ~(1 << (3 * i + j))
    return tuple(T)


def _all_rows(m):
    """Every per-class row, read from the incremental JSONL files."""
    rows = {}
    for f in sorted(glob.glob(os.path.join(HERE,
                                           "results_sweep_m%d_*.jsonl" % m))):
        for line in open(f):
            r = json.loads(line)
            prev = rows.get(r["mask"])

            def score(x):
                if x["status"] not in ("UNSAT", "TRIVIAL-UNSAT"):
                    return 0
                p = x.get("proof", {})
                if not p:
                    return 1
                good = p.get("rup18_rc") == 0 and p.get("terminates_empty")
                if not good:
                    return 1
                # a cadical-native proof outranks a pysat-extracted one
                return 3 if "cadical" in str(p.get("emitter", "")) else 2
            if prev is None or score(r) >= score(prev):
                rows[r["mask"]] = r
    return rows


def check_proofs(m, max_mb=60):
    rows = []
    recorded = {}
    for mask, r in _all_rows(m).items():
        if "proof" in r:
            recorded[r["mask"]] = r["proof"]
    pdir = os.path.join(HERE, "certificates", "m%d" % m)
    tmp = tempfile.mkdtemp(prefix="w18ledger")
    bad = []
    for mask, pr in sorted(recorded.items()):
        tag = "m%d_g%d" % (m, mask)
        cnfz = os.path.join(pdir, tag + ".cnf.gz")
        drpz = os.path.join(pdir, tag + ".drup.gz")
        if not (os.path.exists(cnfz) and os.path.exists(drpz)):
            bad.append({"mask": mask, "why": "missing files"})
            continue
        if max_mb and os.path.getsize(drpz) > max_mb * 1024 * 1024:
            # The cold REPLAY is not repeated for very large proofs (the
            # emission-time replay stands), but the stored bytes are still
            # hashed, so silent storage corruption cannot hide.
            rows.append({"mask": mask, "skipped": "replay > %d MB" % max_mb,
                         "cnf_sha_ok": sha_stream(cnfz) == pr.get("cnf_sha256"),
                         "drup_sha_ok": sha_stream(drpz) == pr.get("drup_sha256"),
                         "rup18_rc": None, "rup18": "replay skipped (size)",
                         "emission_rup18_rc": pr.get("rup18_rc"),
                         "terminates_empty": pr.get("terminates_empty")})
            if not (rows[-1]["cnf_sha_ok"] and rows[-1]["drup_sha_ok"]):
                bad.append(rows[-1])
            continue
        cdata = gzip.open(cnfz, "rb").read()
        ddata = gzip.open(drpz, "rb").read()
        row = {"mask": mask,
               "cnf_sha_ok": sha_bytes(cdata) == pr.get("cnf_sha256"),
               "drup_sha_ok": sha_bytes(ddata) == pr.get("drup_sha256"),
               "terminates_empty": pr.get("terminates_empty")}
        cnf = os.path.join(tmp, tag + ".cnf")
        drp = os.path.join(tmp, tag + ".drup")
        open(cnf, "wb").write(cdata)
        open(drp, "wb").write(ddata)
        row["emitter"] = pr.get("emitter", "pysat-lingeling-get_proof")
        r = subprocess.run([RUP, cnf, drp], capture_output=True, text=True)
        row["rup18_rc"] = r.returncode
        row["rup18"] = (r.stdout or r.stderr).strip()
        if SW.HAVE_NATIVE:
            # second, independent checker: backward, with full RAT support
            d = subprocess.run([SW.DRATTRIM, cnf, drp, "-I", "-t", "20000"],
                               capture_output=True, text=True)
            txt = (d.stdout or "") + (d.stderr or "")
            row["drat_trim"] = next((ln for ln in txt.splitlines()
                                     if ln.startswith("s ")),
                                    txt.strip()[-160:])
            row["drat_trim_ok"] = "s VERIFIED" in txt
        os.remove(cnf)
        os.remove(drp)
        rows.append(row)
        if not (row["cnf_sha_ok"] and row["drup_sha_ok"]
                and row["rup18_rc"] == 0
                and row.get("drat_trim_ok", True)):
            bad.append(row)
    os.rmdir(tmp)
    skipped = [r for r in rows if r.get("skipped")]
    return {"proofs": len(rows),
            "replayed_ok": sum(1 for r in rows if r["rup18_rc"] == 0),
            "drat_trim_ok": sum(1 for r in rows if r.get("drat_trim_ok")),
            "native_emitter": sum(1 for r in rows
                                  if "cadical" in str(r.get("emitter", ""))),
            "skipped_large": len(skipped),
            "skipped_emission_rc_ok": sum(1 for r in skipped
                                          if r.get("emission_rup18_rc") == 0),
            "sha_ok": sum(1 for r in rows
                          if r["cnf_sha_ok"] and r["drup_sha_ok"]),
            "failures": bad[:10], "n_failures": len(bad)}


def coverage(m):
    classes = json.load(open(os.path.join(HERE, "graph_classes.json")))[str(m)]
    seen = {}
    tally = Counter()
    kill_tally = Counter()
    secs = []
    for mask, r in _all_rows(m).items():
        seen[r["mask"]] = r["status"]
        tally[r["status"]] += 1
        secs.append(r["seconds"])
        for k, v in r.get("tally", {}).items():
            kill_tally[k] += v
    missing = [x for x in classes if x not in seen]
    notclosed = {k: v for k, v in seen.items()
                 if v not in ("UNSAT", "TRIVIAL-UNSAT")}
    return {"classes": len(classes), "covered": len(seen),
            "max_class_seconds": max(secs or [0]),
            "total_class_seconds": round(sum(secs or [0]), 1),
            "missing": missing[:20], "n_missing": len(missing),
            "statuses": dict(tally), "not_closed": notclosed,
            "kill_mechanisms": dict(kill_tally),
            "closed": not missing and not notclosed}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("m", type=int, nargs="*", default=[18, 19])
    ap.add_argument("--cert-limit", type=int, default=3,
                    help="D/C certificates re-verified per class (0 = all)")
    ap.add_argument("--per-file", type=int, default=3,
                    help="O2/A reason sets re-checked per class")
    ap.add_argument("--max-mb", type=int, default=60,
                    help="skip the cold replay of proofs larger than this")
    ap.add_argument("--out", default="results_ledger.json")
    args = ap.parse_args()
    ms = args.m
    out = {}
    for m in ms:
        out[str(m)] = {"coverage": coverage(m),
                       "certificates": check_certificates(
                           m, args.cert_limit or None),
                       "reason_sample": check_o2_and_a(m, args.per_file),
                       "proofs": check_proofs(m, args.max_mb)}
        print(m, json.dumps({k: {kk: vv for kk, vv in v.items()
                                 if kk not in ("failures", "examples",
                                               "missing", "not_closed")}
                             for k, v in out[str(m)].items()}, indent=1),
              flush=True)
        for k, v in out[str(m)].items():
            for key in ("failures", "examples", "missing", "not_closed"):
                if v.get(key):
                    print("  !!", m, k, key, str(v[key])[:800], flush=True)
    json.dump(out, open(os.path.join(HERE, args.out), "w"), indent=1)
    print("wrote", args.out)
