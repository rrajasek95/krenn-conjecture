#!/usr/bin/env python3
"""Discover S_n-invariant quadratic equations for binary matching tensors.

This is a finite-field discovery tool.  A quadratic monomial T_c T_d is
classified under simultaneous vertex permutations and interchange of the
two copies by the four contingency counts n_00,n_01,n_10,n_11.  We sample
arbitrary 2 by 2 aggregate edge matrices, evaluate the orbit sums, and row
reduce over a prime field.  Any candidate relation is then checked on fresh
samples and evaluated on e0^n+e1^n+(e0+e1)^n.
"""

from __future__ import annotations

import argparse
import itertools
import random


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for k in range(1, len(vertices)):
        v = vertices[k]
        rest = vertices[1:k] + vertices[k + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def canonical_type(c, d):
    counts = [0, 0, 0, 0]
    for x, y in zip(c, d):
        counts[2 * x + y] += 1
    swapped = (counts[0], counts[2], counts[1], counts[3])
    return min(tuple(counts), swapped)


def orbit_partition(n):
    words = tuple(itertools.product((0, 1), repeat=n))
    groups = {}
    for i, c in enumerate(words):
        for j in range(i, len(words)):
            key = canonical_type(c, words[j])
            groups.setdefault(key, []).append((i, j))
    keys = tuple(sorted(groups))
    return words, keys, tuple(tuple(groups[key]) for key in keys)


def output_tensor(n, words, matchings, matrices, prime):
    result = []
    for coloring in words:
        total = 0
        for matching in matchings:
            term = 1
            for u, v in matching:
                term = term * matrices[u, v][coloring[u]][coloring[v]] % prime
            total += term
        result.append(total % prime)
    return result


def features(tensor, groups, prime):
    return [sum(tensor[i] * tensor[j] for i, j in group) % prime
            for group in groups]


def rref(rows, prime):
    a = [list(map(lambda x: x % prime, row)) for row in rows]
    if not a:
        return a, []
    m, n = len(a), len(a[0])
    pivots = []
    row = 0
    for col in range(n):
        pivot = next((i for i in range(row, m) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        inv = pow(a[row][col], -1, prime)
        a[row] = [(x * inv) % prime for x in a[row]]
        for i in range(m):
            if i != row and a[i][col]:
                factor = a[i][col]
                a[i] = [(x - factor * y) % prime
                        for x, y in zip(a[i], a[row])]
        pivots.append(col)
        row += 1
        if row == m:
            break
    return a[:row], pivots


def nullspace(rref_rows, pivots, columns, prime):
    pivot_set = set(pivots)
    basis = []
    for free in range(columns):
        if free in pivot_set:
            continue
        vector = [0] * columns
        vector[free] = 1
        for row, pivot in reversed(list(zip(rref_rows, pivots))):
            vector[pivot] = -sum(row[j] * vector[j]
                                 for j in range(pivot + 1, columns)) % prime
        basis.append(vector)
    return basis


def random_matrices(n, rng, prime):
    answer = {}
    for u in range(n):
        for v in range(u + 1, n):
            answer[u, v] = tuple(
                tuple(rng.randrange(prime) for _ in range(2))
                for _ in range(2)
            )
    return answer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=8)
    parser.add_argument("--prime", type=int, default=1000003)
    parser.add_argument("--samples", type=int, default=220)
    parser.add_argument("--checks", type=int, default=40)
    parser.add_argument("--seed", type=int, default=20260724)
    args = parser.parse_args()

    n, prime = args.n, args.prime
    words, keys, groups = orbit_partition(n)
    matchings = tuple(perfect_matchings(range(n)))
    rng = random.Random(args.seed)
    rows = []
    for _ in range(args.samples):
        tensor = output_tensor(
            n, words, matchings, random_matrices(n, rng, prime), prime
        )
        rows.append(features(tensor, groups, prime))
    reduced, pivots = rref(rows, prime)
    kernel = nullspace(reduced, pivots, len(keys), prime)
    print(
        f"n={n} words={len(words)} matchings={len(matchings)} "
        f"quadratic_orbits={len(keys)} rank={len(pivots)} "
        f"kernel={len(kernel)}",
        flush=True,
    )

    for _ in range(args.checks):
        tensor = output_tensor(
            n, words, matchings, random_matrices(n, rng, prime), prime
        )
        row = features(tensor, groups, prime)
        assert all(sum(x * y for x, y in zip(vector, row)) % prime == 0
                   for vector in kernel)

    target = [1 + int(not any(c)) + int(all(c)) for c in words]
    target_row = features(target, groups, prime)
    separating = [
        vector for vector in kernel
        if sum(x * y for x, y in zip(vector, target_row)) % prime
    ]
    print(f"fresh_checks={args.checks} separating={len(separating)}")
    for number, vector in enumerate(separating[:5]):
        value = sum(x * y for x, y in zip(vector, target_row)) % prime
        support = [(keys[i], x if x <= prime // 2 else x - prime)
                   for i, x in enumerate(vector) if x]
        print(f"separator={number} value={value} support={support}")


if __name__ == "__main__":
    main()
