#!/usr/bin/env python3
"""Generate deletion-free DRUP proofs for the diagonal N=8 range.

The underlying CNF is the audited occurrence encoding with no lower bound
on the number of noncoordinate edge supports.  Thus each case covers every
support with 18 through 27 live physical edges in the indicated normalized
target chart.  The lower endpoint 12 is forced independently by the 24
singleton coordinate-anchor incidences: each physical edge can serve at
most two incidences and cannot be singleton-supported in two colours.
"""

from __future__ import annotations

import argparse
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_search():
    path = HERE / "search_n8_global_occurrence_cnf.py"
    spec = spec_from_file_location("n8_global_occurrence_cnf_range", path)
    require(spec is not None and spec.loader is not None, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


C = load_search()


def build_range_cnf(target_support):
    cnf, *_rest = C.build_instance(
        support_size=None,
        target_support=target_support,
        degree_sequence=None,
        minimum_nonanchors=0,
        minimum_support_size=12,
        maximum_support_size=27,
    )
    require(len(cnf.names) == 9198, len(cnf.names))
    require(len(cnf.clauses) == 54028, len(cnf.clauses))
    return cnf


def main():
    from pysat.solvers import Solver

    parser = argparse.ArgumentParser()
    parser.add_argument("--target-support", choices=("12", "012"),
                        required=True)
    parser.add_argument("--prefix", type=Path, required=True)
    arguments = parser.parse_args()
    target_support = tuple(map(int, arguments.target_support))

    cnf = build_range_cnf(target_support)
    cnf_path = arguments.prefix.with_suffix(".cnf")
    proof_path = arguments.prefix.with_suffix(".drup")
    cnf_path.write_text(cnf.dimacs(), encoding="ascii")

    with Solver(name="glucose42", bootstrap_with=cnf.clauses,
                with_proof=True) as solver:
        require(not solver.solve(), "range occurrence CNF is SAT")
        proof = solver.get_proof() or []
    additions = [line for line in proof if not line.startswith("d ")]
    require(additions and additions[-1].strip() == "0",
            "proof does not end in the empty clause")
    proof_path.write_text("\n".join(additions) + "\n", encoding="ascii")

    print("target", arguments.target_support)
    print("variables", len(cnf.names), "clauses", len(cnf.clauses))
    print("proof_additions", len(additions))
    print("cnf", cnf_path)
    print("proof", proof_path)


if __name__ == "__main__":
    main()
