#!/usr/bin/env python3
"""Exact Laurent-fiber certificates for residual |F|=1 support charts.

No polynomial solver is trusted here.  The script enumerates perfect
matchings from the stated supports and checks the claimed exponent-vector
identities over the integers.  An odd coefficient sum means that the
corresponding product of binomial equations reads ``1=-1``.
"""

from __future__ import annotations

from analyze_one_exceptional_edge import CHARTS, MATCHINGS, chart_data


SPARSE_CERTIFICATES = {
    "same": (
        ((0, 0, 1, 0, 0, 0), -1),
        ((0, 0, 1, 1, 0, 2), 1),
        ((0, 0, 1, 1, 1, 1), 1),
    ),
    "different": (
        ((0, 0, 0, 1, 0, 0), -1),
        ((0, 0, 2, 1, 1, 0), 1),
        ((0, 0, 2, 1, 2, 2), 1),
    ),
}

FULL_TRINOMIALS = (
    (0, 0, 0, 1, 0, 0),
    (0, 0, 2, 0, 1, 0),
)

FULL_RATIO_CERTIFICATES = (
    (
        1,
        1,
        (
            ((0, 0, 1, 1, 1, 1), -1),
            ((0, 1, 2, 0, 1, 0), 1),
            ((0, 1, 2, 1, 1, 0), -1),
        ),
    ),
    (
        2,
        0,
        (
            ((0, 0, 1, 0, 1, 1), -1),
            ((0, 0, 2, 0, 2, 2), 1),
            ((1, 1, 0, 0, 0, 0), 1),
            ((1, 1, 0, 1, 0, 0), -1),
        ),
    ),
)


def subtract(first, second):
    return tuple(a - b for a, b in zip(first, second, strict=True))


def add_scaled(total, vector, coefficient):
    return tuple(
        old + coefficient * value
        for old, value in zip(total, vector, strict=True)
    )


def fibers_by_coloring(chart_name):
    keys, fibers = chart_data(chart_name)
    return keys, {
        coloring: monomials for coloring, monomials, target in fibers
        if target == 0
    }


def supported_matching_indices(chart_name, coloring):
    exceptional_support, factor_supports = CHARTS[chart_name]
    answer = []
    for index, matching in enumerate(MATCHINGS):
        supported = all(
            (
                f"{coloring[u]}{coloring[v]}" in exceptional_support
                if (u, v) == (0, 1)
                else str(coloring[u]) in factor_supports[u, v][0]
                and str(coloring[v]) in factor_supports[u, v][1]
            )
            for u, v in matching
        )
        if supported:
            answer.append(index)
    return tuple(answer)


def verify_sparse_chart(chart_name):
    keys, fibers = fibers_by_coloring(chart_name)
    total = (0,) * len(keys)
    coefficient_sum = 0
    for coloring, coefficient in SPARSE_CERTIFICATES[chart_name]:
        monomials = fibers[coloring]
        assert len(monomials) == 2
        assert len(supported_matching_indices(chart_name, coloring)) == 2
        total = add_scaled(
            total, subtract(monomials[0], monomials[1]), coefficient
        )
        coefficient_sum += coefficient
    assert total == (0,) * len(keys)
    assert coefficient_sum % 2 == 1
    print(
        f"{chart_name}: three exact binomial fibers multiply to 1=-1"
    )


def verify_full_chart():
    chart_name = "full-after-odd-cuts"
    keys, fibers = fibers_by_coloring(chart_name)
    first = fibers[FULL_TRINOMIALS[0]]
    second = fibers[FULL_TRINOMIALS[1]]
    assert len(first) == len(second) == 3
    assert len(supported_matching_indices(chart_name, FULL_TRINOMIALS[0])) == 3
    assert len(supported_matching_indices(chart_name, FULL_TRINOMIALS[1])) == 3

    verified_parities = []
    for term_index, expected_parity, certificate in FULL_RATIO_CERTIFICATES:
        target = subtract(
            subtract(first[term_index], first[0]),
            subtract(second[term_index], second[0]),
        )
        total = (0,) * len(keys)
        coefficient_sum = 0
        for coloring, coefficient in certificate:
            monomials = fibers[coloring]
            assert len(monomials) == 2
            assert len(supported_matching_indices(chart_name, coloring)) == 2
            total = add_scaled(
                total,
                subtract(monomials[0], monomials[1]),
                coefficient,
            )
            coefficient_sum += coefficient
        assert total == target
        assert coefficient_sum % 2 == expected_parity
        verified_parities.append(expected_parity)

    assert tuple(verified_parities) == (1, 0)
    print(
        "full-after-odd-cuts: translated trinomials have signs "
        "(1,0), forcing twice a nonzero monomial to vanish"
    )


def main():
    verify_sparse_chart("same")
    verify_sparse_chart("different")
    verify_full_chart()
    print("all one-exceptional-edge Laurent certificates verified exactly")


if __name__ == "__main__":
    main()
