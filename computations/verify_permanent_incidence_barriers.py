#!/usr/bin/env python3
"""Exact finite checks for the permanent/incidence route.

The script verifies:
  * the natural cyclic Fourier ansatz on K_{5,5} has a mixed coefficient 20;
  * the star-kernel Glynn cover scan has no solution through m=11.

The second statement concerns only the explicitly documented star-kernel
subclass, not arbitrary restrictions of the permanent tensor.
"""

from __future__ import annotations

import itertools

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csc_matrix

from search_glynn_permanent_restriction import candidates


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


def fourier_counts(c: tuple[int, ...], d: tuple[int, ...]) -> list[int]:
    m = len(c)
    counts = [0] * m
    for sigma in itertools.permutations(range(m)):
        inv = [0] * m
        for i, j in enumerate(sigma):
            inv[j] = i
        exponent = (sum(c[i] * sigma[i] for i in range(m))
                    - sum(d[j] * inv[j] for j in range(m))) % m
        counts[exponent] += 1
    return counts


def canonical_masks(d: int, a: int, b: int, overlap: int):
    first = (1 << a) - 1
    second = ((1 << overlap) - 1) | (
        ((1 << (b - overlap)) - 1) << a)
    return 0, first, second


def star_cover_exists(m: int, survivors: tuple[int, int, int]) -> bool:
    universe, raw = candidates(m, survivors, star_only=True)
    unique = {}
    for item in raw:
        unique.setdefault(item[0], item)
    cand = list(unique.values())
    rows, cols = [], []
    for j, item in enumerate(cand):
        for i in item[0]:
            rows.append(i)
            cols.append(j)
    cover = csc_matrix((np.ones(len(rows)), (rows, cols)),
                       shape=(len(universe), len(cand)))
    if not cand or np.any(np.asarray(cover.sum(axis=1)).ravel() == 0):
        return False
    constraints = [
        LinearConstraint(cover, np.ones(len(universe)), np.inf),
        LinearConstraint(np.ones((1, len(cand))), -np.inf, m),
    ]
    result = milp(np.ones(len(cand)), integrality=np.ones(len(cand)),
                  bounds=Bounds(np.zeros(len(cand)), np.ones(len(cand))),
                  constraints=constraints,
                  options={"mip_rel_gap": 0})
    return result.x is not None


def audit_star_orbits(m: int) -> int:
    d = m - 1
    tested = 0
    for a in range(1, d + 1):
        for b in range(a, d + 1):
            for overlap in range(max(0, a + b - d), min(a, b) + 1):
                survivors = canonical_masks(d, a, b, overlap)
                if len(set(survivors)) < 3:
                    continue
                tested += 1
                require(
                    not star_cover_exists(m, survivors),
                    (m, survivors),
                )
    return tested


def main() -> None:
    c = (0, 0, 0, 0, 0)
    d = (0, 0, 1, 2, 2)
    counts = fourier_counts(c, d)
    require(
        counts == [40, 20, 20, 20, 20],
        "counts == [40, 20, 20, 20, 20]",
    )
    # For a primitive fifth root zeta, the coefficient is
    # 40 + 20(zeta+...+zeta^4) = 20.
    print("K5,5 Fourier mixed residue counts:", counts, "coefficient: 20")

    total = 0
    for m in range(8, 12):
        tested = audit_star_orbits(m)
        total += tested
        print(f"m={m}: {tested} survivor orbits, no <=m star-kernel cover")
    print("verified star-kernel orbits:", total)


if __name__ == "__main__":
    main()
