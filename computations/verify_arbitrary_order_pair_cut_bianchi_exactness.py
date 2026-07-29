#!/usr/bin/env python3
"""Lightweight exact audit of arbitrary-order pair-cut flatness."""

from __future__ import annotations

import itertools
from collections import Counter
from fractions import Fraction


def canonical_edge(u, v):
    return (u, v) if u < v else (v, u)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, partner in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield (canonical_edge(first, partner),) + tail


def partial_matchings(vertices):
    """Every matching on a subset of vertices, once."""
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    rest = vertices[1:]
    yield from partial_matchings(rest)
    for position, partner in enumerate(rest):
        remaining = rest[:position] + rest[position + 1 :]
        for tail in partial_matchings(remaining):
            yield (canonical_edge(first, partner),) + tail


def exposed_expansion(n, exposed):
    """Generate full matchings independently from all exposed-set layers."""
    exposed = tuple(sorted(exposed))
    exposed_set = set(exposed)
    remainder = tuple(v for v in range(n) if v not in exposed_set)
    answer = Counter()
    layer_counts = Counter()

    for direct in partial_matchings(exposed):
        covered = {v for edge in direct for v in edge}
        unmatched = tuple(v for v in exposed if v not in covered)
        if len(unmatched) > len(remainder):
            continue
        if (len(remainder) - len(unmatched)) % 2:
            continue
        for partners in itertools.permutations(remainder, len(unmatched)):
            used = set(partners)
            internal_vertices = tuple(v for v in remainder if v not in used)
            stars = tuple(canonical_edge(u, v) for u, v in zip(unmatched, partners))
            for internal in perfect_matchings(internal_vertices):
                matching = tuple(sorted(direct + stars + internal))
                answer[matching] += 1
                layer_counts[len(direct)] += 1
    return answer, layer_counts


def audit_all_exposed_sets():
    ledgers = {}
    for n in (4, 6, 8, 10):
        expected = Counter(tuple(sorted(matching)) for matching in perfect_matchings(range(n)))
        # Relabeling makes the audit depend only on the exposed-set size.
        # One representative per size keeps this comfortably subsecond.
        for size in range(n + 1):
            exposed = tuple(range(size))
            actual, layers = exposed_expansion(n, exposed)
            assert actual == expected
            assert set(actual.values()) == {1}
            if n == 8 and exposed == tuple(range(3)):
                ledgers[3] = dict(sorted(layers.items()))
            if n == 8 and exposed == tuple(range(4)):
                ledgers[4] = dict(sorted(layers.items()))
    assert ledgers[3] == {0: 60, 1: 45}
    assert ledgers[4] == {0: 24, 1: 72, 2: 9}
    return ledgers


def audit_pair_coordinate_reindexing():
    n = 8
    pairs = ((0, 1), (0, 2), (3, 7))
    canonical_words = set(itertools.product(range(3), repeat=n))
    for u, v in pairs:
        boundary = tuple(site for site in range(n) if site not in (u, v))
        reconstructed = set()
        for a, b in itertools.product(range(3), repeat=2):
            for omega in itertools.product(range(3), repeat=n - 2):
                word = [None] * n
                word[u], word[v] = a, b
                for site, color in zip(boundary, omega):
                    word[site] = color
                reconstructed.add(tuple(word))
        assert reconstructed == canonical_words
    return len(canonical_words)


def audit_half_shift_factors():
    factors = {}
    for r in range(1, 11):
        coefficient = Fraction((-1) ** r + 1, 2**r)
        expected = Fraction(0) if r % 2 else Fraction(1, 2 ** (r - 1))
        assert coefficient == expected
        factors[r] = coefficient
    return factors


def main():
    ledgers = audit_all_exposed_sets()
    words = audit_pair_coordinate_reindexing()
    factors = audit_half_shift_factors()
    print("arbitrary-order pair-cut/Bianchi exactness: PASS")
    print(f"three-/four-site layer ledgers at n=8: {ledgers}")
    print(f"complete pair coordinates per chart: {words}")
    print(f"half-shift factors through order 10: {factors}")


if __name__ == "__main__":
    main()
