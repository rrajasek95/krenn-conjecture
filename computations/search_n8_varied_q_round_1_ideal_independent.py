#!/usr/bin/env python3
"""Independent re-verification of round-1 pair-cap survivor ideals.

Clean-room reconstruction of the saturated coordinate ideals for a
deterministic subsample of the projective-survivor families (default every
20th job of both job files, plus any job named on the command line).  It
shares no expansion code with the primary closure driver:

  * The element (a*Q + 4*p*s) * Q^[3] is computed by literal multiplication
    in the square-zero algebra with symbolic coefficient monomials, where
    Q = q + t1*e1 + ... + t4*e4, p and s are generic site-linear forms, and
    Q^[3] is accumulated as the cube divided by 3! over distinct triples.
    The Gram combinations p_X*s_Y + s_X*p_Y arise from the product; they
    are never postulated.
  * Words are emitted in descending order, the torus generator comes first,
    the variable order is reversed (h, t4..t1, a, then all s before all p,
    sites and colours descending), and the Groebner engine is slimgb.

A reported basis [1] therefore independently certifies the exact exclusion
of the sampled family on its cancellation locus (locus polynomials are
taken verbatim from the survivor ledger, reversed).
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from itertools import combinations, product
import json
import os
import shutil
import subprocess
import time

SITES = tuple(range(8))
COLOURS = (0, 1, 2)
BASE_Q = (
    (2, 3, 0, 0), (4, 5, 0, 0), (6, 7, 0, 0),
    (0, 1, 1, 1), (3, 6, 1, 1), (5, 7, 1, 1),
    (0, 2, 2, 2), (1, 4, 2, 2), (5, 6, 2, 2),
)
ALL_CELLS = tuple(
    (left, right, left_colour, right_colour)
    for left, right in combinations(SITES, 2)
    for left_colour, right_colour in product(COLOURS, repeat=2)
)
EXTRAS = tuple(cell for cell in ALL_CELLS if cell not in BASE_Q)
PURE_WORDS = tuple((colour,) * 8 for colour in COLOURS)


def multiply(left, right):
    """Multiply site-supported symbolic elements.

    Elements: dict[(sites_mask, colour_tuple)] -> dict[monomial] -> integer,
    where colour_tuple lists colours at ascending occupied sites and a
    monomial is a sorted tuple of variable-name strings.
    """
    result = defaultdict(lambda: defaultdict(int))
    for (mask_l, colours_l), terms_l in left.items():
        for (mask_r, colours_r), terms_r in right.items():
            if mask_l & mask_r:
                continue
            mask = mask_l | mask_r
            sites_l = [site for site in SITES if mask_l >> site & 1]
            sites_r = [site for site in SITES if mask_r >> site & 1]
            colour_at = dict(zip(sites_l, colours_l))
            colour_at.update(zip(sites_r, colours_r))
            colours = tuple(
                colour_at[site] for site in SITES if mask >> site & 1
            )
            key = (mask, colours)
            for mono_l, coeff_l in terms_l.items():
                for mono_r, coeff_r in terms_r.items():
                    mono = tuple(sorted(mono_l + mono_r))
                    result[key][mono] += coeff_l * coeff_r
    return {
        key: {mono: coeff for mono, coeff in terms.items() if coeff}
        for key, terms in result.items()
    }


def cell_element(cell, monomial):
    left, right, left_colour, right_colour = cell
    mask = (1 << left) | (1 << right)
    colours = (left_colour, right_colour) if left < right else (right_colour, left_colour)
    return {(mask, colours): {monomial: 1}}


def add_elements(target, source, scale=1):
    for key, terms in source.items():
        for mono, coeff in terms.items():
            target[key][mono] += scale * coeff


def build_quadratic(quad_cells):
    element = defaultdict(lambda: defaultdict(int))
    for cell in BASE_Q:
        add_elements(element, cell_element(cell, ()))
    for position, cell in enumerate(quad_cells):
        add_elements(element, cell_element(cell, (f"t{position + 1}",)))
    return dict(element)


def linear_form(prefix):
    element = defaultdict(lambda: defaultdict(int))
    for site in SITES:
        for colour in COLOURS:
            key = (1 << site, (colour,))
            element[key][(f"{prefix}{site}{colour}",)] += 1
    return dict(element)


def scaled(element, factor):
    return {
        key: {mono: factor * coeff for mono, coeff in terms.items()}
        for key, terms in element.items()
    }


def with_variable(element, name):
    return {
        key: {tuple(sorted(mono + (name,))): coeff for mono, coeff in terms.items()}
        for key, terms in element.items()
    }


def pair_cap_equations(quad_cells):
    quadratic = build_quadratic(quad_cells)
    square = multiply(quadratic, quadratic)
    raw_cube = multiply(square, quadratic)
    cube = {}
    for key, terms in raw_cube.items():
        divided = {}
        for mono, coeff in terms.items():
            assert coeff % 6 == 0
            divided[mono] = coeff // 6
        cube[key] = divided
    direct = multiply(quadratic, cube)          # equals 4*Q^[4]
    gram = multiply(linear_form("p"), linear_form("s"))
    mixed = multiply(gram, cube)

    total = defaultdict(lambda: defaultdict(int))
    add_elements(total, with_variable(direct, "a"))
    add_elements(total, scaled(mixed, 4))

    full_mask = (1 << 8) - 1
    equations = {}
    for (mask, colours), terms in total.items():
        if mask != full_mask:
            continue
        equations[colours] = dict(terms)
    for word in PURE_WORDS:
        equations.setdefault(word, {})
        equations[word][()] = equations[word].get((), 0) - 1
    return equations


def format_polynomial(terms):
    pieces = []
    for mono, coeff in sorted(terms.items(), reverse=True):
        if not coeff:
            continue
        body = "*".join(mono)
        if coeff == 1 and body:
            pieces.append(body)
        elif body:
            pieces.append(f"{coeff}*{body}")
        else:
            pieces.append(str(coeff))
    return "+".join(pieces).replace("+-", "-") if pieces else "0"


def ring_variables():
    names = ["h", "t4", "t3", "t2", "t1", "a"]
    for prefix in ("s", "p"):
        for site in reversed(SITES):
            for colour in reversed(COLOURS):
                names.append(f"{prefix}{site}{colour}")
    return names


def singular_program(quad_cells, locus):
    equations = pair_cap_equations(quad_cells)
    polynomials = ["h*t1*t2*t3*t4-1"]
    polynomials.extend(reversed(list(locus)))
    for word in sorted(equations, reverse=True):
        text = format_polynomial(equations[word])
        if text != "0":
            polynomials.append(text)
    variables = ring_variables()
    return (
        f"ring r=0,({','.join(variables)}),dp;\n"
        f"ideal I={','.join(polynomials)};\n"
        "ideal G=slimgb(I);\n"
        'print("SIZE");\nprint(size(G));\nprint("FIRST");\nprint(G[1]);\n'
    ), len(polynomials)


def run_job(executable, indices, locus, timeout):
    quad_cells = tuple(EXTRAS[index] for index in indices)
    program, count = singular_program(quad_cells, locus)
    start = time.monotonic()
    result = subprocess.run(
        [executable, "-q"], input=program, text=True, capture_output=True,
        check=True, timeout=timeout,
    )
    if result.stderr.strip():
        raise AssertionError(result.stderr)
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    size = lines[lines.index("SIZE") + 1]
    first = lines[lines.index("FIRST") + 1]
    return size == first == "1", count, time.monotonic() - start


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scratch-dir",
        default=os.environ.get("N8_ROUND1_SCRATCH", "/tmp"),
    )
    parser.add_argument("--stride", type=int, default=20)
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--timeout", type=int, default=3600)
    args = parser.parse_args()

    executable = shutil.which("Singular")
    assert executable is not None

    jobs = []
    for name in ("n8_round1_families_ideal_jobs.json",
                 "n8_round1_compatible_ideal_jobs.json"):
        path = os.path.join(args.scratch_dir, name)
        with open(path) as handle:
            records = json.load(handle)
        for position, record in enumerate(records):
            if position % args.stride == 0:
                jobs.append(
                    (tuple(record["indices"]), tuple(record["locus"]))
                )
    print("independent subsample size:", len(jobs), flush=True)

    from concurrent.futures import ThreadPoolExecutor, as_completed
    unit_count = 0
    failures = []
    start = time.monotonic()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(run_job, executable, indices, locus, args.timeout):
            indices for indices, locus in jobs
        }
        done = 0
        for future in as_completed(futures):
            unit, _count, _elapsed = future.result()
            if unit:
                unit_count += 1
            else:
                failures.append(futures[future])
                print("INDEPENDENT NON-UNIT:", futures[future], flush=True)
            done += 1
            if done % 100 == 0:
                print(f"{done}/{len(jobs)} checked,"
                      f" {time.monotonic() - start:.0f}s", flush=True)
    print("independent unit ideals:", unit_count, "/", len(jobs))
    print("independent non-unit:", failures)
    assert not failures


if __name__ == "__main__":
    main()
