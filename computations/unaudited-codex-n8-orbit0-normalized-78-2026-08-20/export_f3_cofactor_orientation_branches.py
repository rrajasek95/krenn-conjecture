#!/usr/bin/env python3
"""Export the 168 F3 cofactor-viable signatures by orientation branch.

A six-bit branch chooses, in edge order 01,02,03,12,13,23, either the
diagonal (bit 0) or antidiagonal (bit 1) cofactor-zero pair.  Endpoint clone
flips gauge-fix the first three bits to zero, leaving eight switching classes.
The four triangle parities have weights 0,2,4, giving the three S4 orbits.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
STREAM = HERE / "f3_diagonal_packet_signatures.jsonl"
OUT = HERE / "results_f3_cofactor_orientation_branches.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def options_for_block(cofactor_mask, block):
    allowed = (~(cofactor_mask >> (4 * block))) & 15
    answer = []
    if allowed & 9 == 9:
        answer.append(0)
    if allowed & 6 == 6:
        answer.append(1)
    return tuple(answer)


def class_tail(bits):
    b01, b02, b03, b12, b13, b23 = bits
    return (b12 ^ b01 ^ b02,
            b13 ^ b01 ^ b03,
            b23 ^ b02 ^ b03)


def class_id(bits):
    tail = class_tail(bits)
    return 4 * tail[0] + 2 * tail[1] + tail[2]


def triangle_parities_from_tail(tail):
    a, b, c = tail
    return (a, b, c, a ^ b ^ c)


def mask_string(mask, width):
    return format(mask, f"0{width}b")


def summarize(member_indices, rows, membership_count=None, masks=None):
    members = [rows[index] for index in sorted(member_indices)]
    q_masks = sorted({row["q16"] for row in members})
    x_masks = {row["x24"] for row in members}
    c_masks = {row["cofactor24"] for row in members}
    q_union = 0
    q_intersection = (1 << 16) - 1
    for mask in q_masks:
        q_union |= mask
        q_intersection &= mask
    record = {
        "unique_signatures": len(members),
        "labelled_graphs_unique_sum": sum(row["labelled_count"]
                                            for row in members),
        "membership_count": (len(members) if membership_count is None
                             else membership_count),
        "unique_X_masks": len(x_masks),
        "unique_cofactor_masks": len(c_masks),
        "unique_Q_masks": len(q_masks),
        "Q_mask_fixed": len(q_masks) == 1,
        "Q_support_size_histogram": dict(sorted(Counter(
            row["q16"].bit_count() for row in members
        ).items())),
        "structural_Q_zero_indices": [index for index in range(16)
                                      if not (q_union >> index & 1)],
        "structural_Q_live_indices": [index for index in range(16)
                                      if q_intersection >> index & 1],
        "representative": None,
    }
    if masks is not None:
        record["branch_masks"] = list(masks)
    if members:
        representative = members[0]
        record["representative"] = {
            "signature_index": representative["index"],
            "block_indices": representative["representative_block_indices"],
            "X24": representative["x24"],
            "X24_bits": mask_string(representative["x24"], 24),
            "cofactor24": representative["cofactor24"],
            "cofactor24_bits": mask_string(representative["cofactor24"], 24),
            "Q16": representative["q16"],
            "Q16_bits": mask_string(representative["q16"], 16),
            "Q_zero_indices": [index for index in range(16)
                               if not (representative["q16"] >> index & 1)],
        }
    return record


def main():
    raw = STREAM.read_bytes()
    lines = raw.decode("ascii").splitlines()
    header = json.loads(lines[0])
    all_rows = [json.loads(line) for line in lines[1:]]
    rows = {}
    row_options = {}
    for row in all_rows:
        options = tuple(options_for_block(row["cofactor24"], block)
                        for block in range(6))
        if all(options):
            rows[row["index"]] = row
            row_options[row["index"]] = options
    require(len(rows) == 168
            and sum(row["labelled_count"] for row in rows.values()) == 2688,
            "cofactor-viable stratum changed")

    branch_members = {mask: set() for mask in range(64)}
    for index, options in row_options.items():
        for bits in product(*options):
            mask = sum(bit << edge for edge, bit in enumerate(bits))
            branch_members[mask].add(index)
    branch_records = []
    for mask in range(64):
        bits = tuple((mask >> edge) & 1 for edge in range(6))
        tail = class_tail(bits)
        parities = triangle_parities_from_tail(tail)
        record = {
            "branch_mask": mask,
            "branch_bits_01_02_03_12_13_23": list(bits),
            "switching_class": class_id(bits),
            "gauge_fixed_tail_12_13_23": list(tail),
            "triangle_parities_012_013_023_123": list(parities),
            "S4_parity_weight": sum(parities),
        }
        record.update(summarize(branch_members[mask], rows))
        branch_records.append(record)

    class_masks = defaultdict(list)
    for record in branch_records:
        class_masks[record["switching_class"]].append(record["branch_mask"])
    class_records = []
    for identifier in range(8):
        masks = tuple(sorted(class_masks[identifier]))
        members = set().union(*(branch_members[mask] for mask in masks))
        memberships = sum(len(branch_members[mask]) for mask in masks)
        tail = ((identifier >> 2) & 1,
                (identifier >> 1) & 1,
                identifier & 1)
        parities = triangle_parities_from_tail(tail)
        record = {
            "switching_class": identifier,
            "gauge_fixed_tail_12_13_23": list(tail),
            "triangle_parities_012_013_023_123": list(parities),
            "S4_parity_weight": sum(parities),
        }
        record.update(summarize(members, rows, memberships, masks))
        class_records.append(record)

    weight_records = []
    for weight in (0, 2, 4):
        classes = [record["switching_class"] for record in class_records
                   if record["S4_parity_weight"] == weight]
        masks = tuple(mask for identifier in classes
                      for mask in class_masks[identifier])
        members = set().union(*(branch_members[mask] for mask in masks))
        memberships = sum(len(branch_members[mask]) for mask in masks)
        record = {"S4_parity_weight": weight,
                  "switching_classes": classes}
        record.update(summarize(members, rows, memberships, sorted(masks)))
        weight_records.append(record)

    require(Counter(record["S4_parity_weight"] for record in class_records)
            == {0: 1, 2: 6, 4: 1}, "S4 class census changed")
    require(all(record["Q_support_size_histogram"] == {10: record["unique_signatures"]}
                for record in class_records),
            "a class acquired a non-ten Q support")
    require(sum(record["membership_count"] for record in branch_records)
            == 672, "branch membership total changed")

    result = {
        "status": "UNAUDITED exact F3 cofactor orientation branch export",
        "source_stream_sha256": sha256(raw).hexdigest(),
        "field": 3,
        "edge_order": header["edge_order"],
        "matrix_types": header["matrix_types"],
        "cofactor_viable_unique_signatures": len(rows),
        "cofactor_viable_labelled_graphs": sum(
            row["labelled_count"] for row in rows.values()
        ),
        "branch_memberships": sum(record["membership_count"]
                                  for record in branch_records),
        "switching_class_rule": (
            "Endpoint flips act by b_ij -> b_ij+f_i+f_j. Gauge f_0=0 and "
            "f_i=b_0i makes star bits zero; the remaining bits are the "
            "triangle parities on 012,013,023."
        ),
        "branches_64": branch_records,
        "switching_classes_8": class_records,
        "S4_orbits_3": weight_records,
        "scope": "Exact F3 support data; representatives guide but do not prove char0 normal forms.",
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("F3 cofactor orientation branches: PASS")
    print("unique/labelled/memberships:", len(rows),
          result["cofactor_viable_labelled_graphs"], result["branch_memberships"])
    for record in class_records:
        print("class", record["switching_class"], "weight",
              record["S4_parity_weight"], "unique/memberships/Qmasks",
              record["unique_signatures"], record["membership_count"],
              record["unique_Q_masks"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
