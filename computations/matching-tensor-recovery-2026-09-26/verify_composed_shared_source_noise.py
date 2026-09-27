"""Replay visible-noise shared recovery and check a distinct compatible source.

The inequalities and arithmetic libraries are shared with the generator.
Tensor, exterior, Jacobian, curvature, and projector checks are separate.
"""

import hashlib
import itertools
import json
import random
import sys
from fractions import Fraction as F
from pathlib import Path

import composed_shared_source_noise as shared
import composed_source_noise_recovery as composed
import covariance_noise_certificate as bounds
import full_source_noise_recovery as original
import numpy as np
import preconditioned_source_bounds as refined
import shared_source_alignment as alignment
import slice_noise_recovery as storage
import source_chart_certificate as chart
from flint import fmpq_mat
from verify_composed_source_noise import (
    check_compression_jacobian,
    independent_refined_curvature,
    symbolic_calibration_audit,
)
from verify_full_source_noise import DirectExterior, check_local_jacobian
from verify_shared_source_noise import (
    audit_derivative,
    independent_joint_curvature,
    independent_tensor,
)
from verify_slice_noise_recovery import direct_slices


def rational_matrix(rows):
    return fmpq_mat([[str(x) for x in row] for row in rows])


def compatible_perturbation(records, saved):
    """Perturb the actual common covariance and all free mean parameters."""
    means = [
        [[F(x) for x in row] for row in mu]
        for mu in saved["alignment_certificate"]["aligned_mean_vectors"]
    ]
    edges = alignment.parse_source(records[0])[1]
    n = len(means[0])
    step, rng = F(1, 2**62), random.Random(275410)
    changed_means = []
    for s, mu in enumerate(means):
        changed_means.append(
            [
                [
                    x + (step * rng.choice([-1, 1]) if s or i == n - 1 or a else 0)
                    for a, x in enumerate(row)
                ]
                for i, row in enumerate(mu)
            ]
        )
    changed_edges = {
        e: [[x + step * rng.choice([-1, 1]) for x in row] for row in block]
        for e, block in edges.items()
    }
    errors = []
    for mu, record in zip(changed_means, records):
        values = independent_tensor(mu, changed_edges, tuple(range(n)))
        error2 = sum(
            (value - F(int(y), int(record["observed_denominator"]))) ** 2
            for value, y in zip(values, record["observed_numerators"])
        )
        budget2 = F(record["error_budget"]) ** 2
        assert error2 <= budget2
        errors.append(
            {"squared_tensor_error": str(error2), "squared_budget": str(budget2)}
        )
    source_error2 = sum(
        (x - y) ** 2
        for before, after in zip(means, changed_means)
        for row, changed in zip(before, after)
        for x, y in zip(row, changed)
    )
    source_error2 += sum(
        (block[a][b] - changed_edges[e][a][b]) ** 2
        for e, block in edges.items()
        for a, b in itertools.product(range(3), repeat=2)
    )
    assert (
        0
        < source_error2
        <= F(saved["joint_local_certificate"]["refined_global_joint_error_bound"]) ** 2
    )
    matrix = rational_matrix(
        list(map(list, zip(*[[x for row in mu for x in row] for mu in means])))
    )
    changed_matrix = rational_matrix(
        list(map(list, zip(*[[x for row in mu for x in row] for mu in changed_means])))
    )
    assert matrix.rank() == changed_matrix.rank() == 4
    projection = matrix * (matrix.transpose() * matrix).inv() * matrix.transpose()
    changed_projection = (
        changed_matrix
        * (changed_matrix.transpose() * changed_matrix).inv()
        * changed_matrix.transpose()
    )
    overlap = projection * changed_projection
    sine2 = F(4) - sum(F(str(overlap[i, i])) for i in range(3 * n))
    assert (
        0
        < sine2
        <= F(saved["refined_mean_span"]["largest_principal_angle_sine_bound"]) ** 2
    )
    return {
        "perturbation_step": str(step),
        "one_distinct_shared_source_fits_all_four_budgets": True,
        "per_observation_errors": errors,
        "actual_joint_source_error_squared": str(source_error2),
        "actual_principal_angle_sines_frobenius_squared": str(sine2),
        "source_error_and_nonzero_subspace_error_within_certified_bounds": True,
        "scope": "One exact nonzero-error model test; not a proof of the universal bounds.",
    }


def run():
    root = Path(__file__).parent
    path = root / "composed-shared-source-certificate.json"
    saved = json.loads(path.read_text())
    records, paths = [], []
    for entry in saved["observations"]:
        current = root / entry["file"]
        assert hashlib.sha256(current.read_bytes()).hexdigest() == entry["sha256"]
        records.append(json.loads(current.read_text()))
        paths.append(current)

    def forbidden(*args, **kwargs):
        raise AssertionError("Replay attempted a numerical proposal")

    bounds.ExactExterior = DirectExterior
    storage.slices = direct_slices
    bounds.eigh = storage.eigh = storage.solve = storage.svd = refined.solve = forbidden
    original.propose_source = original.anchor_proposal = forbidden
    saved_bound, saved_point = bounds.matrix_bound, bounds.point_systems
    all_comparisons = []
    common_edges = None
    for setting, record in enumerate(records):
        print(f"Replaying composed observation {setting}", file=sys.stderr, flush=True)
        mu, edges, _, _ = alignment.parse_source(record)
        n = len(mu)
        comparison = record["comparison_only"]
        if setting:
            physical_mu = [[F(x) for x in row] for row in comparison["actual_means"]]
            physical_edges = {
                tuple(entry["sites"]): [[F(x) for x in row] for row in entry["weights"]]
                for entry in comparison["actual_edges"]
            }
            _, inverses = chart.coordinate_changes(mu)
            changed_edges = {
                (i, j): (
                    inverses[i] @ np.array(block, dtype=object) @ inverses[j].T
                ).tolist()
                for (i, j), block in edges.items()
            }
        else:
            physical_mu, physical_edges, changed_edges = mu, edges, edges
        if common_edges is None:
            common_edges = physical_edges
        assert physical_edges == common_edges
        clean = independent_tensor(physical_mu, physical_edges, tuple(range(n)))
        assert list(clean) == [
            F(int(x), comparison["clean_denominator"])
            for x in comparison["clean_numerators"]
        ]
        observed, denominator = (
            list(map(int, record["observed_numerators"])),
            int(record["observed_denominator"]),
        )
        errors = [F(y, denominator) - x for x, y in zip(clean, observed)]
        assert errors == [
            F(x, int(comparison["noise_denominator"]))
            for x in comparison["noise_numerators"]
        ]
        assert sum(x * x for x in errors) <= F(record["error_budget"]) ** 2
        assert all(F(float(F(y, denominator))) == F(y, denominator) for y in observed)
        assert all(
            float(F(y, denominator)) != float(x) for x, y in zip(clean, observed)
        )
        tensor, tensor_denominator = original.unit_mean_tensor(changed_edges, n)
        unit_clean = independent_tensor(
            [[F(1), F(0), F(0)] for _ in range(n)], changed_edges, tuple(range(n))
        )
        assert all(
            F(int(x), tensor_denominator) == y
            for x, y in zip(tensor.reshape(-1), unit_clean)
        )
        captured = {}

        def audited_bound(
            matrix,
            proposal=None,
            current_edges=changed_edges,
            current_tensor=tensor,
            current_den=tensor_denominator,
            current_n=n,
        ):
            if matrix[0].ncols() == 2 * current_n + 1 + 9 * len(current_edges):
                check_local_jacobian(*matrix, current_edges, current_n)
            elif matrix[0].ncols() == 2 * current_n:
                check_compression_jacobian(*matrix, current_tensor, current_den)
            return saved_bound(matrix, proposal)

        def capture_point(*args, _captured=captured, **kwargs):
            _captured["point"] = saved_point(*args, **kwargs)
            return _captured["point"]

        bounds.matrix_bound, bounds.point_systems = audited_bound, capture_point
        base_path = root / record["baseline_certificate"]["file"]
        assert (
            hashlib.sha256(base_path.read_bytes()).hexdigest()
            == record["baseline_certificate"]["sha256"]
        )
        baseline = json.loads(base_path.read_text())
        if setting:
            rebuilt = shared.certify_chart(
                observed,
                denominator,
                F(record["error_budget"]),
                mu,
                edges,
                baseline,
                record["chart_certificate"],
            )
            assert rebuilt == record["chart_certificate"]
            unit = rebuilt["unit_certificate"]
        else:
            unit = composed.certify(
                observed,
                denominator,
                F(record["error_budget"]),
                mu,
                edges,
                baseline,
                record["certificate"]["composed_constants"],
            )
            assert unit == record["certificate"]
        hessian2, third2 = independent_refined_curvature(changed_edges, n)
        assert hessian2 == F(
            unit["refined_local_certificate"]["point_hessian_frobenius_squared"]
        )
        assert third2 == F(
            unit["refined_local_certificate"][
                "third_derivative_squared_bound_on_unit_ball"
            ]
        )
        symbolic = symbolic_calibration_audit(captured["point"]["coordinates"])
        all_comparisons.append(
            {
                "observation": setting,
                "visible_noisy_entries": len(observed),
                "all_noisy_entries_exactly_binary64": True,
                "independent_point_curvature_checks": True,
                "symbolic_calibration_audit": symbolic,
            }
        )

    bounds.matrix_bound, bounds.point_systems = saved_bound, saved_point
    print(
        "Checking shared derivative, alignment, curvature and distinct compatible source",
        file=sys.stderr,
        flush=True,
    )
    rebuilt = shared.finish(
        records, paths, saved["joint_local_certificate"], audit=audit_derivative
    )
    assert rebuilt == saved
    means, edges, _ = alignment.align(records)
    assert independent_joint_curvature(means, edges) == F(
        saved["joint_local_certificate"]["curvature_squared_bound"]
    )
    reference = alignment.parse_source(records[0])
    invalid = (
        *reference[:3],
        max(abs(x) for block in reference[1].values() for row in block for x in row),
    )
    try:
        alignment.alignment_discs(invalid, alignment.parse_source(records[1]))
    except AssertionError:
        pass
    else:
        raise AssertionError("Zero-containing alignment denominator accepted")
    return {
        "observation_audits": all_comparisons,
        "one_covariance_for_all_comparison_sources_checked": True,
        "all_four_source_certificates_replayed_with_numerical_proposals_disabled": True,
        "all_alignment_and_larger_radius_trials_replayed": True,
        "all_joint_derivative_entries_and_curvature_checked_separately": True,
        "zero_containing_alignment_denominator_rejected": True,
        "distinct_compatible_source_check": compatible_perturbation(records, saved),
        "scope": "Exact replay with separate constructions and a nonzero-error shared-model test. Shares bound propagation and exact arithmetic libraries with the generator; not an independent proof review or Lean formalization.",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
