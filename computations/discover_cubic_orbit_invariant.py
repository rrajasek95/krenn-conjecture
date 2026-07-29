#!/usr/bin/env python3
"""Search for a symmetric cubic output invariant separating GHZ_3 at n=6.

The relevant color multidegree contains products f(c0)f(c1)f(c2) for
which the three colors at every vertex are 0,1,2.  After symmetrizing over
vertices, output colors, and the three factors, these products have only a
small number of orbit sums.  Random exact evaluations over a prime field
discover linear relations among those sums.
"""

from __future__ import annotations

import argparse
import itertools
import random


N = 6
Q = 3


def compose(left, right):
    return tuple(left[right[index]] for index in range(Q))


PERMS = tuple(itertools.permutations(range(Q)))
PERM_INDEX = {permutation: index for index, permutation in enumerate(PERMS)}


def canonical_count(counts):
    images = []
    for left in PERMS:
        for right in PERMS:
            transformed = [0] * len(PERMS)
            for index, count in enumerate(counts):
                image = compose(left, compose(PERMS[index], right))
                transformed[PERM_INDEX[image]] += count
            images.append(tuple(transformed))
    return min(images)


def perfect_matchings(vertices=tuple(range(N))):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


MATCHINGS = tuple(perfect_matchings())
COLORINGS = tuple(itertools.product(range(Q), repeat=N))
COLORING_INDEX = {coloring: index for index, coloring in enumerate(COLORINGS)}


def orbit_data():
    keys = sorted(
        {
            canonical_count(counts)
            for counts in itertools.product(range(N + 1), repeat=len(PERMS))
            if sum(counts) == N
        }
    )
    key_index = {key: index for index, key in enumerate(keys)}
    terms = []
    for choices in itertools.product(range(len(PERMS)), repeat=N):
        counts = tuple(choices.count(index) for index in range(len(PERMS)))
        column = key_index[canonical_count(counts)]
        colorings = tuple(
            COLORING_INDEX[tuple(PERMS[choices[vertex]][factor] for vertex in range(N))]
            for factor in range(Q)
        )
        terms.append((column, colorings))
    constant_key = canonical_count((N, 0, 0, 0, 0, 0))
    return keys, key_index[constant_key], terms


def tensor_values(matrices, prime):
    answer = []
    for coloring in COLORINGS:
        total = 0
        for matching in MATCHINGS:
            value = 1
            for u, v in matching:
                value = value * matrices[u, v][coloring[u]][coloring[v]] % prime
            total += value
        answer.append(total % prime)
    return answer


def add_row_basis(basis, row, prime):
    row = [value % prime for value in row]
    for pivot in sorted(basis):
        if row[pivot]:
            factor = row[pivot]
            pivot_row = basis[pivot]
            row = [(x - factor * y) % prime for x, y in zip(row, pivot_row)]
    pivot = next((index for index, value in enumerate(row) if value), None)
    if pivot is None:
        return False
    inverse = pow(row[pivot], -1, prime)
    row = [value * inverse % prime for value in row]
    for old_pivot, old_row in list(basis.items()):
        if old_row[pivot]:
            factor = old_row[pivot]
            basis[old_pivot] = [
                (x - factor * y) % prime for x, y in zip(old_row, row)
            ]
    basis[pivot] = row
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=300)
    parser.add_argument("--prime", type=int, default=1000003)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    keys, constant_column, terms = orbit_data()
    print(
        f"orbits={len(keys)} tuple_terms={len(terms)} constant_column={constant_column}",
        flush=True,
    )
    basis = {}
    for sample in range(args.samples):
        matrices = {
            (u, v): tuple(
                tuple(rng.randrange(args.prime) for _ in range(Q)) for _ in range(Q)
            )
            for u, v in itertools.combinations(range(N), 2)
        }
        values = tensor_values(matrices, args.prime)
        features = [0] * len(keys)
        for column, indices in terms:
            product = values[indices[0]] * values[indices[1]] % args.prime
            product = product * values[indices[2]] % args.prime
            features[column] = (features[column] + product) % args.prime
        grew = add_row_basis(basis, features, args.prime)
        if sample < 10 or grew and sample % 10 == 0:
            print(f"sample={sample + 1} rank={len(basis)}", flush=True)
        if len(basis) == len(keys):
            break

    # The GHZ feature vector is nonzero only in the constant-tuple orbit.
    # It is separated by a relation iff that coordinate is not a pivot of
    # the sampled row space after reducing the unit vector.
    unit = [0] * len(keys)
    unit[constant_column] = 1
    residue = unit[:]
    for pivot in sorted(basis):
        if residue[pivot]:
            factor = residue[pivot]
            residue = [
                (x - factor * y) % args.prime for x, y in zip(residue, basis[pivot])
            ]
    print(
        f"final_rank={len(basis)}/{len(keys)} ghz_outside_sample_span={any(residue)} "
        f"residue={residue}",
        flush=True,
    )


if __name__ == "__main__":
    main()
