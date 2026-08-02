#!/usr/bin/env python3
"""Obstruct arbitrary (M_05,M_14) changes on the repaired rank-55 packet.

The eight entries of the two blocks are polynomial variables, not sampled
scalars.  The checker constructs the actual vertex-sum-coupled four-slice
factor ideal on the full K4={0,1,4,5} and requires its reduced basis to be
(1) over Q and, in reversed order, over F_32003.  It also rechecks that the
family contains the repaired rank-55, separate-factored-pure, full-R2 base
point.  Python is standard-library; Singular is the sole external
dependency.  Research evidence only; live under -O and -I -S.
"""

from hashlib import sha256
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
BASE = REPAIRED["M"]
SITES = REPAIRED["SITES"]
COLOURS = REPAIRED["COLOURS"]

VARIABLE_EDGES = ((0, 5), (1, 4))
K4_VERTICES = (0, 1, 4, 5)
K4_EDGES = tuple(
    (left, right)
    for position, left in enumerate(K4_VERTICES)
    for right in K4_VERTICES[position + 1:]
)
SLICES = tuple(product(COLOURS, repeat=2))
FIXED_K4_BLOCKS = {
    (0, 1): ((2, 3), (4, 6)),
    (0, 4): ((0, 0), (1, 0)),
    (1, 5): ((0, 0), (1, 0)),
    (4, 5): ((1, 0), (0, 0)),
}
EXPECTED_GAUGE_MINOR = (
    (2, 1, 1, 1, 0),
    (2, 0, 0, 0, -2),
    (0, 1, 0, 0, -2),
    (0, 0, 1, 0, 0),
    (0, 0, 0, 1, 0),
)
GAUGE_MINOR_CELLS = (
    (0, 1, 0, 0),
    (0, 2, 1, 1),
    (0, 3, 0, 0),
    (0, 4, 1, 0),
    (1, 2, 0, 0),
)
EXPECTED_R2 = {
    0: {0: (3, 64), 1: (2, 64)},
    1: {0: (2, 64), 1: (3, 64)},
    2: {0: (3, 64), 1: (0, 64)},
    3: {0: (2, 64), 1: (1, 64)},
    4: {0: (5, 4), 1: (0, 40)},
    5: {0: (4, 4), 1: (1, 40)},
}
EXPECTED_EQUATION_DIGEST = (
    "982ac7f8c1cc1363ae3e41a4a288612d7c21a6d40f970077c1abf963cb4e07db"
)
EXPECTED_PROGRAM_DIGESTS = {
    "Q": "8c5e226c2e56409cbf1d8243730b84b830c1ed44032b9f38d84bd6dfa58cb888",
    "F32003-reverse": (
        "ba8d5450440cca5c28ea6c40e0fe355a3c0f341d50c0bc683ad0d05208fbcfc6"
    ),
}


def star_names():
    u_names = tuple(
        f"u{s}r{root}a{a}"
        for s in COLOURS for root in K4_VERTICES for a in COLOURS
    )
    v_names = tuple(
        f"v{t}r{root}a{a}"
        for t in COLOURS for root in K4_VERTICES for a in COLOURS
    )
    alpha_names = tuple(
        f"z{s}{t}r{root}"
        for s, t in SLICES for root in K4_VERTICES
    )
    names = u_names + v_names + alpha_names
    require(len(names) == len(set(names)) == 48,
            "the arbitrary-pair star-variable census changed")
    return names


STAR_NAMES = star_names()
PARAMETER_NAMES = tuple(
    f"{prefix}{a}{b}"
    for prefix in ("a", "b")
    for a, b in product(COLOURS, repeat=2)
)
ALL_NAMES = STAR_NAMES + PARAMETER_NAMES
require(len(ALL_NAMES) == len(set(ALL_NAMES)) == 56,
        "the arbitrary-pair total-variable census changed")


def symbolic_packet():
    packet = dict(BASE)
    for prefix, edge in zip(("a", "b"), VARIABLE_EDGES):
        for a, b in product(COLOURS, repeat=2):
            packet[edge + (a, b)] = f"{prefix}{a}{b}"
    return packet


SYMBOLIC_PACKET = symbolic_packet()


def block(packet, edge):
    return tuple(
        tuple(packet[edge + (a, b)] for b in COLOURS)
        for a in COLOURS
    )


def coupled_equations():
    equations = []
    for s, t in SLICES:
        for r, u in K4_EDGES:
            for a, b in product(COLOURS, repeat=2):
                left = (
                    f"u{s}r{r}a{a}*v{t}r{u}a{b}"
                    f"+v{t}r{r}a{a}*u{s}r{u}a{b}"
                )
                right = (
                    f"(z{s}{t}r{r}+z{s}{t}r{u})"
                    f"*({SYMBOLIC_PACKET[r, u, a, b]})"
                )
                if (s, t, r, u, a, b) == (0, 0, 0, 1, 0, 0):
                    right = f"({right})+1"
                if (s, t, r, u, a, b) == (1, 1, 4, 5, 1, 1):
                    right = f"({right})+1"
                equations.append(f"({left})-({right})")
    require(len(equations) == len(set(equations)) == 96,
            "the arbitrary-pair coupled equation census changed")
    return tuple(equations)


EQUATIONS = coupled_equations()


def bareiss_determinant(matrix):
    work = [list(row) for row in matrix]
    size = len(work)
    require(all(len(row) == size for row in work),
            "a nonsquare determinant was requested")
    sign = 1
    previous = 1
    for pivot_index in range(size - 1):
        pivot_row = next(
            (row for row in range(pivot_index, size)
             if work[row][pivot_index]),
            None,
        )
        if pivot_row is None:
            return 0
        if pivot_row != pivot_index:
            work[pivot_index], work[pivot_row] = (
                work[pivot_row], work[pivot_index]
            )
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = (
                    work[row][column] * pivot
                    - work[row][pivot_index]
                    * work[pivot_index][column]
                )
                require(numerator % previous == 0,
                        "Bareiss exact division failed")
                work[row][column] = numerator // previous
        previous = pivot
    return sign * work[-1][-1]


def audit_scope_and_base_point():
    for edge, expected in FIXED_K4_BLOCKS.items():
        require(block(BASE, edge) == expected,
                ("a fixed full-K4 block changed", edge, block(BASE, edge)))
        require(block(SYMBOLIC_PACKET, edge) == expected,
                ("a symbolic fixed full-K4 block changed", edge))
    require(block(SYMBOLIC_PACKET, (0, 5))
            == (("a00", "a01"), ("a10", "a11")),
            "the M05 parameter block changed")
    require(block(SYMBOLIC_PACKET, (1, 4))
            == (("b00", "b01"), ("b10", "b11")),
            "the M14 parameter block changed")

    gauge_rows = []
    for basis in range(5):
        mu = [0] * len(SITES)
        mu[basis] = 1
        mu[5] = -1
        gauge_rows.append(tuple(
            (mu[u] + mu[v]) * BASE[u, v, a, b]
            for u, v, a, b in GAUGE_MINOR_CELLS
        ))
    gauge_minor = tuple(gauge_rows)
    require(gauge_minor == EXPECTED_GAUGE_MINOR,
            ("the parameter-independent gauge minor changed", gauge_minor))
    require(bareiss_determinant(gauge_minor) == 8,
            "the parameter-independent gauge determinant changed")

    _derivative, ranks, changed = (
        REPAIRED["audit_residual_rank_and_pure_incidence"]()
    )
    require(ranks == {
        "D": (55, 55, 55, 55),
        "D_mixed": (53, 53, 53, 53),
        "D|e0": (55, 55, 55, 55),
        "D|e1": (55, 55, 55, 55),
        "D|e0,e1": (55, 55, 55, 55),
    }, ("the arbitrary-pair base ranks changed", ranks))
    faces = REPAIRED["audit_factored_faces"]()
    require(faces == (
        (256, (0, 1, 0, 0)),
        (256, (4, 5, 1, 1)),
    ), ("the arbitrary-pair base pure faces changed", faces))
    witnesses = REPAIRED["audit_r2_witnesses"]()
    require(witnesses == EXPECTED_R2,
            ("the arbitrary-pair base R2 table changed", witnesses))
    parameters = (
        block(BASE, (0, 5)),
        block(BASE, (1, 4)),
    )
    return len(changed), ranks, faces, witnesses, parameters


def singular_program(characteristic, reverse):
    names = tuple(reversed(ALL_NAMES)) if reverse else ALL_NAMES
    equations = tuple(reversed(EQUATIONS)) if reverse else EQUATIONS
    label = "REVERSE" if reverse else "PRIMARY"
    return "\n".join((
        f"ring arbitrary_pair={characteristic},({','.join(names)}),dp;",
        "option(redSB);",
        "ideal coupled_ideal=" + ",\n".join(equations) + ";",
        "ideal coupled_basis=slimgb(coupled_ideal);",
        f'print("BEGIN_{label}");',
        "print(size(coupled_basis));",
        "if (size(coupled_basis)==1) { print(coupled_basis[1]); }",
        f'print("END_{label}");',
        "exit;",
        "",
    ))


def run_certificate(executable, characteristic, reverse):
    program = singular_program(characteristic, reverse)
    try:
        completed = subprocess.run(
            (executable, "-q"), input=program, text=True,
            capture_output=True, timeout=180, check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise RuntimeError(
            ("arbitrary-pair Singular timed out", characteristic, reverse)
        ) from error
    require(completed.returncode == 0,
            ("arbitrary-pair Singular failed", characteristic,
             completed.returncode, completed.stderr))
    label = "REVERSE" if reverse else "PRIMARY"
    payload = tuple(
        line.strip() for line in completed.stdout.splitlines()
        if line.strip()
    )
    require(payload == (
        f"BEGIN_{label}", "1", "1", f"END_{label}"
    ), ("the arbitrary-pair unit basis changed",
        characteristic, payload))
    return sha256(program.encode("utf-8")).hexdigest()


def main():
    base_audit = audit_scope_and_base_point()
    executable = which("Singular")
    require(executable is not None,
            "external dependency missing: Singular is not on PATH")
    equation_digest = sha256(
        "\n".join(EQUATIONS).encode("utf-8")
    ).hexdigest()
    require(equation_digest == EXPECTED_EQUATION_DIGEST,
            ("the arbitrary-pair equation ledger changed",
             equation_digest))
    program_digests = {
        "Q": run_certificate(executable, 0, False),
        "F32003-reverse": run_certificate(executable, 32_003, True),
    }
    require(program_digests == EXPECTED_PROGRAM_DIGESTS,
            ("the arbitrary-pair program ledgers changed",
             program_digests))
    print("repaired arbitrary-pair coupled obstruction: passed")
    print(f"  variables/equations         : {len(ALL_NAMES)}/{len(EQUATIONS)}")
    print(f"  base parameters             : {base_audit[4]}")
    print(f"  base ranks                  : {base_audit[1]}")
    print(f"  base R2 witnesses           : {base_audit[3]}")
    gauge_determinant = bareiss_determinant(EXPECTED_GAUGE_MINOR)
    print(f"  parameter-free gauge minor : det={gauge_determinant}")
    print(f"  equation-ledger digest      : {equation_digest}")
    print(f"  program digests             : {program_digests}")
    print("  exact reduced bases         : Q=(1), F32003-reverse=(1)")
    print("  conclusion                  : no arbitrary-pair rank-55/R2 escape")


if __name__ == "__main__":
    main()
