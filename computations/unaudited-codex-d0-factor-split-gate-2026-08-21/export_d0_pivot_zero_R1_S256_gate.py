#!/usr/bin/env python3
"""Export final pivot-zero orbit O3: R1=S256=0."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
O1_EXPORTER = HERE / "export_d0_pivot_zero_R0_R1_gate.py"
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


def main():
    replay = subprocess.run([sys.executable, str(O1_EXPORTER)], cwd=HERE,
                            capture_output=True, text=True, timeout=120)
    require(replay.returncode == 0 and "export PASS" in replay.stdout,
            "ten-row source regeneration failed")
    o1, o1_hash = read_logical(O1_EXPORT)
    require(o1["input_sha256"] == digest(O1_INPUT), "O1 input mismatch")
    header, characteristic, body = O1_INPUT.read_text().split("\n", 2)
    rows = body.rstrip().split(",\n")
    require(len(rows) == 13, "O1 row count changed")

    interface, interface_hash = read_logical(INTERFACE)
    s256 = [factor for minor in interface["forced_consistency_minors"]
            for factor in minor["factorization"]["factors"]
            if factor["profile"]["terms"] == 256]
    require(len(s256) == 1, "S256 extraction is not unique")
    R1 = rows[1]
    rows[0], rows[1] = R1, s256[0]["polynomial"]
    output = HERE / "d0_pivot_zero_R1_S256_char0.msolve"
    output.write_text(header + "\n" + characteristic + "\n" +
                      ",\n".join(rows) + "\n")
    labels = list(o1["labels"]); labels[0], labels[1] = "R1", "S256"
    profiles = list(o1["profiles"]); profiles[0] = o1["profiles"][1]
    profiles[1] = s256[0]["profile"]
    symmetry, symmetry_hash = read_logical(SYMMETRY)
    require(symmetry["factor_images"]["R1"]["target"] == "R2" and
            symmetry["factor_images"]["S256"]["target"] == "S256",
            "O3 involutive mate changed")
    result = {
        "status": "exact Delta-open pre-pivot R1=S256 gate export PASS",
        "input": output.name, "input_sha256": digest(output),
        "labels": labels, "profiles": profiles,
        "ten_literal_rows_source_export_logical_sha256": o1_hash,
        "interface_logical_sha256": interface_hash,
        "symmetry_logical_sha256": symmetry_hash,
        "guaranteed_live_product": o1["guaranteed_live_product"],
        "guaranteed_live_profile": o1["guaranteed_live_profile"],
        "explicit_nonlocalization": ["R0", "R2"],
        "source_row_denominator_records": o1["denominator_records"],
        "involutive_mate": ["R2", "S256"],
        "scope": ("Final corrected O3 representative R1=S256=0. Full ten-row "
                  "pre-pivot packet; only b0*d1*d4*C0*R3 localized. R0/R2 "
                  "unrestricted; involution covers R2=S256."),
    }
    result["logical_sha256"] = logical_hash(result)
    (HERE / "results_d0_pivot_zero_R1_S256_gate_export.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("D0 pivot-zero R1/S256 export PASS", result["logical_sha256"])
    print("input", output.stat().st_size, "bytes", result["input_sha256"])


if __name__ == "__main__": main()
