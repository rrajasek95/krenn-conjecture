#!/usr/bin/env python3
"""Emit the exact R8^2 residual after unary gr16 packet reduction.

For each R8 orbit pair (i,j), fix the canonical left row x_i and partition
the right orbit O_j by Stab(x_i).  Each block is a diagonal G-orbit of ordered
row pairs.  Blocks admitting a mixed all-anchor divisor are removed by a
literal unary leading column Q H_w.  Only surviving weighted blocks are sent
to the downstream canonical collector.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
EXPORT_PATH = BRIDGE / "export_orbit0_cutoff_seed.py"
SPEC = importlib.util.spec_from_file_location("orbit0_export", EXPORT_PATH)
EXPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPORT)
BASE = EXPORT.BASE
R8_PATH = BRIDGE / "results_orbit0_cutoff8_leading_residual.json"
UNARY_PATH = HERE / "results_r8_square_unary_packet_reduction.json"
DOUBLE_COSET_PATH = HERE / "results_r8_double_coset_count.json"
STREAM = HERE / "r8_square_post_unary_blocks.jsonl"
OUT = HERE / "results_r8_square_post_unary_blocks.json"
GROUP_ORDER = 2304


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def transformed_row(row, action):
    transform = EXPORT.TRANSFORMS[action]
    return bytes(sorted(transform[cell] for cell in row))


def anchor_pattern(row):
    masks = [0, 0, 0, 0]
    pair_index = {edge: index for index, edge in enumerate(EXPORT.M0)}
    for cell_id in row:
        if cell_id not in EXPORT.ANCHORS:
            continue
        u, v, a, b = BASE.CELLS[cell_id]
        require(a == b, "anchor cell is not diagonal-colour")
        masks[pair_index[(u, v)]] |= 1 << a
    return tuple(masks)


def mixed_assignments(pattern):
    answer = []
    for assignment in product(BASE.COLORS, repeat=4):
        if len(set(assignment)) == 1:
            continue
        if all(pattern[pair] & (1 << colour)
               for pair, colour in enumerate(assignment)):
            answer.append(assignment)
    return tuple(answer)


ASSIGNMENTS = {pattern: mixed_assignments(pattern)
               for pattern in product(range(8), repeat=4)}


def category(row):
    pattern = anchor_pattern(row)
    if ASSIGNMENTS[pattern]:
        return "unary_reducible", pattern
    if any(mask == 0 for mask in pattern):
        return "survivor_missing_physical_pair", pattern
    require(pattern in ((1, 1, 1, 1), (2, 2, 2, 2), (4, 4, 4, 4)),
            "unclassified full-support survivor")
    return "survivor_only_one_pure_assignment", pattern


def selected_word(assignment):
    word = [None] * BASE.N
    for pair, colour in enumerate(assignment):
        word[2 * pair] = colour
        word[2 * pair + 1] = colour
    return tuple(word)


def subtract_term(row, term):
    residual = Counter(row)
    residual.subtract(term)
    require(all(value >= 0 for value in residual.values()),
            "selected all-anchor term does not divide target row")
    return bytes(sorted(cell for cell, value in residual.items()
                        for _ in range(value)))


def unary_provenance(row):
    verdict, pattern = category(row)
    require(verdict == "unary_reducible", "provenance requested for survivor")
    assignment = min(ASSIGNMENTS[pattern])
    word = selected_word(assignment)
    term = BASE.term_ids(word, EXPORT.M0)
    multiplier = subtract_term(row, term)
    require(len(multiplier) == 20, "degree-20 multiplier has wrong length")
    require(BASE.row_degree(multiplier, EXPORT.ANCHORS) == 16,
            "unary multiplier has wrong K degree")
    degree16 = []
    for output in BASE.column_rows((word, multiplier)):
        if BASE.row_degree(output, EXPORT.ANCHORS) == 16:
            degree16.append(output)
    require(degree16 == [row],
            "all-anchor packet is not literally unary in gr16")
    return word, multiplier, pattern


def encode_fraction(value):
    return [value.numerator, value.denominator]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--residual", type=Path, default=R8_PATH)
    parser.add_argument("--unary", type=Path, default=UNARY_PATH)
    parser.add_argument("--double-cosets", type=Path, default=DOUBLE_COSET_PATH)
    parser.add_argument("--stream", type=Path, default=STREAM)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    residual_path = args.residual.resolve()
    unary_path = args.unary.resolve()
    double_coset_path = args.double_cosets.resolve()
    stream_path = args.stream.resolve()
    raw = json.loads(residual_path.read_text())
    unary = json.loads(unary_path.read_text())
    double_cosets = json.loads(double_coset_path.read_text())
    survivor_pairs = {
        (item["left_orbit"], item["right_orbit"])
        for item in unary["orbit_pair_survivor_census"]
    }
    pair_double_cosets = {
        (left, right): count
        for left, right, count in double_cosets["pair_counts"]
    }
    require(len(survivor_pairs) == unary["orbit_pairs_with_some_survivor"],
            "survivor pair census changed")

    rows = []
    orbits = []
    coefficients = []
    stabilizers = []
    for row_hex, numerator, denominator in raw["residual"]:
        row = bytes.fromhex(row_hex)
        orbit = tuple(EXPORT.row_orbit(row))
        rows.append(row)
        orbits.append(orbit)
        coefficients.append(Fraction(numerator, denominator) / len(orbit))
        stabilizers.append(tuple(
            action for action in range(GROUP_ORDER)
            if transformed_row(row, action) == row
        ))

    stream_hasher = sha256()
    survivor_blocks = 0
    survivor_weight = Fraction(0)
    survivor_categories = Counter()
    killed_blocks_partitioned = 0
    killed_weight_partitioned = Fraction(0)
    unary_patterns = {}
    processed_double_cosets = 0
    with stream_path.open("w") as handle:
        header = {
            "type": "header",
            "format": "krenn-r8-square-post-unary-double-coset-v1",
            "group_order": GROUP_ORDER,
            "r8_sha256": sha256(residual_path.read_bytes()).hexdigest(),
            "unary_census_sha256": sha256(unary_path.read_bytes()).hexdigest(),
            "double_coset_census_sha256":
                sha256(double_coset_path.read_bytes()).hexdigest(),
            "record_weight": (
                "total coefficient mass of the ordered labelled row pairs "
                "in this diagonal-orbit block; i<j includes both orders"
            ),
        }
        encoded = json.dumps(header, sort_keys=True,
                             separators=(",", ":")) + "\n"
        handle.write(encoded)
        stream_hasher.update(encoded.encode("ascii"))

        for left, right in sorted(survivor_pairs):
            left_row = rows[left]
            right_orbit = orbits[right]
            stabilizer = stabilizers[left]
            right_orbit_set = set(right_orbit)
            unseen = set(right_orbit_set)
            local_blocks = 0
            while unseen:
                seed = min(unseen)
                block = {transformed_row(seed, action)
                         for action in stabilizer}
                require(block <= right_orbit_set,
                        "stabilizer block left right orbit")
                unseen.difference_update(block)
                local_blocks += 1
                product_row = bytes(sorted(left_row + seed))
                verdict, pattern = category(product_row)
                require(all(category(bytes(sorted(left_row + member)))[0]
                            == verdict for member in block),
                        "one stabilizer block mixes unary and survivor rows")
                symmetry = 1 if left == right else 2
                weight = (len(orbits[left]) * len(block) * symmetry
                          * coefficients[left] * coefficients[right])
                if verdict == "unary_reducible":
                    killed_blocks_partitioned += 1
                    killed_weight_partitioned += weight
                    key = "".join(map(str, pattern))
                    if key not in unary_patterns:
                        word, multiplier, pattern = unary_provenance(product_row)
                        unary_patterns[key] = {
                            "pattern": list(pattern),
                            "word": "".join(map(str, word)),
                            "example_product_row": product_row.hex(),
                            "example_multiplier": multiplier.hex(),
                            "literal_gr16_outputs": 1,
                        }
                    continue
                record = {
                    "type": "block",
                    "index": survivor_blocks,
                    "left_orbit": left,
                    "right_orbit": right,
                    "relative_representative": seed.hex(),
                    "product_row": product_row.hex(),
                    "stabilizer_block_size": len(block),
                    "ordered_pair_symmetry": symmetry,
                    "coefficient": encode_fraction(weight),
                    "category": verdict,
                }
                encoded = json.dumps(record, sort_keys=True,
                                     separators=(",", ":")) + "\n"
                handle.write(encoded)
                stream_hasher.update(encoded.encode("ascii"))
                survivor_blocks += 1
                survivor_weight += weight
                survivor_categories[verdict] += 1
            require(local_blocks == pair_double_cosets[(left, right)],
                    "direct stabilizer partition differs from character count")
            processed_double_cosets += local_blocks

        trailer = {
            "type": "trailer",
            "survivor_blocks": survivor_blocks,
            "survivor_weight": encode_fraction(survivor_weight),
            "partitioned_double_cosets": processed_double_cosets,
            "partitioned_killed_blocks": killed_blocks_partitioned,
            "partitioned_killed_weight": encode_fraction(
                killed_weight_partitioned),
        }
        encoded = json.dumps(trailer, sort_keys=True,
                             separators=(",", ":")) + "\n"
        handle.write(encoded)
        stream_hasher.update(encoded.encode("ascii"))

    expected_survivor_weight = sum(
        Fraction(*value)
        for key, value in unary["ordered_pair_category_weighted_mass"].items()
        if key.startswith("survivor_")
    )
    require(survivor_weight == expected_survivor_weight,
            "surviving block weights differ from ordered-pair census")
    total_blocks = double_cosets["total_double_coset_blocks"]
    all_killed_pair_blocks = sum(
        pair_double_cosets[pair] for pair in pair_double_cosets
        if pair not in survivor_pairs
    )
    require(processed_double_cosets + all_killed_pair_blocks == total_blocks,
            "partitioned plus all-killed pairs do not exhaust double cosets")
    killed_blocks_total = total_blocks - survivor_blocks

    result = {
        "status": "UNAUDITED exact post-unary double-coset stream",
        "input_r8_path": str(residual_path),
        "input_r8_sha256": sha256(residual_path.read_bytes()).hexdigest(),
        "survivor_orbit_pairs": len(survivor_pairs),
        "total_double_coset_blocks": total_blocks,
        "survivor_double_coset_blocks": survivor_blocks,
        "killed_double_coset_blocks": killed_blocks_total,
        "survivor_block_category_histogram": dict(sorted(
            survivor_categories.items())),
        "survivor_weight": encode_fraction(survivor_weight),
        "expected_survivor_weight": encode_fraction(expected_survivor_weight),
        "stream_sha256": stream_hasher.hexdigest(),
        "stream_records": survivor_blocks,
        "stream_path": stream_path.name,
        "stabilizer_blocks_mix_verdicts": False,
        "unary_provenance_rule": (
            "Choose the lexicographically first non-pure four-pair colour "
            "assignment whose four anchor cells divide the row; let w repeat "
            "those colours on pair endpoints and Q=row/(all-anchor term). "
            "Then deg(Q)=20, Kdeg(Q)=16, and (Q H_w)_gr16 is exactly row."
        ),
        "audited_unary_anchor_patterns": len(unary_patterns),
        "unary_pattern_examples": unary_patterns,
        "soundness_scope": (
            "The stream is R8^2 after literal unary leading-column removal, "
            "before canonical collection of coincident product rows. It is "
            "not yet membership in the full associated-graded source."
        ),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("R8^2 post-unary block export: PASS")
    print("survivor / killed blocks:", survivor_blocks, killed_blocks_total)
    print("survivor weight:", survivor_weight)
    print("patterns:", len(unary_patterns))
    print("stream sha256:", stream_hasher.hexdigest())
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
