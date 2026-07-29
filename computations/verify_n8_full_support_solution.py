#!/usr/bin/env python3
"""Direct verifier for full-support search JSON outputs.

This checker does not instantiate SAT or trust term variables.  It enumerates
all 3**8 colourings and all 105 perfect matchings from the selected decorated
cells, then checks the requested structural, signed, or root-of-unity
coefficient semantics exactly.
"""

from __future__ import annotations

import argparse
from itertools import combinations, product
import json
from pathlib import Path

import search_n8_signed_binomial_lazy_cegar as signed


N = signed.N
Q = signed.Q


def load_instance(path):
    payload = json.loads(Path(path).read_text())
    assert payload["n"] == N
    orbit = payload["orbit"]
    targets = signed.core.target_orbits(N)[orbit]
    assert tuple(
        tuple(tuple(edge) for edge in matching)
        for matching in payload["targets"]
    ) == targets
    cells = frozenset(
        (u, v, a, b)
        for u, v in combinations(range(N), 2)
        for a, b in product(range(Q), repeat=2)
    )
    entries = payload["selected_cells"]
    selected = frozenset(tuple(entry["cell"]) for entry in entries)
    assert len(selected) == len(entries)
    assert selected <= cells
    if payload.get("max_cells") is not None:
        assert len(selected) <= payload["max_cells"]
    if payload.get("min_cells") is not None:
        assert len(selected) >= payload["min_cells"]
    return payload, targets, selected, entries


def verify(path):
    payload, targets, selected, entries = load_instance(path)
    matchings = tuple(
        signed.core.perfect_matchings(tuple(range(N)))
    )
    assert len(matchings) == 105
    fibres = signed.core.exact_fibres(N, selected, matchings)
    mode = payload["mode"]

    weights = None
    order = None
    exponents = None
    toric_survivor = False
    if mode == "signed":
        weights = {
            tuple(entry["cell"]): entry["weight"] for entry in entries
        }
        assert set(weights.values()) <= {-1, 1}
    elif mode == "toric":
        order = payload["root_order"]
        assert isinstance(order, int) and order > 0
        exponents = {
            tuple(entry["cell"]): entry["root_exponent"] % order
            for entry in entries
        }
    elif mode == "toric-survivor":
        toric_survivor = True
    else:
        assert mode == "structural"

    nonempty_mixed = 0
    for coloring in product(range(Q), repeat=N):
        terms = fibres.get(coloring, ())
        if len(set(coloring)) == 1:
            color = coloring[0]
            target_cells = {
                (u, v, color, color) for u, v in targets[color]
            }
            if payload.get("allow_extra_constants", False):
                assert any(
                    set(decorated) == target_cells
                    for _matching_number, decorated in terms
                )
            else:
                assert len(terms) == 1
                assert set(terms[0][1]) == target_cells
            if weights is not None:
                coefficient = 1
                for cell in terms[0][1]:
                    coefficient *= weights[cell]
                assert coefficient == 1
            if exponents is not None:
                exponent = sum(
                    exponents[cell] for cell in terms[0][1]
                ) % order
                assert exponent == 0
            continue

        assert len(terms) in (0, 2)
        if not terms:
            continue
        nonempty_mixed += 1
        if weights is not None:
            products = []
            for _matching_number, decorated in terms:
                value = 1
                for cell in decorated:
                    value *= weights[cell]
                products.append(value)
            assert sum(products) == 0
        if exponents is not None:
            term_exponents = [
                sum(exponents[cell] for cell in decorated) % order
                for _matching_number, decorated in terms
            ]
            assert order % 2 == 0
            assert (
                term_exponents[0] - term_exponents[1]
            ) % order == order // 2

    assert payload.get("mixed_fibres", nonempty_mixed) == nonempty_mixed
    if toric_survivor:
        cells = tuple(
            (u, v, a, b)
            for u, v in combinations(range(N), 2)
            for a, b in product(range(Q), repeat=2)
        )
        cell_index = {cell: index for index, cell in enumerate(cells)}
        mixed = [
            (coloring, terms)
            for coloring, terms in sorted(fibres.items())
            if len(set(coloring)) > 1
        ]
        rows = [
            signed.core.exponent_row(
                terms[0][1], terms[1][1], cell_index, len(cells)
            )
            for _coloring, terms in mixed
        ]
        consistent, lattice = signed.core.signed_quotient_lattice(
            rows, len(cells)
        )
        assert consistent
        remainder, classes = signed.core.reduced_constant_product(
            N, fibres, lattice, cells, cell_index
        )
        assert remainder
        assert payload.get(
            "quotient_classes", len(remainder)
        ) == len(remainder)
        assert payload.get(
            "raw_constant_classes", len(classes)
        ) == len(classes)
    print(
        f"PASS mode={mode} orbit={payload['orbit']} "
        f"cells={len(selected)} mixed_fibres={nonempty_mixed}"
        + (f" root_order={order}" if order is not None else "")
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("json_path")
    args = parser.parse_args()
    verify(args.json_path)


if __name__ == "__main__":
    main()
