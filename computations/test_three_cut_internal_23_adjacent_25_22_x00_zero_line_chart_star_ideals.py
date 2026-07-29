#!/usr/bin/env python3
"""Symbolic shared-star ideals on the five x00=0 normal-line charts.

The companion full-cylinder minors prove that cuts 0 and 1 have common
normal equal to the direct-tensor line on these charts.  This script checks
the resulting two-colour boundary systems over characteristic zero while
leaving every unnormalized A23 entry symbolic.
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

import derive_three_cut_internal_23_adjacent_25_22_x00_zero_line_minors as minors
import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations


ACTIVE = (0, 1)


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


def build_program(pivot_bit):
    _zero_bits, _parameter_bits, parameters = minors.chart_data(pivot_bit)
    blocks = minors.symbolic_blocks(pivot_bit, parameters)
    hs = equations.cylinders.matching_tensor(full.SIX, blocks)
    word_terms = equations.reconstruct_word_terms(blocks)
    coordinates = tuple(sorted(
        set(word_terms) | set(hs) | {(colour,) * 6 for colour in ACTIVE}
    ))
    endpoints = tuple(itertools.product(full.SIX, full.COLOURS))
    star_names = [
        equations.variable(kind, boundary, endpoint)
        for kind in ("p", "q") for boundary in ACTIVE for endpoint in endpoints
    ]
    scalar_names = [f"s{a}{b}" for a, b in itertools.product(ACTIVE, repeat=2)]
    parameter_names = [str(parameter) for parameter in parameters]
    generators = []
    for a, b in itertools.product(ACTIVE, repeat=2):
        scalar = f"s{a}{b}"
        for word in coordinates:
            terms = [beta(word_terms, a, b, word)]
            if a == b and word == (a,) * 6:
                terms.append("-1")
            if word in hs:
                terms.append(f"-({singular_text(hs[word])})*{scalar}")
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


def marker(output, name):
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    return int(lines[lines.index(name) + 1])


def run(job, timeout):
    pivot_bit, program, generators, variables, coordinates = job
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required")
    started = time.monotonic()
    completed = subprocess.run(
        [singular, "-q"], input=program, text=True, capture_output=True,
        check=True, timeout=timeout,
    )
    if completed.stderr.strip():
        raise AssertionError(completed.stderr)
    unit = marker(completed.stdout, "UNIT")
    size = marker(completed.stdout, "GBSIZE")
    assert (unit, size) == (1, 1), (full.CELL_NAMES[pivot_bit], unit, size)
    return (
        full.CELL_NAMES[pivot_bit], variables, coordinates, generators,
        hashlib.sha256(program.encode()).hexdigest(),
        time.monotonic() - started,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pivot", choices=tuple(
            full.CELL_NAMES[bit] for bit in minors.OFF_EXCEPTIONAL_BITS
        ), action="append",
    )
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--timeout", type=int, default=3600)
    args = parser.parse_args()
    selected = set(args.pivot or ())
    jobs = []
    for pivot_bit in minors.OFF_EXCEPTIONAL_BITS:
        if selected and full.CELL_NAMES[pivot_bit] not in selected:
            continue
        program, generators, variables, coordinates = build_program(pivot_bit)
        jobs.append((pivot_bit, program, generators, variables, coordinates))
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        results = list(executor.map(lambda job: run(job, args.timeout), jobs))
    for name, variables, coordinates, generators, digest, elapsed in results:
        print(
            "X00_ZERO_LINE_CHART", name, f"variables={variables}",
            f"coordinates={coordinates}", f"generators={generators}",
            f"sha256={digest}", "unit=1", "gbsize=1",
            f"seconds={elapsed:.3f}",
        )


if __name__ == "__main__":
    main()
