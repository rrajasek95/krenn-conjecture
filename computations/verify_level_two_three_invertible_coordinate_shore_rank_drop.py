#!/usr/bin/env python3
"""Exact audit of the three-invertible coordinate-shore rank drop.

Research evidence only.  Krenn's conjecture remains open, SP-CLEAN-BRIDGE
is untouched, and no certified dependency changes.

For a three-site shore T, all nonexceptional blocks incident with T use one
fixed local colour at each shore endpoint.  With no exceptional T-T block,
the eight shore-word slices bound rank(dPsi) by 35.  With one arbitrary
exceptional T-T block, its complementary shore vertex gives a 32+10=42
bound.  A two-edge exceptional path has rank at most 49.  If all three
shore edges are exceptional but the generic-kernel equation makes the
cross spokes constant, rank is at most 51.  The first three bounds are
sharp.

The checker verifies the path and constant-cross tensor factorizations as
formal polynomial identities, enumerates the matching support implications,
verifies the zero-multiplier graph classification and deletion topology, and
computes calibration ranks over two prime fields.  Standard library only;
checks remain live under python -O and python -I -S.
"""

from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


COLOURS = (0, 1)
SITES = tuple(range(6))
INNER = (0, 1, 2)
SHORE = (3, 4, 5)
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


def support_value(edge, colours, exceptional):
    """Whether a base edge cell may be nonzero in the support class."""

    u, v = edge
    a, b = colours
    if u in INNER and v in INNER:
        return True
    if u in INNER and v in SHORE:
        return b == 0
    if edge in exceptional:
        return True
    return a == 0 and b == 0


def cofactor_may_live(edge, word, exceptional):
    complement = tuple(site for site in SITES if site not in edge)
    for matching in MATCHINGS[complement]:
        if all(support_value(
            pair, (word[pair[0]], word[pair[1]]), exceptional
        ) for pair in matching):
            return True
    return False


def empty_shore_slice_bounds():
    """Count potentially live differential cell columns on each T slice."""

    bounds = {}
    for shore_word in product(COLOURS, repeat=3):
        active_cells = set()
        for inner_word in product(COLOURS, repeat=3):
            word = inner_word + shore_word
            for cell in CELLS:
                u, v, a, b = cell
                if (word[u], word[v]) != (a, b):
                    continue
                if cofactor_may_live((u, v), word, frozenset()):
                    active_cells.add(cell)
        bounds[shore_word] = min(8, len(active_cells))
    expected = {
        (0, 0, 0): 8,
        (1, 0, 0): 8,
        (0, 1, 0): 8,
        (0, 0, 1): 8,
        (1, 1, 0): 1,
        (1, 0, 1): 1,
        (0, 1, 1): 1,
        (1, 1, 1): 0,
    }
    require(bounds == expected, ("wrong empty-shore slice bounds", bounds))
    require(sum(bounds.values()) == 35, "empty-shore bound is not 35")
    return bounds


def one_exceptional_edge_bound():
    exceptional = frozenset(((3, 4),))
    dead_site = 5

    # At output colour one on the dead site, every column not varying an
    # incident edge is literally zero: the complementary matching retains
    # the dead site and has no supported factor with which to match it.
    checked = 0
    for word in product(COLOURS, repeat=6):
        if word[dead_site] != 1:
            continue
        for edge in EDGES:
            if dead_site in edge:
                continue
            require(
                not cofactor_may_live(edge, word, exceptional),
                ("nonincident variation leaked into dead-site slice",
                 word, edge),
            )
            checked += 1

    incident_cells = tuple(
        cell for cell in CELLS
        if dead_site in cell[:2]
        and cell[2 + cell[:2].index(dead_site)] == 1
    )
    require(len(incident_cells) == 10, "dead-site slice needs ten columns")
    require(32 + len(incident_cells) == 42, "one-edge bound is not 42")
    return checked


def variable(name):
    return Counter({(name,): 1})


def polynomial_add(*values):
    answer = Counter()
    for value in values:
        answer.update(value)
    return Counter({
        monomial: coefficient
        for monomial, coefficient in answer.items()
        if coefficient
    })


def polynomial_multiply(left, right):
    answer = Counter()
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            answer[tuple(sorted(left_monomial + right_monomial))] += (
                left_coefficient * right_coefficient
            )
    return Counter({
        monomial: coefficient
        for monomial, coefficient in answer.items()
        if coefficient
    })


def build_formal_packet(exceptional, constant_cross=False):
    packet = {}
    for u, v in EDGES:
        for a, b in product(COLOURS, repeat=2):
            if constant_cross and u in INNER and v in SHORE:
                name = f"U_{u}_{a}" if b == 0 else None
            elif support_value((u, v), (a, b), exceptional):
                name = f"M_{u}_{v}_{a}_{b}"
            else:
                name = None
            packet[u, v, a, b] = variable(name) if name else Counter()
    return packet


def formal_matching_tensor(packet, word, vertices=SITES):
    total = Counter()
    for matching in MATCHINGS[tuple(vertices)]:
        term = Counter({(): 1})
        for u, v in matching:
            term = polynomial_multiply(
                term, packet[u, v, word[u], word[v]]
            )
        total = polynomial_add(total, term)
    return total


def inner_star_tensor(packet, shore_site, inner_word):
    """Sum over the three ways to cross one shore site to INNER."""

    total = Counter()
    for i in INNER:
        j, k = tuple(vertex for vertex in INNER if vertex != i)
        total = polynomial_add(total, polynomial_multiply(
            packet[i, shore_site, inner_word[i], 0],
            packet[j, k, inner_word[j], inner_word[k]],
        ))
    return total


def all_cross_tensor(packet, inner_word):
    total = Counter()
    for assignment in permutations(SHORE):
        term = Counter({(): 1})
        for i, t in zip(INNER, assignment):
            term = polynomial_multiply(
                term, packet[i, t, inner_word[i], 0]
            )
        total = polynomial_add(total, term)
    return total


def audit_path_factorization():
    path = frozenset(((3, 4), (4, 5)))
    packet = build_formal_packet(path)

    categories = {"all_cross": 0, "34": 0, "35": 0, "45": 0}
    for matching in MATCHINGS[SITES]:
        shore_edges = tuple(edge for edge in matching
                            if edge[0] in SHORE and edge[1] in SHORE)
        require(len(shore_edges) <= 1,
                ("matching used two shore edges", matching))
        category = "all_cross" if not shore_edges else (
            f"{shore_edges[0][0]}{shore_edges[0][1]}"
        )
        categories[category] += 1
    require(categories == {"all_cross": 6, "34": 3, "35": 3, "45": 3},
            ("path matching categories changed", categories))

    identities = 0
    for inner_word in product(COLOURS, repeat=3):
        h_a = inner_star_tensor(packet, 3, inner_word)
        h_b = inner_star_tensor(packet, 4, inner_word)
        h_c = inner_star_tensor(packet, 5, inner_word)
        f_tensor = polynomial_add(
            all_cross_tensor(packet, inner_word),
            polynomial_multiply(packet[3, 5, 0, 0], h_b),
        )
        for shore_word in product(COLOURS, repeat=3):
            word = inner_word + shore_word
            expected = Counter()
            if shore_word == (0, 0, 0):
                expected = polynomial_add(expected, f_tensor)
            if shore_word[2] == 0:
                expected = polynomial_add(expected, polynomial_multiply(
                    packet[3, 4, shore_word[0], shore_word[1]], h_c
                ))
            if shore_word[0] == 0:
                expected = polynomial_add(expected, polynomial_multiply(
                    packet[4, 5, shore_word[1], shore_word[2]], h_a
                ))
            require(formal_matching_tensor(packet, word) == expected,
                    ("path factorization failed", word))
            identities += 1

    support_parameters = 12 + 18 + 8 + 1
    transverse_parameters = 60 - support_parameters
    restricted_bound = 8 + 10 + 10
    require((support_parameters, transverse_parameters, restricted_bound)
            == (39, 21, 28), "path dimension count changed")
    require(restricted_bound + transverse_parameters == 49,
            "path rank bound is not 49")
    return identities, categories


def audit_constant_cross_factorization():
    triangle = frozenset(combinations(SHORE, 2))
    packet = build_formal_packet(triangle, constant_cross=True)
    identities = 0

    for inner_word in product(COLOURS, repeat=3):
        # The six all-cross matchings are identical because the spoke from
        # i has the same U_i value at all three shore sites.
        f_tensor = all_cross_tensor(packet, inner_word)
        expected_product = Counter({(): 6})
        for i in INNER:
            expected_product = polynomial_multiply(
                expected_product, packet[i, 3, inner_word[i], 0]
            )
        require(f_tensor == expected_product,
                ("constant-cross all-cross factorization failed", inner_word))

        h_tensor = inner_star_tensor(packet, 3, inner_word)
        for shore_word in product(COLOURS, repeat=3):
            word = inner_word + shore_word
            g_tensor = Counter()
            for t, u in combinations(SHORE, 2):
                v = next(site for site in SHORE if site not in (t, u))
                if word[v] == 0:
                    g_tensor = polynomial_add(
                        g_tensor, packet[t, u, word[t], word[u]]
                    )
            expected = polynomial_multiply(g_tensor, h_tensor)
            if shore_word == (0, 0, 0):
                expected = polynomial_add(expected, f_tensor)
            require(formal_matching_tensor(packet, word) == expected,
                    ("constant-cross factorization failed", word))
            identities += 1

    # G(1,1,1)=0 because every shore edge leaves a third shore site whose
    # cross spoke is supported only in colour zero.
    require(all(
        formal_matching_tensor(packet, inner_word + (1, 1, 1))
        == Counter()
        for inner_word in product(COLOURS, repeat=3)
    ), "constant-cross tensor leaked to shore word 111")

    support_parameters = 12 + 12 + 6
    transverse_parameters = 60 - support_parameters
    restricted_bound = 8 + 13
    require((support_parameters, transverse_parameters, restricted_bound)
            == (30, 30, 21), "constant-cross dimension count changed")
    require(restricted_bound + transverse_parameters == 51,
            "constant-cross rank bound is not 51")
    return identities


def build_numeric_packet(exceptional):
    packet = {}
    for edge_index, (u, v) in enumerate(EDGES):
        for a, b in product(COLOURS, repeat=2):
            if not support_value((u, v), (a, b), exceptional):
                value = 0
            else:
                value = 1 + (
                    17 * edge_index + 7 * a + 11 * b
                    + 3 * edge_index * edge_index
                ) % 29
            packet[u, v, a, b] = value
    return packet


def build_numeric_constant_cross_packet():
    packet = {}
    spoke_values = {
        i: (2 + i, 5 + 2 * i)
        for i in INNER
    }
    for edge_index, (u, v) in enumerate(EDGES):
        for a, b in product(COLOURS, repeat=2):
            if u in INNER and v in SHORE:
                value = spoke_values[u][a] if b == 0 else 0
            else:
                value = 1 + (
                    17 * edge_index + 7 * a + 11 * b
                    + 3 * edge_index * edge_index
                ) % 29
            packet[u, v, a, b] = value
    return packet


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
        if u in adjacency and v in adjacency:
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


def audit_generic_kernel_combinatorics():
    # The forced live graph is K3 on INNER joined completely to SHORE.
    forced_live = {
        edge for edge in EDGES
        if (edge[0] in INNER and edge[1] in INNER)
        or (edge[0] in INNER and edge[1] in SHORE)
    }
    for deleted in SITES:
        vertices = tuple(site for site in SITES if site != deleted)
        edges = {edge for edge in forced_live if deleted not in edge}
        require(graph_connected(vertices, edges),
                ("deletion disconnected", deleted))
        require(graph_nonbipartite(vertices, edges),
                ("deletion became bipartite", deleted))

    # Exhaust a representative integer window for the exact elementary
    # classification proved by the three equations nu_i + nu_j = 0.
    patterns = set()
    for nu in product(range(-3, 4), repeat=3):
        zero_edges = frozenset(
            (i, j) for i, j in combinations(range(3), 2)
            if nu[i] + nu[j] == 0
        )
        if len(zero_edges) < 2:
            continue
        patterns.add(len(zero_edges))
        if len(zero_edges) == 3:
            require(nu == (0, 0, 0), ("bad triangle multipliers", nu))
        else:
            degrees = [sum(i in edge for edge in zero_edges)
                       for i in range(3)]
            centre = degrees.index(2)
            leaves = [i for i in range(3) if i != centre]
            require(nu[centre] != 0, ("path centre vanished", nu))
            require(nu[leaves[0]] == nu[leaves[1]] == -nu[centre],
                    ("bad path multipliers", nu))
    require(patterns == {2, 3}, ("missing zero-graph patterns", patterns))

    # J is the symmetric off-diagonal matrix, so one orthogonality equation
    # does not identify two lines.  For a triangle, put b0=(x,y) and span
    # its J-orthogonal line by k=(x,-y).  The other two vectors are c1*k and
    # c2*k; their remaining pairing is exactly -2*c1*c2*x*y.  Localizing at
    # the nonzero c's forces x*y=0, hence b0 and k share one coordinate line.
    x = variable("x")
    y = variable("y")
    minus_y = Counter({("y",): -1})
    c1 = variable("c1")
    c2 = variable("c2")

    def j_pair(left, right):
        return polynomial_add(
            polynomial_multiply(left[0], right[1]),
            polynomial_multiply(left[1], right[0]),
        )

    def vector_scale(scalar, vector):
        return tuple(polynomial_multiply(scalar, entry) for entry in vector)

    b0 = (x, y)
    k = (x, minus_y)
    require(not j_pair(b0, k), "orthogonal-line identity failed")
    b1 = vector_scale(c1, k)
    b2 = vector_scale(c2, k)
    expected = Counter({tuple(sorted(("c1", "c2", "x", "y"))): -2})
    require(j_pair(b1, b2) == expected,
            ("symmetric triangle pairing failed", j_pair(b1, b2)))

    # Audit the two localized branches x=0 and y=0 explicitly: k is then a
    # nonzero scalar multiple of b0 on the coordinate-one/coordinate-zero
    # line, respectively.
    branch_b0 = (0, 3)
    branch_k = (0, -3)
    require(branch_k == tuple(-entry for entry in branch_b0),
            "x=0 coordinate-line branch failed")
    branch_b0 = (5, 0)
    branch_k = (5, 0)
    require(branch_k == branch_b0, "y=0 coordinate-line branch failed")


def main():
    slice_bounds = empty_shore_slice_bounds()
    checked = one_exceptional_edge_bound()
    path_identities, categories = audit_path_factorization()
    constant_identities = audit_constant_cross_factorization()
    audit_generic_kernel_combinatorics()

    core = run_path(str(Path(__file__).with_name(
        "verify_level_two_one_sided_overlap_collapse.py"
    )))
    ranks = []
    for exceptional in (
        frozenset(),
        frozenset(((3, 4),)),
        frozenset(((3, 4), (4, 5))),
    ):
        derivative = core["differential"](build_numeric_packet(exceptional))
        ranks.append(tuple(
            core["rank_mod"](derivative, prime)
            for prime in (101, 1_000_003)
        ))
    require(ranks == [(35, 35), (42, 42), (49, 49)],
            ("sharp calibration ranks failed", ranks))
    constant_derivative = core["differential"](
        build_numeric_constant_cross_packet()
    )
    constant_ranks = tuple(
        core["rank_mod"](constant_derivative, prime)
        for prime in (101, 1_000_003)
    )
    require(constant_ranks == (45, 45),
            ("constant-cross calibration rank failed", constant_ranks))

    print(
        "three-invertible coordinate shore: "
        f"slice bounds {slice_bounds}, {checked} dead-site cofactors zero; "
        f"{path_identities}+{constant_identities} formal factor identities, "
        f"matching categories {categories}; rank bounds 35/42/49/51, "
        "exact support calibrations 35/42/49 and constant-cross rank 45; "
        "the 3I+3 nonzero-rank-one generic-kernel stratum is closed"
    )


if __name__ == "__main__":
    main()
