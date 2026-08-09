#!/usr/bin/env python3
"""Regenerate four additional deletion-free m=10 DRUP proofs."""

from __future__ import annotations

import gzip
import hashlib
import os

import verify_n8_d1_m10_additional_core_rups as C


def main():
    try:
        from pysat.solvers import Solver
    except ImportError as exc:
        raise RuntimeError("python-sat is required to regenerate proofs") from exc
    admissible, sigma, off_sigma, _kinds = C.V.reconstruct_support_domains()
    for label, base in C.support_bases():
        cnf = C.build_core_cnf(base, admissible, sigma, off_sigma)
        with Solver(name="glucose42", bootstrap_with=cnf.clauses,
                    with_proof=True) as solver:
            if solver.solve():
                raise RuntimeError("the %s core unexpectedly became SAT" % label)
            proof = solver.get_proof()
        deletion_free = [line for line in proof if not line.startswith("d ")]
        if not deletion_free or deletion_free[-1].strip() != "0":
            raise RuntimeError("the %s proof does not end in empty" % label)
        raw = "".join(line + "\n" for line in deletion_free).encode("ascii")
        compressed = gzip.compress(raw, mtime=0)
        expected = C.EXPECTED[label]
        observed = (len(deletion_free), hashlib.sha256(raw).hexdigest(),
                    hashlib.sha256(compressed).hexdigest())
        if observed != (expected[3], expected[4], expected[5]):
            raise RuntimeError("the deterministic %s proof changed" % label)
        with open(C.proof_path(label), "wb") as handle:
            handle.write(compressed)
        print(label, "additions", len(deletion_free),
              "raw", hashlib.sha256(raw).hexdigest(),
              "gzip", hashlib.sha256(compressed).hexdigest())


if __name__ == "__main__":
    main()
