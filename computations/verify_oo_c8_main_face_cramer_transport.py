#!/usr/bin/env python3
"""One-column Cramer transport on the 47 clean (q,r)=(0,2) OO faces."""

from collections import Counter, defaultdict
from fractions import Fraction as F

import verify_oo_c8_clean_face_vertex_recursion as vertex
import verify_oo_c8_common_word_square_curvature as square
import verify_oo_c8_active_leader_quotient as leader
import verify_oo_c8_two_cell_activity_frontier as frontier
import verify_oo_doubly_good_two_anchor_counterguard as base


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def response_by_r_column(blocks, support, word):
    """The pr response term, split by the half-edge column used at r=4."""

    support_index = {cell: index for index, cell in enumerate(support)}
    answer = defaultdict(lambda: defaultdict(F))
    for matching in base.perfect_matchings(base.VERTICES):
        p_partner = None
        r_partner = None
        mask = 0
        coefficient = F(1)
        for u, v in matching:
            term = vertex.cell_term(blocks, support_index, u, v, word[u], word[v])
            if term is None:
                break
            local_mask, value = term
            mask |= local_mask
            coefficient *= value
            if base.P in (u, v):
                p_partner = v if u == base.P else u
            if base.R in (u, v):
                r_partner = v if u == base.R else u
        else:
            require(p_partner is not None and r_partner is not None, "missing p/r partner")
            if p_partner == base.R:
                continue  # remove the direct pr*q^[3] term
            column = (r_partner, word[r_partner])
            answer[column][mask] += coefficient
    return {
        column: {mask: coefficient for mask, coefficient in polynomial.items() if coefficient}
        for column, polynomial in answer.items()
        if any(polynomial.values())
    }


def face_response_hessian(blocks, support, face, r_colour):
    answer = defaultdict(lambda: defaultdict(F))
    for sign, common_word in zip((1, -1, -1, 1), face, strict=True):
        colours = dict(zip(leader.COMMON, common_word, strict=True))
        colours.update({base.P: 1, base.Q: 0, base.R: r_colour})
        word = tuple(colours[vertex_index] for vertex_index in base.VERTICES)
        require(len(set(word)) > 1, "main Cramer face meets a pure full target")
        decomposition = response_by_r_column(blocks, support, word)
        for column, polynomial in decomposition.items():
            vertex.add_polynomial(answer[column], polynomial, sign)
    return {
        column: {mask: coefficient for mask, coefficient in polynomial.items() if coefficient}
        for column, polynomial in answer.items()
        if any(polynomial.values())
    }


def main():
    blocks = base.build_packet()
    regressions = leader.no_compound_regressions(blocks)
    main_profiles = []
    for support in regressions:
        records = tuple(
            leader.leading_record(blocks, support, arm)
            for arm in frontier.ARMS
        )
        residual_pq = tuple(v for v in base.VERTICES if v not in frontier.ARMS[0])
        residual_pr = tuple(v for v in base.VERTICES if v not in frontier.ARMS[1])
        r_colour = records[0]["word"][residual_pq.index(base.R)]
        q_colour = records[1]["word"][residual_pr.index(base.Q)]
        clean = vertex.chosen_clean_face(blocks, support, records)
        if clean is not None and q_colour == 0 and r_colour == 2:
            main_profiles.append((support, records, clean))
    require(len(main_profiles) == 47, "main clean colour sector changed")

    shifted_hessian_census = Counter()
    first_shifted_nonzero = None
    for profile_support, profile_records, (profile_face, profile_hessians) in main_profiles:
        shifted_words = tuple(
            square.cofactor_word(frontier.ARMS[0], common_word, 1)
            for common_word in profile_face
        )
        polynomials = frontier.cofactor_polynomials(
            blocks, profile_support, frontier.ARMS[0]
        )
        shifted = square.hessian(polynomials, shifted_words)
        active = profile_hessians[0]
        overlap = bool(set(shifted) & set(active))
        shifted_hessian_census[(bool(shifted), overlap, len(shifted))] += 1
        if shifted and first_shifted_nonzero is None:
            first_shifted_nonzero = (
                profile_support, profile_face, active, shifted, profile_records
            )
    require(
        shifted_hessian_census == Counter({(False, False, 0): 47}),
        "an r:2->1 shifted pq cofactor Hessian became nonzero",
    )

    support, records, (face, cofactor_hessians) = main_profiles[0]
    row_one = face_response_hessian(blocks, support, face, 1)
    row_two = face_response_hessian(blocks, support, face, 2)

    pivot_one = (base.Q, 1)   # cell 24:11 in endpoint order r--q
    pivot_two = (3, 2)        # cell 34:22
    require(base.entry(blocks, base.R, base.Q, 1, 1) == 1, "row-1 Cramer pivot changed")
    require(base.entry(blocks, base.R, 3, 2, 2) == 1, "row-2 Cramer pivot changed")
    require(base.entry(blocks, base.R, base.Q, 2, 1) == 0, "Cramer cross entry 21 changed")
    require(base.entry(blocks, base.R, 3, 1, 2) == 0, "Cramer cross entry 12 changed")
    require(pivot_two in row_two, "off-diagonal row lost the pq leader pivot")
    require(
        row_two[pivot_two].get(records[0]["mask"], 0)
        == cofactor_hessians[0].get(records[0]["mask"], 0),
        "row-2 pivot does not carry the pq cofactor leader",
    )

    extra_one = {column: polynomial for column, polynomial in row_one.items() if column != pivot_one}
    extra_two = {column: polynomial for column, polynomial in row_two.items() if column != pivot_two}
    extra_grade_census = Counter(
        (row, column, tuple(sorted(mask.bit_count() for mask in polynomial)))
        for row, extra in ((1, extra_one), (2, extra_two))
        for column, polynomial in extra.items()
    )

    print("alternating-C8 main-face Cramer transport: PASS")
    print(f"main clean profiles={len(main_profiles)}")
    print(f"r:2->1 shifted pq-Hessian census={dict(sorted(shifted_hessian_census.items()))}")
    print(f"first nonzero shifted pq-Hessian={first_shifted_nonzero}")
    print(f"chosen support={support}")
    print(f"common face={face}")
    print(f"row1 response Hessian by r-column={row_one}")
    print(f"row2 response Hessian by r-column={row_two}")
    print(f"Cramer pivots={pivot_one,pivot_two}; determinant=1")
    print(f"extra grade census={dict(sorted(extra_grade_census.items(), key=str))}")
    print(f"extra row1={extra_one}")
    print(f"extra row2={extra_two}")

    require(row_one == {}, "representative diagonal response Hessian changed")
    require(row_two == {pivot_two: {12: F(1)}}, "representative off-diagonal pivot changed")
    require(not extra_one and not extra_two, "representative acquired an extra Cramer grade")


if __name__ == "__main__":
    main()
