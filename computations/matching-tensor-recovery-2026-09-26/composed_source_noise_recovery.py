"""Blind numerical proposal and exact recovery certificate with visible noise.

The archived earlier certificate supplies untrusted matrix proposals at the
same candidate. All acceptance quantities are checked again before use.
"""

import hashlib
import json
import math
import random
import sys
from fractions import Fraction as F
from pathlib import Path

import covariance_noise_certificate as old
import full_source_noise_recovery as original
import numpy as np
import preconditioned_source_bounds as new
import slice_noise_recovery as mean_noise
from restricted_source_inverse import serialize_edges


def certify(
    observed,
    denominator,
    epsilon,
    means,
    edges,
    baseline,
    constants=None,
    audit_maps=None,
):
    n = len(means)
    assert n >= 7 and n % 2 == 1
    assert means == [[F(1), F(0), F(0)] for _ in range(n)]
    assert len(observed) == 3**n and denominator > 0 and F(epsilon) >= 0
    tensor, tensor_denominator = original.unit_mean_tensor(edges, n)
    residual2 = sum(
        (F(int(x), tensor_denominator) - F(int(y), denominator)) ** 2
        for x, y in zip(tensor.reshape(-1), observed)
    )
    residual = old.upper_sqrt(residual2)
    reference = baseline["certificate"]
    anchor = reference["anchor_proposal"]
    assert anchor["reference_slice"] == 0
    for name in ["A", "B"]:
        entries, _ = mean_noise.decode(anchor[name])
        assert all(row[0] == 0 for row in entries)
    assert mean_noise.decode(anchor["tail_vector"])[0] == [
        [mean_noise.SCALE] + [0] * (3 ** (n - 1) - 1)
    ]
    slices = mean_noise.slices(tensor)
    assert np.all(slices[1][:, 0] == 0) and np.all(slices[2][:, 0] == 0)
    mean = mean_noise.certify(tensor, tensor_denominator, F(0), anchor)
    assert F(mean["bounds"]["tail_vector_residual_bound"]) == 0
    point = old.point_systems(
        tensor, tensor_denominator, edges, reference["covariance_matrix_certificates"]
    )
    local = old.local_source_certificate(
        edges, n, reference["local_certificate"]["matrix_certificate"]["preconditioner"]
    )
    inverse = F(local["inverse_norm_bound"])
    improved_local = new.refined_local_radius(edges, n, inverse)
    radius = F(improved_local["correction_radius"])
    checked = new.build_constants(
        tensor, tensor_denominator, edges, point, constants, audit_maps
    )
    delta = F(epsilon) + residual
    enclosure = new.propagate_affine(point, delta, mean, checked)
    assert F(enclosure["total_source_error"]) < radius / 2
    assert inverse * residual < radius / 2
    comparisons = []
    strategies = [
        ("original", old.propagate, F(local["correction_radius"])),
        (
            "preconditioned_norms",
            lambda p, d, m: new.propagate(p, d, m, checked),
            F(local["correction_radius"]),
        ),
        (
            "composed_linear_maps",
            lambda p, d, m: new.propagate_affine(p, d, m, checked),
            F(local["correction_radius"]),
        ),
        (
            "composed_maps_and_point_curvature",
            lambda p, d, m: new.propagate_affine(p, d, m, checked),
            radius,
        ),
    ]
    for name, method, ball in strategies:
        trials = []
        for bits in range(30, 141):
            try:
                result = method(point, F(1, 2**bits), mean)
                bound = F(result["total_source_error"])
                trials.append(
                    {
                        "bits": bits,
                        "propagation_passed": True,
                        "source_error_bound": str(bound),
                        "basin_entry_certified": bound < ball / 2,
                    }
                )
            except AssertionError as error:
                trials.append(
                    {"bits": bits, "propagation_passed": False, "reason": str(error)}
                )
        accepted = [
            entry["bits"] for entry in trials if entry.get("basin_entry_certified")
        ]
        comparisons.append(
            {
                "strategy": name,
                "first_accepted_bits_in_tested_range": min(accepted)
                if accepted
                else None,
                "tested_tensor_radii": trials,
            }
        )
    return {
        "candidate_forward_residual_squared": str(residual2),
        "candidate_forward_residual_bound": str(residual),
        "anchor_mean_certificate": mean,
        "covariance_matrix_certificates": point["matrix_certificates"],
        "original_local_certificate": local,
        "refined_local_certificate": improved_local,
        "composed_constants": checked,
        "global_enclosure": enclosure,
        "global_canonical_source_error_bound": str(2 * inverse * delta),
        "exact_arithmetic_correction_error_bound": str(2 * inverse * F(epsilon)),
        "strategy_comparison": comparisons,
        "scope": "Every compatible source in the mean gauge enters the checked full-source correction ball. A supplied noise budget is assumed; no floating correction iteration is validated.",
    }


def run():
    root = Path(__file__).parent
    baseline_path = root / "full-source-noise-certificate.json"
    baseline = json.loads(baseline_path.read_text())
    n, edges = original.source_example()
    clean, clean_denominator = original.unit_mean_tensor(edges, n)
    noise_denominator = 2**46
    rng = random.Random(275346)
    noise = [rng.choice([-1, 1]) for _ in range(3**n)]
    denominator = math.lcm(clean_denominator, noise_denominator)
    observed = [
        int(x) * (denominator // clean_denominator)
        + e * (denominator // noise_denominator)
        for x, e in zip(clean.reshape(-1), noise)
    ]
    means, candidate, diagnostics = original.propose_source(observed, denominator, n)
    print(
        "Proposal from perturbed data ready; certifying composed bounds",
        file=sys.stderr,
        flush=True,
    )
    certificate = certify(
        observed, denominator, F(47, noise_denominator), means, candidate, baseline
    )
    assert candidate == edges
    visible = sum(
        float(F(y, denominator)) != float(F(int(x), clean_denominator))
        for x, y in zip(clean.reshape(-1), observed)
    )
    exact_float = all(
        F(float(F(y, denominator))) == F(y, denominator) for y in observed
    )
    assert visible == 3**n and exact_float
    return {
        "sites": n,
        "baseline_certificate": {
            "file": baseline_path.name,
            "sha256": hashlib.sha256(baseline_path.read_bytes()).hexdigest(),
        },
        "observed_numerators": list(map(str, observed)),
        "observed_denominator": str(denominator),
        "error_budget": str(F(47, noise_denominator)),
        "candidate_means": [[str(x) for x in row] for row in means],
        "candidate_edges": serialize_edges(
            {
                edge: [[str(x) for x in row] for row in block]
                for edge, block in candidate.items()
            }
        ),
        "numerical_proposal_diagnostics": diagnostics,
        "certificate": certificate,
        "comparison_only": {
            "clean_numerators": clean.reshape(-1).tolist(),
            "clean_denominator": clean_denominator,
            "noise_numerators": noise,
            "noise_denominator": str(noise_denominator),
            "all_observed_entries_exactly_representable_in_binary64": exact_float,
            "changed_entries_visible_in_binary64": visible,
            "candidate_equals_test_source": True,
        },
        "limitations": [
            "One point-dependent numerical-scale example, not an experimental-noise or uniform recovery guarantee.",
            "The proposal rounds to denominators at most 64; acceptance does not assume a bound on the true source denominators.",
            "Unit-mean candidate driver; combining with the separate coordinate wrapper and shared-source implementation is not tested here.",
            "No validated floating correction iteration. Not Lean formalized or independently peer reviewed.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
