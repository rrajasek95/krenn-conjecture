#!/usr/bin/env python3
"""Exact no-factor certificate for the repaired full-isotropic boundary.

The repaired packet changes SHARP_M blocks 04 and 15 to E10 and reaches
rank 55/53 with separate literal factorizations of both pure targets.  Its
kernel is still exactly the five vertex gauges.  On core edges 01,04,05,45,
even the weakened four-slice factor equations with independent edge scalars
generate the unit ideal over Q and F_32003.  Standard-library Python with
Singular as the sole external dependency.
"""

from hashlib import sha256
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
FACTOR = run_path(str(
    HERE / "verify_level_two_l0_sharp_factor_obstruction.py"
))
SHARP = REPAIRED["SHARP"]
M = REPAIRED["M"]
CORE_EDGES = FACTOR["CORE_EDGES"]
EXPECTED_CORE_BLOCKS = {
    (0, 1): ((2, 3), (4, 6)),
    (0, 4): ((0, 0), (1, 0)),
    (0, 5): ((6, 7), (13, 9)),
    (4, 5): ((1, 0), (0, 0)),
}


def core_blocks():
    blocks = {
        edge: tuple(
            tuple(M[edge + (a, b)] for b in (0, 1))
            for a in (0, 1)
        )
        for edge in CORE_EDGES
    }
    require(blocks == EXPECTED_CORE_BLOCKS,
            ("the repaired factor core changed", blocks))
    return blocks


def audit_kernel_and_pure_columns():
    derivative, ranks, _changed = REPAIRED["audit_residual_rank_and_pure_incidence"]()
    require(ranks["D"] == (55, 55, 55, 55),
            ("the repaired factor rank changed", ranks))
    gauge_rows = []
    for basis in range(5):
        mu = [0] * 6
        mu[basis] = 1
        mu[5] = -1
        tangent = {
            (u, v, a, b): (mu[u] + mu[v]) * M[u, v, a, b]
            for u, v, a, b in REPAIRED["CELLS"]
        }
        require(not any(SHARP["apply_differential"](M, tangent)),
                ("a repaired vertex gauge left the kernel", basis))
        gauge_rows.append([tangent[cell] for cell in REPAIRED["CELLS"]])
    require(SHARP["rational_rank"](gauge_rows) == 5,
            "the repaired vertex gauges are dependent")
    require(len(REPAIRED["CELLS"]) - ranks["D"][0] == 5,
            "the repaired differential kernel is larger than the gauges")

    pure_zero = [int(word == (0,) * 6) for word in REPAIRED["WORDS"]]
    pure_one = [int(word == (1,) * 6) for word in REPAIRED["WORDS"]]
    zero_column = REPAIRED["CELLS"].index((0, 1, 0, 0))
    one_column = REPAIRED["CELLS"].index((4, 5, 1, 1))
    require([row[zero_column] for row in derivative] == pure_zero,
            "the repaired literal pure-zero column changed")
    require([row[one_column] for row in derivative] == pure_one,
            "the repaired literal pure-one column changed")
    return ranks


def audit_singular():
    names = FACTOR["star_variable_names"]()
    equations = FACTOR["factor_equations"](core_blocks())
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
    require(version.returncode == 0 and "Singular" in version.stdout + version.stderr,
            ("could not identify Singular", version.stdout, version.stderr))

    payloads = {
        "Q": FACTOR["audit_unit_ideal"](
            executable, 0, names, equations, "REPAIRED_Q"
        ),
        "F32003": FACTOR["audit_unit_ideal"](
            executable, 32_003, names, equations, "REPAIRED_F32003"
        ),
    }
    programs = "\n".join(
        FACTOR["singular_program"](
            characteristic, names, equations, label
        )
        for characteristic, label in (
            (0, "REPAIRED_Q"),
            (32_003, "REPAIRED_F32003"),
        )
    )
    digest = sha256(programs.encode()).hexdigest()
    return len(names), len(equations), payloads, digest


def main():
    ranks = audit_kernel_and_pure_columns()
    variables, equations, payloads, digest = audit_singular()
    print("six-rank-one repaired factor obstruction: all checks passed")
    print(f"  repaired differential ranks : {ranks}")
    print("  tangent kernel              : nullity 5 = vertex gauges")
    print("  weakened core               : 4 vertices, 4 edges, 4 slices")
    print(f"  polynomial system           : {variables} variables, {equations} quadrics")
    print(f"  exact Groebner payloads     : {payloads}")
    print(f"  Singular programs SHA-256   : {digest}")
    print("  conclusion                  : no shared factored four-slice completion")


if __name__ == "__main__":
    main()
