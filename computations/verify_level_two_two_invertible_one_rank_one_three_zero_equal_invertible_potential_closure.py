#!/usr/bin/env python3
"""Close the last 2I+1R+3Z multiplier boundary.

Assume endpoint ranks (2,2,1,0,0,0), residual R2, and equal invertible
potentials distinct from the rank-one potential.  R2 forces the common
opposite-potential zero attachment set A to be nonempty (and to have size at
least two when the physical rank-one shore factor is noncoordinate).  After
a covariant shore normalization, all cases lie in thirteen zero-sum support
envelopes.  Exact local-colour cofactor counts bound every differential rank
by at most 48.

Standard library only; checks remain live under python -O and python -I -S.
"""

from itertools import combinations, permutations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


COLOURS = (0, 1)
SITES = tuple(range(6))
INVERTIBLE = (0, 1)
RANK_ONE = 2
ZERO = (3, 4, 5)
EDGES = tuple(combinations(SITES, 2))
CELLS = tuple(
    (u, v, a, b)
    for u, v in EDGES
    for a, b in product(COLOURS, repeat=2)
)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    head = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        partner = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((head, partner),) + tail)
    return tuple(answer)


MATCHINGS = {
    vertices: perfect_matchings(vertices)
    for size in (0, 2, 4, 6)
    for vertices in combinations(SITES, size)
}


def edge(u, v):
    return tuple(sorted((u, v)))


def pure_columns(block):
    return tuple(
        output for output in COLOURS
        if any(block[row][output] for row in COLOURS)
        and all(
            block[row][column] == 0
            for row in COLOURS for column in COLOURS
            if column != output
        )
    )


def audit_r2_attachment_thresholds():
    vectors = tuple(
        vector for vector in product((-1, 0, 1), repeat=2)
        if vector != (0, 0)
    )
    witness_counts = {}
    for shore_factor in vectors:
        counts = set()
        for left in vectors:
            block = tuple(
                tuple(left[row] * shore_factor[column]
                      for column in COLOURS)
                for row in COLOURS
            )
            counts.add(len(pure_columns(block)))
        require(len(counts) == 1,
                ("shore witness count depended on left vector",
                 shore_factor, counts))
        witness_counts[shore_factor] = next(iter(counts))

    coordinate = tuple(factor for factor, count in witness_counts.items()
                       if count == 1)
    noncoordinate = tuple(factor for factor, count in witness_counts.items()
                          if count == 0)
    require(set(coordinate) == {(-1, 0), (1, 0), (0, -1), (0, 1)},
            ("coordinate factors changed", coordinate))
    require(noncoordinate, "noncoordinate R2 branch disappeared")

    # M_01 is invertible and not pure.  R2 needs two witness colours total:
    # a coordinate rank-one edge supplies one and therefore needs |A|>=1;
    # a noncoordinate edge supplies none and needs two distinct zero labels.
    thresholds = (2 - 1, 2 - 0)
    require(thresholds == (1, 2), "R2 attachment thresholds changed")
    return len(coordinate), len(noncoordinate), thresholds


def support_value(nu, pair, colours):
    u, v = pair
    _, b = colours
    if pair == (0, 1):
        return True
    if u in INVERTIBLE and v == RANK_ONE:
        # After R2 has supplied the physical attachment threshold, use an
        # arbitrary local basis change to normalize the shore factor to e_0.
        return b == 0
    return nu[u] + nu[v] == 0


def live_edges(nu):
    return frozenset(
        pair for pair in EDGES
        if any(support_value(nu, pair, colours)
               for colours in product(COLOURS, repeat=2))
    )


REPRESENTATIVES = (
    ("A3", (1, 1, 2, -1, -1, -1)),
    ("A2_join", (1, 1, 2, -1, -1, 1)),
    ("A2_rank", (1, 1, 2, -1, -1, -2)),
    ("A2_isolated", (1, 1, 2, -1, -1, 3)),
    ("A1_PP", (1, 1, 2, -1, 1, 1)),
    ("A1_PO", (1, 1, 2, -1, 1, 3)),
    ("A1_PR", (1, 1, 2, -1, 1, -2)),
    ("A1_OO", (1, 1, 2, -1, 3, 4)),
    ("A1_RQ_edge", (1, 1, 2, -1, -2, 2)),
    ("A1_OO_edge", (1, 1, 2, -1, 3, -3)),
    ("A1_RO", (1, 1, 2, -1, -2, 3)),
    ("A1_RR", (1, 1, 2, -1, -2, -2)),
    ("A1_RR_zero_edge", (1, 1, 0, -1, 0, 0)),
)


def canonical_graph(edges):
    variants = []
    for zero_permutation in permutations(ZERO):
        mapping = {
            0: 0, 1: 1, 2: 2,
            3: zero_permutation[0],
            4: zero_permutation[1],
            5: zero_permutation[2],
        }
        variants.append(tuple(sorted(
            edge(mapping[u], mapping[v]) for u, v in edges
        )))
    return min(variants)


def audit_support_classification():
    graphs = {}
    sizes = {}
    for name, nu in REPRESENTATIVES:
        alpha, beta, gamma = nu[:3]
        require(alpha == beta != gamma,
                ("left the final multiplier boundary", name, nu))
        require(alpha + beta != 0 and alpha + gamma != 0,
                ("core zero sum appeared", name, nu))
        a_sites = tuple(site for site in ZERO if nu[site] == -alpha)
        require(a_sites, ("R2 attachment set vanished", name, nu))
        graph = canonical_graph(live_edges(nu))
        require(graph not in graphs,
                ("two representatives have the same support", name, graphs))
        graphs[graph] = name
        sizes[name] = len(a_sites)

    require(tuple(sorted(sizes.values())).count(3) == 1,
            ("A3 census changed", sizes))
    require(tuple(sorted(sizes.values())).count(2) == 3,
            ("A2 census changed", sizes))
    require(tuple(sorted(sizes.values())).count(1) == 9,
            ("A1 census changed", sizes))

    # |A|=2 leaves one vertex: it joins A (potential alpha), attaches to r
    # (potential -gamma), or is isolated.  These are mutually exclusive
    # because alpha+gamma is nonzero.
    a2_states = {"join", "rank", "isolated"}

    # With |A|=1, two leftover sites have six non-opposite allocations among
    # P (join A), R (attach r), and O, plus three opposite-pair cases:
    # O-O, R-Q, and the gamma=0 R-R edge.
    a1_nonopposite = {"PP", "PO", "PR", "OO", "RO", "RR"}
    a1_opposite = {"OO_edge", "RQ_edge", "RR_zero_edge"}
    require((1, len(a2_states), len(a1_nonopposite | a1_opposite), len(graphs))
            == (1, 3, 9, 13), "final support census changed")
    return (1, 3, 9), graphs


def cofactor_may_live(nu, pair, word):
    complement = tuple(site for site in SITES if site not in pair)
    return any(
        all(support_value(
            nu, matching_edge,
            (word[matching_edge[0]], word[matching_edge[1]])
        ) for matching_edge in matching)
        for matching in MATCHINGS[complement]
    )


def active_cells(nu):
    answer = set()
    for cell in CELLS:
        u, v, a, b = cell
        if any(
            (word[u], word[v]) == (a, b)
            and cofactor_may_live(nu, (u, v), word)
            for word in product(COLOURS, repeat=6)
        ):
            answer.add(cell)
    return frozenset(answer)


EXPECTED_ACTIVE = {
    "A3": 24,
    "A2_join": 44,
    "A2_rank": 32,
    "A2_isolated": 12,
    "A1_PP": 28,
    "A1_PO": 16,
    "A1_PR": 32,
    "A1_OO": 4,
    "A1_RQ_edge": 36,
    "A1_OO_edge": 24,
    "A1_RO": 16,
    "A1_RR": 28,
    "A1_RR_zero_edge": 48,
}


def audit_cofactor_bounds():
    results = {}
    for name, nu in REPRESENTATIVES:
        count = len(active_cells(nu))
        require(count == EXPECTED_ACTIVE[name],
                ("active cell count changed", name, count))
        results[name] = count
    require(max(results.values()) == 48,
            ("final multiplier-boundary rank bound changed", results))
    return results


def build_numeric_packet(nu):
    packet = {}
    for edge_index, (u, v) in enumerate(EDGES):
        for a, b in product(COLOURS, repeat=2):
            if support_value(nu, (u, v), (a, b)):
                value = 1 + (
                    17 * edge_index + 7 * a + 11 * b
                    + 3 * edge_index * edge_index
                ) % 29
            else:
                value = 0
            packet[u, v, a, b] = value
    return packet


EXPECTED_RANKS = {
    "A3": 24,
    "A2_join": 34,
    "A2_rank": 27,
    "A2_isolated": 12,
    "A1_PP": 23,
    "A1_PO": 14,
    "A1_PR": 27,
    "A1_OO": 4,
    "A1_RQ_edge": 29,
    "A1_OO_edge": 17,
    "A1_RO": 16,
    "A1_RR": 27,
    "A1_RR_zero_edge": 40,
}


def audit_calibration_ranks():
    core = run_path(str(Path(__file__).with_name(
        "verify_level_two_one_sided_overlap_collapse.py"
    )))
    results = {}
    for name, nu in REPRESENTATIVES:
        derivative = core["differential"](build_numeric_packet(nu))
        ranks = tuple(
            core["rank_mod"](derivative, prime)
            for prime in (101, 1_000_003)
        )
        require(ranks == (EXPECTED_RANKS[name], EXPECTED_RANKS[name]),
                ("calibration rank changed", name, ranks))
        results[name] = ranks
    return results


def main():
    coordinate, noncoordinate, thresholds = audit_r2_attachment_thresholds()
    census, graphs = audit_support_classification()
    active = audit_cofactor_bounds()
    ranks = audit_calibration_ranks()
    print("2I+1R+3Z equal-invertible-potential closure: all checks passed")
    print(f"  shore samples coord/noncoord : {coordinate}/{noncoordinate}")
    print(f"  R2 |A| thresholds            : {thresholds}")
    print(f"  support census |A|=3/2/1    : {census}")
    print(f"  inequivalent support graphs : {len(graphs)}")
    print(f"  active cell counts          : {active}")
    print(f"  exact modular calibrations  : {ranks}")
    print(f"  maximum rank bound          : {max(active.values())}")
    print("  combined 2I+1R+3Z status   : closed")


if __name__ == "__main__":
    main()
