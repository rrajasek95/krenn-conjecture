#!/usr/bin/env python3
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


for raw in (HERE / "FINAL_MANIFEST.sha256").read_text().splitlines():
    digest, name = raw.split(None, 1)
    path = (HERE / name.strip()).resolve()
    assert path.is_file(), path
    assert sha(path) == digest, (path, sha(path), digest)
print("PASS_FINAL_MANIFEST")
