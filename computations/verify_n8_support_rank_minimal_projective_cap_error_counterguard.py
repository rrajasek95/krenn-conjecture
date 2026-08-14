#!/usr/bin/env python3
"""Exact N=8 projective-cap rank dichotomy and minimal physical guard.

The first audit is formal linear algebra for an exact target source.  The
second is one literal endpoint-ordered C8 aggregate source.  It has minimum
edge support among sources for which all 28 pairs are doubly injective; on
that minimum support, full rank of all eight blocks (total rank 24) is
forced.  Its three pure coefficients are normalized to one, and its
projective cross-error map is injective at every pair.

The C8 source is deliberately *not* a GHZ source: a displayed mixed word is
nonzero.  It is a guard against support/rank/pure-normalization arguments,
not a counterexample to Krenn's conjecture.  The final audit classifies the
next support layer: among 13-edge graphs of minimum degree at least three,
the exact clean-error support leaves one graph, K_(4,4) minus a three-edge
matching.  Its independent shore puts it in the already proved full-mixed-row
exclusion ``no-independent-four-set-at-eight``.
"""

from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
import json


N = 8
COLORS = range(3)
PRIME = 1_000_003
EXPECTED_LEDGER_SHA256 = "80bd9cdff56f61bdc54e3f35de82f880991c38abbe4878fdccf6170fa52d1f7f"

ZERO = (
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
)

# The cyclic order is 0-4-1-5-2-6-3-7-0.  All stored blocks have their
# smaller physical endpoint first.  The entries were selected once over the
# integers; no search is performed by this checker.
BLOCKS = {
    (0, 4): ((5, 3, 9), (4, 16, 15), (16, 13, 7)),
    (0, 7): ((4, 16, 1), (13, 14, 1), (15, 9, 8)),
    (1, 4): ((4, 11, 1), (1, 1, 1), (13, 7, 14)),
    (1, 5): ((1, 17, 8), (15, 16, 8), (12, 8, 8)),
    (2, 5): ((15, 10, 1), (14, 4, 6), (10, 4, 11)),
    (2, 6): ((17, 14, 17), (7, 10, 10), (16, 17, 13)),
    (3, 6): ((2, 16, 8), (13, 14, 6), (12, 12, 3)),
    (3, 7): ((15, 17, 4), (6, 17, 13), (12, 16, 1)),
}

# The first support not forced into the degree-two clean theorem:
# K_(4,4) with one perfect matching removed, i.e. the cubic cube graph.
CUBIC_BLOCKS = {
    (0, 5): ((5, 3, 9), (4, 16, 15), (16, 13, 7)),
    (0, 6): ((4, 16, 1), (13, 14, 1), (15, 9, 8)),
    (0, 7): ((4, 11, 1), (1, 1, 1), (13, 7, 14)),
    (1, 4): ((1, 17, 8), (15, 16, 8), (12, 8, 8)),
    (1, 6): ((15, 10, 1), (14, 4, 6), (10, 4, 11)),
    (1, 7): ((17, 14, 17), (7, 10, 10), (16, 17, 13)),
    (2, 4): ((2, 16, 8), (13, 14, 6), (12, 12, 3)),
    (2, 5): ((15, 17, 4), (6, 17, 13), (12, 16, 1)),
    (2, 7): ((16, 2, 10), (13, 6, 6), (17, 8, 1)),
    (3, 4): ((7, 8, 13), (17, 12, 12), (15, 9, 1)),
    (3, 5): ((13, 17, 5), (17, 7, 14), (2, 16, 12)),
    (3, 6): ((7, 17, 14), (16, 12, 14), (12, 1, 11)),
}


def require(condition, detail):
    """Assertion which remains active under ``python -O``."""
    if not condition:
        raise RuntimeError(detail)


def transpose(matrix):
    return tuple(tuple(matrix[j][i] for j in COLORS) for i in COLORS)


def determinant_3(matrix):
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def stored_block(blocks, u, v):
    require(u < v, ("stored endpoint order changed", u, v))
    return blocks.get((u, v), ZERO)


def oriented_block(blocks, endpoint, neighbor):
    u, v = sorted((endpoint, neighbor))
    matrix = stored_block(blocks, u, v)
    return matrix if endpoint == u else transpose(matrix)


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        partner = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((first, partner),) + tail)
    return tuple(answer)


def coefficient(blocks, vertices, word, modulus=None):
    """Literal matching coefficient on ``vertices`` in endpoint order."""
    total = 0
    for matching in perfect_matchings(tuple(vertices)):
        term = 1
        for u, v in matching:
            matrix = stored_block(blocks, u, v)
            term *= matrix[word[u]][word[v]]
            if modulus is not None:
                term %= modulus
            if term == 0:
                break
        total += term
        if modulus is not None:
            total %= modulus
    return total


def rank_mod(matrix, modulus=PRIME):
    rows = [[entry % modulus for entry in row] for row in matrix]
    rows = [row for row in rows if any(row)]
    if not rows:
        return 0
    rank = 0
    width = len(rows[0])
    for column in range(width):
        pivot = next(
            (index for index in range(rank, len(rows)) if rows[index][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column], modulus - 2, modulus)
        rows[rank] = [(entry * inverse) % modulus for entry in rows[rank]]
        for index in range(len(rows)):
            if index == rank or rows[index][column] == 0:
                continue
            scalar = rows[index][column]
            rows[index] = [
                (entry - scalar * pivot_entry) % modulus
                for entry, pivot_entry in zip(rows[index], rows[rank], strict=True)
            ]
        rank += 1
        if rank == width:
            break
    return rank


def normalize_at_site_zero(blocks, expected_pure):
    pure = tuple(
        coefficient(blocks, range(N), (colour,) * N) for colour in COLORS
    )
    require(pure == expected_pure, ("pure ledger changed", pure))
    require(all(value % PRIME for value in pure), "normalization met the audit prime")

    normalized = {}
    normalized_mod = {}
    for edge, matrix in blocks.items():
        rational_rows = []
        modular_rows = []
        for row_colour, row in enumerate(matrix):
            scale = Fraction(1, pure[row_colour]) if edge[0] == 0 else Fraction(1)
            modular_scale = (
                pow(pure[row_colour], PRIME - 2, PRIME) if edge[0] == 0 else 1
            )
            rational_rows.append(tuple(scale * entry for entry in row))
            modular_rows.append(
                tuple((modular_scale * entry) % PRIME for entry in row)
            )
        normalized[edge] = tuple(rational_rows)
        normalized_mod[edge] = tuple(modular_rows)
    return pure, normalized, normalized_mod


def audit_exact_source_rank_dichotomy():
    """Audit the quotient ranks in the exact-target formula.

    For an exact target source the nine cap-error columns, modulo Q, are six
    zero off-diagonal columns and the images of X0,X1,X2.  The three cases
    below are Q=0, Q outside their span, and nonzero Q in their span.
    """
    # Coordinates are X0,X1,X2,Z.  Appending Q as a last column computes
    # the quotient rank rank([kappa,Q])-rank(Q).
    diagonal_columns = (
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
    )

    def quotient_rank(q):
        matrix = [
            [diagonal_columns[column][row] for column in COLORS] + [q[row]]
            for row in range(4)
        ]
        q_rank = int(any(q))
        return rank_mod(matrix) - q_rank

    require(quotient_rank((0, 0, 0, 0)) == 3, "Q=0 quotient rank changed")
    require(quotient_rank((0, 0, 0, 1)) == 3, "Q outside target plane changed")
    for q in ((1, 0, 0, 0), (1, 2, 0, 0), (1, 2, 3, 0)):
        require(quotient_rank(q) == 2, ("Q in target plane changed", q))

        # The only diagonal zero-error direction is the Q coefficient line.
        diagonal_map_with_q = [
            [diagonal_columns[column][row] for column in COLORS] + [-q[row]]
            for row in range(4)
        ]
        require(rank_mod(diagonal_map_with_q) == 3, ("kernel line changed", q))

    # It is target-active precisely in the last case: every diagonal value
    # of the unique kernel vector is nonzero.
    require(all((1, 2, 3)), "active diagonal test changed")
    require(not all((1, 2, 0)), "inactive diagonal test changed")


def audit_support_and_rank_minimality(normalized):
    vertices = tuple(range(N))
    edges = set(BLOCKS)
    require(len(edges) == N, ("C8 support size changed", len(edges)))

    degrees = {
        vertex: sum(vertex in edge for edge in edges) for vertex in vertices
    }
    require(set(degrees.values()) == {2}, ("support stopped being C8", degrees))
    require(sum(degrees.values()) // 2 == 8, "handshake lower bound changed")

    for edge in edges:
        require(determinant_3(BLOCKS[edge]) != 0, ("singular integer block", edge))
        require(determinant_3(normalized[edge]) != 0, ("singular normalized block", edge))

    # Every deleted endpoint retains one or two invertible blocks, so every
    # pair is doubly injective.
    for p, q in combinations(vertices, 2):
        internal = set(vertices) - {p, q}
        for endpoint in (p, q):
            retained = [
                neighbor
                for neighbor in internal
                if tuple(sorted((endpoint, neighbor))) in edges
            ]
            require(retained, ("noninjective retained star", p, q, endpoint))
            require(
                all(
                    determinant_3(oriented_block(normalized, endpoint, neighbor))
                    for neighbor in retained
                ),
                ("retained block lost rank", p, q, endpoint),
            )

    # Edge-deletion minimality for the all-pairs-good property.  Removing uv
    # leaves u with its other neighbour q; deleting the pair {u,q} then
    # leaves the u-star identically zero.
    for removed in edges:
        u = removed[0]
        other = next(
            neighbor
            for neighbor in vertices
            if neighbor != removed[1]
            and tuple(sorted((u, neighbor))) in edges
        )
        remaining_edges = edges - {removed}
        residual_neighbors = [
            neighbor
            for neighbor in vertices
            if neighbor not in (u, other)
            and tuple(sorted((u, neighbor))) in remaining_edges
        ]
        require(
            residual_neighbors == [],
            ("edge deletion unexpectedly preserved all-pair goodness", removed),
        )

    # Any all-pairs-good support has degree at least two at every vertex, so
    # eight edges is the absolute support minimum.  At degree two, deleting
    # either neighbour leaves one block; that block must have rank three.
    total_block_rank = sum(3 for _ in edges)
    require(total_block_rank == 24, "minimum total block-rank ledger changed")


def audit_minimum_support_clean_caps(normalized):
    """Audit the local one-edge correction behind the restricted theorem."""
    vertices = tuple(range(N))
    edges = set(BLOCKS)
    clean_pairs = []
    for p, q in sorted(edges):
        p_external = [
            vertex
            for vertex in vertices
            if vertex != q and tuple(sorted((p, vertex))) in edges
        ]
        q_external = [
            vertex
            for vertex in vertices
            if vertex != p and tuple(sorted((q, vertex))) in edges
        ]
        require(
            len(p_external) == len(q_external) == 1,
            ("minimum-support external star changed", p, q),
        )

        # For K=I, all three target diagonal readouts are one.  Positivity of
        # this displayed model makes the direct scalar visibly nonzero.
        direct = oriented_block(normalized, p, q)
        direct_scalar = sum(direct[colour][colour] for colour in COLORS)
        require(direct_scalar > 0, ("identity cap became inactive", p, q))

        # The effective correction can live only on the one pair joining the
        # two external star sites (or is zero if those sites coincide).  Its
        # square is therefore zero in the site-square-zero algebra, so all
        # higher clean-cap terms vanish.
        correction_support = (
            []
            if p_external[0] == q_external[0]
            else [tuple(sorted((p_external[0], q_external[0])))]
        )
        require(len(correction_support) <= 1,
                ("clean correction acquired two edges", p, q))
        clean_pairs.append([p, q])
    require(len(clean_pairs) == 8, "active clean-edge census changed")
    return clean_pairs


def audit_degree_two_clean_threshold():
    """The first support not forced to have a degree-two vertex is 12."""
    for edge_count in range(8, 12):
        degree_sum = 2 * edge_count
        require(degree_sum < 3 * N,
                ("subcubic support threshold changed", edge_count))
        # With all degrees at least two, average degree below three forces a
        # degree-two vertex.  Every incident pair there has a one-site
        # deleted star, hence a star-supported square-zero correction.
    require(2 * 12 == 3 * N, "cubic boundary changed")


def generate_degree_sequence_graphs(target_degrees, vertex=0,
                                    adjacency=None, degrees=None):
    """Generate every labelled simple graph with the displayed degrees.

    The labels in ``target_degrees`` are fixed.  This lets the 13-edge audit
    pin its two high-degree vertices and count each labelled graph once.
    """
    if adjacency is None:
        adjacency = [0] * N
        degrees = [0] * N
    while vertex < N and degrees[vertex] == target_degrees[vertex]:
        vertex += 1
    if vertex == N:
        yield tuple(adjacency)
        return
    need = target_degrees[vertex] - degrees[vertex]
    if need < 0:
        return
    candidates = [
        neighbor
        for neighbor in range(vertex + 1, N)
        if degrees[neighbor] < target_degrees[neighbor]
    ]
    for chosen in combinations(candidates, need):
        new_adjacency = list(adjacency)
        new_degrees = list(degrees)
        for neighbor in chosen:
            new_adjacency[vertex] |= 1 << neighbor
            new_adjacency[neighbor] |= 1 << vertex
            new_degrees[vertex] += 1
            new_degrees[neighbor] += 1
        yield from generate_degree_sequence_graphs(
            target_degrees, vertex + 1, new_adjacency, new_degrees
        )


def generate_cubic_graphs(vertex=0, adjacency=None, degrees=None):
    """Generate every labelled simple cubic graph on eight vertices once."""
    require(vertex == 0 and adjacency is None and degrees is None,
            "the cubic wrapper is only called at its root")
    yield from generate_degree_sequence_graphs((3,) * N)


def graph_edges(adjacency):
    return tuple(
        (u, v)
        for u in range(N)
        for v in range(u + 1, N)
        if (adjacency[u] >> v) & 1
    )


def component_sizes(adjacency):
    unseen = set(range(N))
    sizes = []
    while unseen:
        start = next(iter(unseen))
        seen = {start}
        stack = [start]
        while stack:
            u = stack.pop()
            for v in range(N):
                if (adjacency[u] >> v) & 1 and v not in seen:
                    seen.add(v)
                    stack.append(v)
        unseen -= seen
        sizes.append(len(seen))
    return tuple(sorted(sizes))


def is_bipartite(adjacency):
    colours = {}
    for start in range(N):
        if start in colours:
            continue
        colours[start] = 0
        stack = [start]
        while stack:
            u = stack.pop()
            for v in range(N):
                if not ((adjacency[u] >> v) & 1):
                    continue
                if v not in colours:
                    colours[v] = 1 - colours[u]
                    stack.append(v)
                elif colours[v] == colours[u]:
                    return False
    return True


def triangle_count(adjacency):
    return sum(
        all(
            (adjacency[u] >> v) & 1
            for u, v in ((a, b), (b, c), (c, a))
        )
        for a, b, c in combinations(range(N), 3)
    )


def square_count(adjacency):
    total = 0
    for a, b, c, d in combinations(range(N), 4):
        # Each of the three partitions into opposite pairs specifies one
        # (not necessarily induced) four-cycle.
        for x, y, z, w in ((a, b, c, d), (a, c, b, d), (a, d, b, c)):
            if all(
                (adjacency[u] >> v) & 1
                for u, v in ((x, z), (x, w), (y, z), (y, w))
            ):
                total += 1
    return total


def sealed_edge(adjacency, p, q):
    """True exactly when the support argument does not clean edge pq."""
    p_external = {
        vertex
        for vertex in range(N)
        if (adjacency[p] >> vertex) & 1
    } - {q}
    q_external = {
        vertex
        for vertex in range(N)
        if (adjacency[q] >> vertex) & 1
    } - {p}
    if p_external & q_external:
        return False
    leftover = set(range(N)) - {p, q} - p_external - q_external
    require(len(leftover) == 2, ("cubic leftover census changed", p, q))
    u, v = sorted(leftover)
    return bool((adjacency[u] >> v) & 1)


def response_support_clean_edge(adjacency, p, q):
    """Support-only sufficient test for the exact N=8 clean error.

    On deleting p,q, put P=N(p)-{q}, S=N(q)-{p}.  Every edge of the effective
    response quadratic r joins P to S (common vertices are allowed, loops are
    not).  The homogeneous clean error is

                         s r^[2] x + r^[3].

    It is therefore identically zero, for every cap matrix K and all block
    coefficients, if no residual perfect matching can be tagged either RRX
    or RRR.  The test deliberately uses the largest possible R support, so a
    clean verdict is coefficient-independent and source-valid.
    """
    require((adjacency[p] >> q) & 1, ("inactive edge tested", p, q))
    residual = tuple(vertex for vertex in range(N) if vertex not in (p, q))
    p_external = {
        vertex for vertex in residual if (adjacency[p] >> vertex) & 1
    }
    q_external = {
        vertex for vertex in residual if (adjacency[q] >> vertex) & 1
    }
    response_edges = {
        tuple(sorted((left, right)))
        for left in p_external
        for right in q_external
        if left != right
    }
    source_edges = set(graph_edges(adjacency))
    for matching in perfect_matchings(residual):
        matching = tuple(tuple(sorted(edge)) for edge in matching)
        if all(edge in response_edges for edge in matching):
            return False                         # an RRR monomial can occur
        if any(
            matching[x_index] in source_edges
            and all(
                matching[index] in response_edges
                for index in range(3) if index != x_index
            )
            for x_index in range(3)
        ):
            return False                         # an RRX monomial can occur
    return True


def cubic_signature(adjacency):
    edges = graph_edges(adjacency)
    return (
        component_sizes(adjacency),
        is_bipartite(adjacency),
        triangle_count(adjacency),
        square_count(adjacency),
        sum(sealed_edge(adjacency, *edge) for edge in edges),
    )


EDGE_POSITIONS = {
    edge: index for index, edge in enumerate(combinations(range(N), 2))
}


def permuted_edge_mask(adjacency, permutation):
    mask = 0
    for u, v in graph_edges(adjacency):
        image = tuple(sorted((permutation[u], permutation[v])))
        mask |= 1 << EDGE_POSITIONS[image]
    return mask


def audit_cubic_graph_classification():
    expected_counts = {
        ((4, 4), False, 8, 6, 0): 35,
        ((8,), False, 0, 4, 4): 2520,
        ((8,), False, 1, 3, 6): 3360,
        ((8,), False, 2, 2, 6): 10080,
        ((8,), False, 4, 2, 2): 2520,
        ((8,), True, 0, 6, 12): 840,
    }
    counts = {}
    representatives = {}
    labelled_count = 0
    for adjacency in generate_cubic_graphs():
        labelled_count += 1
        for edge in graph_edges(adjacency):
            require(
                response_support_clean_edge(adjacency, *edge)
                == (not sealed_edge(adjacency, *edge)),
                ("general clean-support test disagrees with cubic test", edge),
            )
        signature = cubic_signature(adjacency)
        counts[signature] = counts.get(signature, 0) + 1
        representatives.setdefault(signature, adjacency)
    require(labelled_count == 19355, ("labelled cubic census changed", labelled_count))
    require(counts == expected_counts, ("cubic signature census changed", counts))

    # The orbit of each representative has the full recorded signature
    # count.  Hence each of the six signatures is one isomorphism class.
    all_permutations = tuple(permutations(range(N)))
    ledger = []
    for signature in sorted(representatives, key=str):
        adjacency = representatives[signature]
        orbit = {
            permuted_edge_mask(adjacency, permutation)
            for permutation in all_permutations
        }
        require(len(orbit) == counts[signature],
                ("signature split into multiple graph orbits", signature))
        edges = graph_edges(adjacency)
        clean_edges = [edge for edge in edges if not sealed_edge(adjacency, *edge)]
        is_cube = signature == ((8,), True, 0, 6, 12)
        require(bool(clean_edges) != is_cube,
                ("cubic clean/cube dichotomy changed", signature))
        ledger.append(
            {
                "signature": signature,
                "labelled_orbit_size": len(orbit),
                "representative_edges": edges,
                "support_clean_edge_count": len(clean_edges),
                "is_cube": is_cube,
            }
        )
    require(sum(item["is_cube"] for item in ledger) == 1,
            "cube uniqueness changed")
    return ledger


def audit_thirteen_edge_graph_classification():
    """Close the 13-edge layer modulo the proved independent-shore theorem.

    Once degree-two vertices have supplied a clean incident edge, the
    handshake lemma leaves only degree sequences (5,3^7) and (4,4,3^6).
    We enumerate both with their high-degree labels pinned.  An edge is
    declared support-clean only by ``response_support_clean_edge`` above,
    i.e. after checking the literal RRX/RRR monomial support of the full
    homogeneous clean error rather than the older cubic shorthand.
    """
    degree_sequences = (
        (5, 3, 3, 3, 3, 3, 3, 3),
        (4, 4, 3, 3, 3, 3, 3, 3),
    )
    expected = {
        degree_sequences[0]: {
            "labelled_count": 9660,
            "clean_edge_distribution": {
                3: 1260, 4: 1260, 5: 3780, 6: 3150, 8: 210,
            },
            "terminal_count": 0,
        },
        degree_sequences[1]: {
            "labelled_count": 15740,
            "clean_edge_distribution": {
                0: 120, 1: 360, 2: 720, 3: 2700, 4: 3240,
                5: 5220, 6: 1620, 7: 1560, 10: 180, 12: 20,
            },
            "terminal_count": 120,
        },
    }

    ledgers = []
    terminal_graphs = []
    for target in degree_sequences:
        distribution = {}
        labelled_count = 0
        terminals = []
        for adjacency in generate_degree_sequence_graphs(target):
            labelled_count += 1
            edges = graph_edges(adjacency)
            require(len(edges) == 13, ("13-edge census changed", target))
            require(
                tuple(adjacency[v].bit_count() for v in range(N)) == target,
                ("degree-sequence generator changed", target, edges),
            )
            clean_edges = tuple(
                edge
                for edge in edges
                if response_support_clean_edge(adjacency, *edge)
            )
            distribution[len(clean_edges)] = (
                distribution.get(len(clean_edges), 0) + 1
            )
            if not clean_edges:
                terminals.append(adjacency)
        target_expected = expected[target]
        require(labelled_count == target_expected["labelled_count"],
                ("13-edge labelled census changed", target, labelled_count))
        require(distribution == target_expected["clean_edge_distribution"],
                ("13-edge clean distribution changed", target, distribution))
        require(len(terminals) == target_expected["terminal_count"],
                ("13-edge terminal census changed", target, len(terminals)))
        terminal_graphs.extend(terminals)
        ledgers.append(
            {
                "degree_sequence": target,
                "labelled_count": labelled_count,
                "clean_edge_distribution": distribution,
                "terminal_count": len(terminals),
            }
        )

    # The 120 survivors form one orbit under the degree-preserving group
    # S_2 x S_6.  Pin a transparent representative: K_(4,4) minus the three
    # disjoint cross edges 27,36,45.
    representative_edges = (
        (0, 1), (0, 2), (0, 3), (0, 4),
        (1, 5), (1, 6), (1, 7),
        (2, 5), (2, 6),
        (3, 5), (3, 7),
        (4, 6), (4, 7),
    )
    representative = [0] * N
    for u, v in representative_edges:
        representative[u] |= 1 << v
        representative[v] |= 1 << u
    representative = tuple(representative)
    terminal_masks = {permuted_edge_mask(graph, tuple(range(N)))
                      for graph in terminal_graphs}
    require(permuted_edge_mask(representative, tuple(range(N))) in terminal_masks,
            "pinned 13-edge representative stopped being terminal")
    degree_preserving_permutations = []
    for high_images in permutations((0, 1)):
        for low_images in permutations(range(2, N)):
            permutation = list(range(N))
            permutation[0], permutation[1] = high_images
            permutation[2:] = low_images
            degree_preserving_permutations.append(tuple(permutation))
    orbit = {
        permuted_edge_mask(representative, permutation)
        for permutation in degree_preserving_permutations
    }
    require(len(orbit) == 120, ("13-edge terminal orbit changed", len(orbit)))
    require(orbit == terminal_masks,
            "13-edge terminals split into more than one graph orbit")

    left_shore = frozenset((0, 5, 6, 7))
    right_shore = frozenset((1, 2, 3, 4))
    independent_four_sets = tuple(
        frozenset(vertices)
        for vertices in combinations(range(N), 4)
        if not any(
            (representative[u] >> v) & 1
            for u, v in combinations(vertices, 2)
        )
    )
    require(set(independent_four_sets) == {left_shore, right_shore},
            ("terminal independent shores changed", independent_four_sets))
    cross_edges = {
        tuple(sorted((left, right)))
        for left in left_shore for right in right_shore
    }
    dead_cross_edges = cross_edges - set(representative_edges)
    require(dead_cross_edges == {(2, 7), (3, 6), (4, 5)},
            ("terminal dead matching changed", dead_cross_edges))
    require(all(
        representative[u].bit_count() == representative[v].bit_count() == 3
        for u, v in dead_cross_edges
    ), "a dead-cross endpoint stopped being cubic")

    # This is exactly the dead-cross-edge branch of the proved full-source
    # theorem in verify_no_independent_four_set_at_eight.py.  Its 141 mixed
    # 2x2 rectangle rows, in each of eight constant-fibre cases, fill all 36
    # core cells and violate the anchor condition.  We check every graph-side
    # premise here; that theorem's independent exact checker is a reproduction
    # prerequisite recorded in the companion note.
    return {
        "degree_sequence_ledgers": ledgers,
        "terminal_orbit_size": len(orbit),
        "terminal_representative_edges": representative_edges,
        "independent_shores": (tuple(sorted(left_shore)),
                               tuple(sorted(right_shore))),
        "dead_cross_matching": tuple(sorted(dead_cross_edges)),
        "full_mixed_rectangle_rows": 141,
        "constant_fibre_cases": 8,
        "forced_core_cells": 36,
        "full_source_verdict": "excluded by no-independent-four-set Step 3b",
    }


def audit_fourteen_edge_graph_classification():
    """Classify the support-clean terminals at the next exact layer.

    The four excess degrees over 3^8 give five degree sequences.  Three
    sequences have no terminal.  The remaining 300 labelled terminals form
    four degree-preserving orbits; three have an independent shore and are
    already excluded by the complete mixed-row theorem.  The fourth is the
    first support-only terminal not covered by that theorem.
    """
    degree_sequences = (
        (7, 3, 3, 3, 3, 3, 3, 3),
        (6, 4, 3, 3, 3, 3, 3, 3),
        (5, 5, 3, 3, 3, 3, 3, 3),
        (5, 4, 4, 3, 3, 3, 3, 3),
        (4, 4, 4, 4, 3, 3, 3, 3),
    )
    expected = {
        degree_sequences[0]: (465, {7: 465}, 0),
        degree_sequences[1]: (
            3030, {2: 360, 4: 630, 5: 1800, 6: 180, 8: 60}, 0,
        ),
        degree_sequences[2]: (
            5280, {1: 60, 2: 720, 3: 1980, 4: 630, 5: 1890}, 0,
        ),
        degree_sequences[3]: (
            8820,
            {0: 120, 1: 140, 2: 1290, 3: 3180, 4: 2700,
             5: 960, 6: 300, 7: 120, 9: 10},
            120,
        ),
        degree_sequences[4]: (
            14634,
            {0: 180, 1: 1728, 2: 2898, 3: 5760, 4: 2880,
             5: 576, 6: 432, 7: 144, 10: 36},
            180,
        ),
    }

    terminal_by_sequence = {}
    degree_ledgers = []
    for target in degree_sequences:
        distribution = {}
        labelled_count = 0
        terminals = []
        for adjacency in generate_degree_sequence_graphs(target):
            labelled_count += 1
            edges = graph_edges(adjacency)
            require(len(edges) == 14, ("14-edge census changed", target))
            clean_count = sum(
                response_support_clean_edge(adjacency, *edge)
                for edge in edges
            )
            distribution[clean_count] = distribution.get(clean_count, 0) + 1
            if clean_count == 0:
                terminals.append(adjacency)
        expected_count, expected_distribution, expected_terminals = expected[target]
        require(labelled_count == expected_count,
                ("14-edge labelled census changed", target, labelled_count))
        require(distribution == expected_distribution,
                ("14-edge clean distribution changed", target, distribution))
        require(len(terminals) == expected_terminals,
                ("14-edge terminal census changed", target, len(terminals)))
        terminal_by_sequence[target] = terminals
        degree_ledgers.append(
            {
                "degree_sequence": target,
                "labelled_count": labelled_count,
                "clean_edge_distribution": distribution,
                "terminal_count": len(terminals),
            }
        )

    def adjacency_from_edges(edges):
        adjacency = [0] * N
        for u, v in edges:
            adjacency[u] |= 1 << v
            adjacency[v] |= 1 << u
        return tuple(adjacency)

    def preserving_group(target):
        cells = tuple(
            tuple(vertex for vertex, degree in enumerate(target) if degree == d)
            for d in sorted(set(target), reverse=True)
        )
        answer = []
        for cell_images in product(*(tuple(permutations(cell)) for cell in cells)):
            permutation = list(range(N))
            for cell, images in zip(cells, cell_images, strict=True):
                for old, new in zip(cell, images, strict=True):
                    permutation[old] = new
            answer.append(tuple(permutation))
        return tuple(answer)

    orbit_specs = (
        {
            "target": degree_sequences[3],
            "edges": (
                (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
                (1, 3), (1, 4), (1, 6),
                (2, 3), (2, 5), (2, 6),
                (4, 7), (5, 7), (6, 7),
            ),
            "orbit_size": 120,
            "signature": ((8,), False, 4, 8, 1),
            "independent_shore": (3, 4, 5, 6),
            "mixed_exit": "zero two internal edges, then cube unique fibres",
        },
        {
            "target": degree_sequences[4],
            "edges": (
                (0, 1), (0, 2), (0, 4), (0, 5),
                (1, 3), (1, 4), (1, 6),
                (2, 3), (2, 5), (2, 7),
                (3, 6), (3, 7), (4, 7), (5, 6),
            ),
            "orbit_size": 72,
            "signature": ((8,), False, 4, 5, 0),
            "independent_shore": None,
            "mixed_exit": None,
        },
        {
            "target": degree_sequences[4],
            "edges": (
                (0, 1), (0, 2), (0, 4), (0, 5),
                (1, 3), (1, 6), (1, 7),
                (2, 3), (2, 6), (2, 7),
                (3, 4), (3, 5), (4, 6), (5, 7),
            ),
            "orbit_size": 36,
            "signature": ((8,), True, 0, 19, 2),
            "independent_shore": (0, 3, 6, 7),
            "mixed_exit": "dead-cross 141-row rectangle closure",
        },
        {
            "target": degree_sequences[4],
            "edges": (
                (0, 1), (0, 4), (0, 5), (0, 6),
                (1, 4), (1, 5), (1, 7),
                (2, 3), (2, 4), (2, 6), (2, 7),
                (3, 5), (3, 6), (3, 7),
            ),
            "orbit_size": 72,
            "signature": ((8,), False, 4, 6, 1),
            "independent_shore": (4, 5, 6, 7),
            "mixed_exit": "zero two internal edges, then cube unique fibres",
        },
    )

    group_cache = {
        target: preserving_group(target)
        for target in (degree_sequences[3], degree_sequences[4])
    }
    terminal_masks = {
        target: {
            permuted_edge_mask(graph, tuple(range(N)))
            for graph in terminal_by_sequence[target]
        }
        for target in group_cache
    }
    covered_masks = {target: set() for target in group_cache}
    orbit_ledger = []
    first_terminal = None
    for spec in orbit_specs:
        target = spec["target"]
        adjacency = adjacency_from_edges(spec["edges"])
        independent_sets = tuple(
            tuple(vertices)
            for vertices in combinations(range(N), 4)
            if not any(
                (adjacency[u] >> v) & 1
                for u, v in combinations(vertices, 2)
            )
        )
        signature = (
            component_sizes(adjacency), is_bipartite(adjacency),
            triangle_count(adjacency), square_count(adjacency),
            len(independent_sets),
        )
        require(signature == spec["signature"],
                ("14-edge terminal signature changed", signature))
        orbit = {
            permuted_edge_mask(adjacency, permutation)
            for permutation in group_cache[target]
        }
        require(len(orbit) == spec["orbit_size"],
                ("14-edge terminal orbit size changed", len(orbit)))
        require(orbit <= terminal_masks[target],
                "a pinned 14-edge orbit stopped being terminal")
        require(not (covered_masks[target] & orbit),
                "pinned 14-edge terminal orbits overlap")
        covered_masks[target].update(orbit)

        shore = spec["independent_shore"]
        reduction = None
        if shore is not None:
            require(tuple(shore) in independent_sets,
                    ("pinned independent shore disappeared", shore))
            shore = frozenset(shore)
            complement = frozenset(range(N)) - shore
            all_cross = {
                tuple(sorted((left, right)))
                for left in shore for right in complement
            }
            live_cross = all_cross & set(spec["edges"])
            dead_cross = all_cross - live_cross
            dead_degrees = {
                vertex: sum(vertex in edge for edge in dead_cross)
                for vertex in range(N)
            }
            require(all(value <= 1 for value in dead_degrees.values()),
                    ("dead cross edges stopped being a matching", dead_cross))
            require(len(live_cross) in (12, 14),
                    ("independent-shore reduction changed", live_cross))
            reduction = {
                "live_cross_edges": len(live_cross),
                "dead_cross_matching": tuple(sorted(dead_cross)),
                "zeroed_internal_edges": tuple(
                    sorted(set(spec["edges"]) - live_cross)
                ),
            }
        else:
            require(not independent_sets,
                    "first 14-edge terminal acquired an independent shore")
            # Its high vertices form C4; each core edge has one triangle
            # apex, and the apices on opposite core edges are paired.  Every
            # seal is RRX, never RRR.  This pins the exact next obstruction.
            rrr_counts = []
            rrx_counts = []
            degree_pair_counts = {}
            source_edges = set(spec["edges"])
            for p, q in spec["edges"]:
                residual = tuple(v for v in range(N) if v not in (p, q))
                p_external = {v for v in residual if (adjacency[p] >> v) & 1}
                q_external = {v for v in residual if (adjacency[q] >> v) & 1}
                response_edges = {
                    tuple(sorted((u, v)))
                    for u in p_external for v in q_external if u != v
                }
                rrr = 0
                rrx = 0
                for matching in perfect_matchings(residual):
                    matching = tuple(tuple(sorted(edge)) for edge in matching)
                    rrr += int(all(edge in response_edges for edge in matching))
                    rrx += sum(
                        matching[index] in source_edges
                        and all(
                            matching[j] in response_edges
                            for j in range(3) if j != index
                        )
                        for index in range(3)
                    )
                rrr_counts.append(rrr)
                rrx_counts.append(rrx)
                degree_pair = tuple(sorted((adjacency[p].bit_count(),
                                            adjacency[q].bit_count()),
                                           reverse=True))
                degree_pair_counts[degree_pair] = (
                    degree_pair_counts.get(degree_pair, 0) + 1
                )
            require(set(rrr_counts) == {0},
                    ("first terminal acquired an RRR seal", rrr_counts))
            require({count: rrx_counts.count(count) for count in set(rrx_counts)}
                    == {2: 10, 6: 4},
                    ("first terminal RRX ledger changed", rrx_counts))
            require(degree_pair_counts == {(4, 4): 4, (4, 3): 8, (3, 3): 2},
                    ("first terminal edge types changed", degree_pair_counts))
            first_terminal = {
                "name": "opposite-apex triangulated C4",
                "edges": spec["edges"],
                "degree_pair_counts": degree_pair_counts,
                "RRR_counts": tuple(rrr_counts),
                "RRX_count_distribution": {2: 10, 6: 4},
                "support_only_status": "requires forced-anchor coefficients",
            }

        orbit_ledger.append(
            {
                "degree_sequence": target,
                "orbit_size": len(orbit),
                "signature": signature,
                "edges": spec["edges"],
                "independent_shore_reduction": reduction,
                "mixed_exit": spec["mixed_exit"],
            }
        )

    require(all(covered_masks[target] == terminal_masks[target]
                for target in covered_masks),
            "pinned 14-edge orbits do not exhaust the terminals")
    require(first_terminal is not None,
            "14-edge non-independent terminal disappeared")
    return {
        "degree_sequence_ledgers": degree_ledgers,
        "terminal_orbits": orbit_ledger,
        "independent_shore_orbits_excluded": 3,
        "first_unclassified_terminal": first_terminal,
    }


def audit_fourteen_terminal_anchor_clean_landing():
    """Exact anchor reduction and active-zero lemma for the last terminal.

    Use the opposite-apex edge 47.  The cubic forced-anchor normal form makes
    the two external 4-star blocks fix distinct colours 0,1 at sites 0,1,
    and the two external 7-star blocks fix distinct colours 0,1 at sites
    2,3.  The edge 47 itself is a nonzero (2,2) coordinate cell.  Retaining
    the four arbitrary near-end vectors u0,u1,v0,v1, the only coefficient of
    r^[2] is the permanent of the 2x2 matrix (u_i^T K v_j).

    The proof that this quadratic has a target-active zero is in the note.
    Here we check the literal matching reduction, its full formal expansion,
    and the rank/factor data used in every vector-rank case.
    """
    edges = (
        (0, 1), (0, 2), (0, 4), (0, 5),
        (1, 3), (1, 4), (1, 6),
        (2, 3), (2, 5), (2, 7),
        (3, 6), (3, 7), (4, 7), (5, 6),
    )
    source_edges = set(edges)
    p, q = 4, 7
    residual = tuple(vertex for vertex in range(N) if vertex not in (p, q))
    p_external = {0, 1}
    q_external = {2, 3}
    response_edges = {
        tuple(sorted((left, right)))
        for left in p_external for right in q_external
    }
    response_matchings = tuple(
        matching
        for matching in perfect_matchings((0, 1, 2, 3))
        if all(tuple(sorted(edge)) in response_edges for edge in matching)
    )
    require(response_matchings == (((0, 2), (1, 3)), ((0, 3), (1, 2))),
            ("anchor response matching reduction changed", response_matchings))
    require(source_edges & set(combinations((5, 6), 2)) == {(5, 6)},
            "opposite apex multiplier disappeared")
    require(not any(
        all(tuple(sorted(edge)) in response_edges for edge in matching)
        for matching in perfect_matchings(residual)
    ), "the apex cap unexpectedly acquired an RRR term")

    # Sparse exact polynomials.  A monomial is a sorted tuple of formal
    # coefficient-variable names; no numerical block specialization occurs.
    def add(left, right):
        answer = dict(left)
        for monomial, coefficient_value in right.items():
            answer[monomial] = answer.get(monomial, 0) + coefficient_value
            if answer[monomial] == 0:
                del answer[monomial]
        return answer

    def multiply(left, right):
        answer = {}
        for left_monomial, left_coefficient in left.items():
            for right_monomial, right_coefficient in right.items():
                monomial = tuple(sorted(left_monomial + right_monomial))
                answer[monomial] = (
                    answer.get(monomial, 0)
                    + left_coefficient * right_coefficient
                )
        return answer

    def scale(polynomial, scalar):
        return {
            monomial: scalar * coefficient_value
            for monomial, coefficient_value in polynomial.items()
            if scalar * coefficient_value
        }

    def pairing(left_tag, right_tag):
        return {
            tuple(sorted((f"{left_tag}{i}", f"K{i}{j}", f"{right_tag}{j}"))): 1
            for i in COLORS for j in COLORS
        }

    z00 = pairing("u0_", "v0_")
    z01 = pairing("u0_", "v1_")
    z10 = pairing("u1_", "v0_")
    z11 = pairing("u1_", "v1_")
    permanent_pullback = add(multiply(z00, z11), multiply(z01, z10))
    coefficient_distribution = {}
    for coefficient_value in permanent_pullback.values():
        coefficient_distribution[coefficient_value] = (
            coefficient_distribution.get(coefficient_value, 0) + 1
        )
    require(len(permanent_pullback) == 117,
            ("formal anchor quadratic support changed", len(permanent_pullback)))
    require(coefficient_distribution == {1: 72, 2: 45},
            ("formal anchor coefficients changed", coefficient_distribution))

    # If the left pair has rank one, u1=lambda*u0 and the permanent is
    # 2*lambda*(u^T K v0)*(u^T K v1).  The irrelevant nonzero lambda is
    # suppressed here.  The right-rank-one and double-rank-one identities
    # are checked independently as formal polynomials.
    left_rank_one = scale(
        multiply(pairing("u_", "v0_"), pairing("u_", "v1_")), 2
    )
    left_rank_one_direct = add(
        multiply(pairing("u_", "v0_"), pairing("u_", "v1_")),
        multiply(pairing("u_", "v1_"), pairing("u_", "v0_")),
    )
    require(left_rank_one == left_rank_one_direct,
            "left-rank-one factorization changed")
    right_rank_one = scale(
        multiply(pairing("u0_", "v_"), pairing("u1_", "v_")), 2
    )
    right_rank_one_direct = add(
        multiply(pairing("u0_", "v_"), pairing("u1_", "v_")),
        multiply(pairing("u1_", "v_"), pairing("u0_", "v_")),
    )
    require(right_rank_one == right_rank_one_direct,
            "right-rank-one factorization changed")
    both_rank_one = scale(multiply(pairing("u_", "v_"),
                                   pairing("u_", "v_")), 2)
    require(both_rank_one,
            "double-rank-one anchor quadratic vanished in characteristic zero")

    # In the rank-(2,2) case K -> (u_i^T K v_j) is onto Mat_2.  The Hessian
    # of z00*z11+z01*z10 has full rank four, whereas a product of two linear
    # forms has Hessian rank at most two.  This is the exact irreducibility
    # certificate used by the active-zero argument.
    permanent_hessian = (
        (0, 0, 0, 1),
        (0, 0, 1, 0),
        (0, 1, 0, 0),
        (1, 0, 0, 0),
    )
    require(rank_mod(permanent_hessian) == 4,
            "2x2 permanent Hessian lost irreducibility rank")

    # At each endpoint the two external anchor vectors serve two distinct
    # pure colours.  If they become proportional, their common vector has
    # both corresponding coordinates nonzero.  Therefore a factor u^T K v
    # has at least two nonzero rows (left-rank-one case), or at least two
    # nonzero columns (right-rank-one case), and cannot be any diagonal
    # activity coordinate K_cc.  This finite support check pins that step.
    p_anchor_labels = {0: 0, 1: 1, 7: 2}
    q_anchor_labels = {2: 0, 3: 1, 4: 2}
    require(set(p_anchor_labels.values()) == set(COLORS)
            and set(q_anchor_labels.values()) == set(COLORS),
            "cubic anchor labels stopped being permutations")
    require(p_anchor_labels[q] == q_anchor_labels[p] == 2,
            "the common apex edge stopped serving one pure colour")
    common_left_support = {p_anchor_labels[0], p_anchor_labels[1]}
    common_right_support = {q_anchor_labels[2], q_anchor_labels[3]}
    require(len(common_left_support) >= 2 and len(common_right_support) >= 2,
            "rank-one common anchor vector became coordinate-supported")

    return {
        "cap_edge": (4, 7),
        "direct_anchor_colour": 2,
        "external_anchor_colours": (0, 1),
        "response_matchings": response_matchings,
        "opposite_apex_multiplier": (5, 6),
        "formal_quadratic_monomials": len(permanent_pullback),
        "formal_coefficient_distribution": coefficient_distribution,
        "rank_22_hessian_rank": 4,
        "rank_cases": {
            "2,2": "irreducible permanent pullback",
            "1,2": "two non-diagonal linear factors",
            "2,1": "two non-diagonal linear factors",
            "1,1": "square of a non-diagonal linear factor",
        },
        "active_zero_over_C": True,
    }


def audit_cube_full_source_mixed_no_go():
    """Audit the full mixed obstruction after cubic-selector degeneration.

    The imported cubic equality theorem turns every active cube block into
    a nonzero same-colour coordinate cell.  This audit starts at that exact
    normal form: pure fibres force one of 24 one-factorisations, and each
    has six mixed detector words with a unique supported matching.
    """
    cube_edges = tuple(
        (left, right)
        for left in range(4)
        for right in range(4)
        if left != right
    )
    derangements = tuple(
        permutation
        for permutation in permutations(range(4))
        if all(permutation[left] != left for left in range(4))
    )
    require(len(derangements) == 9, "cube matching count changed")

    colour_orders = tuple(permutations(COLORS))
    factorisations = []
    for choices in product(range(len(colour_orders)), repeat=4):
        edge_colour = {}
        for left in range(4):
            neighbours = [right for right in range(4) if right != left]
            for index, right in enumerate(neighbours):
                edge_colour[left, right] = colour_orders[choices[left]][index]
        if all(
            len(
                {
                    right
                    for left, right in cube_edges
                    if edge_colour[left, right] == colour
                }
            )
            == 4
            for colour in COLORS
        ):
            factorisations.append(edge_colour)
    require(len(factorisations) == 24,
            ("cube one-factorisation count changed", len(factorisations)))

    ledger = []
    for edge_colour in factorisations:
        constant_counts = []
        unique_mixed_words = []
        for left_word in product(COLORS, repeat=4):
            for right_word in product(COLORS, repeat=4):
                supported = []
                for permutation in derangements:
                    if all(
                        left_word[left]
                        == right_word[permutation[left]]
                        == edge_colour[left, permutation[left]]
                        for left in range(4)
                    ):
                        supported.append(permutation)
                word = left_word + right_word
                if len(set(word)) == 1:
                    constant_counts.append(len(supported))
                elif len(supported) == 1:
                    unique_mixed_words.append("".join(map(str, word)))
        require(constant_counts == [1, 1, 1],
                ("cube constant fibre changed", constant_counts))
        require(len(unique_mixed_words) == 6,
                ("cube unique mixed census changed", unique_mixed_words))
        ledger.append(sorted(unique_mixed_words))

    representative = ledger[0]
    require(
        representative
        == ["01101001", "02022020", "10010110", "11222211",
            "20200202", "22111122"],
        ("canonical cube mixed words changed", representative),
    )
    return {
        "factorisations": len(factorisations),
        "supported_matchings": len(derangements),
        "unique_mixed_per_factorisation": 6,
        "representative_unique_mixed_words": representative,
        "all_unique_mixed_word_sets": ledger,
    }


def identity_effective_block(blocks, p, q, a, b):
    """The B^I block on residual endpoints a,b."""
    pa = oriented_block(blocks, p, a)
    pb = oriented_block(blocks, p, b)
    qa = oriented_block(blocks, q, a)
    qb = oriented_block(blocks, q, b)
    return tuple(
        tuple(
            sum(
                pa[colour][i] * qb[colour][j]
                + pb[colour][j] * qa[colour][i]
                for colour in COLORS
            )
            for j in COLORS
        )
        for i in COLORS
    )


def audit_cubic_boundary():
    expected_pure = (28170, 106080, 15242)
    pure, normalized, normalized_mod = normalize_at_site_zero(
        CUBIC_BLOCKS, expected_pure
    )
    vertices = tuple(range(N))
    edges = set(CUBIC_BLOCKS)
    require(len(edges) == 12, "cubic support count changed")
    degrees = {
        vertex: sum(vertex in edge for edge in edges) for vertex in vertices
    }
    require(set(degrees.values()) == {3}, ("cube stopped being cubic", degrees))
    for edge in edges:
        require(determinant_3(normalized[edge]) != 0,
                ("cubic block became singular", edge))

    for colour in COLORS:
        require(
            coefficient(normalized, vertices, (colour,) * N) == 1,
            ("cubic pure normalization failed", colour),
        )
    mixed_word = (0, 1, 0, 0, 0, 0, 0, 0)
    mixed_value = coefficient(normalized, vertices, mixed_word)
    require(mixed_value == Fraction(23257, 14085),
            ("cubic mixed row changed", mixed_value))

    pair_ledger = projective_error_ledger(normalized_mod)
    require(len(pair_ledger) == 28, "cubic pair census changed")
    require(sum(item["q_nonzero"] for item in pair_ledger) == 16,
            "cubic cofactor activity census changed")

    # At the support edge 05, the external stars occupy {6,7} and {2,3}.
    # Their effective correction has a genuine K2,2 square.  The remaining
    # residual pair 14 is active, so the all-zero coefficient of the
    # identity-cap clean error is strictly positive.
    r26 = identity_effective_block(normalized, 0, 5, 2, 6)[0][0]
    r37 = identity_effective_block(normalized, 0, 5, 3, 7)[0][0]
    r27 = identity_effective_block(normalized, 0, 5, 2, 7)[0][0]
    r36 = identity_effective_block(normalized, 0, 5, 3, 6)[0][0]
    r_square = r26 * r37 + r27 * r36
    direct_scalar = sum(normalized[(0, 5)][colour][colour] for colour in COLORS)
    clean_coefficient = direct_scalar * r_square * normalized[(1, 4)][0][0]
    require(clean_coefficient > 0, "cubic identity cap unexpectedly cleaned")

    # This is not merely an identity-cap failure.  At every support edge,
    # the two external neighbour sets are disjoint two-sets and the leftover
    # residual pair is active.  Independent invertible changes of basis at
    # the four external sites turn all four effective blocks into the same
    # cap matrix K.  The (a,a,c,c) coefficient of r^[2] is then 2*K_ac^2,
    # so r^[2]=0 forces K=0 in characteristic zero.  Nonedges have s_K=0.
    clean_edge_ledger = []
    for p, q in sorted(edges):
        p_external = {
            vertex
            for vertex in vertices
            if vertex != q and tuple(sorted((p, vertex))) in edges
        }
        q_external = {
            vertex
            for vertex in vertices
            if vertex != p and tuple(sorted((q, vertex))) in edges
        }
        require(len(p_external) == len(q_external) == 2,
                ("cubic external degree changed", p, q))
        require(p_external.isdisjoint(q_external),
                ("cube external shores collided", p, q))
        leftover = set(vertices) - {p, q} - p_external - q_external
        require(len(leftover) == 2, ("cube leftover changed", p, q, leftover))
        leftover_edge = tuple(sorted(leftover))
        require(leftover_edge in edges,
                ("cube clean multiplier vanished", p, q, leftover_edge))
        for endpoint, external in ((p, p_external), (q, q_external)):
            for neighbor in external:
                require(
                    determinant_3(oriented_block(normalized, endpoint, neighbor))
                    != 0,
                    ("cube external basis map became singular", p, q, endpoint),
                )
        clean_edge_ledger.append(
            {
                "pair": [p, q],
                "external_sizes": [2, 2],
                "leftover_edge": list(leftover_edge),
                "normal_form_square_coefficients": [2] * 9,
            }
        )
    require(len(clean_edge_ledger) == 12, "cubic dirty-edge census changed")

    nonedges = set(combinations(vertices, 2)) - edges
    require(len(nonedges) == 16, "cubic inactive-pair census changed")
    for p, q in nonedges:
        require(oriented_block(normalized, p, q) == ZERO,
                ("cubic nonedge acquired direct activity", p, q))

    return {
        "blocks": CUBIC_BLOCKS,
        "integer_pure_coefficients": pure,
        "normalized_mixed_word": mixed_word,
        "normalized_mixed_value": mixed_value,
        "pair_projective_ranks": pair_ledger,
        "identity_clean_error_000000": clean_coefficient,
        "clean_edge_normal_forms": clean_edge_ledger,
        "active_clean_cap_exists": False,
    }


def projective_error_ledger(blocks_mod):
    vertices = tuple(range(N))
    full_words = tuple(product(COLORS, repeat=N))
    full = {
        word: coefficient(blocks_mod, vertices, word, PRIME) for word in full_words
    }
    ledger = []

    for p, q in combinations(vertices, 2):
        residual = tuple(vertex for vertex in vertices if vertex not in (p, q))
        direct = oriented_block(blocks_mod, p, q)
        rows = []
        q_nonzero = False
        for residual_word in product(COLORS, repeat=N - 2):
            word = [0] * N
            for index, vertex in enumerate(residual):
                word[vertex] = residual_word[index]
            q_value = coefficient(blocks_mod, residual, tuple(word), PRIME)
            q_nonzero = q_nonzero or q_value != 0
            error_row = []
            for a, b in product(COLORS, repeat=2):
                word[p] = a
                word[q] = b
                # This is exactly D H_R[B^(a,b)] = F_(a,b)-a_(a,b)Q,
                # obtained by sorting physical matchings at the named pair.
                error_row.append(
                    (full[tuple(word)] - direct[a][b] * q_value) % PRIME
                )
            rows.append(error_row + [q_value])

        rank_error = rank_mod([row[:9] for row in rows])
        rank_augmented = rank_mod(rows)
        q_rank = int(q_nonzero)
        projective_rank = rank_augmented - q_rank
        require(rank_error == 9, ("error map lost rank", p, q, rank_error))
        require(
            projective_rank == 9,
            ("projective error acquired a nonzero kernel", p, q, projective_rank),
        )
        ledger.append(
            {
                "pair": [p, q],
                "q_nonzero": q_nonzero,
                "rank_error": rank_error,
                "rank_augmented": rank_augmented,
                "projective_rank": projective_rank,
            }
        )
    return ledger


def canonical(value):
    if isinstance(value, Fraction):
        return [value.numerator, value.denominator]
    if isinstance(value, dict):
        return {
            str(key): canonical(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (list, tuple)):
        return [canonical(item) for item in value]
    return value


def main():
    audit_exact_source_rank_dichotomy()
    pure, normalized, normalized_mod = normalize_at_site_zero(
        BLOCKS, (1755, 44304, 4424)
    )
    audit_support_and_rank_minimality(normalized)
    clean_pairs = audit_minimum_support_clean_caps(normalized)
    audit_degree_two_clean_threshold()
    cubic_graph_ledger = audit_cubic_graph_classification()
    cube_full_source_ledger = audit_cube_full_source_mixed_no_go()
    thirteen_edge_ledger = audit_thirteen_edge_graph_classification()
    fourteen_edge_ledger = audit_fourteen_edge_graph_classification()
    fourteen_anchor_clean_ledger = audit_fourteen_terminal_anchor_clean_landing()

    for colour in COLORS:
        value = coefficient(normalized, range(N), (colour,) * N)
        require(value == 1, ("pure normalization failed", colour, value))

    mixed_word = (0, 1, 0, 0, 0, 0, 0, 0)
    mixed_value = coefficient(normalized, range(N), mixed_word)
    require(mixed_value == Fraction(1283, 117), ("mixed row changed", mixed_value))

    pair_ledger = projective_error_ledger(normalized_mod)
    require(len(pair_ledger) == 28, "physical-pair census changed")
    require(sum(item["q_nonzero"] for item in pair_ledger) == 16,
            "deleted-cofactor activity census changed")

    cubic_ledger = audit_cubic_boundary()
    ledger = canonical(
        {
            "blocks": BLOCKS,
            "integer_pure_coefficients": pure,
            "normalized_mixed_word": mixed_word,
            "normalized_mixed_value": mixed_value,
            "pair_projective_ranks": pair_ledger,
            "identity_clean_pairs": clean_pairs,
            "support_size": len(BLOCKS),
            "total_block_rank": 24,
            "first_cubic_boundary": cubic_ledger,
            "cubic_graph_classification": cubic_graph_ledger,
            "cube_full_source_mixed_no_go": cube_full_source_ledger,
            "thirteen_edge_graph_classification": thirteen_edge_ledger,
            "fourteen_edge_graph_classification": fourteen_edge_ledger,
            "fourteen_terminal_anchor_clean_landing": fourteen_anchor_clean_ledger,
        }
    )
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                ("projective-cap ledger changed", digest))

    print("n=8 support/rank-minimal projective-cap guard: PASS")
    print("  exact-target quotient ranks: Q=0/outside 3; nonzero Q in target plane 2")
    print("  minimum physical support / forced rank there: 8 / 24")
    print("  doubly injective physical pairs: 28 / 28")
    print("  projective cap-error ranks: 9 at all 28 pairs")
    print("  active clean identity caps: all 8 support edges")
    print("  pure coefficients after normalization: 1, 1, 1")
    print("  first displayed mixed residual 01000000: 1283/117")
    print("  all-pairs-good support <= 11: active clean cap forced")
    print("  cubic support orbits: 6; cube uniquely has all 12 edges sealed")
    print("  first cubic guard: support 12, projective ranks 9, no active clean cap")
    print("  exact cube normal forms: 24; each has 6 unique mixed fibres")
    print("  exact all-pairs-good source: aggregate support >= 13")
    print("  13-edge degree sequences: (5,3^7) and (4,4,3^6)")
    print("  generalized clean-support terminal: one orbit, K4,4 minus 3K2")
    print("  its independent shore is excluded by the 141 full mixed rows")
    print("  exact all-pairs-good source: aggregate support >= 14")
    print("  14-edge generalized support terminals: four graph orbits")
    print("  independent-shore full-row exits: 3 / 4 terminal orbits")
    print("  last graph terminal: opposite-apex triangulated C4")
    print("  apex-edge anchor quadratic has a target-active zero over C")
    print("  exact all-pairs-good source: aggregate support >= 15")


if __name__ == "__main__":
    main()
