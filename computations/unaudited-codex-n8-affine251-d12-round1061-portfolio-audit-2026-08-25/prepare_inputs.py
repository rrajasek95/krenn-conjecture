#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
V4 = REPO / "computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25"
SOURCE_DIR = V4 / "production_from_round961/stage05"
SOURCE_CHECKPOINT = SOURCE_DIR / "checkpoint.bin"
SOURCE_VECTORS = SOURCE_DIR / "vectors.bin"
EXPECTED_CHECKPOINT_SHA = "1bc0315df0c97878b3d61f0dd945ff0ba28f922d9e62728f043210c9357c7a2d"
EXPECTED_VECTORS_SHA = "0d71ab7b833623d6ea2fb99a822859bef14f9ba30f54e32bf744d383f65995a3"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def checkpoint_header(path):
    with path.open("rb") as stream:
        header = stream.read(44)
    assert header[:12] == b"AFF12CEG1\0\0\0"
    prime, rounds, columns, support = struct.unpack_from("<QQQQ", header, 12)
    assert path.stat().st_size == 44 + 15 * columns + 21 * support
    return {"prime": prime, "round": rounds, "columns": columns, "support": support}


def vectors_header(path):
    with path.open("rb") as stream:
        header = stream.read(44)
    assert header[:12] == b"AFF12VEC1\0\0\0"
    prime, provider, fingerprint, columns = struct.unpack_from("<QQQQ", header, 12)
    return {"prime": prime, "provider": provider, "fingerprint": fingerprint,
            "columns": columns, "bytes": path.stat().st_size}


def clone(source, destination):
    assert not destination.exists(), f"refusing to overwrite {destination}"
    destination.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["/bin/cp", "-c", str(source), str(destination)], check=True)


assert not (ROOT / "INPUT_PINS.json").exists()
assert sha256(SOURCE_CHECKPOINT) == EXPECTED_CHECKPOINT_SHA
assert sha256(SOURCE_VECTORS) == EXPECTED_VECTORS_SHA
state = checkpoint_header(SOURCE_CHECKPOINT)
assert state == {"prime": 1073741827, "round": 1060, "columns": 729800, "support": 826}
vector_header = vectors_header(SOURCE_VECTORS)
assert vector_header["prime"] == 1073741827
assert vector_header["provider"] == 9218588987274412661
assert vector_header["columns"] == 729800

clones = {}
for label in ("portfolio", "selected_control"):
    checkpoint = ROOT / label / "checkpoint.bin"
    vectors = ROOT / label / "vectors.bin"
    clone(SOURCE_CHECKPOINT, checkpoint)
    clone(SOURCE_VECTORS, vectors)
    assert sha256(checkpoint) == EXPECTED_CHECKPOINT_SHA
    assert sha256(vectors) == EXPECTED_VECTORS_SHA
    assert checkpoint_header(checkpoint) == state
    assert vectors_header(vectors) == vector_header
    clones[label] = {
        "checkpoint": str(checkpoint.relative_to(REPO)),
        "vectors": str(vectors.relative_to(REPO)),
        "checkpoint_sha256": EXPECTED_CHECKPOINT_SHA,
        "vectors_sha256": EXPECTED_VECTORS_SHA,
    }

value = {
    "schema": "KRENN_AFF251_D12_ROUND1061_PORTFOLIO_INPUTS_V1",
    "status": "PASS_APFS_CLONED_FROZEN_ROUND1060_INPUTS",
    "source_checkpoint": str(SOURCE_CHECKPOINT.relative_to(REPO)),
    "source_vectors": str(SOURCE_VECTORS.relative_to(REPO)),
    "source_checkpoint_sha256": EXPECTED_CHECKPOINT_SHA,
    "source_vectors_sha256": EXPECTED_VECTORS_SHA,
    "round1060_audit_manifest_sha256": "7c1649f025dfa9286955e4322a166ef2691a72443e8f1075adf4db6e4584365a",
    "input_state": state,
    "vector_header": vector_header,
    "clone_method": "/bin/cp -c (APFS clone)",
    "clones": clones,
    "production_mutated": False,
}
temporary = ROOT / "INPUT_PINS.json.tmp"
temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
os.replace(temporary, ROOT / "INPUT_PINS.json")
print(json.dumps(value, sort_keys=True))
