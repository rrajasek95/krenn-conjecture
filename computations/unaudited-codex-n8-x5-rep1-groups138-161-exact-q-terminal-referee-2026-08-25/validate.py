#!/usr/bin/env python3
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


for line in (HERE / "FINAL_MANIFEST.sha256").read_text().splitlines():
    digest, name = line.split(None, 1)
    path = (HERE / name.strip()).resolve()
    assert path.is_file() and sha(path) == digest
print("PASS_FINAL_MANIFEST")
