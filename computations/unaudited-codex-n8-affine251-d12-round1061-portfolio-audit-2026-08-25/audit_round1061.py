#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
V4 = REPO / "computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25"
ROUND1060 = REPO / "computations/unaudited-codex-n8-affine251-d12-v4-1-round1060-audit-2026-08-25"
WATCHDOG = REPO / "computations/unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/run_with_macos_rss_watchdog_v2.py"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def checkpoint_header(path):
    data = path.read_bytes()[:44]
    assert data[:12] == b"AFF12CEG1\0\0\0"
    prime, rounds, columns, support = struct.unpack_from("<QQQQ", data, 12)
    assert path.stat().st_size == 44 + 15 * columns + 21 * support
    return {"prime": prime, "round": rounds, "columns": columns, "support": support}


def vectors_header(path):
    with path.open("rb") as stream:
        data = stream.read(44)
    assert data[:12] == b"AFF12VEC1\0\0\0"
    prime, provider, fingerprint, columns = struct.unpack_from("<QQQQ", data, 12)
    return {"prime": prime, "provider": provider, "fingerprint": fingerprint,
            "columns": columns, "bytes": path.stat().st_size}


def argument(command, flag):
    assert command.count(flag) == 1
    return command[command.index(flag) + 1]


pins = json.loads((ROOT / "INPUT_PINS.json").read_text())
assert pins["status"] == "PASS_APFS_CLONED_FROZEN_ROUND1060_INPUTS"
assert pins["source_checkpoint_sha256"] == "1bc0315df0c97878b3d61f0dd945ff0ba28f922d9e62728f043210c9357c7a2d"
assert pins["source_vectors_sha256"] == "0d71ab7b833623d6ea2fb99a822859bef14f9ba30f54e32bf744d383f65995a3"
assert pins["round1060_audit_manifest_sha256"] == sha256(ROUND1060 / "FINAL_MANIFEST.sha256")

parent_source = V4 / "sealed_v4_1/main.rs"
audit_source = ROOT / "audit_source/src/main.rs"
audit_binary = ROOT / "audit_source/sparse_d12_dual"
assert sha256(parent_source) == "3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59"
assert sha256(audit_source) == "2cf629054e1b5e2350617b71114544b7d0c7a47f811b67b6dea4483e5e911230"
assert sha256(audit_binary) == "ade47c27a96314bb4391241a60a372c79e643a44b8a62a00054fffc576ccc7ce"
assert sha256(WATCHDOG) == "53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97"
guard = '''    if config.elimination != "hierarchical"
        || config.strategy != "cold"
        || config.pivot != "rare"
        || config.workers != 16
        || config.incremental
    {
        fail("v4 rare-order index requires fixed cold/rare/16 hierarchical nonincremental mode");
    }
'''
parent_text = parent_source.read_text()
assert parent_text.count(guard) == 1
assert audit_source.read_text() == parent_text.replace(guard, "", 1)
hostile = json.loads((ROOT / "hostile_results.json").read_text())
assert hostile["status"] == "PASS" and hostile["hierarchical_non_cold_rejected"]

portfolio = json.loads((ROOT / "portfolio/result.json").read_text())
control = json.loads((ROOT / "selected_control/result.json").read_text())
portfolio_watch = json.loads((ROOT / "portfolio/watchdog.json").read_text())
control_watch = json.loads((ROOT / "selected_control/watchdog.json").read_text())
for result in (portfolio, control):
    assert result["status"] == "INCOMPLETE_SEARCH_CAP"
    assert result["incomplete_reason"] == "ROUND_CAP"
    assert result["rounds_completed"] == 1061
    assert result["column_orbits_exposed"] == 731908
    assert result["dual_support"] == 785
    assert result["cached_vectors_loaded"] == 729800
    assert result["vectors_materialized_on_restore"] == 0
    assert len(result["rounds"]) == 1
for watch in (portfolio_watch, control_watch):
    assert watch["status"] == "PASS" and watch["breach"] is None
    assert watch["returncode"] == 0 and watch["atomic_outputs_clean"]
    assert watch["peak_rss_kib"] < 36 * 1024 * 1024
    assert watch["elapsed_seconds"] < 120
    command = watch["command"]
    assert argument(command, "--round-cap") == "1061"
    assert argument(command, "--workers") == "16"
    assert argument(command, "--elimination") == "tree"
    assert argument(command, "--portfolio-period") == "1"
    assert argument(command, "--portfolio-parallel") == "yes"
assert argument(portfolio_watch["command"], "--pivot") == "auto"
assert argument(portfolio_watch["command"], "--strategy") == "best"
assert argument(control_watch["command"], "--pivot") == "rare"
assert argument(control_watch["command"], "--strategy") == "cold"

round_fields = ["round", "columns", "new_columns", "dual_support", "new_support_rows",
                "selected_strategy", "selected_pivot"]
portfolio_round = {key: portfolio["rounds"][0][key] for key in round_fields}
control_round = {key: control["rounds"][0][key] for key in round_fields}
assert portfolio_round == control_round == {
    "round": 1061, "columns": 731908, "new_columns": 2108,
    "dual_support": 785, "new_support_rows": 451,
    "selected_strategy": "cold", "selected_pivot": "rare",
}

checkpoint_hashes = {label: sha256(ROOT / label / "checkpoint.bin")
                     for label in ("portfolio", "selected_control")}
vector_hashes = {label: sha256(ROOT / label / "vectors.bin")
                 for label in ("portfolio", "selected_control")}
assert len(set(checkpoint_hashes.values())) == 1
assert len(set(vector_hashes.values())) == 1
assert next(iter(checkpoint_hashes.values())) == "9927bfa11b6505d106348ebdd76c7f95714947970535a2bccde3708ea90c57a4"
assert next(iter(vector_hashes.values())) == "acc0f960b0021b0adcd4dcc0efcf4141e1ae51bf54b30332316b33311eeacd1d"
state = checkpoint_header(ROOT / "selected_control/checkpoint.bin")
vectors = vectors_header(ROOT / "selected_control/vectors.bin")
assert state == {"prime": 1073741827, "round": 1061, "columns": 731908, "support": 785}
assert vectors["prime"] == 1073741827 and vectors["provider"] == 9218588987274412661
assert vectors["columns"] == 731908

attempt = ROOT / "portfolio_attempt1_rejected_guard"
attempt_watch = json.loads((attempt / "watchdog.json").read_text())
assert attempt_watch["status"] == "FAIL" and attempt_watch["returncode"] == 2
assert not (attempt / "result.json").exists()

artifacts = {}
for relative in [
    "portfolio/result.json", "portfolio/checkpoint.bin", "portfolio/vectors.bin",
    "portfolio/watchdog.json", "portfolio/stderr.log", "portfolio/stdout.log",
    "selected_control/result.json", "selected_control/checkpoint.bin",
    "selected_control/vectors.bin", "selected_control/watchdog.json",
    "selected_control/stderr.log", "selected_control/stdout.log",
    "INPUT_PINS.json", "hostile_results.json",
]:
    artifacts[relative] = sha256(ROOT / relative)

value = {
    "schema": "KRENN_AFF251_D12_ROUND1061_PORTFOLIO_AUDIT_V1",
    "status": "PASS_EXACT_ONE_ROUND1061_SIX_WAY_PORTFOLIO",
    "scope": "One exact round1060-to-1061 tree portfolio and fixed selected replay; no continuation.",
    "input": pins["input_state"],
    "input_hashes": {"checkpoint": pins["source_checkpoint_sha256"],
                     "vectors": pins["source_vectors_sha256"],
                     "round1060_audit_manifest": pins["round1060_audit_manifest_sha256"]},
    "audit_sibling": {
        "parent_source_sha256": sha256(parent_source),
        "source_sha256": sha256(audit_source),
        "binary_sha256": sha256(audit_binary),
        "only_diff_top_level_v4_fixed_mode_guard_removed": True,
        "parser_hierarchical_fixed_guard_retained": True,
        "hostile_hierarchical_non_cold_rejected": True,
    },
    "portfolio": {
        "task_count": 6, "strategies": ["repair", "cold"],
        "pivots": ["first", "last", "rare"], "parallel": True,
        "selected_strategy": "cold", "selected_pivot": "rare",
        "native_solve_seconds": portfolio["rounds"][0]["solve_seconds"],
        "watchdog_elapsed_seconds": portfolio_watch["elapsed_seconds"],
        "peak_rss_kib": portfolio_watch["peak_rss_kib"],
    },
    "selected_control": {
        "strategy": "cold", "pivot": "rare",
        "native_solve_seconds": control["rounds"][0]["solve_seconds"],
        "watchdog_elapsed_seconds": control_watch["elapsed_seconds"],
        "peak_rss_kib": control_watch["peak_rss_kib"],
    },
    "output": {**state, "new_columns": 2108, "new_support_rows": 451},
    "semantic_round_record_identical_excluding_timings": True,
    "checkpoint_byte_identical": True,
    "vector_cache_byte_identical": True,
    "output_checkpoint_sha256": checkpoint_hashes["selected_control"],
    "output_vectors_sha256": vector_hashes["selected_control"],
    "output_vector_header": vectors,
    "rejected_original_v4_1_guard_attempt_preserved": True,
    "production_mutated": False,
    "continued_beyond_round1061": False,
    "artifact_sha256": artifacts,
}
temporary = ROOT / "results_round1061_audit.json.tmp"
temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
os.replace(temporary, ROOT / "results_round1061_audit.json")
print(json.dumps(value, sort_keys=True))
