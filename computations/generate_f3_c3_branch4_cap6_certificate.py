#!/usr/bin/env python3
"""Generate the compact DRUP certificate for C3 branch 4 at cell cap 6."""

from pathlib import Path

from pysat.solvers import Solver

import search_f3_c3_equivariant_n8 as search


EQUATIONS = (0, 756, 1367, 1876)
PREFIX = Path(__file__).resolve().parent / "cert_f3_c3_branch4_cap6"


class ClauseCollector:
    def __init__(self):
        self.clauses = []

    def append_formula(self, clauses):
        self.clauses.extend(tuple(clause) for clause in clauses)


def build_certificate_cnf():
    pool, base_clauses, rows = search.build_base(max_nonzero=6)
    collector = ClauseCollector()
    encoder = search.EquationEncoder(pool, collector, rows)
    for equation in EQUATIONS:
        encoder.add_equation(equation)
    clauses = [tuple(clause) for clause in base_clauses]
    clauses.extend(collector.clauses)
    clauses.extend((literal,) for literal in search.branch_assumptions(rows, 4))
    assert pool.top == 3491
    assert len(clauses) == 13736
    return pool.top, tuple(clauses)


def main():
    variables, clauses = build_certificate_cnf()
    cnf_lines = [f"p cnf {variables} {len(clauses)}"]
    cnf_lines.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    PREFIX.with_suffix(".cnf").write_text("\n".join(cnf_lines) + "\n")

    with Solver(name="glucose42", bootstrap_with=clauses, with_proof=True) as solver:
        assert not solver.solve()
        raw_proof = solver.get_proof()
    # Keeping deleted clauses can only strengthen unit propagation, so
    # deletion records may be discarded from a DRUP trace.
    additions = [line for line in raw_proof if not line.startswith("d")]
    assert additions and additions[-1].strip() == "0"
    PREFIX.with_suffix(".drup").write_text("\n".join(additions) + "\n")
    print(
        f"WROTE {PREFIX}.{{cnf,drup}} variables={variables} "
        f"clauses={len(clauses)} rup_additions={len(additions)}"
    )


if __name__ == "__main__":
    main()
