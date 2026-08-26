#!/usr/bin/env python3
r"""Count R8 orbit-product blocks by permutation characters.

For R8 row orbits G/H_i and G/H_j, diagonal product blocks are the double
cosets H_i\G/H_j.  We compute their number as the inner product of the two
permutation characters.  Conjugacy classes of
G=(C2 wr S4) x S3 are derived from signed pair cycles and colour cycle type.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
EXPORT_PATH = BRIDGE / "export_orbit0_cutoff_seed.py"
SPEC = importlib.util.spec_from_file_location("orbit0_export", EXPORT_PATH)
EXPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPORT)
R8_PATH = BRIDGE / "results_orbit0_cutoff8_leading_residual.json"
OUT = HERE / "results_r8_double_coset_count.json"
GROUP_ORDER = 2304


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def cycle_type(permutation):
    unseen = set(range(len(permutation)))
    lengths = []
    while unseen:
        start = min(unseen)
        current = start
        length = 0
        while current in unseen:
            unseen.remove(current)
            length += 1
            current = permutation[current]
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def conjugacy_key(action):
    sites, colours = EXPORT.STABILIZER[action]
    pair_permutation = []
    flips = []
    for pair in range(4):
        left_image = sites[2 * pair]
        right_image = sites[2 * pair + 1]
        require(left_image // 2 == right_image // 2,
                "site action does not preserve physical anchor pairs")
        pair_permutation.append(left_image // 2)
        flips.append(left_image % 2)
    unseen = set(range(4))
    positive = []
    negative = []
    while unseen:
        start = min(unseen)
        current = start
        length = 0
        sign = 0
        while current in unseen:
            unseen.remove(current)
            length += 1
            sign ^= flips[current]
            current = pair_permutation[current]
        (negative if sign else positive).append(length)
    return (tuple(sorted(positive, reverse=True)),
            tuple(sorted(negative, reverse=True)), cycle_type(colours))


def transformed_row(row, action):
    transform = EXPORT.TRANSFORMS[action]
    return bytes(sorted(transform[cell] for cell in row))


def direct_double_cosets(left, right):
    stabilizer = tuple(action for action in range(GROUP_ORDER)
                       if transformed_row(left, action) == left)
    unseen = set(EXPORT.row_orbit(right))
    count = 0
    while unseen:
        seed = min(unseen)
        block = {transformed_row(seed, action) for action in stabilizer}
        require(block <= unseen | (set(EXPORT.row_orbit(right)) - unseen),
                "stabilizer block left the right orbit")
        unseen.difference_update(block)
        count += 1
    return count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--residual", type=Path, default=R8_PATH)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    residual_path = args.residual.resolve()
    require(len(EXPORT.STABILIZER) == GROUP_ORDER, "group order changed")
    class_keys = tuple(conjugacy_key(action) for action in range(GROUP_ORDER))
    class_sizes = Counter(class_keys)
    require(len(class_sizes) == 60, "expected 20 signed-pair x 3 colour classes")

    r8 = json.loads(residual_path.read_text())
    rows = tuple(bytes.fromhex(item[0]) for item in r8["residual"])
    stabilizers = []
    characters = []
    orbit_sizes = []
    for row in rows:
        stabilizer = tuple(action for action in range(GROUP_ORDER)
                           if transformed_row(row, action) == row)
        require(stabilizer, "row stabilizer is empty")
        orbit_size = GROUP_ORDER // len(stabilizer)
        require(orbit_size == len(EXPORT.row_orbit(row)),
                "row orbit-stabilizer mismatch")
        intersections = Counter(class_keys[action] for action in stabilizer)
        character = {}
        for key, class_size in class_sizes.items():
            value = (Fraction(GROUP_ORDER, class_size)
                     * intersections[key] / len(stabilizer))
            require(value.denominator == 1,
                    "permutation character is nonintegral")
            character[key] = value.numerator
        stabilizers.append(stabilizer)
        characters.append(character)
        orbit_sizes.append(orbit_size)

    pair_histogram = Counter()
    total = 0
    maximum = (0, None)
    pair_counts = []
    for left in range(len(rows)):
        for right in range(left, len(rows)):
            value = sum(class_sizes[key]
                        * characters[left][key] * characters[right][key]
                        for key in class_sizes)
            require(value % GROUP_ORDER == 0,
                    "character inner product is nonintegral")
            value //= GROUP_ORDER
            pair_histogram[value] += 1
            total += value
            pair_counts.append([left, right, value])
            if value > maximum[0]:
                maximum = (value, (left, right))

    controls = ((0, 0), (0, 1),
                (min(17, len(rows) - 1), min(93, len(rows) - 1)),
                (len(rows) - 1, len(rows) - 1))
    direct_controls = []
    lookup = {(left, right): value for left, right, value in pair_counts}
    for left, right in controls:
        direct = direct_double_cosets(rows[left], rows[right])
        require(direct == lookup[(left, right)],
                "direct double-coset control differs from character result")
        direct_controls.append([left, right, direct])

    result = {
        "status": "UNAUDITED exact finite-group double-coset census",
        "input_r8_path": str(residual_path),
        "input_r8_sha256": sha256(residual_path.read_bytes()).hexdigest(),
        "group_structure": "(C2 wr S4) x S3",
        "group_order": GROUP_ORDER,
        "conjugacy_classes": len(class_sizes),
        "r8_row_orbits": len(rows),
        "unordered_orbit_pairs": len(pair_counts),
        "total_double_coset_blocks": total,
        "double_coset_count_histogram": dict(sorted(pair_histogram.items())),
        "maximum_blocks_for_one_orbit_pair": maximum[0],
        "maximum_pair": list(maximum[1]),
        "direct_partition_controls": direct_controls,
        "formula": (
            "#(H_i\\G/H_j)=<Ind_{H_i}^G 1,Ind_{H_j}^G 1>; "
            "permutation characters are reconstructed from the intersection "
            "of H_i with each signed-cycle/colour conjugacy class"
        ),
        "pair_counts": pair_counts,
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("R8 double-coset count: PASS")
    print("orbit pairs / blocks:", len(pair_counts), total)
    print("max:", maximum)
    print("controls:", direct_controls)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
