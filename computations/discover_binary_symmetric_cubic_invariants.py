#!/usr/bin/env python3
"""Search for S_8-invariant cubic equations of binary matching tensors.

The calculation is exact over a small prime.  Cubic output monomials are
quotiented by simultaneous vertex permutations and permutation of the three
polynomial copies.  NumPy evaluates all orbit sums, while python-flint does
the modular rank/nullspace calculation.
"""

from __future__ import annotations

import argparse
from array import array
import itertools

import numpy as np
from flint import nmod_mat


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


PERMS = tuple(itertools.permutations(range(3)))


def permute_counts(counts, permutation):
    result = [0] * 8
    for pattern, count in enumerate(counts):
        bits = ((pattern >> 2) & 1, (pattern >> 1) & 1, pattern & 1)
        image = ((bits[permutation[0]] << 2)
                 | (bits[permutation[1]] << 1)
                 | bits[permutation[2]])
        result[image] = count
    return tuple(result)


def triple_type(i, j, k, n):
    counts = [0] * 8
    for position in range(n):
        shift = n - 1 - position
        pattern = (((i >> shift) & 1) << 2
                   | ((j >> shift) & 1) << 1
                   | ((k >> shift) & 1))
        counts[pattern] += 1
    return min(permute_counts(counts, permutation) for permutation in PERMS)


def build_cubic_orbits(n):
    count = 1 << n
    first, second, third = array("B"), array("B"), array("B")
    orbit_numbers = array("H")
    key_to_orbit = {}
    keys = []
    for i in range(count):
        for j in range(i, count):
            for k in range(j, count):
                key = triple_type(i, j, k, n)
                orbit = key_to_orbit.get(key)
                if orbit is None:
                    orbit = len(keys)
                    key_to_orbit[key] = orbit
                    keys.append(key)
                first.append(i)
                second.append(j)
                third.append(k)
                orbit_numbers.append(orbit)
    return (
        tuple(keys),
        np.frombuffer(first, dtype=np.uint8),
        np.frombuffer(second, dtype=np.uint8),
        np.frombuffer(third, dtype=np.uint8),
        np.frombuffer(orbit_numbers, dtype=np.uint16),
    )


def matching_lookup(n):
    words = np.asarray(tuple(itertools.product((0, 1), repeat=n)), dtype=np.int8)
    edges = tuple(itertools.combinations(range(n), 2))
    edge_number = {edge: number for number, edge in enumerate(edges)}
    matchings = tuple(perfect_matchings(range(n)))
    lookup = np.empty((len(matchings), n // 2, len(words)), dtype=np.int16)
    for mi, matching in enumerate(matchings):
        for ei, (u, v) in enumerate(matching):
            lookup[mi, ei] = (
                4 * edge_number[u, v] + 2 * words[:, u] + words[:, v]
            )
    return words, edges, matchings, lookup


def source_output(parameters, lookup, prime):
    values = parameters[lookup].astype(np.int64)
    terms = np.prod(values, axis=1) % prime
    return np.sum(terms, axis=0, dtype=np.int64) % prime


def cubic_features(tensor, first, second, third, orbit_numbers,
                   orbit_count, prime):
    products = tensor[first] * tensor[second]
    products %= prime
    products *= tensor[third]
    products %= prime
    # With prime 1009 every exact orbit sum is below 2^53, so bincount's
    # float accumulator remains integer-exact before reduction modulo p.
    sums = np.bincount(
        orbit_numbers, weights=products, minlength=orbit_count
    ).astype(np.int64)
    return (sums % prime).tolist()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=8)
    parser.add_argument("--prime", type=int, default=1009)
    parser.add_argument("--samples", type=int, default=1350)
    parser.add_argument("--checks", type=int, default=30)
    parser.add_argument("--seed", type=int, default=20260724)
    args = parser.parse_args()
    assert args.n <= 8, "uint8 word-index storage assumes n <= 8"
    assert args.prime ** 3 * 50000 < 2 ** 53

    keys, first, second, third, orbit_numbers = build_cubic_orbits(args.n)
    words, edges, matchings, lookup = matching_lookup(args.n)
    print(
        f"n={args.n} words={len(words)} matchings={len(matchings)} "
        f"cubic_monomials={len(first)} cubic_orbits={len(keys)}",
        flush=True,
    )

    rng = np.random.default_rng(args.seed)
    rows = []
    for sample in range(args.samples):
        parameters = rng.integers(
            0, args.prime, size=4 * len(edges), dtype=np.int64
        )
        tensor = source_output(parameters, lookup, args.prime)
        rows.append(cubic_features(
            tensor, first, second, third, orbit_numbers,
            len(keys), args.prime
        ))
        if (sample + 1) % 100 == 0:
            print(f"sample={sample + 1}", flush=True)

    matrix = nmod_mat(rows, args.prime)
    rank = matrix.rank()
    kernel, nullity = matrix.nullspace()
    print(f"rank={rank} nullity={nullity}", flush=True)

    for _ in range(args.checks):
        parameters = rng.integers(
            0, args.prime, size=4 * len(edges), dtype=np.int64
        )
        tensor = source_output(parameters, lookup, args.prime)
        row = cubic_features(
            tensor, first, second, third, orbit_numbers,
            len(keys), args.prime
        )
        for column in range(nullity):
            assert sum(row[i] * int(kernel[i, column])
                       for i in range(len(keys))) % args.prime == 0

    target = np.ones(len(words), dtype=np.int64)
    target[0] += 1
    target[-1] += 1
    target_row = cubic_features(
        target, first, second, third, orbit_numbers,
        len(keys), args.prime
    )
    separating = []
    for column in range(nullity):
        value = sum(target_row[i] * int(kernel[i, column])
                    for i in range(len(keys))) % args.prime
        if value:
            separating.append((column, value))
    print(f"fresh_checks={args.checks} separating={separating[:20]}")


if __name__ == "__main__":
    main()
