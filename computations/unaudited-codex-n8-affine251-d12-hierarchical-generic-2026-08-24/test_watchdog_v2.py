#!/usr/bin/env python3
"""Synthetic fast-exit, poll/exit-race, and RSS-overrun tests."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parent
WRAPPER = ROOT / "run_with_macos_rss_watchdog_v2.py"
FIXTURE = ROOT / "watchdog_fixture.py"
WRAPPER_SHA = "53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97"
FIXTURE_SHA = "575dc2a0bb6c17d8a981601c2b2d3eb371a7b157be214e207088fecb4ebf80df"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_case(root: Path, name: str, mode: str, test_limit=None):
    root.mkdir()
    command = [
        "python3", str(WRAPPER), "--rss-gib", "36", "--wall-seconds", "5",
        "--poll-seconds", "0.01", "--source", str(FIXTURE),
        "--expected-source-sha256", FIXTURE_SHA,
        "--expected-binary-sha256", FIXTURE_SHA,
        "--telemetry", str(root / "telemetry.json"),
        "--stdout", str(root / "stdout.log"),
        "--stderr", str(root / "stderr.log"),
    ]
    environment = os.environ.copy()
    if test_limit is not None:
        command += ["--test-rss-limit-kib", str(test_limit)]
        environment["KRENN_WATCHDOG_SELFTEST"] = "1"
    command += [
        "--", str(FIXTURE), "--fixture", mode,
        "--output", str(root / "result.json"),
        "--checkpoint", str(root / "checkpoint.bin"),
        "--vector-cache", str(root / "vectors.bin"),
        "--rss-gib", "36", "--wall-seconds", "4",
    ]
    run = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         env=environment, text=True, check=False)
    telemetry = json.loads((root / "telemetry.json").read_text())
    return run, telemetry


def main() -> None:
    if sha256(WRAPPER) != WRAPPER_SHA or sha256(FIXTURE) != FIXTURE_SHA:
        raise AssertionError("watchdog/fixture pin")
    records = []
    with tempfile.TemporaryDirectory(prefix="d12-watchdog-v2-") as temporary:
        root = Path(temporary)
        run, telemetry = run_case(root / "fast", "fast", "fast")
        if run.returncode != 0 or telemetry["status"] != "PASS":
            raise AssertionError(f"fast exit: {run.stderr}")
        records.append({"case": "fast_exit", "status": "PASS",
                        "sample_count": telemetry["sample_count"]})

        race_samples = []
        for index in range(32):
            run, telemetry = run_case(root / f"race{index:02d}", f"race{index:02d}", "race")
            if run.returncode != 0 or telemetry["status"] != "PASS":
                raise AssertionError(f"race {index}: return={run.returncode} stderr={run.stderr} telemetry={telemetry}")
            race_samples.append(telemetry["sample_count"])
        records.append({"case": "poll_exit_race_x32", "status": "PASS",
                        "sample_counts": race_samples})

        run, telemetry = run_case(root / "overrun", "overrun", "overrun", 32_768)
        if (run.returncode == 0 or telemetry["status"] != "FAIL"
                or telemetry["breach"] != "RSS_CAP"
                or not telemetry["abort_final_output_absent"]
                or telemetry["last_successful_rss_sample"] is None
                or telemetry["peak_rss_kib"] < telemetry["rss_limit_kib"]):
            raise AssertionError(f"RSS overrun did not fail closed: {telemetry}")
        records.append({"case": "rss_overrun", "status": "PASS",
                        "peak_rss_kib": telemetry["peak_rss_kib"],
                        "rss_limit_kib": telemetry["rss_limit_kib"],
                        "final_output_absent": telemetry["abort_final_output_absent"]})
    result = {
        "schema": "KRENN_AFFINE251_D12_MACOS_WATCHDOG_V2_HOSTILES_V1",
        "status": "PASS",
        "wrapper_sha256": WRAPPER_SHA,
        "fixture_sha256": FIXTURE_SHA,
        "records": records,
    }
    path = ROOT / "results_watchdog_v2_hostiles.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


if __name__ == "__main__":
    main()
