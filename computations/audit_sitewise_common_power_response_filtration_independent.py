#!/usr/bin/env python3
"""Clean-room audit of the sitewise common-power response filtration.

This file intentionally imports neither the primary verifier nor project
code.  It uses three independent models:

* direct enumeration of ordered cofactor-determinant terms;
* finite-field tensor-block and local-pencil calculations; and
* an exact sparse site-square-zero algebra for the six-cycle example.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product


U = tuple(range(6))


def cauchy_binet_audit() -> tuple[int, Counter, int]:
    """Enumerate actual determinant terms, not merely minor supports."""

    histogram: Counter = Counter()
    term_count = 0
    complementary_count = 0
    for rows in combinations(U, 3):
        for column_set in combinations(U, 3):
            for assigned_columns in permutations(column_set):
                # C has zero diagonal, so these determinant terms vanish.
                if any(row == column for row, column in zip(rows, assigned_columns)):
                    continue
                exponents = tuple(
                    sum(site not in (row, column) for row, column in zip(rows, assigned_columns))
                    for site in U
                )
                expected = tuple(
                    3 - int(site in rows) - int(site in column_set) for site in U
                )
                assert exponents == expected
                assert min(exponents) >= 1
                assert sum(exponents) == 12
                histogram[tuple(sorted(exponents))] += 1
                term_count += 1
                if exponents == (2,) * 6:
                    assert set(rows).isdisjoint(column_set)
                    assert set(rows) | set(column_set) == set(U)
                    complementary_count += 1

    assert term_count == 1420
    assert histogram == Counter(
        {
            (2, 2, 2, 2, 2, 2): 120,
            (1, 2, 2, 2, 2, 3): 720,
            (1, 1, 2, 2, 3, 3): 540,
            (1, 1, 1, 3, 3, 3): 40,
        }
    )
    assert complementary_count == 20 * 6
    return term_count, histogram, complementary_count


def coordinate_plane_incidence_audit() -> int:
    """Enumerate omission words rather than the primary mask search."""

    count = 0
    for omissions in product(range(3), repeat=6):
        colour_counts = tuple(6 - omissions.count(colour) for colour in range(3))
        if min(colour_counts) < 4:
            continue
        assert colour_counts == (4, 4, 4)
        assert Counter(omissions) == Counter({0: 2, 1: 2, 2: 2})
        count += 1
    assert count == 90
    return count


def dot(left, right, prime):
    return sum(a * b for a, b in zip(left, right)) % prime


def mat_vec(matrix, vector, prime):
    return tuple(dot(row, vector, prime) for row in matrix)


def transpose(matrix):
    return tuple(tuple(matrix[row][column] for row in range(len(matrix))) for column in range(len(matrix[0])))


def edge_value(blocks, left, right, covectors, prime):
    if left < right:
        matrix = blocks[left, right]
        return dot(covectors[left], mat_vec(matrix, covectors[right], prime), prime)
    matrix = transpose(blocks[right, left])
    return dot(covectors[left], mat_vec(matrix, covectors[right], prime), prime)


def edge_vector_at(blocks, fixed, other, covectors, prime):
    """Contract the ``other`` endpoint and retain a vector at ``fixed``."""

    if fixed < other:
        return mat_vec(blocks[fixed, other], covectors[other], prime)
    return mat_vec(transpose(blocks[other, fixed]), covectors[other], prime)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remaining):
            yield ((first, second),) + tail


def cofactor(blocks, omitted_left, omitted_right, covectors, prime):
    remaining = tuple(site for site in U if site not in (omitted_left, omitted_right))
    answer = 0
    for matching in perfect_matchings(remaining):
        term = 1
        for left, right in matching:
            term = term * edge_value(blocks, left, right, covectors, prime) % prime
        answer = (answer + term) % prime
    return answer


class LCG:
    def __init__(self, seed):
        self.state = seed

    def value(self, prime):
        self.state = (1664525 * self.state + 1013904223) & 0xFFFFFFFF
        return self.state % prime


def arbitrary_block_audit() -> int:
    """Check response orientation and the chain rule for full-rank blocks."""

    prime = 101
    dimension = 3
    checked = 0
    for seed in (7, 101, 2027, 65537):
        generator = LCG(seed)
        blocks = {
            (left, right): tuple(
                tuple(generator.value(prime) for _ in range(dimension))
                for _ in range(dimension)
            )
            for left, right in combinations(U, 2)
        }
        covectors = tuple(
            tuple(generator.value(prime) for _ in range(dimension)) for _ in U
        )
        p_rows = tuple(
            tuple(
                tuple(generator.value(prime) for _ in range(dimension)) for _ in U
            )
            for _ in range(3)
        )
        s_rows = tuple(
            tuple(
                tuple(generator.value(prime) for _ in range(dimension)) for _ in U
            )
            for _ in range(3)
        )

        C = tuple(
            tuple(
                0 if left == right else cofactor(blocks, left, right, covectors, prime)
                for right in U
            )
            for left in U
        )
        assert C == transpose(C)
        P = tuple(
            tuple(dot(covectors[site], p_rows[index][site], prime) for site in U)
            for index in range(3)
        )
        S = tuple(
            tuple(dot(covectors[site], s_rows[index][site], prime) for site in U)
            for index in range(3)
        )

        # Directly enumerate the two ordered row endpoints and a matching of
        # the remaining four sites; compare with P C S^T.
        for i in range(3):
            for j in range(3):
                direct = 0
                matrix_form = 0
                for row_site in U:
                    for column_site in U:
                        if row_site == column_site:
                            continue
                        q_square_coefficient = 0
                        complement = tuple(
                            site for site in U if site not in (row_site, column_site)
                        )
                        for matching in perfect_matchings(complement):
                            matching_value = 1
                            for left, right in matching:
                                matching_value *= edge_value(
                                    blocks, left, right, covectors, prime
                                )
                                matching_value %= prime
                            q_square_coefficient += matching_value
                        direct += (
                            P[i][row_site]
                            * S[j][column_site]
                            * q_square_coefficient
                        )
                        matrix_form += (
                            P[i][row_site] * C[row_site][column_site] * S[j][column_site]
                        )
                assert direct % prime == matrix_form % prime

        # Compare the vector chain sum with an independently enumerated
        # contraction of q^[3].  This identity holds before imposing q^[3]=0.
        for retained_site in U:
            chain = [0] * dimension
            for other in U:
                if other == retained_site:
                    continue
                vector = edge_vector_at(
                    blocks, retained_site, other, covectors, prime
                )
                for coordinate in range(dimension):
                    chain[coordinate] += C[retained_site][other] * vector[coordinate]
                    chain[coordinate] %= prime

            contracted_cube = [0] * dimension
            for matching in perfect_matchings(U):
                incident = next(edge for edge in matching if retained_site in edge)
                other = incident[0] if incident[1] == retained_site else incident[1]
                vector = edge_vector_at(
                    blocks, retained_site, other, covectors, prime
                )
                scalar = 1
                for left, right in matching:
                    if retained_site in (left, right):
                        continue
                    scalar *= edge_value(blocks, left, right, covectors, prime)
                    scalar %= prime
                for coordinate in range(dimension):
                    contracted_cube[coordinate] += scalar * vector[coordinate]
                    contracted_cube[coordinate] %= prime
            assert tuple(chain) == tuple(contracted_cube)
        checked += 1
    return checked


def flatten_matrix(matrix):
    return tuple(entry for row in matrix for entry in row)


def outer(left, right, prime):
    return tuple(tuple(a * b % prime for b in right) for a in left)


def matrix_add(left, right, prime):
    return tuple(
        tuple((left[row][column] + right[row][column]) % prime for column in range(3))
        for row in range(3)
    )


def matrix_rank(vectors, prime):
    """Rank of a list of equal-length row vectors over a prime field."""

    if not vectors:
        return 0
    work = [list(vector) for vector in vectors]
    row = 0
    columns = len(work[0])
    for column in range(columns):
        pivot = next((index for index in range(row, len(work)) if work[index][column] % prime), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        inverse = pow(work[row][column] % prime, -1, prime)
        work[row] = [(entry * inverse) % prime for entry in work[row]]
        for index in range(len(work)):
            if index == row:
                continue
            multiplier = work[index][column] % prime
            if multiplier:
                work[index] = [
                    (entry - multiplier * pivot_entry) % prime
                    for entry, pivot_entry in zip(work[index], work[row])
                ]
        row += 1
        if row == len(work):
            break
    return row


def in_span(target, generators, prime):
    return matrix_rank(generators, prime) == matrix_rank(generators + [target], prime)


def local_two_axis_pencil_audit() -> int:
    """Exhaust (33) over F_3 by solving the rank-one-sum image test."""

    prime = 3
    vectors = tuple(product(range(prime), repeat=3))
    basis = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    targets = (
        flatten_matrix(outer(basis[1], basis[1], prime)),
        flatten_matrix(outer(basis[2], basis[2], prime)),
    )
    feasible = 0
    for alpha in vectors:
        for beta in vectors:
            generators = []
            for coordinate in range(3):
                generators.append(flatten_matrix(outer(basis[coordinate], alpha, prime)))
            for coordinate in range(3):
                generators.append(flatten_matrix(outer(beta, basis[coordinate], prime)))
            if not all(in_span(target, generators, prime) for target in targets):
                continue
            feasible += 1
            alpha_line = next((index for index in (1, 2) if all(
                alpha[k] == (alpha[index] if k == index else 0) for k in range(3)
            ) and alpha[index] != 0), None)
            beta_line = next((index for index in (1, 2) if all(
                beta[k] == (beta[index] if k == index else 0) for k in range(3)
            ) and beta[index] != 0), None)
            assert {alpha_line, beta_line} == {1, 2}
    assert feasible == 8
    return feasible


def local_rank_one_pencil_audit() -> tuple[int, int]:
    """Exhaust (26) and (35), including zero fixed vectors, over F_2."""

    prime = 2
    vectors = tuple(product(range(prime), repeat=3))
    f = (1, 0, 0)
    zero_matrix = ((0, 0, 0),) * 3
    target = outer(f, f, prime)

    response_solutions = 0
    for a_r, a_t, b_t, b_r in product(vectors, repeat=4):
        response = matrix_add(outer(a_r, b_t, prime), outer(a_t, b_r, prime), prime)
        if response != target:
            continue
        response_solutions += 1
        p_oriented = a_r in ((0, 0, 0), f) and a_t in ((0, 0, 0), f)
        s_oriented = b_t in ((0, 0, 0), f) and b_r in ((0, 0, 0), f)
        assert p_oriented or s_oriented

    pencil_solutions = 0
    for alpha, beta, p0, s0, p1, s1 in product(vectors, repeat=6):
        coefficient_zero = matrix_add(outer(p0, alpha, prime), outer(beta, s0, prime), prime)
        coefficient_kernel = matrix_add(outer(p1, alpha, prime), outer(beta, s1, prime), prime)
        if coefficient_zero != target or coefficient_kernel != zero_matrix:
            continue
        pencil_solutions += 1
        column_oriented = all(vector in ((0, 0, 0), f) for vector in (p0, p1, beta))
        row_oriented = all(vector in ((0, 0, 0), f) for vector in (s0, s1, alpha))
        assert column_oriented or row_oriented

    assert response_solutions > 0
    assert pencil_solutions > 0
    return response_solutions, pencil_solutions


EMPTY = -1


def monomial(*entries):
    assert len(entries) == 6
    return tuple(entries)


def sparse_clean(polynomial):
    return {term: coefficient for term, coefficient in polynomial.items() if coefficient}


def sparse_add_term(polynomial, term, coefficient):
    polynomial[term] = polynomial.get(term, Fraction(0)) + coefficient
    if polynomial[term] == 0:
        del polynomial[term]


def sparse_product(left, right):
    answer = {}
    for left_term, left_coefficient in left.items():
        for right_term, right_coefficient in right.items():
            if any(a != EMPTY and b != EMPTY for a, b in zip(left_term, right_term)):
                continue
            term = tuple(b if a == EMPTY else a for a, b in zip(left_term, right_term))
            sparse_add_term(answer, term, left_coefficient * right_coefficient)
    return sparse_clean(answer)


def divided_edge_power(edge_terms, degree):
    answer = {}
    for indices in combinations(range(len(edge_terms)), degree):
        product_term = {monomial(EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY): Fraction(1)}
        for index in indices:
            product_term = sparse_product(product_term, {edge_terms[index][0]: edge_terms[index][1]})
        for term, coefficient in product_term.items():
            sparse_add_term(answer, term, coefficient)
    return answer


def scalar_cycle_audit() -> int:
    """Verify the sharpness model as a full tensor identity over Q."""

    # At site zero the labels 0,1,2 mean e_0,e_1,e_2.  At every other
    # site label 0 is its unique z-vector.
    edges = (
        (monomial(2, 0, EMPTY, EMPTY, EMPTY, EMPTY), Fraction(2)),
        (monomial(EMPTY, 0, EMPTY, EMPTY, EMPTY, 0), Fraction(1)),
        (monomial(EMPTY, EMPTY, 0, EMPTY, EMPTY, 0), Fraction(-1)),
        (monomial(EMPTY, EMPTY, 0, EMPTY, 0, EMPTY), Fraction(1)),
        (monomial(EMPTY, EMPTY, EMPTY, 0, 0, EMPTY), Fraction(1)),
        (monomial(2, EMPTY, EMPTY, 0, EMPTY, EMPTY), Fraction(2)),
    )
    F = divided_edge_power(edges, 2)
    cube = divided_edge_power(edges, 3)
    assert cube == {}

    p = (
        {monomial(0, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY): Fraction(1)},
        {
            monomial(EMPTY, 0, EMPTY, EMPTY, EMPTY, EMPTY): Fraction(-1, 2),
            monomial(EMPTY, EMPTY, EMPTY, 0, EMPTY, EMPTY): Fraction(1, 2),
        },
        {monomial(EMPTY, EMPTY, EMPTY, EMPTY, 0, EMPTY): Fraction(1)},
    )
    s = (
        {
            monomial(EMPTY, 0, EMPTY, EMPTY, EMPTY, EMPTY): Fraction(-1, 2),
            monomial(EMPTY, EMPTY, EMPTY, 0, EMPTY, EMPTY): Fraction(1, 2),
        },
        {monomial(1, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY): Fraction(1)},
        {
            monomial(EMPTY, 0, EMPTY, EMPTY, EMPTY, EMPTY): Fraction(-1, 4),
            monomial(EMPTY, EMPTY, EMPTY, 0, EMPTY, EMPTY): Fraction(-1, 4),
        },
    )

    checked = 0
    for i in range(3):
        for j in range(3):
            response = sparse_product(sparse_product(p[i], s[j]), F)
            expected_term = monomial(i, 0, 0, 0, 0, 0)
            expected = {expected_term: Fraction(1)} if i == j else {}
            assert response == expected
            checked += 1

    incident_site_zero_labels = {
        term[0] for term, coefficient in edges if coefficient and term[0] != EMPTY
    }
    assert incident_site_zero_labels == {2}
    return checked


def main():
    term_count, histogram, complementary_count = cauchy_binet_audit()
    plane_count = coordinate_plane_incidence_audit()
    block_trials = arbitrary_block_audit()
    two_axis_count = local_two_axis_pencil_audit()
    response_count, pencil_count = local_rank_one_pencil_audit()
    scalar_responses = scalar_cycle_audit()
    print("independent sitewise common-power response filtration audit: PASS")
    print("ordered nonzero determinant terms:", term_count)
    print("site-exponent histogram:", dict(sorted(histogram.items())))
    print("complementary leading terms:", complementary_count)
    print("coordinate-plane omission assignments:", plane_count)
    print("arbitrary-rank finite-field block trials:", block_trials)
    print("two-axis pencil realizations over F_3:", two_axis_count)
    print("rank-one response/pencil solutions over F_2:", response_count, pencil_count)
    print("exact scalar-cycle response entries:", scalar_responses)


if __name__ == "__main__":
    main()
