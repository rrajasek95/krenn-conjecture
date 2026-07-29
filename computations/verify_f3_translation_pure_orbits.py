#!/usr/bin/env python3
"""Exact audit of the ordinary translation-invariant F_3 pure branches.

The production search fixes the colour-0 diagonal to one of 18 GL(3,2)
orbits.  This checker independently enumerates those scalar orbits and then
uses two coefficient-preserving gauges to collapse the 18 branches to four.

The default audit is solver-free.  Pass ``--solve-orbit I`` (repeated if
desired) to regenerate and solve any of the production CNFs as an additional
SAT-solver check.
"""

from __future__ import annotations

import argparse
from functools import reduce
from itertools import permutations, product
from operator import mul

from pysat.solvers import Solver

from search_f3_translation_invariant_n8 import (
    MATCHINGS,
    N,
    PURE_ORBIT_REPS,
    build_formula,
    decode,
    verify,
)


EXPECTED_GL_ORBIT_SIZES = (
    7, 7, 21, 42, 21, 28, 28, 84, 84,
    84, 84, 28, 28, 42, 84, 84, 84, 42,
)
EXPECTED_GAUGE_CLASSES = (
    frozenset((0, 1)),
    frozenset((2, 3, 4)),
    frozenset(range(5, 13)),
    frozenset(range(13, 18)),
)
BASE_UNSAT_ORBITS = (0, 2, 5, 13)

# A witness maps the listed source representative exactly to its class base.
# It is (global sign bit, character h, images of differences 1,...,7).
IDENTITY = (1, 2, 3, 4, 5, 6, 7)
WITNESSES_TO_BASE = {
    0: (0, 0, IDENTITY),
    1: (0, 1, IDENTITY),
    2: (0, 0, IDENTITY),
    3: (0, 1, IDENTITY),
    4: (0, 2, IDENTITY),
    5: (0, 0, IDENTITY),
    6: (0, 7, IDENTITY),
    7: (1, 1, IDENTITY),
    8: (1, 6, IDENTITY),
    9: (0, 3, IDENTITY),
    10: (0, 4, IDENTITY),
    11: (1, 7, IDENTITY),
    12: (1, 0, IDENTITY),
    13: (0, 0, IDENTITY),
    14: (0, 1, (1, 4, 5, 6, 7, 2, 3)),
    15: (0, 4, (1, 2, 3, 7, 6, 5, 4)),
    16: (0, 1, (1, 2, 3, 5, 4, 7, 6)),
    17: (0, 4, (1, 4, 5, 6, 7, 2, 3)),
}


def apply_linear(nonzero_images, vector):
    """Apply a binary linear map encoded by its images on 1,...,7."""

    if vector == 0:
        return 0
    return nonzero_images[vector - 1]


def linear_maps():
    """Enumerate all 168 elements of GL(3,2), as images of 1,...,7."""

    answer = []
    for basis_images in permutations(range(1, N), 3):
        images = []
        for vector in range(1, N):
            image = 0
            for bit, basis_image in enumerate(basis_images):
                if vector & (1 << bit):
                    image ^= basis_image
            images.append(image)
        if len(set(images)) == N - 1:
            answer.append(tuple(images))
    assert len(answer) == 168
    assert len(set(answer)) == 168
    return tuple(answer)


def dot(left, right):
    return (left & right).bit_count() & 1


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


def verify_scalar_orbits(maps):
    solutions = {
        row
        for row in product(range(3), repeat=N - 1)
        if scalar_hafnian(row) == 1
    }
    assert len(solutions) == 882

    gl_orbits = []
    for representative in PURE_ORBIT_REPS:
        orbit = {
            transform(representative, 0, 0, linear_map)
            for linear_map in maps
        }
        assert orbit <= solutions
        gl_orbits.append(orbit)
    assert tuple(map(len, gl_orbits)) == EXPECTED_GL_ORBIT_SIZES
    assert sum(map(len, gl_orbits)) == len(solutions)
    assert set().union(*gl_orbits) == solutions
    for left in range(len(gl_orbits)):
        for right in range(left):
            assert gl_orbits[left].isdisjoint(gl_orbits[right])
    return solutions


def verify_gauge(maps, scalar_solutions):
    # Every combined sign gauge has factor one on every perfect matching.
    matching_checks = 0
    matching_set = {tuple(sorted(matching)) for matching in MATCHINGS}
    for linear_map in maps:
        mapped_matchings = {
            tuple(sorted(
                tuple(sorted((
                    apply_linear(linear_map, left),
                    apply_linear(linear_map, right),
                )))
                for left, right in matching
            ))
            for matching in MATCHINGS
        }
        assert mapped_matchings == matching_set
        for global_sign in range(2):
            for character in range(N):
                for matching in MATCHINGS:
                    factor = 1
                    for left, right in matching:
                        difference = apply_linear(
                            linear_map, left ^ right
                        )
                        if global_sign ^ dot(character, difference):
                            factor = -factor
                    assert factor == 1
                    matching_checks += 1
    assert matching_checks == 168 * 2 * N * len(MATCHINGS)

    augmented_orbits = []
    for representative in PURE_ORBIT_REPS:
        orbit = {
            transform(representative, global_sign, character, linear_map)
            for global_sign in range(2)
            for character in range(N)
            for linear_map in maps
        }
        assert orbit <= scalar_solutions
        augmented_orbits.append(frozenset(orbit))

    observed_classes = []
    unused = set(range(len(PURE_ORBIT_REPS)))
    while unused:
        first = min(unused)
        equivalent = frozenset(
            index for index in unused
            if augmented_orbits[index] == augmented_orbits[first]
        )
        observed_classes.append(equivalent)
        unused -= equivalent
    assert tuple(observed_classes) == EXPECTED_GAUGE_CLASSES
    assert set().union(*(set(augmented_orbits[min(cls)])
                         for cls in observed_classes)) == scalar_solutions

    for source, witness in WITNESSES_TO_BASE.items():
        target = next(
            base for base in BASE_UNSAT_ORBITS
            if source in next(cls for cls in EXPECTED_GAUGE_CLASSES
                              if base in cls)
        )
        global_sign, character, linear_map = witness
        assert linear_map in maps
        assert transform(
            PURE_ORBIT_REPS[source],
            global_sign,
            character,
            linear_map,
        ) == PURE_ORBIT_REPS[target]
    return matching_checks


def solve_orbit(orbit, solver_name, phase):
    pool, clauses, values, representatives = build_formula(orbit, False)
    print(
        f"solve orbit={orbit} variables={pool.top} clauses={len(clauses)} "
        f"colouring_orbits={len(representatives)} solver={solver_name}",
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
        print(f"orbit={orbit} SAT={satisfiable}", flush=True)
        if satisfiable:
            entries = decode(solver.get_model(), values)
            verify(entries, False)
            print(
                f"orbit={orbit} direct all-colouring F3 verification: PASS",
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

    maps = linear_maps()
    scalar_solutions = verify_scalar_orbits(maps)
    matching_checks = verify_gauge(maps, scalar_solutions)
    print(
        "PASS scalar_solutions=882 gl_orbits=18 gauge_classes=4 "
        f"matching_gauge_checks={matching_checks} residual_branches=0",
        flush=True,
    )

    requested = list(args.solve_orbit)
    if args.solve_bases:
        requested.extend(BASE_UNSAT_ORBITS)
    for orbit in dict.fromkeys(requested):
        if not 0 <= orbit < len(PURE_ORBIT_REPS):
            parser.error(f"orbit {orbit} is outside range(0, 18)")
        satisfiable = solve_orbit(orbit, args.solver, args.phase)
        if satisfiable:
            raise AssertionError(
                f"orbit {orbit} is SAT despite the recorded UNSAT reduction"
            )


if __name__ == "__main__":
    main()
