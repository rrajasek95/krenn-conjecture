#!/usr/bin/env python3
"""Balanced-K2,2 closure inside the 2I+4R endpoint stratum.

For the zero-multiplier graph K2,2 on the four rank-one endpoint sites,
the generic-kernel equation has a paired-shore normal form.  Two exact
rectangle tangents supplement the five universal vertex gauges, so
rank(dPsi) <= 53.  An exact physical-coordinate packet has rank 52 and
literal residual R2 witnesses at all six roots.

The local output changes used to derive the normal form preserve only
differential rank.  The R2 audit is performed before those changes, in
the displayed physical coordinates.  Standard library only.
"""

from fractions import Fraction as Q
from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


SITES = tuple(range(6))
COLOURS = (0, 1)
EDGES = tuple(combinations(SITES, 2))
CELLS = tuple(
    (u, v, a, b)
    for u, v in EDGES
    for a, b in product(COLOURS, repeat=2)
)
WORDS = tuple(product(COLOURS, repeat=6))
J = ((Q(0), Q(1)), (Q(1), Q(0)))


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


def transpose(matrix):
    return tuple(
        tuple(matrix[column][row] for column in COLOURS)
        for row in COLOURS
    )


def matrix_product(left, right):
    return tuple(
        tuple(
            sum(left[row][middle] * right[middle][column]
                for middle in COLOURS)
            for column in COLOURS
        )
        for row in COLOURS
    )


def determinant(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def matrix_rank(matrix):
    if not any(value for row in matrix for value in row):
        return 0
    return 2 if determinant(matrix) else 1


def outer(left, right):
    return tuple(
        tuple(left[row] * right[column] for column in COLOURS)
        for row in COLOURS
    )


def scale_matrix(coefficient, matrix):
    return tuple(
        tuple(coefficient * matrix[row][column] for column in COLOURS)
        for row in COLOURS
    )


def packet_from_blocks(blocks):
    return {
        (u, v, a, b): blocks[u, v][a][b]
        for u, v in EDGES
        for a, b in product(COLOURS, repeat=2)
    }


def hafnian(packet, vertices, word):
    total = Q(0)
    for matching in MATCHINGS[tuple(sorted(vertices))]:
        term = Q(1)
        for u, v in matching:
            term *= packet[u, v, word[u], word[v]]
        total += term
    return total


def matching_tensor(packet):
    return [hafnian(packet, SITES, word) for word in WORDS]


def cofactor(packet, word, u, v):
    remaining = tuple(site for site in SITES if site not in (u, v))
    return hafnian(packet, remaining, word)


def apply_differential(packet, tangent):
    return [
        sum(
            tangent[u, v, word[u], word[v]]
            * cofactor(packet, word, u, v)
            for u, v in EDGES
        )
        for word in WORDS
    ]


def differential_matrix(packet):
    return [
        [
            cofactor(packet, word, u, v)
            if (word[u], word[v]) == (a, b) else Q(0)
            for u, v, a, b in CELLS
        ]
        for word in WORDS
    ]


def rational_rank(matrix):
    rows = [[Q(value) for value in row] for row in matrix]
    rank = 0
    width = len(rows[0]) if rows else 0
    for column in range(width):
        pivot = next(
            (row for row in range(rank, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            multiple = rows[row][column]
            rows[row] = [
                left - multiple * right
                for left, right in zip(rows[row], rows[rank])
            ]
        rank += 1
    return rank


def modular_rank(matrix, prime):
    rows = [[
        value.numerator * pow(value.denominator, -1, prime) % prime
        if isinstance(value, Q) else value % prime
        for value in row
    ] for row in matrix]
    rank = 0
    width = len(rows[0]) if rows else 0
    for column in range(width):
        pivot = next(
            (row for row in range(rank, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column], -1, prime)
        rows[rank] = [value * inverse % prime for value in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            multiple = rows[row][column]
            rows[row] = [
                (left - multiple * right) % prime
                for left, right in zip(rows[row], rows[rank])
            ]
        rank += 1
    return rank


# ---------------------------------------------------------------------------
# Formal paired-shore normal form and its two extra kernel directions.


def constant(value):
    return {(): Q(value)} if value else {}


def variable(name):
    return {(name,): Q(1)}


def polynomial_add(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, Q(0)) + coefficient
            if not answer[monomial]:
                del answer[monomial]
    return answer


def polynomial_scale(coefficient, polynomial):
    return {
        monomial: coefficient * value
        for monomial, value in polynomial.items()
        if coefficient * value
    }


def polynomial_multiply(*polynomials):
    answer = constant(1)
    for polynomial in polynomials:
        updated = {}
        for left_monomial, left_coefficient in answer.items():
            for right_monomial, right_coefficient in polynomial.items():
                monomial = tuple(sorted(left_monomial + right_monomial))
                updated[monomial] = (
                    updated.get(monomial, Q(0))
                    + left_coefficient * right_coefficient
                )
                if not updated[monomial]:
                    del updated[monomial]
        answer = updated
    return answer


ZERO_MATRIX = (({}, {}), ({}, {}))
E0 = (constant(1), constant(0))


def formal_vector(prefix):
    return tuple(variable(f"{prefix}{row}") for row in COLOURS)


def formal_matrix(prefix):
    return tuple(
        tuple(variable(f"{prefix}{row}{column}") for column in COLOURS)
        for row in COLOURS
    )


def formal_outer(left, right):
    return tuple(
        tuple(polynomial_multiply(left[row], right[column])
              for column in COLOURS)
        for row in COLOURS
    )


def formal_scale(coefficient, matrix):
    return tuple(
        tuple(polynomial_scale(coefficient, matrix[row][column])
              for column in COLOURS)
        for row in COLOURS
    )


def formal_packet_from_blocks(blocks):
    return {
        (u, v, a, b): blocks[u, v][a][b]
        for u, v in EDGES
        for a, b in product(COLOURS, repeat=2)
    }


def formal_hafnian(packet, vertices, word):
    terms = []
    for matching in MATCHINGS[tuple(sorted(vertices))]:
        terms.append(polynomial_multiply(*(
            packet[u, v, word[u], word[v]] for u, v in matching
        )))
    return polynomial_add(*terms)


def formal_apply_differential(packet, tangent):
    answer = []
    for word in WORDS:
        terms = []
        for u, v in EDGES:
            value = tangent[u, v, word[u], word[v]]
            if not value:
                continue
            remaining = tuple(site for site in SITES if site not in (u, v))
            terms.append(polynomial_multiply(
                value, formal_hafnian(packet, remaining, word)
            ))
        answer.append(polynomial_add(*terms))
    return answer


def paired_shore_normal_form():
    p = formal_vector("p")
    q = formal_vector("q")
    r = formal_vector("r")
    s = formal_vector("s")
    blocks = {(0, 1): formal_matrix("A")}
    for site in (2, 3):
        blocks[0, site] = formal_outer(p, E0)
        blocks[1, site] = formal_outer(q, E0)
    for site in (4, 5):
        blocks[0, site] = formal_outer(r, E0)
        blocks[1, site] = formal_outer(s, E0)
    blocks[2, 3] = formal_outer(
        (variable("alpha"), constant(0)), E0
    )
    blocks[4, 5] = formal_outer(
        (variable("beta"), constant(0)), E0
    )
    for u, v in ((2, 4), (2, 5), (3, 4), (3, 5)):
        blocks[u, v] = formal_matrix(f"B{u}{v}")

    tangents = []
    for assignments in (
        {
            (0, 2): formal_outer(r, E0),
            (0, 3): formal_scale(-1, formal_outer(r, E0)),
            (1, 2): formal_scale(-1, formal_outer(s, E0)),
            (1, 3): formal_outer(s, E0),
        },
        {
            (0, 4): formal_outer(p, E0),
            (0, 5): formal_scale(-1, formal_outer(p, E0)),
            (1, 4): formal_scale(-1, formal_outer(q, E0)),
            (1, 5): formal_outer(q, E0),
        },
    ):
        tangent_blocks = {edge: ZERO_MATRIX for edge in EDGES}
        tangent_blocks.update(assignments)
        tangents.append(formal_packet_from_blocks(tangent_blocks))
    return formal_packet_from_blocks(blocks), tuple(tangents)


def audit_formal_extra_kernel():
    packet, tangents = paired_shore_normal_form()
    checks = 0
    for index, tangent in enumerate(tangents):
        residual = formal_apply_differential(packet, tangent)
        require(not any(residual),
                ("a formal paired-shore tangent left the kernel", index))
        checks += len(residual)
    return checks


def normal_form_numeric_packet():
    e0 = (Q(1), Q(0))
    p, q = (Q(2), Q(3)), (Q(5), Q(7))
    r, s = (Q(11), Q(13)), (Q(17), Q(19))
    blocks = {(0, 1): ((Q(23), Q(29)), (Q(31), Q(37)))}
    for site in (2, 3):
        blocks[0, site] = outer(p, e0)
        blocks[1, site] = outer(q, e0)
    for site in (4, 5):
        blocks[0, site] = outer(r, e0)
        blocks[1, site] = outer(s, e0)
    blocks[2, 3] = scale_matrix(Q(41), outer(e0, e0))
    blocks[4, 5] = scale_matrix(Q(43), outer(e0, e0))
    for edge, entries in zip(
        ((2, 4), (2, 5), (3, 4), (3, 5)),
        range(47, 63, 4),
    ):
        blocks[edge] = (
            (Q(entries), Q(entries + 1)),
            (Q(entries + 2), Q(entries + 3)),
        )
    return blocks, (p, q, r, s)


def tangent_from_blocks(blocks):
    return packet_from_blocks({
        edge: blocks.get(edge, ((Q(0), Q(0)), (Q(0), Q(0))))
        for edge in EDGES
    })


def rectangle_tangents_numeric(vectors):
    p, q, r, s = vectors
    e0 = (Q(1), Q(0))
    return tuple(tangent_from_blocks(assignments) for assignments in (
        {
            (0, 2): outer(r, e0),
            (0, 3): scale_matrix(-1, outer(r, e0)),
            (1, 2): scale_matrix(-1, outer(s, e0)),
            (1, 3): outer(s, e0),
        },
        {
            (0, 4): outer(p, e0),
            (0, 5): scale_matrix(-1, outer(p, e0)),
            (1, 4): scale_matrix(-1, outer(q, e0)),
            (1, 5): outer(q, e0),
        },
    ))


def gauge_tangent(packet, mu):
    return {
        cell: (mu[cell[0]] + mu[cell[1]]) * packet[cell]
        for cell in CELLS
    }


def audit_kernel_independence():
    blocks, vectors = normal_form_numeric_packet()
    packet = packet_from_blocks(blocks)
    rectangles = rectangle_tangents_numeric(vectors)
    for index, tangent in enumerate(rectangles):
        require(not any(apply_differential(packet, tangent)),
                ("numeric rectangle tangent left the kernel", index))

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
        for tangent in tuple(gauges) + rectangles
    ]
    require(rational_rank(rows) == 7,
            "the five gauges and two rectangles lost independence")
    require(determinant((vectors[0], vectors[2])) != 0,
            "the open paired-shore independence witness closed")
    combined = rational_rank(rows)
    require(60 - combined == 53, "the paired-shore rank bound changed")
    return len(gauges), len(rectangles), combined, 60 - combined


# ---------------------------------------------------------------------------
# Exact rank-52 physical-coordinate calibration with literal R2.


X = {
    0: ((Q(1), Q(-1)), (Q(73), Q(84))),
    1: ((Q(63), Q(39)), (Q(1), Q(1))),
    2: ((Q(1), Q(1)), (Q(0), Q(0))),
    3: ((Q(1), Q(1)), (Q(0), Q(0))),
    4: ((Q(0), Q(0)), (Q(1), Q(-1))),
    5: ((Q(0), Q(0)), (Q(1), Q(-1))),
}
RHO = (1, 1, 2, 2, -2, -2)
NU = tuple(Q(value, 2) for value in RHO)
Z_VALUE = -sum(NU)
FREE = {
    (2, 4): ((Q(98), Q(47)), (Q(30), Q(13))),
    (2, 5): ((Q(13), Q(52)), (Q(82), Q(92))),
    (3, 4): ((Q(87), Q(72)), (Q(35), Q(35))),
    (3, 5): ((Q(91), Q(46)), (Q(58), Q(43))),
}


def build_exact_blocks():
    blocks = {}
    numerators = {}
    for u, v in EDGES:
        numerator = matrix_product(matrix_product(X[u], J), transpose(X[v]))
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
    require(zero_graph == frozenset(FREE),
            ("the balanced K2,2 potential graph changed", zero_graph))
    require(Z_VALUE == Q(-1), "the direct rare-cell value changed")

    checked = 0
    for u, v in EDGES:
        for a, b in product(COLOURS, repeat=2):
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
    require(ranks == (52, 52, 52),
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
    0: ((2, 0), (4, 1)),
    1: ((2, 0), (4, 1)),
    2: ((3, 0), (0, 1)),
    3: ((2, 0), (0, 1)),
    4: ((1, 0), (5, 1)),
    5: ((1, 0), (4, 1)),
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
    formal_checks = audit_formal_extra_kernel()
    kernel_dimensions = audit_kernel_independence()
    generic_checks, slope_support = audit_exact_generic_kernel()
    ranks = audit_exact_rank()
    r2 = audit_physical_r2()
    print("2I+4R balanced-K2,2 closure: all checks passed")
    print(f"  formal rectangle identities : {formal_checks}")
    print(f"  gauges/rectangles/kernel/bound: {kernel_dimensions}")
    print(f"  generic-kernel scalar rows  : {generic_checks}/60")
    print(f"  selected L2 rows/support    : 64/64, {slope_support}/64")
    print(f"  calibration differential rank: {ranks}")
    print(f"  literal physical R2 roots   : {len(r2)}/6")


if __name__ == "__main__":
    main()
