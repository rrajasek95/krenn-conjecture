#!/usr/bin/env python3
"""Exact smallest-support interference screen above Laurent no-cap rays."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product

from probe_laurent_crosscolour_leakage import (
    BASE, CELLS, GONE, PHASES, balance_correction, canonical_support,
    derivative_coefficients, enumerate_feasible, existing_mixed_cross,
    gadd, gconj, gmul, greal, mixed_inner, support_separated_identity_cap,
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


CAPS = (
    (2, 3, 4), (2, 4, 3), (3, 4, 2),
    (5, 6, 7), (5, 7, 6), (6, 7, 5),
)
ACTIVE_PAIRS = tuple(sorted({(u, v) for u, v, _, _ in BASE}))
ANCHORS = (
    ((2, 5, 1, 2), (4, 6, 1, 2)),
    ((2, 6, 1, 2), (4, 5, 1, 2)),
)


def has_frozen_cap(cells):
    row = {"cells": tuple(cells)}
    return any(support_separated_identity_cap(row, p, q, centre)
               for p, q, centre in CAPS)


def identity_response_edges(cells, p, q):
    support = set(BASE) | set(cells)

    def occupied(u, v, a, b):
        if u < v:
            return (u, v, a, b) in support
        return (v, u, b, a) in support

    residual = tuple(site for site in range(8) if site not in (p, q))
    edges = set()
    for colour in range(3):
        p_neighbours = [site for site in residual
                        if any(occupied(p, site, colour, alpha)
                               for alpha in range(3))]
        q_neighbours = [site for site in residual
                        if any(occupied(q, site, colour, alpha)
                               for alpha in range(3))]
        for left in p_neighbours:
            for right in q_neighbours:
                if left != right:
                    edges.add(tuple(sorted((left, right))))
    return edges


def identity_intersecting_carriers(cells):
    carriers = []
    for p, q in ACTIVE_PAIRS:
        edges = identity_response_edges(cells, p, q)
        if all(set(left) & set(right) for left, right in combinations(edges, 2)):
            carriers.append(((p, q), tuple(sorted(edges))))
    return carriers


def precompute():
    linear = {}
    base = None
    for cell in CELLS:
        this_base, this_linear, _ = derivative_coefficients(
            {cell: Fraction(1)}, {}
        )
        base = this_base if base is None else base
        require(this_base == base, "base changed")
        linear[cell] = this_linear
    yy_cross = {}
    for left, right in combinations(CELLS, 2):
        _, _, qyy = derivative_coefficients(
            {left: Fraction(1), right: Fraction(1)}, {}
        )
        value = existing_mixed_cross(base, qyy)
        if value:
            yy_cross[left, right] = value
    return base, linear, yy_cross


def pair_key(left, right):
    return (left, right) if left < right else (right, left)


def phase_value(cells, phases, linear, yy_cross, z_cross):
    # Linear leakage norm.
    words = set().union(*(linear[cell] for cell in cells))
    value = Fraction(0)
    for word in words:
        if len(set(word)) == 1:
            continue
        total = (Fraction(0), Fraction(0))
        for cell, phase in zip(cells, phases):
            coefficient = linear[cell].get(word, 0)
            total = gadd(total, (coefficient * phase[0], coefficient * phase[1]))
        value += greal(gmul(total, gconj(total)))
    value += 2 * z_cross
    # Holomorphic YY contribution against the two existing mixed defects.
    for left_index, right_index in combinations(range(len(cells)), 2):
        coefficient = yy_cross.get(pair_key(cells[left_index], cells[right_index]), 0)
        value += 2 * coefficient * greal(
            gmul(phases[left_index], phases[right_index])
        )
    return value


def main():
    feasible = enumerate_feasible()
    supports = sorted({tuple(sorted(row["cells"])) for row in feasible})
    require(len(supports) == 72, len(supports))
    base, linear, yy_cross = precompute()

    candidates = {}
    skipped_overlap = 0
    for anchor in ANCHORS:
        for extra in supports:
            if set(anchor) & set(extra):
                skipped_overlap += 1
                continue
            cells = tuple(sorted(anchor + extra))
            if has_frozen_cap(cells):
                continue
            key = canonical_support(cells)
            candidates.setdefault(key, cells)

    print("anchors", len(ANCHORS), "extra rays", len(supports),
          "overlap skips", skipped_overlap)
    print("four-cell no-cap support orbits", len(candidates))

    full_identity_no_carrier = {
        key: cells for key, cells in candidates.items()
        if not identity_intersecting_carriers(cells)
    }
    print("four-cell supports with no identity star/triangle carrier",
          len(full_identity_no_carrier))

    distribution = Counter()
    nonpositive = []
    records = []
    for key, cells in sorted(candidates.items()):
        z = balance_correction(cells)
        require(z is not None, cells)
        _, _, qz = derivative_coefficients({}, z)
        z_cross = existing_mixed_cross(base, qz)
        best = None
        best_phases = []
        for phases in product(PHASES, repeat=4):
            value = phase_value(cells, phases, linear, yy_cross, z_cross)
            if best is None or value < best:
                best, best_phases = value, [phases]
            elif value == best:
                best_phases.append(phases)
        distribution[best] += 1
        record = {"canonical_support": key, "cells": cells, "phase_grid_min": best,
                  "minimizer_count": len(best_phases), "z_cross": z_cross,
                  "phases": best_phases[0]}
        records.append(record)
        if best <= 0:
            nonpositive.append(record)
    print("Gaussian-phase minimum distribution", dict(sorted(distribution.items())))
    print("nonpositive candidates", len(nonpositive))
    for record in nonpositive:
        print("NONPOSITIVE", record)
    for record in sorted(records, key=lambda row: row["phase_grid_min"])[:20]:
        print("small", record)


if __name__ == "__main__":
    main()
