#!/usr/bin/env python3
"""Clean-room audit of the mixed-endpoint one-site Laurent lower bound.

This file deliberately does not import either of the primary mixed-endpoint
search/checker modules.  It reconstructs from the coefficient definitions:

* the 17 directed one-site response-row orbits and the two block-compatible
  representatives;
* the necessary Boolean support formula for all sampled coefficients of
  q^[2] and all coefficients of q^[3];
* the exact sign-lattice obstruction for forced quadratic binomials; and
* cancellation-aware CEGAR clauses, followed by independent cardinality-SAT
  checks of the final support lower bounds.

The only external engines used are PySAT for Boolean solving and python-flint
for integer Hermite normal form.  All coefficient and clause generation is
implemented locally below.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from itertools import combinations, product
from typing import Iterable, Sequence

from flint import fmpz_mat
from pysat.card import CardEnc, EncType
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
from pysat.solvers import Solver
from sympy import Matrix


SITES = tuple(range(6))
COLOURS = tuple(range(3))
ROW_GEOMETRIES = {
    "path-edge": ((0, 1), (1, 2), (3, 4)),
    "matching": ((0, 1), (2, 3), (4, 5)),
}


def perfect_matchings(vertices: Sequence[int]) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Return all unordered perfect matchings, deterministically."""

    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    answer: list[tuple[tuple[int, int], ...]] = []
    for pos in range(1, len(vertices)):
        mate = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((first, mate),) + tail)
    return tuple(answer)


PM4 = {s: perfect_matchings(s) for s in combinations(SITES, 4)}
PM6 = perfect_matchings(SITES)
assert all(len(matchings) == 3 for matchings in PM4.values())
assert len(PM6) == 15


Row = tuple[tuple[int, int], tuple[int, int], tuple[int, int]]


def row_orbits() -> list[set[Row]]:
    """Generate response-row orbits by a small generating set of symmetries."""

    directed_edges = tuple((u, v) for u in SITES for v in SITES if u != v)
    unseen: set[Row] = set(product(directed_edges, repeat=3))

    site_generators: list[tuple[int, ...]] = []
    for k in range(5):
        permutation = list(SITES)
        permutation[k], permutation[k + 1] = permutation[k + 1], permutation[k]
        site_generators.append(tuple(permutation))

    def neighbours(row: Row) -> Iterable[Row]:
        for permutation in site_generators:
            yield tuple((permutation[u], permutation[v]) for u, v in row)  # type: ignore[return-value]
        for k in (0, 1):
            swapped = list(row)
            swapped[k], swapped[k + 1] = swapped[k + 1], swapped[k]
            yield tuple(swapped)  # type: ignore[return-value]
        yield tuple((v, u) for u, v in row)  # type: ignore[return-value]

    orbits: list[set[Row]] = []
    while unseen:
        seed = min(unseen)
        orbit = {seed}
        stack = [seed]
        while stack:
            row = stack.pop()
            for image in neighbours(row):
                if image not in orbit:
                    orbit.add(image)
                    stack.append(image)
        unseen.difference_update(orbit)
        orbits.append(orbit)
    return orbits


def directly_block_compatible(row: Row) -> bool:
    """Test whether diagonal target blocks clash with any forced-zero block."""

    diagonal_pairs = [frozenset(edge) for edge in row]
    # Distinct colours cannot prescribe two different pure tensors on one block.
    if len(set(diagonal_pairs)) != 3:
        return False
    # The (i,j) off-diagonal response samples U\{a_i,b_j}, unless both
    # response rows lie at the same site.  It cannot be one of the three
    # diagonal blocks, which is required to be nonzero.
    for i, (a_i, _) in enumerate(row):
        for j, (_, b_j) in enumerate(row):
            if i != j and a_i != b_j:
                if frozenset((a_i, b_j)) in diagonal_pairs:
                    return False
    return True


@dataclass(frozen=True)
class QuadraticCoefficient:
    sites: tuple[int, ...]
    word: tuple[int, ...]
    monomials: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]


class SupportSystem:
    """Exact Boolean encoding of the necessary support consequences."""

    def __init__(self, row: Row):
        self.row = row
        self.next_var = 1
        self.cell_by_key: dict[tuple[int, int, int, int], int] = {}
        self.cell_key_by_var: dict[int, tuple[int, int, int, int]] = {}
        for u in SITES:
            for v in SITES:
                if u >= v:
                    continue
                for a in COLOURS:
                    for b in COLOURS:
                        variable = self._fresh_var()
                        key = (u, a, v, b)
                        self.cell_by_key[key] = variable
                        self.cell_key_by_var[variable] = key
        self.cell_vars = tuple(sorted(self.cell_key_by_var))
        assert self.cell_vars == tuple(range(1, 136))

        self.term_var_by_monomial: dict[tuple[int, ...], int] = {}
        self.monomial_by_term_var: dict[int, tuple[int, ...]] = {}
        self._clauses: set[tuple[int, ...]] = set()
        self.zero_quadratics: list[QuadraticCoefficient] = []

        requirements = self._quadratic_requirements()
        for key in sorted(requirements):
            sites, word = key
            monomials = self._quadratic_monomials(sites, word)
            term_vars = tuple(self._term_var(monomial) for monomial in monomials)
            if requirements[key] == "nonzero":
                self._add_clause(term_vars)
            else:
                for k, term_var in enumerate(term_vars):
                    self._add_clause((-term_var,) + term_vars[:k] + term_vars[k + 1 :])
                self.zero_quadratics.append(
                    QuadraticCoefficient(sites, word, monomials)  # type: ignore[arg-type]
                )

        # q^[3]=0: for each six-site coordinate word, its fifteen matching
        # monomials may not have support cardinality exactly one.
        for word in product(COLOURS, repeat=6):
            monomials = self._cubic_monomials(word)
            term_vars = tuple(self._term_var(monomial) for monomial in monomials)
            for k, term_var in enumerate(term_vars):
                self._add_clause((-term_var,) + term_vars[:k] + term_vars[k + 1 :])

        self.base_clauses = tuple(sorted(self._clauses))
        self.nvars = self.next_var - 1

    def _fresh_var(self) -> int:
        variable = self.next_var
        self.next_var += 1
        return variable

    def _cell(self, u: int, a: int, v: int, b: int) -> int:
        if u < v:
            return self.cell_by_key[(u, a, v, b)]
        return self.cell_by_key[(v, b, u, a)]

    def _term_var(self, monomial: tuple[int, ...]) -> int:
        monomial = tuple(sorted(monomial))
        if monomial not in self.term_var_by_monomial:
            variable = self._fresh_var()
            self.term_var_by_monomial[monomial] = variable
            self.monomial_by_term_var[variable] = monomial
            # t <=> conjunction(monomial).
            for cell in monomial:
                self._add_clause((-variable, cell))
            self._add_clause((variable,) + tuple(-cell for cell in monomial))
        return self.term_var_by_monomial[monomial]

    def _add_clause(self, literals: Iterable[int]) -> None:
        literal_set = set(literals)
        if any(-literal in literal_set for literal in literal_set):
            return
        if not literal_set:
            raise AssertionError("empty hard clause")
        self._clauses.add(tuple(sorted(literal_set, key=lambda value: (abs(value), value < 0))))

    def _quadratic_requirements(
        self,
    ) -> dict[tuple[tuple[int, ...], tuple[int, ...]], str]:
        requirements: dict[tuple[tuple[int, ...], tuple[int, ...]], str] = {}

        def insert(
            sites: tuple[int, ...], word: tuple[int, ...], requirement: str
        ) -> None:
            key = (sites, word)
            old = requirements.get(key)
            if old is not None and old != requirement:
                raise AssertionError(f"direct target/zero block conflict at {key}")
            requirements[key] = requirement

        # Diagonal response (i,i): exactly the all-i coefficient is nonzero.
        for colour, (a_i, b_i) in enumerate(self.row):
            sites = tuple(u for u in SITES if u not in (a_i, b_i))
            assert len(sites) == 4
            target = (colour,) * 4
            for word in product(COLOURS, repeat=4):
                insert(sites, word, "nonzero" if word == target else "zero")

        # Off-diagonal response (i,j): if the two rows occupy different sites,
        # the entire sampled four-site tensor block is zero.
        for i, (a_i, _) in enumerate(self.row):
            for j, (_, b_j) in enumerate(self.row):
                if i == j or a_i == b_j:
                    continue
                sites = tuple(u for u in SITES if u not in (a_i, b_j))
                assert len(sites) == 4
                for word in product(COLOURS, repeat=4):
                    insert(sites, word, "zero")
        return requirements

    def _quadratic_monomials(
        self, sites: tuple[int, ...], word: tuple[int, ...]
    ) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:
        colour = dict(zip(sites, word, strict=True))
        monomials = []
        for matching in PM4[sites]:
            cells = tuple(
                sorted(self._cell(u, colour[u], v, colour[v]) for u, v in matching)
            )
            monomials.append(cells)
        return tuple(sorted(monomials))  # type: ignore[return-value]

    def _cubic_monomials(self, word: tuple[int, ...]) -> tuple[tuple[int, int, int], ...]:
        monomials = []
        for matching in PM6:
            cells = tuple(sorted(self._cell(u, word[u], v, word[v]) for u, v in matching))
            monomials.append(cells)
        return tuple(sorted(monomials))

    def term_var(self, monomial: tuple[int, ...]) -> int:
        return self.term_var_by_monomial[tuple(sorted(monomial))]

    def active_cells(self, model: Sequence[int]) -> frozenset[int]:
        positive = {literal for literal in model if literal > 0}
        active = frozenset(variable for variable in self.cell_vars if variable in positive)
        # Audit every conjunction indicator against the projected support.
        for monomial, variable in self.term_var_by_monomial.items():
            assert (variable in positive) == all(cell in active for cell in monomial)
        return active

    def forced_binomials(
        self, support: frozenset[int]
    ) -> list[tuple[QuadraticCoefficient, tuple[tuple[int, int], tuple[int, int]], tuple[int, int]]]:
        answer = []
        for coefficient in self.zero_quadratics:
            active = tuple(
                monomial
                for monomial in coefficient.monomials
                if all(cell in support for cell in monomial)
            )
            if len(active) == 2:
                inactive = next(
                    monomial for monomial in coefficient.monomials if monomial not in active
                )
                answer.append((coefficient, active, inactive))  # type: ignore[arg-type]
        return answer


@dataclass(frozen=True)
class OddRelation:
    coefficients: tuple[int, ...]
    parity_coefficient: int


def odd_sign_relation(
    binomials: Sequence[
        tuple[QuadraticCoefficient, tuple[tuple[int, int], tuple[int, int]], tuple[int, int]]
    ],
    support: frozenset[int],
) -> OddRelation | None:
    """Use exact row HNF to test whether (0,1) lies in the sign lattice."""

    columns = tuple(sorted(support))
    column_index = {cell: position for position, cell in enumerate(columns)}
    generators: list[list[int]] = []
    for _, active_terms, _ in binomials:
        row = [0] * (len(columns) + 1)
        for cell in active_terms[0]:
            row[column_index[cell]] += 1
        for cell in active_terms[1]:
            row[column_index[cell]] -= 1
        row[-1] = 1
        generators.append(row)
    generators.append([0] * len(columns) + [2])

    matrix = fmpz_mat(generators)
    hnf, transform = matrix.hnf(transform=True)
    row_count, column_count = hnf.nrows(), hnf.ncols()
    rank = 0
    while rank < row_count and any(hnf[rank, j] != 0 for j in range(column_count)):
        rank += 1
    assert all(
        all(hnf[i, j] == 0 for j in range(column_count))
        for i in range(rank, row_count)
    )
    basis = Matrix(
        [[int(hnf[i, j]) for j in range(column_count)] for i in range(rank)]
    )
    pivots = [next(j for j in range(column_count) if basis[i, j] != 0) for i in range(rank)]
    assert len(set(pivots)) == rank
    target = [0] * (column_count - 1) + [1]

    # Solve y*H=target from the pivot columns.  Integral y and an exact full
    # equality are equivalent to membership in the row lattice generated by H.
    pivot_matrix = basis[:, pivots]
    target_pivots = Matrix([target[j] for j in pivots])
    y = pivot_matrix.T.inv() * target_pivots
    if any(value.q != 1 for value in y):
        return None
    y_int = [int(value) for value in y]
    if list((Matrix([y_int]) * basis).tolist()[0]) != target:
        return None

    padded_y = y_int + [0] * (row_count - rank)
    coefficients = tuple(
        sum(padded_y[i] * int(transform[i, j]) for i in range(row_count))
        for j in range(row_count)
    )
    reconstructed = [
        sum(coefficients[i] * int(matrix[i, j]) for i in range(row_count))
        for j in range(column_count)
    ]
    assert reconstructed == target
    relation = OddRelation(coefficients[:-1], coefficients[-1])
    assert sum(relation.coefficients) + 2 * relation.parity_coefficient == 1
    return relation


def wcnf_for(system: SupportSystem, extra_clauses: Sequence[tuple[int, ...]]) -> WCNF:
    formula = WCNF()
    for clause in system.base_clauses:
        formula.append(list(clause))
    for clause in extra_clauses:
        formula.append(list(clause))
    for cell in system.cell_vars:
        formula.append([-cell], weight=1)
    return formula


def minimum_model(
    system: SupportSystem, extra_clauses: Sequence[tuple[int, ...]]
) -> tuple[int, list[int], frozenset[int]]:
    formula = wcnf_for(system, extra_clauses)
    with RC2(formula, solver="cadical195", adapt=False, exhaust=False, verbose=0) as rc2:
        model = rc2.compute()
        assert model is not None
    support = system.active_cells(model)
    return len(support), model, support


def exact_cost_supports(system: SupportSystem, cost: int) -> list[frozenset[int]]:
    """Enumerate projected cell supports at one exact cardinality."""

    cardinality = CardEnc.equals(
        lits=list(system.cell_vars),
        bound=cost,
        top_id=system.nvars,
        encoding=EncType.seqcounter,
    )
    clauses = [list(clause) for clause in system.base_clauses]
    clauses.extend(cardinality.clauses)
    supports: list[frozenset[int]] = []
    with Solver(name="cadical195", bootstrap_with=clauses) as solver:
        while solver.solve():
            model = solver.get_model()
            support = system.active_cells(model)
            assert len(support) == cost
            supports.append(support)
            # Exact cardinality makes this clause block precisely this projected
            # support, independent of auxiliary-variable assignments.
            solver.add_clause([-cell for cell in sorted(support)])
    return sorted(supports, key=lambda support: tuple(sorted(support)))


def independent_atmost_check(
    system: SupportSystem, extra_clauses: Sequence[tuple[int, ...]], bound: int
) -> bool:
    """Return satisfiability at the bound using a second SAT engine."""

    top_id = max(
        [system.nvars]
        + [abs(literal) for clause in extra_clauses for literal in clause]
    )
    cardinality = CardEnc.atmost(
        lits=list(system.cell_vars),
        bound=bound,
        top_id=top_id,
        encoding=EncType.totalizer,
    )
    clauses = [list(clause) for clause in system.base_clauses]
    clauses.extend([list(clause) for clause in extra_clauses])
    clauses.extend(cardinality.clauses)
    with Solver(name="glucose4", bootstrap_with=clauses) as solver:
        return solver.solve()


def cegar_cut(
    system: SupportSystem,
    binomials: Sequence[
        tuple[QuadraticCoefficient, tuple[tuple[int, int], tuple[int, int]], tuple[int, int]]
    ],
    relation: OddRelation,
    support: frozenset[int],
) -> tuple[int, ...]:
    literals: set[int] = set()
    for coefficient, active_terms, inactive_term in (
        binomial
        for coefficient_index, binomial in enumerate(binomials)
        if relation.coefficients[coefficient_index] != 0
    ):
        del coefficient
        for monomial in active_terms:
            assert all(cell in support for cell in monomial)
            literals.update(-cell for cell in monomial)
        assert not all(cell in support for cell in inactive_term)
        literals.add(system.term_var(inactive_term))
    clause = tuple(sorted(literals, key=lambda value: (abs(value), value < 0)))
    assert clause
    # The current support must falsify the learned clause.
    for literal in clause:
        if literal < 0:
            assert -literal in support
        else:
            assert not all(
                cell in support for cell in system.monomial_by_term_var[literal]
            )
    return clause


def run_cegar(
    geometry: str, system: SupportSystem, target_minimum: int
) -> tuple[list[tuple[int, tuple[int, ...], OddRelation]], list[tuple[int, ...]]]:
    learned: list[tuple[int, ...]] = []
    ledger: list[tuple[int, tuple[int, ...], OddRelation]] = []
    while True:
        cost, _, support = minimum_model(system, learned)
        if cost >= target_minimum:
            assert cost == target_minimum
            break
        binomials = system.forced_binomials(support)
        relation = odd_sign_relation(binomials, support)
        if relation is None:
            raise AssertionError(
                f"{geometry} has Laurent-consistent support of cost {cost}: "
                f"{tuple(sorted(support))}"
            )
        cut = cegar_cut(system, binomials, relation, support)
        assert cut not in learned
        learned.append(cut)
        ledger.append((cost, tuple(sorted(support)), relation))

    assert not independent_atmost_check(system, learned, target_minimum - 1)
    return ledger, learned


def digest_ledger(
    ledger: Sequence[tuple[int, tuple[int, ...], OddRelation]]
) -> str:
    payload = "\n".join(
        f"{round_index}|{cost}|{support}|{relation.coefficients}|{relation.parity_coefficient}"
        for round_index, (cost, support, relation) in enumerate(ledger)
    )
    return sha256(payload.encode()).hexdigest()


def main() -> None:
    orbits = row_orbits()
    sizes = sorted(len(orbit) for orbit in orbits)
    assert len(orbits) == 17
    assert sizes == sorted(
        (30, 720, 90, 720, 1080, 720, 1440, 720, 4320,
         2160, 2160, 4320, 1080, 240, 2160, 4320, 720)
    )
    compatibility_by_orbit = [
        {directly_block_compatible(row) for row in orbit} for orbit in orbits
    ]
    assert all(len(values) == 1 for values in compatibility_by_orbit)
    survivors = [
        orbit
        for orbit, values in zip(orbits, compatibility_by_orbit, strict=True)
        if True in values
    ]
    assert len(survivors) == 2
    assert all(any(rep in orbit for orbit in survivors) for rep in ROW_GEOMETRIES.values())
    assert sorted(len(orbit) for orbit in survivors) == [720, 4320]
    print("row-orbit audit: 17 / 27000; direct-block survivors = 2")

    systems = {name: SupportSystem(row) for name, row in ROW_GEOMETRIES.items()}
    for name, system in systems.items():
        base_minimum, _, _ = minimum_model(system, ())
        assert base_minimum == 30
        print(
            f"{name} formula: {system.nvars} variables, "
            f"{len(system.base_clauses)} hard clauses, base minimum {base_minimum}"
        )

    # Independently reproduce every projected support in the layers used by
    # the support-frontier theorem and audit an explicit odd HNF relation.
    layer_expectations = {
        ("path-edge", 30): 8,
        ("path-edge", 31): 18,
        ("matching", 30): 5,
        ("matching", 31): 0,
    }
    for (name, cost), expected_count in layer_expectations.items():
        supports = exact_cost_supports(systems[name], cost)
        assert len(supports) == expected_count
        for support in supports:
            binomials = systems[name].forced_binomials(support)
            relation = odd_sign_relation(binomials, support)
            assert relation is not None
        print(f"{name} exact support layer {cost}: {len(supports)} (all HNF-audited)")

    path_ledger, path_cuts = run_cegar("path-edge", systems["path-edge"], 33)
    matching_ledger, matching_cuts = run_cegar("matching", systems["matching"], 34)

    path_costs = [cost for cost, _, _ in path_ledger]
    matching_costs = [cost for cost, _, _ in matching_ledger]
    assert max(path_costs) == 32 and max(matching_costs) == 32
    print(
        "path-edge CEGAR:",
        {cost: path_costs.count(cost) for cost in sorted(set(path_costs))},
        "next minimum 33",
        "independent ledger",
        digest_ledger(path_ledger),
    )
    print(
        "matching CEGAR:",
        {cost: matching_costs.count(cost) for cost in sorted(set(matching_costs))},
        "next minimum 34",
        "independent ledger",
        digest_ledger(matching_ledger),
    )
    print(
        f"learned clauses: path-edge {len(path_cuts)}, matching {len(matching_cuts)}"
    )
    print("mixed-endpoint one-site Laurent closure independent audit: PASS")


if __name__ == "__main__":
    main()
