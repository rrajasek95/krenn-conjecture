#!/usr/bin/env python3
"""Replay the exact three-binary-excess obstruction for the n=8 seed.

The support contains the seventeen fixed cells of the rational binary source
plus the chosen colour-2 matching.  At most three of the other 99 principal
0/1 cells may be nonzero; cells involving colour 2 are unrestricted.

The certificate consists of only 110 necessary support conditions for an
exact realization:

* 100 mixed-monomial singleton implications; and
* 10 exact one-row pure-colour-0 annihilation nogoods.

Their CNF conjunction is UNSAT.  This script independently validates the
algebraic meaning of every clause, rebuilds the CNF, and checks UNSAT with
two solvers.  With ``--write-certificate PREFIX`` it also emits DIMACS and a
deletion-free DRUP trace suitable for ``verify_drup_certificate.py``.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver

import search_n8_binary_padding_completion as binary
import search_n8_sparse_triple_completion as sparse


N = 8
Q = 3


def parse_singletons(text: str):
    answer = []
    for line in text.strip().splitlines():
        word, number = line.split()
        colouring = tuple(map(int, word))
        assert len(colouring) == N and len(set(colouring)) > 1
        answer.append((colouring, int(number)))
    return tuple(answer)


SINGLETON_SCHEMAS = parse_singletons(
    """
21120011 30
11110111 60
00001011 0
00100000 1
20100011 15
11020011 15
21121011 60
11111011 45
00000100 1
00001000 1
11011011 21
11001011 51
10010102 28
11000111 66
10011020 24
01111222 90
00111000 9
00001222 2
00000002 1
21121210 90
21121011 45
21110100 91
11120002 91
11111011 60
11011020 24
21100000 31
11121111 45
11110111 45
11101222 47
10101020 49
01120000 31
00210000 1
00002122 2
00000102 1
21110101 91
12010000 16
11120101 62
11111000 46
00210101 13
00002010 1
00000222 2
00000211 0
00000022 2
21120100 62
21111111 60
11121010 46
11120102 62
11120100 62
11120000 31
00210100 13
00111011 6
00020000 1
00011020 9
00010102 13
22210000 31
21111111 45
21111010 75
12001011 51
10020000 16
00211010 9
00211000 9
00110111 3
00002111 0
00001020 1
00000020 1
22211011 60
21111022 60
21111011 60
21111002 60
21110111 45
11121000 46
11111000 75
11101020 46
10011211 21
01111020 75
00210111 3
00001211 0
00000111 0
21111000 75
21110102 91
11121022 45
11121011 45
11121002 45
11120122 60
11120111 60
01111211 60
00211011 6
00011211 6
20100000 16
11101211 45
11020000 16
21000000 1
10120000 1
00120000 1
00000202 1
21000011 0
10120011 0
00002211 0
21120000 31
00002222 2
"""
)


# (mixed colouring, its exact two matching numbers, exact pure-0 numbers).
PURE_ZERO_SCHEMAS = (
    (tuple(map(int, "21120000")), (31, 32), (1, 2, 16, 17)),
    (tuple(map(int, "00120000")), (1, 2), (1, 2, 16, 17)),
    (tuple(map(int, "01020000")), (16, 17), (1, 2, 16, 17)),
    (tuple(map(int, "01120000")), (31, 32), (1, 2)),
    (tuple(map(int, "00120000")), (1, 2), (1, 2)),
    (tuple(map(int, "11120000")), (31, 32), (1, 2)),
    (tuple(map(int, "11020000")), (16, 17), (1, 2)),
    (tuple(map(int, "21120000")), (31, 32), (1, 2)),
    (tuple(map(int, "00020000")), (1, 2), (1, 2)),
    (tuple(map(int, "10020000")), (16, 17), (1, 2)),
)


class CertificateFormula:
    def __init__(self):
        self.pool = IDPool()
        self.cells = tuple(sorted(binary.ALL_CELLS))
        self.cell_index = {cell: index for index, cell in enumerate(self.cells)}
        self.support = {
            cell: self.pool.id(("support", cell)) for cell in self.cells
        }
        self.matchings = tuple(sparse.toric.perfect_matchings(tuple(range(N))))
        self.clauses = []
        self.term_variables = {}
        self.singleton_selectors = 0

        assert len(self.cells) == 252
        assert len(self.matchings) == 105
        for cell in sorted(binary.SEED):
            self.clauses.append([self.support[cell]])

        cardinality = CardEnc.atmost(
            lits=[self.support[cell] for cell in sorted(binary.FORBIDDEN)],
            bound=3,
            top_id=self.pool.top,
            encoding=EncType.kmtotalizer,
        )
        self.pool.occupy(self.pool.top + 1, cardinality.nv)
        self.clauses.extend(cardinality.clauses)

        for colouring, trigger in SINGLETON_SCHEMAS:
            self.add_singleton_schema(colouring, trigger)
        for colouring, mixed_present, pure_present in PURE_ZERO_SCHEMAS:
            self.add_pure_zero_schema(
                colouring, mixed_present, pure_present
            )

    def terms(self, colouring):
        return tuple(
            frozenset(
                (u, v, colouring[u], colouring[v]) for u, v in matching
            )
            for matching in self.matchings
        )

    def add_singleton_schema(self, colouring, trigger_number):
        terms = self.terms(colouring)
        trigger = terms[trigger_number]
        selectors = []
        for number, term in enumerate(terms):
            if number == trigger_number:
                continue
            selector = self.pool.id(
                ("singleton_selector", colouring, trigger_number, number)
            )
            self.singleton_selectors += 1
            selectors.append(selector)
            for cell in sorted(term - trigger):
                self.clauses.append([-selector, self.support[cell]])
        self.clauses.append(
            [-self.support[cell] for cell in sorted(trigger)] + selectors
        )

    def term_indicator(self, colouring, matching_number):
        key = colouring, matching_number
        answer = self.term_variables.get(key)
        if answer is not None:
            return answer
        answer = self.pool.id(("term", colouring, matching_number))
        term = self.terms(colouring)[matching_number]
        for cell in sorted(term):
            self.clauses.append([-answer, self.support[cell]])
        self.clauses.append(
            [answer] + [-self.support[cell] for cell in sorted(term)]
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

    def add_pure_zero_schema(self, colouring, mixed_present, pure_present):
        clause = self.exact_fibre_literals(colouring, mixed_present)
        clause.extend(
            self.exact_fibre_literals((0,) * N, pure_present)
        )
        self.clauses.append(clause)


def validate_algebra(formula: CertificateFormula) -> None:
    assert len(SINGLETON_SCHEMAS) == 100
    assert len(set(SINGLETON_SCHEMAS)) == 100
    assert len(PURE_ZERO_SCHEMAS) == 10
    assert len(set(PURE_ZERO_SCHEMAS)) == 10

    # Every singleton schema concerns a mixed colouring and a genuine
    # four-cell nonzero matching monomial.  Its clause says exactly that if
    # this term is supported, at least one other matching term is supported.
    for colouring, trigger in SINGLETON_SCHEMAS:
        assert len(set(colouring)) > 1
        terms = formula.terms(colouring)
        assert 0 <= trigger < len(terms)
        assert len(terms[trigger]) == N // 2

    # Each Z-schema is independently an exact one-row Laurent certificate:
    # the mixed binomial equation makes the indicated complete pure-0
    # polynomial identically zero in the quotient group algebra.
    for colouring, mixed_present, pure_present in PURE_ZERO_SCHEMAS:
        assert len(set(colouring)) > 1
        assert len(mixed_present) == 2
        mixed_terms = formula.terms(colouring)
        row = sparse.toric.exponent_row(
            mixed_terms[mixed_present[0]],
            mixed_terms[mixed_present[1]],
            formula.cell_index,
            len(formula.cells),
        )
        consistent, lattice = sparse.toric.signed_quotient_lattice(
            [row], len(formula.cells)
        )
        assert consistent
        pure_terms = formula.terms((0,) * N)
        fibres = {
            (0,) * N: tuple(
                (number, pure_terms[number]) for number in pure_present
            )
        }
        remainder, _classes = sparse.toric.reduced_constant_product(
            N,
            fibres,
            lattice,
            formula.cells,
            formula.cell_index,
            colors=(0,),
        )
        assert not remainder


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
    # Retaining deletion lines is optional for DRAT, while omitting them keeps
    # every clause ever learned and produces a deletion-free DRUP transcript.
    additions = [line for line in proof if not line.startswith("d ")]
    assert additions and additions[-1].strip() == "0"
    proof_path.write_text("\n".join(additions) + "\n", encoding="ascii")
    print(f"wrote {cnf_path} and {proof_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", type=Path)
    args = parser.parse_args()

    formula = CertificateFormula()
    validate_algebra(formula)
    results = {}
    for solver_name in ("cadical300", "glucose42"):
        with Solver(name=solver_name, bootstrap_with=formula.clauses) as solver:
            results[solver_name] = solver.solve()
    assert results == {"cadical300": False, "glucose42": False}
    print(
        "three-binary-cell padding obstruction: PASS; "
        f"variables={formula.pool.top} clauses={len(formula.clauses)} "
        f"singleton_schemas={len(SINGLETON_SCHEMAS)} "
        f"singleton_selectors={formula.singleton_selectors} "
        f"pure_zero_schemas={len(PURE_ZERO_SCHEMAS)}"
    )
    if args.write_certificate is not None:
        write_certificate(args.write_certificate, formula)


if __name__ == "__main__":
    main()
