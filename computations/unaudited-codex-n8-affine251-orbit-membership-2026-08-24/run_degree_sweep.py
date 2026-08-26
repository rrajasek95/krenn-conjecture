#!/usr/bin/env python3
"""Cost-free local D4--D12 dual-prime sweep with hard solver gates."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

INPUT_SHA = "75a82d82a979d75507e682fd339e83d4ae35949653d624fb541148bd3957dcff"
PRIMES = (1073741827, 1073741789)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            h.update(block)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--start-degree", type=int, default=4)
    parser.add_argument("--end-degree", type=int, default=12)
    parser.add_argument("--wall-seconds", type=int, default=1800)
    parser.add_argument("--rss-gib", type=int, default=42)
    parser.add_argument("--pivot", choices=("first", "last"), default="first")
    parser.add_argument("--output", type=Path, default=Path("results_sweep.json"))
    args = parser.parse_args()
    assert sha256(args.input) == INPUT_SHA
    assert 4 <= args.start_degree <= args.end_degree <= 12
    assert 1 <= args.wall_seconds <= 1800 and 1 <= args.rss_gib <= 42
    records = []
    for degree in range(args.start_degree, args.end_degree + 1):
        degree_records = []
        for prime in PRIMES:
            result = Path(f"results_d{degree}_p{prime}.json")
            checkpoint = Path(f"closure_d{degree}.bin")
            dual = Path(f"dual_d{degree}_p{prime}.tsv")
            if not result.exists():
                command = [str(args.binary), "--input", str(args.input), "--degree", str(degree),
                           "--prime", str(prime), "--output", str(result), "--checkpoint", str(checkpoint),
                           "--dual", str(dual), "--wall-seconds", str(args.wall_seconds),
                           "--rss-gib", str(args.rss_gib), "--pivot", args.pivot]
                subprocess.run(command, check=True)
            data = json.loads(result.read_text())
            degree_records.append({"prime": prime, "status": data["status"],
                                   "result": str(result), "result_sha256": sha256(result),
                                   "rows": data["row_orbits"], "columns": data["column_orbits"],
                                   "rank": data["rank"], "elapsed_seconds": data["elapsed_seconds"]})
            if data["status"].startswith("INCOMPLETE"):
                records.append({"degree": degree, "primes": degree_records})
                args.output.write_text(json.dumps({"schema": "KRENN_AFFINE251_SWEEP_V1",
                    "status": "INCOMPLETE_RESOURCE_GATE", "degrees": records}, indent=2) + "\n")
                return
        for key in ("status", "rows", "columns", "rank"):
            assert degree_records[0][key] == degree_records[1][key]
        records.append({"degree": degree, "primes": degree_records})
    args.output.write_text(json.dumps({"schema": "KRENN_AFFINE251_SWEEP_V1",
        "status": "COMPLETE_DUAL_PRIME_SWEEP", "degrees": records}, indent=2) + "\n")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, KeyError, subprocess.CalledProcessError) as exc:
        print(f"REJECT: {exc}", file=sys.stderr)
        raise SystemExit(2)
