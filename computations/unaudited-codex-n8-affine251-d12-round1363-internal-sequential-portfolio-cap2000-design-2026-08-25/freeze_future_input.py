#!/usr/bin/env python3
"""Freeze round1362 only after independent FINAL_REPLAY_CLEAR; placeholders block all reads."""
import hashlib
import json
import os
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SCHEDULE = json.loads((HERE / "SCHEDULE.json").read_text())
AUDIT_RESULT_REL = "computations/unaudited-codex-n8-affine251-d12-v4-1-round1362-cap1750-audit-2026-08-25/results_round1362_chain_audit.json"
AUDIT_RESULT_SHA256 = "7386c9d8f24cba33a014f7b90930543ffd2246a265a237c571acd5f321bdb24d"
AUDIT_MANIFEST_REL = "computations/unaudited-codex-n8-affine251-d12-v4-1-round1362-cap1750-audit-2026-08-25/FINAL_MANIFEST.sha256"
AUDIT_MANIFEST_SHA256 = "ab0d32a92c64191d5f67c786f291462b740497deb01b6b4304a6e063e83b8021"
CHECKPOINT_REL = "computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/production_from_round1343_cap1750/stage03/checkpoint.bin"
CHECKPOINT_SHA256 = "ddf8873518c4cef1551daacf1ce82ba67a54ecee9fab6f85af6154964c06112a"
VECTORS_REL = "computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/production_from_round1343_cap1750/stage03/vectors.bin"
VECTORS_SHA256 = "25f42b9b56010684e6f79f648c69ace5a9b09e06756dbe114af5ce9474020f85"
EXPECTED_COLUMNS = 1582672
EXPECTED_SUPPORT = 2043


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
    return {"prime": prime, "round": round_number, "columns": columns,
            "support": support, "bytes": path.stat().st_size}


def vectors_header(path):
    with path.open("rb") as stream:
        data = stream.read(44)
    assert data[:12] == b"AFF12VEC1\0\0\0"
    prime, provider, fingerprint, columns = struct.unpack_from("<QQQQ", data, 12)
    return {"prime": prime, "provider_fingerprint": provider,
            "vector_fingerprint": fingerprint, "columns": columns,
            "bytes": path.stat().st_size}


placeholders = [AUDIT_RESULT_REL, AUDIT_RESULT_SHA256, AUDIT_MANIFEST_REL,
                AUDIT_MANIFEST_SHA256, CHECKPOINT_REL, CHECKPOINT_SHA256,
                VECTORS_REL, VECTORS_SHA256]
assert all(not value.startswith("WAIT_FOR_") for value in placeholders), \
    "launch interlock: round1362 FINAL_REPLAY_CLEAR pins unresolved"
assert EXPECTED_COLUMNS > 0 and EXPECTED_SUPPORT > 0, \
    "launch interlock: round1362 exact counts unresolved"
result_path = REPO / AUDIT_RESULT_REL
manifest_path = REPO / AUDIT_MANIFEST_REL
checkpoint_path = REPO / CHECKPOINT_REL
vectors_path = REPO / VECTORS_REL
assert sha256(result_path) == AUDIT_RESULT_SHA256
assert sha256(manifest_path) == AUDIT_MANIFEST_SHA256
assert sha256(checkpoint_path) == CHECKPOINT_SHA256
assert sha256(vectors_path) == VECTORS_SHA256
result = json.loads(result_path.read_text())
assert result["status"].startswith("PASS_EXACT_")
assert result["input"]["round"] == 1343
assert result["input"]["checkpoint_sha256"] == \
    SCHEDULE["provisional_lineage"]["round1343_checkpoint_sha256"]
assert result["input"]["vectors_sha256"] == \
    SCHEDULE["provisional_lineage"]["round1343_vectors_sha256"]
assert result["final"]["round"] == 1362
assert result["final"]["columns"] == EXPECTED_COLUMNS
assert result["final"]["support"] == EXPECTED_SUPPORT
assert result["final"]["target_coefficient"] == 1
assert result["all_column_replay"]["status"] == "PASS_ALL_COLUMNS"
assert result["all_column_replay"]["columns_replayed"] == EXPECTED_COLUMNS
assert result["all_column_replay"]["verification_failures"] == 0
assert CHECKPOINT_SHA256 in result["artifact_sha256"].values()
assert VECTORS_SHA256 in result["artifact_sha256"].values()
manifest_lines = manifest_path.read_text().splitlines()
assert any(line.startswith(CHECKPOINT_SHA256 + "  ") for line in manifest_lines)
assert any(line.startswith(VECTORS_SHA256 + "  ") for line in manifest_lines)
checkpoint = checkpoint_header(checkpoint_path)
vectors = vectors_header(vectors_path)
assert checkpoint["prime"] == 1073741827 and checkpoint["round"] == 1362
assert checkpoint["columns"] == EXPECTED_COLUMNS and checkpoint["support"] == EXPECTED_SUPPORT
assert vectors["prime"] == 1073741827 and vectors["provider_fingerprint"] == 9218588987274412661
assert vectors["columns"] == EXPECTED_COLUMNS
value = {
    "schema": "KRENN_AFFINE251_D12_ROUND1363_FUTURE_INPUT_PINS_V1",
    "status": "PASS_FROZEN_INDEPENDENT_ROUND1362_FINAL_REPLAY_CLEAR",
    "audit_result": AUDIT_RESULT_REL,
    "audit_result_sha256": AUDIT_RESULT_SHA256,
    "audit_manifest": AUDIT_MANIFEST_REL,
    "audit_manifest_sha256": AUDIT_MANIFEST_SHA256,
    "checkpoint": CHECKPOINT_REL,
    "checkpoint_sha256": CHECKPOINT_SHA256,
    "checkpoint_header": checkpoint,
    "vectors": VECTORS_REL,
    "vectors_sha256": VECTORS_SHA256,
    "vectors_header": vectors,
}
temporary = HERE / "FUTURE_INPUT_PINS.json.tmp"
temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "FUTURE_INPUT_PINS.json")
print(json.dumps(value, sort_keys=True))
