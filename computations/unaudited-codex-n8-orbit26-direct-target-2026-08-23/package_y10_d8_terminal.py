#!/usr/bin/env python3
"""Deterministic terminal package for the exact d8 staged closure ledger."""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
RAW = HERE / "results_y10_d8_staged_blocks.json"
INCIDENT = HERE / "results_y10_dead_row_original_d8.json"
D7 = HERE / "results_y10_d7_staged_blocks.json"
OUTPUT = HERE / "results_y10_d8_terminal.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    raw = json.loads(RAW.read_text())
    incident = json.loads(INCIDENT.read_text())
    d7 = json.loads(D7.read_text())
    require(raw["status"] == "EXACT_TARGET_STANDARD_THROUGH_TOTAL_D8",
            "raw d8 closure is not terminal standard")
    require(d7["logical_sha256"]
            == "30e98f20fd4f5f7a08b43295cf6eb93b46cefc96a232dc44ed0a03c72538251a",
            "d7 theorem changed")
    components = raw["component_records"]
    require(len(components) == 117, "d8 component census changed")
    require(sum(item["seed_columns"] for item in components) == 205,
            "d8 seeds were not partitioned by components")
    require(sum(item["closed_columns"] for item in components) == 70_578,
            "d8 aggregate column census changed")
    require(sum(item["closed_rows"] for item in components) == 3_650_920,
            "d8 aggregate row census changed")
    require(all(item["singleton_residual_columns"] == 0
                and item["singleton_pivots"] == item["closed_columns"]
                for item in components), "a d8 singleton core appeared")
    slice_histogram = Counter()
    for record in incident["incident_records"]:
        if record["multiplier_t_exponent"] != 0:
            continue
        row_lengths = {len(bytes.fromhex(item[0]))
                       for item in record["target_rows"]}
        require(len(row_lengths) == 1, "d8 seed crossed target slices")
        slice_histogram[8 - next(iter(row_lengths))] += 1
    require(slice_histogram == Counter({1: 61, 2: 144}),
            "d8 seed slice histogram changed")

    terminal = {
        "format": "n8-orbit26-y10-d8-terminal-v1",
        "status": "EXACT_TARGET_STANDARD_THROUGH_TOTAL_D8",
        "target_y10_row": incident["target_y10_row"],
        "target_total_degree": incident["target_total_degree"],
        "homogeneous_d8_divisors": incident["distinct_homogeneous_divisors"],
        "new_t_free_y4_seeds": 205,
        "new_seed_target_t_exponent_histogram": dict(sorted(
            slice_histogram.items()
        )),
        "seed_components": len(components),
        "closed_columns": 70_578,
        "closed_rows": 3_650_920,
        "singleton_pivots": 70_578,
        "singleton_residual_columns": 0,
        "largest_component_columns": max(
            item["closed_columns"] for item in components
        ),
        "largest_component_rows": max(
            item["closed_rows"] for item in components
        ),
        "component_ledger_sha256": sha256(json.dumps(
            components, sort_keys=True, separators=(",", ":")
        ).encode("ascii")).hexdigest(),
        "theorem": (
            "Every new t-free y4 column capable of feeding a d8 target divisor "
            "belongs to one of the 117 exact y8 inverse-incidence components, "
            "and private-row peeling proves their direct sum injective. All lower "
            "d8 slices lie in t*M7, so frozen d7 standardness promotes the target "
            "to standardness through total degree eight."
        ),
        "scope": (
            "frozen chart26 t-last target only; no degree-nine or alternative "
            "right-inverse claim"
        ),
        "source_sha256": {
            RAW.name: sha256(RAW.read_bytes()).hexdigest(),
            INCIDENT.name: sha256(INCIDENT.read_bytes()).hexdigest(),
            D7.name: sha256(D7.read_bytes()).hexdigest(),
        },
    }
    encoded = json.dumps(terminal, sort_keys=True, separators=(",", ":"))
    terminal["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    OUTPUT.write_text(json.dumps(terminal, indent=2, sort_keys=True) + "\n")
    print("y10 d8 terminal package: PASS")
    print("components/columns/rows:", 117, 70_578, 3_650_920)
    print("logical sha256:", terminal["logical_sha256"])


if __name__ == "__main__":
    main()
