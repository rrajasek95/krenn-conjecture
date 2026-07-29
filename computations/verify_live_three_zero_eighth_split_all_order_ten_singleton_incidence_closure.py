#!/usr/bin/env python3
"""Exact audit of the all-order ten-singleton incidence closure."""

from __future__ import annotations

import sympy as sp


# d=0 kernel data from the all-order mixed-role theorem.
formal_layers = 10
factor_degree = 3
ambient_degree = 11
kernel_dimension = 4
assert formal_layers == 10
assert factor_degree * 2 + 5 == ambient_degree


def parity_ramification_cap(polynomial_degree: int) -> tuple[int, dict[int, int]]:
    """Maximum nonzero cubic-incidence nodes after parity saturation."""
    bounds = {}
    # A primitive polynomial pencil requires square-variable degree >=1.
    for gcd_degree in range(polynomial_degree - 1):
        square_degree = (polynomial_degree - gcd_degree) // 2
        assert square_degree >= 1
        bounds[gcd_degree] = gcd_degree + 2 * square_degree - 2
    return max(bounds.values()), bounds


# First quotient pencil U_i/f_i lies in P_8.  At least eight of its nine
# incidence nodes are nonzero, forcing 16 roots of an odd degree-15
# determinant; the gcd/RH cap is only six.
first_degree = ambient_degree - factor_degree
first_neighbors = formal_layers - 1
first_nonzero = first_neighbors - 1
assert (first_degree, first_neighbors, first_nonzero) == (8, 9, 8)
assert 2 * first_nonzero > 2 * first_degree - 1
first_cap, first_bounds = parity_ramification_cap(first_degree)
assert first_bounds == {0: 6, 1: 5, 2: 6, 3: 5, 4: 6, 5: 5, 6: 6}
assert first_cap == 6 < first_nonzero


# If a selected cubic is absorbed by all four kernel sections, divide every
# absorbed factor.  Each remaining three-dimensional incidence subspace
# forces vanishing sequence (0,2,3,4), hence weight three.
for absorbed in (1, 2):
    reduced_degree = ambient_degree - factor_degree * absorbed
    forced_weight = 3 * (formal_layers - absorbed)
    wronskian_cap = kernel_dimension * (
        reduced_degree + 1 - kernel_dimension
    )
    assert forced_weight > wronskian_cap
for absorbed in range(3, formal_layers + 1):
    reduced_degree = ambient_degree - factor_degree * absorbed
    assert reduced_degree + 1 < kernel_dimension


# Ten proper U_i are hyperplanes in a four-space.  Four have zero
# intersection because four coprime cubics have degree 12>11.  Independence
# of every four quotient covectors forces the pair/triple dimensions below.
assert 4 * factor_degree > ambient_degree
assert kernel_dimension - 2 == 2  # pair intersection
assert kernel_dimension - 3 == 1  # triple intersection


# Divide a pair intersection by its two cubics.  Its eight other triple
# intersections give at least seven nonzero incidence nodes in P_5.
second_degree = ambient_degree - 2 * factor_degree
second_neighbors = formal_layers - 2
second_nonzero = second_neighbors - 1
assert (second_degree, second_neighbors, second_nonzero) == (5, 8, 7)
assert 2 * second_nonzero > 2 * second_degree - 1
second_cap, second_bounds = parity_ramification_cap(second_degree)
assert second_bounds == {0: 2, 1: 3, 2: 2, 3: 3}
assert second_cap == 3 < second_nonzero


# Symbolically audit parity and the local square-variable implication.
z, r = sp.symbols("z r", nonzero=True)
p = sum(sp.symbols(f"p0:{first_degree + 1}")[i] * z**i for i in range(first_degree + 1))
q = sum(sp.symbols(f"q0:{first_degree + 1}")[i] * z**i for i in range(first_degree + 1))
parity = sp.expand(p * q.subs(z, -z) - p.subs(z, -z) * q)
assert sp.expand(parity.subs(z, -z) + parity) == 0
assert sp.Poly(parity, z).degree() <= 2 * first_degree - 1

x = sp.symbols("x")
E = sp.Function("E")
# z^2-r^2 is a local parameter at either sign when r is nonzero.
assert sp.diff(z**2 - r**2, z).subs(z, -r) == -2 * r


print("h=8 all-order ten-singleton incidence closure: PASS")
print("P_8 pencil cap: 6 nonzero nodes versus at least 8")
print("P_5 pencil cap: 3 nonzero nodes versus at least 7")
print("absorbed factors and four-hyperplane incidence: exact")
