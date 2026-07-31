#!/usr/bin/env python3
"""Exact audit of the unipotent response-transgression criterion."""

from fractions import Fraction
from math import factorial


Q = Fraction


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def delta_coefficients(coefficients, response_scale=Q(0)):
    """Apply delta to sum_j coefficients[j] R^[j] q^[h-j]."""
    out = [Q(0) for _ in coefficients]
    for j, value in enumerate(coefficients):
        out[j] += j * response_scale * value
        if j + 1 < len(coefficients):
            out[j + 1] += (j + 1) * value
    return out


def selected_row(h, alpha):
    row = [Q(0) for _ in range(h + 1)]
    row[0] = alpha
    row[1] = Q(1)
    return row


def expected_derivative_row(h, alpha, order):
    row = [Q(0) for _ in range(h + 1)]
    if order < h:
        row[order] = factorial(order) * alpha
        row[order + 1] = factorial(order + 1)
    else:
        row[h] = factorial(h) * alpha
    return row


def audit_triangular_chain():
    for h in range(1, 13):
        alpha = Q(2 * h + 1, h + 2)
        row = selected_row(h, alpha)
        for order in range(h + 1):
            require(
                row == expected_derivative_row(h, alpha, order),
                f"derivative row mismatch at h={h}, order={order}",
            )
            row = delta_coefficients(row)

        # Downward substitution with arbitrary fixed target T.
        target = Q(3 * h - 1, h + 4)
        values = [Q(0) for _ in range(h + 1)]
        values[0] = target / alpha
        for order in range(1, h + 1):
            derivative = expected_derivative_row(h, alpha, order)
            require(
                sum(c * v for c, v in zip(derivative, values)) == 0,
                "the constructed clean packet violates a derivative row",
            )
        require(
            alpha * values[0] + values[1] == target,
            "the zeroth source row changed",
        )
        effective = sum(
            alpha ** (h - j) * values[j] for j in range(h + 1)
        )
        require(
            effective == alpha ** (h - 1) * target,
            "the clean identity has the wrong normalization",
        )


def audit_h3_factorials():
    alpha = Q(7, 3)
    rows = []
    row = selected_row(3, alpha)
    for _ in range(4):
        rows.append(row)
        row = delta_coefficients(row)
    require(
        rows
        == [
            [alpha, Q(1), Q(0), Q(0)],
            [Q(0), alpha, Q(2), Q(0)],
            [Q(0), Q(0), 2 * alpha, Q(6)],
            [Q(0), Q(0), Q(0), 6 * alpha],
        ],
        "the h=3 factorial chain changed",
    )


def audit_scaled_response_guard():
    alpha = Q(1)
    response_scale = Q(-1, 2)
    values = [Q(4), Q(-4), Q(1), Q(0)]
    row = selected_row(3, alpha)
    for order in range(8):
        require(
            sum(c * v for c, v in zip(row, values)) == 0,
            f"scaled-response guard fails at derivative {order}",
        )
        row = delta_coefficients(row, response_scale)
    require(
        alpha * values[2] + values[3] == 1,
        "the scaled-response mutation no longer leaves a clean-tail defect",
    )


def main():
    audit_triangular_chain()
    audit_h3_factorials()
    audit_scaled_response_guard()
    print("PASS: unipotent transgression is triangular for 1 <= h <= 12")
    print("PASS: h=3 derivative factors are 1, 2, 6")
    print("PASS: scalable-response resonance leaves clean-tail defect 1")


if __name__ == "__main__":
    main()
