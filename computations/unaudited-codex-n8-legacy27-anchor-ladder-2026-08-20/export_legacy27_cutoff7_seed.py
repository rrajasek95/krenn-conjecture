#!/usr/bin/env python3
"""Export the complete legacy27 H0H1H2 target through K-degree six."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROBE_PATH = HERE / "probe_legacy27_k6_orbits.py"
SPEC = importlib.util.spec_from_file_location("legacy27_cutoff7", PROBE_PATH)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)
BASE = PROBE.BASE
OUT = HERE / "legacy27_cutoff7_target_seed.txt"
RESULT = HERE / "results_cutoff7_target_census.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def audit():
    target = Counter()
    actual_by_degree = {}
    orbit_by_degree = {}
    mass_by_degree = {}
    coefficient_histogram_by_degree = {}
    for degree in range(7):
        actual = (Counter({bytes(sorted(PROBE.ANCHORS)): 1})
                  if degree == 0 else PROBE.target_exact(degree))
        quotient = Counter()
        for row, coefficient in actual.items():
            require(BASE.row_degree(row, PROBE.ANCHORS) == degree,
                    "target exact-degree generator leaked")
            quotient[PROBE.canonical_row(row)] += coefficient
        actual_by_degree[degree] = len(actual)
        orbit_by_degree[degree] = len(quotient)
        mass_by_degree[degree] = sum(quotient.values())
        coefficient_histogram_by_degree[degree] = dict(sorted(Counter(
            str(value) for value in quotient.values()
        ).items()))
        target.update(quotient)
    require(actual_by_degree == {0: 1, 1: 0, 2: 36, 3: 96,
                                 4: 612, 5: 2304, 6: 9120},
            "legacy27 target actual-degree census changed")
    require(sum(actual_by_degree.values()) == sum(target.values()) == 12169,
            "legacy27 target mass changed")
    require(len(target) == sum(orbit_by_degree.values()),
            "target row orbits collided across K-degrees")
    lines = [
        "KRENN_ANCHOR_K_SEED_V1",
        "CUTOFF 7",
        "ANCHORS " + bytes(sorted(PROBE.ANCHORS)).hex(),
        "EXPECTED 0 0 0 0 0",
    ]
    for sites, colours in PROBE.STABILIZER:
        lines.append(
            "ACTION " + "".join(map(str, sites)) + " "
            + "".join(map(str, colours))
        )
    for row, coefficient in sorted(target.items()):
        lines.append(f"ROW {row.hex()} {coefficient} 1")
    payload = "\n".join(lines) + "\n"
    core = {
        "status": "UNAUDITED exact target census / Rust whole-cutoff seed",
        "zero_based_chart": 30,
        "legacy_one_based_chart": 27,
        "cutoff": 7,
        "anchor_names": [BASE.cell_name(BASE.CELLS[cell])
                         for cell in sorted(PROBE.ANCHORS)],
        "stabilizer_order": len(PROBE.STABILIZER),
        "actual_target_rows_by_K_degree": actual_by_degree,
        "target_row_orbits_by_K_degree": orbit_by_degree,
        "target_mass_by_K_degree": mass_by_degree,
        "target_orbit_coefficient_histogram_by_K_degree":
            coefficient_histogram_by_degree,
        "target_orbit_rows": len(target),
        "target_mass": sum(target.values()),
        "seed_bytes": len(payload),
        "seed_sha256": sha256(payload.encode("ascii")).hexdigest(),
        "whole_cutoff_source_scope": (
            "all mixed-source columns of minimum K-degree below 7; this "
            "includes the complete 106264-dimensional cutoff<6 kernel"
        ),
        "rank_or_membership_claimed": False,
    }
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    return core, payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    result, payload = audit()
    if args.write_results:
        OUT.write_text(payload)
        RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("target actual by degree:", result["actual_target_rows_by_K_degree"])
    print("target orbit by degree:", result["target_row_orbits_by_K_degree"])
    print("target orbit rows/mass:", result["target_orbit_rows"],
          result["target_mass"])
    print("seed sha256:", result["seed_sha256"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
