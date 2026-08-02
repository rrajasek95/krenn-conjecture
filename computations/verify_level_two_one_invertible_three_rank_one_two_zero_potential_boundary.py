#!/usr/bin/env python3
"""Audit the 1I+3R+2Z generic-kernel potential boundary.

Let site 0 be invertible, sites 1,2,3 be nonzero rank one, and sites
4,5 be zero.  The invertible--rank-one generic-kernel numerators imply
nu_0+nu_i != 0 for i=1,2,3.  Broaden the four-site core {0,1,2,3} to
K4; a zero-incident base edge is potentially nonzero exactly when its
endpoint potentials sum to zero.

Signed partitions enumerate all zero/opposition relations among the six
potentials.  There are 147 labelled support envelopes and 37 modulo S3
on the rank-one sites and S2 on the zero sites.  Complement matching
support leaves at most 13 active tangent edges in 33 quotient envelopes,
so rank(dPsi) <= 52 there.  Of the four dense quotient envelopes, the
all-zero five-site pencil fixes the invertible root and gives rank <= 42,
the two-zero-rank-one K4 shore has a fixed rank-one root and also gives
rank <= 42, while split K2,3 opposition is a boundary specialization of
the exact 1I+5R K2,3 syzygy theorem and gives rank <= 51.  The exact
residual has one potential/support type.

Research evidence only.  Standard library exact arithmetic; checks stay
live under python -O and python -I -S.
"""

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
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
FIVE_RANK_ONE = run_path(str(
    HERE / "verify_level_two_one_invertible_five_rank_one_potential_reduction.py"
))
K23_CLOSURE = run_path(str(
    HERE / "verify_level_two_one_invertible_k23_antipodal_pencil_rank_closure.py"
))
R2_GUARD = run_path(str(
    HERE / "verify_level_two_three_invertible_r2_guard.py"
))

SITES = tuple(range(6))
CORE = (0, 1, 2, 3)
RANK_ONE = (1, 2, 3)
ZERO = (4, 5)
EDGES = tuple(combinations(SITES, 2))
CORE_EDGES = frozenset(combinations(CORE, 2))


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
    # X_0 J X_i^T is nonzero when X_0 is invertible and X_i is nonzero
    # rank one.  Hence its scalar denominator cannot vanish.
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
    # A 2x2 tangent block at uv can occur only when the complementary
    # four-site Pfaffian has a supported perfect matching.
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
    require(len(answer) == 12, "S3 x S2 relabelling count changed")
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
    """Name one of the four dense support types, or return None."""

    optional = optional_part(support)
    zero_pair = edge(4, 5) in optional
    neighbours = {
        zero: frozenset(core for core in CORE
                        if edge(core, zero) in optional)
        for zero in ZERO
    }

    if (not zero_pair
            and neighbours[4] == frozenset(CORE)
            and neighbours[5] == frozenset(CORE)):
        return "all-spokes"

    if zero_pair:
        if (neighbours[4] == neighbours[5]
                and 0 not in neighbours[4]
                and len(neighbours[4]) == 2):
            return "two-zero-rank-one K4 shore"
        if (neighbours[4] == neighbours[5] == frozenset(RANK_ONE)):
            return "five-site zero pencil"
        if (0 not in neighbours[4] and 0 not in neighbours[5]
                and neighbours[4].isdisjoint(neighbours[5])
                and sorted((len(neighbours[4]), len(neighbours[5])))
                == [1, 2]
                and neighbours[4] | neighbours[5]
                == frozenset(RANK_ONE)):
            return "split K23 opposition"
    return None


def audit_potential_support_census():
    signed_partitions = PARTITIONS["signed_partitions"]
    potentials = signed_partitions(6)
    require(len(potentials) == 4088,
            ("signed-partition census changed", len(potentials)))

    admissible_potentials = tuple(filter(admissible, potentials))
    require(len(admissible_potentials) == 2468,
            ("admissible potential census changed",
             len(admissible_potentials)))

    representatives = {}
    for potential in admissible_potentials:
        representatives.setdefault(support_graph(potential), potential)
    require(len(representatives) == 147,
            ("labelled support census changed", len(representatives)))

    labelled_histogram = Counter(
        len(active_tangent_edges(support)) for support in representatives
    )
    require(labelled_histogram == Counter({
        1: 1, 4: 8, 5: 22, 7: 5, 8: 12, 10: 38,
        11: 30, 12: 4, 13: 16, 14: 6, 15: 5,
    }), ("labelled active-edge histogram changed", labelled_histogram))

    quotient = {}
    for support, potential in representatives.items():
        quotient.setdefault(canonical_support(support), (support, potential))
    require(len(quotient) == 37,
            ("quotient support census changed", len(quotient)))

    quotient_histogram = Counter(
        len(active_tangent_edges(support))
        for support, _ in quotient.values()
    )
    require(quotient_histogram == Counter({
        1: 1, 4: 2, 5: 5, 7: 3, 8: 2, 10: 7,
        11: 7, 12: 2, 13: 4, 14: 1, 15: 3,
    }), ("quotient active-edge histogram changed", quotient_histogram))

    labelled_dense = Counter(
        dense_type(support) for support in representatives
        if len(active_tangent_edges(support)) >= 14
    )
    expected_labelled_dense = Counter({
        "all-spokes": 1,
        "two-zero-rank-one K4 shore": 3,
        "five-site zero pencil": 1,
        "split K23 opposition": 6,
    })
    require(labelled_dense == expected_labelled_dense,
            ("labelled dense types changed", labelled_dense))

    quotient_dense = Counter(
        dense_type(support) for support, _ in quotient.values()
        if len(active_tangent_edges(support)) >= 14
    )
    require(quotient_dense == Counter({name: 1
                                       for name in expected_labelled_dense}),
            ("quotient dense types changed", quotient_dense))

    # Every non-dense quotient has at most 13 active 2x2 tangent blocks.
    # Four scalar cells per block give a support-only rank bound of 52.
    support_closed = sum(count for active, count in quotient_histogram.items()
                         if active <= 13)
    require(support_closed == 33,
            ("support-closed quotient count changed", support_closed))
    return {
        "signed_partitions": len(potentials),
        "admissible_potentials": len(admissible_potentials),
        "labelled_supports": len(representatives),
        "quotient_supports": len(quotient),
        "labelled_histogram": dict(sorted(labelled_histogram.items())),
        "quotient_histogram": dict(sorted(quotient_histogram.items())),
        "dense_labelled": dict(labelled_dense),
        "support_closed_quotient": support_closed,
        "support_rank_bound": 52,
    }, quotient


def audit_five_site_zero_pencil_closure(quotient):
    dense = [
        (support, potential)
        for support, potential in quotient.values()
        if dense_type(support) == "five-site zero pencil"
    ]
    require(len(dense) == 1, ("zero-pencil orbit count changed", dense))
    support, potential = dense[0]

    # The optional graph forces nu_1=...=nu_5=0 and nu_0!=0.  Check this
    # on its canonical signed-partition representative.
    require(potential[0] != 0 and potential[1:] == (0, 0, 0, 0, 0),
            ("zero-pencil representative changed", potential, support))

    # For X_i=h_i b_i^T, the three rank-one pair equations make b_1,b_2,
    # b_3 nonzero and pairwise J-orthogonal.  In dimension two they share
    # one isotropic line.  Consequently M_01,M_02,M_03 share the fixed
    # root X_0 J b, while M_04=M_05=0.  The existing fixed-root theorem
    # applies at site 0.
    pencil_checks = FIVE_RANK_ONE["audit_complete_orthogonal_pencil"]()
    require(pencil_checks == (128, 48),
            ("orthogonal-pencil audit changed", pencil_checks))
    fixed_cases, symbolic_bound, calibrated_bound = (
        FIVE_RANK_ONE["audit_fixed_root_bound"]()
    )
    require(symbolic_bound == calibrated_bound == 42,
            ("fixed-root bound changed", symbolic_bound, calibrated_bound))
    require("common isotropic pencil" in fixed_cases,
            ("fixed-root case label changed", fixed_cases))
    return {
        "potential_form": "(lambda,0,0,0,0,0), lambda != 0",
        "orthogonal_pencil_checks": pencil_checks,
        "fixed_root": 0,
        "rank_bound": calibrated_bound,
    }


def audit_split_k23_boundary_closure(quotient):
    dense = [
        (support, potential)
        for support, potential in quotient.values()
        if dense_type(support) == "split K23 opposition"
    ]
    require(len(dense) == 1, ("split K23 orbit count changed", dense))

    # Pin the previously audited exact K2,3 polynomial family.  Its nine
    # function-field kernel directions give rank <= 51 for arbitrary six
    # cross-shore blocks.  Rebuilding the program and checking its digest
    # ties this standard-library boundary audit to that exact syzygy proof
    # without rerunning Singular here.
    fixed, r2 = K23_CLOSURE["audit_covariant_normal_form"]()
    packet = K23_CLOSURE["symbolic_packet"](fixed)
    entries, symbolic_support = (
        K23_CLOSURE["symbolic_differential_entries"](packet)
    )
    program = K23_CLOSURE["singular_program"](entries)
    digest = sha256(program.encode()).hexdigest()
    require(digest
            == "d18201acf82be051be1ed6a77e29f21af72c3649410dc64a4401668725da08f5",
            ("K23 syzygy program changed", digest))
    require(len(fixed) == 9 and len(K23_CLOSURE["FREE_EDGES"]) == 6
            and symbolic_support == 512 and len(r2) == 6,
            ("K23 theorem interface changed", len(fixed),
             len(K23_CLOSURE["FREE_EDGES"]), symbolic_support, len(r2)))

    # In canonical K2,3 labels, scale one endpoint factor on each shore to
    # zero: sites 2 and 5.  Exactly five of the nine fixed blocks then tend
    # to zero, while all six zero-multiplier cross blocks stay arbitrary.
    # The four remaining fixed blocks are precisely the root spokes and
    # same-shore block among the three nonzero rank-one endpoints.
    zero_endpoints = frozenset((2, 5))
    vanishing_fixed = frozenset(
        pair for pair in fixed if zero_endpoints.intersection(pair)
    )
    surviving_fixed = frozenset(fixed) - vanishing_fixed
    require(vanishing_fixed == frozenset({
        (0, 2), (1, 2), (0, 5), (3, 5), (4, 5),
    }), ("K23 zero-endpoint degeneration changed", vanishing_fixed))
    require(surviving_fixed == frozenset({
        (0, 1), (0, 3), (0, 4), (3, 4),
    }), ("K23 surviving fixed blocks changed", surviving_fixed))
    require(len(K23_CLOSURE["FREE_EDGES"]) == 6,
            "K23 cross-shore freedom changed under degeneration")

    # The isotropic subbranch is also in the closure: the orthogonal lines
    # b_A(t)=(1,t), b_B(t)=(1,-t) are distinct and nonisotropic for t!=0,
    # then coalesce to their common isotropic line at t=0.
    pairing = FIVE_RANK_ONE["pairing"]
    for parameter in range(-3, 4):
        b_a = (1, parameter)
        b_b = (1, -parameter)
        require(pairing(b_a, b_b) == 0,
                ("K23 pencil degeneration lost orthogonality", parameter))
        if parameter:
            require(pairing(b_a, b_a) != 0
                    and pairing(b_b, b_b) != 0,
                    ("K23 nonzero degeneration became isotropic", parameter))
        else:
            require(b_a == b_b and pairing(b_a, b_a) == 0,
                    "K23 limiting pencil stopped being common isotropic")

    # Every 52-minor vanishes on the nonzero scaling/pencil parameters by
    # the exact K23 theorem, hence as a polynomial it also vanishes at the
    # zero-endpoint and isotropic limits.
    return {
        "source_theorem": "1I+5R split K23 exact syzygies",
        "syzygy_program_sha256": digest,
        "arbitrary_cross_blocks": 6,
        "vanishing_fixed_blocks": len(vanishing_fixed),
        "surviving_fixed_blocks": len(surviving_fixed),
        "rank_bound": 51,
    }


def audit_two_zero_rank_one_fixed_root_closure(quotient):
    dense = [
        (support, potential)
        for support, potential in quotient.values()
        if dense_type(support) == "two-zero-rank-one K4 shore"
    ]
    require(len(dense) == 1,
            ("two-zero-rank-one shore orbit count changed", dense))

    # Relabel so the potential is (alpha,beta,0,0,0,0), with site 1 the
    # nonzero-potential rank-one endpoint.  The generic-kernel constraints
    # are alpha*beta*(alpha+beta)!=0.  Thus every block at root 1 has its
    # h_1 endpoint factor: M_10,M_12,M_13 are determined outer products,
    # while M_14=M_15=0.  This is exactly the fixed-root envelope.
    displayed = (2, 1, 0, 0, 0, 0)
    require(admissible(displayed)
            and dense_type(support_graph(displayed))
            == "two-zero-rank-one K4 shore",
            ("displayed fixed-root potential changed", displayed))
    support = support_graph(displayed)
    require(edge(1, 4) not in support and edge(1, 5) not in support,
            ("fixed-root zero spokes became free", support))

    pair_checks, root_images = FIVE_RANK_ONE["audit_rank_one_pair_pencil"]()
    require(pair_checks == 625 and len(root_images) == 5,
            ("rank-one outer-product audit changed",
             pair_checks, len(root_images)))
    fixed_cases, symbolic_bound, calibrated_bound = (
        FIVE_RANK_ONE["audit_fixed_root_bound"]()
    )
    require(symbolic_bound == calibrated_bound == 42,
            ("fixed-root bound changed", symbolic_bound, calibrated_bound))
    require("isolated rank-one potential" in fixed_cases,
            ("rank-one fixed-root case changed", fixed_cases))
    return {
        "potential_form": (
            "(alpha,beta,0,0,0,0), alpha*beta*(alpha+beta) != 0"
        ),
        "fixed_root": 1,
        "forced_zero_spokes": ((1, 4), (1, 5)),
        "rank_bound": calibrated_bound,
    }


def audit_exact_residual(quotient):
    expected = {
        "all-spokes": {
            "active_edges": 15,
            "potential_form": (
                "(lambda,lambda,lambda,lambda,-lambda,-lambda), lambda != 0"
            ),
            "witness_potential": (1, 1, 1, 1, -1, -1),
            "labelled_supports": 1,
        },
        "two-zero-rank-one K4 shore": {
            "active_edges": 15,
            "potential_form": (
                "(alpha,beta,0,0,0,0), alpha*beta*(alpha+beta) != 0, "
                "up to S3"
            ),
            "witness_potential": (1, 1, 0, 0, 0, 0),
            "labelled_supports": 3,
        },
        "split K23 opposition": {
            "active_edges": 14,
            "potential_form": (
                "(mu,-lambda,-lambda,lambda,-lambda,lambda), "
                "lambda != 0 and mu != +/-lambda"
            ),
            "witness_potential": (0, -1, -1, 1, -1, 1),
            "labelled_supports": 6,
        },
    }
    actual = {}
    for support, potential in quotient.values():
        name = dense_type(support)
        if name not in expected:
            continue
        actual[name] = {
            "active_edges": len(active_tangent_edges(support)),
            "representative": potential,
            "optional_edges": tuple(sorted(optional_part(support))),
        }
    require(set(actual) == set(expected),
            ("exact residual types changed", actual))
    for name, data in expected.items():
        require(actual[name]["active_edges"] == data["active_edges"],
                ("residual active-edge count changed", name, actual[name]))
        witness_support = support_graph(data["witness_potential"])
        require(canonical_support(witness_support)
                == canonical_support(next(
                    support for support, _ in quotient.values()
                    if dense_type(support) == name
                )), ("displayed residual potential changed type", name,
                     data["witness_potential"], witness_support))

    # In the latter two types nu_0+nu_4 and nu_0+nu_5 are nonzero, so the
    # generic-kernel equation forces M_04=M_05=0.  Since X_0 is invertible,
    # literal R2 at root 0 cannot use pair preservation; its two physical
    # pure-column witnesses must therefore occur on two distinct rank-one
    # spokes.  An outer product g h^T is pure in physical column c exactly
    # when h lies on the corresponding coordinate axis.
    for name in ("two-zero-rank-one K4 shore", "split K23 opposition"):
        support = next(support for support, _ in quotient.values()
                       if dense_type(support) == name)
        require(edge(0, 4) not in support and edge(0, 5) not in support,
                ("forced-zero root spokes changed", name, support))
    all_spokes = next(support for support, _ in quotient.values()
                      if dense_type(support) == "all-spokes")
    require(edge(0, 4) in all_spokes and edge(0, 5) in all_spokes,
            ("all-spokes root freedom changed", all_spokes))

    def outer(left, right):
        return tuple(tuple(left[row] * right[column]
                           for column in range(2))
                     for row in range(2))

    def pure_column(block, column):
        other = 1 - column
        return (any(block[row][column] for row in range(2))
                and all(block[row][other] == 0 for row in range(2)))

    g = (2, 3)
    require(pure_column(outer(g, (5, 0)), 0)
            and not pure_column(outer(g, (5, 0)), 1),
            "physical e0 factor stopped being column-pure")
    require(pure_column(outer(g, (0, 7)), 1)
            and not pure_column(outer(g, (0, 7)), 0),
            "physical e1 factor stopped being column-pure")
    require(not any(pure_column(outer(g, (11, 13)), column)
                    for column in range(2)),
            "mixed physical factor became column-pure")

    # The dense labelled counts leave 10 support envelopes in these three
    # quotient types after the single zero-pencil envelope is closed.
    require(sum(data["labelled_supports"] for data in expected.values()) == 10,
            "residual labelled support count changed")
    r2_root_zero = {
        "two-zero-rank-one K4 shore": (
            "distinct rank-one spokes with h_i || e_0 and h_j || e_1"
        ),
        "split K23 opposition": (
            "distinct rank-one spokes with h_i || e_0 and h_j || e_1"
        ),
        "all-spokes": "zero-endpoint spokes remain free",
    }
    return expected, actual, r2_root_zero


def audit_all_spokes_rank55_r2_guard():
    colours = R2_GUARD["COLOURS"]
    edges = R2_GUARD["EDGES"]
    words = R2_GUARD["WORDS"]
    j_form = R2_GUARD["J"]
    matrix_product = R2_GUARD["matrix_product"]
    transpose = R2_GUARD["transpose"]

    def outer(left, right):
        return tuple(tuple(left[row] * right[column]
                           for column in colours)
                     for row in colours)

    # The input factors b_1=(1,1), b_2=(1,2) are sent by X_0 J to the two
    # physical axes.  The output factors h_1=e_0, h_2=e_1 then give a
    # four-root cycle of literal internal R2 witnesses; h_3=(1,1).
    endpoint = {
        0: ((-1, 2), (1, -1)),
        1: outer((1, 0), (1, 1)),
        2: outer((0, 1), (1, 2)),
        3: outer((1, 1), (2, 3)),
        4: ((0, 0), (0, 0)),
        5: ((0, 0), (0, 0)),
    }
    ranks = tuple(R2_GUARD["matrix_rank"](endpoint[site]) for site in SITES)
    require(ranks == (2, 1, 1, 1, 0, 0),
            ("all-spokes endpoint ranks changed", ranks))

    potential = (Q(1), Q(1), Q(1), Q(1), Q(-1), Q(-1))
    require(admissible(potential)
            and dense_type(support_graph(potential)) == "all-spokes",
            ("all-spokes guard potential changed", potential))

    blocks = {}
    numerators = {}
    for left, right in edges:
        numerator = matrix_product(
            matrix_product(endpoint[left], j_form),
            transpose(endpoint[right]),
        )
        numerators[left, right] = numerator
        denominator = potential[left] + potential[right]
        if denominator:
            blocks[left, right] = tuple(
                tuple(Q(numerator[row][column], denominator)
                      for column in colours)
                for row in colours
            )
        elif (left, right) == (4, 5):
            blocks[left, right] = ((Q(0), Q(0)), (Q(0), Q(0)))
        else:
            # Deterministic dense values on the eight zero-multiplier
            # core-to-zero spokes.
            start = 11 + 7 * left + 13 * right
            blocks[left, right] = (
                (Q(start), Q(start + 1)),
                (Q(start + 2), Q(start + 4)),
            )

        for row, column in product(colours, repeat=2):
            require(numerator[row][column]
                    == denominator * blocks[left, right][row][column],
                    ("all-spokes generic-kernel identity failed",
                     left, right, row, column))

    packet = R2_GUARD["packet_from_blocks"](blocks)

    # The selected level-two equation follows with z=-sum(nu)=-2; audit
    # all 64 rows directly from the matching tensor and its differential.
    numerator_packet = R2_GUARD["packet_from_blocks"](numerators)
    slope = R2_GUARD["matching_tensor"](packet)
    tangent = R2_GUARD["apply_differential"](packet, numerator_packet)
    z_value = -sum(potential)
    require(z_value == -2, ("all-spokes z changed", z_value))
    require(all(z_value * base + derivative == 0
                for base, derivative in zip(slope, tangent)),
            "an all-spokes selected level-two row failed")

    derivative = R2_GUARD["differential_matrix"](packet)

    def modularize(matrix, prime):
        return [
            [int(value.numerator * pow(value.denominator, -1, prime) % prime)
             for value in row]
            for row in matrix
        ]

    differential_ranks = (
        R2_GUARD["rational_rank"](derivative),
        R2_GUARD["modular_rank"](modularize(derivative, 101), 101),
        R2_GUARD["modular_rank"](
            modularize(derivative, 1_000_003), 1_000_003
        ),
    )
    require(differential_ranks == (55, 55, 55),
            ("all-spokes differential rank changed", differential_ranks))

    # Independently display the five universal trace-zero vertex gauges.
    gauge_vectors = []
    for basis in range(5):
        mu = [Q(0)] * 6
        mu[basis] = Q(1)
        mu[5] = Q(-1)
        gauge = {
            (left, right, row, column):
                (mu[left] + mu[right])
                * packet[left, right, row, column]
            for left, right in edges
            for row, column in product(colours, repeat=2)
        }
        require(not any(R2_GUARD["apply_differential"](packet, gauge)),
                ("an all-spokes gauge left the kernel", basis))
        gauge_vectors.append([gauge[cell] for cell in R2_GUARD["CELLS"]])
    require(R2_GUARD["rational_rank"](gauge_vectors) == 5,
            "the all-spokes gauges became dependent")

    def oriented_block(root, neighbour):
        if root < neighbour:
            return blocks[root, neighbour]
        return transpose(blocks[neighbour, root])

    def endpoint_blocks(root):
        if root <= 3:
            p_block = tuple((Q(0), Q(0), endpoint[root][row][0])
                            for row in colours)
            q_block = tuple((Q(0), Q(0), endpoint[root][row][1])
                            for row in colours)
            return p_block, q_block
        scale = Q(root - 2)
        return (
            ((scale, Q(0), Q(0)), (scale + 1, Q(0), Q(0))),
            ((Q(0), scale + 2, Q(0)), (Q(0), scale + 3, Q(0))),
        )

    planned = {
        0: ((1, 0), (2, 1)),
        1: ((0, 0), (2, 1)),
        2: ((1, 0), (0, 1)),
        3: ((1, 0), (2, 1)),
    }
    witness_table = {}
    for root in SITES:
        p_block, q_block = endpoint_blocks(root)
        incident = {
            f"r{neighbour}": oriented_block(root, neighbour)
            for neighbour in SITES if neighbour != root
        }
        incident["p"] = p_block
        incident["q"] = q_block
        pure = {
            output: tuple(label for label, block in incident.items()
                          if R2_GUARD["pure_column"](block, output))
            for output in colours
        }
        preserves_pair = not any(
            endpoint[root][row][column]
            for row, column in product(colours, repeat=2)
        )
        if root in planned:
            require(not preserves_pair,
                    ("a nonzero all-spokes root preserved the pair", root))
            for neighbour, output in planned[root]:
                require(f"r{neighbour}" in pure[output],
                        ("a planned all-spokes R2 witness vanished",
                         root, neighbour, output, pure))
        else:
            require(preserves_pair and "p" in pure[0] and "q" in pure[1],
                    ("a zero all-spokes root lost pair preservation",
                     root, pure))
        witness_table[root] = (preserves_pair, pure)

    # Every planned internal witness has a live complementary four-site
    # cofactor; in fact all 64 binary cofactor words are nonzero here.
    cofactor_counts = {}
    for root, witnesses in planned.items():
        for neighbour, output in witnesses:
            pair = edge(root, neighbour)
            live = sum(
                R2_GUARD["cofactor"](packet, word, *pair) != 0
                for word in words
            )
            require(live == 64,
                    ("an all-spokes R2 cofactor vanished",
                     root, neighbour, output, live))
            cofactor_counts[root, neighbour, output] = live

    return {
        "endpoint_ranks": ranks,
        "potential": potential,
        "selected_level_two_rows": len(words),
        "differential_ranks": differential_ranks,
        "literal_r2_roots": len(witness_table),
        "internal_r2_cofactor_counts": cofactor_counts,
    }


def audit_final_frontier(census, zero_pencil, split_k23,
                         two_zero_fixed_root, dense, guard):
    expected = {
        "all-spokes": {
            "quotient_supports": 1,
            "labelled_supports": 1,
            "status": "residual",
        },
    }
    require(zero_pencil["rank_bound"] == 42
            and split_k23["rank_bound"] == 51
            and two_zero_fixed_root["rank_bound"] == 42,
            ("dense closure bounds changed", zero_pencil, split_k23,
             two_zero_fixed_root))
    require(census["support_closed_quotient"] + 3 == 36,
            ("closed quotient count changed", census))
    require(sum(data["labelled_supports"] for data in expected.values()) == 1,
            "final labelled residual count changed")
    require(set(expected).issubset(dense),
            ("final residual disappeared from dense census", dense))
    require(guard["differential_ranks"] == (55, 55, 55)
            and guard["literal_r2_roots"] == 6,
            ("final all-spokes guard changed", guard))
    return {
        "closed_quotient_supports": 36,
        "closed_labelled_supports": 146,
        "residual_quotient_supports": 1,
        "residual_labelled_supports": 1,
        "residual": expected,
    }


def main():
    census, quotient = audit_potential_support_census()
    zero_pencil = audit_five_site_zero_pencil_closure(quotient)
    split_k23 = audit_split_k23_boundary_closure(quotient)
    two_zero_fixed_root = audit_two_zero_rank_one_fixed_root_closure(quotient)
    dense, representatives, r2_root_zero = audit_exact_residual(quotient)
    guard = audit_all_spokes_rank55_r2_guard()
    frontier = audit_final_frontier(
        census, zero_pencil, split_k23, two_zero_fixed_root, dense, guard
    )
    print("1I+3R+2Z potential boundary audit passed")
    print("census:", census)
    print("five-site zero pencil:", zero_pencil)
    print("split K23 boundary:", split_k23)
    print("two-zero-R fixed root:", two_zero_fixed_root)
    print("dense representatives:", representatives)
    print("root-0 literal R2:", r2_root_zero)
    print("all-spokes rank-55/R2 guard:", guard)
    print("final frontier:", frontier)


if __name__ == "__main__":
    main()
