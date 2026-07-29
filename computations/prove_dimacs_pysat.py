#!/usr/bin/env python3
"""Solve a DIMACS CNF with a PySAT backend and emit deletion-free DRUP."""

from __future__ import annotations

import argparse
from pathlib import Path
from time import monotonic

from pysat.solvers import Solver

import verify_drup_certificate


def prove(cnf_path, proof_path, solver_name):
    variables, clauses = verify_drup_certificate.read_dimacs(cnf_path)
    started = monotonic()
    with Solver(
        name=solver_name,
        bootstrap_with=clauses,
        with_proof=True,
    ) as solver:
        result = solver.solve()
        elapsed = monotonic() - started
        print(
            f"SOLVE solver={solver_name} result={'SAT' if result else 'UNSAT'} "
            f"seconds={elapsed:.3f} variables={variables} "
            f"clauses={len(clauses)}",
            flush=True,
        )
        if result:
            return 2
        proof = solver.get_proof()
    assert proof is not None, f"{solver_name} returned no proof"
    additions = [line for line in proof if not line.startswith("d ")]
    assert additions and additions[-1].strip() == "0", (
        f"{solver_name} proof does not end in the empty clause"
    )
    Path(proof_path).write_text("\n".join(additions) + "\n", encoding="ascii")
    print(
        f"PROOF path={proof_path} additions={len(additions)}",
        flush=True,
    )
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf")
    parser.add_argument("proof")
    parser.add_argument("--solver", required=True)
    args = parser.parse_args()
    raise SystemExit(prove(args.cnf, args.proof, args.solver))


if __name__ == "__main__":
    main()
