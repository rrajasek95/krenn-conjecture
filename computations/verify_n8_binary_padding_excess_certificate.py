#!/usr/bin/env python3
"""Validate, minimize, and freeze binary-excess obstruction schemas.

The input JSON is produced by ``search_n8_binary_padding_excess.py``.  Each
schema is a necessary condition on the support of an exact realization:

* ``singletons``: a supported mixed monomial needs another supported term;
* ``cores``: an inconsistent family of exact signed binomials must change;
* ``zero_products``: fixed mixed binomials annihilate a fixed pure product.

The script checks those algebraic meanings without trusting the CEGAR run,
builds their CNF conjunction with the seed and binary-excess bound, and checks
UNSAT with two independent SAT engines.  ``--minimize-to`` extracts and then
deletion-minimizes an assumption core.  ``--write-certificate`` emits DIMACS
and a deletion-free DRUP transcript for ``verify_drup_certificate.py``.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver

import search_n8_binary_padding_completion as binary
import search_n8_sparse_triple_completion as sparse


N = 8


def _fibre(raw):
    colouring, numbers = raw
    return tuple(colouring), tuple(numbers)


def load_schemas(path: Path):
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {
        "binary_cap": int(raw["binary_cap"]),
        "singletons": tuple(
            (tuple(colouring), int(trigger))
            for colouring, trigger in raw["singletons"]
        ),
        "cores": tuple(
            tuple(_fibre(item) for item in schema)
            for schema in raw["cores"]
        ),
        "zero_products": tuple(
            tuple(_fibre(item) for item in schema)
            for schema in raw["zero_products"]
        ),
        "fibre_statuses": tuple(
            (
                item["proof_kind"],
                bool(item["include_pure"]),
                tuple(_fibre(fibre) for fibre in item["fibres"]),
            )
            for item in raw.get("fibre_statuses", ())
        ),
    }


def dump_schemas(path: Path, schemas) -> None:
    def fibre(item):
        colouring, numbers = item
        return [list(colouring), list(numbers)]

    payload = {
        "binary_cap": schemas["binary_cap"],
        "singletons": [
            [list(colouring), trigger]
            for colouring, trigger in schemas["singletons"]
        ],
        "cores": [
            [fibre(item) for item in schema]
            for schema in schemas["cores"]
        ],
        "zero_products": [
            [fibre(item) for item in schema]
            for schema in schemas["zero_products"]
        ],
        "fibre_statuses": [
            {
                "proof_kind": proof_kind,
                "include_pure": include_pure,
                "fibres": [fibre(item) for item in schema],
            }
            for proof_kind, include_pure, schema in schemas.get(
                "fibre_statuses", ()
            )
        ],
    }
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


class CertificateFormula:
    """CNF encoding, optionally with one assumption per semantic schema."""

    def __init__(self, schemas, *, activated=False):
        self.schemas = schemas
        self.pool = IDPool()
        self.cells = tuple(sorted(binary.ALL_CELLS))
        self.cell_index = {cell: index for index, cell in enumerate(self.cells)}
        self.support = {
            cell: self.pool.id(("support", cell)) for cell in self.cells
        }
        self.matchings = tuple(
            sparse.toric.perfect_matchings(tuple(range(N)))
        )
        self.clauses = []
        self.term_variables = {}
        self.activations = {}
        self.activated = activated

        assert len(self.cells) == 252
        assert len(self.matchings) == 105
        for cell in sorted(binary.SEED):
            self.clauses.append([self.support[cell]])

        cardinality = CardEnc.atmost(
            lits=[self.support[cell] for cell in sorted(binary.FORBIDDEN)],
            bound=schemas["binary_cap"],
            top_id=self.pool.top,
            encoding=EncType.kmtotalizer,
        )
        self.pool.occupy(self.pool.top + 1, cardinality.nv)
        self.clauses.extend(cardinality.clauses)

        for index, (colouring, trigger) in enumerate(schemas["singletons"]):
            clause = [-self.term_indicator(colouring, trigger)]
            clause.extend(
                self.term_indicator(colouring, number)
                for number in range(len(self.matchings))
                if number != trigger
            )
            self.add_schema_clause("S", index, clause)

        for index, schema in enumerate(schemas["cores"]):
            clause = []
            for colouring, present in schema:
                clause.extend(self.exact_fibre_literals(colouring, present))
            self.add_schema_clause("O", index, clause)

        for index, schema in enumerate(schemas["zero_products"]):
            clause = []
            for colouring, present in schema:
                clause.extend(self.exact_fibre_literals(colouring, present))
            self.add_schema_clause("Z", index, clause)

        for index, (_proof_kind, _include_pure, schema) in enumerate(
            schemas["fibre_statuses"]
        ):
            clause = []
            for colouring, present in schema:
                clause.extend(self.exact_fibre_literals(colouring, present))
            self.add_schema_clause("M", index, clause)

    def terms(self, colouring):
        return tuple(
            frozenset(
                (u, v, colouring[u], colouring[v]) for u, v in matching
            )
            for matching in self.matchings
        )

    def term_indicator(self, colouring, matching_number):
        key = tuple(colouring), matching_number
        answer = self.term_variables.get(key)
        if answer is not None:
            return answer
        answer = self.pool.id(("term", key))
        decorated = self.terms(tuple(colouring))[matching_number]
        for cell in sorted(decorated):
            self.clauses.append([-answer, self.support[cell]])
        self.clauses.append(
            [answer] + [-self.support[cell] for cell in sorted(decorated)]
        )
        self.term_variables[key] = answer
        return answer

    def exact_fibre_literals(self, colouring, present):
        present = frozenset(present)
        return [
            -self.term_indicator(colouring, number)
            if number in present
            else self.term_indicator(colouring, number)
            for number in range(len(self.matchings))
        ]

    def add_schema_clause(self, kind, index, clause):
        assert clause
        if self.activated:
            activation = self.pool.id(("activation", kind, index))
            self.activations[kind, index] = activation
            clause = list(clause) + [-activation]
        self.clauses.append(list(clause))


def validate_algebra(formula: CertificateFormula) -> None:
    schemas = formula.schemas

    assert len(set(schemas["singletons"])) == len(schemas["singletons"])
    assert len(set(schemas["cores"])) == len(schemas["cores"])
    assert len(set(schemas["zero_products"])) == len(
        schemas["zero_products"]
    )

    for colouring, trigger in schemas["singletons"]:
        assert len(colouring) == N and len(set(colouring)) > 1
        assert 0 <= trigger < len(formula.matchings)
        assert len(formula.terms(colouring)[trigger]) == N // 2

    for schema in schemas["cores"]:
        rows = []
        assert schema
        for colouring, present in schema:
            assert len(colouring) == N and len(set(colouring)) > 1
            assert len(present) == 2 and len(set(present)) == 2
            terms = formula.terms(colouring)
            rows.append(sparse.toric.exponent_row(
                terms[present[0]], terms[present[1]],
                formula.cell_index, len(formula.cells),
            ))
        consistent, _lattice = sparse.toric.signed_quotient_lattice(
            rows, len(formula.cells)
        )
        assert not consistent

    for schema in schemas["zero_products"]:
        rows = []
        fibres = {}
        pure_colours = []
        for colouring, present in schema:
            assert len(colouring) == N
            terms = formula.terms(colouring)
            fibres[colouring] = tuple(
                (number, terms[number]) for number in present
            )
            if len(set(colouring)) == 1:
                pure_colours.append(colouring[0])
            else:
                assert len(present) == 2 and len(set(present)) == 2
                rows.append(sparse.toric.exponent_row(
                    terms[present[0]], terms[present[1]],
                    formula.cell_index, len(formula.cells),
                ))
        assert rows and pure_colours
        consistent, lattice = sparse.toric.signed_quotient_lattice(
            rows, len(formula.cells)
        )
        assert consistent
        remainder, _classes = sparse.toric.reduced_constant_product(
            N,
            fibres,
            lattice,
            formula.cells,
            formula.cell_index,
            colors=tuple(sorted(pure_colours)),
        )
        assert not remainder

    for proof_kind, include_pure, schema in schemas["fibre_statuses"]:
        fibres = {}
        for colouring, present in schema:
            assert len(colouring) == N
            assert include_pure or len(set(colouring)) > 1
            terms = formula.terms(colouring)
            fibres[colouring] = tuple(
                (number, terms[number]) for number in present
            )

        mixed, rows = sparse.binomial_system(formula, fibres)
        if proof_kind == "monomial":
            consistent, lattice = sparse.toric.signed_quotient_lattice(
                rows, len(formula.cells)
            )
            assert consistent
            remainders = [
                sparse.reduced_polynomial(formula, terms, lattice)
                for colouring, terms in fibres.items()
                if len(set(colouring)) > 1
            ]
            assert any(len(remainder) == 1 for remainder in remainders)
        elif proof_kind in ("closure_inconsistent", "closure_monomial"):
            closure = sparse.quotient_binomial_closure(formula, fibres, rows)
            assert closure["status"] == proof_kind.removeprefix("closure_")
        elif proof_kind == "closure_zero_pure":
            closure = sparse.quotient_binomial_closure(formula, fibres, rows)
            assert closure["status"] not in ("inconsistent", "monomial")
            pure_product, _classes = sparse.toric.reduced_constant_product(
                N,
                fibres,
                closure["lattice"],
                formula.cells,
                formula.cell_index,
            )
            assert not pure_product
        else:
            raise AssertionError(f"unsupported fibre proof kind {proof_kind}")


def minimize_schemas(schemas, solver_name="glucose42", *, deletion=True):
    formula = CertificateFormula(schemas, activated=True)
    validate_algebra(formula)
    assumptions = tuple(formula.activations.values())
    with Solver(
        name=solver_name, bootstrap_with=formula.clauses
    ) as solver:
        assert not solver.solve(assumptions=assumptions)
        core = set(solver.get_core() or ())
        assert core and core <= set(assumptions)
        print(
            f"initial assumption core: {len(core)}/{len(assumptions)}",
            flush=True,
        )
        if deletion:
            for step, activation in enumerate(tuple(sorted(core)), 1):
                trial = sorted(core - {activation})
                if not solver.solve(assumptions=trial):
                    core.remove(activation)
                if step % 25 == 0:
                    print(
                        f"core deletion step={step} remaining={len(core)}",
                        flush=True,
                    )

    reverse = {value: key for key, value in formula.activations.items()}
    chosen = {reverse[activation] for activation in core}
    return {
        "binary_cap": schemas["binary_cap"],
        "singletons": tuple(
            schema for index, schema in enumerate(schemas["singletons"])
            if ("S", index) in chosen
        ),
        "cores": tuple(
            schema for index, schema in enumerate(schemas["cores"])
            if ("O", index) in chosen
        ),
        "zero_products": tuple(
            schema for index, schema in enumerate(schemas["zero_products"])
            if ("Z", index) in chosen
        ),
        "fibre_statuses": tuple(
            schema
            for index, schema in enumerate(schemas["fibre_statuses"])
            if ("M", index) in chosen
        ),
    }


def write_dimacs(path: Path, variables: int, clauses) -> None:
    with path.open("w", encoding="ascii") as stream:
        stream.write(f"p cnf {variables} {len(clauses)}\n")
        for clause in clauses:
            stream.write(" ".join(map(str, clause)) + " 0\n")


def write_certificate(prefix: Path, formula: CertificateFormula) -> None:
    cnf_path = prefix.with_suffix(".cnf")
    proof_path = prefix.with_suffix(".drup")
    write_dimacs(cnf_path, formula.pool.top, formula.clauses)
    with Solver(
        name="glucose42", bootstrap_with=formula.clauses, with_proof=True
    ) as solver:
        assert not solver.solve()
        proof = solver.get_proof() or []
    additions = [line for line in proof if not line.startswith("d ")]
    assert additions and additions[-1].strip() == "0"
    proof_path.write_text("\n".join(additions) + "\n", encoding="ascii")
    print(f"wrote {cnf_path} and {proof_path}")


def verify(schemas, write_prefix=None) -> CertificateFormula:
    formula = CertificateFormula(schemas)
    validate_algebra(formula)
    results = {}
    for solver_name in ("cadical300", "glucose42"):
        with Solver(name=solver_name, bootstrap_with=formula.clauses) as solver:
            results[solver_name] = solver.solve()
    assert results == {"cadical300": False, "glucose42": False}
    print(
        f"binary-excess-{schemas['binary_cap']} obstruction: PASS; "
        f"variables={formula.pool.top} clauses={len(formula.clauses)} "
        f"S={len(schemas['singletons'])} O={len(schemas['cores'])} "
        f"Z={len(schemas['zero_products'])} "
        f"M={len(schemas['fibre_statuses'])}",
        flush=True,
    )
    if write_prefix is not None:
        write_certificate(write_prefix, formula)
    return formula


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("schemas", type=Path)
    parser.add_argument("--minimize-to", type=Path)
    parser.add_argument(
        "--assumption-core-only",
        action="store_true",
        help="skip the slower deletion-minimal refinement",
    )
    parser.add_argument("--write-certificate", type=Path)
    args = parser.parse_args()

    schemas = load_schemas(args.schemas)
    if args.minimize_to is not None:
        schemas = minimize_schemas(
            schemas, deletion=not args.assumption_core_only
        )
        dump_schemas(args.minimize_to, schemas)
        print(f"wrote minimized schemas to {args.minimize_to}", flush=True)
    verify(schemas, args.write_certificate)


if __name__ == "__main__":
    main()
