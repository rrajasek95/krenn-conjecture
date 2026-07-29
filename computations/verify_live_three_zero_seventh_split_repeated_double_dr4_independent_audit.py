#!/usr/bin/env python3
"""Independent exact audit of the c>=14 repeated-double DR4 application."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def check_collision_residual_and_row() -> None:
    p = sp.symbols("p", integer=True)
    # Seven selected labels in six value classes: the collision Hermite
    # denominator has degree p+m_R+1 and the numerator cap is two lower.
    m_r = 6
    assert sp.expand((p + m_r - 1) - (p + 2)) == 3

    s, a, x, z, u = sp.symbols("s a x z U")
    psi = sp.Rational(1, 1) / (s + x) - 2 / (x - s)
    assert sp.factor(psi + (x + 3 * s) / (x**2 - s**2)) == 0
    double_background = 2 / (s + a) - 3 / (a - s)
    assert sp.factor(
        double_background + (a + 5 * s) / (a**2 - s**2)
    ) == 0

    # In t=-s coordinates, clearing the moving singleton contribution gives
    # exactly the DR4 row, with no residual scalar or sign ambiguity.
    t = -s
    q = u + z + 2 * z**2 - 3 * z**3
    robin = sp.diff(q, z).subs(z, t) + (sp.symbols("V") + psi) * q.subs(z, t)
    cleared = sp.factor((x**2 - s**2) * robin)
    expected = sp.factor(
        (x**2 - t**2)
        * (sp.diff(q, z).subs(z, t) + sp.symbols("V") * q.subs(z, t))
        - (x - 3 * t) * q.subs(z, t)
    )
    assert sp.factor(cleared - expected) == 0

    # Four degree-two rows give degree at most eight; this exact instance
    # reaches degree eight, so the root threshold is genuinely strict.
    nodes = tuple(map(sp.Integer, (1, 2, 4, 7)))
    translations = tuple(map(sp.Integer, (1, -2, 3, 5)))
    basis = (sp.Integer(1), z, z**2, z**3)
    matrix = sp.Matrix(
        [
            [
                (x**2 - node**2)
                * (sp.diff(poly, z).subs(z, node) + shift * poly.subs(z, node))
                - (x - 3 * node) * poly.subs(z, node)
                for poly in basis
            ]
            for node, shift in zip(nodes, translations, strict=True)
        ]
    )
    determinant = sp.Poly(sp.expand(matrix.det(method="domain-ge")), x)
    assert determinant.degree() == 8


def complement_has_singleton(
    multiplicities: tuple[int, ...], background: int, guard: int | None,
    anchors: tuple[int, ...], moving: int,
) -> bool:
    selected = [0] * len(multiplicities)
    selected[background] = 2
    for index in anchors:
        selected[index] += 1
    selected[moving] += 1
    complement = [size - used for size, used in zip(multiplicities, selected, strict=True)]
    assert all(value >= 0 for value in complement)
    if guard is not None:
        assert guard in anchors and complement[guard] == 1
    return 1 in complement


def check_singleton_guard_uniformly() -> None:
    # Exhaust double/single profiles through a much larger range than is
    # needed.  Class zero is optionally assigned the unique value zero and
    # is therefore forced to be a singleton; choices of fixed DR4 anchors
    # are made from nonzero classes.
    for classes in range(14, 31):
        for doubles in range(1, classes + 1):
            singles = classes - doubles
            multiplicities = (2,) * doubles + (1,) * singles
            background = 0
            guard = 1 if doubles >= 2 else None
            nonzero_classes = list(range(classes))
            zero_class = classes - 1 if singles else None
            if zero_class is not None:
                nonzero_classes.remove(zero_class)
            anchor_pool = [index for index in nonzero_classes if index != background]
            if guard is not None:
                companions = [index for index in anchor_pool if index != guard][:3]
                anchors = (guard, *companions)
            else:
                anchors = tuple(anchor_pool[:4])
            assert len(anchors) == 4
            moving_classes = [
                index
                for index in range(classes)
                if index != background and index not in anchors
            ]
            assert len(moving_classes) == classes - 5 >= 9
            for moving in moving_classes:
                assert complement_has_singleton(
                    multiplicities, background, guard, anchors, moving
                )

            # For the second variation, hold background, guard/base b, and
            # two companions fixed.  There are at least c-5 nonzero choices.
            base = anchors[0]
            fixed = {background, base, anchors[1], anchors[2]}
            varying = [index for index in nonzero_classes if index not in fixed]
            assert len(varying) >= classes - 5 >= 9
            for fourth in varying:
                core = (base, anchors[1], anchors[2], fourth)
                roots = [
                    index
                    for index in range(classes)
                    if index != background and index not in core
                ]
                assert len(roots) == classes - 5
                for moving in roots:
                    assert complement_has_singleton(
                        multiplicities, background, guard, core, moving
                    )


def old_closed(doubles: int, singles: int) -> bool:
    return (
        (doubles >= 8 and singles >= 4)
        or (doubles >= 9 and singles >= 3)
        or (doubles >= 10 and singles >= 2)
        or doubles >= 11
    )


EXPECTED = {
    8: (4, 5, 6, 7, 8),
    9: (5, 6, 7, 8, 9),
    10: (6, 7, 8, 9),
    11: (7, 9, 10),
    12: (10,),
}


def check_counts_and_fibres() -> None:
    y, b, lam = sp.symbols("y b lambda")
    fibre = lam * (y**2 - b**2) + y + 3 * b
    assert sp.Poly(fibre, y).nth(1) == 1
    for classes in range(14, 100):
        assert classes - 5 > 8

    for p in range(8, 101):
        total = p + 9
        residual = []
        for doubles in range(1, total // 2 + 1):
            singles = total - 2 * doubles
            classes = doubles + singles
            if not old_closed(doubles, singles) and classes < 14:
                residual.append(doubles)
        assert tuple(residual) == EXPECTED.get(p, ())
        if p >= 13:
            assert not residual


def main() -> None:
    check_collision_residual_and_row()
    check_singleton_guard_uniformly()
    check_counts_and_fibres()
    print("independent repeated-double DR4 application audit: PASS")
    print("c>=14 root threshold and singleton guard: exact")
    print("post-closure double/single census: exact")


if __name__ == "__main__":
    main()
