#!/usr/bin/env python3
"""The first repaired 6R four-edge factor escape dies on edge 14.

Starting from the two-block repaired rank-55/53 packet, also set M05=E01.
The original four-edge weakened factor ideal is no longer unit, but adding
edge 14 makes the five-edge weakened ideal unit over Q and F_32003.  The
packet retains both separate factored pure faces and all six residual-R2
witness pairs.  Standard-library Python; Singular is the sole external
dependency.
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
SHARP = REPAIRED["SHARP"]
BOUNDARY = REPAIRED["BOUNDARY"]
SITES = REPAIRED["SITES"]
COLOURS = REPAIRED["COLOURS"]
WORDS = REPAIRED["WORDS"]
CELLS = REPAIRED["CELLS"]
SLICES = tuple(product(COLOURS, repeat=2))
FOUR_EDGES = ((0, 1), (0, 4), (0, 5), (4, 5))
FIVE_EDGES = FOUR_EDGES + ((1, 4),)
VERTICES = (0, 1, 4, 5)
E01 = ((0, 1), (0, 0))


def near_escape_packet():
    packet = dict(REPAIRED["M"])
    for a, b in product(COLOURS, repeat=2):
        packet[0, 5, a, b] = E01[a][b]
    return packet


M = near_escape_packet()


def ranks_over_fields(matrix):
    return (
        SHARP["rational_rank"](matrix),
        SHARP["modular_rank"](matrix, 101),
        SHARP["modular_rank"](matrix, 32_003),
        SHARP["modular_rank"](matrix, 1_000_003),
    )


def audit_boundary_data():
    changed = tuple(cell for cell in CELLS if M[cell] != REPAIRED["M"][cell])
    require(len(changed) == 4 and {cell[:2] for cell in changed} == {(0, 5)},
            ("the M05 near-escape change set changed", changed))
    derivative = SHARP["differential_matrix"](M)
    mixed = [
        row for row, word in zip(derivative, WORDS)
        if word not in ((0,) * 6, (1,) * 6)
    ]
    ranks = (ranks_over_fields(derivative), ranks_over_fields(mixed))
    require(ranks == (
        (55, 55, 55, 55),
        (53, 53, 53, 53),
    ), ("the M05 near-escape ranks changed", ranks))

    gauges = []
    for basis in range(5):
        mu = [0] * 6
        mu[basis] = 1
        mu[5] = -1
        tangent = {
            (u, v, a, b): (mu[u] + mu[v]) * M[u, v, a, b]
            for u, v, a, b in CELLS
        }
        require(not any(SHARP["apply_differential"](M, tangent)),
                ("an M05 near-escape gauge left the kernel", basis))
        gauges.append([tangent[cell] for cell in CELLS])
    require(SHARP["rational_rank"](gauges) == 5,
            "the M05 near-escape gauges are dependent")
    require(len(CELLS) - ranks[0][0] == 5,
            "the M05 near-escape kernel is larger than the gauges")

    selected = REPAIRED["selected_family"](SITES)
    function = BOUNDARY["audit_factored_three_slice_completion"]
    globals_dict = function.__globals__
    old_m = globals_dict["M"]
    old_x = globals_dict["X"]
    try:
        globals_dict["M"] = M
        globals_dict["X"] = selected
        faces = (function(0), function(1))
    finally:
        globals_dict["M"] = old_m
        globals_dict["X"] = old_x
    require(faces == (
        (256, (0, 1, 0, 0)),
        (256, (4, 5, 1, 1)),
    ), ("the M05 near-escape factored faces changed", faces))

    witnesses = {}
    for root in SITES:
        table = {}
        for output, neighbour in REPAIRED["WITNESSES"][root].items():
            require(BOUNDARY["pure_column"](M, root, neighbour, output),
                    ("an M05 near-escape witness vanished",
                     root, output, neighbour))
            complement = tuple(
                site for site in SITES if site not in (root, neighbour)
            )
            nonzero = sum(
                SHARP["hafnian"](M, complement, word) != 0
                for word in WORDS
            )
            require(nonzero,
                    ("an M05 near-escape cofactor vanished",
                     root, output, neighbour))
            table[output] = (neighbour, nonzero)
        witnesses[root] = table
    return ranks, faces, witnesses


def variable_names(edges):
    u_names = tuple(
        f"u{s}r{r}a{a}"
        for s in COLOURS for r in VERTICES for a in COLOURS
    )
    v_names = tuple(
        f"v{t}r{r}a{a}"
        for t in COLOURS for r in VERTICES for a in COLOURS
    )
    lambda_names = tuple(
        f"l{s}{t}e{r}_{u}"
        for s, t in SLICES for r, u in edges
    )
    names = u_names + v_names + lambda_names
    require(len(names) == 32 + 4 * len(edges)
            and len(names) == len(set(names)),
            ("the near-escape variable count changed", len(edges), len(names)))
    return names


def factor_equations(edges):
    equations = []
    for s, t in SLICES:
        for r, u in edges:
            for a, b in product(COLOURS, repeat=2):
                left = (
                    f"u{s}r{r}a{a}*v{t}r{u}a{b}"
                    f"+v{t}r{r}a{a}*u{s}r{u}a{b}"
                )
                right = f"l{s}{t}e{r}_{u}*({M[r, u, a, b]})"
                if (s, t, r, u, a, b) == (0, 0, 0, 1, 0, 0):
                    right = f"({right})+1"
                if (s, t, r, u, a, b) == (1, 1, 4, 5, 1, 1):
                    right = f"({right})+1"
                equations.append(f"({left})-({right})")
    require(len(equations) == 16 * len(edges),
            ("the near-escape equation count changed",
             len(edges), len(equations)))
    return tuple(equations)


def singular_program(characteristic, edges, label):
    names = variable_names(edges)
    equations = factor_equations(edges)
    return "\n".join((
        f"ring near_escape={characteristic},({','.join(names)}),dp;",
        "ideal I=" + ",\n".join(equations) + ";",
        "option(redSB);",
        "ideal G=std(I);",
        f'print("BEGIN_{label}");',
        "print(size(G));",
        "if (size(G)==1) { print(G[1]); }",
        f'print("END_{label}");',
        "exit;",
        "",
    ))


def run_singular(executable, characteristic, edges, label):
    program = singular_program(characteristic, edges, label)
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
        raise RuntimeError(("near-escape Singular timeout", label)) from error
    require(completed.returncode == 0,
            ("near-escape Singular failed", label, completed.stderr))
    lines = tuple(line.strip() for line in completed.stdout.splitlines())
    begin = f"BEGIN_{label}"
    end = f"END_{label}"
    require(lines.count(begin) == lines.count(end) == 1,
            ("near-escape markers changed", label, lines))
    first = lines.index(begin)
    last = lines.index(end)
    payload = tuple(line for line in lines[first + 1:last] if line)
    return payload, program


def audit_factor_ideals():
    executable = which("Singular")
    require(executable is not None,
            "external dependency missing: Singular is not on PATH")
    payloads = {}
    programs = []
    for characteristic, field in ((0, "Q"), (32_003, "F32003")):
        for edges, scope in ((FOUR_EDGES, "four"), (FIVE_EDGES, "five")):
            label = f"NEAR_{field}_{scope}"
            payload, program = run_singular(
                executable, characteristic, edges, label
            )
            expected = ("394",) if scope == "four" else ("1", "1")
            require(payload == expected,
                    ("near-escape Groebner payload changed",
                     field, scope, payload))
            payloads[field, scope] = payload
            programs.append(program)
    digest = sha256("\n".join(programs).encode()).hexdigest()
    return payloads, digest


def main():
    ranks, faces, witnesses = audit_boundary_data()
    payloads, digest = audit_factor_ideals()
    print("six-rank-one M05 near-escape factor obstruction: all checks passed")
    print(f"  differential ranks        : {ranks}")
    print(f"  separate factored faces   : {faces}")
    print(f"  six-root R2 witnesses     : {witnesses}")
    print(f"  four/five-edge payloads   : {payloads}")
    print(f"  Singular programs SHA-256 : {digest}")
    print("  conclusion                : edge 14 closes the first local factor escape")


if __name__ == "__main__":
    main()
