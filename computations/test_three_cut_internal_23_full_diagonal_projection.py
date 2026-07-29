#!/usr/bin/env python3
"""Exact-Q worker for the full A_23 diagonal-block quotient.

All nine variable-cell coordinate blocks except two selected diagonal blocks
are killed.  Off-diagonal coefficients therefore disappear completely, while
the two selected pure targets survive.  The diagonal zero/nonzero pattern is
normalized to 0/1 by the fixed-cell torus.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import time

import explore_three_cut_internal_23_full_supports as full
import test_three_cut_internal_23_plane_support_component as worker


DIAGONAL = ((0, 0), (1, 1), (2, 2))
BITS = (0, 4, 8)


def coefficients_for_pattern(pattern: int, outside_bit: int = 3):
    answer = {full.CELLS[outside_bit]: full.Q(1)}
    for colour, bit in enumerate(BITS):
        if pattern & (1 << colour):
            answer[DIAGONAL[colour]] = full.Q(1)
    return answer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--diagonal-pattern", required=True, type=lambda x: int(x, 0))
    parser.add_argument("--colours", required=True)
    parser.add_argument("--characteristic", type=int, default=0)
    parser.add_argument("--timeout", type=int, default=1200)
    parser.add_argument("--outside-bit", type=int, choices=full.OUTSIDE_BITS, default=3)
    parser.add_argument("--retain-outside", action="store_true")
    parser.add_argument("--components", action="store_true")
    parser.add_argument("--retain-bit", action="append", type=int, choices=range(9), default=[])
    parser.add_argument("--coefficient-bit", action="append", type=int, choices=range(9), default=[])
    parser.add_argument(
        "--coefficient-value", action="append", default=[],
        help="extra normalized coefficient as BIT:VALUE (VALUE is rational)",
    )
    parser.add_argument("--projected-cylinder-normal", action="store_true")
    args = parser.parse_args()
    if not 0 <= args.diagonal_pattern < 8:
        raise SystemExit("diagonal pattern must lie in [0,7]")
    colours = tuple(int(value) for value in args.colours.split(","))
    if len(colours) not in (2, 3) or len(set(colours)) != len(colours) or not set(colours) <= set(range(3)):
        raise SystemExit("colours must be two or three distinct values from 0,1,2")
    retained = tuple(BITS[colour] for colour in colours)
    if args.retain_outside:
        retained += (args.outside_bit,)
    retained += tuple(args.retain_bit)
    retained = tuple(dict.fromkeys(retained))
    coefficients = coefficients_for_pattern(args.diagonal_pattern, args.outside_bit)
    coefficients.update({full.CELLS[bit]: full.Q(1) for bit in args.coefficient_bit})
    for item in args.coefficient_value:
        bit_text, value_text = item.split(":", 1)
        bit = int(bit_text)
        if not 0 <= bit < 9:
            raise SystemExit("coefficient bit must lie in [0,8]")
        coefficients[full.CELLS[bit]] = full.Q(value_text)
    projected, killed, basis = full.projected_problem(
        coefficients,
        maximal_mask=(1 << 9) - 1,
        retained_bits=retained,
        normal="line",
    )
    if args.projected_cylinder_normal:
        blocks = full.blocks_for_coefficients(coefficients)
        normals = [
            full.projected_cylinder_intersection((2, 3, 4, cut), blocks, killed)
            for cut in (0, 1, 5)
        ]
        assert full.equations.same_span(normals[0], normals[1])
        assert full.equations.same_span(normals[0], normals[2])
        basis = normals[0]
    span = full.equations.cylinders.echelon(basis)
    for colour in colours:
        word = (colour,) * 6
        assert word not in killed
        assert not full.equations.cylinders.member({word: full.Q(1)}, span)
    if args.components:
        if args.characteristic != 0:
            raise SystemExit("component mode is intended for characteristic zero")
        program, diagonal_counts, off_count = full.equations.singular_program(
            projected, basis, colours
        )
        generators = sum(diagonal_counts) + off_count
    else:
        program, generators = worker.direct_program(
            projected, basis, colours, characteristic=args.characteristic
        )
    print(
        "START", f"pattern={args.diagonal_pattern}", f"colours={colours}",
        f"killed={len(killed)}", f"words={len(projected)}",
        f"atoms={sum(map(len, projected.values()))}",
        f"normal_dim={len(span)}", f"generators={generators}", flush=True,
    )
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required")
    started = time.monotonic()
    completed = subprocess.run(
        [singular, "-q"], input=program, text=True, capture_output=True,
        check=True, timeout=args.timeout,
    )
    if completed.stderr.strip():
        raise AssertionError(completed.stderr)
    if args.components:
        components = worker.marker_values(completed.stdout, "COMPONENTS", len(colours))
        checked = worker.marker_values(completed.stdout, "CHECKED", 1)[0]
        live = worker.marker_values(completed.stdout, "LIVE", 1)[0]
        print(
            "COMPONENT_RESULT", f"pattern={args.diagonal_pattern}",
            f"colours={colours}", f"components={components}",
            f"checked={checked}", f"live={live}",
            f"seconds={time.monotonic()-started:.3f}", flush=True,
        )
        return
    unit = worker.marker_values(completed.stdout, "UNIT", 1)[0]
    size = worker.marker_values(completed.stdout, "GBSIZE", 1)[0]
    print(
        "RESULT", f"pattern={args.diagonal_pattern}", f"colours={colours}",
        f"characteristic={args.characteristic}", f"unit={unit}",
        f"gbsize={size}", f"seconds={time.monotonic()-started:.3f}", flush=True,
    )


if __name__ == "__main__":
    main()
