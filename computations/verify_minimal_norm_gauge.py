#!/usr/bin/env python3
"""Exact audits for notes/minimal-norm-gauge.md.

There are no floating-point comparisons in this file.  It checks

1. the exact active-rank-two binary gadget and its norm-lowering star
   replacement;
2. the cyclotomic full-isotropy identities and exact constant-fiber
   normalization for the six-vertex phased Fourier countermodel;
3. exact star/triangle and full-derivative ranks for that model; and
4. the tight/free subrank-three counterexample recorded in
   notes/tight-free-subrank-counterexample.md.
"""

from __future__ import annotations

from itertools import combinations, product


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for pos in range(1, len(vertices)):
        second = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def tensor_coefficients(matrices, n, q):
    zero = tuple(tuple(0 for _ in range(q)) for _ in range(q))
    result = {}
    for coloring in product(range(q), repeat=n):
        value = 0
        for matching in perfect_matchings(range(n)):
            term = 1
            for u, v in matching:
                term *= matrices.get((u, v), zero)[coloring[u]][coloring[v]]
            value += term
        result[coloring] = value
    return result


def verify_binary_star_replacement():
    e00 = ((1, 0), (0, 0))
    e11 = ((0, 0), (0, 1))
    zero = ((0, 0), (0, 0))
    original = {
        (0, 1): e00,
        (2, 3): ((1, 0), (0, 1)),
        (0, 2): ((0, -1), (0, 0)),
        (1, 3): ((0, 1), (0, 0)),
        (4, 5): e00,
        (0, 5): e11,
        (1, 2): e11,
        (3, 4): e11,
    }

    target = {
        coloring: int(len(set(coloring)) == 1)
        for coloring in product(range(2), repeat=6)
    }
    assert tensor_coefficients(original, 6, 2) == target

    # Every displayed edge has a nonzero complementary matching tensor.
    for edge in original:
        complement = tuple(v for v in range(6) if v not in edge)
        relabel = {old: new for new, old in enumerate(complement)}
        submatrices = {}
        for (u, v), matrix in original.items():
            if u in relabel and v in relabel:
                submatrices[(relabel[u], relabel[v])] = matrix
        cofactor = tensor_coefficients(submatrices, 4, 2)
        assert any(value != 0 for value in cofactor.values()), edge

    assert original[(2, 3)][0][0] * original[(2, 3)][1][1] == 1

    # The vertex-2 star has norm squared four.  Its exact least-norm
    # competitor displayed in the note has norm squared two.
    def matrix_norm_squared(matrix):
        return sum(value * value for row in matrix for value in row)

    old_star_norm = sum(
        matrix_norm_squared(matrix)
        for edge, matrix in original.items()
        if 2 in edge
    )
    assert old_star_norm == 4

    replaced = dict(original)
    replaced[(0, 2)] = zero
    replaced[(2, 3)] = e00
    assert tensor_coefficients(replaced, 6, 2) == target
    new_star_norm = sum(
        matrix_norm_squared(matrix)
        for edge, matrix in replaced.items()
        if 2 in edge
    )
    assert new_star_norm == 2

    # Edge 13 is now inactive; deleting it gives the norm-six cycle model.
    del replaced[(1, 3)]
    assert tensor_coefficients(replaced, 6, 2) == target
    assert sum(matrix_norm_squared(m) for m in replaced.values()) == 6


# Exact Eisenstein integers a+b*w, with w^2+w+1=0.
def zadd(x, y):
    return x[0] + y[0], x[1] + y[1]


def zmul(x, y):
    a, b = x
    c, d = y
    return a * c - b * d, a * d + b * c - b * d


def zconj(x):
    # conjugation sends w to w^2=-1-w
    a, b = x
    return a - b, -b


Z0 = (0, 0)
Z1 = (1, 0)
ZW = (0, 1)
ZW2 = (-1, -1)


def zmatmul(left, right):
    rows = len(left)
    inner = len(right)
    columns = len(right[0])
    answer = [[Z0 for _ in range(columns)] for _ in range(rows)]
    for i in range(rows):
        for j in range(columns):
            for k in range(inner):
                answer[i][j] = zadd(answer[i][j], zmul(left[i][k], right[k][j]))
    return answer


def zadjoint(matrix):
    return [
        [zconj(matrix[i][j]) for i in range(len(matrix))]
        for j in range(len(matrix[0]))
    ]


def ztranspose(matrix):
    return [list(row) for row in zip(*matrix)]


FOURIER_FACTORS = [
    ((0, 1), (2, 3), (4, 5)),
    ((0, 5), (1, 2), (3, 4)),
    ((0, 2), (1, 4), (3, 5)),
    ((0, 3), (1, 5), (2, 4)),
    ((0, 4), (1, 3), (2, 5)),
]

# Unit Eisenstein phases.  They preserve every Gram matrix.  Their products
# make each anchor matching have weight one and make the three non-anchor
# contributions in every constant-color fiber cancel.
FOURIER_PHASES = {
    (0, 5): ZW2,
    (3, 4): ZW2,
    (0, 4): ZW2,
    (2, 5): ZW,
}


def verify_fourier_isotropy():
    one_factors = FOURIER_FACTORS
    assert len({edge for factor in one_factors for edge in factor}) == 15

    fourier = [
        [Z1, Z1, Z1],
        [Z1, ZW, ZW2],
        [Z1, ZW2, ZW],
    ]
    identity3 = [
        [(3, 0) if i == j else Z0 for j in range(3)] for i in range(3)
    ]
    assert zmatmul(fourier, zadjoint(fourier)) == identity3
    assert zmatmul(zadjoint(fourier), fourier) == identity3

    matrices = {}
    for edge in one_factors[0] + one_factors[1]:
        matrices[edge] = fourier
    for color, factor in enumerate(one_factors[2:]):
        anchor = [
            [Z1 if i == color and j == color else Z0 for j in range(3)]
            for i in range(3)
        ]
        for edge in factor:
            matrices[edge] = anchor
    for edge, phase in FOURIER_PHASES.items():
        matrices[edge] = [
            [zmul(phase, entry) for entry in row] for row in matrices[edge]
        ]

    # Sum the reduced Gram matrices at each endpoint exactly.
    seven_identity = [
        [(7, 0) if i == j else Z0 for j in range(3)] for i in range(3)
    ]
    for vertex in range(6):
        reduced_sum = [[Z0 for _ in range(3)] for _ in range(3)]
        for (u, v), matrix in matrices.items():
            if vertex == u:
                reduced = zmatmul(matrix, zadjoint(matrix))
            elif vertex == v:
                transposed = ztranspose(matrix)
                reduced = zmatmul(transposed, zadjoint(transposed))
            else:
                continue
            reduced_sum = [
                [zadd(reduced_sum[i][j], reduced[i][j]) for j in range(3)]
                for i in range(3)
            ]
        assert reduced_sum == seven_identity, vertex

    # Both Fourier one-factors support every coloring, while Q_i supports
    # the constant-i coloring.
    for coloring in product(range(3), repeat=6):
        supported = []
        for matching in perfect_matchings(range(6)):
            if all(matrices[edge][coloring[edge[0]]][coloring[edge[1]]] != Z0 for edge in matching):
                supported.append(matching)
        assert one_factors[0] in supported
        assert one_factors[1] in supported
        assert len(supported) >= 2
        if len(set(coloring)) == 1:
            assert one_factors[2 + coloring[0]] in supported

    # The phase choice normalizes the complete constant-color coefficients,
    # not just the three selected anchor monomials.
    def coefficient(coloring):
        coefficient = Z0
        for matching in perfect_matchings(range(6)):
            term = Z1
            for edge in matching:
                term = zmul(
                    term,
                    matrices[edge][coloring[edge[0]]][coloring[edge[1]]],
                )
            coefficient = zadd(coefficient, term)
        return coefficient

    for color in range(3):
        value = coefficient((color,) * 6)
        assert value == Z1, (color, value)

    # The selected-factor cancellation-cycle mechanism can occur at this
    # smooth local minimum even though the complete output is not GHZ.
    # Select P in color 0, Q_1 in color 1, and Q_2 in color 2.  Their
    # decorated union has the fourth matching below, with coloring
    # (2,1,0,0,2,1).  Its selected monomial has value w^2, and the full
    # mixed fiber vanishes by the two additional terms w and 1.
    selected = (one_factors[0], one_factors[3], one_factors[4])
    fourth = ((0, 4), (1, 5), (2, 3))
    cycle_coloring = (2, 1, 0, 0, 2, 1)
    decorated_occurrences = {
        (edge, color)
        for color, matching in enumerate(selected)
        for edge in matching
    }
    for edge in fourth:
        color = cycle_coloring[edge[0]]
        assert cycle_coloring[edge[1]] == color
        assert (edge, color) in decorated_occurrences

    nonzero_cycle_terms = []
    for matching in perfect_matchings(range(6)):
        term = Z1
        for edge in matching:
            term = zmul(
                term,
                matrices[edge][cycle_coloring[edge[0]]]
                              [cycle_coloring[edge[1]]],
            )
        if term != Z0:
            nonzero_cycle_terms.append((matching, term))
    assert nonzero_cycle_terms == [
        (one_factors[0], ZW),
        (fourth, ZW2),
        (one_factors[1], Z1),
    ]
    assert coefficient(cycle_coloring) == Z0

    # The model is not a GHZ preimage: this mixed coefficient is 1+w.
    assert coefficient((0, 1, 0, 0, 0, 0)) == zadd(Z1, ZW)


def rank_mod_prime(matrix, prime):
    """Exact row rank over F_prime."""
    rows = [list(map(lambda value: value % prime, row)) for row in matrix]
    if not rows:
        return 0
    row_count = len(rows)
    column_count = len(rows[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], -1, prime)
        rows[pivot_row] = [
            value * inverse % prime for value in rows[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row or not rows[row][column]:
                continue
            multiplier = rows[row][column]
            rows[row] = [
                (left - multiplier * right) % prime
                for left, right in zip(rows[row], rows[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def verify_full_block_injectivity_mod7():
    """Certify cofactor-map injectivity in the Fourier model.

    The homomorphism Z[w] -> F_7 sending w to 2 is valid because
    2^2+2+1=0 mod 7.  Full rank after this reduction proves that the
    corresponding cyclotomic minors are nonzero over C.
    """
    n = 6
    q = 3
    prime = 7
    omega = 2
    edges = tuple(combinations(range(n), 2))
    one_factors = FOURIER_FACTORS
    fourier = tuple(
        tuple(pow(omega, i * j, prime) for j in range(q)) for i in range(q)
    )
    matrices = {}
    for edge in one_factors[0] + one_factors[1]:
        matrices[edge] = fourier
    for color, factor in enumerate(one_factors[2:]):
        anchor = tuple(
            tuple(int(i == color and j == color) for j in range(q))
            for i in range(q)
        )
        for edge in factor:
            matrices[edge] = anchor
    phases_mod_prime = {
        edge: (phase[0] + phase[1] * omega) % prime
        for edge, phase in FOURIER_PHASES.items()
    }
    for edge, phase in phases_mod_prime.items():
        matrices[edge] = tuple(
            tuple(phase * entry % prime for entry in row)
            for row in matrices[edge]
        )

    def subset_tensor(vertices):
        vertices = tuple(vertices)
        answer = {}
        for coloring in product(range(q), repeat=len(vertices)):
            local_color = dict(zip(vertices, coloring))
            value = 0
            for matching in perfect_matchings(vertices):
                term = 1
                for edge in matching:
                    term *= matrices[edge][local_color[edge[0]]][local_color[edge[1]]]
                value += term
            answer[coloring] = value % prime
        return answer

    cofactors = {
        edge: subset_tensor(vertex for vertex in range(n) if vertex not in edge)
        for edge in edges
    }
    full_colorings = tuple(product(range(q), repeat=n))

    def block_matrix(block_edges):
        columns = []
        for edge in block_edges:
            rest = tuple(vertex for vertex in range(n) if vertex not in edge)
            cofactor = cofactors[edge]
            for left_color in range(q):
                for right_color in range(q):
                    column = []
                    for coloring in full_colorings:
                        if (
                            coloring[edge[0]] == left_color
                            and coloring[edge[1]] == right_color
                        ):
                            column.append(
                                cofactor[tuple(coloring[vertex] for vertex in rest)]
                            )
                        else:
                            column.append(0)
                    columns.append(column)
        # Transpose to the conventional row-major form.
        return [list(row) for row in zip(*columns)]

    for vertex in range(n):
        star = tuple(edge for edge in edges if vertex in edge)
        matrix = block_matrix(star)
        assert rank_mod_prime(matrix, prime) == len(star) * q * q

    for triangle in combinations(range(n), 3):
        triangle_edges = tuple(combinations(triangle, 2))
        matrix = block_matrix(triangle_edges)
        assert rank_mod_prime(matrix, prime) == len(triangle_edges) * q * q

    # The same calculation for all 15 edges is the full derivative of the
    # matching-tensor map.  Its five-dimensional kernel is exactly the
    # universal scalar vertex gauge
    #
    #     X_uv = (p_u + p_v) A_uv,       sum_v p_v = 0.
    #
    # Indeed these five independent directions are visibly in the kernel,
    # while the rank computation says that the kernel has dimension five.
    # Thus there is no additional infinitesimal fixed-output move, such as
    # a square/urban-renewal direction, at this isotropic model.
    matrix = block_matrix(edges)
    derivative_rank = rank_mod_prime(matrix, prime)
    assert derivative_rank == len(edges) * q * q - (n - 1), derivative_rank


def verify_tight_free_counterexample():
    support = [
        ("0", "0", "0", "0"),
        ("1", "1", "1", "1"),
        ("2", "2", "2", "2"),
        ("0", "1", "0", "1"),
        ("p", "1", "p", "1"),
    ]
    coefficients = [1, 1, 1, 1, -1]
    weights = [
        {"0": 0, "1": 1, "2": 3, "p": 2},
        {"0": 0, "1": 1, "2": 2},
        {"0": 0, "1": -1, "2": 3, "p": -2},
        {"0": 0, "1": -1, "2": -8},
    ]

    # Free means that deleting any one coordinate is injective on support.
    for left, right in combinations(support, 2):
        assert sum(x != y for x, y in zip(left, right)) >= 2

    # Tightness with injective integer weights.
    for local_weights in weights:
        assert len(set(local_weights.values())) == len(local_weights)
    for term in support:
        assert sum(weights[mode][symbol] for mode, symbol in enumerate(term)) == 0

    # Tight row normalization keeps colors 1 and 2 but loses color 0 for
    # this explicit cocharacter: its three minimum-weight sums are -2,0,0.
    output_color = {
        "0": 0,
        "1": 1,
        "2": 2,
        "p": 0,
    }
    minimum_sums = []
    for color in range(3):
        total = 0
        for mode, local_weights in enumerate(weights):
            candidates = [
                value
                for symbol, value in local_weights.items()
                if output_color[symbol] == color
            ]
            total += min(candidates)
        minimum_sums.append(total)
    assert minimum_sums == [-2, 0, 0]

    # The stated local linear maps send p and 0 to the same output basis
    # vector.  The two mixed terms cancel exactly.
    image = {}
    for term, coefficient in zip(support, coefficients):
        output = tuple(0 if symbol == "p" else int(symbol) for symbol in term)
        image[output] = image.get(output, 0) + coefficient
    image = {term: value for term, value in image.items() if value}
    assert image == {
        (0, 0, 0, 0): 1,
        (1, 1, 1, 1): 1,
        (2, 2, 2, 2): 1,
    }

    # A monomial restriction to a diagonal is an induced matching in the
    # support hypergraph.  Exhaust all subsets and certify the maximum is 2.
    def is_induced_matching(subset):
        size = len(subset)
        if any(len({term[mode] for term in subset}) != size for mode in range(4)):
            return False
        coordinate_sets = [
            {term[mode] for term in subset} for mode in range(4)
        ]
        surviving = {
            term
            for term in support
            if all(term[mode] in coordinate_sets[mode] for mode in range(4))
        }
        return surviving == set(subset)

    maximum = 0
    witnesses = []
    for size in range(1, len(support) + 1):
        current = [
            subset
            for subset in combinations(support, size)
            if is_induced_matching(subset)
        ]
        if current:
            maximum = size
            witnesses = current
    assert maximum == 2
    assert witnesses

    # Incidence rectangle completion propagates the putative mixed
    # cancellation to its all-zero partner.  These are arbitrary exact
    # integer weights satisfying a_p=-a_0.
    a0, a1, ap, b0, b1 = 1, 2, -1, 3, 5
    assert a0 * b1 + ap * b1 == 0
    assert a0 * b0 + ap * b0 == 0


def main():
    verify_binary_star_replacement()
    verify_fourier_isotropy()
    verify_full_block_injectivity_mod7()
    verify_tight_free_counterexample()
    print("verified exact binary star replacement")
    print("verified exact cyclotomic full-isotropy countermodel")
    print(
        "verified Fourier-model block injectivity and gauge-only derivative "
        "kernel modulo 7"
    )
    print("verified tight/free subrank=3 but monomial subrank=2")


if __name__ == "__main__":
    main()
