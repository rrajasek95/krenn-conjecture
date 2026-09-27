#!/usr/bin/env python3
"""A blind numerical source proposal followed by a global exact certificate.

The saved example requires an extremely small error budget. The certificate
proves basin entry and full-source error bounds; it does not claim practical
noise thresholds or certify the floating-point correction iteration.
"""

import itertools
import json
import math
import random
import sys
import time
from fractions import Fraction as F

import covariance_noise_certificate as bounds
import numpy as np
import slice_noise_recovery as mean_noise
from blind_mean_search import integer_tensor
from floating_source_inverse import propose_mean_lines, recover
from restricted_source_inverse import serialize_edges


def source_example():
    n = 7
    rng = random.Random(275101)
    edges = {
        e: [[F(rng.choice([-1, 1]), 16) for _ in range(3)] for _ in range(3)]
        for e in itertools.combinations(range(n), 2)
    }
    for k in range(3):
        i, j = 2 * k + 1, 2 * k + 2
        for a in [1, 2]:
            edges[i, j][a][a] += 1
        for site in [i, j]:
            edges[0, site][1][1] += k + 1
            edges[0, site][2][2] += 1
    return n, edges


def unit_mean_tensor(edges, n):
    denominator = math.lcm(
        *(F(x).denominator for block in edges.values() for row in block for x in row)
    )
    root = math.isqrt(denominator)
    scale = root if root * root == denominator else denominator
    means = [[scale, 0, 0] for _ in range(n)]
    integers = {
        e: [[int(scale * scale * x) for x in row] for row in block]
        for e, block in edges.items()
    }
    return integer_tensor(means, integers), scale**n


def propose_source(observed, denominator, n):
    tensor = np.asarray([float(F(x, denominator)) for x in observed]).reshape((3,) * n)
    lines = propose_mean_lines(tensor)
    means, edges, diagnostics = recover(tensor, lines)
    # Rationalization only proposes a candidate. Its forward residual is checked later.
    rounded_means = [[F(float(x)).limit_denominator(64) for x in row] for row in means]
    rounded_edges = {
        e: [[F(float(x)).limit_denominator(64) for x in row] for row in block]
        for e, block in edges.items()
    }
    return (
        rounded_means,
        rounded_edges,
        {key: float(value) for key, value in diagnostics.items()},
    )


def anchor_proposal(tensor, denominator):
    n = tensor.ndim
    proposal = mean_noise.propose(tensor, denominator)
    for name in ["A", "B"]:
        entries, scale = mean_noise.decode(proposal[name])
        for row in entries:
            row[0] = 0
        proposal[name] = mean_noise.encode(entries, scale)
    proposal["tail_vector"] = mean_noise.encode(
        [[mean_noise.SCALE] + [0] * (3 ** (n - 1) - 1)]
    )
    proposal["tail_lines"] = mean_noise.encode(
        [[mean_noise.SCALE, 0, 0] for _ in range(n - 1)]
    )
    return proposal


def certify(
    observed,
    denominator,
    epsilon,
    candidate_means,
    candidate_edges,
    n,
    anchor=None,
    matrix_certificates=None,
    local_preconditioner=None,
):
    # This implementation handles the unit-mean chart used in the saved witness.
    assert n >= 7 and n % 2 == 1
    assert len(observed) == 3**n and denominator > 0 and F(epsilon) >= 0
    assert candidate_means == [[F(1), F(0), F(0)] for _ in range(n)]
    tensor, tensor_denominator = unit_mean_tensor(candidate_edges, n)
    residual_squared = sum(
        (F(int(x), tensor_denominator) - F(int(y), denominator)) ** 2
        for x, y in zip(tensor.reshape(-1), observed)
    )
    residual = bounds.upper_sqrt(residual_squared)
    delta = F(epsilon) + residual
    anchor = (
        anchor if anchor is not None else anchor_proposal(tensor, tensor_denominator)
    )
    for name in ["A", "B"]:
        entries, _ = mean_noise.decode(anchor[name])
        assert all(row[0] == 0 for row in entries)
    assert mean_noise.decode(anchor["tail_vector"])[0] == [
        [mean_noise.SCALE] + [0] * (3 ** (n - 1) - 1)
    ]
    slices = mean_noise.slices(tensor)
    assert np.all(slices[1][:, 0] == 0) and np.all(slices[2][:, 0] == 0)
    mean_record = mean_noise.certify(tensor, tensor_denominator, F(0), anchor)
    assert F(mean_record["bounds"]["tail_vector_residual_bound"]) == 0
    point = bounds.point_systems(
        tensor, tensor_denominator, candidate_edges, matrix_certificates
    )
    outer = bounds.propagate(point, delta, mean_record)
    local = bounds.local_source_certificate(candidate_edges, n, local_preconditioner)
    radius = F(local["correction_radius"])
    inverse = F(local["inverse_norm_bound"])
    assert F(outer["total_source_error"]) < radius / 2
    assert inverse * residual <= radius / 2
    radii = []
    for bits in [40, 80, 100, 120, 128, 140]:
        try:
            attempt = bounds.propagate(point, F(1, 2**bits), mean_record)
            radii.append(
                {
                    "bits": bits,
                    "propagation_passed": True,
                    "source_error_bound": attempt["total_source_error"],
                    "basin_entry_certified": F(attempt["total_source_error"])
                    < radius / 2,
                }
            )
        except AssertionError as error:
            radii.append(
                {"bits": bits, "propagation_passed": False, "reason": str(error)}
            )
    return {
        "anchor_proposal": anchor,
        "anchor_mean_certificate": mean_record,
        "covariance_matrix_certificates": point["matrix_certificates"],
        "local_certificate": local,
        "candidate_forward_residual_squared": str(residual_squared),
        "candidate_forward_residual_bound": str(residual),
        "outer_bound": outer,
        "global_canonical_source_error_bound": str(2 * inverse * delta),
        "exact_arithmetic_correction_error_bound": str(2 * inverse * F(epsilon)),
        "tested_tensor_radii": radii,
        "scope": "Every matching source compatible with the data-error ball is in the certified local mean-gauge basin. Correction convergence is an exact-arithmetic theorem, not a validated floating-point iteration.",
    }


def run():
    start = time.monotonic()
    n, edges = source_example()
    clean, clean_denominator = unit_mean_tensor(edges, n)
    rng = random.Random(275140)
    noise = [rng.choice([-1, 1]) for _ in range(3**n)]
    noise_denominator = 2**140
    denominator = math.lcm(clean_denominator, noise_denominator)
    observed = [
        int(x) * (denominator // clean_denominator)
        + e * (denominator // noise_denominator)
        for x, e in zip(clean.reshape(-1), noise)
    ]
    epsilon = F(47, noise_denominator)
    means, candidate, diagnostics = propose_source(observed, denominator, n)
    print(
        "Blind source proposal constructed; certifying all compatible sources",
        file=sys.stderr,
        flush=True,
    )
    report = certify(observed, denominator, epsilon, means, candidate, n)
    assert candidate == edges
    print("Complete certificate passed", file=sys.stderr, flush=True)
    return {
        "sites": n,
        "observed_numerators": [str(x) for x in observed],
        "observed_denominator": str(denominator),
        "error_budget": str(epsilon),
        "candidate_means": [[str(x) for x in row] for row in means],
        "candidate_edges": serialize_edges(
            {
                e: [[str(x) for x in row] for row in block]
                for e, block in candidate.items()
            }
        ),
        "numerical_proposal_diagnostics": diagnostics,
        "certificate": report,
        "comparison_only": {
            "clean_numerators": clean.reshape(-1).tolist(),
            "clean_denominator": clean_denominator,
            "noise_numerators": noise,
            "noise_denominator": str(noise_denominator),
            "candidate_equals_test_source": True,
        },
        "elapsed_seconds": time.monotonic() - start,
        "limitations": [
            "Very conservative certified error budget; not a practical noise threshold.",
            "The saved perturbation is below double precision at this source; the numerical proposal effectively sees rounded clean data. The certificate uses the exact perturbed rational data.",
            "Numerical proposal rounds to denominators at most 64; certificate does not assume the true source has that bound.",
            "This saved implementation certifies a unit-mean candidate chart; arbitrary candidate charts require the fixed basis changes described in the note.",
            "Not Lean formalized or independently peer reviewed.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
