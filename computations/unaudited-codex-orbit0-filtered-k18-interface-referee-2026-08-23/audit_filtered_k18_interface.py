#!/usr/bin/env python3
"""Exact component/cost interface for K18; no K18 rows are constructed."""

from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
K16 = (ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23"
       / "results_filtered_k16_run.json")
K17 = K16.with_name("results_filtered_k17_run.json")
COLLECTION = (ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22"
              / "results_orbit0_k16_literal_residual.json")
OUT = HERE / "results_filtered_k18_interface.json"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main(write_results=False):
    k16 = json.loads(K16.read_text())
    k17 = json.loads(K17.read_text())
    collection = json.loads(COLLECTION.read_text())
    assert k16["K16_checkpoint"]["removed_pivotable"][0] == 24_003_767
    assert k17["status"].startswith("PASS one bounded exact")
    uses14 = collection["collection"]["literal_pivot_uses"]
    direct = 485 * (3 * 12 * 60 ** 2 + 3 * 32 ** 2 * 60)
    from14 = uses14 * 60
    # Exact compact H-orbit/pivot scans frozen in the interface census.
    # All available K15 pivots.  The former 44,342,881 value was the
    # already-irreducible K17 child count, not the full parent-pivot count.
    uses15 = 55_934_080
    from15 = uses15 * 32
    uses16 = 129_939_187
    from16 = uses16 * 12
    assert (direct, from14, from15, from16) == (
        152_251_200, 397_156_800, 1_789_890_560, 1_559_270_244)
    total = direct + from14 + from15 + from16
    scale = 281_801_520
    maximum_parent_mass = 8_448
    hostile_collision = total * scale * maximum_parent_mass
    result = {
        "status": "PASS_EXACT_K18_INTERFACE_NO_COLLECTION",
        "components": [
            {"name": "direct_K18",
             "formula": "-R8prime*(three E2E4E4 orders + three E3E3E4 orders)",
             "raw_compact_occurrences": direct, "denominator": 1},
            {"name": "K14_to_K18_K4",
             "formula": "frozen valid-pivot K14 coefficients with correct positive response sign, times 60 K4 tails",
             "pivot_uses": uses14, "raw_compact_occurrences": from14,
             "denominators_divide": [1,2,5,7,8,11,14,15,22,23,34,35]},
            {"name": "K15_to_K18_K3",
             "formula": "all-pivot K15 source coefficients with response sign -p/choices, times 32 K3 tails",
             "pivot_uses": uses15, "raw_compact_occurrences": from15,
             "reduced_denominators": [1,5,7,11,17,23]},
            {"name": "K16_to_K18_K2",
             "formula": "all-pivot coefficients of the 24,003,767 combined pivotable K16 rows, times 12 K2 tails",
             "pivot_uses": uses16, "raw_compact_occurrences": from16,
             "reduced_denominators": [1,5,7,11],
             "maximum_parent_orbit_mass": maximum_parent_mass},
        ],
        "total_raw_compact_tail_occurrences": total,
        "K17_guard": "K17 cannot feed K18 because every singleton pivot tail raises K by at least two; K17 first feeds K19.",
        "integer_bound": {
            "scale": scale,
            "hostile_all_terms_collide_i128_numerator": hostile_collision,
            "i128_max": 2 ** 127 - 1,
            "safety_margin_floor": (2 ** 127 - 1) // hostile_collision,
        },
        "smallest_charge_only_computation": {
            "algorithm": (
                "Precompute the 77-dual charge, split by K2/K3/K4 and child "
                "pivotability, for each encountered enriched local key: four-path/"
                "closed-cycle profile + 12-anchor base signature + pivot word. "
                "Stream the four parent interfaces and accumulate i128 scalars; "
                "never construct or hash K18 child rows."
            ),
            "why_1162_profiles_alone_are_insufficient": (
                "uncoloured cycle profile forgets anchor support, hence cannot decide "
                "whether a K18 child is killed by the 78 K0 heads"
            ),
            "streamed_parent_pivot_uses": uses14 + uses15 + uses16,
            "direct_term_uses": direct,
            "estimated_elementary_lookups": direct + uses14 + uses15 + uses16,
            "hard_gate": "180 seconds / 2 GiB / 250,000-entry LRU; checkpoint each component",
            "expected": (
                "roughly 333 million lookup/term operations; plausible in optimized "
                "8-thread Rust from the 64.5-second K17 control, but not guaranteed "
                "until the enriched-key cache-miss prefix is measured"
            ),
        },
        "scope": "Interface/cost/charge design only; no K18 collection or charge was run.",
        "pinned": {str(path.relative_to(ROOT)): digest(path)
                   for path in (K16, K17, COLLECTION)},
    }
    logical = sha256(json.dumps(result, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "raw": total,
                      "charge_ops": result["smallest_charge_only_computation"]
                      ["estimated_elementary_lookups"],
                      "logical_sha256": logical}, indent=2))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)
