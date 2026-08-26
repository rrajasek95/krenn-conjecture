#!/usr/bin/env python3
"""Replay the frozen exact-Q branch-1 T!=0 mate-unit certificates."""

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
CERT = HERE / "certificate_branch1_generic_fixed_partner_units.json"
OUT = HERE / "results_branch1_generic_fixed_partner_certificates_audit.json"
Q_ZEROS = (3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CORE = load("n8_b1_replay_core", SOURCE / "audit_polarized_superpair_core_identity.py")
PROBE = load("n8_b1_replay_probe", SOURCE / "probe_cofactor_orientation_classes.py")
H = CORE.pure_hafnian()


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


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


def replay_component(row):
    cells = tuple(row["forced_partner_zero_cells"])
    literal = tuple((label, PROBE.singular(specialize(poly, cells)))
                    for label, poly in ROWS)
    stored = tuple((item["label"], item["polynomial"])
                   for item in row["generators"])
    require(stored == literal, row["component"] + " literal rows changed")
    variables = tuple(f"x{index}" for index in range(24)
                      if index not in cells)
    require(row["variables_in_ring_order"] == list(variables),
            row["component"] + " variable order changed")
    definitions, terms = [], []
    for index, item in enumerate(row["generators"]):
        definitions.append(f"poly g{index}=({item['polynomial']})")
        definitions.append(f"poly c{index}=({item['coefficient']})")
        terms.append(f"c{index}*g{index}")
    command = (
        f"ring R=0,({','.join(variables)}),dp; "
        + ";".join(definitions) + ";"
        + f"poly residue={'+'.join(terms)}-1; "
        + 'if(residue==0){print("IDENTITY_PASS");}'
        + 'else{print("IDENTITY_FAIL");}; '
        + "poly mutation=residue+g0; "
        + 'if(mutation!=0){print("MUTATION_PASS");}'
        + 'else{print("MUTATION_FAIL");}; quit;'
    )
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=60, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            row["component"] + " Singular replay failed")
    tokens = completed.stdout.split()
    require("IDENTITY_PASS" in tokens and "MUTATION_PASS" in tokens,
            row["component"] + " identity/mutation failed")
    return {"component": row["component"],
            "generator_count": len(literal),
            "nonzero_coefficient_count": row["nonzero_coefficient_count"],
            "coefficient_character_count": row["coefficient_character_count"],
            "literal_replay": True, "mutation_control": True}


def main():
    certificate = json.loads(CERT.read_text())
    claimed = certificate.pop("result_sha256")
    logical = json.dumps(certificate, sort_keys=True, separators=(",", ":"))
    require(sha256(logical.encode("ascii")).hexdigest() == claimed,
            "certificate logical digest mismatch")
    certificate["result_sha256"] = claimed
    audits = [replay_component(row) for row in certificate["components"]]
    result = {
        "status": "UNAUDITED branch-1 generic mate certificate audit PASS",
        "certificate_logical_sha256": claimed,
        "components": audits,
        "scope": certificate["scope"],
    }
    result_logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(result_logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-1 generic fixed-partner certificate audit: PASS")
    for row in audits:
        print(row["component"], row["generator_count"],
              row["nonzero_coefficient_count"],
              row["coefficient_character_count"])
    print("certificate / audit logical sha256:", claimed,
          result["result_sha256"])


if __name__ == "__main__":
    main()
