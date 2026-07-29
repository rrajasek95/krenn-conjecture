#!/usr/bin/env python3
"""Exact support and cancellation-transfer audit for the four f=5 graphs.

Unlike verify_saturated_rank_graph_obstruction.py, this script does not
enumerate endpoint colors.  Every rank-one edge has two unknown nonempty
factor supports.  The forced-anchor theorem is encoded by requiring, for
every ordered (vertex,color), an incident rank-one edge whose factor at the
opposite endpoint has exactly that singleton support.

Exceptional edges are allowed to be zero or to have support matching number
at least two.  Coefficient constraints require a constant coloring to have
some supported perfect matching and forbid exactly one supported matching
for a mixed coloring.  The final C4+P2 support survivors are eliminated by
exact cancellation transfers between proportional coefficient fibers.
"""

from __future__ import annotations

import itertools
from collections import Counter, defaultdict

from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


VERTICES = tuple(range(6))
COLORS = tuple(range(3))
CELLS = tuple(itertools.product(COLORS, repeat=2))
COLORINGS = tuple(itertools.product(COLORS, repeat=6))
ALL_EDGES = tuple(itertools.combinations(VERTICES, 2))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for v in vertices[1:]:
        rest = tuple(x for x in vertices if x not in (u, v))
        for matching in perfect_matchings(rest):
            yield ((u, v),) + matching


MATCHINGS = tuple(perfect_matchings(VERTICES))


def path(vertices: tuple[int, ...]):
    return {tuple(sorted((u, v))) for u, v in zip(vertices, vertices[1:])}


FIVE_EDGE_GRAPHS = {
    "P6": path((0, 1, 2, 3, 4, 5)),
    "C3+P3": set(itertools.combinations((0, 1, 2), 2)) | path((3, 4, 5)),
    "C4+P2": path((0, 1, 2, 3)) | {(0, 3), (4, 5)},
    "C5+P1": path((0, 1, 2, 3, 4)) | {(0, 4)},
}

FOUR_EDGE_GRAPHS = {
    "P5+P1": path((0, 1, 2, 3, 4)),
    "P4+P2": path((0, 1, 2, 3)) | {(4, 5)},
    "P3+P3": path((0, 1, 2)) | path((3, 4, 5)),
    "C3+P2+P1": set(itertools.combinations((0, 1, 2), 2)) | {(3, 4)},
    "C4+2P1": path((0, 1, 2, 3)) | {(0, 3)},
}

THREE_EDGE_GRAPHS = {
    "3P2": {(0, 1), (2, 3), (4, 5)},
    "P3+P2+P1": path((0, 1, 2)) | {(3, 4)},
    "P4+2P1": path((0, 1, 2, 3)),
    "C3+3P1": set(itertools.combinations((0, 1, 2), 2)),
}


def support_formula(exceptional_edges: set[tuple[int, int]]):
    rank_one_edges = set(ALL_EDGES) - exceptional_edges
    pool = IDPool()
    formula = CNF()

    # factor(tail, head, color) is the support of the rank-one factor at
    # ``head`` on edge tail-head.  This direction matches the anchor theorem.
    def factor(tail: int, head: int, color: int) -> int:
        return pool.id(("factor", tail, head, color))

    for u, v in sorted(rank_one_edges):
        formula.append([factor(u, v, color) for color in COLORS])
        formula.append([factor(v, u, color) for color in COLORS])

    # Each star supplies all three opposite-head coordinate singletons.
    for tail in VERTICES:
        neighbors = sorted(
            head
            for head in VERTICES
            if tuple(sorted((tail, head))) in rank_one_edges
        )
        for color in COLORS:
            witnesses = []
            for head in neighbors:
                witness = pool.id(("anchor", tail, head, color))
                witnesses.append(witness)
                formula.append([-witness, factor(tail, head, color)])
                for other in COLORS:
                    if other != color:
                        formula.append([-witness, -factor(tail, head, other)])
            formula.append(witnesses)

    def entry(edge: tuple[int, int], i: int, j: int) -> int:
        return pool.id(("entry", edge, i, j))

    active = {}
    for edge in sorted(exceptional_edges):
        active[edge] = pool.id(("active", edge))
        witnesses = []
        for (i, j), (k, ell) in itertools.combinations(CELLS, 2):
            if i == k or j == ell:
                continue
            witness = pool.id(("rank_pair", edge, i, j, k, ell))
            witnesses.append(witness)
            formula.append([-witness, entry(edge, i, j)])
            formula.append([-witness, entry(edge, k, ell)])
        formula.append([-active[edge]] + witnesses)
        for i, j in CELLS:
            formula.append([-entry(edge, i, j), active[edge]])

    def rank_one_conditions(edge: tuple[int, int], coloring: tuple[int, ...]):
        u, v = edge
        # The factor at u is indexed by directed tail v -> head u.
        return (
            factor(v, u, coloring[u]),
            factor(u, v, coloring[v]),
        )

    for coloring in COLORINGS:
        monomials = []
        for matching_index, matching in enumerate(MATCHINGS):
            conditions = []
            for edge in matching:
                if edge in exceptional_edges:
                    conditions.append(entry(edge, coloring[edge[0]], coloring[edge[1]]))
                else:
                    conditions.extend(rank_one_conditions(edge, coloring))
            monomial = pool.id(("monomial", coloring, matching_index))
            monomials.append(monomial)
            for condition in conditions:
                formula.append([-monomial, condition])
            formula.append([monomial] + [-condition for condition in conditions])

        if len(set(coloring)) == 1:
            formula.append(monomials)
        else:
            for monomial in monomials:
                formula.append([-monomial] + [other for other in monomials if other != monomial])

    return formula, pool, active


def p6_rectangle_block_clauses(pool: IDPool, edge, row_pair, column_pair):
    """Clauses asserting that no exact {M0,N3}-support rectangle exists."""
    m0 = ((0, 1), (2, 3), (4, 5))
    n3 = ((0, 5), (1, 2), (3, 4))
    m0_index = MATCHINGS.index(m0)
    n3_index = MATCHINGS.index(n3)
    u, v = edge
    other_vertices = [vertex for vertex in VERTICES if vertex not in edge]
    blocks = []

    for other_values in itertools.product(COLORS, repeat=4):
        coloring = [0] * 6
        for vertex, value in zip(other_vertices, other_values, strict=True):
            coloring[vertex] = value
        corners = []
        for row_color in row_pair:
            for column_color in column_pair:
                coloring[u] = row_color
                coloring[v] = column_color
                corner = tuple(coloring)
                if len(set(corner)) == 1:
                    corners = []
                    break
                corners.append(corner)
            if not corners:
                break
        if not corners:
            continue

        # Negate the conjunction saying that, at every corner, precisely M0
        # and N3 are supported.  Requiring all these block clauses says no
        # suitable assignment of the other four colors exists.
        block = []
        for corner in corners:
            block.extend(
                [
                    -pool.id(("monomial", corner, m0_index)),
                    -pool.id(("monomial", corner, n3_index)),
                ]
            )
            block.extend(
                pool.id(("monomial", corner, index))
                for index in range(len(MATCHINGS))
                if index not in (m0_index, n3_index)
            )
        blocks.append(block)
    return blocks


def audit_p6():
    exceptional = FIVE_EDGE_GRAPHS["P6"]
    formula, pool, active = support_formula(exceptional)
    with Solver(name="g4", bootstrap_with=formula) as solver:
        assert solver.solve()

        # Support constraints force every path matrix active and every entry
        # nonzero, despite initially allowing a zero matrix.
        for edge in sorted(exceptional):
            assert not solver.solve(assumptions=[-active[edge]])
            for i, j in CELLS:
                assert not solver.solve(
                    assumptions=[-pool.id(("entry", edge, i, j))]
                )

        # The only possible defective rank-one incidences are the two factors
        # of edge 05, and neither can be a coordinate singleton.
        for tail, head in ((0, 5), (5, 0)):
            selector = pool.id(("coordinate_05_factor", tail, head))
            for first, second in itertools.combinations(COLORS, 2):
                solver.add_clause(
                    [
                        selector,
                        -pool.id(("factor", tail, head, first)),
                        -pool.id(("factor", tail, head, second)),
                    ]
                )
            assert not solver.solve(assumptions=[-selector])

        # Every 2x2 minor of every path matrix has a coloring rectangle on
        # which exactly the two edge-disjoint matchings M0 and N3 survive.
        color_pairs = tuple(itertools.combinations(COLORS, 2))
        rectangle_queries = 0
        for edge in sorted(exceptional):
            for row_pair in color_pairs:
                for column_pair in color_pairs:
                    selector = pool.id(
                        ("no_rectangle", edge, row_pair, column_pair)
                    )
                    for block in p6_rectangle_block_clauses(
                        pool, edge, row_pair, column_pair
                    ):
                        solver.add_clause([selector] + block)
                    assert not solver.solve(assumptions=[-selector]), (
                        edge,
                        row_pair,
                        column_pair,
                    )
                    rectangle_queries += 1

    print(
        "P6: all 45 path entries forced; all 45 two-matching rectangle "
        f"queries certified ({rectangle_queries})"
    )


def audit_c4_p2_survivor():
    """Check one explicit support assignment surviving the relaxation."""
    exceptional = FIVE_EDGE_GRAPHS["C4+P2"]
    formula, pool, _ = support_formula(exceptional)
    exceptional_supports = {
        (0, 1): {(0, 0), (0, 2), (2, 0), (2, 2)},
        (0, 3): {(i, j) for i in (0, 2) for j in COLORS},
        (1, 2): {(0, 0), (0, 2), (2, 0), (2, 2)},
        (2, 3): {(i, j) for i in (0, 2) for j in COLORS},
        (4, 5): {(0, 0), (1, 1), (2, 2)},
    }
    rank_one_labels = {
        (0, 2): (1, 1),
        (0, 4): (2, 2),
        (0, 5): (2, 0),
        (1, 3): (1, 1),
        (1, 4): (1, 2),
        (1, 5): (1, 0),
        (2, 4): (0, 2),
        (2, 5): (0, 0),
        (3, 4): (1, 0),
        (3, 5): (1, 2),
    }
    assumptions = []
    for edge, support in exceptional_supports.items():
        for i, j in CELLS:
            variable = pool.id(("entry", edge, i, j))
            assumptions.append(variable if (i, j) in support else -variable)
    for (u, v), (color_u, color_v) in rank_one_labels.items():
        for color in COLORS:
            at_u = pool.id(("factor", v, u, color))
            at_v = pool.id(("factor", u, v, color))
            assumptions.append(at_u if color == color_u else -at_u)
            assumptions.append(at_v if color == color_v else -at_v)

    with Solver(name="g4", bootstrap_with=formula) as solver:
        assert solver.solve(assumptions=assumptions)
    print("C4+P2: explicit 23-entry support-level survivor verified")


def audit_c4_p2_cancellation_transfers():
    """Eliminate all support survivors by exact proportional-fiber clauses.

    A formal matching monomial uses one exceptional entry variable, or the
    two endpoint-factor variables of a rank-one edge.  Two finite sets of
    monomials have the same ``translated shape`` when one is a common
    Laurent monomial times the other, up to a bijection.

    If a constant and a mixed coefficient have the same nonempty shape,
    their required values 1 and 0 contradict proportionality.  If a mixed
    zero coefficient is a translated copy of all but one term of another
    mixed coefficient, the remaining supported monomial cannot vanish.
    The loop finds such a contradiction in each SAT support model, adds the
    clause excluding exactly those two support fibers, and continues until
    the exact formula is UNSAT.
    """

    exceptional = FIVE_EDGE_GRAPHS["C4+P2"]
    rank_one = set(ALL_EDGES) - exceptional
    formula, pool, _ = support_formula(exceptional)

    formal_keys = []
    for edge in sorted(exceptional):
        for i, j in CELLS:
            formal_keys.append(("entry", edge, i, j))
    for u, v in sorted(rank_one):
        for color in COLORS:
            formal_keys.extend(
                [
                    ("factor_value", v, u, color),
                    ("factor_value", u, v, color),
                ]
            )
    formal_keys = sorted(set(formal_keys), key=repr)
    formal_index = {key: index for index, key in enumerate(formal_keys)}

    def formal_signature(coloring, matching):
        signature = [0] * len(formal_keys)
        for edge in matching:
            u, v = edge
            if edge in exceptional:
                key = ("entry", edge, coloring[u], coloring[v])
                signature[formal_index[key]] += 1
            else:
                keys = (
                    ("factor_value", v, u, coloring[u]),
                    ("factor_value", u, v, coloring[v]),
                )
                for key in keys:
                    signature[formal_index[key]] += 1
        return tuple(signature)

    signatures = {
        (coloring, matching_index): formal_signature(coloring, matching)
        for coloring in COLORINGS
        for matching_index, matching in enumerate(MATCHINGS)
    }

    def subtract(first, second):
        return tuple(a - b for a, b in zip(first, second, strict=True))

    def translated_shape(vectors):
        return min(
            tuple(sorted(subtract(vector, anchor) for vector in vectors))
            for anchor in vectors
        )

    def exact_support_block(coloring, supported):
        return [
            (
                -pool.id(("monomial", coloring, index))
                if index in supported
                else pool.id(("monomial", coloring, index))
            )
            for index in range(len(MATCHINGS))
        ]

    transfer_count = 0
    with Solver(name="g4", bootstrap_with=formula) as solver:
        while solver.solve():
            model = {literal for literal in solver.get_model() if literal > 0}
            fibers = {
                coloring: tuple(
                    index
                    for index in range(len(MATCHINGS))
                    if pool.id(("monomial", coloring, index)) in model
                )
                for coloring in COLORINGS
            }

            mixed_by_shape = defaultdict(list)
            constant_by_shape = defaultdict(list)
            for coloring, supported in fibers.items():
                if not supported:
                    continue
                shape = translated_shape(
                    [signatures[coloring, index] for index in supported]
                )
                table = (
                    constant_by_shape
                    if len(set(coloring)) == 1
                    else mixed_by_shape
                )
                table[len(supported), shape].append((coloring, supported))

            contradiction = None

            # A nonempty constant coefficient cannot be a Laurent-monomial
            # multiple of a mixed zero coefficient.
            for key, constant_fibers in constant_by_shape.items():
                if key in mixed_by_shape:
                    contradiction = (
                        constant_fibers[0],
                        mixed_by_shape[key][0],
                    )
                    break

            # A translated mixed zero relation cannot account for all but
            # one supported term of another mixed zero coefficient.
            if contradiction is None:
                for coloring, supported in fibers.items():
                    if len(set(coloring)) == 1 or len(supported) < 3:
                        continue
                    for extra in supported:
                        subset = tuple(
                            index for index in supported if index != extra
                        )
                        shape = translated_shape(
                            [signatures[coloring, index] for index in subset]
                        )
                        sources = mixed_by_shape.get((len(subset), shape))
                        if sources:
                            contradiction = (
                                (coloring, supported),
                                sources[0],
                            )
                            break
                    if contradiction is not None:
                        break

            assert contradiction is not None
            first, second = contradiction
            solver.add_clause(
                exact_support_block(first[0], set(first[1]))
                + exact_support_block(second[0], set(second[1]))
            )
            transfer_count += 1

    assert transfer_count > 0
    print(
        "C4+P2: all support survivors eliminated by "
        f"{transfer_count} exact cancellation-transfer clauses"
    )


def audit_five_edge_graph_census():
    """Verify all five-edge max-degree-two graphs lie in the four classes."""
    def relabel(edges, permutation):
        return frozenset(
            tuple(sorted((permutation[u], permutation[v]))) for u, v in edges
        )

    orbits = {
        name: {
            relabel(edges, permutation)
            for permutation in itertools.permutations(VERTICES)
        }
        for name, edges in FIVE_EDGE_GRAPHS.items()
    }
    assert {name: len(orbit) for name, orbit in orbits.items()} == {
        "P6": 360,
        "C3+P3": 60,
        "C4+P2": 45,
        "C5+P1": 72,
    }
    candidates = {
        frozenset(edges)
        for edges in itertools.combinations(ALL_EDGES, 5)
        if max(sum(vertex in edge for edge in edges) for vertex in VERTICES)
        <= 2
    }
    union = set().union(*orbits.values())
    assert len(candidates) == 537
    assert sum(map(len, orbits.values())) == len(union) == len(candidates)
    assert union == candidates
    print("f=5 graph census: 537 labelled supports in four disjoint orbits")


def main():
    audit_five_edge_graph_census()
    for name in ("C3+P3", "C5+P1"):
        formula, pool, _ = support_formula(FIVE_EDGE_GRAPHS[name])
        with Solver(name="g4", bootstrap_with=formula) as solver:
            assert not solver.solve(), name
        print(f"{name}: arbitrary-factor support formula UNSAT")

    audit_p6()

    # This relaxation alone has survivors on the final f=5 graph type, but
    # none survives the exact coefficient-transfer audit.
    audit_c4_p2_survivor()
    audit_c4_p2_cancellation_transfers()


if __name__ == "__main__":
    main()
