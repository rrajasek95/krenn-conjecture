#!/usr/bin/env python3
"""Independent structural, K9-equality, H-order, and charge audit."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SEED = ROOT / "computations/unaudited-codex-orbit0-t2-radical-2026-08-20/sparse_r8_k9_tail_terms.txt"
OLD_K9 = ROOT / "computations/unaudited-codex-orbit0-t2-radical-2026-08-20/results_sparse_r8_k9_tail.json"
DUAL = ROOT / "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23/k16_cycle_partition_dual.tsv"
RESULT = HERE / "results_k9_k12_tail_rows.json"
ROWS = HERE / "k9_k12_tail_rows.tsv"
SOURCE = HERE / "expand_k9_k12_tail_rows.rs"
BINARY = HERE / "expand_k9_k12_tail_rows"
OUT = HERE / "results_k9_k12_tail_rows_audit.json"

PINS = {
    SEED: "b572b774d3d50d2618aa2d79338681fcf80542bf19ddd6e319037f9432aab74b",
    OLD_K9: "6b85cca58d6da26f426404eb785b2d9bf7858a4c758a651e1e9aa66729b08132",
    DUAL: "fea91d03250128fa6ea99252659ddd2b46329a9318916a19d6dae0ecfb69dd84",
    RESULT: "9b9afdfa0a568c36baed084a86f4b345760792ff9bd5bc3c840b1be8f1033c52",
    ROWS: "4e214b40aede42b09c4c3dfc05c2969541f1a9dd6271f7eb53b36303478ba3ae",
    SOURCE: "cc63eeb426003b717f9e5526a95f87dc2a422a42f105fe9c20a85f58c0ccd9da",
    BINARY: "43efb3cbb2e844351fedce1cda332493d578f5c13ada78d78d2024b41446b99d",
}
EXPECTED_COUNTS = {9: 49988, 10: 174561, 11: 282556, 12: 210770}
EXPECTED_MASS = {9: -9648576, 10: -37920384, 11: -97206912, 12: 19313280}
EXPECTED_L1 = {9: 102475296, 10: 390468624, 11: 710700864, 12: 550284288}
EXPECTED_CHARGE = {9: -18809856, 10: 14923008, 11: -2981376, 12: 2304000}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cell_tables():
    ports = []
    metadata = []
    edge = 0
    for u in range(8):
        for v in range(u + 1, 8):
            for a in range(3):
                for b in range(3):
                    ports.append((3 * u + a, 3 * v + b))
                    metadata.append((u, v, a, b, edge))
            edge += 1
    return ports, metadata


PORTS, METADATA = cell_tables()


def cycle_partition(cells: tuple[int, ...]) -> tuple[int, ...]:
    adjacency = [[] for _ in range(24)]
    for cell in cells:
        u, v = PORTS[cell]
        adjacency[u].append(v)
        adjacency[v].append(u)
    require(all(len(neighbours) == 2 for neighbours in adjacency), "row is not 2-regular")
    seen = set()
    parts = []
    for start in range(24):
        if start in seen:
            continue
        stack = [start]
        size = 0
        while stack:
            vertex = stack.pop()
            if vertex in seen:
                continue
            seen.add(vertex)
            size += 1
            stack.extend(adjacency[vertex])
        parts.append(size)
    return tuple(sorted(parts))


def parse_seed():
    anchors = None
    actions = []
    for line in SEED.read_text().splitlines():
        fields = line.split()
        if not fields:
            continue
        if fields[0] == "ANCHORS":
            anchors = tuple(bytes.fromhex(fields[1]))
        elif fields[0] == "ACTION":
            actions.append((tuple(map(int, fields[1])), tuple(map(int, fields[2]))))
    require(anchors is not None and len(anchors) == 12, "anchors changed")
    require(len(actions) == 2304, "action census changed")
    return anchors, actions


def transform_row(row: tuple[int, ...], action) -> tuple[int, ...]:
    sites, colours = action
    transformed = []
    for cell in row:
        u, v, a, b, _ = METADATA[cell]
        u, v, a, b = sites[u], sites[v], colours[a], colours[b]
        if u > v:
            u, v, a, b = v, u, b, a
        edge = u * (15 - u) // 2 + (v - u - 1)
        transformed.append(9 * edge + 3 * a + b)
    return tuple(sorted(transformed))


def audit():
    for path, digest in PINS.items():
        require(sha256(path) == digest, f"pin changed: {path}")
    result = json.loads(RESULT.read_text())
    require(result["status"] == "PASS_EXACT_H_COINVARIANT_K9_K12_TAIL_ROWS", "bad producer status")
    require(result["degrees"] == [9, 10, 11, 12], "degree set changed")
    require(result["tail_nonzero_row_orbits"] == list(EXPECTED_COUNTS.values()), "producer count changed")
    require(list(map(int, result["tail_coefficient_mass"])) == list(EXPECTED_MASS.values()), "producer mass changed")
    require(list(map(int, result["tail_coefficient_l1"])) == list(EXPECTED_L1.values()), "producer L1 changed")

    anchors, actions = parse_seed()
    anchor_set = set(anchors)
    dual = {}
    lines = DUAL.read_text().splitlines()
    require(lines[0] == "cycle_partition\tinteger_coefficient", "dual header changed")
    for line in lines[1:]:
        partition, coefficient = line.split("\t")
        dual[tuple(map(int, partition.split(",")))] = int(coefficient)
    require(len(dual) == 77, "dual support changed")

    old_k9_data = json.loads(OLD_K9.read_text())
    old_k9 = {row: int(coefficient) for row, coefficient in old_k9_data["tail"]}
    require(len(old_k9) == 49988, "old K9 row census changed")

    counts = Counter()
    masses = Counter()
    l1 = Counter()
    charges = Counter()
    seen_k9 = {}
    total = sum(EXPECTED_COUNTS.values())
    targets = {index * total // 257 for index in range(257)}
    samples = []
    previous = None
    with ROWS.open() as handle:
        require(handle.readline().rstrip("\n") == "degree\trow\tcoefficient", "row header changed")
        for ordinal, line in enumerate(handle):
            fields = line.rstrip("\n").split("\t")
            require(len(fields) == 3, "row schema changed")
            degree, row_hex, coefficient = int(fields[0]), fields[1], int(fields[2])
            require(degree in EXPECTED_COUNTS, "row degree escaped K9--K12")
            require(coefficient != 0, "zero coefficient retained")
            require(len(row_hex) == 24, "row width changed")
            key = (degree, row_hex)
            require(previous is None or previous < key, "row ledger is not strictly sorted")
            previous = key
            row = tuple(bytes.fromhex(row_hex))
            require(tuple(sorted(row)) == row, "literal row is not sorted")
            require(sum(cell not in anchor_set for cell in row) == degree, "literal K-degree mismatch")
            counts[degree] += 1
            masses[degree] += coefficient
            l1[degree] += abs(coefficient)
            charges[degree] += coefficient * dual.get(cycle_partition(anchors + row), 0)
            if degree == 9:
                seen_k9[row_hex] = coefficient
            if ordinal in targets:
                samples.append((ordinal, row))
    require(sum(counts.values()) == total, "total row count changed")
    require(dict(counts) == EXPECTED_COUNTS, "per-degree row count changed")
    require(dict(masses) == EXPECTED_MASS, "per-degree coefficient mass changed")
    require(dict(l1) == EXPECTED_L1, "per-degree coefficient L1 changed")
    require(dict(charges) == EXPECTED_CHARGE, "per-degree 77-charge changed")
    require(seen_k9 == old_k9, "new K9 ledger is not byte-key/value equal to retained K9")
    require(len(samples) == 257, "distributed sample census changed")
    for ordinal, row in samples:
        minimum = min(transform_row(row, action) for action in actions)
        require(row == minimum, f"row {ordinal} is not the natural H minimum")

    payload = {
        "status": "PASS_INDEPENDENT_K9_K12_TAIL_ROW_INTERFACE_AUDIT",
        "row_count": total,
        "counts_by_degree": EXPECTED_COUNTS,
        "coefficient_mass_by_degree": EXPECTED_MASS,
        "coefficient_l1_by_degree": EXPECTED_L1,
        "charge_by_degree": EXPECTED_CHARGE,
        "charge_total": sum(EXPECTED_CHARGE.values()),
        "K9_exact_key_value_match": True,
        "distributed_natural_H_minimum_checks": len(samples),
        "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
        "scope": "validates the row input interface only; no filtered continuation, relative solve, or conjecture verdict",
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    audit()
