#!/usr/bin/env python3
"""Exact support search for mixed-endpoint q with one-site response rows.

The Boolean relaxation keeps all 135 endpoint-ordered coordinate cells.
For every sampled coefficient of q^[2] and every coefficient of q^[3], a
zero is allowed either no supported matching term or at least two terms;
all possible complex cancellations among two or more terms are granted.
Target coefficients need at least one supported term.

This is a support reconnaissance tool, not a proof that a returned support
has compatible nonzero complex weights.  ``--minimize`` invokes exact
MaxSAT to minimize the number of active q cells.
"""

from __future__ import annotations

import argparse
from collections import deque
from hashlib import sha256
from itertools import product
from math import gcd

import sympy as sp
from flint import fmpz_mat
from pysat.formula import WCNF
from pysat.examples.rc2 import RC2
from pysat.solvers import Solver

from verify_sparse_nonpure_coordinate_response_obstructions import (
    COLOURS,
    EDGES,
    EDGE_INDEX,
    PM4,
    PM6,
    U,
    edge,
)


ROW_GEOMETRIES = {
    "path-edge": ((0, 1), (1, 2), (3, 4)),
    "matching": ((0, 1), (2, 3), (4, 5)),
}


def cell_variable(u: int, v: int, a: int, b: int) -> int:
    if u > v:
        u, v, a, b = v, u, b, a
    return 1 + 9 * EDGE_INDEX[(u, v)] + 3 * a + b


def decode_cell(variable: int):
    assert 1 <= variable <= 135
    offset = variable - 1
    edge_index, cell_index = divmod(offset, 9)
    a, b = divmod(cell_index, 3)
    return EDGES[edge_index] + (a, b)


def active_square_terms(system, active_cells, pair, word):
    sites = tuple(u for u in U if u not in pair)
    colour = dict(zip(sites, word))
    output = []
    for matching in PM4[pair]:
        cells = tuple(
            cell_variable(u, v, colour[u], colour[v])
            for u, v in matching
        )
        if set(cells) <= active_cells:
            output.append(cells)
    return tuple(output)


def zero_binomial_exponent_rows(system, active_cells):
    """Return Laurent exponent differences for two-term zero coefficients."""
    primary = tuple(sorted(active_cells))
    location = {variable: index for index, variable in enumerate(primary)}
    rows = []
    records = []
    for pair, word, target, _indicators in system.square_records:
        if target:
            continue
        terms = active_square_terms(system, active_cells, pair, word)
        if len(terms) != 2:
            continue
        exponent = [0] * len(primary)
        for variable in terms[0]:
            exponent[location[variable]] += 1
        for variable in terms[1]:
            exponent[location[variable]] -= 1
        rows.append(tuple(exponent))
        records.append((pair, word, terms))
    return primary, tuple(rows), tuple(records)


def odd_binomial_graph_cycle(records):
    """Return an odd cycle among equations monomial_a = -monomial_b.

    Each vertex is a quadratic monomial in active q cells and each
    two-term zero coefficient is an edge.  An odd cycle is already an
    exact characteristic-not-two contradiction, and checking bipartiteness
    is much cheaper than recomputing a rational nullspace for every support.
    The returned tuple contains record indices in cyclic traversal order.
    """

    adjacency = {}
    for record_index, (_pair, _word, terms) in enumerate(records):
        left, right = (tuple(sorted(term)) for term in terms)
        adjacency.setdefault(left, []).append((right, record_index))
        adjacency.setdefault(right, []).append((left, record_index))

    colour = {}
    parent = {}
    parent_edge = {}
    depth = {}
    for root in adjacency:
        if root in colour:
            continue
        colour[root] = 0
        parent[root] = None
        depth[root] = 0
        queue = deque((root,))
        while queue:
            here = queue.popleft()
            for there, record_index in adjacency[here]:
                if there not in colour:
                    colour[there] = 1 - colour[here]
                    parent[there] = here
                    parent_edge[there] = record_index
                    depth[there] = depth[here] + 1
                    queue.append(there)
                    continue
                if colour[there] != colour[here]:
                    continue

                left = here
                right = there
                left_edges = []
                right_edges = []
                while depth[left] > depth[right]:
                    left_edges.append(parent_edge[left])
                    left = parent[left]
                while depth[right] > depth[left]:
                    right_edges.append(parent_edge[right])
                    right = parent[right]
                while left != right:
                    left_edges.append(parent_edge[left])
                    right_edges.append(parent_edge[right])
                    left = parent[left]
                    right = parent[right]
                cycle = tuple(left_edges + [record_index] + right_edges[::-1])
                assert len(cycle) % 2 == 1
                return cycle
    return None


def primitive_odd_laurent_relation(exponent_rows):
    """Find r with sum r_k*d_k=0 and odd sum r_k, if present."""
    matrix = sp.Matrix(exponent_rows).T
    for vector in matrix.nullspace():
        denominator = sp.ilcm(*(entry.q for entry in vector))
        relation = [int(entry * denominator) for entry in vector]
        divisor = 0
        for entry in relation:
            divisor = gcd(divisor, abs(entry))
        relation = tuple(entry // divisor for entry in relation)
        if sum(relation) % 2:
            assert all(
                sum(
                    relation[row] * exponent_rows[row][column]
                    for row in range(len(exponent_rows))
                ) == 0
                for column in range(len(exponent_rows[0]))
            )
            return relation
    return None


def exact_odd_laurent_relation(exponent_rows):
    """Return an odd integer relation, or certify sign consistency.

    The augmented lattice has generators (d_k, 1) and (0, 2).
    The binomial signs are inconsistent exactly when it contains (0, 1).
    FLINT's HNF transformation then supplies the coefficients of that vector
    in the original generators.
    """

    if not exponent_rows:
        return None
    number_columns = len(exponent_rows[0])
    augmented = [list(row) + [1] for row in exponent_rows]
    augmented.append([0] * number_columns + [2])
    hnf, transform = fmpz_mat(augmented).hnf(transform=True)
    for row_number in range(hnf.nrows()):
        row = tuple(
            int(hnf[row_number, column])
            for column in range(hnf.ncols())
        )
        if any(row[:-1]) or row[-1] != 1:
            continue
        relation = tuple(
            int(transform[row_number, index])
            for index in range(len(exponent_rows))
        )
        epsilon_coefficient = int(
            transform[row_number, len(exponent_rows)]
        )
        assert sum(relation) + 2 * epsilon_coefficient == 1
        assert all(
            sum(
                relation[index] * exponent_rows[index][column]
                for index in range(len(exponent_rows))
            ) == 0
            for column in range(number_columns)
        )
        assert sum(relation) % 2
        return relation
    return None


def signed_lattice_membership_certificate(
    exponent_rows, target_exponent, target_sign
):
    """Express (target_exponent, target_sign) in the signed row lattice."""

    number_columns = len(target_exponent)
    generators = [list(row) + [1] for row in exponent_rows]
    generators.append([0] * number_columns + [2])
    matrix = fmpz_mat(generators)
    hnf, transform = matrix.hnf(transform=True)

    remainder = list(target_exponent) + [target_sign]
    coefficients = [0] * len(generators)
    previous_pivot = -1
    for row_number in range(hnf.nrows()):
        row = [
            int(hnf[row_number, column])
            for column in range(hnf.ncols())
        ]
        if not any(row):
            continue
        pivot = next(column for column, value in enumerate(row) if value)
        assert pivot > previous_pivot
        assert row[pivot] > 0
        previous_pivot = pivot
        quotient, residue = divmod(remainder[pivot], row[pivot])
        if residue:
            return None
        if not quotient:
            continue
        remainder = [
            value - quotient * basis_value
            for value, basis_value in zip(remainder, row)
        ]
        for generator in range(len(generators)):
            coefficients[generator] += (
                quotient * int(transform[row_number, generator])
            )

    if any(remainder):
        return None
    reconstructed = [
        sum(
            coefficients[row] * generators[row][column]
            for row in range(len(generators))
        )
        for column in range(number_columns + 1)
    ]
    assert reconstructed == list(target_exponent) + [target_sign]
    return tuple(coefficients[:-1]), coefficients[-1]


def forced_zero_two_term_target(system, active_cells, primary, exponents):
    """Find a target binomial forced to vanish by the zero-q2 lattice."""

    location = {variable: index for index, variable in enumerate(primary)}
    for pair, word, target, _indicators in system.square_records:
        if not target:
            continue
        terms = active_square_terms(system, active_cells, pair, word)
        if len(terms) != 2:
            continue
        difference = [0] * len(primary)
        for variable in terms[0]:
            difference[location[variable]] += 1
        for variable in terms[1]:
            difference[location[variable]] -= 1
        certificate = signed_lattice_membership_certificate(
            exponents, difference, 1
        )
        if certificate is None:
            continue
        coefficients, epsilon_coefficient = certificate
        assert sum(coefficients) + 2 * epsilon_coefficient == 1
        return (pair, word, terms), coefficients, epsilon_coefficient
    return None


class SupportSystem:
    def __init__(self, rows):
        self.rows = rows
        self.clauses = []
        self.variable_count = 135
        self.monomial_auxiliary = {}
        self.sampled = {}
        self.square_records = []
        self.cube_records = []
        self._record_sampled_blocks()
        self._build_square_constraints()
        self._build_cube_constraints()

    def matching_auxiliary(self, cells):
        cells = tuple(sorted(cells))
        old = self.monomial_auxiliary.get(cells)
        if old is not None:
            return old
        self.variable_count += 1
        z = self.variable_count
        self.monomial_auxiliary[cells] = z
        for cell in cells:
            self.clauses.append((-z, cell))
        self.clauses.append((z,) + tuple(-cell for cell in cells))
        return z

    def require_zero_support(self, matching_indicators):
        # A zero polynomial cannot have exactly one nonzero monomial.  This
        # necessary condition grants arbitrary cancellation with >=2 terms.
        indicators = tuple(dict.fromkeys(matching_indicators))
        for index, z in enumerate(indicators):
            others = indicators[:index] + indicators[index + 1 :]
            self.clauses.append((-z,) + others)

    def add_sample(self, pair, word, target):
        key = pair, word
        old = self.sampled.get(key)
        if old is not None and old != target:
            self.clauses.append(())
        else:
            self.sampled[key] = target

    def _record_sampled_blocks(self):
        words4 = tuple(product(COLOURS, repeat=4))
        for i, (a, b) in enumerate(self.rows):
            diagonal_pair = edge(a, b)
            for word in words4:
                self.add_sample(diagonal_pair, word, word == (i,) * 4)

            for j in COLOURS:
                if i == j:
                    continue
                p_site = self.rows[i][0]
                s_site = self.rows[j][1]
                if p_site == s_site:
                    continue
                off_pair = edge(p_site, s_site)
                for word in words4:
                    self.add_sample(off_pair, word, False)

    def square_matching_indicators(self, pair, word):
        sites = tuple(u for u in U if u not in pair)
        colour = dict(zip(sites, word))
        output = []
        for matching in PM4[pair]:
            cells = tuple(
                cell_variable(u, v, colour[u], colour[v])
                for u, v in matching
            )
            output.append(self.matching_auxiliary(cells))
        return tuple(output)

    def _build_square_constraints(self):
        for (pair, word), target in sorted(self.sampled.items()):
            indicators = self.square_matching_indicators(pair, word)
            self.square_records.append((pair, word, target, indicators))
            if target:
                self.clauses.append(indicators)
            else:
                self.require_zero_support(indicators)

    def cube_matching_indicators(self, word):
        output = []
        for matching in PM6:
            cells = tuple(
                cell_variable(u, v, word[u], word[v])
                for u, v in matching
            )
            output.append(self.matching_auxiliary(cells))
        return tuple(output)

    def _build_cube_constraints(self):
        for word in product(COLOURS, repeat=6):
            indicators = self.cube_matching_indicators(word)
            self.cube_records.append((word, indicators))
            self.require_zero_support(indicators)

    def verify_model(self, model):
        true = set(literal for literal in model if literal > 0)
        for clause in self.clauses:
            assert any(
                (literal > 0 and literal in true)
                or (literal < 0 and -literal not in true)
                for literal in clause
            )

        # Independently count supported matching monomials from the 135
        # primary cells rather than trusting auxiliary assignments.
        active_cells = true & set(range(1, 136))
        square_histogram = {0: 0, 1: 0, 2: 0, 3: 0}
        for pair, word, target, _indicators in self.square_records:
            sites = tuple(u for u in U if u not in pair)
            colour = dict(zip(sites, word))
            count = 0
            for matching in PM4[pair]:
                cells = {
                    cell_variable(u, v, colour[u], colour[v])
                    for u, v in matching
                }
                count += cells <= active_cells
            square_histogram[count] += 1
            assert count >= 1 if target else count != 1

        cube_histogram = {count: 0 for count in range(16)}
        for word, _indicators in self.cube_records:
            count = 0
            for matching in PM6:
                cells = {
                    cell_variable(u, v, word[u], word[v])
                    for u, v in matching
                }
                count += cells <= active_cells
            cube_histogram[count] += 1
            assert count != 1
        return active_cells, square_histogram, cube_histogram


MINIMUM_AUDIT = {
    "path-edge": {
        "models": 8,
        "next_cost": 31,
        "relation_sizes": (9, 9, 9, 7, 3, 9, 7, 7),
        "relation_sums": (-1, 1, 1, -1, 1, -1, 1, 1),
        "ledger": "8f88e995a65d0d4e82543d42bb73bb96eb32cae05012ad54a9bf39b7ff8d7c52",
    },
    "matching": {
        "models": 5,
        "next_cost": 32,
        "relation_sizes": (3, 7, 3, 7, 9),
        "relation_sums": (1, 1, 1, 3, 5),
        "ledger": "c240e8e7c8c7b41ff600a3acc073fb9534a51e7992b31a252cb984b9c973e325",
    },
}

PATH_EDGE_31_AUDIT = {
    "models": 18,
    "next_cost": 32,
    "relation_sizes": (7, 3, 9, 7, 7, 7, 9, 7, 7, 9, 9, 9, 7, 3, 7, 3, 3, 7),
    "relation_sums": (1, 1, 1, 1, 1, -1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1),
    "ledger": "e677d98a4075ff648c096de7e62a16cf8dcf0de393f09d766753d8c3a8e6a6df",
}


def weighted_formula(system, learned_clauses=()):
    formula = WCNF()
    for clause in system.clauses:
        formula.append(list(clause))
    for clause in learned_clauses:
        formula.append(list(clause))
    for variable in range(1, 136):
        formula.append([-variable], weight=1)
    return formula


def third_square_matching_indicator(system, pair, word, active_terms):
    """Return the auxiliary bit for the unique inactive third matching."""

    sites = tuple(u for u in U if u not in pair)
    colour = dict(zip(sites, word))
    all_terms = tuple(
        tuple(
            cell_variable(u, v, colour[u], colour[v])
            for u, v in matching
        )
        for matching in PM4[pair]
    )
    active_keys = {tuple(sorted(term)) for term in active_terms}
    inactive = [
        term for term in all_terms
        if tuple(sorted(term)) not in active_keys
    ]
    assert len(active_keys) == 2
    assert len(inactive) == 1
    key = tuple(sorted(inactive[0]))
    return system.monomial_auxiliary[key]


def laurent_circuit_cut(system, records, relation):
    """Negate persistence of every used binomial in an odd relation."""

    literals = set()
    used = 0
    for coefficient, (pair, word, active_terms) in zip(relation, records):
        if not coefficient:
            continue
        used += 1
        for term in active_terms:
            literals.update(-variable for variable in term)
        literals.add(
            third_square_matching_indicator(
                system, pair, word, active_terms
            )
        )
    assert used
    return tuple(sorted(literals)), used


def forced_zero_target_cut(system, records, target_record, coefficients):
    """Negate persistence of a lattice certificate killing one target."""

    literals = set()
    used = 0
    for coefficient, (pair, word, active_terms) in zip(
        coefficients, records
    ):
        if not coefficient:
            continue
        used += 1
        for term in active_terms:
            literals.update(-variable for variable in term)
        literals.add(
            third_square_matching_indicator(
                system, pair, word, active_terms
            )
        )

    pair, word, active_terms = target_record
    for term in active_terms:
        literals.update(-variable for variable in term)
    literals.add(
        third_square_matching_indicator(system, pair, word, active_terms)
    )
    assert used
    return tuple(sorted(literals)), used


def run_laurent_cegar(name, system, bound, max_rounds, verbose=True):
    """Search for a support whose forced q2 binomials have consistent signs."""

    learned_clauses = []
    digest_rows = []
    for round_number in range(max_rounds):
        with RC2(
            weighted_formula(system, learned_clauses),
            solver="cadical195",
            adapt=True,
            exhaust=True,
        ) as solver:
            model = solver.compute()
            assert model is not None
            cost = solver.cost

        active, _square_histogram, _cube_histogram = system.verify_model(model)
        assert len(active) == cost
        if cost > bound:
            ledger = sha256("\n".join(digest_rows).encode("ascii")).hexdigest()
            return {
                "status": "obstructed-through-bound",
                "rounds": round_number,
                "cost": cost,
                "active": (),
                "ledger": ledger,
            }
        primary, exponents, records = zero_binomial_exponent_rows(
            system, active
        )
        relation = exact_odd_laurent_relation(exponents)
        if relation is None:
            target_obstruction = forced_zero_two_term_target(
                system, active, primary, exponents
            )
            if target_obstruction is None:
                ledger = sha256(
                    "\n".join(digest_rows).encode("ascii")
                ).hexdigest()
                return {
                    "status": "phase-and-target-compatible",
                    "rounds": round_number,
                    "cost": cost,
                    "active": tuple(sorted(active)),
                    "ledger": ledger,
                }
            target_record, coefficients, epsilon_coefficient = (
                target_obstruction
            )
            cut, used = forced_zero_target_cut(
                system, records, target_record, coefficients
            )
            obstruction_kind = "target-zero"
            certificate = coefficients
            certificate_suffix = (
                f"|{target_record[0]}|{target_record[1]}"
                f"|epsilon={epsilon_coefficient}"
            )
        else:
            cut, used = laurent_circuit_cut(system, records, relation)
            obstruction_kind = "odd"
            certificate = relation
            certificate_suffix = ""
        true = set(literal for literal in model if literal > 0)
        assert not any(
            (literal > 0 and literal in true)
            or (literal < 0 and -literal not in true)
            for literal in cut
        )
        learned_clauses.append(cut)
        if obstruction_kind == "odd":
            # Preserve the frozen through-32 ledger format.
            payload = (
                f"{round_number}|{cost}|"
                + ",".join(str(variable) for variable in primary)
                + "|"
                + ",".join(str(entry) for entry in certificate)
                + "|"
                + ",".join(str(literal) for literal in cut)
            )
        else:
            payload = (
                f"{round_number}|{cost}|"
                + ",".join(str(variable) for variable in primary)
                + "|"
                + obstruction_kind
                + "|"
                + ",".join(str(entry) for entry in certificate)
                + certificate_suffix
                + "|"
                + ",".join(str(literal) for literal in cut)
            )
        digest_rows.append(sha256(payload.encode("ascii")).hexdigest())
        if verbose:
            print(
                "cegar_round", round_number, "cost", cost,
                "kind", obstruction_kind,
                "binomials", len(records), "certificate_support", used,
                "cut_literals", len(cut),
                flush=True,
            )
    raise RuntimeError(
        f"{name}: reached max_rounds={max_rounds} at bound={bound}"
    )


def audit_minimum_layer(name, system):
    """Enumerate every minimum support and kill it by an odd Laurent circuit."""
    expected = MINIMUM_AUDIT[name]
    relation_sizes = []
    relation_sums = []
    digests = []
    model_count = 0
    next_cost = None
    with RC2(
        weighted_formula(system), solver="cadical195", adapt=True, exhaust=True
    ) as solver:
        for model in solver.enumerate():
            if solver.cost > 30:
                next_cost = solver.cost
                break
            assert solver.cost == 30
            model_count += 1
            active, _square_histogram, _cube_histogram = system.verify_model(model)
            assert len(active) == 30
            primary, exponents, _records = zero_binomial_exponent_rows(
                system, active
            )
            relation = primitive_odd_laurent_relation(exponents)
            assert relation is not None
            relation_sizes.append(sum(entry != 0 for entry in relation))
            relation_sums.append(sum(relation))
            payload = (
                ",".join(str(variable) for variable in primary)
                + "|"
                + ",".join(str(entry) for entry in relation)
            )
            digests.append(sha256(payload.encode("ascii")).hexdigest())

    ledger = sha256("\n".join(digests).encode("ascii")).hexdigest()
    assert model_count == expected["models"]
    assert next_cost == expected["next_cost"]
    assert tuple(relation_sizes) == expected["relation_sizes"]
    assert tuple(relation_sums) == expected["relation_sums"]
    assert ledger == expected["ledger"]
    return model_count, next_cost, tuple(relation_sizes), tuple(relation_sums), ledger


def audit_path_edge_31_layer(system):
    """Enumerate and exclude all 31-cell supports in the path-edge orbit."""
    expected = PATH_EDGE_31_AUDIT
    relation_sizes = []
    relation_sums = []
    digests = []
    model_count = 0
    next_cost = None
    with RC2(
        weighted_formula(system), solver="cadical195", adapt=True, exhaust=True
    ) as solver:
        for model in solver.enumerate():
            if solver.cost < 31:
                continue
            if solver.cost > 31:
                next_cost = solver.cost
                break
            model_count += 1
            active, _square_histogram, _cube_histogram = system.verify_model(model)
            assert len(active) == 31
            primary, exponents, _records = zero_binomial_exponent_rows(
                system, active
            )
            relation = primitive_odd_laurent_relation(exponents)
            assert relation is not None
            relation_sizes.append(sum(entry != 0 for entry in relation))
            relation_sums.append(sum(relation))
            payload = (
                ",".join(str(variable) for variable in primary)
                + "|"
                + ",".join(str(entry) for entry in relation)
            )
            digests.append(sha256(payload.encode("ascii")).hexdigest())

    ledger = sha256("\n".join(digests).encode("ascii")).hexdigest()
    assert model_count == expected["models"]
    assert next_cost == expected["next_cost"]
    assert tuple(relation_sizes) == expected["relation_sizes"]
    assert tuple(relation_sums) == expected["relation_sums"]
    assert ledger == expected["ledger"]
    return model_count, next_cost, tuple(relation_sizes), tuple(relation_sums), ledger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--geometry", choices=ROW_GEOMETRIES, default="path-edge")
    parser.add_argument("--minimize", action="store_true")
    parser.add_argument("--audit-minimum", action="store_true")
    parser.add_argument("--scan-cost", type=int)
    parser.add_argument("--scan-limit", type=int, default=0)
    parser.add_argument("--laurent-cegar", action="store_true")
    parser.add_argument("--cegar-bound", type=int, default=32)
    parser.add_argument("--cegar-rounds", type=int, default=1000)
    args = parser.parse_args()

    rows = ROW_GEOMETRIES[args.geometry]
    system = SupportSystem(rows)
    print(
        "geometry", args.geometry, "rows", rows,
        "variables", system.variable_count,
        "clauses", len(system.clauses),
        flush=True,
    )

    if args.laurent_cegar:
        result = run_laurent_cegar(
            args.geometry, system, args.cegar_bound, args.cegar_rounds
        )
        print("laurent_cegar_result", result)
        if result["active"]:
            print(
                "active_cells",
                tuple(decode_cell(variable) for variable in result["active"]),
            )
        return

    if args.audit_minimum:
        result = audit_minimum_layer(args.geometry, system)
        print("minimum_layer_audit", result)
        print("all minimum supports have an odd Laurent circuit: PASS")
        if args.geometry == "path-edge":
            path_result = audit_path_edge_31_layer(system)
            print("path_edge_31_layer_audit", path_result)
            print("all 31-cell path-edge supports have an odd Laurent circuit: PASS")
        else:
            assert result[1] == 32
            print("matching support relaxation has no 31-cell model: PASS")
        print("every exact mixed-endpoint one-site solution needs >=32 cells")
        return

    if args.scan_cost is not None:
        tested = 0
        without_odd_graph_cycle = 0
        without_displayed_relation = 0
        with RC2(
            weighted_formula(system),
            solver="cadical195",
            adapt=True,
            exhaust=True,
        ) as solver:
            for model in solver.enumerate():
                if solver.cost < args.scan_cost:
                    continue
                if solver.cost > args.scan_cost:
                    print("next_cost", solver.cost)
                    break
                tested += 1
                active = {literal for literal in model if 0 < literal <= 135}
                _primary, exponents, records = zero_binomial_exponent_rows(
                    system, active
                )
                cycle = odd_binomial_graph_cycle(records)
                if cycle is not None:
                    continue
                without_odd_graph_cycle += 1
                relation = primitive_odd_laurent_relation(exponents)
                if relation is None:
                    without_displayed_relation += 1
                    print(
                        "no_displayed_odd_relation", tested,
                        tuple(decode_cell(variable) for variable in sorted(active)),
                    )
                if args.scan_limit and tested >= args.scan_limit:
                    break
        print(
            "scan_summary", "cost", args.scan_cost, "tested", tested,
            "without_odd_graph_cycle", without_odd_graph_cycle,
            "without_displayed_relation", without_displayed_relation,
        )
        return

    if args.minimize:
        with RC2(
            weighted_formula(system),
            solver="cadical195",
            adapt=True,
            exhaust=True,
        ) as solver:
            model = solver.compute()
            assert model is not None
            print("minimum_active_cells", solver.cost)
    else:
        with Solver(name="cadical195", bootstrap_with=system.clauses) as solver:
            assert solver.solve()
            model = solver.get_model()

    active, square_histogram, cube_histogram = system.verify_model(model)
    cells = tuple(decode_cell(variable) for variable in sorted(active))
    print("active_cells", len(cells), cells)
    print("sampled_q2_term_histogram", square_histogram)
    print(
        "q3_term_histogram",
        {count: frequency for count, frequency in cube_histogram.items() if frequency},
    )
    print("mixed-endpoint one-site support relaxation: SAT")


if __name__ == "__main__":
    main()
