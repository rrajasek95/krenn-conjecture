#!/usr/bin/env python3
"""Freeze the certified orbit0 R8 residual in a compact Rust seed."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
UPSTREAM = HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
RESIDUAL = UPSTREAM / "results_orbit0_cutoff8_leading_residual.json"
EXPORT_PATH = UPSTREAM / "export_orbit0_cutoff_seed.py"
SPEC = importlib.util.spec_from_file_location("orbit0_export", EXPORT_PATH)
EXPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPORT)
OUT = HERE / "r8_seed.txt"
RESULTS = HERE / "results_r8_seed.json"


def main():
    payload = json.loads(RESIDUAL.read_text())
    if payload["result_sha256"] != "25d4acd094eb27e78e3941b738611522f112f57f4ef6f78f3657d50e18762d03":
        raise RuntimeError("R8 logical digest changed")
    rows = []
    orbit_histogram = Counter()
    coefficient_histogram = Counter()
    for row_hex, numerator, denominator in payload["residual"]:
        row = bytes.fromhex(row_hex)
        orbit_size = len(EXPORT.row_orbit(row))
        if denominator != 1 or numerator % 48:
            raise RuntimeError("R8 coefficient is not integral in units of 48")
        if EXPORT.BASE.row_degree(row, EXPORT.ANCHORS) != 8:
            raise RuntimeError("R8 row left K-degree eight")
        rows.append((row_hex, numerator // 48, orbit_size))
        orbit_histogram[orbit_size] += 1
        coefficient_histogram[numerator // 48] += 1
    lines = [
        "KRENN_ORBIT0_R8_SEED_V1",
        "ANCHORS " + bytes(sorted(EXPORT.ANCHORS)).hex(),
        "SCALE 48",
    ]
    for sites, colours in EXPORT.STABILIZER:
        lines.append("ACTION " + "".join(map(str, sites)) + " "
                     + "".join(map(str, colours)))
    for row_hex, mass_units, orbit_size in rows:
        lines.append(f"R8 {row_hex} {mass_units} {orbit_size}")
    text = "\n".join(lines) + "\n"
    OUT.write_text(text)
    result = {
        "status": "exact compact R8 seed; coefficients are quotient masses divided by 48",
        "upstream_logical_sha256": payload["result_sha256"],
        "upstream_file_sha256": sha256(RESIDUAL.read_bytes()).hexdigest(),
        "seed_sha256": sha256(text.encode("ascii")).hexdigest(),
        "stabilizer_order": len(EXPORT.STABILIZER),
        "support_row_orbits": len(rows),
        "labelled_support_rows": sum(size for _row, _mass, size in rows),
        "orbit_size_histogram": dict(sorted(orbit_histogram.items())),
        "coefficient_units_histogram": dict(sorted(coefficient_histogram.items())),
        "normalization": (
            "If quotient mass is 48*m and orbit size is s, the labelled "
            "coefficient is 48*m/s. Repeated degree-24 factors are retained."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("R8 compact seed: PASS")
    print("orbits/labelled:", len(rows), result["labelled_support_rows"])
    print("seed sha256:", result["seed_sha256"])
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()

