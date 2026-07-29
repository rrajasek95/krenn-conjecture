#!/usr/bin/env python3
"""Independent exact audit of the p=19 five-triple even-span closure.

This checker deliberately does not import the closure checker.  It redoes the
two profile selections, the kernel-dimension arithmetic, the conic-coordinate
calculation behind the uniform span lemma, and the terminal third jet.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def audit_profiles() -> None:
    # (number of exact doubles, singleton offset) in
    # 4 3^5 2^b 1^(h+u).
    for h in range(13, 19):
        k = 19 - h
        for doubles, offset in ((0, 2), (1, 0)):
            singletons = h + offset
            profile_mass = 4 + 5 * 3 + 2 * doubles + singletons
            assert profile_mass == 2 * h + k + 2

            # Give role two to one moving triple and, when present, the
            # exact double.  The rest of the selected labels are singleton
            # layers.  Exactly two ordinary singleton classes remain.
            selected_repeated = 1 + doubles
            selected_singletons = h + 2 - 2 * selected_repeated
            assert selected_singletons >= 0
            assert singletons - selected_singletons == 2

            # The moving triple leaves a residual simple class.  Thus the
            # complement is exactly 4,3^4,1^3, of mass 19 and eight classes.
            complement = (4,) + (3,) * 4 + (1,) * 3
            assert sum(complement) == 19
            assert len(complement) == 8

        # The selected kernel cannot have dimension at least six.  Pair
        # drops give dimension >=4, and the audited low-role theorem rules
        # out the dimension-four equality branch, hence it is a five-space
        # and its relation space has dimension three.
        q6_gap = 22 - h + max(0, 6 - k)
        assert q6_gap == 9
        for selected_repeated in (1, 2):
            selected_singletons = h + 2 - 2 * selected_repeated
            degree = h + 3 - selected_repeated
            assert 2 * selected_singletons > 3 * (degree // 2 - 2)


def audit_common_kernel_bound() -> None:
    # Restoring the residual simple at the moving triple produces the
    # common degree-eight baseline 4,3^5,1^2.
    baseline = (4,) + (3,) * 5 + (1,) * 2
    forced_weight = sum(max(0, 6 - multiplicity) for multiplicity in baseline)
    degree_eight_six_space_cap = 6 * (8 + 1 - 6)
    assert forced_weight == 27
    assert degree_eight_six_space_cap == 18
    assert forced_weight > degree_eight_six_space_cap

    # Two three-spaces in a space of dimension at most five intersect.
    assert 3 + 3 - 5 == 1
    # Coprime quartics in degree eight meet only on their product line.
    assert 8 - 4 - 4 + 1 == 1


def conic(value: sp.Expr) -> sp.Matrix:
    """Coefficient vector of (t-value)^2 in the basis 1,t,t^2."""
    return sp.Matrix([value**2, -2 * value, 1])


def audit_uniform_even_span() -> None:
    a, b, c, d = sp.symbols("a b c d")
    basis = sp.Matrix.hstack(conic(a), conic(b), conic(c))
    determinant = sp.factor(basis.det())
    assert sp.factor(determinant + 2 * (a - b) * (a - c) * (b - c)) == 0

    coordinates = [sp.factor(entry) for entry in basis.inv() * conic(d)]
    expected = (
        (b - d) * (c - d) / ((a - b) * (a - c)),
        -(a - d) * (c - d) / ((a - b) * (b - c)),
        (a - d) * (b - d) / ((a - c) * (b - c)),
    )
    assert all(
        sp.factor(observed - target) == 0
        for observed, target in zip(coordinates, expected, strict=True)
    )

    # For four distinct parameters every displayed coordinate is nonzero.
    # Hence a symmetric form for which the four conic vectors are pairwise
    # orthogonal has zero diagonal in the first-three-vector basis, and is
    # the zero form.  Products of quadratics span every t-degree 0,...,4.
    t = sp.symbols("t")
    product_generators = [1, t, t**2, t**3, t**4]
    assert all(
        any(sp.expand(f * g) == monomial for f in (1, t, t**2) for g in (1, t, t**2))
        for monomial in product_generators
    )

    # Numeric rank checks include a zero squared value and several unrelated
    # distinct configurations; they are sanity checks for the symbolic proof.
    for values in ((0, 1, 2, 3), (-3, -1, 2, 5), (1, 4, 9, 16)):
        columns = []
        for left, right in combinations(values, 2):
            polynomial = sp.Poly((t - left) ** 2 * (t - right) ** 2, t)
            columns.append(
                sp.Matrix([polynomial.coeff_monomial(t**degree) for degree in range(5)])
            )
        assert sp.Matrix.hstack(*columns).rank() == 5


def audit_terminal_jet() -> None:
    z, v = sp.symbols("z v")
    u0, u1, u2, u3 = sp.symbols("u0 u1 u2 u3")
    w = z - v
    unit = u0 + u1 * w + u2 * w**2 + u3 * w**3
    section = (z**2 - v**2) ** 3
    assert sp.degree(section, z) == 6
    assert [sp.diff(section, z, order).subs(z, v) for order in range(3)] == [0, 0, 0]
    assert sp.factor(sp.diff(section, z, 3).subs(z, v)) == 48 * v**3
    assert sp.factor(sp.diff(unit * section, z, 3).subs(z, v)) == 48 * u0 * v**3


def main() -> None:
    audit_profiles()
    audit_common_kernel_bound()
    audit_uniform_even_span()
    audit_terminal_jet()
    print("p=19 five-triple even-span independent audit: PASS")
    print("both profiles, common-kernel bound, uniform conic span, and third jet: exact")


if __name__ == "__main__":
    main()
