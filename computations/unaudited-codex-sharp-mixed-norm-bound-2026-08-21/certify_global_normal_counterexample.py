#!/usr/bin/env python3
"""Exact non-minimal two-ray counterexample to global normal-cone positivity."""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import certify_active_cap_normal_cone as normal  # noqa: E402


NEGATIVE_INDICES = (5, 9, 27, 32, 41, 42)
FULL_HITTER_INDICES = (58, 59, 60, 63)
NEGATIVE = 9
HITTER = 58


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def literal_full_union(rays, left, right):
    source = {cell: None for cell in normal.BASE}
    source.update({cell: None for cell in normal.BOUNDARY_LEAK})
    source.update({cell: None for cell in rays[left]})
    source.update({cell: None for cell in rays[right]})
    try:
        stars, triangles = normal.family.carrier_witnesses(source)
    except RuntimeError:
        return False
    return len(stars) == 168 and len(triangles) == 560


def gram_orthogonal(support):
    remote = defaultdict(set)
    for u, v, a, b in support:
        remote[u, v, b].add(a)
        remote[v, u, a].add(b)
    return all(len(local_colours) == 1 for local_colours in remote.values())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate-delete-hitter", action="store_true")
    args = parser.parse_args()
    rays, _ = normal.star_hitting_rays()
    vlo, vhi = normal.minimizer_v_interval()
    unions = [(left, right) for left in NEGATIVE_INDICES
              for right in FULL_HITTER_INDICES
              if literal_full_union(rays, left, right)]
    require(len(unions) == 24, unions)

    direction = {
        rays[NEGATIVE][0]: Fraction(-1),
        rays[NEGATIVE][1]: Fraction(1),
    }
    if not args.mutate_delete_hitter:
        direction.update({
            rays[HITTER][0]: Fraction(-1, 10),
            rays[HITTER][1]: Fraction(-1, 10),
        })
    support = (set(normal.BASE) | set(normal.BOUNDARY_LEAK)
               | set(direction))
    require(gram_orthogonal(support), "port Gram cross term survived")
    require(literal_full_union(rays, NEGATIVE, HITTER)
            and not args.mutate_delete_hitter,
            "full arbitrary-K carrier blockers are absent")
    coefficient = normal.combined_coefficient(direction, vlo, vhi)
    require(coefficient.hi < 0, coefficient)
    print("boundary v interval", (vlo, vhi))
    print("all negative+hitter literal-full unions", len(unions))
    print("direction", direction)
    print("normal coefficient", coefficient)
    print("carrier blockers", 168, 560)
    print("exact integration", "add w*|y_cell|^2 to each incident port-energy edge, solve the four-factor rho equations, and take positive square roots")


if __name__ == "__main__":
    main()
