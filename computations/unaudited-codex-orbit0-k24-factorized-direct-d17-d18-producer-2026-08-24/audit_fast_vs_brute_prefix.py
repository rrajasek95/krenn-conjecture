#!/usr/bin/env python3
"""Fail closed on any semantic drift between brute and fibre prefix1."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BRUTE = HERE / "prefix1"
FAST = HERE / "prefix1_fast"
BRUTE_SOURCE = HERE / "run_k24_factorized_direct_d17_d18_brute_prefix1_e7843511.rs"
FAST_SOURCE = HERE / "run_k24_factorized_direct_d17_d18.rs"
VALIDATOR_SOURCE = HERE / "validate_k24_factorized_bounded_result.py"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_validator():
    spec = importlib.util.spec_from_file_location("k24_equiv_validator", VALIDATOR_SOURCE)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, "validator loader")
    spec.loader.exec_module(module)
    return module


def normalized(result):
    value = json.loads(result.read_text())
    value.pop("H_collection_cache")
    value.pop("timings_seconds")
    value["engine_sha256"] = "<engine>"
    for run in value["column_orbit_runs"]:
        run["engine_sha256"] = "<engine>"
    for group in value["groups"]:
        group["content_path"] = Path(group["content_path"]).name
    value["literal_samples"]["path"] = Path(value["literal_samples"]["path"]).name
    return value


def main():
    validator = load_validator()
    brute = validator.validate(BRUTE / "result.json", BRUTE_SOURCE)
    fast = validator.validate(FAST / "result.json", FAST_SOURCE)
    compared = [
        "compact/source_D17_R3_4/final.bin",
        "compact/source_D18_R2_4/final.bin",
        "source_D17_R3_4.columns.tsv",
        "source_D18_R2_4.columns.tsv",
        "literal_witnesses.tsv",
    ]
    for relative in compared:
        require((BRUTE / relative).read_bytes() == (FAST / relative).read_bytes(),
                f"byte drift: {relative}")
    require(normalized(BRUTE / "result.json") == normalized(FAST / "result.json"),
            "normalized result semantic drift")
    brute_seconds = brute["timings_seconds"]["total"]
    fast_seconds = fast["timings_seconds"]["total"]
    print(json.dumps({
        "status": "PASS_FAST_FIBRE_EQUALS_BRUTE_384_PREFIX1",
        "byte_identical_artifacts": compared,
        "normalized_result_semantics_identical": True,
        "excluded_result_fields": ["engine_sha256", "H_collection_cache", "timings_seconds", "artifact directory prefix"],
        "column_orbits_replayed_per_result": 2_165_760,
        "literal_witnesses_byte_identical": 257,
        "brute_total_seconds": brute_seconds,
        "fast_total_seconds": fast_seconds,
        "end_to_end_speedup": brute_seconds / fast_seconds,
        "brute_H_collection_seconds": brute["timings_seconds"]["exact_labelled_merge_and_H_collection"],
        "fast_H_collection_seconds": fast["timings_seconds"]["exact_labelled_merge_and_H_collection"],
        "H_collection_speedup": (brute["timings_seconds"]["exact_labelled_merge_and_H_collection"] /
                                 fast["timings_seconds"]["exact_labelled_merge_and_H_collection"]),
    }, indent=2))


if __name__ == "__main__":
    main()
