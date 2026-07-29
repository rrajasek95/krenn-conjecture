#!/usr/bin/env python3
"""Exact direct-free unit-minor certificates on eight ordered cells."""

from __future__ import annotations

import sympy as sp

import explore_live_three_zero_minimal_two_extra_boundary as boundary
import explore_live_three_zero_minimal_two_extra_response as response
from explore_live_three_zero_minimal_three_extra_ccb import singular_status


CELLS = ("CB", "BC", "CE", "EC", "BB", "BE", "EB", "EE")
MODULAR_POINTS = {
    "CB": (),
    "BC": (
        (17, (0, 0, 15)),
        (17, (0, 0, 16)),
        (17, (3, 0, 15)),
        (17, (8, 0, 16)),
    ),
    "CE": ((17, (0, 14)),),
    "EC": ((17, (0, 14)),),
    "BB": ((17, (0, 8)), (17, (8, 0))),
    "BE": (),
    "EB": (),
    "EE": (),
}


def assert_cell(cell):
    _charts, _substitutions, _free_names, variables = (
        boundary.cell_data(cell)
    )
    polynomials = list(boundary.base_supports(cell))
    for prime, point in MODULAR_POINTS[cell]:
        full = boundary.modular_full_point(cell, point, prime)
        labels = boundary.labels_at(
            cell, full, prime=prime, raw_modular=True
        )
        assert all(label[1:] != (0, 1) for label in labels)
        polynomial = boundary.exact_support(cell, labels)
        if polynomial not in polynomials:
            polynomials.append(polynomial)

    if not variables:
        assert polynomials == [sp.S.One]
    else:
        status = singular_status(polynomials, variables)
        assert "UNIT" in status and "NONUNIT" not in status, (
            cell, status
        )
    print(cell, "PASS", flush=True)


def main():
    try:
        for cell in CELLS:
            assert_cell(cell)
    finally:
        response.PRIME = boundary.DEFAULT_PRIME
    print("minimal two-extra boundary: PASS")
    print("all eight ordered noncentral cells exact over QQ")
    print("all selected rows direct-free; arbitrary B_01 scale allowed")


if __name__ == "__main__":
    main()
