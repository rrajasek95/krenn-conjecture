#!/usr/bin/env python3
"""Numerically probe the bottom equations after exact dense-top elimination.

This is a discovery script, not a proof.  At n=6 it fixes the rational
complete scalar top endpoint W used by ``verify_collision_top_endpoint_``
``flexibility.py``.  The top tangent equations parameterize K by 48 complex
coordinates.  The two-binary top equations then determine every binary
cell of q0.  Only the coupled bottom equations remain in the residual:

    H(q0) = 2 X + Y,       dH_q0(K) = 0.

The reduction is exact; floating point enters only in the final nonlinear
least-squares search.
"""

from __future__ import annotations

import argparse
import itertools
from fractions import Fraction

import numpy as np
from scipy.optimize import least_squares


N = 6
X, Y, Z = range(3)
VERTICES = tuple(range(N))
EDGES = tuple(itertools.combinations(VERTICES, 2))
EDGE_INDEX = {edge: position for position, edge in enumerate(EDGES)}


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, partner in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, partner),) + tail


MATCHINGS = tuple(perfect_matchings(VERTICES))
BOTTOM_COLORINGS = tuple(itertools.product((X, Y), repeat=N))
TANGENT_COLORINGS = tuple(
    coloring
    for coloring in itertools.product((X, Y, Z), repeat=N)
    if coloring.count(Z) == 1
)
BOTTOM_COLORING_ARRAY = np.asarray(BOTTOM_COLORINGS, dtype=np.int8)
TANGENT_COLORING_ARRAY = np.asarray(TANGENT_COLORINGS, dtype=np.int8)
MATCHING_EDGE_INDICES = np.asarray(
    [[EDGE_INDEX[edge] for edge in matching] for matching in MATCHINGS],
    dtype=np.int8,
)
MATCHING_FIRST_VERTICES = np.asarray(
    [[edge[0] for edge in matching] for matching in MATCHINGS], dtype=np.int8
)
MATCHING_SECOND_VERTICES = np.asarray(
    [[edge[1] for edge in matching] for matching in MATCHINGS], dtype=np.int8
)


def amplitude(matrices, coloring):
    answer = 0j
    for matching in MATCHINGS:
        term = 1 + 0j
        for u, v in matching:
            term *= matrices[EDGE_INDEX[(u, v)], coloring[u], coloring[v]]
        answer += term
    return answer


def scalar_hafnian(weights, vertices):
    answer = Fraction(0)
    for matching in perfect_matchings(vertices):
        term = Fraction(1)
        for edge in matching:
            term *= weights[edge]
        answer += term
    return answer


def dense_w_and_cofactors():
    weights = {edge: Fraction(1) for edge in EDGES}
    weights[(0, 1)] = Fraction(-383, 96)
    cofactors = {}
    for edge in EDGES:
        remaining = tuple(v for v in VERTICES if v not in edge)
        cofactors[edge] = scalar_hafnian(weights, remaining)
    assert scalar_hafnian(weights, VERTICES) == Fraction(1, 32)
    assert all(cofactors.values())
    return weights, cofactors


WEIGHTS_Q, COFACTORS_Q = dense_w_and_cofactors()
WEIGHTS = {edge: float(value) for edge, value in WEIGHTS_Q.items()}
COFACTORS = {edge: float(value) for edge, value in COFACTORS_Q.items()}

# For every (binary site, binary color), pick the first z-neighbor as pivot.
# The other four directed cells are free, and the top tangent equation fixes
# the pivot by its deleted-pair cofactors.
SECTORS = tuple((site, color) for site in VERTICES for color in (X, Y))
FREE = []
PIVOT = {}
for site, color in SECTORS:
    neighbors = tuple(v for v in VERTICES if v != site)
    PIVOT[(site, color)] = neighbors[0]
    FREE.extend((site, color, neighbor) for neighbor in neighbors[1:])
assert len(FREE) == 48


def set_directed_cell(matrices, binary_site, color, z_site, value):
    u, v = sorted((binary_site, z_site))
    if binary_site == u:
        matrices[EDGE_INDEX[(u, v)], color, Z] += value
    else:
        matrices[EDGE_INDEX[(u, v)], Z, color] += value


def set_binary_cell(matrices, first, second, first_color, second_color, value):
    u, v = sorted((first, second))
    colors = (
        (first_color, second_color)
        if first == u
        else (second_color, first_color)
    )
    matrices[EDGE_INDEX[(u, v)], colors[0], colors[1]] = value


def decode_k(parameters):
    matrices = np.zeros((len(EDGES), 3, 3), dtype=complex)
    sector_values = {sector: {} for sector in SECTORS}
    for value, (site, color, neighbor) in zip(parameters, FREE):
        sector_values[(site, color)][neighbor] = value
    for site, color in SECTORS:
        pivot = PIVOT[(site, color)]
        numerator = sum(
            COFACTORS[tuple(sorted((site, neighbor)))] * value
            for neighbor, value in sector_values[(site, color)].items()
        )
        sector_values[(site, color)][pivot] = -numerator / COFACTORS[
            tuple(sorted((site, pivot)))
        ]
        for neighbor, value in sector_values[(site, color)].items():
            set_directed_cell(matrices, site, color, neighbor, value)
    return matrices


# Constant linear map from the 48 top-tangent coordinates to K.  Keeping
# this array also makes the nonlinear reduction's Jacobian exact up to the
# final floating-point evaluation.
K_BASIS = np.stack(
    [
        decode_k(np.eye(len(FREE), dtype=complex)[column])
        for column in range(len(FREE))
    ],
    axis=-1,
)


def amplitude_and_jacobian(matrices, matrix_jacobian, coloring):
    """Return a hafnian coefficient and its holomorphic parameter row."""
    answer = 0j
    derivative = np.zeros(len(FREE), dtype=complex)
    for matching in MATCHINGS:
        values = [
            matrices[EDGE_INDEX[edge], coloring[edge[0]], coloring[edge[1]]]
            for edge in matching
        ]
        answer += np.prod(values)
        for position, edge in enumerate(matching):
            other = np.prod(
                [value for index, value in enumerate(values) if index != position]
            )
            derivative += other * matrix_jacobian[
                EDGE_INDEX[edge], coloring[edge[0]], coloring[edge[1]], :
            ]
    return answer, derivative


def amplitudes_and_jacobian(matrices, matrix_jacobian, colorings):
    """Vectorized version for an array of site colorings."""
    colorings = np.asarray(colorings)
    row_count = len(colorings)
    values = np.zeros(row_count, dtype=complex)
    derivative = np.zeros((row_count, len(FREE)), dtype=complex)
    rows = np.arange(row_count)
    for edge_indices, firsts, seconds in zip(
        MATCHING_EDGE_INDICES,
        MATCHING_FIRST_VERTICES,
        MATCHING_SECOND_VERTICES,
    ):
        factors = [
            matrices[edge_index, colorings[:, first], colorings[:, second]]
            for edge_index, first, second in zip(edge_indices, firsts, seconds)
        ]
        values += factors[0] * factors[1] * factors[2]
        for position in range(3):
            other = factors[(position + 1) % 3] * factors[(position + 2) % 3]
            derivative += other[:, None] * matrix_jacobian[
                edge_indices[position],
                colorings[:, firsts[position]],
                colorings[:, seconds[position]],
                :,
            ]
    return values, derivative


def eliminate_q0(k):
    # B_pq^{ab}(K) is the coefficient with binary sites p,q in W+K.
    # The direct q0 cell is then uniquely obtained by division by C^W_pq.
    source = k.copy()
    for edge, weight in WEIGHTS.items():
        source[EDGE_INDEX[edge], Z, Z] = weight
    q0 = np.zeros_like(k)
    for first, second in EDGES:
        for first_color, second_color in itertools.product((X, Y), repeat=2):
            coloring = [Z] * N
            coloring[first] = first_color
            coloring[second] = second_color
            hessian = amplitude(source, tuple(coloring))
            target = 0.125 if first_color == second_color == X else 0.0
            value = (target - hessian) / COFACTORS[(first, second)]
            set_binary_cell(
                q0, first, second, first_color, second_color, value
            )
    return q0


def eliminate_q0_with_jacobian(parameters):
    k = np.tensordot(K_BASIS, parameters, axes=([-1], [0]))
    source = k.copy()
    source_jacobian = K_BASIS
    for edge, weight in WEIGHTS.items():
        source[EDGE_INDEX[edge], Z, Z] = weight
    q0 = np.zeros_like(k)
    q0_jacobian = np.zeros(K_BASIS.shape, dtype=complex)
    for first, second in EDGES:
        for first_color, second_color in itertools.product((X, Y), repeat=2):
            coloring = [Z] * N
            coloring[first] = first_color
            coloring[second] = second_color
            hessian, hessian_jacobian = amplitude_and_jacobian(
                source, source_jacobian, tuple(coloring)
            )
            target = 0.125 if first_color == second_color == X else 0.0
            value = (target - hessian) / COFACTORS[(first, second)]
            value_jacobian = -hessian_jacobian / COFACTORS[(first, second)]
            u, v = first, second
            q0[EDGE_INDEX[(u, v)], first_color, second_color] = value
            q0_jacobian[
                EDGE_INDEX[(u, v)], first_color, second_color, :
            ] = value_jacobian
    return k, q0, q0_jacobian


def bottom_values(parameters):
    k = decode_k(parameters)
    q0 = eliminate_q0(k)
    bottom = np.asarray(
        [amplitude(q0, coloring) for coloring in BOTTOM_COLORINGS]
    )
    source = q0 + k
    tangent = np.asarray(
        [amplitude(source, coloring) for coloring in TANGENT_COLORINGS]
    )
    return bottom, tangent, k, q0


def bottom_values_and_jacobian(parameters):
    k, q0, q0_jacobian = eliminate_q0_with_jacobian(parameters)
    bottom, bottom_jacobian = amplitudes_and_jacobian(
        q0, q0_jacobian, BOTTOM_COLORING_ARRAY
    )
    source = q0 + k
    source_jacobian = q0_jacobian + K_BASIS
    tangent, tangent_jacobian = amplitudes_and_jacobian(
        source, source_jacobian, TANGENT_COLORING_ARRAY
    )
    jacobian = np.concatenate((bottom_jacobian, tangent_jacobian), axis=0)
    return bottom, tangent, jacobian


BOTTOM_TARGET = np.asarray(
    [
        2.0 if coloring == (X,) * N else 1.0 if coloring == (Y,) * N else 0.0
        for coloring in BOTTOM_COLORINGS
    ],
    dtype=complex,
)


def decode_real(real_vector):
    return real_vector[: len(FREE)] + 1j * real_vector[len(FREE) :]


def residual(real_vector):
    bottom, tangent, _, _ = bottom_values(decode_real(real_vector))
    value = np.r_[bottom - BOTTOM_TARGET, tangent]
    return np.r_[value.real, value.imag]


def jacobian(real_vector):
    _, _, value = bottom_values_and_jacobian(decode_real(real_vector))
    return np.block([[value.real, -value.imag], [value.imag, value.real]])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--scale", type=float, default=0.3)
    parser.add_argument("--max-nfev", type=int, default=3000)
    args = parser.parse_args()

    print(
        "dense W: H=1/32, nonzero cofactors="
        f"{len(COFACTORS)}; complex K parameters={len(FREE)}; "
        f"bottom equations={len(BOTTOM_COLORINGS) + len(TANGENT_COLORINGS)}",
        flush=True,
    )
    rng = np.random.default_rng(args.seed)
    best = np.inf
    for start in range(args.starts):
        initial_complex = args.scale * (
            rng.normal(size=len(FREE)) + 1j * rng.normal(size=len(FREE))
        )
        initial = np.r_[initial_complex.real, initial_complex.imag]
        fit = least_squares(
            residual,
            initial,
            jac=jacobian,
            max_nfev=args.max_nfev,
            ftol=1e-13,
            xtol=1e-13,
            gtol=1e-13,
            verbose=0,
        )
        value = residual(fit.x)
        complex_value = value[: len(value) // 2] + 1j * value[len(value) // 2 :]
        largest = float(np.max(np.abs(complex_value)))
        best = min(best, largest)
        print(
            f"start={start} cost={fit.cost:.12g} max={largest:.8g} "
            f"optimality={fit.optimality:.3g} nfev={fit.nfev} "
            f"norm={np.linalg.norm(decode_real(fit.x)):.6g}",
            flush=True,
        )
        if largest < 1e-8:
            bottom, tangent, k, q0 = bottom_values(decode_real(fit.x))
            np.savez(
                "/tmp/dense_top_bottom_endpoints.npz",
                parameters=decode_real(fit.x),
                k=k,
                q0=q0,
                bottom=bottom,
                tangent=tangent,
            )
            break
    print(f"best_max_residual={best:.12g}")


if __name__ == "__main__":
    main()
