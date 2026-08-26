#!/usr/bin/env python3
"""Independent literal replay of the cap-1m D11 checkpoint pair."""

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
OUTPUT = HERE / "production_cap1m_resume_p1073741827_triangle_endpoint_colour"
SEED = HERE / "sealed_resume_input/selected.tsv"
PARENT_VALIDATOR = REPO / "computations/unaudited-codex-n8-x5-d11-triangle-resume16-design-2026-08-25/validate_resume_checkpoint.py"
PRIME, DEGREE, T = 1_073_741_827, 11, 361
PINS = {
    "provider": "06df5052a50099dc400d622323257fef9b3077a791f918c8f1c46d7bf7a5782c",
    "parent_validator": "89eafe8de1519bd2bd8f5937933ab2a8fd6279563f02b53068ae5cdde841b738",
    "seed_selected": "e19fbb6b57ae672a130c38c03783845e39dceaea795ff371ec07973f6d8e82d5",
    "selected": "81b4c5b8f929b26a8a7dc839a3638c8be9bd7973df843c131e4fc0b1056313c8",
    "dual": "c2c0d95e2063e1437e05b42169879d018031a6b5625955bd548cbca4880ca284",
    "result": "84e645dfc9cfad8368670524bab9840fd2d559b2395d7c5d4a01f71062407dcc",
    "watchdog": "97812ba2b400e45f238e73064d8031440d14b0a4891f50bdc01bead0acab7d27",
    "run_summary": "72541299de5f6b09e5a7075c3f82f501dd132935d4f0f5cf287c0af37b168180",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def main() -> None:
    started = time.monotonic()
    assert sha(PARENT_VALIDATOR) == PINS["parent_validator"]
    spec = importlib.util.spec_from_file_location("parent_replay", PARENT_VALIDATOR)
    replay = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(replay)
    assert sha(replay.PROVIDER) == PINS["provider"]
    paths = {name: OUTPUT / filename for name, filename in (
        ("selected", "selected.tsv"), ("dual", "dual.tsv"), ("result", "result.json"),
        ("watchdog", "watchdog.json"), ("run_summary", "run_summary.json"))}
    assert sha(SEED) == PINS["seed_selected"]
    for name, path in paths.items():
        assert sha(path) == PINS[name]

    watchdog = json.loads(paths["watchdog"].read_text())
    assert watchdog["status"] == "FAIL_CLOSED" and watchdog["breach"] is None
    assert watchdog["returncode"] == 0 and watchdog["engine_status"] == "INCOMPLETE_COLUMN_CAP"
    assert watchdog["engine_status_class"] is None and watchdog["result_exists"]
    assert watchdog["restart_pair_available"] and watchdog["peak_rss_kib"] == 20_707_504
    assert watchdog["peak_rss_kib"] < watchdog["rss_limit_kib"] == 32 * 1024 * 1024
    result = json.loads(paths["result"].read_text())
    assert result["status"] == "INCOMPLETE_COLUMN_CAP"
    assert result["incomplete_reason"] == "MORE_VIOLATING_COLUMNS_THAN_REMAINING_CAPACITY"
    assert result["mathematical_verdict"] is None and result["global_modular_dual"] is None
    assert result["resumed_columns"] == 515_869 and result["selected_columns"] == 913_636
    assert result["dual_support"] == 924_170 and result["column_cap"] == 1_000_000
    assert result["prime"] == PRIME and result["degree"] == DEGREE
    assert len(result["rounds"]) == 2
    assert result["rounds"][0]["columns_before"] == 515_869
    assert result["rounds"][0]["new_violations"] == 397_767
    assert result["rounds"][0]["columns_after"] == 913_636
    assert result["rounds"][1]["new_violations"] == 86_365
    assert result["rounds"][1]["columns_after"] == 913_636

    summary = json.loads(paths["run_summary"].read_text())
    assert summary["status"] == "FAIL_CLOSED" and summary["result_status"] == "INCOMPLETE_COLUMN_CAP"
    assert not summary["second_prime_launched"] and not summary["other_branch_launched"]
    assert not summary["degree_twelve_launched"]

    dual_lines = paths["dual"].read_text().splitlines()
    assert dual_lines[0].split("\t") == ["KRENN_X5_BLOCKER_D11_MODULAR_DUAL_V1", str(PRIME), "924170", "1"]
    dual = {}
    previous = None
    for line in dual_lines[1:]:
        kind, raw, raw_value = line.split("\t")
        row, value = tuple(map(int, raw.split(","))), int(raw_value)
        assert kind == "ROW" and len(row) == DEGREE and row == tuple(sorted(row))
        assert all(0 <= item <= T for item in row)
        assert previous is None or previous < row
        assert row not in dual and 0 < value < PRIME
        dual[row], previous = value, row
    assert len(dual) == 924_170 and dual[(T,) * DEGREE] == 1

    generators = replay.load_provider()
    columns, failures = replay.parse_columns(paths["selected"], generators, dual)
    assert len(columns) == 913_636 and not failures
    seed_columns, seed_failures = replay.parse_columns(SEED, generators)
    assert len(seed_columns) == 515_869 and not seed_failures
    assert set(seed_columns).issubset(columns)

    audit = {
        "schema": "KRENN_X5_D11_TRIANGLE_CAP1M_RESUME32_CHECKPOINT_AUDIT_V1",
        "status": "PASS_FAIL_CLOSED_COLUMN_CAP_CHECKPOINT_CAP1M",
        "resource_terminal": "INCOMPLETE_COLUMN_CAP",
        "mathematical_verdict": None,
        "prime": PRIME,
        "degree": DEGREE,
        "seed_selected_columns": len(seed_columns),
        "selected_columns": len(columns),
        "new_selected_columns": len(columns) - len(seed_columns),
        "seed_subset_preserved": True,
        "dual_support": len(dual),
        "target_coefficient": 1,
        "selected_pairings_replayed": len(columns),
        "pairing_failures": 0,
        "global_incident_scan_terminal": False,
        "selected_sha256": PINS["selected"],
        "dual_sha256": PINS["dual"],
        "result_sha256": PINS["result"],
        "watchdog_sha256": PINS["watchdog"],
        "run_summary_sha256": PINS["run_summary"],
        "provider_sha256": PINS["provider"],
        "elapsed_seconds": time.monotonic() - started,
        "second_prime_launched": False,
        "other_branch_launched": False,
        "degree_twelve_launched": False,
    }
    atomic(OUTPUT / "checkpoint_audit.json", audit)
    print(json.dumps(audit, sort_keys=True))


if __name__ == "__main__":
    main()
