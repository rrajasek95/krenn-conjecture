#!/usr/bin/env python3
"""Independent literal replay of the bounded current-seed partial-batch gate."""

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
OUTPUT = HERE / "current_seed_gate"
SEED_SELECTED = HERE / "seed_selected.tsv"
SEED_DUAL = HERE / "seed_dual.tsv"
PARENT = REPO / "computations/unaudited-codex-n8-x5-d11-triangle-resume16-design-2026-08-25/validate_resume_checkpoint.py"
PRIME, DEGREE, T = 1_073_741_827, 11, 361
PINS = {
    "parent": "89eafe8de1519bd2bd8f5937933ab2a8fd6279563f02b53068ae5cdde841b738",
    "provider": "06df5052a50099dc400d622323257fef9b3077a791f918c8f1c46d7bf7a5782c",
    "seed_selected": "81b4c5b8f929b26a8a7dc839a3638c8be9bd7973df843c131e4fc0b1056313c8",
    "seed_dual": "c2c0d95e2063e1437e05b42169879d018031a6b5625955bd548cbca4880ca284",
    "selected": "8f7d84e13e019f0c8e02a2668d75740fee07bd27707c2e60ec6e0385f32957ed",
    "dual": "16739f78f73f5a3d80d453a0c9018da0dc04b480d28ee228e1d727003ab7cd2a",
    "result": "14b45b263a515bf4752dd50009042a167b5e87d1dd901b96d66c188574e094ff",
    "watchdog": "5ee221db3a96262ce5ad8e2f385bb3e271367bb1d8bac18148ef60b6754b44a0",
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
    assert sha(PARENT) == PINS["parent"]
    spec = importlib.util.spec_from_file_location("parent_replay", PARENT)
    replay = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(replay)
    assert sha(replay.PROVIDER) == PINS["provider"]
    assert sha(SEED_SELECTED) == PINS["seed_selected"]
    assert sha(SEED_DUAL) == PINS["seed_dual"]
    paths = {name: OUTPUT / f"{name}.tsv" for name in ("selected", "dual")}
    paths.update({name: OUTPUT / f"{name}.json" for name in ("result", "watchdog")})
    for name, path in paths.items():
        assert sha(path) == PINS[name]

    result = json.loads(paths["result"].read_text())
    watchdog = json.loads(paths["watchdog"].read_text())
    assert result["schema"] == "KRENN_X5_FOUR_BLOCKER_D11_PARTIAL_BATCH_RESULT_V1"
    assert result["status"] == "INCOMPLETE_COLUMN_CAP"
    assert result["incomplete_reason"] == "CANONICAL_VIOLATION_PREFIX_ACCEPTED_AND_SELECTED_COLUMN_CAP_REACHED"
    assert result["resumed_columns"] == 913_636 and result["selected_columns"] == 913_644
    assert result["dual_support"] == 924_182 and result["column_cap"] == 913_644
    assert result["prime"] == PRIME and result["global_modular_dual"] is None
    assert result["mathematical_verdict"] is None and len(result["rounds"]) == 1
    round0 = result["rounds"][0]
    assert round0["columns_before"] == 913_636 and round0["columns_after"] == 913_644
    assert round0["incident_columns_checked"] == 762_110
    assert round0["violations_observed"] == 730_426
    assert round0["violations_accepted"] == 8 and round0["canonical_partial_batch"] is True
    assert watchdog["status"] == "PASS_RESTART_CHECKPOINT" and watchdog["breach"] is None
    assert watchdog["returncode"] == 0 and watchdog["engine_status"] == result["status"]
    assert watchdog["peak_rss_kib"] == 19_864_288
    assert watchdog["peak_rss_kib"] < watchdog["rss_limit_kib"] == 38 * 1024 * 1024

    generators = replay.load_provider()
    output_dual = load_dual(paths["dual"])
    seed_dual = load_dual(SEED_DUAL)
    columns, failures = replay.parse_columns(paths["selected"], generators, output_dual)
    seed_columns, seed_failures = replay.parse_columns(SEED_SELECTED, generators)
    assert len(columns) == 913_644 and len(seed_columns) == 913_636
    assert not failures and not seed_failures
    new_columns = sorted(set(columns) - set(seed_columns))
    assert len(new_columns) == 8 and set(seed_columns).issubset(columns)
    seed_pairings = [pairing(column, generators, seed_dual) for column in new_columns]
    assert all(value != 0 for value in seed_pairings)

    audit = {
        "schema": "KRENN_X5_D11_TRIANGLE_PARTIAL_BATCH_CURRENT_SEED_GATE_AUDIT_V1",
        "status": "PASS_DIAGNOSTIC_PARTIAL_BATCH",
        "mathematical_verdict": None,
        "seed_selected_columns": len(seed_columns),
        "selected_columns": len(columns),
        "accepted_columns": len(new_columns),
        "all_accepted_were_seed_violations": True,
        "accepted_seed_pairings": seed_pairings,
        "dual_support": len(output_dual),
        "target_coefficient": output_dual[(T,) * DEGREE],
        "selected_pairings_replayed": len(columns),
        "pairing_failures": 0,
        "seed_subset_preserved": True,
        "source_frontier_fully_scanned": True,
        "incident_columns_checked": round0["incident_columns_checked"],
        "violations_observed": round0["violations_observed"],
        "peak_rss_kib": watchdog["peak_rss_kib"],
        "elapsed_seconds": time.monotonic() - started,
        "production_coverage": 0,
        "degree_twelve_read": False,
    }
    atomic(OUTPUT / "checkpoint_audit.json", audit)
    print(json.dumps(audit, sort_keys=True))


if __name__ == "__main__":
    main()
