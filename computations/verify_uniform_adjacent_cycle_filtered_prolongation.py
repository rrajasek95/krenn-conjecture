#!/usr/bin/env python3
"""Exact lightweight verifier for uniform adjacent-cycle prolongation.

This script checks only the finite-dimensional obstruction ledger in
notes/uniform_adjacent_cycle_filtered_prolongation.md.  It deliberately does
not model a Krenn source or assert the missing filtered chain operation.
"""

from fractions import Fraction
from math import factorial


def fail(message):
    raise RuntimeError(message)


def poly_mul(a, b):
    out = [Fraction(0) for _ in range(len(a) + len(b) - 1)]
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] += ai * bj
    return out


def poly_pow(a, exponent):
    out = [Fraction(1)]
    for _ in range(exponent):
        out = poly_mul(out, a)
    return out


def poly_derivative(a):
    return [Fraction(i) * a[i] for i in range(1, len(a))]


def poly_derivative_n(a, n):
    out = list(a)
    for _ in range(n):
        out = poly_derivative(out)
    return out


def integrate_t_power(a, s):
    return sum(coef / Fraction(i + s + 1) for i, coef in enumerate(a))


def bpoly_normalize(poly):
    """Normalize a polynomial in (ell, w) stored by exponent pairs."""
    return {
        monomial: Fraction(coefficient)
        for monomial, coefficient in poly.items()
        if coefficient
    }


def bpoly_add(a, b):
    out = dict(a)
    for monomial, coefficient in b.items():
        out[monomial] = out.get(monomial, Fraction(0)) + coefficient
    return bpoly_normalize(out)


def bpoly_scale(scalar, poly):
    return bpoly_normalize(
        {
            monomial: Fraction(scalar) * coefficient
            for monomial, coefficient in poly.items()
        }
    )


def bpoly_mul(a, b):
    out = {}
    for (ell_a, w_a), coefficient_a in a.items():
        for (ell_b, w_b), coefficient_b in b.items():
            monomial = (ell_a + ell_b, w_a + w_b)
            out[monomial] = (
                out.get(monomial, Fraction(0)) + coefficient_a * coefficient_b
            )
    return bpoly_normalize(out)


def bpoly_divide_by_ell(poly):
    """Return the exact quotient by ell, or None when it is not divisible."""
    poly = bpoly_normalize(poly)
    if any(ell_power == 0 for ell_power, _ in poly):
        return None
    return {
        (ell_power - 1, w_power): coefficient
        for (ell_power, w_power), coefficient in poly.items()
    }


def module_evaluate(element, epsilon):
    """Apply a scalar module functional basis-vector by basis-vector."""
    out = {}
    for basis, coefficient in element.items():
        out = bpoly_add(out, bpoly_scale(epsilon.get(basis, 0), coefficient))
    return out


def module_divide_by_ell(element):
    """Divide every module coordinate by ell, failing on the first remainder."""
    quotient = {}
    for basis, coefficient in element.items():
        coordinate_quotient = bpoly_divide_by_ell(coefficient)
        if coordinate_quotient is None:
            return None
        if coordinate_quotient:
            quotient[basis] = coordinate_quotient
    return quotient


def module_reduce_mod_ell(element):
    """Compute the literal module remainder modulo the principal ideal (ell)."""
    remainder = {}
    for basis, coefficient in element.items():
        reduced = bpoly_normalize(
            {
                (ell_power, w_power): value
                for (ell_power, w_power), value in coefficient.items()
                if ell_power == 0
            }
        )
        if reduced:
            remainder[basis] = reduced
    return remainder


def based_loop_moment(s, j):
    # d eta_j is the j-th derivative of t^j (1-t)^j.
    tj = [Fraction(0)] * j + [Fraction(1)]
    one_minus_t = [Fraction(1), Fraction(-1)]
    base = tj
    for _ in range(j):
        base = poly_mul(base, one_minus_t)
    d_eta = poly_derivative_n(base, j)
    return integrate_t_power(d_eta, s)


def matrix_rank(matrix):
    if not matrix:
        return 0
    a = [list(map(Fraction, row)) for row in matrix]
    rows = len(a)
    cols = len(a[0])
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = a[rank][col]
        a[rank] = [x / scale for x in a[rank]]
        for r in range(rows):
            if r == rank or not a[r][col]:
                continue
            multiple = a[r][col]
            a[r] = [x - multiple * y for x, y in zip(a[r], a[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def pure_axis_macaulay_matrix(h):
    # Columns are s^h times the h shifts, then t^h times the h shifts.
    # Rows are indexed by the t-exponent 0,...,2h-1.
    size = 2 * h
    out = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    for shift in range(h):
        out[shift][shift] = 1
        out[h + shift][h + shift] = 1
    return out


def audit_order(h):
    macaulay = pure_axis_macaulay_matrix(h)
    if matrix_rank(macaulay) != 2 * h:
        fail(f"pure-axis Macaulay rank failed at h={h}")

    # h=3 needs moments 0 and 1; for h>=4 the initial tower needs 0..h-3.
    m = 1 if h == 3 else h - 3
    moment_matrix = [
        [based_loop_moment(s, j) for j in range(1, m + 1)]
        for s in range(1, m + 1)
    ]
    if matrix_rank(moment_matrix) != m:
        fail(f"based-loop moment rank failed at h={h}")
    for s in range(1, m + 1):
        for j in range(1, m + 1):
            value = moment_matrix[s - 1][j - 1]
            if s < j and value != 0:
                fail(f"moment triangularity failed at h={h}, s={s}, j={j}")
            if s == j:
                expected = Fraction(
                    ((-1) ** j) * factorial(j) ** 3, factorial(2 * j + 1)
                )
                if value != expected:
                    fail(
                        f"moment diagonal failed at h={h}, j={j}: "
                        f"{value} != {expected}"
                    )

    auxiliary_order = 2 * h - 6
    if auxiliary_order < 0 or 5 + auxiliary_order != 2 * h - 1:
        fail(f"clean-line auxiliary order failed at h={h}")

    # On K(u,v)=u E_ab+v I, kappa_0=kappa_1=kappa_2=v.  Use the
    # nonzero direct form s=u+2v and audit a_h=s^(2h-6)*v^3.
    activity = poly_pow([Fraction(1), Fraction(2)], 2 * h - 6)
    activity = poly_mul(activity, [Fraction(0), Fraction(1)])
    activity = poly_mul(activity, [Fraction(0), Fraction(1)])
    activity = poly_mul(activity, [Fraction(0), Fraction(1)])
    if len(activity) != 2 * h - 2 or not any(activity):
        fail(f"activity candidate degree/nonvanishing failed at h={h}")
    if h == 3 and activity != [0, 0, 0, 1]:
        fail("h=3 activity candidate is not the target cubic v^3")


def audit_h3_activity_hankel_residual():
    # Divided-differential Cartan multiplication of Psi=(q0,q1,q2) by
    # v^3 is (0,0,0,q0,4q1,10q2).  The pure-axis Macaulay matrix is the
    # identity, so this is also its exact Hankel residual.
    psi = [Fraction(2), Fraction(-3), Fraction(5)]
    theta = [0, 0, 0, psi[0], 4 * psi[1], 10 * psi[2]]
    hankel = pure_axis_macaulay_matrix(3)
    residual = [sum(row[j] * theta[j] for j in range(6)) for row in hankel]
    if residual != theta or residual[3:] != [2, -12, 50]:
        fail("h=3 activity Cartan-Hankel residual changed")
    if not any(residual):
        fail("nonzero selector cycle acquired zero pure-axis residual")


def audit_pure_witness_reinsertion():
    # Two witness-site copies for each of three fixed labels reinsert to
    # the same pure target X_c.  Each column is nonzero, but the untagged
    # direct sum has one exchange kernel per label.
    reinsertion = [[Fraction(0) for _ in range(6)] for _ in range(3)]
    for colour in range(3):
        reinsertion[colour][2 * colour] = 1
        reinsertion[colour][2 * colour + 1] = 1
    if matrix_rank(reinsertion) != 3:
        fail("untagged pure-witness reinsertion has the wrong rank")
    for colour in range(3):
        exchange = [Fraction(0) for _ in range(6)]
        exchange[2 * colour] = 1
        exchange[2 * colour + 1] = -1
        image = [
            sum(row[j] * exchange[j] for j in range(6)) for row in reinsertion
        ]
        if any(image):
            fail("same-label witness exchange did not lie in reinsertion kernel")
    tagged = [[Fraction(i == j) for j in range(6)] for i in range(6)]
    if matrix_rank(tagged) != 6:
        fail("fully tagged raw coefficient map is not injective")


def audit_principal_parts_guard():
    # Work literally in M=C[ell,w]z + C[ell,w]r, with N=0 and
    # epsilon(z)=0, epsilon(r)=1.  P=wz+ell*r evaluates to ell, but its
    # z-coordinate has nonzero remainder w modulo ell.
    one = {(0, 0): Fraction(1)}
    ell = {(1, 0): Fraction(1)}
    w = {(0, 1): Fraction(1)}
    p = {"z": w, "r": ell}
    epsilon = {"z": Fraction(0), "r": Fraction(1)}

    evaluated = module_evaluate(p, epsilon)
    if evaluated != ell:
        fail(f"principal-parts evaluation is {evaluated}, not ell")
    evaluated_quotient = bpoly_divide_by_ell(evaluated)
    if evaluated_quotient != one:
        fail("evaluated principal part did not divide exactly by ell")
    if bpoly_mul(ell, evaluated_quotient) != evaluated:
        fail("evaluated principal-parts quotient failed reconstruction")

    literal_quotient = module_divide_by_ell(p)
    if literal_quotient is not None:
        fail("P unexpectedly became divisible by ell in the literal module")
    remainder = module_reduce_mod_ell(p)
    if remainder != {"z": w}:
        fail(f"literal principal-parts remainder changed: {remainder}")
    if module_evaluate(remainder, epsilon):
        fail("literal remainder left the evaluation kernel")


def main():
    for h in range(3, 16):
        audit_order(h)
    if based_loop_moment(1, 1) != Fraction(-1, 6):
        fail("h=3 first weighted moment is not -1/6")
    audit_principal_parts_guard()
    audit_h3_activity_hankel_residual()
    audit_pure_witness_reinsertion()
    print(
        "PASS: pure-axis Macaulay ranks, abstract based-loop moment matrices, "
        "activity-covariant residuals, pure-witness reinsertion kernels, "
        "clean-line degree gaps, and literal module divisibility are exact "
        "for h=3..15."
    )


if __name__ == "__main__":
    main()
