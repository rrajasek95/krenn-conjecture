"""Joint mean-gauge derivative and local correction certificate at rational sources."""

import itertools
import math
from fractions import Fraction as F
from functools import lru_cache

import covariance_noise_certificate as bounds
import numpy as np
from flint import fmpz_mat


def point_derivative(means, edges, first_observation):
    n = len(means)

    @lru_cache(None)
    def moment(sites):
        if not sites:
            return np.array(F(1), dtype=object)
        i, *rest = sites
        result = (
            np.array(means[i], dtype=object).reshape((3,) + (1,) * len(rest))
            * moment(tuple(rest))[None]
        )
        for position, j in enumerate(rest, 1):
            pair = np.array(edges[i, j], dtype=object).reshape(
                (3, 3) + (1,) * (len(rest) - 1)
            )
            term = pair * moment(tuple(k for k in rest if k != j))[None, None]
            result += np.moveaxis(term, 1, position)
        return result

    keys = [
        ("mu", i, a)
        for i in range(n)
        for a in range(3)
        if not first_observation or i == n - 1 or a
    ]
    keys += [
        ("R", i, j, a, b)
        for i, j in edges
        for a, b in itertools.product(range(3), repeat=2)
    ]
    columns = []
    for key in keys:
        sites, colours = (
            ([key[1]], [key[2]]) if key[0] == "mu" else (key[1:3], key[3:5])
        )
        column = np.zeros((3,) * n, dtype=object)
        selection = [slice(None)] * n
        for site, colour in zip(sites, colours):
            selection[site] = colour
        column[tuple(selection)] = moment(tuple(i for i in range(n) if i not in sites))
        columns.append(column.reshape(-1))
    return moment(tuple(range(n))).reshape(-1), np.column_stack(columns), keys


def curvature_squared(all_means, edges):
    n = len(all_means[0])
    pair_bounds = {
        edge: 1 + max(abs(x) for row in b for x in row) for edge, b in edges.items()
    }
    total = F(0)
    for setting, means in enumerate(all_means):
        monomer_bounds = [1 + max(abs(x) for x in row) for row in means]

        @lru_cache(None)
        def positive(sites, monomers=tuple(monomer_bounds)):
            if not sites:
                return F(1)
            i, *rest = sites
            return monomers[i] * positive(tuple(rest)) + sum(
                pair_bounds[i, j] * positive(tuple(k for k in rest if k != j))
                for j in rest
            )

        supports = [
            (frozenset([i]), 2 if setting == 0 and i < n - 1 else 3) for i in range(n)
        ]
        supports += [(frozenset(edge), 9) for edge in edges]
        total += sum(
            wa
            * wb
            * 3 ** (n - len(a | b))
            * positive(tuple(i for i in range(n) if i not in a | b)) ** 2
            for a, wa in supports
            for b, wb in supports
            if a.isdisjoint(b)
        )
    return total


def certify(means, edges, records, outer_error, saved=None, audit=None):
    n, count = len(means[0]), len(means)
    mean_counts = [2 * n + 1] + [3 * n] * (count - 1)
    free_means = sum(mean_counts)
    total_parameters = free_means + 9 * math.comb(n, 2)
    derivatives, tensors = [], []
    denominators = []
    for setting, mu in enumerate(means):
        tensor, derivative, keys = point_derivative(mu, edges, setting == 0)
        if audit is not None:
            audit(mu, edges, tensor, derivative, keys)
        tensors.append(tensor)
        derivatives.append(derivative)
        denominators.append(
            math.lcm(*(F(x).denominator for x in derivative.reshape(-1)))
        )
    denominator = math.lcm(*denominators)
    rows, start = [], 0
    for setting, derivative in enumerate(derivatives):
        width = mean_counts[setting]
        for row in derivative:
            joint = [0] * total_parameters
            joint[start : start + width] = [
                int(F(x) * denominator) for x in row[:width]
            ]
            joint[free_means:] = [int(F(x) * denominator) for x in row[width:]]
            rows.append(joint)
        start += width
    inverse, matrix_certificate = bounds.matrix_bound(
        (fmpz_mat(rows), denominator),
        None if saved is None else saved["matrix_certificate"]["preconditioner"],
    )
    curvature2 = curvature_squared(means, edges)
    curvature = bounds.upper_sqrt(curvature2)
    radius = min(F(1), 1 / (2 * inverse * curvature))
    residual2 = sum(
        (F(int(y), int(record["observed_denominator"])) - F(x)) ** 2
        for record, tensor in zip(records, tensors)
        for x, y in zip(tensor, record["observed_numerators"])
    )
    residual = bounds.upper_sqrt(residual2)
    epsilon = bounds.length(F(record["error_budget"]) for record in records)
    assert F(outer_error) < radius / 2
    assert inverse * residual < radius / 2
    return {
        "free_parameters": total_parameters,
        "free_mean_parameters": free_means,
        "matrix_certificate": matrix_certificate,
        "curvature_squared_bound": str(curvature2),
        "curvature_bound": str(curvature),
        "inverse_norm_bound": str(inverse),
        "correction_radius": str(radius),
        "stacked_error_budget": str(epsilon),
        "joint_forward_residual_squared": str(residual2),
        "joint_forward_residual_bound": str(residual),
        "outer_joint_error_bound": str(outer_error),
        "refined_global_joint_error_bound": str(2 * inverse * (epsilon + residual)),
        "exact_arithmetic_correction_error_bound": str(2 * inverse * epsilon),
        "scope": "All compatible shared-source representatives in the first observation's mean gauge enter the joint correction ball. Iteration convergence is in exact arithmetic; no floating correction is run here.",
    }
