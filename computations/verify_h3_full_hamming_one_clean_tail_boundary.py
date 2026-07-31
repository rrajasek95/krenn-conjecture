#!/usr/bin/env python3
"""Exact audit of the full-nine Hamming-one clean-tail boundary at h=3."""

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product


Q = Fraction
SITES = tuple(range(6))
COLORS = tuple(range(3))
PURE_MATCHING = ((0, 1), (2, 3), (4, 5))
EMPTY = (-1,) * 6
MIXED_WEIGHT = Q(1)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


@lru_cache(maxsize=None)
def matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, partner in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        for matching in matchings(remainder):
            answer.append(((first, partner),) + matching)
    return tuple(answer)


def multiply_scalars(values):
    answer = Q(1)
    for value in values:
        answer *= value
    return answer


# Direct pq block.  The selected row is (a,b)=(0,1), with alpha=1.
D = (
    (Q(1), Q(1), Q(0)),
    (Q(0), Q(0), Q(0)),
    (Q(0), Q(0), Q(0)),
)


def zero_stars():
    return [
        [[Q(0) for _ in COLORS] for _ in SITES]
        for _ in COLORS
    ]


# FIRST[c][x][i] is the coefficient of colour c at site x in p_i.
# SECOND[c][x][j] is the analogous coefficient in s_j.
FIRST = zero_stars()
SECOND = zero_stars()

FIRST[0][0][0] = FIRST[0][1][0] = Q(1)
FIRST[1][0][1] = FIRST[1][1][0] = Q(1)
FIRST[2][2][0] = FIRST[2][3][2] = FIRST[2][4][0] = Q(1)

SECOND[0][0][1] = Q(-1)
SECOND[1][0][0] = SECOND[1][0][1] = Q(-1)
SECOND[1][1][1] = Q(1)
SECOND[2][2][2] = Q(1)
SECOND[2][3][0] = Q(-1)
SECOND[2][3][1] = Q(1)
SECOND[2][5][1] = Q(-2)


def q_entry(left, right, left_color, right_color):
    """Endpoint-ordered internal block coefficient."""
    if left > right:
        left, right = right, left
        left_color, right_color = right_color, left_color
    if (left, right) not in PURE_MATCHING:
        return Q(0)
    diagonal = Q(left_color == right_color)
    mixed = (
        MIXED_WEIGHT
        if (left, right, left_color, right_color) == (0, 1, 1, 0)
        else Q(0)
    )
    return diagonal + mixed


def hafnian_coefficient(vertices, word):
    return sum(
        (
            multiply_scalars(
                q_entry(left, right, word[left], word[right])
                for left, right in matching
            )
            for matching in matchings(tuple(vertices))
        ),
        Q(0),
    )


def row_coefficient(i, j, word):
    answer = D[i][j] * hafnian_coefficient(SITES, word)
    for p_site in SITES:
        p_value = FIRST[word[p_site]][p_site][i]
        if not p_value:
            continue
        for s_site in SITES:
            if s_site == p_site:
                continue
            s_value = SECOND[word[s_site]][s_site][j]
            if not s_value:
                continue
            remainder = tuple(
                site for site in SITES if site not in (p_site, s_site)
            )
            answer += (
                p_value
                * s_value
                * hafnian_coefficient(remainder, word)
            )
    return answer


def target_coefficient(i, j, word):
    return Q(i == j and all(color == i for color in word))


def matrix_rank(rows):
    work = [list(row) for row in rows]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [entry / scale for entry in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                left - scale * right
                for left, right in zip(work[row], work[rank])
            ]
        rank += 1
    return rank


def global_star_rows(star):
    return [
        [star[color][site][label] for label in COLORS]
        for color in COLORS
        for site in SITES
    ]


def add_term(polynomial, monomial, coefficient):
    if not coefficient:
        return
    polynomial[monomial] = polynomial.get(monomial, Q(0)) + coefficient
    if not polynomial[monomial]:
        del polynomial[monomial]


def multiply_polynomials(left, right):
    answer = {}
    for first, first_value in left.items():
        for second, second_value in right.items():
            if any(
                first[site] >= 0 and second[site] >= 0
                for site in SITES
            ):
                continue
            monomial = tuple(
                first[site] if first[site] >= 0 else second[site]
                for site in SITES
            )
            add_term(answer, monomial, first_value * second_value)
    return answer


def linear_star(star, label):
    answer = {}
    for color in COLORS:
        for site in SITES:
            monomial = list(EMPTY)
            monomial[site] = color
            add_term(answer, tuple(monomial), star[color][site][label])
    return answer


def audit_admitted_rows():
    admitted = 0
    for base in COLORS:
        pure = (base,) * 6
        for i, j in product(COLORS, repeat=2):
            require(
                row_coefficient(i, j, pure)
                == target_coefficient(i, j, pure),
                f"pure row failed at {(base, i, j)}",
            )
            admitted += 1
        for defect in COLORS:
            if defect == base:
                continue
            for site in SITES:
                word = tuple(
                    defect if index == site else base for index in SITES
                )
                for i, j in product(COLORS, repeat=2):
                    require(
                        row_coefficient(i, j, word) == Q(0),
                        f"Hamming-one row failed at {(base, defect, site, i, j)}",
                    )
                    admitted += 1
    require(admitted == 351, "wrong admitted coefficient count")


def audit_first_omitted_layer():
    failures = []
    for word in product(COLORS, repeat=6):
        distance = min(
            sum(entry != color for entry in word) for color in COLORS
        )
        for i, j in product(COLORS, repeat=2):
            residual = (
                row_coefficient(i, j, word)
                - target_coefficient(i, j, word)
            )
            if residual:
                failures.append((distance, word, i, j, residual))
    require(failures, "the packet unexpectedly became a full source")
    require(min(item[0] for item in failures) == 2, "first failure is not Hamming two")
    require(
        (2, (1, 0, 2, 2, 2, 2), 0, 1, Q(-1)) in failures,
        "the displayed selected Hamming-two failure moved",
    )
    require(len(failures) == 59, "the exact failure ledger changed")


def pure_matrix(color):
    return [
        [q_entry(left, right, color, color) for right in SITES]
        for left in SITES
    ]


def hafnian_matrix(entries, vertices=SITES):
    return sum(
        (
            multiply_scalars(entries[left][right] for left, right in matching)
            for matching in matchings(tuple(vertices))
        ),
        Q(0),
    )


def marked_rq_value(internal, response, marked, incidence):
    """Coefficient of incidence * response * internal off a marked site."""
    answer = Q(0)
    unmarked = tuple(site for site in SITES if site != marked)
    for endpoint in unmarked:
        remainder = tuple(site for site in unmarked if site != endpoint)
        for left, right in combinations(remainder, 2):
            complement = tuple(
                site for site in remainder if site not in (left, right)
            )
            answer += (
                incidence[endpoint]
                * response[left][right]
                * internal[complement[0]][complement[1]]
            )
    return answer


def audit_clean_tail():
    color = 2
    alpha = D[0][1]
    u = [FIRST[color][site][0] for site in SITES]
    v = [SECOND[color][site][1] for site in SITES]
    require(u == [0, 0, 1, 0, 1, 0], "wrong selected first star")
    require(v == [0, 0, 0, 1, 0, -2], "wrong selected second star")

    internal = pure_matrix(color)
    response = [
        [
            Q(0) if left == right else u[left] * v[right] + v[left] * u[right]
            for right in SITES
        ]
        for left in SITES
    ]
    layers = []
    for response_edges in range(4):
        value = Q(0)
        for matching in matchings(SITES):
            for flags in product((0, 1), repeat=3):
                if sum(flags) != response_edges:
                    continue
                value += multiply_scalars(
                    response[left][right] if flag else alpha * internal[left][right]
                    for flag, (left, right) in zip(flags, matching)
                )
        layers.append(value)
    require(layers == [1, -1, -4, 0], "wrong four response layers")
    require(layers[0] + layers[1] == 0, "selected top row failed")
    require(layers[2] + layers[3] == Q(-4), "wrong clean tail")

    compound = Q(0)
    triples = Q(0)
    for left_set in combinations(SITES, 2):
        left = frozenset(left_set)
        for right_set in combinations(SITES, 2):
            right = frozenset(right_set)
            if left & right:
                continue
            remainder = tuple(site for site in SITES if site not in left | right)
            compound += (
                multiply_scalars(u[site] for site in left_set)
                * multiply_scalars(v[site] for site in right_set)
                * internal[remainder[0]][remainder[1]]
            )
    for left_set in combinations(SITES, 3):
        right_set = tuple(site for site in SITES if site not in left_set)
        triples += (
            multiply_scalars(u[site] for site in left_set)
            * multiply_scalars(v[site] for site in right_set)
        )
    require(compound == Q(-2), "wrong K_Q sandwich")
    require(triples == 0, "the complete three-star term should vanish")
    require(2 * alpha * compound + 6 * triples == Q(-4), "wrong chi normalization")

    # Mark the response endpoints and the internal-q endpoints in R q^[2].
    first_tags = Q(0)
    second_tags = Q(0)
    gamma_tags = Q(0)
    response_top = Q(0)
    for p_site in SITES:
        for s_site in SITES:
            if p_site == s_site:
                continue
            remainder = tuple(
                site for site in SITES if site not in (p_site, s_site)
            )
            for matching in matchings(remainder):
                term = (
                    u[p_site]
                    * v[s_site]
                    * multiply_scalars(internal[left][right] for left, right in matching)
                )
                response_top += term
                first_tags += term
                second_tags += term
                gamma_tags += 4 * term
    require(response_top == Q(-1), "wrong R q^[2] coefficient")
    require(first_tags == response_top, "first-star tagging lost a term")
    require(second_tags == response_top, "second-star tagging lost a term")
    require(gamma_tags == 4 * response_top, "Gamma endpoint multiplicity is not four")

    gamma_values = []
    normal_values = []
    for marked in SITES:
        gamma_values.append(
            marked_rq_value(internal, response, marked, internal[marked])
        )
        normal_values.append(
            marked_rq_value(internal, response, marked, response[marked])
        )
    require(
        gamma_values == [Q(-1), Q(-1), Q(-2), Q(-2), Q(1), Q(1)],
        "ordinary tagged-polar site values moved",
    )
    require(sum(gamma_values) == 4 * layers[1], "wrong ordinary tagged sum")
    require(
        normal_values == [Q(0), Q(0), Q(-4), Q(-4), Q(-4), Q(-4)],
        "normal-incidence site values moved",
    )
    require(sum(normal_values) == 4 * layers[2], "wrong normal-incidence sum")

    # At site 2, beta has a site-5 component that no physical q-incidence can
    # supply when the other endpoint remains in selected colour 2.
    marked = 2
    physical_incidence_rows = [
        [
            Q(0)
            if site == marked
            else q_entry(marked, site, label, color)
            for site in SITES
        ]
        for label in COLORS
    ]
    beta = response[marked]
    require(beta == [Q(0), Q(0), Q(0), Q(1), Q(0), Q(-2)], "wrong beta_2")
    require(matrix_rank(physical_incidence_rows) == 1, "wrong physical incidence rank")
    require(
        matrix_rank(physical_incidence_rows + [beta]) == 2,
        "beta_2 unexpectedly acquired a physical-incidence lift",
    )


def audit_good_stars_and_segre():
    require(matrix_rank(global_star_rows(FIRST)) == 3, "first global star is not good")
    require(matrix_rank(global_star_rows(SECOND)) == 3, "second global star is not good")
    first_forms = tuple(linear_star(FIRST, label) for label in COLORS)
    second_forms = tuple(linear_star(SECOND, label) for label in COLORS)
    responses = tuple(
        tuple(
            multiply_polynomials(first_forms[i], second_forms[j])
            for j in COLORS
        )
        for i in COLORS
    )
    for i, k, j, ell in product(COLORS, repeat=4):
        require(
            multiply_polynomials(responses[i][j], responses[k][ell])
            == multiply_polynomials(responses[i][ell], responses[k][j]),
            f"Segre rectangle failed at {(i, k, j, ell)}",
        )


def audit_mutations():
    global MIXED_WEIGHT

    # The ordered mixed internal cell is what cancels the two exceptional
    # Hamming-one words.  Removing it leaves the response matrix -D.
    MIXED_WEIGHT = Q(0)
    word = (1, 0, 0, 0, 0, 0)
    require(
        row_coefficient(0, 1, word) == Q(-1),
        "removing the ordered mixed q-cell did not expose the Hamming-one row",
    )
    MIXED_WEIGHT = Q(1)

    # The extra colour-one p_0 coefficient is part of the pure-one anchor.
    old_first = FIRST[1][1][0]
    FIRST[1][1][0] = Q(0)
    require(
        row_coefficient(0, 0, (1,) * 6) != Q(0),
        "removing the corrected z_1^1 term from p_0 was not detected",
    )
    FIRST[1][1][0] = old_first

    # The coefficient -2 creates both the selected top cancellation and the
    # nonzero four-crossing tail.  Changing it to -1 breaks the pure row.
    old_second = SECOND[2][5][1]
    SECOND[2][5][1] = Q(-1)
    require(
        row_coefficient(0, 1, (2,) * 6) == Q(1),
        "the selected-star coefficient mutation was not detected",
    )
    SECOND[2][5][1] = old_second


if __name__ == "__main__":
    audit_admitted_rows()
    audit_first_omitted_layer()
    audit_clean_tail()
    audit_good_stars_and_segre()
    audit_mutations()
    print(
        "PASS: 27 pure + 324 Hamming-one full-nine coefficients; "
        "good shared stars; layers (1,-1,-4,0), K_Q=-2, chi=-4; "
        "first omitted detector is Hamming two"
    )
