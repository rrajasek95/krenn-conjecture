#!/usr/bin/env python3
"""Test a uniform rectangle-span route for the diagonal subproblem.

Columns are ordered triples of perfect matchings of K_n.  For every proper
ordered even partition V=S_0+S_1+S_2 and every choice of outside matchings
K_r on V-S_r, the corresponding row is the indicator of the rectangle

    { K_r union H_r : H_r in PM(S_r) }_{r=0,1,2}.

At a diagonal weighted point, the weighted sum over such a rectangle is a
mixed coefficient times the fixed outside monomial, hence is zero.  If the
all-ones column vector belongs to the row span, these identities force the
product of the three pure hafnians to vanish.

This exploratory checker works modulo a prime and currently targets n=6.
"""

from __future__ import annotations

import argparse
import itertools


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for pos in range(1, len(vertices)):
        second = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def matching_mask(matching, edge_index):
    answer = 0
    for edge in matching:
        answer |= 1 << edge_index[tuple(sorted(edge))]
    return answer


def rectangle_rows(n: int):
    vertices = tuple(range(n))
    edges = tuple(itertools.combinations(vertices, 2))
    edge_index = {edge: index for index, edge in enumerate(edges)}
    matchings = tuple(perfect_matchings(vertices))
    masks = tuple(matching_mask(matching, edge_index) for matching in matchings)
    matching_index = {mask: index for index, mask in enumerate(masks)}
    full = (1 << n) - 1

    pms_by_vertex_mask = {}
    for vertex_mask in range(1 << n):
        if vertex_mask.bit_count() % 2:
            continue
        subset = tuple(v for v in vertices if vertex_mask >> v & 1)
        pms_by_vertex_mask[vertex_mask] = tuple(
            matching_mask(matching, edge_index) for matching in perfect_matchings(subset)
        )

    seen_partitions = set()
    for coloring in itertools.product(range(3), repeat=n):
        shores = [0, 0, 0]
        for vertex, color in enumerate(coloring):
            shores[color] |= 1 << vertex
        shores = tuple(shores)
        if shores in seen_partitions:
            continue
        seen_partitions.add(shores)
        if any(shore.bit_count() % 2 for shore in shores):
            continue
        if full in shores:
            continue

        outside_options = [pms_by_vertex_mask[full ^ shore] for shore in shores]
        inside_options = [pms_by_vertex_mask[shore] for shore in shores]
        for outside in itertools.product(*outside_options):
            choices = []
            for color in range(3):
                choices.append(
                    tuple(matching_index[outside[color] | inside]
                          for inside in inside_options[color])
                )
            row = tuple(
                (a * len(matchings) + b) * len(matchings) + c
                for a, b, c in itertools.product(*choices)
            )
            yield len(matchings) ** 3, row


def reduce_rows(n: int, prime: int):
    """Incremental sparse elimination; also reduce the all-ones target."""
    basis: dict[int, dict[int, int]] = {}
    target = None
    row_count = 0
    column_count = None

    def reduce(vector: dict[int, int]):
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                scale = pow(vector[pivot], -1, prime)
                return {key: value * scale % prime for key, value in vector.items()}
            coefficient = vector[pivot]
            for key, value in basis[pivot].items():
                updated = (vector.get(key, 0) - coefficient * value) % prime
                if updated:
                    vector[key] = updated
                else:
                    vector.pop(key, None)
        return vector

    for column_count, row in rectangle_rows(n):
        row_count += 1
        vector = reduce({column: 1 for column in row})
        if vector:
            basis[min(vector)] = vector
    assert column_count is not None
    target = reduce({column: 1 for column in range(column_count)})
    print(
        f"n={n} rows={row_count} columns={column_count} rank={len(basis)} "
        f"ones_in_span={not target} prime={prime}"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument("--prime", type=int, default=1_000_003)
    args = parser.parse_args()
    reduce_rows(args.n, args.prime)


if __name__ == "__main__":
    main()
