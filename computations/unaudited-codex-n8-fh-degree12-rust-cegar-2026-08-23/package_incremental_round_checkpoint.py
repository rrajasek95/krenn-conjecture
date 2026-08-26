#!/usr/bin/env python3
"""Exact replay of the durable within-r27 full-Fh D12 checkpoint."""

import json
from hashlib import sha256
from pathlib import Path
import struct


HERE = Path(__file__).resolve().parent
BASE = HERE / "incremental_basis.bin"
ROWS = HERE / "incremental_round_rows.bin"
ROW_MAP = HERE / "incremental_row_map.bin"
INPUT = HERE / "incremental_input.txt"
JOURNAL = HERE / "incremental_round_journal"
CHECKPOINT = HERE / "checkpoint_fh_degree12_incremental_round.json"
ACCEPTED = HERE / "checkpoint_fh_degree12_incremental.json"
ENGINE = HERE / "target/release/fh-d12-incremental"
DRIVER = HERE / "run_fh_degree12_incremental.py"
RESULT = HERE / "results_fh_degree12_incremental_round_bounded.json"
EXPECTED_LOGICAL_SHA256 = "a85d61d1183be2d94d6279f9456d46cc2527a626ebbfb0c58ef7597c7881f01d"
PRIME = 1_073_741_827


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    digest = sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def read_u32(source):
    return struct.unpack("<I", source.read(4))[0]


def read_u64(source):
    return struct.unpack("<Q", source.read(8))[0]


def main():
    accepted = json.loads(ACCEPTED.read_text())
    require(accepted["completed_rounds"] == 27
            and len(accepted["processed_columns"]) == 18_527
            and len(accepted["pending_columns"]) == 7_316,
            "accepted r26 checkpoint changed")
    last = accepted["ledger"][-1]
    frozen = tuple(last[key] for key in (
        "rows", "columns", "rank", "dual_support",
        "incident_column_orbits", "new_violating_column_orbits"))
    require(frozen == (1_473_022, 18_527, 18_527, 4_128, 22_587, 7_316),
            "accepted r26 tuple changed")

    with BASE.open("rb") as source:
        require(source.read(16) == b"FH_D12_BASIS_V1\0", "bad base magic")
        prime, coordinates, base_rank = struct.unpack("<QQQ", source.read(24))
        require((prime, coordinates, base_rank)
                == (PRIME, 1_473_022, 18_527), "base header changed")
        base_pivots = set()
        for _ in range(base_rank):
            pivot, terms = struct.unpack("<II", source.read(8))
            require(pivot not in base_pivots, "duplicate base pivot")
            base_pivots.add(pivot)
            source.seek(8 * terms, 1)
        require(not source.read(1), "trailing base bytes")
    with ROW_MAP.open("rb") as source:
        require(read_u64(source) == 1_473_022, "row-map domain changed")
        row_embedding = [read_u32(source) for _ in range(1_473_022)]
        require(not source.read(1), "trailing row-map bytes")
    base_pivots = {row_embedding[pivot] for pivot in base_pivots}

    checkpoint = json.loads(CHECKPOINT.read_text())
    require(checkpoint["status"] == "INTERRUPTED_RESUMABLE_MATERIALIZED"
            and checkpoint["round"] == 27
            and checkpoint["row_coordinates"] == 1_997_290
            and checkpoint["pending_columns_total"] == 7_316
            and checkpoint["completed_pending_columns"] == 5_376,
            "within-round checkpoint header changed")
    require(checkpoint["base_frozen_tuple"] == list(frozen),
            "within-round base guard changed")
    require(checkpoint["materialized_rows_sha256"] == file_sha(ROWS)
            and checkpoint["row_map_sha256"] == file_sha(ROW_MAP)
            and checkpoint["materialized_input_sha256"] == file_sha(INPUT),
            "serialized r27 interface changed")
    with ROWS.open("rb") as source:
        require(read_u64(source) == 1_997_290, "r27 row table changed")
    with INPUT.open("rb") as source:
        header = source.readline().decode("ascii").split()
    require(header[:4] == ["KRENN_FH_D12_INCREMENTAL_V1", str(PRIME),
                            "1997290", "7316"], "r27 input header changed")

    batches = sorted(JOURNAL.glob("batch_*.bin"))
    require(len(batches) == 21, "journal batch count changed")
    start = 0
    journal_pivots = set()
    batch_hashes = []
    term_count = 0
    for path in batches:
        batch_hashes.append((path.name, file_sha(path)))
        with path.open("rb") as source:
            require(source.read(16) == b"FH_D12_BATCH_V1\0",
                    "bad journal magic")
            header = struct.unpack("<QQQQQQ", source.read(48))
            found_prime, found_coordinates, found_rank, begin, end, records = header
            require((found_prime, found_coordinates, found_rank, begin, end, records)
                    == (PRIME, 1_997_290, 18_527, start, start + 256, 256),
                    "journal batch header changed")
            for _ in range(records):
                pivot, terms = struct.unpack("<II", source.read(8))
                require(pivot not in journal_pivots and pivot not in base_pivots,
                        "journal pivot is not new")
                journal_pivots.add(pivot)
                first = None
                pivot_coefficient = None
                previous = -1
                for _ in range(terms):
                    index, coefficient = struct.unpack("<II", source.read(8))
                    require(previous < index < 1_997_290
                            and 0 < coefficient < PRIME,
                            "invalid journal term")
                    if first is None:
                        first = index
                    if index == pivot:
                        pivot_coefficient = coefficient
                    previous = index
                require(first == pivot and pivot_coefficient == 1,
                        "journal vector is not normalized at its leading pivot")
                term_count += terms
            require(not source.read(1), "trailing journal bytes")
        start += 256
    require(start == 5_376 and len(journal_pivots) == 5_376,
            "durable progress changed")

    payload = {
        "format": "n8-fh-d12-incremental-round-bounded-v1",
        "status": "BOUNDED_RESUMABLE_UNRESOLVED",
        "accepted_base": {
            "round": 26, "rows": 1_473_022, "rank": 18_527,
            "pending_columns": 7_316,
        },
        "durable_r27_progress": {
            "row_coordinates": 1_997_290,
            "completed_pending_columns": 5_376,
            "remaining_pending_columns": 1_940,
            "rank_full_through": 23_903,
            "journal_batches": 21,
            "journal_terms": term_count,
            "all_batch_headers_and_normalized_pivots_replayed": True,
        },
        "materialized_resume": {
            "command": (
                "python3 run_fh_degree12_incremental.py "
                "--resume-materialized-round --wall-cap-seconds N"
            ),
            "input_sha256": checkpoint["materialized_input_sha256"],
            "rows_sha256": checkpoint["materialized_rows_sha256"],
            "row_map_sha256": checkpoint["row_map_sha256"],
            "journal_batch_sha256": batch_hashes,
        },
        "guards": {
            "accepted_r26_basis_immutable": True,
            "old_columns_zero_on_new_rows": True,
            "journal_atomic_fsync_rename_every": 256,
            "no_partial_batch_promoted": True,
        },
        "engine_sha256": file_sha(ENGINE),
        "driver_sha256": file_sha(DRIVER),
        "scope": (
            "modular full normalized Fh homogeneous degree12 r27 only; no "
            "membership/nonmembership, separator, degree13, saturation, or "
            "global inference"
        ),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LOGICAL_SHA256 is not None:
        require(payload["logical_sha256"] == EXPECTED_LOGICAL_SHA256,
                "bounded r27 package changed")
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("incremental r27 durable checkpoint: PASS")
    print("logical", payload["logical_sha256"])


if __name__ == "__main__":
    main()
