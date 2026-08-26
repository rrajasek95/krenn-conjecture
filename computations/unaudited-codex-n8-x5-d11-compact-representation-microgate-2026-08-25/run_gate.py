#!/usr/bin/env python3
"""Run and fail-closed validate the 1k/5k baseline/compact D11 microgate."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PROVIDER = REPO / "computations/unaudited-codex-n8-x5-four-blocker-d6-cegar-gate-2026-08-25/provider_triangle_endpoint_colour.ms"
CHECKPOINT = REPO / "computations/unaudited-codex-n8-x5-d11-triangle-resume16-design-2026-08-25/sealed_resume_input"
BINARY = HERE / "d11_compact_microgate"
SOURCE = HERE / "src/main.rs"
WATCHDOG = HERE / "watchdog4_120.py"
PINS = {
    "provider": "06df5052a50099dc400d622323257fef9b3077a791f918c8f1c46d7bf7a5782c",
    "selected": "1f70a3220d6091e0877fd00d86c6ff9f06f25789e03cc854556e6d7ae34fb2a7",
    "dual": "a91f2be59901b4f29c09f64845e700fb40d7f15181bcd7ac8df89022d4e39d93",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def main() -> None:
    if not __debug__:
        raise RuntimeError("assertions required")
    assert sha(PROVIDER) == PINS["provider"]
    assert sha(CHECKPOINT / "selected.tsv") == PINS["selected"]
    assert sha(CHECKPOINT / "dual.tsv") == PINS["dual"]
    selftest = json.loads(subprocess.run([str(BINARY), "--selftest"], cwd=REPO,
                                         check=True, text=True, capture_output=True).stdout)
    assert selftest["status"] == "PASS"
    output_root = HERE / "runs"
    assert not output_root.exists()
    results = {}
    telemetry = {}
    for count in (1000, 5000):
        for mode in ("baseline", "compact"):
            lane = output_root / f"{mode}_{count}"
            result = lane / "result.json"
            command = [str(BINARY), "--mode", mode, "--count", str(count),
                       "--provider", str(PROVIDER), "--selected", str(CHECKPOINT / "selected.tsv"),
                       "--dual", str(CHECKPOINT / "dual.tsv"), "--output", str(result)]
            wrapper = [sys.executable, str(WATCHDOG), "--telemetry", str(lane / "watchdog.json"),
                       "--stdout", str(lane / "stdout.log"), "--stderr", str(lane / "stderr.log"),
                       "--", *command]
            subprocess.run(wrapper, cwd=REPO, check=True)
            measured = json.loads((lane / "watchdog.json").read_text())
            value = json.loads(result.read_text())
            assert measured["status"] == "PASS" and measured["peak_rss_kib"] < 4 * 1024 * 1024
            assert measured["elapsed_seconds"] < 120
            assert value["status"] == "PASS_EXACT_REPRESENTATION" and value["mode"] == mode
            assert value["count"] == count and value["pairing_failures"] == 0
            assert value["dual_support"] == 13116
            assert value["provider_sha256"] == PINS["provider"]
            assert value["selected_input_sha256"] == PINS["selected"]
            assert value["dual_input_sha256"] == PINS["dual"]
            results[(count, mode)] = value
            telemetry[(count, mode)] = measured
        baseline, compact = results[(count, "baseline")], results[(count, "compact")]
        for field in ("count", "terms", "pairing_failures", "selected_prefix_sha256",
                      "dual_support_sha256", "materialized_semantic_sha256", "dual_support"):
            assert baseline[field] == compact[field], (count, field)

    comparisons = []
    promoted = True
    for count in (1000, 5000):
        baseline, compact = results[(count, "baseline")], results[(count, "compact")]
        base_watch, compact_watch = telemetry[(count, "baseline")], telemetry[(count, "compact")]
        rss_ratio = base_watch["peak_rss_kib"] / compact_watch["peak_rss_kib"]
        throughput_ratio = baseline["representation_seconds"] / compact["representation_seconds"]
        retained_ratio = baseline["retained_accounted_bytes"] / compact["retained_accounted_bytes"]
        threshold = rss_ratio >= 2 or throughput_ratio >= 2
        promoted &= threshold
        comparisons.append({
            "count": count,
            "terms": baseline["terms"],
            "exact_sha_equal": True,
            "baseline_peak_rss_kib": base_watch["peak_rss_kib"],
            "compact_peak_rss_kib": compact_watch["peak_rss_kib"],
            "measured_peak_rss_ratio_baseline_over_compact": rss_ratio,
            "baseline_representation_seconds": baseline["representation_seconds"],
            "compact_representation_seconds": compact["representation_seconds"],
            "materialization_throughput_ratio_baseline_over_compact": throughput_ratio,
            "accounted_retained_ratio_baseline_over_compact": retained_ratio,
            "two_x_measured_threshold": threshold,
        })
    summary = {
        "schema": "KRENN_X5_D11_COMPACT_REPRESENTATION_MICROGATE_AUDIT_V1",
        "status": "PASS_PROMOTE" if promoted else "PASS_EXACT_REJECT_NONPERFORMANT",
        "mathematical_scope": "representation only; no solve, continuation, global incident scan, or D12 read",
        "exactness": {
            "selected_prefix_sha_equal": True,
            "dual_support_sha_equal": True,
            "materialized_semantic_sha_equal": True,
            "pairing_failures": 0,
        },
        "promotion_rule": "both 1k and 5k require >=2x measured peak-RSS reduction or >=2x materialization throughput",
        "promoted": promoted,
        "comparisons": comparisons,
        "input_pins": PINS,
        "source_sha256": sha(SOURCE),
        "binary_sha256": sha(BINARY),
        "watchdog_sha256": sha(WATCHDOG),
        "selftest": selftest,
        "resume16_launched": False,
        "d12_cache_reads": False,
    }
    atomic_json(HERE / "results_audit.json", summary)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
