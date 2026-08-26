#!/usr/bin/env python3
"""Enumerate exact normalized two-coordinate relaxations of the sparse chart."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import os
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load(name):
    path = HERE / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalize(text, first, second, base):
    names = {first: "extra0", second: "extra1"}
    pattern = re.compile(r"\b(?:" + "|".join(map(re.escape, names)) + r")\b")
    answer = pattern.sub(lambda match: names[match.group(0)], text)
    lines = answer.splitlines()
    expected = f"ring r=0,({','.join(sorted(set(base) | {'extra0', 'extra1'}))}),dp;"
    for index, line in enumerate(lines):
        if line.startswith("ring r=0,"):
            lines[index] = expected
            break
    else:
        raise AssertionError("ring absent")
    return "\n".join(lines) + "\n"


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def main():
    generator = load("generate_sparse_pair01.py")
    core = generator.load_core()
    all_variables = set(core.SOURCE.values()) | set(core.U) | set(core.V)
    zero = sorted(all_variables - generator.BASE_LIVE)
    assert len(zero) == 70
    groups = {}
    pair_records = []
    retained_inputs = set()
    for pair_index, (first, second) in enumerate(itertools.combinations(zero, 2)):
        label = f"pair_{pair_index:04d}"
        generated = generator.build(generator.BASE_LIVE | {first, second}, label)
        path = HERE / generated["path"]
        text = path.read_text()
        forward = normalize(text, first, second, generator.BASE_LIVE)
        reverse = normalize(text, second, first, generator.BASE_LIVE)
        canonical = min(forward, reverse)
        digest = sha(canonical)
        pair = [first, second]
        pair_records.append({"pair": pair, "normalized_sha256": digest})
        if digest not in groups:
            groups[digest] = {
                "normalized_sha256": digest,
                "representative": pair,
                "input": generated["path"],
                "input_sha256": generated["sha256"],
                "members": [],
            }
            retained_inputs.add(path)
        groups[digest]["members"].append(pair)
        if path not in retained_inputs:
            path.unlink()
    result = {
        "schema": "KRENN_X5_REP2_SPARSE_DOUBLE_RELAXATION_LEDGER_V1",
        "status": "PASS_ALL_DOUBLE_COORDINATES_NORMALIZED",
        "zero_coordinate_count": len(zero),
        "pair_count": len(pair_records),
        "normalized_group_count": len(groups),
        "groups": sorted(groups.values(), key=lambda item: item["normalized_sha256"]),
        "pair_records": pair_records,
        "normalization": "minimum of the two exact programs after extra-coordinate renaming and canonical ring declaration",
        "scope": "base17 plus exactly two amplitude coordinates; no guard/adjoint/incidence/rank assertions",
    }
    output = HERE / "double_relaxation_ledger.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps({
        "pairs": len(pair_records),
        "normalized_groups": len(groups),
        "retained_inputs": len(retained_inputs),
        "largest_group": max(len(item["members"]) for item in groups.values()),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
