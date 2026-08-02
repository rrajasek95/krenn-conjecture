#!/usr/bin/env python3
"""Exclude the exact 1I+3R+2Z all-spokes guard by L0/L1 compatibility.

The potential-boundary checker leaves one selected generic-kernel/R2
support type and displays an exact differential-rank-55 guard on it.  This
checker adds the missing endpoint equations for that guard.

Both pure L0 targets miss im(dPsi): adjoining either raises rank 55 to 56,
and the mixed-row differential still has rank 55 instead of the necessary
53.  The overlapping L1 systems have two genuine star modes on the
four-site core and kill every zero-site star vector.  Even the linear span
of all four products of those U/V modes, together with the direct Psi(M)
term, misses both pure targets.  The same statements hold on the full
nonzero local diagonal torus through the guard.

This excludes the exact guard and its justified covariant family, not the
entire all-spokes support envelope.  Any survivor must lie on the exact
rank-55/mixed-rank-53 incidence locus outside this torus.

Research evidence only.  Standard library; live under -O and -I -S.
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
L0 = run_path(str(
    HERE / "verify_level_two_three_invertible_l0_obstruction.py"
))
CORE = SOURCE["R2_GUARD"]

SITES = tuple(range(6))
NONZERO = (0, 1, 2, 3)
ZEROS = (4, 5)
COLOURS = (0, 1)
EDGES = tuple(combinations(SITES, 2))
WORDS = tuple(product(COLOURS, repeat=6))
J = CORE["J"]


def outer(left, right):
    return tuple(
        tuple(Q(left[row]) * Q(right[column]) for column in COLOURS)
        for row in COLOURS
    )


def transpose(matrix):
    return tuple(tuple(matrix[row][column] for row in COLOURS)
                 for column in COLOURS)


def determinant(matrix):
    return (
        matrix[0][0] * matrix[1][1]
        - matrix[0][1] * matrix[1][0]
    )


def build_guard():
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
                tuple(numerator[a][b] / denominator for b in COLOURS)
                for a in COLOURS
            )
        elif (left, right) == (4, 5):
            block = ((Q(0), Q(0)), (Q(0), Q(0)))
        else:
            start = 11 + 7 * left + 13 * right
            block = (
                (Q(start), Q(start + 1)),
                (Q(start + 2), Q(start + 4)),
            )
        blocks[left, right] = block
        require(numerator == tuple(
            tuple(denominator * block[a][b] for b in COLOURS)
            for a in COLOURS
        ), ("guard generic-kernel block changed", left, right))
    packet = CORE["packet_from_blocks"](blocks)
    return endpoint, potential, blocks, numerators, packet


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
        CORE["modular_rank"](
            modularize(matrix, 1_000_003), 1_000_003
        ),
    )


def append_columns(matrix, *columns):
    require(all(len(column) == len(matrix) for column in columns),
            "an augmented column has the wrong height")
    return [
        row[:] + [column[index] for column in columns]
        for index, row in enumerate(matrix)
    ]


def audit_source_guard(endpoint, potential, blocks, packet):
    source = SOURCE["audit_all_spokes_rank55_r2_guard"]()
    require(source["endpoint_ranks"] == (2, 1, 1, 1, 0, 0)
            and source["differential_ranks"] == (55, 55, 55)
            and source["literal_r2_roots"] == 6,
            ("source all-spokes guard changed", source))
    require(potential == source["potential"],
            ("guard potential changed", potential, source["potential"]))
    require(tuple(CORE["matrix_rank"](endpoint[site]) for site in SITES)
            == source["endpoint_ranks"],
            "rebuilt endpoint ranks changed")
    require(all(determinant(blocks[left, zero])
                for left in NONZERO for zero in ZEROS),
            "a guard zero spoke became singular")
    derivative = CORE["differential_matrix"](packet)
    require(ranks_over_fields(derivative) == (55, 55, 55),
            "rebuilt guard lost differential rank 55")
    return source, derivative


def audit_universal_l0_formula(packet):
    names = (
        "literal_slice_counter",
        "derived_slice_counter",
        "audit_matching_partition_and_slice_formula",
    )
    globals_dict = L0[names[0]].__globals__
    require(all(L0[name].__globals__ is globals_dict for name in names),
            "the imported L0 formula functions stopped sharing globals")
    old_packet = globals_dict["M"]
    try:
        globals_dict["M"] = packet
        checked = L0["audit_matching_partition_and_slice_formula"]()
    finally:
        globals_dict["M"] = old_packet
    require(checked == 256, ("formal L0 slice count changed", checked))
    return checked


def pure_targets():
    pure_zero = [int(word == (0,) * 6) for word in WORDS]
    pure_one = [int(word == (1,) * 6) for word in WORDS]
    return pure_zero, pure_one


def incidence_profile(derivative):
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
        "D": (55, 55, 55),
        "D_mixed": (55, 55, 55),
        "D|e0": (56, 56, 56),
        "D|e1": (56, 56, 56),
        "D|e0,e1": (57, 57, 57),
    }, ("all-spokes L0 incidence profile changed", profile))
    return profile


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
    # Unknowns are a two-vector S_r at every residual site followed by one
    # scalar rho_ru per residual edge.  For selected_column=0 this is the
    # P/V equation; for selected_column=1 it is the Q/U equation:
    #
    # X_r[:,c] S_u^T + S_r X_u[:,c]^T = rho_ru M_ru.
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
            "the L1 coefficient system size changed")
    return equations


def audit_l1_modes(endpoint, blocks):
    data = {}
    modes = {}
    for name, selected_column, aligned_column in (
        ("P/V", 0, 1),
        ("Q/U", 1, 0),
    ):
        equations = l1_system(endpoint, blocks, selected_column)
        rank, pivots, basis = rational_nullspace(equations)
        require(rank == 24 and len(basis) == 3,
                ("all-spokes L1 rank/nullity changed", name, rank, basis))

        star_modes = tuple(vector[:12] for vector in basis
                           if any(vector[:12]))
        vacuous = tuple(vector for vector in basis if not any(vector[:12]))
        require(len(star_modes) == 2 and len(vacuous) == 1,
                ("L1 star/vacuous mode count changed", name, basis))
        require(CORE["rational_rank"](star_modes) == 2,
                ("L1 star modes became dependent", name, star_modes))
        require(all(not any(mode[2 * zero:2 * zero + 2])
                    for mode in star_modes for zero in ZEROS),
                ("a zero-site L1 star survived an invertible spoke",
                 name, star_modes))

        aligned = tuple(
            endpoint[site][row][aligned_column]
            for site in SITES for row in COLOURS
        )
        require(CORE["rational_rank"](star_modes + (aligned,)) == 2,
                ("the selected-column aligned mode left the L1 kernel",
                 name, aligned, star_modes))
        edge45 = EDGES.index((4, 5))
        require(vacuous[0][12 + edge45] != 0
                and sum(value != 0 for value in vacuous[0]) == 1,
                ("the sole vacuous rho_45 mode changed", name, vacuous))
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


def audit_l1_factored_output_span(packet, modes):
    u_modes = modes["Q/U"]
    v_modes = modes["P/V"]
    factored_outputs = tuple(
        CORE["apply_differential"](
            packet, factored_tangent(u_mode, v_mode)
        )
        for u_mode in u_modes for v_mode in v_modes
    )
    require(len(factored_outputs) == 4,
            "the L1 factored product count changed")
    slope = CORE["matching_tensor"](packet)
    output_matrix = column_matrix(factored_outputs)
    enlarged = column_matrix((slope,) + factored_outputs)
    pure_zero, pure_one = pure_targets()
    ranks = {
        "four products": ranks_over_fields(output_matrix),
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
        "four products": (4, 4, 4),
        "direct+products": (4, 4, 4),
        "span|e0": (5, 5, 5),
        "span|e1": (5, 5, 5),
        "span|e0,e1": (6, 6, 6),
    }, ("L1-restricted factored output span changed", ranks))
    return ranks


def transform_matrix(left_scale, matrix, right_scale):
    return tuple(
        tuple(left_scale[row] * matrix[row][column] * right_scale[column]
              for column in COLOURS)
        for row in COLOURS
    )


def audit_diagonal_torus(endpoint, potential, blocks, derivative):
    scales = {
        site: (Q(site + 2), Q(2 * site + 3)) for site in SITES
    }
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
        ), ("diagonal torus broke generic kernel", left, right))

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
    profile = incidence_profile(transformed_derivative)

    planned = {
        0: ((1, 0), (2, 1)),
        1: ((0, 0), (2, 1)),
        2: ((1, 0), (0, 1)),
        3: ((1, 0), (2, 1)),
    }
    for root, witnesses in planned.items():
        for neighbour, output in witnesses:
            block = (
                transformed_blocks[root, neighbour]
                if root < neighbour
                else transpose(transformed_blocks[neighbour, root])
            )
            require(CORE["pure_column"](block, output),
                    ("diagonal torus broke an R2 witness",
                     root, neighbour, output, block))
    return scales, profile


def audit_remaining_scope():
    total_ternary_cells = len(tuple(combinations(range(8), 2))) * 9
    residual_binary_cells = len(EDGES) * 4
    require((total_ternary_cells, residual_binary_cells)
            == (252, 60),
            "the full/residual completion scope changed")
    necessary = {
        "rank(D)": 55,
        "rank(D_mixed)": 53,
        "rank(D|e0)": 55,
        "rank(D|e1)": 55,
        "rank(D|e0,e1)": 55,
    }
    return residual_binary_cells, total_ternary_cells - residual_binary_cells, necessary


def main():
    endpoint, potential, blocks, _numerators, packet = build_guard()
    source, derivative = audit_source_guard(
        endpoint, potential, blocks, packet
    )
    formal = audit_universal_l0_formula(packet)
    incidence = incidence_profile(derivative)
    l1, modes = audit_l1_modes(endpoint, blocks)
    factored = audit_l1_factored_output_span(packet, modes)
    torus = audit_diagonal_torus(endpoint, potential, blocks, derivative)
    scope = audit_remaining_scope()

    packet_digest = sha256(repr(tuple(
        packet[cell] for cell in CORE["CELLS"]
    )).encode()).hexdigest()
    print("1I+3R+2Z all-spokes endpoint compatibility: all checks passed")
    print(f"  source rank/R2              : {source['differential_ranks']}/6 roots")
    print(f"  universal factored slices   : {formal}/256")
    print(f"  unconstrained L0 incidence  : {incidence}")
    print(f"  overlapping L1 systems      : {l1}")
    print(f"  L1-factored output span     : {factored}")
    print(f"  diagonal-torus scales       : {torus[0]}")
    print(f"  completion scope            : {scope[0]} residual/{scope[1]} outside")
    print(f"  necessary survivor profile  : {scope[2]}")
    print(f"  exact packet SHA-256        : {packet_digest}")
    print("  conclusion                  : exact guard and its diagonal torus excluded")
    print("  residual status             : special rank-55/53 incidence locus remains")


if __name__ == "__main__":
    main()
