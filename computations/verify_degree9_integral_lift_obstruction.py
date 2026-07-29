#!/usr/bin/env python3
"""Verify the integral lift of the six-site characteristic-two certificate.

The saved GF(2) certificate expresses

    P = F_000000 F_111111 F_222222

as a sum of mixed-coefficient Macaulay columns modulo two.  This verifier
uses the independently reconstructed *integer* H-orbit matrix to check the
stronger identity

    P - sum(selected integral orbit columns) = 2 R.          (1)

Every monomial occurring in (1) is a perfect matching of all 18
vertex/color stubs.  In particular every monomial of R has degree one at
each stub (v,a), so its exponent vector is a color-balanced Farkas witness.

At a characteristic-zero point with all mixed coefficients zero and the
three uniform coefficients equal to one, (1) gives R(A)=1/2.  Over any
2-adic valuation, the ultrametric inequality therefore forces at least one
monomial of R to have negative source-entry valuation.  Its balanced
exponent vector obstructs every target-preserving diagonal integral gauge.
The final valuation inference is mathematical; this script audits all of
its finite combinatorial and integral-certificate premises.
"""

from __future__ import annotations

import gzip
import pickle
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
N = 6
Q = 3
STUBS = N * Q


def bit_indices(code: int):
    while code:
        low = code & -code
        yield low.bit_length() - 1
        code ^= low


def main() -> None:
    with (HERE / "degree9_source_ideal_char2_h27.pkl").open("rb") as stream:
        parity = pickle.load(stream)
    with (HERE / "degree9_source_ideal_h27_integer.pkl").open("rb") as stream:
        integral = pickle.load(stream)
    with gzip.open(
        HERE / "certificates" / "degree9_char2_h27_membership.pkl.gz", "rb"
    ) as stream:
        certificate = pickle.load(stream)

    rows, columns = integral["shape"]
    assert (rows, columns) == (
        len(parity["row_codes"]),
        len(parity["columns"]),
    )
    assert certificate["shape"] == (rows, columns)
    assert certificate["field"] == "GF(2)"
    assert certificate["group_order"] == 27

    selected = certificate["selected_columns"]
    assert len(selected) == 77_179
    assert len(set(selected)) == len(selected)
    assert all(0 <= column < columns for column in selected)

    # In a full H-orbit sum, ``column_size * raw incidence`` is spread
    # uniformly over a row orbit of size ``row_size``.  Hence this quotient
    # is the coefficient of each individual monomial in that row orbit.
    selected_sum = [0] * rows
    offsets = integral["offsets"]
    row_indices = integral["row_indices"]
    coefficients = integral["coefficients"]
    row_sizes = integral["row_sizes"]
    column_sizes = integral["column_sizes"]
    for column in selected:
        column_size = column_sizes[column]
        for position in range(offsets[column], offsets[column + 1]):
            row = row_indices[position]
            numerator = column_size * coefficients[position]
            assert numerator % row_sizes[row] == 0
            selected_sum[row] += numerator // row_sizes[row]

    target = list(parity["rhs"])
    differences = [p - c for p, c in zip(target, selected_sum)]
    assert all(value % 2 == 0 for value in differences)
    residual = [value // 2 for value in differences]

    # Independently recover the original mod-two relation from the integral
    # one.  This also catches any mismatch in orbit normalizations.
    assert all((selected_sum[row] & 1) == target[row] for row in range(rows))

    # Every row monomial is a matching of all 18 vertex/color stubs.  Thus it
    # has degree exactly one at each (vertex,color) mode.  This is precisely
    # the balanced multidegree needed by the valuation/Farkas argument.
    valid_edges = tuple(
        (a, b)
        for a in range(STUBS)
        for b in range(a + 1, STUBS)
        if a // Q != b // Q
    )
    assert len(valid_edges) == 135
    for code in parity["row_codes"]:
        edge_indices = tuple(bit_indices(code))
        assert len(edge_indices) == STUBS // 2
        endpoint_degrees = [0] * STUBS
        for edge_index in edge_indices:
            a, b = valid_edges[edge_index]
            assert a // Q != b // Q
            endpoint_degrees[a] += 1
            endpoint_degrees[b] += 1
        assert endpoint_degrees == [1] * STUBS

    # The target is exactly the product of the three uniform cubics: one
    # independent six-vertex perfect matching in each color.  The weighted
    # orbit count must therefore be 15^3.
    assert sum(
        row_sizes[row] for row, value in enumerate(target) if value
    ) == 15**3

    residual_counts = Counter(residual)
    assert residual_counts[0] < rows
    assert max(residual) == 0
    assert min(residual) == -12

    cached_residual = HERE / "degree9_char2_first_integral_residual.pkl.gz"
    if cached_residual.exists():
        with gzip.open(cached_residual, "rb") as stream:
            cached = pickle.load(stream)
        assert cached["version"] == 1
        assert list(cached["coefficients"]) == residual

    print(
        "verified integral lift P - sum(C_j) = 2R: "
        f"{len(selected)} selected orbit columns, "
        f"{sum(value != 0 for value in residual)} nonzero residual row orbits"
    )
    print(
        "verified balanced support: every residual monomial is a perfect "
        "matching of all 18 vertex/color stubs"
    )
    print(
        "consequence: at any normalized characteristic-zero solution, "
        "R(A)=1/2 forces a negative color-balanced 2-adic monomial"
    )


if __name__ == "__main__":
    main()
