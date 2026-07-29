#!/usr/bin/env python3
"""Explore the first sole-plane high-t response at (r,t)=(3,6)."""

from __future__ import annotations

import argparse
from functools import lru_cache
from itertools import combinations, product
import random


PRIME = 1_000_003
HESSIAN = ((0, 1, 1), (1, 0, 1), (1, 1, 0))
IDENTITY = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
TYPE_10 = ((1, 0, 0), (0, 1, 0), (0, 0, 0))
VERTICES = tuple(range(9))
ACTIVE = (6, 7, 8)
COLUMNS = tuple((site, row) for site in ACTIVE for row in range(3))
COLUMN_INDEX = {column: index for index, column in enumerate(COLUMNS)}
SOURCE_PAIRS = ((0, 0), (0, 2), (1, 1), (1, 2), (2, 2))

PROFILES = {
    "222": (2, 2, 3, 3, 4, 4),
    "2211": (2, 2, 3, 3, 4, 5),
    "21111": (2, 2, 3, 4, 5, 6),
    "111111": (2, 3, 4, 5, 6, 7),
}


def chart(kind, a, b):
    if kind == "01":
        return ((1, 0, a), (0, 1, b), (0, 0, 0))
    if kind == "12":
        return ((a, 1, 0), (b, 0, 1), (0, 0, 0))
    if kind == "02":
        return ((1, a, 0), (0, b, 1), (0, 0, 0))
    raise ValueError(kind)


@lru_cache(maxsize=None)
def matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    return tuple(
        ((first, vertices[position]),) + tail
        for position in range(1, len(vertices))
        for tail in matchings(
            vertices[1:position] + vertices[position+1:]
        )
    )


def matrix_product(left, middle, right):
    return tuple(
        tuple(
            sum(
                left[i][a]*middle[a][b]*right[j][b]
                for a in range(3) for b in range(3)
            ) % PRIME
            for j in range(3)
        )
        for i in range(3)
    )


def row_engine(kind, values, live_betas):
    matrices = (
        (IDENTITY,)*6
        + (TYPE_10, TYPE_10, chart(kind, *values))
    )
    betas = tuple(live_betas)+(1, 1, 1)
    blocks = {}
    for left, right in combinations(VERTICES, 2):
        denominator = (betas[left]+betas[right]) % PRIME
        assert denominator
        scale = pow(denominator, PRIME-2, PRIME)
        numerator = matrix_product(
            matrices[left], HESSIAN, matrices[right]
        )
        blocks[left, right] = tuple(
            tuple(scale*entry % PRIME for entry in row)
            for row in numerator
        )

    def edge(word, left, right):
        if left < right:
            return blocks[left, right][word[left]][word[right]]
        return blocks[right, left][word[right]][word[left]]

    @lru_cache(maxsize=None)
    def hafnian(word, vertices):
        answer = 0
        for matching in matchings(vertices):
            term = 1
            for left, right in matching:
                term = term*edge(word, left, right) % PRIME
            answer = (answer+term) % PRIME
        return answer

    def row(label):
        word, source_left, source_right = label
        answer = [0]*len(COLUMNS)
        for marked_left, marked_right in combinations(VERTICES, 2):
            marked = (
                matrices[marked_left][word[marked_left]][source_left]
                * matrices[marked_right][word[marked_right]][source_right]
                + matrices[marked_left][word[marked_left]][source_right]
                * matrices[marked_right][word[marked_right]][source_left]
            ) % PRIME
            if not marked:
                continue
            for star in ACTIVE:
                if star in (marked_left, marked_right):
                    continue
                remaining = tuple(
                    site for site in VERTICES
                    if site not in (marked_left, marked_right, star)
                )
                answer[COLUMN_INDEX[star, word[star]]] = (
                    answer[COLUMN_INDEX[star, word[star]]]
                    + marked*hafnian(word, remaining)
                ) % PRIME
        return answer

    return row


def singleton_labels(kind, profile, values=(2, 3)):
    row = row_engine(kind, values, PROFILES[profile])
    labels = {}
    for word in product(range(3), repeat=9):
        for source_left, source_right in SOURCE_PAIRS:
            label = (word, source_left, source_right)
            vector = row(label)
            support = [
                index for index, value in enumerate(vector) if value
            ]
            if len(support) == 1 and support[0] not in labels:
                labels[support[0]] = (label, vector[support[0]])
                if len(labels) == len(COLUMNS):
                    return tuple(labels[index] for index in range(9))
    return tuple(labels[index] for index in sorted(labels))


def generic_basis(kind, profile, values=(2, 3), seed=17):
    row = row_engine(kind, values, PROFILES[profile])
    descriptors = [
        (word, source_left, source_right)
        for word in product(range(3), repeat=9)
        for source_left, source_right in SOURCE_PAIRS
    ]
    random.Random(seed).shuffle(descriptors)
    basis = {}
    selected = []
    for label in descriptors:
        original = row(label)
        reduced = original[:]
        while any(reduced):
            pivot = next(i for i, value in enumerate(reduced) if value)
            if pivot not in basis:
                inverse = pow(reduced[pivot], PRIME-2, PRIME)
                basis[pivot] = [
                    value*inverse % PRIME for value in reduced
                ]
                selected.append(
                    (
                        sum(bool(value) for value in original),
                        label,
                    )
                )
                break
            scale = reduced[pivot]
            reduced = [
                value-scale*basis_value
                for value, basis_value in zip(reduced, basis[pivot])
            ]
            reduced = [value % PRIME for value in reduced]
        if len(basis) == len(COLUMNS):
            break
    return tuple(selected)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=tuple(PROFILES), default="222")
    parser.add_argument("--chart", choices=("01", "12", "02"), default="01")
    parser.add_argument("--singletons", action="store_true")
    args = parser.parse_args()
    if args.singletons:
        labels = singleton_labels(args.chart, args.profile)
        print("singleton columns", len(labels), "/", len(COLUMNS))
        for item in labels:
            print(item)
    else:
        labels = generic_basis(args.chart, args.profile)
        print("rank", len(labels), "/", len(COLUMNS))
        for item in labels:
            print(item)


if __name__ == "__main__":
    main()
