#!/usr/bin/env python3
"""Exclude all site-4 zero-cell lifts of the transverse incidence boundary.

Start with the rank-54/52 full-R2 packet underlying the dense transverse
linear-L0 survivor.  There are exactly eight zero entries on the four
spokes from sites 0,1,2,3 to zero site 4.  Along every corresponding affine
line M + t E:

* four lines destroy the sole output-one R2 witness at root 0 or 1;
* three lines have differential rank at most 54 over Q(t);
* the remaining line has mixed differential rank at least 54 for t != 0.

The checker is standard-library only.  All large vectors and minors below
are exact certificates, not search data.
"""

from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
survivor = run_path(str(
    HERE
    / "verify_level_two_two_invertible_transverse_column_l0_incidence_survivor.py"
))
guard = survivor["guard"]
rank_core = survivor["rank_core"]
dense_core = survivor["dense_core"]
old = survivor["old_survivor"]

SITES = survivor["SITES"]
COLOURS = survivor["COLOURS"]
EDGES = survivor["EDGES"]
CELLS = survivor["CELLS"]
WORDS = rank_core["WORDS"]
ZERO_MATRIX = survivor["ZERO_MATRIX"]

BASE_BLOCKS = dict(guard["CORE_BLOCKS"])
BASE_BLOCKS.update(old["REPLACEMENT"])
BASE_BLOCKS[4, 5] = ZERO_MATRIX

SITE4_ZERO_CELLS = (
    (0, 4, 0, 0),
    (0, 4, 1, 0),
    (1, 4, 0, 0),
    (1, 4, 1, 0),
    (2, 4, 0, 0),
    (2, 4, 1, 0),
    (3, 4, 0, 0),
    (3, 4, 1, 1),
)
R2_BREAKING = frozenset(SITE4_ZERO_CELLS[:4])
RANK_BOUNDED = frozenset((
    (2, 4, 0, 0),
    (3, 4, 0, 0),
    (3, 4, 1, 1),
))
MIXED_OBSTRUCTED = (2, 4, 1, 0)


def packet(blocks):
    return {
        (u, v, a, b): blocks[u, v][a][b]
        for u, v in EDGES
        for a, b in product(COLOURS, repeat=2)
    }


def moved_blocks(direction, value):
    u, v, a, b = direction
    blocks = dict(BASE_BLOCKS)
    changed = [list(row) for row in blocks[u, v]]
    changed[a][b] = value
    blocks[u, v] = tuple(tuple(row) for row in changed)
    return blocks


def differential(blocks):
    return rank_core["differential"](packet(blocks))


BASE_D = differential(BASE_BLOCKS)


def matrix_vector(matrix, vector):
    return [
        sum(entry * value for entry, value in zip(row, vector))
        for row in matrix
    ]


def add_vectors(left, right):
    return [a + b for a, b in zip(left, right)]


def scale_vector(scalar, vector):
    return [scalar * value for value in vector]


def derivative_increment(direction):
    moved = differential(moved_blocks(direction, 1))
    return [
        [entry - base for entry, base in zip(row, base_row)]
        for row, base_row in zip(moved, BASE_D)
    ]


def orient_block(blocks, root, neighbour):
    if root < neighbour:
        return blocks[root, neighbour]
    return dense_core["transpose"](blocks[neighbour, root])


def r2_tables(blocks):
    tables = {}
    failing = []
    for root in SITES:
        p_block, q_block = guard["endpoint_blocks"](root)
        incident = {
            neighbour: orient_block(blocks, root, neighbour)
            for neighbour in SITES
            if neighbour != root
        }
        incident["p"] = p_block
        incident["q"] = q_block
        pure = {
            output: tuple(
                label
                for label, block in incident.items()
                if guard["pure_column"](block, output)
            )
            for output in COLOURS
        }
        has_exit = (
            pure[0]
            and pure[1]
            and any(left != right for left in pure[0] for right in pure[1])
        )
        if not has_exit:
            failing.append(root)
        tables[root] = pure
    return tables, tuple(failing)


def gauge_tangent(blocks, mu):
    values = packet(blocks)
    return [
        (mu[u] + mu[v]) * values[u, v, a, b]
        for u, v, a, b in CELLS
    ]


BASE_EXTRA_DATA = {
    (0, 1, 0, 1): -1591243920,
    (0, 1, 1, 0): -1591243920,
    (0, 2, 1, 0): 10277606304,
    (0, 3, 0, 0): -19547490379,
    (0, 3, 1, 0): -7859314041,
    (0, 4, 0, 1): 2645746709736,
    (0, 4, 1, 1): 1216624926894,
    (0, 5, 0, 0): 1301490536808,
    (0, 5, 0, 1): 2129070420798,
    (0, 5, 1, 0): -380271433248,
    (0, 5, 1, 1): 433830178936,
    (1, 2, 1, 0): -14433105682,
    (1, 3, 0, 0): -24830941944,
    (1, 3, 1, 0): -5962238238,
    (1, 4, 0, 1): 658389860270,
    (1, 4, 1, 1): -639266748624,
    (1, 5, 0, 0): 89109659520,
    (1, 5, 0, 1): 92292147360,
    (1, 5, 1, 1): -29703219840,
    (2, 3, 1, 0): 2077749689,
    (2, 4, 0, 1): -1345735506446,
    (2, 4, 1, 1): 36598610160,
    (2, 5, 0, 1): -873390226464,
    (3, 4, 0, 1): -179084732400,
    (3, 5, 0, 0): 380271433248,
    (3, 5, 0, 1): 29703219840,
    (4, 5, 1, 0): 43845277633584,
    (4, 5, 1, 1): 6091281725760,
}
BASE_EXTRA = [BASE_EXTRA_DATA.get(cell, 0) for cell in CELLS]


P24_X0_DATA = {
    (0, 1, 0, 1): -59314157720612988973839,
    (0, 1, 1, 0): -59314157720612988973839,
    (0, 2, 1, 0): -77226033158032759745472,
    (0, 3, 0, 0): 75609251818517605221923,
    (0, 3, 1, 0): 59054961707711901143238,
    (0, 4, 0, 1): -19880166362697483942763248,
    (0, 4, 1, 1): -9141731466074770777111092,
    (0, 5, 0, 0): -9779412479662975031426544,
    (0, 5, 0, 1): -15997855731089999594633364,
    (0, 5, 1, 0): 2857363226847212110582464,
    (0, 5, 1, 1): -3259804159887658343808848,
    (1, 2, 1, 0): 108450495670156293683276,
    (1, 3, 0, 0): 115309157971641066682593,
    (1, 3, 1, 0): 44800315778264200867284,
    (1, 4, 0, 1): -4947147777039774758519860,
    (1, 4, 1, 1): 4803456531201335369867232,
    (1, 5, 0, 0): -669570843369846362031360,
    (1, 5, 0, 1): -693484087775912303532480,
    (1, 5, 1, 1): 223190281123282120677120,
    (2, 3, 1, 0): -15612231256061766968902,
    (2, 4, 0, 1): 13390325485882396472481382,
    (2, 4, 1, 1): 1364225627574098746398297,
    (2, 5, 0, 0): 3991163675724173744566344,
    (2, 5, 0, 1): 6562662607786402044188352,
    (3, 4, 0, 1): 1345644411095728199383200,
    (3, 5, 0, 0): -2857363226847212110582464,
    (3, 5, 0, 1): -223190281123282120677120,
    (4, 5, 1, 0): -329453840145296746571476512,
    (4, 5, 1, 1): -45769949793210212033143680,
}
P24_X1_DATA = {
    (0, 2, 1, 0): 6721141419298228679616,
    (0, 3, 0, 0): -6721141419298228679616,
    (0, 4, 0, 0): 10654883590587657432997,
    (0, 4, 0, 1): 1479119735091334304101056,
    (0, 4, 1, 0): -861151643171920724452,
    (0, 4, 1, 1): 200430748333776697407072,
    (0, 5, 0, 0): 849968186691966635220480,
    (0, 5, 0, 1): 1375461859882278597876000,
    (0, 5, 1, 0): -248682232514034461145792,
    (0, 5, 1, 1): 275970712960032126072960,
    (1, 2, 1, 0): -4528917734935910344512,
    (1, 3, 0, 0): -15708420043444247636928,
    (1, 4, 0, 0): 1188146945300449827659,
    (1, 4, 0, 1): 596797262593713002525952,
    (1, 4, 1, 0): 5302994605284680815052,
    (1, 4, 1, 1): -250010239068035590289184,
    (1, 5, 0, 0): 469539096957350166281472,
    (1, 5, 0, 1): 501977431764036326187552,
    (1, 5, 1, 1): -163865048256406807761024,
    (2, 4, 0, 1): -1094161727621781924817536,
    (2, 5, 0, 0): -469539096957350166281472,
    (2, 5, 0, 1): -820367040512425714182048,
    (3, 4, 0, 0): -58193810064539980418786,
    (3, 4, 0, 1): -785170051812722592533664,
    (3, 5, 0, 0): 248682232514034461145792,
    (3, 5, 0, 1): 163865048256406807761024,
    (4, 5, 0, 0): 1653538927815933232010664,
    (4, 5, 0, 1): 1592748226438758749327046,
    (4, 5, 1, 0): 54638411723240672307101184,
    (4, 5, 1, 1): 26470595149462192765311360,
}
P24_X0 = [P24_X0_DATA.get(cell, 0) for cell in CELLS]
P24_X1 = [P24_X1_DATA.get(cell, 0) for cell in CELLS]


def audit_family_and_r2():
    zero_cells = tuple(
        (u, v, a, b)
        for u in range(4)
        for v in (4,)
        for a, b in product(COLOURS, repeat=2)
        if BASE_BLOCKS[u, v][a][b] == 0
    )
    require(zero_cells == SITE4_ZERO_CELLS,
            ("site-4 zero-cell census changed", zero_cells))
    require(
        R2_BREAKING | RANK_BOUNDED | {MIXED_OBSTRUCTED}
        == frozenset(SITE4_ZERO_CELLS),
        "the three obstruction classes do not partition the family",
    )

    base_tables, base_failing = r2_tables(BASE_BLOCKS)
    require(not base_failing, ("base packet lost R2", base_failing))
    require(base_tables[0][1] == (4,) and base_tables[1][1] == (4,),
            ("sole invertible-root witnesses changed", base_tables))

    failures = {}
    for direction in R2_BREAKING:
        expected = direction[0]
        tables, failing = r2_tables(moved_blocks(direction, 1))
        require(failing == (expected,),
                ("R2-breaking direction changed", direction, failing, tables))
        # The moved entry is in output column zero of the sole output-one
        # witness.  Its support, and hence this table, is identical for every
        # nonzero parameter.
        require(not tables[expected][1],
                ("breaking direction retained output one", direction))
        failures[direction] = failing
    return failures


def audit_generic_kernel_scope():
    require(all(
        (u, v) in old["FREE_EDGES"]
        and survivor["POTENTIAL"][u] + survivor["POTENTIAL"][v] == 0
        for u, v, _a, _b in SITE4_ZERO_CELLS
    ), "a one-cell direction left the zero-multiplier cut")

    # The generic-kernel numerator is fixed and zero on every moved edge.
    # Checking the two coefficients t=0,1 proves the affine identity.
    selected_checks = 0
    numerator_vector = []
    for u, v, a, b in CELLS:
        numerator = dense_core["matrix_product"](
            dense_core["matrix_product"](
                survivor["X"][u], survivor["J"]
            ),
            dense_core["transpose"](survivor["X"][v]),
        )
        numerator_vector.append(numerator[a][b])
    require(-sum(survivor["POTENTIAL"]) == -1,
            "direct selected value changed")

    for direction in SITE4_ZERO_CELLS:
        for value in (0, 1):
            blocks = moved_blocks(direction, value)
            for u, v in EDGES:
                numerator = dense_core["matrix_product"](
                    dense_core["matrix_product"](
                        survivor["X"][u], survivor["J"]
                    ),
                    dense_core["transpose"](survivor["X"][v]),
                )
                multiplier = survivor["POTENTIAL"][u] + survivor["POTENTIAL"][v]
                for a, b in product(COLOURS, repeat=2):
                    require(
                        numerator[a][b] == multiplier * blocks[u, v][a][b],
                        ("generic-kernel coefficient failed",
                         direction, value, u, v, a, b),
                    )
            derivative = differential(blocks)
            tangent = matrix_vector(derivative, numerator_vector)
            values = packet(blocks)
            slope = [
                rank_core["hafnian"](values, SITES, word)
                for word in WORDS
            ]
            require(all(
                -slope_value + tangent_value == 0
                for slope_value, tangent_value in zip(slope, tangent)
            ), ("selected-row coefficient failed", direction, value))
            selected_checks += len(WORDS)
    return (
        2 * len(SITE4_ZERO_CELLS) * len(CELLS),
        selected_checks,
    )


def audit_polynomial_kernel(direction, x0, x1):
    d1 = derivative_increment(direction)
    require(not any(matrix_vector(BASE_D, x0)),
            ("polynomial kernel constant coefficient failed", direction))
    require(not any(add_vectors(
        matrix_vector(BASE_D, x1),
        matrix_vector(d1, x0),
    )), ("polynomial kernel linear coefficient failed", direction))
    require(not any(matrix_vector(d1, x1)),
            ("polynomial kernel quadratic coefficient failed", direction))

    # Independence at one parameter proves independence over Q(t).  Hence
    # the five gauge polynomials plus x0+t*x1 force rank <= 54 over Q(t);
    # every 55-minor is identically zero and the bound holds at every
    # specialization.
    value = 2
    blocks = moved_blocks(direction, value)
    gauges = []
    for basis in range(5):
        mu = [0] * 6
        mu[basis] = 1
        mu[5] = -1
        gauges.append(gauge_tangent(blocks, mu))
    extra = add_vectors(x0, scale_vector(value, x1))
    columns = gauges + [extra]
    rank = dense_core["rational_rank"]([
        [column[row] for column in columns]
        for row in range(len(CELLS))
    ])
    require(rank == 6,
            ("polynomial kernel certificate became dependent",
             direction, rank))
    return rank


def audit_rank_bounded_lines():
    require(not any(matrix_vector(BASE_D, BASE_EXTRA)),
            "base extra kernel vector failed")
    results = {}
    results[(2, 4, 0, 0)] = audit_polynomial_kernel(
        (2, 4, 0, 0), P24_X0, P24_X1
    )
    zero = [0] * len(CELLS)
    for direction in ((3, 4, 0, 0), (3, 4, 1, 1)):
        results[direction] = audit_polynomial_kernel(
            direction, BASE_EXTRA, zero
        )
    require(frozenset(results) == RANK_BOUNDED,
            ("rank-bounded directions changed", results))
    return results


MIXED_COLUMNS = (
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
    18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
    35, 37, 38, 39, 41, 42, 43, 45, 46, 47, 48, 49, 51, 52, 53, 54,
    56, 57, 58, 59,
)
MIXED_ROWS_A = (
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
    18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
    34, 35, 36, 37, 38, 39, 40, 42, 43, 44, 47, 48, 49, 50, 51, 52,
    54, 55, 56, 60,
)
MIXED_ROWS_B = (
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
    18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 31, 32, 33, 34,
    35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 47, 48, 49, 50, 51, 52,
    54, 55, 56, 60,
)


def bareiss_determinant(matrix):
    work = [list(row) for row in matrix]
    size = len(work)
    require(all(len(row) == size for row in work),
            "Bareiss input is not square")
    if size == 0:
        return 1
    sign = 1
    previous = 1
    for column in range(size - 1):
        pivot_row = next(
            (row for row in range(column, size) if work[row][column]),
            None,
        )
        if pivot_row is None:
            return 0
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
            sign = -sign
        pivot = work[column][column]
        for row in range(column + 1, size):
            for other in range(column + 1, size):
                numerator = (
                    pivot * work[row][other]
                    - work[row][column] * work[column][other]
                )
                require(numerator % previous == 0,
                        ("Bareiss division ceased to be exact",
                         column, row, other))
                work[row][other] = numerator // previous
            work[row][column] = 0
        previous = pivot
    return sign * work[-1][-1]


def selected_minor(mixed0, mixed1, rows, value):
    return [
        [
            mixed0[row][column] + value * mixed1[row][column]
            for column in MIXED_COLUMNS
        ]
        for row in rows
    ]


def audit_mixed_minor_cover():
    d1 = derivative_increment(MIXED_OBSTRUCTED)
    mixed_indices = [
        index
        for index, word in enumerate(WORDS)
        if word not in ((0,) * 6, (1,) * 6)
    ]
    require(len(mixed_indices) == 62, "mixed-row census changed")
    mixed0 = [BASE_D[index] for index in mixed_indices]
    mixed1 = [d1[index] for index in mixed_indices]

    increment_ranks = {}
    constants = {}
    factorizations = {
        "A": lambda value: (
            value ** 11
            * (634878 * value + 1508087)
            * (276626208 * value - 1193709223)
        ),
        "B": lambda value: (
            value ** 12 * (116590108 * value - 677131063)
        ),
    }
    row_sets = {"A": MIXED_ROWS_A, "B": MIXED_ROWS_B}
    for label, rows in row_sets.items():
        inc_minor = selected_minor(mixed0, mixed1, rows, 0)
        inc_part = selected_minor(
            [[0] * len(CELLS) for _ in mixed0], mixed1, rows, 1
        )
        increment_rank = dense_core["rational_rank"](inc_part)
        require(increment_rank <= 15,
                ("minor increment rank changed", label, increment_rank))
        increment_ranks[label] = increment_rank

        factor_at_one = factorizations[label](1)
        determinant_at_one = bareiss_determinant(
            selected_minor(mixed0, mixed1, rows, 1)
        )
        require(factor_at_one and determinant_at_one % factor_at_one == 0,
                ("minor normalization failed", label))
        constant = determinant_at_one // factor_at_one
        require(constant, ("minor constant vanished", label))
        constants[label] = constant

        # det(A+tB) has degree at most rank(B), hence at most 15.  Agreement
        # at sixteen values proves the displayed factorization identically.
        for value in range(16):
            determinant = bareiss_determinant(
                selected_minor(mixed0, mixed1, rows, value)
            )
            require(
                determinant == constant * factorizations[label](value),
                ("mixed-minor factorization failed",
                 label, value, determinant),
            )

    roots_a = (
        Q(-1508087, 634878),
        Q(1193709223, 276626208),
    )
    root_b = Q(677131063, 116590108)
    require(root_b not in roots_a,
            ("nonzero mixed-minor roots collided", roots_a, root_b))
    return increment_ranks, constants, roots_a, root_b


def audit_base_and_calibrations():
    pure_zero = [int(word == (0,) * 6) for word in WORDS]
    pure_one = [int(word == (1,) * 6) for word in WORDS]

    def append_columns(matrix, *columns):
        return [
            row[:] + [column[index] for column in columns]
            for index, row in enumerate(matrix)
        ]

    def incidence_signature(derivative):
        mixed = [
            row
            for row, word in zip(derivative, WORDS)
            if word not in ((0,) * 6, (1,) * 6)
        ]
        return (
            dense_core["rational_rank"](derivative),
            dense_core["rational_rank"](mixed),
            dense_core["rational_rank"](
                append_columns(derivative, pure_zero)
            ),
            dense_core["rational_rank"](
                append_columns(derivative, pure_one)
            ),
            dense_core["rational_rank"](
                append_columns(derivative, pure_zero, pure_one)
            ),
        )

    base_signature = incidence_signature(BASE_D)
    require(base_signature == (54, 52, 54, 54, 54),
            ("base boundary ranks changed", base_signature))
    base_ranks = base_signature[:2]

    calibration = {}
    for direction in SITE4_ZERO_CELLS:
        calibration[direction] = incidence_signature(
            differential(moved_blocks(direction, 1))
        )
    require(all(
        calibration[direction] == (55, 53, 55, 55, 55)
        for direction in R2_BREAKING
    ), ("R2-breaking incidence calibration changed", calibration))
    require(calibration[MIXED_OBSTRUCTED] == (55, 54, 55, 56, 56),
            ("mixed-obstructed calibration changed", calibration))
    require(all(
        calibration[direction][0] <= 54
        for direction in RANK_BOUNDED
    ), ("rank-bounded calibration changed", calibration))
    return base_signature, calibration


def main():
    failures = audit_family_and_r2()
    generic, selected = audit_generic_kernel_scope()
    kernels = audit_rank_bounded_lines()
    increments, constants, roots_a, root_b = audit_mixed_minor_cover()
    base_ranks, calibration = audit_base_and_calibrations()
    print("dense transverse site-4 one-cell R2 obstruction: all checks passed")
    print(f"  zero-cell affine lines       : {len(SITE4_ZERO_CELLS)}")
    print(f"  generic-kernel coefficients : {generic}")
    print(f"  selected-row coefficients   : {selected}")
    print(f"  R2-breaking lines           : {failures}")
    print(f"  rank-bounded kernels        : {kernels}")
    print(f"  mixed-minor increment ranks : {increments}")
    print(f"  nonzero root separation     : {roots_a} versus {root_b}")
    print(f"  base/unit calibration       : {base_ranks}, {calibration}")
    print(f"  determinant constants       : {constants}")


if __name__ == "__main__":
    main()
