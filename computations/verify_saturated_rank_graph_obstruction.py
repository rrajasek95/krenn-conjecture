#!/usr/bin/env python3
"""Exact audit of the two saturated six-vertex rank-graph charts.

This verifies the finite lemmas used in
``proofs/saturated-rank-graph-obstruction.md``.  There is no floating-point
arithmetic.  PySAT is used only for Boolean support implications.

The rank-one complement edges are coordinate-coordinate basis tensors.  At
each vertex, slice covering says that the colors at the *opposite* endpoints
of its three rank-one edges are 0, 1, 2 in some order.  Hence there are
(3!)^6 = 46656 raw directed anchor patterns.

For F=C6 the script checks, on all 718 D12 x S3_color orbits, that

1. coefficient-support necessities force every cycle matrix to be nonzero;
2. they then force all 54 cycle-matrix entries to be nonzero; and
3. every 2x2 minor has a four-coloring rectangle on which only the two
   all-cycle perfect matchings can contribute.

For F=C3 disjoint-union C3 it checks, on all 134
(S3 wreath C2) x S3_color orbits, that the coefficient-support necessities
are inconsistent when each of the six internal matrices is *either*
identically zero *or* of rank at least two.  The zero alternative is part of
the audited formula, so this branch needs no separate hand argument ruling
out a zero internal matrix.

Every check below raises instead of asserting, so the audit is still
performed under ``python3 -O``.
"""

from __future__ import annotations

import itertools
import time
from collections.abc import Iterable

from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


SOLVER_NAMES = ("g4", "cadical195")


def require(condition: object, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


VERTICES = tuple(range(6))
COLORS = tuple(range(3))
COLORINGS = tuple(itertools.product(COLORS, repeat=6))
CELLS = tuple(itertools.product(COLORS, repeat=2))
COLOR_PERMUTATIONS = tuple(itertools.permutations(COLORS))
ALL_EDGES = set(itertools.combinations(VERTICES, 2))


def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    answer: list[tuple[tuple[int, int], ...]] = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            answer.append(((first, second),) + matching)
    return tuple(answer)


MATCHINGS = perfect_matchings(VERTICES)


def c6_edges() -> tuple[tuple[int, int], ...]:
    return tuple(sorted({(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 5)}))


def two_triangle_edges() -> tuple[tuple[int, int], ...]:
    return tuple(
        sorted(
            set(itertools.combinations((0, 1, 2), 2))
            | set(itertools.combinations((3, 4, 5), 2))
        )
    )


def directed_arcs(rank_one_edges: set[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    return tuple(
        sorted(
            (u, v)
            for u in VERTICES
            for v in VERTICES
            if tuple(sorted((u, v))) in rank_one_edges
        )
    )


def raw_anchor_patterns(
    rank_one_edges: set[tuple[int, int]], arcs: tuple[tuple[int, int], ...]
) -> set[tuple[int, ...]]:
    """Enumerate the (3!)^6 outgoing-head color patterns.

    The value on directed arc (u,v) is the coordinate color of the factor at
    v.  For fixed u, its values on the three rank-one neighbors form a
    permutation of 0,1,2.
    """

    patterns: set[tuple[int, ...]] = set()
    for vertex_permutations in itertools.product(COLOR_PERMUTATIONS, repeat=6):
        head_color: dict[tuple[int, int], int] = {}
        for u in VERTICES:
            neighbors = sorted(
                v for v in VERTICES if tuple(sorted((u, v))) in rank_one_edges
            )
            require(len(neighbors) == 3, f"vertex {u} needs three rank-one neighbors")
            for v, color in zip(neighbors, vertex_permutations[u], strict=True):
                head_color[u, v] = color
        patterns.add(tuple(head_color[arc] for arc in arcs))
    require(
        len(patterns) == 6**6 == 46656,
        f"raw anchor patterns: {len(patterns)} != 46656",
    )
    return patterns


def c6_automorphisms() -> tuple[tuple[int, ...], ...]:
    answer = {
        tuple((sign * vertex + shift) % 6 for vertex in VERTICES)
        for sign in (1, -1)
        for shift in VERTICES
    }
    require(len(answer) == 12, f"C6 automorphisms: {len(answer)} != 12")
    return tuple(sorted(answer))


def two_triangle_automorphisms() -> tuple[tuple[int, ...], ...]:
    answer: set[tuple[int, ...]] = set()
    for left in itertools.permutations((0, 1, 2)):
        for right_zero_based in itertools.permutations((0, 1, 2)):
            right = tuple(3 + value for value in right_zero_based)
            answer.add(left + right)
            # Swap the two triangle components.
            answer.add(right + left)
    require(len(answer) == 72, f"C3+C3 automorphisms: {len(answer)} != 72")
    return tuple(sorted(answer))


def orbit_representatives(
    rank_one_edges: set[tuple[int, int]],
    graph_automorphisms: tuple[tuple[int, ...], ...],
    expected_count: int,
) -> tuple[tuple[int, ...], ...]:
    arcs = directed_arcs(rank_one_edges)
    arc_index = {arc: index for index, arc in enumerate(arcs)}
    remaining = raw_anchor_patterns(rank_one_edges, arcs)
    representatives: list[tuple[int, ...]] = []
    covered = 0

    def act(
        pattern: tuple[int, ...],
        vertex_permutation: tuple[int, ...],
        color_permutation: tuple[int, ...],
    ) -> tuple[int, ...]:
        image = [0] * len(arcs)
        for (u, v), color in zip(arcs, pattern, strict=True):
            image[arc_index[vertex_permutation[u], vertex_permutation[v]]] = (
                color_permutation[color]
            )
        return tuple(image)

    while remaining:
        pattern = next(iter(remaining))
        orbit = {
            act(pattern, vertex_permutation, color_permutation)
            for vertex_permutation in graph_automorphisms
            for color_permutation in COLOR_PERMUTATIONS
        }
        present = orbit & remaining
        require(present, "orbit missed its own representative")
        remaining -= present
        covered += len(present)
        representatives.append(min(orbit))

    require(covered == 46656, f"orbit cover: {covered} != 46656")
    require(
        len(representatives) == expected_count,
        f"orbit count: {len(representatives)} != {expected_count}",
    )
    return tuple(sorted(representatives))


def endpoint_labels(
    pattern: tuple[int, ...], rank_one_edges: set[tuple[int, int]]
) -> dict[tuple[int, int], tuple[int, int]]:
    arcs = directed_arcs(rank_one_edges)
    head_color = dict(zip(arcs, pattern, strict=True))
    # On u<v, the local factor at u is seen from tail v, and conversely.
    return {
        (u, v): (head_color[v, u], head_color[u, v])
        for u, v in rank_one_edges
    }


def matching_is_basis_compatible(
    matching: tuple[tuple[int, int], ...],
    coloring: tuple[int, ...],
    labels: dict[tuple[int, int], tuple[int, int]],
) -> bool:
    return all(
        edge not in labels
        or (coloring[edge[0]], coloring[edge[1]]) == labels[edge]
        for edge in matching
    )


def support_formula(
    pattern: tuple[int, ...],
    exceptional_edges: tuple[tuple[int, int], ...],
    allow_zero_exceptional_matrices: bool,
) -> tuple[
    CNF,
    IDPool,
    dict[tuple[tuple[int, int], int, int], int],
    dict[tuple[int, int], int],
]:
    """Build necessary (not sufficient) coefficient-support conditions.

    A mixed target coefficient may have either zero or at least two supported
    perfect-matching monomials; exactly one is impossible over C because its
    monomial is nonzero.  A constant target coefficient must have at least
    one supported matching.

    A rank-at-least-two matrix support contains two nonzero cells in distinct
    rows and columns.  The auxiliary variables below existentially select
    such a pair.  When ``allow_zero_exceptional_matrices`` is true, each
    exceptional matrix is allowed either to be identically zero or to contain
    such a pair.  These are necessary conditions for the actual matrices, so
    an UNSAT result is a rigorous obstruction.
    """

    exceptional = set(exceptional_edges)
    rank_one_edges = ALL_EDGES - exceptional
    labels = endpoint_labels(pattern, rank_one_edges)
    pool = IDPool()
    formula = CNF()
    entry_variables: dict[tuple[tuple[int, int], int, int], int] = {}
    active_variables: dict[tuple[int, int], int] = {}

    def entry(edge: tuple[int, int], i: int, j: int) -> int:
        key = (edge, i, j)
        if key not in entry_variables:
            entry_variables[key] = pool.id(("entry", edge, i, j))
        return entry_variables[key]

    for edge in exceptional_edges:
        active = pool.id(("active", edge))
        active_variables[edge] = active
        rank_two_witnesses: list[int] = []

        if allow_zero_exceptional_matrices:
            # A false active variable forces all entries to vanish.
            for i, j in CELLS:
                formula.append([-entry(edge, i, j), active])

        for (i, j), (k, ell) in itertools.combinations(CELLS, 2):
            if i == k or j == ell:
                continue
            witness = pool.id(("rank_pair", edge, i, j, k, ell))
            rank_two_witnesses.append(witness)
            formula.append([-witness, entry(edge, i, j)])
            formula.append([-witness, entry(edge, k, ell)])

        if allow_zero_exceptional_matrices:
            formula.append([-active] + rank_two_witnesses)
        else:
            formula.append(rank_two_witnesses)
            formula.append([active])

    for coloring in COLORINGS:
        variable_matchings: list[int] = []
        always_supported = 0

        for matching_index, matching in enumerate(MATCHINGS):
            if not matching_is_basis_compatible(matching, coloring, labels):
                continue
            used_entries = [
                entry(edge, coloring[edge[0]], coloring[edge[1]])
                for edge in matching
                if edge in exceptional
            ]
            if not used_entries:
                always_supported += 1
                continue

            monomial = pool.id(("monomial", coloring, matching_index))
            variable_matchings.append(monomial)
            # monomial <=> conjunction(used_entries)
            for used_entry in used_entries:
                formula.append([-monomial, used_entry])
            formula.append([monomial] + [-used_entry for used_entry in used_entries])

        is_constant = len(set(coloring)) == 1
        if is_constant:
            if always_supported == 0:
                formula.append(variable_matchings)
            continue

        if always_supported >= 2:
            continue
        if always_supported == 1:
            # At least one additional matching is needed to avoid a singleton.
            formula.append(variable_matchings)
            continue

        # If a variable matching is supported, at least one other must be.
        for monomial in variable_matchings:
            formula.append(
                [-monomial]
                + [other for other in variable_matchings if other != monomial]
            )

    return formula, pool, entry_variables, active_variables


def coloring_is_free_mixed(
    coloring: tuple[int, ...],
    exceptional: set[tuple[int, int]],
    labels: dict[tuple[int, int], tuple[int, int]],
) -> bool:
    if len(set(coloring)) == 1:
        return False
    return all(
        not (
            any(edge not in exceptional for edge in matching)
            and matching_is_basis_compatible(matching, coloring, labels)
        )
        for matching in MATCHINGS
    )


def audit_c6_rectangles(
    representatives: Iterable[tuple[int, ...]],
    cycle_edges: tuple[tuple[int, int], ...],
) -> int:
    exceptional = set(cycle_edges)
    rank_one_edges = ALL_EDGES - exceptional
    color_pairs = tuple(itertools.combinations(COLORS, 2))
    global_minimum = 10**9

    for pattern in representatives:
        labels = endpoint_labels(pattern, rank_one_edges)
        free = {
            coloring
            for coloring in COLORINGS
            if coloring_is_free_mixed(coloring, exceptional, labels)
        }

        for edge in cycle_edges:
            u, v = edge
            other_vertices = [vertex for vertex in VERTICES if vertex not in edge]
            for row_colors in color_pairs:
                for column_colors in color_pairs:
                    witnesses = 0
                    for other_values in itertools.product(COLORS, repeat=4):
                        coloring = [0] * 6
                        for vertex, value in zip(
                            other_vertices, other_values, strict=True
                        ):
                            coloring[vertex] = value
                        rectangle_is_free = True
                        for row_color in row_colors:
                            coloring[u] = row_color
                            for column_color in column_colors:
                                coloring[v] = column_color
                                if tuple(coloring) not in free:
                                    rectangle_is_free = False
                                    break
                            if not rectangle_is_free:
                                break
                        if rectangle_is_free:
                            witnesses += 1
                    require(
                        witnesses > 0,
                        f"no free rectangle for edge {edge} at "
                        f"{row_colors}x{column_colors}",
                    )
                    global_minimum = min(global_minimum, witnesses)

    return global_minimum


def audit_c6() -> None:
    cycle_edges = c6_edges()
    rank_one_edges = ALL_EDGES - set(cycle_edges)
    representatives = orbit_representatives(
        rank_one_edges, c6_automorphisms(), expected_count=718
    )

    for orbit_index, pattern in enumerate(representatives):
        formula, _, entries, active = support_formula(
            pattern, cycle_edges, allow_zero_exceptional_matrices=True
        )
        with Solver(name="g4", bootstrap_with=formula) as solver:
            require(solver.solve(), f"C6 orbit {orbit_index}: relaxation is UNSAT")
            # No cycle matrix may be zero.
            for edge in cycle_edges:
                require(
                    not solver.solve(assumptions=[-active[edge]]),
                    f"C6 orbit {orbit_index}: {edge} may be zero",
                )
            # In fact every one of their 54 entries is forced nonzero.
            for edge in cycle_edges:
                for i, j in CELLS:
                    require(
                        not solver.solve(assumptions=[-entries[edge, i, j]]),
                        f"C6 orbit {orbit_index}: entry {edge} {(i, j)} "
                        "is not forced",
                    )

    minimum_rectangle_count = audit_c6_rectangles(representatives, cycle_edges)
    print(
        "C6: 46656 raw patterns, 718 orbits; all 54 entries forced; "
        f"minimum free-rectangle witness count = {minimum_rectangle_count}"
    )


def audit_two_triangles() -> None:
    """Exclude F = C3 + C3 while allowing zero internal matrices.

    Each of the six internal matrices is only required to be *either*
    identically zero *or* to contain two supported cells in distinct rows
    and columns.  That disjunction admits strictly more assignments than
    rank at least two alone, so UNSAT of it is the stronger statement: it
    covers the zero charts as well, and no separate hand argument against a
    zero internal matrix is used.

    Some orbits are already refuted while the clauses are being written: a
    constant coloring whose target coefficient is one admits no compatible
    perfect matching at all, and its "at least one supported matching"
    clause comes out empty.  An empty clause is UNSAT by definition, but
    solver front ends differ on how they accept one, so it is counted here
    and the solvers are handed the formula with empty clauses removed.
    Deleting clauses only weakens a formula, so UNSAT of what the solvers
    see implies UNSAT of the full formula.
    """

    internal_edges = two_triangle_edges()
    rank_one_edges = ALL_EDGES - set(internal_edges)
    representatives = orbit_representatives(
        rank_one_edges, two_triangle_automorphisms(), expected_count=134
    )

    empty_clause_orbits = 0
    for orbit_index, pattern in enumerate(representatives):
        formula, _, _, _ = support_formula(
            pattern, internal_edges, allow_zero_exceptional_matrices=True
        )
        nonempty = [clause for clause in formula.clauses if clause]
        if len(nonempty) != len(formula.clauses):
            empty_clause_orbits += 1
        for solver_name in SOLVER_NAMES:
            with Solver(name=solver_name, bootstrap_with=nonempty) as solver:
                require(
                    not solver.solve(),
                    f"C3+C3 orbit {orbit_index}: {solver_name} found a model",
                )

    print(
        "C3+C3: 46656 raw patterns, 134 orbits; every zero-or-rank>=2 "
        f"support formula is UNSAT under {'/'.join(SOLVER_NAMES)} "
        f"({empty_clause_orbits} of them already at construction)"
    )


def main() -> None:
    started = time.monotonic()
    audit_c6()
    audit_two_triangles()
    print(f"exact saturated-chart audit passed in {time.monotonic() - started:.2f}s")


if __name__ == "__main__":
    main()
