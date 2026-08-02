#!/usr/bin/env python3
"""Audit the full spoke tangent and a five-parameter all-spokes family.

At the exact 1I+3R+2Z all-spokes incidence survivor, vary all 32 cells in
the eight free core-to-zero spoke blocks.  The exact first determinantal
obstruction has rank six, hence the rank-53 mixed tangent space has dimension
26.  Its six reduced equations are pinned explicitly below.  This is a
tangent-space certificate, not a claim that the whole 26-plane lies in the
incidence variety.

Inside that tangent plane, extend the previous four-parameter exact family by
one independent cell:

  M34=((a,b),(c,b)), M04=((x,85),(0,87)), M35=((0,y),(0,96)).

Singular proves function-field ranks 55/53 over Q(a,b,c,x,y).  The full L1
star spaces are constant on its rank-55 locus.  All constant, linear, and
quadratic coefficients of its four factored outputs span rank 16; either pure
target raises rank to 17 and both raise it to 18.  Thus the whole rank-55
five-parameter family is excluded by direct-plus-factored L1 compatibility.

Research evidence only.  Python is standard-library; Singular is the sole
external dependency.  Checks remain live under -O and -I -S.
"""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
from runpy import run_path
from shutil import which
from subprocess import run, TimeoutExpired


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
PREVIOUS = run_path(str(
    HERE
    / "verify_level_two_one_invertible_three_rank_one_all_spokes_nearest_incidence_families.py"
))
BASE = PREVIOUS["BASE"]
CORE = BASE["CORE"]
WORDS = BASE["WORDS"]
EDGES = BASE["EDGES"]
COLOURS = BASE["COLOURS"]
FREE_EDGES = tuple(sorted(BASE["SURVIVOR_SPOKES"]))
FREE_CELLS = tuple(
    (edge, row, column)
    for edge in FREE_EDGES
    for row, column in product(COLOURS, repeat=2)
)
PARAMETER_NAMES = ("a", "b", "c", "x", "y")
PURE_WORDS = ((0,) * 6, (1,) * 6)


def mixed_rows(matrix):
    return [
        row for row, word in zip(matrix, WORDS)
        if word not in PURE_WORDS
    ]


def add_to_block(block, row, column, value):
    changed = [list(entries) for entries in block]
    changed[row][column] += value
    return tuple(tuple(entries) for entries in changed)


def full_spoke_direction(edge, row, column):
    spokes = dict(BASE["SURVIVOR_SPOKES"])
    spokes[edge] = add_to_block(spokes[edge], row, column, Q(1))
    packet = BASE["build_packet"](spokes)[4]
    return mixed_rows(CORE["differential_matrix"](packet))


def audit_full_determinantal_tangent():
    base_packet = BASE["build_packet"](
        BASE["SURVIVOR_SPOKES"]
    )[4]
    base = mixed_rows(CORE["differential_matrix"](base_packet))
    rank, _pivots, right_kernel = BASE["rational_nullspace"](base)
    left_rank, _left_pivots, left_kernel = BASE["rational_nullspace"](
        list(map(list, zip(*base)))
    )
    require((rank, len(right_kernel), left_rank, len(left_kernel))
            == (53, 7, 53, 9),
            "the full-spoke tangent base changed")

    directions = []
    for edge, row, column in FREE_CELLS:
        changed = full_spoke_direction(edge, row, column)
        directions.append(PREVIOUS["matrix_subtract"](changed, base))

    obstruction = []
    for left in left_kernel:
        for right in right_kernel:
            equation = []
            for direction in directions:
                image = [
                    sum(direction[i][j] * right[j] for j in range(60))
                    for i in range(62)
                ]
                equation.append(sum(
                    left[i] * image[i] for i in range(62)
                ))
            obstruction.append(equation)
    row_space = PREVIOUS["canonical_row_space"](obstruction)

    expected = []
    for support in (
        {((1, 4), 1, 0): Q(1)},
        {((1, 5), 1, 1): Q(1)},
        {((2, 4), 0, 0): Q(1)},
        {((2, 5), 0, 1): Q(1)},
        {((3, 4), 0, 1): Q(1), ((3, 4), 1, 1): Q(-1)},
        {((3, 5), 0, 0): Q(1), ((3, 5), 1, 0): Q(-1)},
    ):
        expected.append(tuple(
            support.get((edge, row, column), Q(0))
            for edge, row, column in FREE_CELLS
        ))
    require(row_space == tuple(expected),
            ("the full-spoke tangent equations changed", row_space))
    digest = sha256(repr((FREE_CELLS, row_space)).encode()).hexdigest()
    require(digest
            == "5bb8f8b24e8ff22628b12a278e370f925217e7b8c170a304dc5b5da26f6cda49",
            ("the full tangent certificate changed", digest))
    equations = (
        "dM14(1,0)=0",
        "dM15(1,1)=0",
        "dM24(0,0)=0",
        "dM25(0,1)=0",
        "dM34(0,1)=dM34(1,1)",
        "dM35(0,0)=dM35(1,0)",
    )
    return {
        "ambient dimension": len(FREE_CELLS),
        "normal rank": len(row_space),
        "tangent dimension": len(FREE_CELLS) - len(row_space),
        "equations": equations,
        "digest": digest,
    }


def family_spokes(parameters):
    a, b, c, x, y = tuple(Q(value) for value in parameters)
    spokes = dict(BASE["SURVIVOR_SPOKES"])
    spokes[3, 4] = ((a, b), (c, b))
    spokes[0, 4] = ((x, Q(85)), (Q(0), Q(87)))
    spokes[3, 5] = ((Q(0), y), (Q(0), Q(96)))
    return spokes


def family_data(parameters):
    return BASE["build_packet"](family_spokes(parameters))


def family_differential(parameters):
    return CORE["differential_matrix"](family_data(parameters)[4])


def polynomial_differential_data():
    count = len(PARAMETER_NAMES)
    zero = (Q(0),) * count
    constant = family_differential(zero)
    linear = []
    for index in range(count):
        point = [Q(0)] * count
        point[index] = Q(1)
        linear.append(PREVIOUS["matrix_subtract"](
            family_differential(point), constant
        ))
    quadratic = {}
    for left, right in combinations(range(count), 2):
        point = [Q(0)] * count
        point[left] = point[right] = Q(1)
        value = family_differential(point)
        correction = [
            [
                value[row][column] - constant[row][column]
                - linear[left][row][column]
                - linear[right][row][column]
                for column in range(60)
            ]
            for row in range(64)
        ]
        if any(entry for row in correction for entry in row):
            quadratic[left, right] = correction
    require(tuple(quadratic) == ((3, 4),),
            ("the five-parameter quadratic support changed", quadratic))

    test = (Q(2), Q(3), Q(5), Q(7), Q(11))
    reconstructed = [
        [
            constant[row][column]
            + sum(test[index] * linear[index][row][column]
                  for index in range(count))
            + sum(test[left] * test[right] * value[row][column]
                  for (left, right), value in quadratic.items())
            for column in range(60)
        ]
        for row in range(64)
    ]
    require(reconstructed == family_differential(test),
            "the five-parameter differential stopped being quadratic")
    return constant, tuple(linear), quadratic


def rational_string(value):
    value = Q(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"({value.numerator}/{value.denominator})"


def polynomial_entry(constant, linear, quadratic, row, column):
    terms = []
    if constant[row][column]:
        terms.append(rational_string(constant[row][column]))
    for index, name in enumerate(PARAMETER_NAMES):
        coefficient = linear[index][row][column]
        if coefficient:
            terms.append(f"{rational_string(coefficient)}*{name}")
    for (left, right), value in quadratic.items():
        coefficient = value[row][column]
        if coefficient:
            terms.append(
                f"{rational_string(coefficient)}*"
                f"{PARAMETER_NAMES[left]}*{PARAMETER_NAMES[right]}"
            )
    return "+".join(terms) if terms else "0"


def matrix_entries(constant, linear, quadratic, selected_rows):
    return ",".join(
        polynomial_entry(constant, linear, quadratic, row, column)
        for row in selected_rows for column in range(60)
    )


def degenerate_m34_matrix(parameters):
    x, y = parameters
    return family_differential((0, 0, 0, x, y))


def degenerate_polynomial_data():
    constant = degenerate_m34_matrix((0, 0))
    linear = []
    for point in ((1, 0), (0, 1)):
        linear.append(PREVIOUS["matrix_subtract"](
            degenerate_m34_matrix(point), constant
        ))
    pair_value = degenerate_m34_matrix((1, 1))
    quadratic = [
        [
            pair_value[row][column] - constant[row][column]
            - linear[0][row][column] - linear[1][row][column]
            for column in range(60)
        ]
        for row in range(64)
    ]
    test = (Q(2), Q(3))
    reconstructed = [
        [
            constant[row][column]
            + test[0] * linear[0][row][column]
            + test[1] * linear[1][row][column]
            + test[0] * test[1] * quadratic[row][column]
            for column in range(60)
        ]
        for row in range(64)
    ]
    require(reconstructed == degenerate_m34_matrix(test),
            "the M34-zero family stopped being quadratic")
    return constant, tuple(linear), quadratic


def singular_program():
    constant, linear, quadratic = polynomial_differential_data()
    mixed_indices = tuple(
        index for index, word in enumerate(WORDS)
        if word not in PURE_WORDS
    )
    full = matrix_entries(
        constant, linear, quadratic, range(64)
    )
    mixed = matrix_entries(
        constant, linear, quadratic, mixed_indices
    )

    degenerate, degenerate_linear, degenerate_quadratic = (
        degenerate_polynomial_data()
    )
    old_names = globals()["PARAMETER_NAMES"]
    # The degenerate family only uses x,y.  Format it separately rather than
    # changing the global five-parameter formatter.
    def degenerate_entry(row, column):
        terms = []
        if degenerate[row][column]:
            terms.append(rational_string(degenerate[row][column]))
        for index, name in enumerate(("x", "y")):
            coefficient = degenerate_linear[index][row][column]
            if coefficient:
                terms.append(f"{rational_string(coefficient)}*{name}")
        coefficient = degenerate_quadratic[row][column]
        if coefficient:
            terms.append(f"{rational_string(coefficient)}*x*y")
        return "+".join(terms) if terms else "0"

    degenerate_full = ",".join(
        degenerate_entry(row, column)
        for row in range(64) for column in range(60)
    )
    degenerate_mixed = ",".join(
        degenerate_entry(row, column)
        for row in mixed_indices for column in range(60)
    )
    require(old_names == PARAMETER_NAMES,
            "the parameter-name ledger changed")
    return "\n".join((
        'print("BEGIN");',
        "ring r=(0,a,b,c,x,y),t,dp;",
        f"matrix D[64][60]={full};",
        f"matrix X[62][60]={mixed};",
        'print("FAMILY");',
        "rank(D);",
        "rank(X);",
        "ring s=(0,x,y),t,dp;",
        f"matrix D0[64][60]={degenerate_full};",
        f"matrix X0[62][60]={degenerate_mixed};",
        'print("M34ZERO");',
        "rank(D0);",
        "rank(X0);",
        'print("END");',
        "",
    ))


def audit_function_field_ranks():
    executable = which("Singular")
    require(executable is not None,
            "external dependency missing: Singular is not on PATH")
    program = singular_program()
    digest = sha256(program.encode()).hexdigest()
    require(digest == "5e43c4b39fce8115296ec5c247a5a6eaba0bd6b4b5f55a9f21c676bfcc818c85",
            ("the five-parameter Singular input changed", digest))
    try:
        completed = run(
            [executable, "-q"], input=program, text=True,
            capture_output=True, timeout=120, check=False,
        )
    except TimeoutExpired as error:
        raise RuntimeError("five-parameter Singular audit timed out") from error
    require(completed.returncode == 0,
            ("five-parameter Singular audit failed", completed.stderr))
    lines = tuple(
        line.strip() for line in completed.stdout.splitlines()
        if line.strip()
    )
    require(lines == (
        "BEGIN", "FAMILY", "55", "53",
        "M34ZERO", "50", "49", "END",
    ), ("the five-parameter rank ledger changed", lines))
    return digest, lines


def ranks_over_fields(matrix):
    return BASE["ranks_over_fields"](matrix)


def audit_calibration():
    endpoint, potential, blocks, numerators, packet = family_data(
        (1, 2, 3, 4, 5)
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
    }, ("the five-parameter calibration changed", profile))
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


def polynomial_test_points(count):
    origin = (0,) * count
    basis = tuple(
        tuple(int(slot == index) for slot in range(count))
        for index in range(count)
    )
    doubles = tuple(
        tuple(2 * int(slot == index) for slot in range(count))
        for index in range(count)
    )
    pairs = tuple(
        tuple(int(slot in (left, right)) for slot in range(count))
        for left, right in combinations(range(count), 2)
    )
    return origin, basis, doubles, pairs


def audit_uniform_r2():
    witnesses = {
        (0, 0): (1, (0, 0, 0, 1, 1, 1), Q(4416)),
        (0, 1): (2, (0, 1, 0, 1, 1, 1), Q(6336)),
        (1, 0): (0, (0, 0, 0, 1, 1, 1), Q(4416)),
        (1, 1): (4, (0, 0, 0, 0, 0, 0), Q(28)),
        (2, 0): (5, (0, 1, 0, 0, 1, 0), Q(33)),
        (2, 1): (0, (0, 1, 0, 1, 1, 1), Q(6336)),
        (3, 0): (1, (0, 0, 0, 0, 1, 0), Q(8624)),
        (3, 1): (2, (0, 0, 0, 0, 1, 0), Q(6216)),
    }
    origin, basis, doubles, pairs = polynomial_test_points(5)
    points = origin, *basis, *doubles, *pairs, (2, 3, 5, 7, 11)
    audited = {}
    for root_output, (neighbour, word, expected) in witnesses.items():
        root, output = root_output
        values = []
        for point in points:
            _endpoint, _potential, blocks, _numerators, packet = (
                family_data(point)
            )
            require(CORE["pure_column"](
                oriented_block(blocks, root, neighbour), output
            ), ("a five-parameter R2 pure column vanished", root_output))
            pair = tuple(sorted((root, neighbour)))
            values.append(CORE["cofactor"](packet, word, *pair))
        require(all(value == expected for value in values),
                ("a five-parameter R2 cofactor changed",
                 root_output, values))
        audited[root_output] = (neighbour, word, expected)
    return audited


def l1_matrix(parameters, selected_column):
    endpoint, _potential, blocks, _numerators, _packet = family_data(
        parameters
    )
    return BASE["l1_system"](endpoint, blocks, selected_column)


def matrix_vector(matrix, vector):
    return tuple(
        sum(value * vector[column]
            for column, value in enumerate(row))
        for row in matrix
    )


def audit_uniform_l1():
    base_point = (0, 0, 29, 1, 51)
    data = {}
    modes = {}
    digests = {}
    for name, selected_column in (("P/V", 0), ("Q/U", 1)):
        matrix = l1_matrix(base_point, selected_column)
        rank, _pivots, basis = BASE["rational_nullspace"](matrix)
        require(rank == 24 and len(basis) == 3,
                ("the five-parameter base L1 system changed", name))
        origin = l1_matrix((0, 0, 0, 0, 0), selected_column)
        directions = []
        for index in range(5):
            point = [Q(0)] * 5
            point[index] = Q(1)
            directions.append(PREVIOUS["matrix_subtract"](
                l1_matrix(point, selected_column), origin
            ))
        for vector in basis:
            require(not any(matrix_vector(origin, vector))
                    and all(not any(matrix_vector(direction, vector))
                            for direction in directions),
                    ("a fixed L1 mode changed", name))

        star_modes = tuple(vector[:12] for vector in basis
                           if any(vector[:12]))
        vacuous = tuple(vector for vector in basis if not any(vector[:12]))
        require(len(star_modes) == 2 and len(vacuous) == 1,
                ("the L1 mode split changed", name))

        fixed_rows = []
        for edge_index, edge in enumerate(EDGES):
            for cell_index in range(4):
                if edge == (3, 4):
                    continue
                if edge == (0, 4) and cell_index == 0:
                    continue
                if edge == (3, 5) and cell_index == 1:
                    continue
                fixed_rows.append(4 * edge_index + cell_index)
        require(CORE["rational_rank"](
            [origin[row] for row in fixed_rows]
        ) == 23, ("the fixed L1 rank-23 subsystem changed", name))

        digest = sha256(repr(basis).encode()).hexdigest()
        digests[name] = digest
        data[name] = {
            "rank on rank-55 locus": 24,
            "star dimension": 2,
            "vacuous dimension": 1,
            "fixed subsystem rank": 23,
        }
        modes[name] = star_modes
    require(digests == {
        "P/V": "e63aa09838b43d51f3de060f427bb45628e446e61e99f28ea790c80a5ea1f1a6",
        "Q/U": "45b6de4a61f4b66e7afae27574483e06bc4843218eff9a600dab6fff52bc03c3",
    }, ("the five-parameter L1 bases changed", digests))
    return data, modes, digests


def product_outputs(parameters, modes):
    packet = family_data(parameters)[4]
    outputs = tuple(
        tuple(CORE["apply_differential"](
            packet, BASE["factored_tangent"](u_mode, v_mode)
        ))
        for u_mode in modes["Q/U"]
        for v_mode in modes["P/V"]
    )
    return outputs, tuple(CORE["matching_tensor"](packet))


def vector_subtract(*vectors):
    head, *tail = vectors
    return tuple(
        head[index] - sum(vector[index] for vector in tail)
        for index in range(len(head))
    )


def audit_factored_coefficients(modes):
    count = 5
    zero = (Q(0),) * count
    constant, constant_slope = product_outputs(zero, modes)
    columns = list(constant)
    linear = []
    slope_columns = [constant_slope]
    for index in range(count):
        point = [Q(0)] * count
        point[index] = Q(1)
        outputs, slope = product_outputs(point, modes)
        directions = tuple(
            vector_subtract(outputs[slot], constant[slot])
            for slot in range(4)
        )
        linear.append(directions)
        columns.extend(directions)
        slope_columns.append(vector_subtract(slope, constant_slope))

    quadratic = {}
    for left, right in combinations(range(count), 2):
        point = [Q(0)] * count
        point[left] = point[right] = Q(1)
        outputs, slope = product_outputs(point, modes)
        corrections = tuple(
            vector_subtract(
                outputs[slot], constant[slot],
                linear[left][slot], linear[right][slot]
            )
            for slot in range(4)
        )
        quadratic[left, right] = corrections
        columns.extend(corrections)
        slope_columns.append(vector_subtract(
            slope, constant_slope,
            slope_columns[left + 1], slope_columns[right + 1]
        ))

    test = (Q(2), Q(3), Q(5), Q(7), Q(11))
    outputs, slope = product_outputs(test, modes)
    for slot in range(4):
        reconstructed = tuple(
            constant[slot][row]
            + sum(test[index] * linear[index][slot][row]
                  for index in range(count))
            + sum(test[left] * test[right]
                  * correction[slot][row]
                  for (left, right), correction in quadratic.items())
            for row in range(64)
        )
        require(outputs[slot] == reconstructed,
                ("a factored product stopped being quadratic", slot))
    require(all(
        slope[row] == 2 * sum(output[row] for output in outputs)
        for row in range(64)
    ), "the direct/factored Euler identity changed")

    coefficient_matrix = BASE["column_matrix"](tuple(columns))
    with_direct = BASE["column_matrix"](
        tuple(columns + slope_columns)
    )
    pure_zero, pure_one = BASE["pure_targets"]()
    ranks = {
        "all product coefficients": ranks_over_fields(coefficient_matrix),
        "coefficients+direct": ranks_over_fields(with_direct),
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
        "all product coefficients": (16, 16, 16, 16),
        "coefficients+direct": (16, 16, 16, 16),
        "coefficients|e0": (17, 17, 17, 17),
        "coefficients|e1": (17, 17, 17, 17),
        "coefficients|e0,e1": (18, 18, 18, 18),
    }, ("the five-parameter factored span changed", ranks))
    digest = sha256(repr(tuple(
        tuple(row) for row in coefficient_matrix
    )).encode()).hexdigest()
    require(digest == "d28dc4a21a918d6b7089a9ee4d8b67ffe6ad89324ed571ecae7f8da4f4f3b477",
            ("the five-parameter coefficient matrix changed", digest))
    return ranks, digest


def main():
    tangent = audit_full_determinantal_tangent()
    singular_digest, singular_ledger = audit_function_field_ranks()
    calibration = audit_calibration()
    r2 = audit_uniform_r2()
    l1, modes, l1_digests = audit_uniform_l1()
    factored, coefficient_digest = audit_factored_coefficients(modes)

    print("full all-spokes tangent and five-parameter family: all checks passed")
    print(f"  full determinantal tangent : {tangent}")
    print(f"  function-field ranks       : {singular_ledger}")
    print(f"  Singular input SHA-256     : {singular_digest}")
    print(f"  exact calibration          : {calibration}")
    print(f"  uniform R2 witnesses       : {len(r2)}")
    print(f"  uniform L1 systems         : {l1}")
    print(f"  fixed L1 basis digests     : {l1_digests}")
    print(f"  factored coefficient span : {factored}")
    print(f"  coefficient SHA-256        : {coefficient_digest}")
    print("  conclusion                 : rank-55 five-parameter family excluded")
    print("  residual status            : 26D tangent is not a global component claim")


if __name__ == "__main__":
    main()
