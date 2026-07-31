#!/usr/bin/env python3
"""Exact lightweight audit of the scalar-unit oriented-curvature no-go.

The calculation is coefficient arithmetic in the formal divided-power
bases N_k=q^[h-1-k]r^[k] and M_k=q^[h-k]r^[k].  It does not construct a
site-algebra source.
"""

from fractions import Fraction
from math import comb


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def h_coefficients(h: int, denominator_shift: int = 1) -> list[Fraction]:
    """Coefficients of h_h in q/r divided-power order ell=0,...,h-2."""
    return [Fraction(1, ell + denominator_shift) for ell in range(h - 1)]


def theta_from_r_times_h(h: int, h_coeff: list[Fraction]) -> list[Fraction]:
    """Coefficients in N_k after ordinary multiplication by r."""
    answer = [Fraction(0) for _ in range(h)]
    for ell, coefficient in enumerate(h_coeff):
        answer[ell + 1] += (ell + 1) * coefficient
    return answer


def theta_from_binomial(h: int) -> list[Fraction]:
    """Coefficients of (q+r)^[h-1]-q^[h-1] in the N_k basis."""
    return [Fraction(0)] + [Fraction(1) for _ in range(h - 1)]


def curvature_sum_times_h(
    h: int, h_coeff: list[Fraction], q_factor: int = 2
) -> list[Fraction]:
    """Coefficients of c_h=(r-q_factor*q)h_h in the N_k basis."""
    answer = [Fraction(0) for _ in range(h)]
    for ell, coefficient in enumerate(h_coeff):
        answer[ell + 1] += (ell + 1) * coefficient
        answer[ell] -= q_factor * (h - 1 - ell) * coefficient
    return answer


def clean_unary_coefficients(h: int, first_k: int = 2) -> list[Fraction]:
    """Coefficients of u_h after the k=0 and k=1 source rows cancel."""
    return [Fraction(int(k >= first_k)) for k in range(h + 1)]


def multiply_q(h: int, coefficients: list[Fraction]) -> list[Fraction]:
    """Multiply a degree h-1 N-vector by q and return its M-vector."""
    answer = [Fraction(0) for _ in range(h + 1)]
    for k, coefficient in enumerate(coefficients):
        answer[k] += (h - k) * coefficient
    return answer


def multiply_r(h: int, coefficients: list[Fraction]) -> list[Fraction]:
    """Multiply a degree h-1 N-vector by r and return its M-vector."""
    answer = [Fraction(0) for _ in range(h + 1)]
    for k, coefficient in enumerate(coefficients):
        answer[k + 1] += (k + 1) * coefficient
    return answer


def add_scaled(*terms: tuple[Fraction, list[Fraction]]) -> list[Fraction]:
    width = len(terms[0][1])
    answer = [Fraction(0) for _ in range(width)]
    for scalar, vector in terms:
        require(len(vector) == width, "coefficient-vector width mismatch")
        for index, coefficient in enumerate(vector):
            answer[index] += scalar * coefficient
    return answer


def audit_order(
    h: int,
    *,
    denominator_shift: int = 1,
    q_factor: int = 2,
    unary_first_k: int = 2,
    star_sign: int = -1,
    conditional_target_r_factor: int = 2,
) -> None:
    require(h >= 3, "the no-go audit starts at h=3")

    h_coeff = h_coefficients(h, denominator_shift)
    theta_factor = theta_from_r_times_h(h, h_coeff)
    theta_binomial = theta_from_binomial(h)
    require(theta_factor == theta_binomial, "r*h_h != adjacent-power theta_h")

    # At one residual cell use the basis (q, BF, EC).  This first check
    # retains both endpoint orders before BF+EC is renamed r.  In the
    # normalized basis (q,r,x), where x=BF and EC=r-x, the two curvatures
    # q-x and q-r+x sum to 2q-r.
    forward_local = (1, star_sign, 0)
    backward_local = (1, 0, star_sign)
    require(forward_local == (1, -1, 0), "forward curvature sign changed")
    require(backward_local == (1, 0, -1), "backward curvature sign changed")
    local_sum = tuple(a + b for a, b in zip(forward_local, backward_local))
    require(local_sum == (2, -1, -1), "endpoint-ordered curvature sum changed")

    orientation_sum = (q_factor, star_sign, 0)  # q, r, x coefficients
    require(orientation_sum == (2, -1, 0), "oriented curvature sum changed")

    curvature = curvature_sum_times_h(h, h_coeff, q_factor)
    expected = [
        Fraction(int(k >= 1)) - Fraction(2 * (h - 1 - k), k + 1)
        for k in range(h)
    ]
    require(curvature == expected, "curvature-torsion coefficient formula")
    require(curvature[0] == -2 * (h - 1), "c_0 normalization")
    require(curvature[1] == 3 - h, "c_1 normalization")
    require(curvature[-1] == 1, "c_(h-1) normalization")

    # theta_h cannot be a scalar multiple of c_h: N_0 forces the scalar
    # to zero, while theta_h has N_1 coefficient one.
    require(curvature[0] != 0, "theta nonmembership lost its N_0 pivot")
    require(theta_binomial[0] == 0, "theta unexpectedly has an N_0 term")
    require(theta_binomial[1] == 1, "theta lost its N_1 witness")

    q_curvature = multiply_q(h, curvature)
    r_curvature = multiply_r(h, curvature)
    unary = clean_unary_coefficients(h, unary_first_k)
    target = [Fraction(0) for _ in range(h + 1)]
    target[1] = 1

    # Conditional carrier cancellation gives r=2q.  Audit the exact clean
    # and exceptional-target scalars in divided-power normalization.
    conditional_clean = sum(comb(h, k) * 2**k for k in range(2, h + 1))
    require(
        conditional_clean == 3**h - 1 - 2 * h,
        "conditional clean scalar",
    )
    require(conditional_clean != 0, "conditional contradiction vanished")

    # In the M-basis, q^[h] is M_0 and ordinary multiplication sends
    # q*q^[h-1] to h*M_0.  Thus after r=2q the exceptional target
    # q^[h]+r*q^[h-1] has the independently derived coefficient 1+2h.
    pure_q_h = [Fraction(1)] + [Fraction(0) for _ in range(h)]
    q_h_minus_one = [Fraction(1)] + [Fraction(0) for _ in range(h - 1)]
    conditional_target = add_scaled(
        (Fraction(1), pure_q_h),
        (
            Fraction(conditional_target_r_factor),
            multiply_q(h, q_h_minus_one),
        ),
    )
    expected_target = [Fraction(1 + 2 * h)] + [Fraction(0) for _ in range(h)]
    require(conditional_target == expected_target, "exceptional target scalar")
    require(conditional_target[0] != 0, "exceptional target scalar vanished")

    # If M_1=A*q*c_h+B*r*c_h+C*u_h, M_0, M_1, and M_h force
    # these unique values.  M_2 then gives the nonzero obstruction.
    require(q_curvature[0] != 0, "M_0 no longer forces A=0")
    coefficient_a = Fraction(0)
    coefficient_b = Fraction(1, 1) / r_curvature[1]
    require(unary[-1] != 0, "M_h no longer determines C")
    coefficient_c = -coefficient_b * r_curvature[-1] / unary[-1]
    candidate = add_scaled(
        (coefficient_a, q_curvature),
        (coefficient_b, r_curvature),
        (coefficient_c, unary),
    )

    require(coefficient_b == Fraction(-1, 2 * (h - 1)), "forced B value")
    require(coefficient_c == Fraction(h, 2 * (h - 1)), "forced C value")
    require(candidate[0] == target[0], "forced candidate misses M_0")
    require(candidate[1] == target[1], "forced candidate misses M_1")
    require(candidate[-1] == target[-1], "forced candidate misses M_h")
    obstruction = Fraction(3 * (h - 2), 2 * (h - 1))
    require(candidate[2] == obstruction, "M_2 obstruction formula")
    require(obstruction != 0, "M_2 obstruction vanished")
    require(candidate != target, "response M_1 incorrectly entered the ideal")


def mutation_rejected(**mutation: int) -> bool:
    try:
        for h in range(3, 18):
            audit_order(h, **mutation)
    except RuntimeError:
        return True
    return False


def main() -> None:
    for h in range(3, 129):
        audit_order(h)

    require(
        mutation_rejected(denominator_shift=2),
        "divided-power denominator mutation survived",
    )
    require(
        mutation_rejected(q_factor=1),
        "two-orientation factor mutation survived",
    )
    require(
        mutation_rejected(unary_first_k=3),
        "clean-unary cancellation mutation survived",
    )
    require(
        mutation_rejected(star_sign=1),
        "oriented star-sign mutation survived",
    )
    require(
        mutation_rejected(conditional_target_r_factor=-2),
        "exceptional-target sign mutation survived",
    )

    print(
        "intrinsic scalar-unit oriented-curvature torsion no-go: PASS; "
        "orders h=3..128, exact nonmembership and 5 mutations audited"
    )


if __name__ == "__main__":
    main()
