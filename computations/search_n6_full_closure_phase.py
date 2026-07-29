#!/usr/bin/env python3
"""Exact at-most-35 search for a phase-consistent six-site closure.

Unlike the discovery MaxSAT loop, this script builds the complete
no-mixed-singleton support formula up front.  It then learns only semantic
clauses excluding collections of exact binomial fibres whose Laurent rows
have an odd integer dependence.  An UNSAT result therefore proves that every
35-cell no-singleton extension of the fixed seed has an inconsistent exact
binomial subsystem.

With ``--proof-prefix``, every semantic core is recorded in JSON and the final
CNF plus a deletion-free DRUP trace are written for independent replay.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

import optimize_hamiltonian_cycle_cover_closure as closure_module
import search_parallel_binomial_nonzero_constants_cegar as toric


N = 6
Q = 3

# A checked minimum no-singleton support.  This is only a polarity hint; it is
# not asserted, so it cannot affect SAT or UNSAT correctness.
PHASE_HINT_ADDED = frozenset(
    {
        (0, 1, 2, 0),
        (0, 2, 0, 1),
        (0, 2, 0, 2),
        (0, 2, 2, 1),
        (0, 3, 0, 2),
        (0, 3, 2, 1),
        (0, 3, 2, 2),
        (0, 4, 0, 0),
        (0, 4, 2, 0),
        (0, 4, 2, 1),
        (1, 5, 0, 0),
        (2, 5, 1, 2),
        (2, 5, 2, 0),
        (2, 5, 2, 2),
        (3, 5, 1, 0),
        (3, 5, 1, 2),
        (3, 5, 2, 0),
        (4, 5, 0, 2),
        (4, 5, 1, 0),
        (4, 5, 1, 2),
    }
)


def word_text(word):
    return "".join(map(str, word))


class FullPhaseSearch:
    def __init__(
        self,
        cap,
        solver_name,
        proof_prefix=None,
        proof_solver="glucose4",
        minimum=None,
    ):
        self.cap = cap
        self.minimum = minimum
        assert minimum is None or minimum <= cap
        self.solver_name = solver_name
        self.proof_prefix = Path(proof_prefix) if proof_prefix else None
        self.proof_solver = proof_solver
        self.pool = toric.Pool()
        self.cells = tuple(
            (u, v, a, b)
            for u, v in combinations(range(N), 2)
            for a, b in product(range(Q), repeat=2)
        )
        self.cell_index = {cell: index for index, cell in enumerate(self.cells)}
        self.support = {cell: self.pool.new() for cell in self.cells}
        self.seed = closure_module.module(N)
        self.matchings = tuple(toric.perfect_matchings(tuple(range(N))))
        self.term_variables = {}
        self.term_cells = {}
        self.clauses = [[self.support[cell]] for cell in sorted(self.seed)]

        cardinality = CardEnc.atmost(
            lits=[self.support[cell] for cell in self.cells],
            bound=cap,
            top_id=self.pool.top,
            encoding=EncType.kmtotalizer,
        )
        self.pool.top = cardinality.nv
        self.clauses.extend(cardinality.clauses)
        if minimum is not None:
            lower_cardinality = CardEnc.atleast(
                lits=[self.support[cell] for cell in self.cells],
                bound=minimum,
                top_id=self.pool.top,
                encoding=EncType.kmtotalizer,
            )
            self.pool.top = lower_cardinality.nv
            self.clauses.extend(lower_cardinality.clauses)

        for word in product(range(Q), repeat=N):
            fibre_variables = []
            for number, matching in enumerate(self.matchings):
                decorated = tuple(
                    (u, v, word[u], word[v]) for u, v in matching
                )
                term = self.pool.new()
                self.term_variables[word, number] = term
                self.term_cells[word, number] = decorated
                fibre_variables.append(term)
                self.clauses.extend(
                    [-term, self.support[cell]] for cell in decorated
                )
                self.clauses.append(
                    [term] + [-self.support[cell] for cell in decorated]
                )
            if len(set(word)) > 1:
                # A nonempty mixed fibre cannot contain exactly one term.
                self.clauses.extend(
                    [-term]
                    + [other for other in fibre_variables if other != term]
                    for term in fibre_variables
                )

        self.base_clause_count = len(self.clauses)
        self.phase_core_keys = set()
        self.phase_core_records = []
        self.solver = Solver(
            name=solver_name,
            bootstrap_with=self.clauses,
        )
        self.solver.set_phases(
            [
                self.support[cell]
                if cell in self.seed or cell in PHASE_HINT_ADDED
                else -self.support[cell]
                for cell in self.cells
            ]
        )

    def delete(self):
        self.solver.delete()

    def decode(self, model):
        positive = {literal for literal in model if literal > 0}
        return frozenset(
            cell for cell in self.cells if self.support[cell] in positive
        )

    def exact_fibres(self, selected):
        return toric.exact_fibres(N, selected, self.matchings)

    def binomial_system(self, fibres):
        mixed = [
            (word, terms)
            for word, terms in sorted(fibres.items())
            if len(set(word)) > 1 and len(terms) == 2
        ]
        rows = [
            toric.exponent_row(
                terms[0][1], terms[1][1], self.cell_index, len(self.cells)
            )
            for _word, terms in mixed
        ]
        return mixed, rows

    def core_key(self, mixed, row_indices):
        return tuple(
            sorted(
                (
                    word,
                    tuple(number for number, _decorated in terms),
                )
                for index in row_indices
                for word, terms in (mixed[index],)
            )
        )

    def audit_core(self, rows, row_indices):
        selected_rows = [rows[index] for index in row_indices]
        assert selected_rows
        assert not toric.signed_quotient_lattice(
            selected_rows, len(self.cells)
        )[0]

    def add_phase_core(self, mixed, rows, row_indices):
        self.audit_core(rows, row_indices)
        key = self.core_key(mixed, row_indices)
        if key in self.phase_core_keys:
            return False

        clause = []
        record_rows = []
        for word, present_numbers in key:
            present = set(present_numbers)
            assert len(present) == 2
            clause.extend(
                -self.term_variables[word, number]
                if number in present
                else self.term_variables[word, number]
                for number in range(len(self.matchings))
            )
            record_rows.append(
                {"word": word_text(word), "terms": list(present_numbers)}
            )
        self.solver.add_clause(clause)
        self.clauses.append(clause)
        self.phase_core_keys.add(key)
        self.phase_core_records.append({"rows": record_rows})
        return True

    @staticmethod
    def unit_triangle_circuits(rows):
        if len(rows) < 3:
            return ()
        rows = tuple(map(tuple, rows))
        locations = {}
        for index, row in enumerate(rows):
            locations.setdefault(row, []).append(index)
        circuits = set()
        for left in range(len(rows)):
            for right in range(left + 1, len(rows)):
                for left_sign in (-1, 1):
                    for right_sign in (-1, 1):
                        target = tuple(
                            -(left_sign * a + right_sign * b)
                            for a, b in zip(rows[left], rows[right])
                        )
                        for third in locations.get(target, ()):
                            if third not in (left, right):
                                circuits.add(tuple(sorted((left, right, third))))
        return tuple(sorted(circuits))

    def write_formula_bundle(self):
        assert self.proof_prefix is not None
        top = self.pool.top
        dimacs = [f"p cnf {top} {len(self.clauses)}\n"]
        dimacs.extend(
            " ".join(map(str, clause)) + " 0\n" for clause in self.clauses
        )
        cnf_data = "".join(dimacs).encode("ascii")
        cnf_path = self.proof_prefix.with_suffix(".cnf")
        proof_path = self.proof_prefix.with_suffix(".drup")
        json_path = self.proof_prefix.with_suffix(".json")
        payload = {
            "order": N,
            "cap": self.cap,
            "minimum": self.minimum,
            "variables": top,
            "base_clauses": self.base_clause_count,
            "clauses": len(self.clauses),
            "phase_cores": self.phase_core_records,
            "cnf_sha256": hashlib.sha256(cnf_data).hexdigest(),
            "drup_lines": None,
        }
        # Persist the semantic formula before the potentially slower proof
        # replay.  The absent DRUP file and null line count make an unfinished
        # bundle unmistakable.
        cnf_path.write_bytes(cnf_data)
        json_path.write_text(json.dumps(payload, indent=2) + "\n")
        print(
            f"FORMULA_BUNDLE cnf={cnf_path} semantics={json_path}",
            flush=True,
        )
        return cnf_path, proof_path, json_path, payload

    def write_certificate(self):
        (
            cnf_path,
            proof_path,
            json_path,
            payload,
        ) = self.write_formula_bundle()

        # Search with the fastest backend, then replay the final formula once
        # in a proof-capable solver.  The trace is therefore relative to the
        # exact final CNF rather than to an incremental solver's hidden state.
        with Solver(
            name=self.proof_solver,
            bootstrap_with=self.clauses,
            with_proof=True,
        ) as proof_solver:
            assert not proof_solver.solve()
            proof = proof_solver.get_proof() or []
        proof = [line for line in proof if not line.startswith("d ")]
        if not proof or proof[-1].strip() != "0":
            raise RuntimeError("proof trace does not end in the empty clause")
        proof_path.write_text("\n".join(proof) + "\n", encoding="ascii")
        payload["drup_lines"] = len(proof)
        json_path.write_text(json.dumps(payload, indent=2) + "\n")
        print(
            f"CERTIFICATE cnf={cnf_path} proof={proof_path} "
            f"semantics={json_path} proof_lines={len(proof)}",
            flush=True,
        )


def search(cap, solver_name, max_rounds, proof_prefix, proof_solver, minimum):
    searcher = FullPhaseSearch(
        cap, solver_name, proof_prefix, proof_solver, minimum
    )
    try:
        print(
            f"FULL_FORMULA cells={len(searcher.cells)} seed={len(searcher.seed)} "
            f"matchings={len(searcher.matchings)} variables={searcher.pool.top} "
            f"clauses={len(searcher.clauses)} cap={cap} minimum={minimum}",
            flush=True,
        )
        for round_number in range(max_rounds):
            if not searcher.solver.solve():
                print(
                    f"UNSAT cap={cap} rounds={round_number} "
                    f"phase_cores={len(searcher.phase_core_records)} "
                    f"clauses={len(searcher.clauses)}",
                    flush=True,
                )
                if searcher.proof_prefix is not None:
                    searcher.write_certificate()
                return None

            selected = searcher.decode(searcher.solver.get_model())
            fibres = searcher.exact_fibres(selected)
            histogram = Counter(
                len(terms)
                for word, terms in fibres.items()
                if len(set(word)) > 1
            )
            assert 1 not in histogram
            mixed, rows = searcher.binomial_system(fibres)
            consistent, lattice = toric.signed_quotient_lattice(
                rows, len(searcher.cells)
            )
            if consistent:
                pure_sizes = tuple(
                    len(fibres[(colour,) * N]) for colour in range(Q)
                )
                pure_product, _classes = toric.reduced_constant_product(
                    N,
                    fibres,
                    lattice,
                    searcher.cells,
                    searcher.cell_index,
                )
                print(
                    f"PHASE_CONSISTENT cap={cap} round={round_number} "
                    f"cells={len(selected)} pure_sizes={pure_sizes} "
                    f"histogram={dict(sorted(histogram.items()))} "
                    f"binomials={len(rows)} "
                    f"pure_product_classes={len(pure_product)}",
                    flush=True,
                )
                print("EXTRA", sorted(selected - searcher.seed), flush=True)
                return selected

            triangles = searcher.unit_triangle_circuits(rows)
            added = sum(
                searcher.add_phase_core(mixed, rows, indices)
                for indices in triangles
            )
            fallback_size = None
            if not added:
                relation = toric.flint_odd_relation(rows)
                indices = tuple(
                    index
                    for index, coefficient in enumerate(relation or ())
                    if coefficient
                )
                if not indices:
                    indices = tuple(range(len(rows)))
                assert searcher.add_phase_core(mixed, rows, indices)
                added = 1
                fallback_size = len(indices)
            print(
                f"round={round_number} cells={len(selected)} "
                f"histogram={dict(sorted(histogram.items()))} "
                f"inconsistent_binomials={len(rows)} "
                f"triangles={len(triangles)} add_cores={added} "
                f"fallback_size={fallback_size} "
                f"total_cores={len(searcher.phase_core_records)}",
                flush=True,
            )
        print(
            f"BOUNDARY cap={cap} rounds={max_rounds} "
            f"phase_cores={len(searcher.phase_core_records)}",
            flush=True,
        )
        return None
    finally:
        searcher.delete()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cap", type=int, default=35)
    parser.add_argument(
        "--minimum",
        type=int,
        help="optional lower support bound (e.g. 35 from the minimum lemma)",
    )
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--proof-solver", default="glucose4")
    parser.add_argument("--max-rounds", type=int, default=10000)
    parser.add_argument("--proof-prefix")
    args = parser.parse_args()
    search(
        args.cap,
        args.solver,
        args.max_rounds,
        args.proof_prefix,
        args.proof_solver,
        args.minimum,
    )


if __name__ == "__main__":
    main()
