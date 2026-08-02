#!/usr/bin/env python3
"""Audit the first normal cofactor on a rank-(1,1), b=3 coordinate gate.

If the left shore is the fixed physical row i, perturb a clean rank-one
cap (x+tau e_i)y^T.  The unperturbed response is supported on the three
complement sites.  Exact interpolation of the full homogeneous clean error
shows that its tau-linear coefficient is

  2 sigma(0)^(h-2)
    (U_A q_A^[h-2]) tensor (P_B(x) S_B(y)^[2]).

The endpoint transpose is formal.  This checker uses exact rational
specializations in the universal site-square-zero support algebra.
Research evidence only.
"""

from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
ALG = run_path(str(
    HERE / "verify_line_plus_plane_coordinate_gate_quadratic_cofactor.py"
))
add = ALG["add"]
scale = ALG["scale"]
multiply = ALG["multiply"]
divided_power = ALG["divided_power"]
linear_element = ALG["linear_element"]
restrict = ALG["restrict"]
linear_combination = ALG["linear_combination"]
quadratic = ALG["quadratic"]
scalar = ALG["scalar"]
error = ALG["error"]
serialize = ALG["serialize"]

EXPECTED_DIGEST = "82e624f73ebdaff486252bd0f5d36a977c09ecb6d888d4d75533f0c79bf167cf"


def lagrange_derivative_weights(degree):
    require(degree >= 1, ("bad interpolation degree", degree))
    weights = []
    for node in range(degree + 1):
        if node == 0:
            weights.append(-sum(Q(1, other)
                                for other in range(1, degree + 1)))
            continue
        numerator = Q(1)
        denominator = Q(1)
        for other in range(degree + 1):
            if other == node:
                continue
            denominator *= node - other
            if other != 0:
                numerator *= -other
        weights.append(numerator / denominator)
    require(sum(weights) == 0,
            ("interpolation weights do not kill constants", weights))
    require(sum(weight * node for node, weight in enumerate(weights)) == 1,
            ("interpolation weights do not recover the linear term",
             weights))
    return tuple(weights)


def base_rows(h, fixed_row):
    site_count = 2 * h
    a_sites = tuple(range(site_count - 3))
    b_sites = tuple(range(site_count - 3, site_count))
    all_sites = tuple(range(site_count))
    u_values = tuple(Q((site + 2) * (2 + site % 3))
                     for site in all_sites)
    r_values = tuple(Q((site + 3) * (3 + (site + 1) % 2))
                     for site in all_sites)

    p_rows = []
    for label in range(3):
        values = [
            u_values[site] if (
                label == fixed_row and site in a_sites
            ) else (
                Q((label + 2) * (site + 3) - 4)
                if site in b_sites else Q(0)
            )
            for site in all_sites
        ]
        p_rows.append(linear_element(values))

    mu = (Q(1), Q(2), Q(-1))
    s_rows = []
    for label in range(3):
        values = [
            mu[label] * r_values[site]
            if site in a_sites
            else Q((label + 5) * (site + 1) + 2)
            for site in all_sites
        ]
        s_rows.append(linear_element(values))
    matrix = tuple(
        tuple(Q(3 + 2 * i - 3 * j + 2 * i * j)
              for j in range(3))
        for i in range(3)
    )
    return (
        a_sites, b_sites, all_sites, p_rows, s_rows, mu, matrix
    )


def instance(h, fixed_row, x, y):
    (a_sites, b_sites, all_sites,
     p_rows, s_rows, mu, matrix) = base_rows(h, fixed_row)
    require(x[fixed_row] == 0,
            ("the base cap left the coordinate plane", fixed_row, x))
    require(sum(mu[index] * y[index] for index in range(3)) == 0,
            ("the right cap vector left its kernel", y))

    q = quadratic(all_sites)
    q_a = restrict(q, a_sites)
    p_x = linear_combination(p_rows, x)
    s_y = linear_combination(s_rows, y)
    require(not restrict(p_x, a_sites),
            ("the base left star left the complement", fixed_row, x))
    require(not restrict(s_y, a_sites),
            ("the right star left the complement", fixed_row, y))
    base_response = multiply(p_x, s_y)
    require(not divided_power(base_response, 2),
            ("the base response stopped being clean",
             h, fixed_row, x, y))

    e_fixed = tuple(Q(index == fixed_row) for index in range(3))
    normal_star = p_rows[fixed_row]
    sigma_zero = scalar(matrix, x, y)
    weights = lagrange_derivative_weights(h)
    full_values = []
    for parameter in range(h + 1):
        perturbed_x = tuple(
            x[index] + parameter * e_fixed[index]
            for index in range(3)
        )
        response = multiply(
            linear_combination(p_rows, perturbed_x), s_y
        )
        sigma = scalar(matrix, perturbed_x, y)
        full_values.append(error(q, response, sigma, h))
    actual_derivative = {}
    for weight, value in zip(weights, full_values):
        actual_derivative = add(
            actual_derivative, scale(value, weight)
        )

    u_a = restrict(normal_star, a_sites)
    p_x_b = restrict(p_x, b_sites)
    s_y_b = restrict(s_y, b_sites)
    shore_cofactor = multiply(
        u_a, divided_power(q_a, h - 2)
    )
    endpoint_tensor = multiply(
        p_x_b, divided_power(s_y_b, 2)
    )
    expected_derivative = scale(
        multiply(shore_cofactor, endpoint_tensor),
        2 * Q(sigma_zero) ** (h - 2),
    )
    require(actual_derivative == expected_derivative,
            ("the first normal cofactor changed",
             h, fixed_row, x, y))

    direct_derivative = scale(
        multiply(
            divided_power(q, h - 2),
            multiply(
                base_response,
                multiply(normal_star, s_y),
            ),
        ),
        Q(sigma_zero) ** (h - 2),
    )
    require(actual_derivative == direct_derivative,
            ("interpolation disagrees with direct differentiation",
             h, fixed_row, x, y))
    return actual_derivative, sigma_zero


def audit():
    ledger = []
    nonzero = 0
    for h in (3, 4, 5):
        for fixed_row in range(3):
            other = tuple(index for index in range(3)
                          if index != fixed_row)
            x_vectors = []
            for first, second in ((1, 2), (2, -1), (-1, 3)):
                vector = [Q(0)] * 3
                vector[other[0]], vector[other[1]] = first, second
                x_vectors.append(tuple(vector))
            y_vectors = (
                (Q(1), Q(1), Q(3)),
                (Q(2), Q(1), Q(4)),
                (Q(1), Q(2), Q(5)),
            )
            for x in x_vectors:
                for y in y_vectors:
                    derivative, sigma_zero = instance(
                        h, fixed_row, x, y
                    )
                    nonzero += bool(derivative)
                    ledger.append((
                        h, fixed_row, x, y, sigma_zero,
                        serialize(derivative),
                    ))
    require(nonzero > 0, "the first normal cofactor became vacuous")
    digest = sha256(repr(tuple(ledger)).encode()).hexdigest()
    require(digest == EXPECTED_DIGEST,
            ("the first-normal ledger changed", digest))
    return len(ledger), nonzero, digest


def main():
    count, nonzero, digest = audit()
    print("rank-(1,1) coordinate-gate first normal cofactor: passed")
    print(f"  exact rational instances : {count}")
    print(f"  nonzero first normals    : {nonzero}")
    print(f"  aggregate ledger digest  : {digest}")
    print("  conclusion               : coordinate gate enters one-bright jet")


if __name__ == "__main__":
    main()
