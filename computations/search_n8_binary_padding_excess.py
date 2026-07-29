#!/usr/bin/env python3
"""Exact arbitrary-density search by principal-binary excess above the seed.

This is the binary-padding specialization of
``search_n8_sparse_triple_completion.py``.  In addition to a cardinality
bound on the 99 absent principal 0/1 cells, it learns a generalized exact
mixed-fibre-status cut when quotient closure proves a support impossible.
The cut forgets all irrelevant pure-fibre support, avoiding exponential
re-enumeration of the same mixed Laurent system.

An ``UNSAT`` result is exact over C provided no ``SURVIVOR`` was printed.
Any survivor is returned immediately for separate algebraic analysis.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

from pysat.card import CardEnc, EncType

import factorized_laurent_branches as factorized
import search_n8_binary_padding_completion as binary
import search_n8_sparse_triple_completion as sparse
import search_n8_toric_binomial_lazy_cegar as toric_search


class BinaryExcessSearch(sparse.SparseCompletionSearch):
    def __init__(self, total_cap, solver_name, binary_cap):
        super().__init__(
            total_cap,
            solver_name,
            seed_cells=binary.SEED,
        )
        cardinality = CardEnc.atmost(
            lits=[self.support[cell] for cell in sorted(binary.FORBIDDEN)],
            bound=binary_cap,
            top_id=self.pool.top,
            encoding=EncType.kmtotalizer,
        )
        self.pool.top = cardinality.nv
        for clause in cardinality.clauses:
            self.solver.add_clause(clause)
        self.mixed_status_cuts = 0
        self.zero_product_schemas = set()
        self.fibre_status_schemas = set()

    @staticmethod
    def _fibre_schema(colouring, terms):
        return (
            tuple(colouring),
            tuple(sorted(number for number, _term in terms)),
        )

    def add_zero_product_nogood(self, fibres, mixed, used_rows, colours):
        """Record and add an exact quotient/pure-product certificate."""

        schema = []
        for index in used_rows:
            colouring, terms = mixed[index]
            schema.append(self._fibre_schema(colouring, terms))
        for colour in colours:
            colouring = (colour,) * sparse.N
            schema.append(self._fibre_schema(colouring, fibres[colouring]))
        self.zero_product_schemas.add(tuple(sorted(schema)))
        return super().add_zero_product_nogood(
            fibres, mixed, used_rows, colours
        )

    def add_exact_fibre_status_nogood(
        self, fibres, *, include_pure: bool, proof_kind: str
    ) -> int:
        """Block the same exact nonempty mixed fibres (and optionally pure).

        The cited Laurent contradiction only uses these fibre polynomials.
        Altering support elsewhere cannot repair it, so this clause is
        stronger than an exact 252-cell support block and remains sound.
        """

        clause = set()
        cited = 0
        for colouring, terms in sorted(fibres.items()):
            pure = len(set(colouring)) == 1
            if pure and not include_pure:
                continue
            if not terms:
                continue
            if pure and colouring[0] not in range(sparse.Q):
                continue
            present = frozenset(number for number, _term in terms)
            for number in range(len(self.matchings)):
                indicator = self.term_indicator(colouring, number)
                clause.add(-indicator if number in present else indicator)
            cited += 1
        assert clause and cited
        self.solver.add_clause(sorted(clause))
        self.mixed_status_cuts += 1
        schema = tuple(sorted(
            self._fibre_schema(colouring, terms)
            for colouring, terms in fibres.items()
            if terms and (include_pure or len(set(colouring)) > 1)
        ))
        self.fibre_status_schemas.add((proof_kind, include_pure, schema))
        return len(clause)

    def add_monomial_core_nogood(self, fibres, mixed, rows, closure):
        """Greedily shrink a quotient-monomial contradiction to its rows."""

        targets = [
            colouring for colouring, remainder in closure["remainders"].items()
            if len(remainder) == 1
        ]
        assert targets and closure["rounds"] == 0
        target = min(targets)
        target_terms = fibres[target]
        used = list(range(len(rows)))

        def remains_monomial(indices):
            consistent, lattice = sparse.toric.signed_quotient_lattice(
                [rows[index] for index in indices], len(self.cells)
            )
            assert consistent
            return len(sparse.reduced_polynomial(
                self, target_terms, lattice
            )) == 1

        assert remains_monomial(used)
        for index in tuple(used):
            trial = [item for item in used if item != index]
            if remains_monomial(trial):
                used = trial

        core_fibres = {target: target_terms}
        for index in used:
            colouring, terms = mixed[index]
            core_fibres[colouring] = terms
        cut_size = self.add_exact_fibre_status_nogood(
            core_fibres,
            include_pure=False,
            proof_kind="monomial",
        )
        return cut_size, len(core_fibres), len(used)

    def write_schemas(self, path: Path) -> None:
        """Write all learned semantic schemas in deterministic JSON."""

        def fibre(item):
            colouring, numbers = item
            return [list(colouring), list(numbers)]

        payload = {
            "binary_cap": self.binary_cap,
            "singletons": [
                [list(colouring), trigger]
                for colouring, trigger in sorted(self.singleton_gadgets)
            ],
            "cores": [
                [fibre(item) for item in schema]
                for schema in sorted(self.core_gadgets)
            ],
            "zero_products": [
                [fibre(item) for item in schema]
                for schema in sorted(self.zero_product_schemas)
            ],
            "fibre_statuses": [
                {
                    "proof_kind": proof_kind,
                    "include_pure": include_pure,
                    "fibres": [fibre(item) for item in schema],
                }
                for proof_kind, include_pure, schema in sorted(
                    self.fibre_status_schemas
                )
            ],
        }
        path.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def run(binary_cap, total_cap, solver_name, max_rounds, core_batch,
        dump_schemas=None):
    search = BinaryExcessSearch(total_cap, solver_name, binary_cap)
    search.binary_cap = binary_cap
    try:
        seed_fibres = sparse.exact_fibres(search, search.seed)
        seed_histogram = Counter(
            len(terms)
            for colouring, terms in seed_fibres.items()
            if len(set(colouring)) > 1
        )
        print(
            f"binary_cap={binary_cap} total_cap={total_cap} "
            f"seed_cells={len(search.seed)} "
            f"mixed_histogram={dict(seed_histogram)}",
            flush=True,
        )

        for round_number in range(max_rounds):
            if not search.solver.solve():
                print(
                    f"UNSAT binary_cap={binary_cap} total_cap={total_cap} "
                    f"rounds={round_number} "
                    f"singleton_gadgets={len(search.singleton_gadgets)} "
                    f"core_gadgets={len(search.core_gadgets)} "
                    f"zero_product_cuts={search.zero_product_cuts} "
                    f"mixed_status_cuts={search.mixed_status_cuts}",
                    flush=True,
                )
                if dump_schemas is not None:
                    search.write_schemas(dump_schemas)
                return None

            selected = search.decode(search.solver.get_model())
            fibres = sparse.exact_fibres(search, selected)
            singletons = [
                (colouring, terms[0][0])
                for colouring, terms in sorted(fibres.items())
                if len(set(colouring)) > 1 and len(terms) == 1
            ]
            if singletons:
                added = sum(
                    search.add_singleton_gadget(colouring, trigger)
                    for colouring, trigger in singletons
                )
                assert added
                if round_number < 20 or round_number % 20 == 0:
                    print(
                        f"round={round_number} cells={len(selected)} "
                        f"singletons={len(singletons)} add={added}",
                        flush=True,
                    )
                continue

            mixed, rows = sparse.binomial_system(search, fibres)
            consistent, lattice = sparse.toric.signed_quotient_lattice(
                rows, len(search.cells)
            )
            histogram = Counter(
                len(terms)
                for colouring, terms in fibres.items()
                if len(set(colouring)) > 1
            )
            if not consistent:
                triangles = toric_search.unit_triangle_circuits(rows)
                chosen = []
                for indices in triangles:
                    if len(chosen) >= core_batch:
                        break
                    if search.add_core_break_gadget(mixed, indices):
                        chosen.append(indices)
                if not chosen:
                    relation = sparse.toric.flint_odd_relation(rows)
                    indices = tuple(
                        index
                        for index, coefficient in enumerate(relation or ())
                        if coefficient
                    )
                    if not indices:
                        indices = tuple(range(len(rows)))
                    assert search.add_core_break_gadget(mixed, indices)
                    chosen = [indices]
                print(
                    f"round={round_number} cells={len(selected)} "
                    f"histogram={dict(sorted(histogram.items()))} "
                    f"inconsistent triangles={len(triangles)} "
                    f"add_cores={len(chosen)}",
                    flush=True,
                )
                continue

            pure_product, _classes = sparse.toric.reduced_constant_product(
                sparse.N,
                fibres,
                lattice,
                search.cells,
                search.cell_index,
            )
            if not pure_product:
                used_rows, colours = sparse.toric.minimize_zero_product_certificate(
                    sparse.N,
                    fibres,
                    rows,
                    search.cells,
                    search.cell_index,
                )
                cut_size = search.add_zero_product_nogood(
                    fibres, mixed, used_rows, colours
                )
                print(
                    f"round={round_number} cells={len(selected)} "
                    f"zero_product rows={len(used_rows)}/{len(rows)} "
                    f"colours={colours} cut_size={cut_size}",
                    flush=True,
                )
                continue

            closure = sparse.quotient_binomial_closure(search, fibres, rows)
            if closure["status"] in ("inconsistent", "monomial"):
                if closure["status"] == "monomial" and not closure["rounds"]:
                    cut_size, core_fibres, core_rows = (
                        search.add_monomial_core_nogood(
                            fibres, mixed, rows, closure
                        )
                    )
                    core_description = (
                        f" core_fibres={core_fibres} core_rows={core_rows}"
                    )
                else:
                    cut_size = search.add_exact_fibre_status_nogood(
                        fibres,
                        include_pure=False,
                        proof_kind=f"closure_{closure['status']}",
                    )
                    core_description = ""
                print(
                    f"round={round_number} cells={len(selected)} "
                    f"closure={closure['status']} "
                    f"closure_rounds={closure['rounds']} "
                    f"closure_rows={len(closure['rows'])} "
                    f"mixed_status_cut={cut_size}{core_description}",
                    flush=True,
                )
                continue
            closure_pure, _closure_classes = sparse.toric.reduced_constant_product(
                sparse.N,
                fibres,
                closure["lattice"],
                search.cells,
                search.cell_index,
            )
            if not closure_pure:
                cut_size = search.add_exact_fibre_status_nogood(
                    fibres,
                    include_pure=True,
                    proof_kind="closure_zero_pure",
                )
                print(
                    f"round={round_number} cells={len(selected)} "
                    f"closure_zero_pure closure_rounds={closure['rounds']} "
                    f"closure_rows={len(closure['rows'])} "
                    f"fibre_status_cut={cut_size}",
                    flush=True,
                )
                continue
            if closure["status"] == "solved":
                print(
                    "EXACT_BINOMIAL_CLOSURE_SURVIVOR "
                    f"cells={len(selected)} binary_excess="
                    f"{len((selected - binary.SEED) & binary.FORBIDDEN)}",
                    flush=True,
                )
                print("EXTRA", sorted(selected - binary.SEED), flush=True)
                return selected, fibres, closure["rows"], closure["lattice"]

            remainders = closure["remainders"]
            if remainders:
                branch = factorized.solve_factorized_branches(
                    remainders,
                    closure["rows"],
                    fibres,
                    sparse.N,
                    search.cells,
                    search.cell_index,
                    solver_name=solver_name,
                    base_rhs=closure["rhs"],
                )
                if branch.status == "exhausted":
                    cut_size = search.add_exact_fibre_status_nogood(
                        fibres,
                        include_pure=True,
                        proof_kind="factorized_exhausted",
                    )
                    print(
                        f"round={round_number} cells={len(selected)} "
                        f"factorized_exhausted branches={branch.branches} "
                        f"fibre_status_cut={cut_size}",
                        flush=True,
                    )
                    continue
                if branch.status == "survivor":
                    print(
                        "EXACT_FACTORIZED_TORIC_SURVIVOR "
                        f"cells={len(selected)} binary_excess="
                        f"{len((selected - binary.SEED) & binary.FORBIDDEN)}",
                        flush=True,
                    )
                    print("EXTRA", sorted(selected - binary.SEED), flush=True)
                    return selected, fibres, rows, branch.lattice

            print(
                f"SURVIVOR cells={len(selected)} "
                f"binary_excess={len((selected - binary.SEED) & binary.FORBIDDEN)} "
                f"histogram={dict(sorted(histogram.items()))} "
                f"closure={closure['status']} "
                f"remainders={len(remainders)}",
                flush=True,
            )
            print("EXTRA", sorted(selected - binary.SEED), flush=True)
            return selected, fibres, closure["rows"], closure["lattice"]

        print(
            f"BOUNDARY rounds={max_rounds} binary_cap={binary_cap}",
            flush=True,
        )
        if dump_schemas is not None:
            search.write_schemas(dump_schemas)
        return None
    finally:
        search.delete()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary-cap", type=int, required=True)
    parser.add_argument("--total-cap", type=int)
    parser.add_argument("--solver", default="cadical300")
    parser.add_argument("--max-rounds", type=int, default=100000)
    parser.add_argument("--core-batch", type=int, default=512)
    parser.add_argument("--dump-schemas", type=Path)
    args = parser.parse_args()
    run(
        args.binary_cap,
        args.total_cap,
        args.solver,
        args.max_rounds,
        args.core_batch,
        args.dump_schemas,
    )


if __name__ == "__main__":
    main()
