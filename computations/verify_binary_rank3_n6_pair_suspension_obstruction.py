#!/usr/bin/env python3
"""Exact rank certificate excluding pair suspension of the known n=6 point.

All arithmetic in the audit is in F_109.  The chosen values specialize the
number field of ``verify_binary_rank3_projection_exact`` via

    i -> 33, sqrt(3) -> 49, 2^(1/3) -> 57.

The proof over characteristic zero uses six explicit kernel directions:
five universal vertex gauges and the logarithmic ``a`` derivative of the
exact two-parameter family in ``derive_binary_rank3_c3_exact``.
"""

from __future__ import annotations

import itertools


P = 109
I = 33
SQRT3 = 49
CBRT2 = 57
N = 6
Q = 2
H = ((0, 1), (-1, 1))
RHO = (2, 3, 4, 5, 0, 1)
EDGES = tuple(itertools.combinations(range(N), 2))
COLORINGS = tuple(itertools.product(range(Q), repeat=N))
COCYCLE = {
    (0, 1): -I,
    (2, 3): 1,
    (4, 5): I,
    (0, 2): I,
    (2, 4): -1,
    (0, 4): I,
    (0, 3): -I,
    (2, 5): I,
    (1, 4): 1,
    (0, 5): 1,
    (1, 2): 1,
    (3, 4): 1,
    (1, 3): -1,
    (3, 5): -I,
    (1, 5): -I,
}


def inverse(value: int) -> int:
    return pow(value % P, -1, P)


def matrix_product(left, right):
    return tuple(
        tuple(
            sum(left[i][k] * right[k][j] for k in range(Q)) % P
            for j in range(Q)
        )
        for i in range(Q)
    )


def transpose(matrix):
    return tuple(zip(*matrix))


def scale(scalar, matrix):
    return tuple(tuple(scalar * value % P for value in row) for row in matrix)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def generate_orbits(seeds):
    answer = {}
    for (u, v), seed in seeds.items():
        matrix = seed
        for _ in range(3):
            if u < v:
                answer[u, v] = matrix
            else:
                answer[v, u] = transpose(matrix)
            cocycle = COCYCLE[tuple(sorted((u, v)))]
            matrix = scale(
                cocycle,
                matrix_product(matrix_product(H, matrix), transpose(H)),
            )
            u, v = RHO[u], RHO[v]
    assert len(answer) == len(EDGES)
    return answer


def source_and_family_tangent():
    assert I * I % P == -1 % P
    assert SQRT3 * SQRT3 % P == 3
    assert CBRT2**3 % P == 2
    r = inverse(CBRT2)
    q0 = r * inverse(SQRT3) % P
    d = CBRT2 * (-SQRT3 * inverse(9) + I * inverse(6)) % P
    e = CBRT2 * (SQRT3 * inverse(36) + I * inverse(12)) % P
    half = inverse(2)
    seeds = {
        (0, 1): (
            ((r - I * q0) % P, (r - I * q0) * half % P),
            ((r - I * q0) * half % P, -I * q0 % P),
        ),
        (0, 2): ((1, 0), (1, 1)),
        (0, 3): (
            (q0, (q0 + I * r) * half % P),
            ((q0 + I * r) * half % P, (q0 + I * r) % P),
        ),
        (0, 5): (
            (I * q0 % P, (r + I * q0) * half % P),
            ((r + I * q0) * half % P, I * q0 % P),
        ),
        (1, 3): ((d, (d - e) % P), (e, d)),
    }

    zero = ((0, 0), (0, 0))
    # In the exact family, a*d and c*e are constant.  At a=c=1,
    # d/d(log a) therefore sends a -> a and d -> -d.
    tangent_seeds = {
        (0, 1): zero,
        (0, 2): ((1, 1), (0, 1)),
        (0, 3): zero,
        (0, 5): zero,
        (1, 3): ((-d % P, -d % P), (0, -d % P)),
    }
    return generate_orbits(seeds), generate_orbits(tangent_seeds)


def matching_tensor(matrices):
    answer = []
    for coloring in COLORINGS:
        coefficient = 0
        for matching in perfect_matchings(tuple(range(N))):
            term = 1
            for u, v in matching:
                term = term * matrices[u, v][coloring[u]][coloring[v]] % P
            coefficient = (coefficient + term) % P
        answer.append(coefficient)
    return answer


def hessian(matrices):
    """Derivative of the six-site matching tensor: 64 by 60."""
    answer = []
    for coloring in COLORINGS:
        row = []
        for u, v in EDGES:
            remaining = tuple(w for w in range(N) if w not in (u, v))
            cofactor = 0
            for matching in perfect_matchings(remaining):
                term = 1
                for x, y in matching:
                    term = term * matrices[x, y][coloring[x]][coloring[y]] % P
                cofactor = (cofactor + term) % P
            for a, b in itertools.product(range(Q), repeat=2):
                row.append(cofactor if (coloring[u], coloring[v]) == (a, b) else 0)
        answer.append(row)
    return answer


def rank_mod(matrix):
    work = [list(map(lambda value: value % P, row)) for row in matrix]
    row = 0
    for column in range(len(work[0])):
        pivot = next(
            (candidate for candidate in range(row, len(work)) if work[candidate][column]),
            None,
        )
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        factor = inverse(work[row][column])
        work[row] = [factor * value % P for value in work[row]]
        for other in range(len(work)):
            if other == row or not work[other][column]:
                continue
            factor = work[other][column]
            work[other] = [
                (left - factor * right) % P
                for left, right in zip(work[other], work[row])
            ]
        row += 1
        if row == len(work):
            break
    return row


def flatten(matrices):
    return [
        matrices[edge][a][b]
        for edge in EDGES
        for a, b in itertools.product(range(Q), repeat=2)
    ]


def matrix_vector_product(matrix, vector):
    return [sum(left * right for left, right in zip(row, vector)) % P for row in matrix]


def main() -> None:
    matrices, family_tangent = source_and_family_tangent()
    target = [1 + int(not any(c)) + int(all(c)) for c in COLORINGS]
    assert matching_tensor(matrices) == target

    derivative = hessian(matrices)
    gauge_vectors = []
    for vertex in range(N - 1):
        potentials = [0] * N
        potentials[vertex] = 1
        potentials[-1] = -1
        gauge_vectors.append(
            [
                (potentials[u] + potentials[v]) * matrices[u, v][a][b] % P
                for u, v in EDGES
                for a, b in itertools.product(range(Q), repeat=2)
            ]
        )
    kernel_vectors = gauge_vectors + [flatten(family_tangent)]
    assert rank_mod([list(column) for column in zip(*kernel_vectors)]) == 6
    assert all(
        matrix_vector_product(derivative, vector) == [0] * len(COLORINGS)
        for vector in kernel_vectors
    )

    assert rank_mod(derivative) == 54
    all_ones_slice = [1] * len(COLORINGS)
    augmented = [row + [value] for row, value in zip(derivative, all_ones_slice)]
    assert rank_mod(augmented) == 55

    # The direct new edge contributes a multiple of H_6, already in the
    # derivative image by Euler's identity D H_6(A)[A] = 3 H_6(A).
    assert matrix_vector_product(derivative, flatten(matrices)) == [
        3 * value % P for value in target
    ]
    print("F_109 specialization: rank Hessian=54, rank augmented=55")
    print("six independent kernels: five vertex gauges plus exact-family tangent")
    print("verified: the known n=6 point has no n=8 pair suspension")


if __name__ == "__main__":
    main()
