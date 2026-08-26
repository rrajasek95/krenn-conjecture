#!/usr/bin/env python3
"""Hostile exact merger for the four bounded direct-K15 K22 shards."""

from __future__ import annotations

import hashlib
import json
import os
from collections import Counter
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
U = 400_591_699_200
INTERVALS = ((0, 122), (122, 244), (244, 365), (365, 485))
NAMES = (
    "D15:{223,232,322}|R:4-3",
    "D15:{223,232,322}|R:2-2-3",
    "D15:{223,232,322}|R:2-3-2",
    "D15:{223,232,322}|R:3-2-2",
)
IDS = {
    name: [f"D15:{packet}|R:{name.rsplit(':', 1)[1]}" for packet in ("223", "232", "322")]
    for name in NAMES
}
SUM_FIELDS = (
    "source_heads",
    "source_mass",
    "source_l1",
    "terminal_K22_occurrences",
    "full_occurrences",
    "irreducible_occurrences",
    "full_charge_scaled_U",
    "irreducible_charge_scaled_U",
)
ARRAY_FIELDS = (
    "stage_pivot_uses",
    "stage_tail_candidates",
    "stage_pivotable_children",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    shards = []
    pins = []
    for i, interval in enumerate(INTERVALS):
        path = HERE / f"results_shard_{i:02d}.json"
        raw = path.read_bytes()
        doc = json.loads(raw)
        assert doc["status"] == "PASS_BOUNDED_GROUPED_DIRECT_K15_FOUR_SINK_K22_GATE"
        assert tuple(doc["slice_interval"]) == interval
        assert doc["source_slices"] == interval[1] - interval[0]
        assert doc["workers"] == 8
        assert doc["scale_U"] == str(U)
        assert doc["elapsed_seconds"] < 600
        assert list(doc["sinks"]) == list(NAMES)
        shards.append(doc)
        pins.append(
            {
                "path": path.name,
                "sha256": digest(raw),
                "slice_interval": list(interval),
                "elapsed_seconds": doc["elapsed_seconds"],
            }
        )

    assert INTERVALS[0][0] == 0 and INTERVALS[-1][1] == 485
    assert all(INTERVALS[i][1] == INTERVALS[i + 1][0] for i in range(3))

    merged = {}
    all_ids = []
    for name in NAMES:
        pieces = [doc["sinks"][name] for doc in shards]
        assert all(p["ids"] == IDS[name] for p in pieces)
        assert all(p["individual_id_charges"] is None for p in pieces)
        out = {
            "ids": IDS[name],
            "individual_id_charges": None,
        }
        for field in SUM_FIELDS:
            total = sum(int(p[field]) for p in pieces)
            out[field] = str(total) if field.endswith("_scaled_U") or field in ("source_mass", "source_l1") else total
        for field in ARRAY_FIELDS:
            width = len(pieces[0][field])
            assert all(len(p[field]) == width for p in pieces)
            out[field] = [sum(p[field][j] for p in pieces) for j in range(width)]
        hist = Counter()
        for p in pieces:
            hist.update({int(k): int(v) for k, v in p["denominator_product_hist"].items()})
        out["denominator_product_hist"] = {str(k): hist[k] for k in sorted(hist)}

        assert out["source_heads"] == 6_704_640
        assert (int(out["source_mass"]), int(out["source_l1"])) == (322_486_272, 3_085_516_800)
        final_stage = 2 if out["stage_pivot_uses"][2] else 1
        assert out["terminal_K22_occurrences"] == out["stage_tail_candidates"][final_stage]
        assert out["terminal_K22_occurrences"] == out["full_occurrences"] == out["irreducible_occurrences"]
        assert out["full_charge_scaled_U"] == out["irreducible_charge_scaled_U"]
        assert all(U % product == 0 for product in hist)
        charge = Fraction(int(out["full_charge_scaled_U"]), U)
        out["full_charge"] = f"{charge.numerator}/{charge.denominator}"
        out["irreducible_charge"] = out["full_charge"]
        all_ids.extend(out["ids"])
        merged[name] = out

    expected_ids = [id_ for name in NAMES for id_ in IDS[name]]
    assert all_ids == expected_ids
    assert len(all_ids) == len(set(all_ids)) == 12

    result = {
        "status": "PASS_COMPLETE_GROUPED_DIRECT_K15_FOUR_SINK_K22_CHARGE",
        "scale_U": str(U),
        "source_slice_interval": [0, 485],
        "source_slices": 485,
        "shard_coverage_guard": "exact ordered intervals [0,122),[122,244),[244,365),[365,485); no gap or overlap",
        "shards": pins,
        "sinks": merged,
        "strict_id_guard": {
            "expected_ordered_ids": expected_ids,
            "observed_ordered_ids": all_ids,
            "expected_count": 12,
            "observed_count": len(all_ids),
            "missing": sorted(set(expected_ids) - set(all_ids)),
            "unexpected": sorted(set(all_ids) - set(expected_ids)),
            "duplicates": sorted(k for k, v in Counter(all_ids).items() if v != 1),
        },
        "packet_grouping_guard": "packet witnesses 322/232/223 retained only as grouped source classes; no individual scalar split",
        "terminality": "every K22 output has anchor mass 2 below pivot mass 4, so full equals irreducible",
        "scope": "four separate grouped K22 sinks covering exactly 12 IDs; no rows, K23, or K24",
        "elapsed_seconds_sum": sum(p["elapsed_seconds"] for p in pins),
        "elapsed_seconds_max_shard": max(p["elapsed_seconds"] for p in pins),
    }
    guard = result["strict_id_guard"]
    assert not guard["missing"] and not guard["unexpected"] and not guard["duplicates"]
    out_path = HERE / "results_k22_direct_k15_four_sink.json"
    tmp_path = out_path.with_suffix(out_path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(result, indent=2, sort_keys=False) + "\n")
    os.replace(tmp_path, out_path)
    print(json.dumps({"status": result["status"], "result_sha256": digest(out_path.read_bytes())}, indent=2))


if __name__ == "__main__":
    main()
