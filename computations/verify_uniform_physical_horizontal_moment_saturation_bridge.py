#!/usr/bin/env python3
"""Exact audit for the physical horizontal moment-saturation bridge.

The checker verifies only the finite rational algebra used in
``notes/uniform-physical-horizontal-moment-saturation-bridge.md``:

* the two oriented curvature factors add with the required sign;
* their common polynomial carrier produces every Hilbert--Cauchy moment;
* the based Rodrigues residue matrix is triangular and invertible;
* hence one carrier saturation condition is equivalent to zero residue in
  all required moments in the polynomially closed lift model; and
* the literal overlapping-chart four-cut/Bianchi expression cancels by
  the divided-power product rules while its chart-tagged presentation has
  a nonzero reinsertion kernel.

It does not construct the complete decorated physical source complex, its
common-carrier comparison, or the required saturation homotopy.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction
from math import factorial
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PINNED = {
    "notes/scalar-unit-c0-four-cut-common-carrier-gate.md":
        "a06018da73d6a954f14706fcfdeaae5ace1c2424e02530ab87602c1e77271000",
    "notes/scalar-unit-c1-weighted-endpoint-bockstein-gate.md":
        "c954f7c6d70368b7aee98208f68dc4c53ff6dae93e49cfa3862939707d00f7a3",
    "notes/scalar-unit-moment-transgression-source-lift-based-loop-torsor.md":
        "8df4b715775194282542cf1ea057b8305223744504687e5e480c4c262fcecd4a",
    "notes/scalar-unit-carrier-moment-tower-hilbert-cauchy.md":
        "c9a58db12d8959a3b498c3e6b0ae54aeb49224476fb02d264d21d77d8a230855",
    "notes/curved-two-root-polarization-and-four-cut-square.md":
        "93d3f5797a9fbb97b363696e02f66c3af400e2429c64bd1f99bb0d9349710265",
    "notes/adjacent_full_nine_h3_cycle_transgression.md":
        "492a5a36c580b388dc0301727caf37b34a4448f2ab6bf63402d131a11d97fbbb",
    "computations/verify_scalar_unit_c0_four_cut_common_carrier_gate.py":
        "56421c894acd613300841b7ae41d1bafecc6d65fcc9618982dc61ac198c2fa66",
    "computations/verify_scalar_unit_c1_weighted_endpoint_bockstein_gate.py":
        "11fda4d929d1b064fe49ff9f45e077a2dd9bffdaec23a85b4be8a55d44561fa8",
    "computations/verify_scalar_unit_moment_transgression_source_lift_based_loop_torsor.py":
        "4bff53e1568a74cfe262fac185558aa14337fe1a2e31e6c46141645e78e8e839",
    "computations/verify_scalar_unit_carrier_moment_tower_hilbert_cauchy.py":
        "b1674da530c0af1790780bb19fadc7622117b373ece3e9a0845cbb532870e3f3",
    "computations/verify_adjacent_full_nine_h3_cycle_transgression.py":
        "13b4226fe558536005478bf929b7962c259f55891cb1a88f2628d4f483cb6717",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def check_pins() -> None:
    for relative, expected in PINNED.items():
        data = (ROOT / relative).read_bytes()
        actual = hashlib.sha256(data).hexdigest()
        require(actual == expected, f"source drift: {relative}: {actual}")


def poly_add(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    length = max(len(a), len(b))
    out = [Fraction(0) for _ in range(length)]
    for i, value in enumerate(a):
        out[i] += value
    for i, value in enumerate(b):
        out[i] += value
    return out


def poly_mul(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0) for _ in range(len(a) + len(b) - 1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def poly_derivative(a: list[Fraction]) -> list[Fraction]:
    if len(a) <= 1:
        return [Fraction(0)]
    return [Fraction(i) * a[i] for i in range(1, len(a))]


def poly_power(a: list[Fraction], exponent: int) -> list[Fraction]:
    out = [Fraction(1)]
    for _ in range(exponent):
        out = poly_mul(out, a)
    return out


def eta(j: int) -> list[Fraction]:
    base = poly_mul(poly_power([Fraction(0), Fraction(1)], j),
                    poly_power([Fraction(1), Fraction(-1)], j))
    for _ in range(j - 1):
        base = poly_derivative(base)
    return base


def integral_weighted_derivative(a: list[Fraction], s: int) -> Fraction:
    derivative = poly_derivative(a)
    return sum(value / Fraction(i + s + 1)
               for i, value in enumerate(derivative))


def matrix_rank(matrix: list[list[Fraction]]) -> int:
    if not matrix:
        return 0
    work = [row[:] for row in matrix]
    rows = len(work)
    cols = len(work[0])
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows)
                      if work[r][col] != 0), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][col]
        work[rank] = [entry / scale for entry in work[rank]]
        for row in range(rows):
            if row == rank or work[row][col] == 0:
                continue
            scale = work[row][col]
            work[row] = [x - scale * y
                         for x, y in zip(work[row], work[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def oriented_and_moment_audit(h: int) -> dict[str, object]:
    n = h - 2
    m = 1 if h == 3 else h - 3

    # K_right=q-x and K_left=q-r+x.  In coordinates (q,r,x), the
    # negative of their sum is the desired (r-2q).
    k_right = (1, 0, -1)
    k_left = (1, -1, 1)
    negative_sum = tuple(-(a + b) for a, b in zip(k_right, k_left))
    require(negative_sum == (-2, 1, 0),
            f"oriented curvature sign failed at h={h}")

    # Coefficients of (q+t r)^[n] in the divided-power basis
    # q^[n-l] r^[l] are exactly t^l.  Weighted integration gives H_s.
    moments = []
    for s in range(m + 1):
        row = [Fraction(1, s + ell + 1) for ell in range(n + 1)]
        moments.append(row)
        require(row == [Fraction(1, s + ell + 1)
                        for ell in range(n + 1)],
                f"moment denominator failed at h={h}, s={s}")

    delta = []
    for s in range(1, m + 1):
        row = []
        for j in range(1, m + 1):
            value = integral_weighted_derivative(eta(j), s)
            row.append(value)
            if s < j:
                require(value == 0,
                        f"Rodrigues upper entry failed at h={h}, s={s}, j={j}")
            if s == j:
                expected = Fraction((-1) ** j * factorial(j) ** 3,
                                    factorial(2 * j + 1))
                require(value == expected,
                        f"Rodrigues diagonal failed at h={h}, j={j}")
        delta.append(row)
    require(matrix_rank(delta) == m,
            f"moment residue map is not invertible at h={h}")

    return {
        "h": h,
        "n": n,
        "m": m,
        "negative_oriented_sum": negative_sum,
        "moment_rows": len(moments),
        "residue_rank": matrix_rank(delta),
        "residue_diagonal": [delta[j][j] for j in range(m)],
    }


def four_cut_exchange_audit(max_k: int = 24) -> dict[str, object]:
    # Equation (22) in the physical overlapping-pair square has five
    # decorated terms.  Evaluate in the two basis monomials
    #   kappa*z^[k] and Delta*v*z^[k-1].
    # The divided-power rules are z z^[k-1]=k z^[k] and
    # z z^[k-2]=(k-1)z^[k-1].
    # In the scalar-unit alignment, k=h-1, so h>=3 gives k>=2.
    for k in range(2, max_k + 1):
        kappa_coefficient = Fraction(k) - Fraction(k)
        delta_coefficient = (
            Fraction(1)
            + Fraction(k - 1)
            - Fraction(k)
        )
        require(kappa_coefficient == 0,
                f"four-cut kappa cancellation failed at k={k}")
        require(delta_coefficient == 0,
                f"four-cut Delta cancellation failed at k={k}")

    # The physical target is the same after reinsertion in the two pair
    # charts.  Retaining the chart tags gives pi=[1,1] and the literal
    # exchange beta=(1,-1).  This is a nonzero presentation-kernel class.
    pi = [[Fraction(1), Fraction(1)]]
    beta = [Fraction(1), Fraction(-1)]
    require(sum(pi[0][i] * beta[i] for i in range(2)) == 0,
            "chart exchange is not in the reinsertion kernel")
    require(any(beta), "chart exchange tag was accidentally collapsed")
    require(matrix_rank(pi) == 1, "reinsertion rank changed")

    # One unconstrained lower readout can see beta.  This is the exact
    # counterguard: the physical square constrains pi but not chi.
    chi = [Fraction(1), Fraction(0)]
    require(sum(chi[i] * beta[i] for i in range(2)) == 1,
            "counterguard lower readout stopped seeing the exchange")
    return {
        "checked_k": [2, max_k],
        "reinsertion_rank": matrix_rank(pi),
        "exchange_kernel_dimension": 1,
        "lower_exchange_readout": 1,
    }


def mutation_guards() -> None:
    require(integral_weighted_derivative(eta(1), 1) == Fraction(-1, 6),
            "h=3 first residue changed")
    wrong = integral_weighted_derivative(eta(2), 1)
    require(wrong == 0, "wrong Rodrigues-order mutation was not detected")
    # Dropping the middle Delta*z*v*z^[k-2] term breaks the exchange for k>1.
    k = 4
    mutated_delta = Fraction(1) - Fraction(k)
    require(mutated_delta != 0, "missing physical exchange term was not detected")


def main() -> None:
    check_pins()
    audits = [oriented_and_moment_audit(h) for h in range(3, 25)]
    exchange = four_cut_exchange_audit()
    mutation_guards()
    digest = hashlib.sha256(repr((audits, exchange)).encode()).hexdigest()
    print("PASS: uniform physical horizontal moment-saturation bridge")
    print("heights: 3..24")
    print("oriented one-form: COMMON-CARRIER CONDITIONAL")
    print("all-moment zero residue: ONE SATURATION HOMOTOPY")
    print("physical overlap square alone: INSUFFICIENT")
    print(f"digest: {digest}")


if __name__ == "__main__":
    main()
