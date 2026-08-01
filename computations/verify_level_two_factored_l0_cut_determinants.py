#!/usr/bin/env python3
"""Exact audit of the factored-L0 cut determinant identities.

Research evidence only.  Krenn's conjecture remains open, SP-CLEAN-BRIDGE
is untouched, and no certified dependency changes.

At differential rank 55 with kernel equal to the five vertex gauges, four
binary endpoint slices can be normalized to packets

    K^st_ru + (lambda^st_r + lambda^st_u) M_ru.

If these packets come from two physical endpoint stars, every site cut has
the pencil factorization

    B(A) = [U_A V_A] [[0,A],[A^T,0]] [U_B V_B]^T.

This checker verifies formally that all 5x5 minors vanish, every 4x4 minor
is a scalar multiple of det(A)^2, and every 3x3 minor is divisible by
det(A).  It also audits the mixed-slice four-cycle holonomy identity and an
exhaustive characteristic-zero sign-class enumeration proving that the
only C4-free nonzero-sum graphs on six labelled vertices are the empty
graph, six stars, and ten disjoint pairs of triangles.

Standard library only; all checks remain live under python -O and
python -I -S.
"""

from fractions import Fraction as Q
from itertools import combinations, permutations, product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


SITES = tuple(range(6))
EDGES = tuple(combinations(SITES, 2))
ZERO_EXPONENT = (0, 0, 0, 0)


# ---------------------------------------------------------------------------
# Sparse polynomials in a00,a01,a10,a11.


def polynomial_constant(value):
    return {ZERO_EXPONENT: value} if value else {}


def polynomial_variable(index):
    exponent = [0] * 4
    exponent[index] = 1
    return {tuple(exponent): 1}


VARIABLES = tuple(polynomial_variable(index) for index in range(4))


def polynomial_add(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            answer[exponent] = answer.get(exponent, 0) + coefficient
            if not answer[exponent]:
                del answer[exponent]
    return answer


def polynomial_scale(coefficient, polynomial):
    return {
        exponent: coefficient * value
        for exponent, value in polynomial.items()
        if coefficient * value
    }


def polynomial_multiply(left, right):
    answer = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = tuple(a + b for a, b in zip(
                left_exponent, right_exponent
            ))
            answer[exponent] = (
                answer.get(exponent, 0)
                + left_coefficient * right_coefficient
            )
            if not answer[exponent]:
                del answer[exponent]
    return answer


def permutation_sign(permutation):
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def polynomial_determinant(matrix):
    size = len(matrix)
    require(all(len(row) == size for row in matrix), "determinant not square")
    answer = {}
    for permutation in permutations(range(size)):
        term = polynomial_constant(permutation_sign(permutation))
        for row, column in enumerate(permutation):
            term = polynomial_multiply(term, matrix[row][column])
            if not term:
                break
        answer = polynomial_add(answer, term)
    return answer


def numeric_determinant(matrix):
    return next(iter(polynomial_determinant([
        [polynomial_constant(value) for value in row]
        for row in matrix
    ]).values()), 0)


def submatrix(matrix, rows, columns):
    return [[matrix[row][column] for column in columns] for row in rows]


def divides_by_det_a(cubic, determinant_a):
    """Return the exact linear quotient, or fail if det(A) does not divide."""

    leading_exponents = (
        (2, 0, 0, 1),
        (1, 1, 0, 1),
        (1, 0, 1, 1),
        (1, 0, 0, 2),
    )
    quotient = polynomial_add(*(
        polynomial_scale(cubic.get(exponent, 0), VARIABLES[index])
        for index, exponent in enumerate(leading_exponents)
    ))
    require(
        polynomial_multiply(determinant_a, quotient) == cubic,
        ("a cubic minor is not divisible by det(A)", cubic),
    )
    return quotient


# ---------------------------------------------------------------------------
# Formal cut-pencil identities.


def outer(left, right):
    return [[left[row] * right[column] for column in range(len(right))]
            for row in range(len(left))]


def add_numeric_matrices(left, right):
    return [[a + b for a, b in zip(left_row, right_row)]
            for left_row, right_row in zip(left, right)]


def columns_to_rows(columns):
    return [list(row) for row in zip(*columns)]


def build_cut_data():
    # Vandermonde columns make both displayed 6x4 factor matrices rank four.
    left_parameters = tuple(range(1, 7))
    right_parameters = tuple(range(7, 13))
    u_left = columns_to_rows((
        tuple(1 for _ in left_parameters), left_parameters
    ))
    v_left = columns_to_rows((
        tuple(value**2 for value in left_parameters),
        tuple(value**3 for value in left_parameters),
    ))
    u_right = columns_to_rows((
        tuple(1 for _ in right_parameters), right_parameters
    ))
    v_right = columns_to_rows((
        tuple(value**2 for value in right_parameters),
        tuple(value**3 for value in right_parameters),
    ))

    slices = {}
    for source_colour, target_colour in product(range(2), repeat=2):
        first = outer(
            [row[source_colour] for row in u_left],
            [row[target_colour] for row in v_right],
        )
        second = outer(
            [row[target_colour] for row in v_left],
            [row[source_colour] for row in u_right],
        )
        slices[source_colour, target_colour] = add_numeric_matrices(
            first, second
        )

    pencil = [[{} for _ in range(6)] for _ in range(6)]
    for row in range(6):
        for column in range(6):
            pencil[row][column] = polynomial_add(*(
                polynomial_scale(
                    slices[source_colour, target_colour][row][column],
                    VARIABLES[2 * source_colour + target_colour],
                )
                for source_colour, target_colour in product(range(2), repeat=2)
            ))

    left_factor = [u_left[row] + v_left[row] for row in range(6)]
    right_factor = [u_right[row] + v_right[row] for row in range(6)]
    return pencil, left_factor, right_factor


def audit_cut_pencil():
    pencil, left_factor, right_factor = build_cut_data()
    require(numeric_determinant(submatrix(
        left_factor, range(4), range(4)
    )) != 0, "left cut factor lost rank four")
    require(numeric_determinant(submatrix(
        right_factor, range(4), range(4)
    )) != 0, "right cut factor lost rank four")

    determinant_a = polynomial_add(
        polynomial_multiply(VARIABLES[0], VARIABLES[3]),
        polynomial_scale(-1, polynomial_multiply(VARIABLES[1], VARIABLES[2])),
    )
    determinant_a_squared = polynomial_multiply(determinant_a, determinant_a)

    five_checks = 0
    for rows in combinations(range(6), 5):
        for columns in combinations(range(6), 5):
            require(
                not polynomial_determinant(submatrix(pencil, rows, columns)),
                ("a 5x5 pencil minor is nonzero", rows, columns),
            )
            five_checks += 1

    four_checks = 0
    for rows in combinations(range(6), 4):
        left_minor = numeric_determinant(submatrix(
            left_factor, rows, range(4)
        ))
        for columns in combinations(range(6), 4):
            right_minor = numeric_determinant(submatrix(
                right_factor, columns, range(4)
            ))
            expected = polynomial_scale(
                left_minor * right_minor, determinant_a_squared
            )
            actual = polynomial_determinant(submatrix(pencil, rows, columns))
            require(actual == expected,
                    ("a 4x4 pencil minor is not det(A)^2", rows, columns))
            four_checks += 1

    three_checks = 0
    nonzero_quotients = 0
    for rows in combinations(range(6), 3):
        for columns in combinations(range(6), 3):
            minor = polynomial_determinant(submatrix(pencil, rows, columns))
            quotient = divides_by_det_a(minor, determinant_a)
            nonzero_quotients += bool(quotient)
            three_checks += 1
    require(nonzero_quotients > 0, "3x3 divisibility audit became vacuous")
    require((five_checks, four_checks, three_checks) == (36, 225, 400),
            "wrong cut-minor census")
    return five_checks, four_checks, three_checks, nonzero_quotients


# ---------------------------------------------------------------------------
# Gauge/direct normalization.


def audit_gauge_normalization():
    mus = (
        (1, 2, 3, 4, 5, -15),
        (2, -1, 4, -3, 7, -9),
        (5, 1, -2, 6, -4, -6),
        (3, -5, 8, 1, -7, 0),
    )
    direct_weights = (3, -2, 5, 7)
    eta = (2, -3, 5, -7, 11, -8)
    require(sum(eta) == 0, "preimage-shift gauge is not trace zero")
    checks = 0
    for mu, direct in zip(mus, direct_weights):
        require(sum(mu) == 0, "slice gauge is not trace zero")
        lam = tuple(Q(value) - Q(direct, 6) for value in mu)
        require(sum(lam) == -direct, "direct weight was not absorbed")
        shifted = tuple(value - change for value, change in zip(lam, eta))
        require(sum(shifted) == -direct,
                "preimage change altered the direct weight")
        for r, u in EDGES:
            require(
                lam[r] + lam[u]
                == Q(mu[r] + mu[u]) - Q(direct, 3),
                "lambda normalization failed",
            )
            # K -> K+G(eta), lambda -> lambda-eta leaves K+G(lambda).
            require(
                eta[r] + eta[u] + shifted[r] + shifted[u]
                == lam[r] + lam[u],
                "normalized packet depends on the chosen preimage",
            )
            checks += 2
    require(checks == 120, "wrong gauge-normalization count")
    return checks


# ---------------------------------------------------------------------------
# Mixed-slice K2,2 curvature identity.


J = ((0, 1), (1, 0))


def transpose(matrix):
    return tuple(tuple(matrix[column][row] for column in range(2))
                 for row in range(2))


def matrix_product(left, right):
    return tuple(tuple(sum(left[row][middle] * right[middle][column]
                           for middle in range(2))
                       for column in range(2))
                 for row in range(2))


def matrix_scale(scalar, matrix):
    return tuple(tuple(scalar * value for value in row) for row in matrix)


def determinant_2(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def inverse_2(matrix):
    determinant = determinant_2(matrix)
    require(determinant != 0, "attempted to invert a singular block")
    return matrix_scale(Q(1, determinant), (
        (matrix[1][1], -matrix[0][1]),
        (-matrix[1][0], matrix[0][0]),
    ))


def matrix_equal(left, right):
    return all(left[row][column] == right[row][column]
               for row in range(2) for column in range(2))


def scalar_matrix(matrix):
    return matrix[0][1] == matrix[1][0] == 0 and matrix[0][0] == matrix[1][1]


def rational_rank(matrix):
    rows = [[Q(value) for value in row] for row in matrix]
    rank = 0
    width = len(rows[0]) if rows else 0
    for column in range(width):
        pivot = next((slot for slot in range(rank, len(rows))
                      if rows[slot][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for slot in range(len(rows)):
            if slot == rank or not rows[slot][column]:
                continue
            multiple = rows[slot][column]
            rows[slot] = [left - multiple * right
                          for left, right in zip(rows[slot], rows[rank])]
        rank += 1
    return rank


def audit_projective_holonomy():
    site_factors = (
        ((1, 2), (3, 5)),
        ((2, 1), (5, 4)),
        ((3, 2), (4, 7)),
        ((5, 3), (2, 9)),
    )
    require(all(determinant_2(matrix) != 0 for matrix in site_factors),
            "a site factor is singular")
    lam = (1, 2, 4, 8)
    n_blocks = {}
    m_blocks = {}
    for r in (0, 1):
        for u in (2, 3):
            n_block = matrix_product(matrix_product(
                site_factors[r], J
            ), transpose(site_factors[u]))
            coefficient = lam[r] + lam[u]
            n_blocks[r, u] = n_block
            m_blocks[r, u] = matrix_scale(Q(1, coefficient), n_block)
            require(determinant_2(n_block) != 0,
                    "a live cut block is singular")

    block_matrix = [
        list(n_blocks[0, 2][row] + n_blocks[0, 3][row])
        for row in range(2)
    ] + [
        list(n_blocks[1, 2][row] + n_blocks[1, 3][row])
        for row in range(2)
    ]
    require(rational_rank(block_matrix) == 2,
            "the factored K2,2 cut lost rank two")

    reconstructed = matrix_product(matrix_product(
        n_blocks[1, 2], inverse_2(n_blocks[0, 2])
    ), n_blocks[0, 3])
    require(matrix_equal(reconstructed, n_blocks[1, 3]),
            "rank-two anchor reconstruction failed")

    holonomy = matrix_product(matrix_product(
        inverse_2(m_blocks[1, 3]), m_blocks[1, 2]
    ), matrix_product(inverse_2(m_blocks[0, 2]), m_blocks[0, 3]))
    require(scalar_matrix(holonomy), "projective holonomy is not scalar")
    expected_scalar = Q(
        (lam[0] + lam[2]) * (lam[1] + lam[3]),
        (lam[1] + lam[2]) * (lam[0] + lam[3]),
    )
    require(holonomy[0][0] == expected_scalar,
            "projective-holonomy scalar is wrong")

    mutated = dict(m_blocks)
    mutable = [list(row) for row in mutated[1, 3]]
    mutable[0][0] += 1
    mutated[1, 3] = tuple(tuple(row) for row in mutable)
    mutated_holonomy = matrix_product(matrix_product(
        inverse_2(mutated[1, 3]), mutated[1, 2]
    ), matrix_product(inverse_2(mutated[0, 2]), mutated[0, 3]))
    require(not scalar_matrix(mutated_holonomy),
            "holonomy mutation escaped detection")


# ---------------------------------------------------------------------------
# Exhaustive abstract sign-class classification.


def set_partitions(items):
    items = tuple(items)
    if not items:
        yield ()
        return
    head = items[0]
    for tail_partition in set_partitions(items[1:]):
        yield ((head,),) + tail_partition
        for index in range(len(tail_partition)):
            block = tail_partition[index]
            yield tail_partition[:index] + ((head,) + block,) + tail_partition[index + 1:]


def partial_matchings(items):
    items = tuple(items)
    if not items:
        yield ()
        return
    head = items[0]
    for tail in partial_matchings(items[1:]):
        yield tail
    for index, partner in enumerate(items[1:], 1):
        rest = items[1:index] + items[index + 1:]
        for tail in partial_matchings(rest):
            yield ((head, partner),) + tail


def live_graph_from_sign_classes(partition, zero_class, opposite_pairs):
    zero_edges = set()
    if zero_class is not None:
        zero_edges.update(combinations(partition[zero_class], 2))
    for first, second in opposite_pairs:
        zero_edges.update(
            tuple(sorted((left, right)))
            for left in partition[first] for right in partition[second]
        )
    return frozenset(edge for edge in EDGES if edge not in zero_edges)


def contains_k22(live_edges):
    for vertices in combinations(SITES, 4):
        a, b, c, d = vertices
        for left, right in (
            ((a, b), (c, d)),
            ((a, c), (b, d)),
            ((a, d), (b, c)),
        ):
            if all(tuple(sorted((u, v))) in live_edges
                   for u in left for v in right):
                return True
    return False


def graph_from_potentials(potentials):
    return frozenset(
        (r, u) for r, u in EDGES if potentials[r] + potentials[u] != 0
    )


def expected_c4_free_graphs():
    answer = {frozenset()}
    for centre in SITES:
        answer.add(frozenset(tuple(sorted((centre, other)))
                             for other in SITES if other != centre))
    for first_triangle in combinations(SITES, 3):
        if 0 not in first_triangle:
            continue
        second_triangle = tuple(site for site in SITES
                                if site not in first_triangle)
        answer.add(frozenset(
            tuple(combinations(first_triangle, 2))
            + tuple(combinations(second_triangle, 2))
        ))
    require(len(answer) == 17, "wrong expected graph count")
    return answer


def audit_no_flat_support_classification():
    observed = set()
    partition_count = 0
    sign_configurations = 0
    for partition in set_partitions(SITES):
        # Canonical block order removes repetitions generated by insertion.
        partition = tuple(sorted((tuple(sorted(block)) for block in partition),
                                 key=lambda block: block[0]))
        partition_count += 1
        classes = tuple(range(len(partition)))
        for zero_class in (None,) + classes:
            remaining = tuple(index for index in classes if index != zero_class)
            for opposite_pairs in partial_matchings(remaining):
                sign_configurations += 1
                live = live_graph_from_sign_classes(
                    partition, zero_class, opposite_pairs
                )
                if not contains_k22(live):
                    observed.add(live)

    # set_partitions above is canonical for a fixed input order.
    require(partition_count == 203, ("wrong Bell number", partition_count))
    expected = expected_c4_free_graphs()
    require(observed == expected,
            ("C4-free sign-class classification changed", len(observed)))

    representatives = {graph_from_potentials((0,) * 6)}
    representatives.update(
        graph_from_potentials(tuple(1 if site == centre else 0
                                    for site in SITES))
        for centre in SITES
    )
    representatives.update(
        graph_from_potentials(tuple(1 if site in triangle else -1
                                    for site in SITES))
        for triangle in combinations(SITES, 3) if 0 in triangle
    )
    require(representatives == expected,
            "rational representatives do not realize all 17 graphs")
    return partition_count, sign_configurations, len(observed)


def main():
    normalization_checks = audit_gauge_normalization()
    minor_counts = audit_cut_pencil()
    audit_projective_holonomy()
    classification = audit_no_flat_support_classification()
    print(
        "factored-L0 cut determinants: "
        f"{normalization_checks} normalization identities; "
        f"minors 5/4/3={minor_counts[:3]}, "
        f"nonzero cubic quotients={minor_counts[3]}"
    )
    print(
        "mixed K2,2 holonomy: scalar identity and mutation PASS; "
        f"sign-class census partitions/configurations/C4-free="
        f"{classification[0]}/{classification[1]}/{classification[2]}"
    )


if __name__ == "__main__":
    main()
