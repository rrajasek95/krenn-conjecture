#!/usr/bin/env python3
"""Freeze the bounded degree-nine CEGAR wall-cap checkpoint."""

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CHECKPOINT = HERE / "results_degree9_rust_cegar_checkpoint.json"
OUTPUT = HERE / "results_degree9_rust_cegar.json"


def main():
    checkpoint = json.loads(CHECKPOINT.read_text())
    last = checkpoint["rounds"][-1]
    result = {
        "format": "n8-chart26-degree9-rust-cegar-v1",
        "status": "WALL_CAP_UNRESOLVED",
        "prime": 1_073_741_827,
        "lambda8_sha256": "561546730a738ad3e3432ae5f5b63456735514148f32b77268debbebdae09d9d",
        "initial_census_logical_sha256": "2c36f6054bacd4654236037849a2dc841b96b6ecb2161f3ee0322734c7ce94b1",
        "initial_selected_columns": 2308,
        "completed_round": checkpoint["completed_round"],
        "terminal_selected_columns": len(checkpoint["selected_columns"]),
        "rounds": checkpoint["rounds"],
        "last_completed_profile": last,
        "stop": {
            "reason": "manual bounded stop during round 15 before the external 600-second guard",
            "last_completed_driver_elapsed_seconds": last["elapsed_seconds"],
            "peak_sampled_rss_kib": 10_659_520,
            "peak_sampled_rss_gib": 10_659_520 / 1024 ** 2,
            "memory_ceiling_gib": 12,
            "note": "macOS RLIMIT_AS was unavailable; RSS was polled externally and remained below the ceiling",
        },
        "conclusion": "degree-nine lazy extension unresolved at the hard resource gate",
        "scope_guard": "no degree9 membership/nonmembership inference; all completed modular systems had full selected rank and zero remainder, but thousands of new crossings remained",
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("packaged", result["status"], "round", result["completed_round"],
          "selected", result["terminal_selected_columns"])


if __name__ == "__main__":
    main()
