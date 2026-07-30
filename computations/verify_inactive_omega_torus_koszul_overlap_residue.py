#!/usr/bin/env python3
"""Exact checks for the inactive-Omega torus-Koszul residue.

The script is dependency-free.  For every 1 <= d <= max_d it verifies the
bounded convolution from explicit Omega/H coefficient vectors, the
Euler/Koszul image and cokernel, explicit noncentral primitives, the
nonzero transported middle class, its cancellation by the normalized
correction, and the formal zero-prolongation guard.  It also checks the
direct-free triangular carrier on exact rational samples.
"""

from __future__ import annotations

import argparse
from fractions import Fraction


def fail(message: str) -> None:
    raise RuntimeError(message)


def pair(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> Fraction:
    """Exact pairing of equal-length coordinate vectors."""
    if len(left) != len(right):
        fail("pairing vectors have different lengths")
    return sum((x * y for x, y in zip(left, right)), Fraction(0))


def torus_weights(d: int) -> list[int]:
    """Weights of t^(2d-n) u^n under t*d_t-u*d_u."""
    return [2 * (d - n) for n in range(2 * d + 1)]


def apply_torus_operator(d: int, coefficients: list[Fraction]) -> list[Fraction]:
    weights = torus_weights(d)
    if len(coefficients) != len(weights):
        fail("wrong coefficient-vector length")
    return [Fraction(weight) * value for weight, value in zip(weights, coefficients)]


def primitive_of_zero_middle(d: int, values: list[Fraction]) -> list[Fraction]:
    weights = torus_weights(d)
    if len(values) != len(weights):
        fail("wrong residue-vector length")
    if values[d] != 0:
        fail("attempted to integrate a nonzero middle residue")
    primitive: list[Fraction] = []
    for n, value in enumerate(values):
        if n == d:
            primitive.append(Fraction(0))
        else:
            primitive.append(value / weights[n])
    return primitive


def check_degree(d: int) -> None:
    # In the formal guard V=<A_0,B_0,Z>.  The independent A_0,B_0 supports
    # make Omega=t^d A_0+u^d B_0 nonzero whenever tu != 0.  The certificate
    # is H=u^d alpha with alpha(A_0)=1 and alpha(B_0)=alpha(Z)=0.
    zero = (Fraction(0), Fraction(0), Fraction(0))
    a_0 = (Fraction(1), Fraction(0), Fraction(0))
    b_0 = (Fraction(0), Fraction(1), Fraction(0))
    z_vector = (Fraction(0), Fraction(0), Fraction(1))
    alpha = a_0
    if a_0[0] * b_0[1] - a_0[1] * b_0[0] == 0:
        fail(f"degree {d}: formal Omega endpoints are not independent")
    omega = [zero for _ in range(d + 1)]
    omega[0] = a_0
    omega[d] = b_0
    certificate = [zero for _ in range(d + 1)]
    certificate[d] = alpha
    convolution: list[Fraction] = []
    for n in range(2 * d + 1):
        coefficient = Fraction(0)
        for r in range(d + 1):
            k = n - r
            if 0 <= k <= d:
                coefficient += pair(certificate[r], omega[k])
        convolution.append(coefficient)
    if convolution[d] != 1 or any(
        value for n, value in enumerate(convolution) if n != d
    ):
        fail(f"degree {d}: bounded convolution is not delta_d")

    # The boundary map kills A_0,B_0 and sends Z to zeta=1.  Identical chart
    # copies transport the same nonzero defect.  Taking the unspecified
    # source prolongation to be zero leaves that middle obstruction intact.
    def boundary(vector: tuple[Fraction, ...]) -> Fraction:
        return vector[2]

    if boundary(a_0) != 0 or boundary(b_0) != 0 or boundary(z_vector) != 1:
        fail(f"degree {d}: formal boundary map has the wrong values")
    first_polar = tuple(a_0[i] + z_vector[i] for i in range(3))
    endpoint = a_0
    defect = boundary(first_polar) - boundary(endpoint)
    chart_defects = (defect, defect)
    if chart_defects[0] == 0 or chart_defects[0] != chart_defects[1]:
        fail(f"degree {d}: formal defect is zero or not flatly transported")
    certificate_class = [defect * value for value in convolution]
    zero_prolongation = [Fraction(0) for _ in range(2 * d + 1)]
    if certificate_class[d] + zero_prolongation[d] != defect:
        fail(f"degree {d}: zero prolongation changed the middle obstruction")

    weights = torus_weights(d)
    if weights[d] != 0:
        fail(f"degree {d}: middle monomial has nonzero torus weight")
    if any(weight == 0 for n, weight in enumerate(weights) if n != d):
        fail(f"degree {d}: unexpected extra weight-zero monomial")

    # Every form with zero middle coefficient has the explicit primitive.
    zero_middle = [
        Fraction((n + 2) * (d + 3), n + 1) if n != d else Fraction(0)
        for n in range(2 * d + 1)
    ]
    primitive = primitive_of_zero_middle(d, zero_middle)
    if apply_torus_operator(d, primitive) != zero_middle:
        fail(f"degree {d}: explicit torus primitive failed")

    # The transported certificate class is not in the image.
    try:
        primitive_of_zero_middle(d, certificate_class)
    except RuntimeError:
        pass
    else:
        fail(f"degree {d}: nonzero middle certificate class was integrated")

    # A source correction with middle coefficient -zeta cancels the sole
    # obstruction; arbitrary noncentral entries are then integrable.
    correction = [Fraction(0) for _ in range(2 * d + 1)]
    correction[d] = -defect
    correction[0] = Fraction(3, 2)
    correction[-1] = Fraction(-5, 3)
    corrected = [
        certificate_class[n] + correction[n] for n in range(2 * d + 1)
    ]
    if corrected[d] != 0:
        fail(f"degree {d}: correction did not cancel middle residue")
    corrected_primitive = primitive_of_zero_middle(d, corrected)
    if apply_torus_operator(d, corrected_primitive) != corrected:
        fail(f"degree {d}: corrected class is not a torus coboundary")

    # In Laurent coordinate z=u/t after central regrading, the weights are
    # -2 times the exponents n-d.
    for n, weight in enumerate(weights):
        if weight != -2 * (n - d):
            fail(f"degree {d}: Laurent/tori weight mismatch")


def check_direct_free_guard() -> None:
    # Exact rational samples of D=A*T and C4=D*V+A*U*Z.
    samples = (
        (2, 3, 5, 7, 11),
        (2, 3, 0, 7, 11),  # Recovery does not localize at T or D.
        (-3, 4, 2, -5, 9),
        (
            Fraction(2, 3),
            Fraction(-5, 7),
            Fraction(11, 4),
            Fraction(3, 2),
            Fraction(-8, 5),
        ),
    )
    for a, u, t, v, z in samples:
        a = Fraction(a)
        u = Fraction(u)
        t = Fraction(t)
        v = Fraction(v)
        z = Fraction(z)
        if a == 0 or u == 0:
            fail("guard curvature coefficient must be nonzero")
        direct = a * t
        normal = direct * v + a * u * z
        if normal - direct * v != a * u * z:
            fail("direct-free triangular identity failed")
        recovered_z = (normal - direct * v) / (a * u)
        if recovered_z != z:
            fail("power-free triangular recovery failed")


def main() -> None:
    if not __debug__:
        raise SystemExit("refusing to run with -O: exact checks must stay enabled")
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-d", type=int, default=24)
    args = parser.parse_args()
    if args.max_d < 1:
        raise SystemExit("--max-d must be positive")
    for d in range(1, args.max_d + 1):
        check_degree(d)
    check_direct_free_guard()
    print(
        "PASS: bounded convolution, torus-Koszul cokernel, explicit "
        "primitives, normalized residue cancellation, and abstract/direct-free "
        f"guards for d=1..{args.max_d}"
    )


if __name__ == "__main__":
    main()
