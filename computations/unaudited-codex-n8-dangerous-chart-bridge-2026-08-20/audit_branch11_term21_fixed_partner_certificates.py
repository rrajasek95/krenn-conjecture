#!/usr/bin/env python3
"""Independent replay of the two exact (11,21) arbitrary-mate units."""

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
CERT = HERE / "certificate_branch11_term21_fixed_partner_units.json"
OUT = HERE / "results_branch11_term21_fixed_partner_certificates_audit.json"
X_SUPPORT = (0, 1, 2, 4, 5, 7, 8, 9, 10, 12, 13, 15, 16, 17, 18,
             20, 23)
Q_ZEROS = (1, 4, 5, 7, 8, 9, 11, 12, 13, 14, 15)
EXPECTED_CELLS = {
    "v_equals_r_minus_2": (3, 9, 10, 12, 15, 21),
    "v_equals_minus_r": (3, 4, 7, 17, 18, 21),
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CORE = load("n8_b11t21_replay_core", SOURCE / "audit_polarized_superpair_core_identity.py")
PROBE = load("n8_b11t21_replay_probe", SOURCE / "probe_cofactor_orientation_classes.py")
H = CORE.pure_hafnian()


def q(value):
    return CORE.q_orientation(tuple((value >> (3 - site)) & 1
                                    for site in range(4)))


def literal_rows():
    rows = []
    rows.extend(("e_" + "".join(map(str, edge)), CORE.e_pair(*edge))
                for edge in CORE.SUPER_EDGES)
    rows.extend(("t_" + "".join(map(str, triple)), CORE.t_triple(*triple))
                for triple in combinations(range(4), 3))
    rows.extend((f"cofactor_{index}", PROBE.derivative(H, index))
                for index in X_SUPPORT)
    rows.extend((f"Q_{value}", q(value)) for value in Q_ZEROS)
    require(len(rows) == 38, "independent literal row count changed")
    return tuple(rows)


ROWS = literal_rows()


def specialize(poly, cells):
    cells = frozenset(cells)
    return Counter({monomial: coefficient for monomial, coefficient in poly.items()
                    if not any(variable in cells for variable in monomial)})


def replay_component(row):
    name = row["component"]
    cells = tuple(row["forced_partner_zero_cells"])
    require(cells == EXPECTED_CELLS[name], name + " forced cells changed")
    quotient_rows = tuple((label, PROBE.singular(specialize(poly, cells)))
                          for label, poly in ROWS)
    stored = tuple((record["label"], record["polynomial"])
                   for record in row["generators"])
    require(stored == quotient_rows, name + " quotient rows changed")
    variables = tuple(f"x{index}" for index in range(24) if index not in cells)
    require(row["variables_in_ring_order"] == list(variables),
            name + " quotient variable order changed")

    definitions, summands = [], []
    first_nonzero = None
    for index, record in enumerate(row["generators"]):
        definitions += [f"poly g{index}=({record['polynomial']})",
                        f"poly c{index}=({record['coefficient']})"]
        summands.append(f"c{index}*g{index}")
        if first_nonzero is None and record["coefficient"] != "0":
            first_nonzero = index
    require(first_nonzero is not None, name + " certificate is empty")
    command = (
        f"ring R=0,({','.join(variables)}),dp; " + ";".join(definitions)
        + ";poly residue=" + "+".join(summands) + "-1;"
        + 'if(residue==0){print("IDENTITY_PASS");}'
        + 'else{print("IDENTITY_FAIL");};'
        + f"poly mutation=residue-2*c{first_nonzero}*g{first_nonzero};"
        + 'if(mutation!=0){print("MUTATION_PASS");}'
        + 'else{print("MUTATION_FAIL");};quit;'
    )
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=60, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            name + " quotient replay failed: " + completed.stderr[-1000:])
    require({"IDENTITY_PASS", "MUTATION_PASS"} <= set(completed.stdout.split()),
            name + " quotient identity/mutation failed")

    # Restore literal full-ring rows.  The quotient coefficients do not use
    # the forced cells, so the full residual must reduce to zero modulo those
    # six literal cell generators.
    full_variables = tuple(f"x{index}" for index in range(24))
    full_definitions, full_summands = [], []
    for index, ((label, raw), record) in enumerate(zip(ROWS, row["generators"])):
        require(label == record["label"], name + " label order changed")
        full_definitions += [f"poly G{index}=({PROBE.singular(raw)})",
                             f"poly C{index}=({record['coefficient']})"]
        full_summands.append(f"C{index}*G{index}")
    cell_ideal = ",".join(f"x{index}" for index in cells)
    full_command = (
        f"ring R=0,({','.join(full_variables)}),dp; "
        + ";".join(full_definitions)
        + ";poly residual=" + "+".join(full_summands) + "-1;"
        + f"ideal Z={cell_ideal};poly rem=reduce(residual,std(Z));"
        + 'if(rem==0){print("FULL_RING_PASS");}'
        + 'else{print("FULL_RING_FAIL");};quit;'
    )
    full = subprocess.run(["Singular", "-q", "-c", full_command],
                          text=True, capture_output=True,
                          timeout=60, check=False)
    require(full.returncode == 0 and not full.stderr.strip()
            and "FULL_RING_PASS" in full.stdout.split(),
            name + " full-ring residual replay failed")
    return {
        "component": name,
        "generator_count": len(ROWS),
        "nonzero_coefficient_count": row["nonzero_coefficient_count"],
        "coefficient_character_count": row["coefficient_character_count"],
        "quotient_identity_replay": True,
        "literal_full_ring_residual_is_zero_cell_multiple": True,
        "coefficient_sign_mutation_detected": True,
    }


def main():
    certificate = json.loads(CERT.read_text())
    claimed = certificate.pop("result_sha256")
    logical = json.dumps(certificate, sort_keys=True, separators=(",", ":"))
    require(sha256(logical.encode("ascii")).hexdigest() == claimed,
            "certificate logical digest mismatch")
    certificate["result_sha256"] = claimed
    audits = [replay_component(row) for row in certificate["components"]]
    result = {
        "status": "UNAUDITED independent (11,21) mate-unit audit PASS",
        "certificate_logical_sha256": claimed,
        "components": audits,
        "scope": certificate["scope"],
    }
    result_logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(result_logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("(11,21) fixed-partner certificate audit: PASS")
    for row in audits:
        print(row["component"], row["generator_count"],
              row["nonzero_coefficient_count"],
              row["coefficient_character_count"])
    print("certificate / audit logical sha256:", claimed,
          result["result_sha256"])


if __name__ == "__main__":
    main()
