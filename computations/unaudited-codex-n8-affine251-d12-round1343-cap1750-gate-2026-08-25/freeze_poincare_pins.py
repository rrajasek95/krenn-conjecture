#!/usr/bin/env python3
"""Create launch pins only after the independent round1342 seal."""
import hashlib
import json
import os
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
AUDIT = REPO / "computations/unaudited-codex-n8-affine251-d12-v4-1-round1362-audit-2026-08-25"
RESULT = AUDIT / "results_round1342_chain_audit.json"
MANIFEST = AUDIT / "FINAL_MANIFEST.sha256"
STAGE10 = REPO / "computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/production_from_round1262_portfolio_cap1500/stage10"
CHECKPOINT = STAGE10 / "checkpoint.bin"
VECTORS = STAGE10 / "vectors.bin"
EXPECTED_MANIFEST_SHA256 = "7dea99f68ab4d5e04be287b6e382165b679ca29e8271001400152c6c01c33d20"


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


assert EXPECTED_MANIFEST_SHA256 != "WAIT_FOR_POINCARE_FINAL_REPLAY_CLEAR", \
    "launch interlock: authoritative Poincare manifest hash is not patched"
assert RESULT.exists() and MANIFEST.exists(), "round1342 Poincare seal is incomplete"
assert sha256(MANIFEST) == EXPECTED_MANIFEST_SHA256
result = json.loads(RESULT.read_text())
assert result["status"] == "PASS_EXACT_FULLY_TELEMETERED_PROACTIVE_CAP_BOUNDARY_ROUND1342_CHAIN"
assert result["final"] == {"round": 1342, "columns": 1491824, "new_columns": 250973,
                           "remaining_column_headroom": 8176, "support": 1954,
                           "target_coefficient": 1}
assert result["all_column_replay"]["status"] == "PASS_ALL_COLUMNS"
assert result["all_column_replay"]["verification_failures"] == 0
assert result["artifact_sha256"]["stage10_checkpoint"] == sha256(CHECKPOINT)
assert result["artifact_sha256"]["stage10_vectors"] == sha256(VECTORS)
checkpoint = checkpoint_header(CHECKPOINT)
vectors = vectors_header(VECTORS)
assert checkpoint == {"prime": 1073741827, "round": 1342, "columns": 1491824,
                      "support": 1954, "bytes": 22418438}
assert vectors["prime"] == 1073741827 and vectors["provider_fingerprint"] == 9218588987274412661
assert vectors["columns"] == 1491824 and vectors["bytes"] == 3231636588
value = {
    "schema": "KRENN_AFFINE251_D12_ROUND1343_LAUNCH_PINS_V1",
    "status": "PASS_FROZEN_SEALED_ROUND1342_INPUT",
    "poincare_result": str(RESULT.relative_to(REPO)),
    "poincare_result_sha256": sha256(RESULT),
    "poincare_manifest": str(MANIFEST.relative_to(REPO)),
    "poincare_manifest_sha256": sha256(MANIFEST),
    "checkpoint": str(CHECKPOINT.relative_to(REPO)),
    "checkpoint_sha256": result["artifact_sha256"]["stage10_checkpoint"],
    "checkpoint_header": checkpoint,
    "vectors": str(VECTORS.relative_to(REPO)),
    "vectors_sha256": result["artifact_sha256"]["stage10_vectors"],
    "vectors_header": vectors,
}
temporary = HERE / "LAUNCH_PINS.json.tmp"
temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "LAUNCH_PINS.json")
print(json.dumps(value, sort_keys=True))
