#!/usr/bin/env python3
"""Staged sequential D9 branch/prime runs under the frozen watchdog."""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

if not __debug__:
    raise RuntimeError("fail closed: runner requires assertions enabled")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SCHEDULE = json.loads((HERE / "SCHEDULE.json").read_text())

parser = argparse.ArgumentParser()
parser.add_argument("--phase", choices=("coloured", "direct"), required=True)
args = parser.parse_args()
phase_branches = SCHEDULE["branches"][:3] if args.phase == "coloured" else SCHEDULE["branches"][3:]


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


engine = SCHEDULE["engine"]
source = HERE / engine["source"]
binary = HERE / engine["binary"]
watchdog = REPO / SCHEDULE["watchdog"]["path"]
assert sha256(source) == engine["source_sha256"]
assert sha256(binary) == engine["binary_sha256"]
assert sha256(watchdog) == SCHEDULE["watchdog"]["sha256"]

records = []
for prime in SCHEDULE["primes"]:
    root = SCHEDULE["provider_roots"][str(prime)]
    package = REPO / root["package"]
    assert sha256(package / "MANIFEST.sha256") == root["manifest_sha256"]
    for branch in phase_branches:
        provider_spec = root["providers"][branch]
        provider_source = package / provider_spec[0]
        assert sha256(provider_source) == provider_spec[1]
        temporary_provider = None
        if root["compressed"]:
            with tempfile.NamedTemporaryFile(prefix=f"x5_d9_{prime}_{branch}_", suffix=".ms", delete=False) as output:
                temporary_provider = Path(output.name)
                digest = hashlib.sha256()
                with gzip.open(provider_source, "rb") as stream:
                    for block in iter(lambda: stream.read(8 << 20), b""):
                        digest.update(block)
                        output.write(block)
            assert digest.hexdigest() == provider_spec[2]
            provider = temporary_provider
        else:
            provider = provider_source

        directory = HERE / f"p{prime}_{branch}"
        assert not directory.exists(), f"refuse pre-existing {directory}"
        directory.mkdir()
        command = [
            str(binary), "--branch", branch, "--input", str(provider),
            "--output", str(directory / "result.json"),
            "--selected", str(directory / "selected.tsv"),
            "--dual", str(directory / "dual.tsv"),
            "--prime", str(prime), "--column-cap", str(engine["column_cap"]),
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
            if temporary_provider is not None:
                temporary_provider.unlink(missing_ok=True)
        result_path = directory / "result.json"
        result = json.loads(result_path.read_text()) if result_path.exists() else {}
        record = {
            "prime": prime,
            "branch": branch,
            "returncode": completed.returncode,
            "status": result.get("status"),
            "selected_columns": result.get("selected_columns"),
            "dual_support": result.get("dual_support"),
            "elapsed_seconds": result.get("elapsed_seconds"),
        }
        record["accepted_terminal_status"] = record["status"] in {
            "COMPLETE_MODULAR_DUAL_DIAGNOSTIC",
            "MODULAR_MEMBER_REQUIRES_EXACT_RATIONAL_REPLAY",
        }
        records.append(record)
        if completed.returncode != 0 or not record["accepted_terminal_status"]:
            break
    if records[-1]["returncode"] != 0 or not records[-1]["accepted_terminal_status"]:
        break

summary = {
    "schema": "KRENN_X5_D9_STAGED_TWO_PRIME_RUNNER_SUMMARY_V1",
    "status": "TERMINAL" if len(records) == 2 * len(phase_branches) and all(record["returncode"] == 0 and record["accepted_terminal_status"] for record in records) else "FAIL_CLOSED",
    "phase": args.phase,
    "records": records,
    "degree_ten_launched": False,
    "d12_cache_access": False,
}
summary_path = HERE / f"runner_{args.phase}_summary.json"
temporary = summary_path.with_suffix(".json.tmp")
temporary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
os.replace(temporary, summary_path)
print(json.dumps(summary, sort_keys=True))
