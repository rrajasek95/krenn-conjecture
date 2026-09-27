"""Binary64 correction proposals with exact a posteriori output certificates.

No bound trusts the numerical solve or floating forward evaluation. The saved
shared-source certificate supplies the global enclosure, replayed separately.
"""

import hashlib
import itertools
import json
import math
import sys
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

import covariance_noise_certificate as bounds
import numpy as np
import shared_source_alignment as alignment
import shared_source_local_certificate as joint
import slice_noise_recovery as storage
from flint import fmpz_mat
from scipy.linalg import solve


def parameter_keys(means, edges):
    n = len(means[0])
    return [
        ("mu", s, i, a)
        for s in range(len(means))
        for i in range(n)
        for a in range(3)
        if s or i == n - 1 or a
    ] + [
        ("R", i, j, a, b)
        for i, j in edges
        for a, b in itertools.product(range(3), repeat=2)
    ]


def flatten(means, edges, keys):
    return [
        means[key[1]][key[2]][key[3]]
        if key[0] == "mu"
        else edges[key[1], key[2]][key[3]][key[4]]
        for key in keys
    ]


def unflatten(values, means, edges, keys):
    mu = [[list(row) for row in setting] for setting in means]
    cov = {edge: [list(row) for row in block] for edge, block in edges.items()}
    for key, value in zip(keys, values, strict=True):
        if key[0] == "mu":
            mu[key[1]][key[2]][key[3]] = value
        else:
            cov[key[1], key[2]][key[3]][key[4]] = value
    return mu, cov


def matching_array(means, edges, dtype):
    """Matching recurrence for either Python integers or binary64 proposals."""
    n = len(means)

    @lru_cache(None)
    def visit(sites):
        if not sites:
            return np.array(1, dtype=dtype)
        i, *rest = sites
        result = (
            np.array(means[i], dtype=dtype).reshape((3,) + (1,) * len(rest))
            * visit(tuple(rest))[None]
        )
        for position, j in enumerate(rest, 1):
            pair = np.array(edges[i, j], dtype=dtype).reshape(
                (3, 3) + (1,) * (len(rest) - 1)
            )
            result = result + np.moveaxis(
                pair * visit(tuple(k for k in rest if k != j))[None, None], 1, position
            )
        return result

    return visit(tuple(range(n))).reshape(-1)


def exact_forward(means, edges):
    entries = [F(x) for mu in means for row in mu for x in row]
    entries += [F(x) for block in edges.values() for row in block for x in row]
    scale = math.lcm(*(x.denominator for x in entries))
    cov = {
        edge: [[int(F(x) * scale * scale) for x in row] for row in block]
        for edge, block in edges.items()
    }
    values = []
    for setting in means:
        mu = [[int(F(x) * scale) for x in row] for row in setting]
        values.extend(int(x) for x in matching_array(mu, cov, object))
    return values, scale ** len(means[0])


def load_context(audit_derivative=None):
    root = Path(__file__).parent
    path = root / "composed-shared-source-certificate.json"
    source = json.loads(path.read_text())
    records = []
    for entry in source["observations"]:
        observation = root / entry["file"]
        assert hashlib.sha256(observation.read_bytes()).hexdigest() == entry["sha256"]
        records.append(json.loads(observation.read_text()))
    means, edges, aligned = alignment.align(records)
    assert aligned == source["alignment_certificate"]
    keys = parameter_keys(means, edges)
    columns = {key: index for index, key in enumerate(keys)}
    rows, exact_tensors = [], []
    for s, mu in enumerate(means):
        tensor, derivative, local_keys = joint.point_derivative(mu, edges, s == 0)
        if audit_derivative is not None:
            audit_derivative(mu, edges, tensor, derivative, local_keys)
        local_to_global = [
            columns[("mu", s, *key[1:]) if key[0] == "mu" else key]
            for key in local_keys
        ]
        for row in derivative:
            values = [F(0)] * len(keys)
            for index, value in zip(local_to_global, row):
                values[index] = F(value)
            rows.append(values)
        exact_tensors.extend(map(F, tensor))
    denominator = math.lcm(*(x.denominator for row in rows for x in row))
    matrix = fmpz_mat([[int(x * denominator) for x in row] for row in rows])
    local = source["joint_local_certificate"]
    inverse, matrix_certificate = bounds.matrix_bound(
        (matrix, denominator), local["matrix_certificate"]["preconditioner"]
    )
    assert matrix_certificate == local["matrix_certificate"]
    assert joint.curvature_squared(means, edges) == F(local["curvature_squared_bound"])
    data = [
        F(int(x), int(record["observed_denominator"]))
        for record in records
        for x in record["observed_numerators"]
    ]
    clean, clean_denominator = exact_forward(means, edges)
    assert exact_tensors == [F(x, clean_denominator) for x in clean]
    residual2 = sum((x - y) ** 2 for x, y in zip(data, exact_tensors))
    assert residual2 == F(local["joint_forward_residual_squared"])
    epsilon = bounds.length(F(record["error_budget"]) for record in records)
    assert epsilon == F(local["stacked_error_budget"])
    p_values, p_scale = storage.decode(matrix_certificate["preconditioner"])
    preconditioner = fmpz_mat(p_values)
    p_norm = bounds.length(x for row in p_values for x in row) / p_scale
    eta = F(
        int(matrix_certificate["residual_frobenius_upper"]), p_scale**2 * denominator**2
    )
    assert eta < 1
    radius = F(local["refined_global_joint_error_bound"])
    assert 0 < radius <= F(local["correction_radius"]) <= 1
    contraction = inverse * F(local["curvature_bound"]) * radius
    assert contraction < 1
    return {
        "source": source,
        "source_file": path.name,
        "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "means": means,
        "edges": edges,
        "keys": keys,
        "center": list(map(F, flatten(means, edges, keys))),
        "matrix": matrix,
        "matrix_denominator": denominator,
        "preconditioner": preconditioner,
        "preconditioner_scale": p_scale,
        "preconditioner_norm": p_norm,
        "gram_error": eta,
        "inverse": inverse,
        "radius": radius,
        "contraction": contraction,
        "data": data,
        "epsilon": epsilon,
    }


def projected_step_bound(context, residual):
    integers, denominator = bounds.common(residual)
    gradient = context["matrix"].transpose() * fmpz_mat([[x] for x in integers])
    whitened = context["preconditioner"].transpose() * gradient
    whitened_den = (
        denominator * context["matrix_denominator"] * context["preconditioner_scale"]
    )
    squared = F(
        sum(int(x) ** 2 for row in whitened.tolist() for x in row), whitened_den**2
    )
    norm = bounds.upper_sqrt(squared)
    approximate = context["preconditioner"] * whitened
    approximate_den = whitened_den * context["preconditioner_scale"]
    approximate_squared = F(
        sum(int(x) ** 2 for row in approximate.tolist() for x in row),
        approximate_den**2,
    )
    defect = (
        context["preconditioner_norm"]
        * context["gram_error"]
        * norm
        / (1 - context["gram_error"])
    )
    step = min(
        bounds.upper_sqrt(approximate_squared) + defect,
        context["preconditioner_norm"] * norm / (1 - context["gram_error"]),
    )
    return step, squared, approximate_squared, defect


def inspect_output(context, values, audit_forward=None):
    assert len(values) == len(context["keys"])
    displacement2 = sum((x - y) ** 2 for x, y in zip(values, context["center"]))
    assert displacement2 <= context["radius"] ** 2, (
        "Output lies outside the certified common ball"
    )
    means, edges = unflatten(
        values, context["means"], context["edges"], context["keys"]
    )
    numerators, denominator = exact_forward(means, edges)
    forward = [F(x, denominator) for x in numerators]
    if audit_forward is not None:
        audit_forward(means, edges, forward)
    residual = [x - y for x, y in zip(context["data"], forward)]
    step, squared, approximate_squared, defect = projected_step_bound(context, residual)
    fixed_distance = step / (1 - context["contraction"])
    source_error = fixed_distance + context["inverse"] * context["epsilon"] / (
        1 - context["contraction"]
    )
    mean_matrix = list(
        map(list, zip(*[[x for row in mu for x in row] for mu in means]))
    )
    return {
        "source_displacement_squared": str(displacement2),
        "forward_residual_squared": str(sum(x * x for x in residual)),
        "preconditioned_normal_residual_squared": str(squared),
        "approximate_projected_step_squared": str(approximate_squared),
        "gram_defect_correction_bound": str(defect),
        "exact_frozen_correction_norm_bound": str(step),
        "distance_to_exact_fixed_point_bound": str(fixed_distance),
        "global_source_error_bound": str(source_error),
        "observed_mean_span": alignment.full_column_span(mean_matrix, source_error),
        "mean_span_relative_to_exact_fixed_point": alignment.full_column_span(
            mean_matrix, fixed_distance
        ),
    }


def certify_outputs(context, outputs, audit_forward=None):
    center = inspect_output(context, context["center"], audit_forward)
    center_step = F(center["exact_frozen_correction_norm_bound"])
    assert center_step + context["contraction"] * context["radius"] <= context["radius"]
    reports = []
    for output in outputs:
        floats = [float.fromhex(x) for x in output["parameter_hex"]]
        assert all(math.isfinite(x) for x in floats)
        values = list(map(F, floats))
        reports.append(
            {
                "iteration": output["iteration"],
                **inspect_output(context, values, audit_forward),
            }
        )
    selected = min(
        range(len(reports)),
        key=lambda i: F(reports[i]["distance_to_exact_fixed_point_bound"]),
    )
    return {
        "free_parameters": len(context["keys"]),
        "gram_preconditioner_error_bound": str(context["gram_error"]),
        "preconditioner_operator_norm_bound": str(context["preconditioner_norm"]),
        "source_ball_radius": str(context["radius"]),
        "contraction_factor_bound": str(context["contraction"]),
        "noise_error_bound_at_exact_fixed_point": str(
            context["inverse"] * context["epsilon"] / (1 - context["contraction"])
        ),
        "center_check": center,
        "output_checks": reports,
        "selected_output_index": selected,
        "selection_rule": "Smallest certified distance to the exact frozen-Jacobian fixed point among all recorded outputs.",
        "scope": "Every recorded binary64 output is checked as an exact dyadic source. Bounds cover all compatible shared sources in the certified gauge. The numerical trajectory is not assumed exact and need not be contractive.",
    }


def numerical_proposals(context, steps=3):
    values = np.array([float(x) for x in context["center"]])
    assert [F(x) for x in values] == context["center"]
    matrix = (
        np.array(context["matrix"].tolist(), dtype=float)
        / context["matrix_denominator"]
    )
    gram = matrix.T @ matrix
    data = np.array([float(x) for x in context["data"]])
    assert list(map(F, data)) == context["data"]
    outputs = []
    for iteration in range(1, steps + 1):
        means, edges = unflatten(
            values.tolist(), context["means"], context["edges"], context["keys"]
        )
        forward = np.concatenate([matching_array(mu, edges, float) for mu in means])
        correction = solve(gram, matrix.T @ (data - forward), assume_a="pos")
        values = values + correction
        outputs.append(
            {"iteration": iteration, "parameter_hex": [float(x).hex() for x in values]}
        )
    return outputs


def run():
    context = load_context()
    outputs = numerical_proposals(context)
    print(
        "Three binary64 correction outputs ready; certifying with exact arithmetic",
        file=sys.stderr,
        flush=True,
    )
    certificate = certify_outputs(context, outputs)
    return {
        "source_certificate": {
            "file": context["source_file"],
            "sha256": context["source_sha256"],
        },
        "numerical_outputs": outputs,
        "certificate": certificate,
        "limitations": [
            "Validation is a posteriori for the saved binary64 outputs, not a claim that every floating operation or trajectory follows the exact contraction map.",
            "The target fixed point solves projected frozen-Jacobian equations; it need not minimize the full data residual.",
            "The synthetic starting candidate equals the planted source. Moving toward a noisy-data fixed point need not improve error against that planted source.",
            "Conditional on the input global shared-source certificate and stated error budgets; not a uniform or experimental-noise guarantee. Not Lean formalized or independently peer reviewed.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
