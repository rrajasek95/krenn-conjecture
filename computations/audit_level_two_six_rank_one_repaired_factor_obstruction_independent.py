#!/usr/bin/env python3
"""Independent audit of the repaired 6R simultaneous-factor obstruction.

This audit does not import the primary repaired-factor obstruction.  It uses
the alternate four-edge core 01,05,15,45 (so it sees the second repaired
block M_15 rather than M_04), reverses the variable and generator orders,
and regenerates exact unit ideals over Q and F_32003.

It also audits the logical bridge from the full eight-site slice equations
to the weakened edge-scalar system: rank 55 makes ker(dPsi) exactly the five
vertex gauges, while Euler gives dPsi(M)=3 Psi(M), so every direct endpoint
coefficient is absorbed by a uniform shift of the vertex scalars.

Research evidence only.  Standard-library Python with Singular as the sole
external dependency; checks remain live under -O and -I -S.
"""

from hashlib import sha256
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from runpy import run_path
from shutil import which
import subprocess


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
REPAIRED = run_path(str(
    HERE
    / "verify_level_two_six_rank_one_isotropic_pencil_repaired_factored_pure_boundary.py"
))
GUARD = run_path(str(HERE / "verify_level_two_one_sided_rank55_guard.py"))
SHARP = REPAIRED["SHARP"]
M = REPAIRED["M"]
SITES = REPAIRED["SITES"]
COLOURS = REPAIRED["COLOURS"]
WORDS = REPAIRED["WORDS"]
CELLS = REPAIRED["CELLS"]

VERTICES = (0, 1, 4, 5)
ALT_EDGES = ((0, 1), (0, 5), (1, 5), (4, 5))
SLICES = ((0, 0), (0, 1), (1, 0), (1, 1))
EXPECTED_BLOCKS = {
    (0, 1): ((2, 3), (4, 6)),
    (0, 5): ((6, 7), (13, 9)),
    (1, 5): ((0, 0), (1, 0)),
    (4, 5): ((1, 0), (0, 0)),
}
E01 = ((0, 1), (0, 0))
ESCAPE_REPLACEMENTS = ((0, 5), (1, 4))
FULL_K4_EDGES = tuple(
    (left, right)
    for position, left in enumerate(VERTICES)
    for right in VERTICES[position + 1:]
)


def append_columns(matrix, *columns):
    return [
        row[:] + [column[index] for column in columns]
        for index, row in enumerate(matrix)
    ]


def ranks_over_fields(matrix):
    return (
        SHARP["rational_rank"](matrix),
        SHARP["modular_rank"](matrix, 101),
        SHARP["modular_rank"](matrix, 32_003),
        SHARP["modular_rank"](matrix, 1_000_003),
    )


def audit_old_guard_linear_failure():
    packet = GUARD["build_internal_packet"]()
    derivative = GUARD["differential"](packet)
    e_zero = [int(word == (0,) * 6) for word in WORDS]
    e_one = [int(word == (1,) * 6) for word in WORDS]
    ranks = {
        "D": ranks_over_fields(derivative),
        "D|e0": ranks_over_fields(append_columns(derivative, e_zero)),
        "D|e1": ranks_over_fields(append_columns(derivative, e_one)),
        "D|e0,e1": ranks_over_fields(
            append_columns(derivative, e_zero, e_one)
        ),
    }
    require(ranks == {
        "D": (55, 55, 55, 55),
        "D|e0": (56, 56, 56, 56),
        "D|e1": (56, 56, 56, 56),
        "D|e0,e1": (57, 57, 57, 57),
    }, ("the old rank-55 guard incidence failure changed", ranks))
    return ranks


def alternate_core_blocks():
    blocks = {
        edge: tuple(
            tuple(M[edge + (a, b)] for b in COLOURS)
            for a in COLOURS
        )
        for edge in ALT_EDGES
    }
    require(blocks == EXPECTED_BLOCKS,
            ("the alternate repaired core changed", blocks))
    return blocks


def audit_kernel_euler_and_direct_absorption():
    derivative = SHARP["differential_matrix"](M)
    require(ranks_over_fields(derivative) == (55, 55, 55, 55),
            "the independently audited repaired rank changed")

    gauges = []
    for basis in range(5):
        mu = [0] * 6
        mu[basis] = 1
        mu[5] = -1
        tangent = {
            (u, v, a, b): (mu[u] + mu[v]) * M[u, v, a, b]
            for u, v, a, b in CELLS
        }
        require(SHARP["apply_differential"](M, tangent) == [0] * 64,
                ("an independent repaired gauge check failed", basis))
        gauges.append([tangent[cell] for cell in CELLS])
    require(SHARP["rational_rank"](gauges) == 5,
            "the independently audited repaired gauges are dependent")
    require(len(CELLS) - SHARP["rational_rank"](derivative) == 5,
            "the repaired kernel is not exactly the gauge kernel")

    slope = SHARP["matching_tensor"](M)
    require(SHARP["apply_differential"](M, M)
            == [3 * value for value in slope],
            "Euler dPsi(M)=3Psi(M) failed on the repaired packet")

    # For direct coefficient w, the edge coefficient after moving the direct
    # term into the gauge kernel is mu_r+mu_u-w/3.  Shifting every vertex
    # scalar by -w/6 gives exactly the same coefficient as a vertex sum.
    mu = (1, 2, 3, 4, 5, -15)
    require(sum(mu) == 0, "the direct-absorption gauge sample lost trace zero")
    w = Q(6)
    alpha = tuple(Q(value) - w / 6 for value in mu)
    for r, u in REPAIRED["EDGES"]:
        require(alpha[r] + alpha[u] == Q(mu[r] + mu[u]) - w / 3,
                ("the Euler/direct scalar shift changed", r, u))

    e_zero = [int(word == (0,) * 6) for word in WORDS]
    e_one = [int(word == (1,) * 6) for word in WORDS]
    zero_column = CELLS.index((0, 1, 0, 0))
    one_column = CELLS.index((4, 5, 1, 1))
    require([row[zero_column] for row in derivative] == e_zero,
            "the independent pure-zero preimage changed")
    require([row[one_column] for row in derivative] == e_one,
            "the independent pure-one preimage changed")
    return len(gauges), len(CELLS) - 55


def build_first_coupled_escape():
    packet = dict(M)
    for edge in ESCAPE_REPLACEMENTS:
        for a, b in product(COLOURS, repeat=2):
            packet[edge + (a, b)] = E01[a][b]
    return packet


ESCAPE_M = build_first_coupled_escape()


def audit_first_coupled_escape_geometry():
    derivative = SHARP["differential_matrix"](ESCAPE_M)
    mixed = [
        row for row, word in zip(derivative, WORDS)
        if word not in ((0,) * 6, (1,) * 6)
    ]
    e_zero = [int(word == (0,) * 6) for word in WORDS]
    e_one = [int(word == (1,) * 6) for word in WORDS]
    ranks = {
        "D": ranks_over_fields(derivative),
        "D_mixed": ranks_over_fields(mixed),
        "D|e0": ranks_over_fields(append_columns(derivative, e_zero)),
        "D|e1": ranks_over_fields(append_columns(derivative, e_one)),
        "D|e0,e1": ranks_over_fields(
            append_columns(derivative, e_zero, e_one)
        ),
    }
    require(ranks == {
        "D": (55, 55, 55, 55),
        "D_mixed": (53, 53, 53, 53),
        "D|e0": (55, 55, 55, 55),
        "D|e1": (55, 55, 55, 55),
        "D|e0,e1": (55, 55, 55, 55),
    }, ("the first coupled escape rank signature changed", ranks))
    zero_column = CELLS.index((0, 1, 0, 0))
    one_column = CELLS.index((4, 5, 1, 1))
    require([row[zero_column] for row in derivative] == e_zero,
            "the first coupled escape lost the pure-zero preimage")
    require([row[one_column] for row in derivative] == e_one,
            "the first coupled escape lost the pure-one preimage")

    gauges = []
    for basis in range(5):
        mu = [0] * 6
        mu[basis] = 1
        mu[5] = -1
        tangent = {
            (u, v, a, b): (mu[u] + mu[v]) * ESCAPE_M[u, v, a, b]
            for u, v, a, b in CELLS
        }
        require(SHARP["apply_differential"](ESCAPE_M, tangent) == [0] * 64,
                ("a first-escape gauge left the kernel", basis))
        gauges.append([tangent[cell] for cell in CELLS])
    require(SHARP["rational_rank"](gauges) == 5,
            "the first-escape gauges lost independence")

    cofactor_counts = {}
    for root, by_output in REPAIRED["WITNESSES"].items():
        for output, neighbour in by_output.items():
            require(REPAIRED["BOUNDARY"]["pure_column"](
                ESCAPE_M, root, neighbour, output
            ), ("the first coupled escape lost a pure R2 witness",
                root, output, neighbour))
            edge = tuple(sorted((root, neighbour)))
            complement = tuple(site for site in SITES if site not in edge)
            count = sum(
                SHARP["hafnian"](ESCAPE_M, complement, word) != 0
                for word in WORDS
            )
            require(count > 0,
                    ("the first coupled escape killed an R2 cofactor", edge))
            cofactor_counts[edge] = count
    return ranks, cofactor_counts


def reversed_variable_names():
    u_names = tuple(
        f"u{s}r{root}a{a}"
        for s in reversed(COLOURS)
        for root in reversed(VERTICES)
        for a in reversed(COLOURS)
    )
    v_names = tuple(
        f"v{t}r{root}a{a}"
        for t in reversed(COLOURS)
        for root in reversed(VERTICES)
        for a in reversed(COLOURS)
    )
    lambda_names = tuple(
        f"l{s}{t}e{r}{u}"
        for s, t in reversed(SLICES)
        for r, u in reversed(ALT_EDGES)
    )
    names = tuple(reversed(lambda_names + v_names + u_names))
    require((len(u_names), len(v_names), len(lambda_names), len(names))
            == (16, 16, 16, 48),
            "the independent factor variable census changed")
    require(len(set(names)) == len(names),
            "an independent factor variable was duplicated")
    return names


def alternate_factor_equations(blocks):
    equations = []
    for s, t in reversed(SLICES):
        for r, u in reversed(ALT_EDGES):
            for a, b in reversed(tuple(product(COLOURS, repeat=2))):
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
    equations = tuple(reversed(equations))
    require(len(equations) == len(set(equations)) == 64,
            "the independent factor equation census changed")
    return equations


def singular_program(characteristic, names, equations, label):
    return "\n".join((
        f"ring independent_ring={characteristic},({','.join(names)}),dp;",
        "ideal independent_ideal=" + ",\n".join(equations) + ";",
        "option(redSB);",
        "ideal independent_basis=std(independent_ideal);",
        f'print("BEGIN_{label}");',
        "print(size(independent_basis));",
        "if (size(independent_basis)==1) { print(independent_basis[1]); }",
        f'print("END_{label}");',
        "exit;",
        "",
    ))


def run_unit_ideal(executable, characteristic, names, equations, label):
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
        raise RuntimeError(("independent factor ideal timed out", label)) from error
    require(completed.returncode == 0,
            ("Singular failed on independent factor ideal",
             label, completed.returncode, completed.stderr))
    lines = tuple(line.strip() for line in completed.stdout.splitlines())
    begin, end = f"BEGIN_{label}", f"END_{label}"
    require(lines.count(begin) == lines.count(end) == 1,
            ("independent factor markers changed", label, lines))
    first, last = lines.index(begin), lines.index(end)
    payload = tuple(line for line in lines[first + 1:last] if line)
    require(payload == ("1", "1"),
            ("the alternate factor core is not the unit ideal",
             label, payload, completed.stderr))
    return sha256(program.encode("utf-8")).hexdigest(), payload


def audit_alternate_unit_ideals():
    executable = which("Singular")
    require(executable is not None,
            "external dependency missing: Singular is not on PATH")
    names = reversed_variable_names()
    equations = alternate_factor_equations(alternate_core_blocks())
    results = {
        "Q": run_unit_ideal(executable, 0, names, equations, "ALT_Q"),
        "F32003": run_unit_ideal(
            executable, 32_003, names, equations, "ALT_F32003"
        ),
    }
    ledger = "\n".join(equations)
    return len(names), len(equations), sha256(ledger.encode()).hexdigest(), results


def escape_block(edge):
    return tuple(
        tuple(ESCAPE_M[edge + (a, b)] for b in COLOURS)
        for a in COLOURS
    )


def independent_full_k4_system():
    u_names = tuple(
        f"iu{s}r{root}a{a}"
        for s in COLOURS for root in VERTICES for a in COLOURS
    )
    v_names = tuple(
        f"iv{t}r{root}a{a}"
        for t in COLOURS for root in VERTICES for a in COLOURS
    )
    lambda_names = tuple(
        f"il{s}{t}e{r}{u}"
        for s, t in SLICES for r, u in FULL_K4_EDGES
    )
    equations = []
    for s, t in SLICES:
        for r, u in FULL_K4_EDGES:
            block = escape_block((r, u))
            for a, b in product(COLOURS, repeat=2):
                left = (
                    f"iu{s}r{r}a{a}*iv{t}r{u}a{b}"
                    f"+iv{t}r{r}a{a}*iu{s}r{u}a{b}"
                )
                right = f"il{s}{t}e{r}{u}*({block[a][b]})"
                if (s, t, r, u, a, b) == (0, 0, 0, 1, 0, 0):
                    right = f"({right})+1"
                if (s, t, r, u, a, b) == (1, 1, 4, 5, 1, 1):
                    right = f"({right})+1"
                equations.append(f"({left})-({right})")
    names = u_names + v_names + lambda_names
    require((len(names), len(equations)) == (56, 96),
            "the independent full-K4 escape system changed size")
    return names, tuple(equations)


def coupled_full_k4_system():
    # The actual gauge coefficients are vertex sums, not independent edge
    # scalars.  The direct coefficient has already been absorbed into an
    # unrestricted uniform shift of these four retained vertex scalars.
    u_names = tuple(
        f"cu{s}r{root}a{a}"
        for s in reversed(COLOURS)
        for root in reversed(VERTICES)
        for a in reversed(COLOURS)
    )
    v_names = tuple(
        f"cv{t}r{root}a{a}"
        for t in reversed(COLOURS)
        for root in reversed(VERTICES)
        for a in reversed(COLOURS)
    )
    alpha_names = tuple(
        f"ca{s}{t}r{root}"
        for s, t in reversed(SLICES)
        for root in reversed(VERTICES)
    )
    equations = []
    for s, t in reversed(SLICES):
        for r, u in reversed(FULL_K4_EDGES):
            block = escape_block((r, u))
            for a, b in reversed(tuple(product(COLOURS, repeat=2))):
                left = (
                    f"cu{s}r{r}a{a}*cv{t}r{u}a{b}"
                    f"+cv{t}r{r}a{a}*cu{s}r{u}a{b}"
                )
                right = (
                    f"(ca{s}{t}r{r}+ca{s}{t}r{u})*({block[a][b]})"
                )
                if (s, t, r, u, a, b) == (0, 0, 0, 1, 0, 0):
                    right = f"({right})+1"
                if (s, t, r, u, a, b) == (1, 1, 4, 5, 1, 1):
                    right = f"({right})+1"
                equations.append(f"({left})-({right})")
    names = tuple(reversed(alpha_names + v_names + u_names))
    equations = tuple(reversed(equations))
    require((len(names), len(equations)) == (48, 96),
            "the coupled full-K4 escape system changed size")
    return names, equations


def basis_program(characteristic, names, equations, label):
    return "\n".join((
        f"ring escape_ring={characteristic},({','.join(names)}),dp;",
        "ideal escape_ideal=" + ",\n".join(equations) + ";",
        "option(redSB);",
        "ideal escape_basis=std(escape_ideal);",
        f'print("BEGIN_{label}");',
        "print(size(escape_basis));",
        "if (size(escape_basis)==1) { print(escape_basis[1]); }",
        f'print("END_{label}");',
        "exit;",
        "",
    ))


def run_basis(executable, characteristic, names, equations, label, timeout=60):
    program = basis_program(characteristic, names, equations, label)
    try:
        completed = subprocess.run(
            (executable, "-q"), input=program, text=True,
            capture_output=True, timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise RuntimeError(("escape factor ideal timed out", label)) from error
    require(completed.returncode == 0,
            ("Singular failed on escape factor ideal",
             label, completed.returncode, completed.stderr))
    lines = tuple(line.strip() for line in completed.stdout.splitlines())
    begin, end = f"BEGIN_{label}", f"END_{label}"
    require(lines.count(begin) == lines.count(end) == 1,
            ("escape factor markers changed", label, lines))
    first, last = lines.index(begin), lines.index(end)
    payload = tuple(line for line in lines[first + 1:last] if line)
    return sha256(program.encode("utf-8")).hexdigest(), payload


def audit_first_coupled_escape_obstruction():
    executable = which("Singular")
    require(executable is not None,
            "external dependency missing: Singular is not on PATH")
    independent_names, independent_equations = independent_full_k4_system()
    independent = run_basis(
        executable, 0, independent_names, independent_equations,
        "INDEPENDENT_ESCAPE_Q",
    )
    require(independent[1] == ("99",),
            ("the first escape no longer evades independent edge scalars",
             independent))

    coupled_names, coupled_equations = coupled_full_k4_system()
    coupled = {
        "Q": run_basis(
            executable, 0, coupled_names, coupled_equations,
            "COUPLED_ESCAPE_Q",
        ),
        "F32003": run_basis(
            executable, 32_003, coupled_names, coupled_equations,
            "COUPLED_ESCAPE_F32003",
        ),
    }
    require(all(result[1] == ("1", "1") for result in coupled.values()),
            ("the coupled full-K4 escape ideal stopped being unit", coupled))
    return (
        (len(independent_names), len(independent_equations), independent),
        (len(coupled_names), len(coupled_equations), coupled),
    )


def main():
    old_guard = audit_old_guard_linear_failure()
    kernel = audit_kernel_euler_and_direct_absorption()
    ideals = audit_alternate_unit_ideals()
    escape_geometry = audit_first_coupled_escape_geometry()
    escape_obstruction = audit_first_coupled_escape_obstruction()
    print("independent repaired 6R factor obstruction audit: passed")
    print(f"  old guard incidence ranks      : {old_guard}")
    print(f"  repaired gauges/nullity        : {kernel}")
    print(f"  alternate core                 : {ALT_EDGES}")
    print(f"  variables/equations/ledger hash: {ideals[:3]}")
    print(f"  reversed-order unit ideals     : {ideals[3]}")
    print(f"  first coupled escape geometry  : {escape_geometry}")
    print(f"  escape independent/coupled GBs : {escape_obstruction}")
    print("  conclusion                      : Euler/gauge and coupled-core obstructions sound")


if __name__ == "__main__":
    main()
