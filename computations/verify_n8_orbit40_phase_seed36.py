#!/usr/bin/env python3
"""Exact audit of the 36-cell orbit-40 full-formula phase seed."""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product

import search_n8_binomial_support_full_sat as full
import search_n8_signed_binomial_lazy_cegar as signed


def main():
    cells = tuple(
        (u, v, a, b)
        for u, v in combinations(range(signed.N), 2)
        for a, b in product(range(signed.Q), repeat=2)
    )
    cell_index = {cell: index for index, cell in enumerate(cells)}
    matchings = tuple(
        signed.core.perfect_matchings(tuple(range(signed.N)))
    )
    targets = signed.core.target_orbits(signed.N)[40]
    selected = full.ORBIT40_PHASE_CONSISTENT_SEED
    assert len(selected) == 36
    assert selected <= frozenset(cells)
    forced = frozenset(
        (u, v, color, color)
        for color, target in enumerate(targets)
        for u, v in target
    )
    assert forced <= selected

    fibres = signed.core.exact_fibres(
        signed.N, selected, matchings
    )
    assert Counter(map(len, fibres.values())) == {2: 96, 24: 1}
    assert tuple(len(fibres[(color,) * signed.N]) for color in range(3)) == (
        24, 2, 2
    )
    mixed = [
        (coloring, terms)
        for coloring, terms in sorted(fibres.items())
        if len(set(coloring)) > 1
    ]
    assert len(mixed) == 94
    assert all(len(terms) == 2 for _coloring, terms in mixed)
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
    remainder, _classes = signed.core.reduced_constant_product(
        signed.N, fibres, lattice, cells, cell_index
    )
    assert not remainder

    used_rows, used_colors = signed.core.minimize_zero_product_certificate(
        signed.N, fibres, rows, cells, cell_index
    )
    assert used_rows == (75,)
    assert used_colors == (1,)
    guarded = {
        cell
        for index in used_rows
        for _matching_number, decorated in mixed[index][1]
        for cell in decorated
    }
    assert len(guarded) == 6
    # The unsimplified cut has six negative support literals plus all 105
    # pure-term indicators for color one.  Four guard cells are forced target
    # units, so the full encoder removes them and stores 107 literals.
    assert len(guarded & forced) == 4
    assert len(guarded) + len(matchings) == 111
    assert len(guarded - forced) + len(matchings) == 107

    # Import locally to keep the main derivation above independent of the
    # production guard generator.
    import search_n8_toric_binomial_lazy_cegar as toric_search
    assert not any(
        guard <= selected
        for guard in toric_search.global_triangle_guards()
    )
    pure_matching_sets = {
        color: frozenset(
            frozenset(matchings[number])
            for number, _decorated in fibres[(color,) * signed.N]
        )
        for color in range(signed.Q)
    }
    one_row_hits = [
        schema
        for schema in toric_search.global_one_row_pure_zero_schemas()
        if schema[0] <= selected
        and pure_matching_sets[schema[1]] == schema[2]
    ]
    assert len(one_row_hits) == 2
    print(
        "PASS phase seed36: fibres {2:96,24:1}, 94 mixed binomials, "
        "consistent lattice, zero pure product, minimized cut row 75 / "
        "color 1 / guard 6 / forced intersection 4 / 107 simplified "
        "literals, two one-row-schema hits, no triangle guard"
    )


if __name__ == "__main__":
    main()
