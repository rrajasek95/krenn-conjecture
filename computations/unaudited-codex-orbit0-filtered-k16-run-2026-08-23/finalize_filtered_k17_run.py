#!/usr/bin/env python3
"""Freeze hashes and scope for the bounded, globally-cleared K17 run."""

from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def digest(path):
    state = sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 22):
            state.update(block)
    return state.hexdigest()


def main():
    audit = json.loads((HERE / "results_filtered_k17_checkpoint_audit.json").read_text())
    aux = json.loads((HERE / "results_filtered_k17_aux_export.json").read_text())
    files = [
        HERE / "checkpoint_k17_direct.bin",
        HERE / "checkpoint_k17_from_k14.bin",
        HERE / "checkpoint_k17_from_k15.bin",
        HERE / "checkpoint_reduced_k17.bin",
    ]
    result = {
        "status": "PASS one bounded exact filtered reduction through completed K17",
        "elapsed_seconds": 64.528,
        "global_integer_scale": 281_801_520,
        "scale_scope": (
            "LCM of every possible nonzero pivot count on the 4096 anchor supports; "
            "sufficient for this one K17 construction/normal, not promised for nested K18+ divisions"
        ),
        "components": {
            "direct_K17": {
                "raw_irreducible_occurrences": 82_938_880,
                "scaled_census": [1_439_337, 25_243_644_896_870_400,
                                  238_190_584_070_799_360],
            },
            "K14_valid_average_K3": {
                "raw_irreducible_occurrences": 14_402_560,
                "scaled_census": [10_220_344, -132_228_616_126_464_000,
                                  1_264_409_305_186_959_360],
            },
            "K15_all_pivot_average_K2": {
                "raw_irreducible_occurrences": 219_763_200,
                "scaled_census": [44_807_320, -405_581_228_009_717_760,
                                  3_877_463_100_966_174_720],
            },
        },
        "combination": {
            "component_support_slots": 56_467_001,
            "support_union": 55_191_637,
            "overlap_incidences": 1_275_364,
            "exact_zero_rows": 288,
            "reduced_scaled_census": [55_191_349, -512_566_199_239_311_360,
                                      5_316_644_742_680_494_080],
        },
        "cycle_replay": audit,
        "checkpoint_sha256": {path.name: digest(path) for path in files},
        "aux_export_logical_sha256": aux["logical_sha256"],
        "scope": (
            "Only the K17 normal is computed. Pivotable K17 rows are projected away "
            "without emitting their K19+ tails, and no K18 or higher bucket is built."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    target = HERE / "results_filtered_k17_run.json"
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
