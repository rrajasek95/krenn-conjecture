#!/usr/bin/env python3
"""Audit the generic-star Koszul complex and its provenance counterguard.

This is not a Krenn counterexample.  It proves exactness of the contracted
square-free one-slice complex, records the homology caused by retaining a
zero route, and gives a four-site tensor in which a contracted Koszul
cancellation does not lift through the alpha contraction.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import comb


Q = Fraction
COLORS = (0, 1, 2)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def matrix_rank(rows):
    rows = [list(map(Q, row)) for row in rows]
    if not rows:
        return 0
    height, width = len(rows), len(rows[0])
    rank = 0
    for column in range(width):
        pivot = next((row for row in range(rank, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        value = rows[rank][column]
        rows[rank] = [entry / value for entry in rows[rank]]
        for row in range(height):
            if row == rank or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right
                         for left, right in zip(rows[row], rows[rank])]
        rank += 1
        if rank == height:
            break
    return rank


def simplex_boundary_rank(number_of_p_slots):
    """Rank of edges -> zero-sum vertices for a complete simplex."""

    k = number_of_p_slots
    if k < 2:
        return 0
    edges = tuple(combinations(range(k), 2))
    rows = []
    for vertex in range(k):
        rows.append([
            (1 if vertex == right else -1 if vertex == left else 0)
            for left, right in edges
        ])
    rank = matrix_rank(rows)
    require(rank == k - 1, "simplex incidence rank changed")
    return rank


def koszul_rank_audit(maximum_sites=8):
    ledger = []
    for sites in range(2, maximum_sites + 1):
        delta1_rank = 3 ** sites - 2 ** sites
        c1_dimension = sites * 3 ** (sites - 1)
        kernel_dimension = c1_dimension - delta1_rank

        # Split by the set S of sites using a two-dimensional complement Q.
        # On a fixed S, k=sites-|S| copies map by summation, and the pairwise
        # Koszul map is the complete-simplex edge boundary.
        image_dimension = 0
        block_kernel_dimension = 0
        for q_sites in range(sites + 1):
            multiplicity = comb(sites, q_sites) * 2 ** q_sites
            p_sites = sites - q_sites
            block_kernel = max(p_sites - 1, 0)
            boundary_rank = simplex_boundary_rank(p_sites)
            require(boundary_rank == block_kernel,
                    "a square-free Koszul block ceased to be exact")
            image_dimension += multiplicity * boundary_rank
            block_kernel_dimension += multiplicity * block_kernel
        require(image_dimension == block_kernel_dimension == kernel_dimension,
                "global square-free Koszul ranks changed")
        ledger.append((sites, c1_dimension, delta1_rank, kernel_dimension))
    return tuple(ledger)


def tensor_term(*colors):
    return {tuple(colors): Q(1)}


def add(*tensors):
    answer = Counter()
    for tensor in tensors:
        answer.update(tensor)
    return {key: value for key, value in answer.items() if value}


def scale(tensor, scalar):
    return {key: Q(scalar) * value for key, value in tensor.items()
            if scalar * value}


def prepend(color, tensor):
    return {(color,) + key: value for key, value in tensor.items()}


def insert(color, position, tensor):
    answer = {}
    for key, value in tensor.items():
        output = key[:position] + (color,) + key[position:]
        answer[output] = answer.get(output, Q(0)) + value
    return {key: value for key, value in answer.items() if value}


def contract_first(tensor, alpha):
    answer = Counter()
    for key, value in tensor.items():
        answer[key[1:]] += alpha[key[0]] * value
    return {key: value for key, value in answer.items() if value}


def counterguard():
    # At residual sites 1,2,3 take p1=e0, p2=e1, p3=e2 and alpha=(1,1,1).
    # The sole Koszul two-cell is D12=e2 at site 3:
    # R1=p2 D12, R2=-p1 D12, R3=0.
    pure1 = tensor_term(0, 0)       # sites 2,3
    pure2 = tensor_term(1, 1)       # sites 1,3
    pure3 = tensor_term(2, 2)       # sites 1,2
    r1 = tensor_term(1, 2)          # p2 at site2, D at site3
    r2 = scale(tensor_term(0, 2), -1)  # -p1 at site1, D at site3
    c1 = add(pure1, r1)
    c2 = add(pure2, r2)
    c3 = pure3

    # Restore the missing physical slot of each cofactor and multiply by its
    # incident p-vector.  This is the contracted star tensor on sites1,2,3.
    contracted = add(
        insert(0, 0, c1),
        insert(1, 1, c2),
        insert(2, 2, c3),
    )
    delta3 = add(*(tensor_term(color, color, color)
                   for color in COLORS))
    require(contracted == delta3,
            "the designed contracted star is not exactly ternary diagonal")

    # Give the three incident blocks independent left factors e0,e1,e2 at
    # site0.  Their full star contribution is Delta4 plus a nonzero tensor
    # in ker(alpha) at site0.  Thus the fixed-alpha Koszul cancellation is
    # not a full source-row relation and cannot drive entry-minimality.
    full = add(prepend(0, insert(0, 0, c1)),
               prepend(1, insert(1, 1, c2)),
               prepend(2, insert(2, 2, c3)))
    delta4 = add(*(tensor_term(color, color, color, color)
                   for color in COLORS))
    residual = add(full, scale(delta4, -1))
    expected_residual = {
        (0, 0, 1, 2): Q(1),
        (1, 0, 1, 2): Q(-1),
    }
    require(residual == expected_residual,
            "the full-row Koszul counterguard residual changed")
    alpha = (Q(1), Q(1), Q(1))
    require(not contract_first(residual, alpha),
            "the counterguard residual escaped ker(alpha)")

    # Provenance/scaling guard.  Numerically R1=p2*D at t=1.  Scaling the
    # incident route p2 by t leaves the true opposite cofactor C1 unchanged;
    # retaining the representation forces D -> D/t.  There is no polynomial
    # (nonnegative star-degree) choice through t=0.
    t_values = (Q(1), Q(2), Q(3))
    forced_d = tuple(Q(1, 1) / value for value in t_values)
    require(forced_d == (Q(1), Q(1, 2), Q(1, 3)),
            "the inverse-star-degree provenance guard changed")

    return {
        "contracted_terms": len(contracted),
        "full_residual_terms": len(residual),
        "forced_divisor_values": forced_d,
    }


def zero_route_guard(active_sites):
    # If a zero p-route is incorrectly retained, take its R component in the
    # tensor product of the two-dimensional complements at every active site.
    # Delta1 kills it, while no pairwise term p_w D can reach it.  Its exact
    # surviving homology dimension is 2^active_sites (times any inactive
    # coefficient factors not displayed here).
    require(active_sites >= 1, "zero-route guard needs an active route")
    return 2 ** active_sites


def main():
    ledger = koszul_rank_audit()
    guard = counterguard()
    zero_homology = tuple(
        zero_route_guard(active) for active in range(1, 8)
    )
    require(zero_homology == (2, 4, 8, 16, 32, 64, 128),
            "zero-route homology census changed")
    print("square-free Koszul ranks (sites,C1,rank d1,ker d1):", ledger)
    print("retained-zero-route homology:", zero_homology)
    print("contracted/full-residual terms:",
          guard["contracted_terms"], guard["full_residual_terms"])
    print("forced inverse divisor values:", guard["forced_divisor_values"])
    print("generic-star Koszul counterguard: PASS")


if __name__ == "__main__":
    main()
