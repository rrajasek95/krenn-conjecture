#!/usr/bin/env python3
"""Export a source-faithful mixed-cutoff seed for zero-based orbit 0.

Orbit 0 has the same physical perfect matching in all three pure colours and
the full 2304-element anchor stabilizer.  Target quotient coefficients use
the total-mass convention required by the Rust orbit-closure engine.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import permutations, product
import argparse
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "audit_dangerous_charts.py"
SPEC = importlib.util.spec_from_file_location("dangerous_base", BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)

M0 = ((0, 1), (2, 3), (4, 5), (6, 7))
MATCHINGS = (M0, M0, M0)
ANCHORS = frozenset(BASE.CELL_ID[(left, right, colour, colour)]
                    for colour in BASE.COLORS for left, right in M0)


def transform_cell(cell, site_permutation, colour_permutation):
    u, v, a, b = cell
    pu, pv = site_permutation[u], site_permutation[v]
    pa, pb = colour_permutation[a], colour_permutation[b]
    if pu < pv:
        return pu, pv, pa, pb
    return pv, pu, pb, pa


def build_stabilizer():
    answer = []
    anchor_cells = frozenset(BASE.CELLS[index] for index in ANCHORS)
    for sites in permutations(range(BASE.N)):
        moved_matching = tuple(sorted(
            tuple(sorted((sites[left], sites[right]))) for left, right in M0
        ))
        if moved_matching != M0:
            continue
        for colours in permutations(BASE.COLORS):
            image = frozenset(transform_cell(cell, sites, colours)
                              for cell in anchor_cells)
            if image == anchor_cells:
                answer.append((sites, colours))
    if len(answer) != 2304:
        raise RuntimeError("orbit-0 stabilizer is no longer order 2304")
    return tuple(answer)


STABILIZER = build_stabilizer()
TRANSFORMS = tuple(bytes(
    BASE.CELL_ID[transform_cell(cell, sites, colours)]
    for cell in BASE.CELLS
) for sites, colours in STABILIZER)


def target_actual(cutoff):
    groups = []
    for colour in BASE.COLORS:
        by_degree = defaultdict(list)
        for row in BASE.word_terms((colour,) * BASE.N):
            by_degree[BASE.row_degree(row, ANCHORS)].append(row)
        groups.append(by_degree)
    target = Counter()
    for degree in range(cutoff):
        for degrees in product(range(degree + 1), repeat=3):
            if sum(degrees) != degree:
                continue
            for terms in product(*(groups[colour].get(degrees[colour], ())
                                   for colour in BASE.COLORS)):
                target[bytes(sorted(b"".join(terms)))] += 1
    return target


def row_orbit(row):
    return frozenset(bytes(sorted(transform[cell] for cell in row))
                     for transform in TRANSFORMS)


def invariant_target(actual):
    unseen = set(actual)
    quotient = Counter()
    while unseen:
        row = min(unseen)
        orbit = row_orbit(row)
        if not orbit <= set(actual):
            raise RuntimeError("target support is not stabilizer-invariant")
        coefficients = {actual[item] for item in orbit}
        if len(coefficients) != 1:
            raise RuntimeError("target coefficient is not orbit-invariant")
        representative = min(orbit)
        quotient[representative] = sum(actual[item] for item in orbit)
        unseen.difference_update(orbit)
    return quotient


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cutoff", type=int, default=7)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or (HERE / f"orbit0_cutoff{args.cutoff}_seed.txt")
    actual = target_actual(args.cutoff)
    target = invariant_target(actual)
    degree_actual = Counter(BASE.row_degree(row, ANCHORS) for row in actual)
    degree_orbits = Counter(BASE.row_degree(row, ANCHORS) for row in target)
    if args.cutoff == 7:
        assert degree_actual == {0: 1, 2: 36, 3: 96, 4: 612,
                                 5: 2304, 6: 9120}
        assert sum(actual.values()) == 12169
    lines = [
        "KRENN_ANCHOR_K_CUTOFF_SEED_V1",
        f"CUTOFF {args.cutoff}",
        "ANCHORS " + bytes(sorted(ANCHORS)).hex(),
    ]
    for sites, colours in STABILIZER:
        lines.append("ACTION " + "".join(map(str, sites)) + " "
                     + "".join(map(str, colours)))
    for row, coefficient in sorted(target.items()):
        lines.append(f"TARGET {row.hex()} {coefficient} 1")
    payload = "\n".join(lines) + "\n"
    output.write_text(payload)
    print("orbit: 0")
    print("cutoff:", args.cutoff)
    print("stabilizer:", len(STABILIZER))
    print("actual target rows/mass:", len(actual), sum(actual.values()))
    print("target row orbits/mass:", len(target), sum(target.values()))
    print("actual degree histogram:", dict(sorted(degree_actual.items())))
    print("orbit degree histogram:", dict(sorted(degree_orbits.items())))
    print("seed bytes:", len(payload))
    print("seed sha256:", sha256(payload.encode("ascii")).hexdigest())
    print("path:", output)


if __name__ == "__main__":
    main()
