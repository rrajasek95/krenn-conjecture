#!/usr/bin/env python3
"""Build a frozen exact-Q Nullstellensatz certificate for a fixed mate.

This builder uses Singular's exact ``lift`` once.  The separate audit script
reconstructs every literal generator and replays the frozen coefficients.
"""

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
CORE_PATH = SOURCE / "audit_polarized_superpair_core_identity.py"
PROBE_PATH = SOURCE / "probe_cofactor_orientation_classes.py"
OUT = HERE / "certificate_support6_fixed_left_partner_unit.json"
ZERO_CELLS = frozenset((9, 10, 13, 14))
Q_ZEROS = (3, 5, 6, 9, 10, 12)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CORE = load("n8_s6_cert_core", CORE_PATH)
PROBE = load("n8_s6_cert_probe", PROBE_PATH)


def specialize(poly):
    return Counter({monomial: coefficient for monomial, coefficient in poly.items()
                    if not any(variable in ZERO_CELLS for variable in monomial)})


def rows():
    h = CORE.pure_hafnian()
    answer = []
    answer.extend(("e_" + "".join(map(str, edge)), CORE.e_pair(*edge))
                  for edge in CORE.SUPER_EDGES)
    answer.extend(("t_" + "".join(map(str, triple)),
                   CORE.t_triple(*triple))
                  for triple in combinations(range(4), 3))
    answer.extend((f"cofactor_{edge}_{position}",
                   PROBE.derivative(h, 4 * edge + position))
                  for edge in range(6) for position in (1, 2))
    answer.extend((f"Q_{value}", CORE.q_orientation(tuple(
        (value >> (3 - site)) & 1 for site in range(4))))
                  for value in Q_ZEROS)
    return tuple((label, specialize(poly)) for label, poly in answer)


def main():
    generators = rows()
    variables = tuple(f"x{index}" for index in range(24)
                      if index not in ZERO_CELLS)
    variable_text = ",".join(variables)
    ideal_text = ",".join(PROBE.singular(poly)
                          for _, poly in generators)
    prints = ";".join(
        f'print("BEGIN_{index}");'
        f'print(string(L[{index + 1},1]));'
        f'print("END_{index}")'
        for index in range(len(generators))
    )
    command = (
        f"ring R=0,({variable_text}),dp; ideal I={ideal_text}; "
        "matrix L=lift(I,ideal(1)); ideal J=matrix(I)*L; "
        "poly residue=J[1]-1; "
        "if(residue==0){print(\"IDENTITY_PASS\");}"
        "else{print(\"IDENTITY_FAIL\");};"
        f"{prints}; quit;"
    )
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=120, check=False)
    if completed.returncode != 0 or completed.stderr.strip():
        raise RuntimeError("Singular lift failed: " + completed.stderr[-2000:])
    if "IDENTITY_PASS" not in completed.stdout.split():
        raise RuntimeError("Singular did not verify its lifted identity")

    coefficients = []
    for index in range(len(generators)):
        begin = f"BEGIN_{index}\n"
        end = f"\nEND_{index}"
        if begin not in completed.stdout:
            raise RuntimeError(f"missing coefficient marker {index}")
        tail = completed.stdout.split(begin, 1)[1]
        if end not in tail:
            raise RuntimeError(f"missing coefficient end marker {index}")
        coefficients.append(tail.split(end, 1)[0].strip())

    result = {
        "status": "UNAUDITED frozen exact-Q Nullstellensatz certificate",
        "ambient_quotient_ring": (
            "Q[x0,...,x23]/(x9,x10,x13,x14), dp order"
        ),
        "variables_in_ring_order": list(variables),
        "fixed_left_consequences": {
            "partner_zero_cells_from_X_partner_times_C_left":
                sorted(ZERO_CELLS),
            "partner_zero_cofactors_from_X_left_times_C_partner":
                [4 * edge + position for edge in range(6)
                 for position in (1, 2)],
            "partner_zero_Q_coordinates": list(Q_ZEROS),
        },
        "identity": "sum_i coefficient_i * generator_i = 1",
        "generators": [
            {"label": label, "polynomial": PROBE.singular(poly),
             "coefficient": coefficient}
            for (label, poly), coefficient in zip(generators, coefficients)
        ],
        "generator_count": len(generators),
        "nonzero_coefficient_count": sum(value != "0"
                                         for value in coefficients),
        "coefficient_character_count": sum(len(value)
                                           for value in coefficients),
        "conclusion": (
            "The fixed support-six left colour has no partner satisfying "
            "the literal diagonal e/t, 4+4 Q, and both directional 6+2 "
            "cofactor packets. No pure-H localization is needed."
        ),
        "scope": (
            "This fixes the exact support-six left point and leaves the "
            "partner in all 24 block variables; no partner branch or "
            "cofactor orientation is assumed."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("support-six fixed-left certificate built: PASS")
    print("generators / nonzero coefficients / characters:",
          len(generators), result["nonzero_coefficient_count"],
          result["coefficient_character_count"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
