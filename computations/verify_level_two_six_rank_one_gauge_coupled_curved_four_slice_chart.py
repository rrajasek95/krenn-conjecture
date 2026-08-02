#!/usr/bin/env python3
"""Exact curved four-slice chart through the rank-50 precursor.

The exact-line cone at the gauge-coupled precursor is smaller than the
formal local fibre.  This checker constructs the canonical second-order
normal correction for every vector in the 15-dimensional Jacobian kernel,
audits cubic and quartic compatibility, sums the higher corrections to a
rational 15-parameter chart, and proves the chart has differential rank at
most 51/49.  Standard library plus exact Singular; live under -O and -I -S.
"""

from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
from runpy import run_path
from shutil import which
from subprocess import run


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
LOCAL = run_path(str(
    HERE
    / "verify_level_two_six_rank_one_gauge_coupled_four_slice_local_geometry.py"
))
SIX = LOCAL["SIX"]
CORE = LOCAL["CORE"]
BASE = LOCAL["BASE"]
CELLS = LOCAL["CELLS"]
WORDS = LOCAL["WORDS"]
Jet = LOCAL["Jet"]
Poly = LOCAL["Poly"]
rational_rref = LOCAL["rational_rref"]
rational_nullspace = LOCAL["rational_nullspace"]
flatten_outputs = LOCAL["flatten_outputs"]
four_tangents = LOCAL["four_tangents"]
as_poly = LOCAL["as_poly"]
polynomial_string = LOCAL["polynomial_string"]
rational_string = LOCAL["rational_string"]

PIVOT_COLUMNS = (
    0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 16, 18,
    21, 23, 24, 25, 26, 30, 31, 34, 36, 37, 38, 39, 40, 41,
    42, 43, 44, 46, 48, 49, 50, 51, 52, 53, 54, 55, 57, 58, 59,
)
PIVOT_ROWS = (
    0, 1, 2, 3, 4, 8, 9, 10, 11, 12, 13, 14, 15,
    65, 66, 67, 71, 73, 74, 75, 81, 82, 83, 85, 86, 87,
    97, 98, 99, 107, 195, 199, 203, 211, 215, 219, 223,
    227, 231, 235, 239, 243, 247, 251, 255,
)
FREE_CELLS = (
    (0, 3, 0, 0), (0, 3, 1, 0),
    (0, 5, 0, 1), (0, 5, 1, 1),
    (1, 2, 0, 0), (1, 2, 1, 0),
    (1, 3, 1, 1),
    (1, 4, 0, 0), (1, 4, 0, 1),
    (1, 5, 0, 0), (1, 5, 0, 1), (1, 5, 1, 1),
    (2, 5, 0, 1), (2, 5, 1, 1),
    (4, 5, 0, 0),
)
PIVOT_DETERMINANT = Q(
    260659154113472854093012287641452863135382828567552,
    5540457914208984375,
)


def exact_inverse_and_determinant(matrix):
    size = len(matrix)
    require(size and all(len(row) == size for row in matrix),
            "non-square pivot matrix")
    work = [
        list(map(Q, row))
        + [Q(int(row_index == column)) for column in range(size)]
        for row_index, row in enumerate(matrix)
    ]
    determinant = Q(1)
    sign = 1
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]),
            None,
        )
        require(pivot is not None, ("singular pivot minor", column))
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign = -sign
        pivot_value = work[column][column]
        determinant *= pivot_value
        work[column] = [entry / pivot_value for entry in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            multiple = work[row][column]
            work[row] = [
                entry - multiple * pivot_entry
                for entry, pivot_entry
                in zip(work[row], work[column], strict=True)
            ]
    inverse = tuple(tuple(row[size:]) for row in work)
    return inverse, sign * determinant


def reconstruct_linear_data():
    packet, u_star, v_star, _previous = SIX["rank50_member"]()
    tangents = four_tangents(u_star, v_star)
    target = tuple(map(as_poly, flatten_outputs(packet, tangents)))
    jets = {}
    for column, cell in enumerate(CELLS):
        gradient = [Q(0)] * 60
        gradient[column] = Q(1)
        jets[cell] = Jet(packet[cell], gradient)
    outputs = flatten_outputs(jets, tangents)
    jacobian = [list(output.gradient) for output in outputs]
    _reduced, pivot_columns = rational_rref(jacobian)
    require(pivot_columns == PIVOT_COLUMNS,
            ("normal pivot columns changed", pivot_columns))
    column_basis = [
        [jacobian[row][column] for column in PIVOT_COLUMNS]
        for row in range(256)
    ]
    _row_reduced, pivot_rows = rational_rref(
        list(map(list, zip(*column_basis, strict=True)))
    )
    require(pivot_rows == PIVOT_ROWS,
            ("normal pivot rows changed", pivot_rows))
    square = [
        [jacobian[row][column] for column in PIVOT_COLUMNS]
        for row in PIVOT_ROWS
    ]
    inverse, determinant = exact_inverse_and_determinant(square)
    require(determinant == PIVOT_DETERMINANT,
            ("local implicit minor changed", determinant))
    kernel = rational_nullspace(jacobian)
    require(len(kernel) == 15, "formal tangent dimension changed")
    free_columns = tuple(
        column for column in range(60) if column not in PIVOT_COLUMNS
    )
    require(tuple(CELLS[column] for column in free_columns) == FREE_CELLS,
            "the fifteen local coordinate cells changed")
    require(all(
        kernel[variable][free_columns[coordinate]]
        == int(variable == coordinate)
        for variable in range(15)
        for coordinate in range(15)
    ), "the kernel basis lost its free-coordinate normalization")
    return (
        packet, u_star, v_star, tangents, target,
        jacobian, kernel, inverse, free_columns,
    )


def jacobian_apply(jacobian, vector):
    return tuple(
        sum(jacobian[row][column] * vector[CELLS[column]]
            for column in range(60))
        for row in range(256)
    )


def normal_correction(outputs, inverse):
    correction = [Poly() for _ in CELLS]
    for normal_coordinate, column in enumerate(PIVOT_COLUMNS):
        correction[column] = sum(
            -inverse[normal_coordinate][row_coordinate]
            * outputs[PIVOT_ROWS[row_coordinate]]
            for row_coordinate in range(45)
        )
    return {
        cell: correction[column] for column, cell in enumerate(CELLS)
    }


EXPECTED_SECOND_ORDER = {
    (0, 1, 0, 0): {
        (0, 4): Q(-1, 2),
        (0, 14): Q(-1, 6),
        (4, 14): Q(-1, 3),
    },
    (0, 1, 0, 1): {(0, 5): Q(-1, 2), (5, 14): Q(-1, 3)},
    (0, 1, 1, 0): {(1, 4): Q(-1, 2), (1, 14): Q(-1, 6)},
    (0, 1, 1, 1): {(1, 5): Q(-1, 2)},
    (0, 2, 1, 1): {(6, 6): Q(5, 49)},
    (2, 3, 0, 0): {(14, 14): Q(2, 9)},
}

EXPECTED_THIRD_ORDER = {
    (0, 1, 0, 0): {(0, 4, 14): Q(-1, 6)},
    (0, 1, 0, 1): {(0, 5, 14): Q(-1, 6)},
    (0, 1, 1, 0): {(1, 4, 14): Q(-1, 6)},
    (0, 1, 1, 1): {(1, 5, 14): Q(-1, 6)},
    (0, 2, 1, 1): {(6, 6, 6): Q(-5, 343)},
    (2, 3, 0, 0): {(14, 14, 14): Q(-2, 27)},
}

CUBIC_ROWS = (0, 195, 211, 227, 243, 255)
EXPECTED_CUBICS = (
    {(14, 14, 14): Q(1, 27)},
    {(0, 4, 14): Q(1, 105), (14, 14, 14): Q(-2, 945)},
    {(0, 5, 14): Q(1, 105)},
    {(1, 4, 14): Q(1, 105)},
    {(1, 5, 14): Q(1, 105)},
    {(6, 6, 6): Q(1, 343)},
)
QUARTIC_ROWS = (195, 211, 227, 243)
EXPECTED_QUARTICS = (
    {
        (0, 4, 14, 14): Q(-1, 315),
        (0, 14, 14, 14): Q(-1, 945),
        (4, 14, 14, 14): Q(-2, 945),
    },
    {
        (0, 5, 14, 14): Q(-1, 315),
        (5, 14, 14, 14): Q(-2, 945),
    },
    {
        (1, 4, 14, 14): Q(-1, 315),
        (1, 14, 14, 14): Q(-1, 945),
    },
    {(1, 5, 14, 14): Q(-1, 315)},
)


def degree_part(polynomial, degree):
    polynomial = as_poly(polynomial)
    return Poly({
        monomial: coefficient
        for monomial, coefficient in polynomial.coefficients.items()
        if len(monomial) == degree
    })


def independent_polynomial_rows(polynomials, degree):
    monomials = tuple(sorted({
        monomial
        for polynomial in polynomials
        for monomial in polynomial.coefficients
        if len(monomial) == degree
    }))
    require(monomials, ("empty homogeneous system", degree))
    matrix = [
        [polynomial.coefficients.get(monomial, Q(0))
         for monomial in monomials]
        for polynomial in polynomials
    ]
    _reduced, pivots = rational_rref(matrix)
    _transpose, rows = rational_rref(
        list(map(list, zip(*matrix, strict=True)))
    )
    return len(pivots), rows


def audit_second_through_fourth_order(
    packet, tangents, target, jacobian, kernel, inverse,
):
    direction = {
        cell: Poly({
            (variable,): kernel[variable][column]
            for variable in range(15)
        })
        for column, cell in enumerate(CELLS)
    }
    require(all(
        not output.coefficients
        for output in jacobian_apply(jacobian, direction)
    ), "a pinned first-order direction left the Jacobian kernel")
    quadratic = tuple(map(as_poly, flatten_outputs(direction, tangents)))
    second = normal_correction(quadratic, inverse)
    support = {
        cell: value.coefficients
        for cell, value in second.items() if value.coefficients
    }
    require(support == EXPECTED_SECOND_ORDER,
            ("universal second-order correction changed", support))
    second_equations = tuple(
        left + right
        for left, right in zip(
            jacobian_apply(jacobian, second), quadratic, strict=True
        )
    )
    require(all(not equation.coefficients for equation in second_equations),
            "the universal second-order equation failed")

    quadratic_arc = {
        cell: Poly({(): packet[cell]}) + direction[cell] + second[cell]
        for cell in CELLS
    }
    residual = tuple(
        as_poly(output) - target[row]
        for row, output in enumerate(flatten_outputs(quadratic_arc, tangents))
    )
    require(all(
        all(len(monomial) in (3, 4) for monomial in value.coefficients)
        for value in residual
    ), "the quadratic arc acquired a wrong homogeneous order")
    cubics = tuple(degree_part(value, 3) for value in residual)
    quartics = tuple(degree_part(value, 4) for value in residual)
    cubic_rank, cubic_rows = independent_polynomial_rows(cubics, 3)
    quartic_rank, quartic_rows = independent_polynomial_rows(quartics, 4)
    require((cubic_rank, cubic_rows) == (6, CUBIC_ROWS),
            ("raw cubic compatibility changed", cubic_rank, cubic_rows))
    require((quartic_rank, quartic_rows) == (4, QUARTIC_ROWS),
            ("raw quartic compatibility changed", quartic_rank, quartic_rows))
    require(tuple(cubics[row].coefficients for row in cubic_rows)
            == EXPECTED_CUBICS,
            "the six raw cubic forms changed")
    require(tuple(quartics[row].coefficients for row in quartic_rows)
            == EXPECTED_QUARTICS,
            "the four raw quartic forms changed")

    third = normal_correction(cubics, inverse)
    third_support = {
        cell: value.coefficients
        for cell, value in third.items() if value.coefficients
    }
    require(third_support == EXPECTED_THIRD_ORDER,
            ("canonical third-order correction changed", third_support))
    third_equations = tuple(
        left + right
        for left, right in zip(
            jacobian_apply(jacobian, third), cubics, strict=True
        )
    )
    require(all(not equation.coefficients for equation in third_equations),
            "a cubic term survived in the Jacobian cokernel")
    return direction, second, third, cubics, quartics


def variable(index):
    return Poly({(index,): Q(1)})


def exact_scaled_chart(packet, direction):
    one = Poly({(): Q(1)})
    y = tuple(variable(index) for index in range(15))
    factor6 = Poly({(): Q(7)}) + y[6]
    factor14 = Poly({(): Q(3)}) + y[14]
    denominator = factor6 * factor14
    linear = {
        cell: Poly({(): packet[cell]}) + direction[cell] for cell in CELLS
    }
    chart = dict(linear)
    chart[0, 1, 0, 0] = -(
        (one + Q(1, 2) * y[0])
        * (one + y[4])
        * (one + Q(1, 3) * y[14])
    )
    chart[0, 1, 0, 1] = -(
        y[5] * (one + Q(1, 2) * y[0])
        * (one + Q(1, 3) * y[14])
    )
    chart[0, 1, 1, 0] = -(
        Q(1, 2) * y[1] * (one + y[4])
        * (one + Q(1, 3) * y[14])
    )
    chart[0, 1, 1, 1] = -(
        Q(1, 2) * y[1] * y[5]
        * (one + Q(1, 3) * y[14])
    )
    scaled = {
        cell: denominator * value for cell, value in chart.items()
    }
    scaled[0, 2, 1, 1] = Q(35) * factor14
    scaled[2, 3, 0, 0] = Q(6) * factor6
    return scaled, denominator


def audit_exact_chart(packet, tangents, target, direction):
    scaled, denominator = exact_scaled_chart(packet, direction)
    outputs = tuple(map(as_poly, flatten_outputs(scaled, tangents)))
    expected = tuple(denominator * denominator * value for value in target)
    require(outputs == expected,
            "the rational 15-parameter chart left the four-slice fibre")
    return scaled, denominator


def evaluate_poly(polynomial, parameters):
    polynomial = as_poly(polynomial)
    total = Q(0)
    for monomial, coefficient in polynomial.coefficients.items():
        term = coefficient
        for variable_index in monomial:
            term *= Q(parameters[variable_index])
        total += term
    return total


def chart_member(packet, kernel, parameters):
    require(len(parameters) == 15, "chart parameter count changed")
    require(parameters[6] != -7 and parameters[14] != -3,
            "a chart denominator vanished")
    member = dict(packet)
    for variable_index in range(15):
        for column, cell in enumerate(CELLS):
            member[cell] += Q(parameters[variable_index]) * kernel[variable_index][column]
    y0, y1, y4, y5, y6, y14 = (
        Q(parameters[index]) for index in (0, 1, 4, 5, 6, 14)
    )
    member[0, 1, 0, 0] = -(1 + y0 / 2) * (1 + y4) * (1 + y14 / 3)
    member[0, 1, 0, 1] = -y5 * (1 + y0 / 2) * (1 + y14 / 3)
    member[0, 1, 1, 0] = -y1 / 2 * (1 + y4) * (1 + y14 / 3)
    member[0, 1, 1, 1] = -y1 * y5 / 2 * (1 + y14 / 3)
    member[0, 2, 1, 1] = Q(35, 7 + y6)
    member[2, 3, 0, 0] = Q(6, 3 + y14)
    return {
        cell: (value.numerator if value.denominator == 1 else value)
        for cell, value in member.items()
    }


CURVED_PARAMETERS = (
    -26, -26, 0, 0, 1, 0, 0, 0, 0, -26, 0, 0, 0, 0, 0,
)
EXPECTED_CURVE_DIRECTION = {
    (0, 1, 0, 0): 12,
    (0, 1, 1, 0): 13,
    (0, 3, 0, 0): -26,
    (0, 3, 1, 0): -26,
    (0, 5, 0, 0): -22,
    (1, 2, 0, 0): 1,
    (1, 5, 0, 0): -26,
}
EXPECTED_CURVE_QUADRATIC = {
    (0, 1, 0, 0): 13,
    (0, 1, 1, 0): 13,
}


def specialize_homogeneous(vector, parameters):
    result = {}
    for cell, polynomial in vector.items():
        value = evaluate_poly(polynomial, parameters)
        if value:
            result[cell] = (
                value.numerator if value.denominator == 1 else value
            )
    return result


def audit_curved_full_r2_member(
    packet, u_star, v_star, tangents, target, kernel, direction, second,
):
    first_specialized = specialize_homogeneous(direction, CURVED_PARAMETERS)
    second_specialized = specialize_homogeneous(second, CURVED_PARAMETERS)
    require(first_specialized == EXPECTED_CURVE_DIRECTION,
            ("curved calibration direction changed", first_specialized))
    require(second_specialized == EXPECTED_CURVE_QUADRATIC,
            ("curved calibration acceleration changed", second_specialized))
    curve = {
        cell: (
            Poly({(): packet[cell]})
            + Poly({(0,): first_specialized.get(cell, 0)})
            + Poly({(0, 0): second_specialized.get(cell, 0)})
        )
        for cell in CELLS
    }
    require(tuple(map(as_poly, flatten_outputs(curve, tangents))) == target,
            "the genuinely curved quadratic arc lost a four-slice row")
    member = chart_member(packet, kernel, CURVED_PARAMETERS)
    curve_at_one = {
        cell: evaluate_poly(value, (1,)) for cell, value in curve.items()
    }
    require(member == curve_at_one,
            "the curved chart member disagrees with its quadratic arc")
    derivative = CORE["differential_matrix"](member)
    mixed = [
        row for row, word in zip(derivative, WORDS, strict=True)
        if word not in ((0,) * 6, (1,) * 6)
    ]
    ranks = (
        BASE["ranks_over_fields"](derivative),
        BASE["ranks_over_fields"](mixed),
    )
    require(ranks == ((51,) * 4, (49,) * 4),
            ("curved calibration rank changed", ranks))
    selected = SIX["selected_family"](range(6))
    require(SIX["audit_selected_equations"](member, selected) == 60,
            "the curved calibration left the generic kernel")
    require(SIX["audit_literal_slices"](
        member, u_star, v_star, selected
    ) == 256, "the curved calibration lost a literal endpoint slice")
    witnesses = {
        root: SIX["audit_capable_root"](member, root) for root in range(6)
    }
    require(all(set(table) == {0, 1} for table in witnesses.values()),
            ("the curved calibration lost full R2", witnesses))
    radial_values = tuple(
        sum(
            coefficient
            * Q(CURVED_PARAMETERS[left])
            * Q(CURVED_PARAMETERS[right])
            for (left, right), coefficient in quadratic.items()
        )
        for quadratic in LOCAL["EXPECTED_QUADRICS"]
    )
    require(any(radial_values),
            "the curved calibration fell back into the exact-line cone")
    return ranks, witnesses, radial_values


def singular_matrix(name, matrix):
    entries = ",".join(
        polynomial_string(entry, variable="y")
        for row in matrix for entry in row
    )
    return f"matrix {name}[{len(matrix)}][{len(matrix[0])}]={entries};"


def homogeneous_string(coefficients):
    pieces = []
    for monomial, coefficient in sorted(coefficients.items()):
        variables = "*".join(f"y{index}" for index in monomial)
        pieces.append(f"{rational_string(coefficient)}*{variables}")
    return "+".join(pieces).replace("+-", "-") or "0"


def singular_script(cubics, quartics, scaled):
    derivative = CORE["differential_matrix"](scaled)
    mixed = [
        row for row, word in zip(derivative, WORDS, strict=True)
        if word not in ((0,) * 6, (1,) * 6)
    ]
    compatibility = tuple(
        polynomial.coefficients
        for polynomial in cubics + quartics
        if polynomial.coefficients
    )
    lines = [
        'ring compatibility=0,(y0,y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14),dp;',
        'LIB "primdec.lib";',
        'LIB "control.lib";',
        "ideal I=" + ",".join(map(homogeneous_string, compatibility)) + ";",
        "ideal R=radical(I);",
        "ideal P=y6,y14;",
        'if (size(reduce(std(R),std(P)))!=0) { print("FAIL_R_P"); exit; }',
        'if (size(reduce(std(P),std(R)))!=0) { print("FAIL_P_R"); exit; }',
        'ring chart=0,(y0,y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14),dp;',
        singular_matrix("D", derivative),
        singular_matrix("E", mixed),
        'module KD=syz(D);',
        'module KE=syz(E);',
        'if (ncols(KD)!=9) { print("FAIL_D_KGEN"); exit; }',
        'if (colrank(KD)!=9) { print("FAIL_D_KRANK"); exit; }',
        'if (ncols(KE)!=11) { print("FAIL_E_KGEN"); exit; }',
        'if (colrank(KE)!=11) { print("FAIL_E_KRANK"); exit; }',
        'print("CAS_OK");',
    ]
    return "\n".join(lines) + "\n"


EXPECTED_CAS_SHA256 = (
    "6d5e79c6389034376a07ba9e9411492d"
    "68f9780eb9f7224758fc024d6b41eb08"
)


def audit_exact_cas(cubics, quartics, scaled):
    executable = which("Singular")
    require(executable is not None,
            "Singular is required for the curved-chart audit")
    script = singular_script(cubics, quartics, scaled)
    digest = sha256(script.encode()).hexdigest()
    require(digest == EXPECTED_CAS_SHA256,
            ("the pinned curved-chart CAS input changed", digest))
    result = run(
        [executable, "-q"], input=script, text=True,
        capture_output=True, timeout=120, check=False,
    )
    require(result.returncode == 0,
            ("Singular curved-chart audit failed", result.stderr))
    require(result.stdout.strip() == "CAS_OK",
            ("Singular curved-chart certificate failed",
             result.stdout, result.stderr))
    return digest


def main():
    (
        packet, u_star, v_star, tangents, target,
        jacobian, kernel, inverse, _free_columns,
    ) = reconstruct_linear_data()
    direction, second, _third, cubics, quartics = (
        audit_second_through_fourth_order(
            packet, tangents, target, jacobian, kernel, inverse
        )
    )
    scaled, denominator = audit_exact_chart(
        packet, tangents, target, direction
    )
    digest = audit_exact_cas(cubics, quartics, scaled)
    ranks, witnesses, radial_values = audit_curved_full_r2_member(
        packet, u_star, v_star, tangents, target,
        kernel, direction, second,
    )
    print("six-rank-one curved four-slice chart: all checks passed")
    print("  implicit local chart        : 15 parameters, exact rational")
    print(f"  pivot determinant           : {PIVOT_DETERMINANT}")
    print(f"  chart denominator           : {polynomial_string(denominator, variable='y')}")
    print("  quadratic-arc compatibility : radical (y6,y14), dimension 13")
    print(f"  generic chart ranks         : {ranks[0][0]}/{ranks[1][0]}")
    print(f"  curved full-R2 parameters   : {CURVED_PARAMETERS}")
    print(f"  nonzero radial quadrics     : {radial_values}")
    print(f"  six-root witness tables     : {witnesses}")
    print(f"  Singular input SHA-256      : {digest}")


if __name__ == "__main__":
    main()
