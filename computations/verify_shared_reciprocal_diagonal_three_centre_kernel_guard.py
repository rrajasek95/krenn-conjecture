#!/usr/bin/env python3
"""Exact simplex normal form and a genuine diagonal three-centre guard.

For a fixed target line on three possible insertion sites, the kernel of
the sum of the three inserted tensor subspaces is the image of the usual
complete-simplex (Koszul) edge boundary.  Colour parity lets every kernel
row of a colour-diagonal quadratic split into these coordinate-line
complexes.

Exactness does *not* force a two-centre subbridge.  The checker constructs
a rational colour-diagonal quadratic on five sites for which the target
columns at sites 0,1,2 have the unique relation (1,-2,1), every pair of
full three-colour site blocks is independent, and the relation has a
nonzero three-edge triangular Koszul representative.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITES = tuple(range(5))
ACTIVE = (0, 1, 2)
OUTSIDE = (3, 4)
COLOURS = tuple(range(3))
D, _UNUSED, T = COLOURS
PINNED_PARITY_SHA256 = (
    "ddf3c9b1dce264de5e29315d350e15bef56e91b699daf9c90439222b104c7f85"
)
EXPECTED_DIGEST = "ee2d27cc2d98b722bb82356cfd45747db23be096d71095d9b70b9f41b6484fc3"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_dependency():
    dependency = ROOT / (
        "computations/"
        "verify_shared_reciprocal_two_bad_two_centre_parity_straightening.py"
    )
    require(sha256(dependency.read_bytes()).hexdigest()
            == PINNED_PARITY_SHA256,
            "the two-centre parity-straightening dependency changed")


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def sparse_rank(columns, prime=101):
    """Column rank over F_prime for sparse coordinate dictionaries."""
    pivots = {}
    for source in columns:
        vector = {key: value % prime for key, value in source.items()
                  if value % prime}
        while vector:
            pivot = min(vector, key=repr)
            if pivot not in pivots:
                inverse = pow(vector[pivot], -1, prime)
                vector = {key: value * inverse % prime
                          for key, value in vector.items() if value % prime}
                pivots[pivot] = vector
                break
            scalar = vector[pivot]
            row = pivots[pivot]
            for key, value in row.items():
                updated = (vector.get(key, 0) - scalar * value) % prime
                if updated:
                    vector[key] = updated
                else:
                    vector.pop(key, None)
    return len(pivots)


def c1_key(site, full_word):
    remaining = tuple(full_word[index] for index in SITES if index != site)
    return site, remaining


def c2_key(pair, full_word):
    remaining = tuple(full_word[index] for index in SITES
                      if index not in pair)
    return tuple(pair), remaining


def insert_word(missing, remaining_word, colour=T):
    iterator = iter(remaining_word)
    return tuple(colour if site == missing else next(iterator)
                 for site in SITES)


def insert_pair(pair, remaining_word, colour=T):
    iterator = iter(remaining_word)
    return tuple(colour if site in pair else next(iterator)
                 for site in SITES)


def d1_column(site, remaining_word):
    return {insert_word(site, remaining_word): 1}


def d2_column(pair, remaining_word):
    left, right = pair
    full_word = insert_pair(pair, remaining_word)
    return {
        c1_key(left, full_word): 1,
        c1_key(right, full_word): -1,
    }


def d3_column(outside_word):
    full_word = tuple(T if site in ACTIVE
                      else outside_word[OUTSIDE.index(site)]
                      for site in SITES)
    # Boundary of [0,1,2] is [1,2]-[0,2]+[0,1].
    return {
        c2_key((1, 2), full_word): 1,
        c2_key((0, 2), full_word): -1,
        c2_key((0, 1), full_word): 1,
    }


def apply_sparse_map(column, images):
    answer = Counter()
    for key, coefficient in column.items():
        for output, value in images[key].items():
            answer[output] += coefficient * value
            if answer[output] == 0:
                del answer[output]
    return dict(answer)


def audit_simplex_exactness():
    c1_labels = []
    c1_images = {}
    for site in ACTIVE:
        for word in product(COLOURS, repeat=4):
            label = (site, word)
            c1_labels.append(label)
            c1_images[label] = d1_column(site, word)

    c2_labels = []
    c2_images = {}
    for pair in combinations(ACTIVE, 2):
        for word in product(COLOURS, repeat=3):
            label = (pair, word)
            c2_labels.append(label)
            c2_images[label] = d2_column(pair, word)

    c3_labels = list(product(COLOURS, repeat=2))
    c3_images = {word: d3_column(word) for word in c3_labels}

    # Build d1*d2 and d2*d3 literally.
    for label in c2_labels:
        require(not apply_sparse_map(c2_images[label], c1_images),
                "the simplex d1*d2 boundary changed")
    for label in c3_labels:
        require(not apply_sparse_map(c3_images[label], c2_images),
                "the simplex d2*d3 boundary changed")

    rank_d1 = sparse_rank(list(c1_images.values()))
    rank_d2 = sparse_rank(list(c2_images.values()))
    rank_d3 = sparse_rank(list(c3_images.values()))
    require((len(c1_labels), len(c2_labels), len(c3_labels))
            == (243, 81, 9), "the simplex dimensions changed")
    require((rank_d1, rank_d2, rank_d3) == (171, 72, 9),
            "the simplex boundary ranks changed")
    require(len(c1_labels) - rank_d1 == rank_d2,
            "the single-site kernel stopped being the edge image")
    require(len(c2_labels) - rank_d2 == rank_d3,
            "the edge kernel stopped being the triangle image")
    return {
        "dimensions": [len(c1_labels), len(c2_labels), len(c3_labels)],
        "ranks": [rank_d1, rank_d2, rank_d3],
        "kernel_d1": len(c1_labels) - rank_d1,
        "kernel_d2": len(c2_labels) - rank_d2,
    }


def audit_parity_split():
    sectors = {}
    for inserted in COLOURS:
        parities = set()
        for word in product(COLOURS, repeat=4):
            counts = [word.count(colour) for colour in COLOURS]
            if not all(count % 2 == 0 for count in counts):
                continue
            counts[inserted] += 1
            parities.add(tuple(count % 2 for count in counts))
        expected = tuple(int(colour == inserted) for colour in COLOURS)
        require(parities == {expected},
                "a diagonal cofactor left its inserted-colour parity sector")
        sectors[inserted] = expected
    require(len(set(sectors.values())) == len(COLOURS),
            "two inserted colours entered the same parity sector")
    return sectors


def put(cells, left, right, colour, value):
    edge = tuple(sorted((left, right)))
    key = (edge, colour)
    cells[key] = cells.get(key, 0) + value
    if cells[key] == 0:
        del cells[key]


def matching_tensor(vertices, cells):
    vertices = tuple(vertices)
    answer = Counter()
    for matching in perfect_matchings(vertices):
        edge_options = []
        for edge in matching:
            edge = tuple(sorted(edge))
            options = [(colour, value)
                       for (candidate, colour), value in cells.items()
                       if candidate == edge and value]
            if not options:
                break
            edge_options.append(options)
        else:
            for choices in product(*edge_options):
                colouring = {}
                coefficient = 1
                for edge, (colour, value) in zip(matching, choices):
                    colouring[edge[0]] = colour
                    colouring[edge[1]] = colour
                    coefficient *= value
                word = tuple(colouring[site] for site in vertices)
                answer[word] += coefficient
    return {word: value for word, value in answer.items() if value}


def insert_tensor(cofactor, sites, missing, colour):
    answer = {}
    for word, coefficient in cofactor.items():
        partial = dict(zip(sites, word))
        partial[missing] = colour
        full_word = tuple(partial[site] for site in SITES)
        answer[full_word] = answer.get(full_word, 0) + coefficient
    return {word: value for word, value in answer.items() if value}


def exact_rank(vectors):
    basis = {}
    for source in vectors:
        vector = {key: Fraction(value) for key, value in source.items()
                  if value}
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                scale = vector[pivot]
                basis[pivot] = {key: value / scale
                                for key, value in vector.items()}
                break
            scale = vector[pivot]
            for key, value in basis[pivot].items():
                updated = vector.get(key, 0) - scale * value
                if updated:
                    vector[key] = updated
                else:
                    vector.pop(key, None)
    return len(basis)


def add_vectors(*terms):
    answer = Counter()
    for scalar, vector in terms:
        for key, value in vector.items():
            answer[key] += scalar * value
            if answer[key] == 0:
                del answer[key]
    return dict(answer)


def boundary_of_potential(potential):
    answer = Counter()
    for (pair, remaining_word), coefficient in potential.items():
        for key, value in d2_column(pair, remaining_word).items():
            answer[key] += coefficient * value
            if answer[key] == 0:
                del answer[key]
    return dict(answer)


def audit_three_centre_guard():
    cells = {}
    # One non-target chord.  It supplies the same second quotient character
    # to all three active cofactors.
    put(cells, 3, 4, D, 1)
    # Target triangle and four target ports.  The active cofactor vectors
    # become (h_x,s_x)=(1,1),(2,1),(3,1).
    for left, right, value in (
        (0, 1, 1), (0, 2, 1), (1, 2, 1),
        (1, 3, 1), (2, 4, 1), (0, 3, 2), (0, 4, 3),
    ):
        put(cells, left, right, T, value)

    cofactors = {}
    inserted = {}
    for site in SITES:
        remaining = tuple(index for index in SITES if index != site)
        cofactors[site] = matching_tensor(remaining, cells)
        inserted[site] = {
            colour: insert_tensor(cofactors[site], remaining, site, colour)
            for colour in COLOURS
        }

    full_target = (T,) * 5
    mixed = (T, T, T, D, D)
    target_columns = [inserted[site][T] for site in ACTIVE]
    require([{word: vector[word] for word in sorted(vector)}
             for vector in target_columns] == [
                 {mixed: 1, full_target: 1},
                 {mixed: 1, full_target: 2},
                 {mixed: 1, full_target: 3},
             ], "the rational triangular cofactor columns changed")

    relation = add_vectors((1, target_columns[0]),
                           (-2, target_columns[1]),
                           (1, target_columns[2]))
    require(not relation, "the displayed three-centre relation changed")
    require(exact_rank(target_columns) == 2,
            "the target three-centre circuit rank changed")
    require(all(exact_rank([target_columns[left], target_columns[right]]) == 2
                for left, right in combinations(range(3), 2)),
            "a target-axis two-centre subrelation appeared")

    # Stronger mutation guard: even allowing all three local colours, the
    # images of any two active site blocks are disjoint.  Thus this circuit
    # has no arbitrary-vector two-centre subbridge on a proper subset.
    pair_block_ranks = {}
    for left, right in combinations(ACTIVE, 2):
        vectors = ([inserted[left][colour] for colour in COLOURS]
                   + [inserted[right][colour] for colour in COLOURS])
        rank = exact_rank(vectors)
        require(rank == 6,
                "an arbitrary-vector two-centre subbridge appeared")
        pair_block_ranks[f"{left}{right}"] = rank

    # Each active cofactor has no word avoiding the target colour.  The
    # only two global target-sector words are the all-target word and the
    # word using the non-target outside chord.
    no_target = {}
    for site in ACTIVE:
        forbidden = [word for word in cofactors[site] if T not in word]
        require(not forbidden,
                "an active cofactor acquired a no-target four-word")
        no_target[site] = len(forbidden)

    # The two scalar provenance equations are exactly the all-target
    # hafnian row and the complementary non-target-chord row.
    scalar_rows = {
        "outside_non_target": [vector[mixed] for vector in target_columns],
        "all_target": [vector[full_target] for vector in target_columns],
    }
    require(scalar_rows == {
        "outside_non_target": [1, 1, 1],
        "all_target": [1, 2, 3],
    }, "the triangular scalar rows changed")
    require(sum(weight * value for weight, value in
                zip((1, -2, 1), scalar_rows["outside_non_target"])) == 0,
            "the non-target chord scalarization changed")
    require(sum(weight * value for weight, value in
                zip((1, -2, 1), scalar_rows["all_target"])) == 0,
            "the all-target scalarization changed")

    # Give the relation an explicit *three-edge* Koszul representative.
    # For each of its two full words, start with a tree flow and add one
    # triangle boundary so all three edge potentials remain nonzero.
    component_coefficients = {
        full_target: (1, -4, 3),
        mixed: (1, -2, 1),
    }
    potential = {}
    potential_summary = {}
    for full_word, coefficients in component_coefficients.items():
        g0, g1, g2 = coefficients
        require(g0 + g1 + g2 == 0,
                "a guard component stopped being a zero-sum circuit")
        flow = {
            (0, 1): -g1 + 1,
            (0, 2): -g2 - 1,
            (1, 2): 1,
        }
        require(all(flow.values()),
                "the displayed triangular potential lost an edge")
        for pair, value in flow.items():
            potential[(pair, c2_key(pair, full_word)[1])] = value
        potential_summary[str(full_word)] = {
            "component_coefficients": coefficients,
            "edge_flow": {f"{left}{right}": value
                          for (left, right), value in flow.items()},
        }

    relation_c1 = Counter()
    for site, (weight, vector) in enumerate(zip(
            (1, -2, 1), target_columns)):
        for full_word, value in vector.items():
            relation_c1[c1_key(site, full_word)] += weight * value
    relation_c1 = {key: value for key, value in relation_c1.items() if value}
    require(boundary_of_potential(potential) == relation_c1,
            "the explicit triangular Koszul representative changed")

    return {
        "cells": [
            {"edge": list(edge), "colour": colour, "value": value}
            for (edge, colour), value in sorted(cells.items())
        ],
        "active_target_columns": [
            {str(word): value for word, value in sorted(vector.items())}
            for vector in target_columns
        ],
        "relation": [1, -2, 1],
        "target_column_rank": exact_rank(target_columns),
        "target_pair_ranks": [
            exact_rank([target_columns[left], target_columns[right]])
            for left, right in combinations(range(3), 2)
        ],
        "full_site_pair_block_ranks": pair_block_ranks,
        "no_target_four_words": no_target,
        "scalar_rows": scalar_rows,
        "triangular_potential": potential_summary,
        "verdict": (
            "a genuine minimal three-centre target-axis kernel circuit exists "
            "with no arbitrary-vector two-centre subbridge"
        ),
    }


def main():
    pin_dependency()
    simplex = audit_simplex_exactness()
    parity = audit_parity_split()
    guard = audit_three_centre_guard()
    ledger = {
        "pinned_parity_sha256": PINNED_PARITY_SHA256,
        "simplex_exactness": simplex,
        "inserted_colour_parity_sectors": parity,
        "three_centre_guard": guard,
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"the diagonal three-centre guard ledger changed: {digest}")
    print("diagonal three-centre kernel guard: PASS")
    print("simplex dimensions/ranks: 243,81,9 / 171,72,9")
    print("guard target columns: rank 2 with relation (1,-2,1)")
    print("proper active site-pair block ranks: 6,6,6")
    print("nonzero triangular Koszul edge potentials: 6 / 6")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
