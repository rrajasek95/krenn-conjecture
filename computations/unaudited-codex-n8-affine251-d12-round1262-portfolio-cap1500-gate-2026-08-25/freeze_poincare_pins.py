#!/usr/bin/env python3
"""Create launch pins only from the sealed independent round1261 audit."""
import hashlib
import json
import os
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
AUDIT = REPO / "computations/unaudited-codex-n8-affine251-d12-v4-1-round1261-audit-2026-08-25"
RESULT = AUDIT / "results_round1261_chain_audit.json"
MANIFEST = AUDIT / "FINAL_MANIFEST.sha256"
STAGE10 = REPO / "computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/production_from_round1161_portfolio_cap1250/stage10"
CHECKPOINT = STAGE10 / "checkpoint.bin"
VECTORS = STAGE10 / "vectors.bin"
EXPECTED_MANIFEST_SHA256 = "6d6afafd615117f58c91eabb1e3ebb5f348918860636e3b2011cab668c0f8dc0"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def checkpoint_header(path):
    with path.open("rb") as stream:
        data = stream.read(44)
    assert data[:12] == b"AFF12CEG1\0\0\0"
    prime, round_number, columns, support = struct.unpack_from("<QQQQ", data, 12)
    assert path.stat().st_size == 44 + 15 * columns + 21 * support
    return {"prime": prime, "round": round_number, "columns": columns, "support": support,
            "bytes": path.stat().st_size}


def vectors_header(path):
    with path.open("rb") as stream:
        data = stream.read(44)
    assert data[:12] == b"AFF12VEC1\0\0\0"
    prime, provider, fingerprint, columns = struct.unpack_from("<QQQQ", data, 12)
    return {"prime": prime, "provider_fingerprint": provider,
            "vector_fingerprint": fingerprint, "columns": columns,
            "bytes": path.stat().st_size}


assert EXPECTED_MANIFEST_SHA256 != "WAIT_FOR_POINCARE_FINAL_REPLAY_CLEAR", \
    "launch interlock: authoritative Poincare manifest hash has not been patched"
assert RESULT.exists() and MANIFEST.exists(), "Poincare/round1261 seal is not complete"
assert sha256(MANIFEST) == EXPECTED_MANIFEST_SHA256
result = json.loads(RESULT.read_text())
assert result["status"] == "PASS_EXACT_FULLY_TELEMETERED_ROUND1261_CHAIN"
assert result["final"] == {
    "round": 1261, "columns": 1238541, "new_columns": 276738,
    "support": 1065, "target_coefficient": 1,
}
assert result["all_column_replay"]["status"] == "PASS_ALL_COLUMNS"
assert result["all_column_replay"]["verification_failures"] == 0
assert result["artifact_sha256"]["stage10_checkpoint"] == sha256(CHECKPOINT)
assert result["artifact_sha256"]["stage10_vectors"] == sha256(VECTORS)
assert checkpoint_header(CHECKPOINT) == {
    "prime": 1073741827, "round": 1261, "columns": 1238541,
    "support": 1065, "bytes": 18600524,
}
vector_header = vectors_header(VECTORS)
assert vector_header["prime"] == 1073741827
assert vector_header["provider_fingerprint"] == 9218588987274412661
assert vector_header["columns"] == 1238541

value = {
    "schema": "KRENN_AFFINE251_D12_ROUND1262_LAUNCH_PINS_V1",
    "status": "PASS_FROZEN_SEALED_ROUND1261_INPUT",
    "poincare_result": str(RESULT.relative_to(REPO)),
    "poincare_result_sha256": sha256(RESULT),
    "poincare_manifest": str(MANIFEST.relative_to(REPO)),
    "poincare_manifest_sha256": sha256(MANIFEST),
    "checkpoint": str(CHECKPOINT.relative_to(REPO)),
    "checkpoint_sha256": result["artifact_sha256"]["stage10_checkpoint"],
    "checkpoint_header": checkpoint_header(CHECKPOINT),
    "vectors": str(VECTORS.relative_to(REPO)),
    "vectors_sha256": result["artifact_sha256"]["stage10_vectors"],
    "vectors_header": vector_header,
}
temporary = HERE / "LAUNCH_PINS.json.tmp"
temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "LAUNCH_PINS.json")
print(json.dumps(value, sort_keys=True))
