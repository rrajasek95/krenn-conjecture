#!/usr/bin/env python3
"""Discovery test for the old five-cell A_23 locus with moving A_25.

The five previously audited support classes are rebuilt with
A_25=E_00+E_11.  Its moving coordinate block is retained.  Optional A_23
cells are killed termwise exactly as in the old interval quotients.
"""

from __future__ import annotations

import concurrent.futures
import itertools
import shutil
import subprocess
import time

import explore_three_cut_internal_23_adjacent_25_11 as adjacent
import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations
import test_three_cut_internal_23_plane_support_component as worker
import verify_three_cut_internal_23_plane_support_fourth_cut_obstruction as old


Q = full.Q
LOCAL_TO_FULL = (0, 1, 2, 4, 7)


def full_bits(local_mask):
    return tuple(
        LOCAL_TO_FULL[bit] for bit in range(5) if local_mask & (1 << bit)
    )


def blocks_for_local_mask(mask):
    return adjacent.blocks_for(
        {full.CELLS[bit]: Q(1) for bit in full_bits(mask)}, Q(1)
    )


def killed_for_spec(maximal, retained_local):
    maximal_full = set(full_bits(maximal))
    retained_full = {LOCAL_TO_FULL[bit] for bit in retained_local}
    retained_union = set(adjacent.T_BLOCK)
    retained_union.update(*(
        adjacent.X_BLOCKS[bit] for bit in retained_full
    ))
    killed = set(full.UPLUS) - retained_union
    for bit in maximal_full - retained_full:
        killed.update(adjacent.X_BLOCKS[bit])
    return killed


def build_case(spec):
    (
        name, maximal, retained_local, colours,
        _old_killed, _old_words, _old_atoms, _old_normal, _old_generators,
    ) = spec
    retained_full = tuple(LOCAL_TO_FULL[bit] for bit in retained_local)
    representative = 0
    for bit in retained_local:
        representative |= 1 << bit
    killed = killed_for_spec(maximal, retained_local)
    blocks = blocks_for_local_mask(representative)
    terms = adjacent.projected_terms(blocks, killed)
    normals = tuple(
        full.projected_cylinder_intersection((2, 3, 4, cut), blocks, killed)
        for cut in (0, 1, 5)
    )
    safe_normal = list(equations.cylinders.echelon(
        [vector for normal in normals for vector in normal]
    ).values())

    members = [
        mask for mask in range(32)
        if old.class_name(mask) == name
    ]
    for mask in members:
        assert mask & maximal == mask
        assert all(mask & (1 << bit) for bit in retained_local)
        actual_blocks = blocks_for_local_mask(mask)
        assert adjacent.projected_terms(actual_blocks, killed) == terms
        for cut_index, cut in enumerate((0, 1, 5)):
            actual_normal = full.projected_cylinder_intersection(
                (2, 3, 4, cut), actual_blocks, killed
            )
            assert equations.same_span(actual_normal, normals[cut_index])

    span = equations.cylinders.echelon(safe_normal)
    for colour in colours:
        word = (colour,) * 6
        assert word not in killed
        assert not equations.cylinders.member({word: Q(1)}, span)
    hs = equations.cylinders.matching_tensor(full.SIX, blocks)
    assert equations.cylinders.member(full.project_vector(hs, killed), span)
    program, generators = worker.direct_program(terms, safe_normal, colours, 0)
    return (
        name, program, generators, tuple(len(normal) for normal in normals),
        len(safe_normal), len(killed), len(terms), len(members), retained_full,
    )


def run_case(data):
    (
        name, program, generators, cut_dimensions, safe_dimension,
        killed, words, members, retained_full,
    ) = data
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
        name, generators, cut_dimensions, safe_dimension, killed, words,
        members, retained_full,
        worker.marker_values(completed.stdout, "UNIT", 1)[0],
        worker.marker_values(completed.stdout, "GBSIZE", 1)[0],
        time.monotonic() - started,
    )


def main():
    adjacent.no_mixed_x_t_terms()
    adjacent.stabilizer_audit()
    jobs = [build_case(spec) for spec in old.CLASS_SPECS]
    assert sum(data[7] for data in jobs) == 32
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(run_case, jobs))
    for result in results:
        (
            name, generators, cut_dimensions, safe_dimension, killed, words,
            members, retained_full, unit, size, seconds,
        ) = result
        print(
            "RESULT", name, f"members={members}", f"retained={retained_full}",
            f"cuts={cut_dimensions}", f"N={safe_dimension}",
            f"killed={killed}", f"words={words}", f"generators={generators}",
            f"unit={unit}", f"gbsize={size}", f"seconds={seconds:.3f}",
        )


if __name__ == "__main__":
    main()
