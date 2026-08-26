#!/usr/bin/env python3
"""Time-boxed exact/modular probes for Q-coordinate units on cofactor branches.

Discovery/referee helper, not a terminal certificate by itself.  For every
requested branch and Q coordinate it computes the ideal obtained from the
six permanent, four triangle, twelve selected-cofactor equations together
with u*H-1 and Q_s.  Unit ideal means Q_s cannot vanish on the H-live locus.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import subprocess
import time


HERE = Path(__file__).resolve().parent
CORE = HERE / "audit_diagonal_cofactor_branch_orbits.py"
SPEC = importlib.util.spec_from_file_location("cofactor_core", CORE)
core = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(core)


def program(mask, q_indices, characteristic, algorithm):
    variables = ",".join([f"x{index}" for index in range(24)] + ["u"])
    generators = [core.permanent_poly(edge) for edge in range(6)]
    generators.extend(core.triangle_poly(*triple) for triple in core.TRIPLES)
    for edge, (i, j) in enumerate(core.EDGES):
        entries = (((0, 1), (1, 0)) if (mask >> edge) & 1
                   else ((0, 0), (1, 1)))
        for x, y in entries:
            generators.append(core.cofactor_poly(2 * i + x, 2 * j + y))
    hafnian = core.matching_poly(tuple(range(8)))
    generators.append(core.normalize_poly(
        tuple((coefficient, monomial + (24,))
              for monomial, coefficient in hafnian.items()) + ((-1, ()),)))
    generators.extend(core.q_poly(q_index) for q_index in q_indices)
    command = {"std": "std(I)",
               "slimgb": "slimgb(I)",
               "modslimgb": 'modGB("slimgb",I,1)'}[algorithm]
    return (
        f"ring r={characteristic},({variables}),dp;\n"
        + ('LIB "sing.lib";\n' if algorithm == "slimgb" else "")
        + ('LIB "modstd.lib";\n' if algorithm == "modslimgb" else "")
        + "option(redSB);\nideal I="
        + ",\n".join(core.poly_to_singular(poly) for poly in generators)
        + f";\nideal G={command};\n"
        + 'print("MARK_ONE"); reduce(1,G);\n'
        + 'print("MARK_SIZE"); size(G);\n')


def run(mask, q_indices, characteristic, algorithm, timeout):
    started = time.monotonic()
    try:
        completed = subprocess.run(
            ["Singular", "-q"], input=program(mask, q_indices, characteristic,
                                               algorithm),
            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        return "TIMEOUT", time.monotonic() - started, ""
    lines = [line.strip() for line in completed.stdout.splitlines()
             if line.strip()]
    try:
        one = lines[lines.index("MARK_ONE") + 1]
        size = lines[lines.index("MARK_SIZE") + 1]
    except (ValueError, IndexError):
        return "ERROR", time.monotonic() - started, " | ".join(lines[-6:])
    return ("UNIT" if one == "0" else f"NONUNIT(size={size},one={one})",
            time.monotonic() - started, "")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mask", type=int, default=0)
    parser.add_argument("--char", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--algorithm", choices=("std", "slimgb", "modslimgb"),
                        default="std")
    parser.add_argument("--q", type=int, nargs="*", default=list(range(16)))
    parser.add_argument("--together", action="store_true")
    args = parser.parse_args()
    groups = [tuple(args.q)] if args.together else [(q_index,) for q_index in args.q]
    for q_indices in groups:
        status, elapsed, detail = run(args.mask, q_indices, args.char,
                                      args.algorithm, args.timeout)
        print(args.mask, args.char, q_indices, status, f"{elapsed:.3f}", detail,
              flush=True)


if __name__ == "__main__":
    main()
