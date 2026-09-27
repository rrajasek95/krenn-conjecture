#!/usr/bin/env python3
"""Finite-error bounds through the covariance inverse in a fixed mean chart.

The point source is a candidate, not assumed to be the true source.
All error propagation uses fractions and certified matrix inverse bounds.
"""

import itertools
import math
from fractions import Fraction as F
from functools import lru_cache

import numpy as np
import slice_noise_recovery as mean_noise
from flint import fmpz_mat
from floating_source_inverse import add, setup
from scipy.linalg import eigh


def upper_sqrt(value):
    value = F(value)
    assert value >= 0
    if not value:
        return F(0)
    exponent = value.numerator.bit_length() - value.denominator.bit_length()
    return mean_noise.sqrt_upper(value, bits=max(0, 70 - exponent // 2))


def length(values):
    return upper_sqrt(
        sum((F(int(x)) if isinstance(x, np.integer) else F(x)) ** 2 for x in values)
    )


def common(values):
    values = [F(x) for x in values]
    denominator = math.lcm(*(x.denominator for x in values))
    return [int(x * denominator) for x in values], denominator


class ExactExterior:
    def __init__(self, tensor, denominator, n):
        self.tensor = np.asarray(tensor, dtype=object).reshape(-1)
        self.denominator, self.n = denominator, n
        self.powers = 3 ** np.arange(n - 1, -1, -1)
        self.bits = np.array(list(itertools.product([0, 1], repeat=n)))
        self.sign = (-1) ** (n - self.bits.sum(axis=1))
        self.cache = {}

    def column(self, index):
        if index not in self.cache:
            b = index // self.powers % 3
            a = (b + 1 + self.bits) % 3
            c = 3 - a - b
            self.cache[index] = (
                a @ self.powers,
                self.sign * self.tensor[c @ self.powers],
            )
        return self.cache[index]

    def apply(self, polynomials):
        denominator = math.lcm(
            *(F(x).denominator for p in polynomials for x in p.values())
        )
        result = np.zeros((3**self.n, len(polynomials)), dtype=object)
        for j, poly in enumerate(polynomials):
            for index, value in poly.items():
                if value:
                    rows, entries = self.column(index)
                    result[rows, j] += int(F(value) * denominator) * entries
        return fmpz_mat(result.tolist()), denominator * self.denominator


def concatenate(first, second):
    a, da = first
    b, db = second
    denominator = math.lcm(da, db)
    rows = [
        [int(x) * (denominator // da) for x in left]
        + [int(x) * (denominator // db) for x in right]
        for left, right in zip(a.tolist(), b.tolist())
    ]
    return fmpz_mat(rows), denominator


def equation_check(matrix, vector, target):
    a, da = matrix
    b, db = target
    values, dx = common(vector)
    residual = (a * fmpz_mat([[x] for x in values])) * db - b * (da * dx)
    assert all(int(x) == 0 for row in residual.tolist() for x in row)


def matrix_bound(matrix, saved=None):
    """Certify a full-column-rank matrix using an integer preconditioner."""
    a, denominator = matrix
    gram = a.transpose() * a
    size = gram.nrows()
    if saved is None:
        floating = np.asarray(a.tolist(), dtype=float) / denominator
        eigenvalues, vectors = eigh(floating.T @ floating)
        assert eigenvalues[0] > 0
        proposal = (vectors / np.sqrt(eigenvalues)) @ vectors.T
        saved = mean_noise.encode(mean_noise.quantize(proposal))
    entries, scale = mean_noise.decode(saved)
    preconditioner = fmpz_mat(entries)
    tested = preconditioner.transpose() * gram * preconditioner
    target = scale**2 * denominator**2
    squared = sum(
        (int(tested[i, j]) - (target if i == j else 0)) ** 2
        for i in range(size)
        for j in range(size)
    )
    residual = math.isqrt(squared)
    residual += int(residual**2 < squared)
    assert residual < target
    squared_bound = F(
        denominator**2 * sum(x * x for row in entries for x in row), target - residual
    )
    bound = upper_sqrt(squared_bound)
    return bound, {
        "preconditioner": saved,
        "columns": size,
        "residual_frobenius_squared": str(squared),
        "residual_frobenius_upper": str(residual),
        "inverse_norm_bound": str(bound),
    }


def response_frame(n, edge_vector, keys):
    """Exact response coefficients, with a common integer denominator."""
    integers, denominator = common(edge_vector)
    edges = {
        e: np.zeros((3, 3), dtype=object) for e in itertools.combinations(range(n), 2)
    }
    for (i, j, a, b), value in zip(keys, integers):
        edges[i, j][a, b] = value
    cache = {}

    def visit(sites):
        if sites not in cache:
            if not sites:
                return np.array([1], dtype=object)
            i, *rest = sites
            out = np.zeros((len(sites) // 2 + 1,) + (3,) * len(sites), dtype=object)
            old = visit(tuple(rest))
            out[: len(old), 0] = old
            for position, j in enumerate(rest, 1):
                old = visit(tuple(k for k in rest if k != j))
                pair = edges[i, j].reshape((1, 3, 3) + (1,) * (len(rest) - 1))
                term = np.moveaxis(pair * old[:, None, None], 2, position + 1)
                out[1 : len(old) + 1] += term
            cache[sites] = out
        return cache[sites]

    m = n // 2
    layers = visit(tuple(range(n))).reshape(m + 1, -1)
    frame = [
        [int(layers[k, row]) * denominator ** (m - k) for k in reversed(range(m + 1))]
        for row in range(3**n)
    ]
    return fmpz_mat(frame), denominator**m


def point_systems(tensor, denominator, edges, saved=None):
    """Point means are e0 at every site; derives, then verifies all four solves."""
    n = np.asarray(tensor).ndim
    keys, codes, flows, pure_basis, product = setup(n)
    count = len(keys)
    vector = [F(edges[i, j][a][b]) for i, j, a, b in keys]
    pairs = list(itertools.combinations(range(n), 2))
    mean_shift = sum(
        vector[q] for q, (_, _, a, b) in enumerate(keys) if a == b == 0
    ) / len(pairs)
    pivot_edge = min(
        (q for q, (_, _, a, b) in enumerate(keys) if a and b and vector[q]),
        key=lambda q: abs(abs(vector[q]) - 1),
    )
    covariance_scale = vector[pivot_edge]
    representative = [
        (x - (mean_shift if a == b == 0 else 0)) / covariance_scale
        for x, (_, _, a, b) in zip(vector, keys)
    ]
    f2 = sorted(set(codes))
    coordinate = {code: F(0) for code in f2}
    for code, value in zip(codes, representative):
        coordinate[code] += value
    assert coordinate[0] == 0 and coordinate[codes[pivot_edge]] == 1
    pivot = f2.index(codes[pivot_edge])
    section = {}
    for q, code in enumerate(codes):
        section.setdefault(code, q)
    q0 = {section[code]: value for code, value in coordinate.items() if value}
    flow_coefficients = []
    for flow in flows:
        q = next(q for q, value in flow.items() if value == 1)
        flow_coefficients.append(representative[q] - q0.get(q, 0))
    q1 = add(q0, flows, flow_coefficients)
    pure_coefficients = []
    for row in pure_basis:
        q = next(q for q, value in row.items() if value == 1)
        pure_coefficients.append(representative[q] - q1.get(q, 0))
    qfinal = add(q1, pure_basis, pure_coefficients)
    assert [qfinal.get(q, 0) for q in range(count)] == representative
    flow_part = add({}, flows, flow_coefficients)
    pure_part = add({}, pure_basis, pure_coefficients)
    remainder = {}
    for poly, coefficient in [
        (product(flow_part, flow_part), F(1, 2)),
        (product(q1, pure_part), F(1)),
        (product(pure_part, pure_part), F(1, 2)),
    ]:
        for code, value in poly.items():
            remainder[code] = remainder.get(code, 0) + coefficient * value
    assert all(code in f2 for code, value in remainder.items() if value)
    free = [i for i in range(len(f2)) if i not in [0, pivot]]
    nuisance_coefficients = [
        remainder.get(f2[i], 0) - remainder.get(f2[pivot], 0) * coordinate[f2[i]]
        for i in free
    ]
    action = ExactExterior(tensor, denominator, n)
    first = action.apply([{f2[i]: 1} for i in free])
    first_target = action.apply([{f2[pivot]: -1}])
    e_coefficients = [coordinate[f2[i]] for i in free]
    equation_check(first, e_coefficients, first_target)
    flow_matrix = action.apply([product(q0, flow) for flow in flows])
    second = concatenate(flow_matrix, first)
    second_target = action.apply(
        [{code: -value / 2 for code, value in product(q0, q0).items()}]
    )
    coefficients1 = flow_coefficients + nuisance_coefficients
    equation_check(second, coefficients1, second_target)
    third = action.apply([product(q1, row) for row in pure_basis])
    third_target = action.apply(
        [{code: -value / 2 for code, value in product(q1, q1).items()}]
    )
    equation_check(third, pure_coefficients, third_target)
    frame = response_frame(n, representative, keys)
    m = n // 2
    coordinates = []
    for k in range(m + 1):
        degree = 2 * k + 1
        moment = sum(
            F(
                math.factorial(degree),
                2**j * math.factorial(j) * math.factorial(degree - 2 * j),
            )
            * mean_shift**j
            for j in range(k + 1)
        )
        coordinates.append(covariance_scale ** (m - k) * moment)
    target = fmpz_mat([[int(x)] for x in np.asarray(tensor).reshape(-1)]), denominator
    equation_check(frame, coordinates, target)
    matrices = [first, second, third, frame]
    reports, inverse_bounds = [], []
    for i, matrix in enumerate(matrices):
        bound, report = matrix_bound(
            matrix, None if saved is None else saved[i]["preconditioner"]
        )
        inverse_bounds.append(bound)
        reports.append(report)
    outside = [
        int(x)
        for code, x in enumerate(np.asarray(tensor).reshape(-1))
        if sum(code // 3**k % 3 != 0 for k in range(n)) == n - 1
    ]
    return {
        "n": n,
        "tensor_norm": length(np.asarray(tensor).reshape(-1)) / denominator,
        "outside_norm_lower": max(map(abs, outside)) / F(denominator),
        "inverse_bounds": inverse_bounds,
        "matrix_certificates": reports,
        "linear_systems": matrices,
        "Q0": [q0.get(q, F(0)) for q in range(count)],
        "Q1": [q1.get(q, F(0)) for q in range(count)],
        "Q": representative,
        "x0": e_coefficients,
        "x1": coefficients1,
        "x2": pure_coefficients,
        "coordinates": coordinates,
        "keys": keys,
        "source_vector": vector,
        "pivot_coordinate": int(f2[pivot]),
        "covariance_scale": covariance_scale,
        "mean_shift": mean_shift,
    }


class ScalarBall:
    def __init__(self, center, radius=0):
        self.center, self.radius = F(center), F(radius)

    def __add__(self, other):
        if not isinstance(other, ScalarBall):
            other = ScalarBall(other)
        return ScalarBall(self.center + other.center, self.radius + other.radius)

    __radd__ = __add__

    def __neg__(self):
        return ScalarBall(-self.center, self.radius)

    def __sub__(self, other):
        return (
            self + -other
            if isinstance(other, ScalarBall)
            else self + ScalarBall(-other)
        )

    def __mul__(self, other):
        if not isinstance(other, ScalarBall):
            other = ScalarBall(other)
        return ScalarBall(
            self.center * other.center,
            abs(self.center) * other.radius
            + abs(other.center) * self.radius
            + self.radius * other.radius,
        )

    __rmul__ = __mul__

    def inverse(self):
        gap = abs(self.center) - self.radius
        assert gap > 0, "A calibration denominator is not separated from zero"
        return ScalarBall(1 / self.center, self.radius / (abs(self.center) * gap))

    def __truediv__(self, other):
        if not isinstance(other, ScalarBall):
            other = ScalarBall(other)
        return self * other.inverse()

    def __pow__(self, exponent):
        if exponent < 0:
            return self.inverse() ** (-exponent)
        result = ScalarBall(1)
        for _ in range(exponent):
            result = result * self
        return result


def anchored_mean_bounds(delta_tensor, record, n):
    """Point A,B and their solve residuals must annihilate the anchor tail vector."""
    values = {key: F(value) for key, value in record["bounds"].items()}
    nu, a, b, c, g = [
        values[key]
        for key in [
            "observed_inverse_norm_bound",
            "A_norm_bound",
            "B_norm_bound",
            "C_norm_bound",
            "perpendicular_inverse_bound",
        ]
    ]
    rho_a, rho_b = values["A_solve_residual_bound"], values["B_solve_residual_bound"]
    delta = 2 ** ((n - 1) // 2) * delta_tensor
    assert nu * delta < 1
    inverse = nu / (1 - nu * delta)
    a0, b0 = inverse * delta * (1 + a), inverse * delta * (1 + b)
    a1, b1 = inverse * rho_a, inverse * rho_b
    at, bt = a + a0 + a1, b + b0 + b1
    s0, s1 = (b + bt) * a0 + (a + at) * b0, (b + bt) * a1 + (a + at) * b1
    t0, t1 = at * s0 + c * a0, at * s1 + c * a1
    h0, h1 = upper_sqrt(s0 * s0 + t0 * t0), upper_sqrt(s1 * s1 + t1 * t1)
    feedback = g * h1
    assert feedback < 1
    angle = g * h0 / (1 - feedback)
    assert angle < F(1, 4)
    first_chart = upper_sqrt(
        ((a + a1) * angle + a0) ** 2 + ((b + b1) * angle + b0) ** 2
    )
    other_chart = angle / (1 - angle)
    return [first_chart] + [other_chart] * (n - 1), {
        "feedback_bound": str(feedback),
        "tail_sine_bound": str(angle),
    }


def propagate(point, delta_tensor, mean_record):
    n = point["n"]
    chart_errors, mean_report = anchored_mean_bounds(F(delta_tensor), mean_record, n)
    product = math.prod(1 + e for e in chart_errors)
    delta = product * delta_tensor + (product - 1) * point["tensor_norm"]
    assert delta < point["outside_norm_lower"]
    kappa = 2 ** ((n + 1) // 2)
    multiplication = upper_sqrt(6 * math.comb(n, 4))
    flow_norm, pure_norm = upper_sqrt(n - 1), upper_sqrt(math.comb(n, 2))
    g0, g1, g2 = point["inverse_bounds"][:3]

    def solve_error(g, matrix_error, target_error, center):
        assert g * matrix_error < 1, (
            "A perturbed correction matrix is not certified injective"
        )
        return (
            g * (target_error + matrix_error * length(center)) / (1 - g * matrix_error)
        )

    error_q0 = solve_error(g0, kappa * delta, kappa * delta, point["x0"])

    def correction(previous, previous_error, basis_norm, g, center, nuisance=False):
        norm = length(previous)
        matrix_error = (
            kappa
            * multiplication
            * basis_norm
            * ((point["tensor_norm"] + delta) * previous_error + delta * norm)
        )
        if nuisance:
            matrix_error += kappa * delta
        target_error = (
            kappa
            * multiplication
            / 2
            * (
                delta * norm**2
                + (point["tensor_norm"] + delta)
                * previous_error
                * (2 * norm + previous_error)
            )
        )
        return solve_error(g, matrix_error, target_error, center)

    error_x1 = correction(point["Q0"], error_q0, flow_norm, g1, point["x1"], True)
    error_q1 = error_q0 + flow_norm * error_x1
    error_x2 = correction(point["Q1"], error_q1, pure_norm, g2, point["x2"])
    error_q = error_q1 + pure_norm * error_x2
    return finish_from_class_error(
        point,
        delta_tensor,
        chart_errors,
        mean_report,
        delta,
        error_q0,
        error_x1,
        error_x2,
        error_q,
    )


def finish_from_class_error(
    point,
    delta_tensor,
    chart_errors,
    mean_report,
    delta,
    error_q0,
    error_x1,
    error_x2,
    error_q,
    coefficient_error=None,
):
    """Calibrate a certified covariance class and return to the original mean frame."""
    n, m = point["n"], point["n"] // 2
    gf = point["inverse_bounds"][3]
    q_norm = length(point["Q"])
    column_errors = [
        upper_sqrt(F(math.factorial(2 * k) * math.comb(n, 2 * k), 2**k))
        * error_q
        * (q_norm + error_q) ** (k - 1)
        / math.factorial(k - 1)
        for k in range(1, m + 1)
    ]
    frame_error = length(column_errors)
    if coefficient_error is None:
        assert gf * frame_error < 1, (
            "A perturbed correction matrix is not certified injective"
        )
        coefficient_error = (
            gf
            * (delta + frame_error * length(point["coordinates"]))
            / (1 - gf * frame_error)
        )
    z, c3, c5, c7 = [
        ScalarBall(value, coefficient_error) for value in point["coordinates"][:4]
    ]
    s = c3 / (3 * z)
    beta2 = F(3, 2) * (15 * z * s**2 - c5) / z**5
    beta3 = F(9, 16) * (c7 - 105 * z * s**3 + 14 * beta2 * z**5 * s) / z**7
    beta = beta3 / beta2
    shift = s - beta * z * z / 3
    tau = z**n * beta**m
    nonlast, last = (beta * z * z).inverse(), beta ** (m - 1) * z ** (n - 2)
    assert tau.center == 1
    errors = []
    for group, factor in [(False, nonlast), (True, last)]:
        indices = [
            j
            for j, (_, site, _, _) in enumerate(point["keys"])
            if (site == n - 1) == group
        ]
        pure_count = sum(point["keys"][j][2:] == (0, 0) for j in indices)
        shifted = [
            point["Q"][j] + (shift.center if point["keys"][j][2:] == (0, 0) else 0)
            for j in indices
        ]
        radius = error_q + upper_sqrt(pure_count) * shift.radius
        errors.append(
            abs(factor.center) * radius + factor.radius * (length(shifted) + radius)
        )
        assert all(
            factor.center * x == point["source_vector"][j]
            for x, j in zip(shifted, indices)
        )
    frame_covariance_error = length(errors)
    gains, changes = [], []
    for i, j in itertools.combinations(range(n), 2):
        gain = (1 + chart_errors[i]) * (1 + chart_errors[j])
        block = [
            x
            for key, x in zip(point["keys"], point["source_vector"])
            if key[:2] == (i, j)
        ]
        gains.append(gain)
        changes.append((gain - 1) * length(block))
    covariance_error = max(gains) * frame_covariance_error + length(changes)
    mean_error = length(
        chart_errors[:-1] + [chart_errors[-1] + tau.radius * (1 + chart_errors[-1])]
    )
    total = upper_sqrt(covariance_error**2 + mean_error**2)
    return {
        **mean_report,
        "tensor_radius": str(delta_tensor),
        "adapted_tensor_radius": str(delta),
        "first_lift_error": str(error_q0),
        "flow_correction_error": str(error_x1),
        "pure_mean_correction_error": str(error_x2),
        "covariance_class_error": str(error_q),
        "response_coordinate_error": str(coefficient_error),
        "canonical_mean_error": str(mean_error),
        "canonical_covariance_error": str(covariance_error),
        "total_source_error": str(total),
    }


def local_source_certificate(edges, n, saved=None):
    """Mean gauge: mu_i[0]=1 for i<n-1; every edge entry remains free."""
    means = [[F(1), F(0), F(0)] for _ in range(n)]

    @lru_cache(None)
    def moment(sites):
        if not sites:
            return np.array(F(1), dtype=object)
        i, *rest = sites
        answer = (
            np.asarray(means[i], dtype=object).reshape((3,) + (1,) * len(rest))
            * moment(tuple(rest))[None]
        )
        for position, j in enumerate(rest, 1):
            pair = np.asarray(edges[i, j], dtype=object).reshape(
                (3, 3) + (1,) * (len(rest) - 1)
            )
            term = pair * moment(tuple(k for k in rest if k != j))[None, None]
            answer += np.moveaxis(term, 1, position)
        return answer

    keys = [("mu", i, a) for i in range(n) for a in range(3) if i == n - 1 or a != 0]
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
        array = np.zeros((3,) * n, dtype=object)
        index = [slice(None)] * n
        for site, colour in zip(sites, colours):
            index[site] = colour
        array[tuple(index)] = moment(tuple(i for i in range(n) if i not in sites))
        columns.append(array.reshape(-1).tolist())
    denominator = math.lcm(*(F(x).denominator for column in columns for x in column))
    matrix = fmpz_mat(
        [
            [int(columns[j][i] * denominator) for j in range(len(columns))]
            for i in range(3**n)
        ]
    )
    inverse, report = matrix_bound((matrix, denominator), saved)
    edge_bounds = {
        e: 1 + max(abs(F(x)) for row in block for x in row)
        for e, block in edges.items()
    }

    @lru_cache(None)
    def majorant(sites):
        if not sites:
            return F(1)
        i, *rest = sites
        return 2 * majorant(tuple(rest)) + sum(
            edge_bounds[i, j] * majorant(tuple(k for k in rest if k != j)) for j in rest
        )

    supports = [(frozenset([i]), 3 if i == n - 1 else 2) for i in range(n)]
    supports += [(frozenset(e), 9) for e in edges]
    squared = sum(
        wa
        * wb
        * 3 ** (n - len(a | b))
        * majorant(tuple(i for i in range(n) if i not in a | b)) ** 2
        for a, wa in supports
        for b, wb in supports
        if a.isdisjoint(b)
    )
    curvature = upper_sqrt(squared)
    radius = min(F(1), 1 / (2 * inverse * curvature))
    return {
        "matrix_certificate": report,
        "curvature_squared_bound": str(squared),
        "curvature_bound": str(curvature),
        "inverse_norm_bound": str(inverse),
        "correction_radius": str(radius),
        "free_parameters": len(keys),
    }
