#!/usr/bin/env python3
"""Bounded Boolean census for the exact block-normal tensor-activity clause."""

from __future__ import annotations

import argparse
from collections import defaultdict
from itertools import product
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import integrate_twenty_two_cell_branch as branch  # noqa: E402


MINIMUM = (0.22235570199505403, 0.10692046095948153,
           0.02918848455871847, 0.17124569877870893)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1:]
        for rest in perfect_matchings(remaining):
            answer.append((tuple(sorted((first, second))),) + rest)
    return tuple(answer)


def cofactor_ledger(edge, source=None):
    residual = tuple(site for site in range(8) if site not in edge)
    edge_cells = defaultdict(list)
    for cell in branch.SUPPORT:
        if cell[0] in residual and cell[1] in residual:
            edge_cells[cell[:2]].append(cell)
    ledger = defaultdict(list)
    for matching in perfect_matchings(residual):
        choices = [edge_cells[pair] for pair in matching]
        if any(not choice for choice in choices):
            continue
        for picked in product(*choices):
            word = [None] * 6
            positions = {site: index for index, site in enumerate(residual)}
            for u, v, a, b in picked:
                word[positions[u]], word[positions[v]] = a, b
            ledger[tuple(word)].append(tuple(picked))
    if source is None:
        return ledger
    values = {}
    for word, monomials in ledger.items():
        values[word] = sum(
            product_values(source[cell] for cell in monomial)
            for monomial in monomials
        )
    return ledger, values


def product_values(values):
    answer = 1.0
    for value in values:
        answer *= value
    return answer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate-delete-cofactor", action="store_true")
    args = parser.parse_args()
    source = {cell: jets[0] for cell, jets in branch.source_jets(MINIMUM).items()}
    live_edges = sorted({cell[:2] for cell in branch.SUPPORT})
    rows = []
    for edge in live_edges:
        ledger, values = cofactor_ledger(edge, source)
        supported = len(ledger)
        actual = sum(abs(value) > 1e-10 for value in values.values())
        singleton = sum(len(monomials) == 1 for monomials in ledger.values())
        rows.append((edge, supported, actual, singleton,
                     sum(map(len, ledger.values()))))
    if args.mutate_delete_cofactor:
        rows[0] = (rows[0][0], 0, 0, 0, 0)
    require(all(supported and actual for _, supported, actual, _, _ in rows), rows)

    stars, triangles = branch.family.carrier_witnesses(
        {cell: None for cell in branch.SUPPORT})
    require((len(stars), len(triangles)) == (168, 560),
            (len(stars), len(triangles)))
    cell_clauses = len(branch.SUPPORT)
    edge_clauses = len(live_edges)
    require((cell_clauses, edge_clauses) == (22, 19),
            (cell_clauses, edge_clauses))
    print("exact theorem",
          "at a norm-minimal exact fibre point A_e!=0 => H_{V\\e}!=0")
    print("Boolean relaxation",
          "every live cell lies on an edge with at least one supported residual six-word column")
    print("clauses", cell_clauses, "deduplicated edge clauses", edge_clauses)
    for row in rows:
        print("EDGE", row)
    print("Boolean counterguard support", len(branch.SUPPORT),
          "outputs", len(branch.TERMS), "carrier blockers", len(stars), len(triangles))
    print("known fixed-left entry counts", {"support6": 12, "support8": 18},
          "global live-cell count", len(branch.SUPPORT))
    print("verdict",
          "tensor activity plus literal carrier blockers does not force a cap or either fixed-left support count; coefficient-level simultaneous GHZ cancellation is still required")


if __name__ == "__main__":
    main()
