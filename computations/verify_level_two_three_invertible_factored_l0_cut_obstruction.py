#!/usr/bin/env python3
"""Exact cut-rank obstruction for the 3I+1R+2Z incidence survivor.

For a factored pure L0 slice, every residual cut flattening has rank at
most two after adding an arbitrary vertex-gauge packet.  On the cut
{0,1}|{2,3,4,5}, the 224 cubic minors for the pure-zero slice of the exact
incidence survivor generate the unit ideal over Q and F_32003.

Standard-library Python generates the Singular programs in memory.  An
external Singular executable is the sole non-stdlib dependency.
"""

from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
from runpy import run_path
from shutil import which
import subprocess


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "verify_level_two_three_invertible_l0_incidence_survivor.py"
LEFT = (0, 1)
RIGHT = (2, 3, 4, 5)
VARIABLES = tuple(f"l{site}" for site in range(6))
EXPECTED_MINORS = 224


def solve_linear_system(matrix, target):
    height = len(matrix)
    width = len(matrix[0])
    rows = [
        [Q(value) for value in row] + [Q(target[index])]
        for index, row in enumerate(matrix)
    ]
    rank = 0
    pivots = []
    for column in range(width):
        pivot = next((slot for slot in range(rank, height)
                      if rows[slot][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for slot in range(height):
            if slot == rank or not rows[slot][column]:
                continue
            multiple = rows[slot][column]
            rows[slot] = [
                left - multiple * right
                for left, right in zip(rows[slot], rows[rank])
            ]
        pivots.append(column)
        rank += 1
    require(all(any(row[:width]) or row[width] == 0 for row in rows),
            "pure-zero target left the differential image")
    solution = [Q(0)] * width
    for row, column in enumerate(pivots):
        solution[column] = rows[row][width]
    require([
        sum(Q(value) * coordinate
            for value, coordinate in zip(row, solution))
        for row in matrix
    ] == [Q(value) for value in target],
            "computed pure-zero preimage does not solve D K=e0")
    return solution, tuple(pivots)


def oriented_value(packet, r, u, a, b):
    if r < u:
        return packet[r, u, a, b]
    return packet[u, r, b, a]


def rational_literal(value):
    value = Q(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"({value.numerator}/{value.denominator})"


def build_cut_matrix(source):
    guard = source["guard"]
    packet = source["M"]
    derivative = guard["differential_matrix"](packet)
    words = tuple(product((0, 1), repeat=6))
    pure_zero = [int(word == (0,) * 6) for word in words]
    preimage, pivots = solve_linear_system(derivative, pure_zero)
    require(len(pivots) == 55,
            ("differential rank changed during solve", len(pivots)))
    tangent = {
        cell: preimage[index]
        for index, cell in enumerate(guard["CELLS"])
    }

    cut = []
    for r in LEFT:
        for a in (0, 1):
            row = []
            for u in RIGHT:
                for b in (0, 1):
                    constant = oriented_value(tangent, r, u, a, b)
                    residual = oriented_value(packet, r, u, a, b)
                    row.append(
                        f"({rational_literal(constant)})"
                        f"+({VARIABLES[r]}+{VARIABLES[u]})"
                        f"*({rational_literal(residual)})"
                    )
            cut.append(row)
    require((len(cut), len(cut[0])) == (4, 8),
            "cut flattening is not 4 by 8")
    require(
        len(tuple(combinations(range(4), 3)))
        * len(tuple(combinations(range(8), 3)))
        == EXPECTED_MINORS,
        "cubic cut-minor count changed",
    )
    return cut, preimage


def singular_program(characteristic, cut, label):
    entries = ",".join(entry for row in cut for entry in row)
    return "\n".join((
        f"ring cut_ring={characteristic},({','.join(VARIABLES)}),dp;",
        f"matrix cut_matrix[4][8]={entries};",
        "ideal cut_minors=minor(cut_matrix,3);",
        "option(redSB);",
        "ideal cut_basis=std(cut_minors);",
        f'print("BEGIN_{label}");',
        "print(size(cut_basis));",
        "if (size(cut_basis)==1) { print(cut_basis[1]); }",
        f'print("END_{label}");',
        "exit;",
        "",
    ))


def audit_unit_ideal(executable, characteristic, cut, label):
    program = singular_program(characteristic, cut, label)
    try:
        completed = subprocess.run(
            (executable, "-q"),
            input=program,
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise RuntimeError(("Singular cut-minor audit timed out", label)) \
            from error
    require(completed.returncode == 0,
            ("Singular failed", label, completed.stderr))
    lines = tuple(line.strip() for line in completed.stdout.splitlines())
    begin = f"BEGIN_{label}"
    end = f"END_{label}"
    require(lines.count(begin) == lines.count(end) == 1,
            ("Singular result markers changed", label, lines))
    payload = tuple(
        line for line in lines[lines.index(begin) + 1:lines.index(end)]
        if line
    )
    require(payload == ("1", "1"),
            ("cut-minor ideal is not the unit ideal", label, payload))
    return payload


def main():
    require(SOURCE.is_file(), ("missing incidence-survivor checker", SOURCE))
    source = run_path(str(SOURCE))
    source["audit_replacement_scope"]()
    source["guard"]["audit_generic_kernel_equation"]()
    source["guard"]["audit_rank_55"]()
    source["guard"]["audit_literal_r2"]()
    source["audit_l0_incidence"]()
    cut, preimage = build_cut_matrix(source)

    executable = which("Singular")
    require(executable is not None,
            "external dependency missing: Singular is not on PATH")
    version = subprocess.run(
        (executable, "--version"),
        text=True,
        capture_output=True,
        timeout=10,
        check=False,
    )
    require(version.returncode == 0
            and "Singular" in version.stdout + version.stderr,
            "could not identify the Singular executable")

    audit_unit_ideal(executable, 0, cut, "Q")
    audit_unit_ideal(executable, 32_003, cut, "F32003")
    print("three-invertible factored L0 cut obstruction: all checks passed")
    print("  source packet          : exact rank-55/53 incidence survivor")
    print("  pure-zero preimage     : D K=e_(0^6), exact rational RREF")
    print("  necessary flattening   : rank <=2 on cut {0,1}|{2,3,4,5}")
    print(f"  cut-minor system       : {EXPECTED_MINORS} cubics in 6 gauges")
    print("  exact Groebner bases   : (1) over Q and F_32003")
    print("  external dependency    : Singular")
    print(f"  preimage support       : {sum(value != 0 for value in preimage)}/60")


if __name__ == "__main__":
    main()
