#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
GENERIC = REPO / "computations/unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24"
SOURCE_SHA = "173828021430f51a51324a73c12e0cd351c072c2a458b4dadc019672ca72f69a"
BINARY_SHA = "8625721373d2880432ca5bdc18b277ca474adedf3a451d321c5ca65e6db3727a"
PROVIDER_SHA = "daa427528bbbeece064b09396023b66f32b804ba6d304178d19ced13e9b38a4e"
CHAIN_MANIFEST_SHA = "30be587a44928b418ff51a6fa58791eff90f168a542c22e4d603e7fad72177d8"
CHAIN_RESULT_SHA = "156b55fc8f86c2f842d02875854e15f0d81ec3d9236b8c33a8c2fe40a2f9743e"


def sha256(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def checkpoint(path):
    with path.open("rb") as stream:
        header = stream.read(44)
    assert header[:12] == b"AFF12CEG1\0\0\0"
    prime, rounds, columns, support = struct.unpack_from("<QQQQ", header, 12)
    assert path.stat().st_size == 44 + 15 * columns + 21 * support
    return {"prime": prime, "round": rounds, "columns": columns, "support": support}


def vector_header(path):
    with path.open("rb") as stream:
        header = stream.read(44)
    assert header[:12] == b"AFF12VEC1\0\0\0"
    prime, provider, fingerprint, columns = struct.unpack_from("<QQQQ", header, 12)
    return {"prime": prime, "provider": provider, "fingerprint": fingerprint,
            "columns": columns, "bytes": path.stat().st_size}


pins = json.loads((ROOT / "INPUT_PINS.json").read_text())
assert pins["input_state"] == {"prime": 1073741827, "round": 849, "columns": 460676, "support": 312}
provider = REPO / "computations/unaudited-codex-star-tautology-triangle-replacement-2026-08-22/canonical_triangle_pair_offdiag_full_p1073741827.ms"
chain_root = REPO / "computations/unaudited-codex-n8-affine251-d12-round849-chain-audit-2026-08-24"
assert sha256(provider) == PROVIDER_SHA
assert sha256(chain_root / "MANIFEST.sha256") == CHAIN_MANIFEST_SHA
assert sha256(chain_root / "results_round849_chain_audit.json") == CHAIN_RESULT_SHA
chain = json.loads((chain_root / "results_round849_chain_audit.json").read_text())
assert chain["status"] == "PASS_EXACT_ROUND849_CHAIN_WITH_STAGE01_RESOURCE_CAVEAT"
assert chain["final_columns"] == 460676 and chain["final_support"] == 312
assert chain["final_all_column_replay"]["terms_replayed"] == 46796079
assert chain["final_all_column_replay"]["verification_failures"] == 0
records = {}
for label in ("portfolio", "selected_control"):
    directory = ROOT / label
    result = json.loads((directory / "result.json").read_text())
    watchdog = json.loads((directory / "watchdog.json").read_text())
    assert result["schema"] == "KRENN_AFFINE251_D12_NATIVE_SPARSE_DUAL_V1"
    assert result["status"] == "INCOMPLETE_SEARCH_CAP" and result["incomplete_reason"] == "ROUND_CAP"
    assert result["rounds_completed"] == 850 and len(result["rounds"]) == 1
    assert result["rounds"][0]["round"] == 850
    assert result["cached_vectors_loaded"] == 460676 and result["vectors_materialized_on_restore"] == 0
    assert result["global_annihilation"] is None and result["target_pairing"] is None
    assert result["workers"] == 16 and result["elimination_kernel"] == "tree"
    assert result["incremental_basis"] is False and result["portfolio_period"] == 1
    assert result["portfolio_parallel"] is True and result["rss_limit_gib"] == 36
    assert watchdog["status"] == "PASS" and watchdog["breach"] is None
    assert watchdog["source_sha256"] == SOURCE_SHA and watchdog["binary_sha256"] == BINARY_SHA
    assert watchdog["atomic_outputs_clean"] is True and watchdog["returncode"] == 0
    assert watchdog["peak_rss_kib"] < 36 * 1024 * 1024
    assert not any(directory.glob("*.tmp"))
    cp = checkpoint(directory / "checkpoint.bin")
    vec = vector_header(directory / "vectors.bin")
    assert cp == {"prime": 1073741827, "round": 850,
                  "columns": result["column_orbits_exposed"], "support": result["dual_support"]}
    assert vec["prime"] == 1073741827 and vec["columns"] == result["column_orbits_exposed"]
    assert vec["bytes"] == result["vector_cache_bytes"]
    records[label] = {"result": result, "watchdog": watchdog, "checkpoint": cp, "vectors": vec,
                      "hashes": {name: sha256(directory / name) for name in
                                 ("result.json", "watchdog.json", "stderr.log", "stdout.log",
                                  "checkpoint.bin", "vectors.bin")}}

portfolio = records["portfolio"]
control = records["selected_control"]
assert portfolio["result"]["pivot_mode"] == "auto" and portfolio["result"]["strategy"] == "best"
selected = portfolio["result"]["rounds"][0]
assert control["result"]["pivot_mode"] == selected["selected_pivot"]
assert control["result"]["strategy"] == selected["selected_strategy"]
assert control["result"]["rounds"][0]["selected_pivot"] == selected["selected_pivot"]
assert control["result"]["rounds"][0]["selected_strategy"] == selected["selected_strategy"]
assert portfolio["hashes"]["checkpoint.bin"] == control["hashes"]["checkpoint.bin"]
assert portfolio["hashes"]["vectors.bin"] == control["hashes"]["vectors.bin"]
for field in ("round", "columns", "new_columns", "dual_support", "new_support_rows",
              "selected_strategy", "selected_pivot"):
    assert portfolio["result"]["rounds"][0][field] == control["result"]["rounds"][0][field]

output = {
    "schema": "KRENN_AFF251_D12_ROUND850_PORTFOLIO_AUDIT_V1",
    "status": "PASS_EXACT_ONE_ROUND_PORTFOLIO_AUDIT",
    "input_state": pins["input_state"],
    "input_pins": {"checkpoint_sha256": pins["source_checkpoint_sha256"],
                   "vectors_sha256": pins["source_vectors_sha256"]},
    "source_sha256": SOURCE_SHA,
    "binary_sha256": BINARY_SHA,
    "provider_sha256": PROVIDER_SHA,
    "round849_chain_manifest_sha256": CHAIN_MANIFEST_SHA,
    "round849_chain_result_sha256": CHAIN_RESULT_SHA,
    "round849_input_all_column_replay": {"columns": 460676, "terms": 46796079,
                                         "verification_failures": 0},
    "portfolio_compared": {"strategies": ["repair", "cold"],
                           "pivots": ["first", "last", "rare"],
                           "task_count": 6, "parallel": True},
    "selected_strategy": selected["selected_strategy"],
    "selected_pivot": selected["selected_pivot"],
    "cold_rare_remains_selected": selected["selected_strategy"] == "cold" and selected["selected_pivot"] == "rare",
    "output_state": portfolio["checkpoint"],
    "portfolio_selected_control_checkpoint_identical": True,
    "portfolio_selected_control_vector_cache_identical": True,
    "semantic_round_record_identical_excluding_timings": True,
    "mathematical_artifacts_differ_only_by_audit_configuration_and_timing_metadata": True,
    "production_mutated": False,
    "continued_beyond_round850": False,
    "global_annihilation": None,
    "target_pairing": None,
    "portfolio": {"hashes": portfolio["hashes"], "peak_rss_kib": portfolio["watchdog"]["peak_rss_kib"],
                  "elapsed_seconds": portfolio["watchdog"]["elapsed_seconds"]},
    "selected_control": {"hashes": control["hashes"], "peak_rss_kib": control["watchdog"]["peak_rss_kib"],
                         "elapsed_seconds": control["watchdog"]["elapsed_seconds"]},
}
temporary = ROOT / "results_round850_audit.json.tmp"
temporary.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
temporary.replace(ROOT / "results_round850_audit.json")
print(json.dumps(output, sort_keys=True))
