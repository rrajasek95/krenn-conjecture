#!/usr/bin/env python3
"""Add each exact reconstructed eliminant factor to a modular D0 input."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
COMPUTATIONS = HERE.parent
sys.path.insert(0, str(COMPUTATIONS / "toolkit/groebner"))
from msolve_io import read_msolve_basis  # noqa: E402

SOURCE = HERE / "d0_pivot_sat_p536870879.ms"
FACTORS = HERE / "results_d0_eliminant_factor_reconstruction.json"
SATURATED_BASES = [
    (COMPUTATIONS / "unaudited-codex-root-integration-2026-08-20" /
     "msolve_d0_pivot_sat_p1073741827_full.out"),
    HERE / "d0_pivot_sat_p536870909_full.out",
    HERE / "d0_pivot_sat_p536870879_toolkit.sat.full.gb.out",
    HERE / "d0_pivot_sat_p536870869_toolkit.sat.full.gb.out",
    HERE / "d0_pivot_sat_p536870849_toolkit.sat.full.gb.out",
]


def factor_text(rows, prime):
    terms = []
    for row in rows:
        coefficient = Fraction(*row["coefficient"])
        residue = (coefficient.numerator *
                   pow(coefficient.denominator, -1, prime)) % prime
        factors = [str(residue)]
        if row["d1_degree"]:
            factors.append("d1^" + str(row["d1_degree"]))
        if row["d4_degree"]:
            factors.append("d4^" + str(row["d4_degree"]))
        terms.append("*".join(factors))
    return "+".join(terms)


def main():
    lines = SOURCE.read_text().splitlines()
    variables, prime = lines[:2]
    prime = int(prime)
    body = "\n".join(lines[2:]).strip()
    rows = [value.strip() for value in body.split(",") if value.strip()]
    if len(rows) != 5 or any(token in body for token in "()[];"):
        raise RuntimeError("source must be four expanded rows plus pivot")
    factors = json.loads(FACTORS.read_text())["factors"]
    for index, factor in enumerate(factors):
        output = HERE / f"d0_factor{index}_p{prime}.ms"
        value = [*rows[:-1], factor_text(factor["coefficients"], prime),
                 rows[-1]]
        output.write_text(variables + "\n" + str(prime) + "\n" +
                          ",\n".join(value) + "\n")
        print(output)

    # The existing full bases are already pivot-saturated.  Adding one
    # factor and running plain block elimination restricts to that component
    # without repeating the expensive F4SAT stage.
    for basis_path in SATURATED_BASES:
        basis = read_msolve_basis(basis_path, require_full=True)
        for index, factor in enumerate(factors):
            output = HERE / f"d0_factor{index}_p{basis.characteristic}_stage2.ms"
            rows = [*basis.polynomials,
                    factor_text(factor["coefficients"],
                                basis.characteristic)]
            output.write_text(
                ",".join(basis.variables) + "\n" +
                str(basis.characteristic) + "\n" +
                ",\n".join(rows) + "\n")
            print(output)

            raw_input = HERE / f"d0_pivot_sat_p{basis.characteristic}.ms"
            raw_lines = raw_input.read_text().splitlines()
            raw_rows = [value.strip() for value in
                        "\n".join(raw_lines[2:]).strip().split(",")
                        if value.strip()]
            if len(raw_rows) != 5:
                raise RuntimeError("raw input must end in its pivot row")
            resat = HERE / f"d0_factor{index}_p{basis.characteristic}_resat.ms"
            resat.write_text(
                ",".join(basis.variables) + "\n" +
                str(basis.characteristic) + "\n" +
                ",\n".join([*rows, raw_rows[-1]]) + "\n")
            print(resat)


if __name__ == "__main__":
    main()
