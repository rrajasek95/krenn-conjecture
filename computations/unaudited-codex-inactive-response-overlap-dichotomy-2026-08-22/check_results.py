#!/usr/bin/env python3
"""Replay the inactive response-kernel overlap census at two primes."""

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
    r"^inactive_overlap source=(\S+) corank_one=(\d+) "
    r"inactive_corank_one=(\d+) common_plane_wedge_matches=(\d+) "
    r"joint_rank_hist=(\{.*?\}) adjacent_rank_hist=(\{.*?\}) elapsed="
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def literal(text: str):
    return ast.literal_eval(text.replace("false", "False").replace("true", "True"))


def normalized(mapping):
    return {str(key): value for key, value in mapping.items()}


def replay(prime: int):
    run = subprocess.run(
        [
            "cargo",
            "run",
            "--release",
            "--",
            f"../sources_p{prime}.txt",
            "--inactive-kernel-overlap",
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
        name, corank, inactive, wedge, joint, adjacent = match.groups()
        records[name] = {
            "corank_one": int(corank),
            "inactive_corank_one": int(inactive),
            "common_plane_wedge_matches": int(wedge),
            "joint_rank_hist": joint,
            "adjacent_rank_hist": normalized(literal(adjacent)),
        }
    assert records, run.stdout
    return records


def abstract_guards():
    # Common-plane normal form. The first two source rows are shared by the
    # two endpoint stars; their alternating tensor is killed by commutative
    # squarefree multiplication.
    p = ((1, 0, 0, 1, 1, 0), (0, 1, 0, 1, 0, 1))
    s = p
    wedge = [[0, 1, 0], [-1, 0, 0], [0, 0, 0]]
    coefficient = [[0 for _ in range(6)] for _ in range(6)]
    for i in range(2):
        for j in range(2):
            for a in range(6):
                for b in range(6):
                    if a != b:
                        coefficient[min(a, b)][max(a, b)] += wedge[i][j] * (
                            p[i][a] * s[j][b] + p[i][b] * s[j][a]
                        )
    assert all(value == 0 for row in coefficient for value in row)

    # Six-line split guard: complementary 3-planes in six coordinate lines.
    # Deleting any coordinate makes the two projected 3-planes intersect.
    p_code = (
        (1, 0, 0, 1, 1, 1),
        (0, 1, 0, 1, 2, 3),
        (0, 0, 1, 1, 4, 9),
    )
    s_code = (
        (1, 0, 0, -1, -1, -1),
        (0, 1, 0, -1, -2, -3),
        (0, 0, 1, -1, -4, -9),
    )
    # The six full rows are independent; every five-coordinate projection
    # has rank at most five, hence a nonzero cross-intersection.
    from fractions import Fraction

    def rank(rows):
        matrix = [[Fraction(x) for x in row] for row in rows]
        answer = 0
        for column in range(len(matrix[0])):
            pivot = next((r for r in range(answer, len(matrix)) if matrix[r][column]), None)
            if pivot is None:
                continue
            matrix[answer], matrix[pivot] = matrix[pivot], matrix[answer]
            scale = matrix[answer][column]
            matrix[answer] = [x / scale for x in matrix[answer]]
            for row in range(len(matrix)):
                if row != answer and matrix[row][column]:
                    scale = matrix[row][column]
                    matrix[row] = [x - scale * y for x, y in zip(matrix[row], matrix[answer])]
            answer += 1
        return answer

    assert rank(p_code + s_code) == 6
    assert all(
        rank(tuple(tuple(x for c, x in enumerate(row) if c != omitted) for row in p_code + s_code))
        == 5
        for omitted in range(6)
    )
    return {"common_plane_wedge": True, "six_line_split": True}


def main():
    first = replay(1009)
    second = replay(1013)
    assert first == second
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
        RESULTS_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    else:
        assert payload == json.loads(RESULTS_PATH.read_text())
    print("PASS: inactive-kernel overlap ledgers and dichotomy guards")


if __name__ == "__main__":
    main()
