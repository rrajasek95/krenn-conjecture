#!/usr/bin/env python3
"""Audit the retained response at the first two-extra frontier."""

from __future__ import annotations

from itertools import product

import explore_live_three_zero_minimal_two_extra_response as response


KINDS = ("01", "12", "02")
VALUES = (2, 3, 5, 7)


def main():
    expected_columns = tuple(
        [(site, row) for site in range(6) for row in range(3)]
        + [(6, 1), (6, 2)]
    )
    assert response.COLUMNS == expected_columns
    assert (6, 0) not in response.COLUMNS
    assert len(response.COLUMNS) == 20

    selected_by_chart = {}
    for kinds in product(KINDS, repeat=2):
        selected = response.select_labels(kinds, VALUES)
        assert len(selected) == 20, kinds
        assert all(
            (label[1], label[2]) != (0, 1)
            for _support, label in selected
        )
        selected_by_chart[kinds] = selected

    central = selected_by_chart[("01", "01")]
    determinant = response.flint_determinant(
        ("01", "01"),
        tuple(label for _support, label in central),
    )
    context = determinant.context()
    a, b, c, d = context.gens()
    q_polynomial = a*c + 3*a + 3*c + 6
    expected = (
        2**44 * 3**7
        * a**9 * c**10 * (b-d) * q_polynomial**5
    )
    assert determinant == expected

    print("minimal two-extra retained response frontier: PASS")
    print("all seven nonzero sites retained; exact column count=20")
    print("all nine row-plane chart products generically rank 20")
    print(
        "central divisor: a*c*(b-d)*(a*c+3*a+3*c+6)=0"
    )
    print("all selected rows direct-free")


if __name__ == "__main__":
    main()
