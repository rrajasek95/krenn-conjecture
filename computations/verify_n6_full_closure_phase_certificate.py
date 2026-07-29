#!/usr/bin/env python3
"""Rebuild and verify an n=6 full-closure phase certificate bundle.

The JSON file names every exact-binomial core.  This verifier reconstructs
the base support/term/cardinality CNF, checks by signed Hermite reduction that
each named collection of Laurent rows is inconsistent, rebuilds its exact
term-status blocking clause, matches the stored DIMACS file byte for byte and
by SHA-256, and finally streams the deletion-free DRUP proof through the
repository's independent RUP checker.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import search_n6_full_closure_phase as phase
import search_parallel_binomial_nonzero_constants_cegar as toric
import verify_drup_certificate


def parse_word(text):
    word = tuple(map(int, text))
    assert len(word) == phase.N
    assert all(colour in range(phase.Q) for colour in word)
    return word


def dimacs_bytes(top, clauses):
    lines = [f"p cnf {top} {len(clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(lines).encode("ascii")


def core_clause_and_rows(searcher, record):
    clause = []
    rows = []
    seen_patterns = set()
    for row_record in record["rows"]:
        assert set(row_record) == {"word", "terms"}
        word = parse_word(row_record["word"])
        terms = tuple(row_record["terms"])
        assert len(terms) == 2 and terms[0] < terms[1]
        assert all(0 <= number < len(searcher.matchings) for number in terms)
        pattern = word, terms
        assert pattern not in seen_patterns
        seen_patterns.add(pattern)

        present = set(terms)
        clause.extend(
            -searcher.term_variables[word, number]
            if number in present
            else searcher.term_variables[word, number]
            for number in range(len(searcher.matchings))
        )
        rows.append(
            toric.exponent_row(
                searcher.term_cells[word, terms[0]],
                searcher.term_cells[word, terms[1]],
                searcher.cell_index,
                len(searcher.cells),
            )
        )
    assert rows
    consistent, _lattice = toric.signed_quotient_lattice(
        rows, len(searcher.cells)
    )
    assert not consistent
    return clause


def verify(prefix, rup_solver, skip_drup=False):
    prefix = Path(prefix)
    json_path = prefix.with_suffix(".json")
    cnf_path = prefix.with_suffix(".cnf")
    proof_path = prefix.with_suffix(".drup")
    payload = json.loads(json_path.read_text())
    assert payload["order"] == phase.N
    if skip_drup:
        assert payload.get("drup_lines") is None or isinstance(
            payload["drup_lines"], int
        )
    else:
        assert isinstance(payload.get("drup_lines"), int)
        assert payload["drup_lines"] > 0

    searcher = phase.FullPhaseSearch(
        payload["cap"], "cadical195", minimum=payload.get("minimum")
    )
    try:
        assert len(searcher.clauses) == payload["base_clauses"]
        clauses = list(searcher.clauses)
        seen_clauses = set()
        for record in payload["phase_cores"]:
            clause = core_clause_and_rows(searcher, record)
            key = tuple(clause)
            assert key not in seen_clauses
            seen_clauses.add(key)
            clauses.append(clause)
        assert searcher.pool.top == payload["variables"]
        assert len(clauses) == payload["clauses"]

        rebuilt = dimacs_bytes(searcher.pool.top, clauses)
        assert hashlib.sha256(rebuilt).hexdigest() == payload["cnf_sha256"]
        assert rebuilt == cnf_path.read_bytes()
        print(
            f"PASS semantic replay: base_clauses={payload['base_clauses']} "
            f"phase_cores={len(payload['phase_cores'])} "
            f"total_clauses={len(clauses)}",
            flush=True,
        )
    finally:
        searcher.delete()

    if skip_drup:
        print("SKIP DRUP replay (semantic CNF only)")
    else:
        verify_drup_certificate.verify(cnf_path, proof_path, rup_solver)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prefix")
    parser.add_argument("--rup-solver", default="cadical195")
    parser.add_argument("--skip-drup", action="store_true")
    args = parser.parse_args()
    verify(args.prefix, args.rup_solver, args.skip_drup)


if __name__ == "__main__":
    main()
