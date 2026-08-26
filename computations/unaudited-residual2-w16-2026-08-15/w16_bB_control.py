#!/usr/bin/env python3
"""W16 -- control for the Branch-B gauge-fixed closed form.

Verifies EXACTLY (Fractions, deterministic pseudo-random rationals) that on
every Branch-B/gauge-fixed point,   Phi(x,y) = lam_x*g(b,c,d) + F_a*k_x(b,c,d)
with lam_x = P_L(x), against w16_core's independent Phi (the Gamma-matching
sum).  Also runs a mutation control.
"""
from __future__ import annotations
import os, sys, itertools, json
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w16_core import (W8_IMMUNE, EIDX, VarMap, phi_poly, full_pm_indices,
                      peval, EDGES)

T = W8_IMMUNE[25]
FULLM = full_pm_indices(T)


def lcg(seed):
    s = seed
    while True:
        s = (1103515245 * s + 12345) % (1 << 31)
        yield s


def build(seed):
    r = lcg(seed)
    def rn():
        return Fraction(next(r) % 17 - 8 or 3, next(r) % 7 + 1)
    B = {}
    B[(1, 4)] = [[Fraction(1)] + [rn() for _ in range(2)] for _ in range(2)] \
        + [[Fraction(1)] * 3]
    B[(2, 5)] = [[Fraction(1)] * 3] + \
        [[Fraction(1)] + [rn() for _ in range(2)] for _ in range(2)]
    B[(0, 7)] = [[Fraction(1)] + [rn() for _ in range(2)],
                 [Fraction(1)] * 3, [Fraction(1)] * 3]
    B[(6, 7)] = [[Fraction(1)] + [rn() for _ in range(2)] for _ in range(3)]
    B[(5, 6)] = [[rn() for _ in range(3)] for _ in range(3)]
    B[(0, 3)] = [[Fraction(1)] * 3] + [[rn() for _ in range(3)]
                                       for _ in range(2)]
    B[(2, 3)] = [[rn() for _ in range(3)] for _ in range(3)]
    mu, nu = rn(), rn()
    B[(4, 5)] = [[mu] * 3 for _ in range(3)]
    B[(4, 7)] = [[nu] * 3 for _ in range(3)]
    for e in [(0, 1), (0, 2), (1, 2), (1, 3)]:
        B[e] = [[rn() for _ in range(3)] for _ in range(3)]
    return B, mu, nu


def PL(B, x):
    x0, x1, x2, x3 = x
    return (B[(0, 1)][x0][x1] * B[(2, 3)][x2][x3]
            + B[(0, 2)][x0][x2] * B[(1, 3)][x1][x3]
            + B[(0, 3)][x0][x3] * B[(1, 2)][x1][x2])


def main():
    vm = VarMap(T)
    bad = 0
    tested = 0
    for seed in (1, 7, 99, 2024, 31337):
        B, mu, nu = build(seed)
        vals = {}
        for ei, (u, v) in enumerate(EDGES):
            if T[ei] != 511:
                continue
            for c in range(9):
                vals[vm.v(ei, c)] = B[(u, v)][c // 3][c % 3]
        for x in itertools.product(range(3), repeat=4):
            lam = PL(B, x)
            for y in itertools.product(range(3), repeat=4):
                a, b, c, d = y
                g = mu * B[(6, 7)][c][d] + nu * B[(5, 6)][b][c]
                k = (B[(0, 3)][x[0]][x[3]] * B[(2, 5)][x[2]][b]
                     * B[(6, 7)][c][d]
                     + B[(2, 3)][x[2]][x[3]] * B[(0, 7)][x[0]][d]
                     * B[(5, 6)][b][c])
                mine = lam * g + B[(1, 4)][x[1]][a] * k
                truth = peval(phi_poly(T, vm, tuple(x) + tuple(y), FULLM),
                              vals)
                tested += 1
                if mine != truth:
                    bad += 1
    print("Branch-B closed form: %d/%d words matched, %d mismatches"
          % (tested - bad, tested, bad))
    # MUTATION CONTROL: perturb the closed form -> must mismatch
    B, mu, nu = build(1)
    vals = {}
    for ei, (u, v) in enumerate(EDGES):
        if T[ei] != 511:
            continue
        for c in range(9):
            vals[vm.v(ei, c)] = B[(u, v)][c // 3][c % 3]
    mism = 0
    for x in itertools.product(range(3), repeat=4):
        lam = PL(B, x)
        for y in itertools.product(range(3), repeat=4):
            a, b, c, d = y
            g = mu * B[(6, 7)][c][d] + nu * B[(5, 6)][b][c]
            k = (B[(0, 3)][x[0]][x[3]] * B[(2, 5)][x[2]][b] * B[(6, 7)][c][d]
                 + Fraction(2) * B[(2, 3)][x[2]][x[3]] * B[(0, 7)][x[0]][d]
                 * B[(5, 6)][b][c])                      # <-- mutated
            mine = lam * g + B[(1, 4)][x[1]][a] * k
            if mine != peval(phi_poly(T, vm, tuple(x) + tuple(y), FULLM),
                             vals):
                mism += 1
    print("mutation control (doubled A23 term): %d mismatches (must be > 0)"
          % mism)
    json.dump(dict(tested=tested, mismatches=bad, mutation_mismatches=mism),
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "results_bB_control.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
