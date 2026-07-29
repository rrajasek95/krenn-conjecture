#!/usr/bin/env python3
"""Rebuild and streaming-RUP-check the C3 branch-4 cap-6 certificate."""

import argparse
from pathlib import Path

import generate_f3_c3_branch4_cap6_certificate as generator
import search_f3_c3_equivariant_n8 as search
from verify_n8_orbit40_cell180_certificate import (
    StreamingRupChecker,
    read_dimacs,
    read_proof,
)


def audit_mathematical_scope():
    assert generator.EQUATIONS == (0, 756, 1367, 1876)
    assert search.COLOURING_REPS[0] == (0,) * search.N
    assert search.TARGETS[0] == 1
    assert all(search.TARGETS[index] == 0
               for index in generator.EQUATIONS[1:])
    assert search.PURE_MATCHING_REPS[4] == (
        (0, 3), (1, 4), (2, 6), (5, 7),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prefix",
        default=str(Path(__file__).resolve().parent / "cert_f3_c3_branch4_cap6"),
    )
    args = parser.parse_args()
    audit_mathematical_scope()
    variables, clauses = read_dimacs(Path(args.prefix).with_suffix(".cnf"))
    expected_variables, expected_clauses = generator.build_certificate_cnf()
    assert variables == expected_variables
    assert clauses == expected_clauses

    proof = read_proof(Path(args.prefix).with_suffix(".drup"))
    checker = StreamingRupChecker(variables, clauses)
    for addition_number, clause in enumerate(proof, start=1):
        assert checker.rup_conflict(clause), (
            "non-RUP addition", addition_number, clause,
        )
        checker.add_clause(clause)
    print(
        "PASS F3 joint-C3 branch-4 cap-6 certificate: "
        f"rebuilt {variables}-variable/{len(clauses)}-clause CNF from "
        f"equations {generator.EQUATIONS} and checked {len(proof)} "
        "deletion-free RUP additions through empty"
    )


if __name__ == "__main__":
    main()
