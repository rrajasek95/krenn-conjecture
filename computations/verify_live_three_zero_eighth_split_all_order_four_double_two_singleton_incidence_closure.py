#!/usr/bin/env python3
"""Exact audit of the complete all-order d=4 incidence closure."""

from __future__ import annotations

from pathlib import Path
import runpy

import sympy as sp


HERE = Path(__file__).resolve().parent

# Uniform d=4 kernel arithmetic.
d = 4
singletons = 2
repeated = 4
ambient_degree = 11 - d
assert (singletons, repeated, ambient_degree) == (2, 4, 7)
assert 10 - 2 * d == singletons

# If a singleton cubic divides K, divide it out.  The four exact repeated
# rows alone force weight 4*(4-2)=8 on a four-space in P_4, above cap four.
reduced_degree = ambient_degree - 3
forced_repeated_weight = repeated * (4 - 2)
wronskian_cap = 4 * (reduced_degree + 1 - 4)
assert (reduced_degree, forced_repeated_weight, wronskian_cap) == (4, 8, 4)
assert forced_repeated_weight > wronskian_cap

singleton_dimensions = (2, 3)
dimension_patterns = {
    (left, right)
    for left in singleton_dimensions
    for right in singleton_dimensions
}
assert dimension_patterns == {(2, 2), (2, 3), (3, 2), (3, 3)}

# Exact singleton-plane gcd alternatives.
normal_form_cases = []
for gcd_degree in range(5):
    for square_degree in range(1, 3):
        if gcd_degree + 2 * square_degree > 4:
            continue
        for order_at_other_double_root in range(gcd_degree + 1):
            if order_at_other_double_root == 1:
                continue
            if order_at_other_double_root == 0 and square_degree < 2:
                continue
            if (
                order_at_other_double_root >= 2
                and gcd_degree != order_at_other_double_root
            ):
                continue
            normal_form_cases.append(
                (gcd_degree, square_degree, order_at_other_double_root)
            )
assert normal_form_cases == [(0, 2, 0), (2, 1, 2)]

z, r, s = sp.symbols("z r s")


def singleton_factor(parameter):
    return (z - parameter) * (z + parameter) ** 2


f_r = singleton_factor(r)
f_s = singleton_factor(s)

# The two canonical f_s-lines in U_r and the two canonical f_r-lines in
# U_s have distinct residual linear factors under r != +/-s.
left_lines = (z - s, z + s)
right_lines = (z - r, z + r)
for left in left_lines:
    for right in right_lines:
        proportional_determinant = sp.Matrix(
            [
                [sp.Poly(left, z).coeff_monomial(z), sp.Poly(left, z).coeff_monomial(1)],
                [sp.Poly(right, z).coeff_monomial(z), sp.Poly(right, z).coeff_monomial(1)],
            ]
        ).det()
        assert sp.factor(proportional_determinant) in (
            r - s,
            r + s,
            -r - s,
            -r + s,
        )

# Coincident singleton planes would be f_r*f_s*P_1 and have no q_i member.
assert 3 + 3 <= ambient_degree
assert 3 + 3 + 2 > ambient_degree

# Missing-edge parity audit: normally four repeated pairs give eight roots;
# with the triple-zero edge removed, three repeated pairs plus the other
# singleton pair still give eight.
plane_parity_degree = 2 * (ambient_degree - 3) - 1
assert plane_parity_degree == 7
assert 2 * 4 == 8 > plane_parity_degree
assert 2 * 3 + 2 == 8 > plane_parity_degree

# Run the two exact deep-branch audits in isolated globals.
one_hyperplane_checker = (
    HERE
    / "verify_live_three_zero_eighth_split_all_order_four_double_two_singleton_one_hyperplane_closure.py"
)
two_hyperplane_checker = (
    HERE
    / "verify_live_three_zero_eighth_split_all_order_four_double_two_singleton_two_hyperplane_exclusion.py"
)
assert one_hyperplane_checker.is_file()
assert two_hyperplane_checker.is_file()
runpy.run_path(str(one_hyperplane_checker), run_name="_d4_one_hyperplane_audit")
runpy.run_path(str(two_hyperplane_checker), run_name="_d4_two_hyperplane_audit")


print("h=8 all-order d=4 incidence closure: PASS")
print("singleton dimensions (2,2), (2,3), (3,2), and (3,3): impossible")
print("zero singleton and unique triple-zero missing edge: exact")
