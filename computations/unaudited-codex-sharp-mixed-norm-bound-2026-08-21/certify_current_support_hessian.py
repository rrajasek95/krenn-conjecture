#!/usr/bin/env python3
"""Outward constrained Hessian for the 18-cell two-parameter active set."""

from __future__ import annotations

from itertools import product
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import integrate_negative_multiray_family as family  # noqa: E402
import integrate_global_normal_counterfamily as current  # noqa: E402
from certify_negative_family_global_min import I, down, up  # noqa: E402


VBOX = (0.20523, 0.20526)
WBOX = (0.19294, 0.19297)
V_COEFF = {0: (0, 1, 0, 0), 1: (1, 0, 0, 0), 2: (0, 0, 0, 0)}
W_COEFF = current.W_COEFFICIENTS


def root_bracket(energies):
    lo, hi = max(energies), max(1.0, max(energies) + 1)

    def equation(rho):
        value = 1.0
        for energy in energies:
            value *= rho - energy
        return value - 1

    for _ in range(64):
        middle = (lo + hi) / 2
        if equation(middle) < 0:
            lo = middle
        else:
            hi = middle
    return down(lo), up(hi)


def source_box():
    v, w = I(*VBOX), I(*WBOX)
    corners = tuple(product(VBOX, WBOX))
    source = {}
    for colour, layer in family.LAYERS.items():
        corner_energies = [current.energies(colour, a, b) for a, b in corners]
        roots = [root_bracket(values) for values in corner_energies]
        gaps = []
        for index in range(4):
            values = []
            for root, energy in zip(roots, corner_energies):
                values.extend((root[0] - energy[index], root[1] - energy[index]))
            gaps.append(I(down(min(values)), up(max(values))))
        denominator = sum((I(1) / gap for gap in gaps), I(0))
        av = [float(x) for x in V_COEFF[colour]]
        aw = [float(x) for x in W_COEFF[colour]]
        rv = sum((a / gap for a, gap in zip(av, gaps)), I(0)) / denominator
        rw = sum((a / gap for a, gap in zip(aw, gaps)), I(0)) / denominator
        rvv = sum((((rv - a) / gap).square() for a, gap in zip(av, gaps)), I(0)) / denominator
        rww = sum((((rw - a) / gap).square() for a, gap in zip(aw, gaps)), I(0)) / denominator
        rvw = sum((((rv - a) * (rw - b) / gap.square())
                   for a, b, gap in zip(av, aw, gaps)), I(0)) / denominator
        for edge, gap, a, b in zip(layer, gaps, av, aw):
            value = gap.sqrt()
            dv, dw = (rv - a) / (2 * value), (rw - b) / (2 * value)
            value_cubed = value * value * value
            dvv = rvv / (2 * value) - (rv - a).square() / (4 * value_cubed)
            dww = rww / (2 * value) - (rw - b).square() / (4 * value_cubed)
            dvw = rvw / (2 * value) - (rv - a) * (rw - b) / (4 * value_cubed)
            source[edge + (colour, colour)] = (value, dv, dw, dvv, dvw, dww)
    root_v, root_w = v.sqrt(), w.sqrt()
    for cell, coefficient in current.BOUNDARY.items():
        value = coefficient * root_v
        root_v_cubed = root_v * root_v * root_v
        source[cell] = (value, coefficient / (2 * root_v), I(0),
                        -coefficient / (4 * root_v_cubed), I(0), I(0))
    for cell, coefficient in current.DIRECTION.items():
        c = float(coefficient)
        value = c * root_w
        root_w_cubed = root_w * root_w * root_w
        source[cell] = (value, I(0), c / (2 * root_w), I(0), I(0),
                        -c / (4 * root_w_cubed))
    return source


def product_jets(factors):
    def prod_values(replacements):
        value = I(1)
        for index, factor in enumerate(factors):
            value = value * replacements.get(index, factor[0])
        return value
    value = prod_values({})
    dv = sum((prod_values({i: factor[1]}) for i, factor in enumerate(factors)), I(0))
    dw = sum((prod_values({i: factor[2]}) for i, factor in enumerate(factors)), I(0))
    dvv = sum((prod_values({i: factor[3]}) for i, factor in enumerate(factors)), I(0))
    dww = sum((prod_values({i: factor[5]}) for i, factor in enumerate(factors)), I(0))
    dvw = sum((prod_values({i: factor[4]}) for i, factor in enumerate(factors)), I(0))
    for i in range(len(factors)):
        for j in range(i + 1, len(factors)):
            dvv = dvv + 2 * prod_values({i: factors[i][1], j: factors[j][1]})
            dww = dww + 2 * prod_values({i: factors[i][2], j: factors[j][2]})
            dvw = dvw + prod_values({i: factors[i][1], j: factors[j][2]})
            dvw = dvw + prod_values({i: factors[i][2], j: factors[j][1]})
    return value, dv, dw, dvv, dvw, dww


def main():
    source = source_box()
    p = [I(0) for _ in range(6)]
    for word, monomials in current.TERMS.items():
        if len(set(word)) == 1:
            continue
        a = [I(0) for _ in range(6)]
        for monomial in monomials:
            jets = product_jets([source[cell] for cell in monomial])
            a = [left + right for left, right in zip(a, jets)]
        p[0] = p[0] + a[0].square()
        p[1] = p[1] + 2 * a[0] * a[1]
        p[2] = p[2] + 2 * a[0] * a[2]
        p[3] = p[3] + 2 * (a[1].square() + a[0] * a[3])
        p[4] = p[4] + 2 * (a[1] * a[2] + a[0] * a[4])
        p[5] = p[5] + 2 * (a[2].square() + a[0] * a[5])
    determinant = p[3] * p[5] - p[4].square()
    print("box", VBOX, WBOX)
    print("P,dv,dw", p[:3])
    print("Hessian", p[3], p[4], p[5], "det", determinant)
    if p[3].lo <= 0 or determinant.lo <= 0:
        raise RuntimeError((p[3], p[4], p[5], determinant))


if __name__ == "__main__":
    main()
