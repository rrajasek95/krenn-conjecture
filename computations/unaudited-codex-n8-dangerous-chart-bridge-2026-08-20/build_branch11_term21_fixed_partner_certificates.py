#!/usr/bin/env python3
"""Build exact arbitrary-mate units for the two generic (11,21) lines."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "unaudited-codex-n8-orbit0-normalized-78-2026-08-20"
OUT = HERE / "certificate_branch11_term21_fixed_partner_units.json"
X_SUPPORT = (0, 1, 2, 4, 5, 7, 8, 9, 10, 12, 13, 15, 16, 17, 18,
             20, 23)
Q_ZEROS = (1, 4, 5, 7, 8, 9, 11, 12, 13, 14, 15)
LEFT_C = {
    "v_equals_r_minus_2": (3, 9, 10, 12, 15, 21),
    "v_equals_minus_r": (3, 4, 7, 17, 18, 21),
}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CORE = load("n8_b11t21_cert_core", SOURCE / "audit_polarized_superpair_core_identity.py")
PROBE = load("n8_b11t21_cert_probe", SOURCE / "probe_cofactor_orientation_classes.py")
H = CORE.pure_hafnian()


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def q(value):
    return CORE.q_orientation(tuple((value >> (3 - site)) & 1
                                    for site in range(4)))


def rows():
    result = []
    result.extend(("e_" + "".join(map(str, edge)), CORE.e_pair(*edge))
                  for edge in CORE.SUPER_EDGES)
    result.extend(("t_" + "".join(map(str, triple)),
                   CORE.t_triple(*triple))
                  for triple in combinations(range(4), 3))
    result.extend((f"cofactor_{index}", PROBE.derivative(H, index))
                  for index in X_SUPPORT)
    result.extend((f"Q_{value}", q(value)) for value in Q_ZEROS)
    require(len(result) == 38, "forced mate row count changed")
    return tuple(result)


ROWS = rows()


def specialize(poly, cells):
    cells = frozenset(cells)
    return Counter({monomial: coefficient for monomial, coefficient in poly.items()
                    if not any(variable in cells for variable in monomial)})


def lift_one(name, cells):
    specialized = tuple((label, specialize(poly, cells))
                        for label, poly in ROWS)
    variables = tuple(f"x{index}" for index in range(24)
                      if index not in cells)
    ideal = ",".join(PROBE.singular(poly) for _, poly in specialized)
    prints = ";".join(
        f'print("BEGIN_{index}");print(string(L[{index + 1},1]));'
        f'print("END_{index}")' for index in range(len(specialized))
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
    require(completed.returncode == 0 and not completed.stderr.strip(),
            name + " lift failed: " + completed.stderr[-1000:])
    require("IDENTITY_PASS" in completed.stdout.split(),
            name + " lift did not replay")
    coefficients = []
    for index in range(len(specialized)):
        begin, end = f"BEGIN_{index}\n", f"\nEND_{index}"
        require(begin in completed.stdout,
                f"missing coefficient marker {index}")
        tail = completed.stdout.split(begin, 1)[1]
        require(end in tail, f"missing coefficient end marker {index}")
        coefficients.append(tail.split(end, 1)[0].strip())
    return {
        "component": name,
        "forced_partner_zero_cells": list(cells),
        "variables_in_ring_order": list(variables),
        "generators": [
            {"label": label, "polynomial": PROBE.singular(poly),
             "coefficient": coefficient}
            for (label, poly), coefficient in zip(specialized, coefficients)
        ],
        "generator_count": len(specialized),
        "nonzero_coefficient_count": sum(value != "0"
                                         for value in coefficients),
        "coefficient_character_count": sum(len(value)
                                           for value in coefficients),
    }


def main():
    components = [lift_one(name, cells) for name, cells in LEFT_C.items()]
    result = {
        "status": "UNAUDITED frozen exact-Q (11,21) arbitrary-mate units",
        "fixed_left_stratum": (
            "aligned branch 11 / permanent-term 21, either irreducible "
            "line, with T nonzero"
        ),
        "fixed_left_supports": {
            "entry_indices": list(X_SUPPORT),
            "Q_indices": [0, 1, 2, 3, 4, 6, 7, 8, 10, 11, 14],
            "cofactor_indices_by_component": {
                key: list(value) for key, value in LEFT_C.items()
            },
        },
        "partner_forced_rows": {
            "base": "six e and four t rows",
            "cofactors": list(X_SUPPORT),
            "Q_indices": list(Q_ZEROS),
            "cells": "the six component-specific live left cofactors",
        },
        "identity": "for each component, sum_i coefficient_i*generator_i=1",
        "components": components,
        "conclusion": (
            "No T-nonzero point on either (11,21) irreducible line has an "
            "arbitrary second-colour mate satisfying the diagonal "
            "78+48+144 packet. No partner H localization or partner aligned "
            "chart is assumed."
        ),
        "scope": (
            "Each certificate is written after quotienting by the six forced "
            "partner cell equations. The independent auditor restores their "
            "literal full-ring provenance and tests a coefficient mutation."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("(11,21) fixed-partner certificates built: PASS")
    for row in components:
        print(row["component"], row["generator_count"],
              row["nonzero_coefficient_count"],
              row["coefficient_character_count"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
