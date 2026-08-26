#!/usr/bin/env python3
"""Enumerate all C(70,3) sparse charts and retain one canonical program/group."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import os
import re
import statistics
import tempfile
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT = ROOT / "computations/unaudited-codex-n8-x5-rep2-sparse-pair01-boundary-2026-08-25"
PINS = {
    PARENT / "MANIFEST.sha256": "52c4900fab9799096f4967dc04eaba223c36d640d787a87a5708652b2d187ee8",
    PARENT / "generate_sparse_pair01.py": "635049c3df63a3a078c1b03a0e99c20867e97acf3ce8c405d0641715242b42b9",
    PARENT / "results_double_search.json": "abdc997b6fb601b0d046226a51ff70752495f908bd4600a287505e8e7af59a94",
    PARENT / "single_relaxation_ledger.json": "0ccd1d583721d5a7fb9546acedff13e7405d2eacbb4117e65c0af8fe26c84fff",
}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalize(text, extras, base):
    candidates = []
    pattern = re.compile(r"\b(?:" + "|".join(map(re.escape, extras)) + r")\b")
    for ordering in itertools.permutations(extras):
        names = {name: f"extra{index}" for index, name in enumerate(ordering)}
        answer = pattern.sub(lambda match: names[match.group(0)], text)
        lines = answer.splitlines()
        expected = f"ring r=0,({','.join(sorted(set(base) | set(names.values())))}),dp;"
        for index, line in enumerate(lines):
            if line.startswith("ring r=0,"):
                lines[index] = expected
                break
        else:
            raise AssertionError("ring absent")
        candidates.append("\n".join(lines) + "\n")
    return min(candidates)


def atomic_write(path, text):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text)
    os.replace(temporary, path)


def main():
    assert __debug__
    for path, digest in PINS.items():
        assert sha256(path) == digest, path
    generator = load(PARENT / "generate_sparse_pair01.py")
    singles = json.loads((PARENT / "single_relaxation_ledger.json").read_text())
    zero = sorted(item["extra"] for item in singles["records"])
    assert len(zero) == 70 and len(set(zero)) == 70
    triples = list(itertools.combinations(zero, 3))
    assert len(triples) == 54740
    groups = {}
    triple_records = []
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="rep2_triple_enum_") as temporary_directory:
        original_here = generator.HERE
        generator.HERE = Path(temporary_directory)
        try:
            for index, triple in enumerate(triples):
                generated = generator.build(generator.BASE_LIVE | set(triple), f"triple_{index}")
                raw = (generator.HERE / generated["path"]).read_text()
                canonical = normalize(raw, triple, generator.BASE_LIVE)
                digest = hashlib.sha256(canonical.encode()).hexdigest()
                triple_records.append({"triple": list(triple), "normalized_sha256": digest})
                if digest not in groups:
                    group_index = len(groups)
                    canonical_path = HERE / f"group_{group_index:05d}_{digest[:16]}.sing"
                    atomic_write(canonical_path, canonical)
                    groups[digest] = {
                        "normalized_sha256": digest,
                        "representative": list(triple),
                        "canonical_input": canonical_path.name,
                        "canonical_input_sha256": sha256(canonical_path),
                        "canonical_input_bytes": canonical_path.stat().st_size,
                        "members": [],
                    }
                groups[digest]["members"].append(list(triple))
        finally:
            generator.HERE = original_here
    enumeration_wall = time.monotonic() - started
    group_list = sorted(groups.values(), key=lambda item: item["normalized_sha256"])
    total_bytes = sum(item["canonical_input_bytes"] for item in group_list)

    double = json.loads((PARENT / "results_double_search.json").read_text())
    timings = [item["wall_seconds"] for item in double["attempts"]]
    assert len(timings) == 381 and all(item["status"] == "UNIT_IDEAL" for item in double["attempts"])
    mean = statistics.mean(timings)
    median = statistics.median(timings)
    maximum = max(timings)
    projected_mean = mean * len(group_list)
    projected_conservative = min(maximum * len(group_list), mean * 2 * len(group_list))
    result = {
        "schema": "KRENN_X5_REP2_SPARSE_TRIPLE_NORMALIZATION_LEDGER_V1",
        "status": "PASS_ENUMERATION_ONLY_NO_IDEALS_RUN",
        "pins": {str(path): digest for path, digest in PINS.items()},
        "zero_coordinate_count": len(zero),
        "raw_triple_count": len(triples),
        "normalized_group_count": len(group_list),
        "enumeration_wall_seconds": enumeration_wall,
        "canonical_input_total_bytes": total_bytes,
        "canonical_input_max_bytes": max(item["canonical_input_bytes"] for item in group_list),
        "groups": group_list,
        "triple_records": triple_records,
        "projection_from_double_gate": {
            "double_group_count": len(timings),
            "double_total_wall_seconds": sum(timings),
            "per_group_mean_seconds": mean,
            "per_group_median_seconds": median,
            "per_group_max_seconds": maximum,
            "projected_triple_mean_seconds": projected_mean,
            "projected_triple_conservative_seconds": projected_conservative,
            "projected_under_15_minutes": projected_conservative <= 900,
        },
        "launch_gate": {
            "group_count_at_most_10000": len(group_list) <= 10000,
            "projected_wall_at_most_15_minutes": projected_conservative <= 900,
            "ready_under_requested_gate": len(group_list) <= 10000 and projected_conservative <= 900,
            "no_ideals_launched": True,
        },
        "prior_388_monomial_triples": "diagnostic noncoverage only; not imported into group outcomes",
        "normalization": "lexicographic minimum of all six exact new-variable renamings with canonical ring declaration",
        "scope": "full 257 pair01 amplitudes on base17 plus exactly three coordinates; no guard/adjoint/incidence/rank",
    }
    output = HERE / "triple_group_ledger.json"
    atomic_write(output, json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "raw_triples": len(triples),
        "groups": len(group_list),
        "input_bytes": total_bytes,
        "enumeration_wall": enumeration_wall,
        "projected_mean": projected_mean,
        "projected_conservative": projected_conservative,
        "ready": result["launch_gate"]["ready_under_requested_gate"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
