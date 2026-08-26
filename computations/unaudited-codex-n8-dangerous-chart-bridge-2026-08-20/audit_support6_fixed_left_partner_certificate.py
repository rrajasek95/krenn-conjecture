#!/usr/bin/env python3
"""Independent exact replay of the frozen fixed-left mate certificate."""

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
CERT = HERE / "certificate_support6_fixed_left_partner_unit.json"
OUT = HERE / "results_support6_fixed_left_partner_certificate_audit.json"
ZERO_CELLS = frozenset((9, 10, 13, 14))
Q_ZEROS = (3, 5, 6, 9, 10, 12)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CORE = load("n8_s6_replay_core", CORE_PATH)
PROBE = load("n8_s6_replay_probe", PROBE_PATH)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def specialize(poly):
    return Counter({monomial: coefficient for monomial, coefficient in poly.items()
                    if not any(variable in ZERO_CELLS for variable in monomial)})


def literal_rows():
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
    return tuple((label, PROBE.singular(specialize(poly)))
                 for label, poly in answer)


def main():
    certificate = json.loads(CERT.read_text())
    claimed_digest = certificate.pop("result_sha256")
    logical = json.dumps(certificate, sort_keys=True, separators=(",", ":"))
    require(sha256(logical.encode("ascii")).hexdigest() == claimed_digest,
            "certificate logical digest mismatch")
    certificate["result_sha256"] = claimed_digest

    literal = literal_rows()
    stored = tuple((row["label"], row["polynomial"])
                   for row in certificate["generators"])
    require(stored == literal, "stored generators differ from literal rows")
    variables = tuple(f"x{index}" for index in range(24)
                      if index not in ZERO_CELLS)
    require(certificate["variables_in_ring_order"] == list(variables),
            "ring-variable order mismatch")

    definitions = []
    terms = []
    for index, row in enumerate(certificate["generators"]):
        definitions.append(f"poly g{index}=({row['polynomial']})")
        definitions.append(f"poly c{index}=({row['coefficient']})")
        terms.append(f"c{index}*g{index}")
    command = (
        f"ring R=0,({','.join(variables)}),dp; "
        + ";".join(definitions) + ";"
        + f"poly residue={'+'.join(terms)}-1; "
        + "if(residue==0){print(\"IDENTITY_PASS\");}"
        + "else{print(\"IDENTITY_FAIL\");}; "
        + "poly mutation=residue+g0; "
        + "if(mutation!=0){print(\"MUTATION_PASS\");}"
        + "else{print(\"MUTATION_FAIL\");}; quit;"
    )
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=60, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            "Singular replay error: " + completed.stderr[-1000:])
    tokens = completed.stdout.split()
    require("IDENTITY_PASS" in tokens and "MUTATION_PASS" in tokens,
            "certificate replay or mutation failed")

    result = {
        "status": "UNAUDITED exact-Q fixed-left certificate audit PASS",
        "certificate_logical_sha256": claimed_digest,
        "generator_count": len(literal),
        "nonzero_coefficient_count": certificate[
            "nonzero_coefficient_count"],
        "coefficient_character_count": certificate[
            "coefficient_character_count"],
        "literal_generator_match": True,
        "exact_identity_replay": True,
        "coefficient_mutation_control": True,
        "scope": certificate["scope"],
    }
    result_logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(
        result_logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("support-six fixed-left certificate audit: PASS")
    print("generators / nonzero coefficients / characters:",
          result["generator_count"], result["nonzero_coefficient_count"],
          result["coefficient_character_count"])
    print("certificate / audit logical sha256:", claimed_digest,
          result["result_sha256"])


if __name__ == "__main__":
    main()
