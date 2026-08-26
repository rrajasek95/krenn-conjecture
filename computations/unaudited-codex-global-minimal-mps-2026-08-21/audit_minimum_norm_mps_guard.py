#!/usr/bin/env python3
"""Exact minimum-norm/block-normal guard for the global MPS quotient."""

from __future__ import annotations

from itertools import combinations, product
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "computations"))
import audit_global_minimal_mps as mps  # noqa: E402
import verify_minimal_norm_gauge as gauge  # noqa: E402


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def n4_matrices():
    zero = tuple(tuple(0 for _ in range(3)) for _ in range(3))
    matrices = {edge: zero for edge in combinations(range(4), 2)}
    _, matchings = mps.n4_source()
    for colour, matching in matchings.items():
        matrix = tuple(tuple(int(i == colour and j == colour)
                             for j in range(3)) for i in range(3))
        for edge in matching:
            matrices[edge] = matrix
    return matrices


def subset_tensor(matrices, vertices, q=3):
    vertices = tuple(vertices)
    answer = {}
    for colouring in product(range(q), repeat=len(vertices)):
        local = dict(zip(vertices, colouring))
        value = 0
        for matching in gauge.perfect_matchings(vertices):
            term = 1
            for edge in matching:
                term *= matrices[edge][local[edge[0]]][local[edge[1]]]
            value += term
        answer[colouring] = value
    return answer


def block_matrix(matrices, n, block_edges, q=3):
    colourings = tuple(product(range(q), repeat=n))
    columns = []
    for edge in block_edges:
        rest = tuple(vertex for vertex in range(n) if vertex not in edge)
        cofactor = subset_tensor(matrices, rest, q)
        for a, b in product(range(q), repeat=2):
            column = []
            for colouring in colourings:
                if colouring[edge[0]] == a and colouring[edge[1]] == b:
                    column.append(cofactor[tuple(colouring[v] for v in rest)])
                else:
                    column.append(0)
            columns.append(column)
    return [list(row) for row in zip(*columns)]


def n4_minimum_block_guard():
    matrices = n4_matrices()
    edges = tuple(combinations(range(4), 2))
    star_ranks = []
    for vertex in range(4):
        star = tuple(edge for edge in edges if vertex in edge)
        rank = mps.exact_rank(block_matrix(matrices, 4, star))
        star_ranks.append(rank)
        require(rank == 27, (vertex, rank))
    triangle_ranks = []
    for triangle in combinations(range(4), 3):
        block = tuple(combinations(triangle, 2))
        rank = mps.exact_rank(block_matrix(matrices, 4, block))
        triangle_ranks.append(rank)
        require(rank == 27, (triangle, rank))

    source, _ = mps.n4_source()
    prefix = (0, 1)
    vector = mps.forward(prefix, source, 4)
    witness = ((0, 0), (1, 1))
    require(vector == {witness: mps.ONE}, vector)
    require(not mps.is_observable(witness, source, 2, 4), witness)
    completions = {
        suffix: mps.completion(witness, suffix, 2, source, 4)
        for suffix in product(range(3), repeat=2)
    }
    require(not any(completions.values()), completions)

    # The witness has squared norm six.  For each colour, writing the three
    # left-edge and opposite-edge coordinates as p,q gives
    # |p.q| <= ||p|| ||q|| <= (||p||^2+||q||^2)/2.  H_c=1 therefore costs
    # at least two; summing the three disjoint diagonal colour packets costs
    # at least six.  The displayed source attains equality.
    norm = len(source)
    require(norm == 6, norm)
    return {
        "global_minimum_norm_squared": norm,
        "minimum_proof": "three pure Cauchy-AMGM lower bounds, 2 per colour",
        "star_block_ranks": star_ranks,
        "triangle_block_ranks": triangle_ranks,
        "block_kernels": 0,
        "cut": 2,
        "prefix": prefix,
        "reachable_unobservable_state": witness,
        "all_nine_suffix_completions_zero": True,
        "meaning": (
            "This exact global norm minimum has no star/triangle affine "
            "kernel at all, yet its literal matching automaton has a "
            "reachable top-Hankel radical state."
        ),
    }


def fourier_source_mod7():
    prime, omega, q = 7, 2, 3
    fourier = tuple(tuple(pow(omega, i*j, prime) for j in range(q))
                    for i in range(q))
    matrices = {}
    for edge in gauge.FOURIER_FACTORS[0] + gauge.FOURIER_FACTORS[1]:
        matrices[edge] = fourier
    for colour, factor in enumerate(gauge.FOURIER_FACTORS[2:]):
        anchor = tuple(tuple(int(i == colour and j == colour)
                             for j in range(q)) for i in range(q))
        for edge in factor:
            matrices[edge] = anchor
    for edge, phase in gauge.FOURIER_PHASES.items():
        scalar = (phase[0] + phase[1]*omega) % prime
        matrices[edge] = tuple(tuple(scalar*entry % prime for entry in row)
                               for row in matrices[edge])
    return {(u, v, a, b): matrix[a][b] % prime
            for (u, v), matrix in matrices.items()
            for a, b in product(range(q), repeat=2) if matrix[a][b] % prime}


def step_mod(vector, site, colour, source, n, prime=7):
    answer = {}
    remaining = n-site-1
    for state, coefficient in vector.items():
        if len(state)+1 <= remaining:
            opened = state + ((site, colour),)
            answer[opened] = (answer.get(opened, 0) + coefficient) % prime
        for index, (left, left_colour) in enumerate(state):
            weight = source.get((left, site, left_colour, colour), 0)
            if weight:
                closed = state[:index] + state[index+1:]
                answer[closed] = (answer.get(closed, 0)
                                  + coefficient*weight) % prime
    return {state: value for state, value in answer.items() if value}


def forward_mod(prefix, source, n):
    vector = {(): 1}
    for site, colour in enumerate(prefix):
        vector = step_mod(vector, site, colour, source, n)
    return vector


def completion_mod(state, suffix, cut, source, n):
    vector = {state: 1}
    for offset, colour in enumerate(suffix):
        vector = step_mod(vector, cut+offset, colour, source, n)
    return vector.get((), 0)


def matrix_rank_mod7(rows):
    return gauge.rank_mod_prime(rows, 7)


def null_vector_mod7(rows):
    """Return one nonzero vector in the right kernel over F_7."""
    matrix = [[value % 7 for value in row] for row in rows]
    width = len(matrix[0])
    pivot_row = 0
    pivots = []
    for column in range(width):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, 7)
        matrix[pivot_row] = [value*inverse % 7 for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [(left-scale*right) % 7
                           for left, right in zip(matrix[row], matrix[pivot_row])]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    free = next(column for column in range(width) if column not in pivots)
    vector = [0] * width
    vector[free] = 1
    for row, pivot in reversed(list(enumerate(pivots))):
        vector[pivot] = -sum(matrix[row][column]*vector[column]
                             for column in range(pivot+1, width)) % 7
    require(any(vector), vector)
    require(all(sum(a*b for a, b in zip(row, vector)) % 7 == 0
                for row in rows), vector)
    return vector


def fourier_hostile_guard():
    gauge.verify_fourier_isotropy()
    gauge.verify_full_block_injectivity_mod7()
    source, n = fourier_source_mod7(), 6
    records = []
    witness = None
    for cut in range(1, n):
        prefixes = tuple(product(range(3), repeat=cut))
        suffixes = tuple(product(range(3), repeat=n-cut))
        forwards = [forward_mod(prefix, source, n) for prefix in prefixes]
        states = sorted(set().union(*(row.keys() for row in forwards)))
        reachable = [[row.get(state, 0) for state in states] for row in forwards]
        observable = [[completion_mod(state, suffix, cut, source, n)
                       for suffix in suffixes] for state in states]
        output = [[sum(left*right for left, right in zip(row, column)) % 7
                   for column in zip(*observable)] for row in reachable]
        rr, hr = matrix_rank_mod7(reachable), matrix_rank_mod7(output)
        records.append((cut, len(states), rr, hr, rr-hr))
        if cut == 3:
            coefficients = null_vector_mod7([list(row) for row in zip(*output)])
            radical = [sum(coefficients[row]*reachable[row][column]
                           for row in range(len(prefixes))) % 7
                       for column in range(len(states))]
            require(any(radical), radical)
            require(all(sum(radical[column]*observable[column][suffix]
                            for column in range(len(states))) % 7 == 0
                        for suffix in range(len(suffixes))), radical)
            witness = {
                "prefix_coefficients": {
                    "".join(map(str, prefixes[index])): value
                    for index, value in enumerate(coefficients) if value
                },
                "boundary_state_coefficients": {
                    mps.state_label(states[index]): value
                    for index, value in enumerate(radical) if value
                },
            }
    require(records == [(1, 3, 3, 3, 0), (2, 10, 9, 9, 0),
                        (3, 36, 27, 25, 2), (4, 55, 51, 9, 42),
                        (5, 15, 15, 3, 12)], records)
    require(witness is not None, "missing cut-three radical")
    return {"cut_records": records, "cut3_radical": witness}


def main():
    n4 = n4_minimum_block_guard()
    hostile = fourier_hostile_guard()
    print("one-cut kernel-to-edge theorem")
    print("O_k r=0 lifts to ker L_E only when the histories in r share a common remainder and differ solely in an intersecting edge block E")
    print("n4 exact GHZ minimum", n4)
    print("phased block-injective local-minimum cut census", hostile)
    print("verdict minimum norm deletes the old inactive chord, but does not make the top-Hankel quotient source-faithful; the n4 mixed-prefix radical is reachable, unobservable, and not an affine edge-block kernel")


if __name__ == "__main__":
    main()
