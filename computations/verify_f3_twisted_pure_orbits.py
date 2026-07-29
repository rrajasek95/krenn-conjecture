#!/usr/bin/env python3
"""Exact gauge audit for the colour-swap-twisted n=8 search over F_3.

The default run is solver-free.  It independently verifies the 36 scalar
normalization branches, classifies the source gauges which can change the
distinguished pure row, and reduces the branch list to 11 representatives.
Optional SAT calls use the production formula and directly enumerate all
3^8 colourings before accepting any SAT model.
"""

from __future__ import annotations

import argparse
from functools import reduce
from itertools import permutations, product
from operator import mul

from pysat.solvers import Solver

from search_f3_translation_invariant_n8 import (
    COLOUR_SWAP,
    MATCHINGS,
    N,
    Q,
    TWISTED_PURE_ORBIT_REPS,
    build_formula,
    decode,
    verify,
)


EXPECTED_BASE_ORBIT_SIZES = (
    8, 6, 24, 24, 12, 12, 6, 6, 24, 24, 24, 24,
    48, 48, 24, 48, 24, 48, 24, 24, 8, 8, 24, 24,
    24, 24, 24, 48, 48, 24, 24, 12, 48, 12, 24, 24,
)
EXPECTED_GAUGE_CLASSES = (
    frozenset((0,)),
    frozenset((1,)),
    frozenset((2, 3)),
    frozenset((4, 5)),
    frozenset((6, 7)),
    frozenset(range(8, 14)),
    frozenset(range(14, 20)),
    frozenset(range(20, 24)),
    frozenset(range(24, 30)),
    frozenset((30, 32, 34)),
    frozenset((31, 33, 35)),
)
MINIMAL_BRANCHES = (0, 1, 2, 4, 6, 8, 14, 20, 24, 30, 31)
IDENTITY = (1, 2, 3, 4, 5, 6, 7)

# For each source orbit: (global sign, character, images of 1,...,7).
# The transformation maps that representative exactly to its class base.
WITNESSES_TO_BASE = {
    0: (0, 0, IDENTITY),
    1: (0, 0, IDENTITY),
    2: (0, 0, IDENTITY),
    3: (0, 1, IDENTITY),
    4: (0, 0, IDENTITY),
    5: (0, 2, IDENTITY),
    6: (0, 0, IDENTITY),
    7: (0, 2, IDENTITY),
    8: (0, 0, IDENTITY),
    9: (0, 7, IDENTITY),
    10: (1, 1, IDENTITY),
    11: (1, 6, IDENTITY),
    12: (1, 2, IDENTITY),
    13: (1, 5, IDENTITY),
    14: (0, 0, IDENTITY),
    15: (1, 5, IDENTITY),
    16: (0, 3, IDENTITY),
    17: (1, 6, IDENTITY),
    18: (1, 6, (1, 2, 3, 6, 7, 4, 5)),
    19: (1, 1, IDENTITY),
    20: (0, 0, IDENTITY),
    21: (0, 1, IDENTITY),
    22: (1, 7, IDENTITY),
    23: (1, 6, IDENTITY),
    24: (0, 0, IDENTITY),
    25: (1, 6, IDENTITY),
    26: (0, 1, (1, 4, 5, 6, 7, 2, 3)),
    27: (1, 7, (1, 4, 5, 6, 7, 2, 3)),
    28: (1, 6, (1, 2, 3, 6, 7, 4, 5)),
    29: (0, 5, (1, 4, 5, 6, 7, 2, 3)),
    30: (0, 0, IDENTITY),
    31: (0, 0, IDENTITY),
    32: (0, 2, (5, 2, 7, 4, 1, 6, 3)),
    33: (0, 4, (1, 2, 3, 6, 7, 4, 5)),
    34: (0, 4, (1, 2, 3, 6, 7, 4, 5)),
    35: (0, 2, IDENTITY),
}


def dot(left, right):
    return (left & right).bit_count() & 1


def apply_linear(nonzero_images, vector):
    if vector == 0:
        return 0
    return nonzero_images[vector - 1]


def all_linear_maps():
    maps = []
    for basis_images in permutations(range(1, N), 3):
        images = []
        for vector in range(1, N):
            image = 0
            for bit, basis_image in enumerate(basis_images):
                if vector & (1 << bit):
                    image ^= basis_image
            images.append(image)
        if len(set(images)) == N - 1:
            maps.append(tuple(images))
    assert len(maps) == 168
    assert len(set(maps)) == 168
    return tuple(maps)


def twist_stabilizer(maps):
    stabilizer = tuple(
        linear_map for linear_map in maps
        if all(
            (apply_linear(linear_map, vector) & 1) == (vector & 1)
            for vector in range(N)
        )
    )
    assert len(stabilizer) == 24
    return stabilizer


def transform(row, global_sign, character, nonzero_images):
    """Return T_(e,h,M)(row)_d=(-1)^(e+h.Md) row_(Md)."""

    answer = []
    for difference in range(1, N):
        image = apply_linear(nonzero_images, difference)
        sign = 2 if global_sign ^ dot(character, image) else 1
        answer.append(sign * row[image - 1] % 3)
    return tuple(answer)


def scalar_hafnian(row):
    total = 0
    for matching in MATCHINGS:
        term = reduce(
            mul,
            (row[(left ^ right) - 1] for left, right in matching),
            1,
        )
        total = (total + term) % 3
    return total


def verify_scalar_normalization(stabilizer):
    solutions = {
        row
        for row in product(range(3), repeat=N - 1)
        if scalar_hafnian(row) == 1
    }
    assert len(solutions) == 882

    base_orbits = []
    for representative in TWISTED_PURE_ORBIT_REPS:
        orbit = {
            transform(representative, global_sign, 0, linear_map)
            for global_sign in range(2)
            for linear_map in stabilizer
        }
        assert orbit <= solutions
        base_orbits.append(orbit)
    assert tuple(map(len, base_orbits)) == EXPECTED_BASE_ORBIT_SIZES
    assert sum(map(len, base_orbits)) == len(solutions)
    assert set().union(*base_orbits) == solutions
    for left in range(len(base_orbits)):
        for right in range(left):
            assert base_orbits[left].isdisjoint(base_orbits[right])
    return solutions, base_orbits


def matching_difference_mask(matching):
    mask = 0
    for left, right in matching:
        mask ^= 1 << ((left ^ right) - 1)
    return mask


def gf2_rank(rows):
    pivots = {}
    for original in rows:
        row = original
        while row:
            pivot = row.bit_length() - 1
            if pivot in pivots:
                row ^= pivots[pivot]
            else:
                pivots[pivot] = row
                break
    return len(pivots)


def verify_difference_signs():
    matching_rows = {matching_difference_mask(m) for m in MATCHINGS}
    assert gf2_rank(matching_rows) == 3
    valid = {
        mask for mask in range(1 << (N - 1))
        if all((mask & row).bit_count() % 2 == 0
               for row in matching_rows)
    }
    affine = {
        sum(
            (global_sign ^ dot(character, difference)) << (difference - 1)
            for difference in range(1, N)
        )
        for global_sign in range(2)
        for character in range(N)
    }
    assert len(valid) == 16
    assert valid == affine
    return valid


def verify_augmented_orbits(stabilizer, solutions, base_orbits):
    augmented = []
    for representative in TWISTED_PURE_ORBIT_REPS:
        orbit = {
            transform(representative, global_sign, character, linear_map)
            for global_sign in range(2)
            for character in range(N)
            for linear_map in stabilizer
        }
        assert orbit <= solutions
        augmented.append(frozenset(orbit))

    observed = []
    unused = set(range(len(TWISTED_PURE_ORBIT_REPS)))
    while unused:
        first = min(unused)
        equivalent = frozenset(
            index for index in unused
            if augmented[index] == augmented[first]
        )
        observed.append(equivalent)
        unused -= equivalent
    assert tuple(observed) == EXPECTED_GAUGE_CLASSES
    for gauge_class in observed:
        union = set().union(*(base_orbits[index] for index in gauge_class))
        assert union == set(augmented[min(gauge_class)])
    assert set().union(
        *(set(augmented[min(gauge_class)]) for gauge_class in observed)
    ) == solutions

    class_base = {
        index: min(gauge_class)
        for gauge_class in EXPECTED_GAUGE_CLASSES
        for index in gauge_class
    }
    assert tuple(sorted(set(class_base.values()))) == MINIMAL_BRANCHES
    for source, witness in WITNESSES_TO_BASE.items():
        global_sign, character, linear_map = witness
        assert linear_map in stabilizer
        assert transform(
            TWISTED_PURE_ORBIT_REPS[source],
            global_sign,
            character,
            linear_map,
        ) == TWISTED_PURE_ORBIT_REPS[class_base[source]]


def difference_map(vertex_permutation):
    images = []
    for difference in range(1, N):
        possible = {
            vertex_permutation[vertex]
            ^ vertex_permutation[vertex ^ difference]
            for vertex in range(N)
        }
        if len(possible) != 1:
            return None
        images.append(possible.pop())
    return tuple(images)


def verify_vertex_and_colour_normalizer(all_maps, stabilizer):
    affine = []
    twisted_affine = []
    for vertex_permutation in permutations(range(N)):
        linear_part = difference_map(vertex_permutation)
        if linear_part is None:
            continue
        affine.append(vertex_permutation)
        assert linear_part in all_maps
        if linear_part in stabilizer:
            twisted_affine.append(vertex_permutation)
    assert len(affine) == N * len(all_maps) == 1344
    assert len(twisted_affine) == N * len(stabilizer) == 192

    colour_centralizer = tuple(
        colour_permutation
        for colour_permutation in permutations(range(Q))
        if all(
            colour_permutation[COLOUR_SWAP[colour]]
            == COLOUR_SWAP[colour_permutation[colour]]
            for colour in range(Q)
        )
    )
    assert len(colour_centralizer) == 2

    # Check that no non-stabilizing linear map can be rescued by a common
    # colour permutation: conjugated twist actions must agree for every d.
    compatible_pairs = []
    for linear_map in all_maps:
        for colour_permutation in permutations(range(Q)):
            inverse = tuple(colour_permutation.index(c) for c in range(Q))
            compatible = True
            for difference in range(1, N):
                image = apply_linear(linear_map, difference)
                for colour in range(Q):
                    old = inverse[colour]
                    if difference & 1:
                        old = COLOUR_SWAP[old]
                    conjugated = colour_permutation[old]
                    expected = (
                        COLOUR_SWAP[colour] if image & 1 else colour
                    )
                    if conjugated != expected:
                        compatible = False
            if compatible:
                compatible_pairs.append((linear_map, colour_permutation))
    assert len(compatible_pairs) == len(stabilizer) * 2 == 48
    assert all(
        linear_map in stabilizer
        and colour_permutation in colour_centralizer
        for linear_map, colour_permutation in compatible_pairs
    )
    return len(twisted_affine), len(colour_centralizer)


def twisted_colour(shift, colour):
    return COLOUR_SWAP[colour] if shift & 1 else colour


def gauge_index(vertex, colour):
    return Q * vertex + colour


def verify_local_diagonal_gauges():
    # Let x_(u,c) be the exponent of a local sign.  Twisted equivariance for
    # every arbitrary source entry gives the following homogeneous equations.
    constraints = set()
    for shift in range(N):
        for left_vertex in range(N):
            for right_vertex in range(left_vertex + 1, N):
                for left_colour in range(Q):
                    for right_colour in range(Q):
                        row = 0
                        positions = (
                            (left_vertex ^ shift,
                             twisted_colour(shift, left_colour)),
                            (left_vertex, left_colour),
                            (right_vertex ^ shift,
                             twisted_colour(shift, right_colour)),
                            (right_vertex, right_colour),
                        )
                        for vertex, colour in positions:
                            row ^= 1 << gauge_index(vertex, colour)
                        if row:
                            constraints.add(row)
    assert len(constraints) == 378
    assert gf2_rank(constraints) == N * Q - 6 == 18

    candidates = set()
    for character in range(N):
        for base_colour_signs in range(1 << Q):
            mask = 0
            for vertex in range(N):
                for colour in range(Q):
                    base_colour = twisted_colour(vertex, colour)
                    exponent = (
                        dot(character, vertex)
                        ^ ((base_colour_signs >> base_colour) & 1)
                    )
                    mask |= exponent << gauge_index(vertex, colour)
            candidates.add(mask)
    assert len(candidates) == 64
    assert all(
        all((candidate & row).bit_count() % 2 == 0
            for row in constraints)
        for candidate in candidates
    )

    # Nullity six and 64 distinct candidates prove that this is the full
    # local diagonal gauge space.  Every candidate fixes all three pure
    # target coefficients, and its pure-colour-0 row effect is a character.
    pure_row_effects = set()
    for candidate in candidates:
        for colour in range(Q):
            exponent = sum(
                (candidate >> gauge_index(vertex, colour)) & 1
                for vertex in range(N)
            ) & 1
            assert exponent == 0
        effect = 0
        for difference in range(1, N):
            exponent = (
                ((candidate >> gauge_index(0, 0)) & 1)
                ^ ((candidate >> gauge_index(difference, 0)) & 1)
            )
            effect |= exponent << (difference - 1)
        pure_row_effects.add(effect)
    character_effects = {
        sum(
            dot(character, difference) << (difference - 1)
            for difference in range(1, N)
        )
        for character in range(N)
    }
    assert pure_row_effects == character_effects
    return len(candidates)


def solve_orbit(orbit, solver_name, phase):
    pool, clauses, values, representatives = build_formula(orbit, True)
    print(
        f"solve twisted_orbit={orbit} variables={pool.top} "
        f"clauses={len(clauses)} colouring_orbits={len(representatives)} "
        f"solver={solver_name}",
        flush=True,
    )
    with Solver(name=solver_name, bootstrap_with=clauses) as solver:
        if phase != "none":
            phase_literals = []
            for zero, one, two in values.values():
                if phase == "sparse":
                    phase_literals.extend((zero, -one, -two))
                else:
                    phase_literals.extend((-zero, one, -two))
            solver.set_phases(phase_literals)
        satisfiable = solver.solve()
        print(f"twisted_orbit={orbit} SAT={satisfiable}", flush=True)
        if satisfiable:
            entries = decode(solver.get_model(), values)
            verify(entries, True)
            print(
                f"twisted_orbit={orbit} direct all-colouring F3 "
                "verification: PASS",
                flush=True,
            )
    return satisfiable


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solve-orbit", type=int, action="append", default=[])
    parser.add_argument("--solve-bases", action="store_true")
    parser.add_argument("--solver", default="cadical300")
    parser.add_argument(
        "--phase", choices=("none", "sparse", "dense"), default="sparse"
    )
    args = parser.parse_args()

    maps = all_linear_maps()
    stabilizer = twist_stabilizer(maps)
    solutions, base_orbits = verify_scalar_normalization(stabilizer)
    difference_signs = verify_difference_signs()
    verify_augmented_orbits(stabilizer, solutions, base_orbits)
    affine_normalizer, colour_centralizer = (
        verify_vertex_and_colour_normalizer(maps, stabilizer)
    )
    diagonal_gauges = verify_local_diagonal_gauges()
    print(
        "PASS scalar_solutions=882 base_orbits=36 gauge_classes=11 "
        f"difference_signs={len(difference_signs)} "
        f"affine_normalizer={affine_normalizer} "
        f"colour_centralizer={colour_centralizer} "
        f"diagonal_gauges={diagonal_gauges} minimal_branches=11",
        flush=True,
    )

    requested = list(args.solve_orbit)
    if args.solve_bases:
        requested.extend(MINIMAL_BRANCHES)
    for orbit in dict.fromkeys(requested):
        if not 0 <= orbit < len(TWISTED_PURE_ORBIT_REPS):
            parser.error(f"orbit {orbit} is outside range(0, 36)")
        solve_orbit(orbit, args.solver, args.phase)


if __name__ == "__main__":
    main()
