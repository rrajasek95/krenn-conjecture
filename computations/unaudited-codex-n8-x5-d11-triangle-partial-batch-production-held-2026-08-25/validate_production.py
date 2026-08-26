#!/usr/bin/env python3
"""Frozen exact acceptance/replay for the one partial-batch production run."""

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
DESIGN = REPO / "computations/unaudited-codex-n8-x5-d11-triangle-partial-batch-held-2026-08-25"
OUTPUT = HERE / "production_partial_batch_p107"
PARENT = REPO / "computations/unaudited-codex-n8-x5-d11-triangle-resume16-design-2026-08-25/validate_resume_checkpoint.py"
PRIME, DEGREE, T = 1_073_741_827, 11, 361
PINS = {
    "acceptance": "cdfe4d47dcc9d11e05be0bfb65bda269ca5ec5f5d9003ae7fc57db19da4c90c0",
    "design_manifest": "54c4d29df4c77ffc3b678d72e01a60ac694a866f29c280501108314ab3365e7a",
    "parent_validator": "89eafe8de1519bd2bd8f5937933ab2a8fd6279563f02b53068ae5cdde841b738",
    "provider": "06df5052a50099dc400d622323257fef9b3077a791f918c8f1c46d7bf7a5782c",
    "source": "261f03cfcf9bd86de1e97e2f56221e51d8597ed3f2aa9f7ab30aa092b18be889",
    "binary": "72c8a091a2a58a444121fc178ea1b71a16e580d49546e54a996e2508685b7e98",
    "seed_selected": "81b4c5b8f929b26a8a7dc839a3638c8be9bd7973df843c131e4fc0b1056313c8",
    "seed_dual": "c2c0d95e2063e1437e05b42169879d018031a6b5625955bd548cbca4880ca284",
    "prior_gate_selected": "8f7d84e13e019f0c8e02a2668d75740fee07bd27707c2e60ec6e0385f32957ed",
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


def pairing(column, generators, dual):
    generator, multiplier = column
    return sum(coefficient * dual.get(tuple(sorted(term + multiplier)), 0)
               for term, coefficient in generators[generator][1]) % PRIME


def atomic(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def main() -> None:
    started = time.monotonic()
    assert sha(HERE / "LAUNCH_ACCEPTANCE.json") == PINS["acceptance"]
    assert sha(DESIGN / "MANIFEST.sha256") == PINS["design_manifest"]
    assert sha(DESIGN / "src/main.rs") == PINS["source"]
    assert sha(DESIGN / "x5_d11_partial_batch") == PINS["binary"]
    assert sha(DESIGN / "seed_selected.tsv") == PINS["seed_selected"]
    assert sha(DESIGN / "seed_dual.tsv") == PINS["seed_dual"]
    assert sha(DESIGN / "current_seed_gate/selected.tsv") == PINS["prior_gate_selected"]
    assert sha(PARENT) == PINS["parent_validator"]
    spec = importlib.util.spec_from_file_location("parent_replay", PARENT)
    replay = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(replay)
    assert sha(replay.PROVIDER) == PINS["provider"]

    result_path, selected_path, dual_path = (OUTPUT / name for name in
                                             ("result.json", "selected.tsv", "dual.tsv"))
    watchdog_path, summary_path = OUTPUT / "watchdog.json", OUTPUT / "run_summary.json"
    for path in (result_path, selected_path, dual_path, watchdog_path, summary_path):
        assert path.is_file()
    assert not list(OUTPUT.glob("*.tmp"))
    result = json.loads(result_path.read_text())
    watchdog = json.loads(watchdog_path.read_text())
    summary = json.loads(summary_path.read_text())
    assert watchdog["status"] == "PASS_RESTART_CHECKPOINT"
    assert watchdog["breach"] is None and watchdog["returncode"] == 0
    assert watchdog["engine_status"] == "INCOMPLETE_COLUMN_CAP"
    assert watchdog["peak_rss_kib"] < watchdog["rss_limit_kib"] == 38 * 1024 * 1024
    assert watchdog["wall_limit_seconds"] == 600
    assert result["schema"] == "KRENN_X5_FOUR_BLOCKER_D11_PARTIAL_BATCH_RESULT_V1"
    assert result["status"] == "INCOMPLETE_COLUMN_CAP"
    assert result["incomplete_reason"] == "CANONICAL_VIOLATION_PREFIX_ACCEPTED_AND_SELECTED_COLUMN_CAP_REACHED"
    assert result["resumed_columns"] == 913_636 and result["selected_columns"] == 1_250_001
    assert result["column_cap"] == 1_250_001 and result["prime"] == PRIME
    assert result["mathematical_verdict"] is None and result["global_modular_dual"] is None
    assert len(result["rounds"]) == 1
    round0 = result["rounds"][0]
    assert round0 == {
        **round0,
        "columns_before": 913_636,
        "incident_columns_checked": 762_110,
        "violations_observed": 730_426,
        "violations_accepted": 336_365,
        "canonical_partial_batch": True,
        "columns_after": 1_250_001,
    }
    assert summary["returncode"] == 0 and summary["result_exists"]
    assert summary["watchdog_exists"] and not summary["automatic_relaunch"]
    assert not summary["second_prime_launched"] and not summary["other_branch_launched"]
    assert not summary["degree_twelve_read"]

    generators = replay.load_provider()
    output_dual = load_dual(dual_path)
    seed_dual = load_dual(DESIGN / "seed_dual.tsv")
    columns, failures = replay.parse_columns(selected_path, generators, output_dual)
    seed_columns, seed_failures = replay.parse_columns(DESIGN / "seed_selected.tsv", generators)
    prior_columns, prior_failures = replay.parse_columns(DESIGN / "current_seed_gate/selected.tsv", generators)
    assert len(columns) == 1_250_001 and len(seed_columns) == 913_636
    assert len(prior_columns) == 913_644 and not failures and not seed_failures and not prior_failures
    column_set, seed_set = set(columns), set(seed_columns)
    new_columns = sorted(column_set - seed_set)
    prior_new = sorted(set(prior_columns) - seed_set)
    assert len(new_columns) == 336_365 and seed_set.issubset(column_set)
    assert new_columns[:8] == prior_new
    assert all(pairing(column, generators, seed_dual) != 0 for column in new_columns)

    audit = {
        "schema": "KRENN_X5_D11_TRIANGLE_PARTIAL_BATCH_PRODUCTION_AUDIT_V1",
        "status": "PASS_EXACT_RESTART_CHECKPOINT",
        "mathematical_verdict": None,
        "prime": PRIME,
        "seed_selected_columns": len(seed_columns),
        "selected_columns": len(columns),
        "new_selected_columns": len(new_columns),
        "seed_subset_preserved": True,
        "canonical_prefix_first8_matches_prior_gate": True,
        "all_new_columns_were_seed_violations": True,
        "full_incident_columns_checked": round0["incident_columns_checked"],
        "full_violations_observed": round0["violations_observed"],
        "dual_support": len(output_dual),
        "target_coefficient": output_dual[(T,) * DEGREE],
        "selected_pairings_replayed": len(columns),
        "pairing_failures": 0,
        "selected_sha256": sha(selected_path),
        "dual_sha256": sha(dual_path),
        "result_sha256": sha(result_path),
        "watchdog_sha256": sha(watchdog_path),
        "run_summary_sha256": sha(summary_path),
        "elapsed_seconds": time.monotonic() - started,
        "second_prime_launched": False,
        "other_branch_launched": False,
        "degree_twelve_read": False,
        "automatic_relaunch": False,
    }
    atomic(OUTPUT / "checkpoint_audit.json", audit)
    print(json.dumps(audit, sort_keys=True))


if __name__ == "__main__":
    main()
