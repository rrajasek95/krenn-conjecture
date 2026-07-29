#!/usr/bin/env python3
"""Generate the CNF and deletion-free DRUP proof excluding 180 cells."""

import argparse
from hashlib import sha256
from pathlib import Path

from pysat.solvers import Solver

import verify_n8_orbit40_cell180_equality as equality


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prefix",
        default="computations/cert_n8_orbit40_cell180_equality",
    )
    args = parser.parse_args()
    prefix = Path(args.prefix)
    cnf_path = prefix.with_suffix(".cnf")
    proof_path = prefix.with_suffix(".drup")

    variables, clauses = equality.build_equality_cnf()
    cnf_lines = [f"p cnf {variables} {len(clauses)}"]
    cnf_lines.extend(
        " ".join(map(str, clause)) + " 0" for clause in clauses
    )
    cnf_path.write_text("\n".join(cnf_lines) + "\n")

    solver = Solver(
        name="cadical195", bootstrap_with=clauses, with_proof=True
    )
    assert not solver.solve()
    proof = solver.get_proof()
    solver.delete()
    assert proof and proof[-1] == "0"
    assert not any(line.startswith("d ") for line in proof)
    proof_path.write_text("\n".join(proof) + "\n")

    print(
        f"WROTE {cnf_path} clauses={len(clauses)} "
        f"sha256={digest(cnf_path)}"
    )
    print(
        f"WROTE {proof_path} additions={len(proof)} "
        f"sha256={digest(proof_path)}"
    )


if __name__ == "__main__":
    main()
