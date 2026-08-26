#!/usr/bin/env python3
"""Extract the exhaustive zero-provider remainder-coordinate antichain."""
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "remainder_provider_screen.tsv"
OUT = HERE / "zero_mixed_provider_coordinates.tsv"
RESULT = HERE / "results_zero_mixed_provider_coordinates.json"


def main():
    lines = SOURCE.read_text().splitlines()
    if lines[0] != "colour_content_type\ttarget_rows\tdistinct_literal_provider_lower_bound":
        raise RuntimeError(lines[0])
    rows = [line for line in lines[1:] if line.rsplit("\t", 1)[1] == "0"]
    if len(rows) != 40:
        raise RuntimeError(len(rows))
    OUT.write_text(lines[0] + "\n" + "\n".join(rows) + "\n")
    counts = [int(row.split("\t")[1]) for row in rows]
    result = {
        "status": "EXACT_40_ZERO_MIXED_PROVIDER_COORDINATES",
        "coordinates": 40,
        "target_row_count_sum": sum(counts),
        "target_row_count_min": min(counts),
        "target_row_count_max": max(counts),
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "output_sha256": sha256(OUT.read_bytes()).hexdigest(),
        "scope": "all frozen K17 checkpoint rows whose colour-content coordinate is in the 4612-coordinate modular remainder; literal mixed selected-word providers only",
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
