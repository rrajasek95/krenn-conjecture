#!/usr/bin/env python3
"""All-zero potential closure inside the 2I+4R endpoint stratum.

Four zero rank-one potentials force their source factors onto one common
isotropic line.  After rank-preserving local output bases, the two
invertible sites have constant spokes to the four-site shore.  A
four-parameter cross-spoke cancellation family supplements the five vertex
gauges with three new directions modulo their one-dimensional intersection,
so rank(dPsi) <= 52.

An exact physical-coordinate packet has rank 42 and literal residual R2 at
all six roots.  The R2 audit does not use the normalizing bases.  Standard
library only.
"""

from fractions import Fraction as Q
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
core = run_path(str(
    HERE
    / "verify_level_two_two_invertible_four_rank_one_balanced_k22_closure.py"
))

SITES = core["SITES"]
COLOURS = core["COLOURS"]
EDGES = core["EDGES"]
CELLS = core["CELLS"]
WORDS = core["WORDS"]
MATCHINGS = core["MATCHINGS"]
J = core["J"]
constant = core["constant"]
variable = core["variable"]
polynomial_add = core["polynomial_add"]
polynomial_scale = core["polynomial_scale"]
polynomial_multiply = core["polynomial_multiply"]
formal_matrix = core["formal_matrix"]
formal_outer = core["formal_outer"]
formal_packet_from_blocks = core["formal_packet_from_blocks"]
formal_hafnian = core["formal_hafnian"]
formal_apply_differential = core["formal_apply_differential"]
ZERO_MATRIX = core["ZERO_MATRIX"]
transpose = core["transpose"]
matrix_product = core["matrix_product"]
matrix_rank = core["matrix_rank"]
outer = core["outer"]
scale_matrix = core["scale_matrix"]
packet_from_blocks = core["packet_from_blocks"]
matching_tensor = core["matching_tensor"]
apply_differential = core["apply_differential"]
differential_matrix = core["differential_matrix"]
rational_rank = core["rational_rank"]
modular_rank = core["modular_rank"]

INNER = (0, 1)
SHORE = (2, 3, 4, 5)
SHORE_EDGES = tuple(
    (u, v) for u in SHORE for v in SHORE if u < v
)
E0 = (constant(1), constant(0))


def audit_common_isotropic_line():
    # If b=(x,y), its J-orthogonal line is spanned by k=(x,-y).
    # Two nonzero vectors c*k,d*k on that line pair to -2cdxy.
    x, y = variable("x"), variable("y")
    c, d = variable("c"), variable("d")
    pairing = polynomial_add(
        polynomial_multiply(c, x, d, polynomial_scale(-1, y)),
        polynomial_multiply(c, polynomial_scale(-1, y), d, x),
    )
    expected = polynomial_scale(-2, polynomial_multiply(c, d, x, y))
    require(pairing == expected,
            "the common-isotropic-line pairing identity changed")

    branches = []
    for b in ((Q(1), Q(0)), (Q(0), Q(1))):
        orthogonal = (b[0], -b[1])
        require(b[0] * orthogonal[1] - b[1] * orthogonal[0] == 0,
                "an isotropic orthogonal line failed to coincide")
        branches.append((b, orthogonal))
    return tuple(branches)


def formal_constant_spoke_packet():
    c_block = formal_matrix("C")
    p = tuple(variable(f"p{row}") for row in COLOURS)
    q = tuple(variable(f"q{row}") for row in COLOURS)
    blocks = {(0, 1): c_block}
    for shore in SHORE:
        blocks[0, shore] = formal_outer(p, E0)
        blocks[1, shore] = formal_outer(q, E0)
    for u, v in SHORE_EDGES:
        blocks[u, v] = formal_matrix(f"B{u}{v}")
    return blocks, formal_packet_from_blocks(blocks), p, q


def audit_constant_spoke_factorization():
    blocks, packet, p, q = formal_constant_spoke_packet()
    checked = 0
    for word in WORDS:
        actual = formal_hafnian(packet, SITES, word)
        shore_word = word[2:]
        h = formal_hafnian(packet, SHORE, word)
        k_terms = []
        for u, v in SHORE_EDGES:
            complement = tuple(site for site in SHORE if site not in (u, v))
            if any(word[site] != 0 for site in complement):
                continue
            k_terms.append(polynomial_scale(
                2, blocks[u, v][word[u]][word[v]]
            ))
        k = polynomial_add(*k_terms)
        expected = polynomial_add(
            polynomial_multiply(blocks[0, 1][word[0]][word[1]], h),
            polynomial_multiply(p[word[0]], q[word[1]], k),
        )
        require(actual == expected,
                ("the constant-spoke factorization failed", word, shore_word))
        checked += 1
    return checked


def formal_cancellation_tangents(packet, p, q):
    answer = []
    for selected in SHORE:
        blocks = {edge: ZERO_MATRIX for edge in EDGES}
        blocks[0, selected] = formal_outer(p, E0)
        blocks[1, selected] = tuple(
            tuple(polynomial_scale(-1, value) for value in row)
            for row in formal_outer(q, E0)
        )
        answer.append(formal_packet_from_blocks(blocks))
    return tuple(answer)


def audit_formal_cancellation_kernel():
    _, packet, p, q = formal_constant_spoke_packet()
    tangents = formal_cancellation_tangents(packet, p, q)
    checked = 0
    for index, tangent in enumerate(tangents):
        residual = formal_apply_differential(packet, tangent)
        require(not any(residual),
                ("a constant-spoke cancellation left the kernel", index))
        checked += len(residual)
    return checked


def numeric_constant_spoke_packet():
    e0 = (Q(1), Q(0))
    p, q = (Q(2), Q(3)), (Q(5), Q(7))
    blocks = {(0, 1): ((Q(11), Q(13)), (Q(17), Q(19)))}
    for shore in SHORE:
        blocks[0, shore] = outer(p, e0)
        blocks[1, shore] = outer(q, e0)
    start = 23
    for edge in SHORE_EDGES:
        blocks[edge] = (
            (Q(start), Q(start + 1)),
            (Q(start + 2), Q(start + 3)),
        )
        start += 4
    return blocks, p, q


def tangent_from_blocks(blocks):
    zero = ((Q(0), Q(0)), (Q(0), Q(0)))
    return packet_from_blocks({
        edge: blocks.get(edge, zero) for edge in EDGES
    })


def gauge_tangent(packet, mu):
    return {
        cell: (mu[cell[0]] + mu[cell[1]]) * packet[cell]
        for cell in CELLS
    }


def audit_kernel_dimension():
    blocks, p, q = numeric_constant_spoke_packet()
    packet = packet_from_blocks(blocks)
    e0 = (Q(1), Q(0))
    cancellations = []
    for selected in SHORE:
        cancellations.append(tangent_from_blocks({
            (0, selected): outer(p, e0),
            (1, selected): scale_matrix(-1, outer(q, e0)),
        }))
    for index, tangent in enumerate(cancellations):
        require(not any(apply_differential(packet, tangent)),
                ("a numeric cancellation left the kernel", index))

    gauges = []
    for basis in range(5):
        mu = [Q(0)] * 6
        mu[basis] = Q(1)
        mu[5] = Q(-1)
        tangent = gauge_tangent(packet, mu)
        require(not any(apply_differential(packet, tangent)),
                ("a vertex gauge left the kernel", basis))
        gauges.append(tangent)
    rows = [
        [tangent[cell] for cell in CELLS]
        for tangent in tuple(gauges) + tuple(cancellations)
    ]
    combined = rational_rank(rows)
    require(combined == 8,
            "the gauge/cancellation kernel dimension changed")
    require(60 - combined == 52,
            "the all-zero rank bound changed")
    return len(gauges), len(cancellations), combined, 60 - combined


# ---------------------------------------------------------------------------
# Exact physical-coordinate rank-42/R2 calibration.


X = {
    0: ((Q(0), Q(1)), (Q(1), Q(0))),
    1: ((Q(1), Q(0)), (Q(0), Q(1))),
    2: ((Q(1), Q(0)), (Q(0), Q(0))),
    3: ((Q(0), Q(0)), (Q(1), Q(0))),
    4: ((Q(1), Q(0)), (Q(0), Q(0))),
    5: ((Q(0), Q(0)), (Q(1), Q(0))),
}
RHO = (1, 1, 0, 0, 0, 0)
NU = tuple(Q(value, 2) for value in RHO)
Z_VALUE = -sum(NU)
FREE = {
    (2, 3): ((Q(15), Q(52)), (Q(42), Q(21))),
    (2, 4): ((Q(94), Q(58)), (Q(38), Q(55))),
    (2, 5): ((Q(96), Q(97)), (Q(85), Q(12))),
    (3, 4): ((Q(80), Q(28)), (Q(56), Q(75))),
    (3, 5): ((Q(87), Q(92)), (Q(3), Q(37))),
    (4, 5): ((Q(78), Q(79)), (Q(24), Q(79))),
}


def build_exact_blocks():
    blocks = {}
    numerators = {}
    for u, v in EDGES:
        numerator = matrix_product(
            matrix_product(X[u], J), transpose(X[v])
        )
        numerators[u, v] = numerator
        weight = RHO[u] + RHO[v]
        if weight:
            blocks[u, v] = scale_matrix(Q(2, weight), numerator)
        else:
            require(not any(value for row in numerator for value in row),
                    ("a zero-multiplier numerator survived", u, v))
            blocks[u, v] = FREE[u, v]
    return blocks, numerators


BLOCKS, NUMERATORS = build_exact_blocks()
M = packet_from_blocks(BLOCKS)


def audit_exact_generic_kernel():
    require([matrix_rank(X[site]) for site in SITES] == [2, 2, 1, 1, 1, 1],
            "the physical endpoint rank pattern changed")
    zero_graph = frozenset(
        edge for edge in EDGES if RHO[edge[0]] + RHO[edge[1]] == 0
    )
    require(zero_graph == frozenset(SHORE_EDGES),
            ("the all-zero shore graph changed", zero_graph))
    require(Z_VALUE == Q(-1), "the direct rare-cell value changed")

    checked = 0
    for u, v in EDGES:
        for a in COLOURS:
            for b in COLOURS:
                require(
                    2 * NUMERATORS[u, v][a][b]
                    == (RHO[u] + RHO[v]) * BLOCKS[u, v][a][b],
                    ("the generic-kernel equation failed", u, v, a, b),
                )
                checked += 1
    n_packet = packet_from_blocks(NUMERATORS)
    slope = matching_tensor(M)
    response = apply_differential(M, n_packet)
    require(all(
        Z_VALUE * slope_value + response_value == 0
        for slope_value, response_value in zip(slope, response)
    ), "a selected level-two value row failed")
    return checked, sum(value != 0 for value in slope)


def audit_exact_rank():
    differential = differential_matrix(M)
    ranks = (
        rational_rank(differential),
        modular_rank(differential, 101),
        modular_rank(differential, 1_000_003),
    )
    require(ranks == (42, 42, 42),
            ("the calibration rank changed", ranks))
    return ranks


def orient_block(root, neighbour):
    if root < neighbour:
        return BLOCKS[root, neighbour]
    return transpose(BLOCKS[neighbour, root])


def pure_column(block, output):
    width = len(block[0])
    return (
        any(block[row][output] for row in COLOURS)
        and all(
            block[row][column] == 0
            for row in COLOURS
            for column in range(width)
            if column != output
        )
    )


def endpoint_blocks(root):
    return (
        tuple((Q(0), Q(0), X[root][row][0]) for row in COLOURS),
        tuple((Q(0), Q(0), X[root][row][1]) for row in COLOURS),
    )


EXPECTED_R2 = {
    0: ((2, 0), (3, 1)),
    1: ((2, 0), (3, 1)),
    2: ((0, 0), (1, 1)),
    3: ((0, 0), (1, 1)),
    4: ((0, 0), (1, 1)),
    5: ((0, 0), (1, 1)),
}


def audit_physical_r2():
    tables = {}
    for root in SITES:
        p_block, q_block = endpoint_blocks(root)
        require(tuple(p_block[row][2] for row in COLOURS)
                == tuple(X[root][row][0] for row in COLOURS),
                ("the physical p-star column changed", root))
        require(tuple(q_block[row][2] for row in COLOURS)
                == tuple(X[root][row][1] for row in COLOURS),
                ("the physical q-star column changed", root))
        incident = {
            neighbour: orient_block(root, neighbour)
            for neighbour in SITES if neighbour != root
        }
        incident["p"] = p_block
        incident["q"] = q_block
        pure = {
            output: tuple(
                label for label, block in incident.items()
                if pure_column(block, output)
            )
            for output in COLOURS
        }
        require(pure[0] and pure[1],
                ("R2 lacks one physical pure-column witness", root, pure))
        require(any(left != right for left in pure[0] for right in pure[1]),
                ("R2 witnesses are not distinct", root, pure))
        for neighbour, output in EXPECTED_R2[root]:
            require(neighbour in pure[output],
                    ("a planned physical R2 witness vanished", root, pure))
        tables[root] = pure
    return tables


def main():
    isotropic = audit_common_isotropic_line()
    factor_checks = audit_constant_spoke_factorization()
    kernel_checks = audit_formal_cancellation_kernel()
    kernel_dimensions = audit_kernel_dimension()
    generic_checks, slope_support = audit_exact_generic_kernel()
    ranks = audit_exact_rank()
    r2 = audit_physical_r2()
    print("2I+4R all-zero potential closure: all checks passed")
    print(f"  common-isotropic branches  : {isotropic}")
    print(f"  formal factor identities   : {factor_checks}")
    print(f"  formal kernel identities   : {kernel_checks}")
    print(f"  gauges/cancellations/kernel/bound: {kernel_dimensions}")
    print(f"  generic-kernel scalar rows : {generic_checks}/60")
    print(f"  selected L2 rows/support   : 64/64, {slope_support}/64")
    print(f"  calibration ranks          : {ranks}")
    print(f"  literal physical R2 roots  : {len(r2)}/6")


if __name__ == "__main__":
    main()
