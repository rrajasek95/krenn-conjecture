#!/usr/bin/env python3
"""Classify the E14 unary S-pairs and audit their first complete reduction.

The private rewrite audit identifies, for every private G11 target term
``endpoint * x*y``, a unary row with a linear pivot p dividing x*y.  Write
that row uniquely as

    U = p*A + B,

where no monomial of B is divisible by p.  This checker classifies all 228
canonical choices, verifies A(0) is nonzero, and verifies every multiplied B
tail has a literal divisor in a complete G11 zero row.

It then constructs the exact first-hit reduction module for the lexicographically
first chart-(1,1) S-pair.  The columns are *all* complete unary and G11 rows,
with target readouts and literal q multipliers, that hit one of the twelve B tails.
The B target is not in their rational span.  Exact echelon reduction returns

    endpoint*u35_11*v24_11*(1-v04_00),

the original private generator times its local unary unit.  A sparse rational
dual (support 16) separates the 245-column first-hit module.  This is the
first exact attaching obstruction; further reduction needs columns entering
through companion coordinates rather than another support face.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REWRITE_PATH = "computations/verify_h3_c6_e14_private_rewrite_spair_boundary.py"
PINS = {
    REWRITE_PATH:
        "d3605323f2a305dbc6c5dec38313ecb55c2f7a5676a255117abe9d0b773889a4",
    "notes/h3-c6-e14-private-rewrite-spair-boundary.md":
        "ac81c307c484dd1470a1ea953a70ee8c00a2e0cf875e31aff7f75f2e25315593",
}
EXPECTED_LEDGER_SHA256 = (
    "fe460881c3e2bb19f7c6679d50a5ea93c98108960c2970dab0fd6557f9b7c773"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(path, name):
    spec = spec_from_file_location(name, ROOT / path)
    require(spec is not None and spec.loader is not None,
            f"cannot load dependency {path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def quotient(dividend, divisor):
    answer = list(dividend)
    for factor in divisor:
        if factor not in answer:
            return None
        answer.remove(factor)
    return tuple(sorted(answer))


def multiply_monomials(left, right):
    return tuple(sorted(left + right))


def canonical_breakers(rewrite, private, unary):
    rules = rewrite.unary_rules(private, unary, (0,) * 6)
    by_source = {}
    for rule in rules:
        if not rule["private_tails"]:
            by_source.setdefault(rule["source"], []).append(rule)
    require(set(by_source) == private,
            "the private unary-breaker cover changed")
    answer = {}
    for source, choices in by_source.items():
        minimum_degree = min(
            choice["maximum_tail_degree"] for choice in choices
        )
        answer[source] = min(
            (choice for choice in choices
             if choice["maximum_tail_degree"] == minimum_degree),
            key=lambda choice: (
                choice["word"], choice["pivot"], choice["multiplier"]
            ),
        )
    return answer


def factor_unary(polynomial, pivot):
    factor = {}
    remainder = {}
    for monomial, coefficient in polynomial.items():
        divided = quotient(monomial, pivot)
        if divided is None:
            remainder[monomial] = coefficient
        else:
            factor[divided] = coefficient
    return factor, remainder


def response_terms(row):
    return tuple(
        (endpoint, monomial, coefficient)
        for endpoint, polynomial in row.items()
        for monomial, coefficient in polynomial.items()
    )


def exact_reduce(vector, pivots):
    vector = {coordinate: Q(coefficient)
              for coordinate, coefficient in vector.items() if coefficient}
    while vector:
        leading = min(vector)
        if leading not in pivots:
            return vector
        factor = vector[leading]
        for coordinate, coefficient in pivots[leading].items():
            new = vector.get(coordinate, Q(0)) - factor * coefficient
            if new:
                vector[coordinate] = new
            elif coordinate in vector:
                del vector[coordinate]
    return {}


def add_exact_column(vector, pivots):
    vector = exact_reduce(vector, pivots)
    if not vector:
        return False
    leading = min(vector)
    coefficient = vector[leading]
    pivots[leading] = {
        coordinate: value / coefficient
        for coordinate, value in vector.items()
    }
    return True


def specialize_vector(vector, variable, value):
    """Specialize one q coordinate in an endpoint/readout vector."""
    answer = defaultdict(Q)
    for (grade, monomial), coefficient in vector.items():
        exponent = monomial.count(variable)
        specialized = tuple(item for item in monomial if item != variable)
        answer[(grade, specialized)] += coefficient * Q(value) ** exponent
    return {coordinate: coefficient
            for coordinate, coefficient in answer.items() if coefficient}


def first_hit_module(responses, unary):
    endpoint = ("p1_0_1", "s1_1_1")
    pivot = ("u35_11",)
    multiplier = ("v2411",)
    word = (0, 0, 0, 1, 0, 1)
    factor, remainder = factor_unary(unary[word], pivot)
    require(factor == {(): Q(-1), ("v0400",): Q(1)},
            f"the canonical unary unit factor changed: {factor}")
    require(len(remainder) == 12,
            "the canonical unary remainder stopped having twelve tails")

    target = {
        (endpoint, multiply_monomials(monomial, multiplier)): coefficient
        for monomial, coefficient in remainder.items()
    }
    response_rows = [
        (output_word, response_terms(row))
        for output_word, row in responses.items()
    ]
    unary_rows = [
        (output_word, tuple(polynomial.items()))
        for output_word, polynomial in unary.items()
    ]

    columns = {}
    for target_endpoint, target_monomial in target:
        for row_index, (output_word, row) in enumerate(response_rows):
            for row_endpoint, row_monomial, _coefficient in row:
                if row_endpoint != target_endpoint:
                    continue
                row_multiplier = quotient(target_monomial, row_monomial)
                if row_multiplier is None:
                    continue
                column = {
                    (output_endpoint,
                     multiply_monomials(output_monomial, row_multiplier)):
                        output_coefficient
                    for output_endpoint, output_monomial, output_coefficient
                    in row
                }
                if output_word == (1,) * 6:
                    column[(
                        ("target_G11",), row_multiplier
                    )] = Q(-1)
                columns[("G11", row_index, row_multiplier)] = column
        for row_index, (output_word, row) in enumerate(unary_rows):
            for row_monomial, _coefficient in row:
                row_multiplier = quotient(target_monomial, row_monomial)
                if row_multiplier is None:
                    continue
                column = {
                    (target_endpoint,
                     multiply_monomials(output_monomial, row_multiplier)):
                        output_coefficient
                    for output_monomial, output_coefficient in row
                }
                if output_word == (0,) * 6:
                    column[(
                        ("target_unary",) + target_endpoint,
                        row_multiplier,
                    )] = Q(-1)
                columns[("unary", row_index, target_endpoint,
                         row_multiplier)] = column

    pivots = {}
    for column in columns.values():
        add_exact_column(column, pivots)
    reduced = exact_reduce(target, pivots)
    expected_reduced = {
        (endpoint, ("u35_11", "v2411")): Q(1),
        (endpoint, ("u35_11", "v0400", "v2411")): Q(-1),
    }
    require(reduced == expected_reduced,
            f"the first S-pair residual changed: {reduced}")

    # The first free coordinate of the remainder gives a deterministic
    # rational dual.  Back substitution evaluates pivot coordinates so that
    # every echelon column pairs to zero.
    free = min(reduced)
    dual = {free: Q(1)}
    for leading in sorted(pivots, reverse=True):
        value = sum(
            coefficient * dual.get(coordinate, Q(0))
            for coordinate, coefficient in pivots[leading].items()
            if coordinate != leading
        )
        if value:
            dual[leading] = -value
    for column in columns.values():
        require(sum(coefficient * dual.get(coordinate, Q(0))
                    for coordinate, coefficient in column.items()) == 0,
                "the first-hit dual stopped killing a source column")
    pairing = sum(coefficient * dual.get(coordinate, Q(0))
                  for coordinate, coefficient in target.items())
    require(pairing == -1,
            f"the first-hit dual pairing changed: {pairing}")
    denominator = 1
    for value in dual.values():
        denominator = math.lcm(denominator, value.denominator)
    integral_values = [int(value * denominator) for value in dual.values()]
    content = 0
    for value in integral_values:
        content = math.gcd(content, abs(value))
    integral_pairing = pairing * denominator / content
    require(integral_pairing == -30,
            f"the primitive integral first-hit pairing changed: "
            f"{integral_pairing}, denominator={denominator}, "
            f"content={content}, support={len(dual)}")

    private_target = {
        (endpoint, ("u35_11", "v2411")): Q(1)
    }
    specializations = {}
    for value, expected_rank in ((0, 224), (1, 257)):
        specialized_pivots = {}
        for column in columns.values():
            add_exact_column(
                specialize_vector(column, "v0400", value),
                specialized_pivots,
            )
        specialized_B = exact_reduce(
            specialize_vector(target, "v0400", value),
            specialized_pivots,
        )
        specialized_private = exact_reduce(
            specialize_vector(private_target, "v0400", value),
            specialized_pivots,
        )
        require(len(specialized_pivots) == expected_rank,
                f"the v04={value} first-hit rank changed")
        require(bool(specialized_private),
                f"the private generator vanished at v04={value}")
        if value == 0:
            require(specialized_B == specialized_private,
                    "the chordless specialization lost B=private")
        else:
            require(not specialized_B,
                    "the singular-return specialization did not kill B")
        specializations[str(value)] = {
            "rank_Q": len(specialized_pivots),
            "B_remainder_support": len(specialized_B),
            "private_remainder_support": len(specialized_private),
            "B_equals_private_remainder":
                specialized_B == specialized_private,
        }

    coordinates = set(target)
    for column in columns.values():
        coordinates.update(column)
    return {
        "chart": [1, 1],
        "endpoint": list(endpoint),
        "private_monomial": ["u35_11", "v2411"],
        "unary_word": "000101",
        "unary_pivot": list(pivot),
        "unary_unit_factor": [
            [list(monomial), str(coefficient)]
            for monomial, coefficient in sorted(factor.items())
        ],
        "B_tail_count": len(target),
        "target_augmented_first_hit_column_count": len(columns),
        "first_hit_coordinate_count": len(coordinates),
        "target_augmented_first_hit_rank_Q": len(pivots),
        "reduced_target": [
            [list(coordinate[0]), list(coordinate[1]), str(coefficient)]
            for coordinate, coefficient in sorted(reduced.items())
        ],
        "rational_dual_support": len(dual),
        "rational_dual_pairing": str(pairing),
        "primitive_integral_dual_pairing": str(integral_pairing),
        "v04_specializations": specializations,
    }


def audit():
    pin_dependencies()
    rewrite = load(REWRITE_PATH, "e14_spair_rewrite")
    top = rewrite.load(rewrite.TOP_PATH, "e14_spair_top")
    two = top.load(top.TWO_CELL_PATH, "e14_spair_two")
    e14 = two.load(two.E14_PATH, "e14_spair_base")
    b4 = e14.load(e14.B4_PATH, "e14_spair_b4")

    word_orbits = Counter()
    factor_types = Counter()
    normalized_return_factors = Counter()
    tail_divisor_types = Counter()
    canonical_count = 0
    canonical_chart = None

    for first_index in (1, 2, 3):
        for second_index in (1, 2, 3):
            _candidates, _names, responses, unary = two.universal(
                e14, b4, first_index, second_index
            )
            target_terms = set(rewrite.row_terms(responses[(1,) * 6]))
            zero_rows = {
                word: rewrite.row_terms(row)
                for word, row in responses.items() if word != (1,) * 6
            }
            zero_terms = set().union(*(set(row) for row in zero_rows.values()))
            private = target_terms - zero_terms
            nonprivate_target = target_terms & zero_terms
            breakers = canonical_breakers(rewrite, private, unary)
            canonical_count += len(breakers)

            for source, breaker in breakers.items():
                factor, remainder = factor_unary(
                    unary[breaker["word"]], breaker["pivot"]
                )
                require(factor.get((), Q(0)) != 0,
                        "a unary pivot factor lost its local unit")
                require(min(map(len, remainder)) == 2,
                        "a unary nonpivot remainder gained a linear term")
                factor_types[(
                    tuple(sorted(map(len, factor))),
                    tuple(sorted(map(len, remainder))),
                )] += 1
                constant = factor[()]
                normalized_return_factors[tuple(sorted(
                    (monomial, coefficient / constant)
                    for monomial, coefficient in factor.items()
                ))] += 1
                word_orbits[(
                    "".join(map(str, breaker["word"])),
                    breaker["maximum_tail_degree"],
                )] += 1

                endpoint, _private_monomial = source
                for monomial in remainder:
                    tail = multiply_monomials(
                        monomial, breaker["multiplier"]
                    )
                    if any(
                        candidate_endpoint == endpoint
                        and quotient(tail, candidate_monomial) is not None
                        for candidate_endpoint, candidate_monomial
                        in nonprivate_target
                    ):
                        tail_divisor_types["nonprivate_target_G11"] += 1
                    elif any(
                        candidate_endpoint == endpoint
                        and quotient(tail, candidate_monomial) is not None
                        for candidate_endpoint, candidate_monomial in zero_terms
                    ):
                        tail_divisor_types["other_complete_G11_zero"] += 1
                    else:
                        raise RuntimeError(
                            f"unfactored unary S-pair tail: "
                            f"{(first_index, second_index)}, {source}, {tail}"
                        )

            if (first_index, second_index) == (1, 1):
                canonical_chart = first_hit_module(responses, unary)

    require(canonical_count == 228,
            f"the canonical S-pair count changed: {canonical_count}")
    require(word_orbits == Counter({
        ("001001", 4): 48,
        ("000101", 4): 36,
        ("000011", 4): 36,
        ("001010", 4): 24,
        ("001100", 4): 24,
        ("010001", 4): 18,
        ("011000", 4): 18,
        ("010010", 3): 12,
        ("100100", 3): 12,
    }), f"the nine unary-word orbits changed: {word_orbits}")
    require(factor_types == Counter({
        ((0, 1), (2,) * 10 + (3,) * 2): 156,
        ((0, 2), (2,) * 8 + (3,) * 4): 48,
        ((0,), (2,) * 12): 24,
    }), f"the unary factor types changed: {factor_types}")
    require(normalized_return_factors == Counter({
        (((), Q(1)),): 24,
        (((), Q(1)), (("v0400",), Q(-1))): 54,
        (((), Q(1)), (("v0400",), Q(-1, 5))): 24,
        (((), Q(1)), (("v0400",), Q(1, 3))): 18,
        (((), Q(1)), (("v0400", "v1300"), Q(-1, 7))): 48,
        (((), Q(1)), (("v1300",), Q(-1))): 24,
        (((), Q(1)), (("v1300",), Q(1, 3))): 36,
    }), f"the normalized return factors changed: "
        f"{normalized_return_factors}")
    require(tail_divisor_types == Counter({
        "other_complete_G11_zero": 2304,
        "nonprivate_target_G11": 432,
    }), f"the S-pair tail divisor split changed: {tail_divisor_types}")
    require(canonical_chart is not None, "the canonical chart was not audited")

    ledger = {
        "pins": PINS,
        "canonical_S_pair_count": canonical_count,
        "unary_word_orbits": [
            {"word": word, "maximum_tail_degree": degree, "count": count}
            for (word, degree), count in sorted(word_orbits.items())
        ],
        "factor_types": [
            {
                "A_quotient_degrees": list(a_degrees),
                "B_monomial_degrees": list(b_degrees),
                "count": count,
            }
            for (a_degrees, b_degrees), count in sorted(factor_types.items())
        ],
        "normalized_return_factors": [
            {
                "factor": [
                    [list(monomial), str(coefficient)]
                    for monomial, coefficient in factor
                ],
                "count": count,
            }
            for factor, count in sorted(normalized_return_factors.items())
        ],
        "multiplied_B_tail_count": sum(tail_divisor_types.values()),
        "tail_divisor_types": dict(sorted(tail_divisor_types.items())),
        "canonical_first_reduction": canonical_chart,
        "theorem": (
            "all 228 private cycle-breakers fall into nine unary-word orbits "
            "and three factorizations U=p*A+B with A(0) nonzero; every one "
            "of the 2,736 multiplied B tails has a literal complete-G11-zero "
            "divisor"
        ),
        "first_obstruction": (
            "for the canonical chart-(1,1) S-pair, all 269 target-augmented "
            "complete unary/G11 columns that directly hit its twelve B tails "
            "have rational rank 269, but B has nonzero cokernel and reduces "
            "exactly to the "
            "original private generator times (1-v04_00)"
        ),
        "next_attachment": (
            "a source column entering through the first-hit companion "
            "coordinates (equivalently the next Buchberger/endpoint-word-"
            "change layer); another internal support face cannot remove the "
            "displayed primitive first-hit dual"
        ),
        "physical_return_split": (
            "the only return coordinates are v04_00 and v13_00, the two "
            "missing physical chord tables of the silent C6.  On the strict "
            "chordless branch both are zero, so every normalized A is 1. "
            "Every nonconstant singular locus forces at least one of those "
            "chords nonzero and therefore exits to the crossed C4 response "
            "landing.  Algebraically A=0 kills B but not the private "
            "generator, while A invertible identifies B with that generator"
        ),
        "scope": (
            "classification is universal over the nine minimal E14 charts. "
            "The exact cokernel is the first-hit reduction module of one "
            "canonical orbit representative; it is not a completed Groebner "
            "calculation, arbitrary-support emptiness, or a full-source "
            "counterexample.  G22 endpoint-star columns are grade-separated "
            "from this p1/s1 private module"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"unary S-pair ledger changed: {digest}")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h3 C6 E14 unary S-pair first reduction: PASS (exact)")
    print(f"S_pairs={ledger['canonical_S_pair_count']}")
    print(f"B_tails={ledger['multiplied_B_tail_count']}")
    canonical = ledger["canonical_first_reduction"]
    print("canonical_first_hit="
          f"{canonical['target_augmented_first_hit_rank_Q']}/"
          f"{canonical['target_augmented_first_hit_column_count']}, "
          f"dual_pairing={canonical['rational_dual_pairing']}")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
