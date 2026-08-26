#!/usr/bin/env python3
import glob
import hashlib
import json
import os
from pathlib import Path

HERE = Path("computations/unaudited-codex-orbit0-k16-k2-full-export-2026-08-23")
OPT = Path("computations/unaudited-codex-orbit0-k16-k2-export-optimization-2026-08-23")
N = 24_097_095


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(8 << 20)
            if not b:
                return h.hexdigest()
            h.update(b)


result = json.loads((HERE / "results_k16_cached_export.json").read_text())
assert result["status"] == "PASS_COMPLETE_64_SHARD_K16_CACHED_EXPORT"
paths = sorted(HERE.glob("shards/shard_*.accepted.json"))
assert len(paths) == 64
accepted = [json.loads(p.read_text()) for p in paths]
assert [x["shard"] for x in accepted] == list(range(64))
assert [x["source_range"] for x in accepted] == [[N*i//64,N*(i+1)//64] for i in range(64)]
assert accepted[0]["source_range"][0] == 0 and accepted[-1]["source_range"][1] == N

fields = ["source_rows", "pivotable_source_rows", "generated_k18_parents",
          "pivotable_k18_parents", "outgoing_pivot_uses",
          "emitted_records_local_unique", "parts"]
sums = {k: sum(x["kernel"][k] for x in accepted) for k in fields}
sums["signed_weight_scaled"] = str(sum(int(x["kernel"]["signed_weight_scaled"]) for x in accepted))
assert sums == result["totals"]
assert sums["source_rows"] == N
assert sums["pivotable_source_rows"] == 24_003_767
assert sums["generated_k18_parents"] == 1_559_270_244
assert sums["generated_k18_parents"] // 12 == 129_939_187
assert sums["pivotable_k18_parents"] == 807_499_618

hist = {}
for x in accepted:
    assert x["status"] == "PASS_ACCEPTED_K16_CACHED_SHARD"
    assert sha(x["kernel_path"]) == x["kernel_sha256"]
    assert sha(x["verify_path"]) == x["verify_sha256"]
    assert Path(x["verify_path"]).read_text().startswith("PASS_PREFIX_LITERAL_VERIFY")
    for k, v in x["kernel"]["denominator_histogram"].items():
        hist[k] = hist.get(k, 0) + v
assert dict(sorted(hist.items())) == result["denominator_histogram"]
assert sum(hist.values()) == sums["pivotable_k18_parents"]
assert sum(int(k.split("_")[1]) * v for k, v in hist.items()) == sums["outgoing_pivot_uses"]

parts = [q for x in accepted for q in x["part_files"]]
assert len(parts) == 281
assert len({q["path"] for q in parts}) == len(parts)
for q in parts:
    assert os.path.getsize(q["path"]) == q["bytes"]
    assert sha(q["path"]) == q["sha256"]
assert sum(q["bytes"] for q in parts) == result["part_bytes"] == 6_647_540_680
assert not list(HERE.rglob("*.tmp"))
assert sha(OPT / "export_k16_cached_profiles.rs") == result["source_sha256"]
assert sha(OPT / "export_k16_cached_profiles") == result["binary_sha256"]

out = {
    "status": "PASS_FULL_64_SHARD_PACKAGE_HASH_AND_COVERAGE_REPLAY",
    "accepted_shards": 64,
    "parts": 281,
    "part_bytes": 6_647_540_680,
    "source_rows": sums["source_rows"],
    "pivotable_source_rows": sums["pivotable_source_rows"],
    "first_pivot_uses": sums["generated_k18_parents"] // 12,
    "generated_k18_parents": sums["generated_k18_parents"],
    "pivotable_k18_parents": sums["pivotable_k18_parents"],
    "outgoing_pivot_uses": sums["outgoing_pivot_uses"],
    "local_nonzero_records": sums["emitted_records_local_unique"],
    "signed_weight_scaled": sums["signed_weight_scaled"],
    "literal_verifier_ledgers": 64,
    "temporary_files": 0,
}
tmp = HERE / "results_k16_cached_export_package_audit.json.tmp"
dst = HERE / "results_k16_cached_export_package_audit.json"
tmp.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
os.replace(tmp, dst)
print(json.dumps(out, indent=2, sort_keys=True))
