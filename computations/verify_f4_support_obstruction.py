#!/usr/bin/env python3
"""Exact support/cancellation exploration for the five f=4 rank graphs."""

from __future__ import annotations

import itertools
from collections import defaultdict

from pysat.solvers import Solver

import search_f5_support_sat as base


def require(condition, message):
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise RuntimeError(message)


def formal_signatures(exceptional, pool):
    rank_one = set(base.ALL_EDGES) - exceptional
    keys = []
    for edge in exceptional:
        for i, j in base.CELLS:
            keys.append(("entry", edge, i, j))
    for u, v in rank_one:
        for color in base.COLORS:
            keys.extend(
                [
                    ("factor_value", v, u, color),
                    ("factor_value", u, v, color),
                ]
            )
    keys = sorted(set(keys), key=repr)
    index = {key: position for position, key in enumerate(keys)}

    def signature(coloring, matching):
        answer = [0] * len(keys)
        for edge in matching:
            u, v = edge
            if edge in exceptional:
                key = ("entry", edge, coloring[u], coloring[v])
                answer[index[key]] += 1
            else:
                for key in (
                    ("factor_value", v, u, coloring[u]),
                    ("factor_value", u, v, coloring[v]),
                ):
                    answer[index[key]] += 1
        return tuple(answer)

    return {
        (coloring, matching_index): signature(coloring, matching)
        for coloring in base.COLORINGS
        for matching_index, matching in enumerate(base.MATCHINGS)
    }


def translated_shape(vectors, coefficients=None):
    """Canonical Laurent shape, optionally retaining relative term signs.

    A zero coefficient fiber may be multiplied by an arbitrary nonzero
    Laurent monomial and by one global scalar.  When ``coefficients`` are
    supplied, the canonical form therefore records each exponent relative
    to an anchor and each coefficient relative to the anchor coefficient.
    This is the only change needed by cancellation transfers for Pfaffian
    matching signs.  The historical unsigned caller gets exactly its old
    exponent-only key.
    """
    def subtract(first, second):
        return tuple(a - b for a, b in zip(first, second, strict=True))

    if coefficients is not None:
        require(
            len(vectors) == len(coefficients),
            f"{len(vectors)} vectors but {len(coefficients)} coefficients",
        )
        require(
            all(value in (-1, 1) for value in coefficients),
            f"coefficients {coefficients} are not all +-1",
        )
        return min(
            tuple(
                sorted(
                    (
                        subtract(vector, vectors[anchor]),
                        coefficient * coefficients[anchor],
                    )
                    for vector, coefficient in zip(
                        vectors, coefficients, strict=True
                    )
                )
            )
            for anchor in range(len(vectors))
        )

    return min(
        tuple(sorted(subtract(vector, anchor) for vector in vectors))
        for anchor in vectors
    )


def exact_support_block(pool, coloring, supported):
    return [
        (
            -pool.id(("monomial", coloring, index))
            if index in supported
            else pool.id(("monomial", coloring, index))
        )
        for index in range(len(base.MATCHINGS))
    ]


def add_cancellation_transfers(
    solver,
    pool,
    signatures,
    limit=10000,
    clause_sink=None,
    term_signs=None,
    semantic_sink=None,
):
    """Add all model-guided sound transfer cuts until UNSAT or stable."""
    if term_signs is None:
        term_signs = (1,) * len(base.MATCHINGS)
        signed_shapes = False
    else:
        term_signs = tuple(term_signs)
        require(
            len(term_signs) == len(base.MATCHINGS),
            f"{len(term_signs)} term signs but {len(base.MATCHINGS)} matchings",
        )
        require(
            all(value in (-1, 1) for value in term_signs),
            f"term signs {term_signs} are not all +-1",
        )
        signed_shapes = True

    def shape_for(coloring, supported):
        vectors = [signatures[coloring, index] for index in supported]
        coefficients = (
            [term_signs[index] for index in supported]
            if signed_shapes
            else None
        )
        return translated_shape(vectors, coefficients)

    transfer_count = 0
    while solver.solve():
        model = {literal for literal in solver.get_model() if literal > 0}
        fibers = {
            coloring: tuple(
                index
                for index in range(len(base.MATCHINGS))
                if pool.id(("monomial", coloring, index)) in model
            )
            for coloring in base.COLORINGS
        }
        mixed = defaultdict(list)
        constant = defaultdict(list)
        for coloring, supported in fibers.items():
            if not supported:
                continue
            shape = shape_for(coloring, supported)
            table = constant if len(set(coloring)) == 1 else mixed
            table[len(supported), shape].append((coloring, supported))

        contradiction = None
        semantic_record = None
        for key, constant_fibers in constant.items():
            if key in mixed:
                target = constant_fibers[0]
                source = mixed[key][0]
                contradiction = [target, source]
                semantic_record = {
                    "kind": "transfer",
                    "target_kind": "constant",
                    "target": target,
                    "sources": ((source, target[1]),),
                    "leftover": (),
                }
                break

        if contradiction is None:
            for coloring, supported in fibers.items():
                if len(set(coloring)) == 1 or len(supported) < 3:
                    continue
                for extra in supported:
                    subset = tuple(
                        index for index in supported if index != extra
                    )
                    shape = shape_for(coloring, subset)
                    sources = mixed.get((len(subset), shape))
                    if sources:
                        target = (coloring, supported)
                        source = sources[0]
                        contradiction = [target, source]
                        semantic_record = {
                            "kind": "transfer",
                            "target_kind": "mixed",
                            "target": target,
                            "sources": ((source, subset),),
                            "leftover": (extra,),
                        }
                        break
                if contradiction is not None:
                    break

        # More generally, disjoint translated mixed-zero fibers cannot cover
        # a constant fiber, nor all but one monomial of a mixed fiber.
        if contradiction is None:
            for coloring, supported in fibers.items():
                if not supported:
                    continue
                target_size = len(supported)
                is_constant = len(set(coloring)) == 1
                if not is_constant and target_size < 3:
                    continue

                candidates = []
                for mask in range(1, 1 << target_size):
                    subset_positions = [
                        position
                        for position in range(target_size)
                        if mask & (1 << position)
                    ]
                    if len(subset_positions) < 2:
                        continue
                    subset = tuple(supported[position] for position in subset_positions)
                    shape = shape_for(coloring, subset)
                    sources = mixed.get((len(subset), shape))
                    if sources:
                        candidates.append((mask, sources[0]))

                desired_masks = (
                    [(1 << target_size) - 1]
                    if is_constant
                    else [
                        ((1 << target_size) - 1) ^ (1 << leftover)
                        for leftover in range(target_size)
                    ]
                )

                def exact_cover(remaining, chosen):
                    if remaining == 0:
                        return chosen
                    first_bit = remaining & -remaining
                    for mask, source in candidates:
                        if mask & first_bit and mask & remaining == mask:
                            answer = exact_cover(
                                remaining ^ mask, chosen + [(mask, source)]
                            )
                            if answer is not None:
                                return answer
                    return None

                for desired in desired_masks:
                    cover = exact_cover(desired, [])
                    if cover is not None:
                        target = (coloring, supported)
                        contradiction = [target] + [source for _mask, source in cover]
                        covered_sources = []
                        for mask, source in cover:
                            target_subset = tuple(
                                supported[position]
                                for position in range(target_size)
                                if mask & (1 << position)
                            )
                            covered_sources.append((source, target_subset))
                        leftover = tuple(
                            supported[position]
                            for position in range(target_size)
                            if not desired & (1 << position)
                        )
                        semantic_record = {
                            "kind": "transfer",
                            "target_kind": (
                                "constant" if is_constant else "mixed"
                            ),
                            "target": target,
                            "sources": tuple(covered_sources),
                            "leftover": leftover,
                        }
                        break
                if contradiction is not None:
                    break

        if contradiction is None:
            return True, transfer_count
        require(
            semantic_record is not None,
            "a contradiction was found without a semantic record",
        )

        clause = []
        for coloring, supported in contradiction:
            clause.extend(
                exact_support_block(pool, coloring, set(supported))
            )
        solver.add_clause(clause)
        if clause_sink is not None:
            clause_sink.append(list(clause))
        if semantic_sink is not None:
            semantic_sink.append(semantic_record)
        transfer_count += 1
        require(transfer_count < limit, f"transfer limit {limit} exhausted")

    return False, transfer_count


def all_two_matching_rectangles(
    solver, pool, exceptional, active_variables=None
):
    """Check every exceptional 2x2 minor has some exact binomial rectangle."""
    color_pairs = tuple(itertools.combinations(base.COLORS, 2))
    matching_pairs = tuple(itertools.combinations(range(len(base.MATCHINGS)), 2))
    queries = 0

    for edge in sorted(exceptional):
        u, v = edge
        other_vertices = [vertex for vertex in base.VERTICES if vertex not in edge]
        candidate_pairs = [
            (first, second)
            for first, second in matching_pairs
            if (edge in base.MATCHINGS[first]) != (edge in base.MATCHINGS[second])
        ]
        require(candidate_pairs, f"edge {edge} has no separating matching pair")

        for row_pair in color_pairs:
            for column_pair in color_pairs:
                selector = pool.id(
                    ("no_any_rectangle", edge, row_pair, column_pair)
                )
                for first, second in candidate_pairs:
                    for other_values in itertools.product(base.COLORS, repeat=4):
                        coloring = [0] * 6
                        for vertex, value in zip(
                            other_vertices, other_values, strict=True
                        ):
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

                        block = []
                        for corner in corners:
                            block.extend(
                                [
                                    -pool.id(("monomial", corner, first)),
                                    -pool.id(("monomial", corner, second)),
                                ]
                            )
                            block.extend(
                                pool.id(("monomial", corner, index))
                                for index in range(len(base.MATCHINGS))
                                if index not in (first, second)
                            )
                        solver.add_clause([selector] + block)

                assumptions = [-selector]
                if active_variables is not None:
                    assumptions.append(active_variables[edge])
                for row_color in row_pair:
                    for column_color in column_pair:
                        assumptions.append(
                            pool.id(
                                (
                                    "entry",
                                    edge,
                                    row_color,
                                    column_color,
                                )
                            )
                        )
                if solver.solve(assumptions=assumptions):
                    return False, (edge, row_pair, column_pair)
                queries += 1

    return True, queries


def support_is_two_closed(solver, pool, exceptional, active_variables):
    """Check that an active support 2-matching completes its 2x2 rectangle."""
    color_pairs = tuple(itertools.combinations(base.COLORS, 2))
    queries = 0
    for edge in sorted(exceptional):
        for row_pair in color_pairs:
            for column_pair in color_pairs:
                i, k = row_pair
                j, ell = column_pair
                for diagonal, cross in (
                    (((i, j), (k, ell)), ((i, ell), (k, j))),
                    (((i, ell), (k, j)), ((i, j), (k, ell))),
                ):
                    base_assumptions = [
                        active_variables[edge],
                        pool.id(("entry", edge, *diagonal[0])),
                        pool.id(("entry", edge, *diagonal[1])),
                    ]
                    for missing in cross:
                        if solver.solve(
                            assumptions=base_assumptions
                            + [-pool.id(("entry", edge, *missing))]
                        ):
                            return False, (
                                edge,
                                row_pair,
                                column_pair,
                                diagonal,
                                missing,
                            )
                        queries += 1
    return True, queries


def audit_graph(name, exceptional):
    formula, pool, active = base.support_formula(exceptional)
    signatures = formal_signatures(exceptional, pool)
    with Solver(name="g4", bootstrap_with=formula) as solver:
        survives, transfers = add_cancellation_transfers(
            solver, pool, signatures
        )
        if not survives:
            print(f"{name}: UNSAT after {transfers} cancellation transfers")
            return
        all_zero_impossible = not solver.solve(
            assumptions=[-variable for variable in active.values()]
        )
        forced_active = {
            edge
            for edge, variable in active.items()
            if not solver.solve(assumptions=[-variable])
        }
        good_edges = []
        first_failure = None
        for edge in sorted(exceptional):
            two_closed, closure_detail = support_is_two_closed(
                solver, pool, {edge}, active
            )
            rectangles, detail = all_two_matching_rectangles(
                solver, pool, {edge}, active_variables=active
            )
            if two_closed and rectangles:
                good_edges.append(edge)
            elif first_failure is None:
                first_failure = (
                    edge,
                    two_closed,
                    closure_detail,
                    rectangles,
                    detail,
                )

            # One forced-active good edge already contradicts rank >= 2.
            if edge in forced_active and edge in good_edges:
                break

        forced_good = sorted(forced_active & set(good_edges))
        every_edge_good = all_zero_impossible and set(good_edges) == set(
            exceptional
        )
        closed = bool(forced_good) or every_edge_good
        require(
            closed,
            repr(
                {
                    "name": name,
                    "transfers": transfers,
                    "all_zero_impossible": all_zero_impossible,
                    "forced_active": sorted(forced_active),
                    "good_edges": good_edges,
                    "first_failure": first_failure,
                }
            ),
        )
        # Two distinct certificates close a row, and only one of them forces
        # an edge active.  Report whichever one was actually obtained.
        if forced_good:
            certificate = (
                f"exceptional edge {forced_good[0]} is forced active and good"
            )
        else:
            certificate = (
                f"every exceptional edge {sorted(good_edges)} is good and the "
                "all-zero assignment is impossible, so some good edge is "
                "active"
            )
        print(f"{name}: {transfers} transfers; {certificate}")


def audit_graph_census():
    def relabel(edges, permutation):
        return frozenset(
            tuple(sorted((permutation[u], permutation[v]))) for u, v in edges
        )

    orbits = {
        name: {
            relabel(edges, permutation)
            for permutation in itertools.permutations(base.VERTICES)
        }
        for name, edges in base.FOUR_EDGE_GRAPHS.items()
    }
    orbit_sizes = {name: len(orbit) for name, orbit in orbits.items()}
    require(
        orbit_sizes
        == {
            "P5+P1": 360,
            "P4+P2": 180,
            "P3+P3": 90,
            "C3+P2+P1": 60,
            "C4+2P1": 45,
        },
        f"f=4 orbit sizes {orbit_sizes} differ from the census",
    )
    candidates = {
        frozenset(edges)
        for edges in itertools.combinations(base.ALL_EDGES, 4)
        if max(
            sum(vertex in edge for edge in edges)
            for vertex in base.VERTICES
        )
        <= 2
    }
    union = set().union(*orbits.values())
    require(len(candidates) == 735, f"{len(candidates)} candidates != 735")
    require(
        sum(map(len, orbits.values())) == len(union) == len(candidates),
        f"orbits overlap or miss candidates: "
        f"{sum(map(len, orbits.values()))}/{len(union)}/{len(candidates)}",
    )
    require(union == candidates, "f=4 orbit union != candidate set")
    print("f=4 graph census: 735 labelled supports in five disjoint orbits")


def main():
    audit_graph_census()
    for name, exceptional in base.FOUR_EDGE_GRAPHS.items():
        audit_graph(name, exceptional)


if __name__ == "__main__":
    main()
