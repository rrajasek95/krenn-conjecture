#!/usr/bin/env python3
"""Generate SAT witnesses and DRUP candidates for the remaining m=10 cores."""

from __future__ import annotations

import gzip
import hashlib
import json

import verify_n8_d1_m10_remaining_core_inheritance as C


def main():
    try:
        from pysat.solvers import Solver
    except ImportError as exc:
        raise RuntimeError("python-sat is required to regenerate witnesses") from exc
    branches, admissible, sigma, off_sigma = C.surviving_branches()
    models, proofs = {}, []
    for family, index, state in branches:
        key = "%s:%d" % (family, index)
        cnf = C.build_branch_cnf(state, admissible, sigma, off_sigma)
        with Solver(name="glucose42", bootstrap_with=cnf.clauses,
                    with_proof=True) as solver:
            satisfiable = solver.solve()
            if satisfiable:
                positive = sum(1 << (literal - 1)
                               for literal in solver.get_model()
                               if literal > 0)
                models[key] = hex(positive)
                continue
            trace = solver.get_proof()
        deletion_free = [line for line in trace if not line.startswith("d ")]
        if not deletion_free or deletion_free[-1].strip() != "0":
            raise RuntimeError("the %s proof does not end in empty" % key)
        raw = "".join(line + "\n" for line in deletion_free).encode("ascii")
        compressed = gzip.compress(raw, mtime=0)
        with open(C.proof_path(family, index), "wb") as handle:
            handle.write(compressed)
        proofs.append((key, len(deletion_free),
                       hashlib.sha256(raw).hexdigest(),
                       hashlib.sha256(compressed).hexdigest()))
    raw = json.dumps(models, sort_keys=True,
                     separators=(",", ":")).encode("ascii")
    compressed = gzip.compress(raw, mtime=0)
    if (hashlib.sha256(raw).hexdigest() != C.EXPECTED_MODELS_RAW_SHA256
            or hashlib.sha256(compressed).hexdigest()
            != C.EXPECTED_MODELS_GZIP_SHA256):
        raise RuntimeError("the deterministic SAT model payload changed")
    if [(key, count, raw_sha, gzip_sha)
        for key, count, raw_sha, gzip_sha in proofs] != [
            (key, C.EXPECTED_PROOFS[key][3],
             C.EXPECTED_PROOFS[key][4], C.EXPECTED_PROOFS[key][5])
            for key in sorted(C.EXPECTED_PROOFS)
        ]:
        raise RuntimeError("the deterministic inherited proofs changed")
    with open(C.MODELS_PATH, "wb") as handle:
        handle.write(compressed)
    print("models", len(models), "raw", hashlib.sha256(raw).hexdigest(),
          "gzip", hashlib.sha256(compressed).hexdigest())
    for row in proofs:
        print("proof", *row)


if __name__ == "__main__":
    main()
