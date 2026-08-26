#!/usr/bin/env python3
"""Exact referee of the F3 diagonal packet signature stream.

The 6+2 cofactor equations imply that the cofactor-zero positions of either
colour must support a nonzero permanent in every 2x2 block of the other.
This reduces 69,696 live signatures to 168.  Every survivor has ten nonzero
Q coordinates, while the 4+4 equations require one Q support to be disjoint
from the complemented support of the other.  Two ten-subsets cannot be
disjoint in a 16-set; a literal pair scan is retained as a control.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
STREAM = HERE / "f3_diagonal_packet_signatures.jsonl"
OUT = HERE / "results_f3_diagonal_signature_compatibility.json"


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def permanent(matrix):
    return (matrix[0] * matrix[3] + matrix[1] * matrix[2]) % 3


def complement_q(mask):
    answer = 0
    for index in range(16):
        if mask >> index & 1:
            answer |= 1 << (15 - index)
    return answer


def allowed_permanent_in_every_block(cofactor_mask):
    for block in range(6):
        allowed = (~(cofactor_mask >> (4 * block))) & 0b1111
        has_diagonal = allowed & 0b1001 == 0b1001
        has_antidiagonal = allowed & 0b0110 == 0b0110
        if not (has_diagonal or has_antidiagonal):
            return False
    return True


def block_failure_count(cofactor_mask):
    count = 0
    for block in range(6):
        allowed = (~(cofactor_mask >> (4 * block))) & 15
        if not (allowed & 9 == 9 or allowed & 6 == 6):
            count += 1
    return count


def compatible(left, right):
    return not (
        left["x24"] & right["cofactor24"]
        or right["x24"] & left["cofactor24"]
        or left["q16"] & complement_q(right["q16"])
        or right["q16"] & complement_q(left["q16"])
    )


def main():
    raw = STREAM.read_bytes()
    stream_sha = sha256(raw).hexdigest()
    lines = raw.decode("ascii").splitlines()
    header = json.loads(lines[0])
    rows = [json.loads(line) for line in lines[1:]]
    require(header["type"] == "header" and header["field"] == 3,
            "signature header changed")
    require(len(header["matrix_types"]) == 24
            and all(permanent(matrix) == 2
                    for matrix in header["matrix_types"]),
            "F3 block type census changed")
    require(len(rows) == 69_696
            and sum(row["labelled_count"] for row in rows) == 1_115_904,
            "live signature/labelled count changed")
    signatures = {(row["x24"], row["cofactor24"], row["q16"])
                  for row in rows}
    require(len(signatures) == len(rows), "signature stream has duplicates")

    x_histogram = Counter(row["x24"].bit_count() for row in rows)
    failure_histogram = Counter()
    weighted_failure_histogram = Counter()
    viable = []
    for row in rows:
        failures = block_failure_count(row["cofactor24"])
        failure_histogram[failures] += 1
        weighted_failure_histogram[failures] += row["labelled_count"]
        if failures == 0:
            viable.append(row)
    require(min(x_histogram) == 14,
            "a live graph uses fewer than 14 nonanchor entries")
    require(failure_histogram == {
        0: 168, 1: 768, 2: 2232, 3: 8256,
        4: 22080, 5: 21024, 6: 15168,
    }, "cofactor failure histogram changed")
    require(weighted_failure_histogram == {
        0: 2688, 1: 12288, 2: 35712, 3: 132096,
        4: 354048, 5: 336384, 6: 242688,
    }, "weighted cofactor failure histogram changed")
    require(len(viable) == 168
            and sum(row["labelled_count"] for row in viable) == 2688,
            "6+2 viable stratum changed")

    viable_joint_histogram = Counter(
        (row["x24"].bit_count(), row["cofactor24"].bit_count(),
         row["q16"].bit_count()) for row in viable
    )
    require(viable_joint_histogram == {
        (16, 4, 10): 72,
        (16, 12, 10): 48,
        (20, 12, 10): 48,
    }, "viable support-size histogram changed")
    require(all(row["q16"].bit_count() == 10 for row in viable),
            "a 6+2 viable signature does not have Q support ten")

    # The size argument already proves no pair.  Replay the literal bitmask
    # conditions over all 168^2 ordered pairs as an independent control.
    compatible_pairs = [(left["index"], right["index"])
                        for left in viable for right in viable
                        if compatible(left, right)]
    require(not compatible_pairs, "a compatible live signature pair exists")
    cofactor_only_pairs = sum(
        not (left["x24"] & right["cofactor24"]
             or right["x24"] & left["cofactor24"])
        for left in viable for right in viable
    )
    require(cofactor_only_pairs == 288,
            "Q-orbit must-fire control changed")

    result = {
        "status": "UNAUDITED exact F3 diagonal signature compatibility theorem",
        "signature_stream_sha256": stream_sha,
        "live_signatures": len(rows),
        "live_labelled_graphs": sum(row["labelled_count"] for row in rows),
        "x_support_histogram": dict(sorted(x_histogram.items())),
        "cofactor_permanent_failure_histogram_signatures": dict(
            sorted(failure_histogram.items())
        ),
        "cofactor_permanent_failure_histogram_labelled": dict(
            sorted(weighted_failure_histogram.items())
        ),
        "six_plus_two_viable_signatures": len(viable),
        "six_plus_two_viable_labelled_graphs": sum(
            row["labelled_count"] for row in viable
        ),
        "viable_X_C_Q_size_histogram": {
            ",".join(map(str, key)): value
            for key, value in sorted(viable_joint_histogram.items())
        },
        "q_support_size_on_viable_stratum": 10,
        "literal_ordered_compatible_pairs": len(compatible_pairs),
        "cofactor_only_ordered_pairs_must_fire": cofactor_only_pairs,
        "proof": (
            "For X_d*C_c=0 and perm(M^d_ij)=-1, the zero set of C_c in "
            "each 2x2 block must contain a diagonal or antidiagonal pair. "
            "Only 168 live signatures pass this six-block test, and every "
            "one has |supp Q|=10. The 4+4 equations require supp(Q_c) "
            "disjoint from complement(supp(Q_d)); two size-10 subsets of "
            "a 16-set cannot be disjoint."
        ),
        "conclusion": (
            "Over F3, no two live same-colour-diagonal graphs can jointly "
            "satisfy the pairconstant, 00000101, and 01010101 packet; hence "
            "there is no three-colour diagonal solution to this packet."
        ),
        "scope": (
            "This is an exact special-fibre theorem over F3, not yet a "
            "characteristic-zero theorem. It also assumes all cross-colour "
            "cells vanish, so literal full-row residual tails are absent."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("F3 diagonal signature compatibility: PASS")
    print("live / 6+2 viable:", len(rows), len(viable))
    print("viable (|X|,|C|,|Q|):", viable_joint_histogram)
    print("compatible / cofactor-only pairs:", len(compatible_pairs),
          cofactor_only_pairs)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
