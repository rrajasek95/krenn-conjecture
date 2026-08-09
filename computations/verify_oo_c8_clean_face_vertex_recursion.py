#!/usr/bin/env python3
"""Literal shared-vertex recursion on one clean active common-word face."""

from collections import Counter, defaultdict
from fractions import Fraction as F

import verify_oo_c8_common_word_square_curvature as square
import verify_oo_c8_active_leader_quotient as leader
import verify_oo_c8_two_cell_activity_frontier as frontier
import verify_oo_doubly_good_two_anchor_counterguard as base


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def cell_term(blocks, support_index, u, v, i, j):
    cell = base.key(u, v, i, j)
    if cell in blocks:
        return 0, blocks[cell]
    if cell in support_index:
        return 1 << support_index[cell], F(1)
    return None


def recursion_by_neighbor(blocks, support, word):
    """Decompose one full coefficient by the physical partner of p=0."""

    support_index = {cell: index for index, cell in enumerate(support)}
    answer = defaultdict(lambda: defaultdict(F))
    for matching in base.perfect_matchings(base.VERTICES):
        mask = 0
        coefficient = F(1)
        partner = None
        for u, v in matching:
            term = cell_term(blocks, support_index, u, v, word[u], word[v])
            if term is None:
                break
            local_mask, value = term
            mask |= local_mask
            coefficient *= value
            if u == base.P:
                partner = v
            elif v == base.P:
                partner = u
        else:
            require(partner is not None, "p has no matching partner")
            answer[partner][mask] += coefficient
    return {
        neighbor: {mask: coefficient for mask, coefficient in polynomial.items() if coefficient}
        for neighbor, polynomial in answer.items()
        if any(polynomial.values())
    }


def add_polynomial(target, polynomial, sign=1):
    for mask, coefficient in polynomial.items():
        target[mask] += sign * coefficient


def face_neighbor_hessian(blocks, support, face, p_colour, q_colour, r_colour):
    answer = defaultdict(lambda: defaultdict(F))
    for sign, common_word in zip((1, -1, -1, 1), face, strict=True):
        colours = dict(zip(leader.COMMON, common_word, strict=True))
        colours.update({base.P: p_colour, base.Q: q_colour, base.R: r_colour})
        word = tuple(colours[vertex] for vertex in base.VERTICES)
        require(len(set(word)) > 1, "clean face acquired a pure full target word")
        decomposition = recursion_by_neighbor(blocks, support, word)
        for neighbor, polynomial in decomposition.items():
            add_polynomial(answer[neighbor], polynomial, sign)
    return {
        neighbor: {mask: coefficient for mask, coefficient in polynomial.items() if coefficient}
        for neighbor, polynomial in answer.items()
        if any(polynomial.values())
    }


def chosen_clean_face(blocks, support, records):
    faces = square.faces_for_words(records[0]["common"], records[1]["common"])
    for face in faces:
        all_mixed = True
        nonzero = []
        for arm, record in zip(frontier.ARMS, records, strict=True):
            residual = tuple(vertex for vertex in base.VERTICES if vertex not in arm)
            exclusive = base.R if arm == frontier.ARMS[0] else base.Q
            exclusive_colour = record["word"][residual.index(exclusive)]
            words = tuple(
                square.cofactor_word(arm, common_word, exclusive_colour)
                for common_word in face
            )
            all_mixed &= all(len(set(word)) > 1 for word in words)
            polynomials = frontier.cofactor_polynomials(blocks, support, arm)
            nonzero.append(square.hessian(polynomials, words))
        if all_mixed and all(nonzero):
            return face, tuple(nonzero)
    return None


def main():
    blocks = base.build_packet()
    regressions = leader.no_compound_regressions(blocks)
    candidate_census = Counter()
    bianchi_visibility = Counter()
    chosen = None
    for support in regressions:
        records = tuple(
            leader.leading_record(blocks, support, arm)
            for arm in frontier.ARMS
        )
        distance = sum(
            first != second
            for first, second in zip(records[0]["common"], records[1]["common"], strict=True)
        )
        if distance not in (1, 2):
            continue
        residual_pq = tuple(vertex for vertex in base.VERTICES if vertex not in frontier.ARMS[0])
        residual_pr = tuple(vertex for vertex in base.VERTICES if vertex not in frontier.ARMS[1])
        r_colour = records[0]["word"][residual_pq.index(base.R)]
        q_colour = records[1]["word"][residual_pr.index(base.Q)]
        clean = chosen_clean_face(blocks, support, records)
        candidate_census[(distance, q_colour, r_colour, clean is not None)] += 1
        if clean is not None:
            q_visible = q_colour == 0
            r_visible = r_colour == 1
            bianchi_visibility[
                "both" if q_visible and r_visible
                else "pr_only" if q_visible
                else "pq_only" if r_visible
                else "neither"
            ] += 1
        if clean is not None and q_colour == 0 and r_colour == 1 and chosen is None:
            chosen = (support, records, clean[0], clean[1])

    if chosen is None:
        print("alternating-C8 clean-face shared-vertex recursion: PASS (counterguard)")
        print(f"clean/direct-colour candidate census={dict(sorted(candidate_census.items()))}")
        print(f"fixed-label Bianchi visibility={dict(sorted(bianchi_visibility.items()))}")
        print("no clean face has q-colour 0 and r-colour 1 simultaneously")
        require(
            candidate_census
            == Counter({(1, 0, 2, True): 47,
                        (1, 1, 2, False): 14,
                        (1, 1, 0, False): 3,
                        (2, 2, 0, True): 2,
                        (1, 2, 1, True): 1,
                        (2, 0, 0, True): 1}),
            "clean/direct-colour census changed",
        )
        require(
            bianchi_visibility == Counter({"pr_only": 48, "neither": 2, "pq_only": 1}),
            "fixed-label Bianchi visibility changed",
        )
        return
    support, records, face, cofactor_hessians = chosen
    neighbor_hessians = {
        p_colour: face_neighbor_hessian(blocks, support, face, p_colour, 0, 1)
        for p_colour in base.COLORS
    }
    selected = neighbor_hessians[1]
    require(base.Q in selected and base.R in selected, "selected q/r recursion terms vanished")
    require(
        selected[base.Q] == cofactor_hessians[0],
        "q-neighbor term is not the pq cofactor Hessian",
    )
    require(
        selected[base.R] == cofactor_hessians[1],
        "r-neighbor term is not the pr cofactor Hessian",
    )

    extra = {
        p_colour: {
            neighbor: polynomial
            for neighbor, polynomial in decomposition.items()
            if neighbor not in (base.Q, base.R)
        }
        for p_colour, decomposition in neighbor_hessians.items()
    }
    extra_grade_census = Counter(
        (p_colour, neighbor, tuple(sorted(mask.bit_count() for mask in polynomial)))
        for p_colour, decomposition in extra.items()
        for neighbor, polynomial in decomposition.items()
    )

    print("alternating-C8 clean-face shared-vertex recursion: PASS")
    print(f"clean/direct-colour candidate census={dict(sorted(candidate_census.items()))}")
    print(f"chosen support={support}")
    print(f"chosen common face={face}")
    print(f"selected cofactor Hessians={cofactor_hessians}")
    print(f"neighbor Hessians by p-colour={neighbor_hessians}")
    print(f"extra-neighbor grade census={dict(sorted(extra_grade_census.items()))}")
    print(f"extra-neighbor ledger={extra}")


if __name__ == "__main__":
    main()
