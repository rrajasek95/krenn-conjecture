#!/usr/bin/env python3
"""Seal the single authorized retry as zero-coverage process failure."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    assert sha256(HERE / "MANIFEST.sha256") == "4651d21012e34a6237edc3d8fcf391185b6d7422d345a079e2b873952b5c57e4"
    assert sha256(HERE / "results_p32003_p00.json") == "1572f7573f8fab7a907ad2aefd52e0c1c6596461878a4c0bfc9f9dc4ad7c2c94"
    assert not list(HERE.glob("results_retry_*.json"))
    assert not list(HERE.glob("results_Q_*.json"))
    result = {
        "schema": "KRENN_X5_REP5_RETRY_WATCHDOG_FAILURE_V1",
        "status": "FAIL_CLOSED_PROCESS_ZERO_COVERAGE",
        "mathematical_coverage": False,
        "attempt": "single authorized resource-only p00 modular retry",
        "intended_geometry": {"native_wall_seconds": 180, "wrapper_wall_seconds": 190, "rss_cap_gib": 8},
        "failure": "sandbox denied the runner's child process-group ps RSS probe immediately after launch; parent could not capture stdout or emit an atomic result",
        "external_wrapper": "exited; subsequent process census clear",
        "captured_result": None,
        "Q_runs": 0,
        "later_chart_runs": 0,
        "automatic_retry_allowed": False,
        "pins": {"prior_manifest_sha256": "4651d21012e34a6237edc3d8fcf391185b6d7422d345a079e2b873952b5c57e4", "prior_60s_failure_sha256": "1572f7573f8fab7a907ad2aefd52e0c1c6596461878a4c0bfc9f9dc4ad7c2c94", "retry_runner_sha256": sha256(HERE / "run_retry180_300.py")},
    }
    temporary = HERE / "results_retry_watchdog_failure.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_retry_watchdog_failure.json")
    print(json.dumps({"status": result["status"], "coverage": False, "Q_runs": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
