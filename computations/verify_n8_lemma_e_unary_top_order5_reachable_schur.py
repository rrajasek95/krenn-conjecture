#!/usr/bin/env python3
"""Exact reachable-tail Schur certificate through off-diagonal order five.

This extends the order-four Schur graph by carrying only the quotient of the
order-five rows by minimum-order-five source columns.  Exact modular pivots
and 85 reconstructed integral left annihilators prove the full truncated
rank over Q and target membership.  Orders six and seven remain open.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json

import verify_n8_lemma_e_unary_top_offdiagonal_filtered_lift as filtered
import verify_n8_lemma_e_unary_top_order4_reachable_schur as order_four


EXPECTED_MATRIX_DIGEST = "b3aa200868fe0b2bb2268253b14eea43544f1e38629cf1d1ee638fe9725c29c7"
EXPECTED_COVECTOR_DIGEST = "3f34028ebf06ff1ee286d176e0bb8b5dbea9a16c33aee9bd82971d9f384e98a9"
EXPECTED_LEDGER_DIGEST = "5014b520ee5396b8505ae478aed1bbe33f3d042e094ef7d20a626b553354a569"
EXPECTED_INHERITED_SUPPORTS = (
    24, 16, 16, 28, 26, 12, 24, 24, 24, 16, 24,
    48, 48, 16, 28, 24, 26, 12, 24, 48, 48,
)
EXPECTED_NEW_SUPPORTS = (
    13, 43, 17, 25, 13, 13, 28, 41, 28, 25, 28, 28, 27, 25, 39, 20,
    28, 21, 20, 17, 27, 35, 28, 17, 13, 28, 21, 16, 16, 28, 26, 12,
    13, 43, 17, 25, 13, 13, 28, 41, 28, 25, 28, 16, 28, 27, 25, 39,
    20, 28, 21, 16, 20, 28, 17, 27, 35, 28, 17, 13, 26, 28, 12, 21,
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def canonical_bytes(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode()


def normalize(vector, *tails):
    lead = min(vector)
    inverse = pow(vector[lead], filtered.PRIME - 2, filtered.PRIME)
    normalized = {
        row: value * inverse % filtered.PRIME
        for row, value in vector.items()
    }
    normalized_tails = tuple({
        row: value * inverse % filtered.PRIME
        for row, value in tail.items()
    } for tail in tails)
    return (normalized,) + normalized_tails


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
    order_five_basis = tuple(
        monomial for monomial in all_monomials
        if filtered.offdiagonal_order(monomial) == 5
    )
    low_row = {monomial: index for index, monomial in enumerate(low_basis)}
    four_row = {
        monomial: index for index, monomial in enumerate(order_four_basis)
    }
    five_row = {
        monomial: index for index, monomial in enumerate(order_five_basis)
    }
    require((len(low_basis), len(order_four_basis), len(order_five_basis))
            == (11118, 14617, 18988), "the filtered basis counts changed")
    generators = filtered.build_generators()

    # Minimum-order-five columns give the first quotient.
    five_pivots = {}
    direct_five_columns = 0
    for _, _, minimum, monomials, orders in order_four.source_columns(generators):
        if minimum != 5:
            continue
        entries = Counter(
            five_row[monomial]
            for monomial, value in zip(monomials, orders)
            if value == 5
        )
        vector = {
            row: value % filtered.PRIME for row, value in entries.items()
        }
        direct_five_columns += 1
        filtered.reduce_column(vector, five_pivots)
    require(direct_five_columns == 26452,
            f"the direct order-five columns changed: {direct_five_columns}")
    require(len(five_pivots) == 18040,
            f"the direct order-five rank changed: {len(five_pivots)}")
    free_five = tuple(
        row for row in range(len(order_five_basis))
        if row not in five_pivots
    )
    require(len(free_five) == 948,
            "the direct order-five quotient dimension changed")
    five_quotient_index = {
        row: index for index, row in enumerate(free_five)
    }

    def five_quotient(entries):
        remainder = order_four.quotient_remainder(entries, five_pivots)
        require(all(row in five_quotient_index for row in remainder),
                "a direct order-five pivot survived reduction")
        return {
            five_quotient_index[row]: value
            for row, value in remainder.items()
        }

    # Eliminate minimum-order-four columns, carrying their order-five tails.
    four_pivots = {}
    four_pivot_tails = {}
    reachable_five_pivots = {}
    direct_four_columns = 0
    direct_four_dependencies = 0
    for _, _, minimum, monomials, orders in order_four.source_columns(generators):
        if minimum != 4:
            continue
        four = Counter(
            four_row[monomial]
            for monomial, value in zip(monomials, orders)
            if value == 4
        )
        five = Counter(
            five_row[monomial]
            for monomial, value in zip(monomials, orders)
            if value == 5
        )
        four = {
            row: value % filtered.PRIME for row, value in four.items()
        }
        five = five_quotient({
            row: value % filtered.PRIME for row, value in five.items()
        })
        direct_four_columns += 1
        while four:
            lead = min(four)
            if lead not in four_pivots:
                four, five = normalize(four, five)
                four_pivots[lead] = four
                four_pivot_tails[lead] = five
                break
            scale = four[lead]
            order_four.subtract_scaled(four, scale, four_pivots[lead])
            order_four.subtract_scaled(
                five, scale, four_pivot_tails[lead]
            )
        else:
            direct_four_dependencies += 1
            filtered.reduce_column(five, reachable_five_pivots)
    require(direct_four_columns == 30812,
            f"the direct order-four columns changed: {direct_four_columns}")
    require(len(four_pivots) == 14460,
            f"the direct order-four rank changed: {len(four_pivots)}")
    require(direct_four_dependencies == 16352,
            "the direct order-four dependency count changed")
    free_four = tuple(
        row for row in range(len(order_four_basis))
        if row not in four_pivots
    )
    require(len(free_four) == 157,
            "the direct order-four quotient dimension changed")
    four_quotient_index = {
        row: index for index, row in enumerate(free_four)
    }

    def reduce_four(four, five):
        for lead, pivot in sorted(four_pivots.items()):
            if lead not in four:
                continue
            scale = four[lead]
            order_four.subtract_scaled(four, scale, pivot)
            order_four.subtract_scaled(
                five, scale, four_pivot_tails[lead]
            )
        require(all(row in four_quotient_index for row in four),
                "a direct order-four pivot survived reduction")
        return ({
            four_quotient_index[row]: value
            for row, value in four.items()
        }, five)

    # Replay the low graph, carrying both quotient tails.  Full low
    # dependencies first generate the reachable order-four pivots; their
    # dependencies then enlarge the reachable order-five image.
    low_pivots = {}
    low_four_tails = {}
    low_five_tails = {}
    reachable_four_pivots = {}
    reachable_four_five_tails = {}
    low_columns = 0
    low_dependencies = 0
    for _, _, minimum, monomials, orders in order_four.source_columns(generators):
        if minimum > 3:
            continue
        low = Counter(
            low_row[monomial]
            for monomial, value in zip(monomials, orders)
            if value <= 3
        )
        four = Counter(
            four_row[monomial]
            for monomial, value in zip(monomials, orders)
            if value == 4
        )
        five = Counter(
            five_row[monomial]
            for monomial, value in zip(monomials, orders)
            if value == 5
        )
        low = {row: value % filtered.PRIME for row, value in low.items()}
        four = {row: value % filtered.PRIME for row, value in four.items()}
        five = five_quotient({
            row: value % filtered.PRIME for row, value in five.items()
        })
        four, five = reduce_four(four, five)
        low_columns += 1
        while low:
            lead = min(low)
            if lead not in low_pivots:
                low, four, five = normalize(low, four, five)
                low_pivots[lead] = low
                low_four_tails[lead] = four
                low_five_tails[lead] = five
                break
            scale = low[lead]
            order_four.subtract_scaled(low, scale, low_pivots[lead])
            order_four.subtract_scaled(
                four, scale, low_four_tails[lead]
            )
            order_four.subtract_scaled(
                five, scale, low_five_tails[lead]
            )
        else:
            low_dependencies += 1
            while four:
                lead = min(four)
                if lead not in reachable_four_pivots:
                    four, five = normalize(four, five)
                    reachable_four_pivots[lead] = four
                    reachable_four_five_tails[lead] = five
                    break
                scale = four[lead]
                order_four.subtract_scaled(
                    four, scale, reachable_four_pivots[lead]
                )
                order_four.subtract_scaled(
                    five, scale, reachable_four_five_tails[lead]
                )
            else:
                filtered.reduce_column(five, reachable_five_pivots)

    require(low_columns == 31182 and len(low_pivots) == 11118,
            f"the low block changed: {low_columns}/{len(low_pivots)}")
    require(low_dependencies == 20064,
            "the low dependency count changed")
    require(len(reachable_four_pivots) == 136,
            f"the reachable order-four rank changed: "
            f"{len(reachable_four_pivots)}")
    require(len(reachable_five_pivots) == 884,
            f"the reachable order-five rank changed: "
            f"{len(reachable_five_pivots)}")

    # Transport the particular target.
    target = filtered.target_vector(low_row)
    target_four = {}
    target_five = {}
    while target:
        lead = min(target)
        scale = target[lead]
        order_four.subtract_scaled(target, scale, low_pivots[lead])
        order_four.subtract_scaled(
            target_four, scale, low_four_tails[lead]
        )
        order_four.subtract_scaled(
            target_five, scale, low_five_tails[lead]
        )
    while target_four:
        lead = min(target_four)
        require(lead in reachable_four_pivots,
                f"the target acquired an order-four remainder at {lead}")
        scale = target_four[lead]
        order_four.subtract_scaled(
            target_four, scale, reachable_four_pivots[lead]
        )
        order_four.subtract_scaled(
            target_five, scale, reachable_four_five_tails[lead]
        )
    target_five_terms = len(target_five)
    target_remainder = order_four.quotient_remainder(
        target_five, reachable_five_pivots
    )
    require(target_five_terms == 939,
            f"the transported order-five target changed: {target_five_terms}")
    require(not target_remainder,
            "the target acquired an order-five Schur obstruction mod prime")

    free_reachable_four = tuple(
        row for row in range(len(free_four))
        if row not in reachable_four_pivots
    )
    free_reachable_five = tuple(
        row for row in range(len(free_five))
        if row not in reachable_five_pivots
    )
    require((len(free_reachable_four), len(free_reachable_five)) == (21, 64),
            "the inherited/new cokernel split changed")

    def build_covector(free_four_row=None, free_five_row=None):
        quotient_five = {}
        if free_five_row is not None:
            quotient_five[free_five_row] = 1
        for lead in sorted(reachable_five_pivots, reverse=True):
            value = -sum(
                coefficient * quotient_five.get(row, 0)
                for row, coefficient in reachable_five_pivots[lead].items()
                if row != lead
            ) % filtered.PRIME
            if value:
                quotient_five[lead] = value

        quotient_four = {}
        if free_four_row is not None:
            quotient_four[free_four_row] = 1
        for lead in sorted(reachable_four_pivots, reverse=True):
            value = -sum(
                coefficient * quotient_four.get(row, 0)
                for row, coefficient in reachable_four_pivots[lead].items()
                if row != lead
            )
            value -= sum(
                coefficient * quotient_five.get(row, 0)
                for row, coefficient
                in reachable_four_five_tails[lead].items()
            )
            value %= filtered.PRIME
            if value:
                quotient_four[lead] = value

        literal_five = {
            free_five[index]: value
            for index, value in quotient_five.items()
        }
        for lead in sorted(five_pivots, reverse=True):
            value = -sum(
                coefficient * literal_five.get(row, 0)
                for row, coefficient in five_pivots[lead].items()
                if row != lead
            ) % filtered.PRIME
            if value:
                literal_five[lead] = value

        literal_four = {
            free_four[index]: value
            for index, value in quotient_four.items()
        }
        for lead in sorted(four_pivots, reverse=True):
            value = -sum(
                coefficient * literal_four.get(row, 0)
                for row, coefficient in four_pivots[lead].items()
                if row != lead
            )
            value -= sum(
                coefficient * quotient_five.get(row, 0)
                for row, coefficient in four_pivot_tails[lead].items()
            )
            value %= filtered.PRIME
            if value:
                literal_four[lead] = value

        literal_low = {}
        for lead in sorted(low_pivots, reverse=True):
            value = -sum(
                coefficient * literal_low.get(row, 0)
                for row, coefficient in low_pivots[lead].items()
                if row != lead
            )
            value -= sum(
                coefficient * quotient_four.get(row, 0)
                for row, coefficient in low_four_tails[lead].items()
            )
            value -= sum(
                coefficient * quotient_five.get(row, 0)
                for row, coefficient in low_five_tails[lead].items()
            )
            value %= filtered.PRIME
            if value:
                literal_low[lead] = value

        def centered(value):
            return value if value <= filtered.PRIME // 2 else value - filtered.PRIME

        result = tuple({
            row: centered(value) for row, value in packet.items()
        } for packet in (literal_low, literal_four, literal_five))
        require(all(set(packet.values()) <= {-1, 1} for packet in result),
                "an order-five cokernel vector did not reconstruct over ZZ")
        return result

    inherited_covectors = tuple(
        build_covector(free_four_row=row)
        for row in free_reachable_four
    )
    new_covectors = tuple(
        build_covector(free_five_row=row)
        for row in free_reachable_five
    )
    inherited_supports = tuple(
        sum(map(len, covector)) for covector in inherited_covectors
    )
    new_supports = tuple(
        sum(map(len, covector)) for covector in new_covectors
    )
    require(inherited_supports == EXPECTED_INHERITED_SUPPORTS,
            f"the inherited cokernel supports changed: {inherited_supports}")
    require(new_supports == EXPECTED_NEW_SUPPORTS,
            f"the new cokernel supports changed: {new_supports}")
    covectors = inherited_covectors + new_covectors

    matrix_hash = sha256(canonical_bytes({
        "low_basis": low_basis,
        "order_four_basis": order_four_basis,
        "order_five_basis": order_five_basis,
    }))
    truncated_columns = 0
    for label, multiplier, minimum, monomials, orders in order_four.source_columns(
        generators
    ):
        if minimum > 5:
            continue
        low_entries = Counter(
            low_row[monomial]
            for monomial, value in zip(monomials, orders)
            if value <= 3
        )
        four_entries = Counter(
            four_row[monomial]
            for monomial, value in zip(monomials, orders)
            if value == 4
        )
        five_entries = Counter(
            five_row[monomial]
            for monomial, value in zip(monomials, orders)
            if value == 5
        )
        truncated_columns += 1
        matrix_hash.update(canonical_bytes((
            truncated_columns, label, multiplier,
            tuple(sorted(low_entries.items())),
            tuple(sorted(four_entries.items())),
            tuple(sorted(five_entries.items())),
        )))
        for index, (low_covector, four_covector, five_covector) in enumerate(
            covectors
        ):
            pairing = sum(
                value * low_covector.get(row, 0)
                for row, value in low_entries.items()
            )
            pairing += sum(
                value * four_covector.get(row, 0)
                for row, value in four_entries.items()
            )
            pairing += sum(
                value * five_covector.get(row, 0)
                for row, value in five_entries.items()
            )
            require(pairing == 0,
                    f"column {truncated_columns} pairs {pairing} with "
                    f"integral covector {index}")
    require(truncated_columns == 88446,
            f"the order-five truncated columns changed: {truncated_columns}")

    integral_target = filtered.target_vector(low_row)
    for index, (low_covector, _, _) in enumerate(covectors):
        pairing = sum(
            value * low_covector.get(row, 0)
            for row, value in integral_target.items()
        )
        require(pairing == 0,
                f"the target pairs {pairing} with integral covector {index}")

    matrix_digest = matrix_hash.hexdigest()
    covector_payload = tuple(
        tuple(tuple(sorted(packet.items())) for packet in covector)
        for covector in covectors
    )
    covector_digest = sha256(canonical_bytes(covector_payload)).hexdigest()
    if EXPECTED_MATRIX_DIGEST != "TO_BE_FILLED":
        require(matrix_digest == EXPECTED_MATRIX_DIGEST,
                f"the order-five matrix changed: {matrix_digest}")
    if EXPECTED_COVECTOR_DIGEST != "TO_BE_FILLED":
        require(covector_digest == EXPECTED_COVECTOR_DIGEST,
                f"the order-five integral cokernel changed: {covector_digest}")

    total_rows = len(low_basis) + len(order_four_basis) + len(order_five_basis)
    rank = (
        len(low_pivots) + len(four_pivots) + len(reachable_four_pivots)
        + len(five_pivots) + len(reachable_five_pivots)
    )
    require((total_rows, rank, len(covectors)) == (44723, 44638, 85),
            f"the full order-five rank/cokernel changed: "
            f"{rank}/{total_rows}/{len(covectors)}")
    ledger = {
        "rows": total_rows,
        "columns": truncated_columns,
        "rank_over_Q": rank,
        "cokernel_over_Q": len(covectors),
        "direct_order_five_rank": len(five_pivots),
        "direct_order_five_cokernel": len(free_five),
        "reachable_order_five_rank": len(reachable_five_pivots),
        "inherited_cokernel_dimension": len(inherited_covectors),
        "new_cokernel_dimension": len(new_covectors),
        "target_tail_terms_before_reachable_reduction": target_five_terms,
        "target_remainder_terms": len(target_remainder),
        "inherited_integral_cokernel_supports": inherited_supports,
        "new_integral_cokernel_supports": new_supports,
        "matrix_sha256": matrix_digest,
        "integral_cokernel_sha256": covector_digest,
        "verdict": (
            "the concentrated unary-top target belongs to the literal "
            "source span through off-diagonal order five over Q"
        ),
        "scope": (
            "all 135 internal cells and concentrated holes (01),(23), modulo "
            "terms with at least six off-diagonal cells; no full ideal or "
            "multisite-star conclusion"
        ),
    }
    digest = sha256(canonical_bytes(ledger)).hexdigest()
    if EXPECTED_LEDGER_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_DIGEST,
                f"the order-five Schur ledger changed: {digest}")

    print("N=8 unary-top reachable order-five Schur lift: PASS")
    print(f"rows={total_rows}; columns={truncated_columns}; "
          f"rank over Q={rank}; cokernel={len(covectors)}")
    print("direct order-five rank=18040/18988; reachable quotient rank=884/948")
    print(f"target quotient tail terms={target_five_terms}; remainder=0")
    print(f"cokernel split: inherited={len(inherited_covectors)}; "
          f"new={len(new_covectors)}")
    print(f"matrix sha256: {matrix_digest}")
    print(f"integral cokernel sha256: {covector_digest}")
    print("orders six and seven and multisite stars: OPEN")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
