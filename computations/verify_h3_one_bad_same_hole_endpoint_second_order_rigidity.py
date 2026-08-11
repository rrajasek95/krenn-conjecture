#!/usr/bin/env python3
"""Second-order endpoint rigidity on the three same-hole carrier packets.

Restrict the exact endpoint Hasse map to the 29/11/11 full-Jacobian kernels
from bb35c6a.  Only three quadratic kernel monomials per packet have nonzero
full-output Hasse columns, and each has an explicit rational endpoint
correction.  The private defect Hessian is zero on every kernel pair, so no
order-two output-preserving endpoint arc breaks the private-row unit.
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
    "computations/verify_h3_one_bad_same_hole_endpoint_tangent_rigidity.py":
        "c93fab358b25993b51feb250ec2f142ed99d178866af5fc9081fade405859587",
    "computations/verify_h3_one_bad_crossed_second_hasse_obstruction.py":
        "a7e4b8e81a4891a3d3c25fdd0216f4be75dfc8fc6152327f847dc32786776b4f",
}
EXPECTED_LEDGER_SHA256 = (
    "d61dfb5a47967ea8997d994e2067da529956d8f9326970fcd4098cec3e73c7e1"
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


def solve_correction(columns, target, width):
    """Solve J*w=-target with deterministic free variables set to zero."""
    pivots = {}
    rows = tuple(sorted(
        set(target).union(*(set(column) for column in columns.values()))
    ))
    for word in rows:
        row = {
            index: column[word]
            for index, column in columns.items() if word in column
        }
        rhs = -target.get(word, Fraction(0))
        while row:
            pivot = min(row)
            if pivot not in pivots:
                scale = row.pop(pivot)
                pivots[pivot] = (
                    {index: value / scale for index, value in row.items()},
                    rhs / scale,
                )
                break
            scale = row.pop(pivot)
            old_row, old_rhs = pivots[pivot]
            for index, value in old_row.items():
                row[index] = row.get(index, Fraction(0)) - scale * value
                if not row[index]:
                    del row[index]
            rhs -= scale * old_rhs
        else:
            require(not rhs, f"inconsistent Hasse correction at row {word}: {rhs}")

    solution = {}
    for pivot in sorted(pivots, reverse=True):
        row, rhs = pivots[pivot]
        value = rhs - sum(
            coefficient * solution.get(index, Fraction(0))
            for index, coefficient in row.items()
        )
        if value:
            solution[pivot] = value
    require(all(index < width for index in solution),
            "a correction index left the endpoint space")
    return solution


def apply_correction(columns, target, solution):
    residual = Counter(target)
    for index, coefficient in solution.items():
        for word, value in columns[index].items():
            residual[word] += coefficient * value
    return Counter({word: value for word, value in residual.items() if value})


def serial_direction(vector, cells):
    return tuple((cells[index], str(value))
                 for index, value in sorted(vector.items()))


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

    cells = tuple(
        (u, v, a, b)
        for u, v in itertools.combinations(VERTICES, 2)
        if u in OUTER or v in OUTER
        for a, b in itertools.product(COLORS, repeat=2)
    )
    require(len(cells) == 162, "the endpoint variable count changed")

    expected = {
        "shared_CA": {
            "kernel_dimension": 29,
            "kernel_pair_count": 435,
            "nonzero_hasse_columns": 3,
            "hasse_entries": 67,
            "hasse_labels": ((18, 18), (18, 19), (19, 19)),
            "hasse_sizes": (25, 20, 22),
            "jacobian_rank": 133,
            "distinguished_free_cells": ((5, 6, 0, 0), (5, 7, 1, 1)),
        },
        "middle_AT_right": {
            "kernel_dimension": 11,
            "kernel_pair_count": 66,
            "nonzero_hasse_columns": 3,
            "hasse_entries": 49,
            "hasse_labels": ((9, 9), (9, 10), (10, 10)),
            "hasse_sizes": (17, 15, 17),
            "jacobian_rank": 151,
            "distinguished_free_cells": ((5, 7, 1, 1), (6, 7, 1, 0)),
        },
        "middle_AT_left_secondary": {
            "kernel_dimension": 11,
            "kernel_pair_count": 66,
            "nonzero_hasse_columns": 3,
            "hasse_entries": 78,
            "hasse_labels": ((9, 9), (9, 10), (10, 10)),
            "hasse_sizes": (28, 24, 26),
            "jacobian_rank": 151,
            "distinguished_free_cells": ((5, 7, 1, 1), (6, 7, 1, 0)),
        },
    }

    packets = {}
    for name, expected_summary in expected.items():
        source = Counter(repair.common_packets(base.cell)[name])
        source.update(repair.outer_source(base.cell))
        jacobian = {
            index: first.derivative_column(oo, source, cell)
            for index, cell in enumerate(cells)
        }
        rows = tuple(sorted(
            set().union(*(set(column) for column in jacobian.values()))
        ))
        free, kernel = second.jacobian_kernel_basis(rows, jacobian, len(cells))
        require(len(kernel) == expected_summary["kernel_dimension"],
                f"{name} kernel dimension changed")
        distinguished_indices = tuple(sorted({
            index
            for pair in expected_summary["hasse_labels"]
            for index in pair
        }))
        require(tuple(cells[free[index]] for index in distinguished_indices)
                == expected_summary["distinguished_free_cells"],
                f"{name} distinguished kernel coordinates changed")

        physical_cache = {}

        def physical_hasse(first_index, second_index):
            key = tuple(sorted((first_index, second_index)))
            if key not in physical_cache:
                physical_cache[key] = second.physical_hasse_column(
                    oo, source, cells[key[0]], cells[key[1]])
            return physical_cache[key]

        nonzero = []
        private_nonzero = []
        corrections = []
        all_pair_count = 0
        for left, right in itertools.combinations_with_replacement(
                range(len(kernel)), 2):
            all_pair_count += 1
            column = second.direction_hasse_column(
                kernel[left], kernel[right], left == right, physical_hasse)
            # On kernel directions, the cross terms involving d(ra),d(rc)
            # and first private derivatives vanish.  Thus the coefficient of
            # the private defect D is H_mixed+2 H_pure.
            private_value = (
                column.get(MIXED, Fraction(0))
                + 2 * column.get(PURE, Fraction(0))
            )
            if private_value:
                private_nonzero.append(((left, right), private_value))
            if not column:
                continue
            nonzero.append(((left, right), column))
            correction = solve_correction(jacobian, column, len(cells))
            require(not apply_correction(jacobian, column, correction),
                    f"{name} Hasse correction replay failed at {(left, right)}")
            corrections.append({
                "kernel_pair": (left, right),
                "hasse_entries": len(column),
                "correction": serial_direction(correction, cells),
            })

        labels = tuple(label for label, _column in nonzero)
        sizes = tuple(len(column) for _label, column in nonzero)
        require(all_pair_count == expected_summary["kernel_pair_count"],
                f"{name} kernel pair count changed")
        require(len(nonzero) == expected_summary["nonzero_hasse_columns"]
                and sum(sizes) == expected_summary["hasse_entries"]
                and labels == expected_summary["hasse_labels"]
                and sizes == expected_summary["hasse_sizes"],
                f"{name} restricted Hasse ledger changed")
        require(not private_nonzero,
                f"{name} has a quadratic private escape: {private_nonzero}")

        augmented = dict(jacobian)
        for offset, (_label, column) in enumerate(nonzero, start=len(cells)):
            augmented[offset] = column
        augmented_rows = tuple(sorted(
            set(rows).union(*(set(column) for _label, column in nonzero))
        ))
        rank_j = first.sparse_rank(augmented_rows, jacobian)
        rank_augmented = first.sparse_rank(augmented_rows, augmented)
        require(rank_j == rank_augmented == expected_summary["jacobian_rank"],
                f"{name} Hasse image rank changed: {rank_j}, {rank_augmented}")

        packets[name] = {
            "kernel_dimension": len(kernel),
            "kernel_pair_count": all_pair_count,
            "nonzero_hasse_columns": len(nonzero),
            "hasse_entries": sum(sizes),
            "jacobian_rank": rank_j,
            "jacobian_plus_hasse_rank": rank_augmented,
            "private_defect_hessian_nonzero_pairs": len(private_nonzero),
            "distinguished_free_cells": expected_summary[
                "distinguished_free_cells"],
            "corrections": corrections,
        }

    ledger = {
        "dependencies": PINS,
        "arc_convention": "X(t)=X0+t*v+t^2*w; order2 equation Jw+H(v,v)=0",
        "packets": packets,
        "verdict": (
            "every endpoint tangent has a full-output second-order lift, but "
            "the private defect Hessian vanishes on every kernel pair; no "
            "genuine order-two endpoint arc breaks the private-row unit"
        ),
        "scope": (
            "endpoint-star/direct jets through order two at the three carrier "
            "calibrations with internal q frozen; base calibrations remain "
            "nonexact, and cubic endpoint effects are not classified"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the endpoint second-order ledger changed: {digest}")

    print("h=3 same-hole endpoint second-order rigidity: PASS")
    print("kernel pairs: 435/66/66; nonzero Hasse columns: 3/3/3")
    print("all Hasse columns lie in im(J); explicit corrections replay")
    print("private defect Hessian nonzero pairs: 0/0/0")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
