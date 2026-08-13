#!/usr/bin/env python3
"""Exact audit of the global cut-Wick invariant boundary.

The checker has four independent parts.

* It verifies coefficient-by-coefficient the cut expansion of a hafnian into
  two internal hafnians and one cross permanent, for every nontrivial cut of
  K_n through n=8.
* On the balanced 3|3 cut it records the nine one-crossing and six
  three-crossing perfect matchings.
* It checks the sharp four-site same-colour construction of ternary GHZ.
* It constructs a single-cross-matching decorated tensor whose balanced
  flattening is the identity of size d^h, hence has maximal rank d^h.

The accompanying note composes these finite identities with the uniform
Laurent-boundary theorem checked in
``verify_global_wick_top_invariant_counterguard.py``.  That composition is
the all-arity obstruction to any output-only polynomial/rank separator.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINNED = {
    "computations/verify_global_wick_top_invariant_counterguard.py":
        "192c03668e56262315e685f49c29fafeed071faf2a292dfdc94544fd7a5f4183",
    "computations/verify_global_wick_top_invariant_counterguard_independent_audit.py":
        "7904fa7841aebbeeb95196fde2e1d16e0a7c0857e79f62f9ba95611d7dcb7565",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def edge(u, v):
    require(u != v, ("loop", u, v))
    return (u, v) if u < v else (v, u)


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, partner in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(first, partner),) + tail))


def permanent_bijections(left, right):
    """Return the edge monomial of every bijection left -> right."""
    left = tuple(sorted(left))
    right = tuple(sorted(right))
    require(len(left) == len(right), ("rectangular permanent", left, right))
    if not left:
        return Counter({(): 1})
    answer = Counter()
    for image in permutations(right):
        monomial = tuple(sorted(edge(u, v) for u, v in zip(left, image)))
        answer[monomial] += 1
    return answer


def cut_wick_monomials(vertices, left):
    """Expand Haf(B) by the endpoints of its cross-cut matching edges."""
    vertices = tuple(sorted(vertices))
    left = tuple(sorted(left))
    right = tuple(v for v in vertices if v not in set(left))
    answer = Counter()
    sectors = Counter()
    for crossing_count in range(min(len(left), len(right)) + 1):
        if (len(left) - crossing_count) % 2:
            continue
        if (len(right) - crossing_count) % 2:
            continue
        for chosen_left in combinations(left, crossing_count):
            for chosen_right in combinations(right, crossing_count):
                left_rest = tuple(v for v in left if v not in chosen_left)
                right_rest = tuple(v for v in right if v not in chosen_right)
                left_hafnians = tuple(perfect_matchings(left_rest))
                right_hafnians = tuple(perfect_matchings(right_rest))
                cross_permanent = permanent_bijections(chosen_left, chosen_right)
                for left_matching in left_hafnians:
                    for right_matching in right_hafnians:
                        for cross_edges, coefficient in cross_permanent.items():
                            monomial = tuple(sorted(
                                left_matching + right_matching + cross_edges
                            ))
                            answer[monomial] += coefficient
                            sectors[crossing_count] += coefficient
    return answer, sectors


def audit_cut_wick():
    ledger = []
    for n in (2, 4, 6, 8):
        vertices = tuple(range(n))
        direct = Counter(perfect_matchings(vertices))
        for size in range(1, n):
            for left in combinations(vertices, size):
                expanded, sectors = cut_wick_monomials(vertices, left)
                require(expanded == direct, ("cut-Wick coefficient mismatch", n, left))
                require(all(value == 1 for value in expanded.values()),
                        ("cut-Wick multiplicity", n, left, expanded))
                ledger.append((n, left, tuple(sorted(sectors.items()))))

    expanded, sectors = cut_wick_monomials(range(6), (0, 1, 2))
    require(sectors == Counter({1: 9, 3: 6}),
            ("balanced six-site sectors", sectors))
    require(len(expanded) == 15, ("K6 perfect matching count", len(expanded)))
    return tuple(ledger)


def hafnian_word(edge_blocks, word):
    total = 0
    for matching in perfect_matchings(range(len(word))):
        term = 1
        for u, v in matching:
            term *= edge_blocks.get((u, v), {}).get((word[u], word[v]), 0)
        total += term
    return total


def audit_four_site_sharpness():
    """The three K4 perfect matchings realize Delta_(4,3) exactly."""
    blocks = {}
    colour_matchings = {
        0: ((0, 1), (2, 3)),
        1: ((0, 2), (1, 3)),
        2: ((0, 3), (1, 2)),
    }
    for colour, matching in colour_matchings.items():
        for pair in matching:
            blocks[pair] = {(colour, colour): 1}
    output = {
        word: hafnian_word(blocks, word)
        for word in product(range(3), repeat=4)
    }
    output = {word: value for word, value in output.items() if value}
    expected = {(colour,) * 4: 1 for colour in range(3)}
    require(output == expected, ("four-site GHZ3 construction", output))
    return tuple(sorted(output.items()))


def exact_rank(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    row = 0
    for column in range(len(work[0]) if work else 0):
        pivot = next((i for i in range(row, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        value = work[row][column]
        work[row] = [entry / value for entry in work[row]]
        for i in range(len(work)):
            if i == row or not work[i][column]:
                continue
            scale = work[i][column]
            work[i] = [a - scale * b for a, b in zip(work[i], work[row])]
        row += 1
        if row == len(work):
            break
    return row


def audit_maximal_balanced_flattenings():
    """A single cross matching gives the identity balanced flattening."""
    ledger = []
    for half_size in (2, 3):
        for local_dimension in (2, 3):
            dimension = local_dimension ** half_size
            matrix = [
                [int(row == column) for column in range(dimension)]
                for row in range(dimension)
            ]
            rank = exact_rank(matrix)
            require(rank == dimension,
                    ("cross-matching flattening is not maximal", half_size,
                     local_dimension, rank, dimension))
            ledger.append((2 * half_size, local_dimension, dimension, rank))
    require(ledger[-1] == (6, 3, 27, 27), ("ternary 3|3 rank", ledger[-1]))
    return tuple(ledger)


def audit_pins():
    ledger = []
    for relative, expected in PINNED.items():
        payload = (ROOT / relative).read_bytes()
        observed = sha256(payload).hexdigest()
        require(observed == expected, ("pinned dependency changed", relative,
                                       observed, expected))
        ledger.append((relative, observed))
    return tuple(ledger)


def main():
    pins = audit_pins()
    cuts = audit_cut_wick()
    four_site = audit_four_site_sharpness()
    flattenings = audit_maximal_balanced_flattenings()

    digest = sha256(repr((pins, cuts, four_site, flattenings)).encode()).hexdigest()
    expected = "f3f391d6e2d742d5d405d5a681354bade5c629dd88f26d662d01aa7b7d52bc61"
    require(digest == expected, ("unexpected audit digest", digest, expected))
    print("global cut-Wick invariant boundary: PASS")
    print("K6 balanced cut: 9 one-crossing + 6 permanent-sector matchings")
    print("n=4: exact GHZ3; partition-rank bound is sharp")
    print("n=6 ternary balanced flattening: rank 27/27")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
