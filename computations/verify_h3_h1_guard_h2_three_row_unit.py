#!/usr/bin/env python3
"""Exact three-row Hamming-two unit over the chi=-12 H1 packet."""

from fractions import Fraction as Q
from hashlib import sha256
import json

import analyze_h3_h1_guard_h2_fredholm as A
import verify_h3_hamming_two_sum_clean_tail_boundary as B


ROWS = (
    (Q(1), 0, 0, (0, 0, 1, 1, 1, 1)),
    (Q(-1), 0, 1, (0, 0, 0, 0, 1, 1)),
    (Q(-1), 0, 1, (0, 0, 1, 1, 0, 0)),
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    # Recheck the packet's admitted layer and its nonzero clean tail.
    B.audit_admitted_rows()
    B.audit_sum_is_not_tail()
    B.audit_goodness_segre_and_mutations()

    raw_cross = {
        key: {(index,): Q(1)}
        for index, key in enumerate(A.CROSS_KEYS)
    }
    selected = []
    total = {}
    for weight, row, column, word in ROWS:
        polynomial = A.residual(raw_cross, row, column, word)
        selected.append({
            "weight": int(weight),
            "row": row,
            "column": column,
            "word": "".join(map(str, word)),
            "terms": len(polynomial),
        })
        total = A.add(total, A.scale(weight, polynomial))
    require(total == {(): Q(1)}, ("literal three-row unit moved", total))

    # Independently record how much freedom survives the already-admitted
    # Hamming-one system.  The unit above does not use this reduction.
    _, h1_rows, h1_rank, h1_nullity = A.h1_affine_graph()
    require((h1_rows, h1_rank, h1_nullity) == (70, 34, 56),
            ("H1 affine graph moved", h1_rows, h1_rank, h1_nullity))

    ledger = {
        "cross_q_variables": len(A.CROSS_KEYS),
        "h1_nonzero_rows": h1_rows,
        "h1_rank": h1_rank,
        "h1_nullity": h1_nullity,
        "selected_h2_rows": selected,
        "weighted_sum": 1,
        "uses_h1_reduction": False,
        "selected_layers": [1, -1, -12, 0],
        "conclusion": "no Hamming-two lift of the chi=-12 packet",
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    digest = sha256(encoded).hexdigest()
    expected = "86a5689038f95a933f2f4166b1041b2d633284652856d1b1194ef6c484071011"
    require(digest == expected, ("ledger changed", digest, ledger))
    print("h=3 chi=-12 packet / three-row Hamming-two unit: PASS")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
