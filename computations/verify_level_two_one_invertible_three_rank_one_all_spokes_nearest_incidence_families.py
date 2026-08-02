#!/usr/bin/env python3
"""Classify the nearest all-spokes incidence families and exclude them at L1.

Start from the exact 1I+3R+2Z all-spokes incidence survivor.  With

    M_34 = ((a,b),(c,d)),

the rank-53 mixed determinantal locus is locally the hyperplane b=d.  This
checker certifies that statement by the exact determinantal tangent space and
by function-field ranks in Singular.  It then frees the smallest extra cell,

    M_04(0,0) = x,

while retaining M_34=((a,b),(c,b)).  The resulting four-parameter coupled
family has generic ranks 55/53, and every rank-55 member has both pure L0
incidences and uniform literal R2.

The L1 star spaces are constant on the rank-55 locus.  All coefficients of
all four parameter-dependent factored products span a fixed 13-dimensional
rational space; adjoining either pure target raises rank to 14, and adjoining
both raises it to 15.  Hence the whole rank-55 coupled family is excluded.

Research evidence only.  Python is standard-library; Singular is the sole
external dependency.  Checks remain live under -O and -I -S.
"""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from pathlib import Path
from runpy import run_path
from shutil import which
from subprocess import run, TimeoutExpired


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
BASE = run_path(str(
    HERE
    / "verify_level_two_one_invertible_three_rank_one_all_spokes_incidence_survivor_l1_obstruction.py"
))
CORE = BASE["CORE"]
WORDS = BASE["WORDS"]
EDGES = BASE["EDGES"]
COLOURS = BASE["COLOURS"]
CELLS = CORE["CELLS"]

ARBITRARY_NAMES = ("a", "b", "c", "d")
COUPLED_NAMES = ("a", "b", "c", "x")
PURE_WORDS = ((0,) * 6, (1,) * 6)


def qtuple(values):
    return tuple(Q(value) for value in values)


def packet_for(kind, parameters):
    parameters = qtuple(parameters)
    spokes = dict(BASE["SURVIVOR_SPOKES"])
    if kind == "arbitrary":
        a, b, c, d = parameters
        spokes[3, 4] = ((a, b), (c, d))
    elif kind == "coupled":
        a, b, c, x = parameters
        spokes[3, 4] = ((a, b), (c, b))
        spokes[0, 4] = ((x, Q(85)), (Q(0), Q(87)))
    elif kind == "x_zero":
        a, b, c = parameters
        spokes[3, 4] = ((a, b), (c, b))
        spokes[0, 4] = ((Q(0), Q(85)), (Q(0), Q(87)))
    elif kind == "m34_zero":
        (x,) = parameters
        spokes[3, 4] = ((Q(0), Q(0)), (Q(0), Q(0)))
        spokes[0, 4] = ((x, Q(85)), (Q(0), Q(87)))
    else:
        raise RuntimeError(("unknown family", kind))
    return BASE["build_packet"](spokes)


def differential_for(kind, parameters):
    packet = packet_for(kind, parameters)[4]
    return CORE["differential_matrix"](packet)


def mixed_rows(matrix):
    return [
        row for row, word in zip(matrix, WORDS)
        if word not in PURE_WORDS
    ]


def matrix_subtract(left, right):
    return [
        [a - b for a, b in zip(left_row, right_row)]
        for left_row, right_row in zip(left, right)
    ]


def matrix_add_scaled(base, directions, parameters):
    return [
        [
            base[row][column] + sum(
                Q(parameters[index]) * direction[row][column]
                for index, direction in enumerate(directions)
            )
            for column in range(len(base[0]))
        ]
        for row in range(len(base))
    ]


def affine_matrix_data(kind, names):
    zero = (Q(0),) * len(names)
    constant = differential_for(kind, zero)
    directions = []
    for index in range(len(names)):
        point = [Q(0)] * len(names)
        point[index] = Q(1)
        directions.append(matrix_subtract(
            differential_for(kind, point), constant
        ))
    test = tuple(Q(2 * index + 3) for index in range(len(names)))
    require(
        differential_for(kind, test)
        == matrix_add_scaled(constant, directions, test),
        ("a claimed differential family is not affine", kind),
    )
    return constant, tuple(directions)


def rational_string(value):
    value = Q(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"({value.numerator}/{value.denominator})"


def singular_matrix_entries(constant, directions, names, selected_rows):
    entries = []
    for row in selected_rows:
        for column in range(len(constant[0])):
            terms = []
            if constant[row][column]:
                terms.append(rational_string(constant[row][column]))
            for index, name in enumerate(names):
                coefficient = directions[index][row][column]
                if coefficient:
                    terms.append(
                        f"{rational_string(coefficient)}*{name}"
                    )
            entries.append("+".join(terms) if terms else "0")
    return ",".join(entries)


def singular_rank_section(label, kind, names):
    constant, directions = affine_matrix_data(kind, names)
    full = singular_matrix_entries(
        constant, directions, names, range(64)
    )
    mixed_indices = tuple(
        index for index, word in enumerate(WORDS)
        if word not in PURE_WORDS
    )
    mixed = singular_matrix_entries(
        constant, directions, names, mixed_indices
    )
    return "\n".join((
        f"ring r{label}=(0,{','.join(names)}),t,dp;",
        f"matrix D[64][60]={full};",
        f"matrix X[62][60]={mixed};",
        f'print("{label}");',
        "rank(D);",
        "rank(X);",
    ))


def singular_program():
    return "\n".join((
        'print("BEGIN");',
        singular_rank_section("ARBITRARY", "arbitrary", ARBITRARY_NAMES),
        singular_rank_section("COUPLED", "coupled", COUPLED_NAMES),
        singular_rank_section("XZERO", "x_zero", ("a", "b", "c")),
        singular_rank_section("M34ZERO", "m34_zero", ("x",)),
        'print("END");',
        "",
    ))


def audit_singular_function_fields():
    executable = which("Singular")
    require(executable is not None,
            "external dependency missing: Singular is not on PATH")
    program = singular_program()
    digest = sha256(program.encode()).hexdigest()
    expected_digest = "1b968e0d7056d6f18dcb4ec27805d578499579e84f27954a1e6f096da6fc6c51"
    require(digest == expected_digest,
            ("the Singular function-field input changed", digest))
    try:
        completed = run(
            [executable, "-q"],
            input=program,
            text=True,
            capture_output=True,
            timeout=180,
            check=False,
        )
    except TimeoutExpired as error:
        raise RuntimeError("Singular family-rank audit timed out") from error
    require(completed.returncode == 0,
            ("Singular family-rank audit failed", completed.stderr))
    lines = tuple(
        line.strip() for line in completed.stdout.splitlines()
        if line.strip()
    )
    require(lines == (
        "BEGIN",
        "ARBITRARY", "55", "54",
        "COUPLED", "55", "53",
        "XZERO", "53", "52",
        "M34ZERO", "50", "49",
        "END",
    ), ("the function-field rank ledger changed", lines))
    return digest, lines


def canonical_row_space(matrix):
    rows = [[Q(value) for value in row] for row in matrix]
    rank = 0
    width = len(rows[0]) if rows else 0
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
        rank += 1
    return tuple(tuple(rows[row]) for row in range(rank))


def audit_arbitrary_m34_tangent():
    base_point = (Q(0), Q(0), Q(29), Q(0))
    base = mixed_rows(differential_for("arbitrary", base_point))
    rank, _pivots, right_kernel = BASE["rational_nullspace"](base)
    left_rank, _left_pivots, left_kernel = BASE["rational_nullspace"](
        list(map(list, zip(*base)))
    )
    require((rank, len(right_kernel), left_rank, len(left_kernel))
            == (53, 7, 53, 9),
            "the rank-53 tangent base changed")

    constant, directions = affine_matrix_data(
        "arbitrary", ARBITRARY_NAMES
    )
    mixed_directions = tuple(mixed_rows(direction)
                             for direction in directions)
    obstruction = []
    for left in left_kernel:
        for right in right_kernel:
            row = []
            for direction in mixed_directions:
                direction_right = [
                    sum(direction[i][j] * right[j] for j in range(60))
                    for i in range(62)
                ]
                row.append(sum(
                    left[i] * direction_right[i] for i in range(62)
                ))
            obstruction.append(row)
    row_space = canonical_row_space(obstruction)
    require(row_space == ((Q(0), Q(1), Q(0), Q(-1)),),
            ("the local incidence tangent changed", row_space))
    require(constant == differential_for("arbitrary", (0, 0, 0, 0)),
            "the arbitrary-family affine origin changed")
    return {
        "mixed rank": rank,
        "left nullity": len(left_kernel),
        "right nullity": len(right_kernel),
        "normal": "b-d",
    }


def ranks_over_fields(matrix):
    return BASE["ranks_over_fields"](matrix)


def audit_coupled_calibration():
    endpoint, potential, blocks, numerators, packet = packet_for(
        "coupled", (Q(1), Q(2), Q(3), Q(4))
    )
    selected = BASE["audit_selected_equation"](
        endpoint, potential, numerators, packet
    )
    derivative = CORE["differential_matrix"](packet)
    mixed = mixed_rows(derivative)
    pure_zero, pure_one = BASE["pure_targets"]()
    profile = {
        "D": ranks_over_fields(derivative),
        "D_mixed": ranks_over_fields(mixed),
        "D|e0": ranks_over_fields(
            BASE["append_columns"](derivative, pure_zero)
        ),
        "D|e1": ranks_over_fields(
            BASE["append_columns"](derivative, pure_one)
        ),
        "D|e0,e1": ranks_over_fields(
            BASE["append_columns"](
                derivative, pure_zero, pure_one
            )
        ),
    }
    require(profile == {
        "D": (55, 55, 55, 55),
        "D_mixed": (53, 53, 53, 53),
        "D|e0": (55, 55, 55, 55),
        "D|e1": (55, 55, 55, 55),
        "D|e0,e1": (55, 55, 55, 55),
    }, ("the coupled-family calibration changed", profile))
    return selected, profile


def transpose(matrix):
    return tuple(tuple(matrix[row][column] for row in COLOURS)
                 for column in COLOURS)


def oriented_block(blocks, root, neighbour):
    return (
        blocks[root, neighbour]
        if root < neighbour
        else transpose(blocks[neighbour, root])
    )


def audit_uniform_r2():
    witnesses = {
        (0, 0): (1, (0, 0, 0, 0, 1, 1), Q(2346)),
        (0, 1): (2, (0, 1, 0, 0, 1, 1), Q(3366)),
        (1, 0): (0, (0, 0, 0, 0, 1, 1), Q(2346)),
        (1, 1): (4, (0, 0, 0, 0, 0, 0), Q(28)),
        (2, 0): (5, (0, 1, 0, 0, 1, 0), Q(33)),
        (2, 1): (0, (0, 1, 0, 0, 1, 1), Q(3366)),
        (3, 0): (1, (0, 0, 0, 0, 1, 1), Q(4002)),
        (3, 1): (2, (0, 0, 0, 0, 1, 0), Q(6216)),
    }
    origin = (0, 0, 0, 0)
    basis_points = tuple(
        tuple(int(slot == index) for slot in range(4))
        for index in range(4)
    )
    double_points = tuple(
        tuple(2 * int(slot == index) for slot in range(4))
        for index in range(4)
    )
    pair_points = tuple(
        tuple(int(slot in (left, right)) for slot in range(4))
        for left in range(4) for right in range(left + 1, 4)
    )
    test_points = (
        (origin,) + basis_points + double_points + pair_points
        + ((2, 3, 5, 7),)
    )
    audited = {}
    for root_output, (neighbour, word, expected) in witnesses.items():
        root, output = root_output
        values = []
        for point in test_points:
            _endpoint, _potential, blocks, _numerators, packet = (
                packet_for("coupled", point)
            )
            require(CORE["pure_column"](
                oriented_block(blocks, root, neighbour), output
            ), ("a uniform R2 pure column vanished", root_output))
            pair = tuple(sorted((root, neighbour)))
            values.append(CORE["cofactor"](packet, word, *pair))
        require(all(value == expected for value in values),
                ("a uniform R2 cofactor changed", root_output, values))
        audited[root_output] = (neighbour, word, expected)
    endpoint = packet_for("coupled", (2, 3, 5, 7))[0]
    require(all(not any(endpoint[site][a][b]
                        for a, b in product(COLOURS, repeat=2))
                for site in (4, 5)),
            "a zero endpoint stopped preserving its witness pair")
    return audited


def matrix_vector(matrix, vector):
    return tuple(
        sum(value * vector[column]
            for column, value in enumerate(row))
        for row in matrix
    )


def l1_affine_matrices(selected_column):
    zero_endpoint, _p, zero_blocks, _n, _m = packet_for(
        "coupled", (0, 0, 0, 0)
    )
    constant = BASE["l1_system"](
        zero_endpoint, zero_blocks, selected_column
    )
    directions = []
    for index in range(4):
        point = [Q(0)] * 4
        point[index] = Q(1)
        endpoint, _p, blocks, _n, _m = packet_for("coupled", point)
        directions.append(matrix_subtract(
            BASE["l1_system"](endpoint, blocks, selected_column),
            constant,
        ))
    test = (Q(2), Q(3), Q(5), Q(7))
    endpoint, _p, blocks, _n, _m = packet_for("coupled", test)
    require(
        BASE["l1_system"](endpoint, blocks, selected_column)
        == matrix_add_scaled(constant, directions, test),
        "an L1 family stopped being affine",
    )
    return constant, tuple(directions)


def audit_uniform_l1_modes():
    base_endpoint, _p, base_blocks, _n, _m = packet_for(
        "coupled", (0, 0, 29, 1)
    )
    data = {}
    modes = {}
    basis_digests = {}
    edge34 = EDGES.index((3, 4))
    edge04 = EDGES.index((0, 4))
    for name, selected_column in (("P/V", 0), ("Q/U", 1)):
        matrix = BASE["l1_system"](
            base_endpoint, base_blocks, selected_column
        )
        rank, _pivots, basis = BASE["rational_nullspace"](matrix)
        require(rank == 24 and len(basis) == 3,
                ("the base L1 system changed", name, rank))
        constant, directions = l1_affine_matrices(selected_column)
        for vector in basis:
            require(not any(matrix_vector(constant, vector)),
                    ("a fixed L1 mode failed at the origin", name))
            require(all(not any(matrix_vector(direction, vector))
                        for direction in directions),
                    ("a fixed L1 mode became parameter-dependent", name))

        star_modes = tuple(vector[:12] for vector in basis
                           if any(vector[:12]))
        vacuous = tuple(vector for vector in basis if not any(vector[:12]))
        require(len(star_modes) == 2 and len(vacuous) == 1,
                ("the L1 star/vacuous split changed", name))
        require(vacuous[0][12 + EDGES.index((4, 5))] != 0,
                ("the rho_45 mode changed", name))

        # A parameter-independent 55-row subsystem, omitting edge 34 and
        # the sole x-dependent equation M_04(0,0), has rank 23.  If M_34 is
        # nonzero, its unique rho_34 column raises rank by one.  The Singular
        # M34ZERO rank bound proves every rank-55 packet has M_34 != 0.
        fixed_rows = []
        for edge_index, edge in enumerate(EDGES):
            for cell_index in range(4):
                if edge == (3, 4):
                    continue
                if edge == (0, 4) and cell_index == 0:
                    continue
                fixed_rows.append(4 * edge_index + cell_index)
        fixed = [constant[row] for row in fixed_rows]
        require(CORE["rational_rank"](fixed) == 23,
                ("the fixed L1 rank-23 subsystem changed", name))
        require(all(vector[12 + edge34] == 0
                    and vector[12 + edge04] == 0 for vector in basis),
                ("a variable-edge rho entered a fixed L1 mode", name))

        digest = sha256(repr(basis).encode()).hexdigest()
        basis_digests[name] = digest
        data[name] = {
            "rank on rank-55 locus": 24,
            "nullity": 3,
            "star modes": 2,
            "vacuous modes": 1,
            "fixed subsystem rank": 23,
        }
        modes[name] = star_modes
    require(basis_digests == {
        "P/V": "e63aa09838b43d51f3de060f427bb45628e446e61e99f28ea790c80a5ea1f1a6",
        "Q/U": "45b6de4a61f4b66e7afae27574483e06bc4843218eff9a600dab6fff52bc03c3",
    }, ("the fixed L1 bases changed", basis_digests))
    return data, modes, basis_digests


def product_outputs(parameters, modes):
    packet = packet_for("coupled", parameters)[4]
    outputs = tuple(
        CORE["apply_differential"](
            packet, BASE["factored_tangent"](u_mode, v_mode)
        )
        for u_mode in modes["Q/U"]
        for v_mode in modes["P/V"]
    )
    return outputs, CORE["matching_tensor"](packet)


def vector_subtract(left, right):
    return tuple(a - b for a, b in zip(left, right))


def audit_uniform_factored_span(modes):
    zero = (Q(0),) * 4
    constant_outputs, constant_slope = product_outputs(zero, modes)
    coefficient_columns = list(constant_outputs)
    slope_columns = [constant_slope]
    output_directions = []
    for index in range(4):
        point = [Q(0)] * 4
        point[index] = Q(1)
        outputs, slope = product_outputs(point, modes)
        directions = tuple(
            vector_subtract(outputs[slot], constant_outputs[slot])
            for slot in range(4)
        )
        output_directions.append(directions)
        coefficient_columns.extend(directions)
        slope_columns.append(vector_subtract(slope, constant_slope))

    test = (Q(2), Q(3), Q(5), Q(7))
    test_outputs, test_slope = product_outputs(test, modes)
    for slot in range(4):
        reconstructed = tuple(
            constant_outputs[slot][row] + sum(
                test[index] * output_directions[index][slot][row]
                for index in range(4)
            )
            for row in range(64)
        )
        require(tuple(test_outputs[slot]) == reconstructed,
                ("a factored output stopped being affine", slot))
    reconstructed_slope = tuple(
        constant_slope[row] + sum(
            test[index] * slope_columns[index + 1][row]
            for index in range(4)
        )
        for row in range(64)
    )
    require(tuple(test_slope) == reconstructed_slope,
            "the direct slope stopped being affine")

    affine_test_points = [zero]
    for index in range(4):
        point = [Q(0)] * 4
        point[index] = Q(1)
        affine_test_points.append(tuple(point))
    affine_test_points.append(test)
    for point in affine_test_points:
        outputs, slope = product_outputs(point, modes)
        require(all(
            slope[row] == 2 * sum(output[row] for output in outputs)
            for row in range(64)
        ), ("the direct/product Euler identity changed", point))

    coefficient_matrix = BASE["column_matrix"](
        tuple(coefficient_columns)
    )
    with_slopes = BASE["column_matrix"](
        tuple(coefficient_columns + slope_columns)
    )
    pure_zero, pure_one = BASE["pure_targets"]()
    ranks = {
        "all product coefficients": ranks_over_fields(coefficient_matrix),
        "coefficients+direct": ranks_over_fields(with_slopes),
        "coefficients|e0": ranks_over_fields(
            BASE["append_columns"](coefficient_matrix, pure_zero)
        ),
        "coefficients|e1": ranks_over_fields(
            BASE["append_columns"](coefficient_matrix, pure_one)
        ),
        "coefficients|e0,e1": ranks_over_fields(
            BASE["append_columns"](
                coefficient_matrix, pure_zero, pure_one
            )
        ),
    }
    require(ranks == {
        "all product coefficients": (13, 13, 13, 13),
        "coefficients+direct": (13, 13, 13, 13),
        "coefficients|e0": (14, 14, 14, 14),
        "coefficients|e1": (14, 14, 14, 14),
        "coefficients|e0,e1": (15, 15, 15, 15),
    }, ("the uniform factored coefficient span changed", ranks))
    digest = sha256(repr(tuple(
        tuple(row) for row in coefficient_matrix
    )).encode()).hexdigest()
    require(digest == "b64fad8a27c094f6376e220746356656840d473ad00a4dec0a20c820564040d2",
            ("the factored coefficient matrix changed", digest))
    return ranks, digest


def main():
    tangent = audit_arbitrary_m34_tangent()
    singular_digest, singular_ledger = audit_singular_function_fields()
    calibration = audit_coupled_calibration()
    r2 = audit_uniform_r2()
    l1, modes, basis_digests = audit_uniform_l1_modes()
    factored, coefficient_digest = audit_uniform_factored_span(modes)

    print("nearest all-spokes incidence families: all checks passed")
    print(f"  arbitrary-M34 local tangent : {tangent}")
    print(f"  function-field rank ledger : {singular_ledger}")
    print(f"  Singular input SHA-256     : {singular_digest}")
    print(f"  coupled calibration        : {calibration}")
    print(f"  uniform fixed R2 witnesses : {len(r2)}")
    print(f"  uniform L1 systems         : {l1}")
    print(f"  fixed L1 basis digests     : {basis_digests}")
    print(f"  factored coefficient span : {factored}")
    print(f"  coefficient SHA-256        : {coefficient_digest}")
    print("  conclusion                 : full rank-55 nearest coupled family excluded")
    print("  residual status            : deformations of a second full spoke remain open")


if __name__ == "__main__":
    main()
