#!/usr/bin/env python3
"""Fail-closed validator for the exact K9--K12 omitted-tail charge result."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


EXPECTED_CHARGES = {
    "target": {"9": 245760, "10": -1170432, "11": 331776, "12": 13824},
    "source": {"9": 19055616, "10": -16093440, "11": 3313152, "12": -2290176},
    "tail_target_minus_source": {"9": -18809856, "10": 14923008, "11": -2981376, "12": 2304000},
    "K10_through_K12_subtotal": 14245632,
    "K9_through_K12_total": -4564224,
    "expected_missing_correction_charge": -4564224,
    "retained_K9_quotient_pairing": -18809856,
}
EXPECTED_COUNTS = {
    "source_terms": 9607,
    "source_actions_in_seed": 2304,
    "perfect_matchings_per_H_word": 105,
    "target_literal_emissions": {"9": 171008, "10": 313920, "11": 345600, "12": 216000},
    "source_literal_emissions": {"9": 92410, "10": 272332, "11": 350472, "12": 249840},
    "source_firing_terms": {"9": 5308, "10": 9238, "11": 7522, "12": 4164},
}
EXPECTED_PINS = {
    "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23/k16_cycle_partition_dual.tsv": "fea91d03250128fa6ea99252659ddd2b46329a9318916a19d6dae0ecfb69dd84",
    "computations/unaudited-codex-orbit0-t2-radical-2026-08-20/results_anchor_times_e9_cutoff10_seed.json": "8106f094ba796f124f80213d019420a9df469a8ced8e72b4d37a493b6da23ba9",
    "computations/unaudited-codex-orbit0-t2-radical-2026-08-20/results_sparse_r8_k9_tail.json": "6b85cca58d6da26f426404eb785b2d9bf7858a4c758a651e1e9aa66729b08132",
    "computations/unaudited-codex-orbit0-t2-radical-2026-08-20/sparse_r8_k9_tail_terms.txt": "b572b774d3d50d2618aa2d79338681fcf80542bf19ddd6e319037f9432aab74b",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate(path: Path) -> dict:
    data = json.loads(path.read_text())
    require(data["status"] == "PASS_EXACT_BOUNDED_K9_THROUGH_K12_LITERAL_CHARGE", "bad status")
    require(data["charges"] == EXPECTED_CHARGES, "charge ledger changed")
    require(data["counts"] == EXPECTED_COUNTS, "count ledger changed")
    require(data["pins"] == EXPECTED_PINS, "input pins changed")
    require(data["scope"].endswith("no row reduction or broad continuation"), "scope guard changed")
    logical = dict(data)
    logical.pop("elapsed_seconds")
    claimed = logical.pop("logical_sha256")
    digest = hashlib.sha256(json.dumps(logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    require(claimed == digest, "logical hash mismatch")
    require(digest == "e18048edf346a8d6516f817bb820a9f26df6c5633cee9b594520b498c8c638b6", "unexpected logical result")
    return {
        "status": "PASS_STRICT_K9_THROUGH_K12_TAIL_CHARGE_VALIDATION",
        "result_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "logical_sha256": digest,
        "verified_total": data["charges"]["K9_through_K12_total"],
        "scope": "validates the bounded scalar replay only; no row continuation, membership, or conjecture verdict",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        audit = validate(args.result)
    except Exception as exc:
        print(f"REJECT: {exc}", file=sys.stderr)
        raise SystemExit(2)
    text = json.dumps(audit, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
