#!/usr/bin/env python3
"""Localized r:2->1 Ward audit on the 47 active curved-OO profiles.

The source Ward derivation is column-local:

    W_(2->1) = sum_alpha a_(1,alpha) d/d a_(2,alpha).

For a fixed residual word it sends the full r=2 matching coefficient to the
full r=1 coefficient.  This checker keeps every incident r-star coordinate,
including absent coordinates and the direct pr cell, and applies the Ward
identity before specializing to the sparse regression packet.
"""

from collections import Counter, defaultdict
from fractions import Fraction as F

import verify_oo_c8_fullnine_star_inverse as inverse
import verify_oo_c8_clean_face_vertex_recursion as vertex
import verify_oo_c8_active_leader_quotient as leader
import verify_oo_c8_two_cell_activity_frontier as frontier
import verify_oo_doubly_good_two_anchor_counterguard as base


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def clean(polynomial):
    return {mask: coefficient for mask, coefficient in polynomial.items() if coefficient}


def add_scaled(target, polynomial, scale=1):
    for mask, coefficient in polynomial.items():
        target[mask] += scale * coefficient


def multiply(left, right):
    """Multiply square-free source polynomials with disjoint provenance."""

    answer = defaultdict(F)
    for left_mask, left_coefficient in left.items():
        for right_mask, right_coefficient in right.items():
            require(not (left_mask & right_mask), "a matching coordinate was used twice")
            answer[left_mask | right_mask] += left_coefficient * right_coefficient
    return clean(answer)


def subtract(left, right):
    answer = defaultdict(F, left)
    add_scaled(answer, right, -1)
    return clean(answer)


def cofactor_coefficient(blocks, support, partner, partner_colour, common_word):
    """Coefficient after forcing r to the given physical half-edge column."""

    support_index = {cell: index for index, cell in enumerate(support)}
    colours = dict(zip(leader.COMMON, common_word, strict=True))
    colours[base.P] = 1
    colours[base.Q] = 0
    if partner in colours and colours[partner] != partner_colour:
        return {}
    colours[partner] = partner_colour
    residual = tuple(v for v in base.VERTICES if v not in (base.R, partner))
    answer = defaultdict(F)
    for matching in base.perfect_matchings(residual):
        mask = 0
        coefficient = F(1)
        for u, v in matching:
            term = vertex.cell_term(
                blocks, support_index, u, v, colours[u], colours[v]
            )
            if term is None:
                break
            local_mask, value = term
            mask |= local_mask
            coefficient *= value
        else:
            answer[mask] += coefficient
    return clean(answer)


def column_hessians(blocks, support, face):
    """Return nabla^2 C_alpha for all 21 physical r half-edge columns."""

    answer = {}
    for partner in base.VERTICES:
        if partner == base.R:
            continue
        for partner_colour in base.COLORS:
            polynomial = defaultdict(F)
            for sign, common_word in zip((1, -1, -1, 1), face, strict=True):
                add_scaled(
                    polynomial,
                    cofactor_coefficient(
                        blocks, support, partner, partner_colour, common_word
                    ),
                    sign,
                )
            polynomial = clean(polynomial)
            if polynomial:
                answer[(partner, partner_colour)] = polynomial
    return answer


def star_coefficient(blocks, support, row, column):
    """The specialized source coefficient a_(row,column), with provenance."""

    partner, partner_colour = column
    answer = defaultdict(F)
    constant = base.entry(blocks, base.R, partner, row, partner_colour)
    if constant:
        answer[0] += constant
    cell = base.key(base.R, partner, row, partner_colour)
    for index, support_cell in enumerate(support):
        if support_cell == cell:
            answer[1 << index] += 1
    return clean(answer)


def specialized_row(blocks, support, hessians, row):
    """sum_alpha a_(row,alpha) nabla^2 C_alpha."""

    answer = defaultdict(F)
    by_column = {}
    for column, cofactor in hessians.items():
        contribution = multiply(star_coefficient(blocks, support, row, column), cofactor)
        if contribution:
            by_column[column] = contribution
            add_scaled(answer, contribution)
    return clean(answer), by_column


def full_face_hessian(blocks, support, face, r_colour):
    tensor = frontier.tensor_polynomials(blocks, support)
    answer = defaultdict(F)
    for sign, common_word in zip((1, -1, -1, 1), face, strict=True):
        colours = dict(zip(leader.COMMON, common_word, strict=True))
        colours.update({base.P: 1, base.Q: 0, base.R: r_colour})
        word = tuple(colours[v] for v in base.VERTICES)
        require(len(set(word)) > 1, "Ward face acquired a pure target corner")
        add_scaled(answer, tensor.get(word, {}), sign)
    return clean(answer)


def active_column(record):
    """The r half-edge column used by the selected pq-cofactor matching."""

    residual = tuple(v for v in base.VERTICES if v not in frontier.ARMS[0])
    word = dict(zip(residual, record["word"], strict=True))
    edge = next(edge for edge in record["matching"] if base.R in edge)
    partner = edge[1] if edge[0] == base.R else edge[0]
    return partner, word[partner]


def main_profiles(blocks):
    profiles = []
    for support in leader.no_compound_regressions(blocks):
        records = tuple(leader.leading_record(blocks, support, arm) for arm in frontier.ARMS)
        residual_pq = tuple(v for v in base.VERTICES if v not in frontier.ARMS[0])
        residual_pr = tuple(v for v in base.VERTICES if v not in frontier.ARMS[1])
        r_colour = records[0]["word"][residual_pq.index(base.R)]
        q_colour = records[1]["word"][residual_pr.index(base.Q)]
        clean_face = inverse.cramer.vertex.chosen_clean_face(blocks, support, records)
        if clean_face is not None and q_colour == 0 and r_colour == 2:
            profiles.append((support, records, clean_face[0], clean_face[1]))
    require(len(profiles) == 47, "main Ward profile sector changed")
    return profiles


def main():
    blocks = base.build_packet()
    profiles = main_profiles(blocks)
    census = Counter()
    ward_column_counts = Counter()
    first_same_column = None
    first_direct_absent_coordinate_failure = None

    for support, records, face, active_hessians in profiles:
        hessians = column_hessians(blocks, support, face)
        row_one, row_one_columns = specialized_row(blocks, support, hessians, 1)
        row_two, row_two_columns = specialized_row(blocks, support, hessians, 2)
        require(
            row_one == full_face_hessian(blocks, support, face, 1),
            "complete r=1 Ward column expansion changed",
        )
        require(
            row_two == full_face_hessian(blocks, support, face, 2),
            "complete r=2 Ward column expansion changed",
        )

        column = active_column(records[0])
        require(column in hessians, "selected active column lost its cofactor Hessian")
        active_piece = multiply(star_coefficient(blocks, support, 2, column), hessians[column])
        require(
            active_piece.get(records[0]["mask"], 0)
            == active_hessians[0].get(records[0]["mask"], 0),
            "selected r=2 Ward column lost its active leader",
        )
        same_column_piece = multiply(
            star_coefficient(blocks, support, 1, column), hessians[column]
        )
        direct_column = (base.P, 1)
        direct_piece = multiply(
            star_coefficient(blocks, support, 1, direct_column),
            hessians.get(direct_column, {}),
        )
        extra = subtract(row_one, same_column_piece)
        same_carries_leader = bool(same_column_piece.get(records[0]["mask"], 0))
        direct_carries_leader = bool(direct_piece.get(records[0]["mask"], 0))
        extra_carries_leader = bool(extra.get(records[0]["mask"], 0))
        census[(same_carries_leader, direct_carries_leader, extra_carries_leader)] += 1
        ward_column_counts[len(row_one_columns)] += 1
        if same_carries_leader and first_same_column is None:
            first_same_column = (support, column, same_column_piece)
        if (
            not same_carries_leader
            and direct_carries_leader
            and first_direct_absent_coordinate_failure is None
        ):
            first_direct_absent_coordinate_failure = (
                support, face, column, active_piece, direct_piece,
                row_one_columns, hessians,
            )

    require(
        census == Counter({(False, True, True): 47}),
        "the localized Ward provenance census changed",
    )
    require(first_same_column is None, "an active leader acquired same-column Ward transport")

    # Freeze the smallest packet literally.  The active row-2 term is supplied
    # by (r3)_(2,2).  Ward differentiation does not select it because the
    # same physical column (r3)_(1,2) is zero.  Instead the existing direct
    # coefficient (rp)_(1,1) differentiates the absent coordinate
    # (rp)_(2,1), producing the direct-cofactor term -m.
    support, records, face, _ = profiles[0]
    hessians = column_hessians(blocks, support, face)
    require(
        hessians
        == {
            (base.P, 1): {12: F(-1)},
            (3, 0): {12: F(-1)},
            (3, 2): {12: F(1)},
        },
        "canonical universal Ward cofactor ledger changed",
    )
    row_one, row_one_columns = specialized_row(blocks, support, hessians, 1)
    row_two, row_two_columns = specialized_row(blocks, support, hessians, 2)
    require(row_one == {12: F(-1)}, "canonical diagonal Ward face changed")
    require(row_two == {12: F(1)}, "canonical off-diagonal Ward face changed")
    require(row_one_columns == {(base.P, 1): {12: F(-1)}}, "direct Ward term changed")
    require(row_two_columns == {(3, 2): {12: F(1)}}, "active Ward term changed")
    require(
        not star_coefficient(blocks, support, 1, (3, 2)),
        "missing same-column r=1 cell became occupied",
    )
    require(
        star_coefficient(blocks, support, 1, (base.P, 1)) == {0: F(1)},
        "direct r=1 Ward multiplier changed",
    )

    print("alternating-C8 localized color-raising Ward audit: PASS")
    print(f"main clean profiles={len(profiles)}")
    print(f"same-column/direct/extra active-leader census={dict(census)}")
    print(f"nonzero specialized r=1 Ward-column count={dict(sorted(ward_column_counts.items()))}")
    print(f"canonical support={support}")
    print(f"canonical universal cofactor Hessians={hessians}")
    print(f"canonical r=2 active face={row_two}; r=1 diagonal face={row_one}")
    print("active derivative column=(3,2): a_1,(3,2)=0")
    print("surviving Ward provenance=(rp)_(1,1) * d/d(rp)_(2,1), acting on direct cofactor -mask12")
    print("all four face corners are mixed, so the Ward target term is zero; no diagonal-anchor constant appears")
    print(f"first direct absent-coordinate guard={first_direct_absent_coordinate_failure}")


if __name__ == "__main__":
    main()
