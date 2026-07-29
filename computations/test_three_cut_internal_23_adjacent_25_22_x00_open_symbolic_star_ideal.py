#!/usr/bin/env python3
"""Symbolic two-colour star ideal on the E22 x00-open normal-line chart."""

from __future__ import annotations

import hashlib
import itertools
import shutil
import subprocess
import time

import sympy as sp

import derive_three_cut_internal_23_adjacent_25_22_x00_open_line_minors as lock
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


def build_program():
    blocks = lock.symbolic_blocks(lock.PARAMETERS)
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
    parameter_names = [str(parameter) for parameter in lock.PARAMETERS]
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


def main():
    program, generators, variables, coordinates = build_program()
    digest = hashlib.sha256(program.encode()).hexdigest()
    print(
        "X00_OPEN_SYMBOLIC", f"variables={variables}",
        f"coordinates={coordinates}", f"generators={generators}",
        f"sha256={digest}", flush=True,
    )
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
    print(
        "RESULT", "unit", marker(completed.stdout, "UNIT"),
        "gbsize", marker(completed.stdout, "GBSIZE"),
        f"seconds={time.monotonic()-started:.3f}",
    )


if __name__ == "__main__":
    main()
