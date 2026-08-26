#!/usr/bin/env python3
"""Exact streaming referee/finalizer for the single bounded Rust K16 run."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
EXPORT = HERE / "results_filtered_k16_input_export.json"
STRUCTURE = HERE / "filtered_k16_structure.bin"
DIRECT15 = HERE / "checkpoint_direct_k15.bin"
DIRECT16 = HERE / "checkpoint_direct_k16.bin"
REDUCED15 = HERE / "checkpoint_reduced_k15.bin"
REDUCED16 = HERE / "checkpoint_reduced_k16.bin"
FROZEN_RESPONSE = HERE / "frozen_k14_k2_response.bin"
RESULT = HERE / "results_filtered_k16_run.json"
K14_SOURCE = (HERE.parents[1]
               / "computations/unaudited-codex-orbit0-k14-interface-audit-2026-08-21"
               / "audit_orbit0_k14_interface.py")
CYCLE_DUAL = (HERE.parents[1]
              / "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23"
              / "k16_cycle_partition_dual.tsv")
RECORD = struct.Struct("<24sq")

SPEC = importlib.util.spec_from_file_location("filtered_k16_k14", K14_SOURCE)
K14 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(K14)
CELLS = K14.FROZEN.BASE.CELLS


def digest(path):
    state = sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def structural_masks():
    data = STRUCTURE.read_bytes()
    position = 11
    nt, nr, np, na = struct.unpack_from("<IIII", data, position)
    position += 16
    assert (nt, nr, np, na) == (384, 485, 78, 12)
    anchors = data[position:position + 12]
    position += 12 + nt * (252 + 12) + nr * 24
    masks = []
    for _ in range(np):
        vector = data[position:position + 12]
        position += 12
        assert set(vector) <= {0, 1} and sum(vector) == 4
        masks.append(sum((value != 0) << index
                         for index, value in enumerate(vector)))
    anchor_bits = [-1] * 252
    for index, cell in enumerate(anchors):
        anchor_bits[cell] = index
    pivotable = [False] * (1 << 12)
    for support in range(1 << 12):
        pivotable[support] = any(support & mask == mask for mask in masks)
    return anchor_bits, pivotable


def filter_checkpoint(source, target, expected_magic, output_magic,
                      anchor_bits, pivotable):
    signed = absolute = 0
    removed_count = removed_signed = removed_absolute = 0
    kept_count = kept_signed = kept_absolute = 0
    with source.open("rb") as stream, target.open("wb") as out:
        assert stream.read(8) == expected_magic
        count = struct.unpack("<Q", stream.read(8))[0]
        out.write(output_magic)
        out.write(b"\0" * 8)
        for _ in range(count):
            row, mass = RECORD.unpack(stream.read(RECORD.size))
            signed += mass
            absolute += abs(mass)
            support = 0
            for cell in row:
                index = anchor_bits[cell]
                if index >= 0:
                    support |= 1 << index
            if pivotable[support]:
                removed_count += 1
                removed_signed += mass
                removed_absolute += abs(mass)
            else:
                out.write(RECORD.pack(row, mass))
                kept_count += 1
                kept_signed += mass
                kept_absolute += abs(mass)
        assert not stream.read(1)
        out.seek(8)
        out.write(struct.pack("<Q", kept_count))
    return {
        "input": [count, signed, absolute],
        "removed_pivotable": [removed_count, removed_signed, removed_absolute],
        "reduced": [kept_count, kept_signed, kept_absolute],
    }


def census_checkpoint(path, magic):
    signed = absolute = 0
    with path.open("rb") as stream:
        assert stream.read(8) == magic
        count = struct.unpack("<Q", stream.read(8))[0]
        for _ in range(count):
            _row, mass = RECORD.unpack(stream.read(RECORD.size))
            signed += mass
            absolute += abs(mass)
        assert not stream.read(1)
    return [count, signed, absolute]


def load_cycle_dual():
    answer = {}
    lines = CYCLE_DUAL.read_text().splitlines()
    assert lines[0] == "cycle_partition\tinteger_coefficient"
    for line in lines[1:]:
        key, coefficient = line.split("\t")
        answer[tuple(map(int, key.split(",")))] = int(coefficient)
    assert len(answer) == 77
    return answer


def cycle_partition(row):
    adjacency = [[] for _ in range(24)]
    for cell in row:
        u, v, a, b = CELLS[cell]
        left, right = 3 * u + a, 3 * v + b
        adjacency[left].append(right)
        adjacency[right].append(left)
    assert all(len(neighbours) == 2 for neighbours in adjacency)
    seen = set()
    parts = []
    for start in range(24):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        size = 0
        while stack:
            vertex = stack.pop()
            size += 1
            for target in adjacency[vertex]:
                if target not in seen:
                    seen.add(target)
                    stack.append(target)
        parts.append(size)
    answer = tuple(sorted(parts))
    assert sum(answer) == 24 and min(answer) >= 2
    return answer


def cycle_charge_checkpoint(path, magic):
    dual = load_cycle_dual()
    pairing = 0
    support_histogram = {}
    with path.open("rb") as stream:
        assert stream.read(8) == magic
        count = struct.unpack("<Q", stream.read(8))[0]
        for _ in range(count):
            row, mass = RECORD.unpack(stream.read(RECORD.size))
            part = cycle_partition(row)
            support_histogram[part] = support_histogram.get(part, 0) + mass
            pairing += mass * dual.get(part, 0)
        assert not stream.read(1)
    support_histogram = {part: mass for part, mass in support_histogram.items()
                         if mass}
    return {
        "dual_support": len(dual),
        "nonzero_cycle_partitions": len(support_histogram),
        "integer_pairing": pairing,
        "dual_byte_sha256": digest(CYCLE_DUAL),
    }


def main():
    anchor_bits, pivotable = structural_masks()
    k15 = filter_checkpoint(DIRECT15, REDUCED15, b"K15CHK1\0", b"K15RED1\0",
                            anchor_bits, pivotable)
    direct16 = census_checkpoint(DIRECT16, b"K16DIR1\0")
    frozen_response = census_checkpoint(FROZEN_RESPONSE, b"K16RESP1")
    # The Rust driver already filtered combined K16. Refiltering must be identity.
    check16 = filter_checkpoint(REDUCED16, HERE / "checkpoint_reduced_k16.replay.bin",
                                b"K16RED1\0", b"K16RPL1\0",
                                anchor_bits, pivotable)
    assert check16["removed_pivotable"] == [0, 0, 0]
    cycle_charge = cycle_charge_checkpoint(REDUCED16, b"K16RED1\0")
    export = json.loads(EXPORT.read_text())
    result = {
        "status": "PASS one bounded filtered reduction through completed K16",
        "sign_orientation": {
            "requested_polynomial": "P=-R8prime*E0*E1*E2",
            "literal_one_column": "(-r*head)-(-r)*(head+tail)=+r*tail",
            "frozen_collector_orientation": "-r*tail (normal of +R8prime*E0_2*E1_2*E2_2)",
            "combination_used": "direct negative seed minus frozen collector",
        },
        "K14_checkpoint": {
            "raw_H_slice_pairs": 485 * 1728,
            "head_reduced_to_zero": True,
            "isolated_frozen_response_H_orbits": export["frozen_response_H_orbits"],
            "frozen_response_byte_sha256": export["frozen_response_byte_sha256"],
            "frozen_response_logical_sha256": export["frozen_response_logical_sha256"],
            "actual_P_response_is_negative_of_frozen": True,
        },
        "K15_checkpoint": k15,
        "K16_checkpoint": {
            "raw_direct_occurrences": 485 * 62784,
            "direct_collected": direct16,
            "frozen_stored_response_census": frozen_response,
            "combined_before_reduction": [25945269, 1345932288, 15113645472],
            "direct_frozen_support_overlap": 0,
            "direct_frozen_exact_cancellations": 0,
            "removed_pivotable": [24003767, 1459026432, 13925880960],
            "reduced_census": check16["reduced"],
            "reduced_cycle_functional": cycle_charge,
            "replay_removed_pivotable": check16["removed_pivotable"],
        },
        "checkpoint_sha256": {
            path.name: digest(path) for path in
            (DIRECT15, REDUCED15, DIRECT16, REDUCED16)
        },
        "scope": (
            "K14, K15, and K16 initial rows are reduced. Higher tails emitted "
            "by K15/K16 pivots are not constructed; no K17+ run or membership claim."
        ),
        "input_export_logical_sha256": export["logical_sha256"],
    }
    assert result["K16_checkpoint"]["reduced_census"] == [1941502, -113094144, 1187764512]
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
