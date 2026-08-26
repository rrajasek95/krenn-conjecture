#!/usr/bin/env python3
"""Singleton-peel the exact first K9 incidence subsystem modulo two primes."""

from __future__ import annotations

import hashlib
import json
from collections import deque
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROWS = HERE / "k9_k12_tail_rows.tsv"
COLUMNS = HERE / "k9_incidence_full_layer1_columns.tsv"
EDGES = HERE / "k9_incidence_full_layer1_edges.tsv"
OUT = HERE / "results_k9_layer1_modular_peel.json"
PINS = {
    ROWS: "4e214b40aede42b09c4c3dfc05c2969541f1a9dd6271f7eb53b36303478ba3ae",
    COLUMNS: "3f940e0296bed5eed868f9631c390c871bbc0c0608a4f9d5eada8e82356c6656",
    EDGES: "c36834d59758cd98f0e74fda6989c5ac4d185da018bc8b510293f437ae3cfb07",
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
    with ROWS.open() as handle:
        require(handle.readline().rstrip("\n") == "degree\trow\tcoefficient", "target header changed")
        for line in handle:
            degree, row, coefficient = line.rstrip("\n").split("\t")
            if degree == "9":
                target[row] = int(coefficient)
    require(len(target) == 49988, "target K9 census changed")

    dense_column = {}
    with COLUMNS.open() as handle:
        require(handle.readline().rstrip("\n") == "column_index\tminimum_degree\tword\tmultiplier", "column header changed")
        for line in handle:
            index, minimum, _, _ = line.rstrip("\n").split("\t")
            if minimum == "9":
                dense_column[int(index)] = len(dense_column)
    require(len(dense_column) == 59429, "min9 column census changed")

    row_index = {}
    row_adj = []
    column_adj = [[] for _ in dense_column]
    edge_count = 0
    with EDGES.open() as handle:
        require(handle.readline().rstrip("\n") == "column_index\trow\tmultiplicity", "edge header changed")
        for line in handle:
            global_column, row, value = line.rstrip("\n").split("\t")
            column = dense_column[int(global_column)]
            if row not in row_index:
                row_index[row] = len(row_index)
                row_adj.append([])
            r = row_index[row]
            value = int(value)
            require(value > 0, "nonpositive incidence")
            row_adj[r].append((column, value))
            column_adj[column].append((r, value))
            edge_count += 1
    require(len(row_index) == 272579 and edge_count == 484000, "edge/row census changed")
    target_by_row = [0] * len(row_index)
    missing_target = 0
    for row, coefficient in target.items():
        if row in row_index:
            target_by_row[row_index[row]] = coefficient
        elif coefficient:
            missing_target += 1
    return target_by_row, row_adj, column_adj, missing_target


def peel(prime: int, target, row_adj, column_adj, missing_target: int):
    rhs = [value % prime for value in target]
    degree = [len(edges) for edges in row_adj]
    active = bytearray(b"\x01") * len(column_adj)
    assignment = [None] * len(column_adj)
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
        assignment[column] = value
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
    zero_rows_nonzero_rhs = missing_target + sum(bool(value == 0 and rhs[index]) for index, value in enumerate(degree))
    return {
        "prime": prime,
        "assigned_columns": assigned,
        "core_columns": core_columns,
        "core_rows": core_rows,
        "zero_rows_nonzero_rhs": zero_rows_nonzero_rhs,
        "contradiction_samples": contradictions,
        "status": (
            "PASS_LAYER1_SUBSYSTEM_SOLVED" if core_columns == 0 and zero_rows_nonzero_rhs == 0
            else "INCOMPLETE_LAYER1_SUBSYSTEM_CONTRADICTION" if zero_rows_nonzero_rhs
            else "INCOMPLETE_LAYER1_CORE_REMAINS"
        ),
    }


def main() -> None:
    target, row_adj, column_adj, missing_target = load()
    results = [peel(prime, target, row_adj, column_adj, missing_target) for prime in (1009, 1013)]
    payload = {
        "status": "PASS_EXACT_FIRST_LAYER_MODULAR_PEEL_AUDIT",
        "target_rows": 49988,
        "incidence_rows": len(row_adj),
        "min9_columns": len(column_adj),
        "weighted_edges": sum(map(len, row_adj)),
        "target_rows_without_min9_incidence": missing_target,
        "prime_results": results,
        "interpretation": (
            "A solved subsystem is a positive K9 certificate. A contradiction or core in this first target-rooted layer "
            "is not a nonmembership result because further min9 columns from newly reached rows and lower-kernel transfers are absent."
        ),
        "pins": {path.name: digest for path, digest in PINS.items()},
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
