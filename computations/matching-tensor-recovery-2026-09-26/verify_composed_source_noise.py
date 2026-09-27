"""Exact replay, symbolic calibration audit, and nonzero model perturbations.

Numerical proposals are disabled. Several constructions are checked separately;
the inequalities and integer matrix library are shared with the generator.
"""

import hashlib
import itertools
import json
import math
import random
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

import composed_source_noise_recovery as source
import covariance_noise_certificate as bounds
import full_source_noise_recovery as original
import numpy as np
import preconditioned_source_bounds as refined
import slice_noise_recovery as storage
import sympy as sp
from calibration_interval_jets import calibration
from flint import fmpz_mat
from verify_full_source_noise import (
    DirectExterior,
    check_local_jacobian,
    independent_moment,
)
from verify_shared_source_noise import independent_tensor
from verify_slice_noise_recovery import direct_slices


def mode_product(tensor, matrix, site):
    return np.moveaxis(np.tensordot(matrix, tensor, axes=(1, site)), 0, site)


def check_compression_jacobian(matrix, denominator, tensor, tensor_denominator):
    """Central differences are exact here: only one affine variable changes."""
    n = tensor.ndim
    for column, (site, colour) in enumerate(itertools.product(range(n), range(2))):
        evaluations = []
        for sign in [-1, 1]:
            value = tensor.copy()
            for i in range(n):
                local = np.array([[0, 1, 0], [0, 0, 1]], dtype=object)
                if i == site:
                    local[colour, 0] = -sign
                value = mode_product(value, local, i)
            evaluations.append(value.reshape(-1))
        expected = (evaluations[1] - evaluations[0]) / F(2 * tensor_denominator)
        assert all(
            F(int(matrix[row, column]), denominator) == x
            for row, x in enumerate(expected)
        )


def independent_refined_curvature(edges, n):
    """Count individual parameter columns; enumerate scalar matchings directly."""
    supports = [frozenset([i]) for i in range(n) for a in range(3) if i == n - 1 or a]
    supports += [frozenset(edge) for edge in edges for _ in range(9)]
    universe = frozenset(range(n))
    pairs, triples = Counter(), Counter()
    for first in supports:
        for second in supports:
            if not first.isdisjoint(second):
                continue
            union = first | second
            pairs[tuple(sorted(universe - union))] += 1
            for third in supports:
                if union.isdisjoint(third):
                    triples[tuple(sorted(universe - union - third))] += 1
    hessian2 = sum(
        count * sum(x * x for x in independent_moment(edges, n, sites))
        for sites, count in pairs.items()
    )
    edge_bounds = {
        e: 1 + max(abs(x) for row in block for x in row) for e, block in edges.items()
    }
    third2 = F(0)
    for sites, count in triples.items():
        majorant = F(0)
        for size in range(len(sites) // 2 + 1):
            for matching in itertools.combinations(
                list(itertools.combinations(sites, 2)), size
            ):
                used = [site for edge in matching for site in edge]
                if len(set(used)) == len(used):
                    majorant += 2 ** (len(sites) - 2 * size) * math.prod(
                        edge_bounds[edge] for edge in matching
                    )
        third2 += count * 3 ** len(sites) * majorant**2
    return hessian2, third2


def symbolic_calibration_audit(coordinates):
    """Different expressions and symbolic derivatives check the interval jets."""
    z, c3, c5, c7 = variables = sp.symbols("z c3 c5 c7")
    determinant = 5 * c3**2 - 3 * z * c5
    numerator = 9 * z**2 * c7 - 63 * z * c3 * c5 + 70 * c3**3
    shift = (-10 * c3**3 + 13 * z * c3 * c5 - 3 * z**2 * c7) / (8 * z * determinant)
    radius = F(1, 2**20)
    rng = random.Random(275347)
    offsets = [[F(0)] * 4] + [
        [radius * F(rng.randint(-8, 8), 8) for _ in range(4)] for _ in range(4)
    ]
    checks = 0
    for n in [7, 9]:
        m = n // 2
        expressions = {
            "shift": shift,
            "nonlast": 8 * z * determinant / numerator,
            "tau": z ** (1 - m) * numerator**m / (8**m * determinant**m),
            "last": z ** (2 - m)
            * numerator ** (m - 1)
            / (8 ** (m - 1) * determinant ** (m - 1)),
        }
        point = calibration(coordinates, F(0), n)
        discs = calibration(coordinates, radius, n)
        for name, expression in expressions.items():
            derivatives = [expression] + [sp.diff(expression, x) for x in variables]
            derivatives += [
                sp.diff(expression, x, y) for x in variables for y in variables
            ]
            exact = (
                [point[name].value]
                + point[name].gradient
                + [x for row in point[name].hessian for x in row]
            )
            enclosed = (
                [discs[name].value]
                + discs[name].gradient
                + [x for row in discs[name].hessian for x in row]
            )
            for derivative, center, disc in zip(derivatives, exact, enclosed):
                poly_num, poly_den = sp.fraction(sp.cancel(derivative))
                assert all(
                    x.q == 1
                    for poly in [poly_num, poly_den]
                    for x in sp.Poly(poly, *variables).coeffs()
                )
                evaluate_num = sp.lambdify(
                    variables, poly_num, modules="math", cse=True
                )
                evaluate_den = sp.lambdify(
                    variables, poly_den, modules="math", cse=True
                )
                for offset in offsets:
                    at = [
                        F(value + delta)
                        for value, delta in zip(coordinates[:4], offset)
                    ]
                    rational = F(evaluate_num(*at), evaluate_den(*at))
                    assert abs(rational - disc.center) <= disc.radius, (
                        n,
                        name,
                        str(derivative),
                        offset,
                    )
                    if not any(offset):
                        assert rational == center.center and center.radius == 0
                    checks += 1
    return {
        "orders": [7, 9],
        "exact_value_gradient_hessian_comparisons": checks,
        "nonzero_coefficient_offsets": len(offsets) - 1,
    }


def nonzero_source_checks(edges, n, point, mean_record, constants, affine):
    base_means = [[F(1), F(0), F(0)] for _ in range(n)]
    base_tensor = independent_tensor(base_means, edges, tuple(range(n)))
    source_matrix, source_denominator = affine["source"]
    reports = []
    for bits in [55, 90]:
        rng = random.Random(275348)
        step = F(1, 2**bits)
        means = [
            [F(1), step * rng.choice([-1, 1]), step * rng.choice([-1, 1])]
            for _ in range(n)
        ]
        means[-1][0] += step
        perturbed_edges = {
            e: [[x + step * rng.choice([-1, 1]) for x in row] for row in block]
            for e, block in edges.items()
        }
        tensor = independent_tensor(means, perturbed_edges, tuple(range(n)))
        distance = bounds.length(tensor - base_tensor)
        report = refined.propagate_affine(point, distance, mean_record, constants)
        lines = [
            np.array([F(0), mu[1] / mu[0], mu[2] / mu[0]], dtype=object) for mu in means
        ]
        mean_error = sum(x * x for row in lines for x in row)
        assert mean_error <= F(report["refined_affine_mean_error_bound"]) ** 2
        projections = [
            np.eye(3, dtype=object) - np.outer(row, [1, 0, 0]) for row in lines
        ]
        adapted = tensor.reshape((3,) * n)
        for i, projection in enumerate(projections):
            adapted = mode_product(adapted, projection, i)
        aligned_edges = {
            e: projections[e[0]] @ np.array(block, dtype=object) @ projections[e[1]].T
            for e, block in perturbed_edges.items()
        }
        aligned_change = [means[-1][0] - 1]
        aligned_change += [
            aligned_edges[i, j][a, b] - edges[i, j][a][b]
            for i, j, a, b in point["keys"]
        ]
        integers, denominator = bounds.common(adapted.reshape(-1) - base_tensor)
        linear = source_matrix * fmpz_mat([[x] for x in integers])
        remainder2 = sum(
            (value - F(int(linear[i, 0]), source_denominator * denominator)) ** 2
            for i, value in enumerate(aligned_change)
        )
        assert remainder2 <= F(report["aligned_source_remainder"]) ** 2
        actual2 = sum(
            (a - b) ** 2
            for mu, base in zip(means, base_means)
            for a, b in zip(mu, base)
        )
        actual2 += sum(
            (perturbed_edges[e][a][b] - block[a][b]) ** 2
            for e, block in edges.items()
            for a, b in itertools.product(range(3), repeat=2)
        )
        assert actual2 <= F(report["total_source_error"]) ** 2
        reports.append(
            {
                "perturbation_bits": bits,
                "tensor_distance_bound": str(distance),
                "actual_source_error_squared": str(actual2),
                "certified_source_error_bound": report["total_source_error"],
                "actual_composed_remainder_squared": str(remainder2),
                "certified_composed_remainder_bound": report[
                    "aligned_source_remainder"
                ],
                "nonzero_mean_and_edge_errors_checked": True,
            }
        )
    return reports


def run():
    root = Path(__file__).parent
    saved = json.loads((root / "composed-source-noise-certificate.json").read_text())
    baseline_path = root / saved["baseline_certificate"]["file"]
    assert (
        hashlib.sha256(baseline_path.read_bytes()).hexdigest()
        == saved["baseline_certificate"]["sha256"]
    )
    baseline = json.loads(baseline_path.read_text())
    n = saved["sites"]
    means = [[F(x) for x in row] for row in saved["candidate_means"]]
    edges = {
        tuple(record["sites"]): [[F(x) for x in row] for row in record["weights"]]
        for record in saved["candidate_edges"]
    }
    observed, denominator = (
        list(map(int, saved["observed_numerators"])),
        int(saved["observed_denominator"]),
    )
    clean = independent_tensor(means, edges, tuple(range(n)))
    comparison = saved["comparison_only"]
    assert list(clean) == [
        F(x, comparison["clean_denominator"]) for x in comparison["clean_numerators"]
    ]
    errors = [F(y, denominator) - x for x, y in zip(clean, observed)]
    assert errors == [
        F(x, int(comparison["noise_denominator"]))
        for x in comparison["noise_numerators"]
    ]
    assert sum(x * x for x in errors) <= F(saved["error_budget"]) ** 2
    assert all(F(float(F(y, denominator))) == F(y, denominator) for y in observed)
    assert all(float(F(y, denominator)) != float(x) for x, y in zip(clean, observed))
    tensor, tensor_denominator = original.unit_mean_tensor(edges, n)
    saved_bound, saved_point = bounds.matrix_bound, bounds.point_systems
    captured = {}

    def audited_bound(matrix, proposal=None):
        if matrix[0].ncols() == 2 * n + 1 + 9 * math.comb(n, 2):
            check_local_jacobian(*matrix, edges, n)
        elif matrix[0].ncols() == 2 * n:
            check_compression_jacobian(*matrix, tensor, tensor_denominator)
        return saved_bound(matrix, proposal)

    def capture_point(*args, **kwargs):
        captured["point"] = saved_point(*args, **kwargs)
        return captured["point"]

    def forbidden(*args, **kwargs):
        raise AssertionError("Replay attempted a numerical proposal")

    bounds.ExactExterior = DirectExterior
    bounds.matrix_bound, bounds.point_systems = audited_bound, capture_point
    bounds.eigh = storage.eigh = storage.solve = storage.svd = refined.solve = forbidden
    original.propose_source = original.anchor_proposal = forbidden
    storage.slices = direct_slices
    print(
        "Replaying exact certificate with numerical proposals disabled",
        file=sys.stderr,
        flush=True,
    )
    certificate = saved["certificate"]
    maps = {}
    rebuilt = source.certify(
        observed,
        denominator,
        F(saved["error_budget"]),
        means,
        edges,
        baseline,
        certificate["composed_constants"],
        maps.update,
    )
    assert rebuilt == certificate
    print(
        "Checking independent curvature, symbolic derivatives and perturbed sources",
        file=sys.stderr,
        flush=True,
    )
    hessian2, third2 = independent_refined_curvature(edges, n)
    local = certificate["refined_local_certificate"]
    assert hessian2 == F(local["point_hessian_frobenius_squared"])
    assert third2 == F(local["third_derivative_squared_bound_on_unit_ball"])
    point = captured["point"]
    symbolic = symbolic_calibration_audit(point["coordinates"])
    perturbations = nonzero_source_checks(
        edges,
        n,
        point,
        certificate["anchor_mean_certificate"],
        certificate["composed_constants"],
        maps,
    )
    matrix = point["linear_systems"][0]
    try:
        refined.left_inverse(
            matrix,
            storage.encode([[0] * matrix[0].nrows() for _ in range(matrix[0].ncols())]),
        )
    except AssertionError:
        pass
    else:
        raise AssertionError("Zero left inverse accepted")
    try:
        bounds.ScalarBall(1, 1).inverse()
    except AssertionError:
        pass
    else:
        raise AssertionError("Zero-containing denominator accepted")
    return {
        "sites": n,
        "all_saved_exact_acceptance_quantities_replayed": True,
        "numerical_proposal_functions_disabled": True,
        "tensor_and_exterior_assembly_checked_separately": True,
        "full_source_and_compression_jacobians_checked_separately": True,
        "point_hessian_and_third_derivative_majorant_checked_separately": True,
        "binary64_representability_and_visible_noise_checked": True,
        "symbolic_calibration_checks": symbolic,
        "nonzero_model_perturbations": perturbations,
        "invalid_left_inverse_and_zero_containing_denominator_rejected": True,
        "scope": "Exact replay and separate algebraic constructions share bound propagation and integer arithmetic with the generator. Perturbation examples are tests, not a proof of the general estimates. Not Lean formalized or independently peer reviewed.",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
