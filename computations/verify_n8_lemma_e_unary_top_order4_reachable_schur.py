#!/usr/bin/env python3
"""Exact reachable-tail Schur certificate through off-diagonal order four.

The order-at-most-three unary-top Macaulay block is onto.  Rather than form
the dense 25735-row extension directly, this checker first quotients the
order-four rows by columns whose minimum order is four, then transports the
low-block kernel tails into the resulting 157-dimensional quotient.

Modular ranks and 21 explicit integral left annihilators prove that the full
truncated integer matrix has rank exactly 25714 over Q.  The pure target
pairs to zero with all annihilators, so it belongs to the source column span
through order four.  This is not full ideal membership.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json

import verify_n8_lemma_e_unary_top_offdiagonal_filtered_lift as filtered


EXPECTED_MATRIX_DIGEST = "3e8dbdf007efba0e3cc489fb5f6d567a030a4b5c52cdc1beb972cd81ef5dd02e"
EXPECTED_COVECTOR_DIGEST = "56372be6439bbb30329207a9eaebe7285c0c5b2fb8f0719006a9fb5a7d3f9cee"
EXPECTED_LEDGER_DIGEST = "d32fe8dac31de82ecffd8878253e35ff01e9ce658939e41f886e015c73cf2ed8"
EXPECTED_COVECTOR_SUPPORTS = (
    24, 16, 16, 28, 26, 12, 24, 24, 24, 16, 24,
    48, 48, 16, 28, 24, 26, 12, 24, 48, 48,
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def canonical_bytes(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode()


def subtract_scaled(destination, scale, source):
    for row, coefficient in source.items():
        value = (
            destination.get(row, 0) - scale * coefficient
        ) % filtered.PRIME
        if value:
            destination[row] = value
        else:
            destination.pop(row, None)


def source_columns(generators):
    for vertices, word, label in generators:
        used_tokens = set(zip(vertices, word))
        complement = tuple(
            token for token in filtered.ALL_TOKENS
            if token not in used_tokens
        )
        terms = filtered.coefficient_terms(vertices, word)
        for multiplier in filtered.token_matchings(complement):
            monomials = tuple(
                tuple(sorted(term + multiplier)) for term in terms
            )
            orders = tuple(map(filtered.offdiagonal_order, monomials))
            yield label, multiplier, min(orders), monomials, orders


def quotient_remainder(vector, pivots):
    vector = dict(vector)
    for lead, pivot in sorted(pivots.items()):
        if lead in vector:
            subtract_scaled(vector, vector[lead], pivot)
    return vector


def main():
    all_monomials = filtered.token_matchings(filtered.ALL_TOKENS)
    low_basis = tuple(
        monomial for monomial in all_monomials
        if filtered.offdiagonal_order(monomial) <= 3
    )
    order_four_basis = tuple(
        monomial for monomial in all_monomials
        if filtered.offdiagonal_order(monomial) == 4
    )
    low_row = {monomial: index for index, monomial in enumerate(low_basis)}
    order_four_row = {
        monomial: index for index, monomial in enumerate(order_four_basis)
    }
    require(len(low_basis) == 11118, "the low basis count changed")
    require(len(order_four_basis) == 14617,
            "the order-four basis count changed")
    generators = filtered.build_generators()

    # Quotient the order-four block by columns with no lower terms.
    direct_pivots = {}
    direct_columns = 0
    for _, _, minimum, monomials, orders in source_columns(generators):
        if minimum != 4:
            continue
        entries = Counter(
            order_four_row[monomial]
            for monomial, order in zip(monomials, orders)
            if order == 4
        )
        vector = {
            row: value % filtered.PRIME
            for row, value in entries.items()
            if value % filtered.PRIME
        }
        direct_columns += 1
        filtered.reduce_column(vector, direct_pivots)
    require(direct_columns == 30812,
            f"the direct order-four column count changed: {direct_columns}")
    require(len(direct_pivots) == 14460,
            f"the direct order-four rank changed: {len(direct_pivots)}")
    free_order_four = tuple(
        row for row in range(len(order_four_basis))
        if row not in direct_pivots
    )
    require(len(free_order_four) == 157,
            "the direct order-four quotient dimension changed")
    quotient_index = {
        row: index for index, row in enumerate(free_order_four)
    }

    def order_four_quotient(entries):
        remainder = quotient_remainder(entries, direct_pivots)
        require(all(row in quotient_index for row in remainder),
                "a direct order-four pivot survived normal reduction")
        return {
            quotient_index[row]: value
            for row, value in remainder.items()
        }

    # Eliminate the low block and retain only its 157 quotient-tail
    # coordinates.  Dependent low columns give the reachable correction map.
    low_pivots = {}
    pivot_tails = {}
    reachable_pivots = {}
    low_columns = 0
    low_dependencies = 0
    for _, _, minimum, monomials, orders in source_columns(generators):
        if minimum > 3:
            continue
        low_entries = Counter(
            low_row[monomial]
            for monomial, order in zip(monomials, orders)
            if order <= 3
        )
        four_entries = Counter(
            order_four_row[monomial]
            for monomial, order in zip(monomials, orders)
            if order == 4
        )
        low_vector = {
            row: value % filtered.PRIME
            for row, value in low_entries.items()
            if value % filtered.PRIME
        }
        tail = order_four_quotient({
            row: value % filtered.PRIME
            for row, value in four_entries.items()
            if value % filtered.PRIME
        })
        low_columns += 1
        while low_vector:
            lead = min(low_vector)
            if lead not in low_pivots:
                inverse = pow(
                    low_vector[lead], filtered.PRIME - 2, filtered.PRIME
                )
                low_vector = {
                    row: value * inverse % filtered.PRIME
                    for row, value in low_vector.items()
                }
                tail = {
                    row: value * inverse % filtered.PRIME
                    for row, value in tail.items()
                }
                low_pivots[lead] = low_vector
                pivot_tails[lead] = tail
                break
            scale = low_vector[lead]
            subtract_scaled(low_vector, scale, low_pivots[lead])
            subtract_scaled(tail, scale, pivot_tails[lead])
        else:
            low_dependencies += 1
            filtered.reduce_column(tail, reachable_pivots)

    require(low_columns == 31182,
            f"the low column count changed: {low_columns}")
    require(len(low_pivots) == len(low_basis) == 11118,
            f"the low block lost surjectivity: {len(low_pivots)}")
    require(low_dependencies == 20064,
            f"the low-kernel column count changed: {low_dependencies}")
    require(len(reachable_pivots) == 136,
            f"the reachable order-four rank changed: {len(reachable_pivots)}")

    # Transport the target through the same low graph and reachable quotient.
    target = filtered.target_vector(low_row)
    target_tail = {}
    while target:
        lead = min(target)
        require(lead in low_pivots,
                f"the target found a missing low pivot {lead}")
        scale = target[lead]
        subtract_scaled(target, scale, low_pivots[lead])
        subtract_scaled(target_tail, scale, pivot_tails[lead])
    target_tail_terms = len(target_tail)
    target_remainder = quotient_remainder(target_tail, reachable_pivots)
    require(target_tail_terms == 148,
            f"the transported target tail changed: {target_tail_terms}")
    require(not target_remainder,
            "the target acquired an order-four Schur obstruction mod prime")

    # Reconstruct the 21 full left annihilators.  The reachable quotient
    # annihilator first lifts across the direct order-four pivots and then
    # uniquely across the surjective low block.
    free_reachable = tuple(
        row for row in range(len(free_order_four))
        if row not in reachable_pivots
    )
    require(len(free_reachable) == 21,
            "the final Schur cokernel dimension changed")
    covectors = []
    for free_row in free_reachable:
        quotient_covector = {free_row: 1}
        for lead in sorted(reachable_pivots, reverse=True):
            value = -sum(
                coefficient * quotient_covector.get(row, 0)
                for row, coefficient in reachable_pivots[lead].items()
                if row != lead
            ) % filtered.PRIME
            if value:
                quotient_covector[lead] = value

        order_four_covector = {
            free_order_four[index]: value
            for index, value in quotient_covector.items()
        }
        for lead in sorted(direct_pivots, reverse=True):
            value = -sum(
                coefficient * order_four_covector.get(row, 0)
                for row, coefficient in direct_pivots[lead].items()
                if row != lead
            ) % filtered.PRIME
            if value:
                order_four_covector[lead] = value

        low_covector = {}
        for lead in sorted(low_pivots, reverse=True):
            value = -sum(
                coefficient * low_covector.get(row, 0)
                for row, coefficient in low_pivots[lead].items()
                if row != lead
            )
            value -= sum(
                coefficient * quotient_covector.get(row, 0)
                for row, coefficient in pivot_tails[lead].items()
            )
            value %= filtered.PRIME
            if value:
                low_covector[lead] = value

        def centered(value):
            return value if value <= filtered.PRIME // 2 else value - filtered.PRIME

        integral_low = {
            row: centered(value) for row, value in low_covector.items()
        }
        integral_four = {
            row: centered(value)
            for row, value in order_four_covector.items()
        }
        require(set(integral_low.values()) <= {-1, 1}
                and set(integral_four.values()) <= {-1, 1},
                "a Schur covector did not reconstruct over ZZ")
        covectors.append((integral_low, integral_four))

    supports = tuple(
        len(low) + len(four) for low, four in covectors
    )
    require(supports == EXPECTED_COVECTOR_SUPPORTS,
            f"the integral covector supports changed: {supports}")

    # Freeze the complete truncated matrix and verify annihilation over ZZ.
    matrix_hash = sha256(canonical_bytes({
        "low_basis": low_basis,
        "order_four_basis": order_four_basis,
    }))
    truncated_columns = 0
    for label, multiplier, minimum, monomials, orders in source_columns(generators):
        if minimum > 4:
            continue
        low_entries = Counter(
            low_row[monomial]
            for monomial, order in zip(monomials, orders)
            if order <= 3
        )
        four_entries = Counter(
            order_four_row[monomial]
            for monomial, order in zip(monomials, orders)
            if order == 4
        )
        truncated_columns += 1
        matrix_hash.update(canonical_bytes((
            truncated_columns,
            label,
            multiplier,
            tuple(sorted(low_entries.items())),
            tuple(sorted(four_entries.items())),
        )))
        for index, (low_covector, four_covector) in enumerate(covectors):
            pairing = sum(
                coefficient * low_covector.get(row, 0)
                for row, coefficient in low_entries.items()
            )
            pairing += sum(
                coefficient * four_covector.get(row, 0)
                for row, coefficient in four_entries.items()
            )
            require(pairing == 0,
                    f"column {truncated_columns} pairs {pairing} with "
                    f"integral covector {index}")
    require(truncated_columns == 61994,
            f"the truncated column count changed: {truncated_columns}")

    integral_target = filtered.target_vector(low_row)
    for index, (low_covector, _) in enumerate(covectors):
        pairing = sum(
            coefficient * low_covector.get(row, 0)
            for row, coefficient in integral_target.items()
        )
        require(pairing == 0,
                f"the target pairs {pairing} with integral covector {index}")

    matrix_digest = matrix_hash.hexdigest()
    covector_payload = tuple(
        (tuple(sorted(low.items())), tuple(sorted(four.items())))
        for low, four in covectors
    )
    covector_digest = sha256(canonical_bytes(covector_payload)).hexdigest()
    if EXPECTED_MATRIX_DIGEST != "TO_BE_FILLED":
        require(matrix_digest == EXPECTED_MATRIX_DIGEST,
                f"the truncated matrix changed: {matrix_digest}")
    if EXPECTED_COVECTOR_DIGEST != "TO_BE_FILLED":
        require(covector_digest == EXPECTED_COVECTOR_DIGEST,
                f"the integral cokernel changed: {covector_digest}")

    total_rows = len(low_basis) + len(order_four_basis)
    rank = len(low_pivots) + len(direct_pivots) + len(reachable_pivots)
    require(total_rows == 25735 and rank == 25714,
            f"the total Schur rank changed: {rank}/{total_rows}")
    ledger = {
        "rows": total_rows,
        "columns": truncated_columns,
        "rank_over_Q": rank,
        "cokernel_over_Q": len(covectors),
        "direct_order_four_rank": len(direct_pivots),
        "direct_order_four_cokernel": len(free_order_four),
        "reachable_tail_rank": len(reachable_pivots),
        "target_tail_terms_before_reachable_reduction": target_tail_terms,
        "target_remainder_terms": len(target_remainder),
        "integral_cokernel_supports": supports,
        "matrix_sha256": matrix_digest,
        "integral_cokernel_sha256": covector_digest,
        "verdict": (
            "the concentrated unary-top target belongs to the literal "
            "source span through off-diagonal order four over Q"
        ),
        "scope": (
            "all 135 internal cells and concentrated holes (01),(23), modulo "
            "terms with at least five off-diagonal cells; no full ideal or "
            "multisite-star conclusion"
        ),
    }
    digest = sha256(canonical_bytes(ledger)).hexdigest()
    if EXPECTED_LEDGER_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_DIGEST,
                f"the order-four Schur ledger changed: {digest}")

    print("N=8 unary-top reachable order-four Schur lift: PASS")
    print(f"rows={total_rows}; columns={truncated_columns}; "
          f"rank over Q={rank}; cokernel={len(covectors)}")
    print("direct order-four rank=14460/14617; reachable quotient rank=136/157")
    print(f"target quotient tail terms={target_tail_terms}; remainder=0")
    print(f"integral covector supports: {supports}")
    print(f"matrix sha256: {matrix_digest}")
    print(f"integral cokernel sha256: {covector_digest}")
    print("orders five through seven and multisite stars: OPEN")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
