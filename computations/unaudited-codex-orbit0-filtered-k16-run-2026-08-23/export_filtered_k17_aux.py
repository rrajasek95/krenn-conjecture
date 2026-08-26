#!/usr/bin/env python3
"""Export the exact cover/pivot packets needed by the bounded K17 driver."""

import ast
from hashlib import sha256
import importlib.util
import json
from math import lcm
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = (ROOT / "computations/unaudited-codex-orbit0-filtered-k24-reducer-design-2026-08-23"
          / "filtered_k24_reducer.py")
COVER = (ROOT / "computations/unaudited-codex-orbit0-k14-interface-audit-2026-08-21"
         / "results_k16_anchor_cover.json")
OUT = HERE / "filtered_k17_aux.bin"
CYCLE_OUT = HERE / "filtered_k17_cycle_aux.bin"
CYCLE_DUAL = (ROOT / "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23"
              / "k16_cycle_partition_dual.tsv")
RESULT = HERE / "results_filtered_k17_aux_export.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


D = load("filtered_k17_aux_design", DESIGN)


def main():
    raw = json.loads(COVER.read_text())
    cover = sorted(ast.literal_eval(row) for row in
                   raw["single_pivot_cover"]["minimum_cover_orbit_representatives"])
    assert len(cover) == 25 and all(len(row) == 12 for row in cover)
    masks = [sum((value != 0) << index
                 for index, value in enumerate(vector))
             for vector in D.CTX.vectors]
    pivot_counts = sorted({sum((support & mask) == mask for mask in masks)
                           for support in range(1 << 12)} - {0})
    scale = lcm(*pivot_counts)
    assert scale == 281_801_520
    with OUT.open("wb") as stream:
        stream.write(b"K17AUX1\0")
        stream.write(struct.pack("<QII", scale, len(cover), len(D.CTX.anchors)))
        for signature in cover:
            stream.write(bytes(signature))
        for pivot in range(78):
            stream.write(D.CTX.anchors[pivot])
            for degree, expected in ((2, 12), (3, 32)):
                tails = D.CTX.tails[pivot][degree]
                assert len(tails) == expected
                for tail in tails:
                    stream.write(tail)
    dual_lines = CYCLE_DUAL.read_text().splitlines()
    assert dual_lines[0] == "cycle_partition\tinteger_coefficient"
    with CYCLE_OUT.open("wb") as stream:
        stream.write(b"K17CYC1\0")
        stream.write(bytes(cell for record in D.F.BASE.CELLS for cell in record))
        stream.write(struct.pack("<I", len(dual_lines) - 1))
        for line in dual_lines[1:]:
            key, coefficient = line.split("\t")
            parts = tuple(map(int, key.split(",")))
            assert len(parts) <= 12 and sum(parts) == 24
            stream.write(bytes((len(parts),) + parts + (0,) * (12 - len(parts))))
            stream.write(struct.pack("<q", int(coefficient)))
    result = {
        "status": "PASS exact K17 auxiliary export",
        "global_integer_scale": scale,
        "all_possible_nonzero_pivot_counts": pivot_counts,
        "cover_signatures": len(cover),
        "pivots": 78,
        "K2_tails_per_pivot": 12,
        "K3_tails_per_pivot": 32,
        "aux_sha256": sha256(OUT.read_bytes()).hexdigest(),
        "cycle_aux_sha256": sha256(CYCLE_OUT.read_bytes()).hexdigest(),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
