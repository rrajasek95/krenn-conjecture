#!/usr/bin/env python3
"""Freeze r1463 only after independent FINAL_REPLAY_CLEAR; placeholders block reads."""
import hashlib
import json
import os
from pathlib import Path
import struct

if not __debug__:
    raise RuntimeError("fail closed: freezer requires assertions enabled")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SCHEDULE = json.loads((HERE / "SCHEDULE.json").read_text())
AUDIT_RESULT_REL = "computations/unaudited-codex-n8-affine251-d12-v4-1-round1463-cap2250-audit-2026-08-25/results_round1463_chain_audit.json"
AUDIT_RESULT_SHA256 = "6d207999056a49fc5d94d63dda182e47348131078627b241bca024ca45e6c28d"
AUDIT_MANIFEST_REL = "computations/unaudited-codex-n8-affine251-d12-v4-1-round1463-cap2250-audit-2026-08-25/FINAL_MANIFEST.sha256"
AUDIT_MANIFEST_SHA256 = "46e69f29a46d24fadd2163e301ad77127071981aad3c0ad2305882b214da6bbb"
CHECKPOINT_REL = "computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/production_from_round1448_cap2250/stage04/checkpoint.bin"
CHECKPOINT_SHA256 = "1b4dde9f009b4343099190e293913818b3df88dfc34c27653e7cfcd4acf08c8e"
VECTORS_REL = "computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/production_from_round1448_cap2250/stage04/vectors.bin"
VECTORS_SHA256 = "46744c37b6c1ab30e6ce945a9f049e45683b4324470e661554f4ae4134b9d48c"
EXPECTED_COLUMNS = 2049529
EXPECTED_SUPPORT = 2389


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
    "launch interlock: round1463 FINAL_REPLAY_CLEAR pins unresolved"
assert EXPECTED_COLUMNS > 0 and EXPECTED_SUPPORT > 0, \
    "launch interlock: round1463 exact counts unresolved"
result_path, manifest_path = REPO / AUDIT_RESULT_REL, REPO / AUDIT_MANIFEST_REL
checkpoint_path, vectors_path = REPO / CHECKPOINT_REL, REPO / VECTORS_REL
assert sha256(result_path) == AUDIT_RESULT_SHA256
assert sha256(manifest_path) == AUDIT_MANIFEST_SHA256
assert sha256(checkpoint_path) == CHECKPOINT_SHA256
assert sha256(vectors_path) == VECTORS_SHA256
result = json.loads(result_path.read_text())
assert result["status"].startswith("PASS_EXACT_")
assert result["final"]["round"] == 1463
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
checkpoint, vectors = checkpoint_header(checkpoint_path), vectors_header(vectors_path)
assert checkpoint["prime"] == 1073741827 and checkpoint["round"] == 1463
assert checkpoint["columns"] == EXPECTED_COLUMNS and checkpoint["support"] == EXPECTED_SUPPORT
assert vectors["prime"] == 1073741827 and vectors["provider_fingerprint"] == 9218588987274412661
assert vectors["columns"] == EXPECTED_COLUMNS
value = {
    "schema": "KRENN_AFFINE251_D12_ROUND1464_FUTURE_INPUT_PINS_V1",
    "status": "PASS_FROZEN_INDEPENDENT_ROUND1463_FINAL_REPLAY_CLEAR",
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
