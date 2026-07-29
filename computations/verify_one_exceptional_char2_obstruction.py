#!/usr/bin/env python3
"""Exact Laurent-lattice obstruction for two residual charts in char 2.

All calculations are over the integers.  Mixed binomial fibers identify
their two Laurent monomials in characteristic two.  Their exponent lattice
is saturated, and in the indicated mixed trinomial fiber all three exponent
vectors of two terms have the same quotient class.  Those two cancel and
leave the third nonzero monomial.
"""

from __future__ import annotations

import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

from analyze_one_exceptional_edge import chart_data


WITNESSES = {
    "same": (0, 0, 2, 2, 2, 2),
    "different": (0, 0, 1, 1, 1, 1),
}


def difference(first, second):
    return [a - b for a, b in zip(first, second, strict=True)]


def verify(chart_name, witness_coloring):
    keys, fibers = chart_data(chart_name)
    binomial_rows = []
    witness = None
    for coloring, monomials, target in fibers:
        if target == 0 and len(monomials) == 2:
            binomial_rows.append(difference(monomials[1], monomials[0]))
        if coloring == witness_coloring:
            assert target == 0 and len(monomials) == 3
            witness = monomials
    assert witness is not None

    lattice_matrix = sp.Matrix(binomial_rows)
    rank = lattice_matrix.rank()
    smith = smith_normal_form(lattice_matrix, domain=ZZ)
    invariant_factors = [
        abs(int(smith[index, index]))
        for index in range(min(smith.shape))
        if smith[index, index]
    ]
    assert len(invariant_factors) == rank
    assert set(invariant_factors) == {1}

    augmented = sp.Matrix(
        binomial_rows + [difference(witness[2], witness[1])]
    )
    assert augmented.rank() == rank

    print(
        f"{chart_name}: {len(keys)} Laurent variables, binomial-lattice "
        f"rank {rank}, saturated Smith factors; in fiber {witness_coloring} "
        "the last two monomials agree and cancel, leaving the first nonzero"
    )


def main():
    for chart_name, coloring in WITNESSES.items():
        verify(chart_name, coloring)
    print("exact characteristic-two one-edge chart obstruction verified")


if __name__ == "__main__":
    main()
