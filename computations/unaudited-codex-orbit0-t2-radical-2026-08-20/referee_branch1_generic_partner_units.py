#!/usr/bin/env python3
"""Independent bridge and exact replay for branch-1 generic partner units."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CORE_PATH = (ROOT / "computations" /
             "unaudited-codex-n8-orbit0-normalized-78-2026-08-20" /
             "audit_polarized_superpair_core_identity.py")
CLASSIFICATION = HERE / "results_referee_branch1_dzero_classification.json"
PRODUCER_CLASSIFICATION = (ROOT / "computations" /
    "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
    "results_branch1_dzero_classification.json")
CERTIFICATE = (ROOT / "computations" /
    "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
    "certificate_branch1_generic_fixed_partner_units.json")
OUT = HERE / "results_referee_branch1_generic_partner_units.json"
Q_BAR = lambda index: 15 - index


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


CORE = load("n8_b1_partner_referee_core", CORE_PATH)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def derivative(poly, variable_index):
    answer = Counter()
    for monomial, coefficient in poly.items():
        multiplicity = monomial.count(variable_index)
        if multiplicity:
            reduced = list(monomial)
            reduced.remove(variable_index)
            answer[tuple(reduced)] += multiplicity * coefficient
    return CORE.clean(answer)


def q_row(index):
    bits = tuple((index >> (3 - site)) & 1 for site in range(4))
    return CORE.q_orientation(bits)


def specialize(poly, zero_cells):
    zero_cells = frozenset(zero_cells)
    return Counter({monomial: coefficient for monomial, coefficient in poly.items()
                    if not any(variable in zero_cells for variable in monomial)})


def singular(poly):
    if not poly:
        return "0"
    terms = []
    for monomial, coefficient in sorted(poly.items()):
        body = "*".join(f"x{variable}" for variable in monomial) or "1"
        terms.append(f"({coefficient})*{body}")
    return "+".join(terms)


def literal_rows(q_zeros):
    h = CORE.pure_hafnian()
    rows = [("e_" + "".join(map(str, edge)), CORE.e_pair(*edge))
            for edge in CORE.SUPER_EDGES]
    rows += [("t_" + "".join(map(str, triple)), CORE.t_triple(*triple))
             for triple in combinations(range(4), 3)]
    rows += [(f"cofactor_{edge}_{position}",
              derivative(h, 4 * edge + position))
             for edge in range(6) for position in (0, 1, 2)]
    rows += [(f"Q_{index}", q_row(index)) for index in q_zeros]
    return tuple(rows)


def decode_pt(record):
    return {item["T_degree"]:
            tuple(Fraction(numerator, denominator)
                  for numerator, denominator in item["coefficient_1_z"])
            for item in record}


def generic_nonzero(record):
    return bool(decode_pt(record))


def replay_identity(component, q_zeros):
    cells = tuple(component["forced_partner_zero_cells"])
    rebuilt = tuple((label, singular(specialize(poly, cells)))
                    for label, poly in literal_rows(q_zeros))
    stored = tuple((row["label"], row["polynomial"])
                   for row in component["generators"])
    require(rebuilt == stored, component["component"] + " raw row mismatch")
    variables = tuple(f"x{index}" for index in range(24) if index not in cells)
    require(variables == tuple(component["variables_in_ring_order"]),
            component["component"] + " ring order mismatch")
    declarations, terms = [], []
    for index, row in enumerate(component["generators"]):
        declarations += [f"poly g{index}=({row['polynomial']})",
                         f"poly c{index}=({row['coefficient']})"]
        terms.append(f"c{index}*g{index}")
    command = (f"ring R=0,({','.join(variables)}),dp;"
               + ";".join(declarations) + ";"
               + f"poly residue={'+'.join(terms)}-1;"
               + 'if(residue==0){print("PASS");}else{print("FAIL");};'
               + "poly mutation=residue+g0;"
               + 'if(mutation!=0){print("MUTATION");};quit;')
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=60, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            component["component"] + " exact replay failed")
    require("PASS" in completed.stdout.split()
            and "MUTATION" in completed.stdout.split(),
            component["component"] + " identity/mutation failed")
    return {
        "component": component["component"],
        "forced_partner_zero_cells": list(cells),
        "generator_count": len(rebuilt),
        "nonzero_certificate_coefficients": component["nonzero_coefficient_count"],
        "exact_identity_pass": True,
        "mutation_fired": True,
    }


def main():
    local_classification = json.loads(CLASSIFICATION.read_text())
    require(local_classification["result_sha256"] ==
            "fe7e46044fa3ea93bb3ca76c127267df55ae6e750872d042829a86d42cecb215",
            "independent branch1 referee digest changed")
    producer_classification = json.loads(PRODUCER_CLASSIFICATION.read_text())
    certificate = json.loads(CERTIFICATE.read_text())
    claimed = certificate.pop("result_sha256")
    logical = json.dumps(certificate, sort_keys=True, separators=(",", ":"))
    require(sha256(logical.encode("ascii")).hexdigest() == claimed,
            "partner certificate logical digest mismatch")
    certificate["result_sha256"] = claimed

    left_q_support = set(local_classification["component_replays"][0]
                         ["generic_Q_support"])
    require(all(set(row["generic_Q_support"]) == left_q_support
                for row in local_classification["component_replays"]),
            "branch1 components no longer have common generic Q support")
    q_zeros = tuple(sorted(Q_BAR(index) for index in left_q_support))
    require(q_zeros == (3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15),
            "Q-cross-compatible forced-zero set changed")

    expected_cells = []
    for record in producer_classification["components"]:
        cofactors = record["cofactor_polynomials"]
        support = tuple(index for index in range(24)
                        if generic_nonzero(cofactors[str(index)]))
        expected_cells.append(support)
    require(expected_cells == [(3, 5, 6, 17, 18),
                               (3, 9, 10, 13, 14)],
            "generic left cofactor support changed")
    require([tuple(row["forced_partner_zero_cells"])
             for row in certificate["components"]] == expected_cells,
            "certificate cells are not forced by left cofactor support")

    audits = [replay_identity(row, q_zeros)
              for row in certificate["components"]]
    result = {
        "status": "UNAUDITED independent branch1 generic partner-unit referee",
        "certificate_logical_sha256": claimed,
        "left_generic_X_support": (
            "positions 0,1,2 in each of six blocks (18 cells)"
        ),
        "left_generic_Q_support": sorted(left_q_support),
        "forced_partner_Q_zeros_under_bar": list(q_zeros),
        "left_component_cofactor_supports_equal_forced_partner_entry_zeros":
            [list(value) for value in expected_cells],
        "component_replays": audits,
        "conclusion": (
            "Neither generic T!=0 branch1 component has a packet-compatible "
            "partner: the support-forced mate ideal is the unit ideal over Q."
        ),
        "scope": (
            "The certificates apply to the two classified uniform d=0 "
            "components. They do not classify the surrounding 24-variable "
            "branch1 chart or rule out unrelated support-at-most-five strata."
        ),
    }
    result_logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(result_logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch1 generic partner-unit independent referee: PASS")
    print("components / forced Q zeros:", len(audits), len(q_zeros))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
