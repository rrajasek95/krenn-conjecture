#!/usr/bin/env python3
"""Strict audit of the prefix-only hidden-collected K23 singleton gates."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
U = 400_591_699_200
TOTAL = 158_439_965
LINEAGE = "D14:222|R:2-2-2-3"
SOURCE = ROOT / "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/checkpoint_k18_22_pivotable.bin"
SOURCE_SHA = "442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8"
SOURCE_LEDGER = SOURCE.parent / "CHECKPOINTS.sha256"
SOURCE_LEDGER_SHA = "3a8f14e7daf0620c5f4e09e1928f286857d8c3d77c6051570135aa8f13134c85"
PREFIXES = [
    ("results_prefix1.json", 1, 1, 128, -2_043_889_061_068_800),
    ("results_prefix4096.json", 4_096, 257, 742_144, -7_837_849_435_786_444_800),
    ("results_prefix1000000.json", 1_000_000, 257, 120_571_904, -128_019_438_175_017_664_512),
]


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def intervals(total: int, parts: int) -> list[list[int]]:
    boundaries = [total * index // parts for index in range(parts + 1)]
    return [[boundaries[index], boundaries[index + 1]] for index in range(parts)]


def main() -> None:
    require(SOURCE.stat().st_size == 12_675_197_280, SOURCE.stat().st_size)
    require(digest(SOURCE_LEDGER) == SOURCE_LEDGER_SHA, "source ledger drift")
    require(SOURCE_LEDGER.read_text().splitlines()[0].startswith(SOURCE_SHA + "  "), "source hash not first ledger pin")
    with SOURCE.open("rb") as stream:
        header = stream.read(80)
    require(header[:8] == b"H18PIV2\0", header[:8])
    require(int.from_bytes(header[8:24], "little", signed=True) == U, "source U")
    require(int.from_bytes(header[28:30], "little") == 80, "record bytes")
    require(int.from_bytes(header[48:56], "little") == TOTAL, "source records")
    require(int.from_bytes(header[56:64], "little") == 1, "source groups")
    require(int.from_bytes(header[64:80], "little", signed=True) == 724_159_651_336_720_220_160, "source mass")

    gates = []
    for name, count, samples, terminal, charge in PREFIXES:
        path = HERE / name
        result = json.loads(path.read_text())
        require(result["status"] == "PASS_BOUNDED_HIDDEN_COLLECTED_K18_K23_GATE", name)
        require(result["degree"] == 23 and int(result["scale_U"]) == U, name)
        require(result["strict_id"] == LINEAGE and result["input_interval"] == [0, count] and result["input_records"] == count, name)
        require(result["pivotable_K20_children"] == result["selected_K20_p4_uses"], name)
        require(result["terminal_K3_tails"] == terminal == 32 * result["selected_K20_p4_uses"], name)
        require(result["full_occurrences"] == result["irreducible_occurrences"] == terminal, name)
        require(int(result["full_charge_scaled_U"]) == int(result["irreducible_charge_scaled_U"]) == charge, name)
        require(result["full_equals_irreducible"] is True and "mass 1" in result["terminality"], name)
        cache = result["cache"]
        require(cache["K18_keys"] == cache["K18_misses"] and cache["K18_hits"] + cache["K18_misses"] == result["selected_K18_p3_uses"], name)
        require(cache["K20_K3_keys"] == cache["K20_K3_misses"] and cache["K20_K3_hits"] + cache["K20_K3_misses"] == result["selected_K20_p4_uses"], name)
        histogram = {tuple(map(int, key.split("_"))): value for key, value in result["m2_m3_m4_hist"].items()}
        require(sum(histogram.values()) == result["selected_K20_p4_uses"], name)
        require(all(m4 == 1 and U % (m2 * m3 * m4) == 0 for (m2, m3, m4) in histogram), name)
        require(result["literal_sample_source_records"] == samples, name)
        ledger = HERE / (name + ".samples.tsv")
        with ledger.open(newline="") as stream:
            rows = list(csv.DictReader(stream, delimiter="\t"))
        require(len(rows) == samples, (name, len(rows)))
        expected_indices = sorted({index * (count - 1) // 256 for index in range(257)})
        require([int(row["input_index"]) for row in rows] == expected_indices, name)
        gates.append({
            "count": count,
            "result_path": str(path.relative_to(ROOT)),
            "result_sha256": digest(path),
            "sample_path": str(ledger.relative_to(ROOT)),
            "sample_sha256": digest(ledger),
            "elapsed_seconds": result["elapsed_seconds"],
            "projected_full_seconds": result["projected_full_seconds"],
            "terminal_K3_tails": terminal,
            "charge_scaled_U": str(charge),
        })

    referee_path = HERE / "results_k23_hidden_prefix1000000_referee.json"
    referee = json.loads(referee_path.read_text())
    require(referee["status"] == "PASS_INDEPENDENT_257_LITERAL_H18PIV2_K23_SINGLETON_PREFIX_REFEREE", referee)
    require(referee["strict_id"] == LINEAGE and referee["distributed_parents"] == 257, referee)
    require(referee["source_interval"] == [0, 1_000_000] and referee["last_index"] == 999_999, referee)
    require(referee["literal_terminal_K23_children"] == 32 * referee["literal_pivotable_K20_children"] == 33_152, referee)
    require(referee["all_divisions_exact"] and referee["all_K23_children_terminal"] and referee["source_provenance_replayed"], referee)

    schedule = intervals(TOTAL, 3)
    require(schedule == [[0, 52_813_321], [52_813_321, 105_626_643], [105_626_643, 158_439_965]], schedule)
    projection = gates[-1]["projected_full_seconds"]
    conservative_shard = projection / 3 * 2
    require(conservative_shard < 540, conservative_shard)
    full_result = HERE / "results_k23_hidden_collected_k18.json"
    require(not full_result.exists(), "full production result unexpectedly exists")

    result = {
        "status": "PASS_K23_HIDDEN_COLLECTED_SINGLETON_PREFIX_GATES_FULL_HELD",
        "strict_id": LINEAGE,
        "degree": 23,
        "scale_U": U,
        "source": {
            "path": str(SOURCE.relative_to(ROOT)),
            "sha256": SOURCE_SHA,
            "bytes": SOURCE.stat().st_size,
            "records": TOTAL,
            "header_and_geometry_replayed": True,
        },
        "prefix_gates": gates,
        "independent_literal_referee": {
            "path": str(referee_path.relative_to(ROOT)),
            "sha256": digest(referee_path),
            "distributed_source_records": 257,
            "literal_terminal_K23_children": referee["literal_terminal_K23_children"],
        },
        "recurrence": {
            "path": "H18PIV2 D14 R2-2 -> K2 response -> pivotable K20 -> K3 response -> terminal K23",
            "sign": "w -> -w/m3 -> +w/(m3*m4)",
            "m4_universally_one": True,
            "terminal_anchor_mass": 1,
            "full_equals_irreducible": True,
        },
        "production_schedule": {
            "atomic_intervals": schedule,
            "shards": 3,
            "prefix_million_linear_full_projection_seconds": projection,
            "cache_reset_safety_multiplier": 2,
            "conservative_max_shard_seconds": conservative_shard,
            "hard_wall_seconds": 600,
            "launch_projection_limit_seconds": 540,
            "family_RSS_limit_GiB": 8,
            "aggregate_RSS_limit_GiB": 16,
            "memory_bound": "non-increasing versus sealed K22 H18PIV2 full fold (<1.4 GiB): same cache keys/value sizes, smaller K18 plan, no row output",
            "gap_free_no_overlap": True,
            "atomic_results_and_exact_merge_required": True,
        },
        "full_production": {
            "launched": False,
            "held_reason": "direct23 shard2 is active; no concurrent full hidden scan authorized",
        },
        "scope": "three prefix gates, independent 257-source literal replay, and production schedule only; no full K23 scalar, rows, K24, membership, or conjecture claim",
    }
    logical = hashlib.sha256(json.dumps(result, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    output = HERE / "results_k23_hidden_gate_audit.json"
    temporary = Path(str(output) + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(output)
    print(json.dumps({
        "status": result["status"],
        "projection_full_seconds": projection,
        "conservative_max_shard_seconds": conservative_shard,
        "full_launched": False,
        "logical_sha256": logical,
    }, indent=2))


if __name__ == "__main__":
    main()
