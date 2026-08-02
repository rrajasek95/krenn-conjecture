#!/usr/bin/env python3
"""Close the 1I+1R+4Z generic-kernel potential/support boundary.

Site 0 is invertible, site 1 is nonzero rank one, and sites 2,3,4,5
are zero.  Signed partitions enumerate 675 labelled support envelopes, or
85 modulo S4 on the zero sites.  Every quotient except one has at most 11
active tangent edges and rank at most 44 directly.

The remaining K3,3 envelope has the three tangent edges in one shore
inactive.  Their twelve coordinate directions and the five universal
gauges have a one-dimensional intersection, giving sixteen kernel
directions and again rank at most 44.  Polynomial specialization extends
the dense-locus gauge bound to every packet in that envelope.

Research evidence only.  Standard library exact arithmetic; checks remain
live under python -O and python -I -S.
"""

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, permutations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
PARTITIONS = run_path(str(
    HERE / "verify_level_two_two_invertible_same_column_potential_boundary.py"
))
LITERAL = run_path(str(
    HERE / "verify_level_two_three_invertible_r2_guard.py"
))

SITES = tuple(range(6))
COLOURS = (0, 1)
CORE = (0, 1)
ZERO = (2, 3, 4, 5)
EDGES = tuple(combinations(SITES, 2))
CELLS = tuple(
    (left, right, row, column)
    for left, right in EDGES
    for row, column in product(COLOURS, repeat=2)
)
CORE_EDGES = frozenset(((0, 1),))
ZERO_MATRIX = ((Q(0), Q(0)), (Q(0), Q(0)))


def edge(left, right):
    return tuple(sorted((left, right)))


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


COMPLEMENT_MATCHINGS = {
    pair: perfect_matchings(site for site in SITES if site not in pair)
    for pair in EDGES
}


def admissible(potential):
    return not PARTITIONS["zero_sum"](potential[0], potential[1])


def support_graph(potential):
    zero_sum = PARTITIONS["zero_sum"]
    optional = {
        pair for pair in EDGES
        if pair not in CORE_EDGES
        and zero_sum(potential[pair[0]], potential[pair[1]])
    }
    return frozenset(CORE_EDGES | optional)


def active_tangent_edges(support):
    return frozenset(
        pair for pair in EDGES
        if any(all(edge(*matching_edge) in support
                   for matching_edge in matching)
               for matching in COMPLEMENT_MATCHINGS[pair])
    )


def relabellings():
    answer = []
    for zero_order in permutations(ZERO):
        mapping = list(SITES)
        for old, new in zip(ZERO, zero_order):
            mapping[old] = new
        answer.append(tuple(mapping))
    require(len(answer) == 24, "S4 relabelling count changed")
    return tuple(answer)


RELABELINGS = relabellings()


def canonical_support(support):
    return min(
        tuple(sorted(edge(mapping[left], mapping[right])
                     for left, right in support))
        for mapping in RELABELINGS
    )


def optional_part(support):
    return frozenset(support - CORE_EDGES)


def maximal_type(support):
    optional = optional_part(support)
    core_neighbours = {
        zero: frozenset(core for core in CORE
                        if edge(core, zero) in optional)
        for zero in ZERO
    }
    positive = tuple(
        zero for zero in ZERO if not core_neighbours[zero]
    )
    negative = tuple(
        zero for zero in ZERO
        if core_neighbours[zero] == frozenset(CORE)
    )
    if len(positive) != 1 or len(negative) != 3:
        return None
    positive_site = positive[0]
    expected_zero_edges = frozenset(
        edge(positive_site, site) for site in negative
    )
    actual_zero_edges = frozenset(
        pair for pair in combinations(ZERO, 2) if pair in optional
    )
    if actual_zero_edges == expected_zero_edges:
        return "split K33 zero boundary"
    return None


def audit_potential_support_census():
    potentials = PARTITIONS["signed_partitions"](6)
    require(len(potentials) == 4088,
            ("signed-partition census changed", len(potentials)))
    admissible_potentials = tuple(filter(admissible, potentials))
    require(len(admissible_potentials) == 3440,
            ("admissible potential census changed",
             len(admissible_potentials)))

    representatives = {}
    for potential in admissible_potentials:
        representatives.setdefault(support_graph(potential), potential)
    require(len(representatives) == 675,
            ("labelled support census changed", len(representatives)))

    labelled_histogram = Counter(
        len(active_tangent_edges(support)) for support in representatives
    )
    require(labelled_histogram == Counter({
        0: 35, 1: 72, 2: 96, 3: 131, 4: 98, 5: 87, 6: 59,
        7: 49, 8: 24, 9: 4, 10: 14, 11: 2, 12: 4,
    }), ("labelled active-edge histogram changed", labelled_histogram))

    quotient = {}
    for support, potential in representatives.items():
        quotient.setdefault(canonical_support(support), (support, potential))
    require(len(quotient) == 85,
            ("quotient support census changed", len(quotient)))
    quotient_histogram = Counter(
        len(active_tangent_edges(support))
        for support, _ in quotient.values()
    )
    require(quotient_histogram == Counter({
        0: 10, 1: 8, 2: 8, 3: 16, 4: 10, 5: 9, 6: 8,
        7: 7, 8: 2, 9: 1, 10: 3, 11: 2, 12: 1,
    }), ("quotient active-edge histogram changed", quotient_histogram))

    labelled_maximal = Counter(
        maximal_type(support) for support in representatives
        if len(active_tangent_edges(support)) == 12
    )
    require(labelled_maximal == Counter({"split K33 zero boundary": 4}),
            ("labelled maximal type changed", labelled_maximal))
    quotient_maximal = Counter(
        maximal_type(support) for support, _ in quotient.values()
        if len(active_tangent_edges(support)) == 12
    )
    require(quotient_maximal == Counter({"split K33 zero boundary": 1}),
            ("quotient maximal type changed", quotient_maximal))

    direct_closed = sum(
        count for active, count in quotient_histogram.items() if active <= 11
    )
    require(direct_closed == 84,
            ("directly closed quotient count changed", direct_closed))
    return {
        "signed_partitions": len(potentials),
        "admissible_potentials": len(admissible_potentials),
        "labelled_supports": len(representatives),
        "quotient_supports": len(quotient),
        "labelled_histogram": dict(sorted(labelled_histogram.items())),
        "quotient_histogram": dict(sorted(quotient_histogram.items())),
        "direct_closed_labelled": 671,
        "direct_closed_quotient": direct_closed,
        "direct_rank_bound": 44,
        "maximal_labelled": dict(labelled_maximal),
    }, quotient


def outer(left, right):
    return tuple(tuple(Q(left[row]) * Q(right[column])
                       for column in COLOURS)
                 for row in COLOURS)


def exact_maximal_packet():
    potential = (Q(1), Q(1), Q(1), Q(-1), Q(-1), Q(-1))
    endpoint = {
        0: ((Q(2), Q(3)), (Q(5), Q(7))),
        1: outer((2, 3), (1, 2)),
        2: ZERO_MATRIX,
        3: ZERO_MATRIX,
        4: ZERO_MATRIX,
        5: ZERO_MATRIX,
    }
    free = frozenset(
        (left, right) for left in (0, 1, 2) for right in (3, 4, 5)
    )
    blocks = {}
    numerators = {}
    for left, right in EDGES:
        numerator = LITERAL["matrix_product"](
            LITERAL["matrix_product"](endpoint[left], LITERAL["J"]),
            LITERAL["transpose"](endpoint[right]),
        )
        numerators[left, right] = numerator
        denominator = potential[left] + potential[right]
        if denominator:
            block = tuple(
                tuple(Q(numerator[row][column], denominator)
                      for column in COLOURS)
                for row in COLOURS
            )
        elif (left, right) in free:
            start = 11 + 7 * left + 13 * right
            block = (
                (Q(start), Q(start + 1)),
                (Q(start + 2), Q(start + 4)),
            )
        else:
            block = ZERO_MATRIX
        blocks[left, right] = block
        for row, column in product(COLOURS, repeat=2):
            require(numerator[row][column]
                    == denominator * block[row][column],
                    ("maximal generic-kernel identity failed",
                     left, right, row, column))

    ranks = tuple(LITERAL["matrix_rank"](endpoint[site]) for site in SITES)
    require(ranks == (2, 1, 0, 0, 0, 0),
            ("maximal endpoint ranks changed", ranks))
    packet = LITERAL["packet_from_blocks"](blocks)
    numerator_packet = LITERAL["packet_from_blocks"](numerators)
    slope = LITERAL["matching_tensor"](packet)
    tangent = LITERAL["apply_differential"](packet, numerator_packet)
    z_value = -sum(potential)
    require(z_value == 0,
            ("maximal direct parameter changed", z_value))
    require(all(z_value * base + derivative == 0
                for base, derivative in zip(slope, tangent)),
            "a maximal selected level-two row failed")
    return potential, endpoint, blocks, packet


def coordinate_tangent(cell):
    return {candidate: Q(candidate == cell) for candidate in CELLS}


def gauge_tangent(packet, mu):
    return {
        (left, right, row, column):
            (mu[left] + mu[right]) * packet[left, right, row, column]
        for left, right, row, column in CELLS
    }


def constraint_nullity(graph_edges):
    # Rows encode mu_u+mu_v=0 on graph edges, together with sum mu=0.
    rows = []
    for left, right in sorted(graph_edges):
        row = [Q(0)] * 6
        row[left] = Q(1)
        row[right] = Q(1)
        rows.append(row)
    rows.append([Q(1)] * 6)
    return 6 - LITERAL["rational_rank"](rows)


def modularize(matrix, prime):
    return [
        [int(value.numerator * pow(value.denominator, -1, prime) % prime)
         for value in row]
        for row in matrix
    ]


def audit_maximal_gauge_closure(quotient):
    members = [
        (support, potential) for support, potential in quotient.values()
        if maximal_type(support) == "split K33 zero boundary"
    ]
    require(len(members) == 1,
            ("maximal quotient orbit count changed", members))
    support, representative = members[0]
    inactive = frozenset(EDGES) - active_tangent_edges(support)
    inactive_shore = frozenset(((0, 1), (0, 2), (1, 2)))
    require(inactive == inactive_shore,
            ("maximal inactive triangle changed", inactive))

    active_graph = frozenset(support - inactive_shore)
    require(active_graph == frozenset(
        (left, right) for left in (0, 1, 2) for right in (3, 4, 5)
    ), ("maximal active graph stopped being K33", active_graph))
    require(constraint_nullity(support) == 0,
            "the full dense graph lost gauge injectivity")
    require(constraint_nullity(active_graph) == 1,
            "the K33 gauge/intersection line changed")

    potential, endpoint, blocks, packet = exact_maximal_packet()
    require(canonical_support(support_graph(potential))
            == canonical_support(support),
            ("maximal calibration support changed", potential, support))
    packet_support = frozenset(
        pair for pair, block in blocks.items()
        if any(value for row in block for value in row)
    )
    require(packet_support == support,
            ("maximal packet lost dense support", packet_support, support))

    inactive_vectors = []
    for left, right in sorted(inactive_shore):
        for row, column in product(COLOURS, repeat=2):
            tangent = coordinate_tangent((left, right, row, column))
            require(not any(LITERAL["apply_differential"](packet, tangent)),
                    ("an inactive-shore coordinate tangent became live",
                     left, right, row, column))
            inactive_vectors.append([tangent[cell] for cell in CELLS])
    require(LITERAL["rational_rank"](inactive_vectors) == 12,
            "the inactive triangle stopped supplying twelve directions")

    gauges = []
    for basis in range(5):
        mu = [Q(0)] * 6
        mu[basis] = Q(1)
        mu[5] = Q(-1)
        tangent = gauge_tangent(packet, mu)
        require(not any(LITERAL["apply_differential"](packet, tangent)),
                ("a maximal gauge left the kernel", basis))
        gauges.append([tangent[cell] for cell in CELLS])
    require(LITERAL["rational_rank"](gauges) == 5,
            "the five maximal gauges became dependent")
    combined_rank = LITERAL["rational_rank"](inactive_vectors + gauges)
    require(combined_rank == 16,
            ("inactive-triangle/gauge span changed", combined_rank))

    derivative = LITERAL["differential_matrix"](packet)
    ranks = (
        LITERAL["rational_rank"](derivative),
        LITERAL["modular_rank"](modularize(derivative, 101), 101),
        LITERAL["modular_rank"](
            modularize(derivative, 1_000_003), 1_000_003
        ),
    )
    require(ranks == (43, 43, 43),
            ("maximal calibration rank changed", ranks))

    # On the open locus where every K3,3 block and M01 are nonzero, the
    # full graph is connected and nonbipartite, so the five gauges inject.
    # A gauge in the twelve-coordinate inactive shore obeys its vanishing
    # equations on K3,3; that solution space is the single bipartite sign
    # line.  Hence the combined kernel has dimension 12+5-1=16.  Vanishing
    # of all 45-minors extends the rank-44 bound to every specialization.
    return {
        "potential_form": (
            "(lambda,lambda,lambda,-lambda,-lambda,-lambda), "
            "lambda != 0, up to S4"
        ),
        "representative": representative,
        "inactive_edges": tuple(sorted(inactive_shore)),
        "inactive_coordinate_directions": 12,
        "gauge_directions": 5,
        "intersection_dimension": 1,
        "independent_kernel_directions": combined_rank,
        "uniform_rank_bound": 44,
        "calibration_ranks": ranks,
        "selected_level_two_rows": 64,
    }


def main():
    census, quotient = audit_potential_support_census()
    maximal = audit_maximal_gauge_closure(quotient)
    print("1I+1R+4Z potential boundary audit passed")
    print("census:", census)
    print("maximal K33 gauge closure:", maximal)
    print("frontier: all 675 labelled / 85 quotient supports have rank <= 44")


if __name__ == "__main__":
    main()
