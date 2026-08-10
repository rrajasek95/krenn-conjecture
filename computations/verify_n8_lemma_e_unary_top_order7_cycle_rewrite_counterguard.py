#!/usr/bin/env python3
"""Exact counterguard to a strict off-diagonal cycle rewrite.

In the fine multidegree of the concentrated unary-top target, project every
literal source multiple to its maximal off-diagonal-order-seven part.  The
resulting 3570 by 9164 integer matrix has rank exactly 3559 over Q.  Modular
elimination gives the lower bound, while eleven reconstructed integral
{+1,-1} left-kernel vectors give the matching upper bound.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json

import verify_n8_lemma_e_unary_top_offdiagonal_filtered_lift as filtered


ORDER = 7
EXPECTED_ROWS = 3570
EXPECTED_COLUMNS = 9164
EXPECTED_RANK = 3559
EXPECTED_FREE_ROWS = (
    592, 593, 947, 3173, 3215, 3523, 3540, 3541, 3547, 3564, 3569,
)
EXPECTED_COVECTOR_SUPPORTS = (
    20, 38, 420, 420, 248, 248, 20, 38, 420, 420, 2130,
)
EXPECTED_MATRIX_DIGEST = "bef3875c1056ce960d0347785e2144292e6948b6e1b03530a427fa544ea2dae4"
EXPECTED_COVECTOR_DIGEST = "c87d6575b7d604cec58a57cbe01397737a7ba07421e289955323f66830f07c5d"
EXPECTED_LEDGER_DIGEST = "3f86c920492d6d706722f9b3eb8325e5e90f18a241378e0515a8e6c15d8957d1"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def canonical_bytes(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode()


def build_columns(generators, row_index, matrix_hash):
    columns = []
    maximum_histogram = Counter()
    column_count = 0
    for vertices, word, label in generators:
        used_tokens = set(zip(vertices, word))
        complement = tuple(
            token for token in filtered.ALL_TOKENS
            if token not in used_tokens
        )
        source_terms = filtered.coefficient_terms(vertices, word)
        for multiplier in filtered.token_matchings(complement):
            monomials = tuple(
                tuple(sorted(source_term + multiplier))
                for source_term in source_terms
            )
            maximum = max(map(filtered.offdiagonal_order, monomials))
            maximum_histogram[maximum] += 1
            if maximum != ORDER:
                continue
            entries = Counter(
                row_index[monomial]
                for monomial in monomials
                if filtered.offdiagonal_order(monomial) == ORDER
            )
            column_count += 1
            canonical_entries = tuple(sorted(entries.items()))
            matrix_hash.update(canonical_bytes((
                column_count, label, multiplier, canonical_entries
            )))
            columns.append(canonical_entries)
    return tuple(columns), maximum_histogram


def main():
    basis = tuple(
        monomial
        for monomial in filtered.token_matchings(filtered.ALL_TOKENS)
        if filtered.offdiagonal_order(monomial) == ORDER
    )
    row_index = {monomial: index for index, monomial in enumerate(basis)}
    require(len(basis) == EXPECTED_ROWS,
            f"the order-seven row count changed: {len(basis)}")
    signatures = Counter(map(filtered.cross_colour_signature, basis))
    require(signatures == {(3, 3, 1): EXPECTED_ROWS},
            f"the order-seven transition type changed: {signatures}")

    generators = filtered.build_generators()
    matrix_hash = sha256(canonical_bytes({
        "basis": basis,
        "order": ORDER,
        "prime": filtered.PRIME,
    }))
    columns, maximum_histogram = build_columns(
        generators, row_index, matrix_hash
    )
    require(len(columns) == EXPECTED_COLUMNS,
            f"the order-seven column count changed: {len(columns)}")

    pivots = {}
    for entries in columns:
        vector = {
            row: value % filtered.PRIME
            for row, value in entries
            if value % filtered.PRIME
        }
        filtered.reduce_column(vector, pivots)
    require(len(pivots) == EXPECTED_RANK,
            f"the modular plateau rank changed: {len(pivots)}")

    free_rows = tuple(row for row in range(len(basis)) if row not in pivots)
    require(free_rows == EXPECTED_FREE_ROWS,
            f"the free-row ledger changed: {free_rows}")
    covectors = []
    for free_row in free_rows:
        covector = {free_row: 1}
        for lead in sorted(pivots, reverse=True):
            value = -sum(
                coefficient * covector.get(row, 0)
                for row, coefficient in pivots[lead].items()
                if row != lead
            ) % filtered.PRIME
            if value:
                covector[lead] = value
        integral = {
            row: value if value <= filtered.PRIME // 2
            else value - filtered.PRIME
            for row, value in covector.items()
        }
        require(set(integral.values()) <= {-1, 1},
                "a modular cokernel vector did not reconstruct integrally")
        covectors.append(integral)

    supports = tuple(len(covector) for covector in covectors)
    require(supports == EXPECTED_COVECTOR_SUPPORTS,
            f"the integral covector supports changed: {supports}")
    for column_index, entries in enumerate(columns, 1):
        for covector_index, covector in enumerate(covectors):
            pairing = sum(
                coefficient * covector.get(row, 0)
                for row, coefficient in entries
            )
            require(pairing == 0,
                    f"column {column_index} pairs {pairing} with integral "
                    f"covector {covector_index}")

    # Each covector is one on its own free row and zero on the other free
    # rows, so the eleven exact annihilators are visibly independent.
    for left, covector in enumerate(covectors):
        require(tuple(covector.get(row, 0) for row in free_rows)
                == tuple(1 if left == right else 0
                         for right in range(len(free_rows))),
                "the integral cokernel basis lost its free-row echelon form")

    matrix_digest = matrix_hash.hexdigest()
    covector_payload = tuple(
        tuple(sorted(covector.items())) for covector in covectors
    )
    covector_digest = sha256(canonical_bytes(covector_payload)).hexdigest()
    if EXPECTED_MATRIX_DIGEST != "TO_BE_FILLED":
        require(matrix_digest == EXPECTED_MATRIX_DIGEST,
                f"the order-seven matrix changed: {matrix_digest}")
    if EXPECTED_COVECTOR_DIGEST != "TO_BE_FILLED":
        require(covector_digest == EXPECTED_COVECTOR_DIGEST,
                f"the integral cokernel changed: {covector_digest}")

    ledger = {
        "order": ORDER,
        "rows": len(basis),
        "transition_signature": {"3,3,1": len(basis)},
        "columns": len(columns),
        "rank_mod_prime": len(pivots),
        "prime": filtered.PRIME,
        "integral_cokernel_dimension": len(covectors),
        "integral_cokernel_supports": supports,
        "free_rows": free_rows,
        "maximum_order_column_histogram": dict(sorted(maximum_histogram.items())),
        "matrix_sha256": matrix_digest,
        "integral_cokernel_sha256": covector_digest,
        "verdict": (
            "the strict primitive-cycle rewrite has an exact "
            "eleven-dimensional top-plateau cokernel over Q"
        ),
        "scope": (
            "concentrated unary-top fine degree and maximal-order-seven "
            "projections only; no claim that the target survives the full ideal"
        ),
    }
    digest = sha256(canonical_bytes(ledger)).hexdigest()
    if EXPECTED_LEDGER_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_DIGEST,
                f"the order-seven ledger changed: {digest}")

    print("N=8 unary-top order-seven cycle rewrite counterguard: PASS")
    print(f"rows={len(basis)}; columns={len(columns)}; "
          f"rank over Q={len(pivots)}; cokernel={len(covectors)}")
    print("transition signature: (x01,x02,x12)=(3,3,1)")
    print(f"integral covector supports: {supports}")
    print(f"matrix sha256: {matrix_digest}")
    print(f"integral cokernel sha256: {covector_digest}")
    print("full ideal membership: OPEN")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
