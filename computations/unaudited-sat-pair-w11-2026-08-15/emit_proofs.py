"""UNAUDITED (W11).  Emit and verify a DRUP proof for every isomorphism class
of support graph at a given support size, for an UNSAT verdict.

usage:  python3 emit_proofs.py M [--diagonal] [--outdir DIR]

Writes DIR/m{M}_{i}.cnf(.gz) and DIR/m{M}_{i}.drup(.gz) and runs ./rupcheck
on each pair.  Only the SHA-256 and the checker verdict are kept for classes
that verify, so the artefact stays small; use --keep to retain everything.
"""

import argparse
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

from pysat.solvers import Lingeling

import per_graph as PG

HERE = os.path.dirname(os.path.abspath(__file__))
RUPCHECK = os.path.join(HERE, "rupcheck")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def write_cnf(path, nvars, clauses):
    with open(path, "w") as f:
        f.write("p cnf %d %d\n" % (nvars, len(clauses)))
        for cl in clauses:
            f.write(" ".join(map(str, cl)) + " 0\n")


def run(m, outdir, keep=False, **kw):
    md = json.load(open(os.path.join(HERE, "graph_classes_mindeg3.json")))
    masks = md[str(m)]
    os.makedirs(outdir, exist_ok=True)
    rows = []
    t0 = time.time()
    tmp = tempfile.mkdtemp(prefix="w11proof")
    for i, g in enumerate(masks):
        enc = PG.GraphEncoder(g, **kw)
        if enc.trivial_unsat:
            rows.append(dict(mask=g, status="TRIVIAL_UNSAT",
                             reason="support graph has no perfect matching"))
            continue
        s = Lingeling(bootstrap_with=enc.clauses, with_proof=True)
        sat = s.solve()
        if sat:
            s.delete()
            rows.append(dict(mask=g, status="SAT"))
            print("  [SAT] mask=%d -- no proof" % g, flush=True)
            continue
        proof = s.get_proof()
        s.delete()
        cnf = os.path.join(tmp, "m%d_%d.cnf" % (m, i))
        drp = os.path.join(tmp, "m%d_%d.drup" % (m, i))
        write_cnf(cnf, enc.pool.top, enc.clauses)
        with open(drp, "w") as f:
            f.write("\n".join(proof) + "\n")
        r = subprocess.run([RUPCHECK, cnf, drp], capture_output=True, text=True)
        row = dict(mask=g, status="UNSAT", nvars=enc.pool.top,
                   nclauses=len(enc.clauses), npm=len(enc.P),
                   proof_lemmas=len(proof),
                   cnf_sha256=sha(cnf), drup_sha256=sha(drp),
                   rupcheck=r.stdout.strip(), rupcheck_rc=r.returncode)
        rows.append(row)
        if r.returncode != 0:
            print("  !! RUPCHECK FAILED mask=%d : %s" % (g, r.stdout.strip()),
                  flush=True)
        if keep:
            # proofs are small and are the actual certificate; the CNF is
            # regenerated deterministically from the mask by per_graph, so
            # only its SHA-256 is recorded -- except for one exemplar per
            # support, kept in full so the pair can be rechecked standalone.
            srcs = [drp] + ([cnf] if i == 0 else [])
            for src in srcs:
                with open(src, "rb") as fi, gzip.open(
                        os.path.join(outdir, os.path.basename(src) + ".gz"),
                        "wb") as fo:
                    shutil.copyfileobj(fi, fo)
        os.remove(cnf)
        os.remove(drp)
        if (i + 1) % 25 == 0:
            print("   ... %d/%d  %.1fs" % (i + 1, len(masks),
                                           time.time() - t0), flush=True)
    shutil.rmtree(tmp, ignore_errors=True)
    ok = all(r.get("rupcheck_rc", 0) == 0 for r in rows)
    nsat = sum(1 for r in rows if r["status"] == "SAT")
    out = dict(m=m, options=kw, classes=len(masks), sat_classes=nsat,
               all_proofs_verified=ok, seconds=time.time() - t0, rows=rows)
    name = "proofs_m%d%s.json" % (m, "_diagonal" if kw.get("diagonal_only")
                                  else "")
    json.dump(out, open(os.path.join(outdir, name), "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}), flush=True)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("m", type=int)
    ap.add_argument("--diagonal", action="store_true")
    ap.add_argument("--outdir", default=os.path.join(HERE, "certificates"))
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    r = run(a.m, a.outdir, keep=a.keep, diagonal_only=a.diagonal)
    sys.exit(0 if r["all_proofs_verified"] else 1)
