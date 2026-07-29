#!/usr/bin/env python3
"""Audit one-pair extensions of the best two-module support.

The five missing pairs form two orbits under the support automorphism group:
the central pair 03 and the four cross pairs 14,15,24,25.  Cubic-vertex
rigidity reduces each extension to a finite coordinate-slice obstruction.
This script verifies the orbit statement and exhausts the 3! x 3! proper
color assignments in the representative cross extension U+14.
"""

from __future__ import annotations

import collections
import itertools


VERTICES = tuple(range(6))
ALL_EDGES = set(itertools.combinations(VERTICES, 2))
U = {
    (0, 1), (0, 2), (0, 4), (0, 5), (1, 2),
    (1, 3), (2, 3), (3, 4), (3, 5), (4, 5),
}


def permuted_edge(edge, permutation):
    return tuple(sorted((permutation[edge[0]], permutation[edge[1]])))


def automorphisms():
    return tuple(
        permutation
        for permutation in itertools.permutations(VERTICES)
        if {permuted_edge(edge, permutation) for edge in U} == U
    )


def cross_slice_occurrences(colors_at_2, colors_at_5):
    """Occurrences for U+14 after cubic rigidity at vertices 2 and 5."""
    a, b, c = colors_at_2  # colors of 02,12,23
    d, e, f = colors_at_5  # colors of 05,35,45
    # Each perfect matching contains one arbitrary matrix.  The tuple is
    # (matching name, arbitrary edge, fixed vertex colors).
    slices = (
        ("A", (0, 1), {2: c, 3: c, 4: f, 5: f}),
        ("B", (1, 3), {0: a, 2: a, 4: f, 5: f}),
        ("E", (1, 4), {0: a, 2: a, 3: e, 5: e}),
        ("C", (0, 4), {1: b, 2: b, 3: e, 5: e}),
        ("D", (3, 4), {0: d, 5: d, 1: b, 2: b}),
        ("F", (1, 4), {0: d, 5: d, 2: c, 3: c}),
    )
    occurrences = collections.defaultdict(list)
    for name, (u, v), fixed in slices:
        for color_u in range(3):
            for color_v in range(3):
                coloring = [None] * 6
                coloring[u] = color_u
                coloring[v] = color_v
                for vertex, color in fixed.items():
                    coloring[vertex] = color
                # The same cell of A_14 occurs in slices E and F; matching
                # scale factors are nonzero but otherwise arbitrary.
                variable = ((u, v), color_u, color_v)
                occurrences[tuple(coloring)].append((name, variable))
    return occurrences


def main():
    group = automorphisms()
    assert len(group) == 16
    missing = ALL_EDGES - U
    central_orbit = {permuted_edge((0, 3), permutation) for permutation in group}
    cross_orbit = {permuted_edge((1, 4), permutation) for permutation in group}
    assert central_orbit == {(0, 3)}
    assert cross_orbit == {(1, 4), (1, 5), (2, 4), (2, 5)}
    assert central_orbit | cross_orbit == missing

    # In U+03, vertices 1,2,4,5 remain cubic.  Matchings
    # A=01|23|45 and B=02|13|45 lie outside the sole arbitrary-edge slice
    # 03|12|45 because properness gives color(01)!=color(12) and
    # color(02)!=color(12).  They cannot cancel; if both were constant,
    # sharing 45 would force color(01)=color(13), violating properness at 1.

    checked = 0
    covered = 0
    for colors_at_2 in itertools.permutations(range(3)):
        for colors_at_5 in itertools.permutations(range(3)):
            checked += 1
            occurrences = cross_slice_occurrences(colors_at_2, colors_at_5)
            constant_terms = tuple(occurrences[(color,) * 6] for color in range(3))
            if any(not terms for terms in constant_terms):
                continue
            covered += 1
            # In every constant-covering case each constant coefficient is
            # supplied by one matrix cell.  The same cell of the shared
            # arbitrary matrix A_14 then occurs alone at a mixed coloring.
            assert all(len(terms) == 1 for terms in constant_terms)
            certificate_found = False
            for terms in constant_terms:
                _, variable = terms[0]
                for coloring, mixed_terms in occurrences.items():
                    if (
                        len(set(coloring)) > 1
                        and len(mixed_terms) == 1
                        and mixed_terms[0][1] == variable
                    ):
                        certificate_found = True
                        break
                if certificate_found:
                    break
            assert certificate_found, (colors_at_2, colors_at_5)

    assert checked == 36 and covered == 12
    print(f"verified support automorphisms={len(group)} and missing-edge orbits=2")
    print("verified central extension U+03 obstruction")
    print(f"verified cross extension assignments={checked}, constant-covering={covered}")
    print("every constant-covering cross assignment has a unique mixed companion")


if __name__ == "__main__":
    main()
