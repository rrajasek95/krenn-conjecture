#!/usr/bin/env python3
"""Small deletion-free DRUP checker for generated lazy-SAT certificates.

For each proof addition C, reverse unit propagation is the propagation test
of the current CNF under the negation of every literal of C.  A conflict
certifies C; the checker then adds C and continues.  The last addition must
be the empty clause.  The implementation intentionally ignores no proof
steps: the producer has already removed optional deletion lines.

Every check below raises instead of asserting.  A bare ``assert`` is deleted
by ``python3 -O``, and for this checker that is catastrophic: the RUP test is
the entire verification, so under ``-O`` the script would report PASS for any
proof file whatsoever, including a one-line derivation of the empty clause
from a satisfiable CNF.
"""

from __future__ import annotations

import argparse

from pysat.solvers import Solver


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


def read_dimacs(path):
    clauses = []
    variables = None
    declared_clauses = None
    with open(path, encoding="ascii") as stream:
        pending = []
        for raw in stream:
            line = raw.strip()
            if not line or line.startswith("c"):
                continue
            if line.startswith("p "):
                _p, kind, number_variables, number_clauses = line.split()
                require(kind == "cnf", f"header is not cnf: {kind!r}")
                variables = int(number_variables)
                declared_clauses = int(number_clauses)
                continue
            for literal in map(int, line.split()):
                if literal:
                    pending.append(literal)
                else:
                    clauses.append(tuple(pending))
                    pending = []
        require(not pending, f"cnf ends mid-clause: {pending}")
    require(variables is not None, "cnf has no p-line")
    require(
        len(clauses) == declared_clauses,
        f"cnf clause count {len(clauses)} != declared {declared_clauses}",
    )
    require(
        all(abs(literal) <= variables
            for clause in clauses for literal in clause),
        f"cnf literal exceeds declared variable count {variables}",
    )
    return variables, clauses


def read_proof(path):
    """Yield proof clauses without retaining a potentially large trace."""

    with open(path, encoding="ascii") as stream:
        pending = []
        for raw in stream:
            line = raw.strip()
            if not line or line.startswith("c"):
                continue
            require(
                not line.startswith("d "), "proof must be deletion-free"
            )
            for literal in map(int, line.split()):
                if literal:
                    pending.append(literal)
                else:
                    yield tuple(pending)
                    pending = []
        require(not pending, f"proof ends mid-clause: {pending}")


def verify(cnf_path, proof_path, solver_name="cadical195"):
    variables, clauses = read_dimacs(cnf_path)
    number_proof = 0
    last_clause = None
    with Solver(name=solver_name, bootstrap_with=clauses) as solver:
        for index, clause in enumerate(read_proof(proof_path)):
            assumptions = [-literal for literal in clause]
            consistent, _propagated = solver.propagate(
                assumptions=assumptions
            )
            require(
                not consistent,
                f"proof clause {index} is not RUP: {clause}",
            )
            solver.add_clause(list(clause))
            number_proof += 1
            last_clause = clause
            if number_proof % 10000 == 0:
                print(f"checked proof additions={number_proof}", flush=True)
    require(number_proof, "empty proof file")
    require(last_clause == (), "proof does not end in the empty clause")
    print(
        f"PASS deletion-free DRUP: variables={variables} "
        f"cnf_clauses={len(clauses)} proof_additions={number_proof}"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf")
    parser.add_argument("proof")
    parser.add_argument("--solver", default="cadical195")
    args = parser.parse_args()
    verify(args.cnf, args.proof, args.solver)


if __name__ == "__main__":
    main()
