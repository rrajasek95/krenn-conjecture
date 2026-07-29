#!/usr/bin/env python3
"""Exact direct-free unit-minor certificates on CCE, CEC, and ECC."""

from __future__ import annotations

import explore_live_three_zero_minimal_three_extra_remaining_cells as explore
import explore_live_three_zero_minimal_three_extra_response as response
import verify_live_three_zero_minimal_three_extra_boundary_low_cells as low


DEFAULT_PRIME = 1_000_003

COMMON_MODULAR_POINTS = (
    (17, (0, 1, 0, 2)),
    (17, (0, 5, 0, 14)),
    (17, (0, 7, 0, 16)),
    (17, (0, 14, 0, 5)),
    (17, (0, 14, 0, 14)),
    (17, (0, 14, 0, 16)),
    (17, (0, 14, 4, 16)),
    (17, (0, 14, 15, 0)),
    (17, (0, 15, 0, 16)),
)

MODULAR_POINTS = {
    "CCE": COMMON_MODULAR_POINTS + (
        (17, (0, 16, 0, 16)),
        (17, (1, 14, 2, 16)),
        (17, (4, 0, 0, 14)),
        (17, (5, 7, 0, 16)),
        (17, (5, 14, 0, 14)),
        (17, (15, 0, 0, 14)),
        (17, (15, 0, 0, 16)),
        (17, (15, 16, 0, 16)),
        (19, (0, 6, 0, 10)),
        (23, (4, 20, 4, 20)),
        (23, (4, 20, 4, 22)),
        (23, (4, 22, 4, 22)),
    ),
    "CEC": COMMON_MODULAR_POINTS + (
        (17, (0, 16, 0, 16)),
        (17, (1, 14, 2, 16)),
        (17, (4, 0, 0, 14)),
        (17, (5, 7, 0, 16)),
        (17, (5, 14, 0, 14)),
        (17, (15, 0, 0, 14)),
        (17, (15, 0, 0, 16)),
        (17, (15, 16, 0, 16)),
        (19, (0, 6, 0, 10)),
        (23, (4, 20, 4, 20)),
        (23, (4, 20, 4, 22)),
        (23, (4, 22, 4, 22)),
    ),
    "ECC": COMMON_MODULAR_POINTS + (
        (17, (0, 16, 0, 7)),
        (17, (0, 16, 0, 14)),
        (17, (0, 16, 0, 15)),
        (17, (0, 16, 0, 16)),
        (17, (1, 14, 2, 16)),
        (17, (5, 7, 0, 16)),
        (17, (15, 0, 0, 14)),
        (17, (15, 0, 0, 16)),
        (17, (15, 16, 0, 16)),
        (19, (0, 6, 0, 10)),
        (23, (4, 20, 4, 22)),
        (23, (4, 22, 4, 20)),
        (23, (4, 22, 4, 22)),
    ),
}


def assert_cell(cell):
    _charts, _substitutions, _indices, variables = low.cell_data(cell)
    polynomials = []
    for point in explore.FOUR_POINTS:
        polynomial = explore.selected_support(cell, point)
        if polynomial not in polynomials:
            polynomials.append(polynomial)
    for prime, point in MODULAR_POINTS[cell]:
        polynomial = explore.selected_support(
            cell, point, prime=prime, raw_modular=True
        )
        if polynomial not in polynomials:
            polynomials.append(polynomial)
    status = explore.singular_unit(polynomials, variables)
    assert "UNIT" in status and "NONUNIT" not in status, (cell, status)
    print(cell, "PASS", flush=True)


def main():
    try:
        for cell in ("CCE", "CEC", "ECC"):
            assert_cell(cell)
    finally:
        response.PRIME = DEFAULT_PRIME

    print("minimal three-extra CCE orbit: PASS")
    print("CCE, CEC, ECC: exact unit ideals over QQ")
    print("all selected rows direct-free; arbitrary B_01 scale allowed")


if __name__ == "__main__":
    main()
