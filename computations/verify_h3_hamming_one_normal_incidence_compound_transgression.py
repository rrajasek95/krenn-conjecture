#!/usr/bin/env python3
"""Exact audit of the h=3 marked normal-incidence compound identity.

The first part checks the identities for several deterministic integral
pure slices.  The second part is the sharply scoped all-word mutation from
notes/h3-hamming-one-normal-incidence-compound-transgression.md.  It is
not a complete full-nine GHZ source.
"""

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from math import prod


SITES = tuple(range(6))
COLORS = tuple(range(3))
FULL_MASK = (1 << len(SITES)) - 1


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def matrix_rank(rows):
    """Exact row rank over the rationals."""

    if not rows:
        return 0
    work = [[Fraction(entry) for entry in row] for row in rows]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [entry / pivot_value for entry in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(work[row], work[rank])
            ]
        rank += 1
    return rank


def in_row_span(vector, rows):
    return matrix_rank(rows + [vector]) == matrix_rank(rows)


def add_term(polynomial, mask, coefficient):
    if not coefficient:
        return
    polynomial[mask] = polynomial.get(mask, 0) + coefficient
    if not polynomial[mask]:
        del polynomial[mask]


def multiply(left, right):
    answer = {}
    for first_mask, first_value in left.items():
        for second_mask, second_value in right.items():
            if first_mask & second_mask:
                continue
            add_term(
                answer,
                first_mask | second_mask,
                first_value * second_value,
            )
    return answer


def linear_polynomial(entries, excluded=()):
    excluded = frozenset(excluded)
    return {
        1 << site: value
        for site, value in enumerate(entries)
        if site not in excluded and value
    }


def quadratic_polynomial(matrix, excluded=()):
    excluded = frozenset(excluded)
    answer = {}
    for left, right in combinations(SITES, 2):
        if left in excluded or right in excluded:
            continue
        add_term(answer, (1 << left) | (1 << right), matrix[left][right])
    return answer


def divided_quadratic_power(quadratic, exponent):
    """Divided power of a square-free quadratic.

    Each unordered collection of disjoint edge monomials occurs once.
    """

    if exponent == 0:
        return {0: 1}
    edges = tuple(quadratic.items())
    answer = {}
    for chosen in combinations(range(len(edges)), exponent):
        mask = 0
        coefficient = 1
        for index in chosen:
            edge_mask, edge_value = edges[index]
            if mask & edge_mask:
                break
            mask |= edge_mask
            coefficient *= edge_value
        else:
            add_term(answer, mask, coefficient)
    return answer


def response_matrix(u, v):
    answer = [[0 for _ in SITES] for _ in SITES]
    for left, right in combinations(SITES, 2):
        value = u[left] * v[right] + v[left] * u[right]
        answer[left][right] = answer[right][left] = value
    return answer


def top_coefficient(polynomial, mask=FULL_MASK):
    return polynomial.get(mask, 0)


def coefficient_rho(q_matrix, u, v, marked, incidence):
    excluded = (marked,)
    response = quadratic_polynomial(response_matrix(u, v), excluded)
    internal = quadratic_polynomial(q_matrix, excluded)
    incidence_polynomial = linear_polynomial(incidence, excluded)
    mask = FULL_MASK ^ (1 << marked)
    return multiply(
        multiply(incidence_polynomial, response),
        internal,
    ).get(mask, 0)


def coefficient_sigma(u, v, marked, incidence):
    excluded = (marked,)
    response = quadratic_polynomial(response_matrix(u, v), excluded)
    incidence_polynomial = linear_polynomial(incidence, excluded)
    mask = FULL_MASK ^ (1 << marked)
    return multiply(
        incidence_polynomial,
        divided_quadratic_power(response, 2),
    ).get(mask, 0)


def response_incidence(u, v, marked):
    return [
        0 if site == marked else u[marked] * v[site] + v[marked] * u[site]
        for site in SITES
    ]


def pure_q_incidence(q_matrix, marked):
    return [
        0 if site == marked else q_matrix[marked][site]
        for site in SITES
    ]


def subset_product(values, subset):
    return prod(values[index] for index in subset)


def hafnian(matrix, vertices=SITES):
    vertices = tuple(vertices)

    @lru_cache(maxsize=None)
    def recur(remaining):
        if not remaining:
            return 1
        first = remaining[0]
        answer = 0
        for position, partner in enumerate(remaining[1:], start=1):
            rest = remaining[1:position] + remaining[position + 1 :]
            answer += matrix[first][partner] * recur(rest)
        return answer

    return recur(vertices)


def four_hole_sum(q_matrix, u, v):
    answer = 0
    for left in combinations(SITES, 2):
        left_set = frozenset(left)
        for right in combinations(SITES, 2):
            right_set = frozenset(right)
            if left_set & right_set:
                continue
            complement = tuple(
                site for site in SITES if site not in left_set | right_set
            )
            answer += (
                subset_product(u, left)
                * subset_product(v, right)
                * q_matrix[complement[0]][complement[1]]
            )
    return answer


def complementary_triple_sum(u, v):
    answer = 0
    for left in combinations(SITES, 3):
        left_set = frozenset(left)
        right = tuple(site for site in SITES if site not in left_set)
        answer += subset_product(u, left) * subset_product(v, right)
    return answer


def audit_marked_identities(seed):
    q_matrix = [[0 for _ in SITES] for _ in SITES]
    for left, right in combinations(SITES, 2):
        value = ((left + 2) * (right + 3) + seed * (left + right + 1)) % 11 - 5
        q_matrix[left][right] = q_matrix[right][left] = value

    u = [((site + 1) * (seed + 2)) % 7 - 3 for site in SITES]
    v = [((site + 3) * (2 * seed + 1)) % 9 - 4 for site in SITES]
    response = quadratic_polynomial(response_matrix(u, v))
    internal = quadratic_polynomial(q_matrix)

    first_layer = top_coefficient(
        multiply(response, divided_quadratic_power(internal, 2))
    )
    second_layer = top_coefficient(
        multiply(divided_quadratic_power(response, 2), internal)
    )
    third_layer = top_coefficient(divided_quadratic_power(response, 3))

    four_hole = four_hole_sum(q_matrix, u, v)
    triple = complementary_triple_sum(u, v)
    require(second_layer == 2 * four_hole, f"1/2 normalization failed at {seed}")
    require(third_layer == 6 * triple, f"1/6 normalization failed at {seed}")

    normal_values = []
    q_marked_values = []
    gamma_values = []
    cubic_marked_values = []
    for marked in SITES:
        beta = response_incidence(u, v, marked)
        q_incidence = pure_q_incidence(q_matrix, marked)
        normal = coefficient_rho(q_matrix, u, v, marked, beta)
        q_marked = coefficient_sigma(u, v, marked, q_incidence)
        gamma = coefficient_rho(q_matrix, u, v, marked, q_incidence)
        cubic_marked = coefficient_sigma(u, v, marked, beta)
        normal_values.append(normal)
        q_marked_values.append(q_marked)
        gamma_values.append(gamma)
        cubic_marked_values.append(cubic_marked)

        require(
            normal + q_marked == second_layer,
            f"fixed-site C2 split failed at seed={seed}, site={marked}",
        )
        require(
            cubic_marked == third_layer,
            f"fixed-site C3 marking failed at seed={seed}, site={marked}",
        )

    require(
        sum(normal_values) == 4 * second_layer,
        f"response-site factor four failed at seed={seed}",
    )
    require(
        sum(q_marked_values) == 2 * second_layer,
        f"q-site factor two failed at seed={seed}",
    )
    require(
        sum(gamma_values) == 4 * first_layer,
        f"Gamma first-layer marking failed at seed={seed}",
    )

    alpha = seed + 1
    chi = alpha * second_layer + third_layer
    require(
        4 * chi
        == alpha * sum(normal_values) + 24 * triple,
        f"cancellation-gate normalization failed at seed={seed}",
    )


for deterministic_seed in range(1, 6):
    audit_marked_identities(deterministic_seed)


# The exact selected-all-word grade-separation mutation.
#
# Sites are (x, 0, 1, 2, 3, 4) = (0, 1, 2, 3, 4, 5), and c=0.
TAGGED = 0
PURE = 0


def mutation_q_edge(left, right, left_label, right_label):
    if left > right:
        return mutation_q_edge(right, left, right_label, left_label)
    entries = {
        (0, 1, 0, 0): 1,
        (0, 4, 1, 0): 1,
        (0, 5, 2, 0): 1,
        (4, 5, 0, 0): 1,
    }
    return entries.get((left, right, left_label, right_label), 0)


def mutation_p(site, label, parameter):
    return int(label == PURE) * ({0: parameter, 1: 1}.get(site, 0))


def mutation_s(site, label):
    return int(label == PURE and site in (2, 3))


def word_hafnian(word, vertices=SITES):
    vertices = tuple(vertices)

    @lru_cache(maxsize=None)
    def recur(remaining):
        if not remaining:
            return 1
        first = remaining[0]
        answer = 0
        for position, partner in enumerate(remaining[1:], start=1):
            rest = remaining[1:position] + remaining[position + 1 :]
            answer += (
                mutation_q_edge(
                    first,
                    partner,
                    word[first],
                    word[partner],
                )
                * recur(rest)
            )
        return answer

    return recur(vertices)


def selected_response_coefficient(word, parameter):
    answer = 0
    for left, right in combinations(SITES, 2):
        response_value = (
            mutation_p(left, word[left], parameter)
            * mutation_s(right, word[right])
            + mutation_s(left, word[left])
            * mutation_p(right, word[right], parameter)
        )
        if not response_value:
            continue
        complement = tuple(site for site in SITES if site not in (left, right))
        answer += response_value * word_hafnian(word, complement)
    return answer


for parameter in (0, 1):
    for word in product(COLORS, repeat=len(SITES)):
        direct = word_hafnian(word)
        response = selected_response_coefficient(word, parameter)
        require(
            direct + response == 0,
            f"selected all-word mutation row failed at t={parameter}, word={word}",
        )


def mutation_pure_data(parameter):
    q_matrix = [[0 for _ in SITES] for _ in SITES]
    for left, right in combinations(SITES, 2):
        value = mutation_q_edge(left, right, PURE, PURE)
        q_matrix[left][right] = q_matrix[right][left] = value
    u = [mutation_p(site, PURE, parameter) for site in SITES]
    v = [mutation_s(site, PURE) for site in SITES]
    return q_matrix, u, v


mutation_layers = {}
for parameter in (0, 1):
    q_matrix, u, v = mutation_pure_data(parameter)
    response = quadratic_polynomial(response_matrix(u, v))
    internal = quadratic_polynomial(q_matrix)
    first_layer = top_coefficient(
        multiply(response, divided_quadratic_power(internal, 2))
    )
    second_layer = top_coefficient(
        multiply(divided_quadratic_power(response, 2), internal)
    )
    third_layer = top_coefficient(divided_quadratic_power(response, 3))
    mutation_layers[parameter] = (first_layer, second_layer, third_layer)

    selected_gammas = []
    for marked in SITES:
        for label in COLORS:
            incidence = [
                0
                if site == marked
                else mutation_q_edge(marked, site, label, PURE)
                for site in SITES
            ]
            selected_gammas.append(
                coefficient_rho(q_matrix, u, v, marked, incidence)
            )
    require(
        not any(selected_gammas),
        f"selected Gamma data moved at mutation t={parameter}",
    )

require(mutation_layers[0] == (0, 0, 0), "zero mutation layers changed")
require(mutation_layers[1] == (0, 2, 0), "unit mutation layers changed")

q_matrix, u, v = mutation_pure_data(1)
marked_values = [
    coefficient_rho(
        q_matrix,
        u,
        v,
        marked,
        response_incidence(u, v, marked),
    )
    for marked in SITES
]
require(marked_values == [2, 2, 2, 2, 0, 0], "mutation marks changed")
require(sum(marked_values) == 8 == 4 * mutation_layers[1][1], "factor four")
require(four_hole_sum(q_matrix, u, v) == 1, "factor eight/four-hole sum")

# Derive the tagged physical incidence rows from the decorated q-blocks.
# The present packet gives beta=z_1+z_2 in local D coordinates, whereas
# those three rows span z_0,z_3,z_4.  Both the rank jump and the computed
# supports certify the nonzero cokernel class; no expected support is used
# to define the physical incidence image.
tagged_beta = response_incidence(u, v, TAGGED)
tagged_incidence_rows = [
    [
        0
        if site == TAGGED
        else mutation_q_edge(TAGGED, site, label, PURE)
        for site in SITES
    ]
    for label in COLORS
]
incidence_rank = matrix_rank(tagged_incidence_rows)
augmented_rank = matrix_rank(tagged_incidence_rows + [tagged_beta])
incidence_support = {
    site
    for row in tagged_incidence_rows
    for site, value in enumerate(row)
    if value
}
beta_support = {site for site, value in enumerate(tagged_beta) if value}
require(incidence_rank == 3, "tagged physical incidence rank changed")
require(augmented_rank == 4, "tagged beta did not raise incidence rank")
require(
    not in_row_span(tagged_beta, tagged_incidence_rows),
    "tagged beta entered physical incidence image",
)
require(beta_support == {2, 3}, "tagged beta support changed")
require(
    beta_support.isdisjoint(incidence_support),
    "beta and incidence supports ceased to be disjoint",
)
require(
    coefficient_rho(q_matrix, u, v, TAGGED, tagged_beta) == 2,
    "tagged normal value changed",
)

# A canceling physical-incidence mutant (replace one of the three label
# rows by beta) must be detected as a lift, not mislabeled by the original
# packet's expected support.
canceling_incidence_mutant = [row[:] for row in tagged_incidence_rows]
canceling_incidence_mutant[0] = tagged_beta[:]
require(
    in_row_span(tagged_beta, canceling_incidence_mutant),
    "canceling incidence mutant was not detected as a lift",
)
require(
    matrix_rank(canceling_incidence_mutant + [tagged_beta])
    == matrix_rank(canceling_incidence_mutant),
    "canceling incidence mutant rank audit changed",
)

# A selected curvature scalar can be nonzero independently of this local map.
A, U, B, F = 1, 1, 0, 0
require(A * U - B * F == 1, "formal curvature guard changed")

print("PASS: marked C2/C3 identities and cancellation factors on five dense slices")
print("PASS: selected all-word/Gamma mutation 0 -> 2 with marks (2,2,2,2,0,0)")
print(
    "PASS: beta cokernel ranks "
    f"{incidence_rank}->{augmented_rank}, supports "
    f"{sorted(beta_support)} versus {sorted(incidence_support)}"
)
