"""Integrate composed single-source certificates with shared-source alignment.

Each observed tensor is supplied to the numerical proposal independently.
Archived files supply only matrix proposals, which are checked again.
"""

import argparse
import hashlib
import json
import math
import random
import sys
from fractions import Fraction as F
from pathlib import Path

import composed_source_noise_recovery as composed
import covariance_noise_certificate as bounds
import full_source_noise_recovery as original
import numpy as np
import preconditioned_source_bounds as refined
import shared_source_alignment as alignment
import shared_source_local_certificate as joint
import source_chart_certificate as chart
from blind_mean_search import contract
from shared_source_noise_recovery import encode_edges


def certify_chart(
    observed, denominator, epsilon, means, edges, baseline, saved=None, audit_maps=None
):
    n = len(means)
    bases, inverses = chart.coordinate_changes(means)
    tensor = np.array([F(int(x), denominator) for x in observed], dtype=object).reshape(
        (3,) * n
    )
    changed = contract(tensor, inverses).reshape(-1)
    changed_integers, changed_denominator = bounds.common(changed)
    changed_edges = {
        (i, j): (inverses[i] @ np.array(block, dtype=object) @ inverses[j].T).tolist()
        for (i, j), block in edges.items()
    }
    data_gain = math.prod(chart.norm_bound(matrix) for matrix in inverses)
    unit_baseline = {"certificate": baseline["chart_certificate"]["unit_certificate"]}
    unit_record = composed.certify(
        changed_integers,
        changed_denominator,
        F(epsilon) * data_gain,
        [[F(1), F(0), F(0)] for _ in range(n)],
        changed_edges,
        unit_baseline,
        None if saved is None else saved["unit_certificate"]["composed_constants"],
        audit_maps,
    )
    basis_norms = [chart.norm_bound(matrix) for matrix in bases]
    mean_gain = max(basis_norms)
    edge_gain = max(basis_norms[i] * basis_norms[j] for i, j in edges)
    unit_error = F(unit_record["global_canonical_source_error_bound"])
    return {
        "unit_certificate": unit_record,
        "data_norm_amplification_bound": str(data_gain),
        "mean_return_norm_bound": str(mean_gain),
        "edge_return_norm_bound": str(edge_gain),
        "global_mean_error_bound": str(mean_gain * unit_error),
        "global_edge_error_bound": str(edge_gain * unit_error),
        "global_total_source_error_bound": str(max(mean_gain, edge_gain) * unit_error),
        "gauge": "At each site except the last, the true first mean coordinate equals that of this candidate. This is a product-one scaling gauge in the original coordinates.",
    }


def make_observation(index, noise_bits=46):
    assert index in [1, 2, 3]
    root = Path(__file__).parent
    baseline_path = root / f"shared-source-observation-{index}.json"
    baseline = json.loads(baseline_path.read_text())
    n, edges = original.source_example()
    means = [[F(1), F(0), F(0)] for _ in range(n)]
    means[index - 1][0] = F(2)
    for i, row in enumerate(means):
        if index == 1:
            row[1] = F(1, 16)
        elif index == 2:
            row[2] = F(1, 16)
        else:
            row[1], row[2] = F(i % 3 - 1, 16), F(2 * (i % 2) - 1, 16)
    clean, clean_denominator = chart.rational_tensor(means, edges)
    noise_denominator = 2**noise_bits
    denominator = math.lcm(clean_denominator, noise_denominator)
    rng = random.Random(275400 + index)
    noise = [rng.choice([-1, 1]) for _ in range(3**n)]
    observed = [
        int(x) * (denominator // clean_denominator)
        + e * (denominator // noise_denominator)
        for x, e in zip(clean.reshape(-1), noise)
    ]
    mu, candidate_edges, diagnostics = original.propose_source(observed, denominator, n)
    print(
        f"Observation {index}: raw noisy-data proposal ready",
        file=sys.stderr,
        flush=True,
    )
    certificate = certify_chart(
        observed, denominator, F(47, noise_denominator), mu, candidate_edges, baseline
    )
    print(
        f"Observation {index}: global certificate accepted", file=sys.stderr, flush=True
    )
    scales = [1 / row[0] for row in means[:-1]]
    scales.append(1 / math.prod(scales))
    assert mu == [[x * scales[i] for x in row] for i, row in enumerate(means)]
    assert all(
        candidate_edges[i, j]
        == [[x * scales[i] * scales[j] for x in row] for row in block]
        for (i, j), block in edges.items()
    )
    visible = sum(
        float(F(y, denominator)) != float(F(int(x), clean_denominator))
        for x, y in zip(clean.reshape(-1), observed)
    )
    exact_float = all(
        F(float(F(y, denominator))) == F(y, denominator) for y in observed
    )
    return {
        "sites": n,
        "baseline_certificate": {
            "file": baseline_path.name,
            "sha256": hashlib.sha256(baseline_path.read_bytes()).hexdigest(),
        },
        "observed_numerators": list(map(str, observed)),
        "observed_denominator": str(denominator),
        "error_budget": str(F(47, noise_denominator)),
        "candidate_means": [[str(x) for x in row] for row in mu],
        "candidate_edges": encode_edges(candidate_edges),
        "numerical_proposal_diagnostics": diagnostics,
        "chart_certificate": certificate,
        "comparison_only": {
            "actual_means": [[str(x) for x in row] for row in means],
            "actual_edges": encode_edges(edges),
            "clean_numerators": clean.reshape(-1).tolist(),
            "clean_denominator": clean_denominator,
            "noise_numerators": noise,
            "noise_denominator": str(noise_denominator),
            "changed_entries_visible_in_binary64": visible,
            "all_observed_entries_exactly_representable_in_binary64": exact_float,
        },
    }


def finish(records, paths, saved_joint=None, audit=None):
    means, edges, aligned = alignment.align(records)
    local = joint.certify(
        means, edges, records, aligned["joint_source_error_bound"], saved_joint, audit
    )
    matrix = list(map(list, zip(*[[x for row in mu for x in row] for mu in means])))
    return {
        "sites": len(means[0]),
        "observations": [
            {"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            for path in paths
        ],
        "alignment_certificate": aligned,
        "joint_local_certificate": local,
        "refined_mean_span": alignment.full_column_span(
            matrix, F(local["refined_global_joint_error_bound"])
        ),
        "input_radius_trials": [larger_radius_trials(record) for record in records[1:]],
        "limitations": [
            "Conditional on existence of one common source fitting the supplied per-observation error budgets; acceptance is not an existence test.",
            "Point-dependent certificate from four full tensors at seven sites, not uniform recovery or an experimental-noise guarantee.",
            "The recovered mean space is the span of the four observed global mean vectors, in the first observation's gauge; no unobserved directions are inferred.",
            "Exact-arithmetic correction is certified; no floating-point correction iteration is validated. Not Lean formalized or independently peer reviewed.",
        ],
    }


def larger_radius_trials(record):
    """Retain sufficient-condition failures without rerunning source proposals."""
    mu, edges, _, _ = alignment.parse_source(record)
    n = len(mu)
    _, inverses = chart.coordinate_changes(mu)
    changed_edges = {
        (i, j): (inverses[i] @ np.array(block, dtype=object) @ inverses[j].T).tolist()
        for (i, j), block in edges.items()
    }
    tensor, denominator = original.unit_mean_tensor(changed_edges, n)
    unit = record["chart_certificate"]["unit_certificate"]
    point = bounds.point_systems(
        tensor, denominator, changed_edges, unit["covariance_matrix_certificates"]
    )
    base_radius = F(unit["global_enclosure"]["tensor_radius"])
    ball = F(unit["refined_local_certificate"]["correction_radius"])
    trials = []
    for multiplier in [1, 2, 4, 8]:
        trial = {
            "tensor_radius_multiplier": multiplier,
            "tensor_radius": str(multiplier * base_radius),
        }
        try:
            result = refined.propagate_affine(
                point,
                multiplier * base_radius,
                unit["anchor_mean_certificate"],
                unit["composed_constants"],
            )
            trial.update(
                {
                    "propagation_passed": True,
                    "outer_source_error_bound": result["total_source_error"],
                    "half_ball_entry_certified": F(result["total_source_error"])
                    < ball / 2,
                }
            )
        except AssertionError as error:
            trial.update({"propagation_passed": False, "reason": str(error)})
        trials.append(trial)
    return {
        "half_ball_radius": str(ball / 2),
        "trials": trials,
        "scope": "Multiples of this observation's candidate-centered tensor radius in its unit-mean chart; failed sufficient conditions do not prove ambiguity.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--observation", type=int, choices=[1, 2, 3])
    parser.add_argument("--noise-bits", type=int, default=46)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.observation:
        record = make_observation(args.observation, args.noise_bits)
        path = args.output_dir / f"composed-shared-observation-{args.observation}.json"
        path.write_text(json.dumps(record, indent=2) + "\n")
        print(
            json.dumps(
                {
                    "saved": str(path),
                    "global_source_error_bound": record["chart_certificate"][
                        "global_total_source_error_bound"
                    ],
                    "visible_entries": record["comparison_only"][
                        "changed_entries_visible_in_binary64"
                    ],
                }
            )
        )
    else:
        root = Path(__file__).parent
        paths = [root / "composed-source-noise-certificate.json"] + [
            args.output_dir / f"composed-shared-observation-{i}.json" for i in [1, 2, 3]
        ]
        records = [json.loads(path.read_text()) for path in paths]
        archived = json.loads(
            (root / "shared-source-noise-certificate.json").read_text()
        )
        print(
            json.dumps(
                finish(records, paths, archived["joint_local_certificate"]), indent=2
            )
        )
