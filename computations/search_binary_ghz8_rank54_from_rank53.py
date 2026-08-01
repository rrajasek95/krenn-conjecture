#!/usr/bin/env python3
"""Numerical reconnaissance around the exact rational rank-53 GHZ8 source.

This script is deliberately separate from the exact checker.  Its output is
search evidence only: failure to find rank 54 or 55 proves no upper bound.

Default mode replays all 28 deletion ranks and reports the singular-value gap
at each exact rank.  ``--stress`` additionally performs deterministic
scale-normalized tangent continuation and fixed-support random restarts aimed
at opening singular value 53 (zero based), which would raise rank 53 to 54.

Run with

    uv run python computations/search_binary_ghz8_rank54_from_rank53.py
    uv run python computations/search_binary_ghz8_rank54_from_rank53.py --stress
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np

from verify_binary_ghz8_exact_rank53_source import (
    EDGES,
    VERTICES,
    rank_profile,
    source,
)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


PAIRS = tuple(itertools.combinations(VERTICES, 2))
PAIR_INDEX = {edge: index for index, edge in enumerate(PAIRS)}
MATCHINGS8 = perfect_matchings(VERTICES)
WORDS8 = tuple(itertools.product((0, 1), repeat=8))

MATCHING_EDGE_INDEX = np.array(
    [[PAIR_INDEX[edge] for edge in matching] for matching in MATCHINGS8],
    dtype=int,
)
MATCHING_LEFT_COLOUR = np.array(
    [
        [[word[u] for u, _ in matching] for matching in MATCHINGS8]
        for word in WORDS8
    ],
    dtype=int,
)
MATCHING_RIGHT_COLOUR = np.array(
    [
        [[word[v] for _, v in matching] for matching in MATCHINGS8]
        for word in WORDS8
    ],
    dtype=int,
)
TARGET = np.zeros(256)
TARGET[0] = TARGET[-1] = 1.0


def source_vector():
    vector = np.zeros(112)
    for (u, v, a, b), value in source().items():
        vector[4 * PAIR_INDEX[u, v] + 2 * a + b] = float(value)
    return vector


def tensor_residual(vector):
    blocks = vector.reshape(28, 2, 2)
    selected = blocks[
        MATCHING_EDGE_INDEX[None, :, :],
        MATCHING_LEFT_COLOUR,
        MATCHING_RIGHT_COLOUR,
    ]
    return np.prod(selected, axis=2).sum(axis=1) - TARGET


def tensor_jacobian(vector):
    blocks = vector.reshape(28, 2, 2)
    selected = blocks[
        MATCHING_EDGE_INDEX[None, :, :],
        MATCHING_LEFT_COLOUR,
        MATCHING_RIGHT_COLOUR,
    ]
    jacobian = np.zeros((256, 112))
    rows = np.repeat(np.arange(256), len(MATCHINGS8))
    for position in range(4):
        derivative = np.ones((256, len(MATCHINGS8)))
        for other in range(4):
            if other != position:
                derivative *= selected[:, :, other]
        columns = np.broadcast_to(
            4 * MATCHING_EDGE_INDEX[None, :, position]
            + 2 * MATCHING_LEFT_COLOUR[:, :, position]
            + MATCHING_RIGHT_COLOUR[:, :, position],
            (256, len(MATCHINGS8)),
        ).ravel()
        np.add.at(jacobian, (rows, columns), derivative.ravel())
    return jacobian


def numerical_differential(vector, deleted):
    """Build dPsi independently from the exact checker."""

    blocks = vector.reshape(28, 2, 2)
    remaining = tuple(vertex for vertex in VERTICES if vertex not in deleted)
    columns = []
    for u, v in itertools.combinations(remaining, 2):
        cofactor_vertices = tuple(
            vertex for vertex in remaining if vertex not in (u, v)
        )
        for a, b in itertools.product((0, 1), repeat=2):
            output = np.zeros(64)
            for matching in perfect_matchings(cofactor_vertices):
                for cofactor_word in itertools.product((0, 1), repeat=4):
                    assignment = dict(zip(cofactor_vertices, cofactor_word))
                    assignment[u] = a
                    assignment[v] = b
                    coefficient = 1.0
                    for left, right in matching:
                        edge = (min(left, right), max(left, right))
                        coefficient *= blocks[
                            PAIR_INDEX[edge], assignment[left], assignment[right]
                        ]
                    output_index = sum(
                        assignment[vertex] << (5 - position)
                        for position, vertex in enumerate(remaining)
                    )
                    output[output_index] += coefficient
            columns.append(output)
    return np.stack(columns, axis=1)


def singular_gap(matrix, exact_rank):
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    first_zero = singular_values[exact_rank]
    last_nonzero = singular_values[exact_rank - 1]
    return singular_values, last_nonzero, first_zero


def replay():
    vector = source_vector()
    residual = tensor_residual(vector)
    exact_profile = rank_profile(source())
    print(
        "floating replay of exact tensor: "
        f"||F||_inf={np.max(np.abs(residual)):.3e}"
    )
    print("deleted  ranks   full gap                 mixed gap")
    for deleted in EDGES:
        matrix = numerical_differential(vector, deleted)
        full_rank, mixed_rank = exact_profile[deleted]
        _, full_last, full_first_zero = singular_gap(matrix, full_rank)
        _, mixed_last, mixed_first_zero = singular_gap(
            matrix[1:-1], mixed_rank
        )
        print(
            f"{deleted!s:8} {full_rank:2}/{mixed_rank:2}  "
            f"{full_last:.3e}/{full_first_zero:.3e}  "
            f"{mixed_last:.3e}/{mixed_first_zero:.3e}"
        )

    target_matrix = numerical_differential(vector, (3, 4))
    target_singular = np.linalg.svd(target_matrix, compute_uv=False)
    print("rank-53 target singular values s[49:56]:", target_singular[49:56])
    return vector


def tangent_stress(vector, trial_count=20):
    """Correct scale-normalized predictions on the 45-cell support chart."""

    try:
        from scipy.optimize import least_squares
    except ImportError as error:
        raise SystemExit("--stress requires scipy") from error

    active = np.flatnonzero(vector)
    active_start = vector[active]

    def unpack(active_vector):
        full = np.zeros(112)
        full[active] = active_vector
        return full

    active_jacobian = tensor_jacobian(vector)[:, active]
    _, singular_values, right = np.linalg.svd(
        active_jacobian, full_matrices=True
    )
    jacobian_rank = int(
        np.sum(singular_values > 1e-10 * singular_values[0])
    )
    tangent = right[jacobian_rank:].T
    print(
        "active-support Jacobian: "
        f"rank={jacobian_rank}, nullity={tangent.shape[1]}, "
        f"gap={singular_values[jacobian_rank - 1]:.3e}/"
        f"{singular_values[jacobian_rank]:.3e}"
    )

    rng = np.random.default_rng(26080154)
    relative_steps = (0.001, 0.004, 0.015, 0.05, 0.15)
    accepted = 0
    rank53_points = 0
    largest_opening = 0.0
    for trial in range(trial_count):
        coefficients = rng.normal(size=tangent.shape[1])
        direction = tangent @ coefficients
        direction /= np.linalg.norm(direction)
        step = relative_steps[trial % len(relative_steps)] * np.linalg.norm(
            active_start
        )
        predicted = active_start + step * direction

        def augmented(active_vector):
            return np.concatenate(
                (
                    tensor_residual(unpack(active_vector)),
                    tangent.T @ (active_vector - predicted),
                )
            )

        def augmented_jacobian(active_vector):
            return np.vstack(
                (tensor_jacobian(unpack(active_vector))[:, active], tangent.T)
            )

        fit = least_squares(
            augmented,
            predicted,
            jac=augmented_jacobian,
            method="trf",
            xtol=2.3e-14,
            ftol=2.3e-14,
            gtol=2.3e-14,
            max_nfev=1000,
            x_scale="jac",
        )
        corrected = unpack(fit.x)
        residual = np.max(np.abs(tensor_residual(corrected)))
        singular = np.linalg.svd(
            numerical_differential(corrected, (3, 4)), compute_uv=False
        )
        if residual < 1e-11:
            accepted += 1
            largest_opening = max(largest_opening, singular[53])
            rank53_points += singular[52] > 1e-8

    print(
        f"tangent stress: accepted {accepted}/{trial_count}; "
        f"rank-53 points {rank53_points}; max attempted s[53] opening "
        f"{largest_opening:.3e}"
    )
    if accepted != trial_count or largest_opening >= 1e-10:
        raise RuntimeError("deterministic tangent-stress baseline changed")


def support_restarts(vector, trial_count=24):
    """Restart the nonlinear GHZ equations on the same exact-zero support."""

    try:
        from scipy.optimize import least_squares
    except ImportError as error:
        raise SystemExit("--stress requires scipy") from error

    active = np.flatnonzero(vector)
    active_start = vector[active]

    def unpack(active_vector):
        full = np.zeros(112)
        full[active] = active_vector
        return full

    def residual(active_vector):
        return tensor_residual(unpack(active_vector))

    def jacobian(active_vector):
        return tensor_jacobian(unpack(active_vector))[:, active]

    rng = np.random.default_rng(26080155)
    accepted = 0
    histogram = {}
    largest_opening = 0.0
    for trial in range(trial_count):
        mode = trial % 6
        if mode < 4:
            scale = (0.05, 0.2, 0.7, 2.0)[mode]
            start = active_start + scale * rng.normal(size=len(active)) * np.maximum(
                np.abs(active_start), 0.2
            )
        else:
            start = rng.normal(scale=(0.5, 2.0)[mode - 4], size=len(active))
        fit = least_squares(
            residual,
            start,
            jac=jacobian,
            method="trf",
            xtol=1e-14,
            ftol=1e-14,
            gtol=1e-14,
            max_nfev=1500,
            x_scale="jac",
        )
        corrected = unpack(fit.x)
        if np.max(np.abs(tensor_residual(corrected))) >= 1e-10:
            continue
        accepted += 1
        singular = np.linalg.svd(
            numerical_differential(corrected, (3, 4)), compute_uv=False
        )
        numerical_rank = int(np.sum(singular > 1e-8))
        histogram[numerical_rank] = histogram.get(numerical_rank, 0) + 1
        largest_opening = max(largest_opening, singular[53])

    print(
        f"fixed-support restarts: accepted {accepted}/{trial_count}; "
        f"rank histogram {dict(sorted(histogram.items()))}; "
        f"max s[53]={largest_opening:.3e}"
    )
    if largest_opening >= 1e-8:
        raise RuntimeError("deterministic restart found a rank-54 candidate")


def generic_support_control(vector, trial_count=4):
    """Show that the residual support alone does not impose the rank-53 cap."""

    active = np.flatnonzero(vector)
    rng = np.random.default_rng(26080156)
    ranks = []
    for _ in range(trial_count):
        random_vector = np.zeros(112)
        random_vector[active] = rng.normal(size=len(active))
        singular = np.linalg.svd(
            numerical_differential(random_vector, (3, 4)), compute_uv=False
        )
        ranks.append(int(np.sum(singular > 1e-8)))
    print("same-support non-GHZ control ranks:", ranks)
    if ranks != [55] * trial_count:
        raise RuntimeError("generic-support rank control changed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stress", action="store_true")
    arguments = parser.parse_args()

    vector = replay()
    if arguments.stress:
        generic_support_control(vector)
        tangent_stress(vector)
        support_restarts(vector)
        print("SEARCH EVIDENCE ONLY: no rank 54 or 55 was found")


if __name__ == "__main__":
    main()
