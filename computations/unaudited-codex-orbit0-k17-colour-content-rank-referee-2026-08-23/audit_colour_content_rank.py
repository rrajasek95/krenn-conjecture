#!/usr/bin/env python3
"""Provenance, arithmetic, and modular-remainder replay for the rank result."""
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "computations/unaudited-codex-orbit0-filtered-k17-census-2026-08-23"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    result = json.loads((HERE / "results_colour_content_rank.json").read_text())
    if "--mutate" in sys.argv:
        result["results"][0]["rank"] += 1
    require(result["status"] == "PARTIAL_SHELL_TWO_PRIME_RANK", result["status"])
    require((result["coordinates"], result["vectors"], result["vector_nnz"], result["target_nnz"])
            == (16_412, 100_000, 1_019_457, 6_529), result)
    require(result["scope"] == "literal_source_columns", result["scope"])
    pins = {
        "k17_colour_content_first_shell_coordinates.tsv": "10ebfdcf622f0fd04ca7bf05f83f977c7cec81af8921fefb3fbf57b075d2114c",
        "k17_colour_content_first_shell_vectors.tsv": "f642f9b0ab22180919bcde2144bc66e59905cf75f72897af669485a41a68993d",
        "results_k17_colour_content_first_shell.json": "c84949cf56e929c95174d090299b8e3c0d3113c9b2084701eb325a6129d5286b",
    }
    for name, digest in pins.items():
        require(sha256((SOURCE / name).read_bytes()).hexdigest() == digest, name)
    interface = json.loads((HERE / "results_rank_interface.json").read_text())
    require(interface["sha256"]["rank_interface"] ==
            sha256((HERE / "k17_colour_content_first_shell_rank.bin").read_bytes()).hexdigest(), "interface")
    require(interface["target_clear_denominator"] == 6545, interface)

    coordinate_lines = (SOURCE / "k17_colour_content_first_shell_coordinates.tsv").read_text().splitlines()[1:]
    expected = {}
    for line in coordinate_lines:
        ident, _label, numerator, denominator = line.split("\t")
        n, d = int(numerator), int(denominator)
        if n:
            expected[int(ident)] = n * (6545 // d)
    require(len(expected) == 6529, len(expected))
    for record in result["results"]:
        prime = record["prime"]
        require((record["rank"], record["augmented_rank"], record["target_in_span"],
                 record["target_remainder_nnz"]) == (10917, 10918, False, 4612), record)
        lines = (HERE / f"target_remainder_p{prime}.tsv").read_text().splitlines()
        require(lines[0] == "coordinate_id\tresidue", lines[0])
        actual = {int(line.split("\t")[0]): int(line.split("\t")[1]) for line in lines[1:]}
        require(len(actual) == 4612 and all(0 <= coordinate < 16412 and 0 < value < prime
                                           for coordinate, value in actual.items()), prime)
        if "common_support" not in locals():
            common_support = set(actual)
        else:
            require(set(actual) == common_support, "prime-dependent remainder support")
    logical = {key: value for key, value in result.items() if key != "elapsed_seconds"}
    print(json.dumps({"status": "PASS", "logical_sha256": sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
