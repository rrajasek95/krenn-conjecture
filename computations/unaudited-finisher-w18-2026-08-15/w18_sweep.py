#!/usr/bin/env python3
"""UNAUDITED PROBE (W18) -- the exhaustion driver for one support size.

Pinned HEAD: see PINNED_HEAD.txt.  Probe output; not a proved project claim.

PER SUPPORT-GRAPH ISOMORPHISM CLASS (the split is complete and disjoint):

  repeat
    solve the accumulated CNF
      UNSAT -> the class is closed; re-solve from scratch with lingeling,
               store the native DRUP proof and replay it with rup18
      SAT   -> decode the template T, re-check (SC) / constants / support with
               independent code, then
        (a) T has a mixed singleton word  -> Lemma W18-O2 kill; verify it;
            minimise its reason set; add the negation of the reason and of
            every image of the reason under Aut(G) x S_3
        (b) Lemma W18-A (cut contradiction) -> verify the certificate,
            minimise its reason set, re-check that the reason alone forces the
            kill, and add the negation of the reason AND of every image of the
            reason under Aut(G) x S_3 as clauses
        (c) Lemma W18-D (cut-local ratio engine) -> verify the certificate,
            extract and minimise a reason set (falling back to blocking the
            Aut(G) x S_3 orbit of T if no reason set is available)
        (d) Lemma W18-C (whole-template ratio engine) -> ditto
        (e) Lemma W18-B (Groebner on an extracted half-system) -> ditto
        (f) nothing fires -> SURVIVOR: record it and stop the class loudly

Clauses from (a) are exact consequences of exactness (O2); clauses from (b)
are negations of reason sets CHECKED to force the kill on their own; clauses
from (c)/(d)/(e) block templates each killed with a verified certificate.  So
UNSAT means: no template with this support graph carries an exact source.
"""

from __future__ import annotations

import argparse
import glob
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import w18_core as C            # noqa: E402
import w18_deep as D            # noqa: E402
import w18_fast as F            # noqa: E402
import w18_half as H            # noqa: E402
import w18_kill as K            # noqa: E402
import w18_lattice as L         # noqa: E402
import w18_sat as S             # noqa: E402
import w18_sym as SY            # noqa: E402
from pysat.solvers import Solver, Lingeling      # noqa: E402

RUP = os.path.join(HERE, "rup18")

# Native solver + checker binaries, built from source by the H1 hygiene lane.
# Using a solver that writes its own proof FILE removes the pysat in-memory
# get_proof() hazard (notes/2026-08-15-pysat-cadical-proof-truncation-hazard.md)
# at the source instead of relying on replay to catch the damage afterwards.
TOOLS = os.path.abspath(os.path.join(
    HERE, "..", "unaudited-hygiene-h1-2026-08-15", "tools"))
CADICAL = os.path.join(TOOLS, "cadical", "build", "cadical")
DRATTRIM = os.path.join(TOOLS, "drat-trim", "drat-trim")
HAVE_NATIVE = os.path.exists(CADICAL) and os.path.exists(DRATTRIM)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def _tail_is_empty_clause(path):
    """Does the proof file end with the empty clause '0'?"""
    with open(path, "rb") as fh:
        fh.seek(0, os.SEEK_END)
        n = min(4096, fh.tell())
        fh.seek(-n, os.SEEK_END)
        tail = fh.read(n).decode("ascii", "replace")
    lines = [x.strip() for x in tail.splitlines() if x.strip()]
    return bool(lines) and lines[-1] == "0"


def _count_lines(path):
    n = 0
    with open(path, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 22), b""):
            n += blk.count(b"\n")
    return n


def emit_and_check_proof(nv, clauses, tag, outdir, keep=True,
                         rup_max_mb=1500, dt_seconds=20000):
    """Solve with cadical run AS A BINARY writing its own DRAT file, then
    replay: drat-trim (backward, full RAT) is the primary checker and rup18
    (this lane's own forward RUP checker) is the independent second opinion.
    Falls back to the old pysat path only if the binaries are missing."""
    tmp = tempfile.mkdtemp(prefix="w18proof")
    cnf = os.path.join(tmp, tag + ".cnf")
    drp = os.path.join(tmp, tag + ".drup")
    S.write_cnf(cnf, nv, clauses)
    out = {"status": "UNSAT", "tag": tag, "nvars": nv,
           "nclauses": len(clauses)}

    if HAVE_NATIVE:
        r = subprocess.run([CADICAL, "--binary=false", "-q", cnf, drp],
                           capture_output=True, text=True)
        out["emitter"] = "cadical-3.0.1-binary"
        out["cadical_rc"] = r.returncode
        if r.returncode == 10:
            shutil.rmtree(tmp, ignore_errors=True)
            return {"status": "PROOF-EMIT-SAT", "tag": tag,
                    "emitter": "cadical-3.0.1-binary"}
        if r.returncode != 20 or not os.path.exists(drp):
            shutil.rmtree(tmp, ignore_errors=True)
            return {"status": "PROOF-EMIT-ERROR", "tag": tag,
                    "cadical_rc": r.returncode,
                    "stderr": (r.stderr or r.stdout)[-400:]}
    else:
        s = Lingeling(bootstrap_with=clauses, with_proof=True)
        if s.solve():
            s.delete()
            shutil.rmtree(tmp, ignore_errors=True)
            return {"status": "PROOF-EMIT-SAT", "tag": tag}
        proof = s.get_proof()
        s.delete()
        with open(drp, "w") as fh:
            fh.write("\n".join(proof) + "\n")
        out["emitter"] = "pysat-lingeling-get_proof (NATIVE BINARY MISSING)"

    out["proof_lemmas"] = _count_lines(drp)
    out["proof_bytes"] = os.path.getsize(drp)
    out["terminates_empty"] = _tail_is_empty_clause(drp)

    if HAVE_NATIVE:
        d = subprocess.run([DRATTRIM, cnf, drp, "-I", "-t", str(dt_seconds)],
                           capture_output=True, text=True)
        txt = (d.stdout or "") + (d.stderr or "")
        out["drat_trim"] = next((ln for ln in txt.splitlines()
                                 if ln.startswith("s ")), txt.strip()[-200:])
        out["drat_trim_ok"] = "s VERIFIED" in txt

    if out["proof_bytes"] <= rup_max_mb * 1024 * 1024:
        r2 = subprocess.run([RUP, cnf, drp], capture_output=True, text=True)
        out["rup18"] = (r2.stdout or r2.stderr).strip()
        out["rup18_rc"] = r2.returncode
    else:
        out["rup18"] = "skipped (proof > %d MB); drat-trim is the checker" \
            % rup_max_mb
        out["rup18_rc"] = None

    out["cnf_sha256"] = sha256(cnf)
    out["drup_sha256"] = sha256(drp)

    # CHECKER CAPABILITY, not just checker verdict.
    #
    # rup18 is a FORWARD RUP checker.  Lingeling's DRUP is RUP-only, so there
    # an rup18 failure really does refute the proof -- that is how the pysat
    # corruptions were caught.  CaDiCaL, however, emits DRAT, whose lemmas may
    # be RAT rather than RUP; rup18 cannot validate those and reports "RUP
    # FAILURE" on a perfectly good proof.  So on a DRAT proof rup18 can only
    # CONFIRM, never refute, and the authority is drat-trim (or our own drat18,
    # which does all-pivot RAT).
    #
    # Three-way outcome, because "not checked" must never masquerade as
    # "checked and failed":
    native = "cadical" in str(out.get("emitter", ""))
    dt_ok = out.get("drat_trim_ok")
    rup_ok = out.get("rup18_rc") == 0
    rup_bad = out.get("rup18_rc") not in (0, None)
    if not out["terminates_empty"]:
        out["check"] = "refuted"
        out["check_reason"] = "proof does not end in the empty clause"
    elif dt_ok or rup_ok:
        out["check"] = "verified"
        out["check_reason"] = ("drat-trim" if dt_ok else "rup18")
    elif rup_bad and not native:
        out["check"] = "refuted"          # RUP-only proof, RUP checker refutes
        out["check_reason"] = "rup18 on a RUP-only proof: %s" % out["rup18"]
    elif dt_ok is False and "TIMEOUT" not in str(out.get("drat_trim", "")):
        out["check"] = "refuted"
        out["check_reason"] = "drat-trim: %s" % out.get("drat_trim")
    else:
        out["check"] = "unchecked"
        out["check_reason"] = (
            "drat-trim %s; rup18 cannot decide a DRAT proof's RAT lemmas"
            % out.get("drat_trim", "not run"))
    out["verified"] = out["check"] == "verified"
    if keep:
        os.makedirs(outdir, exist_ok=True)
        for src in (cnf, drp):
            with open(src, "rb") as fi, gzip.open(
                    os.path.join(outdir, os.path.basename(src) + ".gz"),
                    "wb", compresslevel=6) as fo:
                while True:
                    blk = fi.read(1 << 22)
                    if not blk:
                        break
                    fo.write(blk)
    shutil.rmtree(tmp, ignore_errors=True)
    return out


def run_class(mask, m, solver_name="cadical195", seconds=3600, outdir=None,
              keep_proof=True, sing_batch=16, exact_after=0, deep_timeout=60,
              store_certs=True, cert_cap=3000, dreason_keys=40,
              orbit_cap=48, sing_orbit_cap=1, sing_minimise=False,
              exact_word_cap=2500, extra_units=None):
    t0 = time.time()
    enc = S.ClassEncoder(mask)
    if any(not cl for cl in enc.clauses):
        return {"mask": mask, "m": m, "status": "TRIVIAL-UNSAT",
                "reason": "an (SC) slot has no possible server on this graph",
                "rounds": 0, "seconds": round(time.time() - t0, 2), "tally": {}}
    if extra_units:
        # a cube of the case split: sound because the sweep runs every cube
        for (e, k, b) in extra_units:
            lit = enc.x[(e, k)]
            enc.clauses.append([lit if b else -lit])
    off_edges = [e for e in range(C.NE) if e not in enc.edge_set]
    eng = S.FibreEngine(enc.edges)
    group = SY.class_group(mask) if not extra_units else [SY.IDENT]
    sol = Solver(name=solver_name, bootstrap_with=enc.clauses)
    ptr = len(enc.clauses)
    tally = Counter()
    seen_sing = Counter()
    certs = {"O2": [], "A": [], "D": [], "C": [], "B": []}
    survivors = []
    deep_templates = []
    deep_errors = []
    rounds = 0
    status = "timeout"

    def push():
        nonlocal ptr
        for cl in enc.clauses[ptr:]:
            sol.add_clause(cl)
        ptr = len(enc.clauses)


    def add_reason_orbit(reason, cap=None):
        for r in SY.reason_orbit([tuple(x) for x in reason], group,
                                 cap=orbit_cap if cap is None else cap):
            enc.add_kill_clause(r)
        push()

    def add_template_orbit(T):
        for img in SY.template_orbit(T, group, cap=orbit_cap):
            enc.block_template(img)
        push()

    def keep(kind, cert):
        if store_certs and len(certs[kind]) < cert_cap:
            certs[kind].append(cert)

    while time.time() - t0 < seconds:
        if sol.solve() is False:
            status = "UNSAT"
            break
        rounds += 1
        T = enc.decode(sol.get_model())
        assert C.support(T) == m, "encoding unsound: support"
        assert C.sc_ok(T), "encoding unsound: (SC)"
        sizes = eng.sizes(T)
        assert eng.constants_ok(sizes), "encoding unsound: constants"
        sing, _ = eng.singleton_words(T)
        if sing:
            tally["O2-singleton"] += 1
            for w in sing[:sing_batch]:
                seen_sing[w] += 1
                if (exact_after and seen_sing[w] >= exact_after
                        and len(enc.word_done) < exact_word_cap):
                    enc.add_word_constraint(w)
                    continue
                cert = K.singleton_reason(T, w)
                ok, _ = K.verify_singleton(T, cert)
                if not ok:
                    status = "O2-CERT-FAILURE"
                    survivors.append([int(x) for x in T])
                    break
                if sing_minimise:
                    cert = K.minimise_singleton_reason(T, cert, off_edges)
                else:
                    cert["reason"] = [l for l in cert["reason"]
                                      if l[1] in enc.edge_set]
                ok2, _ = K.singleton_reason_sufficient(T, cert, off_edges)
                if not ok2:
                    status = "O2-REASON-FAILURE"
                    survivors.append([int(x) for x in T])
                    break
                add_reason_orbit(cert["reason"], cap=sing_orbit_cap)
                keep("O2", cert)
            push()
            if status != "timeout":
                break
            continue
        occ = F.occupancy(T)
        compat = F.support_matrix(occ)
        hit = F.find(T, compat)
        if hit is not None:
            cert = F.certificate(T, hit)
            ok, _ = K.verify_certificate(T, cert)
            if not ok:
                status = "A-CERT-FAILURE"
                survivors.append([int(x) for x in T])
                break
            cert = K.minimise_reason(T, cert, off_edges)
            ok2, _ = K.check_reason_sufficient(T, cert, off_edges)
            if not ok2:
                status = "A-REASON-FAILURE"
                survivors.append([int(x) for x in T])
                break
            add_reason_orbit(cert["reason"])
            tally["W18-A"] += 1
            keep("A", cert)
            continue
        cert = H.find_kill_D(T, occ, compat, side_sizes=(4, 6))
        if cert is not None:
            ok, _ = H.verify_D(T, cert)
            if not ok:
                status = "D-CERT-FAILURE"
                survivors.append([int(x) for x in T])
                break
            reason = (H.reason_D(T, cert)
                      if len(cert["justification"]) <= dreason_keys else None)
            ok2 = bool(reason) and H.reason_D_sufficient(
                T, cert, reason, off_edges)[0]
            if ok2:
                reason = H.minimise_reason_D(T, cert, reason, off_edges)
                ok3, _ = H.reason_D_sufficient(T, cert, reason, off_edges)
                if not ok3:
                    status = "D-REASON-FAILURE"
                    survivors.append([int(x) for x in T])
                    break
                cert["reason"] = reason
                add_reason_orbit(reason)
                tally["W18-D:" + cert["ratio"]["rule"]] += 1
            else:
                add_template_orbit(T)
                tally["W18-D-blocked:" + cert["ratio"]["rule"]] += 1
            cert["template"] = [int(x) for x in T]
            keep("D", cert)
            continue
        cert = L.find_kill_C(T)
        if cert is not None:
            ok, _ = L.verify_C(T, cert)
            if not ok:
                status = "C-CERT-FAILURE"
                survivors.append([int(x) for x in T])
                break
            cert["template"] = [int(x) for x in T]
            add_template_orbit(T)
            tally["W18-C:" + str(cert.get("rule")
                                 or cert["ratio"]["rule"])] += 1
            keep("C", cert)
            continue
        # Reaching W18-B means O2, A, D and C all failed on this template:
        # rare and interesting, so record it whatever happens next.
        deep_templates.append([int(x) for x in T])
        try:
            certB, sysB = D.find_kill_B(T, timeout=deep_timeout)
        except Exception as exc:                       # Singular timeout/crash
            deep_errors.append({"template": [int(x) for x in T],
                                "error": type(exc).__name__})
            certB, sysB = None, None
        if certB is not None:
            lift = certB["verdict"].get("lift")
            gcols = certB["verdict"].get("gauge_cols", ())
            esub = certB["verdict"].get("eq_subset")
            liftok = (D.verify_lift(sysB, lift, gauge_cols=gcols,
                                    eq_subset=esub)[0]
                      if lift else None)
            add_template_orbit(T)
            tally["W18-B"] += 1
            keep("B", {"template": [int(x) for x in T],
                       "cut_L": certB["cut_L"], "side": certB["side"],
                       "sites": certB.get("sites"),
                       "reason": certB["verdict"].get("reason"),
                       "gauge_cols": list(gcols),
                       "eq_subset": (list(esub) if esub else None),
                       "subset_plan": certB["verdict"].get("subset_plan"),
                       "lift_verified": liftok})
            continue
        survivors.append([int(x) for x in T])
        # a Singular timeout/crash is an engine failure, not a survivor
        status = ("B-ENGINE-ERROR"
                  if deep_errors and deep_errors[-1]["template"] == survivors[-1]
                  else "SURVIVOR")
        break
    sol.delete()
    row = {"mask": mask, "m": m, "status": status, "rounds": rounds,
           "tally": dict(tally), "group_order": len(group),
           "nvars": enc.nv, "nclauses": len(enc.clauses),
           "kill_clauses": enc.kill_clauses,
           "exact_words": len(enc.word_done),
           "seconds": round(time.time() - t0, 2)}
    if survivors:
        row["survivors"] = survivors
    if deep_templates:
        row["deep_templates"] = deep_templates[:20]
        row["n_deep"] = len(deep_templates)
    if deep_errors:
        row["deep_errors"] = deep_errors[:20]
    if status == "UNSAT" and outdir is not None:
        row["proof"] = emit_and_check_proof(enc.nv, enc.clauses,
                                            "m%d_g%d" % (m, mask), outdir,
                                            keep=keep_proof)
    row["certificates"] = certs if store_certs else None
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", type=int, required=True)
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--stop", type=int, default=10 ** 9)
    ap.add_argument("--stride", type=int, default=1)
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--seconds", type=float, default=3600.0)
    ap.add_argument("--solver", default="cadical195")
    ap.add_argument("--tag", default="")
    ap.add_argument("--no-proof", action="store_true")
    ap.add_argument("--no-certs", action="store_true")
    ap.add_argument("--skip-done", action="store_true")
    ap.add_argument("--sing-batch", type=int, default=32)
    ap.add_argument("--sing-minimise", action="store_true")
    ap.add_argument("--exact-after", type=int, default=1)
    ap.add_argument("--exact-word-cap", type=int, default=2500)
    ap.add_argument("--sing-orbit-cap", type=int, default=1)
    ap.add_argument("--orbit-cap", type=int, default=48)
    ap.add_argument("--deep-timeout", type=float, default=60.0)
    args = ap.parse_args()
    classes = json.load(open(os.path.join(HERE, "graph_classes.json")))
    allmasks = classes[str(args.m)]
    idxs = list(range(args.start, min(args.stop, len(allmasks))))
    idxs = idxs[args.offset::args.stride]
    masks = [allmasks[i] for i in idxs]
    if args.skip_done:
        done = set()
        for f in glob.glob(os.path.join(HERE,
                                        "results_sweep_m%d_*.jsonl" % args.m)):
            for line in open(f):
                r = json.loads(line)
                if r["status"] in ("UNSAT", "TRIVIAL-UNSAT"):
                    done.add(r["mask"])
        pairs = [(i, x) for i, x in zip(idxs, masks) if x not in done]
        idxs = [i for i, _ in pairs]
        masks = [x for _, x in pairs]
        print("skipping %d already-closed classes" % len(done), flush=True)
    proofdir = os.path.join(HERE, "certificates", "m%d" % args.m)
    certdir = os.path.join(HERE, "certificates", "m%d_kills" % args.m)
    os.makedirs(certdir, exist_ok=True)
    rows = []
    t0 = time.time()
    jsonl = open(os.path.join(HERE, "results_sweep_m%d%s.jsonl"
                              % (args.m, args.tag)), "a")
    for n, mask in enumerate(masks):
        row = run_class(mask, args.m, solver_name=args.solver,
                        seconds=args.seconds,
                        outdir=None if args.no_proof else proofdir,
                        store_certs=not args.no_certs,
                        sing_batch=args.sing_batch,
                        exact_after=args.exact_after,
                        exact_word_cap=args.exact_word_cap,
                        sing_orbit_cap=args.sing_orbit_cap,
                        orbit_cap=args.orbit_cap,
                        deep_timeout=args.deep_timeout,
                        sing_minimise=args.sing_minimise)
        row["index"] = idxs[n]
        certs = row.pop("certificates", None)
        if certs:
            with gzip.open(os.path.join(certdir, "g%d.json.gz" % mask),
                           "wt") as fh:
                json.dump({"mask": mask, "m": args.m, "certificates": certs},
                          fh)
        rows.append(row)
        jsonl.write(json.dumps(row) + "\n")
        jsonl.flush()
        pr = row.get("proof", {})
        print(f"[{time.time()-t0:8.1f}s] class {idxs[n]:4d} "
              f"mask={mask:<12d} {row['status']:<14s} rounds={row['rounds']:6d} "
              f"|Aut|x6={row.get('group_order', 0):5d} "
              f"{row['seconds']:8.2f}s  proof_rc={pr.get('rup18_rc')} "
              f"tally={row['tally']}", flush=True)
        if row["status"] not in ("UNSAT", "TRIVIAL-UNSAT"):
            print("  !!!!! NON-UNSAT:", row["status"], row.get("survivors"),
                  flush=True)
    summary = {"m": args.m, "classes": len(rows),
               "statuses": dict(Counter(r["status"] for r in rows)),
               "total_rounds": sum(r["rounds"] for r in rows),
               "tally": dict(sum((Counter(r["tally"]) for r in rows),
                                 Counter())),
               "proofs_replayed": sum(1 for r in rows
                                      if r.get("proof", {}).get("rup18_rc") == 0),
               "proof_failures": [r["mask"] for r in rows
                                  if "proof" in r
                                  and r["proof"].get("rup18_rc") != 0],
               "seconds": round(time.time() - t0, 1)}
    name = os.path.join(HERE, "results_sweep_m%d%s.json" % (args.m, args.tag))
    json.dump({"summary": summary, "rows": rows}, open(name, "w"))
    print(json.dumps(summary, indent=1))
    print("wrote", name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
