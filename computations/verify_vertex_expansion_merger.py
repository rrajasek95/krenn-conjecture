#!/usr/bin/env python3
"""Exact integer audit of the K4 vertex-expansion sector and merger identities."""

from __future__ import annotations

import itertools

import numpy as np


Q = 3
C = tuple(range(5))
U = tuple(range(5, 8))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    a = vertices[0]
    for pos in range(1, len(vertices)):
        b = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1 :]
        for tail in perfect_matchings(rest):
            yield ((min(a, b), max(a, b)),) + tail


def tensor_for_matching(matching, matrices, vertices):
    letters = "abcdefgh"
    inputs = []
    operands = []
    for edge in matching:
        a, b = edge
        inputs.append(letters[vertices.index(a)] + letters[vertices.index(b)])
        operands.append(matrices[edge])
    return np.einsum(
        ",".join(inputs) + "->" + letters[: len(vertices)],
        *operands,
        optimize=True,
    )


def matching_tensor(vertices, matrices):
    result = np.zeros((Q,) * len(vertices), dtype=np.int64)
    count = 0
    for matching in perfect_matchings(vertices):
        result += tensor_for_matching(matching, matrices, vertices)
        count += 1
    return result, count


def embed_one_cross(k_r, r):
    """Multiply K_r by E_rr on the other two terminal slots."""
    result = np.zeros((Q,) * 8, dtype=np.int64)
    for colors_c in itertools.product(range(Q), repeat=5):
        for terminal_color in range(Q):
            colors = list(colors_c) + [r, r, r]
            colors[5 + r] = terminal_color
            result[tuple(colors)] = k_r[colors_c + (terminal_color,)]
    return result


def main():
    rng = np.random.default_rng(20260724)
    internal = {
        edge: rng.integers(-2, 3, size=(Q, Q), dtype=np.int64)
        for edge in itertools.combinations(C, 2)
    }
    boundary = {
        (c, 5 + r): rng.integers(-2, 3, size=(Q, Q), dtype=np.int64)
        for c in C
        for r in range(3)
    }

    one = []
    for r in range(3):
        vertices = C + (5 + r,)
        matrices = internal | {
            (c, 5 + r): boundary[c, 5 + r]
            for c in C
        }
        value, count = matching_tensor(vertices, matrices)
        assert count == 15
        one.append(value)

    # Terminal merger: sum the three boundary families at one new vertex.
    star = 5
    merged = internal | {
        (c, star): sum(
            (boundary[c, 5 + r] for r in range(3)),
            start=np.zeros((Q, Q), dtype=np.int64),
        )
        for c in C
    }
    merged_tensor, merged_count = matching_tensor(C + (star,), merged)
    assert merged_count == 15
    assert np.array_equal(merged_tensor, sum(one))

    # Put E_rr on the old edge opposite terminal r and audit the 1/3 split.
    expanded = internal | boundary
    for a, b in itertools.combinations(U, 2):
        missing = ({0, 1, 2} - {a - 5, b - 5}).pop()
        matrix = np.zeros((Q, Q), dtype=np.int64)
        matrix[missing, missing] = 1
        expanded[a, b] = matrix

    full = np.zeros((Q,) * 8, dtype=np.int64)
    high = np.zeros_like(full)
    one_count = 0
    high_count = 0
    for matching in perfect_matchings(C + U):
        crossings = sum((a in C) != (b in C) for a, b in matching)
        term = tensor_for_matching(matching, expanded, C + U)
        full += term
        if crossings == 1:
            one_count += 1
        elif crossings == 3:
            high += term
            high_count += 1
        else:
            raise AssertionError(f"unexpected crossing number {crossings}")
    reconstructed = high.copy()
    for r in range(3):
        reconstructed += embed_one_cross(one[r], r)
    assert one_count == 45
    assert high_count == 60
    assert one_count + high_count == 105
    assert np.array_equal(full, reconstructed)

    print("verified terminal merger H6=sum_r K_r (15 matching terms)")
    print("verified expanded K4 split: 45 one-cross + 60 three-cross = 105")
    print("all coefficient comparisons exact over the integers")


if __name__ == "__main__":
    main()
