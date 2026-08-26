#!/usr/bin/env python3
"""Independent fail-closed audit and hostile tests for the compact microgate."""

import copy
import hashlib
import json
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PROVIDER = REPO / "computations/unaudited-codex-n8-x5-four-blocker-d6-cegar-gate-2026-08-25/provider_triangle_endpoint_colour.ms"
CHECKPOINT = REPO / "computations/unaudited-codex-n8-x5-d11-triangle-resume16-design-2026-08-25/sealed_resume_input"
PINS = {
    "source": "c4052dfa3e2a5ec538af30f357f1211d4720d4fee376fd9fdd071d59a8131113",
    "binary": "9575a99a5d39a0ee93979fee4867e56441ed8c812b913f85deb095746afcd19e",
    "watchdog": "6c77af08481c20b045b0a8e7bfe8c8710d15b129862f0e6f8766c72636c02443",
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


def validate_result(value: dict, mode: str, count: int) -> None:
    assert set(value) == {
        "schema", "status", "mode", "count", "terms", "pairing_failures",
        "selected_prefix_sha256", "dual_support_sha256", "materialized_semantic_sha256",
        "dual_support", "provider_sha256", "selected_input_sha256", "dual_input_sha256",
        "parse_seconds", "representation_seconds", "retained_accounted_bytes", "total_seconds",
    }
    assert value["schema"] == "KRENN_X5_D11_COMPACT_REPRESENTATION_MICROGATE_RESULT_V1"
    assert value["status"] == "PASS_EXACT_REPRESENTATION"
    assert value["mode"] == mode and value["count"] == count
    assert value["pairing_failures"] == 0 and value["dual_support"] == 13_116
    assert value["provider_sha256"] == PINS["provider"]
    assert value["selected_input_sha256"] == PINS["selected"]
    assert value["dual_input_sha256"] == PINS["dual"]
    for key in ("selected_prefix_sha256", "dual_support_sha256", "materialized_semantic_sha256"):
        assert len(value[key]) == 64 and all(character in "0123456789abcdef" for character in value[key])
    assert value["terms"] > 0 and value["representation_seconds"] > 0
    assert value["retained_accounted_bytes"] > 0 and value["total_seconds"] < 120


def validate_pair(baseline: dict, compact: dict, count: int) -> None:
    validate_result(baseline, "baseline", count)
    validate_result(compact, "compact", count)
    for field in ("count", "terms", "pairing_failures", "selected_prefix_sha256",
                  "dual_support_sha256", "materialized_semantic_sha256", "dual_support"):
        assert baseline[field] == compact[field]


def main() -> None:
    assert sha(HERE / "src/main.rs") == PINS["source"]
    assert sha(HERE / "d11_compact_microgate") == PINS["binary"]
    assert sha(HERE / "watchdog4_120.py") == PINS["watchdog"]
    assert sha(PROVIDER) == PINS["provider"]
    assert sha(CHECKPOINT / "selected.tsv") == PINS["selected"]
    assert sha(CHECKPOINT / "dual.tsv") == PINS["dual"]

    accepted = {}
    watches = {}
    for count in (1000, 5000):
        for mode in ("baseline", "compact"):
            lane = HERE / "runs" / f"{mode}_{count}"
            value = json.loads((lane / "result.json").read_text())
            watch = json.loads((lane / "watchdog.json").read_text())
            validate_result(value, mode, count)
            assert watch["status"] == "PASS" and watch["breach"] is None and watch["returncode"] == 0
            assert watch["rss_cap_kib"] == 4 * 1024 * 1024 and watch["wall_cap_seconds"] == 120
            assert 0 < watch["peak_rss_kib"] < watch["rss_cap_kib"]
            assert 0 < watch["elapsed_seconds"] < watch["wall_cap_seconds"]
            assert len(watch["samples"]) > 0
            command = watch["command"]
            assert command[0] == str(HERE / "d11_compact_microgate")
            assert command[command.index("--mode") + 1] == mode
            assert command[command.index("--count") + 1] == str(count)
            assert command[command.index("--provider") + 1] == str(PROVIDER)
            assert command[command.index("--selected") + 1] == str(CHECKPOINT / "selected.tsv")
            assert command[command.index("--dual") + 1] == str(CHECKPOINT / "dual.tsv")
            assert all("affine251" not in argument and "d12" not in argument.lower() for argument in command)
            accepted[(count, mode)] = value
            watches[(count, mode)] = watch
        validate_pair(accepted[(count, "baseline")], accepted[(count, "compact")], count)

    summary = json.loads((HERE / "results_audit.json").read_text())
    assert summary["status"] == "PASS_EXACT_REJECT_NONPERFORMANT" and not summary["promoted"]
    assert not summary["resume16_launched"] and not summary["d12_cache_reads"]
    for comparison in summary["comparisons"]:
        count = comparison["count"]
        baseline, compact = accepted[(count, "baseline")], accepted[(count, "compact")]
        base_watch, compact_watch = watches[(count, "baseline")], watches[(count, "compact")]
        assert comparison["exact_sha_equal"] and not comparison["two_x_measured_threshold"]
        assert comparison["baseline_peak_rss_kib"] == base_watch["peak_rss_kib"]
        assert comparison["compact_peak_rss_kib"] == compact_watch["peak_rss_kib"]
        assert comparison["measured_peak_rss_ratio_baseline_over_compact"] == base_watch["peak_rss_kib"] / compact_watch["peak_rss_kib"]
        assert comparison["materialization_throughput_ratio_baseline_over_compact"] == baseline["representation_seconds"] / compact["representation_seconds"]
        assert comparison["accounted_retained_ratio_baseline_over_compact"] == baseline["retained_accounted_bytes"] / compact["retained_accounted_bytes"]

    hostile_tests = {}
    base = accepted[(5000, "baseline")]
    compact = accepted[(5000, "compact")]
    mutations = {
        "wrong_semantic_sha": ("materialized_semantic_sha256", "0" * 64),
        "wrong_selected_sha": ("selected_prefix_sha256", "f" * 64),
        "positive_pairing_failure": ("pairing_failures", 1),
        "wrong_count": ("count", 4999),
        "extra_property": ("hostile_extra", True),
    }
    for name, (key, value) in mutations.items():
        hostile = copy.deepcopy(compact)
        hostile[key] = value
        rejected = False
        try:
            validate_pair(base, hostile, 5000)
        except AssertionError:
            rejected = True
        assert rejected
        hostile_tests[name] = "REJECTED"

    rejected_ps = list((HERE / "runs_rejected_ps_sampler").glob("*/watchdog.json"))
    assert len(rejected_ps) == 4
    for path in rejected_ps:
        value = json.loads(path.read_text())
        assert value["peak_rss_kib"] == 0 and value["samples"] == []
    superseded = json.loads((HERE / "results_audit_superseded_fairness_v1.json").read_text())
    assert superseded["status"] == "PASS_EXACT_REJECT_NONPERFORMANT"

    result = {
        "schema": "KRENN_X5_D11_COMPACT_REPRESENTATION_MICROGATE_INDEPENDENT_AUDIT_V1",
        "status": "PASS_EXACT_REJECT_NONPERFORMANT",
        "accepted_lanes": 4,
        "exact_pairing_failures": 0,
        "hostile_tests": hostile_tests,
        "rejected_ps_sampler_lanes_zero_coverage": 4,
        "superseded_unfair_timing_lanes_zero_coverage": 4,
        "promotion_verdict": "REJECT",
        "reason": "compact mode is slower and has higher measured peak RSS at both 1k and 5k",
        "pins": PINS,
        "resume16_launched": False,
        "d12_cache_reads": False,
    }
    atomic_json(HERE / "results_independent_audit.json", result)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
