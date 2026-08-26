#!/usr/bin/env python3
"""Fail-closed mode hostiles for the frozen v4 sparse binary."""

import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
BINARY = ROOT / "target/release/sparse_d12_dual"
SOURCE = ROOT / "src/main.rs"
OUTPUT = ROOT / "results_hostiles.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def command(**updates: str) -> list[str]:
    values = {
        "--input": str(ROOT / "deliberately_absent_provider.ms"),
        "--output": str(ROOT / "hostile_result.json"),
        "--checkpoint": str(ROOT / "hostile_checkpoint.bin"),
        "--vector-cache": str(ROOT / "hostile_vectors.bin"),
        "--dual": str(ROOT / "hostile_dual.tsv"),
        "--prime": "1073741827",
        "--wall-seconds": "1",
        "--rss-gib": "1",
        "--workers": "16",
        "--pivot": "rare",
        "--strategy": "cold",
        "--elimination": "hierarchical",
        "--incremental": "no",
        "--portfolio-period": "256",
        "--portfolio-parallel": "yes",
        "--support-cap": "100000",
        "--column-cap": "1000000",
        "--round-cap": "951",
    }
    values.update(updates)
    argv = [str(BINARY)]
    for key, value in values.items():
        argv.extend([key, value])
    return argv


def main() -> None:
    cases = {
        "workers8": {"--workers": "8"},
        "pivot_first": {"--pivot": "first"},
        "strategy_repair": {"--strategy": "repair"},
        "elimination_vec": {"--elimination": "vec"},
        "incremental_yes": {"--incremental": "yes"},
        "round_cap_10001": {"--round-cap": "10001"},
    }
    records = {}
    for name, updates in cases.items():
        run = subprocess.run(command(**updates), text=True, capture_output=True, timeout=5)
        passed = (
            run.returncode == 2
            and (
                "v4 rare-order index requires fixed cold/rare/16 hierarchical nonincremental mode"
                in run.stderr
                or "hierarchical elimination requires explicit --workers 16 --pivot rare --strategy cold --incremental no"
                in run.stderr
                or "incremental mode requires tree elimination" in run.stderr
                or "bad sparse search cap" in run.stderr
            )
            and not any((ROOT / suffix).exists() for suffix in (
                "hostile_result.json", "hostile_checkpoint.bin", "hostile_vectors.bin", "hostile_dual.tsv"
            ))
        )
        if not passed:
            raise SystemExit(f"hostile failed: {name}: rc={run.returncode}: {run.stderr}")
        records[name] = {"status": "PASS_REJECTED", "returncode": run.returncode}
    result = {
        "schema": "KRENN_AFFINE251_D12_RARE_ORDER_V4_HOSTILES_V1",
        "status": "PASS",
        "source_sha256": sha256(SOURCE),
        "binary_sha256": sha256(BINARY),
        "cases": records,
    }
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, OUTPUT)


if __name__ == "__main__":
    main()
