#!/usr/bin/env python3
"""Enumerate and analyze the all-offdiagonal even-rewrite bottom complex."""

from collections import Counter
from hashlib import sha256
from itertools import permutations
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
GRAPH_PATH = HERE / "analyze_n8_even_rewrite_state_graph.py"
SPEC = importlib.util.spec_from_file_location("n8_even_graph_for_bottom", GRAPH_PATH)
GRAPH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GRAPH)
SOURCE = GRAPH.SOURCE
PERMUTATIONS = tuple(permutations(range(3)))
IDENTITY = (0, 1, 2)
EXPECTED_LEDGER_SHA256 = (
    "7e48e2ba288d542e22053cdd36db8ea94143da96920461b293b41d406f029463"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def root_factor_edges(row):
    mate = SOURCE.decode_key(row)
    edges = []
    for first, second in SOURCE.mate_edges(mate):
        left, left_colour = divmod(first, 3)
        right, right_colour = divmod(second, 3)
        require(left_colour == right_colour,
                "pure root acquired an offdiagonal occurrence")
        edges.append((left, right, left_colour))
    require(len(edges) == 12, "pure root edge count changed")
    return tuple(edges)


def relabelled_state(edges, assignments):
    mate = [-1] * 24
    for left, right, factor in edges:
        first = 3 * left + assignments[left][factor]
        second = 3 * right + assignments[right][factor]
        require(first // 3 != second // 3, "state acquired a physical loop")
        require(mate[first] == mate[second] == -1,
                "local factor relabelling repeated a port")
        mate[first] = second
        mate[second] = first
    require(all(value >= 0 for value in mate),
            "local factor relabelling missed a port")
    return SOURCE.canonical_key(tuple(mate))


def bottom_states():
    roots = tuple(sorted(SOURCE.target_orbit_rows()))
    states = set()
    root_solution_counts = []
    for root_index, row in enumerate(roots, 1):
        edges = root_factor_edges(row)
        incident = [[] for _vertex in range(8)]
        for left, right, factor in edges:
            incident[left].append((right, factor))
            incident[right].append((left, factor))
        assignments = [None] * 8
        assignments[0] = IDENTITY
        solutions = 0

        def search(vertex):
            nonlocal solutions
            if vertex == 8:
                state = relabelled_state(edges, assignments)
                require(GRAPH.diagonal_count(state) == 0,
                        "offdiagonal constraint produced a diagonal cell")
                states.add(state)
                solutions += 1
                return
            for permutation in PERMUTATIONS:
                if all(
                    assignments[other] is None
                    or assignments[other][factor] != permutation[factor]
                    for other, factor in incident[vertex]
                ):
                    assignments[vertex] = permutation
                    search(vertex + 1)
                    assignments[vertex] = None

        search(1)
        root_solution_counts.append(solutions)
        print("root", root_index, "labelled/fixed-colour solutions", solutions,
              "bottom orbits so far", len(states), flush=True)
    return tuple(sorted(states)), tuple(root_solution_counts)


def bottom_columns(states):
    state_set = frozenset(states)
    columns = set()
    for position, row in enumerate(states, 1):
        for column, _cycles in GRAPH.even_columns(row):
            outputs = SOURCE.column_outputs(column)
            if any(GRAPH.diagonal_count(output) == 0 for output in outputs):
                columns.add(column)
        if position % 100 == 0:
            print("bottom scan", position, "/", len(states),
                  "columns", len(columns), flush=True)
    vectors = []
    missing = set()
    for column in sorted(columns):
        entries = Counter(
            output for output in SOURCE.column_outputs(column)
            if GRAPH.diagonal_count(output) == 0
        )
        missing.update(set(entries) - state_set)
        require(sum(entries.values()) in {24, 36},
                "bottom fibre size left the four word types")
        vectors.append((column, entries))
    require(not missing,
            "an even bottom fibre escaped the three-factor state census")
    return tuple(vectors)


def connected_components(states, vectors):
    adjacency = {row: set() for row in states}
    for _column, entries in vectors:
        support = tuple(entries)
        if not support:
            continue
        root = support[0]
        adjacency[root].update(support[1:])
        for other in support[1:]:
            adjacency[other].add(root)
    unseen = set(states)
    sizes = []
    while unseen:
        root = min(unseen)
        component = {root}
        frontier = [root]
        while frontier:
            row = frontier.pop()
            for other in adjacency[row]:
                if other not in component:
                    component.add(other)
                    frontier.append(other)
        unseen -= component
        sizes.append(len(component))
    return tuple(sorted(sizes, reverse=True))


def rank_mod_prime(states, vectors, prime):
    row_index = {row: index for index, row in enumerate(states)}
    basis = {}
    for _column, entries in vectors:
        value = {
            row_index[row]: coefficient % prime
            for row, coefficient in entries.items() if coefficient % prime
        }
        while value:
            pivot = min(value)
            if pivot not in basis:
                inverse = pow(value[pivot], -1, prime)
                value = {
                    row: coefficient * inverse % prime
                    for row, coefficient in value.items()
                    if coefficient * inverse % prime
                }
                basis[pivot] = value
                break
            scale = value[pivot]
            old = basis[pivot]
            for row, coefficient in old.items():
                new = (value.get(row, 0) - scale * coefficient) % prime
                if new:
                    value[row] = new
                else:
                    value.pop(row, None)
    return len(basis), tuple(sorted(basis))


def exact_rational_rank(states, vectors):
    try:
        from sympy.polys.domains import QQ
        from sympy.polys.matrices import DomainMatrix
    except ImportError as error:
        raise RuntimeError(
            "--exact-rank requires sympy in the selected interpreter"
        ) from error
    row_index = {row: index for index, row in enumerate(states)}
    entries = {}
    for column, (_column_key, values) in enumerate(vectors):
        for row, coefficient in values.items():
            entries.setdefault(row_index[row], {})[column] = QQ(coefficient)
    matrix = DomainMatrix(entries, (len(states), len(vectors)), QQ)
    return matrix.rank()


def sequence_digest(values):
    digest = sha256()
    for value in values:
        digest.update(repr(value).encode())
        digest.update(b"\n")
    return digest.hexdigest()


def incidence_digest(states, vectors):
    row_index = {row: index for index, row in enumerate(states)}
    records = (
        (column, tuple(sorted(
            (row_index[row], coefficient)
            for row, coefficient in entries.items()
        )))
        for column, entries in vectors
    )
    return sequence_digest(records)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--exact-rank", action="store_true")
    arguments = parser.parse_args()
    states, root_counts = bottom_states()
    vectors = bottom_columns(states)
    incidence_classes = Counter(
        tuple(sorted(entries.items())) for _column, entries in vectors
    )
    components = connected_components(states, vectors)
    modular_records = []
    common_pivots = None
    for prime in (1009, 1000003, 2147483647):
        rank, pivots = rank_mod_prime(states, vectors, prime)
        if common_pivots is None:
            common_pivots = pivots
        require(pivots == common_pivots,
                "modular pivot row set depends on the audit prime")
        modular_records.append({
            "prime": prime,
            "rank": rank,
            "pivot_index_sha256": sha256(repr(pivots).encode()).hexdigest(),
        })
    require(all(record["rank"] == 1090 for record in modular_records),
            "raw bottom modular rank changed")
    require(common_pivots is not None, "missing modular pivot basis")
    pivot_set = frozenset(common_pivots)
    critical_states = tuple(
        row for index, row in enumerate(states) if index not in pivot_set
    )
    ledger = {
        "physical_matching_triple_root_orbits": 31,
        "fixed_global_colour_local_assignment_solutions": sum(root_counts),
        "root_solution_histogram": dict(sorted(Counter(root_counts).items())),
        "all_offdiagonal_state_orbits": len(states),
        "state_orbit_sha256": sequence_digest(states),
        "zero_diagonal_even_fibre_column_orbits": len(vectors),
        "column_orbit_sha256": sequence_digest(
            column for column, _entries in vectors
        ),
        "incidence_sha256": incidence_digest(states, vectors),
        "distinct_incidence_columns": len(incidence_classes),
        "incidence_multiplicity_histogram": dict(sorted(Counter(
            incidence_classes.values()
        ).items())),
        "bottom_fibre_size_histogram": dict(sorted(Counter(
            sum(entries.values()) for _column, entries in vectors
        ).items())),
        "raw_plateau_support_scc_sizes": list(components),
        "modular_rank_certificates": modular_records,
        "exact_rational_and_integer_rank": 1090,
        "rational_cokernel_dimension": len(states) - 1090,
        "integer_cokernel_free_rank": len(states) - 1090,
        "integer_cokernel_torsion": "not computed",
        "critical_nonpivot_state_orbits": len(critical_states),
        "critical_nonpivot_state_orbit_sha256": sequence_digest(
            critical_states
        ),
        "generator_completeness": (
            "all 31 physical matching-triple root orbits and every local "
            "port-colour permutation are enumerated; every zero-diagonal "
            "output of every incident even fibre is asserted present"
        ),
        "scope_guard": (
            "raw zero-diagonal associated incidence only; eliminating "
            "higher diagonal fibres can add homological-perturbation path "
            "terms, so this is not the transferred Morse differential"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "all-offdiagonal bottom incidence ledger changed")
    if arguments.exact_rank:
        rank = exact_rational_rank(states, vectors)
        require(rank == ledger["exact_rational_and_integer_rank"],
                "exact rational rank changed")
        print("exact rational rank independently verified")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
