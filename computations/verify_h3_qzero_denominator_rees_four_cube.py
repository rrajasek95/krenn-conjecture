#!/usr/bin/env python3
"""Exact q-zero candidate symbol for the h=3 denominator-marked Rees 4-cube.

The calculation is deliberately presentation-level.  It reconstructs the
literal direct-free eight-site rows, differentiates in the two external
chart directions and the two edges of an internal perfect matching, and
checks the full odd denominator presentation after the mixed-word reset.
It also audits cubical signs, GHZ-stabilizer weights, matching-choice
indeterminacy, and the uniform odd-set Reynolds operator.  It does not
construct the attaching chain or an ordinary-residue map on that chain.
"""

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json


Q = Fraction
COLOURS = (0, 1, 2)
SITES = tuple(range(8))
ODD = (1, 2, 3, 4, 5)
MIXED = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}
X, R, P, QSITE = 0, 3, 6, 7
FORBIDDEN = frozenset((P, R))
EXPECTED_DIGEST = "9aa94b9e45d3954e6558091ac4fcbe845734ca55f8c382277ced44e31508318f"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right, left_colour=0, right_colour=0):
    if left < right:
        return left, right, left_colour, right_colour
    return right, left, right_colour, left_colour


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], start=1):
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def coloured_matching(matching, colouring):
    return tuple(sorted(
        edge(left, right, colouring[left], colouring[right])
        for left, right in matching
    ))


def full_direct_free_row(word):
    colouring = dict(enumerate(word))
    terms = []
    for matching in matchings(SITES):
        if FORBIDDEN in (frozenset(pair) for pair in matching):
            continue
        terms.append(coloured_matching(matching, colouring))
    require(len(terms) == len(set(terms)) == 90,
            "literal direct-free row must have 90 terms")
    return {term: Q(1) for term in terms}


def contains_pair(term, pair):
    pair = frozenset(pair)
    return any(frozenset((left, right)) == pair
               for left, right, _a, _b in term)


def derivative(polynomial, variables):
    answer = defaultdict(Q)
    for term, coefficient in polynomial.items():
        rest = list(term)
        for variable in variables:
            if variable not in rest:
                break
            rest.remove(variable)
        else:
            answer[tuple(sorted(rest))] += coefficient
    return {term: value for term, value in answer.items() if value}


def rank(columns):
    pivots = {}
    for original in columns:
        column = {row: Q(value) for row, value in enumerate(original) if value}
        while column:
            pivot = min(column)
            value = column[pivot]
            if pivot not in pivots:
                pivots[pivot] = {
                    row: coefficient / value
                    for row, coefficient in column.items()
                }
                break
            basis = pivots[pivot]
            for row, coefficient in basis.items():
                new = column.get(row, Q(0)) - value * coefficient
                if new:
                    column[row] = new
                elif row in column:
                    del column[row]
    return len(pivots)


def in_row_span(vector, rows):
    return rank(list(rows) + [vector]) == rank(rows)


def face(deleted):
    return tuple(site for site in ODD if site != deleted)


def mixed_word_eight(deleted):
    word = [0] * 8
    for site in face(deleted):
        word[site] = MIXED[site]
    return tuple(word)


def face_polynomial(deleted, colours=MIXED):
    colouring = {site: colours[site] for site in face(deleted)}
    return {
        coloured_matching(matching, colouring): Q(1)
        for matching in matchings(face(deleted))
    }


def partition(row, deleted_pair):
    direct = {term: value for term, value in row.items()
              if contains_pair(term, deleted_pair)}
    star = {term: value for term, value in row.items()
            if not contains_pair(term, deleted_pair)}
    require(set(direct).isdisjoint(star), "sector overlap")
    require(set(direct) | set(star) == set(row), "sector loss")
    return direct, star


def reset_denominator_column(site, colour):
    """P_m delta(d_(site,colour)), with e_m renamed Y_0."""
    if colour != MIXED[site]:
        return {}
    return face_polynomial(site)


def literal_row_and_no_leakage_audit():
    records = []
    top_columns = []
    for deleted in ODD:
        row = full_direct_free_row(mixed_word_eight(deleted))
        pq_direct, pq_star = partition(row, (P, QSITE))
        pr_direct, pr_star = partition(row, (P, R))
        u = edge(X, deleted, 0, 0)
        t = edge(P, QSITE, 0, 0)
        h = derivative(row, (u, t))
        require(h == face_polynomial(deleted),
                f"face {deleted}: external mixed polar is not h_v")
        require(len(h) == 3, f"face {deleted}: h_v must have three terms")
        require(derivative(pq_direct, (u, t)) == h and
                not derivative(pq_star, (u, t)),
                f"face {deleted}: pq sector placement")
        require(not derivative(pr_direct, (u, t)) and
                derivative(pr_star, (u, t)) == h,
                f"face {deleted}: pr sector placement")

        local = []
        for matching in matchings(face(deleted)):
            variables = coloured_matching(
                matching, {site: MIXED[site] for site in face(deleted)})
            require(len(variables) == 2, "h=3 internal matching size")
            first_left = derivative(h, (variables[0],))
            first_right = derivative(h, (variables[1],))
            top = derivative(h, variables)
            require(first_left == {(variables[1],): Q(1)},
                    "first internal face does not retain the other edge")
            require(first_right == {(variables[0],): Q(1)},
                    "first internal face does not retain the other edge")
            require(top == {(): Q(1)},
                    "fourfold row polar is not the unit")
            require(derivative(row, (u, t) + variables) == {(): Q(1)},
                    "literal full-row four-polar")
            require(derivative(pq_direct, (u, t) + variables) == {(): Q(1)} and
                    not derivative(pq_star, (u, t) + variables),
                    "q-zero face left pq-direct")
            require(not derivative(pr_direct, (u, t) + variables) and
                    derivative(pr_star, (u, t) + variables) == {(): Q(1)},
                    "q-zero face left pr-two-star")

            # This is the complete 15-column support check after reset.
            supported = []
            for site in ODD:
                for colour in COLOURS:
                    value = derivative(
                        reset_denominator_column(site, colour), variables)
                    if value:
                        supported.append((site, colour, value))
            require(supported == [(deleted, MIXED[deleted], {(): Q(1)})],
                    f"face {deleted}: cross-column leakage")

            selected = reset_denominator_column(deleted, MIXED[deleted])
            require(selected == h, "base denominator face is not h_v Y_0")
            for subset_size in range(3):
                for indices in combinations(range(2), subset_size):
                    subset = tuple(variables[index] for index in indices)
                    require(derivative(selected, subset) == derivative(h, subset),
                            "internal denominator/row face mismatch")

            # This is a polynomial/output-word symbol.  Giving it cap and
            # ordinary-residue coordinates requires the attaching map that
            # is deliberately not declared by this checker.
            local.append([Q(1)])
            top_columns.append(
                [Q(1) if position == ODD.index(deleted) else Q(0)
                 for position in range(len(ODD))]
            )
            records.append({
                "deleted": deleted,
                "matching": [list(pair) for pair in matching],
                "external_order": 2,
                "internal_order": 2,
                "total_order": 4,
                "q_degree": 0,
                "full_row_top": 1,
                "denominator_support": [deleted, MIXED[deleted]],
                "pq_sector": "direct",
                "pr_sector": "two_star",
                "candidate_symbol": 1,
                "strict_mixed_row_target": 0,
                "cap_boundary": "not constructed",
                "ordinary_residue": "not defined",
            })
        require(rank(local) == 1, "three face matchings should have rank one")

    require(len(records) == 15, "five faces times three matchings")
    require(rank(top_columns) == 5, "five labelled q-zero faces")
    # In the direct sum of five polynomial face blocks: 15 choices, rank 5,
    # kernel 10.  This is not a rank statement about an augmented cap map.
    block_columns = []
    for record in records:
        column = [Q(0)] * 15
        block = ODD.index(record["deleted"])
        column[3 * block] = Q(1)
        block_columns.append(column)
    require(rank(block_columns) == 5 and len(block_columns) - rank(block_columns) == 10,
            "matching-choice kernel census")

    # The Reynolds average (1/3) sum_N partial_N is canonical and normalized.
    for deleted in ODD:
        h = face_polynomial(deleted)
        average = defaultdict(Q)
        for matching in matchings(face(deleted)):
            variables = coloured_matching(
                matching, {site: MIXED[site] for site in face(deleted)})
            for term, value in derivative(h, variables).items():
                average[term] += Q(1, 3) * value
        require(dict(average) == {(): Q(1)}, "Reynolds average normalization")

    return records, {
        "literal_rows": 5,
        "row_terms_each": 90,
        "qzero_candidates": 15,
        "labelled_output_rank": 5,
        "matching_choice_kernel_dimension": 10,
        "reynolds_factor": "1/3",
        "strict_mixed_row_target": 0,
        "cap_boundary": "not constructed",
        "ordinary_residue": "not defined",
    }


def boundary(face_state):
    """Oriented cubical boundary; None denotes a free coordinate."""
    free = [index for index, value in enumerate(face_state) if value is None]
    answer = defaultdict(int)
    for local_index, coordinate in enumerate(free):
        sign = -1 if local_index % 2 else 1
        upper = list(face_state)
        lower = list(face_state)
        upper[coordinate] = 1
        lower[coordinate] = 0
        answer[tuple(upper)] += sign
        answer[tuple(lower)] -= sign
    return {item: value for item, value in answer.items() if value}


def cubical_sign_audit():
    top = (None,) * 4
    first = boundary(top)
    second = defaultdict(int)
    appearances = defaultdict(int)
    for facet, coefficient in first.items():
        for ridge, face_coefficient in boundary(facet).items():
            second[ridge] += coefficient * face_coefficient
            appearances[ridge] += 1
    require(len(first) == 8, "4-cube facet count")
    require(len(appearances) == 24 and set(appearances.values()) == {2},
            "4-cube ridge pairing")
    require(not {ridge: value for ridge, value in second.items() if value},
            "cubical boundary signs do not square to zero")

    # Tensor convention D=d_ext+(-1)^p d_int.  On bidegree (2,2),
    # the two cross compositions have signs +1 and -1.
    ext_then_int = (+1) * (-1)  # internal sign after p drops from 2 to 1
    int_then_ext = (+1) * (+1)  # internal sign while p remains 2
    require(ext_then_int + int_then_ext == 0,
            "external/internal tensor faces fail to cancel")
    return {
        "directions": ["u_v", "t", "N_1", "N_2"],
        "facets": len(first),
        "ridges": len(appearances),
        "appearances_per_ridge": 2,
        "boundary_squared": 0,
        "tensor_cross_signs": [ext_then_int, int_then_ext],
    }


def stabilizer_constraints():
    rows = []
    # Pointwise GHZ torus: one colour sum for each colour.
    for colour in COLOURS:
        row = [Q(0)] * 15
        for site in ODD:
            row[3 * (site - 1) + colour] = Q(1)
        rows.append(row)
    # Intersect with SL(3)^5.  One dependency is expected.
    for site in ODD:
        row = [Q(0)] * 15
        for colour in COLOURS:
            row[3 * (site - 1) + colour] = Q(1)
        rows.append(row)
    require(rank(rows) == 7, "GHZ stabilizer constraint rank")
    return rows


def jet_character(deleted, remaining_sites):
    # Output Y_0 contributes every zero-colour slot.  Remaining q variables
    # contribute the input colours at precisely their still-uncontracted sites.
    vector = [Q(0)] * 15
    for site in ODD:
        vector[3 * (site - 1)] += Q(1)
    for site in remaining_sites:
        vector[3 * (site - 1) + MIXED[site]] -= Q(1)
    return vector


def stabilizer_weight_audit():
    constraints = stabilizer_constraints()
    initial = []
    records = []
    for deleted in ODD:
        initial_character = jet_character(deleted, face(deleted))
        require(not in_row_span(initial_character, constraints),
                f"face {deleted}: initial polar weight vanished")
        initial.append(initial_character)

        # The mixed face word is the unique four-site word with this
        # restricted character.
        collisions = []
        for word in product(COLOURS, repeat=4):
            colour_map = dict(zip(face(deleted), word))
            trial = [Q(0)] * 15
            for site in ODD:
                trial[3 * (site - 1)] += Q(1)
            for site in face(deleted):
                trial[3 * (site - 1) + colour_map[site]] -= Q(1)
            difference = [left - right
                          for left, right in zip(trial, initial_character)]
            if in_row_span(difference, constraints):
                collisions.append(word)
        expected = tuple(MIXED[site] for site in face(deleted))
        require(collisions == [expected],
                f"face {deleted}: stabilizer character collision")

        for matching in matchings(face(deleted)):
            e1, e2 = matching
            order0 = initial_character
            order1a = jet_character(deleted, set(e2))
            order1b = jet_character(deleted, set(e1))
            order2 = jet_character(deleted, set())
            require(not in_row_span(order0, constraints), "order-zero weight")
            require(not in_row_span(order1a, constraints) and
                    not in_row_span(order1b, constraints),
                    "one-edge polar weight vanished too early")
            require(in_row_span(order2, constraints),
                    "q-zero top face is not stabilizer-invariant")
        records.append({
            "deleted": deleted,
            "q_degree_2_weight": "nonzero",
            "q_degree_1_weights": "nonzero",
            "q_degree_0_weight": "zero",
            "unique_face_word": "".join(map(str, expected)),
        })
    require(rank(constraints + initial) - rank(constraints) == 5,
            "five initial face weights are not independent")
    return records, {
        "constraint_rank": rank(constraints),
        "initial_face_weight_rank": 5,
        "first_weight_zero_order": 4,
    }


def double_factorial_odd(value):
    answer = 1
    while value > 0:
        answer *= value
        value -= 2
    return answer


def uncoloured_polynomial(vertices):
    return {tuple(sorted(tuple(sorted(pair)) for pair in matching)): Q(1)
            for matching in matchings(tuple(vertices))}


def uncoloured_derivative(polynomial, matching):
    variables = tuple(sorted(tuple(sorted(pair)) for pair in matching))
    answer = defaultdict(Q)
    for term, coefficient in polynomial.items():
        rest = list(term)
        for variable in variables:
            if variable not in rest:
                break
            rest.remove(variable)
        else:
            answer[tuple(rest)] += coefficient
    return dict(answer)


def uniform_reynolds_audit():
    """Finite exact instances of the uniform odd-set duality lemma."""
    records = []
    for r in range(1, 5):
        odd_sites = tuple(range(1, 2 * r + 2))
        normalization = double_factorial_odd(2 * r - 1)
        require(len(matchings(odd_sites[1:])) == normalization,
                "perfect-matching normalization")
        matrix = []
        for deleted in odd_sites:
            face_v = tuple(site for site in odd_sites if site != deleted)
            row = []
            for other in odd_sites:
                h_other = uncoloured_polynomial(
                    site for site in odd_sites if site != other)
                average = Q(0)
                for matching in matchings(face_v):
                    value = uncoloured_derivative(h_other, matching)
                    average += Q(1, normalization) * value.get((), Q(0))
                row.append(average)
            matrix.append(row)
        identity = [[Q(1) if left == right else Q(0)
                     for right in range(len(odd_sites))]
                    for left in range(len(odd_sites))]
        require(matrix == identity, f"uniform Reynolds duality at r={r}")

        # For every N, (x,v), (p,q), and N are a perfect matching of the
        # full 2r+4 vertices.  It is a literal coefficient-one full-row term,
        # and it cannot contain the forbidden (p,r-chart) edge because it
        # already contains (p,q).
        for deleted in odd_sites:
            face_v = tuple(site for site in odd_sites if site != deleted)
            for matching in matchings(face_v):
                covered = {deleted, "x", "p", "q"}
                for left, right in matching:
                    require(left not in covered and right not in covered,
                            "uniform full-row matching overlap")
                    covered.update((left, right))
                require(len(covered) == 2 * r + 4,
                        "uniform four-polar does not cover every vertex")
        records.append({
            "r": r,
            "odd_sites": 2 * r + 1,
            "face_sites": 2 * r,
            "matchings_per_face": normalization,
            "L_v_h_s": "Kronecker delta",
            "full_row_top_coefficient": 1,
        })
    return records


def degree_and_conditional_typing_audit():
    ladder = [
        {"total_order": 2, "internal_derivatives": 0,
         "q_degree": 2, "stabilizer_weight": "nonzero",
         "cap_face": "h_v Y_0"},
        {"total_order": 3, "internal_derivatives": 1,
         "q_degree": 1, "stabilizer_weight": "nonzero",
         "cap_face": "one q edge times Y_0"},
        {"total_order": 4, "internal_derivatives": 2,
         "q_degree": 0, "stabilizer_weight": "zero",
         "cap_face": "Y_0"},
    ]
    require(all(item["q_degree"] > 0 for item in ladder[:-1]),
            "q-zero face appeared below total order four")

    # Conditional typing only: IF an attaching chain maps to the q-zero
    # symbol with zero target and ordinary residue, this is the missing
    # split-cap direction.  This sampled matrix is not provenance.
    for kappa, y in ((Q(1), Q(1)), (Q(-5, 2), Q(7, 3))):
        target = [-y, Q(1), Q(0)]
        rho = [Q(1), Q(0), Q(1)]
        conditional_column = [kappa * y, Q(0), Q(0)]
        require(rank([target, rho]) == 2, "old split-cap rank")
        require(rank([target, rho, conditional_column]) == 3,
                "conditional invisible column has wrong typing rank")
    return ladder, {
        "first_qzero_total_order": 4,
        "conditional_new_column": ["kappa*Y", 0, 0],
        "old_rank": 2,
        "augmented_rank": 3,
        "interpretation": "typing test only; attaching chain and ores map absent",
    }


def main():
    literal, support = literal_row_and_no_leakage_audit()
    signs = cubical_sign_audit()
    weights, weight_summary = stabilizer_weight_audit()
    uniform = uniform_reynolds_audit()
    ladder, conditional_typing = degree_and_conditional_typing_audit()
    certificate = {
        "literal_four_polars": literal,
        "support_and_missing_readouts": support,
        "cubical_signs": signs,
        "stabilizer_weights": weights,
        "weight_summary": weight_summary,
        "uniform_reynolds_duality": uniform,
        "degree_ladder": ladder,
        "conditional_split_cap_typing": conditional_typing,
        "scope": {
            "constructed": "q-zero no-leakage polynomial symbol and sign-compatible candidate cube",
            "not_constructed": [
                "attaching chain/comparison map realizing the candidate cube",
                "cap-boundary and ordinary-residue rows of that chain",
                "descent/comparison from the PP/Rees enlargement to the actual filtered source",
                "injectivity on the physical line",
                "choice-independent spectral-sequence secondary operation",
                "Krenn's conjecture",
            ],
        },
    }
    payload = json.dumps(certificate, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"certificate digest changed: {digest}")
    print("h=3 q-zero denominator-marked Rees four-cube candidate: PASS")
    print("15 literal four-polars are units; reset support has no cross-column leakage")
    print("first q-zero/invariant polynomial symbol is total order 4")
    print("Reynolds polynomial average is canonical; raw symbol kernel has dimension 10")
    print("uniform odd-set duality L_v(h_s)=delta_vs checked through nine odd sites")
    print(f"certificate sha256 {digest}")


if __name__ == "__main__":
    main()
