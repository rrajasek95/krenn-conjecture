#!/usr/bin/env python3
"""Replay the reordered chart26 solution on the frozen original interface."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
RUST = HERE.parent / "unaudited-codex-anchor-k-rust-2026-08-20"
SOURCE = RUST / "results_chart26_cutoff7_direct.jsonl"
REFERENCE = RUST / "results_chart26_cutoff7_solution_p1009.json"
ORDERED = HERE / "chart26_cutoff7_filtration_ordered_control.jsonl"
SOLUTION = HERE / "results_chart26_filtration_ordered_p1009.json"
RESULT = HERE / "results_chart26_filtration_reorder_invariance.json"


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def main() -> None:
    solve = json.loads(SOLUTION.read_text())
    reference = json.loads(REFERENCE.read_text())
    prime = solve["prime"]
    require(prime == reference["prime"] == 1009, "prime mismatch")
    coefficients = dict(solve["solution"])

    new_to_old = {}
    ordered_hasher = sha256()
    with ORDERED.open() as handle:
        raw = next(handle)
        ordered_hasher.update(raw.encode("ascii"))
        ordered_header = json.loads(raw)
        for expected, raw in enumerate(handle):
            ordered_hasher.update(raw.encode("ascii"))
            record = json.loads(raw)
            require(record["index"] == expected, "ordered index mismatch")
            new_to_old[expected] = record["source_original_index"]

    require(len(set(new_to_old.values())) == ordered_header["column_count"],
            "old provenance is not bijective")
    old_coefficients = {new_to_old[index]: value
                        for index, value in coefficients.items()}

    source_hasher = sha256()
    with SOURCE.open() as handle:
        raw = next(handle)
        source_hasher.update(raw.encode("ascii"))
        source_header = json.loads(raw)
        accumulated = [0] * source_header["row_count"]
        for expected, raw in enumerate(handle):
            source_hasher.update(raw.encode("ascii"))
            value = old_coefficients.get(expected, 0)
            if value:
                record = json.loads(raw)
                require(record["index"] == expected, "source index mismatch")
                for row, multiplicity in record["entries"]:
                    accumulated[row] = (
                        accumulated[row] + value * multiplicity
                    ) % prime

    target = [0] * source_header["row_count"]
    for row, numerator, denominator in source_header["target"]:
        target[row] = numerator * pow(denominator, -1, prime) % prime
    residual = [(index, (actual - wanted) % prime)
                for index, (actual, wanted) in enumerate(zip(accumulated, target))
                if actual != wanted]
    require(not residual, f"original-interface replay failed: {residual[:5]}")
    require(solve["rank"] == reference["rank"], "rank changed")
    require(solve["target_in_image"] == reference["target_in_image"],
            "target membership changed")

    core = {
        "status": "UNAUDITED exact-integer interface permutation; modular solve only",
        "prime": prime,
        "reference_rank": reference["rank"],
        "ordered_rank": solve["rank"],
        "reference_target_in_image": reference["target_in_image"],
        "ordered_target_in_image": solve["target_in_image"],
        "ordered_solution_terms": len(coefficients),
        "ordered_solution_original_interface_residual_terms": len(residual),
        "source_interface_sha256": source_hasher.hexdigest(),
        "ordered_interface_sha256": ordered_hasher.hexdigest(),
        "ordered_solution_sha256": sha256(SOLUTION.read_bytes()).hexdigest(),
        "rank_invariant": True,
        "target_membership_invariant": True,
        "old_column_provenance_replay_passed": True,
    }
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(core, indent=2, sort_keys=True) + "\n")
    print(json.dumps(core, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
