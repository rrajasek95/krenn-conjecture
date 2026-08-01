#!/usr/bin/env python3
"""Exact no-factor certificate for the sharp L0 tangent packet.

Research evidence only.  Krenn's conjecture remains open.  This checker is
specific to SHARP_M in verify_level_two_three_invertible_l0_obstruction.py.
It does not exclude the general tangent-incidence locus.

The sharp packet has rank(dPsi)=55 and five independent universal gauge
directions, hence its differential kernel is exactly the gauge kernel.  After
absorbing the direct endpoint cell by Euler, a factored L0 completion would
therefore obey

    U_r^s (V_u^t)^T + V_r^t (U_u^s)^T
      = R_{st,ru} + (alpha_r^{st} + alpha_u^{st}) M_ru.

We weaken every vertex sum to an independent edge scalar.  Already on the
four edges 01, 04, 05, 45 and vertices 0, 1, 4, 5, the resulting 64
quadrics in 48 variables generate the unit ideal.  The calculation is exact
over Q and is repeated over F_32003.

Standard-library Python generates the Singular programs entirely in memory.
An external Singular executable is the sole non-stdlib dependency.
"""

from pathlib import Path
from runpy import run_path
from shutil import which
import subprocess


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


SOURCE = Path(__file__).with_name(
    "verify_level_two_three_invertible_l0_obstruction.py"
)
VERTICES = (0, 1, 4, 5)
CORE_EDGES = ((0, 1), (0, 4), (0, 5), (4, 5))
SLICES = ((0, 0), (0, 1), (1, 0), (1, 1))
EXPECTED_CORE_BLOCKS = {
    (0, 1): ((2, 3), (4, 6)),
    (0, 4): ((5, 6), (11, 8)),
    (0, 5): ((6, 7), (13, 9)),
    (4, 5): ((1, 0), (0, 0)),
}


def audit_sharp_packet_and_kernel(source):
    blocks = source["SHARP_BLOCKS"]
    require(
        {edge: blocks[edge] for edge in CORE_EDGES}
        == EXPECTED_CORE_BLOCKS,
        "the four SHARP_M core blocks changed",
    )

    packet = source["SHARP_M"]
    cells = source["CELLS"]
    edges = source["EDGES"]
    derivative = source["differential_matrix"](packet)
    rank = source["rational_rank"](derivative)
    require(rank == 55, ("SHARP_M differential rank changed", rank))
    require(len(cells) - rank == 5, "SHARP_M differential nullity is not five")

    gauge_rows = []
    for basis in range(5):
        mu = [0] * 6
        mu[basis] = 1
        mu[5] = -1
        tangent = {
            (u, v, a, b): (mu[u] + mu[v]) * packet[u, v, a, b]
            for u, v, a, b in cells
        }
        require(
            not any(source["apply_differential"](packet, tangent)),
            ("a gauge direction left the differential kernel", basis),
        )
        gauge_rows.append([tangent[cell] for cell in cells])
    require(
        source["rational_rank"](gauge_rows) == 5,
        "the five SHARP_M gauge directions are dependent",
    )

    words = source["WORDS"]
    pure_zero = [int(word == (0,) * 6) for word in words]
    pure_one = [int(word == (1,) * 6) for word in words]
    zero_column = cells.index((0, 1, 0, 0))
    one_column = cells.index((4, 5, 1, 1))
    require(
        [row[zero_column] for row in derivative] == pure_zero,
        "the literal (01,00) pure tangent column changed",
    )
    require(
        [row[one_column] for row in derivative] == pure_one,
        "the literal (45,11) pure tangent column changed",
    )
    return blocks


def star_variable_names():
    u_names = tuple(
        f"u{s}r{r}a{a}"
        for s in (0, 1)
        for r in VERTICES
        for a in (0, 1)
    )
    v_names = tuple(
        f"v{t}r{r}a{a}"
        for t in (0, 1)
        for r in VERTICES
        for a in (0, 1)
    )
    lambda_names = tuple(
        f"l{s}{t}e{r}{u}"
        for s, t in SLICES
        for r, u in CORE_EDGES
    )
    names = u_names + v_names + lambda_names
    require(len(u_names) == 16 and len(v_names) == 16,
            "the endpoint-star variable count changed")
    require(len(lambda_names) == 16,
            "the independent edge-scalar count changed")
    require(len(names) == len(set(names)) == 48,
            "the total variable count is not 48")
    require(not any("alpha" in name for name in names),
            "a vertex-sum parameter leaked into the weakened ideal")
    return names


def factor_equations(blocks):
    equations = []
    for s, t in SLICES:
        for r, u in CORE_EDGES:
            for a in (0, 1):
                for b in (0, 1):
                    left = (
                        f"u{s}r{r}a{a}*v{t}r{u}a{b}"
                        f"+v{t}r{r}a{a}*u{s}r{u}a{b}"
                    )
                    right = f"l{s}{t}e{r}{u}*({blocks[r, u][a][b]})"
                    if (s, t, r, u, a, b) == (0, 0, 0, 1, 0, 0):
                        right = f"({right})+1"
                    if (s, t, r, u, a, b) == (1, 1, 4, 5, 1, 1):
                        right = f"({right})+1"
                    equations.append(f"({left})-({right})")
    require(len(equations) == 4 * 4 * 4 == 64,
            "the factor-equation count is not 64")
    require(len(set(equations)) == 64, "a factor equation was duplicated")
    return tuple(equations)


def singular_program(characteristic, names, equations, label):
    return "\n".join((
        f"ring factor_ring={characteristic},({','.join(names)}),dp;",
        "ideal factor_ideal=" + ",\n".join(equations) + ";",
        "option(redSB);",
        "ideal factor_basis=std(factor_ideal);",
        f'print("BEGIN_{label}");',
        "print(size(factor_basis));",
        "if (size(factor_basis)==1) { print(factor_basis[1]); }",
        f'print("END_{label}");',
        "exit;",
        "",
    ))


def audit_unit_ideal(executable, characteristic, names, equations, label):
    program = singular_program(characteristic, names, equations, label)
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
        raise RuntimeError(
            ("Singular unit-ideal audit timed out", label)
        ) from error
    require(
        completed.returncode == 0,
        ("Singular failed", label, completed.returncode, completed.stderr),
    )
    lines = tuple(line.strip() for line in completed.stdout.splitlines())
    begin = f"BEGIN_{label}"
    end = f"END_{label}"
    require(lines.count(begin) == lines.count(end) == 1,
            ("Singular result markers changed", label, lines))
    first = lines.index(begin)
    last = lines.index(end)
    require(first < last, ("Singular result markers are reversed", label))
    payload = tuple(line for line in lines[first + 1:last] if line)
    require(
        payload == ("1", "1"),
        ("the factor ideal is not certified as the unit ideal", label,
         payload, completed.stderr),
    )
    return payload


def main():
    require(SOURCE.is_file(), ("missing source checker", SOURCE))
    source = run_path(str(SOURCE))
    blocks = audit_sharp_packet_and_kernel(source)
    names = star_variable_names()
    equations = factor_equations(blocks)

    executable = which("Singular")
    require(executable is not None,
            "external dependency missing: Singular is not on PATH")
    try:
        version = subprocess.run(
            (executable, "--version"),
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise RuntimeError("Singular version check timed out") from error
    version_text = version.stdout + version.stderr
    require(version.returncode == 0 and "Singular" in version_text,
            ("could not identify the Singular executable", version_text))

    audit_unit_ideal(executable, 0, names, equations, "Q")
    audit_unit_ideal(executable, 32003, names, equations, "F32003")
    print("sharp L0 factor obstruction: all checks passed")
    print("  SHARP_M tangent kernel : rank 55, nullity 5 = gauge kernel")
    print("  weakened core          : 4 vertices, 4 edges, 4 slices")
    print("  polynomial system      : 48 variables, 64 quadrics")
    print("  exact Groebner bases   : (1) over Q and F_32003")
    print("  external dependency    : Singular")
    print("  scope                  : exact SHARP_M packet only")


if __name__ == "__main__":
    main()
