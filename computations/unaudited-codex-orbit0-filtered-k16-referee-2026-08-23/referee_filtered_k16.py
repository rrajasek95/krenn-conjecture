#!/usr/bin/env python3
"""Streaming exact referee of the bounded filtered K16 run."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import struct


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RUN = ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23"
DIRECT = RUN / "checkpoint_direct_k16.bin"
RESPONSE = RUN / "frozen_k14_k2_response.bin"
REDUCED = RUN / "checkpoint_reduced_k16.bin"
STRUCTURE = RUN / "filtered_k16_structure.bin"
EXPORT_RESULT = RUN / "results_filtered_k16_input_export.json"
RUST_SOURCE = RUN / "run_filtered_k16.rs"
FROZEN_JSON = (ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22"
               / "results_orbit0_k16_literal_residual.json")
DAFSA_SOURCE = (ROOT / "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23"
                / "build_k16_weighted_dafsa.py")
K14_SOURCE = (ROOT / "computations/unaudited-codex-orbit0-k14-interface-audit-2026-08-21"
              / "audit_orbit0_k14_interface.py")
DUAL = (ROOT / "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23"
        / "k16_cycle_partition_dual.tsv")
SIGN_RESULT = (ROOT / "computations/unaudited-codex-orbit0-filtered-k16-sign-referee-2026-08-23"
               / "results_filtered_k16_sign_referee.json")
OUT = HERE / "results_filtered_k16_referee.json"
RECORD = struct.Struct("<24sq")


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


def digest(path):
    state = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def structure():
    data = STRUCTURE.read_bytes()
    p = 11
    nt, nr, np, na = struct.unpack_from("<IIII", data, p)
    p += 16
    require((nt, nr, np, na) == (384, 485, 78, 12), (nt, nr, np, na))
    anchors = data[p:p + 12]
    p += 12 + nt * (252 + 12) + nr * 24
    masks = []
    for _ in range(np):
        vector = data[p:p + 12]
        p += 12
        require(set(vector) <= {0, 1} and sum(vector) == 4, vector)
        masks.append(sum((value != 0) << i for i, value in enumerate(vector)))
    anchor_position = [-1] * 252
    for i, cell in enumerate(anchors):
        anchor_position[cell] = i
    pivotable = [any(support & mask == mask for mask in masks)
                 for support in range(1 << 12)]
    return frozenset(anchors), anchor_position, pivotable


class Reader:
    def __init__(self, path, magic):
        self.handle = path.open("rb")
        require(self.handle.read(8) == magic, (path, "magic"))
        self.count = struct.unpack("<Q", self.handle.read(8))[0]
        self.seen = 0
        self.previous = None

    def next(self):
        if self.seen == self.count:
            require(not self.handle.read(1), "trailing bytes")
            return None
        raw = self.handle.read(RECORD.size)
        require(len(raw) == RECORD.size, "short record")
        row, mass = RECORD.unpack(raw)
        require(mass != 0 and (self.previous is None or self.previous < row),
                (self.previous, row, mass))
        self.previous = row
        self.seen += 1
        return row, mass

    def close(self):
        self.handle.close()


def support_mask(row, positions):
    answer = 0
    for cell in row:
        index = positions[cell]
        if index >= 0:
            answer |= 1 << index
    return answer


def replay_frozen_response():
    dafsa = load("filtered_k16_referee_dafsa", DAFSA_SOURCE)
    response = Reader(RESPONSE, b"K16RESP1")
    records = 0
    for records, expected in enumerate(dafsa.literal_records(FROZEN_JSON), 1):
        actual = response.next()
        require(actual is not None, "response ended early")
        row, numerator, denominator = expected
        require(denominator == 1 and actual == (row, numerator),
                (records, actual, expected))
    require(response.next() is None and records == 1_848_174,
            (records, response.count))
    response.close()
    return records


def replay_combined(positions, pivotable):
    direct = Reader(DIRECT, b"K16DIR1\0")
    response = Reader(RESPONSE, b"K16RESP1")
    reduced = Reader(REDUCED, b"K16RED1\0")
    a, b, expected = direct.next(), response.next(), reduced.next()
    combined_count = combined_sum = combined_l1 = 0
    removed_count = removed_sum = removed_l1 = 0
    kept_count = kept_sum = kept_l1 = 0
    while a is not None or b is not None:
        row = b[0] if a is None else a[0] if b is None else min(a[0], b[0])
        value = 0
        if a is not None and a[0] == row:
            value += a[1]
            a = direct.next()
        if b is not None and b[0] == row:
            # Exact sign referee: actual P response is minus frozen response.
            value -= b[1]
            b = response.next()
        if not value:
            continue
        combined_count += 1
        combined_sum += value
        combined_l1 += abs(value)
        if pivotable[support_mask(row, positions)]:
            removed_count += 1
            removed_sum += value
            removed_l1 += abs(value)
        else:
            require(expected == (row, value),
                    (kept_count, expected, (row, value)))
            expected = reduced.next()
            kept_count += 1
            kept_sum += value
            kept_l1 += abs(value)
    require(expected is None, "reduced checkpoint has extra records")
    direct.close(); response.close(); reduced.close()
    return {
        "direct_records": direct.count,
        "frozen_response_records": response.count,
        "combined": [combined_count, combined_sum, combined_l1],
        "removed_pivotable": [removed_count, removed_sum, removed_l1],
        "reduced": [kept_count, kept_sum, kept_l1],
    }


def load_dual():
    answer = {}
    lines = DUAL.read_text().splitlines()
    require(lines[0] == "cycle_partition\tinteger_coefficient", lines[0])
    for line in lines[1:]:
        partition, coefficient = line.split("\t")
        answer[tuple(map(int, partition.split(",")))] = int(coefficient)
    require(sum(value != 0 for value in answer.values()) == 77, len(answer))
    return answer


def cycle_partition(row, cells):
    adjacency = [[] for _ in range(24)]
    degree = [0] * 24
    for cell in row:
        i, j, a, b = cells[cell]
        u, v = 3 * i + a, 3 * j + b
        adjacency[u].append(v); adjacency[v].append(u)
        degree[u] += 1; degree[v] += 1
    require(set(degree) == {2}, (row.hex(), degree))
    seen = set(); parts = []
    for start in range(24):
        if start in seen:
            continue
        stack = [start]; seen.add(start); size = 0
        while stack:
            u = stack.pop(); size += 1
            for v in adjacency[u]:
                if v not in seen:
                    seen.add(v); stack.append(v)
        parts.append(size)
    return tuple(sorted(parts))


def cycle_charge():
    k14 = load("filtered_k16_referee_k14", K14_SOURCE)
    dual = load_dual()
    reader = Reader(REDUCED, b"K16RED1\0")
    charge = 0
    partition_vector = {}
    while (record := reader.next()) is not None:
        row, mass = record
        partition = cycle_partition(row, k14.FROZEN.BASE.CELLS)
        partition_vector[partition] = partition_vector.get(partition, 0) + mass
        charge += mass * dual.get(partition, 0)
    reader.close()
    partition_vector = {key: value for key, value in partition_vector.items() if value}
    return charge, len(partition_vector)


def main(write_results=False):
    anchors, positions, pivotable = structure()
    require(len(anchors) == 12, anchors)
    sign = json.loads(SIGN_RESULT.read_text())
    require(sign["status"].startswith("EXACT_SIGN_RETRACTION"), sign["status"])
    rust = RUST_SOURCE.read_text()
    require("add(&mut k16,r,-i64::from_le_bytes(vb))" in rust,
            "Rust merge did not subtract frozen response")
    frozen_records = replay_frozen_response()
    combined = replay_combined(positions, pivotable)
    charge, cycle_support = cycle_charge()
    require(combined["reduced"] == [1_941_502, -113_094_144, 1_187_764_512],
            combined["reduced"])
    result = {
        "status": "PASS_EXACT_FILTERED_K16_STREAMING_REFEREE",
        "choice_semantics": {
            "direct_seed": "-R8prime times the K16 (2+2+4 and 2+3+3) E layers",
            "isolated_response": "byte-exact frozen K14-pivot K2 response",
            "sign": "combined = direct - frozen response",
            "K16_projection": (
                "discard exactly rows divisible by one of the 78 mixed K0 anchor heads"
            ),
            "higher_tail_guard": (
                "K16 pivot K18/K19/K20 tails were not emitted; this is only the "
                "completed K16 initial bucket"
            ),
        },
        "frozen_response_byte_replay_records": frozen_records,
        "streaming_combined_replay": combined,
        "reduced_K16": {
            "H_orbits": combined["reduced"][0],
            "signed_orbit_mass": combined["reduced"][1],
            "orbit_mass_L1": combined["reduced"][2],
            "cycle_partition_support": cycle_support,
            "integer_77_cycle_charge": charge,
        },
        "checkpoint_sha256": {
            path.name: digest(path) for path in (DIRECT, RESPONSE, REDUCED, STRUCTURE)
        },
        "source_sha256": {
            str(RUST_SOURCE.relative_to(ROOT)): digest(RUST_SOURCE),
            str(SIGN_RESULT.relative_to(ROOT)): digest(SIGN_RESULT),
            str(DUAL.relative_to(ROOT)): digest(DUAL),
        },
        "scope": (
            "Exact for the chosen orbit-zero H-mass convention through the reduced "
            "K16 bucket. No K17+ state, confluence, ideal membership, or localization."
        ),
    }
    logical = sha256(json.dumps(result, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)
