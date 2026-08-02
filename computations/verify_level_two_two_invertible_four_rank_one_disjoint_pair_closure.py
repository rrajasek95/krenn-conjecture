#!/usr/bin/env python3
"""Sharp disjoint-pair closure inside the 2I+4R endpoint stratum.

When the zero-multiplier graph on the four rank-one sites is two disjoint
edges, local output bases put the residual packet in a paired support class.
Its support-preserving matching tensor factors through 24 parameters with
four exact reparametrization kernels.  The 28 transverse cells then give
rank(dPsi) <= 20 + 28 = 48.

An exact physical-coordinate packet attains rank 48 and has literal R2 at
all six roots.  The normalizing bases are used only for differential rank;
the R2 audit is physical.  Standard library only.
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
PAIR_A = (2, 3)
PAIR_B = (4, 5)
FREE_EDGES = frozenset((PAIR_A, PAIR_B))
NONFREE_SHORE = ((2, 4), (2, 5), (3, 4), (3, 5))
E0 = (constant(1), constant(0))


def formal_support_packet():
    blocks = {(0, 1): formal_matrix("C")}
    for inner in INNER:
        for shore in PAIR_A + PAIR_B:
            vector = tuple(
                variable(f"P{inner}{shore}{row}")
                for row in COLOURS
            )
            blocks[inner, shore] = formal_outer(vector, E0)
    blocks[PAIR_A] = formal_matrix("A")
    blocks[PAIR_B] = formal_matrix("B")
    for u, v in NONFREE_SHORE:
        blocks[u, v] = formal_outer(
            (variable(f"g{u}{v}"), constant(0)), E0
        )
    return blocks, formal_packet_from_blocks(blocks)


def audit_matching_factorization():
    blocks, packet = formal_support_packet()
    c_block = blocks[0, 1]
    a_block = blocks[PAIR_A]
    b_block = blocks[PAIR_B]

    f_tensor = {}
    g_tensor = {}
    h_tensor = {}
    for x0 in COLOURS:
        for x1 in COLOURS:
            inner_word = (x0, x1)
            f_tensor[inner_word] = polynomial_add(
                polynomial_multiply(
                    blocks[0, 2][x0][0], blocks[1, 3][x1][0]
                ),
                polynomial_multiply(
                    blocks[0, 3][x0][0], blocks[1, 2][x1][0]
                ),
            )
            g_tensor[inner_word] = polynomial_add(
                polynomial_multiply(
                    blocks[0, 4][x0][0], blocks[1, 5][x1][0]
                ),
                polynomial_multiply(
                    blocks[0, 5][x0][0], blocks[1, 4][x1][0]
                ),
            )
            zero_word = inner_word + (0, 0, 0, 0)
            value = formal_hafnian(packet, SITES, zero_word)
            h_tensor[inner_word] = polynomial_add(
                value,
                polynomial_scale(-1, polynomial_multiply(
                    c_block[x0][x1], a_block[0][0], b_block[0][0]
                )),
                polynomial_scale(-1, polynomial_multiply(
                    f_tensor[inner_word], b_block[0][0]
                )),
                polynomial_scale(-1, polynomial_multiply(
                    g_tensor[inner_word], a_block[0][0]
                )),
            )

    checked = 0
    for word in WORDS:
        inner_word = word[:2]
        pair_a_word = word[2:4]
        pair_b_word = word[4:6]
        actual = formal_hafnian(packet, SITES, word)
        expected = polynomial_add(
            polynomial_multiply(
                c_block[inner_word[0]][inner_word[1]],
                a_block[pair_a_word[0]][pair_a_word[1]],
                b_block[pair_b_word[0]][pair_b_word[1]],
            ),
            polynomial_multiply(
                f_tensor[inner_word],
                constant(pair_a_word == (0, 0)),
                b_block[pair_b_word[0]][pair_b_word[1]],
            ),
            polynomial_multiply(
                g_tensor[inner_word],
                a_block[pair_a_word[0]][pair_a_word[1]],
                constant(pair_b_word == (0, 0)),
            ),
            polynomial_multiply(
                h_tensor[inner_word],
                constant(pair_a_word == (0, 0)),
                constant(pair_b_word == (0, 0)),
            ),
        )
        require(actual == expected,
                ("the disjoint-pair factorization failed", word))
        checked += 1
    return checked


E_PAIR = tuple(constant(index == 0) for index in range(4))


def effective_vector(prefix):
    return tuple(variable(f"{prefix}{index}") for index in range(4))


def zero_effective_vector():
    return tuple({} for _ in range(4))


def negate_vector(vector):
    return tuple(polynomial_scale(-1, value) for value in vector)


def effective_tangent_residual(base, tangent):
    c, a, b, f, g, h = base
    dc, da, db, df, dg, dh = tangent
    answer = []
    for wi in range(4):
        for ui in range(4):
            for vi in range(4):
                answer.append(polynomial_add(
                    polynomial_multiply(dc[wi], a[ui], b[vi]),
                    polynomial_multiply(c[wi], da[ui], b[vi]),
                    polynomial_multiply(c[wi], a[ui], db[vi]),
                    polynomial_multiply(df[wi], E_PAIR[ui], b[vi]),
                    polynomial_multiply(f[wi], E_PAIR[ui], db[vi]),
                    polynomial_multiply(dg[wi], a[ui], E_PAIR[vi]),
                    polynomial_multiply(g[wi], da[ui], E_PAIR[vi]),
                    polynomial_multiply(dh[wi], E_PAIR[ui], E_PAIR[vi]),
                ))
    return answer


def effective_kernel_directions(base):
    c, a, b, f, g, h = base
    zero = zero_effective_vector()
    return (
        # Scale A, compensated in C and G.
        (negate_vector(c), a, zero, zero, negate_vector(g), zero),
        # Scale B, compensated in C and F.
        (negate_vector(c), zero, b, negate_vector(f), zero, zero),
        # Translate A by its distinguished e00 line.
        (zero, E_PAIR, zero, negate_vector(c), zero, negate_vector(g)),
        # Translate B by its distinguished e00 line.
        (zero, zero, E_PAIR, zero, negate_vector(c), negate_vector(f)),
    )


def audit_effective_kernel_and_dimensions():
    base = tuple(effective_vector(prefix) for prefix in "CABFGH")
    directions = effective_kernel_directions(base)
    checked = 0
    for index, direction in enumerate(directions):
        residual = effective_tangent_residual(base, direction)
        require(not any(residual),
                ("an effective reparametrization left the kernel", index))
        checked += len(residual)

    numeric = tuple(
        tuple(Q(7 * family + index + 1) for index in range(4))
        for family in range(6)
    )
    c, a, b, f, g, h = numeric
    e = (Q(1), Q(0), Q(0), Q(0))
    zero = (Q(0),) * 4
    numeric_directions = (
        (tuple(-x for x in c), a, zero, zero,
         tuple(-x for x in g), zero),
        (tuple(-x for x in c), zero, b, tuple(-x for x in f),
         zero, zero),
        (zero, e, zero, tuple(-x for x in c), zero,
         tuple(-x for x in g)),
        (zero, zero, e, zero, tuple(-x for x in c),
         tuple(-x for x in f)),
    )
    rows = [
        [entry for family in direction for entry in family]
        for direction in numeric_directions
    ]
    require(rational_rank(rows) == 4,
            "the four effective kernel directions became dependent")

    support_parameters = 4 + 16 + 8 + 4
    effective_parameters = 6 * 4
    effective_kernel = 4
    support_image_bound = effective_parameters - effective_kernel
    transverse_parameters = 60 - support_parameters
    total_bound = support_image_bound + transverse_parameters
    require((support_parameters, effective_parameters, effective_kernel,
             support_image_bound, transverse_parameters, total_bound)
            == (32, 24, 4, 20, 28, 48),
            "the disjoint-pair dimension count changed")
    return checked, (
        support_parameters,
        effective_parameters,
        effective_kernel,
        support_image_bound,
        transverse_parameters,
        total_bound,
    )


# ---------------------------------------------------------------------------
# Exact physical-coordinate rank-48/R2 calibration.


X = {
    0: ((Q(83), Q(98)), (Q(97), Q(19))),
    1: ((Q(70), Q(45)), (Q(6), Q(19))),
    2: ((Q(1), Q(1)), (Q(0), Q(0))),
    3: ((Q(0), Q(0)), (Q(1), Q(-1))),
    4: ((Q(1), Q(2)), (Q(0), Q(0))),
    5: ((Q(0), Q(0)), (Q(1), Q(-2))),
}
RHO = (1, 1, 2, -2, 3, -3)
NU = tuple(Q(value, 2) for value in RHO)
Z_VALUE = -sum(NU)
FREE = {
    (2, 3): ((Q(7), Q(89)), (Q(98), Q(2))),
    (4, 5): ((Q(9), Q(28)), (Q(70), Q(30))),
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
    require(zero_graph == FREE_EDGES,
            ("the disjoint-pair potential graph changed", zero_graph))
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
    require(ranks == (48, 48, 48),
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
    2: ((4, 0), (5, 1)),
    3: ((4, 0), (5, 1)),
    4: ((2, 0), (3, 1)),
    5: ((2, 0), (3, 1)),
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
    factor_checks = audit_matching_factorization()
    effective_checks, dimensions = audit_effective_kernel_and_dimensions()
    generic_checks, slope_support = audit_exact_generic_kernel()
    ranks = audit_exact_rank()
    r2 = audit_physical_r2()
    print("2I+4R disjoint-pair closure: all checks passed")
    print(f"  formal matching identities : {factor_checks}")
    print(f"  effective kernel identities: {effective_checks}")
    print(f"  support/effective/kernel/image/transverse/bound: {dimensions}")
    print(f"  generic-kernel scalar rows : {generic_checks}/60")
    print(f"  selected L2 rows/support   : 64/64, {slope_support}/64")
    print(f"  calibration ranks          : {ranks}")
    print(f"  literal physical R2 roots  : {len(r2)}/6")


if __name__ == "__main__":
    main()
