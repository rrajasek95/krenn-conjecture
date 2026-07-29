#!/usr/bin/env python3
"""Run one exact characteristic-zero component test in the A_23 support census.

This is the per-orbit worker used by the eventual exhaustive verifier.  It
reconstructs the endpoint-ordered cofactors and actual cylinder normal, then
asks Singular over Q for minimal components of the diagonal fibres and tests
every component tuple against all ordered off-diagonal fibres.
"""

from __future__ import annotations

import argparse
import itertools
import shutil
import subprocess
import time

import explore_three_cut_internal_23_perturbation as equations
import explore_three_cut_internal_23_plane_supports as supports


def marker_values(output: str, marker: str, count: int):
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    start = lines.index(marker) + 1
    return tuple(int(lines[start + offset]) for offset in range(count))


def direct_program(word_terms, basis, active, characteristic=0):
    types = tuple((site, colour) for site in supports.SIX for colour in supports.COLOURS)
    names = [
        equations.variable(kind, boundary, endpoint)
        for kind in ("p", "q")
        for boundary in active
        for endpoint in types
    ]
    generators = []
    for a, b in itertools.product(active, repeat=2):
        target = a if a == b else None
        generators.extend(equations.fibre_equations(word_terms, basis, a, b, target))
    code = f"ring r={characteristic},(" + ",".join(names) + "),dp;\n"
    code += "option(redSB);\n"
    code += "ideal I=" + ",".join(generators) + ";\n"
    code += "ideal G=std(I);\n"
    code += 'print("UNIT"); if(G[1]==1){1;}else{0;}\n'
    code += 'print("GBSIZE"); size(G);\n'
    return code, len(generators)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mask", required=True, type=lambda value: int(value, 0))
    parser.add_argument("--cut", required=True, type=int, choices=(0, 1, 5))
    parser.add_argument("--timeout", type=int, default=7200)
    parser.add_argument("--direct", action="store_true")
    parser.add_argument("--characteristic", type=int, default=0)
    args = parser.parse_args()

    if not 0 <= args.mask < 32:
        raise SystemExit("mask must be between 0 and 31")
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required")

    row = supports.census(args.mask)
    basis = row["normals"][args.cut]
    absorbed = set(row["absorbed"][args.cut])
    active = tuple(colour for colour in supports.COLOURS if colour not in absorbed)
    if len(active) < 2:
        raise SystemExit(f"only {len(active)} active target colours; worker expects >=2")
    word_terms = equations.reconstruct_word_terms(supports.blocks_for_mask(args.mask))
    if args.direct:
        program, generator_count = direct_program(
            word_terms, basis, active, args.characteristic
        )
        diagonal_counts = ()
        off_count = generator_count
    else:
        program, diagonal_counts, off_count = equations.singular_program(
            word_terms, basis, active
        )

    print(
        "START",
        f"mask={args.mask}",
        f"support={supports.support_name(args.mask)}",
        f"cut={args.cut}",
        f"normal_dim={len(equations.cylinders.echelon(basis))}",
        f"active={active}",
        f"diagonal={diagonal_counts}",
        f"off={off_count}",
        flush=True,
    )
    started = time.monotonic()
    completed = subprocess.run(
        [singular, "-q"], input=program, text=True, capture_output=True,
        check=True, timeout=args.timeout,
    )
    elapsed = time.monotonic() - started
    if completed.stderr.strip():
        raise AssertionError(completed.stderr)
    if args.direct:
        unit = marker_values(completed.stdout, "UNIT", 1)[0]
        gbsize = marker_values(completed.stdout, "GBSIZE", 1)[0]
        print(
            "DIRECT_RESULT", f"mask={args.mask}", f"cut={args.cut}",
            f"characteristic={args.characteristic}", f"unit={unit}",
            f"gbsize={gbsize}", f"seconds={elapsed:.3f}", flush=True,
        )
        return
    components = marker_values(completed.stdout, "COMPONENTS", len(active))
    checked = marker_values(completed.stdout, "CHECKED", 1)[0]
    live = marker_values(completed.stdout, "LIVE", 1)[0]
    expected = 1
    for count in components:
        expected *= count
    assert checked == expected
    print(
        "RESULT",
        f"mask={args.mask}",
        f"cut={args.cut}",
        f"components={components}",
        f"checked={checked}",
        f"live={live}",
        f"seconds={elapsed:.3f}",
        flush=True,
    )


if __name__ == "__main__":
    main()
