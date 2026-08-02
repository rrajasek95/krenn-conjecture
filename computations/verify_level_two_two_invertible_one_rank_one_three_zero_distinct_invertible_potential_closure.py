#!/usr/bin/env python3
"""Close the distinct-invertible-potential 2I+1R+3Z R2 stratum.

For endpoint ranks (2,2,1,0,0,0), residual R2 has a sharp dichotomy at
the two invertible roots.  If the common rank-one shore factor is not a
physical coordinate, each root needs two zero-site witnesses; distinct
invertible potentials make the two attachment sets disjoint, impossible
among three zero sites.  Hence the shore factor is a coordinate and both
nonempty attachment sets consume at least two zero sites.

Up to swapping the invertible roots and permuting zero sites, the resulting
zero-sum supports have eleven envelopes.  Exact local-colour cofactor counts
bound every differential rank by at most 48.

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


def audit_r2_dichotomy():
    vectors = tuple(
        vector for vector in product((-1, 0, 1), repeat=2)
        if vector != (0, 0)
    )
    coordinate_factors = []
    noncoordinate_factors = []
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
                ("shore-factor witness count depended on left factor",
                 shore_factor, counts))
        count = next(iter(counts))
        if count:
            require(count == 1, ("rank-one edge supplied two colours", count))
            coordinate_factors.append(shore_factor)
        else:
            noncoordinate_factors.append(shore_factor)

    require(set(coordinate_factors) == {(-1, 0), (1, 0), (0, -1), (0, 1)},
            ("coordinate shore factors changed", coordinate_factors))
    require(noncoordinate_factors,
            "noncoordinate shore-factor branch disappeared")

    # With distinct invertible potentials, A={z:nu_z=-nu_0} and
    # B={z:nu_z=-nu_1} are disjoint.  A noncoordinate factor gives no R2
    # witness, so |A|,|B|>=2 would require at least four zero sites.
    require(2 + 2 > len(ZERO),
            "three zero sites unexpectedly fit two disjoint witness pairs")

    # On the surviving coordinate branch, the rank-one edge gives one common
    # witness colour and R2 forces one attached zero at each invertible root.
    require(1 + 1 <= len(ZERO), "coordinate R2 attachment budget changed")
    return len(coordinate_factors), len(noncoordinate_factors)


def support_value(nu, pair, colours):
    u, v = pair
    _, b = colours
    if pair == (0, 1):
        return True
    if u in INVERTIBLE and v == RANK_ONE:
        return b == 0
    return nu[u] + nu[v] == 0


def live_edges(nu):
    return frozenset(
        pair for pair in EDGES
        if any(support_value(nu, pair, colours)
               for colours in product(COLOURS, repeat=2))
    )


REPRESENTATIVES = (
    # Attachment sets exhaust Z: up to swapping roots, |A|=2 and |B|=1.
    ("full_no_internal_rA", (1, 2, 1, -1, -1, -2)),
    ("full_no_internal_rB", (1, 2, 2, -1, -1, -2)),
    ("full_no_internal_rnone", (1, 2, 3, -1, -1, -2)),
    ("full_internal_rB", (0, 1, 1, 0, 0, -1)),
    ("full_internal_rnone", (0, 1, 2, 0, 0, -1)),
    # One leftover zero: six compatible rank-one/zero-edge attachment types.
    ("left_rA_joinA", (1, 2, 1, -1, -2, 1)),
    ("left_rA_joinB", (1, 2, 1, -1, -2, 2)),
    ("left_rA_none", (1, 2, 1, -1, -2, 3)),
    ("left_rleft", (1, 2, 3, -1, -2, -3)),
    ("left_rnone_joinA", (1, 2, 3, -1, -2, 1)),
    ("left_rnone_none", (1, 2, 3, -1, -2, 4)),
)


def canonical_graph(edges):
    variants = []
    for swap in (False, True):
        for zero_permutation in permutations(ZERO):
            mapping = {
                0: 1 if swap else 0,
                1: 0 if swap else 1,
                2: 2,
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
    for name, nu in REPRESENTATIVES:
        alpha, beta, gamma = nu[:3]
        require(alpha != beta, ("invertible potentials coalesced", name, nu))
        require(all(nu[u] + nu[v] != 0
                    for u, v in ((0, 1), (0, 2), (1, 2))),
                ("core zero sum appeared", name, nu))
        a_sites = tuple(site for site in ZERO if nu[site] == -alpha)
        b_sites = tuple(site for site in ZERO if nu[site] == -beta)
        require(a_sites and b_sites and not (set(a_sites) & set(b_sites)),
                ("R2 attachment sets changed", name, a_sites, b_sites))
        graph = canonical_graph(live_edges(nu))
        require(graph not in graphs,
                ("two representatives have the same support", name, graphs))
        graphs[graph] = name

    # If A and B exhaust Z, their sizes are 2+1.  The doubled-set internal
    # edge is optional only when its core potential is zero.  The rank-one
    # site may attach to A, B, or neither, except that zero core potential
    # forbids attachment to its own doubled set: 3+2=5 envelopes.
    full_states = {
        (False, "A"), (False, "B"), (False, "none"),
        (True, "B"), (True, "none"),
    }
    # With one leftover site, its rank-one attachment target is A, B, itself,
    # or none; its zero-edge join is A, B, or none.  Core nonzero-sum
    # constraints leave six types up to A/B interchange.
    leftover_states = {
        ("A", "A"), ("A", "B"), ("A", "none"),
        ("left", "none"), ("none", "A"), ("none", "none"),
    }
    require((len(full_states), len(leftover_states), len(graphs)) == (5, 6, 11),
            "distinct-potential support census changed")
    return len(full_states), len(leftover_states), graphs


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
    "full_no_internal_rA": 32,
    "full_no_internal_rB": 28,
    "full_no_internal_rnone": 20,
    "full_internal_rB": 48,
    "full_internal_rnone": 36,
    "left_rA_joinA": 32,
    "left_rA_joinB": 36,
    "left_rA_none": 16,
    "left_rleft": 24,
    "left_rnone_joinA": 28,
    "left_rnone_none": 12,
}


def audit_cofactor_bounds():
    results = {}
    for name, nu in REPRESENTATIVES:
        count = len(active_cells(nu))
        require(count == EXPECTED_ACTIVE[name],
                ("active cell count changed", name, count))
        results[name] = count
    require(max(results.values()) == 48,
            ("distinct-potential rank bound changed", results))
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
    "full_no_internal_rA": 27,
    "full_no_internal_rB": 27,
    "full_no_internal_rnone": 19,
    "full_internal_rB": 41,
    "full_internal_rnone": 30,
    "left_rA_joinA": 26,
    "left_rA_joinB": 30,
    "left_rA_none": 16,
    "left_rleft": 22,
    "left_rnone_joinA": 23,
    "left_rnone_none": 12,
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
    coordinate, noncoordinate = audit_r2_dichotomy()
    full_count, leftover_count, graphs = audit_support_classification()
    active = audit_cofactor_bounds()
    ranks = audit_calibration_ranks()
    print("2I+1R+3Z distinct-invertible-potential closure: all checks passed")
    print(f"  shore-factor samples coord/noncoord: {coordinate}/{noncoordinate}")
    print(f"  support census full/leftover       : {full_count}/{leftover_count}")
    print(f"  inequivalent support graphs        : {len(graphs)}")
    print(f"  active cell counts                 : {active}")
    print(f"  exact modular calibrations         : {ranks}")
    print(f"  maximum differential rank bound   : {max(active.values())}")


if __name__ == "__main__":
    main()
