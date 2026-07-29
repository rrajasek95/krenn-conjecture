#!/usr/bin/env python3
"""Exact audit for the p=18 five-triple overlap closure."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from verify_live_three_zero_higher_split_q5_boundary_census import (  # noqa: E402
    formal_selections,
)


def assert_zero(expr: sp.Expr) -> None:
    assert sp.factor(sp.together(expr)) == 0, sp.factor(sp.together(expr))


def wronskian(polys: list[sp.Expr], z: sp.Symbol) -> sp.Expr:
    size = len(polys)
    return sp.factor(
        sp.Matrix(
            [[sp.diff(poly, z, order) for poly in polys]
             for order in range(size)]
        ).det()
    )


EXPECTED_SELECTIONS = {
    0: {
        (0, 0, ((3, 5), (1, 3))),
        (1, 1, ((3, 4), (1, 6))),
    },
    1: {
        (0, 0, ((3, 5), (2, 1), (1, 1))),
        (1, 0, ((3, 5), (1, 3))),
        (1, 1, ((3, 4), (2, 1), (1, 4))),
        (2, 1, ((3, 4), (1, 6))),
    },
    2: {
        (1, 0, ((3, 5), (2, 1), (1, 1))),
        (1, 1, ((3, 4), (2, 2), (1, 2))),
        (2, 0, ((3, 5), (1, 3))),
        (2, 1, ((3, 4), (2, 1), (1, 4))),
    },
    3: {
        (2, 0, ((3, 5), (2, 1), (1, 1))),
        (2, 1, ((3, 4), (2, 2), (1, 2))),
    },
}


def counter_signature(parts: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(parts).items(), reverse=True))


def audit_family_and_selection_classification() -> None:
    admissible_b = []
    for b in range(12):
        u = 5 - 2 * b
        applicable = (
            u >= 2
            or (u >= 0 and 5 + b >= 1)
            or (u >= -2 and (b >= 2 or (5 >= 1 and b >= 1)))
        )
        if applicable:
            admissible_b.append(b)
    assert admissible_b == [0, 1, 2, 3]

    for h in range(13, 18):
        k = 18 - h
        for b in admissible_b:
            u = 5 - 2 * b
            profile = (3,) * 5 + (2,) * b + (1,) * (h + u)
            assert sum(profile) == 2 * h + k + 2
            observed = {
                (
                    selection.d,
                    selection.selected_triples,
                    counter_signature(selection.complement),
                )
                for selection in formal_selections(profile, h, 18)
            }
            assert observed == EXPECTED_SELECTIONS[b]

            # The convenient selection used in the proof is present.
            if b <= 2:
                assert (b, 0, ((3, 5), (1, 3))) in observed
            else:
                assert (2, 0, ((3, 5), (2, 1), (1, 1))) in observed


def audit_three_simple_relation_space() -> None:
    z, a, b, c = sp.symbols("z a b c")
    basis = [
        (z - a) ** 2 * (z - b) ** 2,
        (z - a) ** 2 * (z - c) ** 2,
        (z - b) ** 2 * (z - c) ** 2,
    ]
    wr = wronskian(basis, z)
    target = (z - a) ** 2 * (z - b) ** 2 * (z - c) ** 2
    assert wr != 0
    assert_zero(sp.diff(wr / target, z))

    # At a, the nonzero section is J_a^2 and determines the Robin row.
    section = (z - b) ** 2 * (z - c) ** 2
    beta = -sp.diff(section, z).subs(z, a) / section.subs(z, a)
    assert_zero(beta + 2 / (a - b) + 2 / (a - c))


def audit_singleton_exchange() -> None:
    z, mu, q, x, a, b, c, r, y, k = sp.symbols(
        "z mu q x a b c r y k"
    )
    common = (z + mu) ** k * (z + q) ** 2 * (z + y) / (z - x) ** 4

    # Base complement {a,b,c}, with r selected.
    base_unit_at_b = common * (z + r) / ((z - a) ** 2 * (z - c) ** 2)
    base_beta = -2 / (b - a) - 2 / (b - c)
    base_log = sp.diff(sp.log(base_unit_at_b), z).subs(z, b)

    # Swap a and r.  The common complementary root b survives.
    new_unit_at_b = common * (z + a) / ((z - r) ** 2 * (z - c) ** 2)
    new_beta = -2 / (b - r) - 2 / (b - c)
    new_log = sp.diff(sp.log(new_unit_at_b), z).subs(z, b)

    base_reduced = sp.factor(base_log - base_beta)
    new_reduced = sp.factor(new_log - new_beta)
    assert_zero(
        (new_reduced - base_reduced)
        - (1 / (b + a) - 1 / (b + r))
    )
    assert_zero(
        (1 / (b + a) - 1 / (b + r))
        - (r - a) / ((b + a) * (b + r))
    )


def audit_simple_double_relation_space() -> None:
    z, a, v = sp.symbols("z a v")
    l0 = sp.Integer(1)
    l1 = (2 * a + v) / 3
    l2 = (a**2 + 2 * a * v) / 3
    l3 = a**2 * v
    basis = [
        1 - l0 * z**3 / l3,
        z - l1 * z**3 / l3,
        z**2 - l2 * z**3 / l3,
    ]
    wr = wronskian(basis, z)
    target = (z - a) ** 2 * (z - v)
    assert wr != 0
    assert_zero(sp.diff(wr / target, z))

    beta = 3 / (v - a)
    robin = sp.Matrix(
        [beta, 1 + beta * a, 2 * a + beta * a**2,
         3 * a**2 + beta * a**3]
    )
    functional = sp.Matrix([l0, l1, l2, l3])
    for coordinate in robin - beta * functional:
        assert_zero(coordinate)


def audit_double_exchange() -> None:
    z, mu, x, a, u, v, w, y, k = sp.symbols(
        "z mu x a u v w y k"
    )
    common = (z + mu) ** k * (z + w) ** 2 * (z + y) / (z - x) ** 4

    base_unit = common * (z + u) ** 2 / (z - v) ** 3
    base_beta = 3 / (v - a)
    base_log = sp.diff(sp.log(base_unit), z).subs(z, a)

    new_unit = common * (z + v) ** 2 / (z - u) ** 3
    new_beta = 3 / (u - a)
    new_log = sp.diff(sp.log(new_unit), z).subs(z, a)

    base_reduced = sp.factor(base_log - base_beta)
    new_reduced = sp.factor(new_log - new_beta)
    assert_zero(
        (new_reduced - base_reduced)
        - (2 / (a + v) - 2 / (a + u))
    )
    assert_zero(
        (2 / (a + v) - 2 / (a + u))
        - 2 * (u - v) / ((a + u) * (a + v))
    )


def main() -> None:
    audit_family_and_selection_classification()
    audit_three_simple_relation_space()
    audit_singleton_exchange()
    audit_simple_double_relation_space()
    audit_double_exchange()
    print("PASS: p=18 five-triple overlap closure audited exactly")


if __name__ == "__main__":
    main()
