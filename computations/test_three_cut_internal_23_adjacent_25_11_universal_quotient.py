#!/usr/bin/env python3
"""Test the four universal quotient charts for A_25=E_00+E_11.

Retain only the x11 and x22 coordinate blocks of arbitrary A_23 together
with the moving A_25 E_11 block.  Every other A_23 coefficient is killed
termwise.  The effective stabilizer normalizes nonzero t, x11, and x22
independently, leaving four zero/nonzero charts for (x11,x22).

This is a discovery worker; a promoted theorem checker should independently
restate all structural assertions.
"""

from __future__ import annotations

import concurrent.futures
import shutil
import subprocess
import time

import explore_three_cut_internal_23_adjacent_25_11 as adjacent
import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations
import test_three_cut_internal_23_plane_support_component as worker


Q = full.Q
RETAINED_X = (4, 8)
ACTIVE = (1, 2)


def build_case(pattern):
    coefficients = {
        full.CELLS[bit]: Q(1)
        for offset, bit in enumerate(RETAINED_X)
        if pattern & (1 << offset)
    }
    killed = adjacent.quotient_killed(RETAINED_X, retain_t=True)
    blocks = adjacent.blocks_for(coefficients, Q(1))
    terms = adjacent.projected_terms(blocks, killed)
    normals = tuple(
        full.projected_cylinder_intersection((2, 3, 4, cut), blocks, killed)
        for cut in (0, 1, 5)
    )
    assert equations.same_span(normals[0], normals[1])
    assert equations.same_span(normals[0], normals[2])
    normal = normals[0]

    # Every omitted A_23 coefficient remains arbitrary.
    for bit in range(9):
        if bit in RETAINED_X:
            continue
        augmented = dict(coefficients)
        augmented[full.CELLS[bit]] = Q(1)
        augmented_blocks = adjacent.blocks_for(augmented, Q(1))
        assert adjacent.projected_terms(augmented_blocks, killed) == terms
        for cut in range(6):
            assert equations.same_span(
                full.projected_cylinder_columns(cut, augmented_blocks, killed),
                full.projected_cylinder_columns(cut, blocks, killed),
            )

    span = equations.cylinders.echelon(normal)
    for colour in ACTIVE:
        word = (colour,) * 6
        assert word not in killed
        assert not equations.cylinders.member({word: Q(1)}, span)
    hs = equations.cylinders.matching_tensor(full.SIX, blocks)
    assert equations.cylinders.member(full.project_vector(hs, killed), span)

    program, generators = worker.direct_program(terms, normal, ACTIVE, 0)
    return pattern, program, generators, len(normal)


def run_case(data):
    pattern, program, generators, normal_dimension = data
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required")
    started = time.monotonic()
    completed = subprocess.run(
        [singular, "-q"], input=program, text=True, capture_output=True,
        check=True, timeout=3600,
    )
    if completed.stderr.strip():
        raise AssertionError(completed.stderr)
    unit = worker.marker_values(completed.stdout, "UNIT", 1)[0]
    size = worker.marker_values(completed.stdout, "GBSIZE", 1)[0]
    return (
        pattern, generators, normal_dimension, unit, size,
        time.monotonic() - started,
    )


def main():
    adjacent.no_mixed_x_t_terms()
    adjacent.stabilizer_audit()
    jobs = [build_case(pattern) for pattern in range(4)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(run_case, jobs))
    for pattern, generators, normal_dimension, unit, size, seconds in results:
        print(
            "RESULT", f"pattern={pattern:02b}", f"N={normal_dimension}",
            f"generators={generators}", f"unit={unit}", f"gbsize={size}",
            f"seconds={seconds:.3f}",
        )


if __name__ == "__main__":
    main()
