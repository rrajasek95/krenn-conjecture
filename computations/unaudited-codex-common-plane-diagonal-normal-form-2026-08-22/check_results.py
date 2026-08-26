#!/usr/bin/env python3
"""Replay the exact common-plane normal-form split at two primes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


HERE = Path(__file__).resolve().parent
UPSTREAM = HERE.parent / "unaudited-codex-five-set-response-surjectivity-2026-08-22"
CRATE = UPSTREAM / "rust-five-set"
RESULTS = HERE / "results.json"
PATTERN = re.compile(
    r"^common_plane_normal source=(\S+) cases=(\d+) generic=(\d+) "
    r"coordinate=(\d+) diagonal_lifts=(\d+) rank_one_defects=(\d+) "
    r"direct_symmetry=(\d+) exceptional_no_lift=(\d+)$"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(prime: int):
    run = subprocess.run(
        [
            "cargo", "run", "--release", "--",
            f"../sources_p{prime}.txt", "--common-plane-normal-form",
        ],
        cwd=CRATE,
        check=True,
        capture_output=True,
        text=True,
    )
    records = {}
    for line in run.stdout.splitlines():
        match = PATTERN.match(line)
        if not match:
            continue
        name, *values = match.groups()
        records[name] = dict(zip(
            (
                "cases", "generic", "coordinate", "diagonal_lifts",
                "rank_one_defects", "direct_symmetry", "exceptional_no_lift",
            ),
            map(int, values),
            strict=True,
        ))
    assert records, run.stdout
    return records


def abstract_guards():
    # A generic plane U=ker(1,1,1) and phi=D|U.  The three defect columns
    # are all multiples of the common physical form L.
    generic = {
        "normal": [1, 1, 1],
        "diagonal": [2, 3, 5],
        "defect_rank": 1,
        "diagonal_lift": True,
    }

    # Coordinate-plane counterexample to the unqualified diagonal claim.
    # U=<e0,e1>, phi(e0)=e0+e2, phi(e1)=e1.  In relation coordinates
    # (x,-phi(x)), the alternating 3x3 tensor has zero diagonal, yet no
    # diagonal D can restrict to phi because the e2 output is nonzero on U.
    r0 = (1, 0, 0, -1, 0, -1)
    r1 = (0, 1, 0, 0, -1, 0)
    wedge = [
        r0[i] * r1[3 + j] - r1[i] * r0[3 + j]
        for i in range(3) for j in range(3)
    ]
    assert all(wedge[3 * c + c] == 0 for c in range(3))
    assert r0[2] == r1[2] == 0 and (r0[5], r1[5]) != (0, 0)
    exceptional = {
        "left_plane": "span(e0,e1)",
        "zero_diagonal_kernel": True,
        "diagonal_lift": False,
        "wedge": wedge,
    }
    return {"generic": generic, "coordinate_exception": exceptional}


def main():
    first = replay(1009)
    second = replay(1013)
    assert first == second
    assert first["good_star_E1_block"]["generic"] == 1
    assert first["good_star_E1_block"]["rank_one_defects"] == 1
    assert first["dense_support_E1_block"]["coordinate"] == 1
    assert first["dense_support_E1_block"]["exceptional_no_lift"] == 1
    payload = {
        "primes": [1009, 1013],
        "sources": first,
        "abstract_guards": abstract_guards(),
        "sha256": {
            "rust-five-set/src/main.rs": digest(CRATE / "src/main.rs"),
            "sources_p1009.txt": digest(UPSTREAM / "sources_p1009.txt"),
            "sources_p1013.txt": digest(UPSTREAM / "sources_p1013.txt"),
        },
    }
    if "--write-results" in sys.argv:
        RESULTS.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    else:
        assert payload == json.loads(RESULTS.read_text())
    print("PASS: common-plane normal form and coordinate exception")


if __name__ == "__main__":
    main()
