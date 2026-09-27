"""Sharper global-to-local mean bounds and preconditioned covariance residuals.

Proposals are numerical; every accepted bound is replayed with integers and
fractions. Published earlier certificates retain their original inequalities.
"""

import itertools
import math
from fractions import Fraction as F
from functools import lru_cache

import covariance_noise_certificate as old
import numpy as np
import slice_noise_recovery as storage
from calibration_interval_jets import calibration
from flint import fmpz_mat
from floating_source_inverse import setup
from scipy.linalg import solve
from shared_source_local_certificate import point_derivative


def round_up(value, precision=70):
    value = F(value)
    assert value >= 0
    if not value:
        return F(0)
    exponent = value.numerator.bit_length() - value.denominator.bit_length()
    scale = 2 ** max(0, precision - exponent)
    return F(
        (value.numerator * scale + value.denominator - 1) // value.denominator, scale
    )


def matrix_norm(matrix, denominator=1):
    rows = matrix.tolist()
    squared = sum(int(x) ** 2 for row in rows for x in row)
    one = max(sum(abs(int(row[j])) for row in rows) for j in range(matrix.ncols()))
    infinity = max(sum(abs(int(x)) for x in row) for row in rows)
    return old.upper_sqrt(F(min(squared, one * infinity), denominator**2))


def left_inverse(matrix, saved=None):
    a, denominator = matrix
    if saved is None:
        floating = np.array(a.tolist(), dtype=float) / denominator
        proposal = solve(floating.T @ floating, floating.T, assume_a="pos")
        saved = storage.encode(storage.quantize(proposal))
    entries, scale = storage.decode(saved)
    left = fmpz_mat(entries)
    product = left * a
    expected = denominator * scale
    residual2 = sum(
        (int(product[i, j]) - (expected if i == j else 0)) ** 2
        for i in range(a.ncols())
        for j in range(a.ncols())
    )
    residual = old.upper_sqrt(F(residual2, expected**2))
    assert residual < 1
    norm = matrix_norm(left, scale)
    return (left, scale), {
        "proposal": saved,
        "left_identity_residual_squared": str(F(residual2, expected**2)),
        "left_identity_residual_bound": str(residual),
        "left_operator_norm_bound": str(norm),
    }


def multiply(left, right):
    a, da = left
    b, db = right
    return a * b, da * db


def matrix_add(first, second, sign=1):
    a, da = first
    b, db = second
    denominator = math.lcm(da, db)
    return a * (denominator // da) + b * (sign * (denominator // db)), denominator


def rational_matrix(rows):
    denominator = math.lcm(*(F(x).denominator for row in rows for x in row))
    return fmpz_mat(
        [[int(F(x) * denominator) for x in row] for row in rows]
    ), denominator


def polyadd(*terms):
    result = {}
    for coefficient, poly in terms:
        for index, value in poly.items():
            result[index] = result.get(index, F(0)) + coefficient * value
    return {index: value for index, value in result.items() if value}


def vector_poly(vector):
    return {i: F(x) for i, x in enumerate(vector) if x}


def dense_exterior(poly, n):
    entries, denominator = old.common(poly.values())
    tensor = np.zeros(3**n, dtype=object)
    for index, value in zip(poly, entries):
        tensor[index] = value
    action = old.ExactExterior(tensor, denominator, n)
    return action.apply([{i: 1} for i in range(3**n)])


def compression_certificate(tensor, denominator, saved=None):
    n = tensor.ndim
    words = list(itertools.product([1, 2], repeat=n))
    columns = [(i, a) for i in range(n) for a in [1, 2]]
    jacobian = []
    for word in words:
        row = []
        for i, a in columns:
            index = list(word)
            index[i] = 0
            row.append(-int(tensor[tuple(index)]) if word[i] == a else 0)
        jacobian.append(row)
    inverse, certificate = old.matrix_bound(
        (fmpz_mat(jacobian), denominator),
        None if saved is None else saved["matrix_certificate"]["preconditioner"],
    )
    assert all(tensor[word] == 0 for word in words)
    slice_sum = F(0)
    for i in range(n):
        for j in range(n):
            if i != j:
                index = [slice(None)] * n
                index[i] = index[j] = 0
                slice_sum += sum(
                    F(int(x), denominator) ** 2
                    for x in tensor[tuple(index)].reshape(-1)
                )
    factor = (1 + F(1, n - 2)) ** (n - 2)
    curvature2 = 4 * factor * slice_sum
    curvature = old.upper_sqrt(curvature2)
    radius = min(F(1), 1 / (2 * inverse * curvature))
    return {
        "matrix_certificate": certificate,
        "inverse_norm_bound": str(inverse),
        "ordered_two_zero_slice_norms_squared": str(slice_sum),
        "curvature_squared_bound": str(curvature2),
        "curvature_bound": str(curvature),
        "local_radius": str(radius),
    }


def anchored_bounds(delta_tensor, record, n):
    values = {k: F(v) for k, v in record["bounds"].items()}
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
    delta = 2 ** ((n - 1) // 2) * delta_tensor
    assert nu * delta < 1, "Reference slice inverse not certified"
    inverse = nu / (1 - nu * delta)
    a0 = b0 = inverse * delta
    a1 = inverse * (values["A_solve_residual_bound"] + delta * a)
    b1 = inverse * (values["B_solve_residual_bound"] + delta * b)
    at, bt = a + a0 + a1, b + b0 + b1
    s0, s1 = (b + bt) * a0 + (a + at) * b0, (b + bt) * a1 + (a + at) * b1
    t0, t1 = at * s0 + c * a0, at * s1 + c * a1
    h0, h1 = old.upper_sqrt(s0**2 + t0**2), old.upper_sqrt(s1**2 + t1**2)
    feedback = g * h1
    assert feedback < 1, "Anchored feedback is not below one"
    angle = g * h0 / (1 - feedback)
    assert angle < F(1, 4), "Global mean-angle bound too large"
    first = old.upper_sqrt(((a + a1) * angle + a0) ** 2 + ((b + b1) * angle + b0) ** 2)
    errors = [first] + [angle / (1 - angle)] * (n - 1)
    return errors, {"feedback_bound": str(feedback), "tail_sine_bound": str(angle)}


def refined_means(delta, mean_record, n, compression):
    coarse, report = anchored_bounds(delta, mean_record, n)
    coarse_norm = old.length(coarse)
    radius = F(compression["local_radius"])
    assert coarse_norm < radius, "Global means have not entered the compression ball"
    inverse = F(compression["inverse_norm_bound"])
    projection_gain = old.upper_sqrt((1 + coarse_norm**2 / n) ** n)
    total = min(coarse_norm, round_up(2 * inverse * projection_gain * delta))
    return [total] * n, {
        **report,
        "coarse_affine_mean_error_bound": str(coarse_norm),
        "refined_affine_mean_error_bound": str(total),
    }


def build_constants(tensor, denominator, edges, point, saved=None, audit_maps=None):
    n, m = point["n"], point["n"] // 2
    keys, codes, flows, pure, product = setup(n)
    f2 = sorted(set(codes))
    free = [code for code in f2 if code not in [0, point["pivot_coordinate"]]]
    section = {}
    for i, code in enumerate(codes):
        section.setdefault(code, i)
    q0, q1, q = [vector_poly(point[name]) for name in ["Q0", "Q1", "Q"]]
    d1, d2 = polyadd((1, q1), (-1, q0)), polyadd((1, q), (-1, q1))
    response = {}
    for index, value in q0.items():
        code = codes[index]
        response[code] = response.get(code, F(0)) + value
    nuisance = {code: x for code, x in zip(free, point["x1"][len(flows) :]) if x}
    s1 = polyadd((F(1, 2), product(q0, q0)), (1, product(q0, d1)), (1, nuisance))
    s2 = polyadd((F(1, 2), product(q1, q1)), (1, product(q1, d2)))
    action = old.ExactExterior(tensor, denominator, n)
    for residual in [response, s1, s2]:
        applied, _ = action.apply([residual])
        assert all(int(x) == 0 for row in applied.tolist() for x in row)
    lefts, reports = [], []
    for i, matrix in enumerate(point["linear_systems"]):
        left, report = left_inverse(
            matrix, None if saved is None else saved["left_inverses"][i]["proposal"]
        )
        lefts.append(left)
        reports.append(report)
    data_norms, data_maps = [], []
    for left, residual in zip(lefts, [response, s1, s2]):
        matrix = multiply(left, dense_exterior(residual, n))
        data_maps.append(matrix)
        data_norms.append(matrix_norm(*matrix))
    prior1 = action.apply([product(q1, {section[code]: F(1)}) for code in free])
    prior2 = action.apply([product(q, {i: F(1)}) for i in range(len(keys))])
    prior_map1, prior_map2 = multiply(lefts[1], prior1), multiply(lefts[2], prior2)
    k1 = matrix_norm(*prior_map1)
    k2 = matrix_norm(*prior_map2)
    _, source_jacobian, _ = point_derivative(
        [[F(1), F(0), F(0)] for _ in range(n)], edges, True
    )
    covariance_jacobian = source_jacobian[:, 2 * n + 1 :] * point["covariance_scale"]
    common = math.lcm(*(F(x).denominator for x in covariance_jacobian.reshape(-1)))
    derivative = (
        fmpz_mat([[int(F(x) * common) for x in row] for row in covariance_jacobian]),
        common,
    )
    coordinate_prior = multiply(lefts[3], derivative)
    kc = matrix_norm(*coordinate_prior)
    section_map = (
        fmpz_mat(
            [[int(i == section[code]) for code in free] for i in range(len(keys))]
        ),
        1,
    )
    flow_map = (
        fmpz_mat(
            [
                [int(row.get(i, 0)) for row in flows] + [0] * len(free)
                for i in range(len(keys))
            ]
        ),
        1,
    )
    pure_map = (
        fmpz_mat([[int(row.get(i, 0)) for row in pure] for i in range(len(keys))]),
        1,
    )
    x0_map = data_maps[0]
    x1_map = matrix_add(data_maps[1], multiply(prior_map1, x0_map), -1)
    q1_map = matrix_add(multiply(section_map, x0_map), multiply(flow_map, x1_map))
    x2_map = matrix_add(data_maps[2], multiply(prior_map2, q1_map), -1)
    q_map = matrix_add(q1_map, multiply(pure_map, x2_map))
    coordinate_map = matrix_add(lefts[3], multiply(coordinate_prior, q_map), -1)
    scalar = calibration(point["coordinates"], F(0), n)
    q_coefficients = [[F(0)] * len(keys)]
    c_coefficients = [[x.center for x in scalar["tau"].gradient] + [F(0)] * (m - 3)]
    for index, (_, site, a, b) in enumerate(keys):
        factor = scalar["last" if site == n - 1 else "nonlast"]
        pure_entry = int(a == b == 0)
        shifted = point["Q"][index] + pure_entry * scalar["shift"].value.center
        q_coefficients.append(
            [factor.value.center if index == j else F(0) for j in range(len(keys))]
        )
        c_coefficients.append(
            [
                shifted * factor.gradient[j].center
                + pure_entry * factor.value.center * scalar["shift"].gradient[j].center
                for j in range(4)
            ]
            + [F(0)] * (m - 3)
        )
    source_map = matrix_add(
        multiply(rational_matrix(q_coefficients), q_map),
        multiply(rational_matrix(c_coefficients), coordinate_map),
    )
    affine = {
        "x0": x0_map,
        "x1": x1_map,
        "q1": q1_map,
        "x2": x2_map,
        "q": q_map,
        "c": coordinate_map,
        "source": source_map,
    }
    if audit_maps is not None:
        audit_maps(affine)
    restricted_derivative = rational_matrix(
        source_jacobian[
            :, [2 * n - 2] + list(range(2 * n + 1, len(source_jacobian[0])))
        ].tolist()
    )
    identity_check, identity_den = multiply(source_map, restricted_derivative)
    assert identity_check.nrows() == identity_check.ncols()
    identity_residual = identity_check - fmpz_mat(
        [
            [identity_den if i == j else 0 for j in range(identity_check.ncols())]
            for i in range(identity_check.nrows())
        ]
    )
    identity_norm = matrix_norm(identity_residual, identity_den)
    assert identity_norm < F(1, 1000), (
        "Composed linear source map fails the forward-derivative check"
    )
    return {
        "left_inverses": reports,
        "data_forcing_norm_bounds": list(map(str, data_norms)),
        "first_prior_forcing_norm_bound": str(k1),
        "second_prior_forcing_norm_bound": str(k2),
        "coordinate_prior_forcing_norm_bound": str(kc),
        "composed_linear_norm_bounds": {
            name: str(matrix_norm(*matrix)) for name, matrix in affine.items()
        },
        "composed_source_forward_identity_residual_bound": str(identity_norm),
        "compression": compression_certificate(
            tensor, denominator, None if saved is None else saved["compression"]
        ),
        "scope": "Bounds of composed linear residual maps, checked by exact multiplication; all numerical left inverses are proposals only.",
    }


def refined_local_radius(edges, n, inverse):
    """Use the point Hessian and a unit-ball third-derivative bound."""

    @lru_cache(None)
    def moment(sites):
        if not sites:
            return np.array(F(1), dtype=object)
        i, *rest = sites
        result = np.zeros((3,) * len(sites), dtype=object)
        result[0] = moment(tuple(rest))
        for position, j in enumerate(rest, 1):
            pair = np.array(edges[i, j], dtype=object).reshape(
                (3, 3) + (1,) * (len(rest) - 1)
            )
            result += np.moveaxis(
                pair * moment(tuple(k for k in rest if k != j))[None, None], 1, position
            )
        return result

    edge_bounds = {
        edge: 1 + max(abs(F(x)) for row in block for x in row)
        for edge, block in edges.items()
    }

    @lru_cache(None)
    def majorant(sites):
        if not sites:
            return F(1)
        i, *rest = sites
        return 2 * majorant(tuple(rest)) + sum(
            edge_bounds[i, j] * majorant(tuple(k for k in rest if k != j)) for j in rest
        )

    @lru_cache(None)
    def norm_squared(sites):
        return sum(F(x) ** 2 for x in moment(sites).reshape(-1))

    supports = [(frozenset([i]), 3 if i == n - 1 else 2) for i in range(n)]
    supports += [(frozenset(edge), 9) for edge in edges]
    hessian2 = F(0)
    third2 = F(0)
    for a, wa in supports:
        for b, wb in supports:
            if a.isdisjoint(b):
                remaining = tuple(i for i in range(n) if i not in a | b)
                hessian2 += wa * wb * norm_squared(remaining)
                for c, wc in supports:
                    if (a | b).isdisjoint(c):
                        rest = tuple(i for i in remaining if i not in c)
                        third2 += wa * wb * wc * 3 ** len(rest) * majorant(rest) ** 2
    hessian, third = old.upper_sqrt(hessian2), old.upper_sqrt(third2)
    radius = min(
        F(1), 1 / (4 * inverse * hessian), 1 / old.upper_sqrt(4 * inverse * third)
    )
    assert inverse * (hessian + third * radius) * radius <= F(1, 2)
    return {
        "point_hessian_frobenius_squared": str(hessian2),
        "point_hessian_bound": str(hessian),
        "third_derivative_squared_bound_on_unit_ball": str(third2),
        "third_derivative_bound": str(third),
        "inverse_norm_bound": str(inverse),
        "correction_radius": str(radius),
    }


def propagate(point, delta_tensor, mean_record, constants, bootstrap=True):
    n, m = point["n"], point["n"] // 2
    delta_tensor = F(delta_tensor)
    if bootstrap:
        chart_errors, mean_report = refined_means(
            delta_tensor, mean_record, n, constants["compression"]
        )
    else:
        chart_errors, mean_report = anchored_bounds(delta_tensor, mean_record, n)
    product = math.prod(1 + x for x in chart_errors)
    delta = round_up(product * delta_tensor + (product - 1) * point["tensor_norm"])
    assert delta < point["outside_norm_lower"], "Outside response might vanish"
    kappa = 2 ** ((n + 1) // 2)
    multiplication = old.upper_sqrt(6 * math.comb(n, 4))
    w1, w2 = old.upper_sqrt(n - 1), old.upper_sqrt(math.comb(n, 2))
    left_norms = [F(r["left_operator_norm_bound"]) for r in constants["left_inverses"]]
    left_errors = [
        F(r["left_identity_residual_bound"]) for r in constants["left_inverses"]
    ]
    forcing = [F(x) for x in constants["data_forcing_norm_bounds"]]

    def solve_bound(index, matrix_change, rhs_bound):
        gap = 1 - left_errors[index] - left_norms[index] * matrix_change
        assert gap > 0, "Perturbed preconditioned system not certified invertible"
        return round_up(rhs_bound / gap)

    error0 = solve_bound(0, kappa * delta, forcing[0] * delta)

    def correction(
        index, previous, following, error, basis_norm, prior_norm, nuisance=False
    ):
        before, after = old.length(previous), old.length(following)
        matrix_change = (
            kappa
            * multiplication
            * basis_norm
            * ((point["tensor_norm"] + delta) * error + delta * before)
        )
        if nuisance:
            matrix_change += kappa * delta
        remainder = (
            left_norms[index]
            * kappa
            * multiplication
            * (delta * after * error + (point["tensor_norm"] + delta) * error**2 / 2)
        )
        rhs = forcing[index] * delta + prior_norm * error + remainder
        return solve_bound(index, matrix_change, rhs)

    x1_error = correction(
        1,
        point["Q0"],
        point["Q1"],
        error0,
        w1,
        F(constants["first_prior_forcing_norm_bound"]),
        True,
    )
    error1 = round_up(error0 + w1 * x1_error)
    x2_error = correction(
        2,
        point["Q1"],
        point["Q"],
        error1,
        w2,
        F(constants["second_prior_forcing_norm_bound"]),
    )
    errorq = round_up(error1 + w2 * x2_error)
    qnorm = old.length(point["Q"])
    multiplicities = {
        k: old.upper_sqrt(F(math.factorial(2 * k) * math.comb(n, 2 * k), 2**k))
        for k in range(1, m + 1)
    }
    frame_change = old.length(
        multiplicities[k] * (qnorm + errorq) ** (k - 1) * errorq / math.factorial(k - 1)
        for k in range(1, m + 1)
    )
    remainder = sum(
        abs(point["coordinates"][m - k])
        * multiplicities[k]
        * (qnorm + errorq) ** (k - 2)
        * errorq**2
        / (2 * math.factorial(k - 2))
        for k in range(2, m + 1)
    )
    coordinate_error = solve_bound(
        3,
        frame_change,
        left_norms[3] * (delta + remainder)
        + F(constants["coordinate_prior_forcing_norm_bound"]) * errorq,
    )
    return old.finish_from_class_error(
        point,
        delta_tensor,
        chart_errors,
        mean_report,
        delta,
        error0,
        x1_error,
        x2_error,
        errorq,
        coordinate_error,
    )


def propagate_affine(point, delta_tensor, mean_record, constants):
    """Keep the common linear data dependence; bound only the remaining errors."""
    n, m = point["n"], point["n"] // 2
    delta_tensor = F(delta_tensor)
    chart_errors, mean_report = refined_means(
        delta_tensor, mean_record, n, constants["compression"]
    )
    gain = math.prod(1 + x for x in chart_errors)
    delta = round_up(gain * delta_tensor + (gain - 1) * point["tensor_norm"])
    assert delta < point["outside_norm_lower"], "Outside response might vanish"
    kappa = 2 ** ((n + 1) // 2)
    multiplication = old.upper_sqrt(6 * math.comb(n, 4))
    w1, w2 = old.upper_sqrt(n - 1), old.upper_sqrt(math.comb(n, 2))
    norms = [F(r["left_operator_norm_bound"]) for r in constants["left_inverses"]]
    defects = [F(r["left_identity_residual_bound"]) for r in constants["left_inverses"]]
    linear = {k: F(v) for k, v in constants["composed_linear_norm_bounds"].items()}

    def error_and_remainder(name, index, matrix_change, forcing_remainder):
        beta = defects[index] + norms[index] * matrix_change
        assert beta < 1, f"Preconditioned {name} system not certified invertible"
        remainder = round_up(
            (forcing_remainder + beta * linear[name] * delta) / (1 - beta)
        )
        return round_up(linear[name] * delta + remainder), remainder

    error0, remainder0 = error_and_remainder("x0", 0, kappa * delta, F(0))

    def correction(
        name,
        index,
        previous,
        following,
        error,
        remainder,
        basis_norm,
        prior_norm,
        nuisance=False,
    ):
        before, after = old.length(previous), old.length(following)
        matrix_change = (
            kappa
            * multiplication
            * basis_norm
            * ((point["tensor_norm"] + delta) * error + delta * before)
        )
        if nuisance:
            matrix_change += kappa * delta
        nonlinear = (
            norms[index]
            * kappa
            * multiplication
            * (delta * after * error + (point["tensor_norm"] + delta) * error**2 / 2)
        )
        return error_and_remainder(
            name, index, matrix_change, prior_norm * remainder + nonlinear
        )

    error_x1, remainder_x1 = correction(
        "x1",
        1,
        point["Q0"],
        point["Q1"],
        error0,
        remainder0,
        w1,
        F(constants["first_prior_forcing_norm_bound"]),
        True,
    )
    remainder_q1 = round_up(remainder0 + w1 * remainder_x1)
    error_q1 = round_up(linear["q1"] * delta + remainder_q1)
    error_x2, remainder_x2 = correction(
        "x2",
        2,
        point["Q1"],
        point["Q"],
        error_q1,
        remainder_q1,
        w2,
        F(constants["second_prior_forcing_norm_bound"]),
    )
    remainder_q = round_up(remainder_q1 + w2 * remainder_x2)
    error_q = round_up(linear["q"] * delta + remainder_q)
    qnorm = old.length(point["Q"])
    multiplicities = {
        k: old.upper_sqrt(F(math.factorial(2 * k) * math.comb(n, 2 * k), 2**k))
        for k in range(1, m + 1)
    }
    frame_change = old.length(
        multiplicities[k]
        * (qnorm + error_q) ** (k - 1)
        * error_q
        / math.factorial(k - 1)
        for k in range(1, m + 1)
    )
    response_remainder = sum(
        abs(point["coordinates"][m - k])
        * multiplicities[k]
        * (qnorm + error_q) ** (k - 2)
        * error_q**2
        / (2 * math.factorial(k - 2))
        for k in range(2, m + 1)
    )
    error_c, remainder_c = error_and_remainder(
        "c",
        3,
        frame_change,
        norms[3] * response_remainder
        + F(constants["coordinate_prior_forcing_norm_bound"]) * remainder_q,
    )
    scalars = calibration(point["coordinates"], error_c, n)
    gradient_norms = {name: jet.gradient_norm() for name, jet in scalars.items()}
    hessian_norms = {name: jet.hessian_bound() for name, jet in scalars.items()}
    scalar_remainders = {
        name: round_up(bound * error_c**2 / 2) for name, bound in hessian_norms.items()
    }
    increments = {
        name: min(
            jet.value.radius,
            round_up(gradient_norms[name] * error_c + scalar_remainders[name]),
        )
        for name, jet in scalars.items()
    }
    mean_remainder = gradient_norms["tau"] * remainder_c + scalar_remainders["tau"]
    group_remainders = []
    for last in [False, True]:
        name = "last" if last else "nonlast"
        indices = [
            i
            for i, (_, site, _, _) in enumerate(point["keys"])
            if (site == n - 1) == last
        ]
        count = sum(point["keys"][i][2:] == (0, 0) for i in indices)
        pure_norm = old.upper_sqrt(count)
        center = [
            point["Q"][i]
            + (scalars["shift"].value.center if point["keys"][i][2:] == (0, 0) else 0)
            for i in indices
        ]
        center_norm = old.length(center)
        scale = abs(scalars[name].value.center)
        remainder = scale * remainder_q
        remainder += (
            gradient_norms[name] * center_norm
            + scale * gradient_norms["shift"] * pure_norm
        ) * remainder_c
        remainder += (
            scalar_remainders[name] * center_norm
            + scale * scalar_remainders["shift"] * pure_norm
        )
        remainder += increments[name] * (error_q + increments["shift"] * pure_norm)
        group_remainders.append(round_up(remainder))
    aligned_remainder = old.length([mean_remainder] + group_remainders)
    aligned_error = round_up(linear["source"] * delta + aligned_remainder)
    gains, changes = [], []
    for i, j in itertools.combinations(range(n), 2):
        pair_gain = (1 + chart_errors[i]) * (1 + chart_errors[j])
        gains.append(pair_gain)
        block = [
            x
            for key, x in zip(point["keys"], point["source_vector"])
            if key[:2] == (i, j)
        ]
        changes.append((pair_gain - 1) * old.length(block))
    frame_error = old.length(
        [F(mean_report["refined_affine_mean_error_bound"])] + changes
    )
    total = round_up(max(gains) * aligned_error + frame_error)
    return {
        **mean_report,
        "tensor_radius": str(delta_tensor),
        "adapted_tensor_radius": str(delta),
        "first_lift_error": str(error0),
        "first_lift_remainder": str(remainder0),
        "flow_correction_error": str(error_x1),
        "flow_correction_remainder": str(remainder_x1),
        "pure_mean_correction_error": str(error_x2),
        "pure_mean_correction_remainder": str(remainder_x2),
        "covariance_class_error": str(error_q),
        "covariance_class_remainder": str(remainder_q),
        "response_coordinate_error": str(error_c),
        "response_coordinate_remainder": str(remainder_c),
        "calibration_hessian_bounds": {k: str(v) for k, v in hessian_norms.items()},
        "aligned_source_error": str(aligned_error),
        "aligned_source_remainder": str(aligned_remainder),
        "total_source_error": str(total),
    }
