#!/usr/bin/env python3
"""Exact audit of the target-fixed scalar-unit unary-lift no-go.

This checker audits the algebraic/Hasse--Schmidt part of the note.  The
minimum-support star deletion is an exact source argument recorded in prose.
Only the Python standard library is used.
"""

from fractions import Fraction
from math import factorial


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def hs_rows(h, alpha):
    """Positive-t coefficients on Q_1,...,Q_h."""
    rows = []
    for power in range(1, h + 1):
        row = [Fraction(0) for _ in range(h)]
        row[power - 1] = alpha
        if power < h:
            row[power] = power + 1
        rows.append(row)
    return rows


def descend(rows, h):
    """Back-substitute the upper triangular fixed-target system."""
    values = [Fraction(0) for _ in range(h + 1)]
    for power in range(h, 0, -1):
        diagonal = rows[power - 1][power - 1]
        upper = (
            rows[power - 1][power] * values[power + 1]
            if power < h
            else 0
        )
        values[power] = -upper / diagonal
    return values


def audit_divided_power_coefficient(h, k):
    """Check R*(q+tR)^[h-1] contributes (k+1)Q_(k+1)."""
    # Ordinary coefficient of q^(h-1-k) R^(k+1) in the response term.
    ordinary = Fraction(1, factorial(h - 1 - k) * factorial(k))
    # The same ordinary monomial inside Q_(k+1).
    q_basis = Fraction(
        1,
        factorial(h - 1 - k) * factorial(k + 1),
    )
    factor = ordinary / q_basis
    require(
        factor == k + 1,
        f"divided-power response factor failed at h={h}, k={k}",
    )
    return factor


def audit_activity_and_rescaling():
    alpha = Fraction(7, 3)
    for selected in range(3):
        diagonal = tuple(int(index == selected) for index in range(3))
        direct_scalar = alpha * diagonal[selected]
        activity = direct_scalar
        for entry in diagonal:
            activity *= entry
        require(activity == 0, "the unary cap unexpectedly became active")

    active_diagonal = (1, Fraction(-2, 5), Fraction(9, 4))
    # Select a=0.  In the scalar-unit chart s(K)=alpha*K_aa and
    # kappa_i(K)=K_ii, exactly as in the physical cap definition.
    active = alpha * active_diagonal[0]
    for entry in active_diagonal:
        active *= entry
    require(active != 0, "the active-cap control lost activity")

    # If q^[h]=sum c_i X_i, scaling the i-th colour at one chosen site by
    # c_i^-1 normalizes every target coefficient.  No root extraction occurs.
    target_coefficients = (Fraction(2, 3), Fraction(-5, 7), Fraction(11, 4))
    site_scales = tuple(1 / coefficient for coefficient in target_coefficients)
    normalized = tuple(
        coefficient * scale
        for coefficient, scale in zip(target_coefficients, site_scales)
    )
    require(normalized == (1, 1, 1), "local target rescaling failed")


def audit_target_motion_guard():
    """Without fixed target, a nonzero Q1 is compatible with transport."""
    h = 3
    alpha = Fraction(1)
    q_values = [Fraction(4), Fraction(1), Fraction(-2), Fraction(3)]
    transported_target = []
    for power in range(h + 1):
        coefficient = alpha * q_values[power]
        if power < h:
            coefficient += (power + 1) * q_values[power + 1]
        transported_target.append(coefficient)
    require(q_values[1] != 0, "target-motion guard lost its response")
    require(
        any(transported_target[1:]),
        "moving target accidentally became fixed",
    )
    # Defining Phi_t(X) by these coefficients makes the transported row exact;
    # hence target fixation, not algebra homomorphism alone, kills Q1.


def audit_terminal_guard():
    """Rows below terminal order alone allow Q1 != 0."""
    h = 3
    alpha = Fraction(1)
    # Solve the k=1,2 equations upward from a freely chosen Q3=1.
    q3 = Fraction(1)
    q2 = -3 * q3 / alpha
    q1 = -2 * q2 / alpha
    require(alpha * q1 + 2 * q2 == 0, "first nonterminal row failed")
    require(alpha * q2 + 3 * q3 == 0, "second nonterminal row failed")
    require(q1 != 0, "terminal guard no longer retains Q1")
    require(alpha * q3 != 0, "terminal row mutation was not detected")


def audit_factor_mutation():
    h = 7
    k = 3
    ordinary = Fraction(1, factorial(h - 1 - k) * factorial(k))
    q_basis = Fraction(1, factorial(h - 1 - k) * factorial(k + 1))
    correct = ordinary / q_basis
    require(correct == k + 1, "correct response factor changed")
    require(correct != k, "the missing +1 mutation was not detected")


def main():
    for h in range(2, 65):
        derived_factors = tuple(
            audit_divided_power_coefficient(h, k) for k in range(h)
        )

        for alpha in (Fraction(1), Fraction(-2), Fraction(7, 3)):
            rows = hs_rows(h, alpha)
            require(
                all(
                    rows[power - 1][power] == derived_factors[power]
                    for power in range(1, h)
                ),
                f"triangular rows disagree with the independent factor audit at h={h}",
            )
            require(
                all(
                    rows[row][column] == 0
                    for row in range(h)
                    for column in range(row)
                ),
                f"coefficient matrix ceased to be upper triangular at h={h}",
            )
            determinant = Fraction(1)
            for index in range(h):
                determinant *= rows[index][index]
            require(
                determinant == alpha**h and determinant != 0,
                f"triangular determinant failed at h={h}",
            )
            values = descend(rows, h)
            require(
                all(value == 0 for value in values[1:]),
                f"fixed-target descent retained a response at h={h}",
            )
            require(values[1] == 0, f"Q1 survived at h={h}")

    audit_activity_and_rescaling()
    audit_target_motion_guard()
    audit_terminal_guard()
    audit_factor_mutation()

    print("PASS: fixed-target unary translation forces Q1=...=Qh=0")
    print("PASS: unary E_aa cap is inactive; active diagonal control is nonzero")
    print("PASS: target-motion, terminal-row, and k+1 mutations are detected")


if __name__ == "__main__":
    main()
