#!/usr/bin/env python3
"""Build frozen exact-Q mate-unit certificates for branch-1 T!=0."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "unaudited-codex-n8-orbit0-normalized-78-2026-08-20"
OUT = HERE / "certificate_branch1_generic_fixed_partner_units.json"
Q_ZEROS = (3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15)
LEFT_C = {"z2_minus_14z_minus_1": (3, 5, 6, 17, 18),
          "z2_plus_2z_minus_1": (3, 9, 10, 13, 14)}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CORE = load("n8_b1_cert_core", SOURCE / "audit_polarized_superpair_core_identity.py")
PROBE = load("n8_b1_cert_probe", SOURCE / "probe_cofactor_orientation_classes.py")
H = CORE.pure_hafnian()


def q(value):
    return CORE.q_orientation(tuple((value >> (3 - site)) & 1
                                    for site in range(4)))


def literal_rows():
    rows = []
    rows.extend(("e_" + "".join(map(str, edge)), CORE.e_pair(*edge))
                for edge in CORE.SUPER_EDGES)
    rows.extend(("t_" + "".join(map(str, triple)),
                 CORE.t_triple(*triple))
                for triple in combinations(range(4), 3))
    rows.extend((f"cofactor_{edge}_{position}",
                 PROBE.derivative(H, 4 * edge + position))
                for edge in range(6) for position in (0, 1, 2))
    rows.extend((f"Q_{value}", q(value)) for value in Q_ZEROS)
    return tuple(rows)


ROWS = literal_rows()


def specialize(poly, cells):
    cells = frozenset(cells)
    return Counter({monomial: coefficient for monomial, coefficient in poly.items()
                    if not any(variable in cells for variable in monomial)})


def lift_one(name, cells):
    rows = tuple((label, specialize(poly, cells)) for label, poly in ROWS)
    variables = tuple(f"x{index}" for index in range(24)
                      if index not in cells)
    ideal = ",".join(PROBE.singular(poly) for _, poly in rows)
    prints = ";".join(
        f'print("BEGIN_{index}");print(string(L[{index + 1},1]));'
        f'print("END_{index}")' for index in range(len(rows))
    )
    command = (
        f"ring R=0,({','.join(variables)}),dp; ideal I={ideal}; "
        "matrix L=lift(I,ideal(1)); ideal J=matrix(I)*L; "
        "poly residue=J[1]-1; "
        'if(residue==0){print("IDENTITY_PASS");}'
        'else{print("IDENTITY_FAIL");};'
        f"{prints}; quit;"
    )
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=120, check=False)
    if completed.returncode != 0 or completed.stderr.strip():
        raise RuntimeError(name + " lift failed: " + completed.stderr[-1000:])
    if "IDENTITY_PASS" not in completed.stdout.split():
        raise RuntimeError(name + " lift did not replay")
    coefficients = []
    for index in range(len(rows)):
        begin, end = f"BEGIN_{index}\n", f"\nEND_{index}"
        tail = completed.stdout.split(begin, 1)[1]
        coefficients.append(tail.split(end, 1)[0].strip())
    return {
        "component": name,
        "forced_partner_zero_cells": list(cells),
        "variables_in_ring_order": list(variables),
        "generators": [
            {"label": label, "polynomial": PROBE.singular(poly),
             "coefficient": coefficient}
            for (label, poly), coefficient in zip(rows, coefficients)
        ],
        "generator_count": len(rows),
        "nonzero_coefficient_count": sum(value != "0"
                                         for value in coefficients),
        "coefficient_character_count": sum(len(value)
                                           for value in coefficients),
    }


def main():
    components = [lift_one(name, cells) for name, cells in LEFT_C.items()]
    result = {
        "status": "UNAUDITED frozen exact-Q branch-1 mate units",
        "fixed_left_stratum": (
            "branch-1 uniform-d-zero component with T nonzero and Q support 11"
        ),
        "partner_forced_rows": {
            "base": "six e and four t rows",
            "cofactors": "positions 0,1,2 in every partner block (18 rows)",
            "Q_indices": list(Q_ZEROS),
            "cells": "component-specific five nonzero left cofactors",
        },
        "identity": "for each component, sum_i coefficient_i*generator_i=1",
        "components": components,
        "conclusion": (
            "Neither T-nonzero irreducible left component has any arbitrary "
            "partner satisfying the diagonal 78+48+144 packet. No partner H "
            "localization or cofactor branch is assumed."
        ),
        "scope": (
            "The certificates live in the quotient by the five forced "
            "partner cell equations; adjoining those cells gives the literal "
            "full-ring Nullstellensatz."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-1 generic fixed-partner certificates built: PASS")
    for row in components:
        print(row["component"], row["generator_count"],
              row["nonzero_coefficient_count"],
              row["coefficient_character_count"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
