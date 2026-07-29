#!/usr/bin/env python3
"""Small deletion-free DRUP checker for generated lazy-SAT certificates.

For each proof addition C, reverse unit propagation is the propagation test
of the current CNF under the negation of every literal of C.  A conflict
certifies C; the checker then adds C and continues.  The last addition must
be the empty clause.  The implementation intentionally ignores no proof
steps: the producer has already removed optional deletion lines.
"""

from __future__ import annotations

import argparse

from pysat.solvers import Solver


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
                assert kind == "cnf"
                variables = int(number_variables)
                declared_clauses = int(number_clauses)
                continue
            for literal in map(int, line.split()):
                if literal:
                    pending.append(literal)
                else:
                    clauses.append(tuple(pending))
                    pending = []
        assert not pending
    assert variables is not None
    assert len(clauses) == declared_clauses
    assert all(abs(literal) <= variables for clause in clauses
               for literal in clause)
    return variables, clauses


def read_proof(path):
    """Yield proof clauses without retaining a potentially large trace."""

    with open(path, encoding="ascii") as stream:
        pending = []
        for raw in stream:
            line = raw.strip()
            if not line or line.startswith("c"):
                continue
            assert not line.startswith("d "), "proof must be deletion-free"
            for literal in map(int, line.split()):
                if literal:
                    pending.append(literal)
                else:
                    yield tuple(pending)
                    pending = []
        assert not pending


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
            assert not consistent, (
                f"proof clause {index} is not RUP: {clause}"
            )
            solver.add_clause(list(clause))
            number_proof += 1
            last_clause = clause
            if number_proof % 10000 == 0:
                print(f"checked proof additions={number_proof}", flush=True)
    assert number_proof, "empty proof file"
    assert last_clause == (), "proof does not end in the empty clause"
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
