#!/usr/bin/env python3
"""Replay the Rust census and compare both primes with the frozen ledger."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
CRATE = HERE / "rust-five-set"
RESULTS = json.loads((HERE / "results.json").read_text())
PATTERN = re.compile(
    r"^source=(\S+) profiles=(\d+) theta_rank_hist=(\{.*?\}) "
    r"triangle_min_rank_hist=(\{.*?\}) base_rank_hist=(\{.*?\}) .*?examples="
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized(mapping):
    return {str(key): value for key, value in mapping.items()}


def replay(prime: int):
    completed = subprocess.run(
        ["cargo", "run", "--release", "--", f"../sources_p{prime}.txt"],
        cwd=CRATE,
        check=True,
        capture_output=True,
        text=True,
    )
    records = {}
    for line in completed.stdout.splitlines():
        match = PATTERN.match(line)
        if not match:
            continue
        name, profiles, theta, triangle, base = match.groups()
        if name not in RESULTS["sources"]:
            continue
        records[name] = {
            "profiles": int(profiles),
            "theta_rank": normalized(ast.literal_eval(theta)),
            "triangle_min_rank": normalized(ast.literal_eval(triangle)),
            "base_rank": normalized(ast.literal_eval(base)),
        }
    assert set(records) == set(RESULTS["sources"]), records.keys()
    for name, expected in RESULTS["sources"].items():
        actual = records[name]
        assert actual["profiles"] == RESULTS["profiles_per_source"]
        for key in ("theta_rank", "triangle_min_rank", "base_rank"):
            assert actual[key] == expected[key], (prime, name, key, actual[key])
    return records


def main():
    for relative, expected in RESULTS["sha256"].items():
        assert digest(HERE / relative) == expected, relative
    first = replay(RESULTS["primes"][0])
    second = replay(RESULTS["primes"][1])
    assert first == second
    print("PASS: Rust 5,040-profile ledgers agree at p1009 and p1013")


if __name__ == "__main__":
    main()
