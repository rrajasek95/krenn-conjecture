#!/usr/bin/env python3
"""Exact symbolic P5 degree-six compatibility and the H0 kill.

The 39 normal-eliminated mixed equations are expanded on the full
45-parameter Ferrers branch P5.  Three transverse Hensel corrections are
verified as polynomial identities.  The degree-six terminal pieces are then
restricted factor by factor, without constructing their large ambient
expansions.

On the chart b=z44+z45 != 0 the eleven transverse Jacobian pivots are the
diagonal matrix b*I.  Only two degree-six compatibility equations remain.
Their difference times an explicit linear factor is the eight-term H0 class,
so H0 is already killed by the new mixed initial equations.  The boundary
b=0 kills H0 directly.  Thus no P5 component can support this H0 escape.
"""

from collections import Counter
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
    "n8_p5_degree6_lifted_series",
    "verify_n8_lifted_cubic_spair_first_tails.py",
)
CUBIC = LIFTED.CUBIC
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "0029166951a75000c77856a54d0606c940d78af19c9f1466fbc40e9550aca1f0"
)

P5_NORMAL_VARIABLES = (12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23)
P5_NORMAL_SET = set(P5_NORMAL_VARIABLES)

# These rows, in the same order as P5_NORMAL_VARIABLES, give b times the
# identity.  H0 itself contains b, so this one chart covers every point at
# which H0 could be nonzero.
B_PIVOT_ROWS = (1, 4, 7, 16, 19, 28, 31, 34, 11, 22, 38)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(target, source, scale=QQ(1)):
    CUBIC.add_scaled(target, source, scale)


def multiply(left, right):
    return CUBIC.multiply_polynomials(left, right)


def polynomial(entries):
    answer = {}
    for monomial, coefficient in entries:
        monomial = tuple(sorted(monomial))
        answer[monomial] = answer.get(monomial, QQ(0)) + QQ(coefficient)
        if not answer[monomial]:
            answer.pop(monomial)
    return answer


def monomial(*variables, coefficient=QQ(1)):
    return {tuple(sorted(variables)): QQ(coefficient)}


def multiply_many(items):
    answer = {(): QQ(1)}
    for item in items:
        answer = multiply(answer, item)
    return answer


def derivative(source, variable):
    answer = {}
    for source_monomial, coefficient in source.items():
        multiplicity = source_monomial.count(variable)
        if not multiplicity:
            continue
        output = list(source_monomial)
        output.remove(variable)
        output = tuple(output)
        answer[output] = (
            answer.get(output, QQ(0)) + coefficient * multiplicity
        )
    return answer


def evaluate(source, point):
    answer = QQ(0)
    for source_monomial, coefficient in source.items():
        term = QQ(coefficient)
        for variable in source_monomial:
            term *= point[variable]
        answer += term
    return answer


def multiply_polynomial_series(left, right, maximum_order):
    answer = [{} for _order in range(maximum_order + 1)]
    for left_order, left_polynomial in enumerate(left):
        if not left_polynomial:
            continue
        for right_order, right_polynomial in enumerate(right):
            order = left_order + right_order
            if order > maximum_order:
                break
            if right_polynomial:
                add(
                    answer[order],
                    multiply(left_polynomial, right_polynomial),
                )
    return answer


def coefficient_on_p5_arc(source, corrections, requested_order):
    """Coefficient on P5 with the given transverse correction polynomials.

    All 45 P5 coordinates remain polynomial variables.  Free-coordinate
    corrections are fixed to zero.  Since orders one through three close as
    identities in those 45 variables, the first compatibility at order four
    is unchanged by subsequently allowing the free coordinates themselves
    to vary with the radial parameter.
    """

    answer = {}
    for source_monomial, coefficient in source.items():
        term = [{(): coefficient}] + [
            {} for _order in range(requested_order)
        ]
        for variable in source_monomial:
            variable_series = [
                {} for _order in range(requested_order + 1)
            ]
            if variable not in P5_NORMAL_SET:
                variable_series[0] = monomial(variable)
            elif variable == 15:
                variable_series[0] = monomial(16)
            for order in range(
                1, min(requested_order, len(corrections)) + 1
            ):
                variable_series[order] = corrections[order - 1].get(
                    variable, {}
                )
            term = multiply_polynomial_series(
                term, variable_series, requested_order
            )
        add(answer, term[requested_order])
    return answer


def p5_restriction(source):
    return coefficient_on_p5_arc(source, [], 0)


def transverse_jacobian(quadratic_parts):
    return [
        [
            p5_restriction(derivative(source, variable))
            for variable in P5_NORMAL_VARIABLES
        ]
        for source in quadratic_parts
    ]


def jacobian_times(jacobian, correction):
    answer = []
    for row in jacobian:
        value = {}
        for column, variable in enumerate(P5_NORMAL_VARIABLES):
            if row[column] and correction.get(variable):
                add(value, multiply(row[column], correction[variable]))
        answer.append(value)
    return answer


def strict_residual(parts, corrections, strict_order, terminal_part=None):
    answer = []
    for equation in range(39):
        value = {}
        for degree in range(2, min(5, strict_order + 2) + 1):
            arc_order = strict_order - degree + 2
            add(
                value,
                coefficient_on_p5_arc(
                    parts[degree][equation], corrections, arc_order
                ),
            )
        if terminal_part is not None:
            add(value, terminal_part[equation])
        answer.append(value)
    return answer


def expected_corrections():
    n1 = {
        12: monomial(9, 16),
        13: monomial(9, 16),
        15: polynomial((((16, 36), 1), ((16, 37), -1))),
        17: monomial(16, 38),
        18: monomial(11, 16),
        19: monomial(11, 16),
    }
    n2 = {
        12: polynomial((
            ((9, 10, 16), -1), ((9, 16, 36), 1),
            ((9, 16, 37), -1),
        )),
        13: monomial(9, 10, 16, coefficient=-1),
        14: monomial(9, 16, 38),
        15: polynomial((((16, 36, 37), -1), ((16, 37, 37), 1))),
        17: monomial(16, 37, 38, coefficient=-1),
        18: polynomial((
            ((10, 11, 16), -1), ((11, 16, 36), 1),
            ((11, 16, 37), -1),
        )),
        19: monomial(10, 11, 16, coefficient=-1),
        20: monomial(11, 16, 38),
    }
    n3 = {
        12: polynomial((
            ((9, 10, 10, 16), 1), ((9, 10, 16, 36), -1),
            ((9, 10, 16, 37), 1), ((9, 16, 36, 37), -1),
            ((9, 16, 37, 37), 1),
        )),
        13: monomial(9, 10, 10, 16),
        14: polynomial((
            ((9, 10, 16, 38), -1), ((9, 16, 37, 38), -1),
        )),
        15: polynomial((
            ((16, 36, 37, 37), 1), ((16, 37, 37, 37), -1),
        )),
        17: monomial(16, 37, 37, 38),
        18: polynomial((
            ((10, 10, 11, 16), 1), ((10, 11, 16, 36), -1),
            ((10, 11, 16, 37), 1), ((11, 16, 36, 37), -1),
            ((11, 16, 37, 37), 1),
        )),
        19: monomial(10, 10, 11, 16),
        20: polynomial((
            ((10, 11, 16, 38), -1), ((11, 16, 37, 38), -1),
        )),
    }
    return [n1, n2, n3]


def terminal_degree_six_on_p5(series):
    """Restrict Q^(6) correction by correction before multiplication."""

    functional_cache = {}
    answers = []
    totals = Counter()
    maximum_output_terms = 0
    maximum_product_terms = 0

    def restrict_ambient(source):
        return p5_restriction(series.reducer.tangent_restriction(source))

    for number in range(1, 40):
        state = series._state(number)
        require(
            state["maximum_degree"] == 5,
            f"Q{number}: degree-six stream lacks the degree-five prefix",
        )
        answer = {}
        local = Counter()
        for multiplier, functional in state["corrections"]:
            multiplier_degree = len(next(iter(multiplier)))
            equation_degree = 6 - multiplier_degree
            if not 0 <= equation_degree <= 4:
                continue
            local["candidate_factors"] += 1
            restricted_multiplier = restrict_ambient(multiplier)
            if not restricted_multiplier:
                local["zero_multipliers"] += 1
                continue
            key = tuple(sorted(functional.items())), equation_degree
            if key not in functional_cache:
                functional_cache[key] = restrict_ambient(
                    series.reducer.functional_hasse(
                        functional, equation_degree
                    )
                )
            restricted_equation = functional_cache[key]
            if not restricted_equation:
                local["zero_equations"] += 1
                continue
            product = multiply(restricted_multiplier, restricted_equation)
            add(answer, product, -1)
            local["nonzero_products"] += 1
            local["product_terms"] += len(product)
            maximum_product_terms = max(maximum_product_terms, len(product))
        answers.append(answer)
        maximum_output_terms = max(maximum_output_terms, len(answer))
        totals.update(local)

    return answers, {
        **dict(totals),
        "functional_restriction_cache_entries": len(functional_cache),
        "total_output_terms": sum(map(len, answers)),
        "maximum_output_terms": maximum_output_terms,
        "maximum_product_terms": maximum_product_terms,
    }


def encode_polynomial(source):
    return [
        {
            "monomial": list(source_monomial),
            "numerator": coefficient.numerator,
            "denominator": coefficient.denominator,
        }
        for source_monomial, coefficient in sorted(source.items())
    ]


def audit():
    series = LIFTED.NormalObstructionSeries()
    parts = {degree: [] for degree in range(2, 6)}
    for number in range(1, 40):
        for degree in range(2, 6):
            parts[degree].append(series.part(number, degree))

    require(56 - len(P5_NORMAL_VARIABLES) == 45, "P5 dimension changed")
    require(
        all(not p5_restriction(source) for source in parts[2]),
        "a quadratic obstruction no longer vanishes identically on P5",
    )

    jacobian = transverse_jacobian(parts[2])
    b = polynomial((((44,), 1), ((45,), 1)))
    for column, row_index in enumerate(B_PIVOT_ROWS):
        expected = [dict() for _column in P5_NORMAL_VARIABLES]
        expected[column] = b
        require(
            jacobian[row_index] == expected,
            f"b-chart pivot row {row_index + 1} changed",
        )

    corrections = expected_corrections()
    residual_term_counts = []
    for strict_order in range(1, 4):
        residual = strict_residual(
            parts, corrections[:strict_order - 1], strict_order
        )
        image = jacobian_times(jacobian, corrections[strict_order - 1])
        for equation in range(39):
            add(residual[equation], image[equation])
        require(
            not any(residual),
            f"symbolic P5 bend failed at strict order {strict_order}",
        )
        # Count the incoming residual before its exact Jacobian cancellation.
        incoming = strict_residual(
            parts, corrections[:strict_order - 1], strict_order
        )
        residual_term_counts.append(sum(map(len, incoming)))

    degree_six, stream_ledger = terminal_degree_six_on_p5(series)
    require(
        stream_ledger["total_output_terms"] == 6090,
        "degree-six P5 stream term count changed",
    )
    require(
        stream_ledger["maximum_output_terms"] == 499,
        "degree-six P5 maximum output changed",
    )

    residual4 = strict_residual(parts, corrections, 4, degree_six)
    require(sum(map(len, residual4)) == 176,
            "degree-six strict residual term count changed")

    # Solve the b-diagonal pivot equations without fractions.  If p_j is the
    # pivot residual for normal variable j, then
    # b*r_i - sum_j J_ij*p_j is the compatibility numerator on b != 0.
    pivot_residuals = [residual4[row] for row in B_PIVOT_ROWS]
    compatibility_numerators = []
    for equation, row in enumerate(jacobian):
        value = multiply(b, residual4[equation])
        for column in range(11):
            if row[column] and pivot_residuals[column]:
                add(
                    value,
                    multiply(row[column], pivot_residuals[column]),
                    -1,
                )
        compatibility_numerators.append(value)

    h0_core = multiply_many((
        monomial(16, 16, 41),
        polynomial((((9, 25), 1), ((11, 46), -1))),
    ))
    u = polynomial((((26,), 1), ((45,), 1)))
    v = polynomial((((26,), 1), ((44,), -1)))
    g30 = multiply_many((h0_core, u))
    g30 = {source_monomial: -coefficient / 2
           for source_monomial, coefficient in g30.items()}
    g33 = multiply_many((h0_core, v))
    g33 = {source_monomial: -coefficient / 2
           for source_monomial, coefficient in g33.items()}

    expected_numerators = [{} for _equation in range(39)]
    expected_numerators[29] = multiply(b, g30)
    expected_numerators[32] = multiply(b, g33)
    require(
        compatibility_numerators == expected_numerators,
        "degree-six P5 compatibility factorization changed",
    )

    b_from_compatibility = dict(u)
    add(b_from_compatibility, v, -1)
    require(b_from_compatibility == b, "u-v no longer equals b")

    final_factor = polynomial((((53,), 1), ((51,), -1)))
    h0 = multiply_many((h0_core, b, final_factor))
    compatibility_difference = dict(g30)
    add(compatibility_difference, g33, -1)
    h0_reconstruction = multiply(final_factor, compatibility_difference)
    h0_reconstruction = {
        source_monomial: -2 * coefficient
        for source_monomial, coefficient in h0_reconstruction.items()
    }
    require(
        h0_reconstruction == h0,
        "H0 is no longer reconstructed by the compatibility difference",
    )
    require(len(h0) == 8, "H0 class lost its eight-term expansion")

    deterministic_point = {index: QQ(index + 2) for index in range(56)}
    for variable in (12, 13, 14, 17, 18, 19, 20, 21, 22, 23):
        deterministic_point[variable] = QQ(0)
    deterministic_point[15] = deterministic_point[16]
    deterministic_compatibility = [
        evaluate(g30, deterministic_point),
        evaluate(g33, deterministic_point),
    ]
    require(
        deterministic_compatibility == [QQ(170841150), QQ(-41001876)],
        "symbolic compatibility disagrees with the prior rational P5 point",
    )

    active_compatibility_variables = sorted({
        variable
        for source in (g30, g33)
        for source_monomial in source
        for variable in source_monomial
    })
    ledger = {
        "p5_free_parameters_retained": 45,
        "mixed_equations": 39,
        "transverse_variables": 11,
        "b_chart_pivot_rows_one_based": [
            row + 1 for row in B_PIVOT_ROWS
        ],
        "b_chart_determinant": "(z44+z45)^11",
        "h0_nonzero_implies_b_chart": True,
        "symbolic_bend_nonzero_entries": [
            len(correction) for correction in corrections
        ],
        "strict_orders_one_to_three_incoming_terms": residual_term_counts,
        "closed_through_original_mixed_degree": 5,
        "degree_six_stream": stream_ledger,
        "degree_six_strict_residual_terms": sum(map(len, residual4)),
        "degree_six_compatibility_equations_one_based": [30, 33],
        "active_compatibility_variables": active_compatibility_variables,
        "normalized_compatibility": {
            "g30": "-1/2*z16^2*z41*(z9*z25-z11*z46)*(z26+z45)",
            "g33": "-1/2*z16^2*z41*(z9*z25-z11*z46)*(z26-z44)",
        },
        "normalized_compatibility_polynomials": {
            "g30": encode_polynomial(g30),
            "g33": encode_polynomial(g33),
        },
        "prior_point_compatibility_values": [
            value.numerator for value in deterministic_compatibility
        ],
        "chart_saturation": (
            "<g30,g33>:(z44+z45)^infinity "
            "=<z16^2*z41*(z9*z25-z11*z46)>"
        ),
        "reduced_chart_components": [
            "z16=0", "z41=0", "z9*z25-z11*z46=0",
        ],
        "boundary_component": "z44+z45=0",
        "h0_membership_identity": (
            "H0=-2*(z53-z51)*(g30-g33)"
        ),
        "h0_terms": len(h0),
        "all_compatible_p5_components_force_h0_zero": True,
        "scope_guard": (
            "kills the unique degree-seven H0 standard-monomial class on "
            "P5; this is a filtered initial-ideal result, not an all-orders "
            "standard-basis or global conjecture proof"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(digest == EXPECTED_LEDGER_SHA256,
            "P5 degree-six compatibility ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
