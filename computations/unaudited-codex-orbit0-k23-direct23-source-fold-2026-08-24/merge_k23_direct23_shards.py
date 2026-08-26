#!/usr/bin/env python3
"""Strict no-gap merger for the three bounded K23 direct-source shards."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path

U = 400_591_699_200
INTERVALS = [(0, 161), (161, 323), (323, 485)]
GROUPS = {
    "source_D17_R2_4": [f"D17:{x}|R:2-4" for x in (234, 243, 324, 333, 342, 423, 432)],
    "source_D17_R3_3": [f"D17:{x}|R:3-3" for x in (234, 243, 324, 333, 342, 423, 432)],
    "source_D18_R2_3": [f"D18:{x}|R:2-3" for x in (244, 334, 343, 424, 433, 442)],
    "source_D19_R4": [f"D19:{x}|R:4" for x in (344, 434, 443)],
}
RATIOS = {
    "source_D17_R2_4": ("p2_uses", 60),
    "source_D17_R3_3": ("p2_uses", 32),
    "source_D18_R2_3": ("p2_uses", 32),
    "source_D19_R4": ("p1_uses", 60),
}
SUM_FIELDS = (
    "source_heads", "pivotable_source_heads", "p1_uses", "intermediate_children",
    "pivotable_intermediate_children", "p2_uses", "K23_terminal_occurrences",
    "full_occurrences", "irreducible_occurrences",
)
CACHE_SUM = (
    "literal_first_hits", "literal_first_misses", "terminal_hits", "terminal_misses",
    "terminality_assertions_on_realized_keys",
)
CACHE_MAX = ("peak_literal_first_keys_per_R8", "peak_terminal_keys_per_R8")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("shards", nargs=3, type=Path)
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args()
    docs = [json.loads(x.read_text()) for x in args.shards]

    for i, (doc, (lo, hi)) in enumerate(zip(docs, INTERVALS, strict=True)):
        assert doc["status"] == "PASS_BOUNDED_K23_DIRECT_D17_D19_23_ID_PREFIX"
        assert doc["degree"] == 23 and doc["scale_U"] == str(U)
        assert doc["covered_ids"] == 23 and doc["scalar_groups"] == 4
        sel = doc["source_selection"]
        assert sel["mode"] == "interval" and sel["record_count"] == hi - lo
        assert sel["indices"] == list(range(lo, hi)), (i, lo, hi)
        assert [g["group_id"] for g in doc["groups"]] == list(GROUPS)
        for g in doc["groups"]:
            assert g["ids"] == GROUPS[g["group_id"]]
            assert g["full_occurrences"] == g["irreducible_occurrences"]
            assert g["full_charge_scaled_U"] == g["irreducible_charge_scaled_U"]

    merged_groups = []
    for gid in GROUPS:
        parts = [next(g for g in d["groups"] if g["group_id"] == gid) for d in docs]
        out = {"group_id": gid, "ids": GROUPS[gid]}
        for field in SUM_FIELDS:
            out[field] = sum(x[field] for x in parts)
        charge = sum(int(x["full_charge_scaled_U"]) for x in parts)
        out["full_charge_scaled_U"] = str(charge)
        out["irreducible_charge_scaled_U"] = str(charge)
        exact = Fraction(charge, U)
        out["exact_charge"] = f"{exact.numerator}/{exact.denominator}"
        hist: dict[str, int] = {}
        for x in parts:
            for key, value in x["denominator_hist"].items():
                hist[key] = hist.get(key, 0) + value
        out["denominator_hist"] = dict(sorted(hist.items()))
        base, multiplier = RATIOS[gid]
        assert out["K23_terminal_occurrences"] == multiplier * out[base]
        assert out["full_occurrences"] == out["K23_terminal_occurrences"]
        assert out["irreducible_occurrences"] == out["K23_terminal_occurrences"]
        merged_groups.append(out)

    cache = {field: sum(d["cache"][field] for d in docs) for field in CACHE_SUM}
    cache.update({field: max(d["cache"][field] for d in docs) for field in CACHE_MAX})
    for field in ("hard_literal_first_cap_per_R8", "hard_terminal_cap_per_R8"):
        values = {d["cache"][field] for d in docs}
        assert len(values) == 1
        cache[field] = values.pop()
    assert cache["peak_literal_first_keys_per_R8"] <= cache["hard_literal_first_cap_per_R8"]
    assert cache["peak_terminal_keys_per_R8"] <= cache["hard_terminal_cap_per_R8"]

    header = None
    samples: dict[int, str] = {}
    sample_inputs = []
    for result_path, doc in zip(args.shards, docs, strict=True):
        path = Path(doc["sample_ledger"])
        if not path.is_absolute():
            path = Path.cwd() / path
        lines = path.read_text().splitlines()
        assert lines
        header = header or lines[0]
        assert lines[0] == header
        for line in lines[1:]:
            cols = line.split("\t")
            assert len(cols) == 20
            ordinal = int(cols[1])
            assert ordinal not in samples
            assert int(cols[2]) == ordinal * 484 // 256
            assert int(cols[0]) in range(4)
            assert int(cols[15]) != 0 and int(cols[18]) != 0
            samples[ordinal] = line
        sample_inputs.append({"result": str(result_path), "samples": str(path), "sha256": sha256(path)})
    assert set(samples) == set(range(257))
    group_counts = [sum(int(line.split("\t")[0]) == group for line in samples.values()) for group in range(4)]
    assert all(group_counts), group_counts
    sample_out = Path(f"{args.output}.samples.tsv")
    sample_tmp = Path(f"{sample_out}.tmp")
    sample_tmp.write_text(header + "\n" + "\n".join(samples[i] for i in range(257)) + "\n")
    os.replace(sample_tmp, sample_out)

    result = {
        "status": "PASS_COMPLETE_K23_DIRECT_D17_D19_23_ID_SOURCE_FOLD",
        "degree": 23,
        "scale_U": str(U),
        "source_selection": {"mode": "strict_three_shard_merge", "intervals": [list(x) for x in INTERVALS], "record_count": 485},
        "source_slices_declared": 485,
        "covered_ids": 23,
        "scalar_groups": 4,
        "groups": merged_groups,
        "cache": cache,
        "literal_samples": 257,
        "literal_sample_group_counts": group_counts,
        "sample_ledger": str(sample_out),
        "sample_inputs": sample_inputs,
        "input_result_sha256": {str(path): sha256(path) for path in args.shards},
        "sign_rule": docs[0]["sign_rule"],
        "terminality": docs[0]["terminality"],
        "degree_separation": docs[0]["degree_separation"],
        "elapsed_seconds_sum": sum(d["elapsed_seconds"] for d in docs),
        "scope": "exact strict three-shard merge of four grouped scalars covering only the sealed 23 K23 IDs; no row output, K24 scalar, membership, or conjecture claim",
    }
    tmp = Path(f"{args.output}.tmp")
    tmp.write_text(json.dumps(result, indent=2, sort_keys=False) + "\n")
    os.replace(tmp, args.output)
    print(json.dumps({"status": result["status"], "output": str(args.output), "sha256": sha256(args.output), "samples_sha256": sha256(sample_out)}, indent=2))


if __name__ == "__main__":
    main()
