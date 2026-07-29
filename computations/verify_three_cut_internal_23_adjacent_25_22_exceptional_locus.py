#!/usr/bin/env python3
"""Exact true-normal checks on the exceptional {x01,x11,x21} locus.

With x00=0, t normalized to one, and all other A23 entries zero, the
remaining three stabilizer characters are independent.  Their eight support
patterns therefore give exact torus representatives.  This script constructs
the unprojected four-cylinder normal for every representative and final cut,
then checks the literal two-colour shared-star ideal over characteristic zero.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import itertools
import shutil
import subprocess
import time

import sympy as sp

import explore_three_cut_internal_23_adjacent_25_11 as adjacent
import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations
import test_three_cut_internal_23_plane_support_component as worker


Q = full.Q
ACTIVE = (0, 1)
EXCEPTIONAL_BITS = (1, 4, 7)


def select_e22():
    adjacent.T_CELL = (2, 2)
    adjacent.T_BLOCK, adjacent.T_DETAILS = adjacent.variable_coordinate_block(
        adjacent.T_EDGE, adjacent.T_CELL
    )


def compact_slimgb(program):
    lines = program.replace("ideal G=std(I);", "ideal G=slimgb(I);").splitlines()
    ring = lines[0]
    names_text = ring.split(",(", 1)[1].rsplit("),dp;", 1)[0]
    names = names_text.split(",")
    ideal_index = next(
        index for index, line in enumerate(lines) if line.startswith("ideal I=")
    )
    generators = lines[ideal_index][len("ideal I="):-1].split(",")
    generators = list(dict.fromkeys(generators))
    body = ",".join(generators)
    used = [name for name in names if name in body]
    prefix = ring.split(",(", 1)[0]
    lines[0] = prefix + ",(" + ",".join(used) + "),dp;"
    lines[ideal_index] = "ideal I=" + body + ";"
    return "\n".join(lines) + "\n", len(generators), len(used)


def support_patterns():
    for mask in range(1 << len(EXCEPTIONAL_BITS)):
        yield tuple(
            bit for index, bit in enumerate(EXCEPTIONAL_BITS)
            if mask & (1 << index)
        )


def build_job(support, cut):
    coefficients = {full.CELLS[bit]: Q(1) for bit in support}
    blocks = adjacent.blocks_for(coefficients, Q(1))
    terms = equations.reconstruct_word_terms(blocks)
    normal = full.projected_cylinder_intersection((2, 3, 4, cut), blocks, set())
    span = equations.cylinders.echelon(normal)
    hs = equations.cylinders.matching_tensor(full.SIX, blocks)
    assert equations.cylinders.member(hs, span)
    assert all(
        not equations.cylinders.member({(colour,) * 6: Q(1)}, span)
        for colour in ACTIVE
    )
    expected_dimension = 2 if support and cut in (0, 1) else 1
    assert len(normal) == expected_dimension, (support, cut, len(normal))
    raw_program, _raw_generators = worker.direct_program(terms, normal, ACTIVE, 0)
    program, generators, variables = compact_slimgb(raw_program)
    return {
        "support": support,
        "cut": cut,
        "normal_dimension": len(normal),
        "generators": generators,
        "variables": variables,
        "program": program,
        "sha256": hashlib.sha256(program.encode()).hexdigest(),
    }


def marker(output, name):
    return worker.marker_values(output, name, 1)[0]


def run(job, timeout):
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required")
    started = time.monotonic()
    completed = subprocess.run(
        [singular, "-q"], input=job["program"], text=True,
        capture_output=True, check=True, timeout=timeout,
    )
    if completed.stderr.strip():
        raise AssertionError(completed.stderr)
    unit = marker(completed.stdout, "UNIT")
    size = marker(completed.stdout, "GBSIZE")
    if (unit, size) != (1, 1):
        raise AssertionError((job["support"], job["cut"], unit, size))
    return job, time.monotonic() - started


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--timeout", type=int, default=3600)
    parser.add_argument("--cut", choices=(0, 1, 5), type=int, action="append")
    args = parser.parse_args()
    select_e22()
    cuts = tuple(args.cut or (0, 1, 5))
    jobs = [
        build_job(support, cut)
        for support in support_patterns() for cut in cuts
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        results = list(executor.map(lambda job: run(job, args.timeout), jobs))
    for job, elapsed in results:
        print(
            "EXCEPTIONAL", "support=" + repr(tuple(
                full.CELL_NAMES[bit] for bit in job["support"]
            )), f'cut={job["cut"]}', f'N={job["normal_dimension"]}',
            f'variables={job["variables"]}', f'generators={job["generators"]}',
            f'sha256={job["sha256"]}', "unit=1", "gbsize=1",
            f"seconds={elapsed:.3f}",
        )


if __name__ == "__main__":
    main()
