#!/usr/bin/env python3
"""Shared-star unit ideals for the rank-one slice A25 = E00 + t*E10 + s*E20.

Three characteristic-zero programs close the star systems on the two
normal shapes established by the slice W-structure certificates:

* the line packet over Q[x00..x22, t, s], split into the x00-invertible
  (Rabinowitsch) and x00 = 0 cases purely to bound Groebner time;
* the plane packet over the degenerate-locus parameters
  (a0, a1, a2, w1, w2, t, s) with scalar families for H and D.

A unit Groebner basis over Q[parameters, scalars, stars] specializes to
every complex parameter point, covering the whole rank-one family
A25 = (e0 + t e1 + s e2) (x) e0 including t = s = 0 and every special
complex cancellation, with no torus normalization.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib

import sympy as sp

import derive_three_cut_internal_23_adjacent_25_rank_one_slice_w_structure as swstruct
import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations
import test_three_cut_internal_23_adjacent_25_rank_one_star_ideals as ideals


T = swstruct.T
S = swstruct.S
X9 = swstruct.X9


def h_basis(blocks):
    tensor = equations.cylinders.matching_tensor(full.SIX, blocks)
    return [{
        word: sp.expand(value) for word, value in tensor.items()
        if sp.expand(value) != 0
    }]


def line_jobs():
    jobs = []
    blocks = swstruct.slice_blocks()
    program, generators, variables, coordinates = ideals.build_program(
        blocks, [str(symbol) for symbol in X9] + ["t", "s", "yinv"],
        h_basis(blocks), ("1-yinv*x00",),
    )
    jobs.append({
        "name": "ts_line_x00_invertible",
        "program": program, "generators": generators,
        "variables": variables, "coordinates": coordinates,
    })
    blocks0 = equations.cylinders.aggregate()
    blocks0[2, 3] = {
        cell: X9[bit] for bit, cell in enumerate(full.CELLS) if bit != 0
    }
    block25 = dict(blocks0[2, 5])
    block25[1, 0] = block25.get((1, 0), sp.Integer(0)) + T
    block25[2, 0] = block25.get((2, 0), sp.Integer(0)) + S
    blocks0[2, 5] = block25
    program, generators, variables, coordinates = ideals.build_program(
        blocks0, [str(symbol) for symbol in X9[1:]] + ["t", "s"],
        h_basis(blocks0),
    )
    jobs.append({
        "name": "ts_line_x00_zero",
        "program": program, "generators": generators,
        "variables": variables, "coordinates": coordinates,
    })
    return jobs


def plane_job():
    blocks = swstruct.locus_blocks()
    program, generators, variables, coordinates = ideals.build_program(
        blocks, ["a0", "a1", "a2", "w1", "w2", "t", "s"],
        h_basis(blocks) + [swstruct.d_plane_tensor()],
    )
    return {
        "name": "ts_plane_locus",
        "program": program, "generators": generators,
        "variables": variables, "coordinates": coordinates,
    }


def all_jobs():
    jobs = line_jobs() + [plane_job()]
    for job in jobs:
        job["sha256"] = hashlib.sha256(job["program"].encode()).hexdigest()
    return jobs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=28800)
    arguments = parser.parse_args()
    jobs = all_jobs()
    for job in jobs:
        print(
            "JOB", job["name"], f'generators={job["generators"]}',
            f'variables={job["variables"]}',
            f'coordinates={job["coordinates"]}',
            f'sha256={job["sha256"]}', flush=True,
        )
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=arguments.workers
    ) as executor:
        elapsed = list(executor.map(
            lambda job: ideals.run_job(job, arguments.timeout), jobs,
        ))
    for job, seconds in zip(jobs, elapsed):
        print("RESULT", job["name"], "unit=1 gbsize=1",
              f"seconds={seconds:.3f}", flush=True)


if __name__ == "__main__":
    main()
