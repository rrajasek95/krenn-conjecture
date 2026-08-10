#!/usr/bin/env python3
"""Bounded exact census of the order-six reachable-Schur frontier.

This deliberately constructs only the minimum-order-six plateau over a fixed
finite field.  It quantifies the quotient that a full order-six transport
would have to carry and stops before building that transport.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json

import verify_n8_lemma_e_unary_top_offdiagonal_filtered_lift as filtered
import verify_n8_lemma_e_unary_top_order4_reachable_schur as schur


EXPECTED_MATRIX_DIGEST = "7dd2f5e7fca787615932d0eb0e7d1af5b02a650796cf994004c384bb9e9c8dc3"
EXPECTED_LEDGER_DIGEST = "cb4e695ed5f4adde8b14106dd0cf24850c4f277dde540616c161219a300d1fc8"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def canonical_bytes(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode()


def main():
    order_six_basis = tuple(
        monomial
        for monomial in filtered.token_matchings(filtered.ALL_TOKENS)
        if filtered.offdiagonal_order(monomial) == 6
    )
    row_index = {
        monomial: index for index, monomial in enumerate(order_six_basis)
    }
    require(len(order_six_basis) == 12835,
            f"the order-six basis count changed: {len(order_six_basis)}")

    pivots = {}
    columns = 0
    matrix_hash = sha256(canonical_bytes({
        "basis": order_six_basis,
        "prime": filtered.PRIME,
    }))
    for label, multiplier, minimum, monomials, orders in schur.source_columns(
        filtered.build_generators()
    ):
        if minimum != 6:
            continue
        entries = Counter(
            row_index[monomial]
            for monomial, order in zip(monomials, orders)
            if order == 6
        )
        columns += 1
        canonical_entries = tuple(sorted(entries.items()))
        matrix_hash.update(canonical_bytes((
            columns, label, multiplier, canonical_entries
        )))
        vector = {
            row: value % filtered.PRIME
            for row, value in canonical_entries
            if value % filtered.PRIME
        }
        filtered.reduce_column(vector, pivots)

    require(columns == 8476,
            f"the minimum-order-six columns changed: {columns}")
    require(len(pivots) == 7918,
            f"the modular direct order-six rank changed: {len(pivots)}")
    quotient_dimension = len(order_six_basis) - len(pivots)
    require(quotient_dimension == 4917,
            f"the modular order-six quotient changed: {quotient_dimension}")

    # Previous exact checker dimensions.  The product is only a transparent
    # workload proxy, not a runtime theorem.
    order_five_quotient = 948
    order_five_upstream_pivots = 25714
    order_six_upstream_pivots = 44638
    workload_ratio = (
        quotient_dimension * order_six_upstream_pivots
        / (order_five_quotient * order_five_upstream_pivots)
    )
    require(round(workload_ratio, 6) == 9.003823,
            f"the workload proxy changed: {workload_ratio}")

    matrix_digest = matrix_hash.hexdigest()
    if EXPECTED_MATRIX_DIGEST != "TO_BE_FILLED":
        require(matrix_digest == EXPECTED_MATRIX_DIGEST,
                f"the direct order-six matrix changed: {matrix_digest}")
    ledger = {
        "order_six_rows": len(order_six_basis),
        "minimum_order_six_columns": columns,
        "direct_rank_mod_prime": len(pivots),
        "prime": filtered.PRIME,
        "direct_quotient_dimension_mod_prime": quotient_dimension,
        "total_rows_through_order_six": 57558,
        "total_columns_through_order_six": 96922,
        "previous_order_five_quotient_dimension": order_five_quotient,
        "quotient_dimension_ratio": quotient_dimension / order_five_quotient,
        "previous_upstream_pivots": order_five_upstream_pivots,
        "order_six_upstream_pivots": order_six_upstream_pivots,
        "dimension_times_pivots_workload_ratio": workload_ratio,
        "matrix_sha256": matrix_digest,
        "verdict": (
            "the order-six reachable quotient is materially larger; freeze "
            "the exact modular census and do not construct the full transport"
        ),
        "scope": (
            "the modular direct rank is exact over the stated finite field "
            "and gives a Q-rank lower bound only; no order-six target "
            "membership or obstruction conclusion"
        ),
    }
    digest = sha256(canonical_bytes(ledger)).hexdigest()
    if EXPECTED_LEDGER_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_DIGEST,
                f"the order-six frontier ledger changed: {digest}")

    print("N=8 unary-top order-six reachable frontier census: PASS")
    print(f"new rows={len(order_six_basis)}; direct columns={columns}; "
          f"rank mod {filtered.PRIME}={len(pivots)}; "
          f"quotient={quotient_dimension}")
    print("full truncated dimensions: rows=57558; columns=96922")
    print(f"quotient ratio vs order5={quotient_dimension/order_five_quotient:.3f}x; "
          f"dimension*pivot proxy={workload_ratio:.3f}x")
    print(f"matrix sha256: {matrix_digest}")
    print("order-six membership/obstruction: NOT COMPUTED")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
