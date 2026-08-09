#!/usr/bin/env python3
"""Regenerate the frozen deletion-free DRUP proof (requires python-sat)."""

from __future__ import annotations

import gzip
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import audit_n8_d1_m10_support_frontier as A

OUTPUT = os.path.join(
    HERE, "certificates", "n8_d1_m10_first_core.glucose42.drup.gz"
)
EXPECTED_RAW_SHA256 = (
    "12be9116c777e020d0362117aec555393a6be6119ee41ce955d13d8c1ac6647b"
)
EXPECTED_GZIP_SHA256 = (
    "edacb7215a32476d2b7c22def364be589c5d9ef7f507ec88b4442468c07c5bd1"
)


def main():
    try:
        from pysat.solvers import Solver
    except ImportError as exc:
        raise RuntimeError("python-sat is required to regenerate the proof") from exc
    admissible, sigma, off_sigma, _kinds = A.V.reconstruct_support_domains()
    group = A.V.d1_group()
    triples = [{state[0] for state in A.N.triple_states(colour)}
               for colour in (0, 1)]
    pairs = A.support_pair_orbits(triples[0], triples[1], group)
    base = pairs[0][0] | pairs[0][1]
    cnf = A.build_frontier_cnf(base, admissible, sigma, off_sigma)
    with Solver(name="glucose42", bootstrap_with=cnf.clauses,
                with_proof=True) as solver:
        if solver.solve():
            raise RuntimeError("the frozen frontier unexpectedly became SAT")
        proof = solver.get_proof()
    deletion_free = [line for line in proof if not line.startswith("d ")]
    raw = "".join(line + "\n" for line in deletion_free).encode("ascii")
    compressed = gzip.compress(raw, mtime=0)
    if len(deletion_free) != 4090 or not deletion_free[-1].strip() == "0":
        raise RuntimeError("the deterministic Glucose proof shape changed")
    if hashlib.sha256(raw).hexdigest() != EXPECTED_RAW_SHA256:
        raise RuntimeError("the deletion-free DRUP proof changed")
    if hashlib.sha256(compressed).hexdigest() != EXPECTED_GZIP_SHA256:
        raise RuntimeError("the deterministic gzip payload changed")
    with open(OUTPUT, "wb") as handle:
        handle.write(compressed)
    print("wrote:", OUTPUT)
    print("proof additions:", len(deletion_free))
    print("raw sha256:", EXPECTED_RAW_SHA256)
    print("gzip sha256:", EXPECTED_GZIP_SHA256)


if __name__ == "__main__":
    main()
