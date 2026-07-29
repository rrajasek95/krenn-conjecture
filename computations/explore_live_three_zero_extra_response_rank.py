#!/usr/bin/env python3
"""Exploratory modular ranks for the remaining extra-singular response."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations, product
from random import Random

import sympy as sp


PRIME = 1_000_003
HESSIAN = ((0, 1, 2), (1, 0, 3), (2, 3, 0))
DIRECT = ((0, 1, 0), (1, 0, 0), (0, 0, 0))
IDENTITY = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
TYPE_10 = ((1, 0, 0), (0, 1, 0), (0, 0, 0))
MISS_2 = ((1, 0, 2), (0, 1, 3), (0, 0, 0))
MISS_0 = ((0, 0, 0), (1, 0, 4), (0, 1, 5))
MISS_1 = ((1, 0, 6), (0, 0, 0), (0, 1, 7))


def inverse(value: int) -> int:
    return pow(value % PRIME, PRIME - 2, PRIME)


def matrix_product(left, middle, right_transpose):
    return tuple(
        tuple(
            sum(
                left[row][a] * middle[a][b] * right_transpose[column][b]
                for a in range(3)
                for b in range(3)
            )
            % PRIME
            for column in range(3)
        )
        for row in range(3)
    )


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    first = vertices[0]
    return tuple(
        ((first, vertices[position]),) + tail
        for position in range(1, len(vertices))
        for tail in perfect_matchings(
            vertices[1:position] + vertices[position + 1 :]
        )
    )


def response_rank(
    matrices,
    betas,
    active_sites,
    shuffle_seed=None,
    hessian=HESSIAN,
    direct=DIRECT,
    excluded_sources=(),
):
    site_count = len(matrices)
    columns = tuple(
        (site, colour) for colour in range(3) for site in active_sites
    )
    column_index = {column: index for index, column in enumerate(columns)}
    blocks = {}
    for left, right in combinations(range(site_count), 2):
        numerator = matrix_product(
            matrices[left], hessian, matrices[right]
        )
        scale = inverse(betas[left] + betas[right])
        blocks[left, right] = tuple(
            tuple(scale * entry % PRIME for entry in row)
            for row in numerator
        )

    def edge(word, left, right):
        if left < right:
            return blocks[left, right][word[left]][word[right]]
        return blocks[right, left][word[right]][word[left]]

    @lru_cache(maxsize=None)
    def hafnian(word, vertices):
        return sum(
            (
                product_mod(
                    edge(word, left, right) for left, right in matching
                )
                for matching in perfect_matchings(vertices)
            ),
            0,
        ) % PRIME

    def response_row(word, source_left, source_right):
        row = [0] * len(columns)
        direct_weight = direct[source_left][source_right]
        if direct_weight:
            for star_site in active_sites:
                remaining = tuple(
                    site for site in range(site_count) if site != star_site
                )
                row[column_index[star_site, word[star_site]]] += (
                    direct_weight * hafnian(word, remaining)
                )
        for u, v in combinations(range(site_count), 2):
            marked_weight = (
                matrices[u][word[u]][source_left]
                * matrices[v][word[v]][source_right]
                + matrices[u][word[u]][source_right]
                * matrices[v][word[v]][source_left]
            ) % PRIME
            if not marked_weight:
                continue
            for star_site in active_sites:
                if star_site in (u, v):
                    continue
                remaining = tuple(
                    site
                    for site in range(site_count)
                    if site not in (u, v, star_site)
                )
                row[column_index[star_site, word[star_site]]] += (
                    marked_weight * hafnian(word, remaining)
                )
        return [entry % PRIME for entry in row]

    basis = {}
    basis_labels = {}
    rows_seen = 0
    descriptors = [
        (word, source_left, source_right)
        for word in product(range(3), repeat=site_count)
        for source_left, source_right in product(range(3), repeat=2)
        if (source_left, source_right) not in excluded_sources
    ]
    if shuffle_seed is not None:
        Random(shuffle_seed).shuffle(descriptors)
    for word, source_left, source_right in descriptors:
            row = response_row(word, source_left, source_right)
            rows_seen += 1
            while any(row):
                pivot = next(index for index, entry in enumerate(row) if entry)
                if pivot not in basis:
                    scale = inverse(row[pivot])
                    basis[pivot] = [
                        scale * entry % PRIME for entry in row
                    ]
                    basis_labels[pivot] = (
                        word,
                        source_left,
                        source_right,
                    )
                    break
                scale = row[pivot]
                row = [
                    (entry - scale * basis_entry) % PRIME
                    for entry, basis_entry in zip(row, basis[pivot])
                ]
            if len(basis) == len(columns):
                return (
                    len(basis),
                    len(columns),
                    rows_seen,
                    tuple(basis_labels[pivot] for pivot in sorted(basis_labels)),
                )
    return (
        len(basis),
        len(columns),
        rows_seen,
        tuple(basis_labels[pivot] for pivot in sorted(basis_labels)),
    )


def product_mod(values):
    answer = 1
    for value in values:
        answer = answer * value % PRIME
    return answer


def audit_case(name, live_count, extras):
    for exceptional_count in range(live_count + 1):
        live_betas = tuple(
            [index + 2 for index in range(exceptional_count)]
            + [1] * (live_count - exceptional_count)
        )
        matrices = (
            (IDENTITY,) * live_count
            + (TYPE_10, TYPE_10)
            + tuple(extras)
        )
        betas = live_betas + (1,) * (2 + len(extras))
        active_sites = tuple(
            range(exceptional_count, live_count)
        ) + tuple(range(live_count, len(matrices)))
        rank, columns, rows_seen, _ = response_rank(
            matrices, betas, active_sites
        )
        print(
            f"{name}, t={exceptional_count}: "
            f"rank={rank}/{columns}, rows<={rows_seen}"
        )


def symbolic_minimal_chart_determinant(
    labels=None,
    simplify_hessian=False,
    symbolic_direct=False,
    chart="01",
    verbose=True,
):
    """Factor one response minor on a normalized kernel chart."""
    a, b = sp.symbols("a b")
    if simplify_hessian:
        h01 = h02 = h12 = sp.S.One
        mu = sp.S.One
    else:
        h01, h02, h12 = sp.symbols("h01 h02 h12")
        mu = sp.Symbol("mu")
    nu0, nu1 = sp.symbols("nu0 nu1")
    direct_scale = (
        sp.Symbol("lambda")
        if symbolic_direct
        else sp.S.One
    )
    hessian = sp.Matrix(
        [[0, h01, h02], [h01, 0, h12], [h02, h12, 0]]
    )
    if chart == "01":
        extra_matrix = sp.Matrix(
            [[1, 0, a], [0, 1, b], [0, 0, 0]]
        )
    elif chart == "12":
        extra_matrix = sp.Matrix(
            [[a, 1, 0], [b, 0, 1], [0, 0, 0]]
        )
    else:
        raise ValueError(f"unsupported chart: {chart}")
    matrices = (
        sp.eye(3),
        sp.eye(3),
        sp.diag(1, 1, 0),
        sp.diag(1, 1, 0),
        extra_matrix,
    )
    betas = (nu0, nu1, mu, mu, mu)
    active_sites = (2, 3, 4)
    columns = tuple(
        (site, colour) for colour in range(3) for site in active_sites
    )
    column_index = {column: index for index, column in enumerate(columns)}
    blocks = {
        (left, right): (
            matrices[left]
            * hessian
            * matrices[right].T
            / (betas[left] + betas[right])
        )
        for left, right in combinations(range(5), 2)
    }

    def edge(word, left, right):
        if left < right:
            return blocks[left, right][word[left], word[right]]
        return blocks[right, left][word[right], word[left]]

    def hafnian(word, vertices):
        return sum(
            (
                sp.prod(edge(word, left, right) for left, right in matching)
                for matching in perfect_matchings(vertices)
            ),
            sp.S.Zero,
        )

    def row(word, source_left, source_right):
        result = [sp.S.Zero] * len(columns)
        direct_weight = int(
            source_left != source_right
            and {source_left, source_right} == {0, 1}
        ) * direct_scale
        if direct_weight:
            for star_site in active_sites:
                remaining = tuple(site for site in range(5) if site != star_site)
                result[column_index[star_site, word[star_site]]] += (
                    direct_weight * hafnian(word, remaining)
                )
        for u, v in combinations(range(5), 2):
            marked_weight = (
                matrices[u][word[u], source_left]
                * matrices[v][word[v], source_right]
                + matrices[u][word[u], source_right]
                * matrices[v][word[v], source_left]
            )
            if marked_weight == 0:
                continue
            for star_site in active_sites:
                if star_site in (u, v):
                    continue
                remaining = tuple(
                    site
                    for site in range(5)
                    if site not in (u, v, star_site)
                )
                result[column_index[star_site, word[star_site]]] += (
                    marked_weight * hafnian(word, remaining)
                )
        return result

    if labels is None:
        labels = (
            ((0, 0, 0, 0, 0), 0, 0),
            ((0, 0, 0, 1, 0), 0, 0),
            ((0, 0, 0, 1, 0), 0, 1),
            ((0, 0, 1, 0, 0), 0, 0),
            ((0, 0, 0, 1, 1), 0, 0),
            ((0, 0, 1, 1, 0), 0, 0),
            ((0, 0, 2, 0, 0), 0, 0),
            ((0, 0, 0, 2, 0), 0, 0),
            ((0, 0, 0, 1, 2), 0, 0),
        )
    minor = sp.Matrix([row(*label) for label in labels])
    determinant = sp.factor(sp.cancel(minor.det(method="domain-ge")))
    if verbose:
        print("minimal one-extra symbolic minor determinant:")
        print(determinant)
    return determinant


def main():
    audit_case("one-extra-M2/U2", 2, (MISS_2,))
    audit_case("two-extra-M2M0/U3", 3, (MISS_2, MISS_0))
    audit_case("three-extra-M2M0M1/U2", 2, (MISS_2, MISS_0, MISS_1))
    symbolic_minimal_chart_determinant()


if __name__ == "__main__":
    main()
