#!/usr/bin/env python3
"""Freeze/replay the bounded Rust Fh-D12 CEGAR checkpoint without solving."""

import json
from hashlib import sha256
from pathlib import Path


HERE = Path(__file__).resolve().parent
CHECKPOINT = HERE / "checkpoint_fh_degree12_rust_cegar.json"
BINARY = HERE / "target/release/fh-d12-moddual"
DRIVER = HERE / "run_fh_degree12_rust_cegar.py"
RESULT = HERE / "results_fh_degree12_rust_cegar.json"
EXPECTED_LOGICAL_SHA256 = (
    "f60c9441192a94fbeaf4f3a68b0ccdd6a5977c50d5ef402782336881d685e09e"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    checkpoint = json.loads(CHECKPOINT.read_text())
    ledger = checkpoint["ledger"]
    require(checkpoint["format"] == "n8-fh-degree12-rust-cegar-checkpoint-v1"
            and checkpoint["status"] == "RESUMABLE_AFTER_COMPLETED_ROUND"
            and checkpoint["next_round"] == len(ledger) == 27,
            "resumable checkpoint header changed")
    require(len(checkpoint["columns"]) == 25_843,
            "r27 admitted-column checkpoint changed")
    r22 = ledger[22]
    require(tuple(r22[key] for key in (
        "rows", "columns", "rank", "dual_support",
        "incident_column_orbits", "new_violating_column_orbits",
    )) == (355_170, 4_200, 4_200, 625, 4_112, 2_048)
            and r22["python_exact_q_shape_match"] is True,
            "Rust did not reproduce authoritative Python r22")
    r26 = ledger[26]
    require(tuple(r26[key] for key in (
        "rows", "columns", "rank", "dual_support",
        "incident_column_orbits", "new_violating_column_orbits",
    )) == (1_473_022, 18_527, 18_527, 4_128, 22_587, 7_316),
            "terminal accepted r26 checkpoint changed")
    require(all(record["rank"] == record["columns"] for record in ledger),
            "an accepted modular interface lost full column rank")

    payload = {
        "format": "n8-fh-degree12-rust-cegar-bounded-v1",
        "status": "BOUNDED_RESUMABLE_UNRESOLVED",
        "completed_rounds": len(ledger),
        "authoritative_python_r22_reproduced": True,
        "last_completed_round": r26,
        "resume_state": {
            "next_round": checkpoint["next_round"],
            "admitted_column_orbits": len(checkpoint["columns"]),
            "checkpoint_file": CHECKPOINT.name,
            "checkpoint_sha256": sha256(CHECKPOINT.read_bytes()).hexdigest(),
        },
        "discarded_partial_round": {
            "round": 27,
            "matrix_column_orbits": 25_843,
            "full_rank_verified_through_vector": 17_152,
            "reason": "20-minute hard wall",
            "inference": "none",
        },
        "engine": {
            "prime": 1_073_741_827,
            "binary_sha256": sha256(BINARY.read_bytes()).hexdigest(),
            "driver_sha256": sha256(DRIVER.read_bytes()).hexdigest(),
            "deterministic_policy": (
                "least coordinate sparse pivots; add every crossing orbit; "
                "exact-Q replay required before any modular stall is promoted"
            ),
        },
        "scope": (
            "full normalized F^h homogeneous degree12 mixed ideal only; "
            "no membership/nonmembership, truncated C10, degree13, "
            "saturation, or global inference"
        ),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LOGICAL_SHA256 is not None:
        require(payload["logical_sha256"] == EXPECTED_LOGICAL_SHA256,
                "bounded Rust ledger changed")
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("bounded Rust full-Fh D12 checkpoint: PASS")
    print("logical", payload["logical_sha256"])


if __name__ == "__main__":
    main()
