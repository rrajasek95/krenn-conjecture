#!/usr/bin/env python3
"""K1,3 zero-sum closure inside the 2I+4R endpoint stratum.

The generic-kernel equation puts a K1,3 zero-multiplier pattern in a
35-parameter star-shore support class.  Its matching tensor factors through
28 effective parameters with six exact scaling/translation kernels.  The
25 transverse cells give rank(dPsi) <= 22 + 25 = 47.

An exact physical-coordinate packet has rank 44 and literal residual R2 at
all roots.  Local output bases are used only for differential rank; the R2
audit remains in physical coordinates.  Standard library only.
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
scale_matrix = core["scale_matrix"]
packet_from_blocks = core["packet_from_blocks"]
matching_tensor = core["matching_tensor"]
apply_differential = core["apply_differential"]
differential_matrix = core["differential_matrix"]
rational_rank = core["rational_rank"]
modular_rank = core["modular_rank"]

INNER = (0, 1)
CENTER = 2
LEAVES = (3, 4, 5)
FREE_EDGES = frozenset((
    (CENTER, 3), (CENTER, 4), (CENTER, 5),
))
LEAF_EDGES = ((3, 4), (3, 5), (4, 5))
E0 = (constant(1), constant(0))


def formal_support_packet():
    blocks = {(0, 1): formal_matrix("C")}
    for inner in INNER:
        for shore in (CENTER,) + LEAVES:
            vector = tuple(
                variable(f"P{inner}{shore}{row}")
                for row in COLOURS
            )
            blocks[inner, shore] = formal_outer(vector, E0)
    for leaf in LEAVES:
        blocks[CENTER, leaf] = formal_matrix(f"A{leaf}")
    for u, v in LEAF_EDGES:
        blocks[u, v] = formal_outer(
            (variable(f"g{u}{v}"), constant(0)), E0
        )
    return blocks, formal_packet_from_blocks(blocks)


def audit_matching_factorization():
    blocks, packet = formal_support_packet()
    c_block = blocks[0, 1]
    g_tensors = {}
    h_tensor = {}
    for leaf in LEAVES:
        other = tuple(site for site in LEAVES if site != leaf)
        edge = tuple(sorted(other))
        gamma = blocks[edge][0][0]
        g_tensors[leaf] = {}
        for x0 in COLOURS:
            for x1 in COLOURS:
                inner_word = (x0, x1)
                crossed = polynomial_add(
                    polynomial_multiply(
                        blocks[0, other[0]][x0][0],
                        blocks[1, other[1]][x1][0],
                    ),
                    polynomial_multiply(
                        blocks[0, other[1]][x0][0],
                        blocks[1, other[0]][x1][0],
                    ),
                )
                g_tensors[leaf][inner_word] = polynomial_add(
                    polynomial_multiply(c_block[x0][x1], gamma),
                    crossed,
                )

    for x0 in COLOURS:
        for x1 in COLOURS:
            inner_word = (x0, x1)
            zero_word = inner_word + (0, 0, 0, 0)
            value = formal_hafnian(packet, SITES, zero_word)
            corrections = [value]
            for leaf in LEAVES:
                corrections.append(polynomial_scale(
                    -1,
                    polynomial_multiply(
                        g_tensors[leaf][inner_word],
                        blocks[CENTER, leaf][0][0],
                    ),
                ))
            h_tensor[inner_word] = polynomial_add(*corrections)

    checked = 0
    for word in WORDS:
        inner_word = word[:2]
        actual = formal_hafnian(packet, SITES, word)
        expected_terms = []
        for leaf in LEAVES:
            other = tuple(site for site in LEAVES if site != leaf)
            if any(word[site] != 0 for site in other):
                continue
            expected_terms.append(polynomial_multiply(
                g_tensors[leaf][inner_word],
                blocks[CENTER, leaf][word[CENTER]][word[leaf]],
            ))
        if word[2:] == (0, 0, 0, 0):
            expected_terms.append(h_tensor[inner_word])
        expected = polynomial_add(*expected_terms)
        require(actual == expected,
                ("the K1,3 matching factorization failed", word))
        checked += 1
    return checked


E_LOCAL = tuple(constant(index == 0) for index in range(4))


def effective_vector(prefix):
    return tuple(variable(f"{prefix}{index}") for index in range(4))


def zero_vector():
    return tuple({} for _ in range(4))


def negate(vector):
    return tuple(polynomial_scale(-1, value) for value in vector)


def embedded_local(local, leaf, shore_word):
    other = tuple(site for site in LEAVES if site != leaf)
    if any(shore_word[site - 2] != 0 for site in other):
        return {}
    local_index = 2 * shore_word[0] + shore_word[leaf - 2]
    return local[local_index]


def effective_tangent_residual(base, tangent):
    gs, h, star_blocks = base
    dgs, dh, dstar_blocks = tangent
    answer = []
    for wi in range(4):
        for shore_word in (
            (a, b, c, d)
            for a in COLOURS for b in COLOURS
            for c in COLOURS for d in COLOURS
        ):
            terms = []
            for index, leaf in enumerate(LEAVES):
                star_value = embedded_local(
                    star_blocks[index], leaf, shore_word
                )
                dstar_value = embedded_local(
                    dstar_blocks[index], leaf, shore_word
                )
                terms.extend((
                    polynomial_multiply(dgs[index][wi], star_value),
                    polynomial_multiply(gs[index][wi], dstar_value),
                ))
            if shore_word == (0, 0, 0, 0):
                terms.append(dh[wi])
            answer.append(polynomial_add(*terms))
    return answer


def effective_kernel_directions(base):
    gs, h, star_blocks = base
    zero = zero_vector()
    directions = []
    for index in range(3):
        dgs = [zero, zero, zero]
        dstars = [zero, zero, zero]
        dgs[index] = negate(gs[index])
        dstars[index] = star_blocks[index]
        directions.append((tuple(dgs), zero, tuple(dstars)))
    for index in range(3):
        dgs = (zero, zero, zero)
        dstars = [zero, zero, zero]
        dstars[index] = E_LOCAL
        directions.append((dgs, negate(gs[index]), tuple(dstars)))
    return tuple(directions)


def audit_effective_kernel_and_dimensions():
    gs = tuple(effective_vector(f"G{index}") for index in range(3))
    h = effective_vector("H")
    star_blocks = tuple(
        effective_vector(f"A{index}") for index in range(3)
    )
    base = (gs, h, star_blocks)
    directions = effective_kernel_directions(base)
    checked = 0
    for index, direction in enumerate(directions):
        residual = effective_tangent_residual(base, direction)
        require(not any(residual),
                ("an effective star reparametrization survived", index))
        checked += len(residual)

    numeric_gs = tuple(
        tuple(Q(10 * index + coordinate + 2) for coordinate in range(4))
        for index in range(3)
    )
    numeric_stars = tuple(
        tuple(Q(20 + 10 * index + coordinate) for coordinate in range(4))
        for index in range(3)
    )
    e = (Q(1), Q(0), Q(0), Q(0))
    zero = (Q(0),) * 4
    rows = []
    for index in range(3):
        dg = [zero, zero, zero]
        da = [zero, zero, zero]
        dg[index] = tuple(-value for value in numeric_gs[index])
        da[index] = numeric_stars[index]
        rows.append([
            entry for family in tuple(dg) + (zero,) + tuple(da)
            for entry in family
        ])
    for index in range(3):
        da = [zero, zero, zero]
        da[index] = e
        rows.append([
            entry
            for family in (zero, zero, zero,
                           tuple(-value for value in numeric_gs[index]))
            + tuple(da)
            for entry in family
        ])
    require(rational_rank(rows) == 6,
            "the six effective star kernels became dependent")

    support_parameters = 4 + 16 + 12 + 3
    effective_parameters = 7 * 4
    effective_kernel = 6
    support_image_bound = effective_parameters - effective_kernel
    transverse_parameters = 60 - support_parameters
    total_bound = support_image_bound + transverse_parameters
    require((support_parameters, effective_parameters, effective_kernel,
             support_image_bound, transverse_parameters, total_bound)
            == (35, 28, 6, 22, 25, 47),
            "the K1,3 dimension count changed")
    return checked, (
        support_parameters,
        effective_parameters,
        effective_kernel,
        support_image_bound,
        transverse_parameters,
        total_bound,
    )


# ---------------------------------------------------------------------------
# Exact physical-coordinate rank-44/R2 calibration.


X = {
    0: ((Q(1), Q(1)), (Q(-1), Q(1))),
    1: ((Q(1), Q(-1)), (Q(1), Q(1))),
    2: ((Q(1), Q(1)), (Q(0), Q(0))),
    3: ((Q(0), Q(0)), (Q(1), Q(-1))),
    4: ((Q(1), Q(-1)), (Q(0), Q(0))),
    5: ((Q(0), Q(0)), (Q(1), Q(-1))),
}
RHO = (1, 1, 2, -2, -2, -2)
NU = tuple(Q(value, 2) for value in RHO)
Z_VALUE = -sum(NU)
FREE = {
    (2, 3): ((Q(61), Q(69)), (Q(41), Q(69))),
    (2, 4): ((Q(63), Q(99)), (Q(10), Q(69))),
    (2, 5): ((Q(60), Q(6)), (Q(74), Q(51))),
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
            ("the K1,3 potential graph changed", zero_graph))
    require(Z_VALUE == Q(1), "the direct rare-cell value changed")

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
    require(ranks == (44, 44, 44),
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
    3: ((1, 0), (0, 1)),
    4: ((1, 0), (0, 1)),
    5: ((1, 0), (0, 1)),
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
    print("2I+4R K1,3 closure: all checks passed")
    print(f"  formal matching identities : {factor_checks}")
    print(f"  effective kernel identities: {effective_checks}")
    print(f"  support/effective/kernel/image/transverse/bound: {dimensions}")
    print(f"  generic-kernel scalar rows : {generic_checks}/60")
    print(f"  selected L2 rows/support   : 64/64, {slope_support}/64")
    print(f"  calibration ranks          : {ranks}")
    print(f"  literal physical R2 roots  : {len(r2)}/6")


if __name__ == "__main__":
    main()
