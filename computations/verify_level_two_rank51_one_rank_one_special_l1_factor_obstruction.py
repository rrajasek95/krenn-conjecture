#!/usr/bin/env python3
"""Exclude the special 1R L1-incidence direction on the rank-51 packet.

At root 2, choose the selected rank-one matrix e_1 e_0^T.  The two L1
star projections have dimensions 5 and 12, and the linear span of their
60 factored products contains both pure targets.  Parameterize the actual
four shared stars and four direct coefficients instead.  The resulting
256 bilinear slice equations in 38 variables generate the unit ideal over
Q and, independently reversed, over F_32003.

Research evidence only.  Python is standard-library only; Singular is the
sole external executable.  Checks stay live under -O and -I -S.
"""

from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
from runpy import run_path
from shutil import which
from subprocess import run


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
SIX = run_path(str(
    HERE / "verify_level_two_six_rank_one_gauge_coupled_repair.py"
))
L1 = SIX["L1"]
CORE = SIX["CORE"]
SITES = SIX["SITES"]
COLOURS = SIX["COLOURS"]
EDGES = SIX["EDGES"]
ZERO_MATRIX = SIX["ZERO_MATRIX"]
ROOT = 2
SELECTED = {
    site: (((0, 0), (1, 0)) if site == ROOT else ZERO_MATRIX)
    for site in SITES
}

VARIABLES = tuple(
    [f"u{s}_{index}" for s in COLOURS for index in range(12)]
    + [f"v{t}_{index}" for t in COLOURS for index in range(5)]
    + [f"w{s}{t}" for s in COLOURS for t in COLOURS]
)

EXPECTED_HASHES = {
    "equations": "5019394e6c609b4eb415ae7c2b73f92f74d14ed9bfd60bda943af24991433919",
    "Q": "83df92ed89441d60e5d489cb2becdb66b6bc06a85c936ce4c880c434b87c6921",
    "F32003-reversed": "94bcff74b88eec659dcb63637db173cd66ad77c3153dd844468188ac67bd2c6b",
}


def blocks_from_packet(packet):
    return {
        (left, right): tuple(
            tuple(packet[left, right, a, b] for b in COLOURS)
            for a in COLOURS
        )
        for left, right in EDGES
    }


def l1_star_bases(packet):
    blocks = blocks_from_packet(packet)
    data = {}
    modes = {}
    for selected_column in COLOURS:
        equations = L1["l1_system"](SELECTED, blocks, selected_column)
        rank, _pivots, basis = L1["rational_nullspace"](equations)
        star_modes = tuple(
            tuple(vector[:12]) for vector in basis if any(vector[:12])
        )
        vacuous = tuple(
            vector for vector in basis if not any(vector[:12])
        )
        data[selected_column] = (
            rank, len(basis), len(star_modes),
            CORE["rational_rank"](star_modes), len(vacuous),
        )
        modes[selected_column] = star_modes
    require(data == {
        0: (20, 7, 5, 5, 2),
        1: (13, 14, 12, 12, 2),
    }, ("the special one-rank-one L1 systems changed", data))
    return data, modes


def column_matrix(columns):
    require(columns, "the special product family is empty")
    return [list(row) for row in zip(*columns)]


def append_columns(matrix, *columns):
    return [
        row + list(entries)
        for row, entries in zip(matrix, zip(*columns))
    ]


def audit_linear_incidence(packet, modes):
    products = tuple(
        CORE["apply_differential"](
            packet, L1["factored_tangent"](left_mode, right_mode)
        )
        for left_mode in modes[1]
        for right_mode in modes[0]
    )
    require(len(products) == 60,
            ("the special product count changed", len(products)))
    slope = CORE["matching_tensor"](packet)
    product_matrix = column_matrix(products)
    enlarged = column_matrix((slope,) + products)
    pure_zero = [int(word == (0,) * 6) for word in CORE["WORDS"]]
    pure_one = [int(word == (1,) * 6) for word in CORE["WORDS"]]
    ranks = {
        "products": CORE["rational_rank"](product_matrix),
        "direct+products": CORE["rational_rank"](enlarged),
        "+e0": CORE["rational_rank"](
            append_columns(enlarged, pure_zero)
        ),
        "+e1": CORE["rational_rank"](
            append_columns(enlarged, pure_one)
        ),
        "+e0+e1": CORE["rational_rank"](
            append_columns(enlarged, pure_zero, pure_one)
        ),
    }
    require(ranks == {
        "products": 40,
        "direct+products": 40,
        "+e0": 40,
        "+e1": 40,
        "+e0+e1": 40,
    }, ("the special linear L1 incidence changed", ranks))
    return ranks


def coefficient_string(value):
    value = Q(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"({value.numerator}/{value.denominator})"


def factor_equations(packet, modes):
    standard = []
    for index in range(12):
        vector = [Q(0)] * 12
        vector[index] = Q(1)
        standard.append(tuple(vector))
    nonzero_modes = modes[0]
    require(len(standard) == 12 and len(nonzero_modes) == 5,
            "the special factor-mode dimensions changed")

    output_tensor = {
        (left_index, right_index): CORE["apply_differential"](
            packet,
            L1["factored_tangent"](
                standard[left_index], nonzero_modes[right_index]
            ),
        )
        for left_index in range(12)
        for right_index in range(5)
    }
    slope = CORE["matching_tensor"](packet)
    pure_zero = [int(word == (0,) * 6) for word in CORE["WORDS"]]
    pure_one = [int(word == (1,) * 6) for word in CORE["WORDS"]]
    equations = []
    for s in COLOURS:
        for t in COLOURS:
            target = (
                pure_zero if (s, t) == (0, 0)
                else pure_one if (s, t) == (1, 1)
                else [0] * 64
            )
            for row in range(64):
                terms = []
                for left_index in range(12):
                    for right_index in range(5):
                        coefficient = output_tensor[
                            left_index, right_index
                        ][row]
                        if coefficient:
                            terms.append(
                                f"{coefficient_string(coefficient)}"
                                f"*u{s}_{left_index}*v{t}_{right_index}"
                            )
                if slope[row]:
                    terms.append(
                        f"{coefficient_string(slope[row])}*w{s}{t}"
                    )
                if target[row]:
                    terms.append("-1")
                require(terms,
                        ("an identically zero special equation appeared",
                         s, t, row))
                equations.append("+".join(terms))
    require(len(equations) == 256,
            ("the special factor equation count changed", len(equations)))
    return tuple(equations)


def singular_program(equations, characteristic, reverse=False):
    variables = tuple(reversed(VARIABLES)) if reverse else VARIABLES
    generators = tuple(reversed(equations)) if reverse else equations
    return (
        f"ring r={characteristic},({','.join(variables)}),dp;\n"
        f"ideal I={','.join(generators)};\n"
        "option(redSB);\n"
        "ideal G=slimgb(I);\n"
        "print(size(G));\n"
        "print(G[1]);\n"
    )


def audit_unit_ideals(equations):
    executable = which("Singular")
    require(executable is not None,
            "external dependency missing: Singular is not on PATH")
    programs = {
        "Q": singular_program(equations, 0),
        "F32003-reversed": singular_program(
            equations, 32003, reverse=True
        ),
    }
    hashes = {
        "equations": sha256("\n".join(equations).encode()).hexdigest(),
        **{
            label: sha256(program.encode()).hexdigest()
            for label, program in programs.items()
        },
    }
    require(hashes == EXPECTED_HASHES,
            ("the special factor ledgers changed", hashes))
    payloads = {}
    for label, program in programs.items():
        result = run(
            (executable, "-q"), input=program, text=True,
            capture_output=True, timeout=120, check=False,
        )
        require(result.returncode == 0,
                ("Singular failed on the special factor ideal",
                 label, result.stderr))
        payload = tuple(line.strip() for line in result.stdout.splitlines()
                        if line.strip())
        require(payload == ("1", "1"),
                ("the special factor ideal stopped being unit",
                 label, payload))
        payloads[label] = payload
    return hashes, payloads


def main():
    packet, u_star, v_star, _repair = SIX["repaired_member"]()
    selected_checks = SIX["audit_selected_equations"](packet, SELECTED)
    literal_checks = SIX["audit_literal_slices"](
        packet, u_star, v_star, SELECTED
    )
    witness = SIX["audit_capable_root"](packet, ROOT)
    data, modes = l1_star_bases(packet)
    incidence = audit_linear_incidence(packet, modes)
    equations = factor_equations(packet, modes)
    hashes, payloads = audit_unit_ideals(equations)
    print("rank-51 special one-rank-one L1 factor obstruction: passed")
    print(f"  selected/literal checks      : {selected_checks}/{literal_checks}")
    print(f"  root-2 R2 witnesses          : {witness}")
    print(f"  L1 system data               : {data}")
    print(f"  linear incidence ranks       : {incidence}")
    print(f"  variables/equations          : {len(VARIABLES)}/{len(equations)}")
    print(f"  exact unit payloads          : {payloads}")
    print(f"  ledger hashes                : {hashes}")
    print("  conclusion                   : linear span survives; factorization fails")


if __name__ == "__main__":
    main()
