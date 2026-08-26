#!/usr/bin/env python3
"""Run the four literal branches at the frozen independent prime."""
import hashlib
import gzip
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SCHEDULE = json.loads((HERE / "SCHEDULE.json").read_text())


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


engine = SCHEDULE["second_prime_engine"]
source = HERE / engine["source"]
binary = HERE / engine["binary"]
watchdog = REPO / SCHEDULE["watchdog"]["path"]
assert sha256(source) == engine["source_sha256"]
assert sha256(binary) == engine["binary_sha256"]
assert sha256(watchdog) == SCHEDULE["watchdog"]["sha256"]

records = []
for branch in SCHEDULE["branches"]:
    spec = SCHEDULE["providers"][branch]
    provider_archive = HERE / spec["path"]
    assert sha256(provider_archive) == spec["sha256"]
    directory = HERE / f"second_prime_{branch}"
    assert not directory.exists()
    directory.mkdir()
    with tempfile.NamedTemporaryFile(prefix=f"x5_{branch}_", suffix=".ms", delete=False) as temporary_provider:
        temporary_provider_path = Path(temporary_provider.name)
        digest = hashlib.sha256()
        with gzip.open(provider_archive, "rb") as source_stream:
            for block in iter(lambda: source_stream.read(8 << 20), b""):
                digest.update(block)
                temporary_provider.write(block)
    assert digest.hexdigest() == spec["uncompressed_sha256"]
    command = [
        str(binary), "--branch", branch, "--input", str(temporary_provider_path),
        "--output", str(directory / "result.json"),
        "--selected", str(directory / "selected.tsv"),
        "--dual", str(directory / "dual.tsv"),
        "--prime", str(SCHEDULE["primes"]["second"]),
        "--column-cap", str(engine["column_cap"]),
        "--wall-seconds", str(engine["native_wall_seconds"]),
    ]
    wrapper = [
        sys.executable, str(watchdog), "--rss-gib", str(engine["rss_gib"]),
        "--wall-seconds", str(engine["wrapper_wall_seconds"]),
        "--poll-seconds", "0.25", "--source", str(source),
        "--expected-source-sha256", engine["source_sha256"],
        "--expected-binary-sha256", engine["binary_sha256"],
        "--telemetry", str(directory / "watchdog.json"),
        "--stdout", str(directory / "stdout.log"),
        "--stderr", str(directory / "stderr.log"), "--", *command,
    ]
    try:
        completed = subprocess.run(wrapper, cwd=REPO, check=False)
    finally:
        temporary_provider_path.unlink(missing_ok=True)
    result_path = directory / "result.json"
    result = json.loads(result_path.read_text()) if result_path.exists() else {}
    records.append({
        "branch": branch,
        "returncode": completed.returncode,
        "status": result.get("status"),
        "selected_columns": result.get("selected_columns"),
        "dual_support": result.get("dual_support"),
        "elapsed_seconds": result.get("elapsed_seconds"),
    })

summary = {
    "schema": "KRENN_X5_D6_SECOND_PRIME_RUNNER_SUMMARY_V1",
    "status": "TERMINAL" if all(record["returncode"] == 0 for record in records) else "FAIL_CLOSED",
    "prime": SCHEDULE["primes"]["second"],
    "records": records,
    "degree_above_six": False,
    "d12_cache_access": False,
}
temporary = HERE / "second_prime_runner_summary.json.tmp"
temporary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "second_prime_runner_summary.json")
print(json.dumps(summary, sort_keys=True))
