#!/usr/bin/env python3
"""Exact provenance-closure guard for the particular order-six target tail.

Rebuild the certified order-at-most-five filtered elimination, recording only
an acyclic source-provenance recipe for each pivot.  Back-substitute the pure
target and compute the transitive closure of the pivot recipes it uses.  The
closure is essentially the full upstream graph, so a supposedly
support-restricted order-six tail evaluation would not be bounded.  No
order-six quotient vectors are evaluated here.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json

import verify_n8_lemma_e_unary_top_offdiagonal_filtered_lift as filtered
import verify_n8_lemma_e_unary_top_order4_reachable_schur as schur


EXPECTED_RECIPE_DIGEST = "96428a5a2a800fdefdcd79a6d9f0f37dbd063d137f4b6cb8d240e4e97a469f57"
EXPECTED_LEDGER_DIGEST = "b2f2811438615cfa3ddc564625493b225fdd88bf86a895d1054a0e8cbf2c7200"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def canonical_bytes(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode()


def source_columns(generators):
    for column_id, packet in enumerate(schur.source_columns(generators), 1):
        yield (column_id,) + packet


def normalize(vector, *tails):
    inverse = pow(vector[min(vector)], filtered.PRIME - 2, filtered.PRIME)
    packets = (vector,) + tails
    return inverse, tuple({
        row: value * inverse % filtered.PRIME
        for row, value in packet.items()
    } for packet in packets)


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

    # A recipe is inverse * (raw column - sum scale * earlier pivot recipe).
    # Node identifiers therefore form a topological order.
    recipes = []

    def make_recipe(raw_column, inverse, edges):
        require(all(node < len(recipes) for node, _ in edges),
                "a provenance edge is not acyclic")
        recipes.append((raw_column, inverse, tuple(edges)))
        return len(recipes) - 1

    # Direct order-five pivots.
    five_pivots = {}
    five_nodes = {}
    for column_id, _, _, minimum, monomials, orders in source_columns(generators):
        if minimum != 5:
            continue
        vector = Counter(
            five_row[monomial]
            for monomial, order in zip(monomials, orders)
            if order == 5
        )
        vector = {
            row: value % filtered.PRIME for row, value in vector.items()
        }
        edges = []
        while vector:
            lead = min(vector)
            if lead not in five_pivots:
                inverse, (vector,) = normalize(vector)
                node = make_recipe(column_id, inverse, edges)
                five_pivots[lead] = vector
                five_nodes[lead] = node
                break
            scale = vector[lead]
            schur.subtract_scaled(vector, scale, five_pivots[lead])
            edges.append((five_nodes[lead], scale))
    require(len(five_pivots) == 18040,
            f"the direct order-five pivot count changed: {len(five_pivots)}")
    free_five = tuple(
        row for row in range(len(order_five_basis))
        if row not in five_pivots
    )
    five_quotient_index = {
        row: index for index, row in enumerate(free_five)
    }

    def reduce_five(vector, edges):
        for lead, pivot in sorted(five_pivots.items()):
            if lead not in vector:
                continue
            scale = vector[lead]
            schur.subtract_scaled(vector, scale, pivot)
            edges.append((five_nodes[lead], scale))
        require(all(row in five_quotient_index for row in vector),
                "a direct order-five pivot survived reduction")
        return {
            five_quotient_index[row]: value for row, value in vector.items()
        }

    # Direct order-four pivots and their dependent reachable-five pivots.
    four_pivots = {}
    four_nodes = {}
    four_five_tails = {}
    reachable_five_pivots = {}
    reachable_five_nodes = {}
    for column_id, _, _, minimum, monomials, orders in source_columns(generators):
        if minimum != 4:
            continue
        four = Counter(
            four_row[monomial]
            for monomial, order in zip(monomials, orders)
            if order == 4
        )
        five = Counter(
            five_row[monomial]
            for monomial, order in zip(monomials, orders)
            if order == 5
        )
        four = {row: value % filtered.PRIME for row, value in four.items()}
        five = {row: value % filtered.PRIME for row, value in five.items()}
        edges = []
        five = reduce_five(five, edges)
        while four:
            lead = min(four)
            if lead not in four_pivots:
                inverse, (four, five) = normalize(four, five)
                node = make_recipe(column_id, inverse, edges)
                four_pivots[lead] = four
                four_five_tails[lead] = five
                four_nodes[lead] = node
                break
            scale = four[lead]
            schur.subtract_scaled(four, scale, four_pivots[lead])
            schur.subtract_scaled(five, scale, four_five_tails[lead])
            edges.append((four_nodes[lead], scale))
        else:
            while five:
                lead = min(five)
                if lead not in reachable_five_pivots:
                    inverse, (five,) = normalize(five)
                    node = make_recipe(column_id, inverse, edges)
                    reachable_five_pivots[lead] = five
                    reachable_five_nodes[lead] = node
                    break
                scale = five[lead]
                schur.subtract_scaled(
                    five, scale, reachable_five_pivots[lead]
                )
                edges.append((reachable_five_nodes[lead], scale))
    require(len(four_pivots) == 14460,
            f"the direct order-four pivot count changed: {len(four_pivots)}")
    require(len(reachable_five_pivots) == 842,
            "the direct-four reachable-five pivot count changed")
    free_four = tuple(
        row for row in range(len(order_four_basis))
        if row not in four_pivots
    )
    four_quotient_index = {
        row: index for index, row in enumerate(free_four)
    }

    def reduce_four(four, five, edges):
        for lead, pivot in sorted(four_pivots.items()):
            if lead not in four:
                continue
            scale = four[lead]
            schur.subtract_scaled(four, scale, pivot)
            schur.subtract_scaled(five, scale, four_five_tails[lead])
            edges.append((four_nodes[lead], scale))
        require(all(row in four_quotient_index for row in four),
                "a direct order-four pivot survived reduction")
        return ({
            four_quotient_index[row]: value for row, value in four.items()
        }, five)

    # Low pivots and the remaining reachable-four/reachable-five graph.
    low_pivots = {}
    low_nodes = {}
    low_four_tails = {}
    low_five_tails = {}
    reachable_four_pivots = {}
    reachable_four_nodes = {}
    reachable_four_five_tails = {}
    final_low_kernel_relations = 0
    for column_id, _, _, minimum, monomials, orders in source_columns(generators):
        if minimum > 3:
            continue
        low = Counter(
            low_row[monomial]
            for monomial, order in zip(monomials, orders)
            if order <= 3
        )
        four = Counter(
            four_row[monomial]
            for monomial, order in zip(monomials, orders)
            if order == 4
        )
        five = Counter(
            five_row[monomial]
            for monomial, order in zip(monomials, orders)
            if order == 5
        )
        low = {row: value % filtered.PRIME for row, value in low.items()}
        four = {row: value % filtered.PRIME for row, value in four.items()}
        five = {row: value % filtered.PRIME for row, value in five.items()}
        edges = []
        five = reduce_five(five, edges)
        four, five = reduce_four(four, five, edges)
        while low:
            lead = min(low)
            if lead not in low_pivots:
                inverse, (low, four, five) = normalize(low, four, five)
                node = make_recipe(column_id, inverse, edges)
                low_pivots[lead] = low
                low_four_tails[lead] = four
                low_five_tails[lead] = five
                low_nodes[lead] = node
                break
            scale = low[lead]
            schur.subtract_scaled(low, scale, low_pivots[lead])
            schur.subtract_scaled(four, scale, low_four_tails[lead])
            schur.subtract_scaled(five, scale, low_five_tails[lead])
            edges.append((low_nodes[lead], scale))
        else:
            while four:
                lead = min(four)
                if lead not in reachable_four_pivots:
                    inverse, (four, five) = normalize(four, five)
                    node = make_recipe(column_id, inverse, edges)
                    reachable_four_pivots[lead] = four
                    reachable_four_five_tails[lead] = five
                    reachable_four_nodes[lead] = node
                    break
                scale = four[lead]
                schur.subtract_scaled(
                    four, scale, reachable_four_pivots[lead]
                )
                schur.subtract_scaled(
                    five, scale, reachable_four_five_tails[lead]
                )
                edges.append((reachable_four_nodes[lead], scale))
            else:
                while five:
                    lead = min(five)
                    if lead not in reachable_five_pivots:
                        inverse, (five,) = normalize(five)
                        node = make_recipe(column_id, inverse, edges)
                        reachable_five_pivots[lead] = five
                        reachable_five_nodes[lead] = node
                        break
                    scale = five[lead]
                    schur.subtract_scaled(
                        five, scale, reachable_five_pivots[lead]
                    )
                    edges.append((reachable_five_nodes[lead], scale))
                else:
                    final_low_kernel_relations += 1

    require((len(low_pivots), len(reachable_four_pivots),
             len(reachable_five_pivots), len(recipes))
            == (11118, 136, 884, 44638),
            "the order-five provenance graph dimensions changed")
    require(final_low_kernel_relations == 19886,
            f"the final low-kernel relation count changed: "
            f"{final_low_kernel_relations}")

    # Back-substitute the target, recording only pivot recipe use.
    target = filtered.target_vector(low_row)
    target_four = {}
    target_five = {}
    target_edges = []
    while target:
        lead = min(target)
        scale = target[lead]
        schur.subtract_scaled(target, scale, low_pivots[lead])
        schur.subtract_scaled(target_four, scale, low_four_tails[lead])
        schur.subtract_scaled(target_five, scale, low_five_tails[lead])
        target_edges.append((low_nodes[lead], scale))
    while target_four:
        lead = min(target_four)
        scale = target_four[lead]
        schur.subtract_scaled(
            target_four, scale, reachable_four_pivots[lead]
        )
        schur.subtract_scaled(
            target_five, scale, reachable_four_five_tails[lead]
        )
        target_edges.append((reachable_four_nodes[lead], scale))
    while target_five:
        lead = min(target_five)
        scale = target_five[lead]
        schur.subtract_scaled(
            target_five, scale, reachable_five_pivots[lead]
        )
        target_edges.append((reachable_five_nodes[lead], scale))
    require(len(target_edges) == 6865,
            f"the target pivot-use count changed: {len(target_edges)}")

    closure = set()
    stack = [node for node, _ in target_edges]
    while stack:
        node = stack.pop()
        if node in closure:
            continue
        closure.add(node)
        stack.extend(dependency for dependency, _ in recipes[node][2])
    raw_columns = {recipes[node][0] for node in closure}
    require(len(closure) == len(raw_columns) == 44203,
            f"the target closure changed: {len(closure)}/{len(raw_columns)}")

    recipe_hash = sha256()
    for index, recipe in enumerate(recipes):
        recipe_hash.update(canonical_bytes((index, recipe)))
    recipe_hash.update(canonical_bytes(("target", tuple(target_edges))))
    recipe_digest = recipe_hash.hexdigest()
    if EXPECTED_RECIPE_DIGEST != "TO_BE_FILLED":
        require(recipe_digest == EXPECTED_RECIPE_DIGEST,
                f"the target provenance graph changed: {recipe_digest}")
    ledger = {
        "upstream_pivots": len(recipes),
        "target_pivot_terms": len(target_edges),
        "target_closure_nodes": len(closure),
        "target_closure_raw_columns": len(raw_columns),
        "target_closure_fraction": len(closure) / len(recipes),
        "order_six_direct_quotient_coordinates_mod_prime": 4917,
        "final_low_kernel_relations_not_expanded": final_low_kernel_relations,
        "recipe_sha256": recipe_digest,
        "verdict": (
            "the particular target provenance closure is essentially the "
            "full order-at-most-five pivot graph; stop before lazy order-six "
            "quotient evaluation"
        ),
        "scope": (
            "exact finite-field provenance closure only; no order-six target "
            "tail, membership, obstruction, or rational-rank conclusion"
        ),
    }
    digest = sha256(canonical_bytes(ledger)).hexdigest()
    if EXPECTED_LEDGER_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_DIGEST,
                f"the target closure ledger changed: {digest}")

    print("N=8 unary-top order-six target closure frontier: PASS")
    print(f"upstream pivots={len(recipes)}; target pivot terms="
          f"{len(target_edges)}")
    print(f"target closure nodes/raw columns={len(closure)}/{len(raw_columns)} "
          f"({100*len(closure)/len(recipes):.2f}% of pivots)")
    print("order-six quotient coordinates=4917; tail NOT EVALUATED")
    print(f"recipe sha256: {recipe_digest}")
    print("order-six membership/obstruction: NOT COMPUTED")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
