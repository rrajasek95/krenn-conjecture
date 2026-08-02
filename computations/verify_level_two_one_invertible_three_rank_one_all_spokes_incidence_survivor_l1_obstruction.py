#!/usr/bin/env python3
"""Audit an exact L0-incidence survivor in the 1I+3R+2Z all-spokes envelope.

The preceding endpoint-compatibility audit leaves the necessary exceptional
profile rank(D)=55 and rank(D_mixed)=53, with both pure rows incident to the
image.  This checker gives an exact packet with that profile.  It is obtained
from a pinned all-spokes packet by changing the single entry M_34(0,1) from
3 to 0.  Exact maximal minors, rational pure-target preimages, the five gauge
directions, generic-kernel equations, and literal R2 witnesses are audited.

The packet is a genuine linear-L0 survivor, but not a full endpoint survivor:
the two overlapping L1 systems each have only two genuine star modes, and the
span of all four compatible factored products misses both pure targets.  The
same conclusion holds on the nonzero local diagonal torus through the packet.

Research evidence only.  Standard library; checks stay live under -O/-I -S.
"""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
SOURCE = run_path(str(
    HERE
    / "verify_level_two_one_invertible_three_rank_one_two_zero_potential_boundary.py"
))
CORE = SOURCE["R2_GUARD"]

SITES = tuple(range(6))
NONZERO = (0, 1, 2, 3)
ZEROS = (4, 5)
COLOURS = (0, 1)
EDGES = tuple(combinations(SITES, 2))
WORDS = tuple(product(COLOURS, repeat=6))
J = CORE["J"]

REFERENCE_SPOKES = {
    (0, 4): ((1, 85), (0, 87)),
    (0, 5): ((84, 87), (0, 28)),
    (1, 4): ((0, 74), (0, 66)),
    (1, 5): ((0, 76), (37, 0)),
    (2, 4): ((0, 46), (0, 23)),
    (2, 5): ((56, 0), (0, 0)),
    (3, 4): ((0, 3), (29, 0)),
    (3, 5): ((0, 51), (0, 96)),
}
SURVIVOR_SPOKES = dict(REFERENCE_SPOKES)
SURVIVOR_SPOKES[3, 4] = ((0, 0), (29, 0))

D_MINOR_ROWS = (
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
    18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
    35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 50, 51,
    56, 58, 59, 60, 63,
)
D_MINOR_COLUMNS = (
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
    18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
    35, 36, 37, 38, 40, 41, 42, 43, 45, 46, 47, 48, 49, 51, 52, 53,
    54, 56, 57, 58, 59,
)
MIXED_MINOR_ROWS = (
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
    18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
    35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 49, 50, 55,
    57, 58, 59,
)
MIXED_MINOR_COLUMNS = (
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
    18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
    35, 36, 37, 38, 40, 41, 42, 43, 45, 46, 47, 48, 49, 51, 52, 53,
    54, 56, 57,
)


def outer(left, right):
    return tuple(
        tuple(Q(left[row]) * Q(right[column]) for column in COLOURS)
        for row in COLOURS
    )


def transpose(matrix):
    return tuple(tuple(matrix[row][column] for row in COLOURS)
                 for column in COLOURS)


def build_packet(spokes):
    endpoint = {
        0: ((Q(-1), Q(2)), (Q(1), Q(-1))),
        1: outer((1, 0), (1, 1)),
        2: outer((0, 1), (1, 2)),
        3: outer((1, 1), (2, 3)),
        4: ((Q(0), Q(0)), (Q(0), Q(0))),
        5: ((Q(0), Q(0)), (Q(0), Q(0))),
    }
    potential = (Q(1), Q(1), Q(1), Q(1), Q(-1), Q(-1))
    blocks = {}
    numerators = {}
    for left, right in EDGES:
        numerator = CORE["matrix_product"](
            CORE["matrix_product"](endpoint[left], J),
            transpose(endpoint[right]),
        )
        numerators[left, right] = numerator
        denominator = potential[left] + potential[right]
        if denominator:
            block = tuple(
                tuple(Q(numerator[a][b]) / denominator for b in COLOURS)
                for a in COLOURS
            )
        elif (left, right) == (4, 5):
            block = ((Q(0), Q(0)), (Q(0), Q(0)))
        else:
            block = tuple(tuple(Q(value) for value in row)
                          for row in spokes[left, right])
        blocks[left, right] = block
        require(numerator == tuple(
            tuple(denominator * block[a][b] for b in COLOURS)
            for a in COLOURS
        ), ("generic-kernel block identity failed", left, right))
    return (
        endpoint,
        potential,
        blocks,
        numerators,
        CORE["packet_from_blocks"](blocks),
    )


def modularize(matrix, prime):
    return [
        [int(Q(value).numerator
             * pow(Q(value).denominator, -1, prime) % prime)
         for value in row]
        for row in matrix
    ]


def ranks_over_fields(matrix):
    return (
        CORE["rational_rank"](matrix),
        CORE["modular_rank"](modularize(matrix, 101), 101),
        CORE["modular_rank"](modularize(matrix, 32_003), 32_003),
        CORE["modular_rank"](
            modularize(matrix, 1_000_003), 1_000_003
        ),
    )


def pure_targets():
    return (
        [Q(word == (0,) * 6) for word in WORDS],
        [Q(word == (1,) * 6) for word in WORDS],
    )


def append_columns(matrix, *columns):
    require(all(len(column) == len(matrix) for column in columns),
            "an augmented column has the wrong height")
    return [
        list(row) + [column[index] for column in columns]
        for index, row in enumerate(matrix)
    ]


def exact_determinant(matrix):
    rows = [[Q(value) for value in row] for row in matrix]
    require(rows and len(rows) == len(rows[0]),
            "determinant input is not square")
    answer = Q(1)
    for column in range(len(rows)):
        pivot = next(
            (row for row in range(column, len(rows))
             if rows[row][column]),
            None,
        )
        require(pivot is not None, "the pinned maximal minor vanished")
        if pivot != column:
            rows[column], rows[pivot] = rows[pivot], rows[column]
            answer = -answer
        value = rows[column][column]
        answer *= value
        for row in range(column + 1, len(rows)):
            if not rows[row][column]:
                continue
            multiple = rows[row][column] / value
            for slot in range(column + 1, len(rows)):
                rows[row][slot] -= multiple * rows[column][slot]
    return answer


def pinned_minor(matrix, selected_rows, selected_columns, expected_digest):
    require(len(selected_rows) == len(selected_columns),
            "a pinned minor is not square")
    minor = [
        [matrix[row][column] for column in selected_columns]
        for row in selected_rows
    ]
    determinant = exact_determinant(minor)
    require(determinant != 0, "a pinned maximal minor became singular")
    digest = sha256(str(determinant).encode()).hexdigest()
    require(digest == expected_digest,
            ("a pinned maximal minor changed", digest))
    return determinant, digest


def solve_linear_system(matrix, target):
    rows = [
        [Q(value) for value in row] + [Q(rhs)]
        for row, rhs in zip(matrix, target)
    ]
    width = len(matrix[0])
    rank = 0
    pivots = []
    for column in range(width):
        pivot = next(
            (row for row in range(rank, len(rows))
             if rows[row][column]),
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
        pivots.append(column)
        rank += 1
    require(all(any(row[:width]) or not row[width] for row in rows),
            "a pure target left the differential image")
    solution = [Q(0)] * width
    for row, column in enumerate(pivots):
        solution[column] = rows[row][width]
    require([
        sum(value * solution[column]
            for column, value in enumerate(row))
        for row in matrix
    ] == list(target), "the rational preimage check failed")
    return rank, tuple(pivots), tuple(solution)


def audit_one_cell_repair():
    changes = []
    for edge in SURVIVOR_SPOKES:
        for row, column in product(COLOURS, repeat=2):
            before = REFERENCE_SPOKES[edge][row][column]
            after = SURVIVOR_SPOKES[edge][row][column]
            if before != after:
                changes.append((edge, row, column, before, after))
    require(changes == [((3, 4), 0, 1, 3, 0)],
            ("the one-cell incidence repair changed", changes))

    reference = build_packet(REFERENCE_SPOKES)[4]
    derivative = CORE["differential_matrix"](reference)
    mixed = [
        row for row, word in zip(derivative, WORDS)
        if word not in ((0,) * 6, (1,) * 6)
    ]
    pure_zero, pure_one = pure_targets()
    profile = (
        ranks_over_fields(derivative),
        ranks_over_fields(mixed),
        ranks_over_fields(append_columns(derivative, pure_zero)),
        ranks_over_fields(append_columns(derivative, pure_one)),
        ranks_over_fields(
            append_columns(derivative, pure_zero, pure_one)
        ),
    )
    require(profile == (
        (55, 55, 55, 55),
        (54, 54, 54, 54),
        (56, 56, 56, 56),
        (55, 55, 55, 55),
        (56, 56, 56, 56),
    ), ("the pre-repair incidence profile changed", profile))
    return changes[0], profile


def audit_selected_equation(endpoint, potential, numerators, packet):
    require(tuple(CORE["matrix_rank"](endpoint[site]) for site in SITES)
            == (2, 1, 1, 1, 0, 0),
            "the endpoint-rank pattern changed")
    numerator_packet = CORE["packet_from_blocks"](numerators)
    slope = CORE["matching_tensor"](packet)
    tangent = CORE["apply_differential"](packet, numerator_packet)
    z_value = -sum(potential)
    require(z_value == -2 and all(
        z_value * base + derivative == 0
        for base, derivative in zip(slope, tangent)
    ), "a selected level-two equation failed")
    return len(slope), z_value


def audit_gauges(packet, derivative):
    vectors = []
    for basis in range(5):
        mu = [Q(0)] * 6
        mu[basis] = Q(1)
        mu[5] = Q(-1)
        tangent = {
            (left, right, a, b):
                (mu[left] + mu[right])
                * packet[left, right, a, b]
            for left, right in EDGES
            for a, b in product(COLOURS, repeat=2)
        }
        require(not any(CORE["apply_differential"](packet, tangent)),
                ("a universal gauge left the kernel", basis))
        vectors.append([tangent[cell] for cell in CORE["CELLS"]])
    require(CORE["rational_rank"](vectors) == 5,
            "the universal gauge vectors became dependent")
    require(ranks_over_fields(derivative) == (55, 55, 55, 55),
            "the survivor no longer has exactly the gauge kernel")
    return len(vectors)


def audit_incidence(packet):
    derivative = CORE["differential_matrix"](packet)
    pure_zero, pure_one = pure_targets()
    mixed = [
        row for row, word in zip(derivative, WORDS)
        if word not in ((0,) * 6, (1,) * 6)
    ]
    profile = {
        "D": ranks_over_fields(derivative),
        "D_mixed": ranks_over_fields(mixed),
        "D|e0": ranks_over_fields(
            append_columns(derivative, pure_zero)
        ),
        "D|e1": ranks_over_fields(
            append_columns(derivative, pure_one)
        ),
        "D|e0,e1": ranks_over_fields(
            append_columns(derivative, pure_zero, pure_one)
        ),
    }
    require(profile == {
        "D": (55, 55, 55, 55),
        "D_mixed": (53, 53, 53, 53),
        "D|e0": (55, 55, 55, 55),
        "D|e1": (55, 55, 55, 55),
        "D|e0,e1": (55, 55, 55, 55),
    }, ("the exact survivor incidence profile changed", profile))

    full_minor = pinned_minor(
        derivative,
        D_MINOR_ROWS,
        D_MINOR_COLUMNS,
        "1ac310b475bb7447b59363106fc7d45b168c66a1d005d53d4619acda8100ee33",
    )
    mixed_minor = pinned_minor(
        mixed,
        MIXED_MINOR_ROWS,
        MIXED_MINOR_COLUMNS,
        "ce0bef574a72a13560b3af6921c570dd45cd4273f2000611974cf17a697f271f",
    )

    preimages = []
    for name, target, expected_digest in (
        ("e0", pure_zero,
         "20c09932f59107f31f086ddbb6311733b8677d031500bd7b27612c6851a66611"),
        ("e1", pure_one,
         "e8f9e38153547c39153e8d7dce889a6f21833ff360ac0098c932de1235c2f4e4"),
    ):
        rank, pivots, solution = solve_linear_system(derivative, target)
        digest = sha256(repr(solution).encode()).hexdigest()
        require(rank == 55 and tuple(pivots) == D_MINOR_COLUMNS
                and digest == expected_digest,
                ("a normalized pure preimage changed", name, digest))
        preimages.append((name, digest, sum(value != 0 for value in solution)))
    return derivative, profile, full_minor, mixed_minor, tuple(preimages)


def oriented_block(blocks, root, neighbour):
    return (
        blocks[root, neighbour]
        if root < neighbour
        else transpose(blocks[neighbour, root])
    )


def audit_r2(endpoint, blocks, packet):
    planned = {
        0: ((1, 0), (2, 1)),
        1: ((0, 0), (2, 1)),
        2: ((1, 0), (0, 1)),
        3: ((1, 0), (2, 1)),
    }
    expected_counts = {
        (0, 1, 0): 20,
        (0, 2, 1): 24,
        (1, 0, 0): 20,
        (1, 2, 1): 32,
        (2, 1, 0): 32,
        (2, 0, 1): 24,
        (3, 1, 0): 32,
        (3, 2, 1): 36,
    }
    counts = {}
    for root, witnesses in planned.items():
        for neighbour, output in witnesses:
            block = oriented_block(blocks, root, neighbour)
            require(CORE["pure_column"](block, output),
                    ("a planned internal R2 witness vanished",
                     root, neighbour, output, block))
            pair = tuple(sorted((root, neighbour)))
            count = sum(
                CORE["cofactor"](packet, word, *pair) != 0
                for word in WORDS
            )
            counts[root, neighbour, output] = count
    require(counts == expected_counts,
            ("the internal R2 cofactor table changed", counts))
    require(all(not any(endpoint[site][a][b]
                        for a, b in product(COLOURS, repeat=2))
                for site in ZEROS),
            "a zero root stopped preserving its endpoint pair")
    return counts


def rational_nullspace(matrix):
    rows = [[Q(value) for value in row] for row in matrix]
    height = len(rows)
    width = len(rows[0]) if rows else 0
    rank = 0
    pivots = []
    for column in range(width):
        pivot = next(
            (row for row in range(rank, height) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for row in range(height):
            if row == rank or not rows[row][column]:
                continue
            multiple = rows[row][column]
            rows[row] = [
                left - multiple * right
                for left, right in zip(rows[row], rows[rank])
            ]
        pivots.append(column)
        rank += 1

    free = tuple(column for column in range(width)
                 if column not in pivots)
    basis = []
    for free_column in free:
        vector = [Q(0)] * width
        vector[free_column] = Q(1)
        for row, pivot_column in reversed(tuple(enumerate(pivots))):
            vector[pivot_column] = -sum(
                rows[row][column] * vector[column] for column in free
            )
        basis.append(tuple(vector))
    require(len(basis) == width - rank,
            "nullspace dimension changed during RREF")
    return rank, tuple(pivots), tuple(basis)


def l1_system(endpoint, blocks, selected_column):
    width = 2 * len(SITES) + len(EDGES)
    equations = []
    for edge_index, (left, right) in enumerate(EDGES):
        for a, b in product(COLOURS, repeat=2):
            row = [Q(0)] * width
            row[2 * right + b] += endpoint[left][a][selected_column]
            row[2 * left + a] += endpoint[right][b][selected_column]
            row[2 * len(SITES) + edge_index] -= blocks[left, right][a][b]
            equations.append(row)
    require(len(equations) == 60 and width == 27,
            "an L1 coefficient system changed size")
    return equations


def audit_l1_modes(endpoint, blocks):
    data = {}
    modes = {}
    for name, selected_column, aligned_column in (
        ("P/V", 0, 1),
        ("Q/U", 1, 0),
    ):
        equations = l1_system(endpoint, blocks, selected_column)
        rank, _pivots, basis = rational_nullspace(equations)
        star_modes = tuple(vector[:12] for vector in basis
                           if any(vector[:12]))
        vacuous = tuple(vector for vector in basis if not any(vector[:12]))
        require(rank == 24 and len(basis) == 3
                and len(star_modes) == 2 and len(vacuous) == 1,
                ("an L1 rank/mode count changed", name, rank, basis))
        require(CORE["rational_rank"](star_modes) == 2,
                ("the L1 star projection lost dimension", name))
        require(all(not any(mode[2 * zero:2 * zero + 2])
                    for mode in star_modes for zero in ZEROS),
                ("a zero-site L1 star survived", name, star_modes))
        aligned = tuple(
            endpoint[site][row][aligned_column]
            for site in SITES for row in COLOURS
        )
        require(CORE["rational_rank"](star_modes + (aligned,)) == 2,
                ("the aligned L1 mode left the kernel", name))
        edge45 = EDGES.index((4, 5))
        require(vacuous[0][12 + edge45] != 0
                and sum(value != 0 for value in vacuous[0]) == 1,
                ("the vacuous rho_45 mode changed", name, vacuous))
        data[name] = {
            "rank": rank,
            "nullity": len(basis),
            "star_modes": len(star_modes),
            "vacuous_modes": len(vacuous),
        }
        modes[name] = star_modes
    return data, modes


def factored_tangent(u_mode, v_mode):
    return {
        (left, right, a, b): (
            u_mode[2 * left + a] * v_mode[2 * right + b]
            + v_mode[2 * left + a] * u_mode[2 * right + b]
        )
        for left, right in EDGES
        for a, b in product(COLOURS, repeat=2)
    }


def column_matrix(columns):
    require(columns and all(len(column) == len(columns[0])
                            for column in columns),
            "a column family is ragged")
    return [list(row) for row in zip(*columns)]


def audit_factored_span(packet, modes):
    products = tuple(
        CORE["apply_differential"](
            packet, factored_tangent(u_mode, v_mode)
        )
        for u_mode in modes["Q/U"]
        for v_mode in modes["P/V"]
    )
    require(len(products) == 4, "the factored L1 product count changed")
    direct = CORE["matching_tensor"](packet)
    output = column_matrix(products)
    enlarged = column_matrix((direct,) + products)
    pure_zero, pure_one = pure_targets()
    ranks = {
        "four products": ranks_over_fields(output),
        "direct+products": ranks_over_fields(enlarged),
        "span|e0": ranks_over_fields(
            append_columns(enlarged, pure_zero)
        ),
        "span|e1": ranks_over_fields(
            append_columns(enlarged, pure_one)
        ),
        "span|e0,e1": ranks_over_fields(
            append_columns(enlarged, pure_zero, pure_one)
        ),
    }
    require(ranks == {
        "four products": (4, 4, 4, 4),
        "direct+products": (4, 4, 4, 4),
        "span|e0": (5, 5, 5, 5),
        "span|e1": (5, 5, 5, 5),
        "span|e0,e1": (6, 6, 6, 6),
    }, ("the L1-compatible factored span changed", ranks))
    return ranks


def transform_matrix(left_scale, matrix, right_scale):
    return tuple(
        tuple(left_scale[row] * matrix[row][column] * right_scale[column]
              for column in COLOURS)
        for row in COLOURS
    )


def audit_diagonal_torus(endpoint, potential, blocks, derivative):
    scales = {site: (Q(site + 2), Q(2 * site + 3)) for site in SITES}
    transformed_endpoint = {
        site: tuple(
            tuple(scales[site][row] * endpoint[site][row][column]
                  for column in COLOURS)
            for row in COLOURS
        )
        for site in SITES
    }
    transformed_blocks = {
        (left, right): transform_matrix(
            scales[left], blocks[left, right], scales[right]
        )
        for left, right in EDGES
    }
    for left, right in EDGES:
        numerator = CORE["matrix_product"](
            CORE["matrix_product"](transformed_endpoint[left], J),
            transpose(transformed_endpoint[right]),
        )
        denominator = potential[left] + potential[right]
        require(numerator == tuple(
            tuple(denominator * transformed_blocks[left, right][a][b]
                  for b in COLOURS)
            for a in COLOURS
        ), ("the diagonal torus broke generic kernel", left, right))

    transformed_packet = CORE["packet_from_blocks"](transformed_blocks)
    transformed_derivative = CORE["differential_matrix"](
        transformed_packet
    )
    for row_index, word in enumerate(WORDS):
        row_scale = Q(1)
        for site in SITES:
            row_scale *= scales[site][word[site]]
        for column_index, (left, right, a, b) in enumerate(CORE["CELLS"]):
            column_scale = scales[left][a] * scales[right][b]
            require(
                transformed_derivative[row_index][column_index]
                == row_scale * derivative[row_index][column_index]
                / column_scale,
                ("differential covariance failed", row_index, column_index),
            )
    pure_zero, pure_one = pure_targets()
    mixed = [
        row for row, word in zip(transformed_derivative, WORDS)
        if word not in ((0,) * 6, (1,) * 6)
    ]
    profile = (
        ranks_over_fields(transformed_derivative),
        ranks_over_fields(mixed),
        ranks_over_fields(
            append_columns(transformed_derivative, pure_zero)
        ),
        ranks_over_fields(
            append_columns(transformed_derivative, pure_one)
        ),
    )
    require(profile == ((55,) * 4, (53,) * 4, (55,) * 4, (55,) * 4),
            ("the torus incidence profile changed", profile))
    r2 = audit_r2(
        transformed_endpoint, transformed_blocks, transformed_packet
    )
    l1, modes = audit_l1_modes(transformed_endpoint, transformed_blocks)
    factored = audit_factored_span(transformed_packet, modes)
    return scales, profile, r2, l1, factored


def main():
    change, reference_profile = audit_one_cell_repair()
    endpoint, potential, blocks, numerators, packet = build_packet(
        SURVIVOR_SPOKES
    )
    selected = audit_selected_equation(
        endpoint, potential, numerators, packet
    )
    derivative, incidence, full_minor, mixed_minor, preimages = (
        audit_incidence(packet)
    )
    gauges = audit_gauges(packet, derivative)
    r2 = audit_r2(endpoint, blocks, packet)
    l1, modes = audit_l1_modes(endpoint, blocks)
    factored = audit_factored_span(packet, modes)
    torus = audit_diagonal_torus(
        endpoint, potential, blocks, derivative
    )

    packet_digest = sha256(repr(tuple(
        packet[cell] for cell in CORE["CELLS"]
    )).encode()).hexdigest()
    require(packet_digest
            == "85542405155ecda5e9069c80c075953b93eee812fb117d2492bc9f5a57309ebd",
            ("the exact survivor packet changed", packet_digest))

    print("1I+3R+2Z all-spokes incidence survivor: all checks passed")
    print(f"  one-cell repair             : {change}")
    print(f"  reference incidence profile: {reference_profile}")
    print(f"  selected rows/z             : {selected}")
    print(f"  survivor incidence profile : {incidence}")
    print(f"  exact maximal minors        : 55/{full_minor[1]} 53/{mixed_minor[1]}")
    print(f"  normalized pure preimages  : {preimages}")
    print(f"  exact gauge kernel          : {gauges} dimensions")
    print(f"  internal R2 cofactors       : {r2}")
    print(f"  overlapping L1 systems     : {l1}")
    print(f"  L1-factored output span    : {factored}")
    print(f"  diagonal-torus scales      : {torus[0]}")
    print(f"  exact packet SHA-256       : {packet_digest}")
    print("  conclusion                 : linear L0 survivor excluded by L1/factored compatibility")
    print("  residual status            : other points of the rank-55/53 locus remain open")


if __name__ == "__main__":
    main()
