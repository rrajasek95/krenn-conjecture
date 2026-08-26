#!/usr/bin/env python3
"""Next exact elementary-ray screen at the 18-cell interior minimum."""

from __future__ import annotations

from collections import defaultdict
from itertools import product
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import integrate_negative_multiray_family as family  # noqa: E402
import integrate_global_normal_counterfamily as current  # noqa: E402
from probe_laurent_crosscolour_leakage import enumerate_feasible  # noqa: E402
from certify_negative_family_global_min import I  # noqa: E402


VLO, VHI = 0.20523, 0.20526
WLO, WHI = 0.19294, 0.19297
CURRENT_SUPPORT = (set(family.BASE) | set(current.BOUNDARY)
                   | set(current.DIRECTION))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def gram_orthogonal(support):
    remote = defaultdict(set)
    for u, v, a, b in support:
        remote[u, v, b].add(a)
        remote[v, u, a].add(b)
    return all(len(colours) == 1 for colours in remote.values())


def full_blockers(ray):
    source = {cell: None for cell in CURRENT_SUPPORT | set(ray)}
    try:
        stars, triangles = family.carrier_witnesses(source)
    except RuntimeError:
        return False
    return len(stars) == 168 and len(triangles) == 560


def term_ledger(ray):
    support = CURRENT_SUPPORT | set(ray)
    edge_cells = defaultdict(list)
    for cell in support:
        edge_cells[cell[:2]].append(cell)
    answer = defaultdict(list)
    for matching in family.PM8:
        choices = [edge_cells[edge] for edge in matching]
        if any(not choice for choice in choices):
            continue
        for picked in product(*choices):
            word = [None] * 8
            for u, v, a, b in picked:
                word[u], word[v] = a, b
            answer[tuple(word)].append(tuple(picked))
    return answer


def energy_multiplicities(ray):
    degree = defaultdict(int)
    for u, v, a, b in ray:
        degree[u, a] += 1
        degree[v, b] += 1
    answer = {}
    for colour, layer in family.LAYERS.items():
        values = []
        for u, v in layer:
            require(degree[u, colour] == degree[v, colour],
                    (ray, colour, u, v, degree))
            values.append(degree[u, colour])
        answer[colour] = values
    return answer


def coefficient(ray, signs):
    raw_source = current.source_box(WLO, WHI, VLO, VHI)
    source = {cell: value for cell, (value, _) in raw_source.items()}
    multiplicities = energy_multiplicities(ray)
    source_z = {}
    for colour, layer in family.LAYERS.items():
        gaps = [source[edge + (colour, colour)].square() for edge in layer]
        values = multiplicities[colour]
        rho_z = sum((value / gap for value, gap in zip(values, gaps)), I(0))
        rho_z = rho_z / sum((I(1) / gap for gap in gaps), I(0))
        for edge, value in zip(layer, values):
            diagonal = source[edge + (colour, colour)]
            source_z[edge + (colour, colour)] = (rho_z - value) / (2 * diagonal)
    for cell in current.BOUNDARY:
        source_z[cell] = I(0)
    for cell in current.DIRECTION:
        source_z[cell] = I(0)

    direction = dict(zip(ray, signs))
    q = I(0)
    for word, monomials in term_ledger(ray).items():
        if len(set(word)) == 1:
            continue
        f0, linear, quadratic = I(0), I(0), I(0)
        for monomial in monomials:
            count = sum(cell in direction for cell in monomial)
            if count == 0:
                value = I(1)
                for cell in monomial:
                    value = value * source[cell]
                f0 = f0 + value
                derivative = I(0)
                for index, cell in enumerate(monomial):
                    piece = source_z[cell]
                    for other, other_cell in enumerate(monomial):
                        if other != index:
                            piece = piece * source[other_cell]
                    derivative = derivative + piece
                quadratic = quadratic + derivative
            elif count in (1, 2):
                value = I(1)
                for cell in monomial:
                    value = value * (direction[cell] if cell in direction else source[cell])
                if count == 1:
                    linear = linear + value
                else:
                    quadratic = quadratic + value
        q = q + linear.square() + 2 * f0 * quadratic
    return q


def hermitian_overlap_absent(ray):
    ledger = term_ledger(ray)
    word_sets = []
    for selected in ray:
        words = set()
        for word, monomials in ledger.items():
            for monomial in monomials:
                if selected in monomial and sum(cell in ray for cell in monomial) == 1:
                    words.add(word)
        word_sets.append(words)
    return not (word_sets[0] & word_sets[1])


def main():
    rays = sorted({tuple(sorted(row["cells"])) for row in enumerate_feasible()})
    candidates = [ray for ray in rays if not set(ray) & CURRENT_SUPPORT
                  and gram_orthogonal(CURRENT_SUPPORT | set(ray))]
    full = [ray for ray in candidates if full_blockers(ray)]
    print("support cells", len(CURRENT_SUPPORT), "all rays", len(rays),
          "Gram-orthogonal outside", len(candidates), "full blockers", len(full))
    records = []
    for ray in full:
        require(hermitian_overlap_absent(ray), ("Hermitian phase overlap", ray))
        values = [(coefficient(ray, signs), signs)
                  for signs in product((-1, 1), repeat=2)]
        best = min(values, key=lambda item: item[0].lo)
        records.append((best[0].lo, best[0].hi, ray, best[1]))
    records.sort()
    print("negative", sum(record[1] < 0 for record in records))
    for record in records[:20]:
        print("RAY", record)
    require(records, "no full-blocker candidates")


if __name__ == "__main__":
    main()
