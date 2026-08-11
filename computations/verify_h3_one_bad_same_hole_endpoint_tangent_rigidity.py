#!/usr/bin/env python3
"""Complete endpoint-star/direct tangent rigidity on three carrier packets.

Freeze internal q on each f057798 carrier calibration and vary all 162
decorated cells on outer-common or outer-outer physical edges.  Build the
complete 6561-output hafnian Jacobian over Q.  The pure/mixed private-tail
defect has zero derivative on the entire endpoint space, hence in particular
on every full-output-preserving source tangent.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_one_bad_same_hole_internal_repair_reselection.py":
        "1bb3893ca00863752f2deb5a715369647c9a0f351cdef0f2ad0985a18d672452",
    "computations/verify_h3_one_bad_crossed_first_rank_repair_obstruction.py":
        "bc078e9f7dab9f0ffb38375687fc1c7d901c3ba388e8a63c3ab73fcde4ed2872",
    "computations/verify_h3_one_bad_crossed_second_hasse_obstruction.py":
        "a7e4b8e81a4891a3d3c25fdd0216f4be75dfc8fc6152327f847dc32786776b4f",
}
EXPECTED_LEDGER_SHA256 = (
    "5f809461152f463e2937fe7206bbf64b835ce2974abbccbd06e4e66209487b05"
)

VERTICES = tuple(range(8))
COLORS = tuple(range(3))
OUTER = frozenset((5, 6, 7))
PURE = (0,) * 8
MIXED = tuple(map(int, "00000001"))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    base = importlib.import_module(
        "verify_h3_one_bad_common_q_cap_extraction_boundary")
    repair = importlib.import_module(
        "verify_h3_one_bad_same_hole_internal_repair_reselection")
    oo = importlib.import_module(
        "verify_oo_doubly_good_two_anchor_counterguard")
    first = importlib.import_module(
        "verify_h3_one_bad_crossed_first_rank_repair_obstruction")
    second = importlib.import_module(
        "verify_h3_one_bad_crossed_second_hasse_obstruction")

    endpoint_cells = tuple(
        (u, v, a, b)
        for u, v in itertools.combinations(VERTICES, 2)
        if u in OUTER or v in OUTER
        for a, b in itertools.product(COLORS, repeat=2)
    )
    require(len(endpoint_cells) == 162,
            f"the endpoint tangent width changed: {len(endpoint_cells)}")
    coordinate = {cell: index for index, cell in enumerate(endpoint_cells)}
    ra_cell = base.cell(2, 7, 0, 0)
    rc_cell = base.cell(2, 7, 0, 1)
    ra_index, rc_index = coordinate[ra_cell], coordinate[rc_cell]

    expected = {
        "shared_CA": {
            "occupied_rows": 487,
            "jacobian_entries": 594,
            "nonzero_columns": 135,
            "rank": 133,
            "kernel_dimension": 29,
        },
        "middle_AT_right": {
            "occupied_rows": 458,
            "jacobian_entries": 549,
            "nonzero_columns": 153,
            "rank": 151,
            "kernel_dimension": 11,
        },
        "middle_AT_left_secondary": {
            "occupied_rows": 574,
            "jacobian_entries": 756,
            "nonzero_columns": 153,
            "rank": 151,
            "kernel_dimension": 11,
        },
    }

    packets = {}
    for name, expected_summary in expected.items():
        source = Counter(repair.common_packets(base.cell)[name])
        source.update(repair.outer_source(base.cell))
        tensor = base.hafnian_tensor(source, VERTICES)
        require(tensor[PURE] == 1 and tensor[MIXED] == -2,
                f"{name} private calibration changed")
        require(source[ra_cell] == 1 and source[rc_cell] == -2,
                f"{name} R_a/R_c normalization changed")

        columns = {
            index: first.derivative_column(oo, source, cell)
            for index, cell in enumerate(endpoint_cells)
        }
        occupied_rows = tuple(sorted(
            set().union(*(set(column) for column in columns.values()))
        ))
        free, kernel = second.jacobian_kernel_basis(
            occupied_rows, columns, len(endpoint_cells))
        summary = {
            "occupied_rows": len(occupied_rows),
            "jacobian_entries": sum(map(len, columns.values())),
            "nonzero_columns": sum(bool(column) for column in columns.values()),
            "rank": len(endpoint_cells) - len(kernel),
            "kernel_dimension": len(kernel),
        }
        require(summary == expected_summary,
                f"{name} Jacobian summary changed: {summary}")
        require(len(free) == len(kernel), f"{name} kernel basis changed")

        # For each endpoint coordinate x, let J0(x),Jm(x) be the derivatives
        # of the two physical private coefficients.  Exactly
        #
        #   2 J0 + Jm = 2 d(ra) + d(rc).
        #
        # This is the differential of their common-tail factorization.
        row_identity = {}
        defect_gradient = {}
        for index in range(len(endpoint_cells)):
            jpure = columns[index].get(PURE, Fraction(0))
            jmixed = columns[index].get(MIXED, Fraction(0))
            lhs = 2 * jpure + jmixed
            rhs = (Fraction(2) if index == ra_index else Fraction(0))
            rhs += (Fraction(1) if index == rc_index else Fraction(0))
            if lhs:
                row_identity[index] = lhs
            require(lhs == rhs,
                    f"{name} private differential row identity failed at "
                    f"{endpoint_cells[index]}: {lhs} != {rhs}")

            # D=ra*F_mixed-rc*F_pure.  At ra=1,rc=-2 and
            # F_pure=1,F_mixed=-2, the exact derivative is zero in every
            # one of the 162 endpoint directions, not only modulo J.
            gradient = (
                (-2 if index == ra_index else 0)
                + jmixed
                - (1 if index == rc_index else 0)
                + 2 * jpure
            )
            if gradient:
                defect_gradient[index] = gradient
        require(row_identity == {ra_index: 2, rc_index: 1},
                f"{name} differential support changed: {row_identity}")
        require(not defect_gradient,
                f"{name} has an endpoint direction breaking the tail: "
                f"{defect_gradient}")

        # A full-output-preserving tangent lies in ker J.  The two selected
        # rows force 2*dra+drc=0 on every exact kernel vector.
        kernel_private_values = tuple(
            2 * vector.get(ra_index, Fraction(0))
            + vector.get(rc_index, Fraction(0))
            for vector in kernel
        )
        require(not any(kernel_private_values),
                f"{name} kernel contains a private-tail breaker")

        packets[name] = {
            **summary,
            "full_output_rows": 3 ** 8,
            "zero_jacobian_rows": 3 ** 8 - len(occupied_rows),
            "endpoint_variables": len(endpoint_cells),
            "private_row_derivative_identity": (
                "2*dF_00000000+dF_00000001=2*dra+drc"
            ),
            "private_defect": "D=ra*F_00000001-rc*F_00000000",
            "private_defect_gradient_rank": 0,
            "kernel_breakers": sum(value != 0
                                   for value in kernel_private_values),
        }

    ledger = {
        "dependencies": PINS,
        "endpoint_variable_scope": {
            "outer_common_cells": 5 * 3 * 9,
            "outer_outer_cells": 3 * 9,
            "total": len(endpoint_cells),
            "internal_q_frozen": True,
        },
        "packets": packets,
        "verdict": (
            "the pure/mixed common-tail defect has zero derivative on the "
            "entire 162-dimensional endpoint-star/direct space for all three "
            "carrier packets; consequently no full-output-preserving source "
            "tangent breaks the private-row unit"
        ),
        "scope": (
            "first-order endpoint-star/direct deformations at the three exact "
            "carrier calibrations with internal q fixed; the calibrations are "
            "not exact GHZ sources, and nonlinear endpoint arcs are not ruled "
            "out by this tangent theorem"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the endpoint tangent ledger changed: {digest}")

    print("h=3 same-hole endpoint tangent rigidity: PASS")
    print("complete Jacobians: 6561 x 162 on three carrier packets")
    print("ranks/kernel dimensions: 133/29, 151/11, 151/11")
    print("private-tail defect gradient: zero on all 162 endpoint directions")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
