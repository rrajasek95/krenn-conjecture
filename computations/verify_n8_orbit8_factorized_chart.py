#!/usr/bin/env python3
"""Independent exact audit of the 36-cell orbit-8 factorized chart."""

from __future__ import annotations

from collections import Counter

import factorized_laurent_branches as branches
import search_parallel_binomial_nonzero_constants_cegar as toric
from search_n8_sparse_triple_completion import (
    N,
    ORBIT8_BALANCED_REPAIR,
    SparseCompletionSearch,
    binomial_system,
    exact_fibres,
    reduced_polynomial,
)


SURVIVOR_EXTRA = frozenset({
    (0, 2, 2, 1), (0, 3, 1, 2),
    (0, 4, 2, 1), (0, 5, 1, 2),
    (1, 2, 2, 1), (1, 3, 1, 2),
    (1, 4, 2, 1), (1, 5, 1, 2),
})


def main():
    search = SparseCompletionSearch(
        None, "cadical300", orbit=8,
        fixed_cells=ORBIT8_BALANCED_REPAIR,
    )
    try:
        support = search.seed | SURVIVOR_EXTRA
        assert len(support) == 36
        fibres = exact_fibres(search, support)
        histogram = Counter(
            len(terms) for colouring, terms in fibres.items()
            if len(set(colouring)) > 1
        )
        assert histogram == {2: 16, 4: 94}
        assert [len(fibres[(colour,) * N]) for colour in range(3)] == [1, 4, 4]

        mixed, rows = binomial_system(search, fibres)
        consistent, lattice = toric.signed_quotient_lattice(
            rows, len(search.cells)
        )
        assert consistent
        assert len(rows) == 16
        assert len(lattice[0]) == 13

        remainders = {
            colouring: reduced_polynomial(search, terms, lattice)
            for colouring, terms in fibres.items()
            if len(set(colouring)) > 1 and len(terms) >= 3
        }
        remainders = {
            colouring: remainder
            for colouring, remainder in remainders.items()
            if remainder
        }
        assert len(remainders) == 62
        assert Counter(
            tuple(sorted(remainder.values()))
            for remainder in remainders.values()
        ) == {
            (-1, -1, -1, -1): 30,
            (-1, -1, 1, 1): 32,
        }
        assert all(
            branches.rectangle_factor_pair(remainder) is not None
            for remainder in remainders.values()
        )

        result = branches.solve_factorized_branches(
            remainders, rows, fibres, N,
            search.cells, search.cell_index,
        )
        assert result.status == "exhausted"
        assert len(result.factors) == 16
        assert len(result.clauses) == 32
        assert result.branches == 4
        assert result.inconsistent_branches == 2
        assert result.pure_zero_branches == 2
    finally:
        search.delete()

    print(
        "PASS cells=36 mixed={2:16,4:94} residuals=62 "
        "factors=16 clauses=32 branches=4 "
        "inconsistent=2 pure_zero=2"
    )


if __name__ == "__main__":
    main()

