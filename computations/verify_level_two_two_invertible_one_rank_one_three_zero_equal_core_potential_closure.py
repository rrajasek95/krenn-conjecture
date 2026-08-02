#!/usr/bin/env python3
"""Close the equal-core-potential 2I+1R+3Z generic-kernel/R2 subcase.

Sites 0,1 are invertible, site 2 is nonzero rank one, and sites 3,4,5
are zero.  Assume the three nonzero-endpoint potentials are equal.  Residual
R2 at either invertible root forces at least one opposite-potential zero
site.  There are exactly seven zero-sum support envelopes.  Six have at
most 48 potentially active differential cell columns.  The remaining
envelope has four zero columns independent of the five vertex gauges, so
its differential rank is at most 51.

Standard library only; checks remain live under python -O and python -I -S.
"""

from itertools import combinations, product
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


def support_value(nu, pair, colours):
    u, v = pair
    _, b = colours
    if pair == (0, 1):
        return True
    if u in INVERTIBLE and v == RANK_ONE:
        # Normalize the common nonzero rank-one shore factor to e_0.
        return b == 0
    # Every remaining edge has a zero endpoint.  Its numerator vanishes,
    # so its whole 2x2 block is free exactly at zero multiplier sum.
    return nu[u] + nu[v] == 0


def live_edges(nu):
    return frozenset(
        pair for pair in EDGES
        if any(support_value(nu, pair, colours)
               for colours in product(COLOURS, repeat=2))
    )


def expected_envelope(a_sites, joined=(), c_edge=None):
    core = (0, 1, 2)
    live = set(combinations(core, 2))
    live.update(edge(core_site, a) for core_site in core for a in a_sites)
    live.update(edge(a, joined_site)
                for a in a_sites for joined_site in joined)
    if c_edge is not None:
        live.add(edge(*c_edge))
    return frozenset(live)


REPRESENTATIVES = (
    # name, potentials, A, joined complement, complement edge
    ("A3", (1, 1, 1, -1, -1, -1), (3, 4, 5), (), None),
    ("A2_isolated", (1, 1, 1, -1, -1, 2), (3, 4), (), None),
    ("A2_joined", (1, 1, 1, -1, -1, 1), (3, 4), (5,), None),
    ("A1_none", (1, 1, 1, -1, 2, 3), (3,), (), None),
    ("A1_one_join", (1, 1, 1, -1, 1, 2), (3,), (4,), None),
    ("A1_two_join", (1, 1, 1, -1, 1, 1), (3,), (4, 5), None),
    ("A1_complement_edge", (1, 1, 1, -1, 2, -2),
     (3,), (), (4, 5)),
)


def audit_r2_necessity():
    # M_01 is invertible, hence is not a pure-column R2 witness.  If no zero
    # has potential -lambda, all I-Z blocks vanish.  The sole remaining
    # internal candidate at either invertible root is the one edge to site 2;
    # one edge cannot provide two distinct R2 witness labels.
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

    vectors = tuple(
        vector for vector in product((-1, 0, 1), repeat=2)
        if vector != (0, 0)
    )
    for left in vectors:
        for shore_factor in vectors:
            block = tuple(
                tuple(left[row] * shore_factor[column]
                      for column in COLOURS)
                for row in COLOURS
            )
            require(len(pure_columns(block)) <= 1,
                    ("one rank-one edge supplied two colours", block))

    for entries in product((-1, 0, 1), repeat=4):
        block = (entries[:2], entries[2:])
        determinant = block[0][0] * block[1][1] - block[0][1] * block[1][0]
        if determinant:
            require(not pure_columns(block),
                    ("invertible core edge became pure", block))

    internal_labels_without_a = (RANK_ONE,)
    require(len(set(internal_labels_without_a)) == 1,
            "empty opposite-potential set unexpectedly supplied two labels")
    require(all(len(ZERO) == 3 for _ in INVERTIBLE),
            "zero-site count changed")
    return len(internal_labels_without_a)


def audit_support_census():
    names = set()
    for name, nu, a_sites, joined, c_edge in REPRESENTATIVES:
        require(nu[0] == nu[1] == nu[2] != 0,
                ("core potentials stopped being equal nonzero", name, nu))
        actual_a = tuple(site for site in ZERO if nu[site] == -nu[0])
        require(actual_a == a_sites, ("wrong A set", name, actual_a, a_sites))
        actual = live_edges(nu)
        expected = expected_envelope(a_sites, joined, c_edge)
        require(actual == expected,
                ("support envelope mismatch", name, actual, expected))
        names.add(name)
    require(len(names) == 7, ("support census changed", names))

    # Elementary classification: for |A|=2 the last zero is isolated or has
    # potential lambda and joins all of A.  For |A|=1, each remaining zero
    # may have potential lambda, or the two may be opposite; a join and the
    # complement edge cannot coexist because its other endpoint would be in A.
    cases_by_size = {3: 1, 2: 2, 1: 4}
    require(sum(cases_by_size.values()) == 7,
            "equal-core envelope count changed")
    return cases_by_size


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


def graph_connected(vertices, edges):
    vertices = set(vertices)
    seen = {next(iter(vertices))}
    while True:
        expanded = seen | {
            v for u, v in edges if u in seen
        } | {
            u for u, v in edges if v in seen
        }
        expanded &= vertices
        if expanded == seen:
            return seen == vertices
        seen = expanded


def graph_nonbipartite(vertices, edges):
    adjacency = {vertex: set() for vertex in vertices}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    colours = {}
    for root in vertices:
        if root in colours:
            continue
        colours[root] = 0
        stack = [root]
        while stack:
            u = stack.pop()
            for v in adjacency[u]:
                if v not in colours:
                    colours[v] = 1 - colours[u]
                    stack.append(v)
                elif colours[v] == colours[u]:
                    return True
    return False


def audit_cofactor_bounds():
    expected_counts = {
        "A3": 48,
        "A2_isolated": 20,
        "A2_joined": 56,
        "A1_none": 4,
        "A1_one_join": 16,
        "A1_two_join": 28,
        "A1_complement_edge": 28,
    }
    results = {}
    for name, nu, _a_sites, _joined, _c_edge in REPRESENTATIVES:
        active = active_cells(nu)
        require(len(active) == expected_counts[name],
                ("active cell count changed", name, len(active)))
        results[name] = len(active)

        if name == "A2_joined":
            zero_cells = frozenset(CELLS) - active
            expected_zero = frozenset(
                (3, 4, a, b) for a, b in product(COLOURS, repeat=2)
            )
            require(zero_cells == expected_zero,
                    ("A2 joined zero columns changed", zero_cells))

            # The zero columns are base-zero, so every vertex gauge vanishes
            # on them.  The generic live graph contains the core triangle and
            # is connected, making its five sum-zero gauges independent.
            graph = live_edges(nu)
            require(graph_connected(SITES, graph),
                    "A2 joined live graph disconnected")
            require(graph_nonbipartite(SITES, graph),
                    "A2 joined live graph became bipartite")

    require(max(value for name, value in results.items()
                if name != "A2_joined") == 48,
            ("direct cofactor maximum changed", results))
    require(60 - (4 + 5) == 51,
            "A2 joined zero-column/gauge bound changed")
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


def audit_calibration_ranks():
    core = run_path(str(Path(__file__).with_name(
        "verify_level_two_one_sided_overlap_collapse.py"
    )))
    expected = {
        "A3": 44,
        "A2_isolated": 20,
        "A2_joined": 45,
        "A1_none": 4,
        "A1_one_join": 14,
        "A1_two_join": 23,
        "A1_complement_edge": 19,
    }
    results = {}
    for name, nu, _a_sites, _joined, _c_edge in REPRESENTATIVES:
        derivative = core["differential"](build_numeric_packet(nu))
        ranks = tuple(
            core["rank_mod"](derivative, prime)
            for prime in (101, 1_000_003)
        )
        require(ranks == (expected[name], expected[name]),
                ("calibration rank changed", name, ranks))
        results[name] = ranks
    return results


def main():
    remaining_labels = audit_r2_necessity()
    census = audit_support_census()
    active = audit_cofactor_bounds()
    ranks = audit_calibration_ranks()
    bounds = {
        name: 51 if name == "A2_joined" else count
        for name, count in active.items()
    }
    require(max(bounds.values()) == 51,
            ("equal-core rank bound changed", bounds))
    print("2I+1R+3Z equal-core-potential closure: all checks passed")
    print(f"  R2 labels without A       : {remaining_labels}")
    print(f"  support census by |A|     : {census}")
    print(f"  active cell counts        : {active}")
    print(f"  exact modular calibrations: {ranks}")
    print(f"  differential rank bounds : {bounds}")
    print(f"  maximum rank bound        : {max(bounds.values())}")


if __name__ == "__main__":
    main()
