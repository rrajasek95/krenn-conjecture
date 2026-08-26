#!/usr/bin/env python3
"""Referee the exact arbitrary-partner unit that dominates the Q0 pullback."""

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
ROOT = HERE.parent.parent
SOURCE = HERE.parent / "unaudited-codex-n8-orbit0-normalized-78-2026-08-20"
DANGEROUS = HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
LEFT_PATH = SOURCE / "audit_weight0_support6_char0_component.py"
CORE_PATH = SOURCE / "audit_polarized_superpair_core_identity.py"
PROBE_PATH = SOURCE / "probe_cofactor_orientation_classes.py"
CERT_PATH = DANGEROUS / "certificate_support6_fixed_left_partner_unit.json"
OUT = HERE / "results_support6_cross_orbit_pullback_unit.json"
Q_ZEROS = (3, 5, 6, 9, 10, 12)
ZERO_CELLS = frozenset((9, 10, 13, 14))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


LEFT = load("Q_pullback_left", LEFT_PATH)
CORE = load("Q_pullback_core", CORE_PATH)
PROBE = load("Q_pullback_probe", PROBE_PATH)


def specialize(poly):
    return Counter({monomial: coefficient
                    for monomial, coefficient in poly.items()
                    if not any(variable in ZERO_CELLS for variable in monomial)})


def literal_right_rows():
    h = CORE.pure_hafnian()
    rows = []
    rows.extend(("e_"+"".join(map(str, edge)), CORE.e_pair(*edge))
                for edge in CORE.SUPER_EDGES)
    rows.extend(("t_"+"".join(map(str, triple)), CORE.t_triple(*triple))
                for triple in combinations(range(4), 3))
    rows.extend((f"cofactor_{edge}_{position}",
                 PROBE.derivative(h, 4*edge+position))
                for edge in range(6) for position in (1, 2))
    rows.extend((f"Q_{value}", CORE.q_orientation(tuple(
        (value >> (3-site)) & 1 for site in range(4))))
                for value in Q_ZEROS)
    return tuple((label, specialize(poly)) for label, poly in rows)


def left_supports():
    entries = LEFT.raw_entries()
    _, hafnian = LEFT.SCREEN.PROBE.equations(LEFT.SCREEN.branch_bits(51))
    cofactors = tuple(LEFT.evaluate(LEFT.derivative(hafnian, variable), entries)
                      for variable in range(24))
    q_values = tuple(LEFT.evaluate(LEFT.SCREEN.q_poly(index), entries)
                     for index in range(16))
    entry_support = tuple(index for index, value in enumerate(entries)
                          if value != LEFT.ZERO)
    cofactor_support = tuple(index for index, value in enumerate(cofactors)
                             if value != LEFT.ZERO)
    q_support = tuple(index for index, value in enumerate(q_values)
                      if value != LEFT.ZERO)
    require(entry_support == tuple(4*edge+position
                                   for edge in range(6)
                                   for position in (1, 2)),
            "left entry support changed")
    require(cofactor_support == tuple(sorted(ZERO_CELLS)),
            "left cofactor support changed")
    require(q_support == Q_ZEROS
            and tuple(15-index for index in reversed(q_support)) == q_support,
            "left Q support/complement invariance changed")
    return entries, cofactors, q_values, entry_support, cofactor_support, q_support


def replay_certificate(rows):
    certificate = json.loads(CERT_PATH.read_text())
    claimed = certificate.pop("result_sha256")
    logical = json.dumps(certificate, sort_keys=True, separators=(",", ":"))
    require(sha256(logical.encode("ascii")).hexdigest() == claimed,
            "certificate logical digest mismatch")
    certificate["result_sha256"] = claimed
    require(claimed == "a17794ac82f6d4616af28fcf583567f1f92cc67de126b0cfe0b08b279d5cbd87",
            "certificate digest changed")
    literal = tuple((label, PROBE.singular(poly)) for label, poly in rows)
    stored = tuple((record["label"], record["polynomial"])
                   for record in certificate["generators"])
    require(stored == literal, "certificate rows differ from literal source")
    variables = tuple(f"x{index}" for index in range(24)
                      if index not in ZERO_CELLS)
    require(certificate["variables_in_ring_order"] == list(variables),
            "certificate ring order changed")

    definitions = []
    summands = []
    for index, record in enumerate(certificate["generators"]):
        definitions.append(f"poly g{index}=({record['polynomial']})")
        definitions.append(f"poly c{index}=({record['coefficient']})")
        summands.append(f"c{index}*g{index}")
    command = (
        f"ring R=0,({','.join(variables)}),dp; "
        + ";".join(definitions) + ";"
        + f"poly residue={'+'.join(summands)}-1; "
        + "if(residue==0){print(\"IDENTITY_PASS\");}"
        + "else{print(\"IDENTITY_FAIL\");}; "
        + "poly source_mutation=residue+g27; "
        + "if(source_mutation!=0){print(\"MUTATION_PASS\");}"
        + "else{print(\"MUTATION_FAIL\");}; quit;")
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=60, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            "Singular replay failed: "+completed.stderr[-1000:])
    tokens = completed.stdout.split()
    require("IDENTITY_PASS" in tokens and "MUTATION_PASS" in tokens,
            "exact identity/mutation replay failed")
    return certificate


def main():
    HERE.mkdir(parents=True, exist_ok=True)
    (_, _, _, entry_support, cofactor_support,
     q_support) = left_supports()
    rows = literal_right_rows()
    require(len(rows) == 28, "right unit core row count changed")
    certificate = replay_certificate(rows)
    labels = [label for label, _ in rows]
    require(labels[:6] == ["e_01", "e_02", "e_03",
                           "e_12", "e_13", "e_23"]
            and labels[6:10] == ["t_012", "t_013", "t_023", "t_123"],
            "permanent/triangle source order changed")

    result = {
        "status": "UNAUDITED exact support6 cross-orbit pullback UNIT PASS",
        "frozen_left": {
            "field": "Q[z]/(z^2+2z-1)",
            "entry_support": list(entry_support),
            "cofactor_support": list(cofactor_support),
            "Q_support": list(q_support),
            "Q_support_complement_invariant": True,
        },
        "directional_packet_reduction": {
            "X_left_times_C_right": (
                "the twelve nonzero left offdiagonal entries force all "
                "twelve right offdiagonal cofactor rows to zero"),
            "X_right_times_C_left": (
                "the four nonzero left cofactors force right cells "
                "x9,x10,x13,x14 to zero"),
            "Q_left_times_Q_right_complement": (
                "the complement-invariant left support forces right "
                "Q3,Q5,Q6,Q9,Q10,Q12 to zero"),
        },
        "right_core": {
            "ambient": "Q[x0,...,x23]/(x9,x10,x13,x14)",
            "permanent_rows": 6,
            "triangle_rows": 4,
            "offdiagonal_cofactor_rows": 12,
            "Q_rows": 6,
            "generator_count": len(rows),
            "pure_H_localizer": False,
            "right_Q_orbit_constraint": False,
        },
        "certificate": {
            "logical_sha256": certificate["result_sha256"],
            "nonzero_coefficient_count": certificate[
                "nonzero_coefficient_count"],
            "coefficient_character_count": certificate[
                "coefficient_character_count"],
            "identity": "sum_i coefficient_i*generator_i=1",
            "literal_source_match": True,
            "exact_replay": True,
            "mutation_control": True,
        },
        "conclusion": (
            "The fixed support-six left record has no arbitrary right "
            "six-block partner satisfying permanent, triangle, both "
            "directional entry/cofactor, and Q compatibility. This strictly "
            "contains and therefore empties both six-dimensional right-Q0 "
            "orbit pullback families from the cross-orbit calculation."),
        "dimension_and_screen_guard": (
            "The exact unit makes the requested tangent/dimension and "
            "large-prime discovery screen unnecessary: the source scheme is "
            "already empty over Q, before H liveness or orbit restriction."),
        "scope_guard": (
            "This closes partners for this exact frozen support-six left "
            "presentation and all its covariant relabellings. It is not a "
            "statement for every tensor in the broader support-six invariant "
            "stratum without transporting the full X/C presentation."),
        "source_hashes": {
            "left": sha256(LEFT_PATH.read_bytes()).hexdigest(),
            "core": sha256(CORE_PATH.read_bytes()).hexdigest(),
            "probe": sha256(PROBE_PATH.read_bytes()).hexdigest(),
            "certificate_file": sha256(CERT_PATH.read_bytes()).hexdigest(),
        },
        "must_fire": [
            "left X/C/Q supports",
            "Q support complement invariance",
            "28 literal right rows",
            "certificate logical digest",
            "exact coefficient identity",
            "source coefficient mutation",
        ],
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("support6 cross-orbit pullback unit: PASS")
    print("rows/coefficients/chars:", len(rows),
          certificate["nonzero_coefficient_count"],
          certificate["coefficient_character_count"])
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
