#!/usr/bin/env python3
"""Replay a positive filtration-ordered p1009 solve on the original interface."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "legacy27_cutoff7_direct.jsonl"
ORDERED = HERE / "legacy27_cutoff7_filtration_ordered.jsonl"
SOLUTION = HERE / "results_cutoff7_filtration_p1009.json"
RESULT = HERE / "results_cutoff7_filtration_p1009_replay.json"
EXPECTED_SOURCE_SHA = (
    "e25b8d81e5b7e7e8170a57322c36decccf404770234a8f9319c34565638cce2c"
)
EXPECTED_ORDERED_SHA = (
    "5251c84d594475153c5ca3939be377376f822dfe158e1e9f7bb14c218b4f392c"
)


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def main() -> None:
    solve = json.loads(SOLUTION.read_text())
    require(solve["prime"] == 1009, "unexpected prime")
    require(solve["target_in_image"],
            "negative result requires an independent left-dual replay")
    coefficients = dict(solve["solution"])

    ordered_hasher = sha256()
    new_to_old = {}
    with ORDERED.open() as handle:
        raw = next(handle)
        ordered_hasher.update(raw.encode("ascii"))
        ordered_header = json.loads(raw)
        for expected, raw in enumerate(handle):
            ordered_hasher.update(raw.encode("ascii"))
            record = json.loads(raw)
            require(record["index"] == expected, "ordered column mismatch")
            new_to_old[expected] = record["source_original_index"]
    require(ordered_hasher.hexdigest() == EXPECTED_ORDERED_SHA,
            "ordered interface SHA changed")
    require(len(set(new_to_old.values())) == ordered_header["column_count"],
            "old-column provenance is not bijective")
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
                require(record["index"] == expected, "source column mismatch")
                for row, multiplicity in record["entries"]:
                    accumulated[row] = (
                        accumulated[row] + value * multiplicity
                    ) % 1009
    require(source_hasher.hexdigest() == EXPECTED_SOURCE_SHA,
            "original interface SHA changed")
    target = [0] * source_header["row_count"]
    for row, numerator, denominator in source_header["target"]:
        target[row] = numerator * pow(denominator, -1, 1009) % 1009
    residual = [(index, (actual - wanted) % 1009)
                for index, (actual, wanted) in enumerate(zip(accumulated, target))
                if actual != wanted]
    require(not residual, f"original-interface residual: {residual[:5]}")

    core = {
        "status": "UNAUDITED modular p1009 discovery; exact-Q replay required",
        "prime": 1009,
        "rank": solve["rank"],
        "target_in_image": True,
        "solution_terms": len(coefficients),
        "original_interface_residual_terms": len(residual),
        "old_column_provenance_bijection_verified": True,
        "source_interface_sha256": source_hasher.hexdigest(),
        "ordered_interface_sha256": ordered_hasher.hexdigest(),
        "modular_solution_sha256": sha256(SOLUTION.read_bytes()).hexdigest(),
    }
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(core, indent=2, sort_keys=True) + "\n")
    print(json.dumps(core, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
