#!/usr/bin/env python3
"""Close the 1I+2R+3Z generic-kernel potential/support boundary.

Site 0 is invertible, sites 1,2 are nonzero rank one, and sites 3,4,5
are zero.  Signed partitions enumerate 376 labelled support envelopes, or
73 modulo S2 on the rank-one sites and S3 on the zero sites.  Seventy-one
quotient envelopes have at most 13 active tangent edges and rank at most
52.  The two dense quotient envelopes each have exactly one inactive edge.

On the dense nonzero-block locus, deletion of that edge leaves a connected
nonbipartite base graph.  The four inactive-edge coordinate tangents and
the five universal vertex gauges are therefore independent kernel
directions.  Rank is at most 51 there, and polynomial specialization
extends the bound to every boundary point.  Thus the full endpoint-rank
stratum closes before L0, L1, or residual R2.

Research evidence only.  Standard library exact arithmetic; checks remain
live under python -O and python -I -S.
"""

from collections import Counter, deque
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
FIXED_ROOT = run_path(str(
    HERE / "verify_level_two_one_invertible_five_rank_one_potential_reduction.py"
))
LITERAL = run_path(str(
    HERE / "verify_level_two_three_invertible_r2_guard.py"
))

SITES = tuple(range(6))
COLOURS = (0, 1)
CORE = (0, 1, 2)
RANK_ONE = (1, 2)
ZERO = (3, 4, 5)
EDGES = tuple(combinations(SITES, 2))
CELLS = tuple(
    (left, right, row, column)
    for left, right in EDGES
    for row, column in product(COLOURS, repeat=2)
)
CORE_EDGES = frozenset(combinations(CORE, 2))
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
    zero_sum = PARTITIONS["zero_sum"]
    return all(not zero_sum(potential[0], potential[site])
               for site in RANK_ONE)


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
    for rank_order, zero_order in product(
            permutations(RANK_ONE), permutations(ZERO)):
        mapping = list(SITES)
        for old, new in zip(RANK_ONE, rank_order):
            mapping[old] = new
        for old, new in zip(ZERO, zero_order):
            mapping[old] = new
        answer.append(tuple(mapping))
    require(len(answer) == 12, "S2 x S3 relabelling count changed")
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


def dense_type(support):
    optional = optional_part(support)
    rank_zero = {
        rank: frozenset(zero for zero in ZERO
                        if edge(rank, zero) in optional)
        for rank in RANK_ONE
    }
    root_zero = frozenset(
        zero for zero in ZERO if edge(0, zero) in optional
    )
    zero_edges = frozenset(
        pair for pair in combinations(ZERO, 2) if pair in optional
    )

    # nu_1=...=nu_5=0, nu_0!=0: K5 on the non-root sites.
    if (not root_zero
            and all(rank_zero[rank] == frozenset(ZERO)
                    for rank in RANK_ONE)
            and zero_edges == frozenset(combinations(ZERO, 2))):
        return "five-site zero clique"

    # One zero endpoint shares the core potential lambda; the other two
    # have potential -lambda.  The optional graph is K_{4,2} between the
    # core plus the positive zero endpoint and the two negative endpoints.
    if len(root_zero) == 2 and all(
            rank_zero[rank] == root_zero for rank in RANK_ONE):
        positive = frozenset(ZERO) - root_zero
        if len(positive) == 1:
            positive_site = next(iter(positive))
            expected_zero_edges = frozenset(
                edge(positive_site, negative) for negative in root_zero
            )
            if zero_edges == expected_zero_edges:
                return "split K42 zero boundary"
    return None


def audit_potential_support_census():
    potentials = PARTITIONS["signed_partitions"](6)
    require(len(potentials) == 4088,
            ("signed-partition census changed", len(potentials)))
    admissible_potentials = tuple(filter(admissible, potentials))
    require(len(admissible_potentials) == 2908,
            ("admissible potential census changed",
             len(admissible_potentials)))

    representatives = {}
    for potential in admissible_potentials:
        representatives.setdefault(support_graph(potential), potential)
    require(len(representatives) == 376,
            ("labelled support census changed", len(representatives)))

    labelled_histogram = Counter(
        len(active_tangent_edges(support)) for support in representatives
    )
    require(labelled_histogram == Counter({
        0: 1, 1: 21, 2: 9, 3: 33, 4: 60, 5: 48, 6: 21,
        7: 69, 8: 27, 9: 52, 10: 6, 11: 12, 12: 10, 13: 3, 14: 4,
    }), ("labelled active-edge histogram changed", labelled_histogram))

    quotient = {}
    for support, potential in representatives.items():
        quotient.setdefault(canonical_support(support), (support, potential))
    require(len(quotient) == 73,
            ("quotient support census changed", len(quotient)))

    quotient_histogram = Counter(
        len(active_tangent_edges(support))
        for support, _ in quotient.values()
    )
    require(quotient_histogram == Counter({
        0: 1, 1: 5, 2: 2, 3: 7, 4: 7, 5: 10, 6: 6,
        7: 11, 8: 4, 9: 9, 10: 1, 11: 3, 12: 3, 13: 2, 14: 2,
    }), ("quotient active-edge histogram changed", quotient_histogram))

    labelled_dense = Counter(
        dense_type(support) for support in representatives
        if len(active_tangent_edges(support)) == 14
    )
    require(labelled_dense == Counter({
        "five-site zero clique": 1,
        "split K42 zero boundary": 3,
    }), ("labelled dense types changed", labelled_dense))
    quotient_dense = Counter(
        dense_type(support) for support, _ in quotient.values()
        if len(active_tangent_edges(support)) == 14
    )
    require(quotient_dense == Counter({
        "five-site zero clique": 1,
        "split K42 zero boundary": 1,
    }), ("quotient dense types changed", quotient_dense))

    support_closed = sum(
        count for active, count in quotient_histogram.items() if active <= 13
    )
    require(support_closed == 71,
            ("support-closed quotient count changed", support_closed))
    return {
        "signed_partitions": len(potentials),
        "admissible_potentials": len(admissible_potentials),
        "labelled_supports": len(representatives),
        "quotient_supports": len(quotient),
        "labelled_histogram": dict(sorted(labelled_histogram.items())),
        "quotient_histogram": dict(sorted(quotient_histogram.items())),
        "support_closed_labelled": 372,
        "support_closed_quotient": support_closed,
        "support_rank_bound": 52,
        "dense_labelled": dict(labelled_dense),
    }, quotient


def connected_nonbipartite(graph_edges):
    adjacency = {site: set() for site in SITES}
    for left, right in graph_edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    reached = set()
    colours = {}
    nonbipartite = False
    queue = deque((0,))
    colours[0] = 0
    while queue:
        site = queue.popleft()
        reached.add(site)
        for neighbour in adjacency[site]:
            if neighbour not in colours:
                colours[neighbour] = 1 - colours[site]
                queue.append(neighbour)
            elif colours[neighbour] == colours[site]:
                nonbipartite = True
    return reached == set(SITES) and nonbipartite


def outer(left, right):
    return tuple(tuple(Q(left[row]) * Q(right[column])
                       for column in COLOURS)
                 for row in COLOURS)


def exact_dense_packet(name):
    if name == "five-site zero clique":
        potential = (Q(1), Q(0), Q(0), Q(0), Q(0), Q(0))
        endpoint = {
            0: ((Q(2), Q(3)), (Q(5), Q(7))),
            1: outer((2, 3), (1, 1)),
            2: outer((5, 7), (1, -1)),
            3: ZERO_MATRIX,
            4: ZERO_MATRIX,
            5: ZERO_MATRIX,
        }
        free = frozenset(combinations((1, 2, 3, 4, 5), 2))
    elif name == "split K42 zero boundary":
        potential = (Q(1), Q(1), Q(1), Q(1), Q(-1), Q(-1))
        endpoint = {
            0: ((Q(2), Q(3)), (Q(5), Q(7))),
            1: outer((2, 3), (1, 2)),
            2: outer((5, 7), (2, 3)),
            3: ZERO_MATRIX,
            4: ZERO_MATRIX,
            5: ZERO_MATRIX,
        }
        free = frozenset(
            (left, right) for left in (0, 1, 2, 3) for right in (4, 5)
        )
    else:
        raise RuntimeError(("unknown dense type", name))

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
                    ("dense generic-kernel identity failed",
                     name, left, right, row, column))

    ranks = tuple(LITERAL["matrix_rank"](endpoint[site]) for site in SITES)
    require(ranks == (2, 1, 1, 0, 0, 0),
            ("dense endpoint ranks changed", name, ranks))
    packet = LITERAL["packet_from_blocks"](blocks)
    numerator_packet = LITERAL["packet_from_blocks"](numerators)
    slope = LITERAL["matching_tensor"](packet)
    tangent = LITERAL["apply_differential"](packet, numerator_packet)
    z_value = -sum(potential)
    require(all(z_value * base + derivative == 0
                for base, derivative in zip(slope, tangent)),
            ("a dense selected level-two row failed", name))
    return potential, endpoint, blocks, packet


def packet_support(blocks):
    return frozenset(
        pair for pair, block in blocks.items()
        if any(value for row in block for value in row)
    )


def coordinate_tangent(cell):
    return {
        candidate: Q(candidate == cell) for candidate in CELLS
    }


def gauge_tangent(packet, mu):
    return {
        (left, right, row, column):
            (mu[left] + mu[right]) * packet[left, right, row, column]
        for left, right, row, column in CELLS
    }


def modularize(matrix, prime):
    return [
        [int(value.numerator * pow(value.denominator, -1, prime) % prime)
         for value in row]
        for row in matrix
    ]


def audit_dense_gauge_closure(quotient):
    expected = {
        "five-site zero clique": {
            "potential": "(lambda,0,0,0,0,0), lambda != 0",
            "inactive_edge": (1, 2),
            "labelled_supports": 1,
            "calibration_rank": 48,
        },
        "split K42 zero boundary": {
            "potential": (
                "(lambda,lambda,lambda,lambda,-lambda,-lambda), "
                "lambda != 0, up to S3"
            ),
            "inactive_edge": (4, 5),
            "labelled_supports": 3,
            "calibration_rank": 43,
        },
    }
    actual = {}
    for name, data in expected.items():
        members = [
            (support, potential) for support, potential in quotient.values()
            if dense_type(support) == name
        ]
        require(len(members) == 1,
                ("dense quotient orbit count changed", name, members))
        support, representative = members[0]
        inactive = frozenset(EDGES) - active_tangent_edges(support)
        require(inactive == frozenset((data["inactive_edge"],)),
                ("dense inactive edge changed", name, inactive))
        reduced_graph = frozenset(support - inactive)
        require(connected_nonbipartite(reduced_graph),
                ("dense gauge graph lost its odd connected core",
                 name, reduced_graph))

        potential, endpoint, blocks, packet = exact_dense_packet(name)
        require(canonical_support(support_graph(potential))
                == canonical_support(support),
                ("dense calibration changed support type", name, potential))
        require(packet_support(blocks) == support,
                ("dense calibration support changed", name,
                 packet_support(blocks), support))

        inactive_vectors = []
        left, right = data["inactive_edge"]
        for row, column in product(COLOURS, repeat=2):
            tangent = coordinate_tangent((left, right, row, column))
            require(not any(LITERAL["apply_differential"](packet, tangent)),
                    ("an inactive coordinate tangent became live",
                     name, left, right, row, column))
            inactive_vectors.append([tangent[cell] for cell in CELLS])

        gauges = []
        for basis in range(5):
            mu = [Q(0)] * 6
            mu[basis] = Q(1)
            mu[5] = Q(-1)
            tangent = gauge_tangent(packet, mu)
            require(not any(LITERAL["apply_differential"](packet, tangent)),
                    ("a dense gauge left the kernel", name, basis))
            gauges.append([tangent[cell] for cell in CELLS])
        combined_kernel_rank = LITERAL["rational_rank"](
            inactive_vectors + gauges
        )
        require(combined_kernel_rank == 9,
                ("inactive/gauge kernel rank changed",
                 name, combined_kernel_rank))

        derivative = LITERAL["differential_matrix"](packet)
        ranks = (
            LITERAL["rational_rank"](derivative),
            LITERAL["modular_rank"](modularize(derivative, 101), 101),
            LITERAL["modular_rank"](
                modularize(derivative, 1_000_003), 1_000_003
            ),
        )
        require(ranks == (data["calibration_rank"],) * 3,
                ("dense calibration rank changed", name, ranks))
        actual[name] = {
            "representative": representative,
            "inactive_edge": data["inactive_edge"],
            "connected_nonbipartite_after_deletion": True,
            "independent_kernel_directions": combined_kernel_rank,
            "uniform_rank_bound": 51,
            "calibration_ranks": ranks,
            "selected_level_two_rows": 64,
        }

    # On the open locus where every displayed support block is nonzero,
    # connected nonbipartiteness makes the five gauge directions injective.
    # The same property after deleting the inactive edge makes their span
    # disjoint from its four coordinate directions.  All 52-minors vanish
    # on that dense open locus and therefore identically on each family.
    require(sum(data["labelled_supports"] for data in expected.values()) == 4,
            "dense labelled closure count changed")
    return expected, actual


def audit_isotropic_zero_clique_fixed_root():
    # If the two orthogonal rank-one input factors are proportional, their
    # common line is isotropic.  The two root spokes then share X_0 J b,
    # while the three root-to-zero blocks vanish, fixing root 0.
    pairing = FIXED_ROOT["pairing"]
    for vector in ((Q(1), Q(0)), (Q(0), Q(1))):
        require(pairing(vector, vector) == 0,
                ("coordinate isotropic line changed", vector))
    fixed_cases, symbolic_bound, calibrated_bound = (
        FIXED_ROOT["audit_fixed_root_bound"]()
    )
    require(symbolic_bound == calibrated_bound == 42
            and "common isotropic pencil" in fixed_cases,
            ("isotropic fixed-root theorem changed",
             fixed_cases, symbolic_bound, calibrated_bound))
    return {
        "subbranch": "b_1 proportional to b_2 and b_1^T J b_2 = 0",
        "fixed_root": 0,
        "rank_bound": calibrated_bound,
    }


def main():
    census, quotient = audit_potential_support_census()
    dense, calibrations = audit_dense_gauge_closure(quotient)
    isotropic = audit_isotropic_zero_clique_fixed_root()
    print("1I+2R+3Z potential boundary audit passed")
    print("census:", census)
    print("dense gauge closures:", dense)
    print("dense exact calibrations:", calibrations)
    print("isotropic zero-clique refinement:", isotropic)
    print("frontier: all 376 labelled / 73 quotient supports close before R2")


if __name__ == "__main__":
    main()
