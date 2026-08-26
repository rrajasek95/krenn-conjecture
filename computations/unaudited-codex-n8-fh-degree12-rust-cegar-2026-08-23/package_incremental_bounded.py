#!/usr/bin/env python3
"""Replay the terminal incremental full-Fh D12 checkpoint without solving."""

import json
from hashlib import sha256
from pathlib import Path
import struct


HERE = Path(__file__).resolve().parent
CHECKPOINT = HERE / "checkpoint_fh_degree12_incremental.json"
BASIS = HERE / "incremental_basis.bin"
ROWS = HERE / "incremental_rows.bin"
ENGINE = HERE / "target/release/fh-d12-incremental"
DRIVER = HERE / "run_fh_degree12_incremental.py"
RESULT = HERE / "results_fh_degree12_incremental_bounded.json"
EXPECTED_LOGICAL_SHA256 = "d469ae0d58c7ddea174bc18abeb07cda1e37d0e7dc724fc5e647911890225341"
FROZEN = [
    (56,1,1,2,17,15),(1438,16,16,2,37,35),(4663,51,51,2,102,93),
    (12410,144,144,3,129,116),(21877,260,260,2,33,31),
    (24501,291,291,2,20,18),(26194,309,309,2,20,17),
    (27771,326,326,11,103,76),(34477,402,402,5,42,32),
    (37304,434,434,4,24,20),(39002,454,454,14,99,78),
    (45934,532,532,8,56,43),(49728,575,575,26,197,139),
    (62095,714,714,11,64,50),(66554,764,764,33,252,183),
    (82434,947,947,90,793,508),(125423,1455,1455,177,1587,981),
    (208112,2436,2436,4,24,18),(209578,2454,2454,32,282,198),
    (226335,2652,2652,10,62,48),(230423,2700,2700,75,596,349),
    (260166,3049,3049,279,2134,1151),(355170,4200,4200,625,4112,2048),
    (522058,6248,6248,906,5250,1790),(664133,8038,8038,1495,8451,3198),
    (914940,11236,11236,2753,16592,7291),
    (1473022,18527,18527,4128,22587,7316),
]


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    checkpoint = json.loads(CHECKPOINT.read_text())
    ledger = checkpoint["ledger"]
    require(checkpoint["status"] == "RESUMABLE_AFTER_COMPLETED_ROUND"
            and checkpoint["completed_rounds"] == len(ledger) == 27,
            "incremental checkpoint header changed")
    require(len(checkpoint["processed_columns"]) == 18_527
            and len(checkpoint["pending_columns"]) == 7_316,
            "processed/pending column census changed")
    for index, (record, expected) in enumerate(zip(ledger, FROZEN)):
        observed = tuple(record[key] for key in (
            "rows", "columns", "rank", "dual_support",
            "incident_column_orbits", "new_violating_column_orbits"))
        require(observed == expected and record["frozen_shape_match"] is True,
                f"incremental frozen guard changed at round {index}")

    with BASIS.open("rb") as source:
        require(source.read(16) == b"FH_D12_BASIS_V1\0",
                "basis magic changed")
        prime, coordinates, rank = struct.unpack("<QQQ", source.read(24))
    require((prime, coordinates, rank)
            == (1_073_741_827, 1_473_022, 18_527),
            "basis header changed")
    with ROWS.open("rb") as source:
        row_count = struct.unpack("<Q", source.read(8))[0]
    require(row_count == coordinates, "row/basis coordinate census differs")

    payload = {
        "format": "n8-fh-degree12-incremental-bounded-v1",
        "status": "BOUNDED_RESUMABLE_UNRESOLVED",
        "completed_rounds": len(ledger),
        "all_frozen_r0_r26_shape_guards_pass": True,
        "last_fully_accepted_round": ledger[-1],
        "resumable_state": {
            "processed_column_orbits": 18_527,
            "pending_crossing_column_orbits": 7_316,
            "row_coordinates": 1_473_022,
            "basis_rank": 18_527,
            "basis_file": BASIS.name,
            "rows_file": ROWS.name,
            "checkpoint_file": CHECKPOINT.name,
            "basis_sha256": sha256(BASIS.read_bytes()).hexdigest(),
            "rows_sha256": sha256(ROWS.read_bytes()).hexdigest(),
            "checkpoint_sha256": sha256(CHECKPOINT.read_bytes()).hexdigest(),
        },
        "discarded_partial_round": {
            "round": 27,
            "new_columns_total": 7_316,
            "full_rank_verified_through_new_column": 7_168,
            "partial_rank": 18_527 + 7_168,
            "reason": "1200-second hard wall",
            "inference": "none",
        },
        "incremental_theorem_guard": (
            "every old column has zero coefficient on every newly discovered "
            "row; the order-preserving row embedding therefore preserves the "
            "old echelon basis and only pending columns need reduction"
        ),
        "engine_sha256": sha256(ENGINE.read_bytes()).hexdigest(),
        "driver_sha256": sha256(DRIVER.read_bytes()).hexdigest(),
        "scope": (
            "modular full normalized Fh homogeneous degree12 only; no exact "
            "membership/nonmembership, truncated C10, degree13, saturation, "
            "or global inference"
        ),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LOGICAL_SHA256 is not None:
        require(payload["logical_sha256"] == EXPECTED_LOGICAL_SHA256,
                "incremental bounded result changed")
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("incremental bounded checkpoint: PASS")
    print("logical", payload["logical_sha256"])


if __name__ == "__main__":
    main()
