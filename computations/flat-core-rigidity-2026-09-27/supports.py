"""Exhaust the allowed rank-25 supports and construct every survivor."""

from collections import Counter
from itertools import combinations
from algebra import (E, ZERO, ONE, OMEGA, require, hafnian, matchings,
                     five_ground, four_outputs)


def check():
    counts = Counter()
    forbidden = {(0, 2), (0, 3), (1, 2), (1, 3)}
    allowed = [edge for edge in combinations(range(6), 2) if edge not in forbidden]
    require(len(allowed) == 11, "Eleven allowed edges")
    ground = {edge: z for edge, z in five_ground().items() if 4 not in edge}
    ground.update({(i, j): ONE for i in range(4) for j in (4, 5)})
    ground[4, 5] = E(-2)
    require(not hafnian(ground, range(6)), "Rank-25 fixture ground output")
    cofactors = {edge: hafnian(ground, tuple(v for v in range(6) if v not in edge))
                 for edge in combinations(range(6), 2)}
    require({edge for edge, value in cofactors.items() if value} == forbidden,
            "Exactly the four forbidden cofactor edges are nonzero")
    for K in combinations(range(6), 5):
        require(any(cofactors[edge] for edge in combinations(K, 2)),
                "Every five-site subset has a nonzero internal cofactor")

    for mask in range(1 << len(allowed)):
        support = {edge for j, edge in enumerate(allowed) if mask & (1 << j)}
        active_matchings = {
            quartet: [matching for matching in matchings(quartet)
                      if all(edge in support for edge in matching)]
            for quartet in combinations(range(6), 4)}
        if any(len(ms) == 1 for ms in active_matchings.values()):
            counts["unique_matching_excluded"] += 1
            continue
        doubles = [i for i in range(4) if (i, 4) in support and (i, 5) in support]
        if len(doubles) >= 3:
            counts["three_double_leaves_excluded"] += 1
            continue
        active = {v for edge in support for v in edge}
        if len(active) <= 4:
            counts["at_most_four_sites"] += 1
        else:
            require(any(all(center in edge for edge in support) for center in (4, 5)),
                    "Every larger survivor is a star at 4 or 5")
            counts["larger_star"] += 1

        weights = {edge: ONE for edge in support}
        for ms in active_matchings.values():
            if not ms:
                continue
            require(len(ms) in (2, 3) and len(active) <= 4, "Only one quartet needs cancellation")
            target = [ONE, -ONE] if len(ms) == 2 else [ONE, OMEGA, OMEGA*OMEGA]
            for matching, value in zip(ms, target):
                weights[matching[0]] = value
        source = {(*edge, 0, 0): value for edge, value in weights.items()}
        require(all(weights.values()), "Every requested support edge is retained")
        require(not four_outputs(source, 6, 1), "Scalar construction realizes the support")

    require(dict(counts) == dict(unique_matching_excluded=1922,
                                three_double_leaves_excluded=10,
                                at_most_four_sites=104, larger_star=12),
            "Exhaustive support census")
    # Formal monomials in the six independent symbols Ai,Aj,Ak,Bi,Bj,Bk.
    terms = Counter()
    for sign, left, pair in ((1, "Bk", ("Ai Bj", "Aj Bi")),
                             (1, "Bj", ("Ai Bk", "Ak Bi")),
                             (-1, "Bi", ("Aj Bk", "Ak Bj"))):
        for term in pair:
            terms[tuple(sorted([left, *term.split()]))] += sign
    terms = {monomial: coefficient for monomial, coefficient in terms.items() if coefficient}
    require(terms == {("Ai", "Bj", "Bk"): 2}, "Three-double-leaf polynomial identity")
    return dict(total_supports=2048, counts=dict(counts), realized_survivors=116,
                nonzero_cofactor_edges=[list(edge) for edge in sorted(forbidden)],
                polynomial_identity="Bk*r_ij + Bj*r_ik - Bi*r_jk = 2*Ai*Bj*Bk")
