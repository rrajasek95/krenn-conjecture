#!/usr/bin/env python3
"""Export compact, source-replayed inputs for the bounded Rust K16 run."""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = (ROOT / "computations/unaudited-codex-orbit0-filtered-k24-reducer-design-2026-08-23"
          / "filtered_k24_reducer.py")
FROZEN = (ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22"
          / "results_orbit0_k16_literal_residual.json")
STRUCTURE = HERE / "filtered_k16_structure.bin"
RESPONSE = HERE / "frozen_k14_k2_response.bin"
RESULT = HERE / "results_filtered_k16_input_export.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


D = load("filtered_k16_input_design", DESIGN)


def main():
    records = D.r8_h_records()
    assert len(records) == 485
    assert all(coefficient.denominator == 1
               for _row, _size, coefficient in records)
    with STRUCTURE.open("wb") as out:
        out.write(b"K16DIRECT1\0")
        out.write(struct.pack("<IIII", len(D.H), len(records), 78, 12))
        out.write(bytes(D.CTX.anchor_cells))
        for action in D.H:
            transform = D.F.EXPORT.TRANSFORMS[action]
            out.write(bytes(transform))
            permutation = D.CTX.signature_permutations[action]
            out.write(bytes(permutation))
        for row, orbit_size, coefficient in records:
            assert len(row) == 12
            out.write(row)
            out.write(struct.pack("<Iq", orbit_size, coefficient.numerator))
        for pivot in range(78):
            out.write(bytes(D.CTX.vectors[pivot]))
        factor_words = tuple(D.F.word_from_pair_colours(row)
                             for row in D.F.PAIR_COLOURS)
        factor_pivots = tuple(D.CTX.anchor_to_pivot[
            D.F.BASE.term_ids(word, D.F.M0)] for word in factor_words)
        for family in factor_pivots:
            for degree in (2, 3, 4):
                tails = D.CTX.tails[family][degree]
                out.write(struct.pack("<I", len(tails)))
                for tail in tails:
                    out.write(tail)

    frozen = json.loads(FROZEN.read_text())
    assert frozen["logical_sha256"] == "8eb9f7dbb220afd759533c10a4881a502a43bdb3bfa28c36e3b89cf98a4ee58c"
    with RESPONSE.open("wb") as out:
        out.write(b"K16RESP1")
        out.write(struct.pack("<Q", len(frozen["literal_orbits"])))
        for row_hex, numerator, denominator in frozen["literal_orbits"]:
            assert denominator == 1
            row = bytes.fromhex(row_hex)
            assert len(row) == 24
            out.write(row)
            out.write(struct.pack("<q", numerator))

    result = {
        "status": "PASS compact filtered-K16 input export",
        "R8prime_H_slices": len(records),
        "frozen_response_H_orbits": len(frozen["literal_orbits"]),
        "structure_sha256": sha256(STRUCTURE.read_bytes()).hexdigest(),
        "response_sha256": sha256(RESPONSE.read_bytes()).hexdigest(),
        "frozen_response_byte_sha256": sha256(FROZEN.read_bytes()).hexdigest(),
        "frozen_response_logical_sha256": frozen["logical_sha256"],
        "direct_K14_terms_per_slice": 1728,
        "direct_K15_terms_per_slice": 13824,
        "direct_K16_terms_per_slice": 62784,
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
