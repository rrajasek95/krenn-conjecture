#!/usr/bin/env python3
"""Residual-led degree-six frontier census for legacy27 / K^7.

This freezes the exact K^6 certificate and closes its K-degree-six residual
under every minimum-degree-six source column, modulo the exact six-element
anchor stabilizer.  It deliberately stops before rank or membership work.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROBE_PATH = HERE / "probe_legacy27_k6_orbits.py"
SPEC = importlib.util.spec_from_file_location("legacy27_probe_k7", PROBE_PATH)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)
BASE = PROBE.BASE
IN_CERT = HERE / "results_k6_exact.json"
OUT = HERE / "results_k7_residual_census.json"
EXPECTED_CERT_SHA256 = (
    "1dc739a4ef4ef5c2e0e6d89d3621d15e0c547a0eaf4802bcc1f87b800e6a3097"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def frozen_residual():
    payload = json.loads(IN_CERT.read_text())
    stored = payload.pop("result_sha256")
    require(stored == EXPECTED_CERT_SHA256,
            "pinned legacy27 K6 certificate digest changed")
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    require(sha256(encoded.encode("ascii")).hexdigest() == stored,
            "pinned legacy27 K6 certificate content changed")
    name_to_id = {
        BASE.cell_name(cell): index for index, cell in enumerate(BASE.CELLS)
    }
    current = Counter()
    for item in payload["certificate"]["terms"]:
        coefficient = Fraction(
            item["coefficient_on_six_transform_average"]
        )
        column = (
            tuple(map(int, item["word"])),
            bytes(sorted(name_to_id[name] for name in item["multiplier"])),
        )
        require(PROBE.canonical_column(column) == column,
                "K6 term is not a canonical column")
        for row in BASE.column_rows(column):
            if BASE.row_degree(row, PROBE.ANCHORS) == 6:
                current[PROBE.canonical_row(row)] += coefficient
    target = Counter()
    for row, coefficient in PROBE.target_exact(6).items():
        target[PROBE.canonical_row(row)] += Fraction(coefficient)
    residual = Counter(target)
    residual.subtract(current)
    residual = Counter({row: value for row, value in residual.items() if value})
    require(all(BASE.row_degree(row, PROBE.ANCHORS) == 6
                for row in residual), "K7 residual degree changed")
    return residual


def close_residual(residual):
    rows = set(residual)
    frontier = set(rows)
    columns = set()
    layers = []
    while frontier:
        new_rows = set()
        before = len(columns)
        for row in frontier:
            for raw_column in BASE.incident_columns(row):
                column = PROBE.canonical_column(raw_column)
                if column in columns:
                    continue
                if PROBE.column_minimum_degree(column) != 6:
                    continue
                columns.add(column)
                for output in BASE.column_rows(column):
                    if BASE.row_degree(output, PROBE.ANCHORS) != 6:
                        continue
                    representative = PROBE.canonical_row(output)
                    if representative not in rows:
                        rows.add(representative)
                        new_rows.add(representative)
        frontier = new_rows
        layers.append((len(new_rows), len(columns) - before))
        print(
            f"layer {len(layers)}: +{len(new_rows)} rows, "
            f"+{len(columns) - before} cols, totals {len(rows)}/{len(columns)}",
            flush=True,
        )
    return rows, columns, layers


def audit(residual_only=False):
    residual = frozen_residual()
    print("frozen degree-six residual row orbits:", len(residual), flush=True)
    core = {
        "status": "UNAUDITED exact residual census; no K7 membership claim",
        "zero_based_chart": 30,
        "legacy_one_based_chart": 27,
        "source_K6_result_sha256": EXPECTED_CERT_SHA256,
        "stabilizer_order": len(PROBE.STABILIZER),
        "frozen_tail_residual_row_orbits": len(residual),
        "residual_coefficient_histogram": dict(sorted(Counter(
            str(value) for value in residual.values()
        ).items())),
        "closure_computed": not residual_only,
        "K7_membership_claimed": False,
    }
    if not residual_only:
        rows, columns, layers = close_residual(residual)
        leading = Counter()
        orbit_collision_columns = 0
        for column in columns:
            outputs = tuple(PROBE.canonical_row(row)
                            for row in BASE.column_rows(column)
                            if BASE.row_degree(row, PROBE.ANCHORS) == 6)
            leading[len(outputs)] += 1
            if len(outputs) != len(set(outputs)):
                orbit_collision_columns += 1
        core.update({
            "closure_row_column_orbits": [len(rows), len(columns)],
            "closure_layers": layers,
            "literal_leading_term_histogram": {
                str(key): value for key, value in sorted(leading.items())
            },
            "columns_with_row_orbit_collisions": orbit_collision_columns,
        })
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    return core


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--residual-only", action="store_true")
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    result = audit(args.residual_only)
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "residual_row_orbits": result["frozen_tail_residual_row_orbits"],
        "closure": result.get("closure_row_column_orbits"),
        "sha256": result["result_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
