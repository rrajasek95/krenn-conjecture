#!/usr/bin/env python3
"""Replay the pure-word quotient census and its source-universal identity."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


HERE = Path(__file__).resolve().parent
UPSTREAM = HERE.parent / "unaudited-codex-five-set-response-surjectivity-2026-08-22"
CRATE = UPSTREAM / "rust-five-set"
RESULTS_PATH = HERE / "results.json"
PATTERN = re.compile(
    r"^pure_quotient source=(\S+) groups=(\d+) open=(\d+) "
    r"open_h6_zero=(\d+) open_carrier_corank=(\d+) "
    r"full_response_increment=(\{.*?\}) profiles=(\{.*?\}) elapsed="
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stringify_keys(mapping):
    return {str(key): value for key, value in mapping.items()}


def rust_literal(text: str):
    return ast.literal_eval(text.replace("false", "False").replace("true", "True"))


def replay(prime: int):
    completed = subprocess.run(
        [
            "cargo",
            "run",
            "--release",
            "--",
            f"../sources_p{prime}.txt",
            "--pure-quotient",
        ],
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
        name, groups, opened, hzero, corank, increment, profiles = match.groups()
        records[name] = {
            "groups": int(groups),
            "open": int(opened),
            "open_h6_zero": int(hzero),
            "open_carrier_corank": int(corank),
            "full_response_increment": stringify_keys(rust_literal(increment)),
            "profiles": stringify_keys(rust_literal(profiles)),
        }
    assert records, completed.stdout
    return records


def current_hashes():
    paths = {
        "rust-five-set/src/main.rs": CRATE / "src/main.rs",
        "rust-five-set/Cargo.toml": CRATE / "Cargo.toml",
        "rust-five-set/Cargo.lock": CRATE / "Cargo.lock",
        "sources_p1009.txt": UPSTREAM / "sources_p1009.txt",
        "sources_p1013.txt": UPSTREAM / "sources_p1013.txt",
    }
    return {name: digest(path) for name, path in paths.items()}


def main():
    first = replay(1009)
    second = replay(1013)
    assert first == second, "two-prime ledgers differ"
    payload = {
        "primes": [1009, 1013],
        "identity_checks_per_source_prime": 28 * 3 * 9,
        "triangle_groups_per_source_prime": 28 * 3 * 20,
        "sources": first,
        "sha256": current_hashes(),
    }
    if "--write-results" in sys.argv:
        RESULTS_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    else:
        expected = json.loads(RESULTS_PATH.read_text())
        assert payload == expected
    print(
        "PASS: 15+90 pure-word identities and quotient profiles agree "
        "at p1009 and p1013"
    )


if __name__ == "__main__":
    main()
