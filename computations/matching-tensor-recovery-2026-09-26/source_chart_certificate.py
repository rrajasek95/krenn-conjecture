"""Reduce a rational candidate with nonzero first mean coordinates to unit means.

The coordinate changes are determined by the candidate, not a hidden source.
All norm amplification and the return to original coordinates are certified.
"""

import math
from fractions import Fraction as F

import covariance_noise_certificate as bounds
import full_source_noise_recovery as unit
import numpy as np
from blind_mean_search import contract, integer_tensor


def rational_tensor(means, edges):
    entries = [F(x) for row in means for x in row]
    entries += [F(x) for block in edges.values() for row in block for x in row]
    scale = math.lcm(*(x.denominator for x in entries))
    integers_mu = [[int(F(x) * scale) for x in row] for row in means]
    integers_r = {
        e: [[int(F(x) * scale * scale) for x in row] for row in block]
        for e, block in edges.items()
    }
    return integer_tensor(integers_mu, integers_r), scale ** len(means)


def norm_bound(matrix):
    rows = [[F(x) for x in row] for row in matrix]
    one = max(
        sum(abs(rows[i][j]) for i in range(len(rows))) for j in range(len(rows[0]))
    )
    infinity = max(sum(abs(x) for x in row) for row in rows)
    return bounds.upper_sqrt(one * infinity)


def coordinate_changes(means):
    bases, inverses = [], []
    for mean in means:
        a, b, c = map(F, mean)
        assert a
        bases.append(np.array([[a, 0, 0], [b, 1, 0], [c, 0, 1]], dtype=object))
        inverses.append(
            np.array([[1 / a, 0, 0], [-b / a, 1, 0], [-c / a, 0, 1]], dtype=object)
        )
        assert np.array_equal(bases[-1] @ inverses[-1], np.eye(3, dtype=int))
    return bases, inverses


def certify(observed, denominator, epsilon, means, edges, saved=None):
    n = len(means)
    assert len(observed) == 3**n and F(epsilon) >= 0
    bases, inverses = coordinate_changes(means)
    tensor = np.array([F(int(x), denominator) for x in observed], dtype=object).reshape(
        (3,) * n
    )
    changed = contract(tensor, inverses).reshape(-1)
    changed_integers, changed_denominator = bounds.common(changed)
    changed_edges = {
        (i, j): (inverses[i] @ np.array(block, dtype=object) @ inverses[j].T).tolist()
        for (i, j), block in edges.items()
    }
    inverse_norms = [norm_bound(matrix) for matrix in inverses]
    data_gain = math.prod(inverse_norms)
    unit_record = unit.certify(
        changed_integers,
        changed_denominator,
        F(epsilon) * data_gain,
        [[F(1), F(0), F(0)] for _ in range(n)],
        changed_edges,
        n,
        None if saved is None else saved["unit_certificate"]["anchor_proposal"],
        None
        if saved is None
        else saved["unit_certificate"]["covariance_matrix_certificates"],
        None
        if saved is None
        else saved["unit_certificate"]["local_certificate"]["matrix_certificate"][
            "preconditioner"
        ],
    )
    basis_norms = [norm_bound(matrix) for matrix in bases]
    mean_gain = max(basis_norms)
    edge_gain = max(basis_norms[i] * basis_norms[j] for i, j in edges)
    source_gain = max(mean_gain, edge_gain)
    unit_error = F(unit_record["global_canonical_source_error_bound"])
    return {
        "unit_certificate": unit_record,
        "data_norm_amplification_bound": str(data_gain),
        "mean_return_norm_bound": str(mean_gain),
        "edge_return_norm_bound": str(edge_gain),
        "global_mean_error_bound": str(mean_gain * unit_error),
        "global_edge_error_bound": str(edge_gain * unit_error),
        "global_total_source_error_bound": str(source_gain * unit_error),
        "gauge": "At each site except the last, the true first mean coordinate equals that of this candidate. This is a product-one scaling gauge, in the original measurement coordinates.",
    }
