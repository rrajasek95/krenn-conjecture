#!/usr/bin/env python3
"""Factor the forced pure anchor square and collect literal collisions.

Every post-unary R8'² block has exactly two copies of the four anchor cells
of one colour.  Normalize that colour to zero, divide by the common factor,
and collect identical sixteen-edge residual rows before the remaining
768-action canonicalization.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
EXPORT_PATH = BRIDGE / "export_orbit0_cutoff_seed.py"
SPEC = importlib.util.spec_from_file_location("orbit0_export", EXPORT_PATH)
EXPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPORT)
BASE = EXPORT.BASE
SOURCE = HERE / "r8prime_square_post_unary_blocks.jsonl"
STREAM = HERE / "r8prime_square_pure_anchor_factored_raw.jsonl"
OUT = HERE / "results_r8prime_square_pure_anchor_factored_raw.json"


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def anchor_factor(colour):
    return bytes(sorted(BASE.CELL_ID[(left, right, colour, colour)]
                        for left, right in EXPORT.M0 for _ in range(2)))


def subtract_factor(row, factor):
    residual = Counter(row)
    residual.subtract(factor)
    require(all(value >= 0 for value in residual.values()),
            "pure anchor square does not divide survivor")
    return bytes(sorted(cell for cell, value in residual.items()
                        for _ in range(value)))


def survivor_colour(row):
    factors = [anchor_factor(colour) for colour in BASE.COLORS]
    matches = [colour for colour, factor in enumerate(factors)
               if not (Counter(factor) - Counter(row))]
    require(len(matches) == 1, "survivor lacks a unique pure anchor square")
    colour = matches[0]
    require(sum(cell in EXPORT.ANCHORS for cell in row) == 8,
            "survivor has extra anchor factors")
    return colour


def colour_normalization(colour):
    if colour == 0:
        return (0, 1, 2)
    if colour == 1:
        return (1, 0, 2)
    return (1, 2, 0)


def normalize_residual(row, colour):
    colours = colour_normalization(colour)
    moved = []
    for cell_id in row:
        u, v, a, b = BASE.CELLS[cell_id]
        moved.append(BASE.CELL_ID[(u, v, colours[a], colours[b])])
    return bytes(sorted(moved))


def audit_ports(row):
    ports = Counter()
    for cell_id in row:
        u, v, a, b = BASE.CELLS[cell_id]
        ports[(u, a)] += 1
        ports[(v, b)] += 1
    require(len(row) == 16, "factored residual does not have degree 16")
    require(all(ports[(site, 0)] == 0 for site in range(BASE.N)),
            "normalized pure colour remains in residual")
    require(all(ports[(site, colour)] == 2
                for site in range(BASE.N) for colour in (1, 2)),
            "two-colour residual is not port-degree two")
    require(not any(cell in EXPORT.ANCHORS for cell in row),
            "factored residual retains an anchor cell")


def main():
    accumulated = Counter()
    input_blocks = 0
    input_mass = Fraction(0)
    colour_histogram = Counter()
    source_hasher = sha256()
    with SOURCE.open() as handle:
        raw = next(handle)
        source_hasher.update(raw.encode("ascii"))
        header = json.loads(raw)
        require(header["type"] == "header", "missing source header")
        trailer = None
        for raw in handle:
            source_hasher.update(raw.encode("ascii"))
            record = json.loads(raw)
            if record["type"] == "trailer":
                trailer = record
                continue
            require(record["type"] == "block", "unknown source record")
            require(record["category"] == "survivor_only_one_pure_assignment",
                    "post-unary stream contains a non-pure-square survivor")
            product_row = bytes.fromhex(record["product_row"])
            coefficient = Fraction(*record["coefficient"])
            colour = survivor_colour(product_row)
            residual = subtract_factor(product_row, anchor_factor(colour))
            residual = normalize_residual(residual, colour)
            audit_ports(residual)
            accumulated[residual] += coefficient
            input_blocks += 1
            input_mass += coefficient
            colour_histogram[colour] += 1
    require(trailer is not None, "source stream lacks trailer")
    require(input_blocks == trailer["survivor_blocks"],
            "source block count changed")
    require(input_mass == Fraction(*trailer["survivor_weight"]),
            "source weight changed")
    pre_cancel_rows = len(accumulated)
    zeros = sum(value == 0 for value in accumulated.values())
    accumulated = Counter({row: value for row, value in accumulated.items()
                           if value})
    require(sum(accumulated.values(), Fraction(0)) == input_mass,
            "literal collection changed total mass")

    subgroup = tuple((sites, colours) for sites, colours in EXPORT.STABILIZER
                     if colours[0] == 0)
    require(len(subgroup) == 768,
            "pure-anchor-square stabilizer is not order 768")
    output_hasher = sha256()
    with STREAM.open("w") as handle:
        output_header = {
            "type": "header",
            "format": "krenn-r8prime-square-pure-anchor-factored-raw-v1",
            "source_sha256": source_hasher.hexdigest(),
            "common_factor": "(x01_00*x23_00*x45_00*x67_00)^2",
            "remaining_stabilizer_order": len(subgroup),
            "remaining_stabilizer": [
                ["".join(map(str, sites)), "".join(map(str, colours))]
                for sites, colours in subgroup
            ],
            "rows_are_canonical": False,
        }
        encoded = json.dumps(output_header, sort_keys=True,
                             separators=(",", ":")) + "\n"
        handle.write(encoded)
        output_hasher.update(encoded.encode("ascii"))
        for index, (row, coefficient) in enumerate(sorted(accumulated.items())):
            record = {
                "type": "row",
                "index": index,
                "row": row.hex(),
                "coefficient": [coefficient.numerator, coefficient.denominator],
            }
            encoded = json.dumps(record, sort_keys=True,
                                 separators=(",", ":")) + "\n"
            handle.write(encoded)
            output_hasher.update(encoded.encode("ascii"))

    result = {
        "status": "UNAUDITED exact symbolic factor and literal collision pass",
        "source_sha256": source_hasher.hexdigest(),
        "input_double_coset_blocks": input_blocks,
        "input_weight": [input_mass.numerator, input_mass.denominator],
        "survivor_pure_colour_block_histogram": dict(sorted(
            colour_histogram.items())),
        "forced_common_factor_before_normalization": (
            "for a unique colour c, product_row is divisible by "
            "(prod_{01,23,45,67} x_uv^{cc})^2"
        ),
        "normalized_common_factor": "(x01_00*x23_00*x45_00*x67_00)^2",
        "factored_row_degree": 16,
        "factored_port_rule": (
            "degree 0 on every colour-0 port; degree 2 on every colour-1 "
            "and colour-2 port; no orbit0 anchor variables"
        ),
        "remaining_stabilizer_structure": "(C2 wr S4) x S2",
        "remaining_stabilizer_order": len(subgroup),
        "distinct_raw_rows_before_zero_removal": pre_cancel_rows,
        "exact_zero_rows_removed": zeros,
        "distinct_raw_rows_after_literal_collection": len(accumulated),
        "output_stream_sha256": output_hasher.hexdigest(),
        "output_stream": STREAM.name,
        "collision_scope": (
            "Only byte-identical rows in the deterministic pure-colour "
            "normalization are collected here. The remaining 768-action "
            "canonical collection is still required."
        ),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("R8' square pure-anchor factor/collection: PASS")
    print("blocks / raw rows / zeros / nonzero:",
          input_blocks, pre_cancel_rows, zeros, len(accumulated))
    print("remaining stabilizer:", len(subgroup))
    print("stream sha256:", output_hasher.hexdigest())
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
