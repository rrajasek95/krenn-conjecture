#!/usr/bin/env python3
"""Exact integer-scale, overflow, and precollection-filter guard for K17."""

from __future__ import annotations

from hashlib import sha256
from math import gcd, lcm
import importlib.util
import json
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = (ROOT / "computations/unaudited-codex-orbit0-filtered-k24-reducer-design-2026-08-23"
          / "filtered_k24_reducer.py")
COLLECTION = (ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22"
              / "results_orbit0_k16_literal_residual.json")
K15 = (ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23"
       / "checkpoint_direct_k15.bin")
OUT = HERE / "results_k17_scale_guard.json"
RECORD = struct.Struct("<24sq")
SCALE = 281_801_520


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def digest(path):
    h = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main(write_results=False):
    d = load("k17_scale_design", DESIGN)
    masks = [sum((value != 0) << i for i, value in enumerate(vector))
             for vector in d.CTX.vectors]
    counts = sorted({sum(support & mask == mask for mask in masks)
                     for support in range(1 << 12)} - {0})
    actual_lcm = 1
    for count in counts:
        actual_lcm = lcm(actual_lcm, count)
    assert actual_lcm == SCALE
    frozen = json.loads(COLLECTION.read_text())
    valid = sorted(map(int, frozen["source_provenance"]
                       ["valid_pivot_count_histogram_per_factored_pair"]))
    assert all(SCALE % count == 0 for count in valid)

    maximum_mass = 0
    records = 0
    with K15.open("rb") as stream:
        assert stream.read(8) == b"K15CHK1\0"
        count = struct.unpack("<Q", stream.read(8))[0]
        for records in range(1, count + 1):
            row, mass = RECORD.unpack(stream.read(RECORD.size))
            maximum_mass = max(maximum_mass, abs(mass))
        assert not stream.read(1)
    assert records == 5_311_211 and maximum_mass == 6_144

    maximum_scaled_occurrence = SCALE * maximum_mass
    collision_cap = 300_000_000 * maximum_scaled_occurrence
    i128_max = 2 ** 127 - 1
    result = {
        "status": "PASS_K17_CONSTRUCTION_SCALE_WITH_TRANSFER_GUARD",
        "scale": SCALE,
        "all_nonzero_pivot_counts": counts,
        "K14_valid_pivot_counts": valid,
        "covers_both_one_step_denominator_families": True,
        "overflow": {
            "maximum_observed_K15_orbit_mass": maximum_mass,
            "maximum_scaled_occurrence": maximum_scaled_occurrence,
            "all_300m_occurrences_collide_bound": collision_cap,
            "i128_max": i128_max,
            "integer_safety_margin_floor": i128_max // collision_cap,
        },
        "orbit_mass_integrality": (
            "The direct input is an H-invariant integer-labelled polynomial; each "
            "stored orbit mass is orbit_size times its integer labelled coefficient. "
            "Expanding an orbit therefore introduces no extra denominator."
        ),
        "precollection_filter": {
            "PASS_for_K17_normal": (
                "pivotability is H-invariant and coordinatewise, hence the projection "
                "killing pivotable rows is linear and commutes with H canonical collection"
            ),
            "guard_for_full_transfer": (
                "dropping a pivotable occurrence is not a full filtered reduction; "
                "K19/K20/K21 tails must be emitted occurrence-wise before dropping it"
            ),
        },
        "scale_scope_guard": (
            "SCALE clears the one-step K14-valid and K15-all divisions defining K17. "
            "It need not clear another K17 pivot division: repeated prime factors can "
            "require products such as 5^2, absent from this lcm."
        ),
        "pinned": {
            str(DESIGN.relative_to(ROOT)): digest(DESIGN),
            str(COLLECTION.relative_to(ROOT)): digest(COLLECTION),
            str(K15.relative_to(ROOT)): digest(K15),
        },
    }
    logical = sha256(json.dumps(result, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"],
                      "scale": SCALE,
                      "margin": result["overflow"]["integer_safety_margin_floor"],
                      "logical_sha256": logical}, indent=2))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)
