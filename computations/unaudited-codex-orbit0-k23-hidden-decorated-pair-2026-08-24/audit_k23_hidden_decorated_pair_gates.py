#!/usr/bin/env python3
import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/hidden_k16_decorated_pair_orbits_full.bin"
SCHEDULE = ROOT / "computations/unaudited-codex-orbit0-k23-availability-schedule-2026-08-24/results_k23_availability_schedule.json"
UPSTREAM_REFEREE = ROOT / "computations/unaudited-codex-orbit0-k22-hidden-pair-fold-2026-08-24/results_hidden_pair_independent_referee.json"
ENGINE_TOP = ROOT / "computations/unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23/run_hidden_children_prefix.rs"
ENGINE_BASE = ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/run_filtered_k17.rs"
CYCLE_AUX = ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin"
K4_AUX = ROOT / "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin"
EXPECTED_IDS = ["D14:222|R:2-3-4", "D14:222|R:2-4-3"]
EXPECTED_SOURCE_SHA = "22f91fc887caecb628df495b6a19e319c0ada39b6940b1ca4f795ae09d6c21c8"
U = 400_591_699_200
N = 101_545_723
HEADER = 80
RECORD = 53
PAIR_MASS = 146_230_609_431_055_564_800

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()

def load(name):
    return json.loads((HERE / name).read_text())

assert SCHEDULE.exists() and sha(SCHEDULE) == "45550f92ea0cae4d988e1cc1c13117134a6c78a66d68c3e4950d3ec24e2dbb15"
schedule = json.loads(SCHEDULE.read_text())
artifact = schedule["artifacts"]["hidden_decorated_k16_pair_orbits"]
assert artifact["sha256"] == EXPECTED_SOURCE_SHA and artifact["records"] == N
assert schedule["artifacts"]["cycle_aux"]["sha256"] == sha(CYCLE_AUX) == "8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7"
assert schedule["artifacts"]["response_k4"]["sha256"] == sha(K4_AUX) == "4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3"
family = next(x for x in schedule["physical_folds"] if x["family_id"] == "hidden_decorated_k16_pair")
intervals = [[0, 33_848_574], [33_848_574, 67_697_148], [67_697_148, N]]
assert family["planned_intervals"] == intervals
assert family["group_ids"] == ["source_D14_R2_3_4", "source_D14_R2_4_3"]

assert sha(UPSTREAM_REFEREE) == "e428846ba3fa8e310405b754a1b2eb8fbf05c2a18b74f86223c67e98b23c4f45"
upstream = json.loads(UPSTREAM_REFEREE.read_text())
assert upstream["status"].startswith("PASS_INDEPENDENT")

assert SOURCE.stat().st_size == HEADER + RECORD * N
with open(SOURCE, "rb") as f:
    h = f.read(HEADER)
assert h[:8] == b"H16ORM1\0"
assert int.from_bytes(h[8:24], "little", signed=True) == U
assert int.from_bytes(h[28:30], "little") == RECORD
assert int.from_bytes(h[32:40], "little") == 246
assert int.from_bytes(h[40:48], "little") == 305
assert int.from_bytes(h[48:56], "little") == N
assert int.from_bytes(h[64:80], "little", signed=True) == PAIR_MASS

gate_specs = [
    ("results_prefix1.json", 1),
    ("results_prefix4096.json", 4_096),
    ("results_prefix1000000.json", 1_000_000),
]
gate_rows = []
for name, count in gate_specs:
    x = load(name)
    assert x["status"] == "PASS_BOUNDED_K23_HIDDEN_DECORATED_PAIR_TWO_SINK"
    assert x["covered_lineage_ids"] == EXPECTED_IDS and len(set(x["covered_lineage_ids"])) == 2
    assert int(x["scale_U"]) == U
    assert x["input_sha256_expected"] == EXPECTED_SOURCE_SHA
    assert x["input_records_declared"] == N
    assert x["input_interval"] == [0, count] and x["input_records_consumed"] == count
    assert set(x["sinks"]) == set(EXPECTED_IDS)
    for lineage, first, terminal in [(EXPECTED_IDS[0], 32, 60), (EXPECTED_IDS[1], 60, 32)]:
        z = x["sinks"][lineage]
        assert z["first_tail_evaluations"] == first * count
        assert z["terminal_K23_occurrences"] == terminal * z["selected_p3"]
        assert z["full_occurrences"] == z["irreducible_occurrences"] == z["terminal_K23_occurrences"]
        assert int(z["normalized_p3_weight_scaled"]) == -int(z["pivotable_weight_scaled"])
        assert int(z["terminal_weight_scaled"]) == terminal * int(z["normalized_p3_weight_scaled"])
        assert z["full_charge_scaled"] == z["irreducible_charge_scaled"]
        assert z["cache"]["hits"] + z["cache"]["misses"] == z["selected_p3"]
        assert z["cache"]["peak_keys"] <= 300_720
    sample = HERE / (name + ".samples.tsv")
    lines = sample.read_text().splitlines()
    expected_samples = count if count <= 257 else 257
    assert len(lines) == expected_samples + 1
    expected_indices = list(range(count)) if count <= 257 else [j * (count - 1) // 256 for j in range(257)]
    nonzero34 = nonzero43 = 0
    with open(SOURCE, "rb") as f:
        for line, index in zip(lines[1:], expected_indices):
            cols = line.split("\t")
            assert len(cols) == 21 and int(cols[0]) == index
            f.seek(HEADER + RECORD * index)
            rec = f.read(RECORD)
            assert cols[1] == rec[:24].hex()
            assert int(cols[2]) == rec[24]
            assert int(cols[3]) == int.from_bytes(rec[25:41], "little", signed=True)
            assert int(cols[4]) == int.from_bytes(rec[41:49], "little")
            assert int(cols[5]) == int.from_bytes(rec[49:51], "little")
            assert int(cols[6]) == int.from_bytes(rec[51:53], "little")
            assert int(cols[7]) == 32 and int(cols[10]) == 60 * int(cols[9])
            assert int(cols[11]) % 60 == 0
            assert int(cols[13]) == 60 and int(cols[16]) == 32 * int(cols[15])
            assert int(cols[17]) % 32 == 0
            assert int(cols[19]) == (int(cols[9]) > 0)
            assert int(cols[20]) == (int(cols[15]) > 0)
            nonzero34 += int(cols[19]); nonzero43 += int(cols[20])
    assert x["literal_witness_guard"]["records"] == expected_samples
    assert x["literal_witness_guard"]["R234_nonzero"] == nonzero34
    assert x["literal_witness_guard"]["R243_nonzero"] == nonzero43
    assert x["literal_witness_guard"]["all_terminal_K23_nonpivotable"] is True
    assert x["literal_witness_guard"]["all_abstract_literal_cycle_keys_equal"] is True
    gate_rows.append({
        "count": count,
        "elapsed_seconds": x["elapsed_seconds"],
        "linear_full_projection_seconds": x["linear_full_projection_seconds"],
        "result_sha256": sha(HERE / name),
        "samples_sha256": sha(sample),
        "sample_records": expected_samples,
        "R234_charge_scaled_U": x["sinks"][EXPECTED_IDS[0]]["full_charge_scaled"],
        "R243_charge_scaled_U": x["sinks"][EXPECTED_IDS[1]]["full_charge_scaled"],
    })

million_projection = gate_rows[-1]["linear_full_projection_seconds"]
conservative_max = million_projection * 2 / 3
assert conservative_max < 540
assert intervals[0][0] == 0 and intervals[-1][1] == N
assert all(intervals[i][1] == intervals[i+1][0] for i in range(2))
full_result = HERE / "results_hidden_decorated_pair_k23_charge.json"
assert not full_result.exists()

payload = {
    "status": "PASS_K23_HIDDEN_DECORATED_PAIR_PREFIX_GATES_FULL_HELD",
    "degree": 23,
    "strict_ids": EXPECTED_IDS,
    "scale_U": U,
    "source": {
        "path": str(SOURCE.relative_to(ROOT)), "sha256": EXPECTED_SOURCE_SHA,
        "records": N, "bytes": SOURCE.stat().st_size, "header_schema_checked": True,
        "full_hash_authority": str(SCHEDULE.relative_to(ROOT)),
    },
    "engine_pins": {
        "run_hidden_children_prefix.rs": sha(ENGINE_TOP),
        "run_filtered_k17.rs": sha(ENGINE_BASE),
        "cycle_aux_sha256": sha(CYCLE_AUX),
        "K4_aux_sha256": sha(K4_AUX),
    },
    "recurrence": {
        EXPECTED_IDS[0]: "decorated K16/p2 -> K3 -> pivotable K19/p3 -> terminal K4",
        EXPECTED_IDS[1]: "decorated K16/p2 -> K4 -> pivotable K20/p3 -> terminal K3",
        "sign": "w2 -> -w2/m3", "all_divisions_exact": True,
        "full_equals_irreducible": True,
    },
    "prefix_gates": gate_rows,
    "witness_replay": {
        "distributed_records": 257, "source_fields_seek_replayed": True,
        "literal_terminal_checks_in_producer": True,
        "abstract_literal_cycle_key_equality_in_producer": True,
    },
    "production_schedule": {
        "atomic_intervals": intervals, "gap_free_no_overlap": True,
        "million_prefix_linear_full_projection_seconds": million_projection,
        "cache_reset_safety_multiplier": 2,
        "conservative_max_shard_seconds": conservative_max,
        "launch_projection_limit_seconds": 540, "hard_wall_seconds": 600,
        "family_RSS_limit_GiB": 8, "aggregate_RSS_limit_GiB": 16,
        "memory_basis": "same two capped 300000-key PKey-to-Resp caches as sealed K22 fold; terminal degree changes response work, not entry size; no rows",
        "atomic_results_and_exact_merge_required": True,
    },
    "full_production": {"launched": False, "result_absent": True, "held_pending_explicit_clearance": True},
    "scope": "two strict K23 scalar sinks and gates only; no full charge, rows, K24, membership, or conjecture claim",
}
logical = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
payload["logical_sha256"] = logical
(HERE / "results_k23_hidden_decorated_pair_gate_audit.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": payload["status"], "logical_sha256": logical, "conservative_max_shard_seconds": conservative_max}, indent=2))
