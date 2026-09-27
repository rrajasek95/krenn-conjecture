"""Exact disc bounds for aligning independently certified source representatives.

The input error bounds must already cover all compatible single-output sources.
This routine proves a conditional shared-source enclosure; it does not test
whether a common source exists.
"""

import itertools
from fractions import Fraction as F

from covariance_noise_certificate import ScalarBall, length, upper_sqrt
from flint import fmpq_mat


def parse_source(record):
    means = [[F(x) for x in row] for row in record["candidate_means"]]
    edges = {
        tuple(edge["sites"]): [[F(x) for x in row] for row in edge["weights"]]
        for edge in record["candidate_edges"]
    }
    if "chart_certificate" in record:
        certificate = record["chart_certificate"]
        mean_error = F(certificate["global_mean_error_bound"])
        edge_error = F(certificate["global_edge_error_bound"])
    else:
        mean_error = edge_error = F(
            record["certificate"]["global_canonical_source_error_bound"]
        )
    return means, edges, mean_error, edge_error


def perfect_matchings(sites, edges):
    if not sites:
        yield []
        return
    i, *rest = sites
    for j in rest:
        edge = tuple(sorted((i, j)))
        if edge in edges:
            for tail in perfect_matchings([k for k in rest if k != j], edges):
                yield [edge] + tail


def alignment_discs(reference, other):
    _, ref_edges, _, ref_error = reference
    _, edges, _, error = other
    n = len(reference[0])
    ratios, coordinates = {}, {}
    for edge, block in ref_edges.items():
        a, b = max(
            itertools.product(range(3), repeat=2),
            key=lambda ab: abs(block[ab[0]][ab[1]]),
        )
        if abs(block[a][b]) <= ref_error:
            continue
        ratios[edge] = ScalarBall(edges[edge][a][b], error) / ScalarBall(
            block[a][b], ref_error
        )
        coordinates[edge] = [a, b]
    result, witnesses = [], []
    for i in range(n):
        proposals = []
        for matching in perfect_matchings([j for j in range(n) if j != i], ratios):
            ball = ScalarBall(1)
            for edge in matching:
                ball *= ratios[edge]
            proposals.append((ball, matching))
        assert proposals, (
            "The certified reference graph has no matching after this vertex deletion"
        )
        ball, matching = min(proposals, key=lambda pair: pair[0].radius)
        result.append(ball)
        witnesses.append(
            {
                "site": i,
                "matching": [list(edge) for edge in matching],
                "coordinates": [coordinates[edge] for edge in matching],
                "scale_center": str(ball.center),
                "scale_radius": str(ball.radius),
            }
        )
    return result, witnesses


def full_column_span(matrix, error):
    rows = [[F(x) for x in row] for row in matrix]
    value = fmpq_mat([[str(x) for x in row] for row in rows])
    gram = value.transpose() * value
    inverse = gram.inv()
    trace = sum(F(str(inverse[i, i])) for i in range(inverse.nrows()))
    lower = 1 / upper_sqrt(trace)
    assert error < lower, "Mean rank is not separated from the error bound"
    return {
        "column_rank": len(rows[0]),
        "gram_inverse_trace": str(trace),
        "candidate_smallest_singular_value_lower": str(lower),
        "mean_matrix_error_bound": str(error),
        "largest_principal_angle_sine_bound": str(error / lower),
    }


def align(records):
    sources = [parse_source(record) for record in records]
    ref = sources[0]
    means, edges, mean_error, edge_error = ref
    aligned = [means]
    mean_errors = [mean_error]
    edge_errors = [edge_error]
    reports = []
    for source in sources[1:]:
        mu, cov, mu_error, cov_error = source
        scalars, witnesses = alignment_discs(ref, source)
        centers = [ball.center for ball in scalars]
        aligned.append([[centers[i] * x for x in row] for i, row in enumerate(mu)])
        error = max(abs(ball.center) + ball.radius for ball in scalars) * mu_error
        error += length([ball.radius * length(row) for ball, row in zip(scalars, mu)])
        mean_errors.append(error)
        pair_discs = {edge: scalars[edge[0]] * scalars[edge[1]] for edge in cov}
        error_r = (
            max(abs(ball.center) + ball.radius for ball in pair_discs.values())
            * cov_error
        )
        error_r += length(
            [
                pair_discs[edge].radius * length(x for row in block for x in row)
                for edge, block in cov.items()
            ]
        )
        edge_errors.append(error_r)
        reports.append(
            {
                "scale_witnesses": witnesses,
                "aligned_mean_error_bound": str(error),
                "aligned_covariance_error_bound": str(error_r),
            }
        )
    mean_radius = length(mean_errors)
    matrix = list(map(list, zip(*[[x for row in mu for x in row] for mu in aligned])))
    total = upper_sqrt(mean_radius**2 + edge_error**2)
    return (
        aligned,
        edges,
        {
            "alignment": reports,
            "aligned_mean_vectors": [
                [[str(x) for x in row] for row in mu] for mu in aligned
            ],
            "mean_error_bounds": list(map(str, mean_errors)),
            "covariance_error_bounds_by_observation": list(map(str, edge_errors)),
            "common_covariance_error_bound": str(edge_error),
            "joint_source_error_bound": str(total),
            "mean_span": full_column_span(matrix, mean_radius),
            "gauge": "One common product-one site scaling, fixed by the first observation's mean gauge. The candidate common covariance is the first observation's candidate covariance.",
        },
    )
