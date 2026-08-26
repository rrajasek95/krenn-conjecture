#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
GENERIC = REPO / "computations/unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24"
SOURCE_CHECKPOINT = GENERIC / "production_from_round749/stage04/checkpoint.bin"
SOURCE_VECTORS = GENERIC / "production_from_round749/stage04/vectors.bin"
EXPECTED_CHECKPOINT_SHA = "ce87c58cf79ddebbc0f9ce39eb36f08b6bf85a8f0f764f7728c3565da13fab49"
EXPECTED_VECTORS_SHA = "040b1b59bad7693fbd7ed71d8ff9f760b39b30943c77f452eae3b4047b5ac254"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
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
assert checkpoint_header(SOURCE_CHECKPOINT) == {
    "prime": 1073741827, "round": 849, "columns": 460676, "support": 312
}
source_vectors = vectors_header(SOURCE_VECTORS)
assert source_vectors["prime"] == 1073741827 and source_vectors["columns"] == 460676

clones = {}
for label in ("portfolio", "selected_control"):
    checkpoint = ROOT / label / "checkpoint.bin"
    vectors = ROOT / label / "vectors.bin"
    clone(SOURCE_CHECKPOINT, checkpoint)
    clone(SOURCE_VECTORS, vectors)
    assert sha256(checkpoint) == EXPECTED_CHECKPOINT_SHA
    assert sha256(vectors) == EXPECTED_VECTORS_SHA
    assert checkpoint_header(checkpoint) == checkpoint_header(SOURCE_CHECKPOINT)
    assert vectors_header(vectors) == source_vectors
    clones[label] = {"checkpoint": str(checkpoint.relative_to(REPO)),
                     "vectors": str(vectors.relative_to(REPO)),
                     "checkpoint_sha256": EXPECTED_CHECKPOINT_SHA,
                     "vectors_sha256": EXPECTED_VECTORS_SHA}

value = {
    "schema": "KRENN_AFF251_D12_ROUND850_PORTFOLIO_INPUTS_V1",
    "status": "PASS_APFS_CLONED_FROZEN_INPUTS",
    "source_checkpoint": str(SOURCE_CHECKPOINT.relative_to(REPO)),
    "source_vectors": str(SOURCE_VECTORS.relative_to(REPO)),
    "source_checkpoint_sha256": EXPECTED_CHECKPOINT_SHA,
    "source_vectors_sha256": EXPECTED_VECTORS_SHA,
    "input_state": checkpoint_header(SOURCE_CHECKPOINT),
    "vector_header": source_vectors,
    "clone_method": "/bin/cp -c (APFS clone)",
    "clones": clones,
    "production_mutated": False,
}
temporary = ROOT / "INPUT_PINS.json.tmp"
temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
os.replace(temporary, ROOT / "INPUT_PINS.json")
print(json.dumps(value, sort_keys=True))
