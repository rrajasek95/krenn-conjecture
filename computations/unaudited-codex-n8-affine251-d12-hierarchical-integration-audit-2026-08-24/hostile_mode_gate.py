#!/usr/bin/env python3
"""Cheap parser-only hostile mode checks for a supplied integration binary."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    binary = args.binary.resolve()
    cases = {
        "workers_not_16": ["--workers", "8", "--pivot", "rare", "--strategy", "cold",
                           "--elimination", "hierarchical", "--incremental", "no"],
        "pivot_first": ["--workers", "16", "--pivot", "first", "--strategy", "cold",
                        "--elimination", "hierarchical", "--incremental", "no"],
        "pivot_last": ["--workers", "16", "--pivot", "last", "--strategy", "cold",
                       "--elimination", "hierarchical", "--incremental", "no"],
        "pivot_auto": ["--workers", "16", "--pivot", "auto", "--strategy", "cold",
                       "--elimination", "hierarchical", "--incremental", "no"],
        "strategy_repair": ["--workers", "16", "--pivot", "rare", "--strategy", "repair",
                            "--elimination", "hierarchical", "--incremental", "no"],
        "strategy_best": ["--workers", "16", "--pivot", "rare", "--strategy", "best",
                          "--elimination", "hierarchical", "--incremental", "no"],
        "incremental_yes": ["--workers", "16", "--pivot", "rare", "--strategy", "cold",
                            "--elimination", "hierarchical", "--incremental", "yes"],
        "unknown_elimination": ["--workers", "16", "--pivot", "rare", "--strategy", "cold",
                                "--elimination", "hierarchical-v0", "--incremental", "no"],
    }
    records = {}
    with tempfile.TemporaryDirectory(prefix="d12-hier-hostile-") as temporary:
        root = Path(temporary)
        common = [
            "--input", str(root / "must_not_read"),
            "--output", str(root / "must_not_write.json"),
            "--checkpoint", str(root / "must_not_write.bin"),
            "--vector-cache", str(root / "must_not_write_vectors.bin"),
            "--dual", str(root / "must_not_write.tsv"),
            "--prime", "1073741827",
            "--wall-seconds", "1",
            "--rss-gib", "1",
            "--round-cap", "1",
        ]
        for label, mode in cases.items():
            completed = subprocess.run([str(binary), *common, *mode], text=True,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       timeout=5, check=False)
            created = sorted(path.name for path in root.iterdir())
            passed = (completed.returncode == 2 and not created and
                      ("requires explicit" in completed.stderr or
                       "incremental mode requires tree elimination" in completed.stderr or
                       "bad sparse elimination kernel" in completed.stderr))
            records[label] = {
                "pass": passed,
                "exit_code": completed.returncode,
                "stderr": completed.stderr.strip(),
                "created_paths": created,
            }
            if not passed:
                raise SystemExit(f"hostile mode accepted or wrong failure: {label}")
    result = {
        "schema": "KRENN_AFFINE251_D12_HIERARCHICAL_HOSTILE_MODES_V1",
        "status": "PASS_ALL_UNSUPPORTED_MODES_REJECTED_BEFORE_IO",
        "binary_sha256": sha256(binary),
        "cases": records,
    }
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, args.output)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
