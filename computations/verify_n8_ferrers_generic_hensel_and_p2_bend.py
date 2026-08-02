#!/usr/bin/env python3
"""Certify candidate Hensel pivots on all five n=8 Ferrers branches.

At deterministic rational points of the five linear minimal primes, the
Jacobian of the 39 tangent quadrics has rank equal to the prime codimension.
This proves that the scheme cut out by the known tangent equations is
generically smooth along every reduced component and supplies candidate
strict-transform normal variables.  It does not prove that unknown higher
initial equations fail to cut those components.

The checker also carries out the first nontrivial bend on branch P2.  The
cubic mixed deformation is an exact Jacobian coboundary modulo P2, and after
using the resulting quadratic coordinate correction the local H1 class
still vanishes through degree four.
"""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LIFTED = load_module(
    "n8_lifted_cubic_spairs",
    "verify_n8_lifted_cubic_spair_first_tails.py",
)
AMBIENT = load_module(
    "n8_ambient_local_standard_basis",
    "analyze_n8_ambient_local_standard_basis.py",
)

CUBIC = LIFTED.CUBIC
LOCAL = LIFTED.LOCAL
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "b34d65974c400bb22de21a1e543ca741c2a1925be29e29e0236fe65a0db8dd67"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def derivative(polynomial, variable):
    answer = {}
    for monomial, coefficient in polynomial.items():
        multiplicity = monomial.count(variable)
        if not multiplicity:
            continue
        output = list(monomial)
        output.remove(variable)
        output = tuple(output)
        answer[output] = (
            answer.get(output, QQ(0)) + multiplicity * coefficient
        )
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


def gradient_value(polynomial, variable, point):
    answer = QQ(0)
    for monomial, coefficient in polynomial.items():
        multiplicity = monomial.count(variable)
        if not multiplicity:
            continue
        residual = list(monomial)
        residual.remove(variable)
        value = QQ(coefficient * multiplicity)
        for index in residual:
            value *= point[index]
        answer += value
    return answer


def substitute_linear(polynomial, substitutions):
    answer = {}
    for monomial, coefficient in polynomial.items():
        term = {(): coefficient}
        for variable in monomial:
            term = CUBIC.multiply_polynomials(
                term,
                substitutions.get(variable, {(variable,): QQ(1)}),
            )
        CUBIC.add_scaled(answer, term)
    return answer


def audit():
    series = LIFTED.NormalObstructionSeries()
    quadratic_rows = [value[0] for _pivot, value in series.items]

    # Each tuple gives pivot normal variables and the exact linear-prime
    # substitutions.  Unspecified tangent variables receive generic values.
    branches = {
        "P1": {
            "normal_variables": [25, 26, 27, 44, 46],
            "substitutions": {
                25: {}, 26: {(45,): QQ(1)}, 27: {},
                44: {(45,): QQ(-1)}, 46: {},
            },
        },
        "P2": {
            "normal_variables": [12, 13, 15, 18, 19, 25, 26, 44, 46],
            "substitutions": {
                12: {}, 13: {}, 15: {(16,): QQ(1)}, 18: {}, 19: {},
                25: {}, 26: {(45,): QQ(1)},
                44: {(45,): QQ(-1)}, 46: {},
            },
        },
        "P3": {
            "normal_variables": [12, 13, 14, 15, 17, 18, 19, 20, 44, 46],
            "substitutions": {
                12: {}, 13: {}, 14: {}, 15: {(16,): QQ(1)},
                17: {}, 18: {}, 19: {}, 20: {},
                44: {(45,): QQ(-1)}, 46: {},
            },
        },
        "P4": {
            "normal_variables": [12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 44],
            "substitutions": {
                12: {}, 13: {}, 14: {}, 15: {(16,): QQ(1)},
                17: {}, 18: {}, 19: {}, 20: {}, 21: {}, 22: {},
                44: {(45,): QQ(-1)},
            },
        },
        "P5": {
            "normal_variables": [12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23],
            "substitutions": {
                12: {}, 13: {}, 14: {}, 15: {(16,): QQ(1)},
                17: {}, 18: {}, 19: {}, 20: {}, 21: {}, 22: {}, 23: {},
            },
        },
    }

    branch_ranks = {}
    for name, branch in branches.items():
        point = {index: QQ(index + 2) for index in range(56)}
        for variable, image in branch["substitutions"].items():
            point[variable] = sum(
                coefficient * point[monomial[0]]
                for monomial, coefficient in image.items()
            )
        matrix = [
            [gradient_value(row, variable, point)
             for variable in branch["normal_variables"]]
            for row in quadratic_rows
        ]
        rank = exact_rank(matrix)
        require(rank == len(branch["normal_variables"]),
                f"generic tangent rank failed on {name}: {rank}")
        branch_ranks[name] = rank

    # Compute the cubic normal-eliminated deformation once, retaining literal
    # provenance in the NormalObstructionSeries state.
    for number in range(1, 40):
        series.part(number, 3)

    # Normal-eliminate H1 without using the 39 obstruction equations.  This
    # is its class after the 196 smooth ambient normal variables are removed.
    reducer = series.reducer
    reducer.add_correction(
        {(): QQ(1)},
        {LOCAL.THIRD.MIXED_WORD_INDEX[LOCAL.SECOND.MIXED_WORD_1]: QQ(1)},
        "selected_mixed_H1",
    )
    h1_parts = {}
    for degree in range(1, 5):
        incoming = reducer.residual(LOCAL.SECOND.PURE_WORD_1, degree)
        remainder, _factor_count, _term_count, _steps = reducer.normal_reduce(
            incoming, degree, "P2_H1_normal_only"
        )
        h1_parts[degree] = reducer.tangent_polynomial(remainder)
    require([len(h1_parts[d]) for d in range(1, 5)] == [0, 0, 4, 24],
            "H1 normal-only leading ledger changed")
    p2_substitutions = branches["P2"]["substitutions"]
    require(not substitute_linear(h1_parts[3], p2_substitutions),
            "H1 cubic does not vanish on straight P2")
    require(not substitute_linear(h1_parts[4], p2_substitutions),
            "H1 quartic does not vanish on straight P2")

    names = [f"z{index}" for index in range(56)]

    def polynomial_string(polynomial):
        return AMBIENT.singular_polynomial(polynomial, names)

    def vector_string(entries):
        terms = [
            f"({polynomial_string(polynomial)})*gen({component + 1})"
            for component, polynomial in entries if polynomial
        ]
        return "+".join(terms) or "0"

    jacobian_columns = []
    for variable in range(56):
        column = vector_string([
            (component, derivative(row, variable))
            for component, row in enumerate(quadratic_rows)
        ])
        if column != "0":
            jacobian_columns.append((variable, column))
    require(len(jacobian_columns) == 18,
            "active tangent-Jacobian variable count changed")

    p2_generators = [
        "z46", "z44+z45", "z26-z45", "z25",
        "z12", "z13", "z15-z16", "z18", "z19",
    ]
    module_generators = [column for _variable, column in jacobian_columns]
    for component in range(39):
        for generator in p2_generators:
            module_generators.append(
                f"({generator})*gen({component + 1})"
            )
    target = vector_string([
        (component, series.part(component + 1, 3))
        for component in range(39)
    ])
    correction_lines = []
    for row_index, (variable, _column) in enumerate(jacobian_columns, 1):
        h1_derivative = derivative(h1_parts[3], variable)
        if h1_derivative:
            correction_lines.append(
                "corrected=corrected-"
                f"({polynomial_string(h1_derivative)})*Lift[{row_index},1];"
            )

    singular = f"""
ring r=0,({','.join(names)}),dp;
module M={','.join(module_generators)};
module G=std(M);
vector target={target};
vector tangentRemainder=reduce(target,G);
matrix Lift=lift(M,target);
module reconstruction=matrix(M)*Lift;
ideal P2={','.join(p2_generators)}; P2=std(P2);
poly corrected={polynomial_string(h1_parts[4])};
{chr(10).join(correction_lines)}
poly pureRemainder=reduce(corrected,P2);
"RESULT",(tangentRemainder==0),(reconstruction[1]==target),
 (pureRemainder==0),size(M),size(G),size(Lift),size(pureRemainder);
quit;
"""
    output, returncode, peak_kib, stop_reason, writer_errors = (
        AMBIENT.bounded_singular(singular, 60, 700)
    )
    require(stop_reason is None,
            f"P2 bend audit stopped: {stop_reason}, peak={peak_kib} KiB")
    require(returncode == 0 and not writer_errors,
            f"P2 Singular failure: {returncode}, {writer_errors}, {output[-1000:]}")
    match = re.search(
        r"RESULT\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)",
        output,
    )
    require(match is not None, f"could not parse P2 bend audit: {output[-2000:]}")
    values = tuple(map(int, match.groups()))
    require(values == (1, 1, 1, 369, 360, 369, 0),
            f"P2 bend ledger changed: {values}")

    return {
        "tangent_branch_count": len(branches),
        "branch_codimensions": branch_ranks,
        "generic_jacobian_ranks": branch_ranks,
        "known_tangent_scheme_generically_smooth_on_all_branches": True,
        "ambient_normal_rank": 196,
        "p2_cubic_deformation_terms": sum(
            len(series.part(number, 3)) for number in range(1, 40)
        ),
        "p2_trivialization_module_generators": values[3],
        "p2_trivialization_standard_basis_size": values[4],
        "p2_lift_reconstruction": bool(values[1]),
        "h1_normal_only_term_counts_degrees_1_to_4": [
            len(h1_parts[degree]) for degree in range(1, 5)
        ],
        "h1_zero_on_bent_p2_through_degree": 4,
        "scope_guard": (
            "candidate generic Hensel pivots on all five branches and first "
            "P2 bend; localized Rees flatness and all-orders pure vanishing "
            "remain open"
        ),
    }


def main():
    ledger = audit()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen Ferrers branch-Hensel ledger changed")
    print(
        "n=8 Ferrers branches: PASS; candidate ranks 5,9,10,11,11; "
        "P2 cubic bend exists and H1 remains zero through degree 4"
    )
    print(json.dumps(ledger, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
