#!/usr/bin/env python3
"""Fail-closed watchdog for the frozen read-only round849/850 order gate.

This script intentionally requires --production-clear before it hashes either
~1 GB cache.  It never copies or mutates either cache.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]
OLD = ROOT / "computations/unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/production_from_round749/stage04/vectors.bin"
NEW = ROOT / "computations/unaudited-codex-n8-affine251-d12-round850-portfolio-audit-2026-08-24/selected_control/vectors.bin"
BINARY = PACKAGE / "rare_order_index_gate"
RUNS = PACKAGE / "runs"
RESULT = RUNS / "result.json"
STDOUT = RUNS / "stdout.log"
STDERR = RUNS / "stderr.log"
WATCHDOG = RUNS / "watchdog.json"

EXPECTED = {
    OLD: "040b1b59bad7693fbd7ed71d8ff9f760b39b30943c77f452eae3b4047b5ac254",
    NEW: "df181c0b86de9a2827d1146a318682482b9af2cae66b470fdf5d11fa036d1ec4",
    BINARY: "2925fa2c47271da0376aa607c4ca3c2ccd274f3c94a4c2899fa14221d2bf8e58",
}
WALL_SECONDS = 120.0
RSS_LIMIT_KIB = 36 * 1024 * 1024


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(8 << 20):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, value: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)


def rss_kib(pid: int) -> int:
    try:
        result = subprocess.run(
            ["ps", "-o", "rss=", "-p", str(pid)],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return -1
    if result.returncode != 0:
        return -1
    try:
        return int(result.stdout.strip())
    except ValueError:
        return 0


def validate(result: dict, peak_rss_kib: int, elapsed: float) -> None:
    required = {
        "schema", "status", "scope", "prime", "provider_fingerprint",
        "round849", "round850", "incremental", "timings_seconds",
        "peak_rss_kib_phase_sampled", "mono_size_bytes",
        "ordered_tuple_size_bytes", "checkpoint_or_cache_written",
    }
    if set(result) != required:
        raise RuntimeError(("top-level result keys", sorted(set(result) ^ required)))
    if result["schema"] != "KRENN_AFF251_D12_RARE_ORDER_INDEX_GATE_V1":
        raise RuntimeError("schema")
    if result["status"] != "PASS_EXACT_ROUND849_850_ORDER_EQUIVALENCE":
        raise RuntimeError("status")
    if result["checkpoint_or_cache_written"] is not False:
        raise RuntimeError("mutation claim")
    if result["prime"] != 1073741827 or result["provider_fingerprint"] != 9218588987274412661:
        raise RuntimeError("prime/provider")
    old, new = result["round849"], result["round850"]
    if old["records"] != 460676 or old["terms"] != 46796079 or old["ranked_rows"] != 27357752:
        raise RuntimeError("round849 census")
    if new["records"] != 461464 or new["new_columns"] != 788:
        raise RuntimeError("round850 census")
    for state in (old, new):
        baseline = state["order_sha256_baseline"]
        indexed = state["order_sha256_index"]
        if baseline != indexed or len(baseline) != 64 or any(c not in "0123456789abcdef" for c in baseline):
            raise RuntimeError("order hash equality")
    inc = result["incremental"]
    if not (0 < inc["touched_rows"] <= 80267):
        raise RuntimeError("touched-row bound")
    if inc["added_rows"] - inc["removed_rows"] != new["ranked_rows"] - old["ranked_rows"]:
        raise RuntimeError("row census transition")
    if result["mono_size_bytes"] != 13 or result["ordered_tuple_size_bytes"] != 20:
        raise RuntimeError("layout")
    if peak_rss_kib >= RSS_LIMIT_KIB or elapsed >= WALL_SECONDS:
        raise RuntimeError("resource cap")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--production-clear", action="store_true")
    args = parser.parse_args()
    if not args.production_clear:
        print("REFUSED: --production-clear is required before cache hashing/benchmark", file=sys.stderr)
        return 2
    if rss_kib(os.getpid()) <= 0:
        raise RuntimeError("RSS_OBSERVER_UNAVAILABLE; refusing cache reads/launch")
    RUNS.mkdir(exist_ok=True)
    if RESULT.exists() or WATCHDOG.exists():
        print("REFUSED: result/watchdog already exists; preserve atomic evidence", file=sys.stderr)
        return 2

    for path, expected in EXPECTED.items():
        if expected.startswith("__"):
            raise RuntimeError(f"unsealed expected hash for {path}")
        actual = sha256(path)
        if actual != expected:
            raise RuntimeError(("input/binary hash", str(path), expected, actual))

    command = [
        str(BINARY),
        "--old-cache", str(OLD),
        "--new-cache", str(NEW),
        "--output", str(RESULT),
        "--expected-old-records", "460676",
        "--expected-new-records", "461464",
        "--expected-new-columns", "788",
        "--wall-seconds", "120",
        "--rss-gib", "36",
    ]
    started = time.monotonic()
    peak = 0
    with STDOUT.open("xb") as stdout, STDERR.open("xb") as stderr:
        process = subprocess.Popen(command, stdout=stdout, stderr=stderr)
        reason = None
        while process.poll() is None:
            elapsed = time.monotonic() - started
            observed_rss = rss_kib(process.pid)
            if observed_rss < 0:
                reason = "RSS_OBSERVER_FAILURE"
            else:
                peak = max(peak, observed_rss)
            if elapsed >= WALL_SECONDS:
                reason = "WALL_CAP"
            elif peak >= RSS_LIMIT_KIB:
                reason = "RSS_CAP"
            if reason:
                process.send_signal(signal.SIGTERM)
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    process.kill()
                break
            time.sleep(0.1)
        returncode = process.wait()
    elapsed = time.monotonic() - started
    peak = max(peak, rss_kib(process.pid))
    evidence = {
        "schema": "KRENN_AFF251_D12_RARE_ORDER_INDEX_WATCHDOG_V1",
        "status": "FAIL" if reason or returncode else "PASS",
        "reason": reason,
        "returncode": returncode,
        "elapsed_seconds": elapsed,
        "peak_rss_kib": peak,
        "wall_limit_seconds": WALL_SECONDS,
        "rss_limit_kib": RSS_LIMIT_KIB,
        "command": command,
        "input_sha256": {str(path.relative_to(ROOT)): value for path, value in EXPECTED.items()},
    }
    if not reason and returncode == 0:
        validate(json.loads(RESULT.read_text()), peak, elapsed)
    atomic_json(WATCHDOG, evidence)
    if evidence["status"] != "PASS":
        raise RuntimeError(evidence)
    print(json.dumps(evidence, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
