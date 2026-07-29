#!/usr/bin/env python3
"""Exclude equality in the exact 180-cell orbit-40 fractional cover."""

from itertools import combinations, product

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

import verify_n8_structural_cell_ceiling as ceiling


def audit_extremal_graph_forms():
    """Audit the two elementary equality classifications used below."""

    edges = tuple(combinations(range(ceiling.N), 2))
    edge_index = {edge: index for index, edge in enumerate(edges)}
    matching_masks = tuple(
        sum(1 << edge_index[edge] for edge in matching)
        for matching in ceiling.perfect_matchings(range(ceiling.N))
    )
    assert len(matching_masks) == 105

    # A 21-edge graph without a perfect matching has a seven-edge complement
    # meeting all 105 perfect matchings.  Exhaust all C(28,7) complements:
    # the only eight minimum blockers are the vertex stars, so the graph is
    # exactly K7 plus the corresponding isolated vertex.
    blockers = []
    for missing_indices in combinations(range(len(edges)), 7):
        missing = sum(1 << index for index in missing_indices)
        if all(missing & matching for matching in matching_masks):
            blockers.append(missing)
    stars = {
        sum(
            1 << edge_index[tuple(sorted((vertex, other)))]
            for other in range(ceiling.N) if other != vertex
        )
        for vertex in range(ceiling.N)
    }
    assert set(blockers) == stars

    # Relative to a fixed perfect matching, the other edges split into six
    # K2,2 blocks.  A block without an alternating flip has <=2 edges; a
    # block with at most one flip has <=3.  Hence a graph with that fixed
    # matching and at most one alternative has <=4 + 5*2 + 3 = 17 edges.
    block_edges = ((0, 2), (0, 3), (1, 2), (1, 3))
    block_pairings = (
        frozenset(((0, 2), (1, 3))),
        frozenset(((0, 3), (1, 2))),
    )
    profiles = []
    for bits in product((0, 1), repeat=4):
        selected = frozenset(
            edge for edge, bit in zip(block_edges, bits) if bit
        )
        profiles.append((
            len(selected),
            sum(pairing <= selected for pairing in block_pairings),
        ))
    assert max(size for size, flips in profiles if flips == 0) == 2
    assert max(size for size, flips in profiles if flips <= 1) == 3


def dual_colorings():
    automorphisms = ceiling.target_automorphisms()
    weights = {}
    for representative, expected_size, weight in ceiling.DUAL_ORBITS:
        orbit = {
            ceiling.image_coloring(representative, automorphism)
            for automorphism in automorphisms
        }
        assert len(orbit) == expected_size
        assert not orbit.intersection(weights)
        weights.update({coloring: weight for coloring in orbit})
    assert len(weights) == 60
    return weights


def build_equality_cnf():
    """Build the necessary local forms of a hypothetical 180-cell support."""

    n = ceiling.N
    q = ceiling.Q
    edges = tuple(combinations(range(n), 2))
    cells = tuple(
        (u, v, a, b)
        for u, v in edges
        for a, b in product(range(q), repeat=2)
    )
    cell_variable = {
        cell: index + 1 for index, cell in enumerate(cells)
    }
    top = len(cells)
    clauses = []

    def new_variable():
        nonlocal top
        top += 1
        return top

    def add_equals(literals, bound):
        nonlocal top
        cardinality = CardEnc.equals(
            lits=list(literals),
            bound=bound,
            top_id=top,
            encoding=EncType.seqcounter,
        )
        top = cardinality.nv
        clauses.extend(map(list, cardinality.clauses))

    weights = dual_colorings()
    ordinary = [
        coloring for coloring in weights
        if ceiling.local_edge_ceiling(coloring) == 21
    ]
    special = [
        coloring for coloring in weights
        if ceiling.local_edge_ceiling(coloring) == 17
    ]
    assert len(ordinary) == 54
    assert len(special) == 6

    # Equality in the weighted 180 bound forces all 54 ordinary local
    # inequalities to have 21 edges.  Such a graph cannot have a perfect
    # matching (a graph containing one and having <=2 total has <=17 edges),
    # and the equality case of the K8 matching blocker bound is K7 plus one
    # isolated vertex.  Encode the choice of that isolated vertex and its
    # exact edge pattern.
    for coloring in ordinary:
        isolated = [new_variable() for _vertex in range(n)]
        clauses.append(isolated)
        for left, right in combinations(isolated, 2):
            clauses.append([-left, -right])
        for vertex, choice in enumerate(isolated):
            for u, v in edges:
                cell = cell_variable[u, v, coloring[u], coloring[v]]
                clauses.append([
                    -choice,
                    -cell if vertex in (u, v) else cell,
                ])

    # Each of the six special colorings already contains a forced perfect
    # matching.  Equality forces 17 edges, while the exact 0/2 condition
    # forces exactly two perfect matching terms.  Encode both statements
    # directly, with every term equivalent to its four edge bits.
    matchings = tuple(ceiling.perfect_matchings(range(n)))
    assert len(matchings) == 105
    for coloring in special:
        graph_edges = [
            cell_variable[u, v, coloring[u], coloring[v]]
            for u, v in edges
        ]
        add_equals(graph_edges, 17)
        terms = []
        for matching in matchings:
            term = new_variable()
            terms.append(term)
            matching_edges = [
                cell_variable[u, v, coloring[u], coloring[v]]
                for u, v in matching
            ]
            clauses.extend([-term, edge] for edge in matching_edges)
            clauses.append([-edge for edge in matching_edges] + [term])
        add_equals(terms, 2)

    for color, target in enumerate(ceiling.TARGETS):
        for u, v in target:
            clauses.append([cell_variable[u, v, color, color]])

    assert top == 6030
    return top, tuple(tuple(clause) for clause in clauses)


def main():
    audit_extremal_graph_forms()
    variables, clauses = build_equality_cnf()
    results = {}
    for solver_name in ("cadical195", "glucose42"):
        solver = Solver(name=solver_name, bootstrap_with=clauses)
        results[solver_name] = solver.solve()
        solver.delete()
    assert results == {"cadical195": False, "glucose42": False}
    print(
        "PASS 180-cell equality CNF: "
        f"{variables} variables, {len(clauses)} clauses, independently "
        "UNSAT with CaDiCaL 1.9.5 and Glucose 4.2; orbit-40 support <=179"
    )


if __name__ == "__main__":
    main()
