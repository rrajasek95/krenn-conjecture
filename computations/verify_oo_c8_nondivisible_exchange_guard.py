#!/usr/bin/env python3
"""Decorated matching-exchange audit on the 12 nondivisible Ward profiles."""

from collections import Counter
from fractions import Fraction as F

import verify_oo_c8_iterated_ward_provenance as provenance
import verify_oo_c8_color_raising_ward as ward
import verify_oo_c8_two_cell_activity_frontier as frontier
import verify_oo_doubly_good_two_anchor_counterguard as base


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def cell_record(blocks, support, edge, word):
    u, v = edge
    cell = base.key(u, v, word[u], word[v])
    if cell in blocks:
        return cell, 0, blocks[cell]
    index = support.index(cell)
    return cell, 1 << index, F(1)


def monomial_records(blocks, support, matching, word):
    return {
        edge: cell_record(blocks, support, edge, word)
        for edge in matching
    }


def mask_location(mask, records, common_edges):
    answer = []
    for bit in range(4):
        if not mask & (1 << bit):
            continue
        edge = next(edge for edge, (_cell, local_mask, _value) in records.items() if local_mask & (1 << bit))
        answer.append((bit, "common_recoloured" if edge in common_edges else "exchange_cycle", edge))
    return tuple(answer)


def numeric_packet(support, values):
    blocks = base.build_packet()
    for cell, value in zip(support, values, strict=True):
        base.add_cell(blocks, *cell, value)
    return blocks


def structural_signature(blocks):
    direct = (
        base.direct_matrix(blocks, *frontier.ARMS[0]),
        base.direct_matrix(blocks, *frontier.ARMS[1]),
    )
    ranks = (
        base.star_rank(blocks, base.P, base.Q),
        base.star_rank(blocks, base.Q, base.P),
        base.star_rank(blocks, base.P, base.R),
        base.star_rank(blocks, base.R, base.P),
    )
    curvature = (
        base.entry(blocks, base.P, base.Q, 1, 0)
        * base.entry(blocks, base.R, base.FOURTH, 1, 0)
        - base.entry(blocks, base.P, base.R, 1, 1)
        * base.entry(blocks, base.Q, base.FOURTH, 0, 0)
    )
    return direct, ranks, curvature


def numeric_word_coefficient(blocks, word):
    tensor, _supported = base.matching_tensor(blocks)
    return tensor.get(word, F(0))


def main():
    blocks = base.build_packet()
    profiles = ward.main_profiles(blocks)
    signature_census = Counter()
    cycle_census = Counter()
    common_recolour_census = Counter()
    first_guard = None
    nondivisible = 0

    for support, records, _face, active_hessians in profiles:
        word = provenance.selected_word(records[0])
        active_matching = provenance.selected_matching(records[0])
        pure_terms = provenance.specialized_matching_terms(blocks, support, (1,) * 8)
        require(len(pure_terms) == 1, "pure matching ceased to be unique")
        pure_matching, pure_polynomial = pure_terms[0]
        pure_mask = next(iter(pure_polynomial))
        active_mask = records[0]["mask"]
        if (active_mask & pure_mask) == active_mask:
            continue
        nondivisible += 1

        active_records = monomial_records(blocks, support, active_matching, word)
        pure_records = monomial_records(blocks, support, pure_matching, (1,) * 8)
        common_edges = set(active_matching) & set(pure_matching)
        changed_common = tuple(
            edge for edge in sorted(common_edges)
            if active_records[edge][0] != pure_records[edge][0]
        )
        active_only_mask = active_mask & ~pure_mask
        pure_only_mask = pure_mask & ~active_mask
        active_locations = mask_location(active_only_mask, active_records, common_edges)
        pure_locations = mask_location(pure_only_mask, pure_records, common_edges)
        cycles = provenance.symmetric_difference_cycles(active_matching, pure_matching)
        cycle_census[cycles] += 1
        common_recolour_census[len(changed_common)] += 1
        signature = (
            cycles,
            len(changed_common),
            tuple(location[1] for location in active_locations),
            tuple(location[1] for location in pure_locations),
        )
        signature_census[signature] += 1

        # A determinant-cleared monomial equality always exists after torus
        # localization, but record both sides: it may require cells on common
        # physical edges that no symmetric-difference-cycle minor sees.
        require(active_only_mask and pure_only_mask, "nondivisible guard lost one monomial side")
        if first_guard is None:
            first_guard = {
                "support": support,
                "word": word,
                "active_matching": active_matching,
                "pure_matching": pure_matching,
                "cycles": cycles,
                "changed_common_edges": changed_common,
                "active_records": active_records,
                "pure_records": pure_records,
                "active_mask": active_mask,
                "pure_mask": pure_mask,
                "active_only_mask": active_only_mask,
                "pure_only_mask": pure_only_mask,
                "active_only_locations": active_locations,
                "pure_only_locations": pure_locations,
                "active_hessian_coefficient": active_hessians[0].get(active_mask, 0),
            }

    require(nondivisible == 12, "nondivisible Ward profile count changed")
    pure_cycle_profiles = sum(
        count
        for signature, count in signature_census.items()
        if not any(location == "common_recoloured" for location in signature[2] + signature[3])
    )

    guard = first_guard
    require(guard["cycles"] == (4,), "first guard cycle changed")
    require(guard["changed_common_edges"] == ((1, 5),), "first common recolouring changed")
    require(guard["active_only_locations"] == ((1, "common_recoloured", (1, 5)),), "active remote grade changed")
    require(
        guard["pure_only_locations"]
        == ((0, "exchange_cycle", (0, 3)), (2, "common_recoloured", (1, 5))),
        "pure remote/cycle grades changed",
    )

    # Two exact rational specializations vary only the remote decorated cell
    # 15:00.  All rank-one arms, four good-star ranks, curvature, the physical
    # C4 edge products, and the pure anchor stay fixed, while the active mixed
    # coefficient changes.  Hence those local structural data cannot imply
    # the missing decorated-edge ratio.
    support = guard["support"]
    packet_a = numeric_packet(support, (2, 3, 5, 7))
    packet_b = numeric_packet(support, (2, 11, 5, 7))
    require(structural_signature(packet_a) == structural_signature(packet_b), "OO structure saw remote weight")
    require(structural_signature(packet_a)[1:] == ((3, 3, 3, 3), F(-1)), "OO packet changed")
    active_a = numeric_word_coefficient(packet_a, guard["word"])
    active_b = numeric_word_coefficient(packet_b, guard["word"])
    pure_a = numeric_word_coefficient(packet_a, (1,) * 8)
    pure_b = numeric_word_coefficient(packet_b, (1,) * 8)
    require((active_a, active_b) == (F(21), F(77)), "remote active coefficient did not vary")
    require(pure_a == pure_b == F(70), "pure anchor or C4 data varied")

    print("alternating-C8 nondivisible exchange guard: PASS")
    print(f"nondivisible profiles={nondivisible}")
    print(f"physical matching cycle census={dict(sorted(cycle_census.items()))}")
    print(f"changed common-edge census={dict(sorted(common_recolour_census.items()))}")
    print(f"decorated exchange signatures={dict(sorted(signature_census.items(), key=str))}")
    print(f"pure cycle-minor profiles={pure_cycle_profiles}")
    print(f"first decorated provenance guard={guard}")
    print(f"remote-weight test: active coefficients={(active_a,active_b)}, pure coefficients={(pure_a,pure_b)}")
    print("verdict=symmetric-difference minors alone do not close the 12; a common-edge colour-cell transport is required")


if __name__ == "__main__":
    main()
