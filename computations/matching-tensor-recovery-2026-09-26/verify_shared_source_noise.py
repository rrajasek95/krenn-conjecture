"""Replay global shared-source certificates with separate matching calculations."""

import hashlib
import itertools
import json
import math
import random
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

import covariance_noise_certificate as bounds
import full_source_noise_recovery as single
import numpy as np
import shared_source_alignment as alignment
import shared_source_local_certificate as joint
import slice_noise_recovery as mean_noise
import source_chart_certificate as chart
from alignment_graph_characters import exact_examples
from audit_pair_observation import moments
from blind_mean_search import scalar_bound
from flint import fmpq_mat
from verify_full_source_noise import DirectExterior, check_local_jacobian
from verify_slice_noise_recovery import direct_slices


def independent_tensor(means, edges, sites):
    values = [F(x) for i in sites for x in means[i]]
    values += [
        F(x)
        for (i, j), block in edges.items()
        if i in sites and j in sites
        for row in block
        for x in row
    ]
    scale = math.lcm(*(x.denominator for x in values))
    mu = [[int(F(x) * scale) for x in means[i]] for i in sites]
    cov = {
        (a, b): [[int(F(x) * scale * scale) for x in row] for row in edges[i, j]]
        for a, i in enumerate(sites)
        for b, j in enumerate(sites)
        if a < b
    }
    maximum = scalar_bound(mu, cov)
    integers = moments(mu, cov, 2 * maximum + 1)
    return np.array(
        [
            F(x if x <= maximum else x - 2 * maximum - 1, scale ** len(sites))
            for x in integers
        ],
        dtype=object,
    )


def audit_derivative(means, edges, tensor, derivative, keys):
    n = len(means)

    @lru_cache(None)
    def complementary(sites):
        return independent_tensor(means, edges, sites).reshape((3,) * len(sites))

    assert np.array_equal(tensor, complementary(tuple(range(n))).reshape(-1))
    for j, key in enumerate(keys):
        sites, colours = (
            ([key[1]], [key[2]]) if key[0] == "mu" else (key[1:3], key[3:5])
        )
        expected = np.zeros((3,) * n, dtype=object)
        index = [slice(None)] * n
        for i, colour in zip(sites, colours):
            index[i] = colour
        expected[tuple(index)] = complementary(
            tuple(i for i in range(n) if i not in sites)
        )
        assert np.array_equal(expected.reshape(-1), derivative[:, j])


def independent_joint_curvature(all_means, edges):
    n = len(all_means[0])
    pair_bounds = {
        e: 1 + max(abs(x) for row in b for x in row) for e, b in edges.items()
    }
    answer = F(0)
    for setting, means in enumerate(all_means):
        supports = [
            frozenset([i])
            for i in range(n)
            for a in range(3)
            if setting or i == n - 1 or a
        ]
        supports += [frozenset(e) for e in edges for _ in range(9)]
        counts = Counter(
            tuple(i for i in range(n) if i not in a | b)
            for a in supports
            for b in supports
            if a.isdisjoint(b)
        )
        mono = [1 + max(abs(x) for x in row) for row in means]
        for sites, count in counts.items():
            scalar = F(0)
            for size in range(len(sites) // 2 + 1):
                for matching in itertools.combinations(
                    list(itertools.combinations(sites, 2)), size
                ):
                    used = [i for edge in matching for i in edge]
                    if len(set(used)) == 2 * size:
                        scalar += math.prod(
                            pair_bounds[e] for e in matching
                        ) * math.prod(mono[i] for i in sites if i not in used)
            answer += count * 3 ** len(sites) * scalar**2
    return answer


def encode_source(mu, edges, em, er):
    return {
        "candidate_means": [[str(x) for x in row] for row in mu],
        "candidate_edges": [
            {"sites": list(e), "weights": [[str(x) for x in row] for row in b]}
            for e, b in edges.items()
        ],
        "chart_certificate": {
            "global_mean_error_bound": str(em),
            "global_edge_error_bound": str(er),
        },
    }


def nonzero_error_alignment_checks():
    results = []
    for n in [3, 5, 7, 9]:
        rng = random.Random(275200 + n)
        physical_edges = {
            e: [[F(rng.choice([-2, -1, 1, 2])) for _ in range(3)] for _ in range(3)]
            for e in itertools.combinations(range(n), 2)
        }
        records, true_means, scalings = [], [], []
        for setting in range(4):
            physical_mu = [
                [F(rng.choice([-2, -1, 1, 2])) for _ in range(3)] for _ in range(n)
            ]
            factors = (
                [F(2) ** rng.choice([-1, 0, 1]) for _ in range(n - 1)]
                if setting
                else [F(1)] * (n - 1)
            )
            factors.append(1 / math.prod(factors))
            mu = [[factors[i] * x for x in row] for i, row in enumerate(physical_mu)]
            edges = {
                (i, j): [[factors[i] * factors[j] * x for x in row] for row in b]
                for (i, j), b in physical_edges.items()
            }
            step = F(1, 2**30)
            candidate_mu = [[x + rng.choice([-1, 1]) * step for x in row] for row in mu]
            candidate_edges = {
                e: [[x + rng.choice([-1, 1]) * step for x in row] for row in b]
                for e, b in edges.items()
            }
            em = bounds.upper_sqrt(3 * n) * step
            er = bounds.upper_sqrt(9 * math.comb(n, 2)) * step
            assert (
                sum(
                    (a - b) ** 2
                    for row, crow in zip(mu, candidate_mu)
                    for a, b in zip(row, crow)
                )
                <= em**2
            )
            assert (
                sum(
                    (a - b) ** 2
                    for e in edges
                    for row, crow in zip(edges[e], candidate_edges[e])
                    for a, b in zip(row, crow)
                )
                <= er**2
            )
            records.append(encode_source(candidate_mu, candidate_edges, em, er))
            true_means.append(physical_mu)
            scalings.append(factors)
        proposed, _, report = alignment.align(records)
        for setting, row in enumerate(report["alignment"], 1):
            for i, witness in enumerate(row["scale_witnesses"]):
                assert abs(1 / scalings[setting][i] - F(witness["scale_center"])) <= F(
                    witness["scale_radius"]
                )
        for exact, estimate, error in zip(
            true_means, proposed, report["mean_error_bounds"]
        ):
            assert (
                sum(
                    (a - b) ** 2
                    for row, crow in zip(exact, estimate)
                    for a, b in zip(row, crow)
                )
                <= F(error) ** 2
            )
        actual = fmpq_mat(
            [
                [str(x) for x in row]
                for row in zip(*[[x for site in mu for x in site] for mu in true_means])
            ]
        )
        estimate = fmpq_mat(
            [
                [str(x) for x in row]
                for row in zip(*[[x for site in mu for x in site] for mu in proposed])
            ]
        )
        ga, ge, cross = (
            actual.transpose() * actual,
            estimate.transpose() * estimate,
            estimate.transpose() * actual,
        )
        overlap = ge.inv() * cross * ga.inv() * cross.transpose()
        sine_frobenius_squared = 4 - sum(F(str(overlap[i, i])) for i in range(4))
        assert (
            0
            < sine_frobenius_squared
            <= F(report["mean_span"]["largest_principal_angle_sine_bound"]) ** 2
        )
        results.append(
            {
                "sites": n,
                "independent_parameter_perturbations": True,
                "scale_and_mean_enclosures_checked_exactly": True,
                "nonzero_principal_angle_checked_by_rational_projectors": True,
            }
        )
    return results


def run():
    root = Path(__file__).parent
    saved = json.loads((root / "shared-source-noise-certificate.json").read_text())
    records = []
    for entry in saved["observations"]:
        path = root / entry["file"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"]
        records.append(json.loads(path.read_text()))
    bounds.ExactExterior = DirectExterior
    mean_noise.slices = direct_slices

    def forbidden(*args, **kwargs):
        raise AssertionError("Audit attempted a numerical proposal")

    bounds.eigh = mean_noise.eigh = mean_noise.solve = mean_noise.svd = forbidden
    single.propose_source = single.anchor_proposal = forbidden
    matrix_bound = bounds.matrix_bound
    shared_edges = None
    for setting, record in enumerate(records):
        mu, edges, _, _ = alignment.parse_source(record)
        if setting:
            physical_mu = [
                [F(x) for x in row] for row in record["comparison_only"]["actual_means"]
            ]
            physical_edges = {
                tuple(e["sites"]): [[F(x) for x in row] for row in e["weights"]]
                for e in record["comparison_only"]["actual_edges"]
            }
            _, inverses = chart.coordinate_changes(mu)
            transformed_edges = {
                (i, j): (
                    inverses[i] @ np.array(block, dtype=object) @ inverses[j].T
                ).tolist()
                for (i, j), block in edges.items()
            }
        else:
            physical_mu, physical_edges, transformed_edges = mu, edges, edges
        if shared_edges is None:
            shared_edges = physical_edges
        assert physical_edges == shared_edges
        clean = independent_tensor(
            physical_mu, physical_edges, tuple(range(record["sites"]))
        )
        comparison = record["comparison_only"]
        assert list(clean) == [
            F(x, comparison["clean_denominator"])
            for x in comparison["clean_numerators"]
        ]
        observed = [int(x) for x in record["observed_numerators"]]
        denominator = int(record["observed_denominator"])
        errors = [F(y, denominator) - x for x, y in zip(clean, observed)]
        assert errors == [
            F(x, int(comparison["noise_denominator"]))
            for x in comparison["noise_numerators"]
        ]
        assert sum(x * x for x in errors) <= F(record["error_budget"]) ** 2

        def audited_bound(matrix, proposal=None, current_edges=transformed_edges):
            if matrix[0].ncols() == 204:
                check_local_jacobian(*matrix, current_edges, 7)
            return matrix_bound(matrix, proposal)

        bounds.matrix_bound = audited_bound
        if setting:
            rebuilt = chart.certify(
                observed,
                denominator,
                F(record["error_budget"]),
                mu,
                edges,
                record["chart_certificate"],
            )
            assert rebuilt == record["chart_certificate"]
        else:
            c = record["certificate"]
            rebuilt = single.certify(
                observed,
                denominator,
                F(record["error_budget"]),
                mu,
                edges,
                7,
                c["anchor_proposal"],
                c["covariance_matrix_certificates"],
                c["local_certificate"]["matrix_certificate"]["preconditioner"],
            )
            assert rebuilt == c
    bounds.matrix_bound = matrix_bound
    means, edges, report = alignment.align(records)
    assert report == saved["certificate"]
    local = joint.certify(
        means,
        edges,
        records,
        report["joint_source_error_bound"],
        saved["joint_local_certificate"],
        audit=audit_derivative,
    )
    assert local == saved["joint_local_certificate"]
    assert independent_joint_curvature(means, edges) == F(
        local["curvature_squared_bound"]
    )
    matrix = list(map(list, zip(*[[x for row in mu for x in row] for mu in means])))
    assert (
        alignment.full_column_span(matrix, F(local["refined_global_joint_error_bound"]))
        == saved["refined_mean_span"]
    )
    assert exact_examples() == saved["graph_character_certificates"]
    reference = alignment.parse_source(records[0])
    invalid_reference = (
        *reference[:3],
        max(abs(x) for block in reference[1].values() for row in block for x in row),
    )
    try:
        alignment.alignment_discs(invalid_reference, alignment.parse_source(records[1]))
    except AssertionError:
        pass
    else:
        raise AssertionError("Reference denominators containing zero were not rejected")
    return {
        "all_four_input_certificates_replayed_without_numerical_proposals": True,
        "every_clean_tensor_and_noise_entry_checked_separately": True,
        "one_shared_covariance_for_all_four_comparison_sources_checked": True,
        "every_single_source_local_derivative_checked_separately": True,
        "every_joint_derivative_entry_checked_separately": True,
        "joint_curvature_checked_by_matching_and_support_enumeration": True,
        "all_scalar_alignment_discs_and_span_bounds_replayed": True,
        "zero_containing_reference_denominators_rejected": True,
        "nonzero_parameter_error_checks": nonzero_error_alignment_checks(),
        "scope": "Exact replay with separate matching, derivative and curvature construction plus nonzero perturbation tests. Shares acceptance code and exact arithmetic libraries; not an independent mathematical proof review.",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
