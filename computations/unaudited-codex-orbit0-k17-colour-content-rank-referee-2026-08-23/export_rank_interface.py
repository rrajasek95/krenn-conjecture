#!/usr/bin/env python3
"""Convert Tail's literal first-shell TSVs to the independent rank schema."""
from hashlib import sha256
from math import lcm
from pathlib import Path
import json
import struct

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "computations/unaudited-codex-orbit0-filtered-k17-census-2026-08-23"
COORDS = SOURCE / "k17_colour_content_first_shell_coordinates.tsv"
VECTORS = SOURCE / "k17_colour_content_first_shell_vectors.tsv"
SOURCE_RESULT = SOURCE / "results_k17_colour_content_first_shell.json"
OUT = HERE / "k17_colour_content_first_shell_rank.bin"
RESULT = HERE / "results_rank_interface.json"
LIMIT = 100_000


def main():
    source_result = json.loads(SOURCE_RESULT.read_text())
    coordinate_lines = COORDS.read_text().splitlines()
    assert coordinate_lines[0] == "coordinate_id\tcolour_content_type\ttarget_numerator\ttarget_denominator"
    coordinates = []
    scale = 1
    for expected, line in enumerate(coordinate_lines[1:]):
        ident, label, numerator, denominator = line.split("\t")
        assert int(ident) == expected and label
        n, d = int(numerator), int(denominator)
        assert d > 0
        scale = lcm(scale, d)
        coordinates.append((n, d))
    vector_lines = VECTORS.read_text().splitlines()
    assert vector_lines[0] == "vector_id\tsparse_integer_vector"
    assert len(coordinates) <= LIMIT and len(vector_lines) - 1 <= LIMIT
    vectors = []
    for expected, line in enumerate(vector_lines[1:]):
        ident, sparse = line.split("\t")
        assert int(ident) == expected
        entries = [] if not sparse else [tuple(map(int, item.split(":"))) for item in sparse.split(",")]
        assert all(0 <= c < len(coordinates) and v != 0 for c, v in entries)
        assert all(entries[i][0] < entries[i + 1][0] for i in range(len(entries) - 1))
        vectors.append(entries)
    target = [(i, n * (scale // d)) for i, (n, d) in enumerate(coordinates) if n]
    assert all(-(1 << 63) <= v < (1 << 63) for _, v in target)

    payload = bytearray(b"K17CCR1\0")
    payload.extend(struct.pack("<III", 1, len(coordinates), len(vectors)))

    def emit(entries):
        payload.extend(struct.pack("<I", len(entries)))
        for coordinate, value in entries:
            payload.extend(struct.pack("<Iq", coordinate, value))

    emit(target)
    for vector in vectors:
        emit(vector)
    OUT.write_bytes(payload)
    result = {
        "schema": "K17CCR1 literal-source-v1",
        "scope": "literal_source_columns",
        "coordinates": len(coordinates),
        "vectors": len(vectors),
        "target_nnz": len(target),
        "target_clear_denominator": scale,
        "vector_nnz": sum(map(len, vectors)),
        "input_status": source_result["status"],
        "input_terminal": source_result["terminal"],
        "sha256": {
            "coordinates": sha256(COORDS.read_bytes()).hexdigest(),
            "vectors": sha256(VECTORS.read_bytes()).hexdigest(),
            "source_result": sha256(SOURCE_RESULT.read_bytes()).hexdigest(),
            "rank_interface": sha256(payload).hexdigest(),
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
