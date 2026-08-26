#!/usr/bin/env python3
"""Freeze the certified 120-orbit cutoff-nine K8 representative for Rust."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
UPSTREAM = HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
RESIDUAL = UPSTREAM / "results_orbit0_cutoff9_sparse_r8.json"
EXPORT_PATH = UPSTREAM / "export_orbit0_cutoff_seed.py"
SPEC = importlib.util.spec_from_file_location("orbit0_export", EXPORT_PATH)
EXPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPORT)
OUT = HERE / "sparse_r8_seed.txt"
RESULTS = HERE / "results_sparse_r8_seed.json"
EXPECTED = "877ca35865130bd9ca55f19387b44d9473acd2b47d5eddd2d29c1718831cf968"


def main():
    payload = json.loads(RESIDUAL.read_text())
    if payload["result_sha256"] != EXPECTED:
        raise RuntimeError("sparse R8 logical digest changed")
    if not payload["exact_core_replay"] or not payload["exact_reverse_pivot_replay"]:
        raise RuntimeError("sparse R8 lost its exact source replay")
    numerators = [numerator for _row, numerator, denominator
                  in payload["residual"] if denominator == 1]
    if len(numerators) != len(payload["residual"]):
        raise RuntimeError("sparse R8 quotient masses are not integral")
    scale = math.gcd(*map(abs, numerators))
    rows = []
    orbit_histogram = Counter()
    coefficient_histogram = Counter()
    for row_hex, numerator, denominator in payload["residual"]:
        row = bytes.fromhex(row_hex)
        orbit_size = len(EXPORT.row_orbit(row))
        if EXPORT.BASE.row_degree(row, EXPORT.ANCHORS) != 8:
            raise RuntimeError("sparse R8 row left K-degree eight")
        rows.append((row_hex, numerator // scale, orbit_size))
        orbit_histogram[orbit_size] += 1
        coefficient_histogram[numerator // scale] += 1
    lines = [
        "KRENN_ORBIT0_R8_SEED_V1",
        "ANCHORS " + bytes(sorted(EXPORT.ANCHORS)).hex(),
        f"SCALE {scale}",
    ]
    for sites, colours in EXPORT.STABILIZER:
        lines.append("ACTION " + "".join(map(str, sites)) + " "
                     + "".join(map(str, colours)))
    for row_hex, mass_units, orbit_size in rows:
        lines.append(f"R8 {row_hex} {mass_units} {orbit_size}")
    text = "\n".join(lines) + "\n"
    OUT.write_text(text)
    result = {
        "status": "exact compact signed sparse-R8 seed",
        "upstream_logical_sha256": payload["result_sha256"],
        "upstream_file_sha256": sha256(RESIDUAL.read_bytes()).hexdigest(),
        "seed_sha256": sha256(text.encode("ascii")).hexdigest(),
        "stabilizer_order": len(EXPORT.STABILIZER),
        "coefficient_scale": scale,
        "support_row_orbits": len(rows),
        "labelled_support_rows": sum(size for _row, _mass, size in rows),
        "orbit_size_histogram": dict(sorted(orbit_histogram.items())),
        "coefficient_units_histogram": dict(sorted(coefficient_histogram.items())),
        "normalization": (
            "If quotient mass is scale*m and orbit size is s, the labelled "
            "coefficient is scale*m/s. Signs are retained. Repeated factors "
            "in degree-24 products are retained."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("sparse R8 compact seed: PASS")
    print("orbits/labelled/scale:", len(rows), result["labelled_support_rows"], scale)
    print("seed sha256:", result["seed_sha256"])
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
