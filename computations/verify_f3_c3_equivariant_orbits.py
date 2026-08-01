#!/usr/bin/env python3
"""Solver-free audit of the exact joint-C3 n=8 search reduction.

This script independently regenerates the coupled cell action, all colouring
orbits, the centralizer of ``(012)(345)``, and its perfect-matching orbits.
It then compares those objects with the exact SAT search and with the older
84-parameter numerical parametrization.  No SAT solver is constructed or
called.
"""

from __future__ import annotations

import sys
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import search_c3_equivariant_n8 as numerical  # noqa: E402
import search_f3_c3_equivariant_n8 as exact  # noqa: E402


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


N = 8
Q = 3
VERTICES = tuple(range(N))
G = (1, 2, 0, 4, 5, 3, 6, 7)


def independent_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1:]
        for tail in independent_matchings(remainder):
            yield ((first, second),) + tail


MATCHINGS = tuple(independent_matchings(VERTICES))


def canonical_cell(u, v, left, right):
    if u < v:
        return u, v, left, right
    return v, u, right, left


def independent_cell_step(cell):
    u, v, left, right = cell
    return canonical_cell(
        G[u], G[v], (left + 1) % Q, (right + 1) % Q,
    )


def independent_cell_orbit(cell):
    cell = canonical_cell(*cell)
    answer = []
    for _ in range(3):
        answer.append(cell)
        cell = independent_cell_step(cell)
    require(
        cell == answer[0],
        "cell == answer[0]",
    )
    return frozenset(answer)


def independent_cell_key(cell):
    return min(independent_cell_orbit(cell))


def independent_colouring_step(colouring):
    image = [None] * N
    for old_vertex, colour in enumerate(colouring):
        image[G[old_vertex]] = (colour + 1) % Q
    return tuple(image)


def independent_colouring_orbit(colouring):
    answer = []
    for _ in range(3):
        answer.append(colouring)
        colouring = independent_colouring_step(colouring)
    require(
        colouring == answer[0],
        "colouring == answer[0]",
    )
    return frozenset(answer)


def canonical_matching(matching):
    return tuple(sorted(
        (min(u, v), max(u, v)) for u, v in matching
    ))


def matching_image(matching, permutation):
    return canonical_matching(
        (permutation[u], permutation[v]) for u, v in matching
    )


def monomial(colouring, matching):
    return tuple(sorted(
        independent_cell_key((u, v, colouring[u], colouring[v]))
        for u, v in matching
    ))


def audit_cells():
    require(
        tuple(G[G[G[v]]] for v in VERTICES) == VERTICES,
        "tuple(G[G[G[v]]] for v in VERTICES) == VERTICES",
    )
    all_cells = tuple(
        (u, v, left, right)
        for u, v in combinations(VERTICES, 2)
        for left, right in product(range(Q), repeat=2)
    )
    orbit_by_key = {}
    for cell in all_cells:
        orbit_by_key.setdefault(
            independent_cell_key(cell), independent_cell_orbit(cell)
        )
    require(
        len(all_cells) == 252,
        "len(all_cells) == 252",
    )
    require(
        len(orbit_by_key) == 84,
        "len(orbit_by_key) == 84",
    )
    require(
        {len(orbit) for orbit in orbit_by_key.values()} == {3},
        "{len(orbit) for orbit in orbit_by_key.values()} == {3}",
    )
    require(
        set().union(*orbit_by_key.values()) == set(all_cells),
        "set().union(*orbit_by_key.values()) == set(all_cells)",
    )
    require(
        sum(map(len, orbit_by_key.values())) == len(all_cells),
        "sum(map(len, orbit_by_key.values())) == len(all_cells)",
    )

    independent_keys = tuple(sorted(orbit_by_key))
    require(
        exact.GENERATOR == G,
        "exact.GENERATOR == G",
    )
    require(
        exact.CELL_KEYS == independent_keys,
        "exact.CELL_KEYS == independent_keys",
    )
    for cell in all_cells:
        key = independent_cell_key(cell)
        require(
            exact.cell_orbit_key(*cell) == key,
            "exact.cell_orbit_key(*cell) == key",
        )
        require(
            exact.CELL_KEYS[exact.CELL_TO_INDEX[cell]] == key,
            "exact.CELL_KEYS[exact.CELL_TO_INDEX[cell]] == key",
        )

    # On the fixed edge 67, the three orbit parameters are exactly b-a mod 3.
    fixed_classes = {}
    for left, right in product(range(Q), repeat=2):
        key = independent_cell_key((6, 7, left, right))
        fixed_classes.setdefault(key, set()).add((right - left) % Q)
    require(
        len(fixed_classes) == 3,
        "len(fixed_classes) == 3",
    )
    require(
        sorted(next(iter(values)) for values in fixed_classes.values()) == [0, 1, 2],
        "sorted(next(iter(values)) for values in fixed_classes.val...",
    )
    require(
        all(len(values) == 1 for values in fixed_classes.values()),
        "all(len(values) == 1 for values in fixed_classes.values())",
    )

    # Compare the equality partition with the pre-existing numerical expand().
    require(
        numerical.G == G and numerical.PARAMETERS == 84,
        "numerical.G == G and numerical.PARAMETERS == 84",
    )
    parameter_labels = np.arange(1, numerical.PARAMETERS + 1, dtype=np.int64)
    matrices = numerical.expand(parameter_labels)
    labels_by_key = {}
    for cell in all_cells:
        u, v, left, right = cell
        label = int(matrices[numerical.EDGE_INDEX[u, v], left, right])
        labels_by_key.setdefault(independent_cell_key(cell), set()).add(label)
    require(
        all(len(labels) == 1 for labels in labels_by_key.values()),
        "all(len(labels) == 1 for labels in labels_by_key.values())",
    )
    require(
        len({next(iter(labels)) for labels in labels_by_key.values()}) == 84,
        "len({next(iter(labels)) for labels in labels_by_key.value...",
    )
    return orbit_by_key


def audit_colourings_and_covariance():
    all_colourings = tuple(product(range(Q), repeat=N))
    reps = tuple(
        colouring for colouring in all_colourings
        if colouring == min(independent_colouring_orbit(colouring))
    )
    require(
        len(all_colourings) == 6561,
        "len(all_colourings) == 6561",
    )
    require(
        len(reps) == 2187,
        "len(reps) == 2187",
    )
    require(
        all(len(independent_colouring_orbit(c)) == 3 for c in reps),
        "all(len(independent_colouring_orbit(c)) == 3 for c in reps)",
    )
    require(
        set().union(*(independent_colouring_orbit(c) for c in reps)) == set(all_colourings),
        "set().union(*(independent_colouring_orbit(c) for c in rep...",
    )
    require(
        reps == exact.COLOURING_REPS,
        "reps == exact.COLOURING_REPS",
    )
    for colouring in all_colourings:
        require(
            exact.transform_colouring(colouring) == independent_colouring_step(colouring),
            "exact.transform_colouring(colouring) == independent_colou...",
        )
        transformed = independent_colouring_step(colouring)
        require(
            (len(set(colouring)) == 1) == (len(set(transformed)) == 1),
            "(len(set(colouring)) == 1) == (len(set(transformed)) == 1)",
        )

        # Matching-by-matching covariance is stronger than merely comparing
        # the final coefficient sums: g(M) has exactly the same cell-orbit
        # monomial at the transformed colouring.
        for matching in MATCHINGS:
            transformed_matching = matching_image(matching, G)
            require(
                transformed_matching in MATCHING_SET,
                "transformed_matching in MATCHING_SET",
            )
            require(
                monomial(colouring, matching) == monomial(
                    transformed, transformed_matching
                ),
                "monomial(colouring, matching) == monomial( transformed, t...",
            )

    # Independently collect the 105 matching monomials modulo 3 and compare
    # every representative equation used by the SAT search.
    independent_index = {
        key: index for index, key in enumerate(sorted({
            independent_cell_key(cell)
            for cell in (
                (u, v, left, right)
                for u, v in combinations(VERTICES, 2)
                for left, right in product(range(Q), repeat=2)
            )
        }))
    }
    for index, colouring in enumerate(reps):
        counts = Counter(
            tuple(independent_index[cell] for cell in monomial(colouring, matching))
            for matching in MATCHINGS
        )
        reduced = tuple(sorted(
            (term, multiplicity % Q)
            for term, multiplicity in counts.items()
            if multiplicity % Q
        ))
        require(
            reduced == exact.REPRESENTATIVE_TERMS[index],
            "reduced == exact.REPRESENTATIVE_TERMS[index]",
        )
        require(
            exact.TARGETS[index] == (1 if len(set(colouring)) == 1 else 0),
            "exact.TARGETS[index] == (1 if len(set(colouring)) == 1 el...",
        )
    return reps


def audit_centralizer_and_branches(cell_orbits):
    centralizer = tuple(
        permutation
        for permutation in permutations(VERTICES)
        if all(permutation[G[v]] == G[permutation[v]] for v in VERTICES)
    )
    require(
        len(centralizer) == 36,
        "len(centralizer) == 36",
    )
    require(
        tuple(range(N)) in centralizer,
        "tuple(range(N)) in centralizer",
    )
    require(
        set(centralizer) == set(exact.CENTRALIZER),
        "set(centralizer) == set(exact.CENTRALIZER)",
    )

    # Every commuting relabeling gives a well-defined permutation of the 84
    # coupled cell orbits.  This is precisely why it may normalize a supported
    # pure matching without leaving the ansatz.
    for permutation in centralizer:
        orbit_image = {}
        for key, orbit in cell_orbits.items():
            images = {
                independent_cell_key(canonical_cell(
                    permutation[u], permutation[v], left, right
                ))
                for u, v, left, right in orbit
            }
            require(
                len(images) == 1,
                "len(images) == 1",
            )
            orbit_image[key] = next(iter(images))
        require(
            len(set(orbit_image.values())) == 84,
            "len(set(orbit_image.values())) == 84",
        )

    unseen = set(MATCHINGS)
    matching_orbits = []
    while unseen:
        representative = min(unseen)
        orbit = frozenset(
            matching_image(representative, permutation)
            for permutation in centralizer
        )
        require(
            orbit <= MATCHING_SET,
            "orbit <= MATCHING_SET",
        )
        matching_orbits.append(orbit)
        unseen -= orbit
    matching_orbits.sort(key=min)
    require(
        len(matching_orbits) == 7,
        "len(matching_orbits) == 7",
    )
    require(
        [len(orbit) for orbit in matching_orbits] == [9, 36, 18, 3, 18, 3, 18],
        "[len(orbit) for orbit in matching_orbits] == [9, 36, 18, ...",
    )
    require(
        tuple(min(orbit) for orbit in matching_orbits) == exact.PURE_MATCHING_REPS,
        "tuple(min(orbit) for orbit in matching_orbits) == exact.P...",
    )
    require(
        set().union(*matching_orbits) == MATCHING_SET,
        "set().union(*matching_orbits) == MATCHING_SET",
    )
    require(
        sum(map(len, matching_orbits)) == len(MATCHINGS),
        "sum(map(len, matching_orbits)) == len(MATCHINGS)",
    )

    # Check that the four branch assumptions really refer to four distinct
    # pure-zero cell variables in every representative matching.
    for representative in exact.PURE_MATCHING_REPS:
        indices = {
            exact.CELL_TO_INDEX[(u, v, 0, 0)] for u, v in representative
        }
        require(
            len(indices) == 4,
            "len(indices) == 4",
        )
    residual_sizes = []
    for branch, matching in enumerate(exact.PURE_MATCHING_REPS):
        first_three = frozenset(matching[:3])
        last = matching[3]
        residual = tuple(
            permutation for permutation in centralizer
            if frozenset(
                canonical_matching(((permutation[u], permutation[v]),))[0]
                for u, v in matching[:3]
            ) == first_three
            and canonical_matching(
                ((permutation[last[0]], permutation[last[1]]),)
            )[0] == last
        )
        require(
            set(residual) == set(exact.RESIDUAL_RELABELINGS[branch]),
            "set(residual) == set(exact.RESIDUAL_RELABELINGS[branch])",
        )
        residual_sizes.append(len(residual))
    require(
        tuple(residual_sizes) == (4, 1, 1, 12, 1, 12, 1),
        "tuple(residual_sizes) == (4, 1, 1, 12, 1, 12, 1)",
    )
    return centralizer, matching_orbits


def audit_equivariant_gauge(cell_orbits):
    inverse = [None] * N
    for vertex, image in enumerate(G):
        inverse[image] = vertex
    inverse = tuple(inverse)

    def inverse_power(vertex, power):
        for _ in range(power):
            vertex = inverse[vertex]
        return vertex

    gauges = []
    for base_signs in product((1, 2), repeat=N):
        total = 1
        for sign in base_signs:
            total = total * sign % Q
        if total != 1:
            continue
        signs = tuple(
            tuple(base_signs[inverse_power(vertex, colour)]
                  for colour in range(Q))
            for vertex in VERTICES
        )
        # This relation is exactly what keeps the edge multiplier constant on
        # each coupled cell orbit.
        require(
            all(
                signs[G[vertex]][(colour + 1) % Q] == signs[vertex][colour]
                for vertex in VERTICES for colour in range(Q)
            ),
            "all( signs[G[vertex]][(colour + 1) % Q] == signs[vertex][...",
        )
        require(
            all(
                np.prod([signs[vertex][colour] for vertex in VERTICES]) % Q == 1
                for colour in range(Q)
            ),
            "all( np.prod([signs[vertex][colour] for vertex in VERTICE...",
        )
        for orbit in cell_orbits.values():
            multipliers = {
                signs[u][left] * signs[v][right] % Q
                for u, v, left, right in orbit
            }
            require(
                len(multipliers) == 1,
                "len(multipliers) == 1",
            )
        gauges.append(signs)
    require(
        len(gauges) == 128,
        "len(gauges) == 128",
    )

    # Explicitly realize the normalization used by each SAT branch for every
    # possible nonzero value pattern on its four supported entries.
    for matching in exact.PURE_MATCHING_REPS:
        for old_values in product((1, 2), repeat=4):
            base_signs = [1] * N
            for position, (u, v) in enumerate(matching[:3]):
                base_signs[u] = 1
                base_signs[v] = old_values[position]
            u, v = matching[3]
            partial_product = 1
            for sign in base_signs:
                partial_product = partial_product * sign % Q
            base_signs[u] = 1
            base_signs[v] = partial_product  # inverse equals itself in F_3^*.
            require(
                np.prod(base_signs) % Q == 1,
                "np.prod(base_signs) % Q == 1",
            )
            transformed = tuple(
                old_values[position] * base_signs[u] * base_signs[v] % Q
                for position, (u, v) in enumerate(matching)
            )
            require(
                transformed[:3] == (1, 1, 1),
                "transformed[:3] == (1, 1, 1)",
            )
            require(
                transformed[3] in (1, 2),
                "transformed[3] in (1, 2)",
            )
    return gauges


MATCHING_SET = set(MATCHINGS)


def main():
    require(
        len(MATCHINGS) == 105,
        "len(MATCHINGS) == 105",
    )
    require(
        set(MATCHINGS) == set(exact.MATCHINGS),
        "set(MATCHINGS) == set(exact.MATCHINGS)",
    )
    cell_orbits = audit_cells()
    reps = audit_colourings_and_covariance()
    centralizer, matching_orbits = audit_centralizer_and_branches(cell_orbits)
    gauges = audit_equivariant_gauge(cell_orbits)
    print(
        "PASS "
        f"cells=252 cell_orbits={len(cell_orbits)} orbit_size=3 "
        f"colourings=6561 colouring_orbits={len(reps)} matchings={len(MATCHINGS)} "
        f"centralizer={len(centralizer)} matching_orbits={len(matching_orbits)} "
        f"matching_orbit_sizes={[len(orbit) for orbit in matching_orbits]} "
        f"residual_groups={[len(group) for group in exact.RESIDUAL_RELABELINGS]} "
        f"equivariant_gauges={len(gauges)} "
        "numerical_partition=matched covariance=all_6561x105"
    )


if __name__ == "__main__":
    main()
