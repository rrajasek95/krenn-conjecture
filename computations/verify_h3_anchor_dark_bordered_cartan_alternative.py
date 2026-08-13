#!/usr/bin/env python3
"""Close the anchor-dark corank-one circuit by a bordered alternative.

Let A be the complete physical target-augmented response map on a minimum
target-circuit block, h the physical pure/target anchor row, and (g,alpha)
the placed Cartan column.  If ker(A)=<k> and h(k)=0, then h=lambda*A.
Put beta=alpha-lambda*g.

* beta != 0: (-lambda,1) kills every old bordered column, including the
  target column, and detects (g,alpha): a normalized target-dark separator.
* beta = 0 and g is internal: a preimage Ay=g automatically has h(y)=alpha,
  so (-y,1) is a unit-Cartan kernel.
* beta = 0 and g is external: an ordinary cokernel covector of A, extended
  by zero on h, is a target-dark separator.

Thus failure of anchor visibility is not a dead linear branch once all rows
and the Cartan column are physically typed.  Maximum-anchor/minimum-support
produces the target circuit but is not needed to force h(k) nonzero.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_shared_odd_comparison_anchor_visibility_gate.py":
        "509cdefe20ca38904cdab3e60b924d3a0b03f87062a380c33bf97f724653b47c",
    "computations/verify_rectangular_interference_anchor_cartan_alternative.py":
        "b3d4db9e58f374bfd1f99a43931cac87fdab109c5d33c2f1c7d110e51e8f9a0a",
    "computations/verify_target_augmented_affine_circuit_cartan_guard.py":
        "7c72b58101cc77a0ca3e3c688b5de0742b4f118777f450f235d578691954d08f",
    "computations/verify_h3_fan_coloop_cartan_circuit_comparison_gate.py":
        "c652f10a8bac32f11f4c090a55687cf672ce3f96629384f0fbde9f08f440a1bd",
}
EXPECTED_LEDGER_SHA256 = (
    "9f5e47e711a6249d256a09a3374b978a14f11f2dea77238a4a265e6816174cbf"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def mat_vec(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def row_mat(vector, matrix):
    return tuple(dot(vector, column)
                 for column in zip(*matrix, strict=True))


def rank(matrix):
    work = [list(map(Q, row)) for row in matrix]
    if not work:
        return 0
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def append_row(matrix, row):
    return tuple(matrix) + (tuple(row),)


def append_column(matrix, column):
    return tuple(tuple(row) + (Q(value),)
                 for row, value in zip(matrix, column, strict=True))


def audit_actual_pivot_dark_alternative():
    # The first two rows and k are the exact actual-pivot guard of e6b390a.
    # The zero output row lets the placed Cartan be either internal or
    # external without changing that circuit block.
    response = (
        (Q(4), Q(-2), Q(-1)),
        (Q(3), Q(-2), Q(0)),
        (Q(0), Q(0), Q(0)),
    )
    circuit = (Q(2), Q(3), Q(2))
    physical_anchor = response[0]
    lam = (Q(1), Q(0), Q(0))
    bordered_old = append_row(response, physical_anchor)
    sigma = (Q(-1), Q(0), Q(0), Q(1))
    require(rank(response) == 2
            and mat_vec(response, circuit) == (Q(0), Q(0), Q(0))
            and dot(physical_anchor, circuit) == 0
            and row_mat(lam, response) == physical_anchor
            and row_mat(sigma, bordered_old) == (Q(0), Q(0), Q(0)),
            "the actual-pivot dark factorization changed")

    # 1. The normalized anchor relation detects the new column.
    external = (Q(0), Q(0), Q(1))
    alpha = Q(1)
    residual = alpha - dot(lam, external)
    require(residual == 1
            and dot(sigma, external + (alpha,)) == residual,
            "the anchor-normalized target-dark separator changed")

    # 2. If that residual vanishes but g is external, the old cokernel
    # separator survives with zero coefficient on the anchor row.
    alpha_external_compatible = Q(0)
    external_separator = (Q(0), Q(0), Q(1), Q(0))
    require(dot(external_separator, external +
                (alpha_external_compatible,)) == 1
            and row_mat(external_separator, bordered_old)
            == (Q(0), Q(0), Q(0)),
            "the compatible external separator changed")

    # 3. If g is internal and beta=0, a preimage automatically satisfies
    # the physical anchor row and gives a unit-Cartan kernel.
    preimage = (Q(1), Q(0), Q(0))
    internal = mat_vec(response, preimage)
    alpha_internal = dot(physical_anchor, preimage)
    full_bordered = append_column(bordered_old,
                                  internal + (alpha_internal,))
    unit_kernel = tuple(-value for value in preimage) + (Q(1),)
    require(alpha_internal - dot(lam, internal) == 0
            and mat_vec(full_bordered, unit_kernel)
            == (Q(0), Q(0), Q(0), Q(0)),
            "the compatible internal unit kernel changed")

    # 4. An incompatible alpha on the same internal g returns to sigma.
    alpha_internal_bad = alpha_internal + 1
    require(dot(sigma, internal + (alpha_internal_bad,)) == 1,
            "the incompatible internal separator changed")
    return {
        "protected_response_matrix": [list(map(str, row))
                                        for row in response],
        "target_circuit": list(map(str, circuit)),
        "dark_physical_anchor": list(map(str, physical_anchor)),
        "anchor_factorization": "h_phys=(1,0,0)*A_D",
        "normalized_dark_separator": list(map(str, sigma)),
        "separator_branch": "beta=alpha-lambda*g != 0",
        "external_compatible_branch":
            "ordinary coker(A_D) separator, extended by zero on h_phys",
        "internal_compatible_branch":
            "physical unit-Cartan kernel (-y,1)",
    }


def audit_all_small_cartan_columns():
    # Exhaust all small Cartan columns and bottom-right entries for the
    # actual pivot guard.  im(A) is exactly the plane g_3=0, lambda*g=g_1.
    # The three cases below are therefore exhaustive without a solver.
    counts = {
        "anchor_relation_separator": 0,
        "external_cokernel_separator": 0,
        "internal_unit_kernel": 0,
    }
    response = (
        (Q(4), Q(-2), Q(-1)),
        (Q(3), Q(-2), Q(0)),
        (Q(0), Q(0), Q(0)),
    )
    physical_anchor = response[0]
    bordered_old = append_row(response, physical_anchor)
    sigma = (Q(-1), Q(0), Q(0), Q(1))
    for g1, g2, g3, alpha in product((-1, 0, 1), repeat=4):
        cartan = (Q(g1), Q(g2), Q(g3))
        alpha = Q(alpha)
        beta = alpha - Q(g1)
        if beta:
            require(dot(sigma, cartan + (alpha,)) == beta,
                    "a small nonzero beta lost its separator")
            counts["anchor_relation_separator"] += 1
            continue
        if g3:
            external_separator = (Q(0), Q(0), Q(1), Q(0))
            require(row_mat(external_separator, bordered_old)
                    == (Q(0), Q(0), Q(0))
                    and dot(external_separator, cartan + (alpha,)) == g3,
                    "a small compatible external column lost its separator")
            counts["external_cokernel_separator"] += 1
            continue
        # The first two response coordinates have independent columns.
        y1 = Q(g1 - g2)
        y2 = Q(3 * g1 - 4 * g2, 2)
        preimage = (y1, y2, Q(0))
        require(mat_vec(response, preimage) == cartan
                and dot(physical_anchor, preimage) == alpha,
                "a small compatible internal column lost its preimage")
        full_bordered = append_column(bordered_old, cartan + (alpha,))
        unit_kernel = tuple(-value for value in preimage) + (Q(1),)
        require(not any(mat_vec(full_bordered, unit_kernel)),
                "a small compatible internal unit kernel changed")
        counts["internal_unit_kernel"] += 1
    require(sum(counts.values()) == 81 and all(counts.values()),
            "the small bordered alternative census changed")
    return counts


def audit_minimum_support_does_not_force_brightness():
    # Regard the first two entries as occupied old endpoint columns and the
    # last entry as the homogenizing target column -t.  The old columns are
    # independent, and t needs both of them.  Thus the affine solution is
    # unique and support-minimal, while the physical anchor can still be an
    # old complete response row and kill the target circuit.
    old_columns = ((Q(4), Q(3)), (Q(-2), Q(-2)))
    target = (Q(1), Q(0))
    solution = (Q(1), Q(3, 2))
    reconstructed = tuple(
        sum(solution[column] * old_columns[column][row]
            for column in range(2))
        for row in range(2)
    )
    require(rank(tuple(zip(*old_columns, strict=True))) == 2
            and reconstructed == target
            and rank(((Q(4),), (Q(3),))) == 1
            and rank(((Q(-2),), (Q(-2),))) == 1,
            "the unique minimum affine packet changed")
    # Neither single old column spans the target.
    require(old_columns[0][0] * target[1]
            != old_columns[0][1] * target[0]
            and old_columns[1][0] * target[1]
            != old_columns[1][1] * target[0],
            "the minimum packet acquired a target-coordinate point")
    return {
        "occupied_old_columns": [list(map(str, column))
                                  for column in old_columns],
        "unique_affine_solution": list(map(str, solution)),
        "support_minimal": True,
        "coordinate_line_hit": False,
        "anchor_dark": True,
        "consequence": (
            "minimum affine support alone cannot force h_phys(k)!=0; the "
            "bordered separator/unit alternative is the exact replacement"
        ),
    }


def main():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    ledger = {
        "theorem": "anchor-dark bordered Cartan alternative",
        "pins": PINS,
        "actual_pivot_packet": audit_actual_pivot_dark_alternative(),
        "small_Cartan_census": audit_all_small_cartan_columns(),
        "minimum_support_guard":
            audit_minimum_support_does_not_force_brightness(),
        "exact_alternative": (
            "on a corank-one target-circuit block, h_phys(k)=0 implies "
            "h_phys=lambda*A_D.  For the physical Cartan column (g,alpha), "
            "beta=alpha-lambda*g nonzero gives the normalized target-dark "
            "separator (-lambda,1).  If beta=0, external g has the ordinary "
            "cokernel separator and internal g gives a physical unit-Cartan "
            "kernel.  Hence anchor darkness has no fourth linear branch"
        ),
        "source_interface": (
            "A_D, h_phys, and (g,alpha) must be the complete physically "
            "typed packet.  Under that hypothesis every displayed covector "
            "is a localized combination of literal output rows and kills "
            "the homogenizing target column; no occurrence-only selector is used"
        ),
        "scope": (
            "exact localized bordered linear algebra using the actual fan "
            "pivot guard.  It does not construct the shared odd Phi, prove "
            "global entry, or assert that the numerical guard is a full "
            "Krenn source"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"anchor-dark bordered ledger changed: {digest}")
    print("h3 anchor-dark bordered Cartan: EXACT CLOSED ALTERNATIVE")
    print("dark -> normalized target-dark separator or unit-Cartan kernel")
    print("minimum support alone does not force anchor brightness")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
