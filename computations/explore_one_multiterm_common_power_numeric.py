#!/usr/bin/env python3
"""Numerically explore the first two-monomial common-power frontier.

This is deliberately a falsification/discovery aid, not a proof artifact.
For each support representative printed by
``explore_one_multiterm_support_orbits.py`` it minimizes the exact real
coefficient equations

    q^[2] = F_0(P_00) + F_0(P_01) + F_1(P_1) + F_2(P_2),
    q F = 0.

The second equation is equivalent to the needed q^[3]=0 once the first one
holds over characteristic zero.  Every edge block of q is an unrestricted
3-by-3 endpoint-colour tensor.  Small residuals are only candidate solutions
and must be converted to exact algebra before use.
"""

from __future__ import annotations

import argparse
from itertools import combinations, product
import math
import random


N_SITE = 6
N_COLOUR = 3
EDGES = tuple(combinations(range(N_SITE), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
N_VAR = len(EDGES) * N_COLOUR * N_COLOUR

REPRESENTATIVES = (
    ((0, 1), (0, 2), (0, 3), (4, 5)),
    ((0, 1), (0, 2), (1, 3), (2, 4)),
    ((0, 1), (0, 2), (1, 3), (3, 4)),
    ((0, 1), (0, 2), (1, 3), (4, 5)),
    ((0, 1), (0, 2), (3, 4), (3, 5)),
    ((0, 1), (2, 3), (0, 2), (1, 4)),
    ((0, 1), (2, 3), (0, 2), (4, 5)),
    ((0, 1), (2, 3), (0, 4), (0, 5)),
    ((0, 1), (2, 3), (0, 4), (1, 5)),
    ((0, 1), (2, 3), (0, 4), (2, 5)),
    ((0, 1), (2, 3), (0, 4), (4, 5)),
)


def vid(u: int, v: int, cu: int, cv: int) -> int:
    if u < v:
        return 9 * EDGE_INDEX[(u, v)] + 3 * cu + cv
    return 9 * EDGE_INDEX[(v, u)] + 3 * cv + cu


def q2_equations(support):
    targets = {}
    for pair, colour in zip(support, (0, 0, 1, 2)):
        sites = tuple(u for u in range(N_SITE) if u not in pair)
        targets[(sites, (colour,) * 4)] = targets.get((sites, (colour,) * 4), 0.0) + 1.0

    equations = []
    patterns = ((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2))
    for sites in combinations(range(N_SITE), 4):
        for colours in product(range(N_COLOUR), repeat=4):
            terms = tuple(
                (
                    vid(sites[i], sites[j], colours[i], colours[j]),
                    vid(sites[k], sites[l], colours[k], colours[l]),
                )
                for i, j, k, l in patterns
            )
            equations.append((terms, targets.get((sites, colours), 0.0)))
    return equations


def qf_equations(support):
    """Return sparse linear coefficients of qF on all full colour words."""
    by_word = {}
    for pair, colour in zip(support, (0, 0, 1, 2)):
        u, v = pair
        for cu, cv in product(range(N_COLOUR), repeat=2):
            word = [colour] * N_SITE
            word[u] = cu
            word[v] = cv
            by_word.setdefault(tuple(word), []).append((vid(u, v, cu, cv), 1.0))
    return tuple(tuple(terms) for terms in by_word.values())


def value_gradient(x, equations2, equationsf):
    grad = [0.0] * N_VAR
    value = 0.0
    maximum = 0.0
    for terms, target in equations2:
        residual = -target
        for i, j in terms:
            residual += x[i] * x[j]
        value += residual * residual
        maximum = max(maximum, abs(residual))
        twice = 2.0 * residual
        for i, j in terms:
            grad[i] += twice * x[j]
            grad[j] += twice * x[i]
    for terms in equationsf:
        residual = sum(coefficient * x[i] for i, coefficient in terms)
        value += residual * residual
        maximum = max(maximum, abs(residual))
        twice = 2.0 * residual
        for i, coefficient in terms:
            grad[i] += twice * coefficient
    return value, maximum, grad


def run(support, seed: int, steps: int):
    rng = random.Random(seed)
    x = [rng.gauss(0.0, 0.12) for _ in range(N_VAR)]
    m = [0.0] * N_VAR
    v = [0.0] * N_VAR
    equations2 = q2_equations(support)
    equationsf = qf_equations(support)
    best = (float("inf"), float("inf"), None)
    for step in range(1, steps + 1):
        loss, maximum, gradient = value_gradient(x, equations2, equationsf)
        if loss < best[0]:
            best = loss, maximum, x[:]
        rate = 0.02 * min(1.0, 2000.0 / step)
        b1, b2 = 0.9, 0.999
        for index, g in enumerate(gradient):
            m[index] = b1 * m[index] + (1.0 - b1) * g
            v[index] = b2 * v[index] + (1.0 - b2) * g * g
            mh = m[index] / (1.0 - b1**step)
            vh = v[index] / (1.0 - b2**step)
            x[index] -= rate * mh / (math.sqrt(vh) + 1e-8)
        if maximum < 1e-10:
            break
    return step, best


def describe(x, cutoff=1e-5):
    entries = []
    for edge_index, (u, v) in enumerate(EDGES):
        for cu, cv in product(range(N_COLOUR), repeat=2):
            value = x[9 * edge_index + 3 * cu + cv]
            if abs(value) >= cutoff:
                entries.append((u, v, cu, cv, value))
    return tuple(entries)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int, action="append")
    parser.add_argument("--seeds", type=int, default=3)
    parser.add_argument("--steps", type=int, default=12000)
    args = parser.parse_args()
    selected = args.orbit or list(range(1, len(REPRESENTATIVES) + 1))
    for orbit in selected:
        support = REPRESENTATIVES[orbit - 1]
        for seed in range(args.seeds):
            step, (loss, maximum, x) = run(support, 1000 * orbit + seed, args.steps)
            print(
                f"orbit={orbit:02d} seed={seed} step={step}",
                f"loss={loss:.6e} max={maximum:.6e}",
            )
            if maximum < 1e-6:
                print("candidate", describe(x))


if __name__ == "__main__":
    main()
