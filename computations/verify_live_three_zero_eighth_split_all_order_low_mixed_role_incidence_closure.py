#!/usr/bin/env python3
"""Exact audit of the all-order d=1,2,3 mixed-role incidence closure."""

from __future__ import annotations


def cubic_pencil_cap(polynomial_degree: int) -> int:
    """Gcd plus square-pencil ramification count, including a zero node."""
    bounds = []
    for gcd_degree in range(polynomial_degree - 1):
        square_degree = (polynomial_degree - gcd_degree) // 2
        assert square_degree >= 1
        bounds.append(gcd_degree + 2 * square_degree - 2)
    assert max(bounds) <= polynomial_degree - 2
    return max(bounds)


for d in (1, 2):
    singletons = 10 - 2 * d
    repeated = d
    layers = 10 - d
    ambient_degree = 11 - d
    assert singletons + repeated == layers

    # A singleton U_i/f_i pencil.  All other singleton edges are legal.
    first_degree = ambient_degree - 3
    other_singletons = singletons - 1

    # Worst parity count: omit a possible zero singleton from root pairs,
    # and allow the unique triple-zero missing edge to remove one repeated
    # neighbor only when the fixed singleton itself is zero.  Both cases
    # have the same or a larger number than the closed form below.
    zero_elsewhere_pairs = other_singletons - 1 + repeated
    fixed_zero_missing_pairs = other_singletons + repeated - 1
    minimum_nonzero_pairs = min(
        zero_elsewhere_pairs,
        fixed_zero_missing_pairs,
    )
    assert 2 * minimum_nonzero_pairs > 2 * first_degree - 1
    assert other_singletons > cubic_pencil_cap(first_degree)

    expected_first = {
        1: (7, 7, 7, 13, 5),
        2: (6, 5, 6, 11, 4),
    }[d]
    assert (
        first_degree,
        other_singletons,
        minimum_nonzero_pairs,
        2 * first_degree - 1,
        cubic_pencil_cap(first_degree),
    ) == expected_first

    # Any absorbed quadratic or cubic factor makes the remaining singleton
    # Wronskian weight exceed the four-space degree cap.
    for absorbed_cubics in range(singletons + 1):
        for absorbed_quadratics in range(repeated + 1):
            if absorbed_cubics + absorbed_quadratics == 0:
                continue
            reduced_degree = (
                ambient_degree
                - 3 * absorbed_cubics
                - 2 * absorbed_quadratics
            )
            if reduced_degree + 1 < 4:
                continue
            forced_weight = 3 * (singletons - absorbed_cubics)
            wronskian_cap = 4 * (reduced_degree - 3)
            deficit = forced_weight - wronskian_cap
            expected_deficit = (
                (-4 if d == 1 else -6)
                + 9 * absorbed_cubics
                + 8 * absorbed_quadratics
            )
            assert deficit == expected_deficit
            assert deficit > 0

    # Four singleton hyperplanes have zero intersection (degree 12>D), so
    # pair/triple intersections have dimensions two/one.  The pair quotient
    # produces the terminal singleton-only pencil.
    assert singletons >= 4
    assert 4 * 3 > ambient_degree
    assert 4 - 2 == 2 and 4 - 3 == 1
    second_degree = ambient_degree - 6
    terminal_cubics = singletons - 2
    terminal_nonzero_pairs = terminal_cubics - 1
    assert 2 * terminal_nonzero_pairs > 2 * second_degree - 1
    assert terminal_cubics > cubic_pencil_cap(second_degree)

    expected_second = {
        1: (4, 6, 5, 7, 2),
        2: (3, 4, 3, 5, 1),
    }[d]
    assert (
        second_degree,
        terminal_cubics,
        terminal_nonzero_pairs,
        2 * second_degree - 1,
        cubic_pencil_cap(second_degree),
    ) == expected_second


# At d=3 the generic first-pencill count is saturated, but the exact
# singleton row makes every gcd-absorbed cubic cost at least two degrees.
d = 3
singletons = 10 - 2 * d
repeated = d
ambient_degree = 11 - d
first_degree = ambient_degree - 3
other_singletons = singletons - 1
zero_elsewhere_pairs = other_singletons - 1 + repeated
fixed_zero_missing_pairs = other_singletons + repeated - 1
minimum_nonzero_pairs = min(
    zero_elsewhere_pairs,
    fixed_zero_missing_pairs,
)
assert (first_degree, other_singletons, minimum_nonzero_pairs) == (5, 3, 5)
assert 2 * minimum_nonzero_pairs > 2 * first_degree - 1
assert cubic_pencil_cap(first_degree) == other_singletons == 3

enhanced_cap = -1
for absorbed_cubic_nodes in range(other_singletons + 1):
    for gcd_degree in range(first_degree + 1):
        if 2 * absorbed_cubic_nodes > gcd_degree:
            continue
        for square_degree in range(1, first_degree + 1):
            if gcd_degree + 2 * square_degree > first_degree:
                continue
            capacity = absorbed_cubic_nodes + 2 * square_degree - 2
            enhanced_cap = max(enhanced_cap, capacity)
assert enhanced_cap == 2 < other_singletons

# The absorption deficit is positive except for exactly one absorbed
# quadratic and no absorbed cubic.  Too-small ambient spaces are already
# impossible for a four-space.
surviving_absorptions = []
for absorbed_cubics in range(singletons + 1):
    for absorbed_quadratics in range(repeated + 1):
        if absorbed_cubics + absorbed_quadratics == 0:
            continue
        reduced_degree = (
            ambient_degree
            - 3 * absorbed_cubics
            - 2 * absorbed_quadratics
        )
        if reduced_degree + 1 < 4:
            continue
        forced_weight = 3 * (singletons - absorbed_cubics)
        wronskian_cap = 4 * (reduced_degree - 3)
        deficit = forced_weight - wronskian_cap
        assert deficit == -8 + 9 * absorbed_cubics + 8 * absorbed_quadratics
        if deficit <= 0:
            surviving_absorptions.append(
                (absorbed_cubics, absorbed_quadratics, deficit)
            )
assert surviving_absorptions == [(0, 1, 0)]

# Three singleton hyperplanes meet nontrivially in a four-space, but their
# three coprime cubics have degree nine.  This exceeds D=8 with no
# absorption and D'=6 in the sole equality case.
triple_cubic_degree = 3 * 3
assert triple_cubic_degree > ambient_degree
assert triple_cubic_degree > ambient_degree - 2

# d=4 remains outside this theorem.
d = 4
assert (10 - 2 * d, 11 - d) == (2, 7)


print("h=8 all-order low mixed-role incidence closure: PASS")
print("d=1, d=2, and d=3 formal selections: impossible")
print("zero singleton, unique missing edge, gcd, and RH counts: exact")
print("d=4 remains outside the incidence closure")
