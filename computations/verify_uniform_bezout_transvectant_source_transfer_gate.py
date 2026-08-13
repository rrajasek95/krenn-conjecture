#!/usr/bin/env python3
"""Audit the Bezout/transvectant route to the uniform Hankel transfer.

This checker separates three statements which must not be conflated.

* The (h-1)-st transvectant of the coprime pure-axis pair u^h,v^h is
  nonzero, although its Sylvester/Bezout matrix is invertible.  Therefore
  a nonzero selector quadratic obtained by transvection does not force a
  common root or a kernel of the clean Macaulay dual.
* A common Bezout kernel is exactly the finite datum which *would* give
  the residual Macaulay annihilator.  One singular selected pair is not
  enough: two different pairwise common roots can have zero simultaneous
  kernel.
* The selector transvectant has dimension 3, whereas the residual quotient
  has dimension h.  They coincide accidentally at h=3; a uniform transfer
  needs an additional source-provenant degree-(h-3) lift (or an equivalent
  direct common-Bezout-kernel construction).

The paired note proves the general algebra.  Exact loops here audit signs,
ranks, common-kernel claims, and the corank-one adjugate limitation.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from math import factorial
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/residual-macaulay-quotient-is-the-common-divisor.md":
        "3ab98728e5ec56acd8c667201721ed1afe35759e7cf5e7be155992d233e54890",
    "notes/uniform-grade-split-sum-channel-activity-hankel-gate.md":
        "118622424ea00d3337ede2c16d1e68b4f50489efeeae0bfe66462d3c009c96ed",
    "computations/verify_uniform_grade_split_sum_channel_activity_hankel_gate.py":
        "f7d41da5f362d0de9f36471bf6d4daf05c93bfc74f842f47b65db4a76222d7b6",
    "notes/five-exposed-site-yoneda-cup-obstruction.md":
        "5d19a2f851c3e1757667a53a808d16c0beabb0647e3b0a67e7630b4bf7b59775",
    "computations/verify_five_exposed_site_yoneda_cup_obstruction.py":
        "7421ca0080779b00d6aab0935822b063053b5cf8eb670885161be98eca7bda1f",
    "notes/derived-base-change-relative-cap-obstruction.md":
        "83b13f7048a7ff9c3c27374bdafa51996403c8806ead0982d83fe37005e65136",
    "computations/verify_derived_base_change_relative_cap_obstruction.py":
        "19c38d42710de2df403aa5cdf8513b6c03a758ab01eb281ce9da21564ca907d3",
}
EXPECTED_LEDGER_SHA256 = "fdf6f145759cb4c35c30167c03642e9485aca9e5d352d8942a9d2d6cc6369a5c"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def matrix_rank(matrix) -> int:
    if not matrix:
        return 0
    work = [list(map(Fraction, row)) for row in matrix]
    rows = len(work)
    columns = len(work[0])
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [entry / pivot_value for entry in work[rank]]
        for row in range(rows):
            if row == rank or not work[row][column]:
                continue
            coefficient = work[row][column]
            work[row] = [
                entry - coefficient * pivot_entry
                for entry, pivot_entry in zip(
                    work[row], work[rank], strict=True
                )
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def determinant(matrix) -> Fraction:
    require(len(matrix) == len(matrix[0]), "determinant needs square matrix")
    work = [list(map(Fraction, row)) for row in matrix]
    result = Fraction(1)
    for column in range(len(work)):
        pivot = next(
            (row for row in range(column, len(work))
             if work[row][column]), None
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result *= -1
        pivot_value = work[column][column]
        result *= pivot_value
        for row in range(column + 1, len(work)):
            coefficient = work[row][column] / pivot_value
            for entry in range(column, len(work)):
                work[row][entry] -= coefficient * work[column][entry]
    return result


def poly_multiply(left, right):
    result = [Fraction(0) for _ in range(len(left) + len(right) - 1)]
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            result[i + j] += Fraction(left_value) * Fraction(right_value)
    return result


def poly_power(polynomial, exponent):
    result = [Fraction(1)]
    for _ in range(exponent):
        result = poly_multiply(result, polynomial)
    return result


def padded(polynomial, size):
    return list(map(Fraction, polynomial)) + [Fraction(0)] * (
        size - len(polynomial)
    )


def bezout_matrix(f, g, h):
    """Return coefficients of (f(x)g(y)-f(y)g(x))/(x-y)."""
    f = padded(f, h + 1)
    g = padded(g, h + 1)
    numerator = [
        [f[i] * g[j] - g[i] * f[j] for j in range(h + 1)]
        for i in range(h + 1)
    ]

    # Synthetic division in x.  If N=(x-y)Q, then
    # q_{a-1}(y)=N_a(y)+y q_a(y), starting with q_h=0.
    quotient = [[Fraction(0) for _ in range(h + 1)] for _ in range(h)]
    next_row = [Fraction(0) for _ in range(h + 1)]
    for a in range(h, 0, -1):
        shifted = [Fraction(0)] + next_row[:-1]
        row = [numerator[a][j] + shifted[j] for j in range(h + 1)]
        quotient[a - 1] = row
        next_row = row

    remainder = [
        numerator[0][j]
        + (Fraction(0) if j == 0 else quotient[0][j - 1])
        for j in range(h + 1)
    ]
    require(not any(remainder), ("Bezout division remainder", f, g))
    require(all(row[h] == 0 for row in quotient),
            ("Bezout bidegree exceeded", f, g))
    return [row[:h] for row in quotient]


def matvec(matrix, vector):
    return [
        sum(entry * value for entry, value in zip(row, vector, strict=True))
        for row in matrix
    ]


def matrix_multiply(left, right):
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right)))
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def reduce_mod_monic(polynomial, f, h):
    """Reduce a low-to-high polynomial modulo a monic degree-h f."""
    work = list(map(Fraction, polynomial))
    while len(work) > h:
        while len(work) > h and not work[-1]:
            work.pop()
        if len(work) <= h:
            break
        degree = len(work) - 1
        coefficient = work[-1]
        for j in range(h + 1):
            work[degree - h + j] -= coefficient * f[j]
    return padded(work, h)[:h]


def multiplication_matrix_mod_f(e, f, h):
    columns = [
        reduce_mod_monic([Fraction(0)] * j + list(e), f, h)
        for j in range(h)
    ]
    return [
        [columns[column][row] for column in range(h)]
        for row in range(h)
    ]


def delete_row_column(matrix, deleted_row, deleted_column):
    return [
        [entry for j, entry in enumerate(row) if j != deleted_column]
        for i, row in enumerate(matrix) if i != deleted_row
    ]


def pure_axis_and_type_audit() -> dict[str, object]:
    records = {}
    for h in range(3, 10):
        f = [Fraction(0)] * h + [Fraction(1)]       # t^h
        g = [Fraction(1)]                           # v^h on v=1
        bezout = bezout_matrix(f, g, h)
        expected_sign = -1 if h * (h - 1) // 2 % 2 else 1
        require(matrix_rank(bezout) == h,
                ("pure-axis Bezout lost rank", h))
        require(determinant(bezout) == expected_sign,
                ("pure-axis Bezout determinant changed", h))

        # In the standard unnormalised convention only k=0 survives in
        # (u^h,v^h)_{h-1}; the coefficient of uv is (h!)^2.
        transvectant_uv = factorial(h) ** 2
        require(transvectant_uv != 0,
                ("pure-axis transvectant vanished", h))

        records[h] = {
            "bezout_rank": h,
            "bezout_determinant": expected_sign,
            "transvectant_uv_coefficient": transvectant_uv,
            "selector_dimension": 3,
            "residual_dimension": h,
            "extra_symmetric_degree_needed": h - 3,
        }
    return {
        "orders": records,
        "counterguard": (
            "(u^h,v^h)_{h-1}=(h!)^2 uv is nonzero while "
            "Bez(u^h,v^h) is invertible"
        ),
        "h3_accident": "Sym^2 U and Q_f both have dimension 3",
        "uniform_type_gap": (
            "for h>3 a selector quadratic is not a vector/covector of "
            "the h-dimensional residual quotient"
        ),
    }


def common_kernel_audit() -> dict[str, object]:
    records = {}
    for h in range(3, 9):
        # Barnett's identity fixes the precise bridge from Bezout kernels
        # to multiplication annihilators in A_f=k[t]/(f):
        # B(f,e)=M_e B(f,1), with B(f,1) invertible.
        f_barnett = [Fraction(j + 1) for j in range(h)] + [Fraction(1)]
        e_barnett = [Fraction((j + 2) % 3) for j in range(h + 1)]
        b_one = bezout_matrix(f_barnett, [Fraction(1)], h)
        b_e = bezout_matrix(f_barnett, e_barnett, h)
        multiplication = multiplication_matrix_mod_f(
            e_barnett, f_barnett, h
        )
        require(matrix_rank(b_one) == h
                and b_e == matrix_multiply(multiplication, b_one),
                ("Barnett Bezout/multiplication identity changed", h))

        # The gcd(t^h,t^j) has degree j, and the Bezout kernel does too.
        gcd_ranks = {}
        f_axis = [Fraction(0)] * h + [Fraction(1)]
        for j in range(1, h):
            e = [Fraction(0)] * j + [Fraction(1)]
            rank = matrix_rank(bezout_matrix(f_axis, e, h))
            require(rank == h - j,
                    ("Bezout gcd rank changed", h, j, rank))
            gcd_ranks[j] = {"rank": rank, "kernel_dimension": j}

        # A literal shared simple root produces the evaluation kernel.
        root = Fraction(2)
        tail0 = [Fraction(1)] + [Fraction(0)] * (h - 2) + [Fraction(1)]
        tail1 = [Fraction(2)] + [Fraction(0)] * (h - 2) + [Fraction(1)]
        f = poly_multiply([-root, Fraction(1)], tail0)
        e = poly_multiply([-root, Fraction(1)], tail1)
        shared = bezout_matrix(f, e, h)
        evaluation = [root ** degree for degree in range(h)]
        require(matvec(shared, evaluation) == [Fraction(0)] * h,
                ("shared-root evaluation left Bezout kernel", h))
        require(matrix_rank(shared) == h - 1,
                ("shared-root pair did not have simple corank", h))

        # Pairwise resultant vanishing is insufficient.  Here f has roots
        # 0 and 1, e0 shares only 0, and e1 shares only 1.
        f_two_roots = [Fraction(0)] * (h - 1) + [Fraction(-1), Fraction(1)]
        e0 = [Fraction(0)] * h + [Fraction(1)]
        e1 = poly_power([Fraction(-1), Fraction(1)], h)
        b0 = bezout_matrix(f_two_roots, e0, h)
        b1 = bezout_matrix(f_two_roots, e1, h)
        require(matrix_rank(b0) < h and matrix_rank(b1) < h,
                ("pairwise resultant guard became nonsingular", h))
        require(matrix_rank(b0 + b1) == h,
                ("different pairwise roots gained common kernel", h))

        records[h] = {
            "Barnett_identity": "B(f,e)=M_e B(f,1)",
            "monomial_gcd_ranks": gcd_ranks,
            "shared_simple_root_kernel_dimension": 1,
            "two_singular_pairs_simultaneous_kernel_dimension": 0,
        }
    return {
        "orders": records,
        "positive_datum": (
            "choose nonzero w_h in the simultaneous right kernel of "
            "Bez(f,e) for every clean coordinate e"
        ),
        "selected_pair_resultant_is_insufficient": True,
    }


def adjugate_audit() -> dict[str, object]:
    records = {}
    for h in range(3, 8):
        corank_one = [
            [Fraction(int(i == j and i > 0)) for j in range(h)]
            for i in range(h)
        ]
        corank_two = [
            [Fraction(int(i == j and i > 1)) for j in range(h)]
            for i in range(h)
        ]
        minors_one = [
            determinant(delete_row_column(corank_one, i, j))
            for i in range(h) for j in range(h)
        ]
        minors_two = [
            determinant(delete_row_column(corank_two, i, j))
            for i in range(h) for j in range(h)
        ]
        require(any(minors_one) and not any(minors_two),
                ("adjugate corank guard changed", h))
        records[h] = {
            "corank_one_adjugate_nonzero": True,
            "corank_two_adjugate_zero": True,
        }
    return {
        "orders": records,
        "consequence": (
            "an adjugate formula constructs the kernel only on the "
            "corank-one stratum; uniform source provenance needs the "
            "first nonzero subresultant/Fitting stratum and gluing"
        ),
    }


def scope_audit() -> dict[str, object]:
    residual = (ROOT / (
        "notes/residual-macaulay-quotient-is-the-common-divisor.md"
    )).read_text()
    grade_split = (ROOT / (
        "notes/uniform-grade-split-sum-channel-activity-hankel-gate.md"
    )).read_text()
    yoneda = (ROOT / (
        "notes/five-exposed-site-yoneda-cup-obstruction.md"
    )).read_text()
    derived_cap = (ROOT / (
        "notes/derived-base-change-relative-cap-obstruction.md"
    )).read_text()
    require(r"\operatorname {rank}\mu_{f,L'}=h-d" in residual,
            "residual gcd theorem changed")
    require("an independent physical" in grade_split
            and r"\operatorname{Tr}_h" in grade_split,
            "uniform transfer frontier changed")
    require("with the augmented cap cycle (5) is again a boundary" in yoneda
            and "again a boundary" in yoneda,
            "ordinary Yoneda/cup obstruction changed")
    require("relative lifting obstruction" in derived_cap
            and "absolute Tor, Yoneda" in derived_cap,
            "relative cap interpretation changed")
    return {
        "Tr_h_constructed": False,
        "bare_transvectant_forces_kernel": False,
        "ordinary_Yoneda_product_supplies_terminal": False,
        "exact_additional_relation": (
            "a source-provenant simultaneous Bezout-kernel section, "
            "nonzero on every Fitting/subresultant stratum"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "uniform Bezout-transvectant source transfer gate",
        "pins": PINS,
        "scope": scope_audit(),
        "pure_axis_and_types": pure_axis_and_type_audit(),
        "common_kernel": common_kernel_audit(),
        "adjugate": adjugate_audit(),
        "verdict": (
            "A transvectant/Bezout formula does not construct Tr_h from "
            "the committed source equations.  The shortest exact missing "
            "relation is a nonzero, source-provenant simultaneous Bezout "
            "kernel for every clean coordinate, with branchwise "
            "subresultant normalization.  At h>3 one also needs a typed "
            "degree-(h-3) transfer from the selector quadratic to the "
            "h-dimensional residual module."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("uniform Bezout/transvectant ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("(h-1)-transvectant alone: DOES NOT FORCE COMMON ROOT")
    print("selected-pair resultant alone: DOES NOT FORCE COMMON KERNEL")
    print("exact positive datum: SOURCE-PROVENANT SIMULTANEOUS BEZOUT KERNEL")
    print("uniform type correction: DEGREE-(h-3) TRANSFER OR EQUIVALENT")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
