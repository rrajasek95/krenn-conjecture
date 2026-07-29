#!/usr/bin/env python3
"""Exact direct-free branch certificate on the central two-extra cell."""

from __future__ import annotations

import explore_live_three_zero_minimal_two_extra_central as central
import explore_live_three_zero_minimal_two_extra_response as response
from explore_live_three_zero_minimal_three_extra_ccb import singular_status


MODULAR_POINTS = {
    "a0": (
        (17, (1, 0, 2)),
        (17, (7, 0, 16)),
        (17, (9, 0, 15)),
        (17, (14, 1, 16)),
        (17, (14, 15, 15)),
        (17, (15, 0, 9)),
        (17, (15, 0, 15)),
        (17, (15, 0, 16)),
        (17, (16, 0, 7)),
        (17, (16, 0, 15)),
        (17, (16, 0, 16)),
        (17, (16, 15, 0)),
    ),
    "c0": (
        (17, (0, 1, 2)),
        (17, (0, 7, 16)),
        (17, (0, 15, 9)),
        (17, (0, 15, 15)),
        (17, (0, 15, 16)),
        (17, (0, 16, 7)),
        (17, (0, 16, 16)),
        (17, (15, 0, 16)),
        (17, (15, 15, 14)),
    ),
    "bd": (
        (17, (1, 16, 2)),
        (23, (0, 4, 0)),
        (23, (4, 22, 4)),
    ),
    "Q": (
        (17, (1, 14, 16)),
        (17, (15, 0, 14)),
        (17, (15, 0, 16)),
    ),
}


def assert_branch(branch):
    variables, _substitutions, _full, localizer = (
        central.branch_data(branch)
    )
    polynomials = list(central.branch_supports(branch))
    for prime, point in MODULAR_POINTS[branch]:
        full_point = central.modular_full_point(
            branch, point, prime
        )
        labels = central.labels_at(
            full_point, prime=prime, raw_modular=True
        )
        assert all(label[1:] != (0, 1) for label in labels)
        polynomial = central.restricted_support(labels, branch)
        if polynomial not in polynomials:
            polynomials.append(polynomial)
    status = singular_status(
        polynomials, variables, localizer=localizer
    )
    assert "UNIT" in status and "NONUNIT" not in status, (
        branch, status
    )
    print(branch, "PASS", flush=True)


def main():
    try:
        for branch in ("a0", "c0", "bd", "Q"):
            assert_branch(branch)
    finally:
        response.PRIME = central.DEFAULT_PRIME
    print("minimal two-extra central 01x01 cell: PASS")
    print("rank 20 everywhere; all selected rows direct-free")
    print("finite-field points select labels only; all ideals over QQ")


if __name__ == "__main__":
    main()
