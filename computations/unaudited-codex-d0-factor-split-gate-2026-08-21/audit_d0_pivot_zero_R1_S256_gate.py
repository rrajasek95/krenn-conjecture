#!/usr/bin/env python3
"""Byte/source/involution replay of final O3 exact unit gate."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
EXPORTER = HERE / "export_d0_pivot_zero_R1_S256_gate.py"
EXPORT = HERE / "results_d0_pivot_zero_R1_S256_gate_export.json"
RUN = HERE / "results_d0_pivot_zero_R1_S256_exact_run.json"
INPUT = HERE / "d0_pivot_zero_R1_S256_char0.msolve"
OUTPUT = HERE / "d0_pivot_zero_R1_S256_char0.out"
O1_EXPORT = HERE / "results_d0_pivot_zero_R0_R1_gate_export.json"
O1_INPUT = HERE / "d0_pivot_zero_R0_R1_char0.msolve"
INTERFACE = HERE / "results_d0_pivot_zero_interface.json"
SYMMETRY = HERE / "results_d0_pivot_zero_symmetry.json"


def require(condition, message):
    if not condition: raise RuntimeError(message)


def digest(path): return sha256(path.read_bytes()).hexdigest()


def logical_hash(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def read_logical(path):
    value = json.loads(path.read_text()); frozen = value.pop("logical_sha256")
    require(logical_hash(value) == frozen, f"logical digest mismatch: {path.name}")
    return value, frozen


def rows(path):
    header, characteristic, body = path.read_text().split("\n", 2)
    require(header == "z,b0,d1,d4,a0,a5" and characteristic == "0",
            f"strict header changed: {path.name}")
    return body.rstrip().split(",\n")


def main():
    export, export_hash = read_logical(EXPORT)
    before = digest(INPUT)
    replay = subprocess.run([sys.executable, str(EXPORTER)], cwd=HERE,
                            capture_output=True, text=True, timeout=150)
    require(replay.returncode == 0 and "export PASS" in replay.stdout,
            "O3 exporter replay failed")
    require(digest(INPUT) == before == export["input_sha256"],
            "O3 input changed on replay")
    export2, export_hash2 = read_logical(EXPORT)
    require(export2 == export and export_hash2 == export_hash,
            "O3 export record changed")

    o1, o1_hash = read_logical(O1_EXPORT)
    require(o1_hash == export["ten_literal_rows_source_export_logical_sha256"] and
            digest(O1_INPUT) == o1["input_sha256"], "O1 source chain mismatch")
    o3_rows, o1_rows = rows(INPUT), rows(O1_INPUT)
    require(len(o3_rows) == len(o1_rows) == 13, "row count changed")
    require(o3_rows[0] == o1_rows[1] and o3_rows[2:] == o1_rows[2:],
            "O3 changed source/localizer rows or failed to retain exact R1")
    require(o3_rows[1] != o1_rows[0] and o3_rows[1] != o1_rows[1],
            "S256 factor replacement failed")
    require("(" not in INPUT.read_text() and ")" not in INPUT.read_text(),
            "strict parenthesis guard failed")

    interface, interface_hash = read_logical(INTERFACE)
    candidates = [factor["polynomial"]
                  for minor in interface["forced_consistency_minors"]
                  for factor in minor["factorization"]["factors"]
                  if factor["profile"]["terms"] == 256]
    require(candidates == [o3_rows[1]], "row 1 is not unique exact S256")
    symmetry, symmetry_hash = read_logical(SYMMETRY)
    require(symmetry_hash == export["symmetry_logical_sha256"] and
            symmetry["factor_images"]["R1"]["target"] == "R2" and
            symmetry["factor_images"]["S256"]["target"] == "S256",
            "involutive mate replay failed")
    require(export["involutive_mate"] == ["R2", "S256"],
            "mate label changed")
    require(export["explicit_nonlocalization"] == ["R0", "R2"],
            "complement nonlocalization changed")
    require(o3_rows[-1] == o1_rows[-1] and
            export["guaranteed_live_product"] == o1["guaranteed_live_product"],
            "guaranteed localizer changed")
    require(export["source_row_denominator_records"] == o1["denominator_records"],
            "source denominator ledger changed")

    run = json.loads(RUN.read_text())
    require(run["timeout_seconds"] == 600 and run["process_status"] == "completed" and
            run["returncode"] == 0 and run["unit_basis"], "exact run status changed")
    require(run["input_sha256"] == digest(INPUT) and
            run["output_sha256"] == digest(OUTPUT), "run digest mismatch")
    require(OUTPUT.read_text().rstrip().endswith("[1]:"), "unit output changed")
    require("[1]:" not in OUTPUT.read_text().replace("[1]:", "[b0]:"),
            "unit-output mutation failed")

    result = {
        "status": "exact corrected O3 R1=S256 unit gate PASS",
        "export_logical_sha256": export_hash,
        "O1_source_export_logical_sha256": o1_hash,
        "interface_logical_sha256": interface_hash,
        "symmetry_logical_sha256": symmetry_hash,
        "input_sha256": digest(INPUT), "output_sha256": digest(OUTPUT),
        "literal_row_count": 10,
        "localized_factors": ["b0", "d1", "d4", "C0", "R3"],
        "explicitly_not_localized": ["R0", "R2"],
        "mutation_controls": ["two_factor_replacement", "strict_parentheses",
                              "unchanged_localizer", "involutive_mate", "unit_output"],
        "theorem": ("In the Delta-open,D0=0,C0!=0 selected-pivot-zero branch, "
                    "the full ten-row pre-pivot literal source system has no "
                    "solution with R1=S256=0 and only guaranteed base/Delta live."),
        "symmetry_consequence": "The exact involution closes R2=S256=0.",
        "combined_pivot_zero_conclusion": ("Together with O1 and O2, all three "
                                           "source-admissible pivot-zero orbits are closed."),
        "scope_guard": ("This closes the selected-pivot-zero complement only inside "
                        "the Delta-open,D0=0,C0!=0 ambient chart."),
    }
    result["logical_sha256"] = logical_hash(result)
    (HERE / "results_d0_pivot_zero_R1_S256_gate_audit.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("D0 pivot-zero O3 exact audit PASS", result["logical_sha256"])


if __name__ == "__main__": main()
