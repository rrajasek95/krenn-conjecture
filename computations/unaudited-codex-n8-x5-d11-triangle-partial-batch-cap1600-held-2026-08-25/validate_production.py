#!/usr/bin/env python3
"""Frozen literal checkpoint acceptance for a future cap-1.6m run."""

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import time

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PARENT = REPO / "computations/unaudited-codex-n8-x5-d11-triangle-partial-batch-production-held-2026-08-25"
REPLAY_SOURCE = REPO / "computations/unaudited-codex-n8-x5-d11-triangle-resume16-design-2026-08-25/validate_resume_checkpoint.py"
OUTPUT = HERE / "production_cap1600_p107"
PRIME, DEGREE, T = 1_073_741_827, 11, 361
PINS = {
    "acceptance": "c17c8dc7b1fcd9506e35a84ede66a2770dc4f094bddd783f68a277c99dd2fd5b",
    "parent_manifest": "6a392f8f65d9ef921227b57d3fcb560e85f327eeb3b03d5750ee26d9d9bbe88b",
    "source": "a5d91a457e1cfdac45b033e31b32a52f65ff1d7f3f86fa229e28f68e20f21e5f",
    "binary": "224f5d0ad9043b62946fc68a70d18b9885f59c4cf1262d9417f5b160e82ae1a8",
    "provider": "06df5052a50099dc400d622323257fef9b3077a791f918c8f1c46d7bf7a5782c",
    "parent_validator": "89eafe8de1519bd2bd8f5937933ab2a8fd6279563f02b53068ae5cdde841b738",
    "seed_selected": "3218c0c3b2dd357a12dc87fb8bc139e03379d5ef434166b6d481db9a34af98b5",
    "seed_dual": "6ba8e603921e0c7c3eb1e92026e46aa42dde94bc18ed8452acf272d193cfbcdd",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_dual(path: Path):
    lines = path.read_text().splitlines()
    header = lines[0].split("\t")
    assert header[:2] == ["KRENN_X5_BLOCKER_D11_MODULAR_DUAL_V1", str(PRIME)]
    assert int(header[2]) == len(lines) - 1 and header[3] == "1"
    dual, previous = {}, None
    for line in lines[1:]:
        kind, raw, raw_value = line.split("\t")
        row, value = tuple(map(int, raw.split(","))), int(raw_value)
        assert kind == "ROW" and len(row) == DEGREE and row == tuple(sorted(row))
        assert previous is None or previous < row
        assert row not in dual and 0 < value < PRIME
        dual[row], previous = value, row
    assert dual[(T,) * DEGREE] == 1
    return dual


def atomic(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def main() -> None:
    started = time.monotonic()
    assert sha(HERE / "LAUNCH_ACCEPTANCE.json") == PINS["acceptance"]
    assert sha(PARENT / "PRODUCTION_MANIFEST.sha256") == PINS["parent_manifest"]
    assert sha(HERE / "src/main.rs") == PINS["source"]
    assert sha(HERE / "x5_d11_partial_batch_cap1600") == PINS["binary"]
    seed_selected_path = PARENT / "production_partial_batch_p107/selected.tsv"
    seed_dual_path = PARENT / "production_partial_batch_p107/dual.tsv"
    assert sha(seed_selected_path) == PINS["seed_selected"] and sha(seed_dual_path) == PINS["seed_dual"]
    assert sha(REPLAY_SOURCE) == PINS["parent_validator"]
    spec = importlib.util.spec_from_file_location("literal_replay", REPLAY_SOURCE)
    replay = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(replay)
    assert sha(replay.PROVIDER) == PINS["provider"]

    result_path, selected_path, dual_path = (OUTPUT / name for name in
                                             ("result.json", "selected.tsv", "dual.tsv"))
    watchdog_path = OUTPUT / "watchdog.json"
    for path in (result_path, selected_path, dual_path, watchdog_path):
        assert path.is_file()
    assert not list(OUTPUT.glob("*.tmp"))
    result, watchdog = json.loads(result_path.read_text()), json.loads(watchdog_path.read_text())
    assert result["schema"] == "KRENN_X5_FOUR_BLOCKER_D11_PARTIAL_BATCH_RESULT_V1"
    assert result["prime"] == PRIME and result["resumed_columns"] == 1_250_001
    assert result["column_cap"] == 1_600_000 and result["mathematical_verdict"] is None
    assert watchdog["breach"] is None and watchdog["returncode"] == 0
    assert watchdog["peak_rss_kib"] < watchdog["rss_limit_kib"] == 38 * 1024 * 1024
    assert watchdog["wall_limit_seconds"] == 600
    current = 1_250_001
    for round_record in result["rounds"]:
        assert round_record["columns_before"] == current
        observed, accepted = round_record["violations_observed"], round_record["violations_accepted"]
        assert round_record["incident_columns_checked"] > 0 and 0 < accepted <= observed
        if round_record["canonical_partial_batch"]:
            assert observed > 1_600_000 - current
            assert accepted == 1_600_000 - current
        else:
            assert accepted == observed
        current += accepted
        assert round_record["columns_after"] == current and round_record["support_after"] > 0
    assert result["selected_columns"] == current <= 1_600_000
    if result["status"] == "INCOMPLETE_COLUMN_CAP":
        assert current == 1_600_000 and current > 1_250_001
    elif result["status"] == "COMPLETE_MODULAR_DUAL_DIAGNOSTIC":
        assert result["global_modular_dual"] is True
    elif result["status"] == "INCOMPLETE_WALL_CAP":
        assert current > 1_250_001
    else:
        raise AssertionError("unaccepted terminal status")

    output_dual = load_dual(dual_path)
    generators = replay.load_provider()
    columns, failures = replay.parse_columns(selected_path, generators, output_dual)
    seed_columns, seed_failures = replay.parse_columns(seed_selected_path, generators)
    assert len(columns) == current and len(seed_columns) == 1_250_001
    assert not failures and not seed_failures and set(seed_columns).issubset(columns)
    audit = {
        "schema": "KRENN_X5_D11_TRIANGLE_PARTIAL_BATCH_CAP1600_AUDIT_V1",
        "status": "PASS_EXACT_CHECKPOINT",
        "engine_status": result["status"],
        "mathematical_verdict": None,
        "seed_selected_columns": len(seed_columns),
        "selected_columns": len(columns),
        "new_selected_columns": len(columns) - len(seed_columns),
        "seed_subset_preserved": True,
        "dual_support": len(output_dual),
        "target_coefficient": output_dual[(T,) * DEGREE],
        "selected_pairings_replayed": len(columns),
        "pairing_failures": 0,
        "selected_sha256": sha(selected_path),
        "dual_sha256": sha(dual_path),
        "result_sha256": sha(result_path),
        "watchdog_sha256": sha(watchdog_path),
        "elapsed_seconds": time.monotonic() - started,
        "second_prime": False,
        "other_branch": False,
        "degree_twelve_read": False,
        "automatic_relaunch": False,
    }
    atomic(OUTPUT / "checkpoint_audit.json", audit)
    print(json.dumps(audit, sort_keys=True))


if __name__ == "__main__":
    main()
