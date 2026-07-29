#!/usr/bin/env python3
"""Finite-field discovery search for the full five-hole shared response.

This is an exploratory script, not a proof certificate.  It searches small
exact integer star-row pairs satisfying prescribed witness masks and every
active triple/nontriple row-lock equation.  At a fixed incidence point it
then asks over a large prime field whether the full ternary diagonal lies in
the actual shared residual family

    sum_{u<v} R_uv * sum_w d_w * A_ab,

where {a,b} is the complement of {u,v,w}.  The internal A_ab matrices are
linear unknowns and the five d_w vectors are sampled.
"""

from __future__ import annotations

from itertools import combinations, product
import random
import sys

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import verify_n8_witness_union_five_stages as stages


PRIME = 1_000_003
COLORS = tuple(range(3))
SMALL_VECTORS = tuple(product((-1, 0, 1), repeat=3))
NONZERO_SMALL_VECTORS = tuple(v for v in SMALL_VECTORS if any(v))
TRIPLE_KINDS = ("P", "Q", "B+", "B-")


def cross(x, y):
    return (
        x[1] * y[2] - x[2] * y[1],
        x[2] * y[0] - x[0] * y[2],
        x[0] * y[1] - x[1] * y[0],
    )


def witness_mask(x, y):
    return sum(1 << color for color, value in enumerate(cross(x, y)) if value == 0)


PAIR_LIBRARY = {
    mask: tuple(
        (x, y)
        for x in SMALL_VECTORS
        for y in SMALL_VECTORS
        if witness_mask(x, y) == mask
    )
    for mask in range(1, 7)
}


def rank_mod(matrix):
    """Row rank of a modest dense integer array modulo PRIME."""

    a = np.asarray(matrix, dtype=np.int64).copy() % PRIME
    rows, columns = a.shape
    rank = 0
    for column in range(columns):
        candidates = np.flatnonzero(a[rank:, column])
        if not len(candidates):
            continue
        pivot = rank + int(candidates[0])
        if pivot != rank:
            a[[rank, pivot]] = a[[pivot, rank]]
        a[rank] = a[rank] * pow(int(a[rank, column]), PRIME - 2, PRIME) % PRIME
        active = np.flatnonzero(a[:, column])
        active = active[active != rank]
        if len(active):
            factors = a[active, column].copy()
            # Products are below 10^12 and therefore safe in int64.
            a[active] = (a[active] - factors[:, None] * a[rank]) % PRIME
        rank += 1
        if rank == rows:
            break
    return rank


WORDS = tuple(product(COLORS, repeat=5))
WORD_INDEX = {word: index for index, word in enumerate(WORDS)}
TARGET = np.asarray(
    [1 if len(set(word)) == 1 else 0 for word in WORDS], dtype=np.int64
)


def pair_response(xu, yu, xv, yv):
    return tuple(
        tuple((xu[i] * yv[j] + yu[i] * xv[j]) % PRIME for j in COLORS)
        for i in COLORS
    )


def shared_columns(star_rows, d_vectors):
    """The 90 columns indexed by an internal edge cell A_ab[i,j]."""

    columns = []
    for a, b in combinations(range(5), 2):
        complement = tuple(site for site in range(5) if site not in (a, b))
        for i in COLORS:
            for j in COLORS:
                column = np.zeros(len(WORDS), dtype=np.int64)
                for u, v in combinations(complement, 2):
                    w = next(site for site in complement if site not in (u, v))
                    xu, yu = star_rows[u]
                    xv, yv = star_rows[v]
                    response = pair_response(xu, yu, xv, yv)
                    for color_u in COLORS:
                        for color_v in COLORS:
                            coefficient = response[color_u][color_v]
                            if not coefficient:
                                continue
                            for color_w in COLORS:
                                value = coefficient * d_vectors[w][color_w]
                                if not value:
                                    continue
                                word = [0] * 5
                                word[u] = color_u
                                word[v] = color_v
                                word[w] = color_w
                                word[a] = i
                                word[b] = j
                                column[WORD_INDEX[tuple(word)]] += value
                columns.append(column % PRIME)
    return np.column_stack(columns)


def target_in_columns(columns):
    rank = rank_mod(columns)
    augmented = np.column_stack((columns, TARGET))
    return rank, rank_mod(augmented) == rank


def triple_parameters(kind):
    if kind == "P":
        return 1, 0
    if kind == "Q":
        return 0, 1
    if kind == "B+":
        return 1, 1
    if kind == "B-":
        return 1, -1
    raise AssertionError(kind)


def star_candidates(masks, hard, type_choice, rng):
    """Yield sampled exact small star rows obeying every scalar row lock."""

    witness_sites = tuple(site for site, mask in enumerate(masks) if mask)
    local_index = {site: index for index, site in enumerate(witness_sites)}
    triple_sites = tuple(site for site in witness_sites if masks[site] == 7)
    kinds = dict(zip(triple_sites, type_choice, strict=True))
    parameters = {site: triple_parameters(kinds[site]) for site in triple_sites}
    rows = {}
    for site in triple_sites:
        color = hard[site].bit_length() - 1
        p_scalar, q_scalar = parameters[site]
        x = [0, 0, 0]
        y = [0, 0, 0]
        x[color] = p_scalar
        y[color] = q_scalar
        rows[local_index[site]] = tuple(x), tuple(y)

    active_pairs = stages.active_triple_nontriple_pairs(masks, hard)
    libraries = {}
    for site in witness_sites:
        mask = masks[site]
        if mask == 7:
            continue
        constraints = tuple(
            (color, parameters[triple_site])
            for color, triple_site, nontriple_site in active_pairs
            if nontriple_site == site
        )
        library = tuple(
            (x, y)
            for x, y in PAIR_LIBRARY[mask]
            if all(
                all(
                    (p_scalar * y[s] + q_scalar * x[s]) == 0
                    for s in COLORS
                    if s != color
                )
                for color, (p_scalar, q_scalar) in constraints
            )
        )
        if not library:
            return
        libraries[local_index[site]] = library

    # A bounded random sample is enough for discovery.  The first element
    # makes every run deterministic even when a library is small.
    for attempt in range(12):
        candidate = dict(rows)
        for site, library in libraries.items():
            candidate[site] = library[0] if attempt == 0 else rng.choice(library)
        yield tuple(candidate[site] for site in range(5))


def search_assignment(masks, hard, rng):
    triple_sites = tuple(site for site, mask in enumerate(masks) if mask == 7)
    for type_choice in product(TRIPLE_KINDS, repeat=len(triple_sites)):
        for star_rows in star_candidates(masks, hard, type_choice, rng):
            for _ in range(24):
                d_vectors = tuple(rng.choice(NONZERO_SMALL_VECTORS) for _ in range(5))
                columns = shared_columns(star_rows, d_vectors)
                rank, contains = target_in_columns(columns)
                if contains:
                    return {
                        "triple_types": type_choice,
                        "star_rows": star_rows,
                        "d_vectors": d_vectors,
                        "rank_mod_p": rank,
                    }
    return None


def main():
    rng = random.Random(20260724)
    for masks in stages.EXPECTED_RESIDUAL:
        remaining = tuple(
            hard for hard in stages.hard_assignments(masks)
            if not stages.rank_two_certificate(masks, hard)
            and not stages.free_plane_monomial_certificate(masks, hard)
        )
        witness = search_assignment(masks, remaining[0], rng)
        print(masks, "shared-response witness:", bool(witness), flush=True)
        if witness:
            print(witness, flush=True)


if __name__ == "__main__":
    main()
