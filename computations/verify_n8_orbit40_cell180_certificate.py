#!/usr/bin/env python3
"""Independently rebuild and streaming-RUP-check the 180-cell certificate."""

import argparse
from collections import defaultdict
from pathlib import Path

import verify_n8_orbit40_cell180_equality as equality


def read_dimacs(path):
    variables = clause_count = None
    clauses = []
    pending = []
    for raw_line in Path(path).read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p "):
            fields = line.split()
            assert fields[:2] == ["p", "cnf"]
            variables, clause_count = map(int, fields[2:])
            continue
        for token in map(int, line.split()):
            if token:
                pending.append(token)
            else:
                clauses.append(tuple(pending))
                pending = []
    assert not pending
    assert variables is not None and clause_count == len(clauses)
    return variables, tuple(clauses)


def read_proof(path):
    proof = []
    for raw_line in Path(path).read_text().splitlines():
        fields = raw_line.split()
        if not fields:
            continue
        assert fields[0] != "d", "certificate must be deletion-free"
        integers = tuple(map(int, fields))
        assert integers[-1] == 0
        proof.append(integers[:-1])
    assert proof and proof[-1] == ()
    return tuple(proof)


class StreamingRupChecker:
    def __init__(self, variables, clauses):
        self.variables = variables
        self.clauses = []
        self.occurrences = defaultdict(list)
        self.units = []
        for clause in clauses:
            self.add_clause(clause)

    def add_clause(self, clause):
        clause = tuple(clause)
        index = len(self.clauses)
        self.clauses.append(clause)
        for literal in clause:
            assert 1 <= abs(literal) <= self.variables
            self.occurrences[literal].append(index)
        if len(clause) == 1:
            self.units.append(clause[0])

    def rup_conflict(self, clause):
        values = bytearray(self.variables + 1)
        # byte values: 0 unassigned, 1 true, 2 false.
        queue = []

        def enqueue(literal):
            variable = abs(literal)
            wanted = 1 if literal > 0 else 2
            if values[variable] == 0:
                values[variable] = wanted
                queue.append(literal)
                return True
            return values[variable] == wanted

        for literal in self.units:
            if not enqueue(literal):
                return True
        for literal in clause:
            if not enqueue(-literal):
                return True

        position = 0
        while position < len(queue):
            true_literal = queue[position]
            position += 1
            for clause_index in self.occurrences[-true_literal]:
                current = self.clauses[clause_index]
                satisfied = False
                unassigned = 0
                last_unassigned = None
                for literal in current:
                    value = values[abs(literal)]
                    if value == 0:
                        unassigned += 1
                        last_unassigned = literal
                    elif (value == 1) == (literal > 0):
                        satisfied = True
                        break
                if satisfied:
                    continue
                if unassigned == 0:
                    return True
                if unassigned == 1 and not enqueue(last_unassigned):
                    return True
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prefix",
        default="computations/cert_n8_orbit40_cell180_equality",
    )
    args = parser.parse_args()
    prefix = Path(args.prefix)
    variables, clauses = read_dimacs(prefix.with_suffix(".cnf"))
    expected_variables, expected_clauses = equality.build_equality_cnf()
    assert variables == expected_variables
    assert clauses == expected_clauses

    proof = read_proof(prefix.with_suffix(".drup"))
    checker = StreamingRupChecker(variables, clauses)
    for addition_number, clause in enumerate(proof, start=1):
        assert checker.rup_conflict(clause), (
            "non-RUP addition", addition_number, clause
        )
        checker.add_clause(clause)
    print(
        "PASS 180-cell certificate: rebuilt exact CNF "
        f"({variables} variables, {len(clauses)} clauses) and checked "
        f"all {len(proof)} deletion-free DRUP additions through empty"
    )


if __name__ == "__main__":
    main()
