#!/usr/bin/env python3
"""Exact lightweight audit of the scalar-unit 80-of-81-row guard."""

from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import runpy


BASE = runpy.run_path(str(Path(__file__).with_name(
    "verify_uncontracted_four_cut_scalar_unit_full_isotropic_packet_guard.py"
)))
add = BASE["add"]
scale = BASE["scale"]
multiply = BASE["multiply"]
monomer = BASE["monomer"]
pure = BASE["pure"]
build_guard = BASE["build_guard"]
flatten_linear = BASE["flatten_linear"]
rational_rank = BASE["rational_rank"]


def full_difference(z, z2, z3, t, v, x, y, direct_a, a, b, c, d):
    """Left minus right in the m=5 four-cut row."""
    u_cd = int((c, d) == (2, 2))
    tv = multiply(t[c], v[d])
    xy = multiply(x[a], y[b])
    left = add(
        scale(z3, direct_a[a][b] * u_cd),
        scale(multiply(tv, z2), direct_a[a][b]),
        scale(multiply(xy, z2), u_cd),
        multiply(multiply(xy, tv), z),
    )
    right = pure(a) if a == b == c == d else Counter()
    return add(left, scale(right, -1))


def audit():
    z, basic_t, basic_v, x, y, _ = build_guard()
    t = basic_t[:2] + (monomer(3, 2),)
    v = basic_v[:2] + (monomer(3, 2),)

    z2 = scale(multiply(z, z), Fraction(1, 2))
    z3 = scale(multiply(z, z2), Fraction(1, 3))
    assert z2 and not z3

    assert rational_rank([flatten_linear(row) for row in t]) == 3
    assert rational_rank([flatten_linear(row) for row in v]) == 3
    assert multiply(t[0], v[0]) and multiply(t[1], v[1])
    assert not multiply(t[2], v[2])
    assert multiply(x[0], y[0]) and multiply(x[1], y[1])
    assert not multiply(x[2], y[2])

    # Zero plus the nine matrix units spans every arbitrary direct block.
    direct_blocks = [[[0] * 3 for _ in range(3)]]
    for a, b in product(range(3), repeat=2):
        block = [[0] * 3 for _ in range(3)]
        block[a][b] = 1
        direct_blocks.append(block)

    checked = 0
    for direct_a in direct_blocks:
        for a, b, c, d in product(range(3), repeat=4):
            difference = full_difference(
                z, z2, z3, t, v, x, y, direct_a, a, b, c, d
            )
            expected = scale(pure(2), -1) if (a, b, c, d) == (2, 2, 2, 2) else Counter()
            assert difference == expected
            checked += 1
    return checked


if __name__ == "__main__":
    rows = audit()
    print(
        "scalar-unit 80-of-81 injective guard: PASS; "
        f"audited rows={rows}; unique residual=(2,2;2,2)=-X_2"
    )
