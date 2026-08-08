#!/usr/bin/env python3
"""Exact P5 strict-transform prefix for the n=8 mixed equations.

The 39 normal-eliminated mixed equations start in tangent degree two.  This
checker fixes a deterministic rational point on Ferrers branch P5 and solves
the strict-transform equations recursively in the eleven transverse P5
coordinates.  Degrees two through five are retained as exact tangent
polynomials.  At degree six only the value at the base point is needed; it is
evaluated directly from the factorized ambient corrections, avoiding the
large degree-six polynomial expansion.

The canonical section with all 45 free-coordinate bends fixed to zero closes
through strict-transform order three, i.e. through original mixed degree
five.  At order four an exact compatibility remains after solving the eleven
normal equations.  This is a finite-jet statement, not proof that every P5
arc fails: the next calculation must allow free-coordinate bends and compute
the resulting symbolic degree-six compatibility ideal.
"""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LIFTED = load_module(
    "n8_p5_lifted_series",
    "verify_n8_lifted_cubic_spair_first_tails.py",
)
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "afd0341d0704ddcd45c578859851b415c147660e7dc7a31cdce9a8fa3f40c99c"
)

P5_NORMAL_VARIABLES = (12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def evaluate(polynomial, point):
    answer = QQ(0)
    for monomial, coefficient in polynomial.items():
        term = QQ(coefficient)
        for variable in monomial:
            term *= point[variable]
        answer += term
    return answer


def gradient_value(polynomial, variable, point):
    answer = QQ(0)
    for monomial, coefficient in polynomial.items():
        multiplicity = monomial.count(variable)
        if not multiplicity:
            continue
        residual = list(monomial)
        residual.remove(variable)
        term = QQ(coefficient * multiplicity)
        for index in residual:
            term *= point[index]
        answer += term
    return answer


def exact_rank(matrix):
    pivots = {}
    for source in matrix:
        row = {index: QQ(value) for index, value in enumerate(source) if value}
        while row:
            pivot = min(row)
            value = row[pivot]
            if pivot not in pivots:
                pivots[pivot] = {
                    index: coefficient / value
                    for index, coefficient in row.items()
                }
                break
            basis = pivots[pivot]
            for index, coefficient in basis.items():
                output = row.get(index, QQ(0)) - value * coefficient
                if output:
                    row[index] = output
                else:
                    row.pop(index, None)
    return len(pivots)


def independent_rows(matrix, count):
    chosen = []
    rank = 0
    for index, row in enumerate(matrix):
        new_rank = exact_rank([matrix[item] for item in chosen] + [row])
        if new_rank > rank:
            chosen.append(index)
            rank = new_rank
            if rank == count:
                return chosen
    raise RuntimeError(f"only {rank} independent P5 Jacobian rows")


def solve_square(matrix, target):
    size = len(matrix)
    rows = [
        [QQ(value) for value in source] + [QQ(target[index])]
        for index, source in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if rows[row][column]),
            None,
        )
        require(pivot is not None, f"singular solve at column {column}")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        scale = rows[column][column]
        rows[column] = [value / scale for value in rows[column]]
        for row in range(size):
            if row == column or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [
                rows[row][entry] - scale * rows[column][entry]
                for entry in range(size + 1)
            ]
    return [rows[index][-1] for index in range(size)]


def multiply_scalar_series(left, right, maximum_order):
    answer = [QQ(0)] * (maximum_order + 1)
    for left_order, left_value in enumerate(left):
        if not left_value:
            continue
        for right_order, right_value in enumerate(right):
            order = left_order + right_order
            if order > maximum_order:
                break
            answer[order] += left_value * right_value
    return answer


def coefficient_on_arc(polynomial, vectors, order):
    """Coefficient of s^order in P(v0+s*v1+...) over QQ."""

    answer = QQ(0)
    for monomial, coefficient in polynomial.items():
        term = [QQ(coefficient)] + [QQ(0)] * order
        for variable in monomial:
            variable_series = [
                vector.get(variable, QQ(0)) for vector in vectors[:order + 1]
            ]
            variable_series += [QQ(0)] * (
                order + 1 - len(variable_series)
            )
            term = multiply_scalar_series(term, variable_series, order)
        answer += term[order]
    return answer


def ambient_tangent_point(series, tangent_point):
    point = {
        coordinate: QQ(0)
        for coordinate in range(len(LIFTED.LOCAL.FACTOR.AMBIENT_COORDINATES))
    }
    for parameter, vector in enumerate(series.reducer.data["tangent_basis"]):
        for coordinate, coefficient in vector.items():
            point[coordinate] += coefficient * tangent_point[parameter]
    return point


def terminal_part_value(series, number, degree, ambient_point):
    """Evaluate the next normal remainder without constructing it.

    Linear normal forms vanish on an ambient tangent vector.  Therefore the
    value of the unreduced residual there equals the value of its tangent
    remainder.  Each correction remains factorized for this evaluation.
    """

    state = series._state(number)
    require(
        state["maximum_degree"] == degree - 1,
        f"Q{number}: terminal evaluation needs prefix through {degree - 1}",
    )
    answer = (
        evaluate(
            series.reducer.functional_hasse(state["functional"], degree),
            ambient_point,
        )
        if degree <= 4 else QQ(0)
    )
    for multiplier, jacobian_functional in state["corrections"]:
        multiplier_degree = len(next(iter(multiplier)))
        equation_degree = degree - multiplier_degree
        if not 0 <= equation_degree <= 4:
            continue
        answer -= evaluate(multiplier, ambient_point) * evaluate(
            series.reducer.functional_hasse(
                jacobian_functional, equation_degree
            ),
            ambient_point,
        )
    return answer


def encoded_fraction(value):
    return [value.numerator, value.denominator]


def audit():
    series = LIFTED.NormalObstructionSeries()
    parts = {degree: [] for degree in range(2, 6)}
    for number in range(1, 40):
        for degree in range(2, 6):
            parts[degree].append(series.part(number, degree))

    # Generic deterministic point subject to P5:
    # z12=z13=z14=z17=...=z23=0 and z15=z16.
    tangent_point = {index: QQ(index + 2) for index in range(56)}
    for variable in (12, 13, 14, 17, 18, 19, 20, 21, 22, 23):
        tangent_point[variable] = QQ(0)
    tangent_point[15] = tangent_point[16]

    require(
        all(evaluate(polynomial, tangent_point) == 0 for polynomial in parts[2]),
        "deterministic point left the P5 tangent cone",
    )

    jacobian = [
        [
            gradient_value(polynomial, variable, tangent_point)
            for variable in P5_NORMAL_VARIABLES
        ]
        for polynomial in parts[2]
    ]
    require(exact_rank(jacobian) == 11, "P5 normal Jacobian rank changed")
    pivot_rows = independent_rows(jacobian, 11)
    pivot_matrix = [jacobian[row] for row in pivot_rows]

    ambient_point = ambient_tangent_point(series, tangent_point)
    degree_six_values = [
        terminal_part_value(series, number, 6, ambient_point)
        for number in range(1, 40)
    ]

    # v(s)=v0+s*v1+... .  In t^2 F(v,t), strict order r receives
    # the coefficient of s^(r-d+2) from homogeneous tangent part Q^(d).
    vectors = [dict(tangent_point)]
    correction_ledger = []
    terminal_compatibility = None
    for strict_order in range(1, 5):
        vectors.append({})
        residual = []
        for equation in range(39):
            value = QQ(0)
            for degree in range(2, min(5, strict_order + 2) + 1):
                arc_order = strict_order - degree + 2
                value += coefficient_on_arc(
                    parts[degree][equation], vectors, arc_order
                )
            if strict_order == 4:
                value += degree_six_values[equation]
            residual.append(value)

        solution = solve_square(
            pivot_matrix,
            [-residual[row] for row in pivot_rows],
        )
        vectors[strict_order] = {
            variable: solution[index]
            for index, variable in enumerate(P5_NORMAL_VARIABLES)
            if solution[index]
        }

        full_coefficients = []
        for equation in range(39):
            value = QQ(0)
            for degree in range(2, min(5, strict_order + 2) + 1):
                arc_order = strict_order - degree + 2
                value += coefficient_on_arc(
                    parts[degree][equation], vectors, arc_order
                )
            if strict_order == 4:
                value += degree_six_values[equation]
            full_coefficients.append(value)
        if any(full_coefficients):
            require(
                strict_order == 4,
                f"P5 compatibility failed early at strict order {strict_order}",
            )
            terminal_compatibility = full_coefficients
        correction_ledger.append({
            "strict_order": strict_order,
            "nonzero_normal_corrections": len(vectors[strict_order]),
            "normal_correction": [
                encoded_fraction(vectors[strict_order].get(variable, QQ(0)))
                for variable in P5_NORMAL_VARIABLES
            ],
        })

    require(terminal_compatibility is not None,
            "canonical P5 section unexpectedly closed through degree six")

    # The eight-term H0 class found at degree seven has this factorization.
    # Its leading coefficient on every arc above v0 is its value at v0.
    h0_factors = (
        tangent_point[16] ** 2,
        tangent_point[41],
        tangent_point[44] + tangent_point[45],
        tangent_point[53] - tangent_point[51],
        tangent_point[9] * tangent_point[25]
        - tangent_point[11] * tangent_point[46],
    )
    h0_initial_value = QQ(1)
    for factor in h0_factors:
        h0_initial_value *= factor
    require(
        h0_initial_value,
        "chosen P5 point lies on the H0 degree-seven divisor",
    )

    ledger = {
        "branch": "P5",
        "base_point_rule": "z_i=i+2, with z12=z13=z14=z17..z23=0 and z15=z16",
        "mixed_equations": 39,
        "p5_codimension": 11,
        "pivot_equations_one_based": [row + 1 for row in pivot_rows],
        "retained_tangent_part_terms": {
            str(degree): sum(len(polynomial) for polynomial in parts[degree])
            for degree in range(2, 6)
        },
        "streamed_degree_six_nonzero_values": sum(
            value != 0 for value in degree_six_values
        ),
        "strict_transform_orders_closed": 3,
        "original_mixed_degree_closed": 5,
        "canonical_section_first_failed_strict_order": 4,
        "canonical_section_first_failed_original_degree": 6,
        "degree_six_compatibility_nonzero_equations": [
            index + 1 for index, value in enumerate(terminal_compatibility)
            if value
        ],
        "degree_six_compatibility_values": [
            encoded_fraction(value) for value in terminal_compatibility
        ],
        "corrections": correction_ledger,
        "h0_degree_seven_initial_value": encoded_fraction(h0_initial_value),
        "next_missing_calculation": (
            "the symbolic degree-six compatibility ideal on P5, allowing "
            "free-coordinate bends; on its zero locus, degree-six normal "
            "quotients and directional contractions are then needed for "
            "the degree-seven mixed values"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(digest == EXPECTED_LEDGER_SHA256, "P5 prefix ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
