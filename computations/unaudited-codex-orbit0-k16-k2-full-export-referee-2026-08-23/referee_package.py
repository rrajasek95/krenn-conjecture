#!/usr/bin/env python3
"""Independent immutable-package referee for the full K16/K2 export."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PKG = ROOT / "computations/unaudited-codex-orbit0-k16-k2-full-export-2026-08-23"
OUT = Path(__file__).resolve().parent
SHARDS = PKG / "shards"
SOURCE_SHA = "8753f475dc7b5165a690236f868a858ce4c3cc94f4b469fadcba889c9d6bd0c7"
BINARY_SHA = "bb9c470b701d99df238264fa4c1da0925817e38009c52b4b887ddb203118628e"
N = 24_097_095


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(16 << 20):
            h.update(chunk)
    return h.hexdigest()


def resolve(recorded: str) -> Path:
    p = Path(recorded)
    return p if p.is_absolute() else ROOT / p


def main() -> None:
    accepted_paths = sorted(SHARDS.glob("shard_*.accepted.json"))
    assert len(accepted_paths) == 64
    top_path = PKG / "results_k16_cached_export.json"
    top = json.loads(top_path.read_text())
    assert top["complete"] and top["accepted_shards"] == 64
    assert top["source_sha256"] == SOURCE_SHA and top["binary_sha256"] == BINARY_SHA

    accepted_hashes: dict[str, str] = {}
    all_manifest_bytes = bytearray()
    listed_parts: set[Path] = set()
    ranges = []
    hist = Counter()
    totals = Counter()
    total_weight = 0
    rows = []
    literal_verifiers = 0
    for shard, ap in enumerate(accepted_paths):
        raw = ap.read_bytes()
        all_manifest_bytes += raw
        accepted_hashes[ap.name] = hashlib.sha256(raw).hexdigest()
        a = json.loads(raw)
        assert a["status"] == "PASS_ACCEPTED_K16_CACHED_SHARD"
        assert a["shard"] == shard
        start, end = a["source_range"]
        assert [shard, start, end] == top["ranges"][shard]
        assert a["source_sha256"] == SOURCE_SHA and a["binary_sha256"] == BINARY_SHA
        assert (start, end) == (N * shard // 64, N * (shard + 1) // 64)
        ranges.append((start, end))

        kpath = resolve(a["kernel_path"])
        vpath = resolve(a["verify_path"])
        assert sha256(kpath) == a["kernel_sha256"]
        assert sha256(vpath) == a["verify_sha256"]
        k = json.loads(kpath.read_text())
        assert k == a["kernel"]
        assert k["status"] == "PASS_COMPLETE_K16_CACHED_SHARD"
        assert k["source_range"] == [start, end]
        verify = vpath.read_text()
        assert verify.startswith("PASS_PREFIX_LITERAL_VERIFY ")
        assert f"start={start} end={end} parts={k['parts']} " in verify
        literal_verifiers += 1

        for name in ("source_rows", "pivotable_source_rows", "generated_k18_parents",
                     "pivotable_k18_parents", "outgoing_pivot_uses",
                     "emitted_records_local_unique", "parts"):
            totals[name] += k[name]
        total_weight += int(k["signed_weight_scaled"])
        hist.update(k["denominator_histogram"])
        assert len(a["part_files"]) == k["parts"]
        assert sum(x["bytes"] for x in a["part_files"]) == a["part_bytes"]
        totals["part_bytes"] += a["part_bytes"]
        for part_index, pmeta in enumerate(a["part_files"]):
            p = resolve(pmeta["path"])
            assert p not in listed_parts
            listed_parts.add(p)
            assert p.name.endswith(f"part{part_index:06}.bin")
            assert p.stat().st_size == pmeta["bytes"]
            assert sha256(p) == pmeta["sha256"]
            rows.append((shard, start, end, part_index, pmeta["path"], pmeta["bytes"], pmeta["sha256"]))

    assert ranges[0][0] == 0 and ranges[-1][1] == N
    assert all(ranges[i][1] == ranges[i + 1][0] for i in range(63))
    actual_parts = set(SHARDS.glob("shard_*_attempt_*.part*.bin"))
    assert actual_parts == listed_parts
    temps = sorted(str(p.relative_to(ROOT)) for p in SHARDS.iterdir() if p.suffix == ".tmp")
    assert not temps

    assert totals["source_rows"] == 24_097_095
    assert totals["pivotable_source_rows"] == 24_003_767
    assert totals["generated_k18_parents"] == 1_559_270_244
    assert totals["pivotable_k18_parents"] == 807_499_618
    assert totals["outgoing_pivot_uses"] == 2_049_974_172
    assert totals["emitted_records_local_unique"] == 63_918_401
    assert totals["parts"] == 281
    assert totals["part_bytes"] == 6_647_540_680
    assert total_weight == 3_218_269_567_887_566_438_400
    assert dict(sorted(hist.items())) == top["denominator_histogram"]
    for key in ("part_bytes", "source_rows", "pivotable_source_rows", "generated_k18_parents",
                "pivotable_k18_parents", "outgoing_pivot_uses"):
        assert totals[key] == top[key]

    parts_tsv = OUT / "verified_parts.tsv"
    parts_tsv.write_text("shard\tstart\tend\tpart\tpath\tbytes\tsha256\n" + "\n".join(
        "\t".join(map(str, r)) for r in rows) + "\n")
    result = {
        "status": "PASS_INDEPENDENT_64_MANIFEST_281_PART_REHASH_AND_COVERAGE",
        "source_package": str(PKG.relative_to(ROOT)),
        "source_sha256": SOURCE_SHA,
        "binary_sha256": BINARY_SHA,
        "top_result_sha256": sha256(top_path),
        "accepted_manifests": 64,
        "accepted_manifest_hashes": accepted_hashes,
        "accepted_manifest_concatenation_sha256": hashlib.sha256(all_manifest_bytes).hexdigest(),
        "literal_verifier_ledgers": literal_verifiers,
        "parts": len(rows),
        "part_bytes": totals["part_bytes"],
        "coverage": [0, N],
        "coverage_disjoint": True,
        "temporary_files": 0,
        "source_rows": totals["source_rows"],
        "pivotable_source_rows": totals["pivotable_source_rows"],
        "generated_k18_parents": totals["generated_k18_parents"],
        "pivotable_k18_parents": totals["pivotable_k18_parents"],
        "outgoing_pivot_uses": totals["outgoing_pivot_uses"],
        "local_nonzero_records": totals["emitted_records_local_unique"],
        "signed_weight_scaled": str(total_weight),
        "denominator_histogram": dict(sorted(hist.items())),
        "hard_gate_seconds": top["hard_gate_seconds"],
        "producer_elapsed_seconds": top["elapsed_seconds"],
        "producer_within_gate": top["elapsed_seconds"] <= top["hard_gate_seconds"],
    }
    dst = OUT / "results_manifest_part_rehash.json"
    dst.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: result[k] for k in ("status", "parts", "part_bytes", "local_nonzero_records",
                                             "accepted_manifest_concatenation_sha256")}, sort_keys=True))


if __name__ == "__main__":
    main()
