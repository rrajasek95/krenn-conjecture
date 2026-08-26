#!/usr/bin/env python3
"""Export O2 by source-faithfully replacing R1 with the exact S42 factor."""

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


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_hash(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def read_logical(path):
    value = json.loads(path.read_text())
    frozen = value.pop("logical_sha256")
    require(logical_hash(value) == frozen, f"logical digest mismatch: {path.name}")
    return value, frozen


def main():
    replay = subprocess.run([sys.executable, str(O1_EXPORTER)], cwd=HERE,
                            capture_output=True, text=True, timeout=120)
    require(replay.returncode == 0 and "export PASS" in replay.stdout,
            "ten-row pre-pivot source regeneration failed")
    o1, o1_hash = read_logical(O1_EXPORT)
    require(o1["input_sha256"] == digest(O1_INPUT), "O1 input hash mismatch")
    header, characteristic, body = O1_INPUT.read_text().split("\n", 2)
    rows = body.rstrip().split(",\n")
    require(header == "z,b0,d1,d4,a0,a5" and characteristic == "0" and
            len(rows) == 13, "O1 strict packet interface changed")

    interface, interface_hash = read_logical(INTERFACE)
    s42_records = []
    for minor in interface["forced_consistency_minors"]:
        for factor in minor["factorization"]["factors"]:
            if factor["profile"]["terms"] == 42:
                s42_records.append(factor)
    require(len(s42_records) == 1, "S42 extraction is not unique")
    S42 = s42_records[0]["polynomial"]
    require("(" not in S42 and ")" not in S42, "S42 is not strict-expanded")
    rows[1] = S42
    output = HERE / "d0_pivot_zero_R0_S42_char0.msolve"
    output.write_text(header + "\n" + characteristic + "\n" +
                      ",\n".join(rows) + "\n")
    labels = list(o1["labels"])
    labels[1] = "S42"
    profiles = list(o1["profiles"])
    profiles[1] = s42_records[0]["profile"]
    result = {
        "status": "exact Delta-open pre-pivot R0=S42 gate export PASS",
        "input": output.name, "input_sha256": digest(output),
        "labels": labels, "profiles": profiles,
        "ten_literal_rows_source_export_logical_sha256": o1_hash,
        "interface_logical_sha256": interface_hash,
        "guaranteed_live_product": o1["guaranteed_live_product"],
        "guaranteed_live_profile": o1["guaranteed_live_profile"],
        "explicit_nonlocalization": ["R1", "R2"],
        "source_row_denominator_records": o1["denominator_records"],
        "scope": ("Corrected O2 representative R0=S42=0. The full ten-row "
                  "pre-pivot literal packet is reused byte-for-byte; only "
                  "b0*d1*d4*C0*R3 is localized. R1/R2 are unrestricted."),
    }
    result["logical_sha256"] = logical_hash(result)
    (HERE / "results_d0_pivot_zero_R0_S42_gate_export.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("D0 pivot-zero R0/S42 export PASS", result["logical_sha256"])
    print("input", output.stat().st_size, "bytes", result["input_sha256"])


if __name__ == "__main__":
    main()
