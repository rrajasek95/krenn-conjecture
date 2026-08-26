#!/usr/bin/env python3
"""Export the audited second-page cache to a fixed-width Rust input.

The expensive third-page computation only needs canonical 24-port matchings,
modular kernel coordinates, and the seven critical tails.  Keeping this
exporter deliberately simple makes Python a serialization/reference layer;
all incidence closure and linear algebra live in the Rust checker.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import pickle
import struct
from pathlib import Path


HERE = Path(__file__).resolve().parent
CACHE = HERE / "second_bockstein_state_p1009.pkl"
SECOND_PATH = HERE / "audit_seven_critical_second_bockstein.py"
SOURCE_PATH = HERE.parent / "analyze_n8_full_s8s3_pure_product_membership.py"
OUT = HERE / "third_bockstein_p1009.rbin"
PRIME = 1009


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load_module("n8_orbit_source", SOURCE_PATH)


def u32(handle, value):
    handle.write(struct.pack("<I", value))


def u16(handle, value):
    handle.write(struct.pack("<H", value))


def key(handle, canonical_key):
    mate = SOURCE.decode_key(canonical_key)
    if len(mate) != 24 or any(not -1 <= value <= 23 for value in mate):
        raise RuntimeError("invalid canonical matching key")
    handle.write(struct.pack("<24b", *mate))


def key_list(handle, values):
    values = tuple(values)
    u32(handle, len(values))
    for value in values:
        key(handle, value)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()

    payload = pickle.loads(CACHE.read_bytes())
    if payload["prime"] != PRIME:
        raise RuntimeError("cache prime changed")
    expected = hashlib.sha256(SECOND_PATH.read_bytes()).hexdigest()
    if payload["second_script_sha256"] != expected:
        raise RuntimeError("cache was made by a different second-page script")
    state = payload["state"]

    support = tuple(state["support_columns"])
    first = tuple(state["first_columns"])
    second = tuple(state["second_columns"])
    used = tuple(sorted(set(support) | set(first) | set(second)))
    third_rows = tuple(sorted(state["third_rows"]))
    kernels = tuple(state["second_correction_kernels"])
    tails = tuple(state["third_tails"])

    with args.output.open("wb") as handle:
        handle.write(b"BCK3R002")
        u32(handle, PRIME)
        key_list(handle, used)
        key_list(handle, second)
        key_list(handle, third_rows)
        old_rows = tuple(sorted(
            set(state["target_set"])
            | set(state["first_set"])
            | set(state["second_set"])
            | set(state["third_rows"])
        ))
        key_list(handle, old_rows)

        u32(handle, len(kernels))
        for vector in kernels:
            items = tuple(sorted(vector.items()))
            u32(handle, len(items))
            for index, coefficient in items:
                u32(handle, index)
                u16(handle, coefficient % PRIME)

        u32(handle, len(tails))
        for vector in tails:
            items = tuple(sorted(vector.items()))
            u32(handle, len(items))
            for row, coefficient in items:
                key(handle, row)
                u16(handle, coefficient % PRIME)

        # Literal cross-language controls.  Rust must reproduce both maps
        # byte-for-byte before it is allowed to run the full computation.
        control_columns = second[:12]
        u32(handle, len(control_columns))
        for column in control_columns:
            key(handle, column)
            outputs = tuple(SOURCE.column_outputs(column))
            key_list(handle, outputs)

        control_rows = third_rows[:12]
        u32(handle, len(control_rows))
        for row in control_rows:
            key(handle, row)
            columns = tuple(sorted(SOURCE.incident_columns(row)))
            key_list(handle, columns)

    print(f"output: {args.output}")
    print(f"bytes: {args.output.stat().st_size}")
    print(f"used_columns: {len(used)}")
    print(f"second_columns: {len(second)}")
    print(f"third_rows: {len(third_rows)}")
    print(f"old_rows: {len(old_rows)}")
    print(f"second_kernels: {len(kernels)}")
    print(f"third_tail_terms: {tuple(map(len, tails))}")


if __name__ == "__main__":
    main()
