#!/usr/bin/env python3
"""Shared-star unit ideals for the rank-one directions E10/E20.

Two characteristic-zero programs per direction close the star systems on
the two normal shapes established by the W-structure certificates:

* the line program keeps all nine A23 entries and t as polynomial
  variables and asks the two-colour packet to reach a multiple of the
  direct tensor H;
* the plane program works on the linear parameterization of the
  degenerate locus D_full and allows an arbitrary combination of H and
  the explicit plane tensor D.

A unit Groebner basis over Q[parameters, scalars, stars] specializes to
every complex parameter value, so each program covers its whole family,
including t = 0 and every special complex cancellation.  The line
program is optionally split into the x00-invertible and x00 = 0 cases
purely to bound Groebner running time; the two cases still cover every
complex point without any torus normalization.
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

import derive_three_cut_internal_23_adjacent_25_rank_one_w_structure as wstruct
import explore_three_cut_internal_23_adjacent_25_rank_one_directions as rankone
import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations


ACTIVE = (0, 1)
T = rankone.T
X9 = wstruct.X9


def singular_text(value):
    value = sp.cancel(value)
    if value == 0:
        return "0"
    return str(value).replace("**", "^")


def beta(word_terms, a, b, word):
    terms = []
    for (left, right), coefficient in word_terms.get(word, ()):
        factor = singular_text(coefficient)
        terms.append(
            f"({factor})*{equations.variable('p', a, left)}*"
            f"{equations.variable('q', b, right)}"
        )
        terms.append(
            f"({factor})*{equations.variable('p', a, right)}*"
            f"{equations.variable('q', b, left)}"
        )
    return "+".join(terms) if terms else "0"


def build_program(blocks, parameter_names, basis, extra_generators=()):
    hs = equations.cylinders.matching_tensor(full.SIX, blocks)
    hs = {
        word: sp.expand(value) for word, value in hs.items()
        if sp.expand(value) != 0
    }
    word_terms = equations.reconstruct_word_terms(blocks)
    coordinates = tuple(sorted(
        set(word_terms) | set(hs)
        | set().union(*(set(vector) for vector in basis))
        | {(colour,) * 6 for colour in ACTIVE}
    ))
    endpoints = tuple(itertools.product(full.SIX, full.COLOURS))
    star_names = [
        equations.variable(kind, boundary, endpoint)
        for kind in ("p", "q") for boundary in ACTIVE for endpoint in endpoints
    ]
    scalar_names = []
    scalars = {}
    for i in range(len(basis)):
        for a, b in itertools.product(ACTIVE, repeat=2):
            name = f"s{i}{a}{b}"
            scalars[i, a, b] = name
            scalar_names.append(name)
    generators = list(extra_generators)
    for a, b in itertools.product(ACTIVE, repeat=2):
        for word in coordinates:
            terms = [beta(word_terms, a, b, word)]
            if a == b and word == (a,) * 6:
                terms.append("-1")
            for i, vector in enumerate(basis):
                if word in vector:
                    terms.append(
                        f"-({singular_text(vector[word])})*{scalars[i, a, b]}"
                    )
            expression = "+".join(terms)
            if expression != "0":
                generators.append(expression)
    generators = list(dict.fromkeys(generators))
    body = ",".join(generators)
    names = parameter_names + scalar_names + [
        name for name in star_names if name in body
    ]
    program = "ring r=0,(" + ",".join(names) + "),dp;\n"
    program += "option(redSB);\n"
    program += "ideal I=" + body + ";\n"
    program += "ideal G=slimgb(I);\n"
    program += 'print("UNIT"); if(G[1]==1){1;}else{0;}\n'
    program += 'print("GBSIZE"); size(G);\n'
    return program, len(generators), len(names), len(coordinates)


def h_basis(blocks):
    hs = equations.cylinders.matching_tensor(full.SIX, blocks)
    return [{
        word: sp.expand(value) for word, value in hs.items()
        if sp.expand(value) != 0
    }]


def line_jobs(key, split=True):
    spec = rankone.select_direction(key)
    jobs = []
    blocks = wstruct.nine_symbol_blocks(key)
    if split:
        program, generators, variables, coordinates = build_program(
            blocks, [str(symbol) for symbol in X9] + ["t", "yinv"],
            h_basis(blocks), ("1-yinv*x00",),
        )
        jobs.append({
            "name": f"line_{key}_x00_invertible",
            "program": program, "generators": generators,
            "variables": variables, "coordinates": coordinates,
        })
        blocks0 = equations.cylinders.aggregate()
        blocks0[2, 3] = {
            cell: X9[bit] for bit, cell in enumerate(full.CELLS) if bit != 0
        }
        block25 = dict(blocks0[2, 5])
        block25[spec["t_cell"]] = (
            block25.get(spec["t_cell"], sp.Integer(0)) + T
        )
        blocks0[2, 5] = block25
        program, generators, variables, coordinates = build_program(
            blocks0, [str(symbol) for symbol in X9[1:]] + ["t"],
            h_basis(blocks0),
        )
        jobs.append({
            "name": f"line_{key}_x00_zero",
            "program": program, "generators": generators,
            "variables": variables, "coordinates": coordinates,
        })
    else:
        program, generators, variables, coordinates = build_program(
            blocks, [str(symbol) for symbol in X9] + ["t"], h_basis(blocks),
        )
        jobs.append({
            "name": f"line_{key}_full",
            "program": program, "generators": generators,
            "variables": variables, "coordinates": coordinates,
        })
    return jobs


def plane_job(key):
    rankone.select_direction(key)
    blocks = wstruct.d_full_blocks(key)
    d_tensor = {
        word: sp.expand(value)
        for word, value in rankone.d_plane_tensor(key, T).items()
    }
    program, generators, variables, coordinates = build_program(
        blocks, ["a0", "a1", "a2", "w", "u", "t"],
        h_basis(blocks) + [d_tensor],
    )
    return {
        "name": f"plane_{key}_d_full",
        "program": program, "generators": generators,
        "variables": variables, "coordinates": coordinates,
    }


def all_jobs(split=True):
    jobs = []
    for key in ("10", "20"):
        jobs.extend(line_jobs(key, split=split))
        jobs.append(plane_job(key))
    for job in jobs:
        job["sha256"] = hashlib.sha256(job["program"].encode()).hexdigest()
    return jobs


def marker(output, name):
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    return int(lines[lines.index(name) + 1])


def run_job(job, timeout=14400):
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
    assert (unit, size) == (1, 1), (job["name"], unit, size)
    return time.monotonic() - started


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--timeout", type=int, default=14400)
    parser.add_argument("--no-split", action="store_true")
    arguments = parser.parse_args()
    jobs = all_jobs(split=not arguments.no_split)
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
            lambda job: run_job(job, arguments.timeout), jobs,
        ))
    for job, seconds in zip(jobs, elapsed):
        print("RESULT", job["name"], "unit=1 gbsize=1",
              f"seconds={seconds:.3f}", flush=True)


if __name__ == "__main__":
    main()
