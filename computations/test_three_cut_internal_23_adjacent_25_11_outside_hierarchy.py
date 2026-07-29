#!/usr/bin/env python3
"""Discovery test for the 27 finite outside-support charts with A_25 moving.

This reuses the first-outside-cell hierarchy for arbitrary A_23, retains the
A_25 E_11 coordinate block, and normalizes its nonzero coefficient to one.
The sole x12 rectangle cross-ratio is intentionally omitted here.
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
import verify_three_cut_internal_23_arbitrary_block_fourth_cut_obstruction as old


Q = full.Q
ACTIVE = (1, 2)


def build_case(name, spec, pattern, x21):
    coefficients = old.coefficients_for_case(spec, pattern, x21)
    blocks = adjacent.blocks_for(coefficients, Q(1))
    killed = adjacent.quotient_killed(spec["retained"], retain_t=True)
    terms = adjacent.projected_terms(blocks, killed)
    normals = tuple(
        full.projected_cylinder_intersection((2, 3, 4, cut), blocks, killed)
        for cut in (0, 1, 5)
    )
    assert equations.same_span(normals[0], normals[1])
    assert equations.same_span(normals[0], normals[2])
    normal = normals[0]

    for bit in range(9):
        if bit in spec["retained"]:
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

    normal_span = equations.cylinders.echelon(normal)
    for colour in ACTIVE:
        word = (colour,) * 6
        assert word not in killed
        assert not equations.cylinders.member({word: Q(1)}, normal_span)
    hs = equations.cylinders.matching_tensor(full.SIX, blocks)
    assert equations.cylinders.member(
        full.project_vector(hs, killed), normal_span
    )
    program, generators = worker.direct_program(terms, normal, ACTIVE, 0)
    return f"{name}_d{pattern}_b{x21}", program, generators, len(normal)


def run_case(data):
    name, program, generators, normal_dimension = data
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
    return (
        name, generators, normal_dimension,
        worker.marker_values(completed.stdout, "UNIT", 1)[0],
        worker.marker_values(completed.stdout, "GBSIZE", 1)[0],
        time.monotonic() - started,
    )


def main():
    adjacent.no_mixed_x_t_terms()
    adjacent.stabilizer_audit()
    jobs = []
    for name, spec in old.FAMILIES.items():
        for pattern in spec["patterns"]:
            for x21 in spec["x21"]:
                if name == "x12" and pattern == 6 and x21:
                    continue
                jobs.append(build_case(name, spec, pattern, x21))
    assert len(jobs) == 27
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(run_case, jobs))
    for name, generators, normal_dimension, unit, size, seconds in results:
        print(
            "RESULT", name, f"N={normal_dimension}",
            f"generators={generators}", f"unit={unit}", f"gbsize={size}",
            f"seconds={seconds:.3f}",
        )


if __name__ == "__main__":
    main()
