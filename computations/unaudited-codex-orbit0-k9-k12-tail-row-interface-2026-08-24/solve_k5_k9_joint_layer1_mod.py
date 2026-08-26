#!/usr/bin/env python3
"""Peel the exact first joint lower/K9 source subsystem modulo two primes."""

from __future__ import annotations

import hashlib
import json
from collections import deque
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE / "k9_k12_tail_rows.tsv"
COLUMNS = HERE / "k9_incidence_full_layer1_columns.tsv"
EDGES = HERE / "k5_k9_column_output_full_edges.tsv"
OUT = HERE / "results_k5_k9_joint_layer1_modular_peel.json"
PINS = {
    TARGET: "4e214b40aede42b09c4c3dfc05c2969541f1a9dd6271f7eb53b36303478ba3ae",
    COLUMNS: "3f940e0296bed5eed868f9631c390c871bbc0c0608a4f9d5eada8e82356c6656",
    EDGES: "84c855eb07ad8283727ff7cf71e9289f41ed6fa4e0439ba15b9bb424a657976e",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load():
    for path, digest in PINS.items():
        require(sha256(path) == digest, f"pin changed: {path}")
    target = {}
    with TARGET.open() as handle:
        require(handle.readline().rstrip("\n") == "degree\trow\tcoefficient", "target header changed")
        for line in handle:
            degree, row, coefficient = line.rstrip("\n").split("\t")
            if degree == "9":
                target[(9, bytes.fromhex(row))] = int(coefficient)
    require(len(target) == 49988, "K9 target census changed")
    with COLUMNS.open() as handle:
        require(handle.readline().rstrip("\n") == "column_index\tminimum_degree\tword\tmultiplier", "column header changed")
        column_count = sum(1 for _ in handle)
    require(column_count == 128875, "column census changed")

    row_index = {}
    row_adj = []
    column_adj = [[] for _ in range(column_count)]
    edge_count = 0
    with EDGES.open() as handle:
        require(handle.readline().rstrip("\n") == "column_index\tdegree\trow\tmultiplicity", "edge header changed")
        for line in handle:
            column, degree, row, value = line.rstrip("\n").split("\t")
            column, degree, value = int(column), int(degree), int(value)
            require(0 <= column < column_count and 5 <= degree <= 9 and value > 0, "bad incidence record")
            key = (degree, bytes.fromhex(row))
            if key not in row_index:
                row_index[key] = len(row_index)
                row_adj.append([])
            r = row_index[key]
            row_adj[r].append((column, value))
            column_adj[column].append((r, value))
            edge_count += 1
    require(edge_count == 2922993, "edge census changed")
    target_by_row = [0] * len(row_index)
    missing = 0
    for key, coefficient in target.items():
        if key in row_index:
            target_by_row[row_index[key]] = coefficient
        else:
            missing += 1
    require(missing == 0, "target escaped joint row closure")
    degree_counts = {}
    for degree, _ in row_index:
        degree_counts[degree] = degree_counts.get(degree, 0) + 1
    require(degree_counts == {5: 138, 6: 1494, 7: 14007, 8: 113952, 9: 719957}, "row degree census changed")
    return target_by_row, row_adj, column_adj, degree_counts


def peel(prime: int, target, row_adj, column_adj):
    rhs = [value % prime for value in target]
    degree = [len(edges) for edges in row_adj]
    active = bytearray(b"\x01") * len(column_adj)
    queue = deque(index for index, value in enumerate(degree) if value <= 1)
    contradictions = []
    assigned = 0
    while queue:
        row = queue.popleft()
        if degree[row] == 0:
            if rhs[row] and len(contradictions) < 16:
                contradictions.append((row, rhs[row]))
            continue
        if degree[row] != 1:
            continue
        live = [(column, value) for column, value in row_adj[row] if active[column]]
        require(len(live) == 1, "active degree bookkeeping mismatch")
        column, coefficient = live[0]
        value = rhs[row] * pow(coefficient, -1, prime) % prime
        active[column] = 0
        assigned += 1
        for affected, entry in column_adj[column]:
            if degree[affected] == 0:
                continue
            rhs[affected] = (rhs[affected] - entry * value) % prime
            degree[affected] -= 1
            if degree[affected] <= 1:
                queue.append(affected)
    core_columns = sum(active)
    core_rows = sum(value > 0 for value in degree)
    inconsistent = sum(bool(value == 0 and rhs[index]) for index, value in enumerate(degree))
    return {
        "prime": prime,
        "assigned_columns": assigned,
        "core_columns": core_columns,
        "core_rows": core_rows,
        "zero_rows_nonzero_rhs": inconsistent,
        "contradiction_samples": contradictions,
        "status": (
            "PASS_JOINT_LAYER1_SUBSYSTEM_SOLVED" if core_columns == 0 and inconsistent == 0
            else "INCOMPLETE_JOINT_LAYER1_SUBSYSTEM_CONTRADICTION" if inconsistent
            else "INCOMPLETE_JOINT_LAYER1_CORE_REMAINS"
        ),
    }


def main() -> None:
    target, row_adj, column_adj, degree_counts = load()
    results = [peel(prime, target, row_adj, column_adj) for prime in (1009, 1013)]
    payload = {
        "status": "PASS_EXACT_JOINT_LAYER1_MODULAR_PEEL_AUDIT",
        "target_K9_rows": 49988,
        "joint_rows_by_degree": degree_counts,
        "columns": len(column_adj),
        "weighted_edges": sum(map(len, row_adj)),
        "prime_results": results,
        "interpretation": (
            "This tests Lx=0 and T9x=R9 on the exact first target-rooted column set. "
            "Only a solved subsystem is positive; a contradiction/core requires closure from newly reached rows."
        ),
        "pins": {path.name: digest for path, digest in PINS.items()},
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
