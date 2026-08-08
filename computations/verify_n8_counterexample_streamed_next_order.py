#!/usr/bin/env python3
"""Exact memory-bounded next orders at the exceptional n=8 mixed torus.

The existing automatic reducer closes H0 through translated degree six and
H1 through degree five, but forming the next ambient residual for H1 exceeded
the exploratory memory budget.  This checker first validates that restriction
to the 56-variable mixed tangent can be pushed through every factorized
correction.  It then computes the two next orders without materializing their
ambient expansions.

The H1 degree-six tangent residual reduces completely through the 39 literal
quadratic-obstruction leads, proving H1 in I_mix + m_p^7.  At H0 degree seven
the same reduction leaves an exact eight-term standard-monomial class.  The
class has a five-factor form, vanishes on Ferrers branches P1--P4, and survives
on P5.  This locates the first unresolved pure escape; it does not prove that
P5 lifts to an all-pure component.
"""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ANALYZER_PATH = HERE / "analyze_n8_counterexample_local_standard_basis.py"
SPEC = importlib.util.spec_from_file_location(
    "n8_local_standard_basis_streamed", ANALYZER_PATH
)
ANALYZER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ANALYZER)

CUBIC = ANALYZER.CUBIC
FACTOR = ANALYZER.FACTOR
FOURTH = ANALYZER.FOURTH
SECOND = ANALYZER.SECOND
THIRD = ANALYZER.THIRD
SOURCE = ANALYZER.SOURCE
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "2d544163df5df35874d073e776d25820bd5b871b9e8f5f5353cc350cb3f6142d"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def selected_words(colour):
    if colour == 0:
        return SECOND.PURE_WORD_0, SECOND.MIXED_WORD_0
    return SECOND.PURE_WORD_1, SECOND.MIXED_WORD_1


def initialized_reducer(colour):
    reducer = ANALYZER.LocalReducer()
    pure, selected = selected_words(colour)
    reducer.add_correction(
        {(): QQ(1)},
        {THIRD.MIXED_WORD_INDEX[selected]: QQ(1)},
        "selected_mixed_coefficient",
    )
    return reducer, pure


def validate_streamed_projection(colour, maximum_degree):
    """Compare streamed and materialized tangent normal forms exactly."""

    reducer, pure = initialized_reducer(colour)
    records = []
    for degree in range(1, maximum_degree + 1):
        streamed, stream_record = reducer.streamed_tangent_residual(
            pure, degree
        )
        ambient = reducer.residual(pure, degree)
        _quotients, ambient_remainder, _steps = (
            SOURCE.fast_divide_by_echelon_linear_forms(
                ambient, reducer.jacobian_pivots
            )
        )
        materialized = reducer.tangent_polynomial(ambient_remainder)
        require(
            streamed == materialized,
            f"H{colour} degree {degree}: streamed projection mismatch",
        )
        record = reducer.reduce_degree(pure, degree)
        require(record["complete"],
                f"H{colour} degree {degree}: prior closure changed")
        require(record["tangent_terms"] == len(streamed),
                f"H{colour} degree {degree}: tangent count mismatch")
        records.append({
            "degree": degree,
            "ambient_terms": len(ambient),
            "tangent_terms": len(streamed),
            "stream_contributing_corrections": (
                stream_record["contributing_corrections"]
            ),
        })
    return reducer, pure, records


def multiply_many(polynomials):
    answer = {(): QQ(1)}
    for polynomial in polynomials:
        answer = CUBIC.multiply_polynomials(answer, polynomial)
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


def encode_polynomial(polynomial):
    return [
        {
            "monomial": list(monomial),
            "numerator": coefficient.numerator,
            "denominator": coefficient.denominator,
        }
        for monomial, coefficient in sorted(polynomial.items())
    ]


def without_raw_polynomial(record):
    return {
        key: value for key, value in record.items()
        if key != "obstruction_remainder"
    }


def audit():
    # These comparisons exercise the streaming identity at every degree for
    # which the old ambient computation is known to fit in memory.
    zero_reducer, zero_pure, zero_validation = validate_streamed_projection(
        0, 6
    )
    one_reducer, one_pure, one_validation = validate_streamed_projection(
        1, 5
    )

    one_terminal = one_reducer.terminal_reduce_degree(one_pure, 6)
    require(one_terminal["complete"],
            "H1 degree-six streamed residual did not close")
    require(not one_terminal["obstruction_remainder"],
            "H1 degree-six remainder is nonzero")

    zero_terminal = zero_reducer.terminal_reduce_degree(zero_pure, 7)
    require(not zero_terminal["complete"],
            "H0 degree-seven frontier unexpectedly closed")
    remainder = zero_terminal["obstruction_remainder"]

    # In tangent-parameter indices this is
    # z16^2 z41 (z44+z45) (z53-z51) (z9 z25-z11 z46).
    expected_factorization = multiply_many((
        {(16, 16, 41): QQ(1)},
        {(44,): QQ(1), (45,): QQ(1)},
        {(53,): QQ(1), (51,): QQ(-1)},
        {(9, 25): QQ(1), (11, 46): QQ(-1)},
    ))
    require(remainder == expected_factorization,
            "H0 degree-seven remainder factorization changed")

    # The nine extra elements of the 48-element tangent Groebner basis have
    # these cubic leading monomials.  The remainder is already reduced by the
    # 39 quadrics; check that no cubic lead reduces it either.
    cubic_leads = (
        (20, 46, 46), (19, 46, 46), (18, 46, 46),
        (20, 20, 46), (19, 20, 46), (18, 20, 46),
        (19, 19, 46), (18, 19, 46), (18, 18, 46),
    )
    require(
        all(
            FOURTH.divides(lead, monomial) is None
            for lead in cubic_leads for monomial in remainder
        ),
        "H0 degree-seven remainder is reducible by a cubic tangent lead",
    )

    # Exact coordinate substitutions for the five linear minimal primes of
    # the Ferrers radical.  Unspecified variables remain free.
    branches = {
        "P1": {
            25: {}, 26: {(45,): QQ(1)}, 27: {},
            44: {(45,): QQ(-1)}, 46: {},
        },
        "P2": {
            12: {}, 13: {}, 15: {(16,): QQ(1)}, 18: {}, 19: {},
            25: {}, 26: {(45,): QQ(1)},
            44: {(45,): QQ(-1)}, 46: {},
        },
        "P3": {
            12: {}, 13: {}, 14: {}, 15: {(16,): QQ(1)}, 17: {},
            18: {}, 19: {}, 20: {}, 44: {(45,): QQ(-1)}, 46: {},
        },
        "P4": {
            12: {}, 13: {}, 14: {}, 15: {(16,): QQ(1)}, 17: {},
            18: {}, 19: {}, 20: {}, 21: {}, 22: {},
            44: {(45,): QQ(-1)},
        },
        "P5": {
            12: {}, 13: {}, 14: {}, 15: {(16,): QQ(1)}, 17: {},
            18: {}, 19: {}, 20: {}, 21: {}, 22: {}, 23: {},
        },
    }
    branch_restrictions = {
        name: substitute_linear(remainder, substitutions)
        for name, substitutions in branches.items()
    }
    require(
        [len(branch_restrictions[name]) for name in branches]
        == [0, 0, 0, 0, 8],
        "H0 degree-seven Ferrers branch restrictions changed",
    )
    require(branch_restrictions["P5"] == remainder,
            "P5 should retain the full degree-seven remainder")

    tangent_labels = {
        str(index): "".join(map(str, FACTOR.AMBIENT_COORDINATES[
            zero_reducer.free_columns[index]
        ]))
        for index in sorted({value for monomial in remainder for value in monomial})
    }
    ledger = {
        "arithmetic": "exact Q",
        "ambient_variables": 252,
        "mixed_tangent_variables": 56,
        "streaming_identity": (
            "NF(multiplier*equation)=NF(multiplier)*NF(equation)"
        ),
        "streaming_regressions": {
            "H0": zero_validation,
            "H1": one_validation,
        },
        "H1_degree_six": without_raw_polynomial(one_terminal),
        "H1_conclusion": "H_1 belongs to I_mix + m_p^7",
        "H0_degree_seven": without_raw_polynomial(zero_terminal),
        "H0_remainder": encode_polynomial(remainder),
        "H0_remainder_factorization": (
            "z16^2*z41*(z44+z45)*(z53-z51)*(z9*z25-z11*z46)"
        ),
        "H0_remainder_coordinate_labels": tangent_labels,
        "H0_remainder_cubic_lead_reductions": 0,
        "H0_branch_remainder_terms": {
            name: len(value) for name, value in branch_restrictions.items()
        },
        "frontier": (
            "the first unresolved H0 standard-monomial class vanishes on "
            "P1--P4 and survives on P5; higher mixed initial equations may "
            "still cut P5"
        ),
    }
    return ledger


def main():
    ledger = audit()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen streamed next-order ledger digest changed")
    print(
        "n=8 streamed next orders: PASS; H1 in I_mix+m_p^7; "
        "H0 degree-7 remainder has 8 terms and survives only on P5"
    )
    print(json.dumps(ledger, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
