#!/usr/bin/env python3
"""Exact replay with separate exterior assembly and matching checks.

Shares the acceptance inequalities with the generator. Numerical proposal
functions are disabled; no floating eigenvalue is accepted as evidence.
"""

import itertools
import json
import math
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

import covariance_noise_certificate as bounds
import full_source_noise_recovery as source
import numpy as np
import slice_noise_recovery as mean_noise
from audit_pair_observation import moments
from blind_mean_search import scalar_bound
from verify_slice_noise_recovery import direct_slices


class DirectExterior(bounds.ExactExterior):
    def column(self, index):
        if index not in self.cache:
            b = index // self.powers % 3
            other = np.array([[1, 2], [0, 2], [0, 1]])
            a = other[b, self.bits]
            third = 3 - a - b
            signs = np.array([[0, 1, -1], [-1, 0, 1], [1, -1, 0]])
            coefficient = np.prod(signs[a, b], axis=1)
            self.cache[index] = (
                a @ self.powers,
                coefficient * self.tensor[third @ self.powers],
            )
        return self.cache[index]


def matching_multiplicities(n):
    powers = [3**i for i in reversed(range(n))]
    edges = list(itertools.combinations(range(n), 2))
    report = []
    for count in range(1, n // 2 + 1):
        values = [0] * (3**n)
        for matching in itertools.combinations(edges, count):
            sites = sorted(i for e in matching for i in e)
            if len(set(sites)) != 2 * count:
                continue
            for colours in itertools.product(range(3), repeat=2 * count):
                code = sum(a * powers[i] for i, a in zip(sites, colours))
                values[code] += math.factorial(count)
        ordered_pairings = math.factorial(2 * count) // 2**count
        for code, value in enumerate(values):
            outside = sum(code // p % 3 != 0 for p in powers)
            expected = (
                ordered_pairings * math.comb(n - outside, 2 * count - outside)
                if outside <= 2 * count
                else 0
            )
            assert value == expected
        assert max(values) == ordered_pairings * math.comb(n, 2 * count)
        report.append(
            {
                "edge_factors": count,
                "maximum_row_multiplicity": max(values),
                "all_tensor_rows_checked": True,
            }
        )
    return report


def independent_moment(edges, n, sites):
    denominator = math.lcm(
        *(F(x).denominator for block in edges.values() for row in block for x in row)
    )
    root = math.isqrt(denominator)
    scale = root if root * root == denominator else denominator
    means = [[scale, 0, 0] for _ in sites]
    blocks = {
        (a, b): [[int(scale * scale * x) for x in row] for row in edges[i, j]]
        for a, i in enumerate(sites)
        for b, j in enumerate(sites)
        if a < b
    }
    bound = scalar_bound(means, blocks)
    values = moments(means, blocks, 2 * bound + 1)
    return [
        F(x if x <= bound else x - 2 * bound - 1, scale ** len(sites)) for x in values
    ]


def check_local_jacobian(matrix, denominator, edges, n):
    keys = [("mu", i, a) for i in range(n) for a in range(3) if i == n - 1 or a != 0]
    keys += [
        ("R", i, j, a, b)
        for i, j in edges
        for a, b in itertools.product(range(3), repeat=2)
    ]

    @lru_cache(None)
    def complement(sites):
        return np.asarray(independent_moment(edges, n, sites), dtype=object).reshape(
            (3,) * len(sites)
        )

    assert matrix.ncols() == len(keys)
    for j, key in enumerate(keys):
        sites, colours = (
            ([key[1]], [key[2]]) if key[0] == "mu" else (key[1:3], key[3:5])
        )
        expected = np.zeros((3,) * n, dtype=object)
        index = [slice(None)] * n
        for i, colour in zip(sites, colours):
            index[i] = colour
        expected[tuple(index)] = complement(
            tuple(i for i in range(n) if i not in sites)
        )
        assert all(
            F(int(matrix[i, j]), denominator) == x
            for i, x in enumerate(expected.reshape(-1))
        )


def independent_curvature(edges, n):
    supports = [
        frozenset([i]) for i in range(n) for a in range(3) if i == n - 1 or a != 0
    ]
    supports += [frozenset(e) for e in edges for _ in range(9)]
    multiplicity = Counter(
        tuple(i for i in range(n) if i not in a | b)
        for a in supports
        for b in supports
        if a.isdisjoint(b)
    )
    edge_bounds = {
        e: 1 + max(abs(x) for row in block for x in row) for e, block in edges.items()
    }
    total = F(0)
    for sites, count in multiplicity.items():
        h = F(0)
        for number in range(len(sites) // 2 + 1):
            for matching in itertools.combinations(
                list(itertools.combinations(sites, 2)), number
            ):
                used = [i for edge in matching for i in edge]
                if len(set(used)) == 2 * number:
                    h += 2 ** (len(sites) - 2 * number) * math.prod(
                        edge_bounds[e] for e in matching
                    )
        total += count * 3 ** len(sites) * h * h
    return total


def run():
    saved = json.loads(
        Path(__file__).with_name("full-source-noise-certificate.json").read_text()
    )
    n = saved["sites"]
    observed = [int(x) for x in saved["observed_numerators"]]
    denominator = int(saved["observed_denominator"])
    edges = {
        tuple(e["sites"]): [[F(x) for x in row] for row in e["weights"]]
        for e in saved["candidate_edges"]
    }
    means = [[F(x) for x in row] for row in saved["candidate_means"]]
    comparison = saved["comparison_only"]
    clean = independent_moment(edges, n, tuple(range(n)))
    assert clean == [
        F(x, comparison["clean_denominator"]) for x in comparison["clean_numerators"]
    ]
    assert [F(y, denominator) - x for x, y in zip(clean, observed)] == [
        F(x, int(comparison["noise_denominator"]))
        for x in comparison["noise_numerators"]
    ]
    assert (
        sum((F(y, denominator) - x) ** 2 for x, y in zip(clean, observed))
        <= F(saved["error_budget"]) ** 2
    )
    original_bound = bounds.matrix_bound

    def audited_bound(matrix, proposal=None):
        if matrix[0].ncols() == 2 * n + 1 + 9 * math.comb(n, 2):
            check_local_jacobian(*matrix, edges, n)
        return original_bound(matrix, proposal)

    def forbidden(*args, **kwargs):
        raise AssertionError("Replay attempted a numerical proposal")

    bounds.ExactExterior = DirectExterior
    bounds.matrix_bound = audited_bound
    bounds.eigh = mean_noise.eigh = mean_noise.solve = mean_noise.svd = forbidden
    source.propose_source = source.anchor_proposal = forbidden
    mean_noise.slices = direct_slices
    c = saved["certificate"]
    rebuilt = source.certify(
        observed,
        denominator,
        F(saved["error_budget"]),
        means,
        edges,
        n,
        c["anchor_proposal"],
        c["covariance_matrix_certificates"],
        c["local_certificate"]["matrix_certificate"]["preconditioner"],
    )
    assert rebuilt == c
    assert independent_curvature(edges, n) == F(
        c["local_certificate"]["curvature_squared_bound"]
    )
    try:
        bounds.ScalarBall(1, 1).inverse()
    except AssertionError:
        rejected = True
    else:
        raise AssertionError("A zero-containing calibration denominator was accepted")
    return {
        "sites": n,
        "every_clean_entry_rebuilt_by_scalar_matchings": True,
        "exact_measurement_error_checked": True,
        "exterior_columns_rebuilt_separately": True,
        "every_local_jacobian_entry_checked_separately": True,
        "curvature_checked_by_matching_enumeration_and_parameter_support_counts": True,
        "all_saved_integer_preconditioners_and_fraction_bounds_replayed": True,
        "response_multiplicities": matching_multiplicities(n),
        "zero_containing_denominator_rejected": rejected,
        "scope": "Exact acceptance replay with separate tensor, exterior, derivative and curvature construction. Shares the bound propagation code and integer matrix library; not an independent proof review.",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
