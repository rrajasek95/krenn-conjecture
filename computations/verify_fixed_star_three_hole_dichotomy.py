#!/usr/bin/env python3
"""Exact audits for the fixed-star three-hole gauge dichotomy.

For odd J and q in the square-free site algebra, write C_j=H_(J-j)(q)
and D_ijk=H_(J-{i,j,k})(q).  After quotienting V_j by one coordinate
line, the common-power star map factors through

  Psi_(j,r)(u,(T_ik)) = u C_j + sum_(i<k; i,k!=j) T_ik D_ijk.

Psi has a universal 2(|J|-1)-dimensional expansion-gauge kernel.  The
script checks the exact expansion identity, constructs every gauge vector,
    and gives specializations for |J|=5,7,9 where this is the complete
kernel.  A maximal-rank minor modulo the prime proves that the gauge-rigid
locus is a nonempty Zariski-open subset over characteristic zero.
"""

from __future__ import annotations

import itertools
import random


P = 1_000_003
Q = 3


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def qentry(q, u: int, v: int, a: int, b: int) -> int:
    if u < v:
        return q[u, v][a][b]
    return q[v, u][b][a]


def hafnian_tensor(q, vertices: tuple[int, ...]):
    matchings = tuple(perfect_matchings(vertices))
    result = {}
    for coloring in itertools.product(range(Q), repeat=len(vertices)):
        local = dict(zip(vertices, coloring, strict=True))
        value = 0
        for matching in matchings:
            term = 1
            for u, v in matching:
                term = term * qentry(q, u, v, local[u], local[v]) % P
            value = (value + term) % P
        result[coloring] = value
    return result


def random_q(n: int, seed: int):
    rng = random.Random(seed)
    return {
        (u, v): tuple(
            tuple(rng.randrange(1, P) for _b in range(Q))
            for _a in range(Q)
        )
        for u, v in itertools.combinations(range(n), 2)
    }


def cofactor_families(q, n: int):
    vertices = tuple(range(n))
    c = {
        j: hafnian_tensor(q, tuple(v for v in vertices if v != j))
        for j in vertices
    }
    d = {
        triple: hafnian_tensor(
            q, tuple(v for v in vertices if v not in triple)
        )
        for triple in itertools.combinations(vertices, 3)
    }
    return c, d


def top_index(coloring: tuple[int, ...], j: int, r: int) -> int:
    """Index rows with the j-color restricted to the two colors != r."""
    allowed = tuple(color for color in range(Q) if color != r)
    digit = allowed.index(coloring[j])
    index = digit
    for site, color in enumerate(coloring):
        if site != j:
            index = index * Q + color
    return index


def psi_columns(q, n: int, j: int, r: int, c, d):
    vertices = tuple(range(n))
    allowed = tuple(color for color in range(Q) if color != r)
    row_count = 2 * Q ** (n - 1)
    columns: list[dict[int, int]] = []
    metadata = []

    rest_j = tuple(v for v in vertices if v != j)
    for color_j in allowed:
        column = {}
        for rest_colors, value in c[j].items():
            if value:
                full = [0] * n
                full[j] = color_j
                for site, color in zip(rest_j, rest_colors, strict=True):
                    full[site] = color
                column[top_index(tuple(full), j, r)] = value
        columns.append(column)
        metadata.append(("u", color_j))

    for i, k in itertools.combinations(rest_j, 2):
        triple = tuple(sorted((i, j, k)))
        outside = tuple(v for v in vertices if v not in triple)
        for color_i, color_j, color_k in itertools.product(
            range(Q), allowed, range(Q)
        ):
            column = {}
            for outside_colors, value in d[triple].items():
                if value:
                    full = [0] * n
                    full[i] = color_i
                    full[j] = color_j
                    full[k] = color_k
                    for site, color in zip(outside, outside_colors, strict=True):
                        full[site] = color
                    column[top_index(tuple(full), j, r)] = value
            columns.append(column)
            metadata.append(("t", i, k, color_i, color_j, color_k))

    expected = 2 + 18 * ((n - 1) * (n - 2) // 2)
    assert len(columns) == expected
    assert len(metadata) == len(columns)
    return row_count, columns, metadata


def sparse_rank(columns: list[dict[int, int]]) -> int:
    """Column rank over F_P by sparse incremental elimination."""
    pivots: dict[int, dict[int, int]] = {}
    for original in columns:
        vector = dict(original)
        while vector:
            pivot = min(vector)
            value = vector[pivot] % P
            if value == 0:
                del vector[pivot]
                continue
            if pivot not in pivots:
                inverse = pow(value, P - 2, P)
                vector = {
                    row: coefficient * inverse % P
                    for row, coefficient in vector.items()
                    if coefficient % P
                }
                pivots[pivot] = vector
                break
            factor = value
            basis = pivots[pivot]
            for row, coefficient in basis.items():
                updated = (vector.get(row, 0) - factor * coefficient) % P
                if updated:
                    vector[row] = updated
                elif row in vector:
                    del vector[row]
    return len(pivots)


def audit_expansion(q, n: int, j: int, r: int, c, d, columns) -> None:
    rng = random.Random(9000 + n)
    z = {
        site: tuple(rng.randrange(P) for _color in range(Q))
        for site in range(n)
    }
    vertices = tuple(range(n))
    rest_j = tuple(v for v in vertices if v != j)

    # Directly compute the quotient of F_q(z)=sum_i z_i C_i.
    direct = [0] * (2 * Q ** (n - 1))
    for coloring in itertools.product(range(Q), repeat=n):
        if coloring[j] == r:
            continue
        value = 0
        for site in vertices:
            outside = tuple(v for v in vertices if v != site)
            outside_colors = tuple(coloring[v] for v in outside)
            value += z[site][coloring[site]] * c[site][outside_colors]
        direct[top_index(coloring, j, r)] = value % P

    # Coordinates of the factorized vector in Psi's domain.
    coefficients = [z[j][color] for color in range(Q) if color != r]
    for i, k in itertools.combinations(rest_j, 2):
        for color_i, color_j, color_k in itertools.product(
            range(Q), (color for color in range(Q) if color != r), range(Q)
        ):
            value = (
                z[i][color_i] * qentry(q, j, k, color_j, color_k)
                + qentry(q, j, i, color_j, color_i) * z[k][color_k]
            ) % P
            coefficients.append(value)
    assert len(coefficients) == len(columns)

    factored = [0] * len(direct)
    for coefficient, column in zip(coefficients, columns, strict=True):
        if coefficient:
            for row, value in column.items():
                factored[row] = (factored[row] + coefficient * value) % P
    assert factored == direct


def audit_gauge_kernel(q, n: int, j: int, r: int, columns, metadata) -> int:
    """Construct G(w): u=sum_i w_i, T_ik=-(w_i+w_k) tensor q_ik."""
    allowed = tuple(color for color in range(Q) if color != r)
    metadata_index = {item: index for index, item in enumerate(metadata)}
    gauge_vectors = []
    for site in range(n):
        if site == j:
            continue
        for color_j in allowed:
            vector = {metadata_index[("u", color_j)]: 1}
            for i, k in itertools.combinations(
                tuple(v for v in range(n) if v != j), 2
            ):
                if site not in (i, k):
                    continue
                for color_i, color_k in itertools.product(range(Q), repeat=2):
                    value = -qentry(q, i, k, color_i, color_k) % P
                    if value:
                        index = metadata_index[
                            ("t", i, k, color_i, color_j, color_k)
                        ]
                        vector[index] = value
            gauge_vectors.append(vector)

            image = {}
            for coefficient_index, coefficient in vector.items():
                for row, value in columns[coefficient_index].items():
                    updated = (image.get(row, 0) + coefficient * value) % P
                    if updated:
                        image[row] = updated
                    elif row in image:
                        del image[row]
            assert not image

    gauge_rank = sparse_rank(gauge_vectors)
    assert gauge_rank == 2 * (n - 1)
    return gauge_rank


def det3(matrix) -> int:
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    ) % P


def audit_order(n: int, seed: int) -> None:
    q = random_q(n, seed)
    c, d = cofactor_families(q, n)
    assert all(det3(matrix) for matrix in q.values())
    rows, columns, metadata = psi_columns(q, n, j=0, r=0, c=c, d=d)
    audit_expansion(q, n, j=0, r=0, c=c, d=d, columns=columns)
    gauge_rank = audit_gauge_kernel(
        q, n, j=0, r=0, columns=columns, metadata=metadata
    )
    rank = sparse_rank(columns)
    print(
        f"|J|={n}: Psi_(0,0) {rows}x{len(columns)}, "
        f"rank={rank}, kernel={len(columns) - rank}=gauge {gauge_rank} over F_{P}"
    )
    assert len(columns) - rank == gauge_rank


def main() -> None:
    audit_order(5, 5105)
    audit_order(7, 7107)
    audit_order(9, 9109)
    print("three-hole identity and nonempty gauge-rigid/full-rank loci: PASS")


if __name__ == "__main__":
    main()
